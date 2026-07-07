# IMPL 16 — Model Upgrade + Academic Wiring

**Author:** Implementation Swarm 16
**Date:** July 7, 2026
**Status:** ✅ Complete

---

## Summary

Upgraded Msaidizi's reasoning models from Qwen 0.5B to latest Qwen3/Qwen3.5 family, improved voice model selection (Whisper small, Microsoft Paza for Swahili), and wired Valentine's 42-degree Economics & Statistics framework into the agent system.

---

## Part 1: Reasoning Model Upgrade

### Changes to `ModelDownloader.kt`

Added new model types with tier-based selection:

| Tier | Model | Size (4-bit) | Characteristics |
|------|-------|-------------|-----------------|
| **LOW** | Qwen3.5-0.8B | ~500MB | Mobile-optimized, smallest reasoning model |
| **MID** | Qwen3-1.7B | ~1.1GB | Thinking mode, strong reasoning (Swarm 2) |
| **HIGH** | Qwen3.5-2B | ~1.2GB | Edge-optimized, best quality (Swarm 7) |

Added `ModelTier` enum (LOW, MID, HIGH) to ModelDownloader.

### Changes to `ModelManager.kt`

- Added `DeviceTier` enum with auto-detection based on RAM and CPU cores
  - LOW: ≤2GB RAM, ≤4 cores
  - MID: ≤4GB RAM, ≤8 cores
  - HIGH: >4GB RAM, >8 cores
- `getReasoningModelForTier()` — returns tier-appropriate reasoning model
- `getASRModelForTier()` — returns tier-appropriate ASR model
- `getDeviceTier()` — auto-detects and caches device capability
- `getTierDescription()` — human-readable tier name in Swahili/English
- Updated `ModelStatus` to include device tier, reasoning model name, ASR model name
- Legacy models (WISPER, QWEN_0_5B) preserved for migration compatibility

### Key Design Decisions

1. **Auto-detection** — No technical screens. Device tier detected from hardware.
2. **Progressive download** — ASR first (voice input), then reasoning, then TTS.
3. **Legacy fallback** — Old models still supported during migration.
4. **Tier caching** — Device tier cached in SharedPreferences after first detection.

---

## Part 2: Voice Model Upgrade

### ASR Improvements

| Model | Size | Best For |
|-------|------|----------|
| Whisper base | 150MB | LOW tier — basic speech recognition |
| Microsoft Paza | 200MB | MID tier — Swahili + African languages (Swarm H) |
| Whisper small | 466MB | HIGH tier — best dialect coverage |

**Selection logic:** Paza preferred for Swahili/African languages (Swarm H recommendation), Whisper small for maximum dialect coverage, Whisper base as fallback.

### TTS Improvements

| Model | Size | Language |
|-------|------|----------|
| Piper Swahili | 50MB | Primary — Swahili (sw-KE) |
| Piper Arabic | 55MB | North/East Africa coverage |

### Cascaded S2S Pipeline (Swarm H)

Updated `FallbackPipeline` documentation to reflect the cascaded architecture:
```
STT (Whisper/Paza) → LLM (Qwen3) → TTS (Piper) with streaming
```

**VoicePipeline.kt** changes:
- Tries Paza ASR first (better for Swahili), then Whisper small, then Whisper base
- Tries Qwen3.5-2B → Qwen3-1.7B → Qwen3.5-0.8B → legacy Qwen 0.5B
- Graceful fallback chain — works with any combination of available models

---

## Part 3: Academic Framework Wiring

### New File: `AcademicFramework.kt`

**31 units mapped** from Valentine's 42-unit Economics & Statistics curriculum:

#### Year 1 (Foundation)
- BCB 108 — Business Communication Skills
- ECO 100 — Development Concepts
- **ECO 101 — Introduction to Microeconomics** → AdvisorAgent, AnalysisAgent, BusinessAgent
- ECO 102 — Introduction to Macroeconomics
- ECO 103 — Mathematics for Economists
- **STA 142 — Probability Theory** → AdvisorAgent, AnalysisAgent (Bayesian inference)
- MAT 121 — Differential Calculus

#### Year 2 (Intermediate)
- **ECO 201 — Intermediate Microeconomics** → AdvisorAgent, BusinessAgent (cost optimization)
- **ECO 206 — Economics of Microfinance** → AdvisorAgent, AnalysisAgent (credit readiness)
- **STA 244 — Time Series Forecasting** → AnalysisAgent (price predictions)
- ECO 202 — Economic Statistics
- ECO 203 — Economic Statistics (advanced)

#### Year 3 (Advanced)
- **ECO 321 — Advanced Microeconomics** → AdvisorAgent, AnalysisAgent (information economics)
- **STA 341 — Theory of Estimation** → AnalysisAgent, AdvisorAgent (confidence intervals)
- ECO 322 — Advanced Macroeconomics

#### Year 4 (Mastery)
- ECO 414 — Econometrics
- STA 442 — Multivariate Analysis

### Agent → Academic Mappings

| Agent | Primary Units | What It Means |
|-------|---------------|---------------|
| **AdvisorAgent** | ECO 101, 201, 206, 321, STA 142 | Price analysis, cost optimization, credit readiness, information economics |
| **AnalysisAgent** | STA 244, 341, 142, ECO 201, 321, 414 | Time series forecasting, estimation theory, Bayesian inference |
| **BusinessAgent** | ECO 201, 101, MAT 121, ECO 103 | Production theory, MR=MC optimization, financial math |
| **MarketAgent** | ECO 101, 102, STA 244, ECO 203 | Supply/demand, inflation, price forecasting |
| **CreditAgent** | ECO 206, 321, STA 142, 341 | Microfinance theory, adverse selection, Bayesian credit scoring |
| **CommunityAgent** | ECO 100, BCB 108, STA 142, ECO 322 | Development economics, communication, welfare |

### Core Formulae (7 key formulae)

1. **Bayes' Theorem** — P(A|B) = P(B|A) × P(A) / P(B) → Alama Score
2. **Price Elasticity** — ε = (%ΔQ) / (%ΔP) → Soko Pulse
3. **Profit Maximization** — π = TR - TC, MR = MC → Biashara Pulse
4. **Search Cost Model** — Search costs ↑ → Price dispersion ↑ → Soko Pulse
5. **Credit Scoring** — Score = Σ wᵢ × P(default | featureᵢ) → Alama Score
6. **Marginal Cost** — MC = dTC/dQ → Biashara Pulse
7. **Confidence Interval** — x̄ ± z × (σ/√n) → Analysis Agent

### Integration Points

1. **AcademicFramework.generateAcademicPromptSuffix()** — Generates prompt injection for any agent type
2. **Orchestrator.buildAgentPrompt()** — Combines base prompt + academic grounding
3. **Orchestrator.getAcademicPromptSuffix()** — Quick access to academic context

### Example: How It Works

When a worker asks "Should I buy more tomatoes to sell?":

1. **AdvisorAgent** receives prompt with ECO 101 (supply/demand) + ECO 201 (cost optimization) context
2. Agent references: "Based on supply-demand analysis (ECO 101), tomato prices typically rise 20% during rainy season. Your marginal cost (ECO 201/MAT 121) is KES 30/kg. Current market price is KES 50/kg. Profit margin: KES 20/kg. Recommendation: Buy — demand is elastic (ε = -1.5) but your margin covers the risk."
3. Response passes through Orchestrator sanitization
4. Worker gets academically-grounded, actionable advice in Swahili

---

## Files Changed

| File | Change |
|------|--------|
| `app/src/main/java/com/msaidizi/app/core/ai/ModelDownloader.kt` | Added 8 new model types + ModelTier enum |
| `app/src/main/java/com/msaidizi/app/core/ai/ModelManager.kt` | Device tier detection, tier-based model selection, updated download logic |
| `app/src/main/java/com/msaidizi/app/voice/VoicePipeline.kt` | Paza ASR support, new model fallback chain |
| `app/src/main/java/com/msaidizi/app/voice/sts/SpeechToSpeechEngine.kt` | Updated FallbackPipeline docs for cascaded S2S |
| `app/src/main/java/com/msaidizi/app/agent/AcademicFramework.kt` | **NEW** — 31 units, 7 formulae, agent mappings |
| `app/src/main/java/com/msaidizi/app/agent/Orchestrator.kt` | Academic prompt injection methods |

## Backward Compatibility

- Legacy model types (WISPER, QWEN_0_5B) preserved in ModelDownloader enum
- Legacy model file names still supported in fallback chains
- All existing APIs unchanged — new methods are additive
- BundledModelManager integration unchanged

---

*"The economics and statistics aren't just a degree — they're the intellectual infrastructure for building Africa's most important economic intelligence platform."* — Valentine Owuor
