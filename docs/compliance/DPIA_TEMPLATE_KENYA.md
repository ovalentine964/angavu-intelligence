# Data Protection Impact Assessment (DPIA) Template
## Kenya Data Protection Act 2019 — Section 31

**Prepared for:** Angavu Intelligence
**Regulatory Authority:** Office of the Data Protection Commissioner (ODPC)
**Date:** July 2026
**Version:** 1.0
**Classification:** Internal — Compliance Document

---

## SECTION 1: PROJECT DESCRIPTION

### 1.1 Overview

| Field | Details |
|-------|---------|
| **Project Name** | Msaidizi — Voice-First AI CFO for Informal Workers |
| **Data Controller** | Angavu Intelligence Ltd |
| **Data Protection Officer** | [Name, Contact — appoint before filing] |
| **Date of Assessment** | [Date] |
| **Review Date** | [12 months from assessment] |
| **Project Lead** | Valentine Owuor, Founder |

### 1.2 Systematic Description of Processing

**Nature of processing:**
- Msaidizi records user-initiated business transactions (sales, expenses, inventory) via voice input on the user's device
- On-device AI model (Qwen 0.5B) processes transaction data locally to generate business insights
- Federated learning aggregates anonymized model gradients (not personal data) across devices to improve the global model
- Alama Score generates a financial readiness assessment from the user's own transaction history, stored locally

**Scope of processing:**
- Transaction amounts, categories, dates, and timestamps
- Voice input for dialect training (opt-in only)
- Aggregated, anonymized business patterns for market intelligence (k-anonymity, k≥5)
- Location data: NOT collected
- Contacts/SMS/call logs: NOT collected
- Biometric data: Voice data collected only with explicit opt-in

**Context of processing:**
- Target population: Informal workers in Kenya (initially), expanding to Nigeria, South Africa
- Users are adults (18+) engaged in informal economic activity
- Processing is performed on-device; data does not leave the user's phone except for anonymized model gradients
- Purpose: Business intelligence, financial literacy, demand forecasting, and financial readiness assessment

**Purpose of processing:**
1. Provide real-time business intelligence (profit/loss, demand forecasting)
2. Generate financial readiness assessments (Alama Score)
3. Improve AI model quality through federated learning
4. Produce anonymized aggregate market intelligence (Angavu Pulse)

### 1.3 Assessment of Necessity and Proportionality

| Principle | Assessment |
|-----------|-----------|
| **Lawful basis** | Explicit consent obtained at onboarding; granular consent for each data type |
| **Purpose limitation** | Data used only for stated purposes; no secondary use without additional consent |
| **Data minimization** | Only business transaction data collected; no contacts, SMS, location, or call logs |
| **Accuracy** | User-initiated input; real-time recording ensures freshness |
| **Storage limitation** | Data stored on-device; user controls retention through app settings |
| **Integrity & confidentiality** | On-device encryption; PQC-ready encryption stubs; no centralized data store |
| **Accountability** | DPO appointed; processing records maintained; this DPIA on file |

---

## SECTION 2: IDENTIFY AND ASSESS RISKS

### 2.1 Risk Assessment Matrix

| Risk ID | Risk Description | Likelihood | Impact | Overall Risk | Mitigation |
|---------|-----------------|------------|--------|-------------|------------|
| R01 | Unauthorized access to user's transaction data on device | Low | High | **Medium** | On-device encryption; biometric/PIN app lock; no cloud sync by default |
| R02 | Model gradient reversal to extract personal data | Very Low | High | **Low** | Differential privacy noise injection; secure aggregation; gradient compression |
| R03 | Re-identification from aggregated market intelligence (Angavu Pulse) | Very Low | High | **Low** | k-anonymity (k≥5); geographic aggregation at county level minimum; minimum cell size enforcement |
| R04 | Voice data misuse for biometric profiling | Low | Medium | **Low** | Explicit opt-in; separate consent; voice data stored locally; can be deleted independently |
| R05 | Unauthorized third-party access to Alama Score | Low | Medium | **Low** | Score stored locally; no external sharing without explicit user action; Phase 2 sharing requires user-initiated export |
| R06 | Inadequate consent for federated learning participation | Medium | Medium | **Medium** | Clear, plain-language consent at onboarding; opt-out available at any time; model contribution is optional |
| R07 | Device theft exposing financial data | Medium | Medium | **Medium** | Encrypted local storage; remote wipe capability; auto-lock after inactivity |
| R08 | Algorithmic bias in financial readiness assessment | Medium | Medium | **Medium** | Regular bias audits; diverse training data; fairness metrics across gender, age, and business type |
| R09 | User data retained after account deletion | Low | High | **Medium** | Automated data purge on account deletion; federated learning models do not retain individual data points |
| R10 | Cross-border model gradient transfer | Very Low | Low | **Very Low** | Gradients are anonymized mathematical parameters, not personal data; differential privacy applied |

### 2.2 Risk Scoring Guide

| Likelihood | Impact | Risk Level |
|-----------|--------|-----------|
| Very Low | Low/Medium/High/Very High | Very Low |
| Low | Low/High | Low |
| Low | Very High | Medium |
| Medium | Low | Low |
| Medium | Medium | Medium |
| Medium | High | High |
| High | Low | Medium |
| High | Medium/High | High |
| Very High | Any | Very High |

---

## SECTION 3: MEASURES TO MITIGATE RISKS

### 3.1 Technical Measures

| Risk ID | Technical Measure | Status |
|---------|-------------------|--------|
| R01 | AES-256 encryption for all on-device data at rest | ✅ Implemented |
| R01 | TLS 1.3 for all network communications | ✅ Implemented |
| R01 | Biometric/PIN app lock | ⬜ Planned |
| R02 | Differential privacy (ε=1.0) on federated learning gradients | ✅ Implemented |
| R02 | Secure aggregation protocol | ✅ Implemented |
| R02 | Gradient compression to reduce information density | ✅ Implemented |
| R03 | k-anonymity enforcement (k≥5) for all aggregated outputs | ✅ Implemented |
| R03 | County-level minimum geographic aggregation | ✅ Implemented |
| R04 | Voice data stored in separate encrypted container | ✅ Implemented |
| R05 | Alama Score stored in encrypted local database | ✅ Implemented |
| R07 | Android Keystore for encryption key management | ✅ Implemented |
| R08 | Automated bias detection pipeline for model updates | ⬜ Planned |
| R09 | Automated data purge on account deletion | ⬜ Planned |

### 3.2 Organizational Measures

| Measure | Description | Status |
|---------|-------------|--------|
| Data Protection Officer | Appointed DPO responsible for compliance | ⬜ TODO |
| Privacy training | Annual privacy training for all staff | ⬜ TODO |
| Incident response plan | Documented breach notification procedure (72h ODPC) | ⬜ TODO |
| Data processing records | Maintained in compliance management system | ✅ Done |
| Vendor assessment | No third-party data processors (on-device architecture) | ✅ N/A |
| Regular DPIA review | Annual review or upon significant processing changes | ⬜ Scheduled |

### 3.3 Consent Framework

| Processing Activity | Consent Type | Granularity | Withdrawal Mechanism |
|--------------------|-------------|-------------|---------------------|
| Transaction recording | Explicit consent | Per-category (sales, expenses, inventory) | Settings → Privacy → Data Management |
| Alama Score generation | Explicit consent | Single toggle | Settings → Privacy → Alama Score |
| Federated learning participation | Explicit consent | Single toggle | Settings → Privacy → Model Training |
| Voice data for dialect improvement | Explicit consent | Separate opt-in | Settings → Privacy → Voice Data |
| Market intelligence aggregation | Legitimate interest | Opt-out | Settings → Privacy → Anonymized Analytics |

---

## SECTION 4: DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S ANDROID DEVICE                      │
│                                                               │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐    │
│  │  Voice    │───>│  Transaction  │───>│  Local Database  │    │
│  │  Input    │    │  Parser       │    │  (Encrypted)     │    │
│  └──────────┘    └──────────────┘    └────────┬─────────┘    │
│                                               │              │
│                    ┌──────────────────────────┼──────────┐   │
│                    │                          │          │   │
│                    ▼                          ▼          ▼   │
│           ┌──────────────┐          ┌────────────┐ ┌──────┐  │
│           │  Business     │          │  Alama     │ │Soko  │  │
│           │  Intelligence │          │  Score     │ │Pulse │  │
│           │  Engine       │          │  Engine    │ │Local │  │
│           └──────────────┘          └────────────┘ └──────┘  │
│                    │                                          │
│                    ▼                                          │
│           ┌──────────────┐                                   │
│           │  Federated    │                                   │
│           │  Learning     │                                   │
│           │  (Local)      │                                   │
│           └──────┬───────┘                                   │
│                  │ Anonymized gradients only                  │
│                  │ (ε=1.0 differential privacy)               │
└──────────────────┼───────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                 ANGAVU AGGREGATION SERVER                     │
│                                                               │
│  ┌──────────────┐    ┌──────────────┐                        │
│  │  Secure       │───>│  Global Model │                       │
│  │  Aggregation  │    │  Update       │                       │
│  └──────────────┘    └──────┬───────┘                        │
│                             │ Improved model                  │
│                             ▼                                 │
│                     ┌──────────────┐                          │
│                     │  Angavu Pulse │                         │
│                     │  (Aggregated, │                         │
│                     │  k≥5, county  │                         │
│                     │  level min)   │                         │
│                     └──────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

**Key data protection features:**
- Personal data NEVER leaves the device
- Only anonymized model gradients are transmitted
- Server aggregates gradients using secure aggregation protocol
- Angavu Pulse outputs are k-anonymized (k≥5) at county level minimum

---

## SECTION 5: CONSULTATION

### 5.1 Internal Stakeholders

| Stakeholder | Consulted | Input |
|-------------|-----------|-------|
| Founder (Valentine Owuor) | ✅ | Product vision and processing purposes |
| Technical Lead | ✅ | Architecture details, encryption implementation |
| Legal Counsel | ⬜ TODO | Legal compliance review |

### 5.2 External Stakeholders

| Stakeholder | Consulted | Input |
|-------------|-----------|-------|
| ODPC | ⬜ TODO | Pre-submission consultation request |
| Strathmore CIPIT | ⬜ TODO | Independent privacy audit |
| Target user representatives | ⬜ TODO | Consent flow usability testing |

### 5.3 Data Subject Consultation

| Method | Status | Findings |
|--------|--------|----------|
| User testing of consent flows | ⬜ TODO | [To be completed] |
| Focus group on data practices | ⬜ TODO | [To be completed] |
| Community feedback (pilot counties) | ⬜ TODO | [To be completed] |

---

## SECTION 6: DECISION AND SIGN-OFF

### 6.1 DPIA Outcome

| Decision | Rationale |
|----------|-----------|
| [ ] **Proceed** | Risks adequately mitigated by technical and organizational measures |
| [ ] **Proceed with conditions** | Risks mitigated after implementing additional measures listed below |
| [ ] **Do not proceed** | Risks cannot be adequately mitigated; redesign required |

### 6.2 Conditions (if applicable)

| Condition | Owner | Deadline | Status |
|-----------|-------|----------|--------|
| Appoint DPO | Founder | [Date] | ⬜ |
| Implement biometric app lock | Tech Lead | [Date] | ⬜ |
| Complete bias audit for Alama Score | Data Science | [Date] | ⬜ |
| Submit to ODPC for review | DPO | [Date] | ⬜ |

### 6.3 Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Data Controller | Valentine Owuor | __________ | ________ |
| Data Protection Officer | [Name] | __________ | ________ |
| Technical Lead | [Name] | __________ | ________ |
| Legal Counsel | [Name] | __________ | ________ |

---

## SECTION 7: REVIEW SCHEDULE

| Trigger | Action |
|---------|--------|
| Annual review | Re-assess all risks and mitigations |
| New product feature | Partial or full DPIA update |
| Regulatory change | Update risk assessments |
| Data breach | Immediate review and update |
| User count milestone (10K, 100K, 1M) | Review proportionality |
| Alama Score expansion (Phase 2/3) | New DPIA for credit-adjacent processing |

---

*This DPIA template complies with Kenya Data Protection Act 2019, Section 31, and the Data Protection (General) Regulations 2021.*

**Angavu Intelligence © 2026**
