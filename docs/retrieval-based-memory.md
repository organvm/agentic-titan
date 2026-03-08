# F-19: Retrieval-Based Memory

> Replace full-history context loading with retrieval-based memory using ChromaDB vectors and aggressive context pruning.

## Problem

Full-history context loading scales linearly with session length and agent count. In multi-agent workflows, context windows fill rapidly, causing degraded reasoning quality and increased latency/cost. Agents carry irrelevant history that crowds out actionable information.

## Memory Types

### Episodic Memory (Session History)

Short-term, session-scoped memory of recent interactions and decisions.

| Property | Value |
|----------|-------|
| Storage | ChromaDB collection per session |
| TTL | Session duration + configurable retention (default 7 days) |
| Embedding | Per-turn summaries, not raw transcripts |
| Retrieval | Recency-weighted semantic search |

### Semantic Memory (Learned Facts)

Long-term knowledge distilled from interactions — facts, preferences, domain knowledge.

| Property | Value |
|----------|-------|
| Storage | Shared ChromaDB collection (cross-session) |
| TTL | Indefinite (with periodic garbage collection) |
| Embedding | Fact-level chunks with source attribution |
| Retrieval | Pure semantic similarity |

### Procedural Memory (Workflow Patterns)

Learned sequences of actions that produced successful outcomes.

| Property | Value |
|----------|-------|
| Storage | Structured records in ChromaDB + Redis cache for hot patterns |
| TTL | Indefinite (scored by success rate) |
| Embedding | Action sequences with context tags |
| Retrieval | Context-match + success-rate ranking |

## Retrieval Pipeline

```
query → embed → top-k search → rerank → inject into context
```

### Steps

1. **Query formulation**: Extract the current task description + recent 2 turns as the retrieval query
2. **Embedding**: Encode query using the same embedding model as storage (sentence-transformers default)
3. **Top-k search**: Retrieve k=20 candidates from each memory type (episodic, semantic, procedural)
4. **Rerank**: Score candidates by relevance × recency × source-type weight; select top 8-12 total
5. **Inject**: Format selected memories as structured context block, prepended to the agent prompt

### Context Budget

| Memory Type | Max Tokens | Priority |
|-------------|-----------|----------|
| Procedural | 1,000 | Highest — directly actionable |
| Semantic | 1,500 | High — factual grounding |
| Episodic | 1,000 | Medium — recent context |
| **Total** | **3,500** | Hard cap, enforced by pruner |

## Context Pruning Strategy

- **Aggressive summarization**: After every 5 turns, summarize and replace raw history
- **Relevance gating**: Memory chunks below similarity threshold (0.65) are dropped
- **Decay function**: Episodic memories decay exponentially; semantic memories do not decay
- **Per-agent budgets**: Each agent in a multi-agent workflow gets an independent memory budget

## Integration

### Memory Adapter in Titan

```python
# titan/memory.py
class MemoryAdapter:
    """Pluggable memory backend for titan agents."""

    def store(self, memory_type: MemoryType, content: str, metadata: dict) -> str: ...
    def retrieve(self, query: str, memory_types: list[MemoryType], top_k: int = 12) -> list[MemoryChunk]: ...
    def prune(self, session_id: str, max_tokens: int = 3500) -> PruneResult: ...
```

### Agent Configuration

```yaml
# agent spec
memory:
  enabled: true
  backend: chromadb          # chromadb | redis | in-memory
  types: [episodic, semantic, procedural]
  context_budget: 3500       # max tokens for memory injection
  pruning:
    summarize_interval: 5    # turns between summarization
    similarity_threshold: 0.65
    episodic_decay_half_life: 24h
```

## Reference

- `hive/` — Redis state management, ChromaDB vector storage
- `hive/chromadb_store.py` — Existing vector store integration
- `hive/redis_state.py` — Pub/sub events and state caching
