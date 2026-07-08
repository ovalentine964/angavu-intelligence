# Product Inventory — What Actually Exists

**Date:** July 2026
**Verdict:** 6 implemented backend products serving 4 worker-facing brands

---

## Honest Product Count

The "43 data products" claim is marketing, not engineering. After code review, here is what actually exists:

### Implemented Backend Products (6 — with code)

| # | Product | Code File | Status | Buyer | Price |
|---|---------|-----------|--------|-------|-------|
| 1 | **Soko Pulse** | `soko_pulse.py` | ✅ Beta | FMCG companies | $2,000-$12,000/mo |
| 2 | **Alama Score** | `alama_score.py` | ✅ Beta | Banks, MFIs | $0.05-$0.50/query |
| 3 | **Biashara Pulse** | `biashara_pulse.py` | ✅ Beta | (Worker-facing) | Free (loss leader) |
| 4 | **Jamii Insights** | `jamii_insights.py` | ✅ Beta | NGOs, dev orgs | $2,000-$10,000/study |
| 5 | **Tax Base Mapping** | `tax_base.py` | ✅ Built | Government (KRA) | $1,500-$10,000/mo |
| 6 | **Distribution Gap** | `distribution_gap.py` | ✅ Built | FMCG companies | $15,000-$30,000 one-time |

### Worker-Facing Brands (4 — compose the 6 products)

| Brand | Products Used | Status |
|-------|--------------|--------|
| **Msaidizi** (AI CFO) | Biashara Pulse + voice interface | ✅ In development |
| **Soko Pulse** (Market Intelligence) | Soko Pulse | ✅ Beta |
| **Alama Score** (Financial Readiness) | Alama Score | ✅ Beta |
| **Jamii Insights** (Inclusion Metrics) | Jamii Insights | ✅ Beta |

### Derived Data Products (~15 — computed, not independently sellable)

These are OUTPUTS of the 6 implemented products, not separate products:
- Price indices (from Soko Pulse)
- Demand forecasts (from Soko Pulse)
- Credit readiness scores (from Alama Score)
- Financial health reports (from Biashara Pulse)
- Inclusion metrics (from Jamii Insights)
- Tax gap estimates (from Tax Base)
- Route optimization data (from Distribution Gap)
- ...and ~8 more computed outputs

**These are NOT independently sellable products. They are features of the 6 core products.**

### Aspirational Products (6 — no code exists)

| Product | Description | Code Status |
|---------|-------------|-------------|
| Afya Pulse | Health economics | ❌ No code |
| Shamba Intelligence | Agricultural optimization | ❌ No code (domain agent exists, no standalone product) |
| Safari Intelligence | Transport economics | ❌ No code |
| Elimu Intelligence | Education economics | ❌ No code |
| Bima Intelligence | Insurance economics | ❌ No code |
| Akiba Pulse | Savings optimization | ❌ No code |

### Training Data Byproducts (5 — not revenue products)

These are generated as side effects of usage, not sold:
- Voice data (dialect model training)
- Transaction data (behavioral patterns)
- Market data (price signals)
- Behavioral data (usage patterns)
- Social data (network effects)

**These are the moat, not the product. They are not sold — they train the AI.**

---

## Summary

| Category | Count | Revenue Potential |
|----------|-------|-------------------|
| Implemented backend products | **6** | Primary B2B revenue |
| Worker-facing brands | **4** | Consumer engagement |
| Derived data outputs | ~15 | Features, not products |
| Aspirational products | **6** | Future roadmap |
| Training byproducts | **5** | The moat (not sold) |
| **Honest total** | **6 products, 4 brands** | |

**Do not claim 43. Claim 6 implemented products serving 4 brands, with 6 more on the roadmap.**

---

*Accuracy > Aspiration. Ship what exists, roadmap what's planned.*
