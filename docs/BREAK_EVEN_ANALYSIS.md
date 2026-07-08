# Break-Even Analysis — Angavu Intelligence

**Date:** July 2026
**Key Finding:** Break-even is a function of B2B client count, NOT worker count.

---

## The Core Insight

Angavu's revenue comes from B2B intelligence products (FMCG, banks, government, NGOs). Workers use Msaidizi for free. Therefore:

> **50,000 workers with zero B2B clients = bankruptcy.**
> **1,000 workers with 10 enterprise clients = profitable.**

Worker count matters for the data moat and long-term defensibility, but break-even is determined entirely by enterprise sales.

---

## Cost Structure

### Monthly Operating Costs (at Scale)

| Cost Category | Phase 1 (0-1K workers) | Phase 2 (1K-10K) | Phase 3 (10K-50K) |
|---------------|----------------------|------------------|-------------------|
| Infrastructure (ARM servers) | $0 (Oracle free tier) | $120 | $400-$1,000 |
| WhatsApp Business API | $0 (OpenWA) | $500-$2,500 | $2,500-$15,000 |
| Cloud fallback inference | $0 (free tier) | $50-$250 | $250-$1,000 |
| Staff (engineering, sales, support) | $5,000-$10,000 | $10,000-$20,000 | $15,000-$30,000 |
| Legal & compliance | $500-$1,000 | $1,000-$2,000 | $1,000-$2,000 |
| Marketing & user acquisition | $1,000-$3,000 | $2,000-$5,000 | $2,000-$5,000 |
| **Total Monthly** | **$6,500-$14,000** | **$13,670-$29,870** | **$21,150-$53,000** |
| **Total Annual** | **$78K-$168K** | **$164K-$358K** | **$254K-$636K** |

### Revenue Per B2B Client (Monthly Average)

| Client Type | Monthly Revenue | Mix Weight |
|-------------|----------------|------------|
| FMCG (Soko Pulse) | $4,000-$8,000 | 30% |
| Bank/MFI (Alama Score) | $3,000-$10,000 | 25% |
| Government (Tax Base, Pulse) | $2,000-$5,000 | 20% |
| NGO (Jamii Insights) | $1,500-$4,000 | 15% |
| Other (Distribution, Insurance) | $2,000-$6,000 | 10% |
| **Weighted Average** | **$3,200-$7,400** | |

---

## Break-Even Scenarios

### Scenario A: Conservative (High Costs, Low Revenue)

| Parameter | Value |
|-----------|-------|
| Monthly costs | $53,000 |
| Revenue per B2B client | $3,200/mo |
| Break-even clients | 53,000 / 3,200 = **17 clients** |
| Timeline | Month 24-30 |

### Scenario B: Optimistic (Low Costs, High Revenue)

| Parameter | Value |
|-----------|-------|
| Monthly costs | $21,000 |
| Revenue per B2B client | $7,400/mo |
| Break-even clients | 21,000 / 7,400 = **3 clients** |
| Timeline | Month 12-15 |

### Scenario C: Realistic (Most Likely)

| Parameter | Value |
|-----------|-------|
| Monthly costs | $35,000 |
| Revenue per B2B client | $5,000/mo |
| Break-even clients | 35,000 / 5,000 = **7 clients** |
| Timeline | Month 18-24 |

---

## Revenue Projections (Corrected)

### Year 1: $90K-$260K (Not $1.18M)

| Quarter | B2B Clients | Quarterly Revenue | Cumulative |
|---------|-------------|-------------------|------------|
| Q1 | 0-1 | $0-$15K | $0-$15K |
| Q2 | 1-2 | $10K-$40K | $10K-$55K |
| Q3 | 2-3 | $25K-$75K | $35K-$130K |
| Q4 | 3-5 | $35K-$100K | $70K-$230K |
| **Year 1 Total** | **3-5** | | **$90K-$260K** |

**Why not $1.18M:** B2B data product sales in Africa take 6-18 months per client. The sales cycle includes:
- Discovery (1-2 months)
- Pilot (2-3 months)
- Procurement (2-4 months)
- Onboarding (1-2 months)

Getting 15+ clients in Year 1 requires an enterprise sales team Angavu doesn't have yet.

### Year 2: $400K-$1.2M

| Quarter | B2B Clients | Quarterly Revenue |
|---------|-------------|-------------------|
| Q1 | 5-8 | $50K-$150K |
| Q2 | 7-10 | $75K-$200K |
| Q3 | 8-12 | $100K-$250K |
| Q4 | 10-15 | $100K-$300K |
| **Year 2 Total** | **10-15** | **$400K-$1.2M** |

### Year 3: $1.5M-$4M

- 20-40 B2B clients
- Mix shifts toward enterprise contracts ($10K+/mo)
- Government procurement begins (12-18 month cycles pay off)
- Pan-African expansion adds Nigeria, Tanzania revenue

---

## The Break-Even Equation

```
Break-Even = Monthly Operating Costs / Average Revenue Per B2B Client

Realistic: $35,000 / $5,000 = 7 enterprise clients
```

**What this means for strategy:**
1. **Focus on B2B sales, not user acquisition.** Users are the data source; clients are the revenue source.
2. **Target FMCG and banks first.** They have the fastest procurement cycles (3-6 months vs. 12-18 for government).
3. **Keep costs low.** Every $10K in monthly costs requires 2 more B2B clients to break even.
4. **The worker base IS the sales pitch.** "We have 50,000 workers generating real-time economic data" is what sells Soko Pulse to FMCG companies.

---

## Unit Economics Per User

### Cost Per Worker (at 50,000 workers)

| Component | Cost/Worker/Month |
|-----------|------------------|
| On-device inference | $0.00 |
| Cloud fallback | $0.005-$0.02 |
| Backend infrastructure | $0.005-$0.01 |
| WhatsApp (if used) | $0.00-$0.05 |
| **Total** | **$0.01-$0.08** |

### Revenue Per Worker (Indirect)

Workers don't pay. But each worker generates data worth:
- ~$0.50-$2.00/year in B2B intelligence product value (at 50,000 workers)
- ~$2.00-$8.00/year at scale (500,000+ workers)

**The math:** It costs $0.12-$0.96/year to serve a worker. Each worker generates $0.50-$8.00/year in indirect B2B revenue. The unit economics work — but only if there are B2B clients to monetize the data.

---

*Break-even at 7-15 B2B clients. Everything else is a means to that end.*

**Angavu Intelligence © 2026**
