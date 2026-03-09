# Plan: Documentation & Repository Cleanup

**Session Goal**: Create project README, update roadmap, commit all changes, and verify repository state.

---

## Current State

### Uncommitted Work (from prior session)
- `.github/workflows/ci.yml` - CI pipeline (new)
- `eslint.config.js` - ESLint flat config (new)
- `shared/api-types.ts` - Shared TypeScript types (new)
- `src/__tests__/setup.ts` - Test setup (new)
- `src/__tests__/unit/*.test.ts` - 59 unit tests (new)
- `unity/` - Unity client scaffold (new)
- `package.json`, `vitest.config.ts` - Updated configs

### Missing Documentation
- No `README.md` at project root
- Roadmap in plan file needs progress update

---

## Task Sequence

### 1. Create README.md with Hero Section

**File**: `/Users/4jp/Workspace/my-block-warfare/README.md`

**Structure**:
```markdown
# TurfSynth AR

## The Problem
Location-based games lack true environmental synthesis - they overlay static content on the real world rather than generating unique experiences from the player's actual surroundings.

## The Approach
TurfSynth AR extracts "Place Fingerprints" (compact environmental feature vectors) from camera, microphone, and sensors to procedurally generate creatures, soundscapes, and visuals that are unique to each location.

## The Outcome
A turf-control game where your neighborhood literally builds the game around you - every block sounds and looks like itself, and every player's experience is different.

[Full content below with setup instructions, architecture overview, development commands]
```

### 2. Update Roadmap Progress

Update plan file to reflect completed Week 1 work:
- ✅ Unit tests (59 passing)
- ✅ CI/CD pipeline
- ✅ Unity project structure
- ✅ Shared API types

### 3. Git Commit & Push

```bash
# Stage all new/modified files
git add README.md .github/ eslint.config.js shared/ src/__tests__/ unity/ package.json package-lock.json vitest.config.ts

# Commit with descriptive message
git commit -m "Add test suite, CI pipeline, Unity scaffold, and project README

- 59 unit tests for influence-manager, zone-checker, raid-engine
- GitHub Actions CI with PostgreSQL/PostGIS and Redis services
- Unity project structure with AR Foundation integration
- Shared TypeScript types for API contract
- ESLint flat config for TypeScript
- Project README with hero section and setup instructions

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Push to remote
git push origin main
```

### 4. Verify Repository State

```bash
git status           # Should show clean working tree
git log -1 --oneline # Confirm commit
git remote -v        # Verify remote
```

---

## Files to Create/Modify

| File | Action | Content |
|------|--------|---------|
| `README.md` | CREATE | Hero section + setup + architecture |
| Plan file | UPDATE | Mark Week 1 complete |

---

## Verification

- [ ] README.md exists with hero section (problem/approach/outcome)
- [ ] All 59 tests still pass (`npm run test -- --run`)
- [ ] Git status shows clean working tree
- [ ] Remote repository matches local

---

# ARCHIVED: Previous Roadmap

The detailed "There-&-Back-Again" roadmap is preserved below for reference.

---

# 📊 EVALUATION REPORT (Evaluation-to-Growth Framework)

**Mode**: Autonomous | **Format**: Markdown Report | **Date**: 2026-01-29

---

## PHASE 1: EVALUATION

### 1.1 Critique — Holistic Assessment

#### Strengths ✓

| Strength | Evidence | Impact |
|----------|----------|--------|
| **Clear phased structure** | 6 phases with week-by-week breakdown | High - Enables incremental delivery |
| **Concrete hour estimates** | "68h", "92h", "88h" per component | High - Enables resource planning |
| **Technical depth** | H3 cells, PostGIS, influence decay formulas | High - Demonstrates feasibility |
| **Risk awareness** | Risk matrix with mitigations | Medium - Proactive problem-solving |
| **Exit criteria defined** | Each phase has measurable gates | High - Prevents scope creep |
| **ASCII visualizations** | Journey map, core loop diagram | Medium - Aids comprehension |

#### Weaknesses ✗

| Weakness | Specific Example | Severity |
|----------|------------------|----------|
| **Platform mismatch** | Plan references `ios/Sources/`, `android/app/`, `Assets/Scripts/` but codebase is **pure Node.js backend** | **Critical** |
| **Missing tests** | `src/__tests__/` is empty despite plan claiming "80% coverage" target | **Critical** |
| **No CI/CD exists** | Phase 0 lists "CI/CD pipeline" as deliverable but no `.github/workflows/` or equivalent | **High** |
| **Unity/Unreal unresolved** | "iOS/Android, Unity/Unreal" mentioned without decision | **High** |
| **Art pipeline undefined** | "120h art" with no asset format, tool, or integration spec | **Medium** |
| **No monitoring** | Phase 0 deliverable but no APM/logging code visible | **Medium** |

#### Priority Areas for Improvement

1. **Align plan with actual codebase architecture** — Plan describes cross-platform mobile but implementation is server-only
2. **Add test suite immediately** — Zero tests creates massive technical debt
3. **Define mobile/client technology stack** — Cannot estimate art or UX work without this
4. **Bootstrap CI/CD** — Critical for sustainable development

---

### 1.2 Logic Check — Internal Consistency

#### Contradictions Found

| Contradiction | Location | Resolution |
|---------------|----------|------------|
| Plan says "Week 2-4: ios/Sources/Fingerprint/*.swift" but no iOS code exists | Phase 1B | Codebase is server-side only; fingerprint service runs on backend |
| "Fingerprint: <500ms on iPhone 12 / Pixel 6" but fingerprint service is server-side | Phase 1 Exit Criteria | Metric doesn't apply; need client-side extraction metrics |
| "80% coverage" target but test infrastructure unused | Verification Strategy | Zero tests written despite Vitest configured |
| "DevOps (part-time, setup only)" but no DevOps artifacts exist | Phase 0 | CI/CD, monitoring, infrastructure-as-code all missing |

#### Reasoning Gaps

1. **Client-server boundary undefined** — Where does fingerprint extraction happen? Plan implies device but code runs on server
2. **Real-time sync missing from Phase 2** — Turf mechanics need live updates but no WebSocket/SSE infrastructure
3. **Asset delivery unspecified** — "30 archetypes with evolution chains" but no CDN, asset bundling, or streaming strategy

#### Unsupported Claims

- "10k req/s, <100ms p95" — No load testing infrastructure or benchmarks
- "$0.10/DAU/month" — No cost modeling, database sizing, or cloud estimates

#### Coherence Recommendations

1. Split plan into **Server Roadmap** vs **Client Roadmap**
2. Add explicit **API Contract** phase between backend and mobile
3. Define **client technology decision** (React Native / Flutter / Unity) before Phase 2

---

### 1.3 Logos Review — Rational Appeal

| Dimension | Assessment | Score |
|-----------|------------|-------|
| **Argument clarity** | Phase structure is logical; dependencies clear | 8/10 |
| **Evidence quality** | Hour estimates lack historical basis; no velocity data | 4/10 |
| **Persuasive strength** | Compelling vision but execution details thin | 6/10 |

#### Enhancement Recommendations

- Add **"Why These Estimates"** section with assumptions (e.g., "8h Zone Checker assumes PostGIS experience")
- Include **benchmarks from prior work** or industry comparables
- Define **spike/research tasks** separately from implementation tasks

---

### 1.4 Pathos Review — Emotional Resonance

| Dimension | Assessment |
|-----------|------------|
| **Current tone** | Technical, methodical, process-oriented |
| **Audience connection** | Strong for engineers; weak for stakeholders/investors |
| **Engagement level** | Medium — dense but lacks narrative momentum |

#### Recommendations

- Add **"Why This Matters"** section connecting to player experience
- Include **mockups or wireframes** to make tangible
- Add a **"Day in the Life"** scenario showing gameplay flow

---

### 1.5 Ethos Review — Credibility

| Dimension | Assessment |
|-----------|------------|
| **Perceived expertise** | High — technical depth signals competence |
| **Trustworthiness signals** | Risk matrix, exit criteria build confidence |
| **Authority markers** | Lacking — no prior project references, team bios |

#### Credibility Recommendations

- Reference **prior location-based game work** if applicable
- Add **technology choice rationale** ("Why Fastify over Express", "Why H3 over S2")
- Include **external validation** (performance of H3-js, PostGIS benchmarks)

---

## PHASE 2: REINFORCEMENT — Synthesis

### Key Contradictions to Resolve

| Issue | Current State | Recommended Fix |
|-------|---------------|-----------------|
| Mobile platform undefined | "Unity/Unreal" mentioned | **DECIDE**: React Native for MVP simplicity OR Unity for AR quality |
| Fingerprint location ambiguous | Server-side code, client-side metrics | **CLARIFY**: Client extracts → Server validates → Server stores |
| Test coverage 0% vs 80% target | Empty test directory | **PRIORITIZE**: Add geofencing + influence unit tests immediately |
| No CI/CD | No automation | **ADD**: GitHub Actions for lint, test, typecheck |

### Coherence Improvements

1. **Rename Phase 1B** from "Place Fingerprint" to "Fingerprint Server" — clarify it's backend
2. **Add Phase 1C: Mobile SDK Stub** — placeholder client that calls APIs
3. **Move "Device Profiling" to Phase 4** — requires real devices, not Week 4

---

## PHASE 3: RISK ANALYSIS

### 3.1 Blind Spots — Hidden Assumptions

| Hidden Assumption | Reality Check | Risk |
|-------------------|---------------|------|
| "Single senior engineer" can build cross-platform AR app | Requires iOS/Android/Unity expertise | **High** — Skill gap |
| OSM data is sufficient for zone coverage | OSM school/hospital data varies by region | **Medium** — May need SafeGraph |
| "10k users" in alpha can be supported by single PostgreSQL | Depends on query patterns | **Medium** — Need connection pooling |
| Players will accept async-only raids | Competitors offer real-time PvP | **Low** — Design choice, not bug |

### Overlooked Perspectives

1. **Accessibility** — Only mentioned in final checklist; no design-phase consideration
2. **Offline mode** — Plan mentions "Offline Queue" but no sync conflict resolution
3. **Moderation** — No content moderation for user-reported zones or crew names
4. **Localization** — No i18n mentioned; limits international launch

### Mitigation Strategies

- **Hire/contract mobile specialist** for Phase 2 if building native
- **Evaluate OSM coverage** for target pilot cities before launch
- **Add pgBouncer** and read replicas to Phase 4 infrastructure

---

### 3.2 Shatter Points — Critical Vulnerabilities

| Vulnerability | Severity | Attack Vector | Mitigation |
|---------------|----------|---------------|------------|
| **Zero tests** | Critical | Any change could break production | Write tests for influence-manager, zone-checker first |
| **No client exists** | Critical | Cannot demo or alpha test | Define mobile stack, build stub in Week 5-6 |
| **Hardcoded influence values** | High | Balance changes require deploys | Add config table or feature flags |
| **No rate limiting implementation** | High | DoS, abuse | Already in package.json; wire to Fastify |
| **Raid resolution is synchronous** | Medium | Long raids block API | Move to background job queue |

### Contingency Preparations

- **If OSM data fails**: Pivot to user-submitted zones with admin approval
- **If device fingerprinting too slow**: Reduce feature count, use simpler visual hash
- **If Unity licensing prohibits**: Fall back to React Native + AR.js

---

## PHASE 4: GROWTH

### 4.1 Bloom — Emergent Insights

#### Emergent Themes

1. **The codebase is ahead of the plan** — Backend infrastructure for Phase 1A, 1B, 2B largely complete
2. **The plan is ahead of the codebase** — Mobile, AR, Synthling generation (2A) not started
3. **Testing and DevOps are the gap** — Infrastructure code exists but no CI, no tests

#### Expansion Opportunities

| Opportunity | Effort | Impact |
|-------------|--------|--------|
| **Add LLM-generated Synthling names/lore** | 8h | High — differentiator |
| **Real-time influence map with WebSockets** | 16h | Medium — engagement |
| **Crew chat/coordination** | 24h | Medium — retention |
| **Seasonal events tied to real weather** | 12h | High — novelty |

#### Novel Angles

- **Passive mode**: Earn influence just by moving through territory (no fingerprinting required)
- **AR spectator mode**: Watch crews battle for your neighborhood without playing
- **Physical meetup incentives**: Bonus influence when multiple crew members are co-located

#### Cross-Domain Connections

- Urban planning data → dynamic district boundaries
- Transit APIs → influence bonuses near stations
- Weather APIs → spawn rate modifiers

---

### 4.2 Evolve — Iterated Plan Revisions

#### Summary of Changes

| Section | Before | After |
|---------|--------|-------|
| Phase 0 | Assumed mobile setup | **Add decision point**: Native vs Cross-platform vs Unity |
| Phase 1 | Mixed client/server | **Split**: 1A Server, 1B Server, 1C Client Stub |
| Phase 2A | Synthling Gen | **Clarify**: Server-side attribute generation, Client-side rendering |
| Testing | Mentioned in exit criteria | **New section**: Test Plan with specific files |
| CI/CD | Not present | **New section**: Automation Pipeline |

#### Risk Mitigations Applied

- ✅ Added test plan section
- ✅ Added CI/CD pipeline specification
- ✅ Clarified client-server boundary
- ✅ Added technology decision checkpoint

---

## EVALUATION SUMMARY

| Category | Score | Key Finding |
|----------|-------|-------------|
| **Critique** | 6/10 | Good structure, but plan-code mismatch |
| **Logic** | 5/10 | Multiple contradictions (mobile vs server) |
| **Logos** | 6/10 | Clear arguments, weak evidence |
| **Pathos** | 5/10 | Technical but lacks vision narrative |
| **Ethos** | 7/10 | Demonstrates competence |
| **Blind Spots** | 4/10 | Accessibility, moderation, offline missing |
| **Shatter Points** | 3/10 | Zero tests is critical vulnerability |

### Top 5 Actions Required

1. **Write tests for `influence-manager.ts` and `zone-checker.ts`** — 8h
2. **Add GitHub Actions CI** (lint, typecheck, test) — 4h
3. **Choose mobile framework** (React Native recommended for MVP speed) — 2h decision
4. **Create API contract documentation** (OpenAPI spec) — 4h
5. **Add WebSocket infrastructure for live influence updates** — 12h

---

*End of Evaluation Report*

---

# 🔄 EVOLVED PLAN — Post-Evaluation Corrections

Based on the evaluation above, here is the corrected roadmap reflecting actual codebase state and addressing critical gaps.

---

## Current Implementation Status

### ✅ Completed (Phase 1-2 Backend)

| Component | Files | Status |
|-----------|-------|--------|
| **Geofencing** | `src/services/geofencing/*.ts` | ✅ h3-cache, zone-checker, zone-sync, speed-validator, spoof-detector |
| **Fingerprint Server** | `src/services/fingerprint/*.ts` | ✅ color-extractor, audio-pipeline, visual-pipeline, assembler, validation-gate, capture-manager |
| **Turf Mechanics** | `src/services/turf/*.ts` | ✅ influence-manager, outpost-manager, raid-engine |
| **API Endpoints** | `src/api/v1/*.ts` | ✅ location, fingerprint, turf routes |
| **Database** | `src/db/migrations/*.sql` | ✅ 3 migrations (geofencing, fingerprint, turf) |
| **Types** | `src/types/*.ts` | ✅ geofencing, fingerprint, turf, synthling |
| **Server** | `src/server.ts` | ✅ Fastify with CORS, rate limiting |

### ❌ Not Started (Critical Gaps)

| Component | Planned Location | Issue |
|-----------|------------------|-------|
| **Unit Tests** | `src/__tests__/*.test.ts` | Empty directory, 0% coverage |
| **CI/CD** | `.github/workflows/*.yml` | No automation pipeline |
| **Mobile Client** | `ios/`, `android/`, or `apps/mobile/` | No client code exists |
| **Synthling Generator** | `Assets/Scripts/Synthlings/*` | Plan assumes Unity; no engine chosen |
| **Monitoring/APM** | N/A | Pino logging only; no metrics |

---

## Revised Phase Structure

### Phase 1: Foundation (MOSTLY COMPLETE)

**Status**: 85% Backend Complete, 0% Client, 0% Testing

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1 REVISED                              │
├─────────────────────────────────────────────────────────────────┤
│  ✅ 1A: Safety Geofencing Backend         │ DONE               │
│  ✅ 1B: Fingerprint Server                │ DONE               │
│  ❌ 1C: Test Suite                        │ NOT STARTED        │
│  ❌ 1D: CI/CD Pipeline                    │ NOT STARTED        │
│  ❌ 1E: Mobile SDK Stub                   │ NOT STARTED        │
└─────────────────────────────────────────────────────────────────┘
```

**Remaining Work for Phase 1:**

| Task | Effort | Priority |
|------|--------|----------|
| Unit tests for `influence-manager.ts` | 4h | **P0** |
| Unit tests for `zone-checker.ts` | 4h | **P0** |
| Unit tests for `fingerprint/assembler.ts` | 4h | **P0** |
| Integration tests for API endpoints | 8h | **P1** |
| GitHub Actions: lint + typecheck + test | 4h | **P0** |
| OpenAPI spec for v1 routes | 4h | **P1** |
| **Subtotal** | **28h** | |

### Phase 2: Core Generation (PARTIAL)

**Status**: 70% Turf Backend Complete, 0% Synthling, 0% Client

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2 REVISED                              │
├─────────────────────────────────────────────────────────────────┤
│  ✅ 2A: Turf Mechanics Backend            │ DONE               │
│  ⚠️  2B: Raid Engine                      │ 80% (needs tests)  │
│  ❌ 2C: Synthling Generation Server       │ NOT STARTED        │
│  ❌ 2D: Mobile Technology Decision        │ BLOCKED            │
│  ❌ 2E: Basic Mobile App Shell            │ BLOCKED            │
└─────────────────────────────────────────────────────────────────┘
```

**Remaining Work for Phase 2:**

| Task | Effort | Priority | Dependency |
|------|--------|----------|------------|
| **DECISION: Mobile Framework** | 2h | **P0** | None |
| Synthling type system (`src/types/synthling.ts` expansion) | 4h | P1 | None |
| Synthling attribute deriver service | 8h | P1 | Types |
| Synthling spawn resolver | 6h | P1 | Deriver |
| Raid engine unit tests | 4h | P0 | None |
| Mobile app scaffold (Expo/RN or Unity) | 16h | P1 | Decision |
| **Subtotal** | **40h** | | |

---

## Immediate Action Plan (Next 2 Weeks)

### Week 1: Close Testing Gap

| Day | Task | Output |
|-----|------|--------|
| Mon | Write `influence-manager.test.ts` | 10+ unit tests |
| Tue | Write `zone-checker.test.ts` | 8+ unit tests |
| Wed | Write `raid-engine.test.ts` | 6+ unit tests |
| Thu | Integration tests for `/api/v1/location` | E2E coverage |
| Fri | GitHub Actions CI pipeline | Automated lint/test/typecheck |

### Week 2: Unity Project Setup

| Day | Task | Output |
|-----|------|--------|
| Mon | Create Unity project with AR Foundation | `unity/` directory |
| Tue | Configure AR Foundation + XR Plugin | iOS/Android AR working |
| Wed | Implement C# API client (RestSharp/UnityWebRequest) | `Scripts/Networking/ApiClient.cs` |
| Thu | Basic location permission + AR camera view | Runnable on device |
| Fri | Connect to local dev server, test location endpoint | End-to-end proof |

---

## Technology Decision: Mobile Framework

### ✅ DECIDED: Unity

**Chosen**: Unity with AR Foundation

**Rationale**:
- Best-in-class AR capabilities (ARKit/ARCore via AR Foundation)
- High-performance 3D rendering for Synthling visuals
- Unity MARS for environmental understanding
- Procedural generation tools built-in
- Long-term scalability for complex visuals

**Trade-offs Accepted**:
- Separate codebase (C# client vs TypeScript server)
- Longer initial setup (~160h to basic playable vs ~80h for React Native)
- Unity licensing considerations for commercial release

**Project Structure**:
```
my-block-warfare/
├── src/                    # Node.js backend (TypeScript)
├── unity/                  # Unity client project
│   ├── Assets/
│   │   ├── Scripts/
│   │   │   ├── Synthlings/
│   │   │   ├── Fingerprint/
│   │   │   ├── Turf/
│   │   │   └── Networking/
│   │   ├── Shaders/
│   │   ├── Prefabs/
│   │   └── Scenes/
│   └── Packages/
└── shared/                 # Shared type definitions (generated)

---

## Test Plan (New Section)

### Unit Tests Required

| File | Test File | Priority | Key Tests |
|------|-----------|----------|-----------|
| `influence-manager.ts` | `influence-manager.test.ts` | P0 | `awardInfluence()`, `processDecay()`, `updateCellControl()` |
| `zone-checker.ts` | `zone-checker.test.ts` | P0 | `checkLocation()` allowed/blocked, `findBlockingZone()` |
| `raid-engine.ts` | `raid-engine.test.ts` | P0 | `initiateRaid()`, `resolveRaid()`, damage calculation |
| `outpost-manager.ts` | `outpost-manager.test.ts` | P1 | `deployOutpost()`, `installModule()`, `processOutpostTick()` |
| `fingerprint/assembler.ts` | `assembler.test.ts` | P1 | `assembleFingerprint()` with mock pipelines |
| `h3-cache.ts` | `h3-cache.test.ts` | P2 | Cache hit/miss, invalidation |

### Integration Tests Required

| Endpoint | Test File | Key Scenarios |
|----------|-----------|---------------|
| `POST /api/v1/location/validate` | `location.integration.test.ts` | Valid coords, blocked zone, spoof detection |
| `POST /api/v1/fingerprint/submit` | `fingerprint.integration.test.ts` | Valid submission, rate limit, invalid payload |
| `POST /api/v1/turf/raid` | `turf.integration.test.ts` | Valid raid, insufficient power, cooldown |

---

## CI/CD Pipeline (New Section)

### GitHub Actions Workflow

**File**: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgis/postgis:15-3.3
        env:
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
      redis:
        image: redis:7
        ports: ['6379:6379']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test:coverage
        env:
          DATABASE_URL: postgres://postgres:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379
```

---

## Revised Key Files to Modify

### Immediate (This Sprint)

| File | Action |
|------|--------|
| `src/__tests__/unit/influence-manager.test.ts` | **CREATE** |
| `src/__tests__/unit/zone-checker.test.ts` | **CREATE** |
| `src/__tests__/unit/raid-engine.test.ts` | **CREATE** |
| `src/__tests__/integration/location.test.ts` | **CREATE** |
| `.github/workflows/ci.yml` | **CREATE** |
| `docs/api/openapi.yaml` | **CREATE** |

### Next Sprint

| File | Action |
|------|--------|
| `unity/Assets/Scripts/Networking/ApiClient.cs` | **CREATE** |
| `unity/Assets/Scripts/Networking/LocationService.cs` | **CREATE** |
| `unity/Assets/Scripts/AR/ARSessionManager.cs` | **CREATE** |
| `unity/Assets/Scripts/Fingerprint/FingerprintCapture.cs` | **CREATE** |
| `src/services/synthling/index.ts` | **CREATE** |
| `src/services/synthling/attribute-deriver.ts` | **CREATE** |
| `shared/api-types.ts` | **CREATE** (for code generation to C#) |

---

## Updated Verification Strategy

### Phase 1 Exit Criteria (Revised)

- [x] ~~Geofencing: 10k req/s, <100ms p95~~ → **Deferred to load testing phase**
- [ ] **NEW**: Unit test coverage ≥70% for `services/` directory
- [ ] **NEW**: CI pipeline passes on all PRs
- [ ] **NEW**: OpenAPI spec documents all v1 endpoints
- [x] Fingerprint server: Compiles and type-safe ✅

### How to Verify (Local Dev)

```bash
# Run tests
npm run test

# Run with coverage
npm run test:coverage

# Typecheck
npm run typecheck

# Start server (requires PostgreSQL + Redis)
npm run dev

# Test endpoint
curl -X POST http://localhost:3000/api/v1/location/validate \
  -H "Content-Type: application/json" \
  -d '{"latitude": 37.7749, "longitude": -122.4194}'
```

---

### Unity-Specific Considerations

| Consideration | Approach |
|---------------|----------|
| **API Type Sync** | Generate C# DTOs from TypeScript types using `quicktype` or manual sync |
| **AR Foundation** | Use AR Foundation 5.x for cross-platform ARKit/ARCore support |
| **Networking** | UnityWebRequest for HTTP; consider Netcode for GameObjects for future multiplayer |
| **Location** | Unity's `LocationService` + custom H3 library (C# port or native plugin) |
| **Synthling Rendering** | Shader Graph for procedural visuals; compute shaders for generation |
| **Build Pipeline** | Unity Cloud Build or GitHub Actions with GameCI |

---

*End of Evolved Plan*

---

# ORIGINAL PLAN (Reference)

> **Note**: The original "There-&-Back-Again" roadmap is preserved below in full.
> The Evolved Plan above updates estimates and adds missing sections (tests, CI/CD)
> while maintaining the original vision and structure.

---

## The Journey Map

```
                          THERE (Build)
    ════════════════════════════════════════════════════════════►

    Week 0        Week 4        Week 8        Week 16       Week 24
    ───┼────────────┼────────────┼─────────────┼─────────────┼───
       │            │            │             │             │
       ▼            ▼            ▼             ▼             ▼
    ┌──────┐    ┌──────┐    ┌──────┐     ┌──────┐     ┌──────┐
    │ FOUN │───▶│ CORE │───▶│ MVP  │────▶│ PILOT│────▶│SCALE │
    │DATION│    │ GEN  │    │LAUNCH│     │      │     │      │
    └──────┘    └──────┘    └──────┘     └──────┘     └──────┘
       │            │            │             │             │
       ▼            ▼            ▼             ▼             ▼
    Safety      Synthlings    Full Loop    Alpha Test   Multi-City
    + Finger    + Turf        Working      10k Users    200k MAU

    ◄════════════════════════════════════════════════════════════
                        & BACK (Operate & Scale)
```

---

## Phase 0: Pre-Flight (Week 0)

### Deliverables
- [ ] Development environment setup (iOS/Android, Unity/Unreal)
- [ ] CI/CD pipeline (build, test, deploy)
- [ ] Database provisioning (PostgreSQL + PostGIS, Redis)
- [ ] Monitoring stack (APM, logging, alerting)
- [ ] H3 + zone data source accounts (OSM API, SafeGraph trial)

### Team
- 1 Senior Engineer (full-time)
- 1 DevOps (part-time, setup only)

### Exit Criteria
- Local dev builds run on simulators
- Staging environment accessible
- Geofencing DB seeded with test city data

---

## Phase 1: Foundation (Weeks 1-4)

### 1A: Safety Geofencing (Weeks 1-2) — 68h

```
Week 1                              Week 2
┌─────────────────────────────────┬─────────────────────────────────┐
│ DB Schema (4h)                  │ Speed Validator (6h)            │
│ H3 Cache Layer (6h)             │ Spoof Detector (8h)             │
│ Zone Data Model (4h)            │ Zone Data Sync (10h)            │
│ Zone Checker (8h)               │ Validation Endpoint (8h)        │
│                                 │ Integration Tests (6h)          │
│                                 │ Load Testing (8h)               │
└─────────────────────────────────┴─────────────────────────────────┘
```

**Critical Path**: Schema → Cache → Zone Checker → Endpoint

**Milestone 1.1**: Geofencing API returns valid/invalid for any GPS coordinate

### 1B: Place Fingerprint (Weeks 2-4) — 92h

```
Week 2                  Week 3                  Week 4
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ Types (4h)          │ Segmenter (8h)      │ Audio Pipeline (10h)│
│ Capture Manager (8h)│ Depth Estimator (8h)│ Motion Analyzer (4h)│
│ Model Assets (6h)   │ Visual Pipeline (4h)│ Assembler (6h)      │
│ Color Extractor (6h)│                     │ Validation Gate (4h)│
│                     │                     │ Offline Queue (6h)  │
│                     │                     │ Integration (8h)    │
│                     │                     │ Device Profiling    │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

**Critical Path**: Capture → Visual Pipeline → Assembler → Validation Gate

**Milestone 1.2**: Extract fingerprint from device camera + microphone in <500ms

### Phase 1 Exit Criteria
- [ ] Geofencing: 10k req/s, <100ms p95
- [ ] Fingerprint: <500ms on iPhone 12 / Pixel 6
- [ ] Cross-integration: Fingerprint calls geofencing before submission
- [ ] Privacy audit: No raw data leaves device

---

## Phase 2: Core Generation (Weeks 5-8)

### 2A: Synthling Generation (Weeks 5-7) — 72h eng + 120h art

```
Week 5                  Week 6                  Week 7
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ Archetype Schema(4h)│ Visual Generator(12h)│ Evolution Mgr (8h) │
│ Registry (4h)       │ Audio Generator(10h)│ Integration Tests(8h)│
│ Spawn Resolver (6h) │                     │ Performance Tune(12h)│
│ Attribute Deriver(8h)│                    │                     │
├─────────────────────┴─────────────────────┴─────────────────────┤
│                 ART (parallel): 10 archetypes (40h) → 20 more (80h)                 │
└─────────────────────────────────────────────────────────────────┘
```

**Critical Path**: Registry → Deriver → Visual Generator → Evolution

**Milestone 2.1**: Generate visually distinct Synthlings from fingerprints

### 2B: Turf Mechanics (Weeks 6-8) — 88h

```
Week 6                  Week 7                  Week 8
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ DB Schema (4h)      │ Outpost Manager (8h)│ API Endpoints (10h) │
│ Data Models (4h)    │ District Aggreg (4h)│ Integration Tests(8h)│
│ H3 Cell Setup (6h)  │ Raid Engine (12h)   │ Load Testing (8h)   │
│ Influence Mgr (8h)  │ Spawn Seeder (4h)   │                     │
│ Control Calc (6h)   │                     │                     │
│ Decay Processor (6h)│                     │                     │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

**Critical Path**: Influence → Control → District → Raid

**Milestone 2.2**: Territory changes hands through influence + raids

### Phase 2 Exit Criteria
- [ ] Synthlings: <100ms GPU generation, deterministic output
- [ ] Turf: 10k influence updates/sec, raid resolution <500ms
- [ ] Integration: Spawn rarity affected by cell control
- [ ] All 30 archetypes complete with evolution chains

---

## Phase 3: MVP Integration (Weeks 9-10)

### End-to-End Flow Validation

```
┌─────────────────────────────────────────────────────────────────┐
│                        THE CORE LOOP                            │
│                                                                 │
│   Player walks into cell                                        │
│        │                                                        │
│        ▼                                                        │
│   Location validated (Safety Geofencing) ─── Fails? ──▶ Blocked │
│        │                                                        │
│        ▼ Passes                                                 │
│   Extract fingerprint (Place Fingerprint)                       │
│        │                                                        │
│        ├──▶ Submit fingerprint ──▶ +10 Influence                │
│        │                                                        │
│        └──▶ Encounter Synthling (Synthling Gen)                 │
│                  │                                              │
│                  ▼                                              │
│             Capture ──▶ +5 Influence + Add to Collection        │
│                                                                 │
│   [Passive] Influence decays hourly                             │
│   [Async]   Raid rival outposts                                 │
│   [Goal]    Control districts, evolve Synthlings                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Integration Tasks (16h)
- [ ] Full flow smoke tests
- [ ] Cross-service contract validation
- [ ] Error handling at integration boundaries
- [ ] Real device testing (iOS + Android matrix)
- [ ] Battery drain profiling (<15% per hour)

### Phase 3 Exit Criteria
- [ ] Complete loop playable on real devices
- [ ] No crashes in 1-hour play session
- [ ] All 4 feature specs pass acceptance criteria
- [ ] Documentation complete (API docs, runbooks)

---

## Phase 4: Alpha Pilot (Weeks 11-16)

### 4A: Production Hardening (Weeks 11-12)

| Task | Effort |
|------|--------|
| Admin dashboard (zone management) | 16h |
| Analytics integration (Amplitude/Mixpanel) | 8h |
| Crash reporting (Sentry/Crashlytics) | 4h |
| Rate limiting + abuse detection | 8h |
| Feature flags (LaunchDarkly/Statsig) | 4h |
| App store preparation | 8h |

### 4B: Private Alpha (Weeks 13-16)

**Scope**: 1-2 test cities, ≤10k users

**What We Learn**:
- Real-world GPS accuracy and spoof patterns
- Fingerprint consistency across device types
- Balance: influence decay rate, spawn rates, raid outcomes
- Zone data quality (missing schools, incorrect boundaries)
- Battery and performance on diverse devices

**Success Metrics**:
| Metric | Target |
|--------|--------|
| DAU/MAU | >30% |
| Sessions/day | >2.5 |
| Crash-free sessions | >99% |
| Avg session length | >8 min |
| Synthlings captured/session | >3 |

### Phase 4 Exit Criteria
- [ ] 10k users onboarded
- [ ] No P0 bugs for 2 weeks
- [ ] Balance tuning complete
- [ ] Zone data coverage >99% for pilot cities
- [ ] Scaling runway confirmed for S1

---

## Phase 5: Scale to S1 (Weeks 17-24)

### City Pilot: 50k-200k MAU

**Infrastructure Scaling**:
| Component | Change |
|-----------|--------|
| PostgreSQL | Read replicas + connection pooling |
| Redis | Cluster mode + persistence |
| API | Horizontal scaling (K8s) |
| CDN | Asset caching + edge compute |
| Zone Data | Commercial provider integration |

**Team Scaling**:
- Engineering: 1 → 3-4
- Content/Art: 1 → 2
- Community/Support: 0 → 1
- Trust & Safety: 0 → 0.5

**Additional Features** (Phase 2 Core Loop):
- [ ] AR Visualization layer
- [ ] Multiplayer sync (presence, real-time events)
- [ ] Audio synthesis (ambient soundscapes)

### Phase 5 Exit Criteria
- [ ] 100k MAU sustained
- [ ] Infrastructure costs <$0.10/DAU/month
- [ ] 99.9% uptime over 30 days
- [ ] Support ticket volume manageable (<50/day)

---

## & Back: Sustainable Operation

### Ongoing Operations

**Weekly**:
- Zone data sync verification
- Spoof detection review queue
- Balance telemetry review

**Monthly**:
- Security audit
- Performance regression testing
- Cost optimization review
- Content refresh (events, seasonal)

**Quarterly**:
- Major feature release (Phase 3 items)
- Infrastructure review
- Team growth planning

### Content Velocity

| Content Type | Frequency | Effort |
|--------------|-----------|--------|
| New archetypes | 2/month | 12h each |
| Events | 1/month | 40h |
| Balance patches | 2/month | 8h |
| Bug fixes | Weekly | 8h/week |

---

## Risk Matrix

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Zone data gaps | High | Medium | Multiple data sources, user reporting |
| GPS spoof waves | High | Medium | Behavioral scoring, not auto-ban |
| Model too slow on older devices | Medium | Low | Tiered quality, CPU fallback |
| Privacy audit failure | Critical | Low | Pre-launch adversarial review |
| App store rejection | High | Low | Early guideline review, test builds |
| Player harassment | High | Medium | No live tracking, async only |

---

## Resource Summary

### MVP (Weeks 1-10)

| Role | Weeks | FTE-Equivalent |
|------|-------|----------------|
| Senior Engineer | 10 | 1.0 |
| Artist/3D | 6 | 0.6 (parallel) |
| DevOps | 1 | 0.1 (setup) |
| **Total** | | **~1.7 FTE** |

### Through S1 (Weeks 1-24)

| Phase | Engineering | Art | Ops/Support |
|-------|-------------|-----|-------------|
| MVP | 320h | 120h | 20h |
| Alpha | 100h | 40h | 40h |
| Scale | 200h | 80h | 80h |
| **Total** | **620h** | **240h** | **140h** |

**Cost Estimate (at $6k/EU)**:
- MVP: ~$140k
- Through S1: ~$360k

---

## Key Files to Modify

### Phase 1 (Foundation)
- `src/db/migrations/001_geofencing_schema.sql`
- `src/services/geofencing/*.ts`
- `ios/Sources/Fingerprint/*.swift`
- `android/app/src/main/java/fingerprint/*.kt`

### Phase 2 (Generation)
- `Assets/Scripts/Synthlings/*.cs`
- `Assets/Shaders/SynthlingGenerator.shader`
- `src/services/turf/*.ts`
- `src/api/v1/*.ts`

### Phase 3 (Integration)
- `src/__tests__/integration/*.test.ts`
- `docs/runbook/*.md`

---

## Verification Strategy

### Per-Phase Testing
| Phase | Test Type | Target |
|-------|-----------|--------|
| 1 | Unit + Integration | 80% coverage |
| 2 | Unit + Load | 10k/sec throughput |
| 3 | E2E + Device Matrix | 8 device configs |
| 4 | Smoke + User Acceptance | 95% task completion |

### Final Validation Checklist
- [ ] All specs pass acceptance criteria
- [ ] Load test: sustained 10k req/s
- [ ] Device test: iOS 14+, Android 10+
- [ ] Battery: <15% drain/hour
- [ ] Privacy: Adversarial audit passed
- [ ] Accessibility: VoiceOver/TalkBack basic support

---

## Summary: The Journey

```
THERE:
  Week 1-4   │ Build safety foundation + fingerprint extraction
  Week 5-8   │ Generate creatures + control territory
  Week 9-10  │ Wire it all together
  Week 11-16 │ Test with real players

& BACK:
  Week 17-24 │ Scale to city-level
  Ongoing    │ Operate, balance, expand
```

**Total MVP effort**: 440 hours (~8 dev-weeks)
**Total to city pilot**: 1,000 hours (~6 months with small team)
**First playable**: Week 10
**First public alpha**: Week 13
