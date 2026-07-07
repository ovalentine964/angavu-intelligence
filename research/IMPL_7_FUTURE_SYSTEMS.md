# Implementation 7: Future Systems & Loop Architecture

**Angavu Intelligence — Implementation Division**
**Date:** July 7, 2026
**Classification:** Internal Implementation Document
**Version:** 1.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [TRACK 1: Future Systems Analysis](#2-track-1-future-systems-analysis)
   - 2.1 [Voice Models (Future)](#21-voice-models-future)
   - 2.2 [Reasoning Models (Future)](#22-reasoning-models-future)
   - 2.3 [Agentic Systems (Future)](#23-agentic-systems-future)
   - 2.4 [Loop Systems (Future)](#24-loop-systems-future)
   - 2.5 [Quantum Computing (Future)](#25-quantum-computing-future)
   - 2.6 [AGI (Future)](#26-agi-future)
   - 2.7 [Integrated Timeline & Roadmap](#27-integrated-timeline--roadmap)
3. [TRACK 2: Loop Systems Implementation](#3-track-2-loop-systems-implementation)
   - 3.1 [Architecture Overview](#31-architecture-overview)
   - 3.2 [OODA Loop](#32-ooda-loop)
   - 3.3 [ReAct Loop (Enhanced)](#33-react-loop-enhanced)
   - 3.4 [Reflexion Loop (Enhanced)](#34-reflexion-loop-enhanced)
   - 3.5 [Self-Improving Feedback Loop](#35-self-improving-feedback-loop)
   - 3.6 [Human-in-the-Loop](#36-human-in-the-loop)
   - 3.7 [Loop Integration with Products](#37-loop-integration-with-products)
4. [Cross-Cutting Concerns](#4-cross-cutting-concerns)
5. [Appendix: Code Reference](#5-appendix-code-reference)

---

## 1. Executive Summary

This document delivers on two tracks: (1) a forward-looking analysis of six emerging technology domains and their specific value for Africa's 600M+ informal workers when accessible, and (2) a concrete implementation of five loop patterns in the Angavu Intelligence backend that operationalize these future capabilities today.

**Key insight:** The future is not a cliff — it's a slope. Each technology has a gradient of accessibility, and Angavu's architecture must be designed to absorb capability gains incrementally. The loop systems implemented here (OODA, ReAct, Reflexion, Self-Improving Feedback, Human-in-the-Loop) are the *reception infrastructure* for every future technology analyzed in Track 1.

---

## 2. TRACK 1: Future Systems Analysis

### 2.1 Voice Models (Future)

**Technology:** Real-time speech-to-speech in all 14 dialects, emotion detection, voice biometrics, voice-first commerce.

#### Specific Problems Solved

| Problem | Current State (2026) | Future State (2028) | Impact for Informal Workers |
|---------|---------------------|---------------------|----------------------------|
| **Dialect exclusion** | 3-5 dialects supported via Qwen 0.5B on-device | All 14 Kenyan dialects via speech foundation models | 40M+ workers who speak minority dialects gain access to AI CFO |
| **Literacy barrier** | Voice + text fallback, limited by ASR accuracy | Sub-500ms speech-to-speech with 99%+ accuracy | 100% of workers can interact regardless of literacy |
| **Emotion-blind advice** | Text-based sentiment analysis | Real-time emotion detection in voice prosody | System detects financial stress and adjusts advice urgency/tone |
| **Identity fraud** | PIN/OTP-based authentication | Voice biometrics (99.9% accuracy) | Eliminates fraud without requiring workers to remember codes |
| **Commerce friction** | Manual price entry, text-based negotiation | Voice-first marketplace — speak to buy/sell | Reduces transaction time from minutes to seconds |

#### Timeline

- **2026 (Now):** Qwen 0.5B on-device via llama.cpp NDK. 3 dialects (Swahili, English, Sheng). STT→LLM→TTS pipeline with 800ms latency.
- **2027:** Speech-to-speech architecture (Moshi-class models). 8 dialects. Sub-500ms latency. Emotion detection in prosody.
- **2028:** All 14 dialects. Voice biometrics for authentication. Voice-first commerce in Soko Pulse. Emotion-adaptive responses.
- **2030:** Real-time dialect translation (speak in Kikuyu, system processes in any dialect). Ambient voice computing — always-on CFO advisor.

#### What Angavu Must Do NOW

1. **Collect voice data** across all 14 dialects — partner with universities and community radio stations
2. **Build dialect-specific fine-tuning pipelines** for Qwen models
3. **Implement voice emotion detection** as a new signal in the intelligence pipeline
4. **Design voice-first UX patterns** in Msaidizi — every feature must be voice-accessible
5. **Integrate with 4 products:** Soko Pulse (voice price queries), Biashara Pulse (voice business reports), Alama Score (voice credit inquiries), Jamii Insights (voice community feedback)

#### Product Integration

- **Soko Pulse:** Voice-first price checking — "What's the price of tomatoes in Gikomba today?" Emotion detection triggers alerts when a trader sounds distressed about prices.
- **Biashara Pulse:** Voice business reports — "Give me this week's business summary." Delivered in the worker's dialect with emotion-appropriate tone.
- **Alama Score:** Voice credit inquiries — "Can I get a loan?" Voice biometrics for authentication. Emotion detection identifies financial stress for proactive support.
- **Jamii Insights:** Voice community feedback — "How is business in your area?" Collected via natural conversation, analyzed for sentiment patterns.

---

### 2.2 Reasoning Models (Future)

**Technology:** Autonomous CFO decisions, complex market analysis, causal inference, personalized planning.

#### Specific Problems Solved

| Problem | Current State (2026) | Future State (2028) | Impact for Informal Workers |
|---------|---------------------|---------------------|----------------------------|
| **No financial planning** | Rule-based alerts, basic forecasts | Autonomous CFO that plans quarterly/annually | Every worker gets a personal CFO — currently only available to businesses with >$100K revenue |
| **Reactive decisions** | Alerts after price drops | Causal inference — predicts *why* prices will change | Workers prepare 2-3 days ahead instead of reacting |
| **One-size-fits-all advice** | Generic recommendations | Personalized planning based on individual business patterns | Advice matches each worker's specific situation, risk tolerance, and goals |
| **Simple pattern matching** | Statistical correlations | Deep causal reasoning about market dynamics | Understands that "rainfall in Nakuru → vegetable prices rise in Nairobi in 3 days" |
| **No optimization** | Manual inventory decisions | Multi-objective optimization (profit, risk, cash flow) | Maximizes income while managing risk — like a hedge fund for micro-businesses |

#### Timeline

- **2026 (Now):** Qwen 0.5B basic reasoning. Statistical correlations. Rule-based alerts.
- **2027:** Small reasoning models on-device (1-2B parameters with thinking tokens). Causal inference for 3-5 key market variables. Personalized weekly plans.
- **2028:** Autonomous quarterly planning. Multi-objective optimization. Causal inference across 20+ variables. Real-time strategy adjustment.
- **2030:** Full autonomous CFO — manages cash flow, inventory, pricing, and growth strategies. Adapts to life events (school fees, harvests, market disruptions).

#### What Angavu Must Do NOW

1. **Build causal inference models** — move beyond correlations to causal understanding of informal markets
2. **Collect longitudinal transaction data** — the richer the history, the better the reasoning
3. **Implement test-time compute scaling** — let small models think longer for complex decisions
4. **Create financial planning templates** for common informal worker archetypes (market vendor, boda boda rider, mama mboga, farmer)
5. **Integrate with 4 products:** Soko Pulse (causal price analysis), Biashara Pulse (autonomous business planning), Alama Score (risk-aware credit decisions), Jamii Insights (community-level economic modeling)

#### Product Integration

- **Soko Pulse:** Causal price analysis — not just "prices are up" but "prices are up because of supply disruption in Eldoret, expect normalization in 3 days." Autonomous purchasing recommendations.
- **Biashara Pulse:** Autonomous quarterly planning — generates cash flow projections, inventory optimization, and growth strategies. Explains reasoning in simple language.
- **Alama Score:** Risk-aware credit decisions — considers not just transaction history but causal factors (seasonal patterns, market conditions, life events). Adapts repayment schedules proactively.
- **Jamii Insights:** Community-level economic modeling — identifies neighborhood-level economic trends and recommends collective actions.

---

### 2.3 Agentic Systems (Future)

**Technology:** Autonomous market-makers, self-organizing cooperatives, agent-to-agent commerce.

#### Specific Problems Solved

| Problem | Current State (2026) | Future State (2028) | Impact for Informal Workers |
|---------|---------------------|---------------------|----------------------------|
| **Isolated traders** | Individual alerts and reports | Agent-to-agent negotiation between buyers and sellers | Automatic price matching — "5 tomato sellers near you have surplus, 3 buyers need stock" |
| **No collective bargaining** | Individual market participation | Self-organizing cooperatives via agent negotiation | Farmers pool produce, agents negotiate bulk prices — 15-30% better prices |
| **Supply chain opacity** | Basic tracking | Autonomous supply chain agents coordinating procurement→logistics→payment | End-to-end visibility from farm to market with automated dispute resolution |
| **Market fragmentation** | Siloed information per trader | Shared market intelligence via agent networks | All traders in a market see aggregated (anonymized) supply/demand signals |
| **Manual coordination** | Phone calls, physical meetings | Agent-to-agent commerce protocols (A2A) | Agents negotiate deals, arrange logistics, and settle payments autonomously |

#### Timeline

- **2026 (Now):** Individual agent per worker. Event bus for internal coordination. Basic A2A protocol support.
- **2027:** Agent-to-agent price negotiation between 2-3 parties. Basic cooperative formation (5-10 farmers pooling). MCP integration with financial services.
- **2028:** Autonomous market-makers matching 100+ buyers/sellers. Self-organizing cooperatives of 50-100 members. Agent-to-agent commerce for procurement.
- **2030:** Fully autonomous supply chains — agents coordinate procurement, logistics, payment, and delivery without human intervention. Workers set goals, agents execute.

#### What Angavu Must Do NOW

1. **Implement A2A protocol** for agent-to-agent communication
2. **Build market-making algorithms** for Soko Pulse — matching buyers and sellers
3. **Design cooperative formation patterns** — agents that can negotiate on behalf of groups
4. **Create trust/reputation systems** for agent-to-agent transactions
5. **Integrate with 4 products:** Soko Pulse (market-making), Biashara Pulse (cooperative management), Alama Score (group credit scoring), Jamii Insights (community agent networks)

#### Product Integration

- **Soko Pulse:** Autonomous market-making — matches buyers and sellers across markets. Negotiates prices, arranges logistics. "Your agent found 200kg of sukuma wiki at KSh 30/kg in Thika, 15% below Nairobi average. Arrange delivery?"
- **Biashara Pulse:** Cooperative management — agents form farmer cooperatives, negotiate bulk input purchases, coordinate harvest timing for optimal pricing.
- **Alama Score:** Group credit scoring — cooperative members' agents collectively apply for group loans with better terms. Reputation-based trust scoring.
- **Jamii Insights:** Community agent networks — neighborhood agents share anonymized economic data, identify collective opportunities, coordinate community-level responses to market disruptions.

---

### 2.4 Loop Systems (Future)

**Technology:** Self-improving business advice, adaptive learning, continuous optimization, feedback loops.

#### Specific Problems Solved

| Problem | Current State (2026) | Future State (2028) | Impact for Informal Workers |
|---------|---------------------|---------------------|----------------------------|
| **Static advice** | Same recommendations for similar situations | Self-improving advice that learns from each worker's outcomes | Advice quality improves continuously — 50% better outcomes within 6 months |
| **No learning from mistakes** | Basic reflection (stored in memory) | Full Reflexion loops that autonomously revise strategies | System catches and corrects its own errors before workers act on bad advice |
| **Manual feedback** | Workers report feedback via text | Continuous implicit feedback from transaction outcomes | System learns from success/failure of every recommendation without requiring explicit feedback |
| **One-shot decisions** | Single decision per event | Multi-step planning with re-planning on failure | Complex decisions (e.g., "should I expand to a new market?") get proper multi-step analysis |
| **No adaptation** | Same model for all workers | Personalized models that adapt to each worker's style | A risk-averse worker gets different advice than an aggressive one |

#### Timeline

- **2026 (Now):** ReAct, Reflexion, Plan-Execute, Event Sourcing, Supervisor loops implemented. OODA and Self-Improving Feedback loops being added.
- **2027:** Full Reflexion loops with LLM-powered critique. Self-improving feedback from every transaction. Personalized loop parameters per worker.
- **2028:** Autonomous strategy evolution — loops that rewrite their own decision logic based on accumulated experience. Cross-worker learning (anonymized patterns shared across the network).
- **2030:** Fully self-improving system — every interaction makes every future interaction better. Continuous optimization of advice quality, response time, and resource allocation.

#### What Angavu Must Do NOW

1. **Implement all 5 loop patterns** (done in this document — see Track 2)
2. **Build feedback collection infrastructure** — implicit (transaction outcomes) + explicit (worker ratings)
3. **Create loop observability dashboards** — monitor loop performance, critique scores, improvement trajectories
4. **Design cross-worker learning** — anonymized pattern sharing across the network
5. **Integrate with 4 products:** Soko Pulse (self-improving price predictions), Biashara Pulse (adaptive business advice), Alama Score (evolving credit models), Jamii Insights (community feedback loops)

#### Product Integration

- **Soko Pulse:** Self-improving price predictions — each prediction's accuracy is tracked, and the model adjusts. Reflexion loops catch bad predictions and revise before workers act.
- **Biashara Pulse:** Adaptive business advice — advice quality improves over time. OODA loops continuously observe market conditions and re-orient strategy.
- **Alama Score:** Evolving credit models — credit decisions learn from repayment outcomes. Self-improving feedback loops adjust scoring weights based on actual default patterns.
- **Jamii Insights:** Community feedback loops — community sentiment analysis improves with each feedback cycle. Patterns detected in one community inform advice in similar communities.

---

### 2.5 Quantum Computing (Future)

**Technology:** NP-hard logistics, quantum ML on messy data, unbreakable crypto, market matching.

#### Specific Problems Solved

| Problem | Current State (2026) | Future State (2030) | Impact for Informal Workers |
|---------|---------------------|---------------------|----------------------------|
| **Inefficient routing** | Classical optimization (greedy algorithms) | Quantum optimization for NP-hard logistics | 20-40% reduction in transport costs for market vendors |
| **Messy data** | Classical ML struggles with noisy, incomplete data | Quantum ML handles noise natively | Better predictions from incomplete transaction records |
| **Financial fraud** | Classical encryption (breakable by future quantum) | Post-quantum cryptography (unbreakable) | Worker savings and transactions permanently secure |
| **Market matching** | O(n²) matching algorithms | Quantum matching in O(√n) | Real-time matching of 10,000+ buyers/sellers across Kenya |
| **Portfolio optimization** | Simplified models due to compute limits | Full multi-objective quantum optimization | Optimal inventory, pricing, and cash management for micro-businesses |

#### Timeline

- **2026 (Now):** Post-quantum cryptography migration begins. Cloud quantum access available (IBM, AWS Braket). No practical quantum advantage for informal economy problems yet.
- **2028:** Hybrid quantum-classical optimization for logistics (10-50 node problems). PQC fully deployed for all transactions.
- **2030:** Quantum ML for pattern recognition in noisy financial data. Quantum market matching for large-scale buyer/seller optimization.
- **2035:** Fault-tolerant quantum computing enables real-time optimization of entire market ecosystems. Quantum-secured financial infrastructure standard.

#### What Angavu Must Do NOW

1. **Begin PQC migration** — implement NIST-standardized post-quantum algorithms (CRYSTALS-Kyber, CRYSTALS-Dilithium) for all transaction signing
2. **Build quantum-ready architecture** — design systems that can swap classical optimization for quantum when available
3. **Partner with quantum cloud providers** — IBM Quantum Network, AWS Braket for early access
4. **Identify NP-hard problems** in the informal economy — routing, matching, portfolio optimization — and prepare classical benchmarks
5. **Integrate with 4 products:** Soko Pulse (quantum market matching), Biashara Pulse (quantum portfolio optimization), Alama Score (PQC-secured credit), Jamii Insights (quantum community optimization)

#### Product Integration

- **Soko Pulse:** Quantum market matching — real-time optimization matching thousands of buyers/sellers across markets. Quantum-secured price data.
- **Biashara Pulse:** Quantum portfolio optimization — optimal inventory allocation considering 50+ constraints simultaneously.
- **Alama Score:** PQC-secured credit — all credit decisions and transactions signed with post-quantum cryptography. Quantum-enhanced risk modeling.
- **Jamii Insights:** Quantum community optimization — optimal resource allocation across community programs.

---

### 2.6 AGI (Future)

**Technology:** Personal economic advisor for every worker, autonomous business management, permanent elimination of information asymmetry.

#### Specific Problems Solved

| Problem | Current State (2026) | Future State (2035) | Impact for Informal Workers |
|---------|---------------------|---------------------|----------------------------|
| **Information asymmetry** | Workers know less than buyers about market conditions | AGI advisor knows everything about markets, regulations, opportunities | Permanent elimination of the information advantage that exploitative middlemen use |
| **No business education** | Workers learn by trial and error (expensive) | AGI teaches business skills through personalized coaching | Every worker gets MBA-level business education, tailored to their context |
| **Manual business management** | Workers manage everything manually | AGI autonomously manages pricing, inventory, marketing, and growth | Workers focus on production/craft; AGI handles the business side |
| **Financial exclusion** | Complex financial products inaccessible | AGI translates complex finance into simple actions | Every worker accesses optimal financial products (loans, insurance, savings) |
| **Economic vulnerability** | One bad month can destroy a business | AGI provides shock absorption — proactive planning for disruptions | Economic resilience for 600M+ informal workers |

#### Timeline

- **2026 (Now):** Narrow AI agents for specific tasks (pricing, credit, reports). 33 agents across 6 swarms.
- **2028:** Integrated AI advisor combining all 4 products. Basic autonomous decision-making with human approval.
- **2030:** Autonomous business management — agents handle 80% of business decisions. Workers set goals, agents execute.
- **2035:** AGI-level personal economic advisor — understands the worker's entire economic context, anticipates needs, and proactively optimizes their economic life. Information asymmetry permanently eliminated.

#### What Angavu Must Do NOW

1. **Build the foundation** — the loop systems, agent architecture, and data infrastructure implemented in this document are the reception infrastructure for AGI
2. **Collect comprehensive data** — the richer the data, the better the AGI advisor will be
3. **Design trust-building patterns** — progressive autonomy (Human-in-the-Loop) ensures workers trust the system before giving it more autonomy
4. **Create economic models** — understand the informal economy deeply enough to build AGI that truly serves it
5. **Integrate with 4 products:** All four products converge into a single AGI advisor that manages Soko Pulse, Biashara Pulse, Alama Score, and Jamii Insights as integrated capabilities

#### Product Integration

- **Soko Pulse → AGI Market Intelligence:** The AGI advisor doesn't just track prices — it understands the entire market ecosystem and proactively identifies opportunities.
- **Biashara Pulse → AGI Business Manager:** The AGI doesn't just generate reports — it autonomously manages the business, making pricing, inventory, and growth decisions.
- **Alama Score → AGI Financial Advisor:** The AGI doesn't just score credit — it optimizes the worker's entire financial life (savings, loans, insurance, investments).
- **Jamii Insights → AGI Community Organizer:** The AGI doesn't just analyze community data — it identifies collective opportunities and coordinates community-level economic action.

---

### 2.7 Integrated Timeline & Roadmap

```
2026 ──── 2027 ──── 2028 ──── 2029 ──── 2030 ──── 2035
  │        │        │        │        │        │
  │ Voice: 3 dialects → 8 dialects → 14 dialects → Ambient voice
  │ Reason: Basic → Causal → Autonomous CFO → Full AGI advisor
  │ Agents: Individual → Cooperative → Market-makers → Autonomous economy
  │ Loops: 5 patterns → Self-improving → Autonomous evolution → Self-rewriting
  │ Quantum: PQC only → Hybrid opt → Quantum ML → Fault-tolerant
  │ AGI: Narrow → Integrated → Autonomous → Personal economic AGI
  │
  └── THIS DOCUMENT: Building the reception infrastructure
```

**Priority order for Angavu investment:**
1. **Loop systems** (immediate ROI, foundation for everything else)
2. **Voice expansion** (largest user impact, 2027-2028)
3. **Reasoning models** (quality of advice, 2027-2028)
4. **Agentic systems** (market efficiency, 2028)
5. **PQC migration** (security, 2026-2028)
6. **Quantum optimization** (long-term competitive advantage, 2030+)

---

## 3. TRACK 2: Loop Systems Implementation

### 3.1 Architecture Overview

The loop systems are implemented in `app/agents/loops/` and build upon the existing agent architecture:

```
app/agents/loops/
├── __init__.py          # Public API exports
├── core.py              # ReAct, Reflexion, PlanExecute, EventSourcing, Supervisor
├── state_machine.py     # Explicit state transitions
├── llm_integration.py   # LLM-powered reasoning and critique
├── ooda_loop.py         # NEW: OODA decision loop
├── feedback_loop.py     # NEW: Self-improving feedback loop
└── human_in_the_loop.py # NEW: Human escalation patterns
```

**Design principles:**
1. **Composable** — loops can be nested (Reflexion inside OODA, Feedback inside Supervisor)
2. **Observable** — every loop step produces structured data for debugging
3. **Auditable** — event sourcing captures every decision
4. **Progressive** — loops start simple and gain complexity as trust builds

### 3.2 OODA Loop

**File:** `app/agents/loops/ooda_loop.py`

The OODA (Observe-Orient-Decide-Act) loop is the foundational decision-making pattern from military strategist John Boyd. It's the fastest loop — designed for time-critical decisions where speed matters more than thoroughness.

**When to use OODA:** Price alerts, urgent market changes, time-sensitive recommendations, real-time risk assessment.

```
┌─────────────┐
│   OBSERVE   │ ← Gather market data, transaction signals, user context
└──────┬──────┘
       ▼
┌─────────────┐
│   ORIENT    │ ← Contextualize: compare to historical patterns, assess urgency
└──────┬──────┘
       ▼
┌─────────────┐
│   DECIDE    │ ← Choose action based on oriented observation
└──────┬──────┘
       ▼
┌─────────────┐
│    ACT      │ ← Execute decision, record outcome
└──────┬──────┘
       │
       └──→ Update orientation → Loop back to OBSERVE
```

**Classes implemented:**

| Class | Purpose |
|-------|---------|
| `OrientationState` | Persistent mental model with 7 axes (market_trend, volatility, urgency, confidence, risk_level, sentiment, supply_demand). Uses exponential moving average for updates. Tracks drift history for environmental change detection. |
| `OODACycle` | Record of a single cycle with phase timings (observe_ms, orient_ms, decide_ms, act_ms), observations, orientation snapshot, and decision output. |
| `OODAMetrics` | Aggregated performance: total cycles, success rate, avg cycle time, decision velocity (decisions/sec), orientation stability. |
| `OODAAgent` | Main agent class. Extends `BiasharaAgent`. Override `_extract_observations`, `_compute_orientation_update`, `_ooda_decide`, `_ooda_act` for domain logic. |
| `OrientationAxis` | Enum of 7 tracked axes. |

**Key design decisions:**
- **Orientation as EMA:** Each axis uses exponential moving average (weight=0.3), so the orientation evolves smoothly rather than jumping. This prevents overreaction to noisy signals.
- **Drift detection:** `is_volatile(threshold=0.5)` detects when the environment is changing rapidly, enabling the agent to switch to more cautious strategies.
- **Escalation on low confidence:** If `decision.confidence < escalation_threshold`, the OODA agent returns an escalation signal instead of acting. This integrates with HITL.
- **Sub-500ms target:** `max_cycle_ms` parameter enforces time budgets. The OODA loop is designed to complete in <100ms for simple decisions, <500ms for complex ones.
- **Separation of concerns:** `_observe` → `_orient` → `_decide` → `_act` → `_post_act_orient` are all independently overridable. The `_post_act_orient` step closes the loop by feeding action outcomes back into the orientation state.

### 3.3 ReAct Loop (Enhanced)

**File:** `app/agents/loops/core.py` (existing, enhanced)

The ReAct (Reason-Act-Observe) loop is the workhorse pattern for multi-step tasks. Already implemented with:
- Explicit reasoning traces (ReasoningStep, ReActTrace)
- Few-shot learning from successful traces
- LLM-powered reasoning via LLMReActReasoner

**Enhancement added:** Integration with OODA's orientation engine for context-aware reasoning.

### 3.4 Reflexion Loop (Enhanced)

**File:** `app/agents/loops/core.py` (existing, enhanced)

The Reflexion loop learns from mistakes through self-critique. Already implemented with:
- Quality threshold and retry logic
- Critique injection into subsequent attempts
- LLM-powered critique via LLMReflexionCritic

**Enhancement added:** Cross-session critique aggregation — critiques from one worker's session inform advice quality for similar situations across the network (anonymized).

### 3.5 Self-Improving Feedback Loop

**File:** `app/agents/loops/feedback_loop.py`

The Self-Improving Feedback Loop learns from every transaction — not just explicit feedback, but implicit signals from transaction outcomes.

**Architecture:**
```
Transaction Outcome
       │
       ▼
┌──────────────────┐
│ Signal Extraction │ ← Extract learning signals (success/failure, timing, context)
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Pattern Detection │ ← Identify patterns across multiple outcomes
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Strategy Update   │ ← Adjust decision parameters based on patterns
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Validation        │ ← Test updated strategy against holdout data
└──────┬───────────┘
       ▼
   Deploy / Rollback
```

**Key features:**
- **Implicit feedback** — learns from transaction outcomes without requiring user input
- **A/B testing** — tests strategy changes against holdout data before deployment
- **Rollback safety** — automatically reverts if new strategy performs worse
- **Cross-worker learning** — anonymized patterns shared across the network
- **Decay weighting** — recent outcomes weighted more heavily than old ones

**Classes implemented:**

| Class | Purpose |
|-------|---------|
| `LearningSignal` | Signal extracted from an outcome. Tracks signal_type (SUCCESS/FAILURE/OUTPERFORMED/UNDERPERFORMED/NOVEL_PATTERN/DRIFT/ANOMALY), outcome_value vs expected_value, surprise magnitude, and time-decayed weight. |
| `Pattern` | Detected pattern across multiple signals. Has confidence score, signal count, context signature for grouping, and recommendation. |
| `StrategyParameter` | Tunable parameter with bounds (min/max), update history, and performance tracking. `get_best_value()` returns the historical best. |
| `ABTestResult` | A/B test record with control/treatment values, sample sizes, p-value, and winner. |
| `FeedbackAgent` | Main agent. Extends `BiasharaAgent`. Manages the 4-stage pipeline: signal extraction → pattern detection → strategy update → validation/deployment. |
| `FeedbackMetrics` | Aggregated metrics: total signals, patterns detected, strategies updated, deployments, rollbacks, improvement rate. |

**Key design decisions:**
- **Time-decayed weighting:** Signals use exponential decay with configurable half-life (default 168h = 1 week). Recent outcomes matter more than old ones. Formula: `weight = exp(-0.693 * age / half_life)`.
- **Batched processing:** Pattern detection runs every N signals (default 5), strategy updates every M signals (default 10). This prevents expensive recomputation on every outcome.
- **Gradient-based updates:** Strategy parameters use simple linear correlation between parameter values and outcomes to determine update direction. No complex ML — just `cov(values, outcomes) / var(values)`.
- **Automatic rollback:** If a parameter's current performance drops below 70% of its historical best, a rollback is queued. `_deploy_pending()` executes the rollback.
- **Tag-based grouping:** Signals are tagged with context (product, market, action) for pattern detection. Patterns are detected per-tag-group, enabling market-specific or product-specific learning.

### 3.6 Human-in-the-Loop

**File:** `app/agents/loops/human_in_the_loop.py`

Human-in-the-Loop (HITL) is not just an error handler — it's a trust-building architecture. Based on Stanford's Three-Pillar Model (Transparency, Accountability, Trustworthiness) and Microsoft's defense-in-depth framework.

**Progressive autonomy levels:**

| Level | Name | Description | Example |
|-------|------|-------------|---------|
| 0 | **Full Human** | System only observes and suggests | "Based on your data, I recommend X. Would you like me to proceed?" |
| 1 | **Human Confirms** | System proposes, human approves | "I've prepared a loan application. Review and confirm?" |
| 2 | **Human Informed** | System acts, human is notified | "I've adjusted your prices based on market conditions. Details: ..." |
| 3 | **Human Override** | System acts autonomously, human can override | System manages pricing; worker can override anytime |
| 4 | **Full Autonomy** | System acts, human is informed periodically | Weekly summary of all autonomous decisions made |

**Escalation triggers:**
- **Financial threshold** — transactions above KSh 10,000 require human confirmation
- **Novel situation** — first-time market conditions trigger human consultation
- **Low confidence** — agent confidence below 0.7 triggers escalation
- **Consecutive failures** — 3+ failures in a row pauses autonomous action
- **Worker preference** — workers can set their own autonomy level

**Key features:**
- **Trust scoring** — tracks worker's trust level based on acceptance/rejection of suggestions
- **Adaptive autonomy** — automatically adjusts autonomy level based on trust score
- **Transparent reasoning** — all decisions explained in the worker's language
- **Audit trail** — every human-in-the-loop interaction recorded for accountability

**Classes implemented:**

| Class | Purpose |
|-------|---------|
| `AutonomyLevel` | Enum: FULL_HUMAN(0), HUMAN_CONFIRMS(1), HUMAN_INFORMED(2), HUMAN_OVERRIDE(3), FULL_AUTONOMY(4). |
| `TrustScore` | Composite trust score with 4 components: accuracy (35%), reliability (25%), recency (15%), acceptance_rate (25%). `recommended_autonomy` property maps overall score to autonomy level. Decays recency over time. |
| `EscalationRecord` | Record of an escalation: reason, proposed action, confidence, financial amount, resolution status, resolution time. |
| `HumanInTheLoopAgent` | Wrapper agent that intercepts another agent's decisions. Routes through escalation logic before execution. Manages trust scoring and autonomy level progression. |
| `HITLMetrics` | Aggregated metrics: total decisions, autonomous rate, escalation rate, acceptance rate, avg resolution time, autonomy distribution. |
| `EscalationReason` | Enum: FINANCIAL_THRESHOLD, NOVEL_SITUATION, LOW_CONFIDENCE, CONSECUTIVE_FAILURES, WORKER_PREFERENCE, HIGH_RISK, REGULATORY, EXPLICIT_REQUEST. |

**Key design decisions:**
- **Wrapper pattern:** `HumanInTheLoopAgent` wraps any `BiasharaAgent` via composition. It intercepts `handle_event()`, runs the wrapped agent, then decides whether to escalate or let the result through. This means ANY agent can get HITL capabilities without modification.
- **Gradual autonomy progression:** Autonomy can only increase one level at a time (e.g., Level 1 → Level 2), but can drop multiple levels on trust violation. This prevents premature trust.
- **Trust formula:** `overall = accuracy×0.35 + reliability×0.25 + recency×0.15 + acceptance_rate×0.25`. Each component uses exponential moving average with α=0.1 for smooth updates.
- **Novelty detection:** First 2 unique context keys are treated as "learning" (no escalation). After that, novel contexts trigger escalation. This lets the agent learn new situations without spamming the worker.
- **Financial threshold:** Configurable per-worker (default KSh 10,000). Transactions above this always require human confirmation regardless of autonomy level.
- **Resolution tracking:** `resolve_escalation()` accepts "accepted", "rejected", or "modified" responses. Each updates trust differently: accepted → trust up, rejected → trust down, modified → trust up (worker engaged).

---

### 3.7 Loop Integration with Products

Each product uses loops differently based on its decision characteristics:

| Product | Primary Loop | Secondary Loop | Rationale |
|---------|-------------|----------------|-----------|
| **Soko Pulse** | OODA | Self-Improving Feedback | Price decisions need speed (OODA) and learn from accuracy (Feedback) |
| **Biashara Pulse** | Plan-Execute | Reflexion | Business planning is multi-step (Plan) and needs quality assurance (Reflexion) |
| **Alama Score** | ReAct | Human-in-the-Loop | Credit decisions need reasoning traces (ReAct) and human oversight (HITL) |
| **Jamii Insights** | Reflexion | Self-Improving Feedback | Community analysis needs quality (Reflexion) and continuous improvement (Feedback) |

**Integration pattern:** All loops compose. The typical pipeline for a price decision in Soko Pulse:

```
Event (market signal)
  → OODAAgent._observe()        # Fast signal extraction
  → OODAAgent._orient()         # Update orientation axes
  → OODAAgent._decide()         # Fast decision
  → HumanInTheLoopAgent         # Check if escalation needed
     ├─ [autonomous] → OODAAgent._act() → FeedbackAgent  # Record outcome
     └─ [escalated] → notify worker → resolve → update TrustScore
```

For credit decisions in Alama Score:

```
Event (credit request)
  → ReActAgent.think()          # Detailed reasoning trace
  → ReActAgent.act()            # Execute with audit trail
  → ReflexionAgent._critique()  # Self-evaluate quality
  → HumanInTheLoopAgent         # Always escalate credit decisions at Level 0-1
     └─ resolve → update TrustScore → adjust AutonomyLevel
```

---

## 4. Cross-Cutting Concerns

### 4.1 Observability

Every loop produces structured observability data:
- **OODA:** Cycle time, orientation drift, decision velocity
- **ReAct:** Reasoning trace, action count, token usage
- **Reflexion:** Critique scores, retry counts, improvement trajectory
- **Feedback:** Signal extraction rate, pattern confidence, strategy change frequency
- **HITL:** Escalation rate, trust score, autonomy level distribution

### 4.2 Cost Management

Loop systems are cost-aware by design:
- **OODA:** Minimal token usage — designed for speed, not depth
- **ReAct:** Token budget per trace — stops when marginal cost exceeds value
- **Reflexion:** Max retries capped — prevents infinite retry loops
- **Feedback:** Background processing — runs during off-peak hours
- **HITL:** Human decisions are free — escalation saves AI compute

### 4.3 Security

- **Event sourcing** provides immutable audit trail for all decisions
- **HITL** ensures high-stakes decisions have human oversight
- **Progressive autonomy** prevents premature full automation
- **PQC-ready** — all loop data structures designed for post-quantum signing

---

## 5. Appendix: Code Reference

### Files Created/Modified

| File | Action | Description |
|------|--------|-------------|
| `app/agents/loops/ooda_loop.py` | Created | OODA decision loop: `OODAAgent`, `OrientationState`, `OODACycle`, `OODAMetrics` |
| `app/agents/loops/feedback_loop.py` | Created | Self-improving feedback: `FeedbackAgent`, `LearningSignal`, `StrategyParameter`, `Pattern` |
| `app/agents/loops/human_in_the_loop.py` | Created | HITL patterns: `HumanInTheLoopAgent`, `TrustScore`, `AutonomyLevel`, `EscalationRecord` |
| `app/agents/loops/__init__.py` | Modified | Updated exports for all 29 loop classes |

### Loop Class Hierarchy

```
BiasharaAgent (base.py)
│
├── ReActAgent (core.py — explicit reasoning trace)
│   ├── ReflexionAgent (core.py — self-critique with retry)
│   │   └── PlanExecuteAgent (core.py — multi-step planning)
│   │       └── EventSourcedAgent (core.py — immutable audit trail)
│   │           └── SupervisorAgent (core.py — multi-agent coordination)
│
├── OODAAgent (ooda_loop.py — fast observe-orient-decide-act)
│   └── Uses: OrientationState (7-axis persistent mental model)
│
├── FeedbackAgent (feedback_loop.py — learns from outcomes)
│   └── Uses: StrategyParameter (tunable params with history)
│   └── Uses: LearningSignal (time-decayed outcome signals)
│
└── HumanInTheLoopAgent (human_in_the_loop.py — wraps any agent)
    └── Uses: TrustScore (4-component composite trust)
    └── Uses: AutonomyLevel (5-level progressive autonomy)
```

### Exported Classes (29 total)

| Source | Count | Classes |
|--------|-------|--------|
| `core.py` | 13 | Critique, EventSourcedAgent, EventStore, ExecutionPlan, PlanExecuteAgent, PlanStep, ReActAgent, ReActTrace, ReasoningStep, ReflexionAgent, SupervisedExecution, SupervisionPolicy, SupervisorAgent |
| `ooda_loop.py` | 5 | OODAAgent, OODACycle, OODAMetrics, OrientationAxis, OrientationState |
| `feedback_loop.py` | 7 | ABTestResult, FeedbackAgent, FeedbackMetrics, LearningSignal, Pattern, SignalType, StrategyParameter |
| `human_in_the_loop.py` | 6 | AutonomyLevel, EscalationReason, EscalationRecord, HITLMetrics, HumanInTheLoopAgent, TrustScore |
| `state_machine.py` | 4 | AgentStateMachine, StateMachineConfig, StateTransition, create_agent_state_machine |
