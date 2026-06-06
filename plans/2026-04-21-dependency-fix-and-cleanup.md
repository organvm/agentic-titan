# agentic-titan: Dependency Fix & Cleanup

**Date:** 2026-04-21
**Status:** EXECUTED

## Context
agentic-titan had a pydantic-core version mismatch (system Python: pydantic 2.13.2 vs pydantic-core 2.46.2) blocking 57+ test files from collecting (only 313 of ~1,561 tests loaded). One stale remote branch remained from merged PR #39.

## Plan (logical order)

### 1. Fix pydantic-core dependency mismatch
- Created project `.venv` (was running against system Python — root cause of version skew)
- Installed `pip install -e ".[dev,dashboard]"` for full test coverage
- Result: pydantic 2.13.3 + pydantic-core 2.46.3 (matched pair)

### 2. Fix test failures
- **Bug 1:** `train()` method used `"test" in str(filepath)` which matched pytest's temp directory path, skipping all test fixture files. Fixed to `"test" in filepath.name`.
- **Bug 2:** Test asserted `type_annotations` pattern detection, but extraction logic was specified (PatternType.TYPING enum exists, StyleProfile.type_annotations field exists) but never wired into `_extract_idiom_patterns`. Added AST-based return-annotation detection.

### 3. Run full test suite
- Before: 313 collected, 57 errors, 1 failure
- After: 1,561 collected, 0 errors, 1,544 passed, 18 skipped

### 4. Clean up stale remote branch
- Deleted `feat/local-inference-f22-f23-f24` (PR #39 merged 2026-03-08)

## Pre-existing issues observed (not addressed — scope discipline)
- `hashlib`, `json` unused imports (lines 16-17)
- `_extract_naming_patterns` is a stub (records stats, returns `[]`)
- `max(cases, key=cases.get)` Pyright type error (line 210)
- `get_style_context()` calls `StyleAdapter.get_prompt_context()` which doesn't exist (line 267) — will raise AttributeError at runtime

## Verification
- `python3 -c "import pydantic; print(pydantic.VERSION)"` — 2.13.3, no SystemError
- `pytest --co -q` — 1,561 collected, 0 errors
- `pytest -q` — 1,544 passed, 18 skipped
- `git branch -r` — only `origin/main`
