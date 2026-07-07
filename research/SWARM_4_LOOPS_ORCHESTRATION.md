# Swarm 4: Agent Loops & Orchestration Systems
## Research Report — February 2026 to July 2026

**Prepared by:** Angavu Intelligence Research Division — Swarm 4  
**Date:** July 7, 2026  
**Classification:** Internal Research Document  
**Version:** 1.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [State of the Art (Feb 2026 — July 2026)](#2-state-of-the-art)
3. [Key Breakthroughs & Emerging Systems](#3-key-breakthroughs--emerging-systems)
4. [Orchestration Patterns for Informal Economy](#4-orchestration-patterns-for-informal-economy)
5. [Application to Informal Economy](#5-application-to-informal-economy)
6. [Angavu Integration Recommendations](#6-angavu-integration-recommendations)
7. [Statistical Data & Performance Benchmarks](#7-statistical-data--performance-benchmarks)
8. [Future Trajectory](#8-future-trajectory)
9. [Citation List](#9-citation-list)

---

## 1. Executive Summary

The period from February to July 2026 represents a watershed moment in agent orchestration. The field has decisively shifted from "can agents work?" to "how do we make agents work reliably at scale?" Five major trends define this period:

1. **Programmatic Orchestration over Tool-Call Loops**: LangChain's Deep Agents introduced "dynamic subagents" (June 2026), where agents write code scripts to orchestrate subagent execution rather than issuing sequential tool calls. This mirrors MIT's Recursive Language Models (RLMs), which process inputs 100× beyond context windows through recursive self-calls. The convergence signals that the agent loop is evolving from a simple observe-act cycle to a programmatic orchestration paradigm.

2. **Durable Execution as Agent Infrastructure**: Temporal's Replay 2026 conference (May 2026) introduced Workflow Streams, Serverless Workers, and Standalone Activities — primitives specifically designed for long-running agent workflows. Temporal's position has crystallized: agents need durable execution infrastructure, not just prompt chains. Kelet AI demonstrated this by building an agent that debugs other agents using Temporal's durable orchestration.

3. **Human-in-the-Loop as Architecture, Not Afterthought**: Microsoft's defense-in-depth framework (May 2026) and Stanford's Three-Pillar Model (Jan 2026) both argue that progressive autonomy — not full automation — is the safe path forward. SAP's supply chain research shows companies deploying 1,000+ agents while maintaining human oversight at strategic decision points.

4. **Context Engineering Replacing Prompt Engineering**: Anthropic's seminal "Effective Context Engineering" paper (2025, widely adopted by Feb 2026) established that managing the entire context state — not just writing better prompts — is the critical engineering discipline for agents. The concept of "context rot" (degrading recall as context grows) has driven architectural decisions across all major frameworks.

5. **Cost as a First-Class Constraint**: Agent costs have become a production crisis. Uber exhausted its full 2026 AI budget in four months. LangSmith now traces sessions across Claude Code, Codex, Cursor, Copilot, and others into a unified cost view. The era of "tokenmaxxing" is ending; cost-aware orchestration is the new imperative.

For Angavu Intelligence's informal economy platform, these developments offer a clear path: use event-driven orchestration with durable execution to coordinate multi-step processes (procurement → logistics → payment → delivery), implement progressive autonomy to build trust with informal workers new to AI, and deploy self-improving loops that adapt to local market conditions over time.

---

## 2. State of the Art (Feb 2026 — July 2026)

### 2.1 Agent Loop Patterns

#### 2.1.1 The Evolution Beyond Simple Loops

The traditional agent loop — **Observe → Orient → Decide → Act (OODA)** — has been the foundational pattern since the early days of autonomous agents. In the Feb–July 2026 period, this pattern has undergone significant evolution:

**From OODA to Programmatic Orchestration**

The OODA loop, originally developed by military strategist John Boyd, has been the implicit architecture behind most agent systems. However, the 2026 period has revealed its limitations at scale. When agents must coordinate hundreds of subtasks (e.g., processing a 300-page document), the sequential observe-act cycle becomes a bottleneck.

LangChain's **Dynamic Subagents** (June 29, 2026) represent the most significant departure from the simple loop pattern. Instead of the agent issuing tool calls one at a time in a loop, the agent writes a short script that orchestrates subagent execution:

```javascript
const results = await Promise.all(pages.map(page =>
  task({ description: `Summarize page ${page.number}`, subagentType: "summarizer" })
));
```

This shift is profound: **the agent loop itself becomes programmable**. The model writes orchestration code that runs deterministically, while the model focuses on reasoning about what to do rather than mechanically executing steps.

**ReAct (Reason + Act) Maturity**

ReAct, which interleaves reasoning traces with action execution, remains the dominant pattern for single-agent loops. However, the 2026 period has seen ReAct augmented with:

- **Verification layers**: LangChain Labs and Harvey demonstrated efficient verifiers for legal agents (June 2026), where a separate model judges agent outputs against rubric criteria. Batch verification reduced costs by an order of magnitude.
- **Cost-aware execution**: ReAct loops now incorporate token budgets and cost gates, terminating when marginal reasoning cost exceeds expected value.

**Reflexion and Self-Reflection Loops**

Reflexion (Shinn et al., 2023) — where agents verbally reflect on task feedback and maintain episodic memory — has been operationalized in production systems. The key 2026 development is **Meta-Harness** (Stanford, March 2026), which applies Reflexion-style self-improvement at the harness level. Meta-Harness uses an outer-loop system that searches over harness code, with an agentic proposer that accesses source code, scores, and execution traces of all prior candidates. Results:

- 7.7-point improvement over state-of-the-art context management on text classification
- 4× fewer context tokens used
- 4.7-point average improvement on 200 IMO-level math problems

**Plan-and-Execute Pattern**

The Plan-and-Execute pattern — where an agent first creates a plan, then executes each step — has been formalized in Google's Agent Development Kit (ADK) 2.0 (2026). ADK 2.0 introduces "Graph Workflows" that weave deterministic code with adaptive AI reasoning, providing explicit execution paths and predictable outcomes. This is a direct response to the observation that pure agentic loops are unreliable for complex multi-step processes.

#### 2.1.2 Recursive Language Models (RLMs)

Perhaps the most intellectually significant development is the **Recursive Language Model** paradigm (Zhang, Kraska, Khattab — MIT CSAIL, December 2025, updated May 2026). RLMs treat long prompts as part of an external environment, allowing the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt.

Key findings:
- RLMs can process inputs **up to two orders of magnitude beyond a model's context window**
- RLM-Qwen3-8B outperforms the underlying Qwen3-8B by **28.3%** on average
- RLM-Qwen3-8B approaches vanilla GPT-5 quality on three long-context tasks
- On GPT-5, RLMs achieve median improvements of **26% against compaction**, **130% against CodeAct with sub-calls**, and **13% against Claude Code**

The RLM paradigm addresses "context rot" — the phenomenon where model accuracy degrades as context length increases — by keeping orchestration logic in code rather than in the model's ephemeral context window.

### 2.2 Orchestration Frameworks

#### 2.2.1 LangGraph & Deep Agents

LangGraph has emerged as the dominant low-level orchestration framework, trusted by Klarna, Uber, and J.P. Morgan. Its core value proposition: **durable execution, streaming, human-in-the-loop, and persistence** for long-running, stateful agents.

The Deep Agents framework (built on LangGraph) represents the state of the art in agent harnesses:

- **Dynamic Subagents** (June 2026): Agents write scripts to orchestrate subagent execution, enabling deterministic coverage at scale
- **RLM Support** (July 2026): Deep Agents now supports Recursive Language Models through dynamic subagents
- **Wiki Memory** (June 2026): Agents maintain persistent, structured knowledge bases by compressing source data into agent-readable wikis
- **Code Interpreters** (June 2026): WebAssembly-based execution isolation for untrusted agent code, providing execution isolation, capability isolation, and durable pauses
- **LangSmith Sandboxes**: Full remote containers for agent code execution

**LangSmith** (the observability platform) has become critical infrastructure:
- Unified tracing across Claude Code, Codex, Cursor, GitHub Copilot, Pi, and OpenCode
- **LangSmith Engine**: Detects issues in agent traces and proposes fixes, including automatic PR generation
- **LangSmith Fleet**: No-code agent builder for templates and routine automation

#### 2.2.2 Temporal — Durable Execution for Agents

Temporal has positioned itself as the **infrastructure layer for production agents**. Replay 2026 (May 2026) introduced several breakthrough capabilities:

**Workflow Streams** (June 2026): A durable streams abstraction that enables rich interactive UIs for agent applications. Agents can continuously update a UI with status, reasoning, tool calls, and generated text, allowing humans to interrupt or steer the agent. Already integrated with Temporal's plugins for OpenAI Agents SDK, Google ADK, and LangGraph.

**Serverless Workers**: Temporal Cloud now automatically invokes, scales, and gracefully shuts down workers based on workload, including scaling to zero. This eliminates infrastructure planning overhead.

**Standalone Activities**: A new primitive enabling Activities to run independently, not just as steps inside a Workflow. This simplifies job processing by eliminating complex queuing and retry logic.

**Kelet AI's Meta-Agent** (June 2026): A durable agent that continuously diagnoses quality failures in other AI agents, built on Temporal. This demonstrates the critical insight that **AI failures don't show up in individual traces** — they emerge from patterns across hundreds of sessions. Kelet processes each session as it arrives, accumulates hypotheses, and reasons across the accumulated set using Temporal's durable orchestration.

#### 2.2.3 Google Agent Development Kit (ADK) 2.0

Google's ADK 2.0 (2026) introduces:
- **Graph Workflows**: Deterministic code paths combined with adaptive AI reasoning
- Multi-language support: Python, TypeScript, Go, Java, Kotlin
- Integration with Temporal for durable execution
- Agents CLI for AI-powered agent development

#### 2.2.4 CrewAI

CrewAI has evolved into a production-grade multi-agent orchestration platform with:
- Agent crews and flows with guardrails
- Built-in memory, knowledge, and observability
- Production-ready from day one

#### 2.2.5 Prefect

Prefect continues to serve as a Python-based orchestration platform, with strengths in:
- Event-driven execution (triggering based on events, not schedules)
- Intelligent pipeline management
- Integration with AI tooling and dbt transformations

### 2.3 Human-in-the-Loop Systems

#### 2.3.1 The Three-Pillar Model (Stanford, Jan 2026)

Cheng, Cheng, and Siu at Stanford propose a Three-Pillar Model for safe AI agents based on:

1. **Transparency**: Agents must explain their reasoning and be visible, auditable, and understandable
2. **Accountability**: Clear chains of responsibility for agent decisions
3. **Trustworthiness**: Progressive validation, analogous to autonomous driving levels

The model argues that **safe agent autonomy must be achieved through progressive validation**, not immediate full automation. This is directly relevant to Angavu's informal economy context, where workers new to AI need to build trust gradually.

#### 2.3.2 Microsoft Defense in Depth (May 2026)

Microsoft's framework for autonomous AI agents emphasizes:
- Application-layer design as the first line of defense
- Identity and access management for agents
- Human oversight at the center of the architecture
- The principle that **as agents gain autonomy, defense in depth must evolve**

#### 2.3.3 SAP's Progressive Autonomy (June 2026)

SAP's research on autonomous supply chains reveals:
- Companies are deploying **1,000+ AI agents** for orchestration, scenario planning, and value chain visibility
- **Progressive autonomy thresholds** are being established — agents earn more autonomy as they demonstrate reliability
- Human-in-the-loop governance is strengthened, not weakened, as agent count increases
- The key insight: **resilience is now defined by decision velocity** — how quickly companies can convert data into action

#### 2.3.4 Temporal's "Stop Failing" Anti-Patterns (June 2026)

Temporal's Joshua Smith identifies critical anti-patterns in agent production:
- **Delegating understanding to agents**: Humans out of the loop, unable to know what agents are doing
- **The "Intelligent Business" model**: Agents process data, humans make decisions — the right data to the right decision-maker
- Ambient agents must be **visible, auditable, and understandable**

### 2.4 Event-Driven Architectures

#### 2.4.1 Event Sourcing for Agents

Event sourcing — storing every state change as an immutable event — has gained significant traction for agent systems in 2026:

**Why Event Sourcing Matters for Agents:**
- **Complete audit trail**: Every agent decision is recorded permanently, critical for trust and compliance
- **AI explainability**: Event sourcing captures the complete chain of events leading to any result
- **Time-travel debugging**: Reproduce any agent failure by replaying the exact sequence of events
- **Flexible analytics**: Build new reports from historical agent behavior

The Axoniq Platform (March 2026) has published production-ready tutorials for event sourcing with CQRS patterns, making the pattern more accessible.

#### 2.4.2 CQRS and Agent Systems

Command Query Responsibility Segregation (CQRS) separates the write model (commands that change state) from the read model (queries that retrieve state). For agent systems:

- **Write side**: Agent actions, decisions, state transitions
- **Read side**: Optimized views for dashboards, analytics, debugging
- **Event store**: Immutable log of everything that happened

Conduktor's analysis (June 2026) shows CQRS with Kafka becoming the standard for event-driven agent architectures.

#### 2.4.3 Saga Patterns for Distributed Agent Systems

The Saga pattern — managing distributed transactions as sequences of local transactions with compensating actions — is critical for multi-agent systems where:

- Agent A completes step 1, triggers Agent B for step 2
- If Agent B fails, a compensating action undoes step 1
- Each agent maintains its own local state

This pattern is directly applicable to Angavu's multi-step processes (procurement → logistics → payment → delivery).

#### 2.4.4 Angavu's Event Bus Architecture

Angavu's existing architecture — event bus with pub/sub messaging, dead letter queue, and agent lifecycle management — aligns well with the 2026 state of the art. The key opportunity is to evolve from a simple event bus to a full event-sourced architecture with:
- Immutable event log as the source of truth
- CQRS separation for agent commands vs. queries
- Saga coordination for multi-agent workflows
- Temporal-style durable execution for long-running processes

### 2.5 Self-Improving Loops

#### 2.5.1 Meta-Harness (Stanford, March 2026)

Meta-Harness represents the state of the art in self-improving agent systems. It is an outer-loop system that searches over harness code for LLM applications, using an agentic proposer that accesses source code, scores, and execution traces of all prior candidates through a filesystem.

Key results:
- 7.7-point improvement over ACE (state-of-the-art context management) on text classification
- 4× fewer context tokens used
- 4.7-point average improvement on 200 IMO-level math problems across five held-out models
- Outperforms all reported Claude Haiku 4.5 harnesses on TerminalBench-2

The critical insight: **richer access to prior experience enables automated harness engineering**. The system learns from its own failures and successes to improve its orchestration code.

#### 2.5.2 Meta's Ranking Engineer Agent (REA) (March 2026)

Meta's REA autonomously executes key steps across the end-to-end ML lifecycle for ads ranking models. It:
- Autonomously generates hypotheses
- Launches training jobs
- Debugs failures
- Iterates on results
- Manages asynchronous workflows spanning days to weeks through a **hibernate-and-wake mechanism**

Results in first production rollout:
- **2× model accuracy**: REA-driven iterations doubled average model accuracy over baseline across six models
- **5× engineering output**: Three engineers delivered proposals for eight models (historically required two engineers per model)

REA demonstrates the power of self-improving loops in production: the agent learns from each experiment cycle and applies those learnings to subsequent iterations.

#### 2.5.3 Kelet AI's Diagnostic Agent (June 2026)

Kelet AI built a durable agent that continuously diagnoses quality failures in other AI agents. The key insight: AI failures don't show up like ordinary bugs. The same input succeeds ten times and fails on the eleventh, and no two failures look quite alike. The root cause is a fuzzy cluster that only becomes visible across hundreds of sessions.

Kelet's architecture:
- Process each session as it arrives
- Accumulate hypotheses about what's going wrong
- Reason across the accumulated set
- Use Temporal's durable orchestration for long-running state, multi-step pipelines, and durable pauses

#### 2.5.4 LangSmith Engine (2026)

LangSmith Engine represents a production-grade self-improving loop:
- Monitors agent traces automatically
- Detects issues in agent behavior
- Proposes fixes
- Can open pull requests with proposed fixes directly

This closes the loop from observation to improvement without human intervention (while keeping humans in the approval loop).

### 2.6 Production Patterns

#### 2.6.1 Cost Management

The "tokenmaxxing" crisis of early 2026 has forced the industry to treat cost as a first-class constraint:

- Uber exhausted its full 2026 AI budget in 4 months
- Microsoft cancelled Claude Code licenses across divisions
- Salesforce facing a $300M Anthropic bill
- One engineering lead saw coding agent bills grow 6× in two quarters

**Solutions emerging:**
- Unified cost visibility across tools (LangSmith's multi-tool tracing)
- Cost-aware orchestration (stopping loops when marginal cost exceeds value)
- Model neutrality (avoiding vendor lock-in to negotiate pricing)
- Efficient verification (batching, using smaller models for verification tasks)

#### 2.6.2 Observability

Observability has matured from "nice to have" to "production requirement":
- **LangSmith**: Unified tracing, evaluation, and debugging across all major agent tools
- **Temporal**: Billable Action Count metric, OpenMetrics support, Worker Status UI
- **Harbor**: Eval harness for running agents in reproducible, isolated environments

#### 2.6.3 Security

Running untrusted agent code is a critical production concern. LangChain's approach (June 2026):
- **Execution isolation**: WebAssembly-based sandboxing for agent-written code
- **Capability isolation**: Agents can only touch data and actions deliberately handed to them
- **Durable pauses**: Execution can stop for human input and resume without losing state

#### 2.6.4 Model Neutrality

LangChain's model neutrality argument (June 2026) draws a direct parallel to the cloud neutrality movement:
- Foundation labs are selling commodity tokens
- The gap between frontier models is closing
- Open-weight models are catching up fast
- Lock-in at the tooling layer is the real risk
- A neutral abstraction layer (like Terraform was for cloud) is needed for models

---

## 3. Key Breakthroughs & Emerging Systems

### 3.1 Breakthrough: Programmatic Orchestration

**What changed**: Agents no longer just issue tool calls in a loop. They write code that orchestrates subagents, enabling:
- Deterministic coverage (a dispatch loop doesn't skip items)
- Reliable complex orchestration (fan-out + synthesis, multi-phase pipelines)
- Context isolation (each subagent has its own context window)

**Why it matters**: This is the same pattern behind Claude Code workflows, RLMs, and Deep Agents' dynamic subagents. The agent loop is becoming a programmable orchestration layer.

### 3.2 Breakthrough: Durable Execution for Agents

**What changed**: Temporal's Workflow Streams, Serverless Workers, and Standalone Activities provide infrastructure specifically designed for long-running agent workflows.

**Why it matters**: Agents that run for hours or days need durable execution — the ability to survive restarts, pause for human input, and resume from where they left off. This is now a solved problem.

### 3.3 Breakthrough: Self-Improving Harnesses

**What changed**: Meta-Harness and LangSmith Engine demonstrate that agent harnesses can automatically improve themselves by learning from execution traces.

**Why it matters**: The harness (the code around the model) often matters as much as the model itself. Automating harness improvement is a force multiplier.

### 3.4 Breakthrough: Cost-Aware Orchestration

**What changed**: The industry has moved from celebrating token spend to treating cost as a primary optimization target.

**Why it matters**: For Angavu's informal economy context, cost efficiency is existential. Every dollar spent on inference must deliver measurable value to traders.

### 3.5 Emerging: Wiki Memory

**What changed**: Harrison Chase (LangChain CEO) identified "wiki memory" as an emerging pattern (June 2026) — agents maintain persistent, structured knowledge bases by compressing source data into agent-readable wikis.

**Why it matters**: This is fundamentally different from RAG. Instead of retrieving raw chunks at query time, a wiki precomputes and maintains higher-level synthesis. The agent doesn't rediscover structure every time.

### 3.6 Emerging: Eval-as-Infrastructure

**What changed**: Harbor (integrated with LangSmith) has emerged as the standard for evaluating long-running, stateful agents. Each trial runs in a fresh, isolated environment with deterministic checks.

**Why it matters**: You can't improve what you can't measure. Eval infrastructure is now as critical as the agent infrastructure itself.

---

## 4. Orchestration Patterns for Informal Economy

### 4.1 Pattern: Event-Sourced Agent Orchestration

**Description**: Every agent action, decision, and state transition is stored as an immutable event. The current state is derived by replaying events.

**Application to Informal Economy**:
- A trader's entire history — prices offered, deals made, routes taken, payments processed — is captured as events
- When the pricing agent recommends a price, the full chain of reasoning is recorded
- Disputes can be resolved by replaying the exact sequence of events
- New market conditions can be analyzed against historical patterns

**Angavu Mapping**:
- Event Bus → Event Store (immutable log)
- Pub/Sub → Event publication and subscription
- Dead Letter Queue → Failed event handling with compensating actions
- Agent Lifecycle → Event-sourced agent state transitions

### 4.2 Pattern: Saga-Based Multi-Step Coordination

**Description**: Complex processes (procurement → logistics → payment → delivery) are managed as sagas — sequences of local transactions with compensating actions.

**Application to Informal Economy**:
- **Procurement saga**: AdvisorAgent finds suppliers → BusinessAgent negotiates → PaymentAgent processes → LogisticsAgent coordinates delivery
- If payment fails, compensating action: cancel order, notify trader, suggest alternatives
- Each step is a local transaction; the saga coordinator ensures consistency
- Partial failures don't corrupt the entire process

**Angavu Mapping**:
- Orchestrator Agent → Saga Coordinator
- Each specialized agent (Advisor, Business, Analysis, Learning) → Saga participant
- Event Bus → Saga event propagation
- Dead Letter Queue → Saga failure handling

### 4.3 Pattern: Progressive Autonomy Ladder

**Description**: Agents earn increasing levels of autonomy based on demonstrated reliability, similar to autonomous driving levels.

**Application to Informal Economy**:
- **Level 0 (Manual)**: Agent provides information only; human makes all decisions
- **Level 1 (Assisted)**: Agent recommends actions; human approves each one
- **Level 2 (Partial)**: Agent executes routine actions autonomously; human approves exceptions
- **Level 3 (Conditional)**: Agent handles most situations; human oversees strategic decisions
- **Level 4 (High)**: Agent operates autonomously; human is notified of decisions
- **Level 5 (Full)**: Agent operates fully autonomously within defined boundaries

**For informal workers new to AI**:
- Start at Level 0: "Here are the market prices in your area"
- After 1 week of reliable use: Level 1: "I recommend buying tomatoes at 50 KES/kg. Approve?"
- After 1 month: Level 2: "I've automatically reordered your regular supplies"
- Trust is built through consistent, transparent, correct recommendations

### 4.4 Pattern: CQRS for Agent Decision-Making

**Description**: Separate the command side (agent actions that change state) from the query side (dashboards, analytics, reporting).

**Application to Informal Economy**:
- **Command side**: Agent places orders, updates prices, routes deliveries
- **Query side**: Trader dashboard shows current inventory, pending orders, revenue trends
- **Benefits**: Commands can be processed quickly; queries can be optimized independently
- **Audit**: Every command is logged; every query can be traced to its data sources

### 4.5 Pattern: Reflexion-Based Market Adaptation

**Description**: Agents reflect on outcomes and maintain episodic memory to improve future decisions.

**Application to Informal Economy**:
- PricingAgent recommends a price for tomatoes
- Outcome: tomatoes didn't sell at that price
- Reflection: "The price was too high for the Tuesday market. Tuesday buyers are more price-sensitive than weekend buyers."
- Memory: Update pricing model for Tuesday markets
- Next Tuesday: Lower price recommendation, higher sell-through

---

## 5. Application to Informal Economy

### 5.1 Continuous Optimization Through Agent Loops

**Pricing Optimization Loop**:

```
┌─────────────────────────────────────────────────────────┐
│                    PRICING OODA LOOP                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  OBSERVE: Market prices, competitor pricing, demand     │
│     │     signals, weather, seasonal patterns           │
│     ▼                                                   │
│  ORIENT: Compare against historical data, identify      │
│     │     trends, assess trader's cost basis            │
│     ▼                                                   │
│  DECIDE: Recommend price with confidence interval       │
│     │     and explanation                               │
│     ▼                                                   │
│  ACT: Update price display, notify trader,              │
│     │  adjust inventory alerts                          │
│     ▼                                                   │
│  REFLECT: Track outcome (sold? at what price? how       │
│     │     fast?), update model, log learning            │
│     ▼                                                   │
│  [Loop back to OBSERVE]                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Specific implementation for Angavu**:
- **Observe**: IntentRouter captures market signals from multiple sources (SMS price services, trader reports, weather APIs)
- **Orient**: AnalysisAgent processes signals against historical data stored in event-sourced format
- **Decide**: BusinessAgent generates price recommendation with confidence score
- **Act**: Orchestrator updates trader's pricing display and sends notification
- **Reflect**: LearningAgent tracks sales outcomes and updates pricing model

**Routing Optimization Loop**:

The same OODA pattern applies to delivery routing:
- **Observe**: Traffic conditions, delivery locations, vehicle availability
- **Orient**: Historical route performance, fuel costs, time windows
- **Decide**: Optimal route with alternatives
- **Act**: Send route to driver, update delivery estimates
- **Reflect**: Track actual delivery time vs. predicted, update model

**Matching Optimization Loop**:

For buyer-seller matching:
- **Observe**: Buyer needs, seller inventory, location proximity
- **Orient**: Historical match success rates, buyer preferences
- **Decide**: Ranked list of matches with explanations
- **Act**: Notify both parties, facilitate connection
- **Reflect**: Track match outcome (transaction completed? satisfaction?)

### 5.2 Multi-Step Process Orchestration

**Procurement-to-Delivery Saga**:

```
┌──────────────────────────────────────────────────────────────┐
│              PROCUREMENT-TO-DELIVERY SAGA                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: PROCUREMENT                                         │
│  ├── AdvisorAgent: Identify optimal suppliers                │
│  ├── AnalysisAgent: Compare prices, quality, reliability     │
│  ├── [HUMAN APPROVAL: Trader confirms supplier selection]    │
│  └── BusinessAgent: Place order                              │
│                                                              │
│  Step 2: PAYMENT                                             │
│  ├── BusinessAgent: Initiate payment via M-Pesa              │
│  ├── [HUMAN APPROVAL: Trader confirms payment amount]        │
│  └── PaymentAgent: Process transaction                       │
│                                                              │
│  Step 3: LOGISTICS                                           │
│  ├── Orchestrator: Coordinate pickup and delivery            │
│  ├── AnalysisAgent: Optimize route                           │
│  └── LogisticsAgent: Track shipment                          │
│                                                              │
│  Step 4: DELIVERY & CONFIRMATION                             │
│  ├── BusinessAgent: Confirm delivery                         │
│  ├── [HUMAN CONFIRMATION: Trader receives goods]             │
│  └── LearningAgent: Record outcome, update models            │
│                                                              │
│  COMPENSATION (if any step fails):                           │
│  ├── Cancel downstream steps                                 │
│  ├── Notify trader of failure and alternatives               │
│  ├── Log failure event for analysis                          │
│  └── LearningAgent: Update failure patterns                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 5.3 Trust and Safety for Informal Workers

**Progressive Trust Building**:

For an informal trader in Nairobi using Angavu for the first time:

**Week 1 — Observation Mode**:
- Agent provides market price information only
- No autonomous actions
- Every recommendation comes with explanation: "Tomatoes are selling at 60-80 KES/kg in Gikombasa market today. Based on your location and the current supply, I recommend 70 KES/kg."
- Trader sees that recommendations are consistently accurate

**Week 2 — Assisted Mode**:
- Agent begins suggesting actions: "Would you like me to notify you when tomato prices drop below 65 KES/kg?"
- Trader approves each suggestion
- Agent tracks approval/rejection rates to calibrate trust

**Week 3-4 — Partial Autonomy**:
- Agent handles routine notifications autonomously
- Escalates unusual situations: "Tomato prices dropped 30% overnight — this is unusual. Should I investigate?"
- Trader reviews agent's investigation reports

**Month 2+ — Conditional Autonomy**:
- Agent handles most routine decisions
- Trader reviews weekly summary of agent decisions
- Agent proactively suggests new opportunities based on learned patterns

**Trust Calibration Metrics**:
- Recommendation acceptance rate
- Escalation frequency (should decrease over time)
- Outcome accuracy (should increase over time)
- Trader satisfaction surveys

### 5.4 Self-Improving Loops for Local Market Adaptation

**Market Condition Adaptation**:

Informal markets have unique characteristics that generic AI models don't capture:
- **Seasonal patterns**: Mango prices in Kenya follow predictable seasonal patterns, but local festivals and school terms create micro-peaks
- **Day-of-week effects**: Tuesday market prices differ from Saturday market prices
- **Weather impacts**: Rain affects both supply (farmers can't transport) and demand (fewer buyers walk to market)
- **Social dynamics**: Certain traders have reputation effects that influence pricing

**Self-Improvement Loop**:

```
┌────────────────────────────────────────────────────────────┐
│            MARKET ADAPTATION SELF-IMPROVING LOOP            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. OBSERVE: Collect market data from all traders           │
│     ├── Prices offered and accepted                         │
│     ├── Transaction volumes                                 │
│     ├── Inventory levels                                    │
│     └── External signals (weather, events, holidays)        │
│                                                            │
│  2. ANALYZE: Pattern recognition across data                │
│     ├── Identify new seasonal patterns                      │
│     ├── Detect demand shifts                                │
│     ├── Find pricing anomalies                              │
│     └── Compare predictions vs. actuals                     │
│                                                            │
│  3. LEARN: Update models and heuristics                     │
│     ├── Adjust pricing models for local conditions          │
│     ├── Update routing algorithms                           │
│     ├── Refine matching criteria                            │
│     └── Generate insights for traders                       │
│                                                            │
│  4. APPLY: Deploy improved models                           │
│     ├── A/B test new recommendations                        │
│     ├── Monitor performance                                 │
│     └── Roll back if performance degrades                   │
│                                                            │
│  5. VERIFY: Validate improvements                           │
│     ├── Compare outcomes before/after                       │
│     ├── Statistical significance testing                    │
│     └── Trader feedback collection                          │
│                                                            │
│  [Loop back to OBSERVE]                                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 6. Angavu Integration Recommendations

### 6.1 Architecture Evolution: From Event Bus to Event-Sourced Orchestration

**Current Architecture**:
- Event bus with pub/sub messaging
- Dead letter queue
- Agent lifecycle management
- On-device agents (Orchestrator, IntentRouter, ModelRouter, AdvisorAgent, BusinessAgent, AnalysisAgent, LearningAgent)

**Recommended Evolution**:

1. **Add Event Store**: Transform the event bus into an event-sourced architecture where every agent action, decision, and state transition is stored as an immutable event. This provides:
   - Complete audit trail for trust and compliance
   - Time-travel debugging for agent failures
   - Historical data for self-improving loops

2. **Implement CQRS**: Separate agent commands (actions that change state) from queries (dashboards, analytics). This enables:
   - Fast command processing for real-time agent actions
   - Optimized query models for trader dashboards
   - Independent scaling of read and write paths

3. **Add Saga Coordinator**: Transform the Orchestrator Agent into a saga coordinator that manages multi-step processes with compensating actions. This enables:
   - Reliable procurement-to-delivery workflows
   - Graceful failure handling
   - Partial progress tracking

4. **Integrate Durable Execution**: Adopt Temporal-style durable execution for long-running agent workflows. This enables:
   - Agents that survive restarts
   - Human-in-the-loop pauses
   - Reliable multi-day processes

### 6.2 Agent Loop Improvements

1. **Implement Programmatic Orchestration**: Move from sequential tool calls to script-based orchestration for complex tasks. When the PricingAgent needs to analyze 100 market signals, it should write a script that processes them in parallel, not make 100 sequential API calls.

2. **Add Verification Layers**: Implement efficient verifiers (following LangChain Labs/Harvey patterns) that check agent outputs before presenting them to traders. Use batch verification with smaller models to reduce costs.

3. **Implement Reflexion**: Add self-reflection loops where agents analyze their own decisions and outcomes, maintaining episodic memory of what worked and what didn't.

4. **Cost-Aware Orchestration**: Implement token budgets and cost gates in all agent loops. Every inference call should be justified by expected value.

### 6.3 Human-in-the-Loop Implementation

1. **Progressive Autonomy Framework**: Implement the five-level autonomy ladder (Section 4.3) with clear escalation criteria at each level.

2. **Trust Calibration Dashboard**: Provide traders with a dashboard showing:
   - Agent recommendation accuracy over time
   - Escalation frequency trends
   - Cost savings from agent recommendations
   - Comparison with manual decision-making

3. **Transparent Reasoning**: Every agent recommendation must include a clear explanation in the trader's language. Use the Wiki Memory pattern to maintain agent-readable knowledge bases about local market conditions.

4. **Override and Feedback**: Traders must be able to easily override agent decisions and provide feedback. This feedback feeds the self-improving loop.

### 6.4 Self-Improving Loop Implementation

1. **Market Adaptation Engine**: Implement a Meta-Harness-inspired system that continuously improves pricing, routing, and matching models based on outcome data.

2. **A/B Testing Framework**: New model versions should be A/B tested against current versions before full deployment.

3. **Performance Monitoring**: Implement LangSmith-style observability that tracks:
   - Agent decision accuracy
   - Cost per decision
   - Latency
   - Trader satisfaction

4. **Automated Improvement**: Implement LangSmith Engine-style automated issue detection and fix proposals for agent harnesses.

### 6.5 Specific Technical Recommendations

| Component | Current | Recommended | Priority |
|-----------|---------|-------------|----------|
| Event Bus | Simple pub/sub | Event-sourced with immutable log | High |
| Orchestrator | Sequential coordination | Saga coordinator with compensation | High |
| Agent Loops | Tool-call based | Programmatic orchestration | Medium |
| Memory | Stateless per session | Wiki Memory + episodic memory | Medium |
| Observability | Basic logging | Unified tracing + evaluation | High |
| Cost Management | None | Token budgets + cost gates | High |
| Human Oversight | Manual escalation | Progressive autonomy framework | High |
| Self-Improvement | None | Meta-Harness-inspired optimization | Medium |
| Security | Basic | WASM sandboxing + capability isolation | Medium |
| Model Selection | Fixed | Model-neutral with routing | Low |

---

## 7. Statistical Data & Performance Benchmarks

### 7.1 Agent Loop Performance

| System | Metric | Value | Source |
|--------|--------|-------|--------|
| RLM-Qwen3-8B | Improvement over base model | +28.3% average | Zhang et al., 2026 |
| RLM on GPT-5 | vs. compaction | +26% median | Zhang et al., 2026 |
| RLM on GPT-5 | vs. CodeAct | +130% median | Zhang et al., 2026 |
| RLM on GPT-5 | vs. Claude Code | +13% median | Zhang et al., 2026 |
| RLM | Context window extension | 100× beyond model limit | Zhang et al., 2026 |
| Meta-Harness | Text classification improvement | +7.7 points over ACE | Lee et al., 2026 |
| Meta-Harness | Context token reduction | 4× fewer tokens | Lee et al., 2026 |
| Meta-Harness | Math reasoning improvement | +4.7 points avg (200 IMO problems) | Lee et al., 2026 |
| Meta REA | Model accuracy improvement | 2× over baseline | Meta Engineering, 2026 |
| Meta REA | Engineering output multiplier | 5× (3 engineers = 15 historically) | Meta Engineering, 2026 |
| Reflexion | HumanEval pass@1 | 91% (vs. GPT-4's 80%) | Shinn et al., 2023 |

### 7.2 Cost Data

| Company | Impact | Source |
|---------|--------|--------|
| Uber | Exhausted full 2026 AI budget in 4 months | LangChain Blog, July 2026 |
| Microsoft | Cancelling Claude Code licenses across divisions | LangChain Blog, July 2026 |
| Salesforce | $300M Anthropic bill | LangChain Blog, July 2026 |
| Mid-sized startup | Coding agent bill grew 6× in two quarters | LangChain Blog, July 2026 |

### 7.3 Orchestration Framework Adoption

| Framework | Notable Users | Key Capability |
|-----------|---------------|----------------|
| LangGraph | Klarna, Uber, J.P. Morgan | Durable execution, HITL, persistence |
| Temporal | Enterprise-wide | Durable execution, Workflow Streams |
| Google ADK | Google ecosystem | Graph Workflows, multi-language |
| CrewAI | Production deployments | Multi-agent crews and flows |

### 7.4 Supply Chain Agent Deployment

| Company | Agent Count | Use Cases | Source |
|---------|-------------|-----------|--------|
| Leading agricultural equipment company | 1,000+ agents | Orchestration, scenario planning, visibility | SAP, June 2026 |
| Global chemicals company | Multiple | Planning, scenario management, explainability | SAP, June 2026 |
| Home appliance company | Selective | Forecasting, transport, safety, logistics | SAP, June 2026 |

---

## 8. Future Trajectory

### 8.1 Self-Organizing Systems (2026-2027)

The next frontier is agents that organize themselves — spawning subagents as needed, reconfiguring workflows based on load, and adapting architectures based on performance data. Dynamic Subagents in Deep Agents (June 2026) are the first step: agents write orchestration code that can spawn, coordinate, and terminate subagents programmatically.

### 8.2 Emergent Workflows

As agent systems grow more complex, workflows will emerge from agent interactions rather than being pre-designed. This is already visible in Meta's REA, where the agent discovers its own experimentation strategies. For Angavu, this could mean:
- Traders' collective behavior patterns inform agent strategies
- Market dynamics self-organize pricing and routing algorithms
- Agent teams form and dissolve based on demand

### 8.3 Ambient Agents

Temporal's "Intelligent Business" model envisions ambient agents that continuously monitor and process data, presenting insights to humans when relevant. For informal economy:
- Ambient pricing agents that monitor markets 24/7
- Ambient logistics agents that optimize routes in real-time
- Ambient matching agents that connect buyers and sellers proactively

### 8.4 Agent-to-Agent Economies

As agents become more capable, they will transact with each other — negotiating prices, coordinating logistics, and managing payments. For informal economy:
- A trader's procurement agent negotiates with a supplier's sales agent
- Logistics agents coordinate across multiple traders for shared transport
- Payment agents settle accounts automatically

### 8.5 Regulatory and Trust Frameworks

Stanford's Three-Pillar Model and Microsoft's defense-in-depth framework are early indicators of a coming regulatory landscape. Angavu should:
- Build audit trails from day one (event sourcing)
- Implement progressive autonomy to demonstrate safety
- Participate in industry standards development
- Prepare for compliance requirements

---

## 9. Citation List

### Academic Papers

1. **Zhang, A.L., Kraska, T., Khattab, O.** (2026). "Recursive Language Models." arXiv:2512.24601v3, May 2026. https://arxiv.org/abs/2512.24601

2. **Lee, Y., Nair, R., Zhang, Q., Lee, K., Khattab, O., Finn, C.** (2026). "Meta-Harness: End-to-End Optimization of Model Harnesses." arXiv:2603.28052, March 2026. https://arxiv.org/html/2603.28052v1

3. **Cheng, E.C., Cheng, J., Siu, A.** (2026). "Toward Safe and Responsible AI Agents: A Three-Pillar Model for Transparency, Accountability, and Trustworthiness." arXiv:2601.06223, January 2026. https://arxiv.org/html/2601.06223v1

4. **Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., Yao, S.** (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." arXiv:2303.11366. https://arxiv.org/abs/2303.11366

### Industry Reports & Blog Posts

5. **LangChain** (2026). "Introducing Dynamic Subagents in Deep Agents." June 29, 2026. https://www.langchain.com/blog/introducing-dynamic-subagents-in-deep-agents

6. **LangChain** (2026). "How to Use RLMs in Deep Agents." July 1, 2026. https://www.langchain.com/blog/how-to-use-rlms-in-deep-agents

7. **LangChain** (2026). "Your coding agent bill doubled. Here's how to fix it." July 2, 2026. https://www.langchain.com/blog/fix-your-coding-agent-bill

8. **LangChain** (2026). "Running Untrusted Agent Code Without a Sandbox." June 30, 2026. https://www.langchain.com/blog/running-untrusted-agent-code-without-a-sandbox

9. **LangChain** (2026). "Why Model Neutrality Matters More Than Cloud Neutrality." June 4, 2026. https://www.langchain.com/blog/model-neutrality

10. **LangChain** (2026). "Designing Efficient Verifiers for Legal Agents." June 2, 2026. https://www.langchain.com/blog/designing-efficient-verifiers-for-legal-agents

11. **LangChain** (2026). "Harbor x LangChain: A Unified Stack for Evaluating Agents." June 30, 2026. https://www.langchain.com/blog/unified-stack-for-evaluating-agents

12. **Chase, H.** (2026). "Wiki Memory." Harrison's In the Loop, June 30, 2026. https://www.langchain.com/blog/wiki-memory

13. **Temporal** (2026). "Announcing new Temporal capabilities from Replay 2026." May 6, 2026. https://temporal.io/blog/replay-2026-product-announcements

14. **Temporal** (2026). "Workflow Streams: Live interactivity for agents and other applications." June 17, 2026. https://temporal.io/blog/workflow-streams-live-interactivity-agents-other-applications

15. **Temporal** (2026). "Stop failing on the path to production: A better way for agentic platforms." June 23, 2026. https://temporal.io/blog/stop-failing-on-the-path-to-production-a-better-way-for-agentic-platforms

16. **Baku, A.** (2026). "We built a durable agent that debugs durable agents." Temporal Blog, June 18, 2026. https://temporal.io/blog/we-built-a-durable-agent-debugs-durable-agents

17. **Anthropic** (2025). "Effective context engineering for AI agents." September 29, 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

18. **Microsoft** (2026). "Defense in depth for autonomous AI agents." May 14, 2026. https://www.microsoft.com/en-us/security/blog/2026/05/14/defense-in-depth-autonomous-ai-agents/

19. **SAP** (2026). "Autonomous Supply Chain: Why Agentic AI Is Rewriting the Operating Model." June 4, 2026. https://news.sap.com/2026/06/autonomous-supply-chain-why-agentic-ai-is-rewriting-the-operating-model/

20. **Meta Engineering** (2026). "Ranking Engineer Agent (REA): The Autonomous AI Agent Accelerating Meta's Ads Ranking Innovation." March 17, 2026. https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/

21. **Google** (2026). "Agent Development Kit (ADK)." https://adk.dev/

22. **CrewAI** (2026). "Documentation." https://docs.crewai.com/

23. **Axoniq** (2026). "Event Sourcing Tutorial: How to Go From Zero to Production-Ready." March 11, 2026. https://www.axoniq.io/blog/event-sourcing-tutorial-beginner-guide

24. **Conduktor** (2026). "CQRS and Event Sourcing with Kafka." June 24, 2026. https://www.conduktor.io/glossary/cqrs-and-event-sourcing-with-kafka

25. **LangChain** (2026). "LangGraph Overview." https://docs.langchain.com/oss/python/langgraph/overview

26. **Srinivasan, A.** (2026). "The Complete Guide for LangChain & LangGraph." April 6, 2026. https://aishwaryasrinivasan.substack.com/p/the-complete-guide-for-langchain

27. **Ruan, J.T.** (2026). "ADK 2.0 vs LangGraph vs LlamaIndex Workflows: A Deep Technical Comparison." LinkedIn, March 31, 2026. https://www.linkedin.com/pulse/adk-20-vs-langgraph-llamaindex-workflows-deep-jin-tan-ruan-x6cie

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **OODA Loop** | Observe-Orient-Decide-Act cycle for agent decision-making |
| **ReAct** | Reason + Act pattern interleaving reasoning traces with actions |
| **Reflexion** | Self-reflection framework where agents learn from verbal feedback |
| **RLM** | Recursive Language Model — processes long inputs through recursive self-calls |
| **CQRS** | Command Query Responsibility Segregation — separating writes from reads |
| **Saga** | Sequence of local transactions with compensating actions for distributed systems |
| **Event Sourcing** | Storing every state change as an immutable event |
| **Durable Execution** | Infrastructure that survives restarts and enables long-running workflows |
| **Wiki Memory** | Persistent, structured knowledge base maintained by agents |
| **HITL** | Human-in-the-Loop — keeping humans involved in agent decision-making |
| **DLQ** | Dead Letter Queue — holding area for failed messages/events |

---

## Appendix B: Angavu Architecture Mapping

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANGAVU EVOLVED ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Event Store  │◄───│  Event Bus   │───►│  Saga        │       │
│  │ (Immutable)  │    │  (Pub/Sub)   │    │  Coordinator │       │
│  └──────┬──────┘    └──────────────┘    └──────┬───────┘       │
│         │                                       │               │
│         ▼                                       ▼               │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ CQRS Read   │    │  Agent       │    │  Progressive │       │
│  │ Model       │    │  Runtime     │    │  Autonomy    │       │
│  └─────────────┘    └──────────────┘    └──────────────┘       │
│                            │                                    │
│         ┌──────────────────┼──────────────────┐                │
│         ▼                  ▼                  ▼                │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Orchestrator │    │ IntentRouter │    │ ModelRouter  │       │
│  │ (Saga)      │    │              │    │ (Neutral)    │       │
│  └──────┬──────┘    └──────────────┘    └──────────────┘       │
│         │                                                       │
│  ┌──────┼──────────────────────────────────┐                   │
│  ▼      ▼          ▼           ▼           ▼                   │
│ Advisor Business  Analysis  Learning    Payment               │
│ Agent   Agent     Agent     Agent       Agent                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Self-Improving Loop                         │   │
│  │  Observe → Analyze → Learn → Apply → Verify → [Loop]    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Observability Layer (LangSmith-style)        │   │
│  │  Tracing │ Evaluation │ Cost Tracking │ Debugging        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

*End of Swarm 4 Research Report*
*Prepared for Angavu Intelligence — July 7, 2026*
