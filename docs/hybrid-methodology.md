# F-21: Hybrid Methodology Support

> Support both Kanban and Scrum-lite in the workflow engine, mapped to organs as DDD bounded contexts.

## Problem

A single methodology does not fit all organs. Infrastructure organs (ORGAN-IV) benefit from continuous flow (Kanban). Product organs (ORGAN-III) benefit from time-boxed delivery cycles (Scrum-lite). The workflow engine must support both without forcing a one-size-fits-all approach.

## Methodology Mapping

| Organ | Methodology | Rationale |
|-------|-------------|-----------|
| ORGAN-I (Theoria) | Kanban | Research is continuous; no predictable sprint cadence |
| ORGAN-II (Poiesis) | Kanban | Creative work resists fixed time-boxing |
| ORGAN-III (Ergon) | Scrum-lite | Product delivery benefits from sprint discipline |
| ORGAN-IV (Taxis) | Kanban | Orchestration is reactive and continuous |
| ORGAN-V (Logos) | Scrum-lite | Editorial calendars map naturally to sprints |
| ORGAN-VI (Koinonia) | Kanban | Community engagement is event-driven |
| ORGAN-VII (Kerygma) | Kanban | Distribution is triggered by upstream events |
| META | Kanban | Governance work is continuous |

## Kanban Configuration

System-wide flow with WIP limits and pull-based scheduling.

```yaml
# workflow-config: kanban
methodology: kanban
wip_limits:
  per_organ: 5          # max concurrent items per organ
  per_agent: 2          # max concurrent items per AI agent
  system_wide: 15       # hard cap across all organs
columns:
  - backlog             # prioritized but not started
  - in_progress         # actively being worked
  - review              # awaiting human review
  - done                # merged and verified
pull_policy: oldest_first  # pull from backlog when capacity opens
blocked_policy: escalate_after_48h
```

### WIP Limit Enforcement

- Agents cannot pull new work when at capacity
- System-wide limit prevents resource contention across organs
- Blocked items escalate to the conductor's scorecard (F-29) after 48 hours

## Scrum-Lite Configuration

Time-boxed sprints per organ with lightweight ceremonies.

```yaml
# workflow-config: scrum-lite
methodology: scrum_lite
sprint:
  duration: 1w          # 1 or 2 week cycles
  planning: monday       # sprint planning day
  review: friday         # sprint review day
  retrospective: monthly # lightweight retro once per month
capacity:
  points_per_sprint: 13  # fibonacci-based estimation
  buffer: 20%            # reserve for unplanned work
artifacts:
  sprint_backlog: true
  burndown: true
  velocity_tracking: true
```

### Sprint Ceremonies (Lightweight)

| Ceremony | Duration | Frequency | Format |
|----------|----------|-----------|--------|
| Planning | 15 min | Per sprint | Review backlog, select items, set sprint goal |
| Review | 10 min | Per sprint | Demo completed work, check velocity |
| Retrospective | 20 min | Monthly | What worked, what didn't, one action item |

## Organs as DDD Bounded Contexts

Each organ operates as a bounded context with explicit boundaries:

```
┌─────────────────┐     ┌─────────────────┐
│   ORGAN-III      │     │   ORGAN-IV       │
│   (Scrum-lite)   │     │   (Kanban)       │
│                  │     │                  │
│  Product backlog │────▶│  Orchestration   │
│  Sprint cycles   │     │  Continuous flow │
│  Velocity tracked│     │  WIP-limited     │
└─────────────────┘     └─────────────────┘
         │                       │
         ▼                       ▼
   Published events         Consumed events
   (product.release)        (governance.review)
```

### Boundary Rules

- Each organ owns its methodology configuration
- Cross-organ work items are tracked as events, not shared backlogs
- No organ can modify another organ's WIP limits or sprint configuration
- The conductor (ORGAN-IV) observes all organs but does not override local methodology

## SRE Practices for ORGAN-III

Reliability targets for deployed surfaces (ORGAN-III products only):

| Metric | Target | Measurement |
|--------|--------|-------------|
| Availability | 99.5% | Uptime checks (monthly) |
| Deploy frequency | >= 1/week per active product | GitHub release count |
| Change failure rate | < 15% | Rollbacks / total deploys |
| MTTR | < 4 hours | Incident open → resolved |

### SRE Integration with Scrum-Lite

- Reliability work gets 20% sprint buffer allocation
- Incidents preempt sprint work (no negotiation)
- Post-incident items added to next sprint backlog automatically
- SLO violations surface on conductor's scorecard (F-29)

## Implementation

### Workflow Engine Configuration

```python
# titan/workflow_engine.py
class MethodologyConfig:
    """Per-organ methodology configuration."""

    organ: str
    methodology: Literal["kanban", "scrum_lite"]
    wip_limits: WIPLimits | None = None        # kanban
    sprint_config: SprintConfig | None = None   # scrum_lite

class WorkflowEngine:
    def configure_organ(self, organ: str, config: MethodologyConfig) -> None:
        """Set methodology for a specific organ."""
        ...

    def can_pull_work(self, organ: str, agent_id: str) -> bool:
        """Check WIP limits before allowing new work."""
        ...
```

### Governance Integration

```json
// governance-rules.json addition
{
  "article_vii": {
    "title": "Methodology Assignment",
    "rule": "Each organ declares its methodology in seed.yaml; the workflow engine enforces it",
    "enforcement": "automated"
  }
}
```

## Reference

- `governance-rules.json` — Existing governance articles
- `titan/workflow_engine.py` — DAG-based workflow execution
- F-03 (WIP limits) — Detailed WIP limit mechanics
- F-29 (Conductor's Scorecard) — Escalation surface for blocked items
