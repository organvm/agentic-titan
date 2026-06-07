# Resume Prompt: Logos Symmetry Remediation — Session Containerization

## Quick Start (Copy & Paste)

```bash
# 1. Create worktree for this session's work
cd /Users/4jp/Code/organvm/organvm-engine
git worktree add ../organvm-engine-worktree-logos-remediation -b work/logos-remediation-2026-06-07

# 2. Navigate to the worktree
cd /Users/4jp/Code/organvm/organvm-engine-worktree-logos-remediation

# 3. Verify the fix is in place
grep -A 20 "_build_logos_context" src/organvm_engine/contextmd/generator.py | head -30

# 4. Run tests to verify
python -m pytest tests/ -q --tb=short 2>&1 | tail -20

# 5. Return to main workspace when done
cd /Users/4jp/Code/organvm/agentic-titan
```

## Resume Prompt for New Session

```
You are resuming after S-2026-06-07-logos-remediation completed. 

CONTEXT:
- Working directory: /Users/4jp/Code/organvm/agentic-titan
- Session task: Fix Logos symmetry detection in organvm-engine
- Status: COMPLETE — all work pushed, (local):(remote)={1:1}

WHAT WAS ACCOMPLISHED:
1. organvm-engine `_build_logos_context` fixed to scan all code dirs (commit 9b64725)
2. IRF-ATN-006 and IRF-ATN-009 marked completed (DONE-597/598)
3. agentic-titan Logos status corrected to ACTIVE | SYMMETRIC
4. All repos verified (local):(remote)={1:1}

VERIFICATION COMMANDS:
```bash
# Check Logos status
cd /Users/4jp/Code/organvm/agentic-titan && grep "Logos" CLAUDE.md

# Check IRF completion
cd /Users/4jp/Code/organvm/organvm-corpvs-testamentvm && organvm irf stats

# Verify sync
cd /Users/4jp/Code/organvm/organvm-corpvs-testamentvm && git fetch origin main && git status
```

HANDOFF ARTIFACTS:
- .claude/plans/2026-06-07-cross-agent-handoff.md (full context)
- .claude/plans/2026-06-07-resume-prompt.md (minimal resume)
- .claude/plans/2026-06-07-closeout-summary.md (verification)

NEXT ACTIONS:
- No immediate actions required — work is complete
- Continue with whatever task the user requests
- If exploring further: check P0/P1 items in IRF (64 P0, 430 P1)
```

## Worktree Management Commands

```bash
# List all worktrees
git worktree list

# Remove worktree when done
git worktree remove /Users/4jp/Code/organvm/organvm-engine-worktree-logos-remediation

# Or prune stale worktrees
git worktree prune
```

## Session Containerization Workflow

```bash
# 1. START: Create isolated worktree
cd /Users/4jp/Code/organvm/organvm-engine
git worktree add ../organvm-engine-$(date +%Y-%m-%d)-$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' ') -b work/session-$(date +%Y-%m-%d)

# 2. WORK: Navigate to worktree and work
cd /Users/4jp/Code/organvm/organvm-engine-*

# 3. VERIFY: Run tests in isolation
python -m pytest tests/ -q

# 4. MERGE: When ready to integrate
cd /Users/4jp/Code/organvm/organvm-engine
git merge work/session-2026-06-07

# 5. CLEANUP: Remove worktree
git worktree remove /Users/4jp/Code/organvm/organvm-engine-*
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git worktree add <path> <branch>` | Create isolated worktree |
| `git worktree list` | Show all worktrees |
| `git worktree remove <path>` | Delete worktree |
| `git worktree prune` | Clean stale worktrees |
| `git merge <branch>` | Integrate worktree work |
