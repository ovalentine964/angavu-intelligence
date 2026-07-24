<div align="center">

# 🌍 Angavu Intelligence

### Revenue Intelligence for Africa's Informal Economy

**Transforming how Africa understands, measures, and grows its $1.2 trillion informal economy through AI-powered intelligence.**

[![Website](https://img.shields.io/badge/🌐_Website-ovalentine964.github.io%2Fangavu--intelligence-blue)](https://ovalentine964.github.io/angavu-intelligence/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## 🎯 The Problem

Africa's informal economy accounts for **~85% of employment** and **~40% of GDP**, yet it remains invisible to policymakers, financial institutions, and the businesses that serve it. Without data:

- **Governments** can't design effective economic policy
- **Banks** can't assess creditworthiness of informal workers
- **FMCG companies** can't optimize distribution to millions of small shops
- **Workers** have no financial identity or access to formal services

## 💡 The Solution

Angavu Intelligence is a **superagent-powered platform** that bridges the gap between Africa's informal economy and the formal financial system. Through voice-first, offline-first AI agents running on budget smartphones, we:

- 📊 **Generate economic intelligence** from ground-level transaction data
- 🏦 **Build credit identities** for the unbanked
- 🗺️ **Map trade routes** and distribution networks
- 📈 **Provide real-time market insights** to businesses and governments

## 🏗️ Platform Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     Angavu Intelligence Platform                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │  Msaidizi    │     │  Intelligence│     │   Website    │     │
│  │  Mobile App  │────▶│  Backend     │────▶│   & Docs     │     │
│  │  (Android)   │     │  (Rust)      │     │  (Static)    │     │
│  └──────────────┘     └──────────────┘     └──────────────┘     │
│         │                    │                     │             │
│         ▼                    ▼                     ▼             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │  On-Device   │     │  15 Revenue  │     │  Public      │     │
│  │  AI Agent    │     │  Intelligence│     │  Presence    │     │
│  │  Qwen 0.8B   │     │  Engines     │     │  & API Docs  │     │
│  └──────────────┘     └──────────────┘     └──────────────┘     │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Data Sources: Voice Transactions │ POS Data │ Mobile Money     │
│  Privacy: k-Anonymity (k≥10) │ Differential Privacy │ PQC       │
└──────────────────────────────────────────────────────────────────┘
```

## 📦 Our Repositories

| Repository | Description | Tech Stack |
|------------|-------------|------------|
| [**msaidizi-app**](https://github.com/ovalentine964/msaidizi-app) | On-device AI business assistant for Android | Kotlin, Qwen 0.8B, Whisper, Piper |
| [**angavu-intelligence-backend**](https://github.com/ovalentine964/angavu-intelligence-backend) | Revenue intelligence API platform | Rust (Axum), PostgreSQL, Redis, ClickHouse |
| [**angavu-intelligence**](https://github.com/ovalentine964/angavu-intelligence) | Website, documentation & public presence | HTML, CSS, JavaScript |

## 🎨 Website Pages

| Page | Description |
|------|-------------|
| [Home](https://ovalentine964.github.io/angavu-intelligence/) | Platform overview and value proposition |
| [For Workers](https://ovalentine964.github.io/angavu-intelligence/for-workers.html) | How informal workers benefit |
| [For Businesses](https://ovalentine964.github.io/angavu-intelligence/for-businesses.html) | FMCG and distribution intelligence |
| [For Government](https://ovalentine964.github.io/angavu-intelligence/for-government.html) | Economic policy intelligence |
| [Technology](https://ovalentine964.github.io/angavu-intelligence/technology.html) | Technical architecture and capabilities |
| [API Docs](https://ovalentine964.github.io/angavu-intelligence/api.html) | API documentation and integration guides |
| [Download](https://ovalentine964.github.io/angavu-intelligence/download.html) | Get the Msaidizi app |
| [Vision](https://ovalentine964.github.io/angavu-intelligence/vision.html) | Our long-term vision |
| [Privacy Policy](https://ovalentine964.github.io/angavu-intelligence/privacy-policy.html) | Data privacy and protection |

## 🚀 Quick Start

This is a static website — no build step required.

```bash
# Clone
git clone https://github.com/ovalentine964/angavu-intelligence.git
cd angavu-intelligence

# Serve locally
python3 -m http.server 8080
# Open http://localhost:8080

# Or simply open in browser
open index.html
```

## 📂 Project Structure

```
angavu-intelligence/
├── index.html              # Landing page
├── for-workers.html        # Worker value proposition
├── for-businesses.html     # Business intelligence page
├── for-government.html     # Government intelligence page
├── technology.html         # Technical architecture
├── api.html                # API documentation
├── download.html           # App download page
├── vision.html             # Company vision
├── privacy-policy.html     # Privacy policy
├── style.css               # Main stylesheet
├── design-tokens.css       # Design system tokens
├── script.js               # Interactive features
├── sw.js                   # Service worker (PWA)
├── manifest.json           # PWA manifest
├── robots.txt              # Search engine directives
├── sitemap.xml             # Sitemap for SEO
└── assets/                 # Images, icons, media
```

## 🎨 Design System

The website uses a consistent design system defined in `design-tokens.css`:

- **Colors**: Deep navy primary, warm gold accents, green growth indicators
- **Typography**: System font stack for fast loading
- **Spacing**: 8px grid system
- **Components**: Cards, badges, charts, responsive grid

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Help

- 🌍 **Translations** — Help us reach more African languages
- 🎨 **Design** — Improve the visual experience
- 📝 **Content** — Improve copy and messaging
- 🐛 **Bug fixes** — Fix issues across devices and browsers
- ♿ **Accessibility** — Make the site usable for everyone

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🔗 Links

- 🌐 **Website**: [ovalentine964.github.io/angavu-intelligence](https://ovalentine964.github.io/angavu-intelligence/)
- 📱 **App**: [msaidizi-app](https://github.com/ovalentine964/msaidizi-app)
- ⚙️ **Backend**: [angavu-intelligence-backend](https://github.com/ovalentine964/angavu-intelligence-backend)

## 📬 Contact

- **GitHub**: [@ovalentine964](https://github.com/ovalentine964)
- **Issues**: [GitHub Issues](../../issues)

---

<div align="center">

**Built with ❤️ for Africa's informal economy**

*Every mama mboga deserves a business intelligence platform.*

</div>
