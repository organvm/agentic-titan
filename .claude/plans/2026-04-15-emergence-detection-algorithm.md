# Plan: Agentic-Titan #71 Emergence Detection + Memory Housekeeping

## Context

Last session saved 3 memory files that never materialized on disk (`feedback_comment_cadence.md`, `feedback_compose_against_conversation.md`, `project_oss_contributions.md`) and identified 2 design seeds needing IRF tracking. The agentic-titan emergence chain (#71→#67→#66→#68→#69→#61+#72→#73) is the active intellectual edge — #71's data model is complete but the detection algorithm is missing.

**Problem:** `EpisodeOutcome.emergence_detected` is always `False` because no code ever detects emergence. The fields exist (learning.py:117-118), serialization works, 11 tests pass — but it's dead metadata. The issue's core requirement is a detection algorithm that compares individual agent traces against collective output.

**Goal:** Implement the detection algorithm, wire it into the episode lifecycle, close #71, and fix the memory gap.

---

## Part 1: Memory Housekeeping (~5 min)

### 1a. Recreate 3 lost memory files

| File | Content |
|------|---------|
| `feedback_comment_cadence.md` | Stagger cross-repo comments; 90-second bursts across multiple repos look inhuman. Space contributions naturally. |
| `feedback_compose_against_conversation.md` | When commenting on PRs, compose against the human conversation thread, not metadata/CI output. Address the maintainer's actual words. |
| `project_oss_contributions.md` | Redirect — content already lives in `project-contrib-upstream-prs.md`. Add design seeds there instead of creating a duplicate. |

### 1b. Add 2 design seeds to `project-contrib-upstream-prs.md`

1. **Consolidation intent** — contrib operations currently scattered across 16 local repos, issue trackers, and memory files. Needs a single home. Blocks on broader ecosystem evolution (a-organvm transition).
2. **External Research Committee** — per-repo intelligence surface: peer discovery → contribution → study → feedback/feedforward/feedthrough loops. Transforms contribution from opportunistic to systematic.

Both should also become IRF items (P3, design-needed).

---

## Part 2: Implement Emergence Detection (#71)

### Design

**New file: `hive/emergence.py`** — `EmergenceDetector` class

The detector compares per-agent memory deposits against a collective output to identify novel information — content in the collective that no individual agent contributed.

```
EmergenceDetector
├── detect(agent_contributions, collective_output) → EmergenceResult
├── _tokenize(text) → set[str]          # Normalize + split into token set
├── _compute_novelty(individual_sets, collective_set) → list[str]
└── _format_evidence(novel_tokens, collective_output) → list[str]
```

**`EmergenceResult`** dataclass: `detected: bool`, `evidence: list[str]`, `novelty_ratio: float`

**V1 detection algorithm (token set-difference):**
1. Tokenize each agent's contributions into token sets (lowercased, stripped, deduplicated)
2. Compute union of all individual agent token sets
3. Tokenize collective output
4. Novel tokens = collective tokens - union of individual tokens
5. `emergence_detected = novelty_ratio > threshold` (default 0.1 = 10% novel content)
6. Evidence = sentences from collective output containing novel tokens

This is deliberately simple. It's a V1 heuristic — the threshold is tunable, and the architecture supports swapping in embedding-based detection later. The issue's own language ("information not traceable to any individual agent") maps directly to set difference.

### Integration

**`hive/topology.py:1591` — `end_task()`:**
- Add optional `collective_output: str | None = None` parameter
- Add optional `agent_contributions: dict[str, list[str]] | None = None` parameter
- If both provided, run `EmergenceDetector.detect()` and pass results to `EpisodeOutcome` constructor
- If not provided, fields remain at defaults (backward compatible)

### Files to modify

| File | Action |
|------|--------|
| `hive/emergence.py` | **NEW** — EmergenceDetector + EmergenceResult |
| `hive/topology.py:1591-1625` | Modify `end_task()` to accept + use emergence params |
| `hive/__init__.py` | Export EmergenceDetector, EmergenceResult |
| `tests/test_hive/test_emergence.py` | **NEW** — detector unit tests |
| `tests/test_hive/test_learning.py` | No changes needed (data model tests already pass) |

### Test cases for `test_emergence.py`

1. **No emergence** — collective output is strict subset of individual contributions → `detected=False`
2. **Clear emergence** — collective contains novel synthesis → `detected=True` with evidence
3. **Threshold boundary** — novelty ratio just below/above threshold
4. **Empty inputs** — no agent contributions, empty collective → graceful `detected=False`
5. **Single agent** — one agent can't produce emergence (need collective)
6. **Overlapping contributions** — agents share knowledge, emergence still detected in synthesis
7. **Custom threshold** — detector respects configurable threshold
8. **Evidence formatting** — evidence strings reference actual novel content

### Existing code to reuse

- `hive/memory.py:Memory` dataclass and `hash_embedding()` — embedding infrastructure if needed for V2
- `hive/learning.py:EpisodeOutcome` — fields already wired, just need to populate them
- `hive/criticality.py:CriticalityMetrics` — pattern for metrics dataclass design

---

## Part 3: Close Issue #71

After implementation + tests pass:
- Close GH issue #71 with commit SHA reference
- Note in issue that V1 uses token set-difference, V2 can use embeddings

---

## Verification

```bash
cd agentic-titan
# Run emergence tests
pytest tests/test_hive/test_emergence.py -v

# Run full hive test suite to confirm no regressions
pytest tests/test_hive/ -v

# Type check
mypy hive/emergence.py

# Lint
ruff check hive/emergence.py tests/test_hive/test_emergence.py
```

---

## Execution Order

1. Memory housekeeping (feedback files + design seeds + IRF)
2. Write `hive/emergence.py` with `EmergenceDetector` + `EmergenceResult`
3. Write `tests/test_hive/test_emergence.py`
4. Run tests, fix any issues
5. Modify `hive/topology.py:end_task()` for integration
6. Update `hive/__init__.py` exports
7. Full hive test suite
8. Lint + type check
9. Close #71
