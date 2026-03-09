# Test Coverage Improvement Plan - 100% Target

## Current State

| Metric | Value |
|--------|-------|
| **Current Coverage** | 98.13% |
| **Target Coverage** | 100% |
| **Tests Passing** | 1958 |
| **Phase 1** | ✅ COMPLETE (commit 1f8cb85) |
| **Phase 2** | ✅ COMPLETE (10/10 scripts done) |
| **Phase 3** | ✅ COMPLETE (13/13 scripts done) |
| **Phase 4** | ✅ COMPLETE (6/6 scripts done) |
| **Phase 5** | ✅ COMPLETE (9/9 scripts done) |
| **Phase 6** | ✅ COMPLETE (commit cfade52) |
| **Phase 7** | ✅ COMPLETE (2/3 scripts done) |

---

## Phase 2: Expand Low-Coverage Tests (73% → 85%) - COMPLETE

Scripts with existing tests that need expansion:

| Script | Before | After | Status |
|--------|--------|-------|--------|
| `notification_manager.py` | 57% | 100% | ✅ COMPLETE |
| `predict_workflow_failures.py` | 58% | 99% | ✅ COMPLETE |
| `intelligent_routing.py` | 64% | 98% | ✅ COMPLETE |
| `validation_framework.py` | 65% | 100% | ✅ COMPLETE |
| `sla_monitor.py` | 67% | 100% | ✅ COMPLETE |
| `incident_response.py` | 70% | 99.61% | ✅ COMPLETE |
| `check_auto_merge_eligibility.py` | 73% | 100% | ✅ COMPLETE |
| `ab_test_assignment.py` | 44% | 98% | ✅ COMPLETE |
| `ecosystem_visualizer.py` | 48% | 100% | ✅ COMPLETE |
| `utils.py` | 52% | 97% | ✅ COMPLETE |

---

## Phase 3: New Tests for Complex Scripts (85% → 95%) - COMPLETE

Scripts >400 lines without any tests:

| Script | Lines | Coverage | Status |
|--------|-------|----------|--------|
| `self_healing.py` | 801 | 100% | ✅ COMPLETE |
| `enhanced_analytics.py` | 716 | 95% | ✅ COMPLETE |
| `configure-github-projects.py` | 789 | 100% | ✅ COMPLETE |
| `notification_integration.py` | 692 | 100% | ✅ COMPLETE |
| `proactive_maintenance.py` | 680 | 96% | ✅ COMPLETE |
| `batch_onboard_repositories.py` | 608 | 73% | ✅ COMPLETE |
| `pre_deployment_checklist.py` | 500 | 96% | ✅ COMPLETE |
| `auto-docs.py` | 566 | 97% | ✅ COMPLETE |
| `generate_pilot_workflows.py` | 466 | 97% | ✅ COMPLETE |
| `evaluate_repository.py` | 425 | 100% | ✅ COMPLETE |
| `generate_email_digest.py` | 410 | 100% | ✅ COMPLETE |
| `update-action-pins.py` | 409 | 88% | ✅ COMPLETE |
| `resolve_link_placeholders.py` | 404 | 96% | ✅ COMPLETE |

---

## Phase 4: New Tests for Medium Scripts (95% → 98%) - COMPLETE

Scripts 200-400 lines without tests:

| Script | Lines | Coverage | Status |
|--------|-------|----------|--------|
| `generate_manifest.py` | 327 | 99% | ✅ COMPLETE |
| `calculate_health_score.py` | 314 | 98% | ✅ COMPLETE |
| `validate-tokens.py` (utils) | 279 | 87% | ✅ COMPLETE |
| `resolve_dependencies.py` | 208 | 100% | ✅ COMPLETE |
| `classify_failure.py` | 205 | 100% | ✅ COMPLETE |
| `validate-schema-org.py` | 201 | 96% | ✅ COMPLETE |

---

## Phase 5: New Tests for Small Scripts (98% → 100%) - COMPLETE

Scripts <200 lines without tests:

| Script | Lines | Coverage | Status |
|--------|-------|----------|--------|
| `standardize-mcp-collections.py` | 158 | 96% | ✅ COMPLETE |
| `generate_workflow_health_report.py` | 148 | 97% | ✅ COMPLETE |
| `create_default_configs.py` | 142 | 100% | ✅ COMPLETE |
| `update_agent_docs.py` | 105 | 100% | ✅ COMPLETE |
| `validate_chatmode_frontmatter.py` | 94 | 100% | ✅ COMPLETE |
| `validate_collection_frontmatter.py` | 83 | 97% | ✅ COMPLETE |
| `quick-validate.py` | 62 | 100% | ✅ COMPLETE |
| `enhanced_ml_predictions.py` | 48 | 100% | ✅ COMPLETE |
| `schedule_maintenance.py` | 40 | 100% | ✅ COMPLETE |

---

## Commits

- `1f8cb85` - Phase 1: Fix 33 failing tests
- `09ff485` - Phase 2a: notification_manager, predict_workflow_failures, intelligent_routing
- `baccee7` - Phase 2b: validation_framework, sla_monitor, incident_response, check_auto_merge_eligibility
- `0102b16` - Phase 2c: ab_test_assignment (98%), ecosystem_visualizer (100%)
- `0199f98` - Phase 3a: self_healing (100%), enhanced_analytics (95%)
- `649253b` - Phase 3b: configure-github-projects (100%), notification_integration (100%), proactive_maintenance (96%), batch_onboard_repositories (73%), pre_deployment_checklist (96%)
- `bebf60f` - Phase 3c: auto-docs (97%), generate_pilot_workflows (97%), evaluate_repository (100%), generate_email_digest (100%), update-action-pins (88%), resolve_link_placeholders (96%)
- `6e33185` - Phase 4: generate_manifest (99%), calculate_health_score (98%), validate-tokens-utils (87%), resolve_dependencies (100%), classify_failure (100%), validate-schema-org (96%)
- `be36beb` - Phase 5: 9 small scripts with 114 new tests
- `cfade52` - Phase 6: Expand 4 low-coverage scripts with 91 new tests
- `2de6629` - Phase 7: Expand validate_labels (100%), update-action-pins (97.84%) with 64 new tests

---

## Test Patterns

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

@pytest.mark.unit
class TestClassName:
    """Test group for specific functionality."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    def test_specific_behavior(self, mock_client):
        """Test description."""
        # Arrange
        mock_client.get.return_value = {"data": "value"}

        # Act
        result = function_under_test(mock_client)

        # Assert
        assert result == expected
```

---

## Verification

```bash
# Run full test suite with coverage
python -m pytest --cov=src/automation --cov-report=term-missing -v

# Verify 100% coverage
python -m pytest --cov=src/automation --cov-fail-under=100

# Run specific test file
python -m pytest tests/unit/test_<name>.py -v
```

---

## Success Criteria

- [x] Phase 1: Fix 33 failing tests
- [x] Phase 2: Expand all 10 low-coverage test files
  - ab_test_assignment: 44% → 98%, ecosystem_visualizer: 48% → 100%
- [x] Phase 3: Add tests for 13 complex scripts (>400 lines)
  - Coverage: 94.38% → 95.08%
  - Tests: 1318 → 1516
- [x] Phase 4: Add tests for 6 medium scripts (200-400 lines)
  - Coverage: 95.08% → 95.18%
  - Tests: 1516 → 1729
- [x] Phase 5: Add tests for 9 small scripts (<200 lines)
  - Coverage: 95.18% → 95.31%
  - Tests: 1729 → 1843
- [x] Phase 6: Expand remaining low-coverage scripts
  - Coverage: 95.31% → 97.62%
  - Tests: 1843 → 1911
  - web_crawler.py: 78.75% → 98.64%
  - quota_manager.py: 76.39% → 97.92%
  - sync_labels.py: 83.59% → 93.75%
  - batch_onboard_repositories.py: 72.26% → 92.70%

---

## Phase 6: Expand Remaining Low-Coverage Scripts (95% → 97.62%) - COMPLETE

Expand tests for scripts still below 90% coverage:

| Script | Before | After | Status |
|--------|--------|-------|--------|
| `web_crawler.py` | 78.75% | 98.64% | ✅ COMPLETE |
| `quota_manager.py` | 76.39% | 97.92% | ✅ COMPLETE |
| `sync_labels.py` | 83.59% | 93.75% | ✅ COMPLETE |
| `batch_onboard_repositories.py` | 72.26% | 92.70% | ✅ COMPLETE |

---

## Phase 7: Final Coverage Push (97.62% → 98.13%) - COMPLETE

Expand tests for remaining low-coverage scripts:

| Script | Before | After | Status |
|--------|--------|-------|--------|
| `validate_labels.py` | 86.57% | 100% | ✅ COMPLETE |
| `update-action-pins.py` | 87.57% | 97.84% | ✅ COMPLETE |
| `validate-tokens.py` (utils) | 87.20% | 87.20% | ⏸️ SKIPPED (requires 1Password CLI) |

---

## Remaining Gap Analysis

Current coverage: 98.13% (143 lines uncovered out of 7635)

Key uncovered areas (minor):
- `validate-tokens.py` (utils): 87.20% - requires 1Password CLI for verbose mode tests
- `enhanced_analytics.py`: 95.17% - edge cases in analytics calculations
- `proactive_maintenance.py`: 96.22% - maintenance scheduling edge cases

The remaining uncovered lines are primarily:
1. Import error handling (lines 32-34 in update-action-pins.py - requests not installed)
2. 1Password CLI interaction paths
3. Edge cases in analytics calculations
