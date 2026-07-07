# Implementation 14: Three-Layer Memory (Hermes Pattern)
## Angavu Intelligence — Msaidizi Memory Architecture

**Date:** 2026-07-07
**Swarm:** Implementation Swarm 14
**Based on:** Swarm G analysis of Hermes Agent & OpenClaw architectures

---

## What Was Implemented

### 1. Android L2 Episodic Memory — `EpisodicMemory.kt`

**Path:** `app/src/main/java/com/msaidizi/app/memory/EpisodicMemory.kt`

SQLite FTS5 full-text search engine for on-device episodic memory. Stores every worker interaction with full-text indexing for sub-10ms retrieval.

**Key features:**
- **FTS5 virtual tables** with `unicode61 remove_diacritics 2` tokenizer (handles Swahili diacritics, Sheng, mixed scripts)
- **BM25 relevance ranking** combined with per-episode relevance boost
- **Automatic sync triggers** — INSERT/UPDATE/DELETE propagate to FTS index
- **Skill store** — stores auto-generated skills from the closed learning loop
- **Relevance decay** — old episodes decay over time, stale ones evicted
- **Eviction policy** — at 10K episodes, removes oldest 10% by access count + relevance
- **Privacy-first** — worker IDs are hashed, no PII stored

**API surface:**
```kotlin
// Store interaction
episodicMemory.storeEpisode(workerId, query, response, outcome, lessons, dialect, context)

// Full-text search (sub-10ms target)
val results = episodicMemory.search("When did I last restock tomatoes?", workerId)

// Skill search (closed learning loop)
val skills = episodicMemory.searchSkills("tomato pricing", workerId)

// Relevance management
episodicMemory.boostRelevance(episodeId, 0.1)
episodicMemory.runDecay()
```

**Why SQLite FTS5 over vector embeddings:**
- Zero dependencies (runs natively on Android)
- Sub-10ms latency on $50 phones (Snapdragon 450 class)
- No embedding model needed (saves 50-200MB storage)
- Works fully offline (critical for Africa's connectivity gaps)
- FTS5 BM25 is excellent for Swahili/multilingual text

---

### 2. Backend L3 User Model — Enhanced `tiered.py`

**Path:** `msaidizi-language-pipeline/agents/memory/tiered.py`

Three major additions to the existing memory system:

#### a) `SQLiteFTS5Store` — L2 Backend
Python-side SQLite FTS5 store mirroring the Android implementation. Provides:
- `store_episode()` — persist interactions with FTS5 indexing
- `search_episodes()` — FTS5 BM25 search (sub-10ms target)
- `store_skill()` / `search_skills()` — closed learning loop storage
- `run_decay()` — relevance decay and stale episode cleanup
- WAL journaling, 8MB cache for performance

#### b) `WorkerBehavioralModel` — L3 User Model
Bayesian behavioral model for each worker. Tracks:

| Belief | Default Prior | Variance | Source |
|--------|--------------|----------|--------|
| daily_revenue | 700 KES | 500 | ECO 201: Production function |
| daily_cost | 400 KES | 300 | ECO 201: Cost structure |
| profit_margin | 25% | 15% | ECO 201: Marginal analysis |
| savings_rate | 5% | 5% | ECO 206: Microfinance |
| risk_aversion | 0.6 | 0.2 | STA 142: Risk modeling |
| price_sensitivity | 0.8 | 0.15 | ECO 101: Consumer theory |
| restock_frequency_days | 3.0 | 2.0 | ECO 201: Inventory cycles |
| loyalty_to_supplier | 0.4 | 0.2 | ECO 101: Brand loyalty |

**Bayesian updating (STA 142):**
```
posterior_var = 1 / (1/prior_var + 1/obs_var)
posterior_mean = posterior_var * (prior_mean/prior_var + observation/obs_var)
```

**Predictive model:** `predict_next_need()` analyzes interaction history to anticipate:
- Restock reminders based on learned frequency
- Usual active time patterns
- Query topic patterns

**Persistence:** Each worker's model stored as JSON in SQLite `user_models` table.

#### c) Enhanced `TieredMemoryManager`
Now integrates all three tiers:
- `think()` returns L1 context + L2 FTS5 episodes + L2 skills + L3 patterns + L3 worker model + L3 predictions
- `observe_interaction()` updates all three tiers in one call
- `consolidate()` runs decay across L2 FTS5 and L3 patterns
- `get_worker_model()` provides per-worker Bayesian model access

---

### 3. Closed Learning Loop — `skill_generator.py`

**Path:** `msaidizi-language-pipeline/agents/memory/skill_generator.py`

Implements Hermes's closed learning loop — the pattern that makes Msaidizi smarter over time.

**Flow:**
```
Worker query → Start trace → Record steps → End trace
    ↓
Is complex (3+ steps)? → Was successful?
    ↓ YES                    ↓ YES
Generate skill document → Store in L2 FTS5
    ↓
Future similar query → FTS5 search → Load skill → Execute faster
```

**Key features:**
- `InteractionTrace` — captures full execution path (steps, tools, duration)
- `GeneratedSkill` — Markdown skill document with procedure, pitfalls, verification
- Category classification — pricing, inventory, savings, market, transport, records
- Academic basis tagging — each skill links to ECO/STA unit
- Confidence scoring — based on outcome quality, complexity, lessons learned
- Usage tracking — skills improve confidence when reused successfully
- FTS5 storage — skills are searchable alongside episodes

**Example generated skill:**
```markdown
# Pricing Protocol: bei ya nyanya soko

**Category:** Pricing
**Academic Basis:** ECO 201 — Producer theory: pricing decisions
**Complexity:** 4 steps

## Procedure
1. Check current wholesale price at Gikomba market
2. Calculate transport cost per kg
3. Apply standard markup (30-40% for tomatoes)
4. Compare with competitor prices in the area

## Pitfalls to Avoid
- Tomatoes spoil fast — don't overstock
- Weekend prices are usually 10-15% higher
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Worker's Phone (Android)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  L1: Working Memory (in-process, session-scoped)      │  │
│  │  Current conversation context, ~50 items              │  │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼────────────────────────────────┐  │
│  │  L2: EpisodicMemory.kt (SQLite + FTS5, on-device)     │  │
│  │  • FTS5 full-text search, BM25 ranking                │  │
│  │  • Worker interactions, outcomes, lessons              │  │
│  │  • Auto-generated skills from closed learning loop    │  │
│  │  • Sub-10ms retrieval, 10K episode capacity           │  │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │ sync when connected                │
└─────────────────────────┼────────────────────────────────────┘
                          │
┌─────────────────────────┼────────────────────────────────────┐
│                    Backend (Python)                           │
│  ┌──────────────────────▼────────────────────────────────┐  │
│  │  L2: SQLiteFTS5Store (server-side mirror)             │  │
│  │  • Same FTS5 schema as Android                        │  │
│  │  • Aggregated data from multiple workers              │  │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼────────────────────────────────┐  │
│  │  L3: WorkerBehavioralModel (Bayesian, per-worker)     │  │
│  │  • Decision patterns, risk tolerance, preferences     │  │
│  │  • Bayesian updating with each interaction            │  │
│  │  • Predictive model: what will worker need next?      │  │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼────────────────────────────────┐  │
│  │  SkillGenerator (Closed Learning Loop)                │  │
│  │  • Trace complex interactions                         │  │
│  │  • Auto-generate reusable skill documents             │  │
│  │  • Store in L2 for future retrieval                   │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Academic Alignment

| Component | Unit | Alignment |
|-----------|------|-----------|
| SQLite FTS5 BM25 | STA 142 | Probabilistic retrieval model — term frequency × inverse document frequency |
| Bayesian updating | STA 142 | Conjugate normal prior → posterior updating with each observation |
| Worker behavioral model | ECO 201 | Producer theory — learn production function, cost structure, pricing decisions |
| Predictive model | ECO 201 | Anticipate restock needs, inventory cycles based on learned patterns |
| Skill generation | ECO 201 | Capture production processes for reuse — compound learning |
| Relevance decay | STA 142 | Exponential decay prevents stale data from dominating predictions |
| Closed learning loop | ECO 201 | Self-improving system that reduces operational cost over time |
| Offline-first FTS5 | ECO 204 | Works without connectivity — critical for African infrastructure |

---

## Files Modified/Created

| File | Action | Lines |
|------|--------|-------|
| `app/src/main/java/com/msaidizi/app/memory/EpisodicMemory.kt` | **Created** | ~600 |
| `msaidizi-language-pipeline/agents/memory/tiered.py` | **Enhanced** | +400 |
| `msaidizi-language-pipeline/agents/memory/skill_generator.py` | **Created** | ~400 |

---

## Key Design Decisions

1. **SQLite FTS5 over vector embeddings** — Embedding models are 50-200MB, too large for $50 phones. FTS5 gives sub-10ms search with zero dependencies.

2. **Bayesian over ML models** — Lightweight statistical updating works on-device without GPU. STA 142 conjugate normal updates are O(1).

3. **Skills as Markdown** — Human-readable, auditable, portable. Academic team can validate each skill against ECO/STA frameworks.

4. **Worker-scoped models** — Each worker has their own Bayesian model. Boda rider patterns differ from mama mboga patterns. No cross-contamination.

5. **Relevance decay** — Prevents stale data from dominating. 30-day half-life for episodes, 60-day for patterns. Matches informal economy cycles.

6. **Closed learning loop threshold** — 3+ steps to generate a skill. Prevents skill bloat from simple interactions while capturing genuinely complex procedures.

---

*Implementation completed by Swarm 14 | Hermes memory pattern → Angavu adaptation*
