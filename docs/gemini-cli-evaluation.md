# F-69: Gemini CLI Evaluation

> Evaluation of Google Gemini CLI for integration into the ORGANVM agent ecosystem.

## Overview

Google's Gemini CLI provides terminal-based access to Gemini models with built-in web grounding. The free tier makes it an attractive option for high-volume, lower-stakes tasks where web search integration adds value.

## Installation

```bash
# npm (global)
npm install -g @anthropic-ai/gemini-cli  # placeholder — actual package TBD

# Or via Google's distribution
# Check https://ai.google.dev/gemini-api/docs/cli for current install method
```

## Evaluation Matrix

### Strengths

| Strength | Detail |
|----------|--------|
| Web grounding | Native web search integration — can verify facts against live sources |
| Free tier | Generous free usage tier reduces cost for bulk operations |
| Multimodal | Image, audio, and video input support |
| Context window | Large context window (1M+ tokens on some models) |
| Speed | Fast inference on lighter models |

### Weaknesses

| Weakness | Detail |
|----------|--------|
| Quality variance | Output quality varies significantly between prompts |
| Less structured output | JSON/YAML generation less reliable than Claude or GPT-4 |
| Limited tool use | Function calling less mature than Anthropic/OpenAI |
| Safety filtering | Aggressive content filtering can block legitimate technical content |
| API stability | Breaking changes between model versions |

## Adapter Integration

If evaluation passes quality bar, add `GeminiAdapter` to the adapters layer:

```python
# adapters/gemini.py
from adapters.base import BaseAdapter

class GeminiAdapter(BaseAdapter):
    """Adapter for Google Gemini models."""

    provider = "gemini"
    supported_models = [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
    ]

    def __init__(self, api_key: str | None = None):  # allow-secret
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")  # allow-secret

    async def generate(self, prompt: str, **kwargs) -> str:
        ...

    async def generate_structured(self, prompt: str, schema: dict) -> dict:
        # Gemini's structured output is less reliable — add validation layer
        ...
```

### Quality Bar Criteria

The adapter is added only if Gemini passes these thresholds on a standard evaluation suite:

| Criterion | Threshold | Test |
|-----------|-----------|------|
| Code generation accuracy | >= 70% pass rate | Run 50 coding tasks, measure test pass rate |
| Structured output validity | >= 85% valid JSON | Generate 100 JSON outputs, validate against schema |
| Instruction following | >= 75% compliance | 50 tasks with specific format requirements |
| Factual accuracy (with grounding) | >= 90% | 30 fact-check queries with web grounding enabled |

## Comparison with Existing Tools

| Capability | claude-code | codex | aider | gemini-cli |
|-----------|------------|-------|-------|------------|
| Code generation quality | Best | Good (bulk) | Good (git) | Variable |
| Structured output | Excellent | Good | Good | Fair |
| Web search | No | No | No | Yes (native) |
| Cost (heavy use) | $$$ | $$ | $$ (BYO key) | Free tier |
| Tool use / MCP | Excellent | Limited | No | Limited |
| Local model support | No | No | Yes (Ollama) | No |
| Git integration | Good | Basic | Best | Basic |

### Recommended Role in Ecosystem

| Task Type | Recommended Tool |
|-----------|-----------------|
| Complex code generation | claude-code |
| Bulk file operations | codex |
| Git-integrated editing | aider |
| Web-grounded research | gemini-cli |
| Local/offline work | aider + Ollama |

Gemini CLI fills the **web-grounded research** niche that no other tool in the ecosystem currently covers. It should not replace claude-code or aider for code generation.

## Evaluation Protocol

1. Install and configure Gemini CLI
2. Run standard evaluation suite (50 coding tasks, 100 structured outputs, 30 fact-checks)
3. Record results in `docs/source-materials/evaluations/gemini-cli-results.json`
4. If thresholds met, implement `GeminiAdapter` in `adapters/gemini.py`
5. Add to adapter router with appropriate task-type routing rules

## Reference

- `adapters/base.py` — Base adapter interface for all LLM providers
- `adapters/router.py` — Task-type routing logic
- F-75 (Agent config audit) — Ecosystem-wide agent configuration review
