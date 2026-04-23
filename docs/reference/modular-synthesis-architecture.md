# Reference: Modular Synthesis Multi-Agent Architecture

**Source Atom:** `prompt-1dd4e88daf85`
**Origin:** ChatGPT thread "Swarm of AI" (2025-08-28)
**Type:** Architecture synthesis document
**Ingested:** 2026-04-23

---

## Summary

This document captures the 9-recommendation architecture proposed in the "Swarm of AI" ChatGPT thread, which synthesized multi-agent AI system design through the lens of modular synthesis (oscillator/filter/patch-cable metaphors). The original prompt explored how concepts from analog synthesizer design -- where specialized modules (oscillators, filters, envelopes, VCAs) are composed via patch cables into arbitrary signal chains -- could inform the architecture of multi-agent AI systems.

---

## The 9 Recommendations

### 1. Agents as Specialized Modules (Oscillator/Filter Metaphor)

Each agent functions as a specialized signal-processing module analogous to components in a modular synthesizer:

- **Oscillators** (generators): Agents that produce raw output -- researchers, content generators, code writers. They create the fundamental signal.
- **Filters** (transformers): Agents that refine, review, or constrain output -- reviewers, editors, security scanners. They shape the signal.
- **Envelopes** (controllers): Agents that modulate other agents' behavior over time -- orchestrators, schedulers, budget managers. They control the amplitude and timing.
- **Mixers** (combiners): Agents that merge multiple outputs -- synthesizers, consensus builders, report assemblers. They blend signals.

The key insight: modules should be maximally specialized and minimally coupled. Each module has a defined input interface and output interface. Composition happens externally via patching, not internally via shared state.

### 2. Orchestration as Patching (DAG + Cycles)

Agent composition should follow the modular synthesis patching model:

- **Patch cables** = directed edges in a computation graph
- **DAGs** handle feed-forward workflows (research -> synthesis -> review -> publish)
- **Cycles** handle iterative refinement (generate -> test -> feedback -> regenerate)
- **Self-patching** = agents that modify the graph topology during execution
- **LangGraph** cited as the closest implementation of this pattern in the AI agent ecosystem

The patching metaphor separates the "what agents do" (module definition) from "how agents connect" (topology definition). This separation enables runtime reconfiguration without modifying agent code.

### 3. Blackboard Pattern for Shared State

A blackboard architecture provides shared state without direct agent-to-agent coupling:

- **Hot tier (Redis):** Active session state, real-time coordination signals, pub/sub event channels. Sub-millisecond reads. Ephemeral.
- **Cold tier (PostgreSQL):** Audit logs, decision history, accumulated knowledge. Durable. Queryable. Compliance-ready.

Agents write findings and read context from the blackboard rather than passing messages directly. This decouples agent execution order from data flow and enables late-joining agents to catch up on accumulated state.

### 4. Hierarchical + Decentralized Collaboration

The architecture should support both organizational models simultaneously:

- **Hierarchical mode:** A coordinator agent delegates subtasks to specialist agents, collects results, and synthesizes. Appropriate for well-structured tasks with clear decomposition.
- **Decentralized mode:** Agents operate autonomously, sharing findings through the blackboard. No central coordinator. Appropriate for exploration, brainstorming, and tasks where the structure is unknown in advance.
- **Hybrid transitions:** The system should switch between hierarchical and decentralized modes based on task characteristics. Exploration phases benefit from decentralization; synthesis phases benefit from hierarchy.

### 5. Budget-Aware Scheduling (CFO Agent)

A dedicated budget management agent (the "CFO") enforces cost discipline:

- Tracks per-agent, per-session, and per-workflow API costs
- Maintains pricing tables for all LLM providers
- Estimates cost before authorizing LLM calls
- Enforces budget thresholds with configurable actions (warn, throttle, block)
- Reports cost-per-feature and cost-per-agent metrics
- Routes tasks to cheaper models/providers when budget is constrained

The CFO operates as both an agent (capable of reasoning about cost optimization) and an infrastructure layer (enforcing hard limits regardless of agent intent).

### 6. Secure Code Execution Sandboxing

When agents generate and execute code, the execution environment must be sandboxed:

- Process-level isolation (minimum): separate processes with restricted filesystem access
- Container-level isolation (standard): Docker containers with resource limits, network restrictions, read-only filesystems
- VM-level isolation (maximum): lightweight VMs (Firecracker, gVisor) for untrusted code execution
- Runtime selection based on trust level: trusted agents get process isolation; untrusted agents get VM isolation

The sandboxing layer should be transparent to the agent -- the same agent code runs in any isolation tier. The runtime selector chooses the appropriate tier based on the agent's trust level, the task's risk classification, and the execution environment's capabilities.

### 7. HITL Workflows for High-Stakes Actions

Human-in-the-loop approval gates prevent autonomous execution of high-consequence actions:

- **Risk classification:** Every agent action is classified as low/medium/high risk before execution
- **Auto-approve:** Low-risk actions execute immediately (reading files, querying APIs, generating text)
- **Notify-and-proceed:** Medium-risk actions execute but notify the human (modifying files, sending messages)
- **Block-until-approved:** High-risk actions halt until a human explicitly approves (deploying code, spending money, deleting data, external communications)
- **Approval channels:** WebSocket for real-time dashboards, email/Slack for async workflows, CLI prompts for interactive sessions

HITL is structural, not optional. The absence of HITL gates makes multi-agent systems unusable for any task with real-world consequences.

### 8. Observability Pipeline for RLHF

Every agent interaction should be instrumented for reinforcement learning from human feedback:

- **Capture:** Log every LLM call with full context (prompt, response, model, latency, cost, tool calls)
- **Annotate:** Human reviewers label interactions as helpful/unhelpful, correct/incorrect, safe/unsafe
- **Aggregate:** Build preference datasets from annotated interactions
- **Train:** Use preference data to fine-tune local models (DPO, RLHF) or refine prompt templates
- **Deploy:** Updated models/prompts feed back into the agent system
- **Measure:** Track quality metrics (acceptance rate, retry rate, self-correction count) to validate improvement

The observability pipeline should be append-only, immutable, and queryable. It serves dual purposes: operational monitoring (is the system working?) and learning (is the system improving?).

### 9. Comprehensive Agentic Test Suite

Multi-agent systems require testing at multiple levels:

- **Unit tests:** Individual agent behavior given specific inputs
- **Integration tests:** Agent-to-agent communication, blackboard reads/writes, tool invocations
- **Topology tests:** Correct behavior across all supported coordination patterns
- **Adversarial tests:** Agent robustness against malicious inputs, prompt injection, resource exhaustion
- **Chaos tests:** System behavior under failure conditions (agent crashes, network partitions, provider outages)
- **End-to-end tests:** Full workflow execution from task input to final output
- **Performance tests:** Latency, throughput, and cost under load
- **Safety tests:** HITL gates trigger correctly, RBAC enforces correctly, budget limits hold

The test suite is not optional infrastructure -- it is a structural requirement that validates the compositional guarantees the modular architecture claims to provide.

---

## Cross-Reference to ORGANVM

This atom was evaluated against the current ORGANVM implementation on 2026-04-23. The gap analysis is at:

`~/Workspace/meta-organvm/organvm-corpvs-testamentvm/data/atoms/multi-agent-architecture-gap-analysis.md`

**Key finding:** 8 of 9 recommendations are fully or substantially implemented in agentic-titan. The primary gap is closing the RLHF feedback loop (recommendation 8) -- the observability infrastructure exists but does not yet feed back into systematic behavior modification.

---

## Provenance

- **Thread:** "Swarm of AI" (ChatGPT, 2025-08-28)
- **Atom ID:** `prompt-1dd4e88daf85`
- **Priority:** P0
- **Domain:** architecture, multi-agent, orchestration
- **Tags:** `modular-synthesis`, `multi-agent`, `DAG`, `blackboard`, `RLHF`, `sandboxing`, `HITL`, `budget`, `testing`
