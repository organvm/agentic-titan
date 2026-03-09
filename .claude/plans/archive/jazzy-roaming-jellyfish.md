# Repository Perfection Plan

## Current State: 98.13% Coverage, ~2000 Tests, Near-Production Quality

The repository is already in excellent condition. This plan addresses the remaining issues to achieve "total perfection."

---

## Phase 1: Fix Critical Bugs (Priority: CRITICAL)

### 1.1 Fix Duplicate Main Block in test_quota_lock.py
**File:** `tests/unit/test_quota_lock.py`
**Issue:** Lines 158 and 162 both have `if __name__ == "__main__":` blocks
**Fix:** Remove duplicate block

### 1.2 Fix Broken HAS_FCNTL Logic in test_quota_lock.py
**File:** `tests/unit/test_quota_lock.py`
**Issue:** Lines 15-20 have empty try block that doesn't actually import fcntl
**Fix:** Add actual `import fcntl` inside try block

### 1.3 Fix Schema File Path Mismatch
**File:** `src/automation/scripts/utils/sync-version.js`
**Issue:** References `.schema-org/` but files are in `.config/schema-org/`
**Fix:** Update paths on lines 43-67

---

## Phase 2: Fix Failing Tests (Priority: HIGH)

### 2.1 Fix 17 Failing Tests

**test_secret_manager.py (14 failures):**
- Fix subprocess mocking for 1Password CLI calls
- Ensure `subprocess.run` is properly mocked to return expected outputs
- Tests should pass without requiring actual 1Password installation

**test_sync_labels.py (2 failures):**
- `test_handles_api_error` - Fix GithubException mocking
- `test_handles_individual_repo_failures` - Fix batch error handling assertions

**test_agent_tracking.py (1 failure):**
- `test_readme_agents_sync` - Fix README sync validation

---

## Phase 3: Complete Documentation (Priority: MEDIUM)

### 3.1 Add Missing Module Docstrings
| File | Action |
|------|--------|
| `src/automation/scripts/quota_manager.py` | Add module docstring |
| `src/automation/scripts/update_agent_docs.py` | Add module docstring |

### 3.2 Fill In Documentation TODOs (47 markers)
**Key files to address:**
- `docs/workflows/PR_LIFECYCLE_AUTOMATION.md` - Fill workflow steps
- `docs/workflows/RAPID_WORKFLOW_QUICK_REF.md` - Complete quick reference
- `docs/guides/GITHUB_PROJECTS_IMPLEMENTATION.md` - TBD sections
- `docs/archive/CLEANUP_ROADMAP.md` - TBD items (or archive properly)

### 3.3 Populate API Documentation
- `docs/api/v1.2.0/README.md` - Write actual API reference content

---

## Phase 4: Package Structure (Priority: MEDIUM)

### 4.1 Add Missing `__init__.py` Files
```
src/automation/scripts/__init__.py
src/automation/scripts/utils/__init__.py
src/automation/project_meta/context-handoff/__init__.py
```

---

## Phase 5: Configuration Cleanup (Priority: LOW)

### 5.1 Update Pre-commit Baseline
```bash
git add .config/.secrets.baseline
```

### 5.2 Add Untracked Folders to .gitignore
Add to `.gitignore`:
```
# Generated/test artifacts
.github/incidents/
.github/notifications/
generated_workflows/
```

### 5.3 Remove Missing Config Reference
Either create `.config/pre-commit-dev.yaml` or remove references to it

---

## Verification

After all phases:
```bash
# 1. Run full test suite
python -m pytest --cov=src/automation -v

# 2. Run pre-commit hooks
pre-commit run --all-files

# 3. Check for remaining issues
ruff check .
mypy src/automation/

# 4. Verify versions sync
npm run version:sync
```

**Target State:**
- [ ] 0 failing tests
- [ ] 98%+ coverage maintained
- [ ] Pre-commit passes cleanly
- [ ] No TODO/FIXME in source code
- [ ] All packages have `__init__.py`
- [ ] Documentation complete

---

## Files to Modify

| File | Changes |
|------|---------|
| `tests/unit/test_quota_lock.py` | Fix duplicate main, fix HAS_FCNTL |
| `src/automation/scripts/utils/sync-version.js` | Fix schema paths |
| `tests/unit/test_secret_manager.py` | Fix mocking issues |
| `tests/unit/test_sync_labels.py` | Fix API error tests |
| `src/automation/scripts/quota_manager.py` | Add docstring |
| `src/automation/scripts/update_agent_docs.py` | Add docstring |
| `src/automation/scripts/__init__.py` | Create |
| `src/automation/scripts/utils/__init__.py` | Create |

---

## Estimated Scope
- **Critical fixes:** 3 bugs in code
- **Test fixes:** 17 failing tests (proper mocking)
- **Documentation:** 2 docstrings + 47 TODO markers to fill + API docs
- **New files:** 3-4 `__init__.py` files
- **Config:** .gitignore updates, pre-commit baseline

## Execution Order
1. Phase 1 (Critical bugs) - Do first, quick wins
2. Phase 2 (Test fixes) - Restore green CI
3. Phase 4 (Package structure) - Quick, no risk
4. Phase 5 (Config cleanup) - Quick
5. Phase 3 (Documentation) - Largest effort, do last
