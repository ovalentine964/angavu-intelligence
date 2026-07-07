# Fix 4 — Architecture Fixes

**Team:** Fixing Team 4 — Architecture  
**Date:** 2026-07-07  
**Status:** ✅ Complete

---

## Summary

Fixed the top 3 architecture issues identified in `REVIEW_2_ARCHITECTURE.md`:

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 1 | Intelligence pipeline agents return stub/fabricated data | 🔴 HIGH | Wired to real services via `IntelligenceServiceRegistry` |
| 2 | No sync conflict resolution for concurrent multi-device updates | 🔴 HIGH | Added last-write-wins with version vectors |
| 3 | IntentRouter has 800+ lines of hardcoded regex | 🟡 MEDIUM | Extracted to JSON config with dynamic loader |

---

## Fix 1: Intelligence Pipeline Wired to Real Services

**File:** `angavu-intelligence-backend/app/agents/intelligence_pipeline.py`

### What Changed

The four domain agents (`MarketDataAgent`, `CreditAnalysisAgent`, `DistributionAgent`, `CompetitorAgent`) previously returned hardcoded sample data like `{"prices": {"avg": 850.0, "min": 600.0}}`. They now:

1. **Accept an `IntelligenceServiceRegistry`** — injected with real clients:
   - `db_session_factory` → SQLAlchemy async sessions (PostgreSQL)
   - `redis_client` → Redis cache
   - `market_data_client` → External market data API
   - `credit_bureau_client` → Credit bureau API
   - `ml_inference_client` → ML model inference endpoints

2. **Each agent calls real services:**
   - `MarketDataAgent` → Fetches market prices from external API, regional benchmarks from DB, runs price trend ML model
   - `CreditAnalysisAgent` → Analyzes real transaction history, fetches credit bureau data, runs credit scoring ML model
   - `DistributionAgent` → Queries supply chain data from DB, fetches market prices, runs distribution optimizer
   - `CompetitorAgent` → Queries competitor aggregates from DB, computes competitive position

3. **Error handling:** Each agent catches service failures gracefully and returns partial results with confidence scores reflecting data availability.

4. **Full pipeline preserved:** `LongHorizonOrchestrator` → `TaskPlanner` → `SubAgentDelegator` → agents → `ResultAggregator` — same architecture, real data.

### Key Design Decisions

- **Service registry pattern:** Agents don't import services directly — they receive a registry. This enables testing with mock services and swapping implementations.
- **Confidence scoring:** Each agent returns `_confidence` based on data availability (e.g., 0.85 with prices, 0.4 without). The aggregator computes weighted overall confidence.
- **Graceful degradation:** If ML inference fails, agents still return available data (DB queries, API results). Partial intelligence > no intelligence.

---

## Fix 2: Sync Conflict Resolution

**Files:**
- `msaidizi-app/app/src/main/java/com/msaidizi/app/data/sync/SyncConflictResolver.kt`
- `msaidizi-app/app/src/main/java/com/msaidizi/app/data/sync/SyncableEntities.kt`

### What Changed

Previously, the backend used idempotent deduplication via `(user_id + timestamp + amount + item)` which silently dropped concurrent updates from different devices. Now:

1. **`SyncableEntity` interface** — All syncing entities carry:
   - `syncVersion: Long` — monotonic counter per device
   - `deviceId: String` — which device last modified
   - `lastModifiedAt: Long` — epoch millis of last change
   - `entityId: String` — globally unique stable ID

2. **`SyncConflictResolver`** — Resolves conflicts with configurable strategy:
   - Same device, same version → no change
   - Same device, different version → higher version wins
   - Different devices → configurable: `LAST_WRITE_WINS` (default), `REMOTE_WINS`, `LOCAL_WINS`, `MERGE`

3. **`ConflictRecord`** — Every conflict is logged with both versions, timestamps, and resolution action. Stored in `ConflictLog` for audit trail and potential client-side review.

4. **`SyncableEntities.kt`** — Concrete Room entities (`SyncableTransaction`, `SyncableGoal`, `SyncableInventory`) implementing `SyncableEntity` with `withUpdate()` / `withContribution()` / `withQuantityChange()` helpers that auto-increment `syncVersion`.

### Key Design Decisions

- **Last-write-wins by default:** Simple, predictable, correct for the primary use case (worker switching phones). Conflicts are logged, not silently dropped.
- **Version vectors as a foundation:** The `deviceId + syncVersion` pair enables future upgrade to full vector clocks or CRDT merge without changing the entity interface.
- **Conflict audit trail:** `ConflictLog` stores up to 1000 conflicts per entity for debugging and user review. In production, this backs a Room table.

---

## Fix 3: IntentRouter Regex Extracted to Config

**Files:**
- `msaidizi-app/app/src/main/assets/intent_patterns.json` — 14 intents, ~150 patterns
- `msaidizi-app/app/src/main/java/com/msaidizi/app/agent/IntentRouter.kt` — config-driven loader

### What Changed

The original `IntentRouter.kt` had 800+ lines of hardcoded regex across ~50 pattern lists. Now:

1. **`intent_patterns.json`** — All patterns in a single JSON file:
   - 14 intent types: `SALE_RECORD`, `EXPENSE_RECORD`, `BALANCE_CHECK`, `STOCK_CHECK`, `PRICE_INQUIRY`, `GREETING`, `HELP_REQUEST`, `GOAL_SETTING`, `LOAN_INQUIRY`, `TITHE_TRACKING`, `REPORT_REQUEST`, `RESTOCK_ALERT`, `BRIEFING_REQUEST`, `FEEDBACK`, `GOODBYE`, `UNKNOWN`
   - Each intent has: `patterns` (standard regex), `sheng_patterns` (Sheng-specific), `keywords`, `response_hints`, `priority`
   - Global settings: `case_sensitive`, `sheng_weight_boost`, `min_confidence_threshold`, `fallback_intent`

2. **`IntentRouter.kt`** — Refactored to ~250 lines:
   - Loads patterns from JSON at init, compiles regex once (cached)
   - `loadConfig()` — reload from assets
   - `loadConfigFromJson(json)` — reload from a downloaded update (enables OTA pattern updates)
   - Scoring: pattern match (1.0) + sheng boost (×1.3) + keyword match (0.5/keyword) + priority bonus

3. **OTA updates:** `loadConfigFromJson()` allows pushing pattern updates from the server without an app update. The backend can serve updated `intent_patterns.json` and the app reloads on next launch.

### Key Design Decisions

- **JSON over YAML:** No additional dependency. Gson is already in the project.
- **Regex compilation is cached:** Patterns are compiled once at load time, not on every classification call. Performance is equivalent to hardcoded patterns.
- **Backward compatible:** The `classify()` method signature is unchanged. Existing callers don't need modification.

---

## Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `angavu-intelligence-backend/app/agents/intelligence_pipeline.py` | ~450 | Intelligence pipeline with real service wiring |
| `msaidizi-app/.../data/sync/SyncConflictResolver.kt` | ~250 | Conflict resolution engine |
| `msaidizi-app/.../data/sync/SyncableEntities.kt` | ~160 | Room entities with sync fields |
| `msaidizi-app/.../assets/intent_patterns.json` | ~250 | Config-driven intent patterns |
| `msaidizi-app/.../agent/IntentRouter.kt` | ~280 | Refactored config-driven router |

## What's NOT Changed (Out of Scope)

These were identified in the review but are lower priority and not in scope for this fix:

- **Orchestrator god object** (Orchestrator.kt refactoring) — Medium priority, separate effort
- **API versioning consolidation** — Medium priority, separate effort  
- **FL state persistence** — Medium priority, separate effort
- **Observability stack** — Low priority, infrastructure work
- **Horizontal scaling** — Low priority, pre-traffic concern
