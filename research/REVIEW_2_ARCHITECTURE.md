# Architecture Review — Angavu Intelligence

**Reviewer:** Review Team 2 — Architecture Reviewer  
**Date:** 2026-07-07  
**Scope:** msaidizi-app (Android) + angavu-intelligence-backend (Python/FastAPI)

---

## Strengths

### 1. Agent Layering is Properly Implemented — ✅

**Evidence:** The app follows the Orchestrator → IntentRouter → Agent pipeline precisely. `Orchestrator.kt` coordinates 15+ specialized agents, `IntentRouter.kt` classifies intents via code/regex (90%+ without LLM), and `ModelRouter.kt` handles hybrid inference routing across on-device and cloud providers. The backend mirrors this with a 3-tier architecture: MetaAgent (Tier 1) → Domain Agents (Tier 2) → Utility Agents (Tier 3), all wired via `AgentFactory.py`.

### 2. Event Bus is Decoupled and Production-Ready — ✅

**Evidence:** The app uses `AgentEventBus` (Kotlin SharedFlow) with type-safe sealed events, replay buffer (64 capacity), filtered subscriptions, and history ring buffer (200 events). The backend uses `EventBus` backed by Redis Streams with consumer groups for exactly-once processing, automatic in-memory fallback when Redis is unavailable, dead letter queue tracking, event persistence (JSONL audit trail), and stream trimming (MAX_STREAM_LENGTH = 10,000). Agents can be added/removed without breaking others — `AgentFactory._subscribe_agents()` maps each agent to its event types independently.

### 3. Voice Pipeline is Modular — ✅

**Evidence:** `VoicePipeline.kt` composes independent components via Hilt DI: `AudioRecorder`, `VoiceActivityDetector`, `SpeechRecognizer`, `TextToSpeech`, `MMSTextToSpeech`, `AdaptiveAsrEngine`. The STS engine (`SpeechToSpeechEngine.kt`) uses a `StsProvider` interface with concrete implementations (`ElevenLabsProvider`, `GptRealtimeProvider`, `LocalStsProvider`) — swappable without code changes. `ModelRegistry.kt` manages model lifecycle with tiered download (CRITICAL → HIGH → LOW → OPTIONAL), SHA-256 verification, resume support, and per-model mutexes.

### 4. Intelligence Pipeline is Modular — ✅

**Evidence:** `intelligence_pipeline.py` defines four domain-specific flows (MarketAnalysis, CreditScoring, Distribution, Competitor) as `LongHorizonOrchestrator` instances with pluggable `TaskPlanner`, `SubAgentDelegator`, and `ResultAggregator` components. New intelligence products can be added by implementing a new Planner + Aggregator and registering with `create_all_intelligence_flows()`. The backend has 20+ intelligence services under `app/services/intelligence/` covering pricing, credit, FMCG, health economics, Markov chains, measure theory, etc.

### 5. Federated Learning is Privacy-Preserving by Design — ✅

**Evidence:** `FederatedLearningClient.kt` documents 6 explicit privacy guarantees: raw audio/text never leaves device, only anonymized correction patterns shared, differential privacy (ε=1.0, δ=1e-5), TLS 1.3 encryption, device-specific signing. The backend `federated_learning.py` implements FedAvg with dialect clustering (K-means per STA 442), quality validation (hypothesis testing per STA 342), and secure aggregation. Communication is limited to weekly uploads on WiFi+charging.

### 6. Data Layer is Clean — ✅

**Evidence:** `AppDatabase.kt` defines 21 Room entities across transactions, inventory, patterns, vocabulary, gamification, tithe, goals, loans, worker profiles, and briefing deliveries. Each entity has a dedicated DAO (`TransactionDao`, `GoalDao`, `LoanDao`, etc.). The backend uses SQLAlchemy async with `DeclarativeBase`, connection pooling (pool_size=20, max_overflow=10), and Alembic migrations (`001_initial.py`, `002_full_schema.py`).

### 7. Model Routing is Cost-Aware and Sophisticated — ✅

**Evidence:** Both app and backend `ModelRouter` implementations feature: 4-tier provider hierarchy (on-device → cloud reasoning → cloud premium → backend), per-user monthly budget tracking ($0.013/user/month target), task-type-based routing table, automatic fallback chains, test-time compute scaling (NONE → LIGHT → STANDARD → EXTENDED → XHIGH), and reasoning chain storage for auditability. The app adds MoE routing (Swarm 7), Reflexion self-critique, and multimodal pipeline support.

### 8. Dialect System is Data-Driven and Extensible — ✅

**Evidence:** `DialectAdapter.kt` provides a base class with shared pipeline (code-switching detection → normalization → translation → region detection). 14 concrete adapters (Sheng, Dholuo, Kikuyu, Kalenjin, Luhya, Maasai, Hausa, Igbo, Yoruba, Zulu, Xhosa, Somali, Amharic, Migori) each supply a `DialectConfig` with business terms, pronunciation variations, and marker patterns. New dialects can be added by creating a config object — no code changes to the adapter.

---

## Weaknesses

### 1. Orchestrator God Object — ⚠️

**What should change:** `Orchestrator.kt` is ~1,200 lines with 20+ constructor dependencies (many nullable), handles 18+ intent types inline with individual handler methods, and mixes routing, gamification, learning, evolution, and domain logic. This violates Single Responsibility and makes testing difficult. 

**Recommendation:** Extract domain handlers (Giving, Goal, Loan, Domain) into separate handler classes. Use a strategy pattern or command pattern for intent → handler mapping instead of a massive `when` block.

### 2. IntentRouter Has Hardcoded Pattern Explosion — ⚠️

**What should change:** `IntentRouter.kt` has ~50 regex pattern lists, each with 5-15 patterns, plus Sheng-specific patterns. Adding a new intent type requires modifying multiple pattern lists and the classify method. The 800+ lines of regex are fragile and hard to test comprehensively.

**Recommendation:** Move patterns to a declarative config (JSON/YAML) or use a trie-based matcher. Consider a composable pattern DSL that separates intent definition from matching logic.

### 3. Intelligence Pipeline Agents Return Stub Data — ⚠️

**What should change:** `intelligence_pipeline.py` domain agents (MarketDataAgent, CreditAnalysisAgent, DistributionAgent, CompetitorAgent) return hardcoded sample data in their `_act_execute` methods. They don't call actual services — they return fabricated JSON like `{"prices": {"avg": 850.0, "min": 600.0}}`.

**Recommendation:** Wire these agents to the actual intelligence services (`app/services/intelligence/`). The planner/delegator/aggregator pattern is correct but the leaf agents need real implementations.

### 4. Backend API Layer Lacks OpenAPI Contract Enforcement — ⚠️

**What should change:** While FastAPI auto-generates OpenAPI docs, there's no explicit schema versioning contract. The `app/api/v1/` directory exists but `__init__.py` is empty (just a docstring). API endpoints are scattered across `app/api/` with mixed versioning — some use `/api/v1/` prefix, others don't. No explicit deprecation strategy.

**Recommendation:** Consolidate all endpoints under `/api/v1/`, add explicit response models, implement API versioning with backward compatibility, and publish an OpenAPI spec as a contract artifact.

### 5. Sync Conflict Resolution is Incomplete — ⚠️

**What should change:** `SyncManager.kt` handles store-forward with compression and encryption, and the backend `sync.py` implements idempotent deduplication via `(user_id + timestamp + amount + item)`. However, there's no conflict resolution for concurrent updates from multiple devices. The dedup key prevents duplicates but doesn't handle the case where two devices update the same record differently.

**Recommendation:** Implement vector clocks or last-write-wins with device priority. Add a `sync_version` field to entities and return conflicts for client-side resolution.

### 6. Federated Learning State is In-Memory — ⚠️

**What should change:** `federated_learning.py` `_FLState` class holds all FL state (pending updates, global models, version counters) in a Python dict singleton. This is lost on process restart. The code acknowledges this: "In-Memory State (production would use Redis/PostgreSQL)".

**Recommendation:** Migrate FL state to Redis (for pending updates) and PostgreSQL (for model versions and aggregation history). The `FLPersistence` class exists but the integration is incomplete.

---

## Gaps

### 1. No Horizontal Scaling Strategy — ❌

**What's missing:** The backend runs as a single FastAPI process with in-memory agent state. The `AgentFactory` creates agents as Python objects in a single process. There's no containerization strategy, no Kubernetes manifests, no stateless API layer separated from stateful agent runtime. The Redis-backed event bus supports multiple consumers, but the agent lifecycle (start/stop, health checks) is process-local.

**Recommendation:** Separate the API layer (stateless, horizontally scalable) from the agent runtime (stateful, single-leader). Use Redis for shared state and a message queue (Redis Streams already used) for agent coordination. Add Docker/K8s deployment configs.

### 2. No Circuit Breaker Pattern — ❌

**What's missing:** `ModelRouter` has basic consecutive-failure tracking (3 failures → mark unavailable) but no circuit breaker with half-open state, exponential backoff, or health probe. Cloud provider failures cascade without graceful degradation.

**Recommendation:** Implement a circuit breaker (closed → open → half-open) with configurable thresholds. Use the existing `consecutiveFailures` counter but add time-based recovery.

### 3. No Observability Stack — ❌

**What's missing:** The backend has `AgentTracer` and `AgentObservability` but no integration with standard observability tools (Prometheus, Grafana, Jaeger/OpenTelemetry). No distributed tracing across app → backend. No alerting on agent failure rates or latency SLAs.

**Recommendation:** Add OpenTelemetry instrumentation, export metrics to Prometheus, and set up Grafana dashboards for agent health, FL aggregation status, and sync pipeline metrics.

### 4. Missing Database Schema Documentation — ❌

**What's missing:** The backend has Alembic migrations (`001_initial.py`, `002_full_schema.py`) but no ERD documentation. The app has Room entities but no migration strategy documentation between versions (v1→v8). No schema compatibility matrix between app versions and backend versions.

**Recommendation:** Generate an ERD from SQLAlchemy models, document Room migration paths, and create a schema compatibility matrix.

### 5. No Integration Test Suite — ❌

**What's missing:** The app has unit tests for individual components (DAOs, IntentRouter, Orchestrator, GamificationEngine) but no integration tests for the full pipeline (voice → intent → agent → response → sync → backend). The backend has tests for autonomous agents and specific services but no end-to-end sync tests.

**Recommendation:** Add integration tests covering: (1) app agent pipeline end-to-end, (2) app↔backend sync with conflict scenarios, (3) FL round-trip with privacy guarantees, (4) onboarding flow completion.

### 6. No Rate Limiting Per-Agent — ❌

**What's missing:** The backend has global rate limiting via `slowapi` (`RATE_LIMIT_PER_MINUTE`), but individual agents have no rate limits. A misbehaving agent could flood the event bus or consume excessive LLM tokens.

**Recommendation:** Add per-agent rate limits using token bucket algorithm. Track LLM token usage per agent and enforce budgets.

---

## Recommendations (Priority Order)

### 1. 🔴 HIGH — Fix Intelligence Pipeline Stubs

The entire backend intelligence pipeline returns fabricated data. The `LongHorizonOrchestrator` architecture is sound, but the leaf agents (`MarketDataAgent`, `CreditAnalysisAgent`, etc.) need to be wired to `app/services/intelligence/`. This is the single highest-impact fix — without it, the intelligence product is non-functional.

**Effort:** 2-3 days  
**Impact:** Critical — enables actual intelligence delivery

### 2. 🔴 HIGH — Implement Sync Conflict Resolution

Two-device conflict resolution is a real-world scenario for workers who switch phones or share devices. The current dedup approach silently drops the second update. Add `sync_version` fields and implement last-write-wins with conflict notification.

**Effort:** 1-2 days  
**Impact:** High — data integrity in production

### 3. 🟡 MEDIUM — Refactor Orchestrator God Object

Extract intent handlers into strategy classes. The Orchestrator should only coordinate, not implement 18+ handlers inline. This improves testability and enables independent feature development.

**Effort:** 2-3 days  
**Impact:** Medium — developer velocity and maintainability

### 4. 🟡 MEDIUM — Consolidate API Versioning

Move all endpoints under `/api/v1/`, publish OpenAPI spec, and document the API contract. This is critical for any third-party integration or mobile app versioning.

**Effort:** 1-2 days  
**Impact:** Medium — API stability and integration readiness

### 5. 🟡 MEDIUM — Migrate FL State to Persistent Storage

Replace in-memory `_FLState` with Redis + PostgreSQL. The `FLPersistence` class exists but needs full integration. This prevents data loss on backend restarts.

**Effort:** 1 day  
**Impact:** Medium — FL reliability

### 6. 🟢 LOW — Add Observability Stack

OpenTelemetry + Prometheus + Grafana. This is standard infrastructure but can be added incrementally.

**Effort:** 2-3 days  
**Impact:** Low now, high at scale

### 7. 🟢 LOW — Horizontal Scaling Preparation

Separate stateless API from stateful agents. Add Docker configs. This can wait until traffic justifies it.

**Effort:** 3-5 days  
**Impact:** Low now, critical at scale

---

## Verdict: **PASS**

### Justification

The architecture is fundamentally sound and demonstrates sophisticated design:

1. **Agent system** is properly layered with clear separation of concerns
2. **Event bus** is production-ready with Redis Streams, consumer groups, dead letter queues, and graceful fallback
3. **Voice pipeline** is genuinely modular with swappable ASR/TTS engines via interface abstraction
4. **Dialect system** is data-driven — 14 dialects added without modifying core adapter code
5. **Model routing** is cost-aware with $0.013/user/month target, 4-tier provider hierarchy, and automatic fallback
6. **Federated learning** is privacy-preserving with differential privacy, secure aggregation, and device-local raw data
7. **Data layer** has proper Room entities/DAOs and SQLAlchemy async with migrations

The weaknesses are all addressable without architectural rework — they're implementation gaps (stubs, in-memory state, missing tests) rather than design flaws. The gaps (horizontal scaling, observability) are appropriate for a pre-production system and can be addressed as the system scales.

**This architecture can support the product vision of a voice-first business assistant for 100M+ informal workers in Africa.**
