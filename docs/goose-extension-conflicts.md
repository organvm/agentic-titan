# F-78: Goose Extension Conflict Resolution

> Document and resolve conflicts between goose extensions in the ORGANVM workflow.

## Problem

Goose supports multiple extensions that can conflict with each other or with ORGANVM's existing tooling. Extensions may compete for the same resources (filesystem access, git operations), produce contradictory outputs, or interfere with titan's orchestration. A priority ordering and conflict resolution strategy is needed.

## Known Conflicts

### JetBrains Extension

| Conflict | Description | Impact |
|----------|-------------|--------|
| File locking | JetBrains IDE locks files during indexing; goose writes fail | Medium |
| Git operations | IDE auto-commit/push can race with goose git extension | High |
| Terminal integration | IDE terminal intercepts goose's stdin/stdout | Low |

**Resolution**: Disable JetBrains extension when running goose in CLI mode. Use JetBrains extension only when goose is invoked from within the IDE.

### Jira Extension

| Conflict | Description | Impact |
|----------|-------------|--------|
| Issue creation | Can create issues that conflict with ORGANVM's GitHub-based tracking | High |
| Status sync | Jira status updates don't propagate to ORGANVM governance layer | Medium |
| Credential scope | Jira OAuth tokens grant broader access than needed | Low |

**Resolution**: Disable Jira extension entirely. ORGANVM uses GitHub Issues exclusively for project tracking. If Jira integration is needed for external stakeholders, route through a dedicated bridge (not through goose).

### Google Drive Extension

| Conflict | Description | Impact |
|----------|-------------|--------|
| File sync | Google Drive sync conflicts with local filesystem operations | Medium |
| Path resolution | Drive paths don't map to local workspace structure | Medium |
| Data leakage | Sensitive files could be uploaded to shared drives | High |

**Resolution**: Disable Google Drive extension. Use local filesystem only. If document sharing is needed, use explicit export scripts.

## Priority Ordering

Extensions are prioritized by how critical they are to ORGANVM workflows:

| Priority | Extension | Status | Rationale |
|----------|-----------|--------|-----------|
| 1 (highest) | filesystem | Enabled | Core operation — reading and writing files |
| 2 | git | Enabled | Version control is fundamental |
| 3 | shell | Enabled | Command execution for builds, tests, scripts |
| 4 | developer | Enabled | Code analysis, refactoring assistance |
| 5 | mcp | Enabled | MCP protocol support for titan integration |
| 6 | memory | Conditional | Enable for long sessions; disable for short tasks |
| 7 | web-search | Conditional | Enable for research tasks only |
| 8 | jetbrains | Disabled | Conflicts with CLI workflow |
| 9 | jira | Disabled | Conflicts with GitHub-based tracking |
| 10 | google-drive | Disabled | Data leakage risk, path conflicts |

## Disable List

Extensions that interfere with ORGANVM workflows and should be permanently disabled:

```yaml
# goose config — disabled extensions
extensions:
  disabled:
    - jetbrains      # file locking conflicts
    - jira            # conflicts with GitHub Issues
    - google-drive    # data leakage risk
    - slack           # notifications handled by ORGAN-VII
```

## Permission Configuration

### permission.yaml

```yaml
# ~/.config/goose/permission.yaml
extensions:
  filesystem:
    allowed_paths:
      - ~/Workspace/          # ORGANVM workspace
    denied_paths:
      - ~/Workspace/intake/   # untrusted inbound material
      - ~/.ssh/               # credentials
      - ~/.gnupg/             # credentials
    write_mode: prompt         # ask before writing

  git:
    allowed_operations:
      - status
      - diff
      - add
      - commit
      - branch
      - checkout
    denied_operations:
      - push --force           # never force push
      - reset --hard           # require explicit confirmation
    auto_commit: false         # never auto-commit

  shell:
    allowed_commands:
      - pytest
      - ruff
      - mypy
      - npm
      - node
      - python
      - pip
      - uv
    denied_commands:
      - rm -rf                 # dangerous
      - curl | sh              # remote code execution
    timeout: 120s              # kill after 2 minutes

  mcp:
    servers:
      - filesystem             # local MCP server
      - memory                 # memory graph
      - sequential-thinking    # reasoning tool
    denied_servers:
      - "*"                    # deny all unlisted servers
```

## Extension Combination Matrix

Testing which extension combinations work correctly together:

| Combination | Status | Notes |
|-------------|--------|-------|
| filesystem + git + shell | Pass | Core trio, no conflicts |
| filesystem + git + shell + developer | Pass | Standard dev workflow |
| filesystem + git + shell + mcp | Pass | With titan integration |
| filesystem + git + memory | Pass | Long session support |
| filesystem + git + web-search | Pass | Research mode |
| filesystem + jetbrains | Fail | File locking issues |
| git + jira | Fail | Dual tracking conflict |
| filesystem + google-drive | Fail | Path resolution errors |
| All enabled | Fail | Multiple conflicts, resource contention |

### Testing Protocol

For each combination:

1. Start goose with only the specified extensions enabled
2. Run standard test suite: create file, edit file, git commit, run tests
3. Check for: file lock errors, race conditions, unexpected state changes
4. Record pass/fail and any error messages

## Reference

- `docs/goose-evaluation.md` (F-25) — Initial goose evaluation
- `docs/goose-titan-ptc-bridge.md` — Goose-titan integration bridge
- F-75 (Agent config audit) — Ecosystem-wide configuration review
