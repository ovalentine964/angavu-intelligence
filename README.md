![Angavu Intelligence](assets/logo-banner.svg)

# Angavu Intelligence — Website

**Making 200 million invisible workers visible through data.**

## Live

https://ovalentine964.github.io/angavu-intelligence/

## Mission

Provide economic intelligence to Africa's 600M+ informal workers by making invisible workers visible through data, fixing market inefficiencies, information asymmetry, and coordination failures.

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

### For Businesses
- **Soko Pulse** — FMCG demand forecasting from informal markets (Beta)
- **Alama Score** — Alternative credit scoring for the unbanked (Beta)
- **Distribution Intelligence** — Route optimization for last-mile delivery
- **Risk Intelligence** — Default probability for informal borrowers
- **FMCG Intelligence** — Informal channel tracking (Pwani Oil pilot)
- **Supply Chain** — Agricultural supply optimization

### For Government
- **Angavu Pulse** — MSME Activity Index (Beta)
- **Employment Intelligence** — Real-time labor market data
- **Tax Base Mapping** — Identify untaxed economic activity
- **GDP Estimator** — Real-time informal GDP by county
- **Inflation Tracker** — Daily price indices from informal markets

### For NGOs
- **Jamii Insights** — Financial inclusion metrics (Beta)
- **Impact Measurement** — Track intervention effectiveness
- **Poverty Mapping** — Community-level economic indicators
- **SDG Tracker** — SDG progress from real economic data
- **Gender Intelligence** — Women's economic participation

### For Researchers
- **Data API** — Raw anonymized transaction data
- **Research Portal** — Academic access program

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

## Goals

| Timeline | Target |
|----------|--------|
| Month 3 | 1,000 workers onboarded |
| Month 6 | 10,000 workers onboarded |
| Month 12 | 100,000 workers + $1M revenue |
| Month 18 | 5 African countries |
| Month 24 | 1,000,000 workers |
| Year 5 | $25M revenue |

## License

Proprietary — Angavu Intelligence

---

*Built with ❤️ in Migori, Kenya*
