# F-32: Labyrinth Frequency Metric

> "How often do you get lost" — tracking sessions that exceed planned duration or produce no merge-ready output.

## Definition

A **labyrinth session** is any work session that meets either criterion:

1. **Duration overrun**: Session exceeds 2x its planned duration
2. **No output**: Session produces no merge-ready artifact (commit, PR, document, or config change)

Both criteria are tracked independently. A session can be a labyrinth on both counts.

## Tracking

### Data Collection

```yaml
# session log entry
session:
  id: "2026-03-08-titan-memory-adapter"
  planned_duration: 2h
  actual_duration: 5h          # 2.5x planned → labyrinth (duration)
  merge_ready_output: false    # → labyrinth (no output)
  labyrinth: true
  causes:
    - unclear_spec
    - unfamiliar_codebase
  notes: "Spent 3h exploring memory backends before realizing ChromaDB was already integrated"
```

### Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Labyrinth rate | labyrinth_sessions / total_sessions | < 15% (3-month target) |
| Duration overrun ratio | avg(actual / planned) for labyrinth sessions | < 2.5x |
| No-output rate | no_output_sessions / total_sessions | < 10% |
| Recovery rate | labyrinth_sessions_that_eventually_produced_output / labyrinth_sessions | > 80% |

### Baseline and Target

| Period | Target Labyrinth Rate | Mechanism |
|--------|----------------------|-----------|
| Month 1 | Establish baseline | Instrument tracking, no intervention |
| Month 2 | Baseline - 25% | Apply mitigations to top 2 causes |
| Month 3 | Baseline - 50% | Full mitigation suite active |

## Common Causes

Ranked by observed frequency:

| Cause | Frequency | Description |
|-------|-----------|-------------|
| Unclear spec | High | Acceptance criteria missing or ambiguous |
| Wrong approach | High | Chose an implementation path that hit a dead end |
| Unfamiliar codebase | Medium | Navigating unknown code without a guide |
| Tool issues | Medium | Environment, dependency, or CI failures |
| Scope creep | Medium | Session expanded beyond original intent |
| Yak shaving | Low | Fixing unrelated prerequisites |

## Mitigations

### Three-Prompt Rule (F-60)

Before starting implementation, answer three prompts:

1. **What is the exit condition?** — Define done in one sentence
2. **What is the smallest possible output?** — Identify the MVP artifact
3. **What will I do if stuck after 30 minutes?** — Pre-commit to a fallback action

### Decision Matrices (F-62)

When choosing between approaches, use a 2x2 matrix:

```
                Low Effort    High Effort
High Certainty   DO FIRST      PLAN THEN DO
Low Certainty    SPIKE FIRST   AVOID / DEFER
```

### Spike-First Approach

For sessions with unfamiliar codebase or unclear feasibility:

1. Time-box a 30-minute spike (exploration only)
2. At the end of the spike, decide: proceed, reshape, or abandon
3. Only count the main session toward labyrinth tracking (spikes are expected exploration)

### Session Checkpoints

Insert a 5-minute checkpoint at the planned midpoint:

- Am I on track to finish within planned duration?
- Have I produced any intermediate artifacts?
- Should I narrow scope to ensure some output?

## Dashboard Integration

Labyrinth frequency feeds into the conductor's scorecard (F-29):

```
┌─────────────────────────────────────┐
│  Labyrinth Frequency   [This Week]  │
│                                     │
│  Sessions: 12                       │
│  Labyrinth: 2 (16.7%)             │
│  Top cause: unclear_spec (2x)      │
│  Trend: ▼ improving                │
└─────────────────────────────────────┘
```

## Reference

- `docs/conductors-scorecard.md` (F-29) — Weekly scorecard integration
- F-60 (Three-Prompt Rule) — Pre-session mitigation
- F-62 (Decision Matrices) — Approach selection framework
