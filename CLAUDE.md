# CLAUDE.md — agentic-titan

**ORGAN IV** (Orchestration) · `organvm-iv-taxis/agentic-titan`
**Status:** ACTIVE · **Branch:** `main`

## What This Repo Is

Polymorphic Agent Swarm Architecture: model-agnostic, self-organizing multi-agent system with 6 topologies, 1,095+ tests (adversarial, chaos, e2e, integration, performance, MCP, Ray), 18 completed phases.

## Stack

**Languages:** Python, HTML, JavaScript
**Build:** Python (pip/setuptools)
**Testing:** pytest (likely)

## Directory Structure

```
📁 .ci/
📁 .github/
📁 .meta/
📁 .serena/
📁 .stress-results/
📁 absorb-alchemize/
📁 adapters/
📁 agents/
📁 alembic/
📁 dashboard/
📁 data/
📁 demos/
📁 deploy/
📁 docs/
    adr
    api.md
    ci-governance-ownership.md
    ci-quality-gates.md
    claude-code-setup.md
    deploy-smoke-evidence.md
    deploy-smoke-runbook.md
    release-approver-signoff.md
    release-closure-checklist.md
    release-evidence-template.md
    ... (12 items)
📁 examples/
📁 hive/
📁 mcp/
📁 plans/
📁 runtime/
📁 specs/
📁 tests/
    adversarial
    analysis
    api
    archetypes
    auth
    batch
    chaos
    conftest.py
    e2e
    evaluation
    ... (20 items)
📁 titan/
📁 tools/
  .dbxignore
  .gitignore
  CHANGELOG.md
  GEMINI.md
  LICENSE
  README.md
  alembic.ini
  mypy.ini
  pyproject.toml
  renovate.json
  seed.yaml
```

## Key Files

- `README.md` — Project documentation
- `pyproject.toml` — Python project config
- `seed.yaml` — ORGANVM orchestration metadata
- `tests/` — Test suite

## Development

```bash
pip install -e .    # Install in development mode
pytest              # Run tests
```

## ORGANVM Context

This repository is part of the **ORGANVM** eight-organ creative-institutional system.
It belongs to **ORGAN IV (Orchestration)** under the `organvm-iv-taxis` GitHub organization.

**Dependencies:**
- organvm-i-theoria/recursive-engine--generative-entity

**Registry:** [`registry-v2.json`](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/registry-v2.json)
**Corpus:** [`organvm-corpvs-testamentvm`](https://github.com/meta-organvm/organvm-corpvs-testamentvm)

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** ORGAN-IV (Orchestration) | **Tier:** flagship | **Status:** PUBLIC_PROCESS
**Org:** `organvm-iv-taxis` | **Repo:** `agentic-titan`

### Edges
- **Produces** → `organvm-iv-taxis/agent--claude-smith`: dependency
- **Produces** → `organvm-v-logos/public-process`: dependency
- **Consumes** ← `organvm-i-theoria/recursive-engine--generative-entity`: dependency

### Siblings in Orchestration
`orchestration-start-here`, `petasum-super-petasum`, `universal-node-network`, `.github`, `agent--claude-smith`, `a-i--skills`

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-03-08T20:11:34Z*

## Session Review Protocol

At the end of each session that produces or modifies files:
1. Run `organvm session review --latest` to get a session summary
2. Check for unimplemented plans: `organvm session plans --project .`
3. Export significant sessions: `organvm session export <id> --slug <slug>`
4. Run `organvm prompts distill --dry-run` to detect uncovered operational patterns

Transcripts are on-demand (never committed):
- `organvm session transcript <id>` — conversation summary
- `organvm session transcript <id> --unabridged` — full audit trail
- `organvm session prompts <id>` — human prompts only


## Active Directives

| Scope | Phase | Name | Description |
|-------|-------|------|-------------|
| system | any | prompting-standards | Prompting Standards |
| system | any | research-standards-bibliography | APPENDIX: Research Standards Bibliography |
| system | any | research-standards | METADOC: Architectural Typology & Research Standards |
| system | any | sop-ecosystem | METADOC: SOP Ecosystem — Taxonomy, Inventory & Coverage |
| system | any | autopoietic-systems-diagnostics | SOP: Autopoietic Systems Diagnostics (The Mirror of Eternity) |
| system | any | cicd-resilience-and-recovery | SOP: CI/CD Pipeline Resilience & Recovery |
| system | any | cross-agent-handoff | SOP: Cross-Agent Session Handoff |
| system | any | document-audit-feature-extraction | SOP: Document Audit & Feature Extraction |
| system | any | essay-publishing-and-distribution | SOP: Essay Publishing & Distribution |
| system | any | market-gap-analysis | SOP: Full-Breath Market-Gap Analysis & Defensive Parrying |
| system | any | pitch-deck-rollout | SOP: Pitch Deck Generation & Rollout |
| system | any | promotion-and-state-transitions | SOP: Promotion & State Transitions |
| system | any | repo-onboarding-and-habitat-creation | SOP: Repo Onboarding & Habitat Creation |
| system | any | research-to-implementation-pipeline | SOP: Research-to-Implementation Pipeline (The Gold Path) |
| system | any | security-and-accessibility-audit | SOP: Security & Accessibility Audit |
| system | any | session-self-critique | session-self-critique |
| system | any | source-evaluation-and-bibliography | SOP: Source Evaluation & Annotated Bibliography (The Refinery) |
| system | any | stranger-test-protocol | SOP: Stranger Test Protocol |
| system | any | strategic-foresight-and-futures | SOP: Strategic Foresight & Futures (The Telescope) |
| system | any | typological-hermeneutic-analysis | SOP: Typological & Hermeneutic Analysis (The Archaeology) |

Linked skills: evaluation-to-growth


**Prompting (Anthropic)**: context 200K tokens, format: XML tags, thinking: extended thinking (budget_tokens)

<!-- ORGANVM:AUTO:END -->


## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.
