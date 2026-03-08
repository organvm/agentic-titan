# F-20: Test-Driven Prompting Pipeline

> TDP workflow where tests constrain AI code generation, reducing hallucination and providing measurable quality.

## Problem

AI code generation without constraints produces plausible but untested output. Developers spend significant time validating and correcting AI-generated code. Without executable acceptance criteria, quality is subjective and inconsistent.

## TDP Workflow

```
spec → generate tests → constrain generation → validate in CI
```

### Phase 1: Developer Writes Spec

The developer provides acceptance criteria in structured format:

```yaml
# tdp-spec.yaml
feature: user-session-timeout
acceptance_criteria:
  - sessions expire after 30 minutes of inactivity
  - expired sessions return 401 on next request
  - session extension resets the timeout clock
  - concurrent sessions per user are limited to 3
edge_cases:
  - clock skew between servers
  - session created just before midnight boundary
```

### Phase 2: AI Generates Tests from Spec

The AI agent converts acceptance criteria into executable tests:

```python
def test_session_expires_after_inactivity(session_manager):
    session = session_manager.create(user_id="u1")
    advance_clock(minutes=31)
    assert session_manager.validate(session.token) is False

def test_expired_session_returns_401(client, expired_session):
    response = client.get("/api/data", headers={"Authorization": expired_session.token})
    assert response.status_code == 401

def test_session_extension_resets_timeout(session_manager):
    session = session_manager.create(user_id="u1")
    advance_clock(minutes=20)
    session_manager.extend(session.token)
    advance_clock(minutes=20)
    assert session_manager.validate(session.token) is True

def test_concurrent_session_limit(session_manager):
    for i in range(3):
        session_manager.create(user_id="u1")
    with pytest.raises(MaxSessionsExceeded):
        session_manager.create(user_id="u1")
```

### Phase 3: Tests Constrain Code Generation

The AI generates implementation code with a hard constraint: all generated tests must pass. The generation loop:

1. Generate candidate implementation
2. Run test suite
3. If tests fail, feed failures back to the AI as correction context
4. Repeat until all tests pass (max 3 iterations)

### Phase 4: CI Validates

Standard CI pipeline runs the full test suite. TDP-generated tests are tagged for traceability:

```python
@pytest.mark.tdp(spec="tdp-spec-session-timeout")
def test_session_expires_after_inactivity(session_manager):
    ...
```

## Integration with Titan Workflow Engine

TDP is implemented as a named topology pattern in the titan workflow engine:

```yaml
# topology: test-driven-prompting
topology: tdp_pipeline
stages:
  - name: spec_intake
    agent: spec-parser
    input: tdp-spec.yaml
    output: parsed_criteria

  - name: test_generation
    agent: test-writer
    input: parsed_criteria
    output: test_suite
    validation: tests must be syntactically valid

  - name: code_generation
    agent: code-writer
    input: [parsed_criteria, test_suite]
    output: implementation
    constraint: all tests in test_suite must pass
    max_iterations: 3

  - name: ci_validation
    agent: ci-runner
    input: [test_suite, implementation]
    output: ci_report
```

### Topology Pattern Registration

```python
# titan/topologies/tdp.py
from titan.topology_engine import TopologyPattern

class TDPTopology(TopologyPattern):
    name = "test_driven_prompting"
    stages = ["spec_intake", "test_generation", "code_generation", "ci_validation"]
    max_iterations = 3  # code generation retry limit
```

## Benefits

| Benefit | Mechanism |
|---------|-----------|
| Reduced hallucination | Tests reject incorrect output before merge |
| Measurable quality | Pass rate is an objective metric |
| Executable spec | Tests serve as living documentation |
| Reproducible | Same spec produces consistent test suites |
| CI-native | Integrates with existing pytest/vitest pipelines |

## Limitations

- Test generation quality depends on spec clarity
- Edge cases may not be captured by initial spec
- Complex integration scenarios require manual test augmentation
- 3-iteration limit may be insufficient for complex features

## Reference

- `titan/topology_engine.py` — Topology pattern registration
- `titan/workflow_engine.py` — DAG-based workflow execution
- `specs/` — Existing spec format examples
