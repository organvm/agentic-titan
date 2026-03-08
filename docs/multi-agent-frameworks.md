# F-28: Multi-Agent Orchestration Frameworks

> Evaluation of 4 frameworks for integration with agentic-titan's existing topology engine.

## Evaluation Criteria

Each framework is evaluated against titan's existing 9 topology patterns:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Topology alignment | High | How well does it map to titan's existing patterns? |
| Model agnosticism | High | Does it support Ollama, Anthropic, OpenAI, Groq? |
| Composability | Medium | Can individual components be adopted without full buy-in? |
| Community/maturity | Medium | Size of ecosystem, release cadence, bus factor |
| Overhead | Low | Additional dependencies, runtime cost |

## LangGraph

**Graph-based agent workflows with complex routing.**

### Installation

```bash
uv venv .venv-langgraph && source .venv-langgraph/bin/activate
uv pip install langgraph langchain-core
```

### Strengths

- Explicit graph definition (nodes + edges) aligns with titan's DAG workflow engine
- Conditional routing and cycles supported natively
- Checkpointing and state persistence built in
- Strong community and documentation

### Weaknesses

- Heavy dependency on LangChain ecosystem (langchain-core required)
- Opinionated state management may conflict with titan's Redis/ChromaDB hive
- Vendor lock-in risk through LangSmith observability integration
- Graph definition syntax is verbose compared to titan's YAML DSL

### Integration Pattern

Adopt LangGraph's **conditional edge routing** as a pattern in titan's topology engine without importing the library. Titan already has DAG execution; the value is in LangGraph's routing logic patterns (retry, fallback, human-in-the-loop branching).

```python
# Pattern adoption, not library import
class ConditionalRouter:
    """LangGraph-inspired conditional routing for titan topologies."""
    def route(self, state: AgentState) -> str:
        if state.confidence < 0.7:
            return "human_review"
        return "next_stage"
```

## AutoGen

**Microsoft's multi-agent conversation framework.**

### Installation

```bash
uv venv .venv-autogen && source .venv-autogen/bin/activate
uv pip install autogen-agentchat autogen-ext
```

### Strengths

- First-class multi-agent conversation with turn-taking
- GroupChat pattern handles agent coordination naturally
- Code execution sandbox built in
- Strong backing from Microsoft Research

### Weaknesses

- Conversation-centric model is a poor fit for titan's task-oriented topologies
- Heavy abstraction layer adds complexity without clear benefit for structured workflows
- AutoGen v0.4 is a breaking rewrite; ecosystem fragmentation
- Default OpenAI dependency requires explicit configuration for other providers

### Integration Pattern

Adopt AutoGen's **GroupChat turn-taking protocol** for titan's debate/review topologies where multiple agents need structured conversation. Do not adopt the framework wholesale.

```python
# Pattern adoption
class TurnTakingProtocol:
    """AutoGen-inspired turn management for multi-agent debate topology."""
    def next_speaker(self, history: list[Turn], agents: list[Agent]) -> Agent:
        # Round-robin with early termination on consensus
        ...
```

## CrewAI

**Role-based agent teams with task delegation.**

### Installation

```bash
uv venv .venv-crewai && source .venv-crewai/bin/activate
uv pip install crewai crewai-tools
```

### Strengths

- Role-based agent definition maps to titan's 22 agent archetypes
- Task delegation with expected output specification
- Sequential and hierarchical process types
- Simple API, fast prototyping

### Weaknesses

- Limited topology options (sequential, hierarchical only — titan has 9)
- Tight coupling to LangChain under the hood
- No native support for custom state backends
- Delegation logic is opaque and hard to debug

### Integration Pattern

Adopt CrewAI's **role + goal + backstory** agent definition pattern as an alternative DSL for titan's Agent Forge YAML specs. The role-based framing is useful for prompt engineering.

```yaml
# CrewAI-inspired agent definition for titan
archetype: code-reviewer
role: "Senior code reviewer with security expertise"
goal: "Find bugs, security issues, and style violations"
backstory: "10 years of experience in Python and TypeScript codebases"
```

## SmolAgents

**Hugging Face lightweight agents.**

### Installation

```bash
uv venv .venv-smolagents && source .venv-smolagents/bin/activate
uv pip install smolagents
```

### Strengths

- Minimal footprint — single package, few dependencies
- Code-first approach (agents write and execute code directly)
- Native Hugging Face Hub integration for model selection
- Good for simple tool-use agents

### Weaknesses

- Single-agent focused — no native multi-agent orchestration
- Limited state management (no persistence, no shared memory)
- Early stage, small community
- Code execution model has security implications

### Integration Pattern

Adopt SmolAgents' **code-as-action** pattern for titan agents that need to generate and execute code. Useful for data analysis and transformation tasks.

```python
# Pattern adoption
class CodeActionAgent:
    """SmolAgents-inspired code execution for titan."""
    def act(self, task: str) -> str:
        code = self.generate_code(task)
        result = self.sandbox_execute(code)  # titan's existing sandbox
        return result
```

## Comparison Matrix

| Feature | LangGraph | AutoGen | CrewAI | SmolAgents | Titan (current) |
|---------|-----------|---------|--------|------------|-----------------|
| Topologies | Graph (flexible) | Conversation | 2 (seq, hier) | 1 (single) | 9 patterns |
| State backend | Checkpointer | In-memory | In-memory | None | Redis + ChromaDB |
| Model support | Via LangChain | OpenAI default | Via LangChain | HF Hub | Ollama/Anthropic/OpenAI/Groq |
| Multi-agent | Yes | Yes (GroupChat) | Yes (Crew) | No | Yes (Hive Mind) |
| YAML DSL | No | No | Partial | No | Yes (Agent Forge) |
| License | MIT | CC-BY-4.0 | MIT | Apache 2.0 | Proprietary |

## Recommendation

**Adopt patterns, not frameworks.** Titan's existing topology engine and Hive Mind state layer are more capable than any single framework. The recommended approach:

1. **From LangGraph**: Conditional edge routing patterns for dynamic topology decisions
2. **From AutoGen**: Turn-taking protocol for debate/review topologies
3. **From CrewAI**: Role + goal + backstory agent definition format for Agent Forge
4. **From SmolAgents**: Code-as-action execution pattern for data transformation agents

No framework should be added as a runtime dependency. Each pattern is implemented natively in titan's existing architecture.

## Reference

- `titan/topology_engine.py` — 9 topology patterns
- `agents/` — 22 agent archetypes
- `adapters/` — LLM adapter layer (Ollama, Anthropic, OpenAI, Groq)
- `hive/` — Redis state, ChromaDB vectors, pub/sub events
