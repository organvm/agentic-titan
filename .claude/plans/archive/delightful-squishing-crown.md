# Phase 20: Comprehensive Enhancement

Complete MCP enhancement, CLI expansion, Dashboard UI, and Expansive Inquiry features.

---

## Summary

| Area | New Files | Modified Files | Est. Tests |
|------|-----------|----------------|------------|
| 20A: MCP Server | 3 | 1 | ~25 |
| 20B: CLI Commands | 0 | 1 | ~30 |
| 20C: Dashboard UI | 4 templates, 2 routes | 2 | ~20 |
| 20D: Inquiry Features | 4 | 3 | ~80 |

**Total: ~155 new tests, ~2500 lines**

---

## Phase 20A: MCP Server Enhancement

### New Files

**`mcp/prompts.py`** - MCP Prompts API
```python
# Prompts: expansive-inquiry, quick-inquiry, creative-inquiry, model-comparison, route-task
# MCPPrompt, MCPPromptArgument dataclasses
# get_inquiry_prompts(), get_prompt_messages()
```

**`mcp/resources.py`** - Resource handlers
```python
# Resources:
# - titan://learning/stats
# - titan://learning/rlhf/stats
# - titan://models/signatures
# - titan://topology/current
# - titan://hive/events/recent
```

**`mcp/notifications.py`** - Real-time notifications
```python
# NotificationManager class
# Events: agent/state, topology/changed, inquiry/stage, learning/feedback
```

### Modify `mcp/server.py`

Add:
- Prompts handlers (prompts/list, prompts/get)
- New tools: `route_cognitive_task`, `compare_models`, `start_inquiry`, `inquiry_status`
- Resource handlers for learning/models/topology
- NotificationManager integration with EventBus

---

## Phase 20B: CLI Commands

### Modify `titan/cli.py`

**Inquiry Commands** (`titan inquiry`)
```
titan inquiry start <topic> --workflow expansive --run
titan inquiry compare <id1> <id2> --format table
titan inquiry export <id> --output file.md
titan inquiry status <id>
titan inquiry list
```

**Knowledge Commands** (`titan knowledge`)
```
titan knowledge search <query> --limit 10 --tag <tag>
titan knowledge explore --topic <topic> --interactive
titan knowledge export output.json --format json
titan knowledge stats
```

**Workflow Commands** (`titan workflow`)
```
titan workflow execute <name> --topic <topic> --mode staged
titan workflow visualize <name> --format mermaid
titan workflow list
titan workflow validate <file.yaml>
```

---

## Phase 20C: Dashboard UI

### New API Routes

**`titan/api/analysis_routes.py`**
```python
POST /api/analysis/contradictions/detect
POST /api/analysis/dialectic/synthesize
GET  /api/analysis/inquiry/{session_id}/contradictions
```

**`titan/api/knowledge_routes.py`**
```python
GET /api/knowledge/search?query=...
GET /api/knowledge/graph?depth=2
GET /api/knowledge/stats
```

### New Templates

**`dashboard/templates/inquiry.html`** - Session list + quick start
**`dashboard/templates/inquiry_detail.html`** - Stage timeline + results
**`dashboard/templates/analysis.html`** - Contradiction matrix + dialectic flow
**`dashboard/templates/knowledge.html`** - D3.js force graph browser

### Modify Files

- `dashboard/app.py` - Add routes for /inquiry, /analysis, /knowledge
- `dashboard/templates/base.html` - Add nav links

---

## Phase 20D: Expansive Inquiry Features

### D1: Conversational Interleaving

**New dataclass in `inquiry_config.py`:**
```python
@dataclass
class UserInterjection:
    content: str
    injected_at_stage: int
    influence_mode: str  # "context" | "redirect" | "clarify"
```

**New InquiryStatus:** `PAUSED`

**New engine methods:**
- `pause_session(session_id)` - Pause at next stage boundary
- `inject_user_input(session_id, content, mode)` - Add interjection
- `resume_session(session_id)` - Resume execution

**New API endpoints:**
- `POST /{session_id}/pause`
- `POST /{session_id}/inject`
- `POST /{session_id}/resume`

---

### D2: Narrative Mode

**New file: `titan/workflows/narrative_synthesizer.py`**
```python
class NarrativeSynthesizer:
    async def synthesize(session, config) -> NarrativeSynthesis

@dataclass
class NarrativeConfig:
    style: str  # academic, journalistic, conversational, poetic
    target_length: str  # brief, medium, comprehensive
    preserve_stage_voices: bool
    highlight_contradictions: bool
```

**New engine method:** `generate_narrative(session_id, config)`

**New API:** `POST /{session_id}/narrative`

---

### D3: Temporal Re-Inquiry

**New file: `titan/workflows/inquiry_temporal.py`**
```python
class TemporalTracker:
    def create_chain(topic, session_id) -> TemporalChain
    async def compute_diff(base, comparison) -> InquiryDiff

@dataclass
class TemporalChain:
    chain_id: str
    topic: str
    sessions: list[str]  # Chronological session IDs

@dataclass
class InquiryDiff:
    stage_diffs: list[StageDiff]
    overall_drift_score: float
    key_changes: list[str]
```

**New session fields:** `parent_session_id`, `chain_id`, `version`

**New API endpoints:**
- `POST /{session_id}/re-inquire`
- `GET /{session_id}/diff/{other_id}`
- `GET /chains`

---

### D4: Visualization Stage

**New stage in `inquiry_config.py`:**
```python
VISUALIZATION_STAGE = InquiryStage(
    name="Visualization Design",
    role="Visual AI",
    cognitive_style=CognitiveStyle.PATTERN_RECOGNITION,
    dependencies=[5],  # After Pattern Recognition
)
```

**New file: `titan/workflows/visualization_generator.py`**
```python
class VisualizationGenerator:
    def parse_visualization_output(content) -> VisualizationSuite

@dataclass
class VisualizationSpec:
    viz_type: VisualizationType  # radar, bar, sankey, force, treemap
    library: VisualizationLibrary  # chartjs, d3
    config: dict
    data: dict
```

**New API:** `GET /{session_id}/visualizations`

---

### D5: Stage Personality Modulation

**New dataclasses in `inquiry_config.py`:**
```python
@dataclass
class PersonalityVector:
    tone: float        # -1=formal, +1=casual
    abstraction: float # -1=concrete, +1=abstract
    verbosity: float   # -1=terse, +1=comprehensive
    creativity: float  # -1=conventional, +1=experimental
    technicality: float # -1=accessible, +1=expert

PRESET_PERSONALITIES = {
    "academic": PersonalityVector(tone=-0.5, technicality=0.7, ...),
    "conversational": PersonalityVector(tone=0.6, technicality=-0.5, ...),
    "creative": PersonalityVector(creativity=0.8, ...),
}
```

**New file: `titan/workflows/personality_modulator.py`**
```python
class PersonalityModulator:
    def modulate_prompt(base_prompt, vector) -> str
```

**Integration:** Modify `_build_stage_prompt` to apply modulation

---

## Execution Order

### Week 1: Foundation
1. **20A-1**: Create `mcp/prompts.py` with inquiry prompts
2. **20A-2**: Create `mcp/resources.py` with learning/models resources
3. **20B-1**: Add `titan inquiry` commands to CLI
4. **20D-5**: Implement PersonalityVector and modulator (simplest)

### Week 2: Core Features
5. **20D-1**: Implement conversational interleaving (pause/resume)
6. **20B-2**: Add `titan knowledge` and `titan workflow` commands
7. **20C-1**: Create analysis_routes.py and knowledge_routes.py
8. **20A-3**: Create `mcp/notifications.py` and integrate

### Week 3: Advanced Features
9. **20D-4**: Implement Visualization Stage
10. **20D-2**: Implement Narrative Mode synthesizer
11. **20C-2**: Create dashboard templates (inquiry, analysis, knowledge)

### Week 4: Completion
12. **20D-3**: Implement Temporal Re-Inquiry tracking
13. **20C-3**: Dashboard integration and polish
14. Full integration testing

---

## Critical Files

### Create
- `mcp/prompts.py`
- `mcp/resources.py`
- `mcp/notifications.py`
- `titan/api/analysis_routes.py`
- `titan/api/knowledge_routes.py`
- `titan/workflows/narrative_synthesizer.py`
- `titan/workflows/inquiry_temporal.py`
- `titan/workflows/visualization_generator.py`
- `titan/workflows/personality_modulator.py`
- `dashboard/templates/inquiry.html`
- `dashboard/templates/inquiry_detail.html`
- `dashboard/templates/analysis.html`
- `dashboard/templates/knowledge.html`

### Modify
- `mcp/server.py` - Add prompts, resources, notifications
- `titan/cli.py` - Add inquiry, knowledge, workflow commands
- `titan/workflows/inquiry_config.py` - Add new dataclasses
- `titan/workflows/inquiry_engine.py` - Add pause/resume, narrative, personality
- `titan/api/inquiry_routes.py` - Add new endpoints
- `dashboard/app.py` - Add new routes
- `dashboard/templates/base.html` - Add navigation

---

## Test Files

- `tests/mcp/test_prompts.py` (~10 tests)
- `tests/mcp/test_resources.py` (~10 tests)
- `tests/mcp/test_notifications.py` (~5 tests)
- `tests/cli/test_inquiry_commands.py` (~15 tests)
- `tests/cli/test_knowledge_commands.py` (~10 tests)
- `tests/cli/test_workflow_commands.py` (~5 tests)
- `tests/api/test_analysis_routes.py` (~10 tests)
- `tests/api/test_knowledge_routes.py` (~10 tests)
- `tests/workflows/test_conversational.py` (~20 tests)
- `tests/workflows/test_narrative.py` (~15 tests)
- `tests/workflows/test_temporal.py` (~15 tests)
- `tests/workflows/test_visualization.py` (~15 tests)
- `tests/workflows/test_personality.py` (~15 tests)

---

## Verification

```bash
# Run new tests
pytest tests/mcp/ tests/cli/ tests/workflows/test_conversational.py -v

# Full test suite
pytest tests/ -v

# Manual verification
titan inquiry start "test topic" --workflow expansive
titan knowledge search "test"
titan workflow list

# Dashboard
titan dashboard start --port 8080
# Visit http://localhost:8080/inquiry
```
