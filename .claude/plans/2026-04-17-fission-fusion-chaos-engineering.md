# Plan: Chaos Engineering Tests for FissionFusion (#35)

## Context

The emergence chain (#70→#71→#61→#72→#73→#64) is complete and committed. It built the full fission-fusion loop: conflict → crisis_level rises → FUSION triggered → agents coordinate → conflict resolves → crisis drops → FISSION. But **no test validates this loop under adversarial conditions**. The existing `tests/chaos/test_fission_recovery.py` (51 lines) tests only the `FissionFusionTopology` data structure — not the `FissionFusionManager` engine — and is currently broken (pydantic collection error). Issue #35 calls for resilience testing of topology recovery.

## What Exists

| File | What it does | Gap |
|------|-------------|-----|
| `hive/fission_fusion.py` | `FissionFusionManager` — state machine (FISSION↔FUSION), crisis resolution (3-tier + conflict floor), windowed majority gate (3-of-5), cooldown, async eval loop | No chaos tests |
| `hive/conflict.py` | `ConflictDetector` — opposing pheromone pairs → crisis signal | Tested in isolation (#64), not under chaos |
| `hive/criticality.py` | `CriticalityMonitor` — SUBCRITICAL/CRITICAL/SUPERCRITICAL with emergence threshold gate | Tested in isolation (#61), not under chaos |
| `hive/topology.py:1109` | `FissionFusionTopology` — cluster data structure, add/remove agent, fission/fusion ops | Basic chaos test exists but broken |
| `tests/chaos/test_fission_recovery.py` | 1 test: 10 agents, kill 3, check neighbors | Broken (pydantic error), tests topology not manager |
| `tests/chaos/test_resilience.py` | 18 tests: network partition, timeouts, LLM failures | Tests agent resilience, not fission-fusion dynamics |

## Implementation

### 1. Fix `tests/chaos/test_fission_recovery.py`

The pydantic collection error likely stems from `hive.topology` → `TopologyEngine` import chain pulling in pydantic v1/v2 conflict. Fix by making the import resilient or adjusting the import path.

### 2. Create `tests/chaos/test_fission_fusion_chaos.py`

New comprehensive chaos test suite targeting the `FissionFusionManager` and its integration with the emergence chain components.

**Test categories:**

#### A. Crisis Signal Propagation (3 tests)
- `test_manual_crisis_triggers_fusion` — `set_crisis_level(0.8)` → `should_transition()` returns FUSION
- `test_criticality_derived_crisis` — wire mock `CriticalityMonitor` in SUPERCRITICAL state → crisis rises above fusion threshold
- `test_conflict_detector_floor` — inject opposing pheromone traces → `ConflictDetector.compute_crisis_signal()` raises floor → crisis rises

#### B. Agent Loss Scenarios (4 tests)
- `test_cluster_survives_minority_loss` — 5 agents in cluster, remove 2, verify remaining connectivity in `FissionFusionTopology`
- `test_cluster_survives_majority_loss` — 5 agents, remove 4, verify last agent exists with empty neighbors
- `test_cross_cluster_loss` — 10 agents in 2 clusters, remove 1 from each, verify both clusters intact
- `test_total_cluster_wipeout` — remove all agents from one cluster, verify other cluster unaffected, empty cluster cleaned

#### C. State Machine Under Stress (4 tests)
- `test_chaos_fission_to_fusion_to_fission` — full loop: start FISSION → inject crisis → verify FUSION → clear crisis → verify return to FISSION
- `test_windowed_gate_blocks_transient_spike` — single high-crisis evaluation should NOT trigger transition (need 3-of-5)
- `test_cooldown_prevents_rapid_oscillation` — after transition, immediate counter-signal should be suppressed during refractory period
- `test_concurrent_crisis_sources` — both CriticalityMonitor AND ConflictDetector fire simultaneously → conflict floor wins when higher

#### D. Recovery Dynamics (3 tests)
- `test_fusion_creates_info_center` — during fusion, verify `_info_center_id` is set and FUSION_COMPLETED event emitted
- `test_fission_after_recovery_forms_clusters` — after crisis clears and fission occurs, verify clusters reformed from neighborhood profiles
- `test_state_change_callbacks_fire_under_chaos` — register callback, trigger transition, verify callback invoked with correct state

#### E. Integration: Full Emergence Loop (2 tests)
- `test_conflict_driven_full_loop` — create PheromoneField with real opposing traces → ConflictDetector detects → crisis_level rises → FissionFusionManager evaluates → transitions to FUSION → clear traces → crisis drops → returns to FISSION
- `test_crisis_level_resolution_priority` — verify 3-tier resolution: manual override > criticality-derived > preserved, with conflict floor as absolute minimum across all tiers

**Total: ~16 new tests**

### Test Infrastructure

- Reuse fixtures from `tests/test_hive/conftest.py` (`mock_event_bus`, `mock_neighborhood`, `mock_pheromone_field`)
- Add chaos-specific fixtures in a local conftest or inline
- All tests async (`asyncio_mode = "auto"` — no `@pytest.mark.asyncio` needed)
- Mark with `pytest.mark.chaos`
- For windowed gate tests: directly manipulate `_metrics_history` to simulate evaluation cycles
- For cooldown tests: directly set `_last_transition_time` to bypass real time waits

### Files Modified

| File | Action |
|------|--------|
| `tests/chaos/test_fission_fusion_chaos.py` | **CREATE** — 16 tests |
| `tests/chaos/test_fission_recovery.py` | **FIX** — pydantic import error |

### Not in Scope

- No changes to production code (`hive/`)
- No new fixtures in root conftest
- No modifications to existing passing tests

## Verification

```bash
cd agentic-titan
pytest tests/chaos/test_fission_fusion_chaos.py -v   # New tests pass
pytest tests/chaos/test_fission_recovery.py -v        # Fixed test passes
pytest tests/chaos/ -v                                # All chaos tests pass
pytest tests/test_hive/ -v                            # Existing hive tests still pass
pytest --tb=short -q                                  # Full suite still at 307+ tests
```
