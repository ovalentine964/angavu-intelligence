# IMPL_9: Smart Onboarding — Implementation Complete

## Overview

Msaidizi's onboarding is NOT a technical setup screen. It's Msaidizi meeting Valentine's mum for the first time. A conversation, not a form.

**Status:** ✅ Complete  
**Date:** 2026-07-07  
**Implementation:** 6 Kotlin files created/updated

---

## What Was Built

### 1. WorkerProfile.kt
**Data model for everything Msaidizi learns during onboarding.**

- `msaidiziName` — What the worker names their agent (psychological ownership)
- `workerName` — Worker's name
- `businessType` — Classified using Producer Theory (ECO 201)
- `products` — Specific goods/services offered
- `location` — Market, roadside, home, mobile
- `workingHours` — Time allocation theory (ECO 204)
- `workAlone` — Solo vs team (returns to scale)
- `supplyMethod` — Input procurement (ECO 201)
- `customerFindMethod` — Market access (ECO 204)
- `paymentMethod` — Financial infrastructure (ECO 209)
- `keepsRecords` — Creditworthiness predictor (ECO 206)
- `biggestChallenge` — Free-text, highest signal
- `language` / `dialect` — Communication preferences (BCB 108)
- `classificationConfidence` — Bayesian posterior (STA 142)

**Academic basis:** ECO 101 (Consumer Theory), ECO 201 (Producer Theory), ECO 204 (African Development), STA 142 (Bayesian Inference), BCB 108 (Communication)

### 2. OnboardingConversation.kt
**Voice-first conversation manager — the brain of onboarding.**

**5 Phases:**
1. **Introduction** (~30s) — Msaidizi introduces herself, asks worker's name, worker names Msaidizi
2. **Getting to Know You** (~2-3 min) — Business type, products, location, hours
3. **Understanding Your Business** (~2-3 min) — Supply, customers, payments, records, challenges
4. **Setting Up** (~1-2 min) — Models download in background
5. **First Value** (immediate) — First insight based on what she learned

**Bayesian Classification (STA 142):**
- Prior: uniform distribution over worker types
- Likelihood: keyword matching per answer
- Posterior: updated classification with confidence
- Each answer refines the classification

**Conversation is natural, not a checklist:**
- "Unafanya biashara gani?" not "Select business type"
- Follow-up questions based on answers
- Encouragement in worker's language
- Skip option for every question

### 3. AgentNamingFragment.kt
**The most important moment in onboarding — worker names their Msaidizi.**

- "Ungependa uniite jina gani?" (What would you like to call me?)
- 5 curated suggestions: Msaidizi, Rafiki, Biashara Yangu, Mshauri, Mwalimu
- Custom name input for personalization
- Then asks worker's name: "Jina lako nani?"
- Creates psychological ownership (Kahneman's endowment effect)

**Academic basis:** PSY 101 (Behavioral), ECO 206 (Trust), BCB 108 (Communication)

### 4. BusinessDiscoveryFragment.kt
**Voice conversation to understand the worker's business.**

- Not a form — a conversation
- 10 natural questions, each building on the last
- Voice input via on-device Whisper (no internet needed)
- Text input fallback for accessibility
- Skip option for every question
- Progress indicator: "Swali 3 kati ya 10"
- Real-time Bayesian classification updates

**Questions flow naturally:**
1. Business type → 2. Products → 3. Location → 4. Hours
5. Solo/team → 6. Supply → 7. Customers → 8. Payment
9. Records → 10. Challenges

### 5. ModelDownloadManager.kt
**Full model download on mobile data — NOT WiFi-only.**

| Model | Size | Purpose | Priority |
|-------|------|---------|----------|
| Whisper tiny (int4) | ~150MB | Speech recognition | 1 (critical) |
| Qwen 0.5B (Q4_K_M) | ~300MB | Reasoning & CFO advice | 2 |
| Piper TTS (Swahili) | ~50MB | Voice output | 3 |
| **Total** | **~500MB** | | |

**Key features:**
- **No WiFi restriction** — works on 3G/4G/5G (Safaricom data bundles)
- **Auto-resume** if interrupted (network loss, app kill)
- **Priority order** — Whisper first (voice input is critical)
- **Background download** during onboarding conversation
- **Natural progress** — "Ninajifunza lugha yako..." not "Downloading 150MB..."
- **Network-aware** — pauses on network loss, resumes on reconnect

### 6. OnboardingActivity.kt (Updated)
**Wires everything together.**

- Initializes ModelDownloadManager on creation
- Starts model downloads immediately (background during onboarding)
- Updated progress indicator for new 5-step flow
- Observes model download state
- Exposes progress to fragments

### 7. nav_onboarding.xml (Updated)
**Updated navigation graph with new fragments.**

New flow: Introduction → AgentNaming → BusinessDiscovery → ModelSetup → FirstUse

---

## Academic Framework Embedded

| Unit | Application in Onboarding |
|------|--------------------------|
| **ECO 101** — Consumer Theory | Budget constraints, payment methods, spending patterns |
| **ECO 201** — Producer Theory | Business classification, production function, cost structure |
| **ECO 204** — African Development | Location, gender, rural-urban, informal institutions |
| **ECO 206** — Microfinance | Record-keeping → creditworthiness, trust-building |
| **STA 142** — Bayesian Inference | Prior → likelihood → posterior for each answer |
| **BCB 108** — Communication | Voice-first, bilingual, culturally appropriate |
| **Applied Stats** — Survey Sampling | Representative data collection through conversation |
| **CS/HCI** — User Experience | Zero technical knowledge required, natural flow |

---

## Critical Design Decisions

### 1. Conversation, Not Form
Valentine's mum doesn't fill out forms. She talks. Msaidizi listens.
- No dropdown menus
- No checkboxes
- No technical jargon
- Just natural questions and voice answers

### 2. Full Models, Not Mini
- Qwen 0.5B (not 0.1B) — real reasoning
- Whisper (not Silero-only) — real speech recognition
- Piper TTS — real voice output
- Total: ~500MB, downloaded on mobile data

### 3. Mobile Data, Not WiFi
- No WiFi-only restriction
- Works on Safaricom data bundles
- Auto-resume if interrupted
- ~500MB is manageable on 4G

### 4. Psychological Ownership
- Worker names their Msaidizi (like OpenClaw agent naming)
- Creates endowment effect (Kahneman)
- "My Msaidizi" not "the app"

### 5. First Value Immediate
- After onboarding, Msaidizi gives first insight
- Based on what she learned about the business
- "Aha moment" — this thing actually knows me

### 6. Works FULLY Offline After Onboarding
- All models on-device
- No internet needed for voice, reasoning, transactions, CFO advice
- Sync only when model improvements available
- Data stays on the phone

---

## Files Created/Updated

```
msaidizi-app/app/src/main/java/com/msaidizi/app/onboarding/
├── WorkerProfile.kt          ✅ NEW — Data model
├── OnboardingConversation.kt ✅ NEW — Conversation manager
├── AgentNamingFragment.kt    ✅ NEW — Naming UI
├── BusinessDiscoveryFragment.kt ✅ REPLACED — Full implementation
├── ModelDownloadManager.kt   ✅ NEW — Mobile data downloads
├── OnboardingActivity.kt     ✅ UPDATED — Wires everything
└── ... (existing files preserved)
```

```
msaidizi-app/app/src/main/res/navigation/
└── nav_onboarding.xml        ✅ UPDATED — New flow
```

---

## What Valentine's Mum Experiences

1. **Opens app** → "Karibu! Welcome to Msaidizi"
2. **Taps "Let's Get Started"** → Sees naming screen
3. **Names Msaidizi "Rafiki"** → "Napenda jina hilo!" (I love that name!)
4. **Tells her name** → "Karibu Mama!"
5. **Conversation begins** → "Unafanya biashara gani?"
6. **Speaks naturally** → "Nauza mboga sokoni"
7. **Msaidizi asks follow-ups** → Products, location, hours, challenges
8. **Meanwhile** → Models downloading in background
9. **Conversation ends** → Msaidizi gives first insight
10. **Ready!** → "Tuanze kazi!" (Let's get to work!)

No technical setup. No WiFi needed. No forms. Just a conversation.

**This is how you onboard 600M+ informal workers.** 🤱
