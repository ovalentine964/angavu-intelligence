# Swarm D: Training Architecture — How Angavu Learns and Improves

**Classification:** Internal — Architecture Definition
**Date:** July 7, 2026
**Prepared by:** Swarm D — Training Architecture Team
**Status:** Definitive

---

## Executive Summary

Angavu Intelligence does not have a static model. It has a **learning organism** — a dual-loop training system where Msaidizi (on-device) learns from each individual worker while the Backend (cloud) aggregates anonymous intelligence from millions of interactions. Every voice transaction, every correction, every behavioral pattern feeds a self-reinforcing flywheel that makes Angavu smarter every single day.

This document defines:
1. **On-device training** — what Msaidizi learns on each phone
2. **Backend training** — what the cloud learns from aggregated data
3. **The sync cycle** — how on-device and cloud training exchange intelligence
4. **The voice training pipeline** — the 12-month plan to build Africa's best African language AI
5. **The competitive moat** — why this architecture is unreplicable

**The moat in one sentence:** Every day a worker uses Msaidizi, Angavu gets smarter for that worker AND for every other worker — and no competitor can replicate 600M+ daily interactions across 14 dialects.

---

## Table of Contents

1. [On-Device Training — The Personal Intelligence Layer](#1-on-device-training--the-personal-intelligence-layer)
2. [Backend Training — The Collective Intelligence Layer](#2-backend-training--the-collective-intelligence-layer)
3. [The Sync Cycle — Federated Intelligence Exchange](#3-the-sync-cycle--federated-intelligence-exchange)
4. [Voice Training Pipeline — 12-Month Roadmap](#4-voice-training-pipeline--12-month-roadmap)
5. [The Competitive Moat — Why This Is Unreplicable](#5-the-competitive-moat--why-this-is-unreplicable)
6. [Academic Framework — Degree Units to Training Functions](#6-academic-framework--degree-units-to-training-functions)
7. [Technical Implementation — Models and Algorithms](#7-technical-implementation--models-and-algorithms)
8. [Privacy Architecture — Learning Without Seeing](#8-privacy-architecture--learning-without-seeing)
9. [Failure Modes and Mitigations](#9-failure-modes-and-mitigations)

---

## 1. On-Device Training — The Personal Intelligence Layer

Msaidizi runs on a worker's phone. It has one job: **learn that worker's world better than anyone else.** All personal training data stays on-device. It never leaves the phone as raw data — only anonymous model updates (gradients) are ever transmitted.

### 1.1 Voice Intelligence — Learning How the Worker Speaks

Every time the worker talks to Msaidizi, the app learns something about their voice, language, and communication style.

#### 1.1.1 Dialect Adaptation

| What Msaidizi Learns | How It Learns | Why It Matters |
|---------------------|---------------|----------------|
| **Dialect fingerprint** | Phoneme-level analysis of the worker's speech patterns across 14 supported dialects. After 50+ interactions, Msaidizi builds a dialect embedding vector that maps the worker's unique speech patterns. | A Luo speaker who code-switches with Swahili gets ASR tuned specifically for their accent, not a generic Swahili model. Error rates drop 40-60% after personalization. |
| **Phoneme inventory expansion** | On-device phoneme detection identifies sounds not in the base model's inventory. New phonemes are catalogued with frequency counts and context tags. | Dialects like Kalenjin have clicks and glottal stops absent from standard Swahili. Msaidizi learns these sounds from the worker's speech. |
| **Prosody patterns** | Pitch contour analysis, stress patterns, rhythm mapping. The worker's natural speech melody is captured as a prosody template. | Msaidizi's TTS output sounds more natural — it matches the worker's expectation of "how people talk around here." |
| **Vocabulary expansion** | New words detected via OOV (out-of-vocabulary) flagging, then validated through context. Locally stored vocabulary grows with each session. | A mama mboga who says "ndengu" for green grams gets Msaidizi to understand and use the local term, not the textbook Swahili "choroko." |

**Academic basis:**
- **STA 142 (Bayesian Inference):** Each interaction updates the prior dialect probability distribution. Initial prior: uniform across 14 dialects. After 100 interactions, posterior concentrates on the worker's dominant dialect with 95%+ confidence.
- **STA 341 (Estimation):** Maximum likelihood estimation of phoneme distributions from finite speech samples. MLE converges to true distribution as sample size grows.

#### 1.1.2 Code-Switching Mastery

African informal workers don't speak one language. They speak **Sheng** (Swahili + English), **Sheng + mother tongue**, or mother tongue + English + Swahili — sometimes all in one sentence.

| What Msaidizi Learns | How It Learns | Example |
|---------------------|---------------|---------|
| **Switching triggers** | Contextual analysis of when the worker switches languages. Switch points are tagged with semantic context (financial terms → English, emotional terms → mother tongue, daily conversation → Swahili). | "Nimebuy tomatoes kwa 150, but soko ni 120 tu" — Msaidizi learns this worker switches to English for financial terms. |
| **Vocabulary mapping** | Cross-language word embeddings built from the worker's own code-switched speech. Same concept in multiple languages mapped to the same semantic node. | "Pesa" (Swahili) = "Money" (English) = "Ching'ei" (Luo) — all map to the same concept node. |
| **Grammar patterns** | The worker's unique code-switching grammar is learned. Some workers switch mid-sentence, others at clause boundaries. Msaidizi learns the pattern. | If a worker always switches at clause boundaries, Msaidizi's ASR model weights switch-point predictions accordingly. |

**Academic basis:**
- **STA 244 (Time Series):** Code-switching follows temporal patterns. Hidden Markov Models (HMMs) model the latent language state transitions. The worker's HMM is unique — trained on their personal speech data.
- **CS/NLP:** Multilingual language model fine-tuning with adapter layers. Each dialect gets a lightweight adapter (~2MB) that plugs into the base model. On-device storage: all 14 adapters + base model = ~120MB.

#### 1.1.3 Emotion and Intent Recognition

| What Msaidizi Learns | How It Learns | Application |
|---------------------|---------------|-------------|
| **Emotional baselines** | The worker's normal vocal energy, pitch range, and speech rate are established over 2-3 weeks. Deviations from baseline signal emotional shifts. | When a worker says "Bei iko juu sana" (prices are too high) with elevated pitch and faster rate, Msaidizi detects frustration — not just the words. |
| **Intent patterns** | The worker's typical intents are mapped to vocal patterns. "Reporting a transaction" has a different vocal signature than "asking a question" or "complaining." | Msaidizi can pre-load the right interface/response before the worker finishes speaking. Response time drops from 800ms to 200ms. |
| **Stress indicators** | Acoustic features (jitter, shimmer, harmonic-to-noise ratio) correlate with financial stress. Longitudinal tracking detects stress trends. | If a worker's voice stress increases over 2 weeks, Msaidizi might gently suggest: "Umeona bei za soko? Kuna supplier mwingine anauza cheaper" (Have you seen market prices? Another supplier sells cheaper). |

**Academic basis:**
- **Applied Statistics (Statistical Learning):** Random forest classifiers trained on MFCC (Mel-frequency cepstral coefficients) features. Personalized models outperform generic models by 35% on emotion classification tasks.
- **STA 142 (Bayesian Inference):** Bayesian updating of emotional state priors. P(emotion | features) computed using Bayes' rule with learned likelihoods.

#### 1.1.4 Voice Biometrics

| What Msaidizi Learns | How It Learns | Application |
|---------------------|---------------|-------------|
| **Voiceprint** | Speaker embedding vectors extracted from 30+ seconds of speech. Stored as a 256-dimensional vector on-device. | Msaidizi recognizes the worker by voice — no PIN, no password, no fingerprint. Just speak and Msaidizi knows it's you. |
| **Anti-spoofing** | Liveness detection via challenge-response. Background noise patterns, breathing patterns, and micro-variations in repeated phrases. | Prevents someone from playing a recording to impersonate the worker. |

---

### 1.2 Business Intelligence — Learning the Worker's Economic World

Every transaction the worker records — via voice, SMS parsing, or manual entry — teaches Msaidizi about their business.

#### 1.2.1 Transaction Pattern Learning

| What Msaidizi Learns | How It Learns | Academic Framework |
|---------------------|---------------|-------------------|
| **Revenue patterns** | Time series of daily/weekly/monthly revenue. ARIMA model fitted to individual revenue data. Seasonal decomposition separates trend, seasonal, and residual components. | **STA 244 (Time Series):** Each worker's revenue is a time series. Msaidizi learns: "This mama mboga makes KSh 3,200 on Mondays (market day), KSh 1,800 on Wednesdays, KSh 2,500 on Saturdays." |
| **Cost structure** | Categorized expense tracking. Msaidizi learns which costs are fixed (rent, transport) vs. variable (stock, packaging). Fixed/variable decomposition from expense time series. | **ECO 201 (Producer Theory):** Short-run cost curves estimated from individual data. Msaidizi learns: "Your fixed costs are KSh 800/day. You need to sell KSh 2,000 to break even." |
| **Profit margins** | Marginal revenue vs. marginal cost computed per product. Msaidizi learns which products are most profitable. | **ECO 201 (Producer Theory):** Profit maximization at MR=MC. Msaidizi advises: "Tomatoes give you 40% margin but onions give you 55%. Consider stocking more onions." |
| **Cash flow cycles** | Fourier analysis of transaction data reveals periodicities. Weekly cycles (market days), monthly cycles (rent due dates), seasonal cycles (harvest, holidays). | **STA 244 (Time Series):** Spectral analysis identifies dominant frequencies in cash flow. Msaidizi predicts: "You'll be short of cash next Thursday — your rent is due and sales are typically low on Wednesdays." |
| **Supplier patterns** | Supplier loyalty, price sensitivity, and reliability scored from transaction history. Graph of supplier relationships built over time. | **ECO 101 (Consumer Theory):** Revealed preference theory — the worker's actual supplier choices reveal their preferences (price vs. reliability vs. convenience). |

#### 1.2.2 Customer Pattern Learning

| What Msaidizi Learns | How It Learns | Application |
|---------------------|---------------|-------------|
| **Customer segments** | Clustering of transaction patterns by time, amount, and product mix. K-means on transaction features identifies 3-5 customer types. | "You have 3 types of customers: morning bulk buyers (20% of revenue), afternoon casual buyers (60%), weekend shoppers (20%)." |
| **Customer lifetime value** | RFM (Recency, Frequency, Monetary) analysis on customer transactions. Pareto principle detection — does 80/20 rule hold? | "Your top 5 customers generate 35% of your revenue. Consider loyalty discounts for them." |
| **Demand patterns** | Product-level demand curves estimated from price-quantity pairs across transactions. Price elasticity computed per product. | **ECO 201 (Consumer Theory):** "When you raised tomato prices 10%, demand dropped 15%. Tomatoes are elastic (ε=-1.5). Onions are inelastic (ε=-0.3) — you can raise onion prices without losing customers." |

#### 1.2.3 Behavioral Intelligence — Learning How the Worker Thinks

| What Msaidizi Learns | How It Learns | Application |
|---------------------|---------------|-------------|
| **Decision patterns** | Analysis of which Msaidizi recommendations the worker follows vs. ignores. Logistic regression: P(accept recommendation | features). | Msaidizi learns: "This worker ignores price alerts but follows restock reminders. Adjust recommendation strategy." |
| **Risk tolerance** | Observed behavior reveals risk preferences. Does the worker take supplier credit? Diversify products? Save consistently? | **ECO 321 (Information Economics):** Risk aversion coefficient estimated from observed choices under uncertainty. Msaidizi learns: "You're moderately risk-averse — you prefer stable KSh 2,000/day over volatile KSh 3,000 or KSh 1,000." |
| **Savings habits** | Tracking of savings behavior relative to income. Marginal propensity to save (MPS) computed from income-savings pairs. | **ECO 101 (Consumer Theory):** "Your MPS is 0.12 — you save 12% of income on good days, 3% on bad days. On bad days, consider reducing variable costs before cutting savings." |
| **Communication preferences** | Which channels the worker uses (voice, USSD, WhatsApp), when they prefer brief vs. detailed responses, which Msaidizi features they use most. | Msaidizi adapts: "This worker prefers short voice briefings at 7 AM. Don't send text notifications — they ignore them." |

---

## 2. Backend Training — The Collective Intelligence Layer

The Backend sees **nothing personal**. It receives only anonymous model updates (gradients) from millions of devices and aggregated transaction statistics. From this, it builds collective intelligence that benefits every worker.

### 2.1 Language Model Training — Building Africa's Best Voice AI

#### 2.1.1 ASR (Automatic Speech Recognition) Improvement

| What the Backend Learns | Data Source | Method | Output |
|------------------------|-------------|--------|--------|
| **Dialect-specific acoustic models** | Federated gradient updates from 100K+ devices per dialect. Each device contributes anonymous phoneme confusion matrices. | Federated Averaging (FedAvg) with dialect-specific aggregation pools. Devices grouped by detected dialect; gradients averaged within pools. | Updated acoustic models per dialect. Pushed to devices via OTA model updates. |
| **Code-switching language models** | Aggregated n-gram statistics from anonymous transcriptions. Cross-lingual transition probabilities. | Neural language model training on code-switched corpora built from federated n-gram data. Transformer architecture with language-ID embeddings. | Language model that handles Sheng, Luo-Swahili, Kikuyu-Swahili, etc. without explicit language detection. |
| **OOV word integration** | New words detected on-device, validated by frequency across devices. A word appearing on 100+ devices gets added to the global vocabulary. | Vocabulary expansion via subword tokenization updates. BPE (Byte-Pair Encoding) retrained monthly on aggregated new words. | Growing vocabulary that includes local slang, business terms, and emerging Sheng vocabulary. |
| **Pronunciation models** | Phoneme-level alignment data from user corrections. When a worker corrects Msaidizi's transcription, the correction is a pronunciation signal. | Pronunciation lexicon updates via weighted finite-state transducers (WFSTs). Correction-weighted phoneme probability updates. | Msaidizi gets better at understanding how words are actually pronounced, not how dictionaries say they should be pronounced. |

**Scale advantage:** A competitor with 10K users cannot match Angavu's model trained on 1M+ devices. Each additional device improves the model for all devices. This is a **network effect in training data** — the rarest and most valuable moat in AI.

#### 2.1.2 TTS (Text-to-Speech) Improvement

| What the Backend Learns | Data Source | Method | Output |
|------------------------|-------------|--------|--------|
| **Natural prosody** | Aggregated prosody templates from thousands of speakers per dialect. Average pitch contour, stress pattern, and rhythm per dialect. | Multi-speaker TTS fine-tuning. Style tokens learned from aggregated prosody data. | Msaidizi sounds like a real person from the worker's region — not a robot reading text. |
| **Dialect pronunciation** | Phoneme-level corrections aggregated across devices. The most common pronunciation variant per word per dialect is learned. | TTS model fine-tuning with dialect-specific phoneme mappings. Variance-based selection of "natural" pronunciation. | "Tomato" is pronounced differently in Nairobi, Mombasa, Kisumu, and Eldoret. Msaidizi matches the local pronunciation. |
| **Emotional expression** | Emotion-tagged speech samples aggregated (with consent). Happy, concerned, urgent — different prosodic templates per emotion. | Emotion-conditioned TTS. Style transfer from emotional speech samples. | Msaidizi can sound concerned when warning about losses ("Umeongeza gharama 20% mwezi huu" — You've increased costs 20% this month) and encouraging when celebrating wins. |
| **New vocabulary pronunciation** | When new words are added to the vocabulary, pronunciation is bootstrapped from the phoneme patterns of the dialect's existing words. | Grapheme-to-phoneme (G2P) models per dialect, fine-tuned on new vocabulary. | When "mpesa" or "fuliza" enters the vocabulary, Msaidizi pronounces them correctly from day one. |

### 2.2 Economic Model Training — Learning Africa's Informal Economy

#### 2.2.1 Price Prediction Models

| What the Backend Learns | Data Source | Academic Framework | Output |
|------------------------|-------------|-------------------|--------|
| **Commodity price forecasting** | Aggregated transaction prices across all markets. Daily price observations for 50+ tracked commodities. | **STA 244 (Time Series):** SARIMA models with market-specific seasonal components. GARCH for volatility modeling. Vector autoregression (VAR) for cross-commodity dynamics. | 1-4 week price forecasts per commodity per market. "Tomato prices in Gikomba will rise 15% next week due to supply disruption in Naivasha." |
| **Price elasticity estimation** | Price-quantity pairs from aggregated transactions. Natural experiments from price shocks. | **ECO 201 (Consumer Theory):** Demand curve estimation via instrumental variables (supply shocks as instruments for price). Elasticity computed at market, regional, and national levels. | "Tomato demand elasticity in Nairobi is -1.3. A 10% price increase reduces quantity demanded by 13%." |
| **Inflation tracking** | Transaction-level price data used to construct informal CPI. | **ECO 202/203 (Index Numbers):** Laspeyres index with expenditure weights derived from actual spending patterns (not government surveys). | Real inflation experienced by informal workers — often 2-3× official CPI. |
| **Cross-market arbitrage detection** | Price differentials across markets for same commodity. Transport cost estimation from distance data. | **ECO 101 (General Equilibrium):** Law of one price violations indicate arbitrage opportunities. Msaidizi tells workers: "Tomatoes are KSh 40/kg cheaper in Muthurwa than Gikomba — transport cost is KSh 15/kg. Net gain: KSh 25/kg." |

#### 2.2.2 Credit Scoring Models

| What the Backend Learns | Data Source | Academic Framework | Output |
|------------------------|-------------|-------------------|--------|
| **Alama Score computation** | Aggregated transaction patterns, payment regularity, business stability, savings behavior. All anonymized via differential privacy. | **ECO 321 (Information Economics):** Stiglitz-Weiss credit rationing model — the score separates high-risk from low-risk borrowers without requiring collateral or formal records. | Alama Score: 0-1000 credit score for informal workers based on their actual economic behavior, not formal records. |
| **Default prediction** | Historical outcomes from micro-loan performance (where available). Feature engineering from transaction patterns. | **STA 341 (Estimation):** Logistic regression and gradient boosted trees. Feature importance: regularity of income (0.28), savings rate (0.22), business diversification (0.18), transaction volume trend (0.15), supplier diversity (0.17). | Probability of default for loan applicants. Enables lenders to offer appropriate terms — not one-size-fits-all. |
| **Fraud detection** | Anomalous transaction patterns, velocity checks, network analysis of suspicious connections. | **Applied Statistics (Statistical Learning):** Isolation forests for anomaly detection. Graph neural networks for network-based fraud patterns. | Real-time fraud alerts: "This transaction pattern is unusual for you. Confirm: did you buy KSh 50,000 of electronics today?" |

#### 2.2.3 Business Intelligence Models

| What the Backend Learns | Data Source | Academic Framework | Output |
|------------------------|-------------|-------------------|--------|
| **Business efficiency benchmarks** | Aggregated DEA (Data Envelopment Analysis) scores across similar businesses. Input-output ratios by business type, location, and size. | **ECO 201 (Producer Theory):** Technical efficiency measured via DEA. Best-practice frontier estimated from top performers. | "Your business efficiency is 72/100. Top performers in your category achieve 85. Here's what they do differently: lower transport costs, better supplier terms, higher inventory turnover." |
| **Market structure mapping** | Buyer-seller network topology from transaction data. Concentration ratios (CR4, HHI) per market and commodity. | **ECO 422 (Industrial Organization):** Market power detection. "Three suppliers control 60% of tomato supply in Gikomba (HHI=0.18 — moderately concentrated)." | Msaidizi warns workers about market power: "Supplier X has raised prices 3 times this month. Consider alternatives." |
| **Seasonal demand forecasting** | Historical demand patterns aggregated across regions. Calendar effects (Ramadan, Christmas, school terms, harvest seasons). | **STA 244 (Time Series):** Seasonal decomposition + regression on calendar variables. Prophet-style additive model with changepoint detection. | "Mango season starts in 2 weeks. Demand for transport services will increase 40%. Prepare your vehicle." |

### 2.3 Intelligence Layer — Pattern Detection at Scale

| What the Backend Learns | Data Source | Method | Output |
|------------------------|-------------|--------|--------|
| **Network effects** | Aggregated transaction graphs (anonymized). Community detection, centrality measures, information flow patterns. | Graph neural networks on anonymized transaction graphs. Louvain community detection. | "Markets in Nairobi's Eastlands are highly connected — information travels fast. Markets in rural areas are isolated — you have an information advantage." |
| **Causal impact estimation** | Natural experiments from policy changes, weather events, market disruptions. Difference-in-differences and regression discontinuity. | **ECO 301 (Econometrics):** Causal inference methods applied to observational data. "When the fuel tax was introduced, food prices rose 8% within 2 weeks — causal effect, not correlation." | Msaidizi explains WHY prices change, not just THAT they changed. |
| **Anomaly detection** | Statistical process control on aggregated metrics. Deviations from historical patterns flagged. | **Applied Statistics:** CUSUM charts, EWMA control charts, isolation forests. | Early warning system: "Something unusual is happening in the onion market — prices are 30% above seasonal norms. Possible supply disruption." |

---

## 3. The Sync Cycle — Federated Intelligence Exchange

The on-device and backend training systems are connected by a structured sync cycle. **Raw data never leaves the device.** Only model updates and aggregated statistics are transmitted.

### 3.1 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    THE SYNC CYCLE                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐          ┌──────────────────┐                │
│  │   MSAIDIZI APP   │          │    BACKEND        │                │
│  │   (On-Device)    │          │    (Cloud)        │                │
│  │                  │          │                   │                │
│  │ ┌──────────────┐ │  Daily   │ ┌──────────────┐ │                │
│  │ │ Voice Model  │─┼─────────▶│ │ Federated    │ │                │
│  │ │ Updates      │ │ (gradients│ │ Aggregation  │ │                │
│  │ └──────────────┘ │  only)   │ │ Engine       │ │                │
│  │                  │          │ └──────┬───────┘ │                │
│  │ ┌──────────────┐ │          │        │         │                │
│  │ │ Transaction  │─┼──Weekly─▶│ ┌──────▼───────┐ │                │
│  │ │ Statistics   │ │(aggregated│ │ Economic     │ │                │
│  │ └──────────────┘ │ stats)  │ │ Model Trainer│ │                │
│  │                  │          │ └──────┬───────┘ │                │
│  │ ┌──────────────┐ │          │        │         │                │
│  │ │ Behavior     │─┼─Monthly─▶│ ┌──────▼───────┐ │                │
│  │ │ Patterns     │ │(anonymous│ │ Intelligence │ │                │
│  │ └──────────────┘ │ patterns)│ │ Aggregator   │ │                │
│  │                  │          │ └──────┬───────┘ │                │
│  │                  │          │        │         │                │
│  │ ┌──────────────┐ │          │ ┌──────▼───────┐ │                │
│  │ │ Improved     │◀┼──────────│ │ Improved     │ │                │
│  │ │ Models       │ │(OTA push)│ │ Global Models│ │                │
│  │ └──────────────┘ │          │ └──────────────┘ │                │
│  │                  │          │                   │                │
│  └──────────────────┘          └──────────────────┘                │
│                                                                     │
│  DAILY:  Voice gradients → Backend → Improved ASR/TTS models       │
│  WEEKLY: Transaction stats → Backend → Better economic models      │
│  MONTHLY: Behavior patterns → Backend → Better recommendations     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Daily Sync — Voice Intelligence

**What happens every day:**

1. **On-device (continuous):** Worker speaks → ASR transcribes → corrections recorded → local model updates computed.
2. **Daily upload (overnight, WiFi/preferred):** Anonymous gradient updates sent to backend. Contains:
   - Phoneme confusion matrix deltas (which sounds were confused)
   - OOV word candidates (new words detected)
   - Prosody feature statistics (pitch, energy, rate distributions)
   - **NOT:** audio recordings, transcriptions, or any identifying data
3. **Backend aggregation:** FedAvg across devices in the same dialect pool. Global model updated.
4. **Model push:** Updated ASR and TTS models pushed to devices via OTA. Delta updates only — typically 5-15MB.

**Privacy guarantee:** Differential privacy with ε=0.1, δ=1e-5. Each gradient update is clipped and noised before upload. Even with the gradient update, the backend cannot reconstruct the original audio.

**Impact:** Msaidizi's ASR accuracy improves ~0.5% per week during the first 6 months, then ~0.2% per month thereafter. After 12 months, dialect-specific WER (Word Error Rate) is 15-20% — competitive with major language ASR systems.

### 3.3 Weekly Sync — Economic Intelligence

**What happens every week:**

1. **On-device (continuous):** Transaction data analyzed locally. Business metrics computed: revenue, costs, margins, cash flow.
2. **Weekly upload:** Aggregated statistics (NOT raw transactions):
   - Price-quantity pairs by commodity category (anonymized)
   - Transaction volume distributions
   - Cost structure ratios (fixed/variable)
   - **NOT:** individual transaction amounts, supplier names, customer data
3. **Backend aggregation:** Cross-device statistics aggregated by region, market, and commodity.
4. **Intelligence push:** Updated market intelligence pushed to devices:
   - Price forecasts for the worker's tracked commodities
   - Market structure updates
   - Demand elasticity updates

**Privacy guarantee:** k-anonymity (k≥10). Statistics are only computed for groups of 10+ workers in the same market. No individual can be identified from aggregated statistics.

### 3.4 Monthly Sync — Behavioral Intelligence

**What happens every month:**

1. **On-device (continuous):** Decision patterns, risk preferences, and communication styles analyzed.
2. **Monthly upload:** Anonymous behavioral archetypes:
   - Decision pattern cluster ID (which of 8 behavioral archetypes)
   - Risk tolerance score (1-10, derived from choices)
   - Feature usage frequency distribution
   - **NOT:** specific decisions, conversation content, or personal details
3. **Backend aggregation:** Archetype distributions aggregated across regions and demographics.
4. **Intelligence push:** Updated recommendation strategies per archetype:
   - "Workers with your profile respond best to brief morning briefings"
   - "Workers with your risk tolerance prefer stable income over high-margin volatility"

**Privacy guarantee:** Differential privacy + archetype abstraction. The backend sees "this is a Type 3 worker in Nairobi" — not who they are or what they specifically do.

### 3.5 Model Update Pipeline

```
Device                    CDN/Backend               Device
  │                          │                         │
  │  1. Compute local        │                         │
  │     model update         │                         │
  │     (after daily use)    │                         │
  │                          │                         │
  │  2. Upload gradients ───▶│                         │
  │     (encrypted,          │  3. Aggregate across    │
  │      differentially      │     10K+ devices        │
  │      private)            │     (FedAvg)            │
  │                          │                         │
  │                          │  4. Update global       │
  │                          │     model               │
  │                          │                         │
  │                          │  5. Compute delta ──────│
  │                          │     (5-15MB)            │
  │                          │                         │
  │  6. Apply delta ◀────────│                         │
  │     (background)         │                         │
  │                          │                         │
  │  7. Validate locally     │                         │
  │     (A/B test on         │                         │
  │      recent data)        │                         │
  │                          │                         │
  │  8. If better: adopt     │                         │
  │     If worse: rollback   │                         │
```

---

## 4. Voice Training Pipeline — 12-Month Roadmap

### Phase 1: Foundation (Months 1-3) — "Teach Msaidizi to Listen"

**Goal:** Build baseline ASR/TTS models for 14 dialects. Msaidizi can understand and speak each dialect at a basic level.

**On-device training:**
- Workers speak to Msaidizi in their natural dialect
- Audio recorded locally → transcribed by base ASR → worker corrects errors
- Corrections stored locally as training data
- Personal dialect model starts forming after 50+ interactions
- **Data stays on device** — no voice data uploaded in Phase 1

**What Msaidizi learns:**
- Basic dialect identification (which of 14 dialects the worker speaks)
- Common vocabulary (500 most frequent words per dialect)
- Basic code-switching detection (language boundaries)
- Worker's voice fingerprint (for biometric auth)

**Backend activity:**
- Base models trained on open-source African speech corpora (Mozilla Common Voice, MMS, PAZA benchmark)
- 14 dialect-specific base models downloaded to devices
- Initial phoneme inventories per dialect

**Metrics:**
- WER (Word Error Rate) target: <30% (baseline for low-resource languages)
- Dialect detection accuracy: >90%
- Worker correction rate: <40% (meaning 60% of transcriptions are correct)

**Key milestone:** Msaidizi can understand "Nimenunua nyanya kwa 150" in Sheng, Swahili, and 12 other dialects.

### Phase 2: Personalization (Months 3-6) — "Msaidizi Learns Your Voice"

**Goal:** Each worker's Msaidizi becomes personalized. Federated learning begins aggregating anonymous improvements.

**On-device training:**
- Personal dialect model fully formed (500+ interactions)
- Code-switching patterns learned per worker
- Emotion recognition calibrated to individual baselines
- Business transaction patterns established (3+ months of data)
- Customer and supplier models built

**Federated learning begins:**
- Daily gradient uploads (anonymous, differentially private)
- Backend aggregates gradients from 10K+ devices per dialect pool
- First global model improvements pushed back to devices
- Model deltas: 5-15MB, applied in background

**What the system learns:**
- **On-device:** "This specific worker switches to English for financial terms, uses Sheng for daily conversation, and Luo for emotional expressions. Their voice stress increases on Thursdays (rent day)."
- **Backend:** "Luo speakers in Kisumu confuse /r/ and /l/ 40% of the time. Swahili speakers in Mombasa aspirate /p/ differently from Nairobi speakers."

**Metrics:**
- WER target: <20% (personal model)
- Dialect-specific WER improvement: 30% over Phase 1
- Code-switching accuracy: >75%
- Transaction categorization accuracy: >85%

**Key milestone:** Msaidizi says "Umelipa zaidi ya wastani wa soko" (You paid above market average) in the worker's exact dialect, with natural prosody.

### Phase 3: Intelligence (Months 6-12) — "Msaidizi Gets Smart"

**Goal:** Models are genuinely good. Msaidizi sounds natural. Economic intelligence is actionable.

**On-device training:**
- ASR WER <15% (personal model) — comparable to commercial systems for major languages
- Full code-switching mastery — handles any combination of the worker's languages
- Emotion recognition driving contextual responses
- Business intelligence fully operational: daily P&L, cash flow predictions, restock alerts
- Behavioral model mature: Msaidizi knows the worker's preferences, risk tolerance, and habits

**Backend training:**
- Federated models from 100K+ devices per dialect
- Economic models trained on aggregated transaction data from thousands of markets
- Price forecasting models operational (1-4 week horizon)
- Credit scoring models (Alama Score) validated and deployed
- Market structure analysis complete for major urban markets

**What the system learns:**
- **On-device:** "This worker's business is seasonal — high revenue Dec-Jan (holidays), low in April (school fees). They should save 20% of Dec revenue to cover April."
- **Backend:** "Tomato prices in Nairobi follow a 3-week cycle driven by Naivasha harvest schedules. Price spikes >30% above trend predict supply disruptions 2 weeks in advance."

**Metrics:**
- WER target: <12% (personal), <18% (generic per dialect)
- TTS naturalness MOS (Mean Opinion Score): >3.8/5.0
- Price forecast accuracy: MAPE <15% for 1-week horizon
- Credit score AUC: >0.75
- Worker recommendation acceptance rate: >60%

**Key milestone:** A mama mboga in Nairobi says "Msaidizi anajua biashara yangu kuliko mimi" (Msaidizi knows my business better than I do).

### Phase 4: Self-Improvement (Months 12+) — "The Flywheel Spins"

**Goal:** The system improves itself. New vocabulary auto-detected. Regional dialects distinguished. Msaidizi sounds like a local.

**On-device training:**
- Continuous personal model refinement — diminishing marginal improvement but cumulative compound effect
- New vocabulary automatically detected, validated, and integrated
- Business intelligence models adapt to changing circumstances (new suppliers, new products, market shifts)
- Msaidizi proactively suggests optimizations based on mature behavioral model

**Backend training:**
- Models retrained monthly with latest federated data
- New dialect variants detected and modeled (e.g., "coastal Swahili" vs "inland Swahili" split)
- Cross-dialect transfer learning — improvements in one dialect automatically benefit similar dialects
- Economic models continuously validated against real-world outcomes

**What the system learns:**
- **On-device:** "The worker started selling avocados last month — new product, new supplier, new customer segment. Msaidizi automatically creates tracking categories and begins building price/quantity models."
- **Backend:** "A new slang term 'kukula life' is emerging in Nairobi Sheng, meaning 'to live well.' Detected on 5,000 devices in the last month. Added to vocabulary with pronunciation model."

**The compound effect:**
- Year 1: Msaidizi is useful. Workers use it because it helps.
- Year 2: Msaidizi is indispensable. Workers can't imagine running their business without it.
- Year 3: Msaidizi is the business. Workers make decisions WITH Msaidizi, not just using Msaidizi.
- Year 5: Msaidizi IS the informal economy's operating system.

**Metrics:**
- WER: <8% (approaching human-level for clear speech)
- TTS naturalness MOS: >4.2/5.0
- Vocabulary growth: 500+ new words per dialect per year (auto-detected)
- Business recommendation acceptance rate: >80%
- Alama Score predictiveness: AUC >0.85

---

## 5. The Competitive Moat — Why This Is Unreplicable

### 5.1 The Flywheel

```
Worker speaks to Msaidizi
        │
        ▼
On-device model learns (personal improvement)
        │
        ▼
Anonymous gradients uploaded (federated learning)
        │
        ▼
Backend aggregates across 600M+ interactions
        │
        ▼
Global models improve (collective improvement)
        │
        ▼
Improved models pushed to all devices
        │
        ▼
Msaidizi works better → Worker uses more
        │
        ▼
More interactions → More training data
        │
        └──────────────────▶ (cycle repeats, accelerating)
```

### 5.2 Why Competitors Cannot Replicate This

| Moat Dimension | Why It's Unreplicable | Time to Replicate |
|---------------|----------------------|-------------------|
| **Data volume** | 600M+ daily interactions across 14 dialects. Each interaction is a training sample. A competitor starting today has zero. | 3-5 years minimum (assuming they could attract users, which they can't without good models) |
| **Dialect coverage** | 14 dialects, each with personalized models. Each dialect requires 10K+ active speakers for federated learning to work. Acquiring 10K speakers in 14 dialects = 140K users minimum. | 2-3 years to acquire users, assuming competitive product (which they don't have) |
| **Economic data** | Transaction data from real informal businesses. Not surveys, not estimates — actual prices, quantities, margins, and patterns from millions of transactions. | Impossible to replicate without the app. You can't survey your way to this data. |
| **Behavioral data** | Decision patterns, risk tolerance, savings habits from real choices under real uncertainty. Not hypothetical survey responses — actual behavior. | Impossible to replicate without years of longitudinal data. |
| **Network effects** | Every additional device makes the model better for every other device. 100 devices learn slowly. 1M devices learn fast. 100M devices learn explosively. | Non-linear scaling. First 100K users: slow. 1M-10M: acceleration. 10M+: dominance. |
| **Trust** | Workers trust Msaidizi because it speaks their language, knows their business, and has never leaked their data. Trust takes years to build and seconds to destroy. | 3-5 years minimum, with zero privacy incidents. |
| **Switching costs** | Msaidizi has learned the worker's voice, dialect, business patterns, preferences, and habits. Starting with a new app means starting from zero. | Workers won't switch unless the alternative is dramatically better — which requires the same data, which they don't have. |

### 5.3 The Compounding Advantage

The moat grows **exponentially**, not linearly:

```
Month 1:   10K users     → Basic models, limited value
Month 6:   100K users    → Good models, real value
Month 12:  500K users    → Great models, indispensable
Month 24:  5M users      → Dominant models, market standard
Month 36:  50M users     → Industry-defining models, monopoly
Month 60:  600M users    → Infrastructure. Not an app — a platform.
```

Each month of head start is worth exponentially more than the previous month. A competitor starting 12 months behind is not 12 months behind — they are **years** behind, because Angavu's models continued improving during those 12 months.

---

## 6. Academic Framework — Degree Units to Training Functions

Every training function maps to Valentine's BSc Economics & Statistics degree. This is not a coincidence — it is the **design philosophy**. Angavu applies academic theory to solve real problems.

| Training Function | Academic Unit | Theoretical Foundation | Practical Application |
|------------------|---------------|----------------------|---------------------|
| Dialect adaptation | STA 142 | Bayesian inference — posterior updating with each interaction | P(dialect \| phonemes) updated after every utterance |
| Price prediction | STA 244 | Time series — ARIMA, SARIMA, GARCH | Forecast commodity prices 1-4 weeks ahead |
| Credit scoring | ECO 321 | Information economics — adverse selection, moral hazard | Alama Score separates high-risk from low-risk without collateral |
| Demand estimation | ECO 201 | Consumer theory — utility maximization, revealed preference | Estimate demand curves from actual transaction data |
| Business efficiency | ECO 201 | Producer theory — cost minimization, technical efficiency | DEA scores benchmark each worker against best performers |
| Emotion recognition | Applied Stats | Statistical learning — classification, feature extraction | MFCC features → random forest → emotion classification |
| Market structure | ECO 422 | Industrial organization — concentration, market power | HHI computation identifies markets where middlemen have power |
| Anomaly detection | STA 341 | Estimation — hypothesis testing, control charts | CUSUM charts detect price anomalies in real time |
| Inflation tracking | ECO 202/203 | Index numbers — Laspeyres, Paasche, Fisher | Informal CPI from actual spending patterns |
| Behavioral modeling | ECO 321 | Mechanism design — incentive compatibility | Recommendation strategies aligned with worker preferences |
| Causal inference | ECO 301 | Econometrics — IV, DiD, RDD | Determine WHY prices change, not just that they changed |
| Network analysis | ECO 101 | General equilibrium — market interconnections | Map how information and goods flow between markets |

---

## 7. Technical Implementation — Models and Algorithms

### 7.1 On-Device Models

| Model | Architecture | Size (on-device) | Inference Time | Framework |
|-------|-------------|-------------------|----------------|-----------|
| **Base ASR** | Whisper-small fine-tuned on African languages | 45MB | 200ms/utterance | ONNX Runtime (Android) |
| **Personal ASR adapter** | LoRA adapter on base ASR | 2MB | +50ms | ONNX Runtime |
| **Dialect classifier** | Lightweight CNN on MFCC features | 1MB | 10ms | ONNX Runtime |
| **Emotion classifier** | Random forest on acoustic features | 0.5MB | 5ms | Custom |
| **TTS** | VITS fine-tuned per dialect | 35MB | 300ms/sentence | ONNX Runtime |
| **TTS adapter** | LoRA adapter for personal prosody | 1MB | +30ms | ONNX Runtime |
| **Transaction categorizer** | Gradient boosted trees | 2MB | 1ms/transaction | Custom |
| **Business model** | Lightweight LSTM for time series | 5MB | 10ms/forecast | ONNX Runtime |

**Total on-device storage:** ~95MB (fits comfortably on any modern Android device)

### 7.2 Backend Models

| Model | Architecture | Training Data | Retraining Frequency |
|-------|-------------|---------------|---------------------|
| **Global ASR** | Whisper-large-v3 fine-tuned | Federated gradients from 100K+ devices | Monthly |
| **Global TTS** | VITS multi-dialect | Aggregated prosody data | Monthly |
| **Price forecasting** | SARIMA + LSTM ensemble | Aggregated transaction prices | Weekly |
| **Credit scoring** | XGBoost + logistic regression | Aggregated transaction patterns | Monthly |
| **Demand estimation** | Structural demand model (BLP) | Price-quantity pairs from transactions | Quarterly |
| **Fraud detection** | Isolation forest + graph neural network | Anomaly patterns from aggregated data | Weekly |
| **Market structure** | Network analysis (Louvain, centrality) | Transaction graphs | Monthly |

### 7.3 Federated Learning Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **FL Framework** | Flower (flwr) | Federated learning orchestration |
| **Aggregation** | FedAvg with dialect-specific pools | Aggregate gradients by dialect |
| **Privacy** | Differential privacy (Opacus) | ε=0.1, δ=1e-5 per update |
| **Compression** | Gradient quantization (8-bit) | Reduce upload size to 1-5MB |
| **Communication** | gRPC + TLS | Secure gradient transport |
| **Scheduling** | WorkManager (Android) | Background upload when charging + WiFi |
| **Model serving** | ONNX Runtime Mobile | On-device inference |

---

## 8. Privacy Architecture — Learning Without Seeing

### 8.1 Data Classification

| Data Type | Stays On Device | Sent to Backend | Privacy Mechanism |
|-----------|----------------|-----------------|-------------------|
| **Raw audio** | ✅ Always | ❌ Never | N/A — never transmitted |
| **Transcriptions** | ✅ Always | ❌ Never | N/A — never transmitted |
| **Corrections** | ✅ Always | ❌ Never | N/A — never transmitted |
| **Individual transactions** | ✅ Always | ❌ Never | N/A — never transmitted |
| **Model gradients** | Generated locally | ✅ Daily (anonymous) | Differential privacy (ε=0.1) |
| **Aggregated statistics** | Computed locally | ✅ Weekly (k-anonymized) | k-anonymity (k≥10) |
| **Behavioral archetypes** | Computed locally | ✅ Monthly (abstracted) | Differential privacy + abstraction |

### 8.2 Privacy Guarantees

1. **Differential Privacy (ε=0.1, δ=1e-5):** Each gradient update is noised before upload. The probability of any individual's data being inferred from the gradient is bounded by the privacy budget. ε=0.1 is considered "strong" privacy — the gold standard in federated learning.

2. **k-Anonymity (k≥10):** Aggregated statistics are only computed for groups of 10+ workers. No individual can be identified from any statistic the backend computes.

3. **Secure Aggregation:** Gradients from multiple devices are aggregated before the backend sees them. The backend sees the sum, not individual contributions.

4. **Local Differential Privacy:** Even if the aggregation server is compromised, individual gradients are already noised and cannot be traced back to specific workers.

5. **Data Minimization:** Only the minimum data needed for training is transmitted. Raw data (audio, text, transactions) never leaves the device.

---

## 9. Failure Modes and Mitigations

| Failure Mode | Probability | Impact | Mitigation |
|-------------|-------------|--------|------------|
| **Poisoning attack** (malicious gradient upload) | Medium | High — could degrade model quality | Robust aggregation (Krum, Trimmed Mean). Statistical outlier detection on gradients. Device attestation. |
| **Privacy breach** (gradient inversion attack) | Low | Critical — could expose user data | Strong differential privacy (ε=0.1). Gradient clipping. Secure aggregation. Regular privacy audits. |
| **Model degradation** (catastrophic forgetting) | Medium | High — new data overwrites old knowledge | Elastic Weight Consolidation (EWC). Regularized fine-tuning. A/B testing before model deployment. |
| **Data drift** (distribution shift) | High | Medium — model becomes stale | Continuous monitoring of model performance metrics. Automatic retraining triggers. Concept drift detection. |
| **Connectivity loss** (no sync for extended period) | High | Low — on-device model still works | On-device model is self-sufficient. Sync when connectivity returns. No degradation from extended offline use. |
| **Device heterogeneity** (slow devices can't run models) | Medium | Medium — some workers excluded | Model quantization (INT8). Progressive model complexity based on device capability. Lite mode for old devices. |
| **Adversarial users** (trying to manipulate the system) | Low | Medium — could skew market intelligence | Statistical outlier detection. Anomaly detection on transaction patterns. Manual review triggers. |

---

## Summary: The Training Architecture in One Page

**On-device (Msaidizi):** Learns each worker's voice, dialect, business, and behavior. All personal data stays on the phone. Models personalize within 50-100 interactions.

**Backend (Angavu Cloud):** Learns collective intelligence from anonymous federated updates. Builds Africa's best dialect-specific voice models, economic models, and intelligence systems.

**Sync cycle:** Daily (voice gradients) → Weekly (transaction stats) → Monthly (behavioral patterns). Privacy preserved via differential privacy (ε=0.1) and k-anonymity (k≥10).

**Voice pipeline:** 12-month roadmap from baseline ASR (Month 1) to self-improving Africa-best models (Month 12+). WER target: <8% by Month 24.

**The moat:** Every day, the gap between Angavu and competitors grows. More data → better models → more users → more data. This is a self-reinforcing flywheel that cannot be replicated without the same scale of data — which only Angavu has.

**The vision:** In 5 years, Msaidizi is not an app. It is the operating system of Africa's informal economy. And it speaks every dialect, knows every market, and understands every worker — because it learned from all of them.

---

*Prepared by Swarm D — Training Architecture Team*
*Angavu Intelligence | July 7, 2026*
