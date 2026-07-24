# Website Architecture: Angavu Intelligence — Superagent Distribution Platform

**Author:** Chief Architect (Subagent)
**Date:** 2026-07-24
**Status:** DESIGN COMPLETE — Ready for Implementation
**Updated:** 2026-07-24 — M-KOPA proof-flywheel model integrated
**Repo:** https://github.com/ovalentine964/angavu-intelligence

---

## 1. Analysis of Current Site

### What Exists Today
| File | Purpose |
|------|---------|
| `index.html` | Single-page marketing site (Kiswahili-first) |
| `download.html` | APK download page with install instructions |
| `vision.html` | Vision/mission page ("Africa's Economic Nervous System") |
| `api.html` | Developer API docs (Soko Pulse, Alama Score, Angavu Pulse) |
| `style.min.css` | Monolithic stylesheet (~14KB minified) |
| `script.min.js` | JS for nav, lang toggle, animations |

### Current Brand Identity
- **Primary BG:** `#1B4965` (deep teal/blue)
- **Accent:** `#E8A838` (gold/amber)
- **Typography:** Inter (body) + Playfair Display (headings)
- **Tone:** Kiswahili-first, Kenyan pride, community-focused
- **Tagline:** "Biashara Yako. Sauti Yako." (Your Business. Your Voice.)

### What Works (Keep)
- ✅ Kiswahili-first + English toggle approach
- ✅ Deep teal + gold color system — strong, distinctive
- ✅ Inter + Playfair Display pairing
- ✅ Accessibility: skip links, ARIA labels, focus-visible, reduced-motion
- ✅ CSP headers, security hardening
- ✅ Phone mockup with live activity feed
- ✅ Trust strip: "Data yako inabaki simu yako"
- ✅ QR code download option
- ✅ WhatsApp share button

### What Needs to Change
- ❌ Positioned as "business assistant app" — must become "superagent platform"
- ❌ Single APK download (~500MB) — needs lite-first progressive model
- ❌ No mention of intelligence products for businesses/government
- ❌ No business flow visualization concept
- ❌ No explanation of the superagent architecture (voice-first, offline-first, gets smarter)
- ❌ Limited to 2 languages in UI
- ❌ Flat information architecture — everything on one page

---

## 2. New Site Architecture

### 2.1 Sitemap

```
/                           → Landing: The Superagent for Informal Workers
├── /download               → One-click APK download (lite flavor)
├── /how-it-works           → Voice demo, flywheel, intelligence layers
├── /for-workers            → Worker-focused value proposition
├── /for-businesses         → Intelligence products (Soko Pulse, Alama Score)
├── /for-government         → Economic visibility tools for policy
├── /technology             → Superagent architecture (simplified public view)
├── /privacy                → Privacy-first design philosophy
└── /api                    → Developer API documentation
```

### 2.2 Page-by-Page Specification

---

#### PAGE 1: `index.html` — Landing Page

**URL:** `/`
**Purpose:** Convert visitors to downloaders. Convey the M-KOPA proof model in 10 seconds.
**Primary CTA:** Download Msaidizi APK
**Secondary CTA:** Learn how it works

**Content Structure:**

```
┌─────────────────────────────────────────────────────┐
│ NAVBAR                                               │
│  Logo ◆ Angavu Intelligence                         │
│  How It Works | Workers | Businesses | Government    │
│  Download | Language (EN/SW/... toggle)              │
├─────────────────────────────────────────────────────┤
│ HERO SECTION                                         │
│  Kicker: 🇰🇪 Built in Migori, Kenya                 │
│  H1: "Your Business, Understood."                    │
│      (SW: "Biashara Yako, Inayoeleweka.")            │
│  Sub: The superagent that speaks your language.       │
│       Voice-first. Offline-first. Gets smarter.      │
│  CTA: [⬇ Download Msaidizi — Free]                   │
│  CTA: [How It Works →]                               │
│                                                      │
│  Trust Strip: 🔒 On-device | 📴 Offline | 🆓 Free   │
│               🧠 Gets smarter | 🗣️ Your language     │
│                                                      │
│  [Phone Mockup: Live conversation + activity feed]   │
├─────────────────────────────────────────────────────┤
│ THE M-KOPA PARALLEL (new section)                    │
│                                                      │
│  "M-KOPA proved daily payments build credit.         │
│   Msaidizi proves daily voice builds business        │
│   intelligence."                                     │
│                                                      │
│  [Side-by-side visual:]                              │
│  M-KOPA: Phone → Payments → Credit → $2B unlocked   │
│  MSAIDIZI: Voice → Tracking → Proof → Economy visible│
├─────────────────────────────────────────────────────┤
│ THE PROOF FLYWHEEL (new section)                     │
│                                                      │
│  Animated circular diagram:                          │
│                                                      │
│     Speak ──→ Track ──→ Prove ──→ Unlock ──→ Grow   │
│      ↑                                        │      │
│      └────────────────────────────────────────┘      │
│                                                      │
│  "Every word is proof. Every day builds more."       │
│                                                      │
│  Step descriptions:                                  │
│  🎤 Speak — Tell Msaidizi what you sold              │
│  📊 Track — He records everything automatically      │
│  📋 Prove — Your business activity becomes proof     │
│  🔓 Unlock — Credit, insurance, market access        │
│  🌱 Grow — Your business, understood and supported   │
├─────────────────────────────────────────────────────┤
│ THE STACKING EFFECT (new section)                    │
│                                                      │
│  "Start with one sale. Unlock everything."           │
│                                                      │
│  Timeline visualization:                             │
│  Day 1:   🎤 "Niliuza nyanya, KES 450"              │
│  Week 2:  📊 "Your profit is up 15%"                 │
│  Month 1: 💳 "Your business qualifies for a loan"    │
│  Month 3: 🛡️ "Insurance access unlocked"             │
│  Month 6: 📈 "Tomatoes will be scarce next week"     │
│  Year 1:  🌍 Full economic profile — visible          │
├─────────────────────────────────────────────────────┤
│ WHO IT'S FOR (3 audience cards)                      │
│  👩‍🌾 Workers — Your business, understood             │
│  🏢 Businesses — Intelligence products               │
│  🏛️ Government — Economic visibility                 │
├─────────────────────────────────────────────────────┤
│ THE VISION                                           │
│  "10 million invisible workers will become visible." │
│  "M-KOPA took 14 years and $2B. We're starting now."│
├─────────────────────────────────────────────────────┤
│ DOWNLOAD CTA (full-width green band)                 │
│  "One download. All models. Works immediately."      │
│  "The smallest action that starts the journey."      │
│  [⬇ Download Msaidizi APK — 65MB Lite]              │
├─────────────────────────────────────────────────────┤
│ FOOTER                                               │
│  Links: Pages | API | GitHub | Contact               │
│  "Making the invisible economy visible"              │
└─────────────────────────────────────────────────────┘
```

**HTML Pattern (reused across all pages):**

```html
<!DOCTYPE html>
<html lang="sw" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Msaidizi — Your Business, Understood | Angavu Intelligence</title>
    <meta name="description" content="The superagent for informal workers. Voice-first, offline-first, gets smarter. Free forever.">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Msaidizi — Your Business, Understood">
    <meta property="og:description" content="The superagent for informal workers. Voice-first, offline-first, gets smarter.">
    <meta property="og:image" content="https://angavu-intelligence.github.io/assets/og-superagent.png">
    <meta property="og:url" content="https://angavu-intelligence.github.io/">
    <meta property="og:type" content="website">
    
    <!-- Multilingual hreflang -->
    <link rel="alternate" hreflang="sw" href="/?lang=sw">
    <link rel="alternate" hreflang="en" href="/?lang=en">
    <link rel="alternate" hreflang="x-default" href="/">
    
    <!-- Preload critical assets -->
    <link rel="preload" href="/css/base.css" as="style">
    <link rel="preload" href="/css/components.css" as="style">
    <link rel="preload" href="/js/app.js" as="script">
    
    <!-- Stylesheets (split for caching) -->
    <link rel="stylesheet" href="/css/base.css">       <!-- Reset + variables + typography -->
    <link rel="stylesheet" href="/css/components.css">  <!-- Cards, buttons, nav, sections -->
    <link rel="stylesheet" href="/css/pages.css">       <!-- Page-specific overrides -->
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
    
    <!-- PWA -->
    <link rel="manifest" href="/manifest.json">
    <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
    <link rel="apple-touch-icon" href="/assets/icon-192.png">
    
    <!-- Security -->
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'none';">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    
    <!-- Accessibility (inline critical styles) -->
    <style>
        .skip-link { position:absolute; top:-100%; left:50%; transform:translateX(-50%); background:#F59E0B; color:#1a1a1a; padding:12px 24px; border-radius:0 0 10px 10px; font-weight:700; z-index:10000; transition:top 0.2s; }
        .skip-link:focus { top:0; }
        .sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
        @media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:0.01ms!important; transition-duration:0.01ms!important; scroll-behavior:auto!important; } }
    </style>
</head>
<body class="lang-sw">
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <div id="lang-announcement" aria-live="polite" aria-atomic="true" class="sr-only"></div>
    
    <!-- Shared navbar (loaded via JS component or inline) -->
    <nav class="navbar" id="navbar" role="navigation" aria-label="Main navigation">...</nav>
    
    <main id="main-content" role="main">
        <!-- Page content here -->
    </main>
    
    <footer class="site-footer">...</footer>
    
    <!-- Scripts -->
    <script src="/js/app.js" defer></script>
</body>
</html>
```

---

#### PAGE 2: `download.html` — Download Experience

**URL:** `/download`
**Purpose:** Single-focus download page. One click → APK.
**Design Principle:** Zero friction. The smallest action that starts the journey.
**M-KOPA Frame:** "M-KOPA's first phone purchase was the smallest commitment that started the biggest journey. Your download is the same."

**Content Structure:**

```
┌─────────────────────────────────────────────────────┐
│ HERO                                                 │
│  H1: "One Download. Everything Works."               │
│      (SW: "Pakua Mara Moja. Kila Kitu Kinafanya.")  │
│                                                      │
│  [ ⬇ DOWNLOAD MSAIDIZI — 65MB ]  ← BIG GREEN BUTTON │
│                                                      │
│  📱 Android 8.0+ | 💾 ~65MB | 🧠 RAM 2GB            │
│  📴 Works offline | 🆓 No account needed             │
│                                                      │
│  QR Code | WhatsApp Share                            │
├─────────────────────────────────────────────────────┤
│ WHAT HAPPENS AFTER DOWNLOAD (3 steps)                │
│                                                      │
│  1. Install — Open the APK, tap "Install"            │
│     (Show: Allow from unknown sources screenshot)    │
│                                                      │
│  2. Launch — Msaidizi greets you in your language     │
│     (Show: Voice onboarding screen)                  │
│                                                      │
│  3. Speak — Tell it about your business               │
│     (Show: First voice interaction)                  │
│                                                      │
│  "No sign-up. No phone number. No internet needed."  │
│  "This is your M-KOPA moment. One tap starts it all."│
├─────────────────────────────────────────────────────┤
│ WHAT YOU'LL UNLOCK (stacking timeline)               │
│                                                      │
│  Visual: Progressive unlock timeline                 │
│  Day 1:   Voice tracking works immediately           │
│  Week 2:  Business insights appear                   │
│  Month 1: Credit proof builds automatically          │
│  Month 3: Insurance, loans, market access            │
│                                                      │
│  "You don't apply for these. They unlock."           │
│  "M-KOPA didn't ask customers to build credit.       │
│   Payments did it automatically. Same here."         │
├─────────────────────────────────────────────────────┤
│ PROGRESSIVE MODEL LOADING                            │
│                                                      │
│  Visual: Phone with progress bar                     │
│  "Msaidizi downloads intelligence models as needed.  │
│   On WiFi: automatic. On data: you choose.           │
│   Core features work immediately — offline."         │
│                                                      │
│  Tier breakdown:                                     │
│  ┌─────────────────────────────────────────┐         │
│  │ Lite APK (65MB) — Instant: Voice track, │         │
│  │   expense logging, basic advice          │         │
│  │ + Voice model (45MB) — Speech recognition│         │
│  │ + Intelligence model (120MB) — Smart     │         │
│  │   pricing, demand prediction             │         │
│  │ + Full bundle (300MB) — All languages,   │         │
│  │   advanced analytics                     │         │
│  └─────────────────────────────────────────┘         │
├─────────────────────────────────────────────────────┤
│ SYSTEM REQUIREMENTS                                  │
│  Minimum: Android 8.0, 2GB RAM, 200MB free           │
│  Recommended: Android 10+, 3GB RAM, 500MB free       │
│  Languages: English, Kiswahili, Sheng, + more        │
├─────────────────────────────────────────────────────┤
│ TROUBLESHOOTING FAQ                                  │
│  "Installation blocked?" → Enable unknown sources    │
│  "Not enough space?" → Lite mode needs only 200MB    │
│  "No internet?" → Core features work immediately     │
│  "Old phone?" → Android 8.0+ supported               │
└─────────────────────────────────────────────────────┘
```

**Key Download Flow:**

```
User clicks "Download" button
    ↓
APK download starts (msaidizi-lite-v3.apk, ~65MB)
    ↓
User opens APK → Android install prompt
    ↓
First launch: Voice-guided onboarding
  → "Habari! Mimi ni Msaidizi. Unaitwa nani?" (voice)
  → User speaks their name
  → "Sema — biashara yako ni ipi?" (What's your business?)
  → User describes their business
  → Msaidizi sets up tracking categories
    ↓
Core features available IMMEDIATELY (offline)
    ↓
On WiFi: progressive model downloads begin
  → Voice model (better speech recognition)
  → Intelligence model (smart pricing, predictions)
  → Each download announced: "Msaidizi ameongezeka!" (Msaidizi got smarter!)
```

---

#### PAGE 3: `how-it-works.html` — The Flywheel

**URL:** `/how-it-works`
**Purpose:** Explain the proof flywheel. Show the M-KOPA parallel. Make the superagent concept tangible.
**Central Narrative:** "If M-KOPA proved daily payments build credit, Msaidizi proves daily voice recordings build business intelligence."

**Content Structure:**

```
┌─────────────────────────────────────────────────────┐
│ HERO                                                 │
│  H1: "How Msaidizi Works"                            │
│      (SW: "Jinsi Msaidizi Anavyofanya Kazi")         │
│  Sub: Not an app. A superagent.                      │
├─────────────────────────────────────────────────────┤
│ THE THREE LAYERS                                     │
│                                                      │
│  ┌──────────────────────────────────────┐            │
│  │ Layer 3: BUSINESS FLOW INTELLIGENCE  │            │
│  │ "Like M-Pesa showed cash flow,       │            │
│  │  Msaidizi shows business flow"        │            │
│  │ Soko Pulse, Alama Score, predictions │            │
│  ├──────────────────────────────────────┤            │
│  │ Layer 2: PERSONAL INTELLIGENCE       │            │
│  │ Your CFO, inventory tracker,         │            │
│  │ pricing advisor — on your phone      │            │
│  ├──────────────────────────────────────┤            │
│  │ Layer 1: VOICE INTERFACE             │            │
│  │ Speak naturally. Your language.      │            │
│  │ No forms. No typing.                 │            │
│  └──────────────────────────────────────┘            │
├─────────────────────────────────────────────────────┤
│ INTERACTIVE DEMO                                     │
│  Animated phone mockup showing:                      │
│                                                      │
│  User: "Niliuza nyanya kilo tatu, mia mbili"         │
│        (I sold 3kg tomatoes for 200)                 │
│                                                      │
│  Msaidizi: "Imerekodwa! Leo umepata KES 450          │
│             mauzo. Gharama ni KES 130.               │
│             Faida: KES 320. Vizuri!"                 │
│             (Recorded! Today you made KES 450         │
│              sales. Cost: KES 130. Profit: KES 320.) │
│                                                      │
│  [Animated: data flows into charts, insights appear] │
├─────────────────────────────────────────────────────┤
│ THE M-KOPA PARALLEL                                 │
│                                                      │
│  Side-by-side comparison:                            │
│  ┌─────────────────┬─────────────────┐               │
│  │    M-KOPA        │    MSAIDIZI     │               │
│  ├─────────────────┼─────────────────┤               │
│  │ Solar panels    │ Voice tracking  │               │
│  │ Daily payments  │ Daily speaking  │               │
│  │ Payment history │ Business history│               │
│  │ Credit score    │ Business proof  │               │
│  │ Loans & finance │ Credit, insurance│              │
│  │ $2B unlocked    │ Economy visible │               │
│  │ 10M customers   │ 10M workers     │               │
│  └─────────────────┴─────────────────┘               │
│                                                      │
│  "8 years for the first million. 6 years for nine    │
│   million more. It was never about phones —           │
│   it was about proof."                               │
│                                                      │
│  "It was never about the app — it was about making    │
│   invisible workers visible."                        │
├─────────────────────────────────────────────────────┤
│ THE PROOF FLYWHEEL (animated)                        │
│                                                      │
│  Circular diagram:                                   │
│                                                      │
│     SPEAK ──→ TRACK ──→ PROVE ──→ UNLOCK ──→ GROW   │
│      ↑                                        │      │
│      └────────────────────────────────────────┘      │
│                                                      │
│  🎤 SPEAK — "Niliuza nyanya kilo tatu, mia mbili"    │
│     The worker speaks naturally. No forms.            │
│                                                      │
│  📊 TRACK — Msaidizi records, categorizes, analyzes  │
│     Every transaction builds the picture.             │
│                                                      │
│  📋 PROVE — Business activity becomes verifiable     │
│     "This business has 90 days of consistent sales." │
│                                                      │
│  🔓 UNLOCK — Credit, insurance, market access        │
│     Proof unlocks what invisibility couldn't.         │
│                                                      │
│  🌱 GROW — Better decisions, more visibility         │
│     The business grows. The economy becomes visible.  │
│                                                      │
│  "Every word is proof. Every day builds more."       │
├─────────────────────────────────────────────────────┤
│ THE STACKING EFFECT                                  │
│                                                      │
│  "Start with one sale. Unlock everything."           │
│                                                      │
│  Visual: Vertical timeline / staircase               │
│                                                      │
│  Day 1:   🎤 "Niliuza nyanya, KES 450"              │
│           → Voice tracking works immediately          │
│                                                      │
│  Week 2:  📊 "Your profit is up 15%"                 │
│           → Business insights appear                  │
│                                                      │
│  Month 1: 💳 "Your business qualifies for a loan"    │
│           → Credit proof builds automatically         │
│                                                      │
│  Month 3: 🛡️ "Insurance access unlocked"             │
│           → You didn't apply. It unlocked.            │
│                                                      │
│  Month 6: 📈 "Tomatoes will be scarce next week"     │
│           → Market intelligence arrives               │
│                                                      │
│  Year 1:  🌍 Full economic profile                    │
│           → Visible. Credible. Empowered.             │
│                                                      │
│  "You don't apply for these. They unlock."           │
│  "M-KOPA didn't ask customers to build credit.       │
│   Payments did it automatically. Same here."         │
├─────────────────────────────────────────────────────┤
│ INTERACTIVE DEMO                                     │
│  Animated phone mockup showing:                      │
│                                                      │
│  User: "Niliuza nyanya kilo tatu, mia mbili"         │
│        (I sold 3kg tomatoes for 200)                 │
│                                                      │
│  Msaidizi: "Imerekodwa! Leo umepata KES 450          │
│             mauzo. Gharama ni KES 130.               │
│             Faida: KES 320. Vizuri!"                 │
│             (Recorded! Today you made KES 450         │
│              sales. Cost: KES 130. Profit: KES 320.) │
│                                                      │
│  [Animated: data flows into charts, insights appear] │
│  [Animated: "Day 47 — proof milestone reached"]      │
├─────────────────────────────────────────────────────┤
│ WHAT MAKES IT A "SUPERAGENT"                         │
│  vs. a regular app:                                  │
│  ┌───────────────┬──────────────┐                    │
│  │ Regular App   │ Superagent   │                    │
│  ├───────────────┼──────────────┤                    │
│  │ You use it    │ It helps you │                    │
│  │ Static        │ Learns       │                    │
│  │ Forms/typing  │ Voice-first  │                    │
│  │ Needs internet│ Works offline│                    │
│  │ One task      │ Many tasks   │                    │
│  │ Same for all  │ Knows YOU    │                    │
│  │ No proof      │ Builds proof │                    │
│  │ No unlocking  │ Unlocks access│                   │
│  └───────────────┴──────────────┘                    │
└─────────────────────────────────────────────────────┘
```

---

#### PAGE 4: `for-workers.html` — Worker Value Prop

**URL:** `/for-workers`
**Purpose:** Direct pitch to Mama Mboga, boda boda riders, mama fua, etc.
**M-KOPA Frame:** "You don't need to understand credit scores. You just need to speak. The proof builds itself."

**Content Structure:**

```
┌─────────────────────────────────────────────────────┐
│ HERO                                                 │
│  H1: "Biashara Yako, Inayoeleweka"                  │
│      (Your Business, Understood)                     │
│  Sub: The superagent that speaks your language,       │
│       knows your business, works without internet.   │
├─────────────────────────────────────────────────────┤
│ USE CASE STORIES                                     │
│                                                      │
│  👩‍🌾 Mama Mboga (Vegetable Seller)                    │
│  "Nilikuwa sijui kama napata faida. Sasa Msaidizi    │
│   ananiambia kila siku."                             │
│  (I didn't know if I was making profit. Now          │
│   Msaidizi tells me every day.)                      │
│  → Daily profit tracking via voice                   │
│  → "Your tomatoes cost more this week — suppliers    │
│     raised prices"                                   │
│                                                      │
│  🏍️ Boda Boda Rider                                  │
│  "Gari inahitaji mafuta. Msaidizi ananiambia         │
│   nitafute pesa ngapi leo."                          │
│  (The bike needs fuel. Msaidizi tells me how much    │
│   I need to earn today.)                             │
│  → Expense tracking + daily targets                  │
│  → Fuel cost optimization                            │
│                                                      │
│  👩‍🍳 Mama Fua (Laundry Worker)                        │
│  "Wateja wangu wananiambia bei za wengine.            │
│   Msaidizi anasaidia kupanga bei yangu."             │
│  (My customers tell me competitors' prices.           │
│   Msaidizi helps me set my prices.)                  │
│  → Competitive pricing intelligence                  │
│  → Customer tracking                                 │
├─────────────────────────────────────────────────────┤
│ FEATURES FOR WORKERS                                 │
│  🎤 Speak in Kiswahili, Sheng, or English             │
│  📊 See today's profit at a glance                    │
│  💡 Get advice: "Buy sukuma today — prices will rise" │
│  🔔 Reminders: "Pay rent on Friday"                   │
│  📈 Weekly reports: "This week was better by 15%"     │
│  🆓 Free forever. No hidden fees.                     │
├─────────────────────────────────────────────────────┤
│ THE PROOF STORY (M-KOPA parallel for workers)        │
│                                                      │
│  "M-KOPA started with one solar panel.                │
│   One daily payment. One customer at a time.          │
│   10 million customers later, $2B in credit unlocked. │
│                                                      │
│   Msaidizi starts with one sale spoken aloud.          │
│   One daily voice note. One worker at a time.         │
│   10 million workers later, an economy becomes visible."
│                                                      │
│  [Visual: M-KOPA solar panel → Msaidizi voice note]  │
├─────────────────────────────────────────────────────┤
│ HOW TO START (the smallest action)                   │
│  1. Download Msaidizi (65MB)                          │
│  2. Open and speak your name                          │
│  3. Tell it what you sell                              │
│  4. Start talking — "Niliuza leo..."                  │
│  That's it. No account. No internet. No typing.       │
│                                                      │
│  "This is your M-KOPA moment.                         │
│   The smallest action that starts the biggest journey."│
├─────────────────────────────────────────────────────┤
│ WHAT UNLOCKS OVER TIME                               │
│                                                      │
│  You don't apply. It unlocks.                         │
│                                                      │
│  Week 1:  ✅ Business tracking works                   │
│  Week 4:  ✅ "Your profit is up 15%"                   │
│  Month 2: ✅ "You qualify for a KES 5,000 loan"        │
│  Month 4: ✅ Insurance access                          │
│  Month 6: ✅ Market intelligence                       │
│                                                      │
│  "M-KOPA didn't teach customers about credit scores.   │
│   Payments built the score automatically.              │
│   Msaidizi doesn't teach you about business analytics.
│   Speaking builds the proof automatically."            │
├─────────────────────────────────────────────────────┤
│ DOWNLOAD CTA                                         │
└─────────────────────────────────────────────────────┘

---

#### PAGE 5: `for-businesses.html` — Intelligence Products

**URL:** `/for-businesses`
**Purpose:** Showcase B2B/B2G intelligence products. Revenue model visibility.

**Content Structure:**

```
┌─────────────────────────────────────────────────────┐
│ HERO                                                 │
│  H1: "Economic Intelligence Products"                │
│      (SW: "Bidhaa za Ufahamu wa Kiuchumi")           │
│  Sub: Real-time market data from the ground up.       │
│       Not surveys. Not estimates. Actual transactions.│
├─────────────────────────────────────────────────────┤
│ SOKO PULSE — Market Intelligence                     │
│                                                      │
│  What it is: Real-time pricing and demand data        │
│  from millions of informal transactions.             │
│                                                      │
│  Who it's for: FMCG companies, supply chains,         │
│  agricultural buyers, logistics companies.            │
│                                                      │
│  What you get:                                       │
│  • Real-time commodity prices by location            │
│  • Demand patterns and seasonality                   │
│  • Supply chain optimization signals                 │
│  • Hyperlocal market intelligence                    │
│                                                      │
│  "Know what Mama Mboga is selling before              │
│   the supply chain does."                            │
│                                                      │
│  [Request Access →]                                  │
├─────────────────────────────────────────────────────┤
│ ALAMA SCORE — Business Credit Intelligence           │
│                                                      │
│  What it is: Business viability scores for            │
│  informal businesses — based on actual activity.     │
│                                                      │
│  Who it's for: Banks, microfinance, mobile lenders,   │
│  insurance companies.                                │
│                                                      │
│  What you get:                                       │
│  • Business activity scores (not personal credit)    │
│  • Revenue estimates from transaction patterns       │
│  • Risk assessment based on business behavior        │
│  • Lending recommendations                           │
│                                                      │
│  "Score the business, not the person."               │
│                                                      │
│  [Request Access →]                                  │
├─────────────────────────────────────────────────────┤
│ ANGAVU PULSE — Economic Activity Index               │
│                                                      │
│  What it is: Macro-level economic activity indices    │
│  derived from aggregated informal economy data.      │
│                                                      │
│  Who it's for: Government agencies, development       │
│  organizations, researchers, policy makers.          │
│                                                      │
│  What you get:                                       │
│  • Regional economic activity indices                │
│  • Sector-level performance metrics                  │
│  • Early warning signals for economic shifts         │
│  • Policy impact measurement                         │
│                                                      │
│  "See the economy that GDP doesn't measure."         │
│                                                      │
│  [Request Access →]                                  │
├─────────────────────────────────────────────────────┤
│ HOW THE DATA FLOWS                                   │
│                                                      │
│  Worker speaks → Transaction recorded →              │
│  Aggregated (anonymized) → Intelligence products     │
│                                                      │
│  🔒 Individual data NEVER leaves the phone.           │
│  📊 Only aggregated, anonymized patterns are shared.  │
│  ✅ Workers opt-in and benefit from participation.    │
├─────────────────────────────────────────────────────┤
│ PRICING TIERS (placeholder)                          │
│  Free tier: Basic market data (delayed)              │
│  Pro: Real-time data, API access                     │
│  Enterprise: Custom feeds, dedicated support         │
├─────────────────────────────────────────────────────┤
│ CONTACT / REQUEST ACCESS CTA                         │
└─────────────────────────────────────────────────────┘
```

---

#### PAGE 6: `for-government.html` — Government Tools

**URL:** `/for-government`
**Purpose:** Show value for policy makers and economic planners.
**M-KOPA Frame:** "M-KOPA proved the underserved are bankable. We prove the informal economy is measurable."

**Content Structure:**

```
┌─────────────────────────────────────────────────────┐
│ HERO                                                 │
│  H1: "Economic Visibility for Policy"                │
│      (SW: "Mwonekano wa Uchumi kwa Sera")            │
│  Sub: See the informal economy. Measure what          │
│       matters. Design policy with real data.         │
├─────────────────────────────────────────────────────┤
│ THE PROBLEM GOVERNMENT FACES                         │
│  • 83% of Africa's workforce is invisible to data    │
│  • GDP estimates miss the informal economy           │
│  • Policy decisions based on outdated surveys        │
│  • No real-time economic pulse for rural areas       │
├─────────────────────────────────────────────────────┤
│ WHAT ANGAVU PROVIDES                                 │
│                                                      │
│  📊 Economic Activity Dashboard                      │
│  Real-time economic activity by county/sub-county    │
│                                                      │
│  📈 Sector Performance Tracking                      │
│  How is retail, transport, agriculture performing?   │
│                                                      │
│  ⚠️ Early Warning System                             │
│  Detect economic distress before it becomes crisis   │
│                                                      │
│  📋 Policy Impact Measurement                        │
│  Did the subsidy program work? Measure it.           │
│                                                      │
│  🗺️ Hyperlocal Economic Maps                         │
│  Economic activity down to market level              │
├─────────────────────────────────────────────────────┤
│ THE M-KOPA PROOF FOR GOVERNMENT
│
│  "M-KOPA showed that people the banking system
│   dismissed were actually reliable payers.
│   $2B in credit, 10 million customers.
│
│   Angavu shows that workers the GDP ignores are
│   actually economic participants.
│   Millions of transactions. Real economic activity.
│   Measured for the first time."
├─────────────────────────────────────────────────────┤
│ CASE STUDY: MIGORI COUNTY                            │
│  (Placeholder for real data from pilot)              │
│  "In the first 3 months, Angavu captured economic    │
│   activity from 500+ informal businesses in Migori.  │
│   This data has never existed before."               │
├─────────────────────────────────────────────────────┤
│ DATA GOVERNANCE                                      │
│  • All data aggregated and anonymized                │
│  • Individual businesses never identified            │
│  • Compliant with Kenya Data Protection Act 2019     │
│  • Workers consent to aggregated data use            │
├─────────────────────────────────────────────────────┤
│ PARTNERSHIP / CONTACT CTA                            │
└─────────────────────────────────────────────────────┘
```

---

#### PAGE 7: `technology.html` — Architecture (Simplified)

**URL:** `/technology`
**Purpose:** Technical credibility for developers, partners, investors. Simplified public view.

**Content Structure:**

```
┌─────────────────────────────────────────────────────┐
│ HERO                                                 │
│  H1: "How It's Built"                                │
│      (SW: "Jinsi Imejengwa")                         │
│  Sub: On-device AI. No cloud dependency.             │
│       Privacy by architecture, not by policy.        │
├─────────────────────────────────────────────────────┤
│ ARCHITECTURE DIAGRAM                                 │
│                                                      │
│  ┌─────────────────────────────────────────────┐     │
│  │              Msaidizi App                    │     │
│  │  ┌───────────────────────────────────────┐  │     │
│  │  │ Voice Interface (STT + TTS)           │  │     │
│  │  │ • On-device speech recognition        │  │     │
│  │  │ • Kiswahili, English, Sheng           │  │     │
│  │  └───────────────────────────────────────┘  │     │
│  │  ┌───────────────────────────────────────┐  │     │
│  │  │ Intelligence Engine                    │  │     │
│  │  │ • Transaction understanding (NLU)     │  │     │
│  │  │ • Pattern recognition                 │  │     │
│  │  │ • Business advice generation          │  │     │
│  │  └───────────────────────────────────────┘  │     │
│  │  ┌───────────────────────────────────────┐  │     │
│  │  │ Local Data Store                       │  │     │
│  │  │ • All data on-device                  │  │     │
│  │  │ • Encrypted at rest                   │  │     │
│  │  │ • Optional cloud sync (user choice)   │  │     │
│  │  └───────────────────────────────────────┘  │     │
│  └─────────────────────────────────────────────┘     │
│                      │                               │
│              [Optional Sync]                         │
│                      │                               │
│  ┌─────────────────────────────────────────────┐     │
│  │           Angavu Cloud (Optional)            │     │
│  │  • Aggregated, anonymized data only          │     │
│  │  • Powers Soko Pulse, Alama Score            │     │
│  │  • Worker controls what is shared            │     │
│  └─────────────────────────────────────────────┘     │
├─────────────────────────────────────────────────────┤
│ KEY TECHNICAL CHOICES                                │
│                                                      │
│  🔒 On-Device AI                                     │
│  Models run on the phone. No data sent to servers.   │
│  Privacy by architecture.                            │
│                                                      │
│  📦 Progressive Model Loading                        │
│  Lite APK (65MB) → downloads models as needed.       │
│  Core works instantly. Gets smarter over time.       │
│                                                      │
│  🗣️ Voice-First NLU                                  │
│  Natural language understanding built for African    │
│  languages. Not adapted from English models.         │
│                                                      │
│  📴 Offline-First Architecture                       │
│  Every feature works without internet.               │
│  Sync is optional, never required.                   │
│                                                      │
│  🧠 Continuous Learning                              │
│  The agent learns your business patterns.            │
│  Personalization happens on-device.                  │
├─────────────────────────────────────────────────────┤
│ TECH STACK (simplified)                              │
│  Mobile: Android (Kotlin/Java)                       │
│  AI: On-device inference (TensorFlow Lite / ONNX)    │
│  Voice: Custom STT/TTS for Kiswahili                 │
│  Storage: SQLite + encrypted local store             │
│  Cloud: Python/FastAPI (optional sync + APIs)        │
├─────────────────────────────────────────────────────┤
│ OPEN SOURCE / GITHUB CTA                             │
│  "We believe in building in the open."               │
│  [View on GitHub →]                                  │
└─────────────────────────────────────────────────────┘
```

---

#### PAGE 8: `privacy.html` — Privacy Philosophy

**URL:** `/privacy`
**Purpose:** Build trust. Explain privacy-first design.

**Content Structure:**

```
┌─────────────────────────────────────────────────────┐
│ HERO                                                 │
│  H1: "Your Data. Your Phone. Your Control."          │
│      (SW: "Data Yako. Simu Yako. Udhibiti Wako.")   │
├─────────────────────────────────────────────────────┤
│ THE PROMISE                                          │
│  1. All data stays on your phone                     │
│  2. No account required                              │
│  3. No phone number needed                           │
│  4. No internet required for core features           │
│  5. No ads. No tracking. No selling data.            │
│  6. You choose what (if anything) to share           │
├─────────────────────────────────────────────────────┤
│ HOW PRIVACY WORKS                                    │
│  On-device AI: Models run locally. Your voice,       │
│  your transactions, your patterns — all on-device.   │
│                                                      │
│  Optional sync: If you want backup, you choose       │
│  what to sync. Encrypted. Your key.                  │
│                                                      │
│  Aggregated intelligence: Soko Pulse and Alama       │
│  Score use anonymized, aggregated data only.         │
│  Your individual data is never identifiable.         │
├─────────────────────────────────────────────────────┤
│ LEGAL                                                │
│  Compliant with:                                     │
│  • Kenya Data Protection Act, 2019                   │
│  • GDPR principles (for international users)         │
│  • African Union Convention on Cyber Security        │
├─────────────────────────────────────────────────────┤
│ TRANSPARENCY                                         │
│  "We don't just promise privacy — we architect for   │
│   it. If we can't see your data, we can't leak it."  │
└─────────────────────────────────────────────────────┘
```

---

#### PAGE 9: `api.html` — Developer API (Enhanced from current)

**URL:** `/api`
**Purpose:** Developer documentation for intelligence products.

**Content Structure:** Keep current api.html structure but add:
- Authentication flow (API keys)
- Rate limiting documentation
- SDKs (Python, JavaScript)
- Webhook support
- Sandbox environment
- Code examples for each endpoint

---

## 3. CSS Architecture

### 3.1 File Structure (replacing monolithic `style.min.css`)

```
css/
├── base.css              # Reset, variables, typography, utilities (~3KB)
├── components.css        # Reusable: cards, buttons, nav, forms (~5KB)
├── pages.css             # Page-specific overrides (~4KB)
└── animations.css        # All keyframes, transitions (~2KB)
```

### 3.2 Design Tokens (CSS Custom Properties)

```css
:root {
    /* === COLORS (keep existing, extend) === */
    --bg-primary: #1B4965;          /* Deep teal — keep */
    --bg-secondary: #163D55;        /* Darker teal — keep */
    --bg-card: #1E4F6B;             /* Card background — keep */
    --bg-card-hover: #245A78;       /* Card hover — keep */
    --bg-accent: #2A6F99;           /* Accent bg — keep */
    
    --text-primary: #f0ece4;        /* Warm white — keep */
    --text-secondary: #b8ccd8;      /* Muted text — keep */
    --text-muted: #8aa3b5;          /* Dimmed text — keep */
    --text-inverse: #0F2D42;        /* Dark text on light — keep */
    
    --accent-gold: #E8A838;         /* Gold — keep */
    --accent-gold-light: #F0C060;   /* Gold hover — keep */
    --accent-gold-dark: #D4942E;    /* Gold active — keep */
    
    /* NEW: Success green for download CTAs */
    --accent-green: #22c55e;
    --accent-green-hover: #16a34a;
    --accent-green-glow: rgba(34, 197, 94, 0.3);
    
    /* NEW: Superagent accent — electric blue for tech pages */
    --accent-blue: #38bdf8;
    --accent-blue-glow: rgba(56, 189, 248, 0.15);
    
    /* === BORDERS === */
    --border-subtle: rgba(255, 255, 255, 0.06);
    --border-light: rgba(255, 255, 255, 0.1);
    --border-gold: rgba(232, 168, 56, 0.25);
    
    /* === TYPOGRAPHY === */
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-display: 'Playfair Display', Georgia, serif;
    
    /* === SPACING === */
    --section-padding: 120px;
    --container-max: 1200px;
    --gap-sm: 16px;
    --gap-md: 24px;
    --gap-lg: 48px;
    --gap-xl: 80px;
    
    /* === TRANSITIONS === */
    --transition-fast: 0.2s ease;
    --transition-base: 0.3s ease;
    --transition-slow: 0.5s ease;
    
    /* === RADII === */
    --radius-sm: 6px;
    --radius-md: 12px;
    --radius-lg: 20px;
    --radius-xl: 32px;
    
    /* === SHADOWS === */
    --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.2);
    --shadow-card-hover: 0 20px 60px rgba(0, 0, 0, 0.3);
    --shadow-glow-gold: 0 0 40px rgba(232, 168, 56, 0.15);
    --shadow-glow-green: 0 8px 40px rgba(34, 197, 94, 0.3);
}
```

### 3.3 Component Patterns

**Reusable Card:**
```css
.card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 36px;
    transition: all var(--transition-base);
}
.card:hover {
    border-color: var(--border-gold);
    transform: translateY(-4px);
    box-shadow: var(--shadow-card-hover);
}
```

**CTA Button (Download):**
```css
.btn-download {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: var(--accent-green);
    color: #fff;
    font-size: 1.1rem;
    font-weight: 700;
    padding: 18px 40px;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-glow-green);
    transition: all var(--transition-base);
}
.btn-download:hover {
    background: var(--accent-green-hover);
    transform: translateY(-2px);
    box-shadow: 0 12px 50px rgba(34, 197, 94, 0.4);
}
```

**Section Pattern:**
```css
.section {
    padding: var(--section-padding) 0;
}
.section-head {
    text-align: center;
    max-width: 700px;
    margin: 0 auto var(--gap-xl);
}
.kicker {
    font-family: var(--font-sans);
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: var(--accent-gold);
    margin-bottom: 16px;
}
.accent {
    color: var(--accent-gold);
}
```

---

## 4. JavaScript Architecture

### 4.1 File Structure

```
js/
├── app.js                # Main entry: nav, lang, scroll effects
├── lang.js               # Multilingual system (data-sw/data-en + more)
└── components.js         # Shared components (navbar, footer injection)
```

### 4.2 Multilingual System

The current `data-sw`/`data-en` attribute system works well. Extend it:

```javascript
// Supported languages
const LANGUAGES = {
    sw: { flag: '🇰🇪', name: 'Kiswahili', dir: 'ltr' },
    en: { flag: '🇬🇧', name: 'English', dir: 'ltr' },
    // Future:
    // am: { flag: '🇪🇹', name: 'አማርኛ', dir: 'ltr' },
    // ha: { flag: '🇳🇬', name: 'Hausa', dir: 'ltr' },
    // ar: { flag: '🇪🇬', name: 'العربية', dir: 'rtl' },
};

function setLang(lang) {
    document.body.className = `lang-${lang}`;
    document.documentElement.lang = lang;
    document.documentElement.dir = LANGUAGES[lang].dir;
    localStorage.setItem('angavu-lang', lang);
    
    // Update all elements with data-{lang} attributes
    document.querySelectorAll(`[data-${lang}]`).forEach(el => {
        el.innerHTML = el.getAttribute(`data-${lang}`);
    });
    
    // Announce for screen readers
    const announcement = document.getElementById('lang-announcement');
    if (announcement) {
        announcement.textContent = `Language changed to ${LANGUAGES[lang].name}`;
    }
}
```

### 4.3 Shared Components (Navbar/Footer)

Instead of duplicating navbar HTML across 8 pages, inject via JS:

```javascript
// components.js — inject shared nav and footer
function injectNavbar(currentPage) {
    const nav = document.getElementById('navbar');
    nav.innerHTML = `
        <div class="nav-container">
            <a href="/" class="nav-logo">
                <span class="logo-icon">◆</span>
                <span>Angavu<span class="logo-accent"> Intelligence</span></span>
            </a>
            <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation">
                <span></span><span></span><span></span>
            </button>
            <ul class="nav-menu" id="navMenu">
                <li><a href="/how-it-works" data-sw="Jinsi Inavyofanya Kazi" data-en="How It Works">Jinsi Inavyofanya Kazi</a></li>
                <li><a href="/for-workers" data-sw="Kwa Wafanyakazi" data-en="For Workers">Kwa Wafanyakazi</a></li>
                <li><a href="/for-businesses" data-sw="Kwa Biashara" data-en="For Businesses">Kwa Biashara</a></li>
                <li><a href="/for-government" data-sw="Kwa Serikali" data-en="For Government">Kwa Serikali</a></li>
                <li><a href="/download" data-sw="Pakua" data-en="Download" class="btn-nav-download">Pakua</a></li>
                <li><button class="lang-toggle" id="langToggle" aria-label="Switch language">🇰🇪 EN</button></li>
            </ul>
        </div>
    `;
}
```

**Alternative (no-JS fallback):** For maximum SEO and no-JS support, inline the navbar in each HTML file. The component injection approach is optional enhancement.

---

## 5. Content Strategy

### 5.0 The M-KOPA Lesson — Our Central Narrative

M-KOPA's story is our story. They didn't sell solar panels or smartphones — they sold **proof**.
- Started with solar panels (everyone needs energy) → pivoted to smartphones (everyone needs a phone)
- 8 years for first million → 6 years for nine million more
- "It was never really about phones. It was about proof."
- 10 million customers, $2B credit unlocked, 2M payments/day

**The parallel:** If M-KOPA proved daily payments build credit, **Msaidizi proves daily voice recordings build business intelligence.**

**Content strategy across the site:**
1. **Lead with the problem** — Invisibility costs money, opportunity, and dignity
2. **Show the proof model** — M-KOPA parallel: small daily actions → proof → unlock → growth
3. **Offer the solution** — Msaidizi superagent: speak → track → prove → unlock → grow → repeat

**The Proof Flywheel (central to every page):**
```
┌─────────────────────────────────────────────────┐
│                                                   │
│   SPEAK ──→ TRACK ──→ PROVE ──→ UNLOCK ──→ GROW  │
│    ↑                                      │      │
│    └──────────────────────────────────────┘      │
│                                                   │
│   "Every word is proof. Every day builds more."   │
│                                                   │
└─────────────────────────────────────────────────┘
```

**The Stacking Effect (what workers unlock over time):**
- **Day 1:** Voice tracking — "Niliuza nyanya, KES 450"
- **Week 2:** Business insights — "Your profit is up 15%"
- **Month 1:** Credit proof — "Your business qualifies for a loan"
- **Month 3:** Insurance access — "Your business activity qualifies you"
- **Month 6:** Market intelligence — "Tomatoes will be scarce next week"
- **Year 1:** Full economic profile — visible, credible, empowered

**The download = M-KOPA's first phone purchase:**
The smallest action that starts the journey. Not a commitment. Not a sign-up. Just a tap that begins the proof.

### 5.1 Brand Messaging Framework

| Element | Current | New |
|---------|---------|-----|
| **Tagline** | "Biashara Yako. Sauti Yako." | "Your Business, Understood." / "Biashara Yako, Inayoeleweka." |
| **Positioning** | Business assistant app | Superagent for informal workers |
| **Key Differentiator** | Voice + offline | Voice-first, offline-first, gets smarter |
| **Audience** | Mama Mboga, boda boda | Workers + Businesses + Government |
| **Value Prop** | Track sales via voice | Economic intelligence platform |
| **Emotional Hook** | "Free forever" | "10 million invisible workers will become visible" |
| **Proof Model** | None | M-KOPA parallel: daily actions → proof → unlock |

### 5.2 Messaging by Audience

**Workers (Primary):**
- "Speak to your phone. Msaidizi understands."
- "Your business CFO — free, offline, in your language."
- "No typing. No internet. No fees. Just speak."
- "Every sale you speak becomes proof. Proof unlocks opportunities."
- "Start small. Speak one sale. Watch what happens."

**Businesses (B2B):**
- "Real market data from real transactions."
- "Not surveys. Not estimates. Actual economic activity."
- "Know the informal economy before your competitors do."
- "If M-KOPA proved payments build credit, we prove voice builds market intelligence."

**Government (B2G):**
- "See the 83% of the economy that's invisible."
- "Policy decisions backed by real-time economic data."
- "Measure what matters — down to the market level."
- "10 million invisible workers will become visible."

### 5.3 SEO Strategy

**Primary Keywords (English):**
- "informal economy app africa"
- "business tracking app kenya"
- "voice business assistant"
- "offline business app"
- "economic intelligence africa"

**Primary Keywords (Kiswahili):**
- "app ya biashara"
- "msaidizi wa biashara"
- "fuatilia mauzo"
- "app ya mama mboga"

**Meta Description Pattern:**
```
Msaidizi — the superagent for informal workers. Voice-first, offline-first, 
gets smarter. Track your business by speaking. Free forever. By Angavu Intelligence.
```

### 5.4 Social Proof Strategy

- Testimonials from pilot users (Migori county)
- Usage statistics (when available): "X transactions tracked"
- Partner logos (when available)
- GitHub stars/activity
- Media mentions

---

## 6. File Manifest (Implementation Order)

### Phase 1: Foundation (Week 1)
```
index.html              # Rewrite with new architecture
css/base.css            # Extract from style.min.css
css/components.css      # Extract reusable components
css/pages.css           # Page-specific styles
css/animations.css      # Extract animations
js/app.js               # Core JS (nav, lang, scroll)
js/lang.js              # Multilingual system
manifest.json           # Update PWA manifest
```

### Phase 2: Core Pages (Week 2)
```
download.html           # New download experience
how-it-works.html       # Flywheel + demo
for-workers.html        # Worker value prop
```

### Phase 3: Intelligence Pages (Week 3)
```
for-businesses.html     # Soko Pulse, Alama Score
for-government.html     # Economic visibility
technology.html         # Architecture overview
privacy.html            # Privacy philosophy
api.html                # Enhanced API docs
```

### Phase 4: Assets & Polish (Week 4)
```
assets/og-superagent.png     # New OG image
assets/qr-download.svg       # Update QR code
assets/diagrams/             # Business flow diagram
assets/diagrams/flywheel.svg
assets/diagrams/architecture.svg
assets/screenshots/          # App screenshots
assets/testimonials/         # User photos (with consent)
```

---

## 7. Technical Decisions

### 7.1 Static Site (Keep)
GitHub Pages = static hosting. No build step needed. This is correct for the current scale.

### 7.2 CSS Split (New)
Replace monolithic `style.min.css` with 4 focused files:
- Better caching (components.css rarely changes)
- Easier maintenance
- Page-specific overrides don't bloat shared styles

### 7.3 No Framework (Keep)
Plain HTML/CSS/JS. No React, no Next.js. The site is marketing pages — frameworks add complexity without benefit at this scale.

### 7.4 Multilingual (Extend)
Keep the `data-sw`/`data-en` attribute system. Add `data-{lang}` for new languages. The JS toggles visibility via CSS class on `<body>`.

### 7.5 Download URL Strategy
- **Current:** Direct GitHub releases link
- **New:** Keep GitHub releases, but consider a redirect URL like `download.angavu.ai` that points to the latest release
- **APK naming:** `msaidizi-lite-v{VERSION}.apk` (lite = ~65MB, no bundled models)

### 7.6 Analytics (Consider)
- No third-party trackers (privacy commitment)
- Self-hosted Plausible or Umami if analytics needed
- GitHub Pages provides basic traffic stats

---

## 8. Migration Path

### What to Keep
- Color system (`--bg-primary`, `--accent-gold`, etc.)
- Typography (Inter + Playfair Display)
- Phone mockup component
- Trust badges pattern
- Accessibility features (skip link, ARIA, focus-visible, reduced-motion)
- Security headers (CSP, referrer policy)
- Language toggle mechanism

### What to Change
- Hero messaging (assistant → superagent)
- Navigation structure (flat → audience-segmented)
- Download flow (single APK → lite-first progressive)
- Add intelligence product pages (B2B/B2G)
- Add flywheel/technology explanation
- Split CSS into focused files
- Update OG images and meta descriptions

### What to Remove
- References to "app ya biashara" as primary positioning (upgrade to "superagent")
- Single-page scroll approach (move to multi-page)
- WhatsApp float button (keep share, remove persistent float)

---

## 9. Success Metrics

| Metric | Current Baseline | Target (3 months) |
|--------|-----------------|-------------------|
| Pages | 4 | 9 |
| Download conversion | Unknown | >5% of visitors |
| Proof milestones | N/A | Track Day 1/Week 4/Month 1 unlock rates |
| Bounce rate | Unknown | <40% |
| Time on site | Unknown | >2 minutes |
| API page visits | Unknown | >100/month |
| Language usage | SW only | SW 60% / EN 35% / Other 5% |
| Business inquiries | 0 | >5/month via for-businesses |

---

## 10. Open Questions for Team

1. **APK size:** Current is ~500MB. Target lite is ~65MB. Is this achievable with current model compression?
2. **Domain:** angavu-intelligence.github.io vs custom domain (angavu.ai)?
3. **OG image:** Need new superagent-themed OG image (1200×630px)
4. **Testimonials:** Do we have pilot user quotes with consent to publish?
5. **Business products:** Are Soko Pulse and Alama Score ready for "Request Access" forms?
6. **API authentication:** API key system ready? Or still placeholder?
7. **Analytics:** Self-hosted or none?
8. **Timeline:** 4-week phased rollout acceptable?
9. **M-KOPA partnership:** Any existing relationship? Their model validates ours.
10. **Proof milestones:** What specific unlock thresholds do we set for credit/insurance access?

---

*This document is the architectural blueprint. Implementation begins with Phase 1 (CSS extraction + index.html rewrite). All content is bilingual (SW/EN) by default.*
