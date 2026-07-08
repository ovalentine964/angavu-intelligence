# EU AI Act — Risk Classification Assessment for Angavu Intelligence

**Applicable Law:** Regulation (EU) 2024/1689 — Artificial Intelligence Act
**Compliance Deadline:** August 2, 2026 (high-risk systems)
**Date:** July 2026
**Classification:** Internal — Strategic Regulatory Document

---

## 1. EXECUTIVE SUMMARY

**Verdict: Angavu Intelligence's core products are LIMITED-RISK or MINIMAL-RISK under the EU AI Act.**

Alama Score, if positioned as credit scoring, would be HIGH-RISK. The "Financial Readiness Assessment" positioning avoids this classification.

| Product | EU AI Act Risk Tier | Reasoning |
|---------|-------------------|-----------|
| Msaidizi (Voice AI) | **Minimal** | General-purpose AI assistant; not in Annex III |
| Msaidizi (Bookkeeping) | **Minimal** | Record-keeping tool; no decision-making |
| Msaidizi (Business Intelligence) | **Limited** | Provides information; transparency obligations apply |
| Alama Score (as "Financial Readiness Assessment") | **Limited** | Advisory self-assessment tool; does not make credit decisions |
| Alama Score (if classified as credit scoring) | **HIGH** | Annex III Category 5(b) explicitly covers credit scoring |
| Soko Pulse | **Limited** | Market information; transparency obligations |
| Angavu Pulse | **Minimal** | Aggregated anonymized data; no individual profiling |
| Agricultural Domain Agents | **Limited/High** | Depends on whether classified as agricultural decision system |

---

## 2. EU AI ACT RISK FRAMEWORK

### 2.1 Four-Tier Classification

```
┌─────────────────────────────────────────────────────────┐
│                    EU AI ACT RISK TIERS                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  UNACCEPTABLE RISK (Prohibited)                           │
│  • Social scoring                                        │
│  • Subliminal manipulation                               │
│  • Real-time biometric surveillance (exceptions apply)   │
│  → ANGAVU: ❌ None of our products fall here              │
│                                                           │
│  HIGH RISK (Annex III — Heavy Regulation)                 │
│  • Biometric identification                               │
│  • Critical infrastructure                                │
│  • Education & training                                   │
│  • Employment & workers management                        │
│  • Access to essential services (credit, insurance)       │
│  • Law enforcement                                        │
│  • Migration & border control                             │
│  • Administration of justice                              │
│  → ANGAVU: ⚠️ Only if Alama Score = credit scoring       │
│                                                           │
│  LIMITED RISK (Transparency Obligations)                   │
│  • Chatbots                                              │
│  • Emotion recognition systems                            │
│  • Deep fake generators                                   │
│  • AI-generated content                                   │
│  → ANGAVU: ✅ Msaidizi voice AI, business intelligence   │
│                                                           │
│  MINIMAL RISK (No Specific Obligations)                    │
│  • Most AI systems                                       │
│  • Spam filters, inventory management, etc.               │
│  → ANGAVU: ✅ Bookkeeping, Angavu Pulse, basic analytics │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 3. ANNEX III ANALYSIS — HIGH-RISK CATEGORIES

### 3.1 Category-by-Category Assessment

| Annex III Category | Description | Angavu Product | Risk? | Reasoning |
|-------------------|-------------|---------------|-------|-----------|
| **1. Biometric identification** | Remote biometric ID, categorization | Voice dialect training | **No** | Voice data used for dialect improvement, not identification |
| **2. Critical infrastructure** | Management of gas, water, electricity | None | **No** | Not applicable |
| **3. Education** | Student assessment, admission | None | **No** | Not applicable |
| **4. Employment** | Recruitment, task allocation, performance | Msaidizi (worker productivity) | **Gray area** | Msaidizi helps workers optimize their OWN work; doesn't manage employees |
| **5a. Access to public services** | Eligibility for benefits | None | **No** | Not applicable |
| **5b. Credit scoring** | Creditworthiness, credit score | **Alama Score** | **⚠️ CONDITIONAL** | See detailed analysis below |
| **5c. Insurance** | Risk assessment for insurance | None | **No** | Not applicable |
| **6. Law enforcement** | Evidence evaluation, profiling | None | **No** | Not applicable |
| **7. Migration** | Border control, asylum | None | **No** | Not applicable |
| **8. Justice** | Legal interpretation, sentencing | None | **No** | Not applicable |

### 3.2 Category 5(b) — Credit Scoring Deep Dive

**EU AI Act Annex III, Category 5(b):**
> "AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, save for AI systems used for the purpose of detecting financial fraud."

**Key question: Does Alama Score "evaluate creditworthiness" or "establish a credit score"?**

| Test | Alama Score as "Financial Readiness Assessment" | Alama Score as "Credit Scoring" |
|------|-----------------------------------------------|--------------------------------|
| Evaluates creditworthiness? | **No** — evaluates business health | **Yes** — evaluates ability to repay |
| Establishes credit score? | **No** — establishes financial readiness score | **Yes** — establishes credit score |
| Used for lending decisions? | **No** — advisory to the worker only | **Yes** — shared with lenders |
| Makes decisions about credit access? | **No** — worker decides | **Potentially** — informs lender decisions |
| Profile of natural person? | **Yes** — but for self-assessment | **Yes** — for external evaluation |

**Verdict:** If Alama Score is positioned as a self-assessment tool that the worker uses to understand their own financial health, it does NOT meet the criteria for Category 5(b). The key differentiator is that the score is used BY the data subject FOR their own benefit, not BY a lender TO make credit decisions.

---

## 4. LIMITED-RISK OBLIGATIONS

### 4.1 Transparency Requirements (Article 50)

For Angavu products classified as limited-risk:

| Obligation | Article | Angavu Implementation | Status |
|-----------|---------|----------------------|--------|
| Disclose AI interaction | 50(1)(a) | "You are speaking with an AI assistant" at conversation start | ⬜ TODO |
| Mark AI-generated content | 50(1)(b) | Label all AI-generated insights in-app | ⬜ TODO |
| Disclose deepfake/content manipulation | 50(1)(c)-(d) | Not applicable (no synthetic media) | N/A |
| Ensure AI literacy | Article 4 | Staff training on AI capabilities and limitations | ⬜ TODO |

### 4.2 AI Literacy (Article 4)

| Requirement | Implementation | Status |
|------------|---------------|--------|
| Staff AI literacy training | Internal training program | ⬜ TODO |
| Document AI capabilities and limitations | Technical documentation | ⬜ TODO |
| Ensure users understand AI interactions | In-app explanations | ⬜ TODO |

---

## 5. HIGH-RISK COMPLIANCE PACKAGE (IF TRIGGERED)

### 5.1 High-Risk System Requirements (Articles 8-15)

If Alama Score is reclassified as high-risk credit scoring:

| Requirement | Article | Implementation | Cost Estimate |
|------------|---------|----------------|---------------|
| Risk management system | 9 | Continuous risk identification and mitigation framework | $15K-$30K setup |
| Data governance | 10 | Training data quality, bias detection, representativeness | $10K-$20K setup |
| Technical documentation | 11 | Comprehensive system documentation | $5K-$15K |
| Record-keeping | 12 | Automatic logging of AI decisions | $5K-$10K setup |
| Transparency & information | 13 | User-facing documentation of system capabilities | $3K-$8K |
| Human oversight | 14 | Human-in-the-loop for credit-related outputs | $10K-$25K setup |
| Accuracy, robustness, cybersecurity | 15 | Testing, validation, adversarial robustness | $15K-$40K setup |
| Conformity assessment | 43 | Third-party conformity assessment | $20K-$50K |
| EU database registration | 49 | Register in EU high-risk AI database | $2K-$5K |
| Post-market monitoring | 72 | Ongoing monitoring system | $10K-$20K/year |
| **Total first-year compliance** | | | **$95K-$223K** |
| **Annual ongoing** | | | **$25K-$50K/year** |

### 5.2 Conformity Assessment Requirements

| Requirement | Notes |
|------------|-------|
| Quality management system (Article 17) | ISO 9001-equivalent for AI systems |
| Risk management system (Article 9) | Continuous risk identification, analysis, estimation, evaluation |
| Technical documentation (Article 11) | System description, design, development, validation |
| Automatic logging (Article 12) | Audit trail for all AI decisions |
| Transparency (Article 13) | User-facing explainability |
| Human oversight (Article 14) | Meaningful human review of automated decisions |
| Accuracy & robustness (Article 15) | Performance metrics, adversarial testing |

---

## 6. GEOGRAPHIC APPLICABILITY

### 6.1 Does the EU AI Act Apply to Angavu?

| Criterion | Assessment |
|-----------|-----------|
| Placed on EU market? | **No** — Angavu operates in Africa only |
| Output used in EU? | **No** — all processing is on-device in Africa |
| EU-based entity? | **No** — Angavu is Kenya-based |
| **Direct applicability** | **No** — EU AI Act does NOT directly apply |

### 6.2 Why EU AI Act Still Matters

| Reason | Impact |
|--------|--------|
| **Investor expectations** | EU/US investors may require EU AI Act compliance as due diligence condition |
| **Kenya AI Bill mirrors EU AI Act** | Kenya's AI Bill 2026 uses EU AI Act as template; compliance with one helps with the other |
| **Pan-African precedent** | Other African nations drafting AI legislation are looking at EU AI Act |
| **Future EU expansion** | If Angavu enters EU market (diaspora users), compliance needed |
| **Global standard** | EU AI Act becoming de facto global AI governance standard |

### 6.3 Strategic Recommendation

**Comply voluntarily with limited-risk requirements** (transparency, AI literacy). This:
1. Costs very little ($5K-$15K)
2. Positions Angavu as globally compliant
3. Satisfies investor due diligence
4. Pre-complies with Kenya AI Bill requirements
5. Creates competitive moat against non-compliant competitors

---

## 7. THE ALAMA SCORE POSITIONING STRATEGY

### 7.1 Why "Financial Readiness Assessment" Avoids High-Risk

| EU AI Act Criterion | "Credit Scoring" Classification | "Financial Readiness" Classification |
|--------------------|--------------------------------|-------------------------------------|
| Evaluates creditworthiness? | Yes | No — evaluates business health |
| Establishes credit score? | Yes | No — establishes readiness score |
| Used for credit decisions? | Yes | No — advisory to worker only |
| Third-party access to score? | Yes (lenders) | No — worker controls data |
| Annex III 5(b) applies? | **YES — HIGH RISK** | **NO — LIMITED RISK** |

### 7.2 The Legal Argument

The EU AI Act targets AI systems that are **used by third parties to make decisions about credit access**. Alama Score, as positioned:

1. Is a **self-assessment tool** — the worker uses it to understand their own finances
2. Does not share data with lenders at launch
3. Does not approve or deny credit
4. Is closer to a **financial calculator** than a **credit bureau**
5. The score belongs to the worker, not to a financial institution

**Legal precedent:** Credit Karma, ClearScore, and similar services that provide free credit scores to consumers are generally NOT classified as credit scoring systems because they inform the consumer, not the lender. Alama Score follows the same model.

### 7.3 Phased Positioning

| Phase | Alama Score Positioning | EU AI Act Classification |
|-------|------------------------|-------------------------|
| Phase 1 (0-12 months) | "Financial Readiness Assessment" — advisory, no external sharing | **Limited risk** |
| Phase 2 (12-24 months) | "Business Health Score" — worker-controlled sharing | **Limited risk** |
| Phase 3 (24-36 months) | Lender integration with full compliance | **High risk** — compliance package activated |

---

## 8. COMPETITIVE IMPLICATIONS

### 8.1 Compliance as Moat

| Competitor | EU AI Act Exposure | Angavu Advantage |
|-----------|-------------------|-----------------|
| Jumo (cloud BaaS) | High — credit scoring for banks | Angavu's advisory positioning avoids high-risk |
| Tala/Branch (digital lenders) | High — credit decisioning | Competitors must comply; Angavu doesn't |
| Big Tech (Google/Meta AI) | Medium — depends on product | Angavu is too small to be a target |
| Cloud-based fintech | High — centralized data processing | Angavu's on-device model = lower risk profile |

### 8.2 Cost Advantage

| | Angavu (Limited Risk) | Competitor (High Risk) |
|---|----------------------|----------------------|
| Compliance setup | $5K-$15K | $95K-$223K |
| Annual compliance | $3K-$8K | $25K-$50K |
| **Total Year 1** | **$8K-$23K** | **$120K-$273K** |
| **Savings** | | **$112K-$250K** |

---

## 9. IMPLEMENTATION CHECKLIST

### 9.1 Immediate Actions (Limited Risk Compliance)

- [ ] Add AI disclosure to Msaidizi onboarding ("You are interacting with an AI assistant")
- [ ] Label all AI-generated insights as "AI-generated"
- [ ] Document AI capabilities and limitations for internal use
- [ ] Staff AI literacy training program
- [ ] Publish transparency page ("How Msaidizi Works")

### 9.2 Contingency Actions (If High-Risk Triggered)

- [ ] Activate high-risk compliance package
- [ ] Commission conformity assessment
- [ ] Implement human-in-the-loop for Alama Score
- [ ] Register in EU AI database (if applicable)
- [ ] Hire regulatory counsel with EU AI Act expertise
- [ ] Prepare technical documentation (Article 11)
- [ ] Implement automatic logging (Article 12)

---

*This assessment is based on the EU AI Act text as published in the Official Journal of the European Union (OJ L, 12.7.2024). Review upon publication of implementing acts and guidelines.*

**Angavu Intelligence © 2026**
