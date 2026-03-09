# Architectural Synthesis Implementation Plan

## Overview

Implement recommendations from "An Architectural Synthesis: A Modular, Multi-Agent AI System" to address critical gaps in the agentic-titan framework.

**Source Document:** `an-architectural-synthesis-a-modular-multi-agent.md`
**Status:** Gap analysis complete - implementation needed

## Gap Analysis Summary

| Area | Status | Critical? |
|------|--------|-----------|
| Ray Serve decoupling | ❌ Not implemented | YES |
| PostgreSQL persistence | ❌ Not implemented | YES |
| LangGraph orchestration | ❌ Not used | Medium |
| HITL approval gates | ❌ Not implemented | YES |
| RLHF data capture | ❌ Not implemented | Medium |
| CFO/Budget agent | ❌ Not implemented | Medium |
| Content filtering | ❌ Not implemented | YES |
| Termination logic | ⚠️ Partial (circuit breaker exists) | Medium |
| Role enforcement | ⚠️ Partial (archetypes exist, no RBAC) | Medium |
| Testing coverage | ⚠️ ~10% (4 test files) | Medium |
| Audit logging | ⚠️ Basic Python logging only | YES |

## What Already Exists (Good Foundations)

- ✅ Topology engine with 6 patterns (Swarm, Hierarchy, Pipeline, Mesh, Ring, Star)
- ✅ Consensus/voting system with multiple strategies
- ✅ Circuit breaker resilience pattern
- ✅ Redis for hot memory / pub-sub
- ✅ ChromaDB for vector storage
- ✅ Langfuse tracing with cost calculation
- ✅ Prometheus metrics
- ✅ Sandbox execution (Seatbelt/Landlock)
- ✅ Agent archetypes (Orchestrator, Researcher, Coder, Reviewer)
- ✅ Gitleaks in CI

---

## Implementation Phases (from Architectural Synthesis)

### Priority 1: Critical Architectural Corrections

#### Phase A: PostgreSQL Persistence Layer
**Goal:** Add durable audit logging and cold storage (document Section 2.3)

**Files to Create:**
```
titan/persistence/postgres.py          # PostgreSQL client wrapper
titan/persistence/audit.py             # Immutable audit log
titan/persistence/models.py            # SQLAlchemy models for audit tables
alembic/                               # Database migrations
```

**Schema (audit tables):**
```sql
CREATE TABLE audit_events (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type VARCHAR(50) NOT NULL,
    agent_id VARCHAR(100),
    session_id VARCHAR(100),
    user_id VARCHAR(100),
    action VARCHAR(255) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    metadata JSONB,
    checksum VARCHAR(64) NOT NULL  -- SHA256 for immutability verification
);

CREATE TABLE agent_decisions (
    id UUID PRIMARY KEY,
    audit_event_id UUID REFERENCES audit_events(id),
    decision_type VARCHAR(50),
    rationale TEXT,
    alternatives JSONB,
    selected_option VARCHAR(255),
    confidence FLOAT
);
```

**Modifications:**
- `hive/events.py` - Add PostgreSQL sink for events
- `agents/framework/base_agent.py` - Log decisions to audit table

---

#### Phase B: Human-in-the-Loop (HITL) Gates
**Goal:** Implement approval workflows for high-risk actions (document Section 5.1)

**Files to Create:**
```
titan/safety/hitl.py                   # HITL approval handler
titan/safety/gates.py                  # Approval gate definitions
titan/safety/policies.py               # Action risk classification
dashboard/components/approval.py       # Approval UI component
```

**Key Classes:**
```python
class ApprovalGate:
    """Gate that pauses execution pending human approval."""
    risk_level: RiskLevel  # LOW, MEDIUM, HIGH, CRITICAL
    requires_approval: bool
    timeout_seconds: int
    fallback_action: str  # "deny" | "allow" | "escalate"

class HITLHandler:
    """Manages approval requests and responses."""
    async def request_approval(action: Action, context: dict) -> ApprovalResult
    async def wait_for_approval(request_id: str, timeout: int) -> bool
```

**Actions requiring approval:**
- File deletion/modification outside workspace
- External API calls with credentials
- Code execution with network access
- Database modifications
- Sending emails/messages

**Modifications:**
- `tools/executor.py` - Check approval gates before execution
- `dashboard/app.py` - WebSocket endpoint for approval requests

---

#### Phase C: Content Filtering & Guardrails
**Goal:** Filter LLM outputs for dangerous patterns (document Section 5.1)

**Files to Create:**
```
titan/safety/filters.py                # Content filter implementations
titan/safety/patterns.py               # Dangerous pattern definitions
titan/safety/sanitizer.py              # Output sanitization
```

**Filter Categories:**
```python
class ContentFilter:
    """Base filter for LLM output scanning."""

class PromptInjectionFilter(ContentFilter):
    """Detect prompt injection attempts."""
    patterns = [
        r"ignore previous instructions",
        r"you are now",
        r"new system prompt",
        # ... more patterns
    ]

class CredentialLeakFilter(ContentFilter):
    """Detect credential exposure."""
    patterns = [
        r"(?i)api[_-]?key\s*[:=]\s*['\"]?\w+",
        r"(?i)password\s*[:=]\s*['\"]?\w+",
        # ... more patterns
    ]

class CommandInjectionFilter(ContentFilter):
    """Detect shell command injection."""
```

**Modifications:**
- `adapters/base.py` - Filter responses before returning
- `tools/executor.py` - Filter tool outputs

---

### Priority 2: Robustness & Safety Enhancements

#### Phase D: CFO Budget Agent
**Goal:** Cost-aware model routing and budget enforcement (document Section 4.2)

**Files to Create:**
```
agents/archetypes/cfo.py               # CFO budget agent
titan/costs/budget.py                  # Budget tracking
titan/costs/router.py                  # Cost-aware model selection
```

**Key Features:**
```python
class CFOAgent(BaseAgent):
    """Budget enforcement and cost optimization."""

    async def allocate_budget(task: Task, available: float) -> Budget
    async def select_model(task: Task, budget: Budget) -> str
    async def track_spend(agent_id: str, cost: float) -> None
    async def enforce_limits(session_id: str) -> bool

class TaskComplexityAnalyzer:
    """Analyze task to determine appropriate model tier."""

    def analyze(task: str) -> ComplexityLevel:
        # Simple tasks → GPT-4o-mini / Haiku
        # Medium tasks → GPT-4o / Sonnet
        # Complex tasks → GPT-4 / Opus
```

**Modifications:**
- `adapters/router.py` - Integrate cost-aware routing
- `hive/orchestrator.py` - Consult CFO before spawning agents

---

#### Phase E: Formal Termination Logic
**Goal:** Connect circuit breakers to orchestration (document Section 2.1)

**Files to Create:**
```
titan/orchestration/termination.py     # Termination conditions
titan/orchestration/watchdog.py        # Execution watchdog
```

**Key Features:**
```python
class TerminationCondition:
    """Formal termination condition for workflows."""
    max_iterations: int = 10
    max_duration_seconds: int = 300
    success_criteria: Callable[[State], bool]
    failure_criteria: Callable[[State], bool]

class ExecutionWatchdog:
    """Monitors execution and enforces termination."""
    async def monitor(workflow_id: str) -> None
    async def force_terminate(workflow_id: str, reason: str) -> None
```

**Modifications:**
- `hive/topology.py` - Add termination conditions to topologies
- `agents/framework/resilience.py` - Connect circuit breaker to watchdog

---

#### Phase F: Role-Based Access Control (RBAC)
**Goal:** Prevent role confusion with runtime validation (document Section 4.1)

**Files to Create:**
```
titan/safety/rbac.py                   # Role-based access control
titan/safety/permissions.py            # Permission definitions
```

**Permission Matrix:**
```python
ROLE_PERMISSIONS = {
    PersonaRole.ORCHESTRATOR: {
        "spawn_agents": True,
        "execute_code": False,
        "modify_files": False,
        "approve_actions": True,
    },
    PersonaRole.CODER: {
        "spawn_agents": False,
        "execute_code": True,
        "modify_files": True,
        "approve_actions": False,
    },
    PersonaRole.REVIEWER: {
        "spawn_agents": False,
        "execute_code": False,
        "modify_files": False,
        "approve_actions": True,
    },
}

class RBACEnforcer:
    """Validates agent actions against role permissions."""
    def check_permission(agent: BaseAgent, action: str) -> bool
    def validate_action(agent: BaseAgent, action: Action) -> ValidationResult
```

**Modifications:**
- `agents/framework/base_agent.py` - Check permissions before actions
- `tools/executor.py` - Validate tool calls against agent role

---

### Priority 3: Strategic Initiatives

#### Phase G: RLHF Data Capture
**Goal:** Capture structured data for reward model training (document Section 5.2)

**Files to Create:**
```
titan/learning/rlhf.py                 # RLHF data collection
titan/learning/feedback.py             # Human feedback handlers
titan/learning/reward_signals.py       # Reward signal extraction
```

**Data Schema:**
```python
@dataclass
class RLHFSample:
    """Sample for RLHF training."""
    prompt: str
    response: str
    human_rating: int | None  # 1-5 scale
    implicit_signals: dict    # time_to_accept, edits_made, etc.
    context: dict
    timestamp: datetime
```

**Modifications:**
- `titan/observability/langfuse.py` - Capture RLHF samples
- `dashboard/app.py` - Feedback collection UI endpoint

---

#### Phase H: Comprehensive Testing Suite
**Goal:** Adversarial testing, prompt banks, automated evaluation (document Section 5.3)

**Files to Create:**
```
tests/adversarial/                     # Adversarial test suite
tests/adversarial/prompt_injection.py
tests/adversarial/role_confusion.py
tests/adversarial/resource_exhaustion.py

tests/prompts/                         # Prompt bank
tests/prompts/bank.py                  # Prompt registry
tests/prompts/regression.json          # Known-good prompts

tests/evaluation/                      # Automated evaluation
tests/evaluation/deepeval_suite.py     # DeepEval integration
tests/evaluation/quality_metrics.py    # Output quality scoring
```

**Test Categories:**
- Prompt injection resistance
- Role boundary enforcement
- Resource limit compliance
- Termination condition verification
- HITL gate triggering
- Cost budget adherence

---

## Files Summary

### New Files (Priority 1 - Critical)
```
titan/persistence/postgres.py
titan/persistence/audit.py
titan/persistence/models.py
titan/safety/hitl.py
titan/safety/gates.py
titan/safety/policies.py
titan/safety/filters.py
titan/safety/patterns.py
titan/safety/sanitizer.py
dashboard/components/approval.py
alembic/                               # Migration directory
```

### New Files (Priority 2 - Robustness)
```
agents/archetypes/cfo.py
titan/costs/budget.py
titan/costs/router.py
titan/orchestration/termination.py
titan/orchestration/watchdog.py
titan/safety/rbac.py
titan/safety/permissions.py
```

### New Files (Priority 3 - Strategic)
```
titan/learning/rlhf.py
titan/learning/feedback.py
titan/learning/reward_signals.py
tests/adversarial/
tests/prompts/
tests/evaluation/
```

### Modifications
```
hive/events.py                         # PostgreSQL audit sink
agents/framework/base_agent.py         # RBAC + audit logging
tools/executor.py                      # HITL gates + content filtering
adapters/base.py                       # Content filtering
adapters/router.py                     # Cost-aware routing
hive/topology.py                       # Termination conditions
hive/orchestrator.py                   # CFO integration
dashboard/app.py                       # Approval UI + feedback endpoints
.github/workflows/ci.yml               # Make lint/typecheck blocking
pyproject.toml                         # New dependencies
```

### New Dependencies
```toml
[project.optional-dependencies]
postgres = [
    "asyncpg>=0.29.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "alembic>=1.13.0",
]
evaluation = [
    "deepeval>=0.21.0",
]
```

---

## Verification Plan

### Priority 1 Verification
- **PostgreSQL**: Insert audit event → query → verify checksum matches
- **HITL**: Trigger high-risk action → verify approval request appears in dashboard
- **Content Filter**: Send prompt injection → verify blocked and logged

### Priority 2 Verification
- **CFO**: Run expensive task with budget limit → verify cheaper model selected
- **Termination**: Create infinite loop scenario → verify watchdog terminates
- **RBAC**: Coder agent attempts to spawn agents → verify permission denied

### Priority 3 Verification
- **RLHF**: Complete task → verify sample captured with all fields
- **Testing**: Run adversarial suite → verify all tests pass

### Integration Tests
```bash
pytest tests/integration/test_postgres_audit.py
pytest tests/integration/test_hitl_gates.py
pytest tests/integration/test_content_filters.py
pytest tests/integration/test_cfo_budget.py
pytest tests/adversarial/
```

---

## Summary

**Source Document:** Architectural Synthesis critique
**Total new files:** ~30
**Total modifications:** ~12
**Dependencies:** PostgreSQL, asyncpg, SQLAlchemy, DeepEval

**Priority 1 (Critical - Week 1-2):**
- PostgreSQL persistence layer
- HITL approval gates
- Content filtering/guardrails

**Priority 2 (Robustness - Week 3-4):**
- CFO budget agent
- Formal termination logic
- RBAC enforcement

**Priority 3 (Strategic - Week 5+):**
- RLHF data capture
- Comprehensive test suite
