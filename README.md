![Angavu Intelligence](assets/logo-banner.svg)

# Angavu Intelligence — Website

**Making 200 million invisible workers visible through data.**

## Live

https://ovalentine964.github.io/angavu-intelligence/

## Mission — AI for Humanity

Provide economic intelligence to Africa's 600M+ informal workers by making invisible workers visible through data, fixing market inefficiencies, information asymmetry, and coordination failures.

**What "AI for Humanity" means:** Not AI that replaces humans. Not AI that surveils humans. AI that makes invisible humans visible — a $50 phone in a Nairobi market running an AI that speaks Sheng, tracks business finances, and tells the owner she's being overcharged by 15%.

**Three structural failures Angavu solves:**
- **Information asymmetry** — Workers don't know fair prices, interest rates, or their own financial position. Angavu gives every worker a CFO.
- **Coordination failures** — 50 million individuals can't act as one. Angavu Pulse aggregates anonymized data so policymakers see what workers actually need.
- **Market exploitation** — Informal workers get the worst prices, credit, and deals. Angavu gives them intelligence and leverage.

See [MISSION.md](MISSION.md) for the full story.

## Vision

Africa's economic nervous system — the platform that forces good governance through data, the CFO for every informal worker in Africa.

## Products

### For Workers
- **Msaidizi** — Voice-based, offline-first mobile app for tracking business finances
  - 🎤 Voice-first: speak in your language (14 dialects supported)
  - 📴 Offline-first: works without internet
  - 🎮 Gamification: points, levels, streaks, badges
  - 💰 Wealth Mindset: daily habit tracking
  - 🤲 Tithe & Giving: track charitable giving
  - 🎯 Goals & Loans: savings goals and loan tracking

### For Businesses (6 Implemented Products)

> **Note:** These are the 6 backend products with actual code. See [docs/PRODUCT_INVENTORY.md](docs/PRODUCT_INVENTORY.md) for full breakdown.

- **Soko Pulse** — FMCG demand forecasting from informal markets (Beta) — $2,000-$12,000/mo
- **Alama Score** — Financial readiness assessment for the unbanked (Beta) — $0.05-$0.50/query
  - ⚠️ Positioned as "Financial Readiness Assessment" — NOT credit scoring
  - See [docs/ALAMA_SCORE_POSITIONING.md](docs/ALAMA_SCORE_POSITIONING.md)
- **Distribution Intelligence** — Route optimization for last-mile delivery — $15,000-$30,000 one-time
- **Tax Base Mapping** — Identify untaxed economic activity — $1,500-$10,000/mo
- **Jamii Insights** — Financial inclusion metrics (Beta) — $2,000-$10,000/study
- **FMCG Intelligence** — Informal channel tracking (Pwani Oil pilot) — Built on Soko Pulse

### For Government
- **Angavu Pulse** — MSME Activity Index (Beta) — $250-$5,000/mo
- **Employment Intelligence** — Real-time labor market data
- **Tax Base Mapping** — Identify untaxed economic activity — $1,500-$10,000/mo + outcome-based

### For NGOs
- **Jamii Insights** — Financial inclusion metrics (Beta) — $2,000-$10,000/study
- **Impact Measurement** — Track intervention effectiveness

### On the Roadmap (No Code Yet)
- Afya Pulse (health economics), Shamba Intelligence (agriculture), Safari Intelligence (transport), Elimu Intelligence (education), Bima Intelligence (insurance), Akiba Pulse (savings)

## Stack

- Pure HTML/CSS/JS (no build tools)
- GitHub Pages hosting
- Bilingual (English/Swahili)
- Mobile-first responsive design
- PWA ready (manifest.json + service worker)

## Features

- **One-click APK download** — Prominent download CTAs
- **Floating WhatsApp button** — Easy contact
- **Sticky mobile download bar** — Always-visible download on mobile
- **Trust signals** — Founder credentials, privacy badges, testimonials
- **Segment targeting** — Different messaging for workers vs businesses
- **Language toggle** (EN/SW)
- **SEO optimized** — Schema.org, Open Graph, Twitter Cards
- **Accessibility** — Skip links, focus-visible, reduced motion support

## Website Structure

```
angavu-intelligence/
├── index.html          # Main landing page
├── style.css           # All styles (mobile-first)
├── style.min.css       # Minified CSS (22KB)
├── script.js           # Interactions, language toggle
├── script.min.js       # Minified JS (4KB)
├── sw.js               # Service worker (offline support)
├── manifest.json       # PWA manifest
├── assets/             # Images, icons, logo SVGs
├── sitemap.xml         # SEO sitemap
├── robots.txt          # SEO robots
└── .nojekyll           # Bypass Jekyll on GitHub Pages
```

## Editing

Just edit `index.html` and push. GitHub Pages auto-deploys.

## Local Development

```bash
# Any static server works
python3 -m http.server 8000
# Open http://localhost:8000
```

## Goals (Corrected — July 2026)

| Timeline | Target | Notes |
|----------|--------|-------|
| Month 6 | 1,000-5,000 workers onboarded | Organic growth through word of mouth |
| Month 12 | 5,000-10,000 workers + $90K-$260K B2B revenue | 3-5 enterprise clients |
| Month 18 | 50,000 workers + 7-15 B2B clients | Approaching break-even |
| Month 24 | 100,000-500,000 workers + $400K-$1.2M revenue | Break-even achieved |
| Year 3 | 500,000+ workers + $1.5M-$4M revenue | 20-40 B2B clients |
| Year 5 | 1M+ workers + $4.9M-$10M revenue | Pan-African expansion |

**Note:** Revenue comes from B2B intelligence products (FMCG, banks, government, NGOs), not from worker subscriptions. Workers use Msaidizi for free. Break-even requires 7-15 B2B clients, not a specific worker count.

## License

Proprietary — Angavu Intelligence

---

*Built with ❤️ in Migori, Kenya*
