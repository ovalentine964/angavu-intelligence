# South Africa POPIA — Compliance Checklist

**Applicable Law:** Protection of Personal Information Act 4 of 2013 (POPIA)
**Regulatory Authority:** Information Regulator of South Africa
**Effective Date:** July 1, 2021 (fully operational)
**Date:** July 2026
**Status:** Pre-expansion preparation — Angavu not yet operating in South Africa

---

## 1. REGISTRATION & ORGANIZATIONAL REQUIREMENTS

### 1.1 Information Officer Registration

| Requirement | POPIA Provision | Status | Action Required | Priority |
|------------|----------------|--------|-----------------|----------|
| Register Information Officer | Section 55(1) | ⬜ TODO | Register with Information Regulator before processing | **Critical** |
| Appoint Deputy Information Officer | Section 55(2) | ⬜ TODO | Optional but recommended for scale | Medium |
| Operator agreements | Section 20(2) | ⬜ TODO | Written contracts with any data processors | High |
| PAIA Manual | Section 51 | ⬜ TODO | Promotion of Access to Information Act manual | High |

### 1.2 Information Officer Responsibilities

| Responsibility | POPIA Section | Action |
|---------------|--------------|--------|
| Encourage compliance | 55(1)(a) | Internal compliance training |
| Handle data subject requests | 55(1)(b) | DSAR workflow implementation |
| Liaise with Information Regulator | 55(1)(c) | Primary regulatory contact |
| Ensure compliance awareness | 55(1)(d) | Staff training program |

---

## 2. EIGHT CONDITIONS FOR LAWFUL PROCESSING

### 2.1 Condition 1: Accountability

| Requirement | POPIA Section | Angavu Implementation | Status |
|------------|--------------|----------------------|--------|
| Responsible party must comply | 8(1) | DPO + compliance framework | ⬜ TODO |
| Demonstrate compliance | 8(1) | Documentation, audits, DPIA | ⬜ TODO |

### 2.2 Condition 2: Processing Limitation

| Requirement | POPIA Section | Angavu Implementation | Status |
|------------|--------------|----------------------|--------|
| Lawful basis for processing | 9(1) | Consent at onboarding | ✅ Design |
| Minimize data collection | 10(1) | Only business transaction data | ✅ Design |
| Purpose limitation | 13(1) | Documented processing purposes | ⬜ TODO |
| No incompatible secondary use | 13(2) | Federated learning is purpose-limited | ✅ Design |

### 2.3 Condition 3: Purpose Specification

| Requirement | POPIA Section | Angavu Implementation | Status |
|------------|--------------|----------------------|--------|
| Collect for specific purpose | 13(1) | Documented per data type | ⬜ TODO |
| Retain only as long as necessary | 14(1) | User-controlled retention | ✅ Design |
| Destroy/de-identify after purpose fulfilled | 14(1)(b) | Account deletion purge | ⬜ TODO |

### 2.4 Condition 4: Further Processing Limitation

| Requirement | POPIA Section | Angavu Implementation | Status |
|------------|--------------|----------------------|--------|
| Compatible purpose test | 15(1) | Each secondary use documented | ⬜ TODO |
| Consent for new purposes | 15(2) | Additional consent flow | ✅ Design |

### 2.5 Condition 5: Information Quality

| Requirement | POPIA Section | Angavu Implementation | Status |
|------------|--------------|----------------------|--------|
| Reasonably complete and up-to-date | 16(1) | Real-time transaction recording | ✅ Design |
| Data accuracy mechanisms | 16(2) | User editing; anomaly detection | ✅ Existing |

### 2.6 Condition 6: Openness

| Requirement | POPIA Section | Angavu Implementation | Status |
|------------|--------------|----------------------|--------|
| Privacy notification at collection | 17(1) | Privacy policy in local languages | ⬜ TODO — SA-specific policy |
| Data subject must be aware | 17(1)(a)-(g) | Clear disclosure at onboarding | ⬜ TODO |
| Source of data disclosure | 17(1)(d) | "Data comes from your transactions" | ✅ Design |

### 2.7 Condition 7: Security Safeguards

| Requirement | POPIA Section | Angavu Implementation | Status |
|------------|--------------|----------------------|--------|
| Reasonable technical measures | 19(1) | AES-256 encryption; TLS 1.3 | ✅ Implemented |
| Reasonable organizational measures | 19(2) | Access controls; staff training | ⬜ TODO |
| Identify reasonably foreseeable risks | 19(2)(a) | Risk assessment (this document) | ⬜ TODO |
| Establish safeguards | 19(2)(b) | Technical safeguards documented | ✅ Partial |
| Regular evaluation | 19(2)(d) | Annual security review | ⬜ TODO |
| Breach notification to Regulator | 22(1) | Within 72 hours | ⬜ TODO — Pipeline needed |
| Breach notification to data subjects | 22(2) | Without undue delay | ⬜ TODO — Notification system |

### 2.8 Condition 8: Data Subject Participation

| Right | POPIA Section | Implementation | Status |
|-------|--------------|----------------|--------|
| Confirmation of processing | 23(1) | Data export feature | ⬜ TODO |
| Access to personal information | 23(2)(a) | JSON/CSV export | ⬜ TODO |
| Correction of information | 24(1) | In-app editing | ✅ Existing |
| Deletion of information | 24(1)(d) | Account deletion + purge | ⬜ TODO |
| Destruction of information | 24(1)(e) | Data destruction on request | ⬜ TODO |
| Objection to processing | 11(3) | Opt-out controls | ⬜ TODO |

---

## 3. SECTION 71: AUTOMATED DECISION-MAKING

### 3.1 POPIA Section 71 — Critical Provision

**Section 71(1):** "Subject to subsection (2), a data subject may not be subject to a decision which results in legal consequences for him, her or it, or which significantly affects him, her or it, based solely on the automated processing of personal information intended to provide a profile of such person."

### 3.2 Angavu Impact Assessment

| Feature | Automated Decision? | Legal Consequence? | Section 71 Applies? | Mitigation |
|---------|--------------------|--------------------|---------------------|------------|
| Msaidizi business insights | Advisory only | No | **No** | User decides what to do with insights |
| Alama Score | Advisory only | No (at launch) | **No** — advisory positioning | Keep score self-assessment; no external sharing at launch |
| Soko Pulse market prices | Informational | No | **No** | Prices are aggregated data, not individualized |
| Demand forecasting | Advisory only | No | **No** | User decides whether to follow recommendations |
| Alama Score (Phase 3 — lender integration) | **Yes** — informs credit decisions | **Yes** | **YES** | Implement human-in-the-loop; explicit consent; right to contest |

### 3.3 Section 71 Compliance Strategy

**Phase 1 (Advisory only):** Section 71 does NOT apply. All AI outputs are advisory. The worker makes all decisions. Document this clearly.

**Phase 3 (Lender integration):** If Alama Score informs credit decisions:

| Requirement | Implementation |
|-------------|---------------|
| Human-in-the-loop | Human reviewer validates automated assessment before credit decision |
| Right to contest | User can request human review of any automated decision |
| Explicit consent | User opts in to credit decision processing specifically |
| Transparency | User informed that automated processing was used |
| Explanation | User receives plain-language explanation of score factors |

---

## 4. SPECIAL PERSONAL INFORMATION

### 4.1 POPIA Section 26-33 — Special Categories

| Category | POPIA Rule | Angavu Handling | Status |
|----------|----------|-----------------|--------|
| **Financial information** | Section 26(1) — requires explicit consent | ✅ Consent in onboarding | ✅ |
| **Religious information** | Section 30 — requires explicit consent | ⚠️ Tithe tracker collects religious giving data | ⬜ TODO — Specific consent flow |
| **Biometric information** | Section 26(1) — requires explicit consent | ⚠️ Voice data = biometric | ⬜ TODO — Separate consent |
| **Health information** | Section 26(1) — requires explicit consent | ❌ Not collected | ✅ N/A |
| **Criminal behavior** | Section 32 — requires explicit consent | ❌ Not collected | ✅ N/A |
| **Trade union membership** | Section 28 — requires explicit consent | ❌ Not collected | ✅ N/A |

### 4.2 Voice Data as Biometric

**Key issue:** POPIA may classify voice data as biometric information (Section 26(1)). This requires:

| Requirement | Implementation | Status |
|------------|---------------|--------|
| Explicit consent | Separate opt-in during onboarding | ⬜ TODO |
| Purpose limitation | Dialect improvement only | ✅ Design |
| No secondary use | Voice data not used for identification | ✅ Design |
| Deletion right | User can delete voice data independently | ⬜ TODO |

---

## 5. CROSS-BORDER TRANSFERS (POPIA)

### 5.1 Section 72 — Transfer Restrictions

| Rule | Angavu Compliance |
|------|-------------------|
| Recipient country must have adequate data protection | ✅ On-device = no transfer |
| Binding corporate rules | ✅ Not needed — no transfer |
| Explicit consent for transfer | ✅ Not needed — no transfer |
| Contractual necessity | ✅ Not needed — no transfer |

### 5.2 Transfer Assessment

| Scenario | Personal Data? | Transfer Occurs? | Safeguard |
|---------|---------------|-----------------|-----------|
| Federated learning gradients | No (anonymized) | No | None needed |
| Model updates | No | No | None needed |
| Angavu Pulse aggregates | No (k≥5) | No | None needed |
| Support tickets | Potentially | Yes (if support offshore) | ⬜ Localize SA support |

---

## 6. PAIA COMPLIANCE (PROMOTION OF ACCESS TO INFORMATION ACT)

### 6.1 Section 51 Manual

| Requirement | Status | Action |
|------------|--------|--------|
| Prepare PAIA Manual | ⬜ TODO | Draft before SA operations |
| Submit to Information Regulator | ⬜ TODO | File upon registration |
| Make publicly available | ⬜ TODO | Publish on website |
| Include: categories of data, purpose, recipients, rights | ⬜ TODO | Use template |

---

## 7. BREACH NOTIFICATION (POPIA)

### 7.1 Section 22 — Security Compromise

| Requirement | Timeline | Implementation | Status |
|------------|----------|----------------|--------|
| Notify Information Regulator | As soon as reasonably possible | ⬜ TODO | Pipeline needed |
| Notify data subjects | As soon as reasonably possible | ⬜ TODO | Notification system |
| Written notification | Must include nature of compromise | ⬜ TODO | Template |
| Sufficient information | Enable protective measures | ⬜ TODO | Checklist |

### 7.2 Notification Content

| Required Information | Notes |
|---------------------|-------|
| Description of compromise | What happened |
| Type of information compromised | Categories of data |
| What Angavu has done | Remedial actions |
| What data subjects should do | Protective measures |
| Contact details | DPO / support contact |

---

## 8. PENALTIES & ENFORCEMENT

### 8.1 POPIA Penalty Framework

| Violation | Maximum Penalty |
|-----------|----------------|
| Failure to comply with enforcement notice | Fine or imprisonment up to 10 years |
| Obstruction of Regulator | Fine or imprisonment up to 10 years |
| Offences under Section 100-109 | Fine or imprisonment up to 10 years |
| Administrative fine | Up to R10 million per violation |

### 8.2 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Registration failure | Low | High (R10M) | Register before processing |
| Section 71 violation (automated decisions) | Low (advisory) | High | Advisory positioning; human-in-the-loop for Phase 3 |
| Breach notification failure | Low | Very High (imprisonment) | Breach pipeline built before operations |
| PAIA manual missing | Low | Medium | Draft before launch |
| Special information processing | Medium | High | Specific consent flows for voice and tithe data |

---

## 9. IMPLEMENTATION TIMELINE

| Phase | Timeline | Actions |
|-------|----------|---------|
| **Pre-SA (Now)** | Months 0-6 | Legal review; draft PAIA manual; design consent flows |
| **Registration** | Before processing | Information Officer registration; PAIA manual filing |
| **Localization** | Months 0-3 of operations | SA-specific privacy policy; consent in local languages (Zulu, Xhosa, Afrikaans) |
| **Compliance** | Months 3-6 of operations | Data subject rights; breach notification pipeline; security review |
| **Section 71 Prep** | Before Phase 3 | Human-in-the-loop framework for Alama Score lender integration |

---

## 10. SOUTH AFRICA-SPECIFIC CONSIDERATIONS

### 10.1 Languages for Consent

| Language | Speakers | Priority |
|----------|----------|----------|
| isiZulu | 12M+ (KwaZulu-Natal, Gauteng) | **Critical** |
| isiXhosa | 8M+ (Eastern Cape, Western Cape) | **Critical** |
| Afrikaans | 7M+ (Western Cape, Northern Cape) | **High** |
| Sesotho | 4M+ (Free State, Gauteng) | **High** |
| English | Official language | **Required** |
| Setswana | 4M+ (North West, Gauteng) | Medium |
| Sepedi | 4M+ (Limpopo, Gauteng) | Medium |

### 10.2 Sector-Specific Considerations

| Sector | POPIA Note |
|--------|-----------|
| Financial services (Alama Score) | Additional oversight from FSCA if credit-related |
| Agriculture (domain agents) | Sector-specific processing norms may apply |
| Employment (worker income) | Labour Relations Act considerations |

---

*This checklist is maintained by Angavu Intelligence. Review quarterly against Information Regulator guidance updates.*

**Angavu Intelligence © 2026**
