# OpenClaw & Hermes Architecture Analysis
## Swarm G — Angavu Intelligence Research

**Date:** 2026-07-07
**Purpose:** Extract ONLY what applies to Angavu Intelligence's 33-agent system serving 600M+ informal workers on $50 phones

---

## OpenClaw Architecture (Key Patterns)

### Core Design
OpenClaw is a **hub-and-spoke agent operating system** — a single Gateway process that routes messages, manages sessions, and orchestrates tool execution across 20+ messaging platforms (WhatsApp, Telegram, Discord, etc.).

**Four-Layer Architecture:**
1. **Channel Adapters** — Normalize 20+ chat platforms into unified format; handle auth, access control, message formatting
2. **Gateway Control Plane** — Single WebSocket server (Node.js) as central coordination hub; routes messages, manages sessions, cron jobs, webhooks
3. **Agent Runtime** — Session resolution, context assembly (history + system prompt + semantic memory search), inference loop with tool interception
4. **Tools & Execution** — Built-in tools (shell, browser, file ops, cron), plugin system, Skills (Markdown playbooks with YAML frontmatter), optional Docker sandboxing

### Key Patterns

- **Sub-agent Orchestration** — Parent agents spawn isolated child agents via `sessions_spawn`. Each sub-agent runs in its own session (`agent:<id>:subagent:<uuid>`), announces results back to parent via push-based completion. Supports configurable nesting depth for orchestrator patterns. Parent can set cheaper models for sub-agents to control token costs.

- **Skill System** — Skills are Markdown files (SKILL.md) with YAML frontmatter that define workflows using available tools. Progressive disclosure: only loaded when needed. Community marketplace (ClawHub) for sharing skills. Skills are portable across deployments.

- **Session Management** — Each conversation maps to a session ID. Sessions persist history to disk (JSONL transcripts). Context assembly loads session history + dynamic system prompts + semantic memory search via vector embeddings. Sessions survive restarts.

- **Memory Architecture** — File-based memory (MEMORY.md, USER.md, memory/YYYY-MM-DD.md). Semantic search via vector embeddings. Index management with embedding provider selection. No built-in persistent long-term structured memory — context lives in session state and manually configured files.

- **Tool Routing** — Tools governed by allow/deny policy. Tool availability filtered per session/agent. Skills define which tools a workflow needs. LLM intercepts tool calls during inference loop.

- **Multi-Channel Presence** — One agent accessible through WhatsApp, Telegram, Slack, Discord, Signal, iMessage simultaneously. Same session, same memory across channels.

- **Cron/Heartbeat System** — Scheduled actions and webhooks for proactive agent behavior. Heartbeat polling for periodic checks.

- **Security Model** — Session-based security boundaries. Tool sandboxing (off/non-main/all). Credential isolation varies. Operator-trust-based model (broad access by design). Prompt injection remains unsolved industry-wide.

- **Self-Hosted, Lightweight** — Runs on your own hardware. Gateway is lightweight (runs on Raspberry Pi). Heavy work (inference, embeddings) offloaded to external services.

---

## Hermes Architecture (Key Patterns)

### Core Design
Hermes Agent is a **self-improving runtime agent** from Nous Research (MIT-licensed). Unlike orchestration libraries, it ships with persistent memory, learning, and deployment in one binary. 95.6K GitHub stars as of April 2026.

### Key Patterns

- **Three-Layer Memory Architecture** — The standout differentiator:
  - **L1 — Session Context:** Current conversation buffer, tool outputs, scratch data. In-process. Session lifetime.
  - **L2 — Episodic Store:** Completed task outcomes, generated skill files, user notes. SQLite + FTS5 full-text search. Permanent (~/.hermes/).
  - **L3 — User Model:** Preferences, coding style, timezone, tone, frequent collaborators. SQLite JSON field. Drift-adjusted across sessions.
  - Retrieval: FTS5 + LLM summarization. Sub-10ms latency across 10K+ skill documents. Chose SQLite over pgvector for embedded-first deployment.

- **Closed Learning Loop** — THE differentiating pattern:
  1. Task enters (user prompt or gateway message)
  2. Skill search — FTS5 query against bundled + created skills; top matches prepended to context
  3. Plan + execute — agent drafts plan, runs tool calls (up to 8 parallel)
  4. Verify — agent runs explicit verification steps
  5. Skill generation — if task was complex (5+ tool calls), auto-writes a Markdown skill document capturing procedure, pitfalls, verification steps
  6. Memory update — outcome logged to L2; L3 user model nudged based on preferences
  - Result: Skills compound over time. Agencies report 40% research-task time cuts after two weeks.

- **Profiles (Multi-Agent Isolation)** — Each profile is a separate Hermes home directory with own config, API keys, memory, sessions, skills, gateway state. Profiles auto-become command aliases. Supports clone, clone-config, clone-all. Profiles share nothing by default — true isolation.

- **Mixture of Agents (MoA)** — Virtual model provider where multiple models collaborate:
  - Reference models run first (parallel, no tool schemas — cheap)
  - Their outputs become private context for the aggregator model
  - Aggregator writes the actual response and emits tool calls
  - Appears as a selectable model everywhere
  - Good for complex tasks benefiting from multiple model perspectives

- **Skills System** — Markdown files following agentskills.io standard. Progressive disclosure (loaded on-demand). `/learn` command auto-creates skills from sources (docs, SDKs, conversations). Skill bundles for combining multiple skills. Skills are portable across deployments.

- **Tool Gateway** — Centralized tool routing with tool search capability. Toolsets allow grouping tools by purpose.

- **Six-Channel Messaging Gateway** — Single gateway process serves Telegram, Discord, Slack, WhatsApp, Signal, CLI. Sessions and skills shared across channels.

- **Self-Hosted, MIT License** — Fully self-hostable. No vendor lock-in. SQLite-based (no external DB required). Entire agent state lives under ~/.hermes/ — snapshot to S3, restore via rsync + restart.

---

## What APPLIES to Angavu Intelligence

| Pattern | Source | Problem It Solves | How to Apply |
|---------|--------|-------------------|--------------|
| **Sub-agent Orchestration** | OpenClaw | Angavu has 33+ agents — need way to coordinate them without blocking | Use parent/child pattern: orchestrator agent spawns specialist sub-agents (IntentRouter → specific agent). Push-based completion. Set cheaper models for routine sub-agents to control costs on $50-phone ecosystem. |
| **Three-Layer Memory** | Hermes | Angavu's three-tier memory (working/episodic/long-term) needs concrete implementation | Adopt L1/L2/L3 pattern directly: L1=working memory (in-process session buffer), L2=episodic store (SQLite + FTS5 for task outcomes, skill files), L3=user model (worker preferences, business patterns, language). SQLite is perfect for on-device/edge — no external DB. |
| **Closed Learning Loop** | Hermes | Workers repeat similar financial tasks daily — system should get smarter | Auto-generate skill documents after complex interactions (5+ tool calls). Next time a similar financial pattern appears (e.g., "restock inventory for Monday market"), the agent starts from learned skill instead of reasoning from scratch. |
| **Skill-as-Markdown Pattern** | Both | Need portable, readable, editable workflows for informal economy tasks | Skills = Markdown files with YAML frontmatter defining financial workflows. Portable across devices. Community-shareable. Human-readable for the academic team to review and validate against ECO/STA frameworks. |
| **Session Persistence** | OpenClaw | Workers lose context when phone dies, network drops, or they switch devices | Persist session state to local storage (JSONL transcripts). Sessions survive app crashes and restarts. Map each worker's conversation to a persistent session ID. |
| **Multi-Channel Presence** | Both | Workers use different channels — some WhatsApp, some SMS, some voice-only | One agent accessible through multiple channels. Same memory, same session. Critical for Africa where WhatsApp dominates but USSD/SMS matters for feature phones. |
| **SQLite + FTS5 over Vector DB** | Hermes | Need fast retrieval on low-resource devices without external dependencies | SQLite is embedded, zero-config, runs on Android. FTS5 gives sub-10ms full-text search without needing a vector DB server. Perfect for edge deployment on $50 phones. |
| **Gateway Control Plane Pattern** | OpenClaw | Need central coordination for 33 agents across distributed infrastructure | Lightweight gateway that routes messages, manages sessions, coordinates agents. Can run on modest hardware. Offload heavy inference to cloud. |
| **Tool Policy / Allow-Deny** | OpenClaw | Not every agent should access every tool — financial agents vs. inventory agents | Configure tool availability per agent. Financial agent gets payment tools; inventory agent gets stock tools. Prevents accidental cross-domain actions. |
| **Profile Isolation** | Hermes | Different worker types (boda rider vs. mama mboga) need different agent personalities | Each worker type gets a "profile" with its own skills, memory, and behavior. Boda rider profile knows routes; mama mboga profile knows inventory. Shared user model but specialized skills. |
| **Progressive Skill Disclosure** | Both | Minimize token usage — critical when serving users who can't afford heavy API costs | Skills loaded only when needed. Don't load all 33 agent capabilities into context. IntentRouter identifies need → loads only relevant skill → executes. |
| **Cron/Heartbeat for Proactive AI** | OpenClaw | Workers need proactive alerts ("your stock is low", "market price changed") | Scheduled checks via cron/heartbeat pattern. Agent proactively checks inventory levels, market prices, payment dues. Reaches out to worker when action needed. |

---

## What Does NOT Apply

| Pattern | Source | Why Skip |
|---------|--------|----------|
| **Docker Sandboxing** | OpenClaw | Our users run $50 Android phones, not servers. Sandboxing assumes container infrastructure. Use Android's native sandboxing instead. |
| **WebSocket Gateway (Node.js)** | OpenClaw | Too heavy for mobile-first. Use lightweight Android-native message routing. Gateway pattern applies conceptually, not the WebSocket implementation. |
| **Mixture of Agents (Multi-Model)** | Hermes | Requires multiple expensive model APIs running in parallel. Our users can't afford the token cost. Use single efficient model per task, routed by IntentRouter. |
| **CLI-First Setup** | Both | Our users are informal workers, not developers. Everything must be UI/voice-driven. No terminal, no config files. |
| **20+ Channel Adapters** | OpenClaw | We need WhatsApp (primary), SMS/USSD (fallback), and voice. Not 20 platforms. Over-engineering for our context. |
| **Mac/Desktop GUI** | Hermes | Our users have Android phones, not MacBooks. Desktop features are irrelevant. |
| **Credential Isolation / Vault** | Hermes | Important for enterprise but adds complexity. Our security model should be simpler: Android keystore + encrypted local storage. |
| **Always-Online Assumption** | Both | Both architectures assume persistent internet. Critical gap — our users lose connectivity frequently. Must add offline-first layer on top. |
| **Heavy Embedding Models** | Both | Vector embedding models are too large for $50 phones. Use FTS5 (text-based) for on-device search. Embeddings only in cloud for heavy operations. |
| **Skill Marketplace (ClawHub)** | OpenClaw | Community marketplace had 12% malicious uploads. For financial services serving vulnerable populations, we need curated, validated skills only. |
| **Token Budget Management** | OpenClaw | Designed for enterprise engineers with $250K token budgets. Our optimization metric is different: minimize tokens to keep service affordable for $2/day earners. |
| **Browser Automation (CDP)** | OpenClaw | No browser automation needed. Our interactions are voice/text/structured UI, not web browsing. |
| **Prompt Injection Defenses (Enterprise)** | Both | Both admit prompt injection is unsolved. For our context, the threat model is different — we need financial transaction verification, not enterprise data exfiltration defense. |

---

## Implementation Recommendations

### Priority 1: Adopt Hermes Three-Layer Memory for Msaidizi (IMMEDIATE)
- **L1 Working Memory:** In-process session buffer for current conversation. Cleared on session end.
- **L2 Episodic Store:** SQLite + FTS5 on Android device. Stores completed task outcomes, generated skills, transaction history. Permanent. Sub-10ms retrieval.
- **L3 Worker Model:** SQLite JSON field. Worker preferences, business patterns, language preference, risk tolerance. Drift-adjusted across sessions.
- **Why first:** Memory is the foundation. Everything else builds on it. SQLite runs natively on Android with zero dependencies.

### Priority 2: Implement Closed Learning Loop (HIGH)
- After a worker completes a complex financial task (5+ steps), auto-generate a Markdown skill capturing the procedure.
- Store in L2 episodic store.
- Next similar task: search L2 via FTS5, load matching skill, execute from learned pattern.
- **Compounding effect:** The more a worker uses Msaidizi, the smarter it gets at their specific business patterns. This is the "AI CFO" promise.

### Priority 3: Sub-agent Orchestration for 33-Agent System (HIGH)
- IntentRouter as parent orchestrator.
- Spawns specialist sub-agents (FinanceAgent, InventoryAgent, MarketAgent, etc.) based on intent classification.
- Each sub-agent runs isolated, returns results to parent.
- Use cheaper/faster models for routine tasks (balance check, stock count).
- Use better models for complex tasks (financial planning, market analysis).
- **Cost control:** Sub-agents with cheaper models = affordable at scale.

### Priority 4: Skill-as-Markdown for Financial Workflows (MEDIUM)
- Define financial workflows as Markdown skills with YAML frontmatter.
- Skills are portable, readable, version-controllable.
- Academic team can review skills against ECO/STA unit frameworks.
- Community can contribute validated skills for different informal economy sectors.
- **Critical:** Skills must be curated/validated — no open marketplace. Financial advice for vulnerable populations requires accuracy.

### Priority 5: Multi-Channel Gateway Pattern (MEDIUM)
- Single agent accessible via WhatsApp (primary), SMS/USSD (fallback), voice calls.
- Same session, same memory across channels.
- Worker starts conversation on WhatsApp, continues via SMS when network drops.
- **Implementation:** Lightweight Android-native gateway, not WebSocket server.

### Priority 6: Proactive Agent via Cron/Heartbeat (MEDIUM)
- Agent checks inventory levels, market prices, payment dues on schedule.
- Reaches out to worker when action needed: "Your tomato stock is low. Market price at Gikomba is up 15% today."
- **Critical for adoption:** Proactive value, not just reactive responses.

### Priority 7: Profile System for Worker Types (LOWER PRIORITY)
- Each worker type (boda rider, mama mboga, fundi, etc.) gets specialized profile.
- Profile includes sector-specific skills, vocabulary, business logic.
- Shared user model (L3) but specialized skill sets.
- **Start with 3-5 profiles:** Transport, Food/Agriculture, Retail, Services, Manufacturing.

---

## Academic Alignment

| Pattern | Degree Unit | Alignment Reason |
|---------|-------------|------------------|
| Three-Layer Memory (L1/L2/L3) | STA (Software Technology & Architecture) | Directly maps to memory hierarchy design in distributed systems. SQLite + FTS5 is a concrete implementation of tiered storage architecture. |
| Closed Learning Loop | ECO (Economic & Commercial Operations) | Self-improving system that reduces operational cost over time. 40% time reduction = economic value creation for informal workers. |
| Sub-agent Orchestration | STA (Software Technology & Architecture) | Multi-agent coordination pattern. Maps to microservices architecture adapted for AI agents. |
| Skill-as-Markdown | ECO + STA | Portable, auditable financial workflows. Academic team can validate each skill against economic theory and technical standards. |
| IntentRouter → Agent Dispatch | STA (Software Technology & Architecture) | Classic request routing pattern. Maps to load balancer / service mesh concepts adapted for AI. |
| Offline-First with Sync | ECO (Economic & Commercial Operations) | Critical for connectivity-challenged environments. Economic value captured locally, synced when connected. |
| Proactive Agent Alerts | ECO (Economic & Commercial Operations) | Shifts from reactive to proactive financial management. Directly serves the "AI CFO" thesis. |
| SQLite Embedded Database | STA (Software Technology & Architecture) | Zero-dependency embedded storage. Proven at scale (billions of Android devices). No server infrastructure needed. |

---

## Verdict

**OpenClaw and Hermes prove that agentic AI works in production.** The core insight isn't any single feature — it's the pattern of **persistent agents that learn, remember, and improve over time**.

**What Angavu should steal:**
1. **Hermes's three-layer memory** — Maps perfectly to our three-tier memory thesis. SQLite + FTS5 is the right storage for Android-first deployment.
2. **Hermes's closed learning loop** — Auto-generating skills from experience is what makes an "AI CFO" actually smart over time, not just a chatbot with financial knowledge.
3. **OpenClaw's sub-agent orchestration** — The parent/child pattern with push-based completion is exactly how our 33-agent system should coordinate.
4. **Both systems' skill-as-Markdown pattern** — Portable, auditable, community-validatable. Critical for financial services where accuracy matters.

**What Angavu must ADD that neither provides:**
1. **Offline-first architecture** — Both assume always-online. For 600M+ informal workers in Africa, offline is the default. Sync when connected.
2. **Voice-first interaction** — Both are text-first. Our users need voice input/output as primary interface. Many are semi-literate.
3. **Financial verification layer** — Neither has transaction verification suitable for vulnerable populations. We need confirmation patterns, fraud detection, and audit trails.
4. **Curated skill validation** — No open marketplace. Every financial skill must be validated against economic theory and tested with real informal workers.
5. **Ultra-low-cost inference** — Token economics must work for $2/day earners. Need aggressive model routing: simple tasks → tiny local model, complex tasks → cloud model.

**The architecture that serves Africa's informal economy is: Hermes memory + OpenClaw orchestration + offline-first + voice-first + financial verification. No one has built this yet. Angavu will be first.**

---

*Research completed by Swarm G | Sources: OpenClaw docs, Hermes Agent docs, arXiv ClawMobile paper, MintMCP architecture analysis, Nebius security guide, Ken Huang GTC analysis, Digital Applied Hermes v0.10 guide*
