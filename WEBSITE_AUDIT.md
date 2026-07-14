# WEBSITE AUDIT — Angavu Intelligence
**Date:** 2026-07-15
**Auditor:** AI Subagent
**Scope:** index.html, all linked docs/, research/, strategy files

---

## EXECUTIVE SUMMARY

The website is **fundamentally misaligned** with its purpose. It reads like an internal strategy document, investor pitch, and technical architecture spec — all at once, all in public. A market vendor in Migori would not understand this. A competitor would understand *everything*.

**Critical finding:** The repo contains strategy documents (SATOSHI_STRATEGY.md, ALAMA_SCORE_POSITIONING.md) that explicitly describe deceiving regulators and hiding the product's true nature. If these files are in the same GitHub repo as the public website, they are one URL guess away from a PR catastrophe.

---

## 🔴 REMOVAL LIST — What Must Be Removed or Completely Rewritten

### 1. [CRITICAL] "Satoshi Strategy" & Related Internal Docs
**Files:** `docs/SATOSHI_STRATEGY.md`, `docs/SATOSHI_IMPLEMENTATION_PLAN.md`
**Why:** These documents explicitly describe a strategy to deceive regulators ("What the world sees vs. What Angavu actually is"), present a "Trojan Horse" approach, and list tactics like "Position as fintech — the most boring, least threatening category." This is a regulatory and PR time bomb. If a journalist, regulator, or competitor finds these, Angavu is finished.
**Action:** DELETE from the repo immediately. These should never exist in any repository linked to the company.

### 2. [CRITICAL] Alama Score Positioning Document
**File:** `docs/ALAMA_SCORE_POSITIONING.md`
**Why:** Contains a "DO NOT Say" list that is essentially a guide to misleading regulators. Sections like "The product that looks like a calculator but builds like a credit bureau" would be devastating in a regulatory hearing.
**Action:** DELETE from repo. The strategic positioning can live in an internal document system, never in the website repo.

### 3. [CRITICAL] Investor Pitch Deck Outline
**File:** `docs/INVESTOR_PITCH_DECK_OUTLINE.md`
**Why:** Contains revenue projections ($90K-$4.5M), break-even analysis, competitive landscape, moat analysis, fundraising details, and the "ask" slide. This is investor-facing material that should be shared via secure data room, not a public repo.
**Action:** REMOVE from repo. Share via secure channels only.

### 4. [CRITICAL] Break-Even Analysis
**File:** `docs/BREAK_EVEN_ANALYSIS.md`
**Why:** Full cost structure, revenue per client, unit economics, break-even scenarios. This is the kind of document competitors would pay for.
**Action:** REMOVE from repo.

### 5. [CRITICAL] Compliance Cost Moat
**File:** `docs/COMPLIANCE_COST_MOAT.md`
**Why:** Detailed comparison of Angavu's compliance costs vs. competitors. Reveals the exact cost advantage and strategic rationale.
**Action:** REMOVE from repo.

### 6. [CRITICAL] Strategy Document
**File:** `STRATEGY.md`
**Why:** Full strategic framework including monopoly analysis, flywheel economics, data center phases, revenue projections, and "The Vision 2030." Marked "Classification: Internal — Founder Level" yet publicly accessible.
**Action:** REMOVE from repo.

### 7. [CRITICAL] Product Inventory (Honest Version)
**File:** `docs/PRODUCT_INVENTORY.md`
**Why:** Opens with "The '43 data products' claim is marketing, not engineering." Admits 6 aspirational products have no code. This document, while honest internally, would destroy credibility if found externally.
**Action:** REMOVE from repo.

### 8. [HIGH] Full AI Agent Architecture (Website Section)
**Location:** `index.html` — `#ai-agents` section
**Why:** This section exposes the complete multi-agent architecture: 3 tiers, 17 agents with names and functions, 4 reasoning loop systems (OODA, ReAct, Reflexion, Plan-Execute), progressive autonomy details. This is a competitive blueprint. No user needs to know about "Orchestrator Agent" or "OODA loops."
**Action:** REMOVE the entire section. Replace with a simple "How Msaidizi Helps You" section focused on user benefits, not technical architecture.

### 9. [HIGH] Technology Stack Section (Website)
**Location:** `index.html` — `#tech-stack` section
**Why:** Reveals specific model names (Qwen3.5-0.8B, Whisper, Kokoro TTS), cryptographic algorithms (ML-KEM-768, ML-DSA-65), privacy parameters (ε=0.1, k≥5), and implementation details. Competitors can reverse-engineer the approach from this.
**Action:** Simplify drastically. Say "Your data is protected with military-grade encryption" not "ML-KEM-768 key encapsulation."

### 10. [HIGH] AI In-House Section (Website)
**Location:** `index.html` — `#ai-inhouse` section
**Why:** Reveals exact cost comparison ("At 200M users, renting AI costs $10-20M/month. Our approach costs $60-100K/month"), model details, and inference architecture. This is internal cost structure.
**Action:** Simplify to "Our AI runs on your phone — free, fast, private." Remove all cost comparisons and model specifics.

### 11. [HIGH] Infrastructure Roadmap
**Location:** `index.html` — `#infrastructure` section
**Why:** Reveals exact infrastructure phases with dates (2027 ARM server, 2028 Mini DC, 2030 Pan-African DC), capacity numbers, and technology choices. This is a strategic roadmap for competitors to follow.
**Action:** REMOVE or replace with vague "We're building infrastructure that scales with you."

### 12. [HIGH] Academic Foundation Section
**Location:** `index.html` — `#academic` section
**Why:** Lists every course code (ECO 101, STA 341, etc.) the founder took. This is resume-padding, not company positioning. The "42 degree units" framing is confusing — it sounds like a PhD but is actually undergraduate coursework. It makes the company look like a student project.
**Action:** REMOVE the entire section. If academic grounding matters, say "Built on Nobel Prize-winning economics" in one line, not an entire section with course codes.

### 13. [MEDIUM] AGI/Insights Section
**Location:** `index.html` — `#insights` section
**Why:** Claims "AGI Arrival Window: 2027-2028" and cites NVIDIA reports. This is speculative and makes the company sound like a hype-chaser. Also reveals "16-agent architecture" (different from the 17 claimed elsewhere — inconsistency).
**Action:** REMOVE or replace with actual research/insights relevant to the informal economy.

### 14. [MEDIUM] Vision/Monopoly Section
**Location:** `index.html` — `#vision` section
**Why:** Quotes Peter Thiel ("Competition is for losers"), claims "Thiel Monopoly Scorecard: 4/4," lists "6 Moats." This is investor-pitch language on a public website. Users don't care about monopoly theory.
**Action:** REWRITE entirely. Focus on the problem (invisible workers) and the solution (Msaidizi), not competitive strategy.

### 15. [MEDIUM] Founder's WhatsApp Number
**Location:** `index.html` — Multiple locations (contact, floating button, footer)
**Why:** `+254 115 965 493` is a personal phone number exposed on a public website. This is a privacy and safety risk.
**Action:** Use a business WhatsApp number or a contact form. Do not expose personal numbers.

### 16. [MEDIUM] Pricing Details
**Location:** `index.html` — Products section
**Why:** Shows exact pricing ($2,000-$12,000/mo, $0.05-$0.50/query, $15,000-$30,000 one-time) for products still in beta. This locks in pricing before the market is tested and gives competitors a target to undercut.
**Action:** REMOVE all pricing. Say "Contact us for enterprise pricing" or "Custom pricing for your needs."

### 17. [LOW] Excessive Navigation
**Location:** `index.html` — `<nav>` element
**Why:** 16 navigation items is overwhelming. A serious company website has 5-7 nav items max.
**Action:** Consolidate to: Home, Products, Download, About, Contact.

### 18. [HIGH] Kenya AI Strategy Alignment Document
**File:** `docs/KENYA_AI_STRATEGY_ALIGNMENT.md`
**Why:** Contains specific unit economics ($0.013/user/month), exact pitch language for regulators, and the explicit strategy of positioning Angavu as the AI Strategy's proof of concept to gain regulatory immunity. Reveals internal positioning playbook.
**Action:** REMOVE from repo.

### 19. [HIGH] Entire `research/` Folder
**Path:** `research/` (40+ files)
**Why:** Contains internal strategy documents, competitive positioning analysis, swarm reports, implementation plans, model comparison strategies, and "what to reveal vs. protect" analysis. These are R&D internal documents, not public content.
**Action:** Move the entire `research/` folder to a private repo. Keep only public-facing whitepapers or blog posts if needed.

### 20. [HIGH] Entire `docs/` Folder (except public-facing docs)
**Path:** `docs/` (compliance, regulatory, positioning docs)
**Why:** Contains regulatory compliance checklists, DPIA templates, EU AI Act classifications, and implementation plans. Internal regulatory strategy.
**Action:** Move to a private repo. Keep only public-facing documentation.

### 21. [HIGH] Internal Strategy Files in Root
**Files:** `STRATEGY.md`, `MISSION.md`, `BRAND_GUIDELINES.md`, `PROFILE_README.md`
**Why:** These are internal positioning and strategy documents marked "Internal — Founder Level." They reveal strategic thinking, competitive analysis, and internal priorities.
**Action:** Move to private repo. MISSION.md can be simplified into a public "About Us" page.

### 22. [MEDIUM] Backend Deploy Workflow
**File:** `.github/workflows/backend-deploy.yml`
**Why:** Reveals the API endpoint (`api.angavu.ai`), Oracle Cloud deployment details, Docker image registry, and CI/CD pipeline structure. Standard for internal repos but shouldn't be in a public website repo.
**Action:** Move to a private backend repo. Keep only the static site deployment workflow in the public repo.

### 20. [LOW] "PhD-Grade Economics" Claim
**Location:** Multiple sections
**Why:** The founder has a BSc, not a PhD. "PhD-grade" is misleading. It implies the founder has a PhD or the work is equivalent to PhD-level research. It's neither.
**Action:** Replace with "Rigorous economics" or "Built on economic theory" — something defensible.

---

## 🟢 KEEP LIST — What's Good and Should Stay

### 1. ✅ Hero Section (Simplified)
The core message is strong: "The Operating System for 600M+ Invisible Workers." Keep the hero but remove "17 AI Agents" and "PhD-Grade Economics" from the eyebrow.

### 2. ✅ Msaidizi App Section
The `#msaidizi` section is the best part of the website. It speaks to users in plain language: "Track Your Money. Grow Your Business." The voice-first, offline-first, free-forever messaging is exactly right. The testimonial from Mama Achieng is perfect.

### 3. ✅ Download Section
The `#download` section is well-designed and user-focused. Clear requirements, QR code, simple install guide. Keep as-is.

### 4. ✅ Installation Guide
The `#install` section is excellent. Simple steps, Swahili instructions, verification details. This is exactly what the target audience needs.

### 5. ✅ What's New Section
The `#whats-new` section is clean and focused on actual features users care about. Keep it.

### 6. ✅ Privacy Section (Simplified)
The privacy-first message is important for trust. Keep the concept but simplify: "Your data stays on your phone" is the message, not "federated learning with ε=0.1 differential privacy."

### 7. ✅ About Section (Simplified)
The problem statement is compelling: "Africa's informal economy employs over 600 million people and generates an estimated $1.3 trillion in annual output." Keep the problem/solution framing. Remove the "Not Competing. Just Operating." tagline — it's investor language.

### 8. ✅ What We Do Section
The 3-step "Workers Speak → AI Transforms → Stakeholders Act" is clear and compelling. Keep it.

### 9. ✅ Contact Section (Modified)
Keep the contact section but use a business number, not a personal one.

### 10. ✅ Community Section
The WhatsApp community and Migori pilot are good signals. Keep them.

### 11. ✅ Visual Design & CSS
The dark theme, gold accents, and overall visual quality are professional. Keep the design system.

### 12. ✅ Bilingual Support (EN/SW)
The English/Swahili toggle is a strong differentiator. Keep and expand.

### 13. ✅ Brand Assets
The SVG logos, icons, and brand guidelines are well-done. Keep everything in `assets/`.

### 14. ✅ Structured Data / SEO
The JSON-LD schema markup and meta tags are well-implemented. Keep them.

---

## 📋 TONE ANALYSIS

| Aspect | Current State | Problem |
|--------|--------------|---------|
| **Audience** | Mixed: investor + developer + user | Pick ONE primary audience |
| **Tone** | Aggressive, Silicon Valley bro energy | "Competition is for losers" doesn't work in Africa |
| **Length** | ~3,000+ lines of HTML | 3-4x too long for a company website |
| **Clarity** | Would a Migori market vendor understand? **No** | Too much jargon, too many concepts |
| **Trust signals** | Looks like a student project with big claims | "42 degree units" and course codes undermine credibility |
| **Professionalism** | Reads like a manifesto, not a company site | Investor pitch language on public pages |

---

## 📋 SECTION-BY-SECTION SUMMARY

| Section | Verdict | Action |
|---------|---------|--------|
| Hero | 🟡 Good core, too much jargon | Simplify eyebrow and subtitle |
| Vision/Monopoly | 🔴 Investor language | REWRITE or REMOVE |
| About | 🟡 Strong problem statement | Simplify, remove strategy language |
| Academic Foundation | 🔴 Resume-padding | REMOVE entirely |
| What We Do | ✅ Clear and compelling | KEEP |
| Infrastructure | 🔴 Strategic roadmap exposed | REMOVE or simplify drastically |
| AI In-House | 🔴 Cost structure exposed | Simplify to user benefits |
| Technology Stack | 🔴 Implementation details exposed | Simplify to trust signals |
| AI Agents | 🔴 Competitive blueprint exposed | REMOVE entirely |
| Privacy First | 🟡 Good concept, too technical | Simplify language |
| Products | 🔴 Pricing exposed, beta products | Remove pricing, simplify |
| Msaidizi App | ✅ Excellent user messaging | KEEP |
| Download | ✅ Excellent UX | KEEP |
| What's New | ✅ Clean, user-focused | KEEP |
| Install Guide | ✅ Excellent | KEEP |
| Insights/AGI | 🔴 Speculative, hype-chasing | REMOVE or replace |
| Community | ✅ Good trust signal | KEEP |
| Contact | 🟡 Personal number exposed | Use business number |

---

## 🎯 RECOMMENDED NEW STRUCTURE

A serious company website for Msaidizi distribution should have **5-7 sections max**:

1. **Hero** — "Track Your Money. Grow Your Business." Download button front and center.
2. **How It Works** — 3 steps: Speak → Track → Grow. Simple, visual.
3. **Features** — Voice input, offline mode, free, privacy. What users actually get.
4. **Download** — Prominent APK download with QR code.
5. **About** — The problem (600M invisible workers) and who we are.
6. **Contact** — WhatsApp, email, location.

That's it. Everything else is either internal strategy that shouldn't be public, or technical details that scare users.

---

## ⚠️ IMMEDIATE ACTIONS

1. **TODAY:** Delete from the repo: `SATOSHI_STRATEGY.md`, `SATOSHI_IMPLEMENTATION_PLAN.md`, `ALAMA_SCORE_POSITIONING.md`, `INVESTOR_PITCH_DECK_OUTLINE.md`, `BREAK_EVEN_ANALYSIS.md`, `COMPLIANCE_COST_MOAT.md`, `STRATEGY.md`, `PRODUCT_INVENTORY.md`, `KENYA_AI_STRATEGY_ALIGNMENT.md`. These are existential risks.
2. **TODAY:** Move the entire `research/` folder, `docs/` folder, `STRATEGY.md`, `MISSION.md`, `BRAND_GUIDELINES.md`, and `skills/` to a **private repository**. The public repo should contain ONLY the static website files (index.html, CSS, JS, assets).
3. **THIS WEEK:** Strip the website down to the 6 sections above. Remove all technical architecture, pricing, infrastructure roadmap, and academic details.
4. **THIS WEEK:** Replace personal WhatsApp number with a business number.
5. **THIS WEEK:** Remove "PhD-grade" claims. Replace with defensible language.
6. **NEXT WEEK:** Rewrite copy for the primary audience: a market vendor in Migori who wants to track her business.

---

*Audit complete. The website has strong bones (design, brand, core message) but is currently serving as a public-facing strategy document instead of a user-facing product page. The internal documents in the repo are a regulatory and PR crisis waiting to happen.*
