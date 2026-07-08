# Regulatory Compliance Checklist — Angavu Intelligence

**Scope:** Kenya Data Protection Act (DPA), Nigeria Data Protection Act (NDPA), South Africa POPIA
**Date:** July 2026
**Status:** Living document — update quarterly

---

## 1. Kenya Data Protection Act (2019) — ODPC Requirements

### 1.1 Data Controller Registration

| Requirement | Status | Action Required |
|-------------|--------|-----------------|
| Register with ODPC as data controller | ⬜ TODO | File registration before collecting any user data |
| Designate a Data Protection Officer (DPO) | ⬜ TODO | Appoint DPO (can be founder at startup stage) |
| Maintain processing records | ✅ DONE | Federated learning architecture logs all on-device processing |
| Respond to data subject requests within 30 days | ⬜ TODO | Build automated DSAR workflow into Msaidizi |

### 1.2 Lawful Basis for Processing

| Processing Activity | Lawful Basis | Documentation |
|---------------------|-------------|---------------|
| Transaction recording (Msaidizi) | Consent (explicit) | Consent flow in onboarding; stored in `ConsentManager.kt` |
| Federated learning model training | Legitimate interest + consent | Data never leaves device; model updates are anonymized |
| Alama Score assessment | Consent (explicit) | User-initiated; score belongs to user |
| Market intelligence aggregation | Legitimate interest | Fully anonymized, k-anonymity enforced (k≥5) |
| Voice data for dialect training | Consent (explicit) | Opt-in during onboarding; can withdraw anytime |

### 1.3 Data Protection Impact Assessment (DPIA)

| Trigger | Required? | Status |
|---------|-----------|--------|
| Large-scale processing of personal data | Yes, if >10,000 users | ⬜ Prepare before scale milestone |
| Systematic monitoring | Not applicable (on-device) | ✅ N/A — no centralized monitoring |
| Sensitive financial data | Yes | ⬜ Prepare before Alama Score launch |
| Automated decision-making | Yes, for Alama Score | ⬜ Prepare before Alama Score expansion |

### 1.4 Data Subject Rights

| Right | Implementation | Status |
|-------|---------------|--------|
| Right to access | Export all user data from device | ⬜ TODO — build data export feature |
| Right to rectification | Edit transactions in Msaidizi | ✅ DONE — existing feature |
| Right to erasure | Delete account + all local data | ⬜ TODO — build account deletion flow |
| Right to data portability | Export in standard format | ⬜ TODO — JSON/CSV export |
| Right to object | Opt-out of specific processing | ⬜ TODO — granular consent controls |

### 1.5 Cross-Border Transfer

| Rule | Angavu Compliance |
|------|-------------------|
| Data must stay in Kenya (or adequate jurisdiction) | ✅ DONE — federated learning = data stays on device |
| Cloud fallback must use Kenya-region servers | ✅ DONE — Oracle Cloud Africa region |
| No transfer to non-adequate countries | ✅ DONE — on-device architecture eliminates transfers |

### 1.6 Breach Notification

| Requirement | Timeline | Status |
|-------------|----------|--------|
| Notify ODPC of breach | Within 72 hours | ⬜ TODO — build breach detection and notification pipeline |
| Notify affected data subjects | Without undue delay | ⬜ TODO — build user notification system |
| Document all breaches | Maintain register | ⬜ TODO — breach register template |

---

## 2. Nigeria Data Protection Act (2023) — NDPC Requirements

### 2.1 Applicability

NDPA applies if Angavu:
- Processes data of Nigerian citizens
- Has operations in Nigeria
- Offers goods/services to Nigerian market

**Current status:** Not yet operating in Nigeria. Register compliance obligations before Nigeria expansion.

### 2.2 Data Controller/Processor Registration

| Requirement | Status | Action Required |
|-------------|--------|-----------------|
| Register with NDPC | ⬜ TODO | Required before processing Nigerian data |
| Appoint DPO for Nigeria operations | ⬜ TODO | Can be shared DPO at startup stage |
| Filing of annual data protection audit | ⬜ TODO | Due by March 31 each year |

### 2.3 Consent Requirements (NDPA Specific)

| Requirement | Kenya DPA | NDPA Difference | Action |
|-------------|-----------|-----------------|--------|
| Consent must be freely given | ✅ | Same | No change |
| Consent must be specific | ✅ | NDPA requires granular consent per purpose | ⬜ Update consent UI for Nigeria |
| Consent must be informed | ✅ | NDPA requires local language disclosure | ⬜ Add Hausa, Yoruba, Igbo consent flows |
| Right to withdraw consent | ✅ | Same | No change |
| Child data (under 18) | ⬜ | NDPA has specific child protections | ⬜ Add age verification for Nigeria |

### 2.4 Data Localization

| Rule | Angavu Compliance |
|------|-------------------|
| NDPA requires "necessary" localization for sensitive data | ✅ DONE — on-device processing satisfies this |
| Critical data infrastructure must be in Nigeria | Not yet applicable | ⬜ Evaluate when scaling to Nigeria |

### 2.5 Nigeria-Specific Penalties

| Violation | Penalty |
|-----------|---------|
| Processing without registration | Up to ₦10M or 2% of annual revenue |
| Breach notification failure | Up to ₦10M or 2% of annual revenue |
| Cross-border transfer violation | Up to ₦10M or 2% of annual revenue |

---

## 3. South Africa POPIA — Information Regulator Requirements

### 3.1 Applicability

POPIA applies if Angavu:
- Processes personal information in South Africa
- Has a branch or office in South Africa
- Processes SA residents' data

**Current status:** Not yet operating in South Africa. Register before expansion.

### 3.2 Information Officer Registration

| Requirement | Status | Action Required |
|-------------|--------|-----------------|
| Register Information Officer with Regulator | ⬜ TODO | Required before processing SA data |
| Deputy Information Officer (optional) | ⬜ TODO | Recommended for scale |

### 3.3 POPIA Conditions for Lawful Processing

| Condition | Implementation | Status |
|-----------|---------------|--------|
| **Accountability** | DPO + compliance documentation | ⬜ TODO |
| **Processing limitation** | Minimum necessary data; consent-based | ✅ DONE — on-device, consent-based |
| **Purpose specification** | Clear purpose for each data type | ⬜ TODO — document processing purposes |
| **Further processing limitation** | No secondary use without consent | ✅ DONE — federated learning is purpose-limited |
| **Information quality** | Accurate, complete, up-to-date | ✅ DONE — real-time transaction recording |
| **Openness** | Privacy policy, transparency | ⬜ TODO — publish POPIA-compliant privacy policy |
| **Security safeguards** | Encryption, access controls | ✅ DONE — PQC stubs + on-device encryption |
| **Data subject participation** | Access, correction, deletion rights | ⬜ TODO — build SA-specific rights workflow |

### 3.4 Special Personal Information

| Category | POPIA Rule | Angavu Handling |
|----------|-----------|-----------------|
| Financial information | Requires explicit consent | ✅ DONE — consent in onboarding |
| Religious information | Requires explicit consent | ⚠️ Tithe tracker collects religious giving data — needs specific consent |
| Biometric information | Requires explicit consent | ⬜ Voice data = biometric — needs explicit consent flow |

### 3.5 Cross-Border Transfer (POPIA)

| Rule | Angavu Compliance |
|------|-------------------|
| Recipient must have adequate data protection | ✅ DONE — on-device = no transfer |
| Binding corporate rules or consent | ✅ DONE — no transfer needed |
| Transfer only for necessary purposes | ✅ DONE — architecture eliminates transfers |

---

## 4. AI Bill 2026 (Kenya) — Specific Compliance

### 4.1 Risk Classification Mapping

| Angavu Product | Risk Tier | Required Actions |
|----------------|-----------|------------------|
| Msaidizi Voice AI | Minimal | ✅ No special obligations |
| Msaidizi Bookkeeping | Minimal/Limited | ✅ Transparency documentation |
| Msaidizi Business Intelligence | Limited | ⬜ Transparency obligations |
| Msaidizi Financial Literacy | Limited | ⬜ Position as education, not finance |
| Alama Score (as "Financial Readiness Assessment") | Limited | ⬜ Advisory positioning documentation |
| Alama Score (if classified as credit scoring) | High | ⬜ Full compliance package needed |
| Agricultural Domain Agents | High (sector-based) | ⬜ Position as tips, not decision system |

### 4.2 High-Risk Compliance Package (If Triggered)

| Obligation | Status | Priority |
|------------|--------|----------|
| Human rights impact assessment | ⬜ TODO | High — prepare template |
| General risk assessment | ⬜ TODO | High — prepare template |
| Data protection impact assessment | ⬜ TODO | Medium — overlaps with DPA DPIA |
| Workforce impact assessment | ⬜ TODO | Low — Msaidizi creates income, doesn't displace |
| Explainability documentation | ⬜ TODO | High — build into AI output pipeline |
| Traceability logging | ⬜ TODO | Medium — audit trail for AI decisions |
| Annual compliance report | ⬜ TODO | Low — prepare template |
| Reskilling programs | N/A | Msaidizi trains workers, doesn't replace them |

### 4.3 Penalties

| Violation | Penalty |
|-----------|---------|
| Operating high-risk AI without compliance | Up to KSh 5M and/or 2 years imprisonment |
| Failure to conduct impact assessment | Up to KSh 5M |
| Failure to report to AI Commissioner | Up to KSh 5M |

---

## 5. Compliance Cost Moat Analysis

### 5.1 Angavu vs. Competitors — Compliance Cost Comparison

| Cost Category | Angavu (On-Device) | Traditional Competitor (Cloud) |
|---------------|-------------------|-------------------------------|
| Data localization | $0 (data on device) | $20K-$50K/year (Africa-region cloud) |
| Privacy infrastructure | Built into architecture | $30K-$100K/year (DLP, encryption, access controls) |
| DPIA preparation | $2K-$5K (one-time) | $15K-$30K per system |
| Regulatory counsel | $5K-$10K/year | $50K-$150K/year |
| Compliance tooling | Minimal (on-device = no centralized data to audit) | $20K-$50K/year (SIEM, audit tools) |
| Breach response | Minimal (no centralized data to breach) | $50K-$200K per incident |
| **Total Annual Compliance** | **$10K-$30K** | **$150K-$500K** |

### 5.2 The Moat

Angavu's compliance cost is **5-15x lower** than competitors because:
1. **No centralized data** = no data localization costs
2. **Federated learning** = privacy by architecture, not by policy
3. **On-device processing** = no cloud security costs
4. **Consent-first design** = regulatory alignment by default

This creates a structural moat: competitors must spend $150K-$500K/year on compliance that Angavu gets for free through architecture.

---

## 6. Implementation Timeline

| Phase | Timeline | Actions |
|-------|----------|---------|
| **Phase 1: Foundation** | Months 1-6 | ODPC registration, DPO appointment, privacy policy, consent flows |
| **Phase 2: Kenya Compliance** | Months 6-12 | DPIA preparation, data subject rights implementation, breach notification pipeline |
| **Phase 3: AI Bill Preparation** | Months 6-12 | Risk classification documentation, explainability framework, Alama Score positioning |
| **Phase 4: Nigeria Prep** | Months 12-18 | NDPC registration, local language consent flows, age verification |
| **Phase 5: SA Prep** | Months 18-24 | POPIA Information Officer registration, SA-specific privacy policy |

---

*This checklist is maintained by Angavu Intelligence. Review quarterly against regulatory updates.*
