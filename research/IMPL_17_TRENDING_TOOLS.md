# 🔬 Implementation Swarm 17: Trending Tools
## Angavu Intelligence — Implementation Report

**Date:** 2026-07-07
**Implementer:** Implementation Swarm 17
**Source:** Swarm H Research (Feb 2026 — July 2026) + Swarm G OpenClaw/Hermes Analysis

---

## Summary

Implemented 5 trending tool patterns identified by Swarm H research into production-ready code:

1. **PydanticAI** — Type-safe validation for financial transactions
2. **CrewAI Pattern** — Role-based agent teams for informal markets
3. **Plan-and-Execute** — Multi-step planning loop for complex tasks
4. **Stigmergy Pattern** — Decentralized coordination through environment traces
5. **ModelRouter Update** — All paid APIs removed, zero-cost fallback chain

---

## 1. PydanticAI — Type-Safe Validation

**File:** `angavu-intelligence-backend/app/schemas/agent_schemas.py` (17KB)

**WHY:** Financial transactions need strict validation. A malformed M-Pesa receipt code or negative amount could corrupt worker records. PydanticAI ensures agent inputs/outputs are type-safe at every boundary.

**WHAT:**
- `TransactionInput` / `TransactionOutput` — Validated financial transaction schemas
- `CreditAssessmentInput` / `CreditAssessmentOutput` — Credit scoring with explainable decisions
- `PriceQueryInput` / `PriceQueryOutput` — Market price query/response with trend data
- `WorkerProfile` — Comprehensive worker identity across all Angavu interactions
- Enums: `Currency` (KES, UGX, TZS, ETB, NGN, GHS, USD), `TransactionType`, `WorkerType`, `MarketCondition`
- Custom validators for M-Pesa receipt codes, amount precision, worker ID format
- JSON Schema generation for API documentation

**ALIGNMENT:**
- NIST AI RMF Layer 1: Transaction Safety — every financial action is validated
- Hermes L3 User Model — WorkerProfile maps to the persistent user model

---

## 2. CrewAI Pattern — Role-Based Agent Teams

**File:** `angavu-intelligence-backend/app/agents/roles/market_roles.py` (18KB)

**WHY:** CrewAI's role-based pattern maps perfectly to informal market roles. A mama mboga needs a different agent personality than a boda boda rider. Role definitions with goals, backstories, and tools make agents contextually aware.

**WHAT:**
- `BuyerAgent` — Goal: find best prices. Knows Gikomba wholesale prices, Wakulima afternoon deals
- `SellerAgent` — Goal: maximize sales revenue. Understands market rhythms, demand patterns
- `MarketAnalystAgent` — Goal: identify trends. Reads stigmergy traces for market intelligence
- `CreditAgent` — Goal: fair credit assessment. 30% income cap, explainable decisions
- `LogisticsAgent` — Goal: minimize transport costs. Knows every matatu route
- `MarketCrew` — Team composition with hierarchical task routing
- `AgentTool` registry — 18 tools with confirmation flags for financial actions
- `AgentTier` — 3-tier model routing (simple → on-device, complex → cloud)

**ALIGNMENT:**
- CrewAI open-source pattern (100K+ developers)
- Hermes Closed Learning Loop — roles evolve based on outcomes
- Swarm G sub-agent orchestration — each role maps to a sub-agent

---

## 3. Plan-and-Execute Pattern

**File:** `angavu-intelligence-backend/app/agents/loops/plan_execute.py` (22KB)

**WHY:** Complex tasks like loan applications need multi-step planning. A single-shot approach fails on multi-step workflows because it can't adapt when intermediate steps fail.

**WHAT:**
- `Planner` — Breaks tasks into ordered steps using template plans
  - Templates: `loan_application`, `price_comparison`, `market_setup`, `restock_inventory`, `daily_planning`
  - Custom replanning with retry/skip/alternative strategies
- `Executor` — Runs each step with registered tool handlers
  - Tool registration, error handling, retry logic
- `Observer` — Checks results against expectations
  - Step-level and plan-level observation
  - Anomaly detection and recommendation generation
- `Replanner` — Adjusts plans based on failures
  - 3 strategies: retry, skip non-critical, add alternatives
  - Max replan limit to prevent infinite loops
- `PlanExecuteOrchestrator` — Full loop: Plan → Execute → Observe → Replan
  - Safety limit (max 10 iterations)
  - Complete audit trail for NIST AI RMF compliance

**ALIGNMENT:**
- LangGraph Plan-and-Execute pattern
- ORPA loop (Observe → Reason → Plan → Act) from XMPro
- NIST AI RMF — predictable, auditable agent behavior

---

## 4. Stigmergy Pattern — Decentralized Coordination

**File:** `angavu-intelligence-backend/app/agents/coordination/stigmergy.py` (23KB)

**WHY:** Informal markets already use stigmergy — indirect coordination through environment. When a tomato seller does well at a corner, others gravitate there. Agent swarms should mirror this natural coordination.

**WHAT:**
- `AgentTrace` — Data markers agents leave in the environment
  - 8 trace types: price_signal, demand_signal, supply_signal, opportunity, warning, route_intel, trust_signal, seasonal_pattern
  - Pheromone-based strength tracking with reinforcement
- `PheromoneDecay` — Traces decay over time (exponential decay)
  - Different decay rates per trace type (price signals decay fast, trust signals decay slowly)
  - Relevance scoring combining pheromone level + recency
- `SharedEnvironment` — Redis-backed shared state (MVP uses in-memory)
  - Indexed by market_id, commodity, and trace_type for fast queries
  - Lazy cleanup of expired traces
  - Similar trace detection for reinforcement (not duplication)
- `TraceReader` — High-level interface for agents
  - `get_price_intelligence()` — Price signals for a commodity
  - `get_market_overview()` — All signals at a market
  - `get_warnings()` — Active warnings (price crashes, shortages)
  - `get_trust_signals()` — Supplier reliability scores

**ALIGNMENT:**
- UPC Barcelona stigmergy research
- PolySwarm swarm intelligence
- Emergent intelligence from African ground truth data — unreplicable by Big Tech

---

## 5. ModelRouter — Zero Paid APIs

**File:** `msaidizi-app/app/src/main/java/com/msaidizi/app/agent/ModelRouter.kt` (11KB)

**WHY:** Valentine's directive: zero paid APIs, full ownership. Previous fallback chain included GPT-5.4 nano, Claude Haiku, DeepSeek V4 Flash — all paid, all sending African data to foreign servers.

**WHAT:**
- **NEW fallback chain:**
  1. On-device (Qwen3.5) — default for all routine tasks, works offline
  2. Angavu Cloud (open-source model TBD) — for complex tasks when online
- **REMOVED:**
  - ❌ GPT-5.4 nano (OpenAI) — paid API
  - ❌ Claude Haiku (Anthropic) — paid API
  - ❌ DeepSeek V4 Flash — paid API
- `TaskTier` routing:
  - Tier 1 (simple): Always on-device
  - Tier 2 (standard): Always on-device
  - Tier 3 (complex): Angavu Cloud when online, on-device when offline
- `routeWithFallback()` — Automatic fallback to on-device if cloud fails
- Offline-first: workers always get a response, even without network
- Placeholders for `ModelManager` (llama.cpp JNI) and `AngavuCloudClient`

**ALIGNMENT:**
- Valentine's directive: zero paid APIs, full ownership
- Swarm G recommendation: single efficient model per task, routed by IntentRouter
- Defense value: African data stays in Africa

---

## Files Created

| # | File | Size | Pattern |
|---|------|------|---------|
| 1 | `app/schemas/__init__.py` | 93B | PydanticAI |
| 2 | `app/schemas/agent_schemas.py` | 17KB | PydanticAI |
| 3 | `app/agents/roles/__init__.py` | 92B | CrewAI |
| 4 | `app/agents/roles/market_roles.py` | 18KB | CrewAI |
| 5 | `app/agents/loops/__init__.py` | 91B | Plan-and-Execute |
| 6 | `app/agents/loops/plan_execute.py` | 22KB | Plan-and-Execute |
| 7 | `app/agents/coordination/__init__.py` | 89B | Stigmergy |
| 8 | `app/agents/coordination/stigmergy.py` | 23KB | Stigmergy |
| 9 | `msaidizi-app/.../agent/ModelRouter.kt` | 11KB | Zero Paid APIs |

**Total:** 9 files, ~92KB of production code

---

## Integration Points

```
┌─────────────────────────────────────────────────┐
│              Worker's $50 Phone                  │
│         IntentRouter → ModelRouter               │
│         (Qwen3.5 on-device, always)              │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────┐
│           Angavu Intelligence Backend            │
│                                                  │
│  ┌──────────────┐  ┌──────────────────────┐     │
│  │ PydanticAI   │  │ CrewAI Roles         │     │
│  │ (agent_      │  │ (market_roles.py)    │     │
│  │  schemas.py) │  │ Buyer/Seller/Analyst/ │     │
│  │ Validates    │  │ Credit/Logistics     │     │
│  │ all I/O      │  │ Agents               │     │
│  └──────┬───────┘  └──────────┬───────────┘     │
│         │                     │                  │
│  ┌──────┴─────────────────────┴───────────┐     │
│  │     Plan-and-Execute Orchestrator       │     │
│  │     (plan_execute.py)                   │     │
│  │     Plan → Execute → Observe → Replan  │     │
│  └──────────────────┬──────────────────────┘     │
│                     │                            │
│  ┌──────────────────┴──────────────────────┐     │
│  │     Stigmergy Shared Environment        │     │
│  │     (stigmergy.py)                      │     │
│  │     Traces, Decay, TraceReader          │     │
│  │     Redis-backed (or in-memory MVP)     │     │
│  └─────────────────────────────────────────┘     │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Wire schemas into API endpoints** — Use Pydantic models in FastAPI request/response validation
2. **Connect roles to IntentRouter** — Route intents to appropriate CrewAI role agents
3. **Register tool handlers** — Wire Plan-and-Execute executor to actual Angavu services
4. **Deploy Redis for stigmergy** — Replace in-memory storage with Redis for multi-instance support
5. **Integrate Qwen3.5 JNI** — Connect ModelRouter to actual llama.cpp on-device inference
6. **Deploy Angavu Cloud** — Stand up the open-source model inference endpoint

---

*Implementation Swarm 17 — Angavu Intelligence*
*"Don't tell your dreams to anyone, let the success make the noise."*
*🔬*
