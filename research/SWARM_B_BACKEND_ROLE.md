# Swarm B: Angavu Intelligence Backend — Role Definition

**Classification:** Internal — Architecture Definition
**Date:** July 7, 2026
**Prepared by:** Swarm B — Backend Role Definition Team
**Status:** Definitive

---

## Executive Summary

The Angavu Intelligence Backend is not a server. It is an **economic intelligence factory** — a cloud-based system that transforms raw transactional data collected by the Msaidizi App into four distinct intelligence products that serve Africa's 600M+ informal workers and 12 buyer segments.

The Backend's role is defined by three principles:

1. **Data → Intelligence.** Every transaction, voice interaction, and behavioral pattern collected by Msaidizi is an input. Every market insight, credit score, business recommendation, and community statistic is an output. The Backend is the transformation engine.

2. **Privacy-Preserving by Architecture.** The Backend never sees raw user data. Through federated learning, differential privacy (ε=0.1, δ=1e-5), and k-anonymity (k≥10), it learns from patterns without exposing individuals.

3. **Degree-Driven Intelligence.** Every analytical function maps to concepts from Valentine Owuor's BSc Economics & Statistics (42 units, Masinde Muliro University). The Backend doesn't just process data — it applies economic theory to transform invisible economic activity into visible, actionable intelligence.

**What the Backend IS:** The economic brain that turns Msaidizi's raw data into the intelligence products that formalize Africa's informal economy.

**What the Backend is NOT:** The Backend cannot function without Msaidizi. It has no sensors, no ears, no eyes. It cannot collect data, interact with workers, or operate offline. The App is the body; the Backend is the mind.

---

## 1. The Economic Intelligence Role

### 1.1 The Core Transformation

The Backend performs a four-stage transformation on every data point:

```
Stage 1: INGEST    → Raw data from Msaidizi (transactions, voice, location, behavior)
Stage 2: PROCESS   → Clean, validate, enrich, anonymize
Stage 3: ANALYZE   → Apply economic theory + statistical models
Stage 4: DELIVER   → Produce intelligence products for workers and buyers
```

Each stage is governed by specific degree units. The Backend is not running generic ML pipelines — it is implementing **applied economics**.

### 1.2 Soko Pulse — Market Intelligence

**What the Backend does:** Transforms individual transaction prices into real-time market intelligence across all markets where Msaidizi operates.

| Backend Function | Economic Mechanism | Degree Unit | Specific Application |
|---|---|---|---|
| **Real-time price discovery** | Walrasian equilibrium, search-and-matching theory | ECO 101 | Aggregate transaction prices across vendors to compute market-clearing prices for every tracked commodity |
| **Demand estimation** | Consumer theory, revealed preference (Samuelson) | ECO 201 | Infer demand curves from transaction volume and price data; identify when informal workers face subsistence constraints |
| **Price elasticity calculation** | Point elasticity, arc elasticity | MAT 121, ECO 201 | Compute real-time price elasticity dashboards — "tomato demand drops 12% for every 10% price increase in Gikomba" |
| **Market structure analysis** | Monopolistic competition, monopsony power, two-sided markets (Rochet & Tirole) | ECO 101, ECO 422 | Identify middlemen with monopsony power over farmers; map market structure (how many buyers, how many sellers, who has power) |
| **Price forecasting** | ARIMA, VAR, cointegration, seasonal decomposition | STA 244 | Predict commodity prices 1-4 weeks ahead using time series models trained on historical transaction data |
| **Cross-border intelligence** | Comparative advantage, H-O trade theory, exchange rate impact | ECO 305/313 | Track informal cross-border trade (ICBT) prices between Kenya, Uganda, Tanzania, Rwanda |
| **Informal CPI construction** | Laspeyres, Paasche, Fisher price indices | ECO 202, ECO 203 | Build the real cost-of-living index for informal workers — Kenya's official CPI uses weights that don't reflect actual spending (30% food weighting vs. 60% actual) |
| **Search cost reduction** | Diamond-Mortensen-Pissarides search theory (2010 Nobel) | ECO 101 | Reduce information asymmetry that causes price dispersion across markets — "tomatoes are KSh 20/kg cheaper in Gikomba than in your local market" |

**Data transformation pipeline:**
```
Raw: "Vendor A sold 5kg tomatoes at KSh 150/kg in Gikomba on 2026-07-07"
  ↓ Data Processing Swarm (7 agents)
Processed: Validated, geotagged, quality-checked price observation
  ↓ Intelligence Swarm
Analyzed: Compared to 847 other tomato transactions today across 23 markets
  ↓ Intelligence Swarm
Output: "Gikomba tomato price: KSh 150/kg (↓8% from yesterday, ↓15% from last week).
         Forecast: KSh 140-155/kg for next 7 days. Cheapest alternative: Muthurwa at KSh 140/kg."
```

### 1.3 Biashara Pulse — Business Intelligence (AI CFO)

**What the Backend does:** Transforms individual transaction patterns into personalized business intelligence — the equivalent of having a Chief Financial Officer for every mama mboga.

| Backend Function | Economic Mechanism | Degree Unit | Specific Application |
|---|---|---|---|
| **Cash flow tracking** | Present value, annuities, compound interest | ECO 103 | Track daily inflows/outflows, identify cash crunch patterns ("You're always short on Wednesdays because your supplier delivers Tuesdays") |
| **Profit maximization** | MR = MC optimization, first/second order conditions | MAT 121, ECO 101 | Recommend optimal pricing: "Your tomatoes are 15% below market average. Raise to KSh X without losing customers" |
| **Production efficiency** | Stochastic Frontier Analysis, Data Envelopment Analysis | ECO 101 | Measure vendor efficiency against the production frontier — which mama mboga operates closest to optimal? |
| **Business growth trajectory** | Geometric series, compound effects, dynamic optimization (Bellman equations) | ECO 103, ECO 104 | Model growth path: "At your current savings rate, you can hire an assistant in 4 months" |
| **Cost optimization** | Constrained optimization, Lagrange multipliers, duality | ECO 103, ECO 104 | Identify cost reduction opportunities: "Switching suppliers saves KSh 2,000/week with no quality loss" |
| **Demand forecasting (business-level)** | Conditional probability, Markov chains | STA 142 | Predict tomorrow's sales: "Based on your patterns, expect 15% more customers on Friday. Stock accordingly" |
| **Behavioral nudges** | Prospect theory, loss aversion, bounded rationality (Kahneman-Tversky) | ECO 101 | Time-sensitive alerts: "You usually restock on Monday. Today's tomato price is 15% cheaper than yesterday" |
| **Business health scoring** | Multiple indicators, composite indices | ECO 202, STA 245 | Compute a 0-10 health score from revenue consistency, margin trends, customer retention, supplier diversification |

**Daily briefing delivery (via Msaidizi voice):**
```
"Good morning, Mama Njeri! Yesterday you sold goods worth KSh 3,200.
 Your profit was KSh 780 — that's 12% better than your weekly average.
 Today's tip: Your supplier has sukuma wiki at KSh 15/bunch, which is 20% cheaper
 than last week. Consider buying extra — demand typically rises on Fridays.
 Your weekly goal is 68% complete. Keep going!"
```

### 1.4 Alama Score — Credit/Reputation Scoring

**What the Backend does:** Transforms transaction history, behavioral patterns, and social network signals into a credit score (300-850) that enables informal workers to access formal financial services — without requiring formal credit history.

| Backend Function | Economic Mechanism | Degree Unit | Specific Application |
|---|---|---|---|
| **Adverse selection solution** | Akerlof's lemons, Spence's signaling, Stiglitz's screening (2001 Nobel) | ECO 321 | Alama Score IS the solution to adverse selection in informal credit markets — alternative data screens reliable borrowers from unreliable ones |
| **Bayesian credit updating** | Bayes' theorem, posterior updating | STA 142 | P(default \| transaction history, demographics, social network) — every transaction updates the probability |
| **MLE parameter estimation** | Maximum Likelihood Estimation, Bayesian estimation | STA 341 | Estimate credit model parameters from incomplete data — informal workers have sparse, irregular records |
| **Credit model dimension reduction** | PCA, factor analysis, LDA | STA 442 | Reduce hundreds of behavioral signals into the key factors that predict repayment |
| **Non-parametric credit scoring** | Kernel density estimation, bootstrap, LOESS | STA 444 | Handle non-normal distributions — informal income is highly skewed, not Gaussian |
| **Mechanism design** | Revelation principle (Myerson, 1981) | ECO 321, BCB 108 | Design scoring that incentivizes honest reporting — workers who accurately log transactions get better scores |
| **Financial mathematics** | True cost of borrowing, present value | ECO 103 | Expose shylocking rates (120-360% annualized) and show workers the real cost of informal lending |
| **Credit model validation** | Hypothesis testing, A/B testing, ROC/AUC analysis | STA 342, MAT 124 | Validate that the score actually predicts repayment — area under the ROC curve must exceed 0.75 |

**Credit scoring pipeline:**
```
Raw signals from Msaidizi:
  - Transaction frequency: 8/10 weeks (consistent) ✓
  - Transaction amounts: Increasing trend ✓
  - Payment regularity: 100% on-time for 3 months ✓
  - Supplier diversification: 3 suppliers (good) ✓
  - Social network: Transacts with 12 other Alama-scored workers ✓
  - Location stability: Same market for 6+ months ✓
  ↓ Data Processing Swarm
Cleaned signals: Anonymized, k-anonymity verified (k≥10)
  ↓ Intelligence Swarm (Alama Agent)
  ↓ Bayesian model: Prior (population average) → Evidence (signals) → Posterior (score)
Output: Alama Score 720/850 — "Strong borrower. Recommend micro-loan up to KSh 50,000 at 12% APR.
        Key factors: Consistent transactions (8/10 weeks), growing revenue (+15% MoM),
        diversified suppliers (3). Risk factors: Single market dependency."
```

### 1.5 Jamii Insights — Community Intelligence

**What the Backend does:** Aggregates individual data into county-level, community-level, and demographic-level economic intelligence — making the invisible informal economy visible.

| Backend Function | Economic Mechanism | Degree Unit | Specific Application |
|---|---|---|---|
| **Informal GDP estimation** | GDP measurement, satellite accounts, SNA 2025 | ECO 102 | Estimate GDP contribution of informal economy by county — what KNBS cannot measure in real-time |
| **Real-time inflation tracking** | Demand-pull, cost-push, Phillips curve | ECO 102 | Compute informal market inflation indices more current than official CPI |
| **Employment monitoring** | Labor force participation, informal employment metrics | STA 245, ECO 102 | Track real-time employment indicators — how many informal workers are active, how many are idle |
| **Poverty measurement** | FGT indices, Lorenz curves, Theil index | ECO 204 | Track poverty dynamics at community level — are informal workers getting richer or poorer? |
| **Financial inclusion tracking** | Institutional economics (Acemoglu & Robinson) | ECO 100, ECO 204 | Measure what percentage of informal workers have access to savings, credit, insurance |
| **Fiscal impact analysis** | Laffer curve, Ramsey rule, fiscal multipliers | ECO 421 | How does government spending affect informal workers? What's the optimal tax policy for the informal sector? |
| **SDG progress measurement** | Capability approach (Sen, Nussbaum), development indicators | ECO 401, ECO 100 | Track SDG progress using real economic data from 600M+ informal workers |
| **Population projection** | Demographic methods, fertility/mortality rates, migration | STA 246 | Project market sizes, labor force growth, urbanization trends for planning |
| **Gender economic analysis** | Women's economic participation, gender gaps | ECO 204 | 60%+ of informal workers are women — track their economic participation, income gaps, barriers |
| **Collective bargaining data** | Game theory, Nash equilibrium, cooperative formation | ECO 103, ECO 101 | Provide community-level data that enables collective bargaining — "150 vendors in your market buy from the same supplier" |

**Community intelligence output:**
```
Nairobi County — Informal Economy Report (July 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Active informal workers (Msaidizi users): 12,450
Estimated total informal workers: ~2.1M
Informal GDP contribution: KSh 340B (37% of county GDP)
Average daily earnings: KSh 850 (↑3% from June)
Most traded commodities: Tomatoes, onions, sukuma wiki
Women participation rate: 64%
Financial inclusion: 23% have formal savings (↑5% from Jan)
Key insight: Tomato prices dropped 15% this week due to
             oversupply from Machakos. Expect recovery in 5-7 days.
```

---

## 2. Multi-Agent Architecture: 33 Agents, 6 Swarms

The Backend runs 33 specialized agents organized into 6 swarms. Each agent has a specific economic function. The swarms communicate via an event bus (pub/sub with dead letter queue).

### 2.1 Data Processing Swarm (7 Agents)

**Role:** Transform raw Msaidizi data into clean, validated, anonymized intelligence inputs.

| Agent | Function | Data Transformation |
|---|---|---|
| **Transaction Ingestion Agent** | Receives transaction batches from Msaidizi sync endpoint | Raw JSON → validated transaction records with timestamps, amounts, categories, locations |
| **Voice Processing Agent** | Processes voice inputs (14 dialects) into structured data | Audio → speech-to-text → entity extraction → structured transaction records |
| **Pattern Recognition Agent** | Identifies behavioral patterns in transaction sequences | Transaction stream → pattern library (seasonal, cyclical, trend, anomaly) |
| **Data Quality Agent** | Validates, deduplicates, and enriches data | Dirty data → clean data; flags anomalies, missing values, inconsistencies |
| **Geospatial Agent** | Maps transactions to markets, regions, and economic zones | Location data → market identification, cross-market linkage, spatial analysis |
| **Receipt Processing Agent** | Extracts data from photographed receipts | Image → OCR → structured line items → transaction records |
| **Data Processing Coordinator** | Orchestrates the swarm, manages load balancing and priority | Routes incoming data to appropriate agents; manages throughput and backpressure |

**Economic function:** The Data Processing Swarm is the **sensory cortex** of the Backend. It converts the raw signals Msaidizi collects into the structured data that the Intelligence Swarm can reason about. Without this swarm, transaction data is noise. With it, transaction data is economic evidence.

### 2.2 Intelligence Swarm (7 Agents)

**Role:** Apply economic theory and statistical models to produce the four intelligence products.

| Agent | Function | Economic Foundation |
|---|---|---|
| **Market Intelligence Agent (Soko Pulse)** | Real-time price discovery, demand estimation, market structure analysis | ECO 101 (supply/demand), ECO 201 (intermediate micro), STA 244 (time series) |
| **Credit Scoring Agent (Alama Score)** | Bayesian credit model, behavioral scoring, risk assessment | STA 341 (MLE/Bayesian estimation), STA 442 (PCA/factor analysis), ECO 321 (information economics) |
| **Business Intelligence Agent (Biashara Pulse)** | Cash flow analysis, profit optimization, growth forecasting | ECO 103/104 (mathematical economics), MAT 121 (optimization), ECO 101 (production theory) |
| **Community Intelligence Agent (Jamii Insights)** | County-level aggregation, GDP estimation, poverty tracking | ECO 102 (macroeconomics), ECO 204 (development), STA 245 (social statistics) |
| **Tax Intelligence Agent** | Tax compliance estimation, formalization readiness | ECO 421 (public finance), ECO 414 (econometrics) |
| **Distribution Gap Agent** | Market coverage analysis, supply chain mapping | ECO 422 (industry economics), STA 246 (demography) |
| **Intelligence Coordinator** | Orchestrates cross-agent analysis, manages intelligence fusion | Coordinates multi-product analysis; ensures consistency across products |

**Economic function:** The Intelligence Swarm is the **analytical core** — where Valentine's degree units come alive. Every agent implements specific economic models:

- The Market Intelligence Agent runs ARIMA models (STA 244) on transaction prices to forecast commodity prices
- The Credit Scoring Agent uses Bayesian updating (STA 142, STA 341) to compute posterior credit probabilities
- The Business Intelligence Agent solves constrained optimization problems (ECO 104) to recommend profit-maximizing actions
- The Community Intelligence Agent constructs price indices (ECO 203) and GDP estimates (ECO 102) from aggregated transaction data

### 2.3 Report Swarm (5 Agents)

**Role:** Transform intelligence outputs into deliverable products for workers, buyers, and institutions.

| Agent | Function | Output |
|---|---|---|
| **Worker Report Agent** | Generates personalized reports for individual informal workers | Daily briefings, weekly summaries, monthly reviews, credit reports |
| **Buyer Report Agent** | Generates market intelligence products for enterprise buyers | FMCG demand signals, market sizing, distribution gap analysis, brand tracking |
| **Formal Report Agent** | Generates institution-ready reports (banks, government, insurance) | Bank-presentable financial statements, government compliance reports, insurance risk profiles |
| **WhatsApp Delivery Agent** | Formats and delivers reports via WhatsApp | Voice messages, text summaries, interactive reports in 14 dialects |
| **Insight Narrator Agent** | Generates natural-language explanations of complex analyses | "Your tomatoes are 15% cheaper because Machakos had a bumper harvest this week" |

**Economic function:** The Report Swarm is the **communication layer** (BCB 108). It solves the information asymmetry problem at the delivery stage — no matter how good the intelligence, it's worthless if workers can't understand it. The Insight Narrator Agent applies the Shannon-Weaver communication model to ensure intelligence reaches workers at the right literacy level, in the right language, at the right time.

### 2.4 Self-Evolution Swarm (6 Agents)

**Role:** Continuously improve the Backend's models, features, and performance.

| Agent | Function | Improvement Mechanism |
|---|---|---|
| **Feedback Processing Agent** | Collects and analyzes user feedback, agent performance metrics | Identifies what's working and what's not; routes feedback to relevant swarms |
| **Feature Design Agent** | Proposes new features and intelligence products based on usage patterns | Detects unmet needs: "Workers in Nakuru frequently ask about cross-border prices — add Tanzania price feeds" |
| **Model Training Agent** | Retrains and fine-tunes models using federated learning updates | Incorporates new data without seeing raw user data; applies curriculum RL for on-device models |
| **Dialect Expansion Agent** | Extends language and dialect coverage based on usage data | Identifies new dialect patterns; trains speech models for underserved language communities |
| **Quality Assurance Agent** | Monitors output quality across all products | Statistical quality control (STA 346): control charts, CUSUM for detecting quality drift |
| **Experiment Agent** | Runs A/B tests and experiments to validate improvements | Experimental design (STA 343): RCTs for feature validation, Thompson sampling for optimization |

**Economic function:** The Self-Evolution Swarm implements the **endogenous growth model** (Romer, Lucas — ECO 100). Knowledge drives growth from within: every transaction creates data, data trains better models, better models create better intelligence, better intelligence attracts more users. The swarm ensures this flywheel accelerates rather than stalls.

### 2.5 Learning Swarm (4 Agents)

**Role:** Enable the Backend to learn continuously while preserving privacy.

| Agent | Function | Learning Mechanism |
|---|---|---|
| **Federated Learning Agent** | Coordinates model aggregation across thousands of Msaidizi devices | Receives encrypted model gradients, aggregates via secure aggregation, distributes improved global models |
| **Active Learning Agent** | Identifies the most valuable data points for model improvement | Selective sampling: "We need more transactions from Nakuru market to improve price forecasts there" |
| **Model Evaluator Agent** | Continuously evaluates model performance across all products | Tracks prediction accuracy, credit model AUC, forecast RMSE, recommendation effectiveness |
| **Knowledge Distillation Agent** | Compresses cloud models into on-device models | Takes large cloud model knowledge and distills into Qwen 0.5B-compatible format for Msaidizi |

**Economic function:** The Learning Swarm implements the **federated learning architecture** that is Angavu's privacy moat. It enables the Backend to learn from 600M+ workers without ever seeing their data. This is the technical implementation of the data moat strategy: more workers → better models → better products → more workers.

### 2.6 Governance Swarm (4 Agents)

**Role:** Enforce security, privacy, compliance, and ethical rules across all operations.

| Agent | Function | Governance Mechanism |
|---|---|---|
| **Security Agent** | Enforces authentication, authorization, encryption, rate limiting | JWT + API key auth, AES-256-GCM encryption, HMAC-SHA256 anonymization |
| **Privacy Agent** | Enforces differential privacy (ε=0.1), k-anonymity (k≥10), data minimization | Rejects any data output that fails privacy guarantees; monitors for re-identification risk |
| **Compliance Agent** | Ensures compliance with Kenya DPA, Nigeria NDPR, South Africa POPIA | Tracks regulatory requirements across jurisdictions; flags compliance risks |
| **Audit Agent** | Maintains append-only audit trails for all agent decisions | Every credit score, every price forecast, every recommendation has a traceable decision chain |

**Economic function:** The Governance Swarm is the **institutional infrastructure** (Acemoglu & Robinson — ECO 100). Inclusive institutions require rules that protect participants. The Governance Swarm ensures that the platform serving 600M+ informal workers operates with the rigor expected of financial infrastructure — because that's what it is.

---

## 3. Intelligence Products: How Each Serves Informal Workers

### 3.1 Soko Pulse — Market Intelligence

**For the worker:** "I know what my goods are worth, where to buy cheapest, and what prices will be next week."

**What the Backend delivers:**

| Product Feature | Backend Process | Worker Benefit |
|---|---|---|
| **Real-time prices** | Aggregate transactions across all vendors in a market; compute median, range, trend | Vendor knows if they're overpaying or underpricing |
| **Price forecasts** | ARIMA/VAR models on historical transaction data (STA 244) | "Tomato prices will rise 20% next week due to supply shortage — stock up now" |
| **Cross-market comparison** | Geospatial analysis across all tracked markets | "Tomatoes are KSh 20/kg cheaper in Muthurwa than Gikomba — worth the trip?" |
| **Demand signals** | Transaction volume analysis, seasonal decomposition | "Demand for sukuma wiki peaks on Fridays and Saturdays — increase stock" |
| **Market structure maps** | Network analysis of buyer-seller relationships | "3 middlemen control 60% of onion supply in your area — here are alternative suppliers" |
| **Informal CPI** | Laspeyres/Paasche/Fisher indices on actual spending patterns (ECO 203) | "Your cost of living rose 4.2% this month, driven by tomato and cooking oil prices" |

**For the buyer (FMCG, traders, logistics):**

| Product Feature | Backend Process | Buyer Benefit |
|---|---|---|
| **Demand forecasting** | Aggregate transaction patterns across regions | "Demand for cooking oil will increase 25% in Western Kenya next month" |
| **Distribution gap analysis** | Map product availability across markets | "Your product is available in 23% of informal outlets in Nairobi — here are the 77% you're missing" |
| **Brand tracking** | Transaction pattern analysis for specific products | "Your brand's market share in informal retail dropped from 34% to 28% in Q2" |
| **Competitor intelligence** | Cross-product transaction analysis | "Competitor X gained 6% share by offering 100ml sachets — consider matching" |

### 3.2 Biashara Pulse — Business Intelligence (AI CFO)

**For the worker:** "I have a financial advisor who understands my business, speaks my language, and works for free."

**What the Backend delivers:**

| Product Feature | Backend Process | Worker Benefit |
|---|---|---|
| **Daily briefings** | Transaction analysis + weather/calendar data + market trends | "Good morning! Yesterday's revenue: KSh 3,200. Today's tip: stock extra tomatoes — Friday demand is high" |
| **Cash flow tracking** | Inflow/outflow pattern recognition, seasonal adjustment | "Your cash reserves are below 2-week safety buffer. Reduce non-essential purchases this week" |
| **Pricing optimization** | Constrained optimization (MR = MC, MAT 121) | "Your tomatoes are 15% below market average. Raise to KSh 160/kg — you'll gain KSh 200/day with minimal customer loss" |
| **Cost reduction** | Supplier comparison, logistics optimization | "Supplier B offers onions at KSh 10/kg less than Supplier A with same quality. Switch to save KSh 1,500/week" |
| **Growth planning** | Dynamic optimization (Bellman equations, ECO 104) | "At your current savings rate of 8%, you can open a second stall in 7 months" |
| **Financial health score** | Composite index from multiple indicators | "Your business health: 7.2/10. Strengths: consistent revenue. Weaknesses: single supplier dependency" |

**Delivery schedule:**
| Report | Frequency | Channel | Content |
|---|---|---|---|
| Daily briefing | 7 PM daily | Voice via Msaidizi | P&L, restock alerts, tomorrow forecast |
| Weekly summary | Monday 8 AM | WhatsApp + voice | Trends, customer insights, business health |
| Monthly review | 1st of month, 9 AM | WhatsApp + voice | Revenue growth, supplier comparison, credit readiness |
| 6-month review | Jun 30 & Dec 31 | Detailed report | Business review, seasonal patterns, formalization readiness |
| Annual review | Dec 31 | Comprehensive report | Annual P&L, tax summary, next year goals |

### 3.3 Alama Score — Credit/Reputation Scoring

**For the worker:** "I can prove I'm creditworthy — not with documents, but with my track record."

**What the Backend delivers:**

| Product Feature | Backend Process | Worker Benefit |
|---|---|---|
| **Credit score (300-850)** | Bayesian model with behavioral inputs (STA 142, STA 341) | Workers with Alama Score >650 can access micro-loans from partner banks |
| **Credit readiness assessment** | Trend analysis of score trajectory | "Your score improved from 580 to 650 over 6 months. You're now eligible for KSh 30,000 micro-loan" |
| **Repayment probability** | Logistic regression with behavioral features (STA 442) | "Based on your patterns, there's an 87% probability you'll repay a KSh 20,000 loan in 3 months" |
| **Behavioral consistency score** | Variance analysis of transaction patterns | "Your business is highly consistent (CV=0.12) — this signals reliability to lenders" |
| **Social network credit signals** | Graph analysis of transaction network | "You transact regularly with 12 other scored workers — this strengthens your score" |
| **Shylocking exposure** | True cost of borrowing calculation (ECO 103) | "Your current informal loan has an effective APR of 240%. A formal micro-loan would cost 18% APR" |

**How lenders use Alama Score:**

| Score Range | Risk Category | Loan Eligibility | Typical Terms |
|---|---|---|---|
| 750-850 | Excellent | Up to KSh 100,000 | 12-15% APR, 6-12 months |
| 650-749 | Good | Up to KSh 50,000 | 15-20% APR, 3-6 months |
| 550-649 | Fair | Up to KSh 20,000 | 20-25% APR, 1-3 months |
| 300-549 | Building | Micro-loans only | Group lending mechanisms (ECO 206) |

### 3.4 Jamii Insights — Community Intelligence

**For the community:** "We can see our own economy — and use that visibility to bargain, plan, and advocate."

**What the Backend delivers:**

| Product Feature | Backend Process | Community Benefit |
|---|---|---|
| **County economic dashboards** | Aggregation of anonymized transaction data by county | Counties can see their informal economy's contribution to GDP — previously invisible |
| **Collective bargaining data** | Market-level aggregation of buyer-seller relationships | "150 vendors in Gikomba buy tomatoes from the same 3 suppliers — collective negotiation is possible" |
| **Policy impact measurement** | Difference-in-differences, regression discontinuity (ECO 424) | "The county's market fee reduction increased vendor profits by 8% — here's the evidence" |
| **Development indicators** | Financial inclusion rates, poverty dynamics, gender gaps | "Women's average daily earnings in your county are 67% of men's — the gap is closing (was 58% last year)" |
| **Employment monitoring** | Worker activity tracking, seasonal employment patterns | "Informal employment in your area dropped 12% during the rainy season — expected seasonal pattern" |
| **SDG tracking** | Maps informal economy data to SDG indicators | "Your county is 45% toward SDG 1 (No Poverty) based on real transaction data" |

**Buyer segments for Jamii Insights:**

| Buyer | What They Need | Pricing Model |
|---|---|---|
| **County governments** | Real-time economic dashboards for policy decisions | Subscription: $5K-50K/year per county |
| **National government (KNBS, CBK)** | Informal GDP estimates, inflation data, employment statistics | Data licensing: $100K-500K/year |
| **World Bank, IMF** | Development indicators, poverty tracking, financial inclusion | Research partnerships + data licensing |
| **NGOs (UNDP, UN Women)** | Program impact measurement, gender economic data | Outcome-based: $10-50 per verified impact metric |
| **Academic researchers** | Anonymized datasets for research | Data access fees: $5K-25K per dataset |

---

## 4. Federated Learning Role

### 4.1 Why Federated Learning is Non-Negotiable

The Backend cannot function without data. But taking raw data from 600M+ informal workers would be:
- **Illegal** under Kenya DPA, Nigeria NDPR, South Africa POPIA
- **Unethical** — informal workers are a vulnerable population
- **Strategic suicide** — raw data in a central server is a single point of failure and a target

Federated learning solves this: the Backend improves its models without ever seeing individual data.

### 4.2 The Federated Learning Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    Msaidizi Device (Worker's Phone)              │
│                                                                  │
│  1. Local model trains on worker's transaction data             │
│  2. Model computes gradient updates (not raw data)              │
│  3. Gradients encrypted with worker's key                       │
│  4. Encrypted update sent to Backend                            │
│                                                                  │
│  DATA NEVER LEAVES THE DEVICE IN RAW FORM                       │
└────────────────────────────┬────────────────────────────────────┘
                             │ Encrypted gradient updates
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Angavu Intelligence Backend (Cloud)                 │
│                                                                  │
│  5. Secure aggregation: combine gradients from 1000s of workers │
│  6. Differential privacy: add calibrated noise (ε=0.1)          │
│  7. K-anonymity check: only use patterns from groups of ≥10     │
│  8. Update global model with aggregated learning                │
│  9. Distribute improved model back to devices                   │
│                                                                  │
│  INDIVIDUAL DATA IS MATHEMETICALLY IRRECOVERABLE                │
└────────────────────────────┬────────────────────────────────────┘
                             │ Improved global model
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Msaidizi Device (Worker's Phone)              │
│                                                                  │
│  10. Receive improved model                                     │
│  11. Worker gets better AI — better forecasts, better scores    │
│                                                                  │
│  PRIVACY PRESERVED, INTELLIGENCE IMPROVED                       │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Privacy Guarantees

| Mechanism | Specification | What It Means |
|---|---|---|
| **Differential Privacy** | ε=0.1, δ=1e-5 | Mathematically guarantee that no one can determine if any individual worker's data was used in training. ε=0.1 is extremely strong — most systems use ε=1.0 or higher |
| **K-Anonymity** | k≥10 | Any data pattern used by the Backend must be shared by at least 10 workers. No individual can be singled out |
| **Secure Aggregation** | Encrypted model updates | The Backend receives encrypted gradients. It can aggregate them but cannot decrypt individual contributions |
| **On-Device Training** | Local model updates | All model training happens on the worker's phone. Only encrypted gradients are transmitted |
| **Data Sovereignty** | African data in Africa | All data processed on African infrastructure (Kenya DPA, Nigeria NDPR, South Africa POPIA compliant) |

### 4.4 What the Backend Learns (Without Seeing Individual Data)

| Learning | Federated Mechanism | Intelligence Product |
|---|---|---|
| Price patterns across markets | Aggregated price gradients from 1000s of vendors | Soko Pulse — better price forecasts |
| Credit repayment signals | Aggregated behavioral gradients from scored workers | Alama Score — more accurate credit models |
| Business growth patterns | Aggregated success/failure patterns | Biashara Pulse — better growth recommendations |
| Community economic dynamics | Aggregated county-level patterns | Jamii Insights — more accurate GDP estimates |
| Dialect and language patterns | Aggregated voice model gradients | Msaidizi — better speech recognition in 14 dialects |

### 4.5 The Model Improvement Cycle

```
Week 1:  Global model v1.0 deployed to 1,000 Msaidizi devices
         → Devices train locally on transaction data
         → 1,000 encrypted gradient updates received
         → Secure aggregation → Global model v1.1
         
Week 2:  Global model v1.1 deployed to 1,000 devices
         → Better predictions → more user engagement → more data
         → 1,200 encrypted gradient updates (20% more users)
         → Secure aggregation → Global model v1.2

Week N:  Global model v1.N deployed to 100,000 devices
         → 100,000 gradient updates
         → Models are now highly accurate for specific markets
         → Soko Pulse forecasts within 5% of actual prices
         → Alama Score AUC > 0.80
```

This is the **flywheel** (STRATEGY.md): more workers → more data → better models → better products → more workers.

---

## 5. Data Buyer Ecosystem

### 5.1 The 12 Buyer Segments

The Backend's intelligence products serve two markets: **workers** (who get free AI CFO services) and **buyers** (who pay for intelligence products that fund the platform).

| # | Segment | What They Buy | Why They Pay |
|---|---|---|---|
| 1 | **FMCG Companies** (Pwani Oil, Unilever, Bidco) | Demand signals, distribution gap analysis, brand tracking | Reach 600M+ consumers in informal retail — a market they can't measure today |
| 2 | **Banks** (KCB, Equity, Co-op) | Alama Score, credit risk profiles, market sizing | Access 600M+ creditworthy-but-unscored potential customers |
| 3 | **Insurance Companies** (Jubilee, Britam, APA) | Risk profiles, micro-insurance demand data | Price micro-insurance products for informal workers profitably |
| 4 | **County Governments** (47 counties) | County economic dashboards, employment data, tax base estimation | Make evidence-based policy decisions for their informal economies |
| 5 | **National Government** (KNBS, CBK, KRA) | Informal GDP estimates, inflation data, employment statistics, tax base | Measure what they cannot currently measure — the informal economy |
| 6 | **International Organizations** (World Bank, IMF, ILO) | Development indicators, poverty tracking, financial inclusion data | Access real-time development data for Africa's informal economy |
| 7 | **NGOs** (UNDP, UN Women, USAID) | Program impact measurement, gender economic data, SDG tracking | Prove their programs work with real economic data |
| 8 | **Commodity Traders** (Twiga, Export Trading Group) | Supply chain intelligence, price forecasting, market entry data | Optimize procurement from informal markets |
| 9 | **Private Equity / Venture Capital** | Market sizing, growth metrics, investment due diligence | Evaluate investment opportunities in informal economy sectors |
| 10 | **Consultancies** (McKinsey, BCG, Dalberg) | Market research data, industry reports, economic analysis | Serve clients who need informal economy data |
| 11 | **Academic Researchers** (MIT, Oxford, J-PAL) | Anonymized datasets, research partnerships | Publish research using the world's largest informal economy dataset |
| 12 | **Mobile Network Operators** (Safaricom, Airtel) | Consumer behavior insights, mobile money usage patterns | Understand their informal economy user base better |

### 5.2 Pricing Model

The Backend uses **outcome-based pricing** — buyers pay for the value they receive, not for data volume.

| Product | Pricing Model | Price Range |
|---|---|---|
| **Soko Pulse (Market Intelligence)** | Subscription per market/commodity | $500-5,000/month per market |
| **Alama Score (Credit Scoring)** | Per-score fee (pay-per-query) | KSh 50-200 per score ($0.40-1.50) |
| **Jamii Insights (Community)** | Subscription per county/dataset | $5,000-50,000/year per county |
| **FMCG Intelligence** | Subscription + outcome bonus | $10,000-100,000/year |
| **Research Data** | Per-dataset licensing | $5,000-25,000 per dataset |
| **Tax Intelligence** | Per-report fee | KSh 100-500 per report ($0.80-4.00) |

### 5.3 Revenue Model

| Revenue Stream | Year 1 Target | Year 2 Target | Year 3 Target |
|---|---|---|---|
| Worker subscriptions | Free (subsidized) | Free (subsidized) | Free (subsidized) |
| FMCG intelligence | $20K/month | $100K/month | $500K/month |
| Alama Score (per-query) | $5K/month | $50K/month | $200K/month |
| Government data | $10K/month | $50K/month | $200K/month |
| NGO/development data | $5K/month | $25K/month | $100K/month |
| Research data | $2K/month | $10K/month | $50K/month |
| Other buyers | $8K/month | $15K/month | $150K/month |
| **Total** | **$50K/month** | **$250K/month** | **$1.2M/month** |

Workers get free intelligence. Buyers fund the platform. This is the **two-sided market** (Rochet & Tirole, ECO 101) that makes Angavu's monopoly sustainable.

---

## 6. How Backend Connects to Msaidizi App

### 6.1 The Data Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    MS AIDIZI APP (Android)                        │
│                                                                   │
│  Voice Input ──→ On-device Qwen 0.5B ──→ Transaction Record     │
│  Receipt Photo ──→ On-device OCR ──→ Transaction Record          │
│  Manual Entry ──→ Form Validation ──→ Transaction Record         │
│  Market Observation ──→ Voice/Text ──→ Market Data               │
│                                                                   │
│  All data stored locally (SQLite)                                │
│  Sync when connected (encrypted batch upload)                    │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                    POST /api/v1/sync/upload
                    (encrypted transaction batches)
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│              ANGAVU INTELLIGENCE BACKEND (Cloud)                  │
│                                                                   │
│  Data Processing Swarm → Intelligence Swarm → Report Swarm      │
│  Learning Swarm (federated updates) → Governance Swarm (privacy) │
│                                                                   │
│  Intelligence Products:                                          │
│  - Soko Pulse (market prices, forecasts)                         │
│  - Biashara Pulse (business recommendations)                     │
│  - Alama Score (credit score)                                    │
│  - Jamii Insights (community statistics)                         │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                    GET /api/v1/sync/intelligence/{worker_id}
                    (personalized intelligence + global models)
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                    MS AIDIZI APP (Android)                        │
│                                                                   │
│  Receives: Personalized intelligence + updated models            │
│  Delivers: Voice briefings, alerts, credit reports               │
│  Displays: Market prices, business health, Alama Score           │
│                                                                   │
│  On-device model updated via federated learning                  │
└──────────────────────────────────────────────────────────────────┘
```

### 6.2 API Contract Summary

| Endpoint | Direction | Purpose |
|---|---|---|
| `POST /api/v1/sync/upload` | App → Backend | Upload transaction batches |
| `GET /api/v1/sync/intelligence/{worker_id}` | Backend → App | Pull personalized intelligence |
| `POST /api/v1/fl/upload-update` | App → Backend | Upload federated learning gradient |
| `GET /api/v1/fl/global-model/{dialect}` | Backend → App | Download improved global model |
| `POST /api/v1/whatsapp/webhook` | WhatsApp → Backend | Receive WhatsApp messages from workers |
| `POST /api/v1/whatsapp/send-report` | Backend → WhatsApp | Deliver reports via WhatsApp |
| `POST /api/v1/analysis/deep` | App → Backend | Request deep cloud analysis |
| `GET /api/v1/intelligence/soko/pulse` | Backend → Buyer API | Market intelligence for buyers |
| `POST /api/v1/intelligence/alama/score` | Backend → Buyer API | Credit score for lenders |
| `GET /api/v1/intelligence/jamii/insights` | Backend → Buyer API | Community intelligence for institutions |

### 6.3 Sync Protocol

Msaidizi operates **offline-first**. The Backend syncs in three modes:

| Mode | Trigger | Data Flow | Latency Tolerance |
|---|---|---|---|
| **Real-time** | Worker opens app, has connectivity | Bidirectional: upload transactions, receive intelligence | <5 seconds |
| **Background sync** | Periodic (every 15 minutes when connected) | Batch upload of accumulated transactions | Minutes |
| **Deep sync** | Overnight (WiFi + charging) | Full federated learning update, model download, historical data reconciliation | Hours |

---

## 7. What Backend CANNOT Do Alone

The Backend is powerful but fundamentally dependent on Msaidizi. It cannot:

| Capability | Why Backend Needs Msaidizi |
|---|---|
| **Collect transaction data** | The Backend has no sensors, no ears, no eyes. Only Msaidizi can capture what informal workers actually buy, sell, and earn. |
| **Interact with workers** | The Backend cannot speak, listen, or display. Only Msaidizi's voice interface in 14 dialects can reach workers who may be illiterate. |
| **Operate offline** | The Backend requires connectivity. Only Msaidizi can function in markets with no internet. |
| **Build trust** | The Backend is invisible infrastructure. Only Msaidizi's daily interactions earn the trust of informal workers. |
| **Capture context** | The Backend sees numbers. Only Msaidizi can capture the voice tone, market atmosphere, weather conditions, and social dynamics that give numbers meaning. |
| **Provide real-time alerts** | The Backend processes in batches. Only Msaidizi can alert a worker instantly: "Tomato prices just dropped 20% — adjust your pricing now." |
| **On-device inference** | The Backend cannot run on a $50 Android phone. Only Msaidizi's Qwen 0.5B via llama.cpp NDK can provide offline AI. |
| **Protect raw data** | The Backend must not see raw data. Only Msaidizi's on-device processing ensures privacy — the Backend only receives encrypted gradients and anonymized aggregates. |

**The fundamental truth:** The Backend transforms data into intelligence. But data only exists because Msaidizi collects it. Without the App, the Backend is an empty factory with no raw materials. Without the Backend, the App is a data collector with no intelligence. They are one system.

---

## 8. Summary: What the Backend IS

| Dimension | Definition |
|---|---|
| **Economic role** | Transforms invisible informal economic activity into visible, actionable intelligence products |
| **Technical role** | Multi-agent runtime (33 agents, 6 swarms) processing data via event bus architecture |
| **Privacy role** | Learns from 600M+ workers without seeing any individual's data (federated learning + differential privacy + k-anonymity) |
| **Business role** | Produces 15 intelligence products sold to 12 buyer segments, generating revenue that funds free services for workers |
| **Academic role** | Implements 42 degree units from BSc Economics & Statistics — every function maps to specific economic theory |
| **Strategic role** | The data moat that makes Angavu's monopoly defensible — more data → better models → more users → more data |

**The Backend is not software. It is applied economics — running at scale, on African infrastructure, powered by solar, serving the 600M+ workers the world forgot.**

---

*End of Document*

**Angavu Intelligence © 2026**
**"Not competing. Just operating."**
