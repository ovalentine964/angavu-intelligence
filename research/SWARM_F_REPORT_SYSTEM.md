# Swarm F2: Report System Design — Msaidizi Financial Reports

**Classification:** Internal — Product Specification
**Date:** July 7, 2026
**Prepared by:** Swarm F2 — Report System Design Team
**Status:** Definitive

---

## Executive Summary

Msaidizi reports are the **visible proof** that informal work is real business. Every day at 7 PM, a mama mboga in Nairobi receives a WhatsApp message showing her revenue, expenses, profit, and one actionable insight — formatted like an M-Pesa confirmation but richer. She didn't fill a spreadsheet. She didn't visit an accountant. She just talked to Msaidizi, and Msaidizi listened.

This document defines exactly what each of 10 worker types sees, at each of 5 report frequencies, on both delivery channels (WhatsApp: online, polished, with charts; Msaidizi App: offline, text-only). It specifies the data tracked, metrics computed, reports rendered, and the academic foundations that make each component defensible.

**Design Principles:**
1. **M-Pesa Familiarity** — Every report feels like a transaction confirmation the worker already trusts
2. **One Glance Suffices** — The daily report must be understood in under 10 seconds
3. **Actionable, Not Informational** — Every report ends with one clear "do this next" instruction
4. **Bank-Ready** — Monthly and longer reports are formatted for presentation to MFIs, banks, and SACCOs
5. **Offline-First** — Msaidizi App reports work without internet; WhatsApp reports are the premium layer

---

## Part I: Worker Type Data Models

Each worker type has a distinct business model. Msaidizi must track the right data for each.

---

### 1. Mama Mboga (Greengrocer)

**Profile:** Sells fresh vegetables (sukuma wiki, nyanya, vitunguu, mboga) from a roadside stall or market stall. Daily inventory cycles. Perishable goods. Single operator or with one helper.

**Daily Data Tracked:**
- Items purchased (name, quantity, unit price, supplier)
- Items sold (name, quantity, unit price, channel)
- Unsold/spoiled inventory (name, quantity, reason)
- Transport costs (to market, to supplier)
- Stall/market fees (daily levy, security)
- Mobile money received (M-Pesa, Airtel Money)
- Cash on hand at start and end of day

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Gross Margin % | (Revenue - COGS) / Revenue × 100 | Spoilage eats margins; tracks waste |
| Spoilage Rate | Spoiled Qty / Total Purchased Qty × 100 | Perishable-specific; drives buying decisions |
| Revenue per Product | Σ(price × qty) per item | Identifies best sellers |
| Daily Profit | Revenue - All Expenses | The number that matters |
| Inventory Turnover | Items Sold / Avg Inventory | Fresh stock = happy customers |

**Report Content:**
- **Daily:** Revenue by product (Tomatoes KSh 1,800, Sukuma KSh 1,200...), total expenses, net profit, spoilage alert, tomorrow's buying suggestion
- **Weekly:** Best/worst selling products, margin trends, supplier price comparison, spoilage reduction tips
- **Monthly:** Cash flow statement, income statement, Alama Score, product mix chart, seasonal buying guide
- **6-Month:** Seasonal demand patterns (e.g., sukuma peaks in rainy season), growth trajectory, credit readiness
- **Yearly:** Annual income statement, tax-ready summary, business valuation, goal review

---

### 2. Boda Boda (Motorcycle Taxi)

**Profile:** Motorcycle taxi operator. Revenue from passenger fares and parcel delivery. Variable fuel costs, maintenance, licensing. May own or lease the motorcycle.

**Daily Data Tracked:**
- Trips completed (count, fare per trip, route)
- Fuel purchased (liters, price per liter, station)
- Parcel deliveries (count, fee per delivery)
- Maintenance/repairs (type, cost, mechanic)
- Daily license/insurance amortization
- M-Pesa receipts from customers
- Cash fares collected

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Revenue per Trip | Total Revenue / Trip Count | Efficiency indicator |
| Fuel Cost % | Fuel Cost / Revenue × 100 | Biggest variable cost |
| Trips per Day | Count of completed trips | Productivity measure |
| Net Daily Income | Revenue - Fuel - Maintenance - Fees | Take-home pay |
| Cost per Kilometer | Total Costs / Estimated KM | Route optimization |

**Report Content:**
- **Daily:** Trips today (X), total revenue, fuel cost, net income, comparison vs yesterday, best earning hour
- **Weekly:** Daily breakdown, fuel efficiency trend, busiest days, maintenance schedule reminder
- **Monthly:** Cash flow, income statement, Alama Score, trip volume chart, earnings trend
- **6-Month:** Seasonal demand (rain = fewer trips, more per trip), maintenance cost trajectory, credit readiness
- **Yearly:** Annual summary, total kilometers, maintenance history, business valuation

---

### 3. Jua Kali (Artisan/Craftsperson)

**Profile:** Informal metalworker, carpenter, mechanic, tailor, or other tradesperson. Project-based work with variable timelines. Materials purchased per job. May have apprentices.

**Daily Data Tracked:**
- Jobs completed (description, client, amount charged)
- Materials purchased (item, quantity, price, supplier)
- Labor costs (apprentice wages, if any)
- Tools/equipment purchases or repairs
- Deposits received (M-Pesa, cash)
- Outstanding balances (credit given to clients)

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Job Profitability | Revenue - Materials - Labor per job | Not all jobs are equal |
| Material Cost % | Materials / Revenue × 100 | Material-intensive work needs tracking |
| Average Job Value | Total Revenue / Job Count | Pricing benchmark |
| Outstanding Receivables | Σ(unpaid client balances) | Cash flow risk |
| Utilization Rate | Working Days / Available Days × 100 | Capacity insight |

**Report Content:**
- **Daily:** Jobs completed, revenue, material costs, net profit, outstanding balances, next day schedule
- **Weekly:** Job profitability ranking, material cost trends, receivables aging, busiest job types
- **Monthly:** Cash flow, income statement, Alama Score, job type mix, receivables chart
- **6-Month:** Seasonal patterns (construction peaks, rainy slowdowns), skill demand trends, credit readiness
- **Yearly:** Annual summary, job history, material cost analysis, business valuation

---

### 4. Mitumba Seller (Secondhand Clothing)

**Profile:** Sells secondhand clothes (mitumba) from market stalls or by the roadside. Buys bales from wholesale markets. Seasonal and fashion-driven inventory.

**Daily Data Tracked:**
- Bales purchased (type, weight, price, source)
- Items sold (category, price, channel)
- Unsold inventory (aging stock)
- Market/stall fees
- Transport costs (bale pickup, market trips)
- M-Pesa and cash receipts

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Bale Yield | Revenue per Bale / Bale Cost | Bale quality varies wildly |
| Sell-Through Rate | Items Sold / Items in Stock × 100 | Dead stock = dead money |
| Average Selling Price | Revenue / Items Sold | Pricing power |
| Inventory Aging | Days since last sale per item | Discount or discard decision |
| Category Mix % | Revenue by category / Total | Dresses vs shirts vs jeans |

**Report Content:**
- **Daily:** Items sold, revenue, bale cost allocation, net profit, slow-moving items alert
- **Weekly:** Bale yield analysis, category performance, pricing suggestions, market fee tracking
- **Monthly:** Cash flow, income statement, Alama Score, category mix chart, seasonal trends
- **6-Month:** Fashion cycle patterns, best-performing categories, bale source comparison, credit readiness
- **Yearly:** Annual summary, inventory turnover analysis, business valuation

---

### 5. Food Vendor (Mama Ntilie / Chips Seller)

**Profile:** Cooks and sells prepared food — chips, chapati, mandazi, nyama choma, or full meals. Daily ingredient purchases. Location-dependent (roadside, market, estate).

**Daily Data Tracked:**
- Meals/portions sold (type, quantity, price)
- Ingredients purchased (item, quantity, price)
- Cooking fuel (charcoal, gas, firewood — quantity, cost)
- Packaging costs (plates, bags, serviettes)
- Water/utilities
- Location fees (if any)
- M-Pesa and cash receipts

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Food Cost % | Ingredients / Revenue × 100 | Industry standard: 30-40% |
| Revenue per Portion | Total Revenue / Portions Sold | Pricing benchmark |
| Fuel Cost % | Fuel / Revenue × 100 | Second-largest cost |
| Daily Portions | Count of portions sold | Volume driver |
| Waste Rate | Unused ingredients / Purchased × 100 | Over-preparation loss |

**Report Content:**
- **Daily:** Portions sold, revenue, ingredient costs, fuel cost, net profit, best-selling item, tomorrow's prep suggestion
- **Weekly:** Daily breakdown, food cost trend, portion volume trend, busiest days, ingredient price changes
- **Monthly:** Cash flow, income statement, Alama Score, menu mix chart, cost trend
- **6-Month:** Seasonal demand (Ramadan, holidays), ingredient price patterns, credit readiness
- **Yearly:** Annual summary, menu profitability ranking, business valuation

---

### 6. Shopkeeper (Duka Owner)

**Profile:** Runs a small retail shop (duka) selling household goods, groceries, airtime, and sundries. Manages inventory across multiple product categories. May extend credit to trusted customers.

**Daily Data Tracked:**
- Sales by category (groceries, airtime, household, drinks, etc.)
- Stock purchased (item, quantity, price, supplier)
- Credit given to customers (name, amount, item)
- Credit repayments received
- Rent, utilities, staff wages
- M-Pesa till receipts and cash

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Gross Margin % | (Revenue - COGS) / Revenue × 100 | Retail margin benchmark |
| Customer Credit Outstanding | Σ(unpaid balances) | Cash flow risk |
| Sales per Category | Revenue by category | Inventory optimization |
| Stock Turnover | COGS / Avg Inventory | Dead stock detection |
| Daily Footfall Estimate | Transactions / Operating Hours | Customer traffic proxy |

**Report Content:**
- **Daily:** Total sales, category breakdown, stock purchased, expenses, net profit, credit alerts, reorder suggestions
- **Weekly:** Category performance, credit collection rate, stock turnover, margin trends
- **Monthly:** Cash flow, income statement, Alama Score, category pie chart, credit aging report
- **6-Month:** Seasonal product demand, supplier cost trends, credit recovery patterns, credit readiness
- **Yearly:** Annual summary, category profitability, customer credit history, business valuation

---

### 7. Hairdresser / Barber

**Profile:** Provides hairdressing, braiding, barbering, or beauty services. Revenue from service fees and product sales. May rent a chair or own a salon. Appointments and walk-ins.

**Daily Data Tracked:**
- Services provided (type, price, client)
- Products sold (hair products, cosmetics — item, price)
- Supplies consumed (chemicals, extensions, combs)
- Salon/chair rent
- Utilities (water, electricity)
- M-Pesa and cash receipts

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Revenue per Client | Total Revenue / Client Count | Service pricing benchmark |
| Service Mix % | Revenue by service type | Identifies high-value services |
| Supply Cost % | Supplies / Revenue × 100 | Consumable tracking |
| Clients per Day | Total clients served | Capacity utilization |
| Product vs Service Ratio | Product Sales / Total Revenue × 100 | Upselling effectiveness |

**Report Content:**
- **Daily:** Clients served, revenue (services + products), supply costs, net profit, busiest hours, top service
- **Weekly:** Daily breakdown, service mix, client count trend, supply cost trend, product sales
- **Monthly:** Cash flow, income statement, Alama Score, service mix chart, client volume trend
- **6-Month:** Seasonal patterns (holidays, weddings), service demand trends, credit readiness
- **Yearly:** Annual summary, client retention estimate, service profitability, business valuation

---

### 8. Farmer

**Profile:** Smallholder farmer growing crops or raising livestock. Seasonal income cycles. Inputs (seeds, fertilizer, feed) are upfront costs. Revenue comes at harvest or sale.

**Daily Data Tracked:**
- Crops planted/harvested (type, quantity, area)
- Inputs purchased (seeds, fertilizer, pesticide, feed)
- Produce sold (type, quantity, price, buyer)
- Transport to market
- Labor costs (casual workers)
- Rainfall/weather observations (voice-reported)
- M-Pesa and cash receipts

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Yield per Acre | Harvest Quantity / Planted Area | Productivity measure |
| Input Cost per Acre | Total Inputs / Area | Cost efficiency |
| Price at Sale vs Market | Sale Price / Market Average | Middleman detection |
| Cost of Production | Total Costs / Harvest Quantity | Profitability per unit |
| Post-Harvest Loss | Lost Quantity / Harvested × 100 | Storage/logistics gap |

**Report Content:**
- **Daily:** Activity log (planted, harvested, sold), expenses, revenue if any, weather advisory, input suggestions
- **Weekly:** Input cost tracking, labor cost tracking, market price comparison, activity summary
- **Monthly:** Cash flow (aligned to harvest cycles), income statement, Alama Score, input cost chart, yield tracking
- **6-Month:** Seasonal yield patterns, input cost trends, market price history, credit readiness (aligned to planting/harvest)
- **Yearly:** Annual summary, yield per acre history, input cost analysis, business valuation, next season planning

---

### 9. Construction Worker (Fundis / Laborer)

**Profile:** Casual or semi-permanent construction worker. Daily wages or project-based. Income is irregular — depends on available work. May be mason, carpenter, plumber, electrician, or general laborer.

**Daily Data Tracked:**
- Work completed (site, hours, wage received)
- Skills used (masonry, plumbing, carpentry, etc.)
- Transport costs (to/from site)
- Tools purchased or maintained
- Protective equipment
- M-Pesa and cash receipts

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Daily Wage | Total Earnings / Days Worked | Income benchmark |
| Working Days per Month | Days with paid work | Employment stability |
| Skill Premium | Wage by skill type | Highest-value skill |
| Transport Cost % | Transport / Earnings × 100 | Net income impact |
| Earnings Stability | Std Dev of Daily Wages / Mean | Income predictability |

**Report Content:**
- **Daily:** Site worked, hours, wage, transport cost, net income, comparison vs yesterday, skill used
- **Weekly:** Days worked, total earnings, transport costs, net income, busiest skills, earnings trend
- **Monthly:** Cash flow, income statement, Alama Score, working days chart, skill premium analysis
- **6-Month:** Seasonal patterns (rain delays, holiday slowdowns), skill demand trends, credit readiness
- **Yearly:** Annual summary, days worked, total earnings, skill development tracking, business valuation

---

### 10. Market Trader (Groceries, Wholesale, Mixed Goods)

**Profile:** Operates in an open-air market. Sells groceries, household goods, or mixed merchandise. Higher volume than mama mboga. May have a stall with rent. May employ one or two assistants.

**Daily Data Tracked:**
- Items sold (name, quantity, unit price)
- Stock purchased (item, quantity, price, supplier)
- Stall rent and market fees
- Assistant wages
- Transport (stock pickup, market trips)
- Storage costs (if perishable)
- M-Pesa till and cash receipts
- Credit given to customers

**Key Metrics:**
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Daily Revenue | Σ(price × qty) | Top line |
| Gross Margin % | (Revenue - COGS) / Revenue × 100 | Margin health |
| Revenue per Assistant | Revenue / Staff Count | Labor productivity |
| Credit Outstanding | Σ(unpaid customer balances) | Cash flow risk |
| Supplier Concentration | Top Supplier Spend / Total Spend × 100 | Diversification risk |

**Report Content:**
- **Daily:** Revenue, expenses (stock, rent, wages, transport), net profit, credit alerts, top products, restock suggestions
- **Weekly:** Daily breakdown, margin trends, credit collection rate, supplier price comparison, assistant productivity
- **Monthly:** Cash flow, income statement, Alama Score, product mix chart, credit aging report
- **6-Month:** Seasonal demand patterns, supplier cost trends, growth trajectory, credit readiness
- **Yearly:** Annual summary, product profitability ranking, business valuation, goal review

---

## Part II: Report Frequencies — Full Specifications

### 2.1 Daily Report (7:00 PM)

**Delivery:** WhatsApp (primary) + Msaidizi App (offline fallback)
**Trigger:** Automatic, daily at 19:00 local time
**Purpose:** End-of-day financial summary with one actionable insight
**Reading Time Target:** < 10 seconds

#### WhatsApp Format (Online, Polished)

```
📊 *MSAIDIZI — Daily Report*
📅 Tuesday, 7 July 2026

💰 *MONEY IN*
Sales: KSh 4,500
  ├─ Tomatoes: KSh 1,800 (12kg × 150)
  ├─ Sukuma Wiki: KSh 1,200 (20 bunches × 60)
  └─ Onions: KSh 1,500 (10kg × 150)

💸 *MONEY OUT*
Stock: KSh 2,000
Transport: KSh 200
Market Fee: KSh 100
Total Out: KSh 2,300

✅ *PROFIT TODAY: KSh 2,200*
📈 Yesterday: KSh 1,800 (+22%)

💡 *INSIGHT:* Tomatoes sold 20% faster than yesterday. Buy 15kg tomorrow — demand is rising.

🔥 *STREAK:* 12 days without loss!

🏆 *ALAMA SCORE:* Building (65/100)

_Reply "details" for breakdown. Reply "help" for Msaidizi._
```

#### Msaidizi App Format (Offline, Text)

```
MSAIDIZI — Daily Report
Tue, 7 Jul 2026

IN: Sales KSh 4,500
  Tomatoes KSh 1,800
  Sukuma KSh 1,200
  Onions KSh 1,500

OUT: KSh 2,300
  Stock KSh 2,000
  Transport KSh 200
  Market Fee KSh 100

PROFIT: KSh 2,200 (vs yesterday KSh 1,800, +22%)

INSIGHT: Tomatoes selling faster. Buy 15kg tomorrow.

STREAK: 12 days without loss
ALAMA: 65/100
```

#### Voice Report (Audio Summary)

Delivered as a 30-second voice note in the worker's language:

> "Habari za jioni! Leo umefanya vizuri. Umepata faida ya elfu mbilia na mia mbili. Nyanya zinazidi kuuza — kesho nunua kilo kumi na tano. Streak yako ni siku kumi na mbili bila hasara! Alama yako ni sitini na tano. Usiku mwema!"

#### Gamification System

| Element | Description | Trigger |
|---------|-------------|---------|
| 🔥 Streak | Consecutive profitable days | 3+ days |
| ⭐ Star Day | Best profit day of the week | Highest weekly profit |
| 🏆 Milestone | Achievement badges | First week, First month, 100 transactions |
| 📈 Growth | Positive trend indicator | Profit > 7-day average |
| 💪 Consistency | Regular reporting streak | 5+ consecutive days of data |

#### Data Flow

```
Worker speaks → Voice Pipeline → NLU Extraction → Transaction DB
    → At 19:00: Aggregation Engine reads today's transactions
    → Computes: revenue, expenses, profit, comparison, insight
    → Checks: streak, Alama Score update
    → Renders: WhatsApp template OR App text template
    → Delivers: WhatsApp API OR in-app notification
```

---

### 2.2 Weekly Report (Monday 8:00 AM)

**Delivery:** WhatsApp + Msaidizi App
**Trigger:** Automatic, Monday at 08:00 local time
**Purpose:** Week-in-review with trends, patterns, and recommendations
**Reading Time Target:** < 30 seconds

#### WhatsApp Format

```
📊 *MSAIDIZI — Weekly Report*
📅 Week of 30 Jun – 6 Jul 2026

💰 *WEEK SUMMARY*
Total Revenue: KSh 28,500
Total Expenses: KSh 16,200
Total Profit: KSh 12,300
Best Day: Friday (KSh 4,200 profit)
Worst Day: Monday (KSh 1,100 profit)

📈 *TRENDS*
Revenue: ↑ 8% vs last week
Expenses: ↓ 3% vs last week
Profit: ↑ 15% vs last week

📊 *TOP PRODUCTS*
1. Tomatoes — KSh 8,400 (29%)
2. Onions — KSh 6,300 (22%)
3. Sukuma Wiki — KSh 5,100 (18%)

💡 *RECOMMENDATIONS*
• Tomatoes are your star product — keep stock high
• Monday is consistently slow — consider promotions
• Transport costs down — you found a good route

🏥 *BUSINESS HEALTH SCORE: 72/100*
✅ Profitable 7/7 days
✅ Growing revenue
⚠️ Product mix could diversify

🏆 *ALAMA SCORE: 67/100* (+2 from last week)

_Reply "details" for daily breakdown._
```

#### Msaidizi App Format (Offline)

```
MSAIDIZI — Weekly Report
30 Jun - 6 Jul 2026

Revenue: KSh 28,500
Expenses: KSh 16,200
Profit: KSh 12,300

Best Day: Fri (KSh 4,200)
Worst Day: Mon (KSh 1,100)

Revenue vs last week: +8%
Profit vs last week: +15%

Top: Tomatoes (29%), Onions (22%), Sukuma (18%)

Tips:
- Stock more tomatoes
- Monday is slow — try promotions
- Transport costs improving

Health Score: 72/100
Alama Score: 67/100 (+2)
```

#### Business Health Score Components

| Component | Weight | Calculation | Source |
|-----------|--------|-------------|--------|
| Profitability | 30% | Profitable days / Total days × 100 | ECO 201 |
| Growth | 25% | Revenue trend vs 4-week average | STA 244 |
| Consistency | 20% | 1 - (Std Dev / Mean) of daily profit | STA 341 |
| Diversification | 15% | 1 - Herfindahl Index of product mix | ECO 101 |
| Efficiency | 10% | Expenses / Revenue ratio trend | ECO 201 |

---

### 2.3 Monthly Report (1st of Month)

**Delivery:** WhatsApp (with chart images) + Msaidizi App (with text tables)
**Trigger:** Automatic, 1st of each month at 08:00
**Purpose:** Comprehensive financial statements + Alama Score update
**Reading Time Target:** < 2 minutes

#### Report Components

**Component 1: Cash Flow Statement (M-Pesa Style)**

This is the flagship. Designed to look and feel like an M-Pesa statement — the one financial document every Kenyan already trusts.

```
📊 *MSAIDIZI — Monthly Cash Flow*
📅 June 2026

━━━━━━━━━━━━━━━━━━━━━
💰 *CASH IN*
━━━━━━━━━━━━━━━━━━━━━
Tomatoes         KSh 38,200
Sukuma Wiki      KSh 22,400
Onions           KSh 19,800
Other Sales      KSh  8,600
━━━━━━━━━━━━━━━━━━━━━
TOTAL IN         KSh 89,000
━━━━━━━━━━━━━━━━━━━━━

💸 *CASH OUT*
━━━━━━━━━━━━━━━━━━━━━
Stock Purchase   KSh 52,000
Transport        KSh  4,800
Market Fees      KSh  3,000
Spoilage/Waste   KSh  2,200
Other Expenses   KSh  1,500
━━━━━━━━━━━━━━━━━━━━━
TOTAL OUT        KSh 63,500
━━━━━━━━━━━━━━━━━━━━━

✅ *NET CASH FLOW: KSh 25,500*
━━━━━━━━━━━━━━━━━━━━━
Opening Balance: KSh  8,000
Closing Balance: KSh 33,500
━━━━━━━━━━━━━━━━━━━━━
```

**Component 2: Income Statement**

```
📊 *INCOME STATEMENT — June 2026*

Revenue                    KSh 89,000
Cost of Goods Sold        (KSh 52,000)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gross Profit               KSh 37,000
Gross Margin                  41.6%

Operating Expenses:
  Transport                KSh  4,800
  Market Fees              KSh  3,000
  Spoilage                 KSh  2,200
  Other                    KSh  1,500
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Operating Expenses   KSh 11,500
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NET PROFIT                 KSh 25,500
Net Margin                    28.7%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Component 3: Alama Score Update**

```
🏆 *ALAMA SCORE — June 2026*
Score: 71/100 (+4 from May)

Breakdown:
  Transaction Regularity    85/100  ✅ Daily records, 28/30 days
  Profit Consistency        72/100  ✅ Profitable 26/30 days
  Growth Trajectory         68/100  ✅ Revenue up 12% vs May
  Diversification           55/100  ⚠️ 65% revenue from 2 products
  Savings Behavior          60/100  ⚠️ Could save more consistently

What This Means:
Your Alama Score qualifies you for:
  ✅ M-Shwari loan limit increase (KSh 5,000 → KSh 8,000)
  ✅ KCB M-Pesa eligibility
  ⚠️ SACCO membership application (needs 75+)

Next Month Target: 75/100
Focus: Diversify products, increase savings frequency
```

**Component 4: Charts (WhatsApp Only)**

Charts delivered as image attachments:

1. **Revenue Bar Chart** — Daily revenue for the month
2. **Expense Pie Chart** — Breakdown of all expenses
3. **Profit Trend Line** — Daily profit with 7-day moving average
4. **Product Mix Donut** — Revenue share by product
5. **Alama Score Trend** — 6-month score progression

Charts are generated server-side using Chart.js and delivered as PNG images via WhatsApp Business API.

#### Bank/Microfinance-Ready Format

The monthly report is designed to be directly presentable to financial institutions. It includes:

- **Transaction Summary:** 30-day count of all recorded transactions
- **Cash Flow Statement:** Formatted per IFRS SME standards (simplified)
- **Income Statement:** Revenue, COGS, expenses, net profit
- **Alama Score:** Proprietary creditworthiness metric with breakdown
- **Business Health Score:** Composite metric from weekly data
- **Peer Comparison:** Anonymous benchmarking against same-sector workers
- **Digital Signature:** Msaidizi watermark + QR code for verification

---

### 2.4 Six-Month Report

**Delivery:** WhatsApp (multi-message with charts) + Msaidizi App
**Trigger:** Automatic, January 1 and July 1 at 08:00
**Purpose:** Growth trajectory, seasonal patterns, credit readiness certification
**Reading Time Target:** < 5 minutes

#### Report Components

**Component 1: Growth Trajectory**

```
📊 *MSAIDIZI — 6-Month Growth Report*
📅 January – June 2026

💰 *FINANCIAL TRAJECTORY*
Revenue Trend:
  Jan: KSh 72,000  ████████░░
  Feb: KSh 68,000  ███████░░░
  Mar: KSh 81,000  █████████░
  Apr: KSh 85,000  █████████░
  May: KSh 82,000  █████████░
  Jun: KSh 89,000  ██████████

6-Month Revenue: KSh 477,000
6-Month Profit:  KSh 128,000
Growth Rate:     +23.6% (Jan → Jun)
Avg Monthly Profit: KSh 21,333

📈 *KEY METRICS TREND*
Daily Revenue (avg):   KSh 2,650 → KSh 2,967 (+12%)
Gross Margin:          38% → 41.6% (+3.6pp)
Working Days/Month:    26 → 28 (+2 days)
Product Categories:    3 → 4 (added onions)
```

**Component 2: Seasonal Patterns (STA 244)**

```
📊 *SEASONAL ANALYSIS*

Your Business Patterns:
┌─────────┬──────────┬──────────┬──────────┐
│ Season  │ Revenue  │ Profit   │ Products │
├─────────┼──────────┼──────────┼──────────┤
│ Jan-Feb │ Medium   │ Medium   │ Tomatoes │
│ Mar-Apr │ High     │ High     │ Tomatoes,│
│         │          │          │ Sukuma   │
│ May-Jun │ Medium   │ Medium   │ Onions   │
│ Jul-Aug │ Low      │ Low      │ Tomatoes │
│ Sep-Oct │ Medium   │ Medium   │ Sukuma   │
│ Nov-Dec │ High     │ High     │ Mixed    │
└─────────┴──────────┴──────────┴──────────┘

Insights:
• March-April is your peak season (planting season drives demand)
• July-August dip is normal (school fees drain customer spending)
• November-December spike = holiday buying
• Stock recommendation: Build inventory in February for March peak

Forecast (Next 6 Months):
  Jul: KSh 78,000 (seasonal dip)
  Aug: KSh 75,000 (lowest month)
  Sep: KSh 80,000 (recovery)
  Oct: KSh 84,000 (building)
  Nov: KSh 92,000 (holiday peak)
  Dec: KSh 95,000 (year-end peak)
```

**Component 3: Credit Readiness Certification (ECO 206)**

```
🏦 *CREDIT READINESS REPORT*
📅 Certification Date: 1 July 2026
Valid Until: 31 December 2026

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATUS: ✅ CREDIT READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Financial History:  6 months continuous records
Transaction Count:  847 verified transactions
Average Monthly Revenue: KSh 79,500
Average Monthly Profit:  KSh 21,333
Profit Margin:           26.8%
Revenue Trend:           Growing (+23.6%)
Alama Score:             71/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ELIGIBLE PRODUCTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ M-Shwari:       Up to KSh 15,000
✅ KCB M-Pesa:     Up to KSh 25,000
✅ Tala:           Up to KSh 20,000
✅ Branch:         Up to KSh 18,000
✅ SACCO Loan:     Eligible to apply
⚠️ Bank SME Loan:  Needs 12 months history

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED LOAN SIZE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Safe Borrowing Limit: KSh 15,000
(Rule: Loan ≤ 1 month average profit)
Repayment Capacity: KSh 5,000/month
(30% of average monthly profit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This report is digitally signed by Msaidizi.
Present this to any MFI, bank, or SACCO.
QR Code: [embedded for verification]
```

**Component 4: Peer Comparison (STA 341)**

```
👥 *PEER COMPARISON — Anonymous*

Your Sector: Fresh Produce Vendors (Nairobi)
Sample Size: 1,247 workers

┌────────────────────┬──────────┬──────────┬──────────┐
│ Metric             │ You      │ Average  │ Top 25%  │
├────────────────────┼──────────┼──────────┼──────────┤
│ Monthly Revenue    │ KSh 89K  │ KSh 62K  │ KSh 95K  │
│ Profit Margin      │ 28.7%    │ 22.1%    │ 31.5%    │
│ Working Days/Month │ 28       │ 24       │ 29       │
│ Product Categories │ 4        │ 3        │ 5        │
│ Alama Score        │ 71       │ 58       │ 78       │
│ Spoilage Rate      │ 2.5%     │ 5.8%     │ 1.5%     │
└────────────────────┴──────────┴──────────┴──────────┘

Your Ranking:
  Revenue:     Top 35% ✅
  Profit:      Top 30% ✅
  Consistency: Top 25% ✅
  Alama Score: Top 40% ⚠️

You're outperforming 65% of similar workers.
Focus: Reduce spoilage to reach Top 25%.
```

---

### 2.5 Yearly Report

**Delivery:** WhatsApp (multi-message with charts) + Msaidizi App + PDF Export
**Trigger:** Automatic, January 1 at 08:00
**Purpose:** Annual summary, tax-ready statements, business valuation, goal review
**Reading Time Target:** < 10 minutes

#### Report Components

**Component 1: Annual Summary**

```
📊 *MSAIDIZI — Annual Business Report*
📅 1 January – 31 December 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 *ANNUAL FINANCIALS*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Revenue:       KSh 948,000
Total Expenses:      KSh 682,500
Total Profit:        KSh 265,500
Average Monthly:     KSh 22,125
Best Month:          December (KSh 31,200)
Worst Month:         August (KSh 14,800)
Working Days:        322/365

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 *YEAR-OVER-YEAR*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Revenue Growth:      +18.5%
Profit Growth:       +24.2%
Margin Improvement:  +1.8pp
Alama Score:         52 → 71 (+19)
Working Days:        +15 days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 *GOALS ACHIEVED*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Daily profit above KSh 500: 89% of days
✅ Alama Score above 60: Achieved in July
✅ 3+ product categories: Achieved in March
⚠️ Monthly savings KSh 5,000: Achieved 8/12 months
❌ Zero spoilage days: 67% of days (target was 80%)
```

**Component 2: Tax-Ready Statement**

```
📊 *TAX-READY INCOME STATEMENT*
📅 Tax Year 2025

For presentation to KRA (Kenya Revenue Authority)
or simplified tax filing under the Turnover Tax regime.

Business Name: [Worker's Business Name]
KRA PIN: [If registered, or "Not yet registered"]
Business Type: Fresh Produce Vendor
Location: [Market Name], Nairobi

GROSS REVENUE:
  Sales Revenue                    KSh 948,000
  Other Income (delivery fees)     KSh   8,400
  ─────────────────────────────────────────────
  TOTAL GROSS REVENUE              KSh 956,400

ALLOWABLE DEDUCTIONS:
  Cost of Goods Sold              KSh 562,500
  Transport                       KSh  57,600
  Market Fees                     KSh  36,000
  Spoilage/Waste                  KSh  26,400
  ─────────────────────────────────────────────
  TOTAL DEDUCTIONS                KSh 682,500

TAXABLE INCOME                    KSh 273,900

TURNOVER TAX (if applicable):
  Rate: 1% of gross revenue
  Tax Due: KSh 9,564

This statement is generated from verified transaction
data recorded through Msaidizi. Digitally signed.
QR Code: [verification link]
```

**Component 3: Business Valuation**

```
📊 *BUSINESS VALUATION*
📅 As at 31 December 2025

Method: Income-Based Approach (Capitalization of Earnings)

Annual Net Profit:         KSh 265,500
Capitalization Rate:       25% (informal sector risk-adjusted)
Business Value:            KSh 1,062,000

Alternative Method: Asset-Based
  Inventory (avg):         KSh  15,000
  Equipment/Tools:         KSh   8,000
  Customer Relationships:  KSh  50,000 (estimated)
  Business Reputation:     KSh  25,000 (Alama Score premium)
  ─────────────────────────────────────────
  Asset Value:             KSh  98,000

Fair Market Range:         KSh 98,000 – KSh 1,062,000
Most Likely Value:         KSh 350,000

Note: This valuation is indicative. For formal valuation,
present this report to a certified valuer.
```

**Component 4: Goal Setting for Next Year**

```
🎯 *2026 GOALS — Msaidizi Recommendation*

Based on your 2025 performance and seasonal patterns:

1. 💰 Increase monthly profit to KSh 25,000
   Current: KSh 22,125 | Target: KSh 25,000 (+13%)
   How: Reduce spoilage, add 1 product category

2. 🏆 Reach Alama Score 80/100
   Current: 71 | Target: 80 (+9 points)
   How: Diversify products, save consistently

3. 📈 Work 340+ days
   Current: 322 | Target: 340 (+18 days)
   How: Reduce sick days, plan for rain delays

4. 💵 Save KSh 5,000/month consistently
   Current: 8/12 months | Target: 12/12 months
   How: Auto-save feature in Msaidizi App

5. 🏦 Qualify for SACCO membership
   Current: Needs 75+ Alama Score
   How: Focus on consistency and diversification

_Reply "accept goals" to track these in Msaidizi._
```

---

## Part III: Academic Framework Integration

Each report component is grounded in economic and statistical theory from Valentine's degree. This ensures the reports are not just useful — they are **academically defensible** for institutional credibility.

### ECO 201: Producer Theory → Cash Flow & Income Statement

**Application:** The cash flow statement and income statement apply producer theory fundamentals — tracking inputs (expenses), outputs (revenue), and the production function (how efficiently the worker converts inputs to outputs).

- **Revenue** = Price × Quantity (demand-side)
- **COGS** = Input costs (supply-side)
- **Profit** = Revenue - Costs (producer surplus)
- **Margin** = Profit / Revenue (efficiency measure)

The daily, weekly, and monthly reports all compute these in real-time, giving the worker a live view of their production function that formal businesses get from accounting software.

### ECO 321: Information Economics → Alama Score

**Application:** The Alama Score is an information economics construct — it solves adverse selection in credit markets by creating a credible signal from the worker's own transaction data.

- **Spence Signaling:** By consistently recording transactions (costly in time, free in money), the worker signals reliability
- **Stiglitz Screening:** The score screens good borrowers from bad using behavioral data, not demographic proxies
- **Akerlof Lemons:** The score prevents the "lemons problem" — reliable workers are no longer pooled with unreliable ones

The score is updated monthly with a breakdown that shows exactly which behaviors drive the score, creating incentive alignment.

### STA 244: Time Series Analysis → Seasonal Patterns

**Application:** The 6-month and yearly reports use time series decomposition to identify:

- **Trend:** Is the business growing, declining, or stable?
- **Seasonality:** What months are high/low? Why?
- **Cyclical:** Are there multi-year patterns?
- **Irregular:** What caused the spikes/dips?

This allows Msaidizi to forecast future revenue, recommend inventory timing, and warn the worker about upcoming slow periods — all from their own historical data.

### ECO 206: Microfinance → Credit Readiness Certification

**Application:** The credit readiness report applies microfinance principles:

- **Character:** Alama Score (behavioral data)
- **Capacity:** Profit margin and revenue trend (ability to repay)
- **Capital:** Savings behavior and inventory value
- **Collateral:** Business asset valuation
- **Conditions:** Seasonal patterns and market conditions

The certification is designed to be accepted by MFIs, banks, and SACCOs as an alternative to traditional credit assessments — solving the collateral-free lending problem for informal workers.

### STA 341: Estimation Theory → Peer Comparison

**Application:** The peer comparison uses statistical estimation to:

- **Estimate population parameters:** What's the average revenue for a mama mboga in Nairobi?
- **Confidence intervals:** How certain are we about the averages?
- **Percentile ranking:** Where does this worker stand relative to peers?
- **Regression analysis:** What factors predict higher earnings?

The comparison is always anonymous and aggregated, using sector, location, and experience as grouping variables. This gives the worker context for their own performance without exposing individual data.

---

## Part IV: Delivery Architecture

### WhatsApp Delivery

```
Report Generation Engine
    │
    ├── Template Engine (per report type)
    │   ├── Daily: Simple text template
    │   ├── Weekly: Text + basic formatting
    │   ├── Monthly: Text + chart images
    │   ├── 6-Month: Multi-message + charts
    │   └── Yearly: Multi-message + charts + PDF link
    │
    ├── Chart Generator (Chart.js server-side)
    │   ├── Bar charts (revenue, expenses)
    │   ├── Line charts (trends, moving averages)
    │   ├── Pie/donut charts (product mix, expenses)
    │   └── Score gauges (Alama Score, Health Score)
    │
    ├── WhatsApp Business API
    │   ├── Text messages (daily, weekly)
    │   ├── Image messages (charts)
    │   ├── Document messages (PDF reports)
    │   └── Template messages (pre-approved formats)
    │
    └── Delivery Tracker
        ├── Sent confirmation
        ├── Read receipt
        └── Reply handler ("details", "help", etc.)
```

### Msaidizi App Delivery (Offline)

```
Report Generation Engine
    │
    ├── Local SQLite Cache
    │   ├── Pre-generated reports (synced when online)
    │   ├── Chart data (rendered natively in-app)
    │   └── PDF exports (downloaded when online)
    │
    ├── In-App Rendering
    │   ├── Text tables (offline-compatible)
    │   ├── Native charts (no internet needed)
    │   └── PDF viewer (cached locally)
    │
    └── Notification System
        ├── Push notification (when online)
        └── Local notification (always)
```

### Voice Delivery

Every report frequency has an optional voice summary:

| Frequency | Voice Length | Content |
|-----------|-------------|---------|
| Daily | 20-30 seconds | Profit, insight, streak |
| Weekly | 45-60 seconds | Week summary, trend, recommendation |
| Monthly | 2-3 minutes | Cash flow highlights, Alama Score, key charts described |
| 6-Month | 3-5 minutes | Growth story, seasonal forecast, credit readiness |
| Yearly | 5-7 minutes | Annual narrative, achievements, goals |

Voice reports are generated using the Msaidizi language pipeline in the worker's preferred language (Swahili, Sheng, Kikuyu, Luo, etc.).

---

## Part V: Report Customization by Worker Type

### Daily Report Variations

| Worker Type | Key Daily Metric | Primary Insight Type | Gamification Focus |
|------------|-----------------|---------------------|-------------------|
| Mama Mboga | Profit by product | Spoilage prevention | Streak (no-loss days) |
| Boda Boda | Revenue per trip | Fuel efficiency | Trip count streak |
| Jua Kali | Job profitability | Material cost control | Jobs completed streak |
| Mitumba Seller | Bale yield | Sell-through rate | Bale yield improvement |
| Food Vendor | Food cost % | Portion optimization | Consistent prep days |
| Shopkeeper | Sales by category | Reorder suggestions | Credit collection streak |
| Hairdresser | Revenue per client | Service mix optimization | Client count streak |
| Farmer | Daily activity | Weather + input advice | Activity consistency |
| Construction Worker | Daily wage | Skill premium | Working days streak |
| Market Trader | Gross margin | Supplier optimization | Margin improvement streak |

### Monthly Report Variations

| Worker Type | Cash Flow Highlight | Unique Chart | Credit Metric |
|------------|--------------------|--------------|--------------| 
| Mama Mboga | Spoilage cost breakdown | Product mix donut | Seasonal credit timing |
| Boda Boda | Fuel cost trend | Daily earnings line | Motorcycle asset value |
| Jua Kali | Receivables aging | Job type profitability | Project pipeline value |
| Mitumba Seller | Bale cost vs yield | Category performance | Inventory asset value |
| Food Vendor | Ingredient cost trend | Menu profitability | Location value |
| Shopkeeper | Credit outstanding | Category pie | Inventory turnover |
| Hairdresser | Supply cost trend | Service mix bar | Client retention rate |
| Farmer | Input cost vs yield | Yield per acre line | Harvest forecast value |
| Construction Worker | Skill premium analysis | Working days bar | Skill certification |
| Market Trader | Supplier concentration | Product mix bar | Customer base value |

---

## Part VI: Implementation Priority

### Phase 1: Foundation (Months 1-3)
- [ ] Daily report for all 10 worker types (WhatsApp + App)
- [ ] Basic gamification (streaks, milestones)
- [ ] Voice summary generation
- [ ] Transaction data pipeline from voice input

### Phase 2: Intelligence (Months 4-6)
- [ ] Weekly report with trends and recommendations
- [ ] Business Health Score computation
- [ ] Chart generation (server-side Chart.js)
- [ ] Peer comparison (anonymized aggregation)

### Phase 3: Formality (Months 7-9)
- [ ] Monthly report with cash flow and income statement
- [ ] Alama Score with full breakdown
- [ ] Bank/MFI-ready formatting
- [ ] PDF export capability

### Phase 4: Certification (Months 10-12)
- [ ] 6-month report with seasonal analysis
- [ ] Credit readiness certification
- [ ] Yearly report with tax-ready statements
- [ ] Business valuation engine
- [ ] Goal setting and tracking system

---

## Appendix A: Report Message Templates

### Daily WhatsApp Template (Pre-approved)

```
📊 *MSAIDIZI — Daily Report*
📅 {{date}}

💰 *MONEY IN*
{{revenue_breakdown}}

💸 *MONEY OUT*
{{expense_breakdown}}

✅ *PROFIT TODAY: KSh {{profit}}*
📈 Yesterday: KSh {{yesterday_profit}} ({{change}}%)

💡 *INSIGHT:* {{insight}}

🔥 *STREAK:* {{streak}} days {{streak_type}}!

🏆 *ALAMA SCORE:* {{alama_label}} ({{alama_score}}/100)
```

### Weekly WhatsApp Template

```
📊 *MSAIDIZI — Weekly Report*
📅 {{week_range}}

💰 *WEEK SUMMARY*
Revenue: KSh {{total_revenue}}
Expenses: KSh {{total_expenses}}
Profit: KSh {{total_profit}}
Best Day: {{best_day}} (KSh {{best_profit}})
Worst Day: {{worst_day}} (KSh {{worst_profit}})

📈 *TRENDS*
Revenue: {{revenue_trend}} vs last week
Profit: {{profit_trend}} vs last week

📊 *TOP PRODUCTS*
{{product_ranking}}

💡 *RECOMMENDATIONS*
{{recommendations}}

🏥 *BUSINESS HEALTH: {{health_score}}/100*
{{health_details}}

🏆 *ALAMA SCORE: {{alama_score}}/100* ({{alama_change}})
```

---

## Appendix B: Error Handling & Edge Cases

| Scenario | Handling |
|----------|---------|
| No transactions recorded | "Hakuna mauzo ya leo" (No sales today) — still send report with zero values and encouragement |
| Partial data (only revenue, no expenses) | Estimate expenses from historical average, flag as estimated |
| Negative profit (loss day) | Show loss clearly, provide context ("Wastage kubwa leo" — big spoilage today), encourage streak restart |
| Worker hasn't reported in 3 days | Send gentle reminder: "Msaidizi anakukumbuka! Tafadhali sema mauzo yako ya leo." (Msaidizi misses you! Please tell me your sales today.) |
| Alama Score drops | Explain which component dropped and what to do about it |
| Chart generation failure | Fall back to text-only report, never skip the report |

---

## Appendix C: Data Privacy & Consent

- Workers consent to report generation during onboarding
- All reports are sent only to the worker's registered WhatsApp number
- Peer comparisons use only anonymized, aggregated data
- No individual worker data is ever shared with other workers
- Reports can be disabled at any time via voice command: "Sitaki ripoti" (I don't want reports)
- Financial data is encrypted at rest and in transit
- PDF exports are watermarked with the worker's unique identifier

---

*End of Swarm F2 Report System Design*
