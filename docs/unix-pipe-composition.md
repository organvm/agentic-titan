# F-76: Unix Pipe Composition for Agent I/O

> Enable `agent-a | agent-b | agent-c` composition pattern with stdin/stdout JSON streaming.

## Problem

Agents are currently invoked through titan's internal topology engine, which requires Python-level integration. There is no way to compose agents from the command line or integrate with non-Python tools. Unix pipe composition enables language-agnostic, testable agent chains.

## Design

### Interface Contract

Each agent reads JSON from stdin and writes JSON to stdout. Stderr is reserved for logging.

```
stdin (JSON) → [Agent Process] → stdout (JSON)
                    │
                    └→ stderr (logs)
```

### Message Schema

```json
{
  "type": "message",
  "content": "Review this code for security issues",
  "metadata": {
    "session_id": "sess_abc123",
    "source_agent": "code-analyzer",
    "timestamp": "2026-03-08T10:00:00Z",
    "trace_id": "tr_def456"
  }
}
```

### Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `message` | Input/Output | Text content for processing |
| `tool_call` | Output | Agent requests a tool execution |
| `tool_result` | Input | Result of a tool execution |
| `result` | Output | Final output of the agent |
| `error` | Output | Agent encountered an error |

### Streaming Protocol

For long-running agents, output is newline-delimited JSON (NDJSON):

```
{"type": "message", "content": "Analyzing file 1/10...", "metadata": {...}}
{"type": "message", "content": "Found 3 issues in auth.py", "metadata": {...}}
{"type": "result", "content": "Analysis complete: 7 issues found", "metadata": {...}}
```

## Composition Examples

### Simple Chain

```bash
# Analyze code, then review the analysis, then format as markdown
echo '{"type":"message","content":"Review auth.py"}' \
  | titan agent run code-analyzer \
  | titan agent run code-reviewer \
  | titan agent run markdown-formatter > report.md
```

### Fan-Out / Fan-In

```bash
# Send to multiple reviewers, merge results
echo '{"type":"message","content":"Review auth.py"}' \
  | tee >(titan agent run security-reviewer > /tmp/security.json) \
        >(titan agent run style-reviewer > /tmp/style.json) \
  && titan agent merge /tmp/security.json /tmp/style.json
```

### Integration with Standard Unix Tools

```bash
# Pipe git diff through an agent
git diff HEAD~1 | titan agent run diff-summarizer

# Process each file independently
find src/ -name "*.py" | while read f; do
  echo "{\"type\":\"message\",\"content\":\"$(cat "$f")\"}" \
    | titan agent run docstring-generator
done

# Filter agent output with jq
titan agent run code-analyzer < input.json | jq '.content'
```

## Implementation

### CLI Wrapper

A thin CLI wrapper around titan agents that handles stdin/stdout marshaling:

```python
# titan/cli/agent_pipe.py
import sys
import json
from titan.agent_forge import load_agent

def pipe_main(agent_name: str):
    """Run an agent in pipe mode: read JSON from stdin, write JSON to stdout."""
    agent = load_agent(agent_name)

    for line in sys.stdin:
        message = json.loads(line.strip())
        result = agent.process(message)
        sys.stdout.write(json.dumps(result) + "\n")
        sys.stdout.flush()
```

### CLI Entry Point

```bash
# titan CLI addition
titan agent run <agent-name> [--pipe]  # --pipe is default when stdin is not a TTY
```

### Auto-Detection

When stdin is a pipe (not a TTY), the agent automatically enters pipe mode:

```python
import sys

if not sys.stdin.isatty():
    # Pipe mode: read JSON from stdin
    pipe_main(agent_name)
else:
    # Interactive mode: existing behavior
    interactive_main(agent_name)
```

## Benefits

| Benefit | Description |
|---------|-------------|
| Composable | Chain agents with standard Unix pipes |
| Testable | Each agent is independently testable with fixture JSON |
| Language-agnostic | Any process that reads/writes JSON can participate |
| Debuggable | Insert `tee` or `jq` at any point in the chain |
| Scriptable | Integrate with shell scripts, cron jobs, CI pipelines |
| Familiar | Developers already know Unix pipes |

## Limitations

- No shared state between piped agents (each process is independent)
- Error propagation requires checking exit codes at each stage
- Large payloads may exceed pipe buffer limits (use temp files for > 1MB)
- Tool calls require a separate orchestrator process to fulfill

## Reference

- `titan/cli.py` — Existing CLI entry point (`titan.cli:main`)
- `agents/` — Agent archetype definitions
- `titan/agent_forge.py` — YAML DSL for agent specification
