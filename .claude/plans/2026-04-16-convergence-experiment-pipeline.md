# Plan: Issue #72 — Convergence Experiment (Full Pipeline Integration)

## Context

The emergence foundation (issues #66-71) built sensing infrastructure across `hive/criticality.py`, `hive/fission_fusion.py`, `hive/learning.py`, and `hive/emergence.py`. Issue #61 (emergence threshold) was also completed — `TopologyEngine.EMERGENCE_THRESHOLDS`, the `emergence_threshold` property, and the `CriticalityMonitor` forced-SUBCRITICAL gate are all in place.

A skeleton `hive/experiments/convergence.py` already exists and runs (16 sweep points, onset at N=16). But it operates in isolation — no `TopologicalNeighborhood`, no `CriticalityMonitor.sample_state()`, no `PheromoneField` traces. It uses a hardcoded binary criticality state (`SUBCRITICAL` vs `CRITICAL` based solely on `above_emergence_threshold`), missing the real metrics pipeline.

**Goal:** Wire the experiment through the full pipeline — neighborhood → criticality monitor → pheromone field → emergence detector — so the sweep produces real metrics and empirically validates the emergence threshold.

## Files to Modify

| File | Changes |
|------|---------|
| `hive/experiments/convergence.py` | Expand vocab to 139 atoms, add `SweepPoint` fields, make `run()`/`_run_single()` async, wire in neighborhood + criticality + pheromone |
| `tests/test_hive/test_convergence_experiment.py` | **New file** — comprehensive tests for the enhanced experiment |

Read-only references (no modifications):
- `hive/criticality.py` — `CriticalityMonitor`, `CriticalityMetrics`, `CriticalityState`
- `hive/neighborhood.py` — `TopologicalNeighborhood`, `InteractionType`, `register_agent()`, `record_interaction()`, `get_network_stats()`
- `hive/stigmergy.py` — `PheromoneField`, `TraceType`, `deposit()`
- `hive/emergence.py` — `EmergenceDetector`, `EmergenceResult`
- `hive/topology.py` — `TopologyEngine`, `TopologyType`, `EMERGENCE_THRESHOLDS`

## Implementation Steps

### Step 1: Expand vocabulary to 139 atoms

In `convergence.py`, expand `_DOMAIN_VOCABULARY` from 40 to 120 terms organized by domain:
- Systems (30): latency, throughput, bottleneck, saturation, capacity, congestion, degradation, failover, redundancy, resilience, partition, consistency, availability, replication, sharding, indexing, caching, prefetching, eviction, invalidation, compaction, deduplication, normalization, denormalization, materialization, linearizability, serializability, isolation, atomicity, durability
- Resilience (20): backpressure, throttling, circuit, breaker, bulkhead, timeout, retry, jitter, exponential, backoff, shedding, quarantine, fallback, recovery, checkpoint, rollback, idempotency, compensation, reconciliation, stabilization
- Observability (20): observability, telemetry, tracing, correlation, propagation, sampling, aggregation, windowing, percentile, histogram, cardinality, dimensionality, instrumentation, profiling, benchmarking, alerting, anomaly, baseline, threshold, dashboard
- Networking (20): routing, forwarding, balancing, proxy, gateway, firewall, encryption, certificate, handshake, multiplexing, pipelining, framing, serialization, compression, decompression, discovery, registration, heartbeat, gossip, quorum
- Scaling (15): horizontal, vertical, autoscaling, provisioning, elasticity, multitenancy, namespace, federation, orchestration, scheduling, placement, affinity, colocation, migration, preemption
- Consensus (15): consensus, leader, election, follower, candidate, proposal, ballot, majority, supermajority, byzantine, membership, reconfiguration, snapshotting, compaction, protocol

Expand `_SYNTHESIS_VOCABULARY` from 16 to 19 terms (add synergy, metamorphosis, catalysis). Total: 139 atoms.

### Step 2: Add new fields to `SweepPoint`

Add 6 fields after `vocab_coverage`:
```python
correlation_length: float = 0.0
functional_connectivity: float = 0.0
order_parameter: float = 0.5
criticality_score: float = 0.0
total_interactions: int = 0
network_density: float = 0.0
```

Update `to_dict()` to include them. Since `SweepPoint` is `frozen=True`, these are keyword-only additions with defaults — no backward compat issues.

### Step 3: Make `run()` and `_run_single()` async

- `async def run(self) -> ConvergenceResult`
- `async def _run_single(self, n: int, rng: random.Random) -> SweepPoint`
- Add `import asyncio` at top

### Step 4: Wire in `TopologicalNeighborhood`

In `_run_single()`, after creating topology and adding agents:
1. Create `TopologicalNeighborhood(neighbor_count=7)`
2. For each agent, `neighborhood.register_agent(agent_id, capabilities=terms)` where `terms` is their vocab subset
3. Simulate interactions: each agent interacts with `min(k, n-1)` random other agents via `neighborhood.record_interaction(a, b, InteractionType.COLLABORATION, success=True)`
4. The number of interactions per agent scales proportionally so larger swarms have richer interaction networks

### Step 5: Wire in `CriticalityMonitor.sample_state()`

In `_run_single()`:
1. Create `CriticalityMonitor(neighborhood=neighborhood)`
2. Call `monitor.set_emergence_threshold(engine.emergence_threshold, n)`
3. `metrics = await monitor.sample_state()` — this calls `_measure_functional_connectivity()`, `_measure_order_parameter()`, `_measure_correlation_length()` using the real neighborhood
4. Use `metrics.infer_state()` for `criticality_state`
5. Populate `SweepPoint` fields from `metrics.correlation_length`, `.functional_connectivity`, `.order_parameter`, `.criticality_score`

### Step 6: Wire in `PheromoneField` trace deposition

In `_run_single()`:
1. Create `PheromoneField(field_id=f"sweep-n{n}")`
2. For each agent, `await field.deposit(agent_id, TraceType.RESOURCE, "shared", payload={"terms": agent_terms})`
3. This establishes the stigmergic communication substrate — primarily for pipeline completeness and proving the pheromone → emergence chain works end-to-end

### Step 7: Add `get_network_stats()` to SweepPoint

After interactions are recorded, `stats = neighborhood.get_network_stats()` provides `total_interactions` and `density` → populate `SweepPoint.total_interactions` and `SweepPoint.network_density`.

### Step 8: Write tests

New file `tests/test_hive/test_convergence_experiment.py`:

**TestSweepPoint:**
- `test_new_fields_have_defaults` — construction with only original fields works
- `test_new_fields_in_to_dict` — all 14 fields appear in serialized output
- `test_frozen` — SweepPoint is immutable

**TestConvergenceResult:**
- `test_emergence_onset_property` — finds first N with emergence
- `test_consistent_emergence_property` — finds N where emergence stabilizes
- `test_to_dict_round_trip` — serialization includes all expected keys

**TestConvergenceExperiment:**
- `test_full_sweep_produces_16_points` — default range 8..128 step 8
- `test_deterministic_with_seed` — same seed → identical results
- `test_emergence_detected_at_high_n` — N=128 always detects emergence
- `test_criticality_metrics_populated` — every point has non-default criticality values
- `test_functional_connectivity_increases_with_n` — positive correlation between N and functional_connectivity
- `test_order_parameter_in_valid_range` — all values in [0, 1]
- `test_total_interactions_scales_with_n` — more agents → more interactions
- `test_network_density_populated` — density > 0 for all points
- `test_vocab_coverage_monotonically_increases` — more agents → more domain coverage
- `test_above_threshold_always_true` — since minimum N=8 = SWARM threshold, all points are above
- `test_small_n_below_threshold` — run with `n_range=[4, 6]` to prove forced SUBCRITICAL

## Invariants the Experiment Should Uphold

1. **Coverage monotonically increases**: more agents → more vocabulary coverage
2. **Large N emergence**: at N=128, `emergence_detected` should be True
3. **All metrics bounded**: criticality_score ∈ [0, 1], order_parameter ∈ [0, 1], functional_connectivity ∈ [0, 1]
4. **Interactions scale with N**: `total_interactions(N=128) > total_interactions(N=8)`
5. **Determinism**: same seed → identical sweep
6. **Below threshold = SUBCRITICAL**: N < 8 with SWARM → forced subcritical via CriticalityMonitor gate

## Verification

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/agentic-titan
.venv/bin/python -m pytest tests/test_hive/test_convergence_experiment.py -v
.venv/bin/python -m pytest tests/test_hive/ -v --tb=short  # Full hive suite
.venv/bin/python -c "
import asyncio
from hive.experiments.convergence import ConvergenceExperiment
r = asyncio.run(ConvergenceExperiment().run())
for p in r.sweep_points:
    print(f'N={p.agent_count:3d} emg={p.emergence_detected} ratio={p.novelty_ratio:.3f} '
          f'fc={p.functional_connectivity:.3f} op={p.order_parameter:.3f} '
          f'cs={p.criticality_score:.3f} state={p.criticality_state}')
print(f'Onset: {r.emergence_onset}, Consistent: {r.consistent_emergence}')
"
ruff check hive/experiments/convergence.py tests/test_hive/test_convergence_experiment.py
```
