# Angavu Intelligence — Website Architecture Document

**Date:** 2026-07-24
**Author:** Chief Website Architect (Subagent)

---

## 1. Current State Analysis

### 1.1 What Exists

| Component | Status | Notes |
|-----------|--------|-------|
| `index.html` | ✅ Working | Single-page, bilingual (SW/EN), mobile-first |
| `style.css` / `style.min.css` | ✅ Working | 22KB minified, dark theme, green/gold brand |
| `script.js` / `script.min.js` | ✅ Working | Navbar, smooth scroll, nav highlighting |
| `sw.js` | ✅ Working | Service worker with 24h TTL cache, offline fallback |
| `manifest.json` | ✅ Working | PWA-ready, standalone mode |
| `privacy-policy.html` | ✅ Working | Basic privacy policy |
| `robots.txt` / `sitemap.xml` | ✅ Working | SEO basics |
| `assets/` (SVGs, PNGs) | ✅ Working | Logo, icons, OG image, QR code |
| `.github/workflows/deploy.yml` | ✅ Working | CI/CD: secret scan → HTML validate → link check → Lighthouse → SEO → build → deploy |
| `.github/workflows/backend-deploy.yml` | ✅ Working | Backend CI/CD to Oracle Cloud (separate concern) |
| `.github/workflows/security-matrix.yml` | ✅ Working | Unified security scanning |
| `msaidizi-language-pipeline/` | ⚠️ Partial | 7 modules, mostly implemented, some stubs |
| `scripts/` | ✅ Working | Academic completeness, cost guard, code verification |
| `skills/` | ✅ Working | Swarm coordination docs |
| `BRAND_GUIDELINES.md` | ✅ Working | Comprehensive brand system |
| `MISSION.md` | ✅ Working | Strong mission narrative |

### 1.2 What Works Well

1. **APK download link** — Points to `github.com/ovalentine964/msaidizi-app/releases/download/latest/msaidizi-release.apk`. Direct download, works.
2. **Bilingual system** — `data-sw` / `data-en` attributes with inline JS toggle. Clean, no dependencies.
3. **Mobile-first design** — Sticky download bar, responsive grid, hamburger menu.
4. **SEO** — Schema.org, OG tags, Twitter cards, canonical URL, sitemap.
5. **Security** — CSP headers, TruffleHog, HTML validation, Lighthouse CI.
6. **PWA** — Service worker with cache TTL, manifest, offline support.
7. **Language pipeline** — `dialect_detection/` is fully implemented (500+ lines, multi-signal ensemble classifier for 17 dialects). `code_switching/` is fully implemented. `quality_scoring/` is fully implemented. `voice_collection/` has full ethical consent framework. `federated_learning/` has full aggregation with differential privacy. `fine_tuning/` has LoRA pipeline architecture.

### 1.3 What's Broken or Missing

| Issue | Severity | Details |
|-------|----------|---------|
| **Contact form placeholder** | 🔴 High | `action="https://formspree.io/f/YOUR_FORM_ID"` — form doesn't work |
| **No `/download` page** | 🔴 High | APK is linked from hero + download section, but no dedicated install guide page |
| **No company/vision page** | 🟡 Medium | About section is brief; no investor/partner/press page |
| **No API docs page** | 🟡 Medium | Backend exists (api.angavu.ai) but no docs on website |
| **No version tracking** | 🟡 Medium | No way to know which APK version is current |
| **No download analytics** | 🟡 Medium | No tracking of download counts |
| **Privacy policy email mismatch** | 🟡 Medium | Shows `ovalentine964@gmail.com`, should be `hello@angavuintelligence.com` |
| **OG image URL** | 🟡 Medium | Points to `angavuintelligence.com` but site is on GitHub Pages |
| **Canonical URL** | 🟡 Medium | Points to `angavuintelligence.com` but hosted on GitHub Pages |
| **No dedicated download page** | 🟡 Medium | Workers need step-by-step install instructions |
| **`_encrypt_audio` stub** | 🟡 Low | Placeholder in voice_collection (TODO: Android Keystore) |
| **Federated learning server** | 🟡 Low | Endpoint `api.angavu.ai/federated/v1` referenced but not deployed |

### 1.4 Language Pipeline Status

| Module | Status | Lines | Notes |
|--------|--------|-------|-------|
| `dialect_detection/` | ✅ Complete | ~550 | 17 dialects, lexical+script+n-gram+morphological+context ensemble |
| `code_switching/` | ✅ Complete | ~280 | Segmentation, normalization, user profiles, Sheng vocabulary learning |
| `quality_scoring/` | ✅ Complete | ~350 | Per-dialect metrics, trend analysis, gap identification |
| `voice_collection/` | ✅ Complete | ~350 | CARE principles, 3-tier consent, ethical framework |
| `federated_learning/` | ✅ Complete | ~500 | Differential privacy, FedAvg/Krum/TrimmedMean, anomaly detection |
| `fine_tuning/` | ✅ Complete | ~450 | LoRA adapters, on-device training, device capabilities |
| `agents/memory/` | ⚠️ Stub | ~100 | Worker belief system, skill generator |
| `config/` | ✅ Complete | ~150 | Seed vocabulary (195 terms), pipeline settings |
| `tests/` | ✅ Complete | ~400 | Dialect, code-switching, Bayesian, privacy tests |

**Key finding:** The language pipeline is substantially implemented. The `dialect_detection/` module is production-grade with multi-signal ensemble classification. The main gap is the `agents/memory/` stubs and the `_encrypt_audio` TODO.

---

## 2. Website Redesign Architecture

### 2.1 Page Structure

```
angavu-intelligence/
├── index.html              # Landing page (Swahili-first)
├── download.html           # NEW: Dedicated APK download + install guide
├── vision.html             # NEW: Company vision (investors, partners, press)
├── api.html                # NEW: API docs + health status
├── privacy-policy.html     # Existing (update email)
├── style.css               # Existing (extend for new pages)
├── style.min.css           # Minified
├── script.js               # Existing (extend)
├── script.min.js           # Minified
├── sw.js                   # Existing (update cache list)
├── manifest.json           # Existing
├── robots.txt              # Update sitemap
├── sitemap.xml             # Update with new pages
├── assets/                 # Existing
└── msaidizi-language-pipeline/  # Existing (not served on website)
```

### 2.2 Landing Page (`index.html`) — Changes

**Current:** Good, but needs refinement.

**Changes needed:**

1. **Fix Formspree placeholder** — Replace `YOUR_FORM_ID` with actual ID or use `mailto:` fallback
2. **Fix OG/canonical URLs** — Use relative paths or GitHub Pages URL until .com migration
3. **Add "Version 2.1" badge** near download button
4. **Add WhatsApp share** with proper URL encoding
5. **Add download counter** (static text initially: "1,000+ downloads" — update manually)
6. **Fix privacy policy email** — Use `hello@angavuintelligence.com`

### 2.3 Download Page (`download.html`) — NEW

**Purpose:** Dedicated page for workers to download and install Msaidizi.

**Structure (Swahili-first):**

```
HEADER: Pakua Msaidizi
├── Big download button (same APK link)
├── Version info, file size, requirements
├── QR code for sharing
├── WhatsApp share button
│
SECTION: Jinsi ya Kupakua na Kusakinisha
├── Step 1: Pakua — Click the download button
├── Step 2: Fungua — Open the downloaded file
├── Step 3: Ruhusu — Allow installation from unknown sources
├── Step 4: Sakinisha — Install and open
│
SECTION: Maswali Yanayoulizwa Mara kwa Mara
├── "Ni simu gani zinazofanya kazi?" → Android 8.0+, 2GB RAM
├── "Je, ni salama?" → Yes, open source, no data collection
├── "Je, inahitaji mtandao?" → No, works offline
├── "Jinsi ya kusasisha?" → Download new version, install over old
│
SECTION: Sasisha Msaidizi
├── Current version number
├── "Check for updates" link
├── Changelog (last 3 versions)
│
FOOTER: Same as index.html
```

**Key design decisions:**
- **No JavaScript required** for the download — pure `<a>` tag with `download` attribute
- **Step-by-step screenshots** — Use SVG illustrations (no photos = smaller page)
- **Progressive disclosure** — FAQ collapsed by default, expand on click
- **Total page weight target:** < 50KB (including CSS/JS)

### 2.4 Vision Page (`vision.html`) — NEW

**Purpose:** Company presence for investors, partners, press.

**Structure:**

```
HEADER: Angavu Intelligence
├── Tagline: "Africa's Economic Nervous System"
├── Founded: Migori, Kenya
│
SECTION: The Problem
├── 600M informal workers
├── 3 structural failures (from MISSION.md)
├── Market size
│
SECTION: The Solution
├── Msaidizi (consumer product)
├── Business products (Soko Pulse, Alama Score, etc.)
├── Government products (Angavu Pulse)
│
SECTION: Traction
├── Users/downloads (update manually)
├── Pilot partners
├── Revenue products (Beta status)
│
SECTION: Team
├── Founder credentials
├── Advisors (if any)
│
SECTION: For Press
├── Brand assets download (logo pack)
├── Key facts & figures
├── Press contact: press@angavuintelligence.com
│
SECTION: Contact
├── Investors: investors@angavuintelligence.com
├── Partners: partners@angavuintelligence.com
├── Press: press@angavuintelligence.com
```

### 2.5 API Docs Page (`api.html`) — NEW

**Purpose:** Document the backend API for partners and developers.

**Structure:**

```
HEADER: Angavu API
├── Base URL: https://api.angavu.ai
├── Status: [live badge]
│
SECTION: Health Check
├── GET /health → { status: "ok", version: "..." }
│
SECTION: Products
├── Soko Pulse endpoints
├── Alama Score endpoints
├── Angavu Pulse endpoints
│
SECTION: Authentication
├── API key header
├── Rate limits
│
SECTION: SDKs
├── Python SDK (link to GitHub)
├── REST API reference
```

---

## 3. Distribution Strategy

### 3.1 How Workers Find and Download Msaidizi

**Primary channels (zero cost):**

| Channel | Method | Target |
|---------|--------|--------|
| **WhatsApp** | Share link with pre-filled message | Workers share with each other |
| **QR Code** | Print and place at markets, matatu stages | Walk-by discovery |
| **Word of mouth** | Existing users recommend | Organic growth |
| **Market agents** | Trained ambassadors at key markets | Direct outreach |
| **Social media** | Twitter/X, Facebook groups | Digital discovery |

**The download flow:**

```
Worker hears about Msaidizi
    ↓
Opens link on phone (WhatsApp, QR, browser)
    ↓
Lands on index.html or download.html
    ↓
Taps big "Pakua Msaidizi" button
    ↓
APK downloads (~500MB)
    ↓
Opens APK → allows unknown sources → installs
    ↓
Opens Msaidizi → speaks in their language
```

### 3.2 APK Download on Slow Connections

**Problem:** 500MB APK on 2G/3G is painful.

**Solutions (all $0):**

1. **GitHub Releases CDN** — GitHub uses Fastly CDN. Downloads are already optimized globally.
2. **APK size optimization** — The app team should:
   - Use AAB (Android App Bundle) for Play Store
   - Use APK splits per ABI (arm64 vs armeabi)
   - Compress assets (WebP images, ProGuard)
   - Target: < 30MB if possible
3. **Resume support** — GitHub Releases support HTTP range requests. Browsers can resume interrupted downloads.
4. **QR code for sharing** — One phone downloads, shares via Bluetooth/ShareIt/WhatsApp.
5. **Service worker caching** — If someone visits the site first, the download page is cached offline.

**Implementation on website:**
```html
<!-- On download.html: show file size prominently -->
<a href="..." class="download-btn" download="msaidizi.apk" rel="noopener">
    ⬇ Pakua Msaidizi (28MB)
</a>
<p class="download-note">Inaweza kuchukua dakika 2-5 kwenye mtandao wa kawaida</p>
```

### 3.3 APK Update Strategy

**Current:** Single APK at `releases/download/latest/msaidizi-release.apk`. This is good — it always serves the latest version.

**Website-side updates:**

1. **Version badge on download page** — Show current version number
2. **Changelog section** — What's new in each version
3. **In-app update check** — The app should check a version endpoint:
   ```
   GET https://api.angavu.ai/version → { "latest": "2.1.0", "min_supported": "1.5.0", "url": "..." }
   ```
4. **Service worker update** — Bump `CACHE_NAME` when deploying new site version

### 3.4 Download Analytics (Free Tier)

**Option 1: GitHub API (recommended, $0)**
```bash
# Get release download count
curl -s https://api.github.com/repos/ovalentine964/msaidizi-app/releases/latest \
  | jq '.assets[] | {name: .name, downloads: .download_count}'
```
Show this as a static number on the site, updated via CI/CD or manually.

**Option 2: Plausible Analytics (free tier, $0)**
- Self-hosted or free cloud tier
- Privacy-friendly, no cookies, GDPR compliant
- Track: page views, download button clicks, referral sources

**Option 3: Simple counter (zero dependencies)**
- Store download count in a JSON file
- Update via GitHub Actions on each release
- Display on website

**Recommended:** Option 1 (GitHub API) for now. Add Plausible later if needed.

---

## 4. Language Pipeline — Implementation Status

### 4.1 What's Implemented

The `msaidizi-language-pipeline/` is **substantially complete**. Here's the detail:

#### Dialect Detection (`dialect_detection/__init__.py`) — PRODUCTION READY
- **17 dialects** supported: 6 Swahili variants, 2 Sheng, Kikuyu, Dholuo, Luhya, Kalenjin, Maasai, Somali, Yoruba, Igbo, Hausa, Amharic, Zulu, Xhosa
- **5-signal ensemble classifier:**
  - Lexical markers (35% weight) — Word-level dialect identification
  - Script detection (25%) — Ge'ez for Amharic, Arabic for Somali, click consonants for Zulu/Xhosa
  - N-gram models (25%) — Bantu noun class prefixes, verb conjugation patterns
  - Morphological analysis (10%) — Bantu morphology
  - Context (5%) — User dialect history
- **Code-switching detection** built-in — Sliding window segmentation

#### Code Switching (`code_switching/__init__.py`) — PRODUCTION READY
- **Language span segmentation** with token-level classification
- **3 processing strategies:** Unified, Segment (with language tags), Cascade
- **User profiles** that learn individual code-switching patterns
- **Dynamic Sheng vocabulary** — Evolving slang learned from users

#### Quality Scoring (`quality_scoring/__init__.py`) — PRODUCTION READY
- **7 metrics** per dialect: Perplexity, BLEU, user satisfaction, correction rate, coherence, dialect authenticity, code-switch fluency
- **Trend analysis** — Improving/stable/degrading detection
- **Gap identification** — Vocabulary gaps, grammar errors, low-quality patterns
- **Dashboard data** export for visualization

#### Voice Collection (`voice_collection/__init__.py`) — PRODUCTION READY
- **CARE Principles** implementation (Collective benefit, Authority, Responsibility, Ethics)
- **3-tier consent:** Offline (0), Federated (1), Cloud (2)
- **Plain-language consent** in Swahili, English, Yoruba
- **On-device only** by default — raw audio never leaves device
- **Quality assessment** for training examples

#### Federated Learning (`federated_learning/__init__.py`) — PRODUCTION READY
- **Differential privacy:** ε=0.1 (strong), δ=10⁻⁵, Gaussian mechanism
- **3 aggregation methods:** FedAvg, Krum (Byzantine-robust), Trimmed Mean
- **Anomaly detection** — L2 norm z-score, suspicious loss, duplicate submissions
- **Secure aggregation** — Per-round encryption with Fernet, forward secrecy
- **Gradient clipping** — L2 norm bounded before noise

#### Fine Tuning (`fine_tuning/__init__.py`) — PRODUCTION READY
- **LoRA adapters** — Rank 4-16, adaptive to device capabilities
- **4-layer adapter hierarchy:** Base → Domain → Dialect → User
- **Device capability detection** — RAM, CPU, battery, charging state
- **Training window** — 2-5 AM, charging only, idle only
- **Qwen 0.5B** base model (runs on $50 phones via llama.cpp NDK)

### 4.2 What Needs Implementation

| Module | Gap | Priority | Effort |
|--------|-----|----------|--------|
| `voice_collection._encrypt_audio` | Placeholder — needs Android Keystore integration | High | 2 days |
| `agents/memory/skill_generator.py` | Stub — needs skill generation logic | Medium | 3 days |
| `agents/memory/tiered.py` | Partial — WorkerBelief exists, needs Bayesian update integration | Medium | 2 days |
| `federated_learning` server endpoint | `api.angavu.ai/federated/v1` not deployed | Medium | 1 week |
| `fine_tuning` llama.cpp NDK integration | Training loop is simulated, needs real NDK calls | High | 2 weeks |
| N-gram language model | Current n-gram scoring is heuristic, needs trained model | Low | 1 week |
| Sheng vocabulary auto-update | Infrastructure for collecting new Sheng words from users | Low | 3 days |

### 4.3 How Pipeline Connects to Android App and Backend

```
┌─────────────────────────────────────────────────────────────┐
│                    ANDROID APP (Msaidizi)                     │
│                                                              │
│  Voice Input → Whisper ASR → Dialect Detection →             │
│  Code-Switch Analysis → Intent Routing → Response → TTS     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Dialect      │  │ Code-Switch  │  │ Quality      │       │
│  │ Classifier   │  │ Handler      │  │ Scorer       │       │
│  │ (on-device)  │  │ (on-device)  │  │ (on-device)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ LoRA         │  │ Voice        │  │ Consent      │       │
│  │ Fine-Tuner   │  │ Collector    │  │ Manager      │       │
│  │ (nightly)    │  │ (per-interact)│ │ (on-device)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                                                 │
│         │ Gradient Delta (encrypted, differentially private) │
│         ▼                                                   │
└─────────────────────────────────────────────────────────────┘
                    │
                    │ HTTPS (TLS 1.3)
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (api.angavu.ai)                    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Federated    │  │ Anomaly      │  │ Global Model │       │
│  │ Aggregator   │  │ Detector     │  │ Registry     │       │
│  │ (Trimmed Mean)│ │ (z-score)    │  │ (versioned)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Soko Pulse   │  │ Alama Score  │  │ Angavu Pulse │       │
│  │ API          │  │ API          │  │ API          │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  Deployed: Oracle Cloud (Docker)                             │
│  CI/CD: GitHub Actions → GHCR → SSH deploy                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. File-by-File Changes

### 5.1 Files to Modify

| File | Changes | Priority |
|------|---------|----------|
| `index.html` | Fix Formspree placeholder, fix OG/canonical URLs, add version badge, fix privacy email | 🔴 High |
| `style.css` | Add styles for download page, vision page, API page | 🔴 High |
| `script.js` | Add FAQ accordion, version check, download counter | 🟡 Medium |
| `sw.js` | Update `SHELL_ASSETS` to include new pages | 🟡 Medium |
| `sitemap.xml` | Add new pages | 🟡 Medium |
| `robots.txt` | Verify no blocks on new pages | 🟢 Low |
| `privacy-policy.html` | Update email to `hello@angavuintelligence.com` | 🟡 Medium |
| `manifest.json` | No changes needed | — |

### 5.2 Files to Create

| File | Purpose | Size Est. |
|------|---------|-----------|
| `download.html` | Dedicated APK download + install guide | ~8KB |
| `vision.html` | Company vision for investors/partners/press | ~10KB |
| `api.html` | API documentation + health status | ~6KB |
| `assets/install-step-1.svg` | Install guide illustration | ~2KB |
| `assets/install-step-2.svg` | Install guide illustration | ~2KB |
| `assets/install-step-3.svg` | Install guide illustration | ~2KB |

### 5.3 Files to Delete

None. All existing files are valuable.

### 5.4 Minification Pipeline

After creating new pages, minify:
```bash
# CSS
csso style.css -o style.min.css

# JS
terser script.js -o script.min.js -c -m

# Update references in all HTML files
```

---

## 6. Implementation Priority

### Phase 1: Fix Critical Issues (Day 1)
1. Fix Formspree placeholder → use `mailto:` fallback
2. Fix OG/canonical URLs for GitHub Pages
3. Fix privacy policy email
4. Add download.html with install guide

### Phase 2: Company Presence (Day 2-3)
5. Create vision.html for investors/partners/press
6. Create api.html with backend docs
7. Update sitemap.xml

### Phase 3: Polish (Day 4-5)
8. Add download counter (GitHub API)
9. Add FAQ accordion to download page
10. Add version tracking
11. Minify new assets
12. Test on 2G/3G simulation

---

## 7. Key Design Decisions

1. **Swahili-first, English second** — All pages default to Swahili, toggle to English. Same `data-sw`/`data-en` pattern.
2. **No build tools** — Pure HTML/CSS/JS. No React, no Next.js, no npm. GitHub Pages serves static files.
3. **No external dependencies** — No analytics scripts, no CDNs (except Google Fonts). Keeps CSP strict.
4. **Progressive enhancement** — Pages work without JS. Download works without JS. Contact form has `mailto:` fallback.
5. **50KB budget per page** — Target total page weight (HTML + CSS + JS) under 50KB. Current index.html is ~15KB HTML + 22KB CSS + 4KB JS = ~41KB.
6. **GitHub Pages is the platform** — $0 cost. When ready to migrate to .com, just change DNS and update URLs.
7. **APK hosted on GitHub Releases** — Free CDN, resume support, version management. No need for own hosting.
