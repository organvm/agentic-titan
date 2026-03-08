# F-77: OpenCode Evaluation

> Evaluation of OpenCode (Go, MIT license, multi-provider) for the ORGANVM agent ecosystem.

## Overview

OpenCode is a terminal-based AI coding assistant written in Go. Its key differentiators are speed (compiled Go binary), MIT licensing, and multi-provider support out of the box. It targets the same niche as claude-code and aider but with a focus on minimal footprint and fast startup.

**Repository**: https://github.com/opencode-ai/opencode
**License**: MIT
**Language**: Go

## Installation

```bash
# Go install
go install github.com/opencode-ai/opencode@latest

# Or download binary from releases
# https://github.com/opencode-ai/opencode/releases
```

## Evaluation Matrix

### Strengths

| Strength | Detail |
|----------|--------|
| Speed | Go binary — sub-second startup, low memory footprint |
| MIT license | No usage restrictions, can embed or fork freely |
| Multi-provider | Supports OpenAI, Anthropic, Ollama, and others |
| TUI | Rich terminal UI with file tree, diff view, conversation history |
| Configuration | TOML-based config, easy to version control |

### Weaknesses

| Weakness | Detail |
|----------|--------|
| Early stage | Pre-1.0, API surface may change |
| Small community | Limited ecosystem of plugins/extensions |
| Limited plugin system | No extension mechanism comparable to MCP or goose extensions |
| Tool use | Basic tool support; not on par with claude-code's MCP integration |
| Documentation | Sparse docs, relies on README and source code |

## Adapter Integration

If evaluation shows sufficient quality, OpenCode could be integrated as an adapter:

```python
# adapters/opencode.py
from adapters.base import BaseAdapter

class OpenCodeAdapter(BaseAdapter):
    """Adapter for OpenCode CLI as a subprocess-based agent."""

    provider = "opencode"

    async def generate(self, prompt: str, **kwargs) -> str:
        # Invoke opencode CLI as subprocess with JSON pipe mode
        proc = await asyncio.create_subprocess_exec(
            "opencode", "--pipe", "--model", self.model,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate(prompt.encode())
        return stdout.decode()
```

### Quality Bar Criteria

| Criterion | Threshold | Test |
|-----------|-----------|------|
| Code generation accuracy | >= 65% pass rate | 50 coding tasks |
| Response latency (p95) | < 5s for simple prompts | 100 timed requests |
| Provider switching | All 3 major providers work | Anthropic, OpenAI, Ollama |
| Stability | No crashes in 100 invocations | Automated stress test |

## Comparison with Existing Tools

| Capability | claude-code | aider | opencode | codex |
|-----------|------------|-------|----------|-------|
| Language | TypeScript | Python | Go | Python |
| License | Proprietary | Apache 2.0 | MIT | Proprietary |
| Startup time | ~2s | ~3s | <1s | ~2s |
| Memory usage | ~200MB | ~150MB | ~50MB | ~200MB |
| MCP support | Full | None | None | Limited |
| Multi-provider | Anthropic only | Many | Many | OpenAI only |
| Git integration | Good | Best | Basic | Basic |
| Plugin system | MCP servers | None | None | None |

## Verdict

OpenCode is worth monitoring but not ready for production integration:

- **Speed advantage** is real but not critical for agent workflows where LLM latency dominates
- **MIT license** is attractive for embedding in custom tooling
- **Limited plugin/tool system** is the primary blocker — titan needs rich tool support
- **Early stage** means API instability risk

### Recommendation

- Add to watchlist for quarterly re-evaluation
- Consider as a lightweight subprocess agent for simple, speed-critical tasks
- Do not invest in a full adapter until plugin/tool support matures

## Reference

- F-75 (Agent config audit) — Ecosystem-wide tool inventory
- `adapters/base.py` — Base adapter interface
- `docs/aider-evaluation.md` — Comparable evaluation for aider
