# Nigeria Data Protection Act (NDPA) 2023 — Compliance Checklist

**Applicable Law:** Nigeria Data Protection Act 2023
**Regulatory Authority:** Nigeria Data Protection Commission (NDPC)
**Effective Date:** June 12, 2023
**Date:** July 2026
**Status:** Pre-expansion preparation — Angavu not yet operating in Nigeria

---

## 1. REGISTRATION & ORGANIZATIONAL REQUIREMENTS

### 1.1 NDPC Registration

| Requirement | NDPA Provision | Status | Action Required | Priority |
|------------|---------------|--------|-----------------|----------|
| Register as Data Controller | Section 5(1)(a) | ⬜ TODO | File registration with NDPC before processing Nigerian data | **Critical** |
| Register as Data Processor | Section 5(1)(b) | ⬜ TODO | Required if processing on behalf of others | High |
| Designate Data Protection Officer | Section 32(1) | ⬜ TODO | Appoint DPO; can be shared at startup stage | **Critical** |
| Maintain Data Protection Register | Section 5(3) | ⬜ TODO | Record of all processing activities | High |
| Annual Data Protection Audit | Section 39 | ⬜ TODO | Due by March 31 each year; submit to NDPC | **Critical** |

### 1.2 Filing Deadlines

| Filing | Deadline | Penalty for Non-Compliance |
|--------|----------|---------------------------|
| NDPC Registration | Before processing begins | Up to ₦10M or 2% annual revenue |
| Annual Audit Report | March 31 each year | Up to ₦10M or 2% annual revenue |
| Breach Notification | Within 72 hours of discovery | Up to ₦10M or 2% annual revenue |

---

## 2. LAWFUL BASIS FOR PROCESSING

### 2.1 Consent Requirements (NDPA-Specific)

| Requirement | NDPA Provision | Angavu Implementation | Status |
|------------|---------------|----------------------|--------|
| Freely given consent | Section 26(1)(a) | Consent at onboarding; no service denial for optional processing | ✅ Design |
| Specific consent | Section 26(1)(b) | Granular consent per data type and purpose | ⬜ TODO — Update consent UI for Nigeria |
| Informed consent | Section 26(1)(c) | Plain-language privacy notice in local languages | ⬜ TODO — Hausa, Yoruba, Igbo consent flows |
| Unambiguous consent | Section 26(1)(d) | Explicit opt-in; no pre-ticked boxes | ✅ Design |
| Withdrawable consent | Section 26(2) | Settings → Privacy → consent toggles | ✅ Design |
| Child data (under 18) | Section 31 | Age verification gate in onboarding | ⬜ TODO — Nigeria-specific age check |

### 2.2 Alternative Lawful Bases

| Basis | Applicable Processing | Documentation |
|-------|----------------------|---------------|
| Contractual necessity | Transaction recording for Msaidizi service delivery | Terms of service clause |
| Legitimate interest | Anonymized market intelligence aggregation | Legitimate interest assessment on file |
| Legal obligation | Tax compliance records (if applicable) | Legal counsel review |

---

## 3. DATA MINIMIZATION & PURPOSE LIMITATION

### 3.1 Data Collection Inventory

| Data Category | Collected? | Purpose | Lawful Basis | Nigeria-Specific Note |
|--------------|-----------|---------|-------------|----------------------|
| Transaction amounts | ✅ | Business intelligence | Consent | Standard |
| Transaction categories | ✅ | Demand forecasting | Consent | Standard |
| Transaction dates/times | ✅ | Time series analysis | Consent | Standard |
| Voice input | ✅ | Dialect training (opt-in) | Explicit consent | ⚠️ Biometric under NDPA — specific consent |
| Location data | ❌ | N/A | N/A | Good — reduces compliance burden |
| Contacts | ❌ | N/A | N/A | Good — FCCPC restriction avoided |
| SMS/messages | ❌ | N/A | N/A | Good — FCCPC restriction avoided |
| Call logs | ❌ | N/A | N/A | Good — FCCPC restriction avoided |
| Device identifiers | Minimal | Fraud prevention only | Legitimate interest | ⚠️ NDPC may require consent |
| Alama Score | ✅ | Financial readiness (user-only) | Explicit consent | ⚠️ Keep advisory — avoid credit scoring classification |

### 3.2 NDPA Data Minimization Compliance

| Principle | Angavu Compliance |
|-----------|-------------------|
| Collect only what's necessary | ✅ On-device AI processes only business transaction data |
| No excessive collection | ✅ No contacts, SMS, call logs, or location |
| Purpose limitation | ✅ Each data type has documented purpose |
| No incompatible secondary use | ✅ Federated learning uses only anonymized gradients |

---

## 4. DATA SUBJECT RIGHTS

### 4.1 NDPA Rights Implementation

| Right | NDPA Provision | Implementation | Status |
|-------|---------------|----------------|--------|
| Right of access | Section 34(1)(a) | Data export feature (JSON/CSV) | ⬜ TODO |
| Right to rectification | Section 34(1)(b) | Edit transactions in-app | ✅ Existing |
| Right to erasure | Section 34(1)(c) | Account deletion + local data purge | ⬜ TODO |
| Right to data portability | Section 34(1)(d) | Export in standard format | ⬜ TODO |
| Right to object | Section 34(1)(e) | Granular opt-out controls | ⬜ TODO |
| Right to restrict processing | Section 34(1)(f) | Processing pause feature | ⬜ TODO |
| Right not to be subject to automated decisions | Section 37 | Alama Score is advisory, not decisional | ✅ Design |

### 4.2 Response Timeline

| Request Type | NDPA Deadline | Angavu Target |
|-------------|---------------|---------------|
| Standard DSAR | 30 days | 14 days |
| Complex requests | 60 days (with notice) | 30 days |
| Identity verification | Before processing | Automated verification |

---

## 5. DATA LOCALIZATION & CROSS-BORDER TRANSFERS

### 5.1 Nigeria Localization Requirements

| Requirement | NDPA Provision | Angavu Compliance |
|------------|---------------|-------------------|
| Local storage preference | Section 41(1) | ✅ On-device = data stays in Nigeria |
| Critical data infrastructure | Section 41(2) | ⬜ Evaluate if scaling to critical mass |
| Cross-border transfer safeguards | Section 41(3)-(5) | ✅ No personal data leaves device |

### 5.2 Cross-Border Transfer Assessment

| Transfer Scenario | Personal Data? | Safeguard Required | Status |
|------------------|---------------|-------------------|--------|
| Federated learning gradients to aggregation server | No (anonymized) | None required | ✅ Compliant |
| Model updates back to device | No | None required | ✅ Compliant |
| Angavu Pulse aggregate data | No (k-anonymized, k≥5) | None required | ✅ Compliant |
| Customer support data | Potentially | Adequacy or consent | ⬜ TODO — Localize support |

### 5.3 NDPC Adequacy Decisions

| Status | Note |
|--------|------|
| No formal adequacy list published yet | Monitor NDPC guidance |
| Use consent + contractual safeguards as interim | Document in transfer impact assessment |

---

## 6. BREACH NOTIFICATION

### 6.1 NDPA Breach Requirements

| Requirement | NDPA Provision | Timeline | Angavu Implementation |
|------------|---------------|----------|----------------------|
| Notify NDPC | Section 40(1) | Within 72 hours | ⬜ TODO — Build breach detection pipeline |
| Notify affected data subjects | Section 40(2) | Without undue delay | ⬜ TODO — Build user notification system |
| Document breach | Section 40(3) | Maintain register | ⬜ TODO — Breach register template |
| Remedial measures | Section 40(4) | Immediate | ⬜ TODO — Incident response plan |

### 6.2 Breach Register Template

| Field | Description |
|-------|------------|
| Breach ID | Unique identifier |
| Date discovered | When breach was identified |
| Date occurred | When breach actually happened |
| Description | Nature and scope of breach |
| Data affected | Categories and volume |
| Individuals affected | Number and type |
| Root cause | Technical/organizational failure |
| Remedial actions | Steps taken |
| NDPC notification | Date and reference number |
| Data subject notification | Date and method |

---

## 7. SPECIAL CATEGORIES (NDPA-SPECIFIC)

### 7.1 Sensitive Data Processing

| Category | NDPA Rule | Angavu Handling | Status |
|----------|----------|-----------------|--------|
| Financial data | Explicit consent required | ✅ Consent in onboarding | ✅ |
| Health data | Explicit consent; no collection | ❌ Not collected | ✅ N/A |
| Biometric data (voice) | Explicit consent required | ⬜ Separate opt-in flow | ⬜ TODO |
| Religious data (tithe tracker) | Explicit consent required | ⬜ Specific consent needed | ⬜ TODO |
| Ethnic data | Explicit consent; no collection | ❌ Not collected | ✅ N/A |

---

## 8. PENALTIES & ENFORCEMENT

### 8.1 NDPA Penalty Framework

| Violation | Maximum Penalty |
|-----------|----------------|
| Processing without registration | ₦10M or 2% annual revenue |
| Failure to notify breach | ₦10M or 2% annual revenue |
| Cross-border transfer violation | ₦10M or 2% annual revenue |
| Failure to conduct audit | ₦10M or 2% annual revenue |
| Non-compliance with data subject rights | ₦10M or 2% annual revenue |
| Processing children's data without safeguards | ₦10M or 2% annual revenue |

### 8.2 Risk Assessment for Angavu

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Registration failure | Low (proactive) | High (₦10M) | Register before processing |
| Audit failure | Low (proactive) | High (₦10M) | Annual audit calendar |
| Consent deficiency | Medium | Medium | Nigeria-specific consent flows |
| Cross-border issue | Very Low | High | On-device architecture eliminates this |

---

## 9. IMPLEMENTATION TIMELINE

| Phase | Timeline | Actions |
|-------|----------|---------|
| **Pre-Nigeria (Now)** | Months 0-6 | Legal review; draft Nigeria privacy policy; design consent flows |
| **Registration** | Before processing | NDPC registration; DPO appointment |
| **Localization** | Months 0-3 of operations | Nigeria-specific consent (Hausa, Yoruba, Igbo); age verification |
| **Compliance** | Months 3-6 of operations | Data subject rights implementation; breach notification pipeline |
| **Audit** | Annually (March 31) | Submit annual data protection audit to NDPC |

---

## 10. NIGERIA-SPECIFIC CONSIDERATIONS

### 10.1 FCCPC Restrictions on Digital Lenders

Nigeria's FCCPC (Federal Competition and Consumer Protection Commission) has restricted digital lenders' access to:
- Call logs
- SMS messages
- Contact lists

**Angavu advantage:** Msaidizi does NOT collect any of these data types. This restriction squeezes competitors (Tala, Branch, FairMoney) who relied on phone data for credit scoring. Angavu's on-device business intelligence model is already compliant.

### 10.2 Nigerian Languages for Consent

| Language | Speakers | Priority |
|----------|----------|----------|
| Hausa | 70M+ (Northern Nigeria) | **Critical** |
| Yoruba | 45M+ (Southwest Nigeria) | **Critical** |
| Igbo | 30M+ (Southeast Nigeria) | **Critical** |
| Pidgin English | 75M+ (National) | **High** |
| English | Official language | **Required** |

---

*This checklist is maintained by Angavu Intelligence. Review quarterly against NDPC guidance updates.*

**Angavu Intelligence © 2026**
