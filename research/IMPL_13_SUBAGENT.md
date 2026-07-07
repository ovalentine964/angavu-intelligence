# Implementation 13: Sub-Agent Orchestration (OpenClaw Pattern)

**Date:** 2026-07-07  
**Swarm:** Impl 13 — Sub-Agent Orchestration  
**Pattern Source:** OpenClaw Gateway — `sessions_spawn` / `sessions_yield`  
**Academic Basis:** STA (Software Technology & Architecture) — multi-agent coordination; ECO 321 (Mechanism Design) — optimal task allocation

---

## What Was Built

### 1. `app/agents/subagent.py` — SubAgentOrchestrator

OpenClaw-style push-based sub-agent orchestration. The core pattern:

```
Parent spawns child → child works independently → child pushes completion event → parent processes result
```

**Key classes:**

| Class | Purpose |
|-------|---------|
| `SubAgentOrchestrator` | Parent spawns isolated children, collects push-based completions |
| `AgentRegistry` | Maps agent_type strings to handler coroutines |
| `SubTask` | Discrete unit of work assigned to a sub-agent |
| `AgentResult` | Push-based completion event from child to parent |
| `ChildAgent` | Tracks a spawned child's lifecycle |

**Features:**
- **Push-based completion:** Children push results to an `asyncio.Queue` — parent doesn't poll
- **Timeout handling:** `asyncio.wait_for` kills stuck agents after configurable timeout
- **Concurrency limiting:** Semaphore caps parallel sub-agents (default: 10)
- **Parent-child tracking:** Full lineage of agent spawns via `parent_id`
- **Cost tracking:** Aggregate cost across all sub-agents
- **Cancellation:** Parent can cancel individual or all children
- **Streaming mode:** `process_completions()` processes results as they arrive

### 2. `app/agents/task_decomposition.py` — TaskDecomposer

Breaks complex worker queries into sub-agent tasks with optimal execution strategy.

**Academic basis:** ECO 321 (Mechanism Design) — allocating tasks across agents with heterogeneous capabilities and costs.

**Key classes:**

| Class | Purpose |
|-------|---------|
| `TaskDecomposer` | Analyzes query, identifies needed agents, plans execution |
| `DecompositionPlan` | Result: sub-tasks, execution strategy, cost estimate |
| `AgentCapability` | Describes what an agent can do, its cost, and speed |

**Execution strategies:**
- **PARALLEL:** All sub-tasks independent → run simultaneously (most common)
- **SEQUENTIAL:** Tasks have dependencies → run in order
- **MIXED:** Some parallel, some sequential (e.g., finance first, then credit scoring)

**Agent capability map:** 12 agent types with keyword matching, cost profiles, and model hints:
`finance`, `credit`, `inventory`, `market`, `tax`, `formalization`, `anomaly`, `supplier`, `health`, `regulatory`, `forecast`, `savings`

### 3. `app/agents/factory.py` — AgentFactory

Wires up the full system: decomposer + orchestrator + registry + pipeline integration.

**Flow:**
1. Worker query arrives
2. `TaskDecomposer.decompose()` identifies needed agents and execution strategy
3. If trivial → `IntelligencePipeline` handles directly (single agent)
4. If complex → `SubAgentOrchestrator` spawns children per strategy
5. Results merged into unified response with confidence scoring

### 4. Updated `app/agents/__init__.py`

Exports all new classes alongside existing causal reasoning and pipeline modules.

---

## How It Maps to Angavu's 33-Agent System

| OpenClaw Pattern | Angavu Implementation |
|------------------|----------------------|
| `sessions_spawn` → isolated child session | `orchestrator.spawn(task)` → isolated `asyncio.Task` |
| `sessions_yield` → wait for completion | `orchestrator.wait_for(agent_id)` → push-based queue |
| Push-based completion events | `asyncio.Queue` + `AgentResult` dataclass |
| Parent sets cheaper models for sub-agents | `SubTask.model_hint` → "on_device" vs "cloud_light" |
| Configurable nesting depth | `SubAgentOrchestrator(parent_id=...)` — recursive spawning |
| Session isolation | Each child runs in its own `asyncio.Task` — no shared state |

### IntentRouter Integration

The `IntentRouter` (existing Kotlin code) becomes the parent orchestrator:

```
Worker: "How is my business? Should I restock? What are market prices?"
    ↓
IntentRouter → TaskDecomposer.decompose()
    ↓
[finance, inventory, market] → parallel execution
    ↓
SubAgentOrchestrator.spawn_many([finance_task, inventory_task, market_task])
    ↓
FinanceAgent ──→ push(result) ──┐
InventoryAgent ─→ push(result) ──┤ → merge → unified response
MarketAgent ──→ push(result) ──┘
```

### Cost Control

The key cost insight from OpenClaw: set cheaper models for routine sub-agents.

| Query Type | Model | Est. Cost |
|------------|-------|-----------|
| Balance check | on_device | $0.0001 |
| Inventory count | on_device | $0.0002 |
| Cash flow analysis | on_device | $0.0003 |
| Credit scoring | cloud_light | $0.0005 |
| Market analysis | cloud_light | $0.0004 |
| Anomaly detection | cloud_light | $0.0006 |

A multi-agent query (3 agents) costs ~$0.0006 total — affordable at scale for $2/day earners.

---

## Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| `angavu-intelligence-backend/app/agents/subagent.py` | **Created** | ~450 |
| `angavu-intelligence-backend/app/agents/task_decomposition.py` | **Created** | ~430 |
| `angavu-intelligence-backend/app/agents/factory.py` | **Created** | ~380 |
| `angavu-intelligence-backend/app/agents/__init__.py` | **Modified** | Updated exports |

---

## Verification

```
✓ All imports resolve correctly
✓ TaskDecomposer decomposes "How is my business? Should I restock tomatoes?" 
  → 2 agents (market + inventory), parallel execution, $0.0006
✓ Simple queries ("What is my balance?") → single agent, no decomposition
✓ SubAgentOrchestrator spawns children, collects push-based completions
✓ AgentFactory.handle_query() runs full flow end-to-end
✓ 12 agent types registered with keyword matching
```

---

## What This Enables

1. **Parallel specialist execution** — IntentRouter fans out to multiple agents simultaneously
2. **Cost-aware routing** — Routine tasks use on-device models; complex tasks use cloud
3. **Timeout resilience** — Stuck agents are killed, parent continues with partial results
4. **Streaming results** — Parent can process completions as they arrive (not batch)
5. **Extensible** — Register new agent types by adding to `AgentRegistry`

---

*Completed by Impl Swarm 13 | Pattern: OpenClaw Sub-Agent Orchestration*
