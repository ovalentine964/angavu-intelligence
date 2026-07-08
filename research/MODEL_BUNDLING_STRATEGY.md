# Model Bundling Strategy for Msaidizi

**Angavu Intelligence — Strategy Recommendation**
**Date:** 2026-07-08
**Author:** Model Bundling Strategy Agent

---

## Executive Summary

**Recommendation: Option 4 — Tiered Bundle with Adaptive Download + P2P Fallback**

Bundle Whisper (tiny, quantized) + Piper in the APK (~55MB total), then download Qwen on first launch with a smart strategy that respects the user's data situation. Add peer-to-peer sharing as a secondary distribution channel.

**Why this wins:** Valentine's mum opens the app, it talks to her within 60 seconds — voice works immediately. The reasoning brain downloads later when conditions are right, but the app is already useful from first launch.

---

## Realistic Model Sizes (Quantized)

Before evaluating options, let's establish actual achievable sizes:

| Model | Variant | Size | Notes |
|-------|---------|------|-------|
| Whisper | tiny (INT8, whisper.cpp) | **~39MB** | Good enough for short voice commands in noisy environments |
| Whisper | base (INT8) | ~75MB | Better accuracy, but 2x size |
| Piper TTS | Small voice (ONNX) | **~15-25MB** | Depends on voice/language quality |
| Qwen 0.8B | Q4_K_M GGUF | **~450-500MB** | Minimum viable quantization for reasoning |
| Qwen 0.8B | Q2_K GGUF | ~350MB | Lower quality, but smaller |

**Key insight:** With aggressive quantization, the "essential" models (Whisper tiny + Piper small) fit in ~55-65MB. This changes everything.

---

## Option Analysis

### Option 1: Full Bundle (~570MB)

| Criterion | Assessment |
|-----------|------------|
| Download size | ❌ 570MB+ APK |
| First-launch time | ❌ 30-60 min download on 3G, 10-15 min on 4G |
| Mobile data | ❌ Costs user $0.50-$1.10 (1-2GB bundle consumed) |
| Works offline | ✅ Immediately |
| User experience | ❌ Terrible first impression, high uninstall rate |
| Technical complexity | ✅ Simple |
| Distribution | ❌ Google Play has 200MB APK limit (need expansion files); sideloading possible but risky |

**Verdict: ELIMINATE.** A 570MB APK on a $50 phone in Kenya is a non-starter. Google Play won't even accept it without expansion files. Users will uninstall during download or refuse to spend the data.

---

### Option 2: Small APK + mobile data Download

| Criterion | Assessment |
|-----------|------------|
| Download size | ✅ 43.5MB APK (code only) |
| First-launch time | ✅ Fast install, but app is useless until models download |
| Mobile data | ✅ No data cost (mobile data) |
| Works offline | ⚠️ Only after mobile data download completes |
| User experience | ❌ App installed but doesn't work. "Download on mobile data" = "maybe never" for most users |
| Technical complexity | ⚠️ Medium — needs download manager, resume logic, storage management |
| Distribution | ✅ Standard Play Store |

**Verdict: ELIMINATE as primary strategy.** The fatal flaw: most target users don't have reliable mobile data. Telling Valentine's mum "find mobile data" means the app sits dead on her phone. Dead apps get uninstalled.

However: mobile data download should be *offered* as an option within any strategy.

---

### Option 3: Small APK + Mobile Data Download

| Criterion | Assessment |
|-----------|------------|
| Download size | ⚠️ 43.5MB APK + ~500MB models = ~543MB total |
| First-launch time | ❌ 20-45 min on mobile data |
| Mobile data | ❌ Costs $0.50-$1.00 on Safaricom bundles |
| Works offline | ✅ After download |
| User experience | ❌ Heavy data cost, long wait, eats into bundle |
| Technical complexity | ⚠️ Medium — resume, progress, background download |
| Distribution | ✅ Standard Play Store |

**Verdict: ELIMINATE as primary strategy.** Forcing a $0.50-$1.00 data download on someone earning $2-5/day is disrespectful. That's 10-50% of their daily income just to install an app.

---

### Option 4: Tiered Bundle (RECOMMENDED)

**Bundle Whisper tiny + Piper (~55MB) in APK. Download Qwen after install.**

| Criterion | Assessment |
|-----------|------------|
| Download size | ✅ 55MB APK (code + voice models) + 450MB Qwen (deferred) |
| First-launch time | ✅ App works within 60 seconds of install — voice in, voice out |
| Mobile data | ✅ 55MB = ~$0.05-0.10 on Safaricom. Acceptable. |
| Works offline | ✅ Voice features immediately. Reasoning after Qwen download. |
| User experience | ✅ App is useful from moment one. "Smart features" unlock progressively. |
| Technical complexity | ⚠️ Medium — tiered download manager, graceful degradation |
| Distribution | ✅ Standard Play Store, sideloading, P2P |

**Why this works for Valentine's mum:**
1. She downloads Msaidizi (55MB) — costs ~5 KSh ($0.04). Done in 2-3 minutes.
2. She opens the app. It greets her in Swahili. She speaks, it listens (Whisper). It talks back (Piper).
3. The app says: "Ninaweza kukusaidia zaidi! Download smart brain? (150MB, ~12 KSh)" — with a clear cost estimate.
4. She can say yes (if she has data), say no (app still works for voice), or wait for mobile data.
5. When Qwen downloads, the app gains reasoning — answers questions, helps with tasks.

**The Qwen download strategy — give users control:**

```
┌─────────────────────────────────────┐
│  Msaidizi is ready! 🎉              │
│                                     │
│  ✅ Voice input — working            │
│  ✅ Voice output — working           │
│  🔒 Smart assistant — downloading... │
│                                     │
│  ▓▓▓▓▓▓░░░░░░░░ 34% — 120MB left   │
│                                     │
│  [Pause] [mobile data Only] [Cancel]       │
│                                     │
│  Estimated cost: ~12 KSh on data    │
│  Estimated time: ~8 minutes         │
└─────────────────────────────────────┘
```

---

### Option 5: Split APK (Device Tiers)

| Criterion | Assessment |
|-----------|------------|
| Download size | ✅ Tailored to device capability |
| First-launch time | ✅ Appropriate for tier |
| Mobile data | ✅ Tier-dependent |
| Works offline | ✅ Yes |
| User experience | ⚠️ Can be confusing — "which APK do I download?" |
| Technical complexity | ❌ High — multiple build pipelines, testing matrix |
| Distribution | ❌ Play Store doesn't easily support manual tier selection |

**Verdict: USE AS COMPLEMENT, not primary strategy.** Let the app detect device capability at runtime and adjust. Don't make users choose. A $50 phone user doesn't want to be told they're on the "LOW" tier.

**What to actually do:**
- Detect available RAM and storage at first launch
- On ≤2GB RAM: Use Whisper tiny, skip Qwen or use aggressive Q2 quantization
- On 3-4GB RAM: Use Whisper base, Q4 Qwen
- On 4GB+: Use Whisper small, full Qwen

This is runtime adaptation, not split APKs. Same APK, different behavior.

---

### Option 6: Google Play App Bundle + Play Asset Delivery

| Criterion | Assessment |
|-----------|------------|
| Download size | ✅ Optimized per device |
| First-launch time | ⚠️ Asset packs download on first launch |
| Mobile data | ⚠️ Asset packs can be large |
| Works offline | ✅ After assets install |
| User experience | ⚠️ "Installing assets..." spinner on first launch |
| Technical complexity | ⚠️ Medium — Play Asset Delivery API |
| Distribution | ❌ Play Store only. Many African users sideload or use alternative stores. |

**Verdict: GOOD COMPLEMENT for Play Store users.** Play Asset Delivery (PAD) can handle the Qwen model download with automatic resume and progress. But it only works through Play Store — and in Kenya, many users share APKs via Bluetooth/ShareIt or install from other sources.

**Recommendation:** Support PAD as one download channel, but don't depend on it exclusively.

---

### Option 7: Peer-to-Peer Transfer

| Criterion | Assessment |
|-----------|------------|
| Download size | ✅ 0 data cost |
| First-launch time | ⚠️ Depends on finding someone with the model |
| Mobile data | ✅ Zero — Bluetooth/mobile data Direct |
| Works offline | ✅ After transfer |
| User experience | ✅ Familiar pattern in Africa |
| Technical complexity | ⚠️ Medium — need secure model verification |
| Distribution | ✅ Organic, viral |

**Verdict: HIGH-VALUE ADDITION to any strategy.** This is culturally aligned with how Africans actually share content. ShareIt, Xender, and Bluetooth file sharing are deeply embedded behaviors.

**Implementation:**
- App can "export" its Qwen model file to a shareable format
- App can "import" a model file from another device
- Verify model integrity with checksum (prevent corruption/tampering)
- Show a "Share Msaidizi's brain with a friend" button
- This creates a viral loop: each install can seed another

```
┌─────────────────────────────────────┐
│  Share Msaidizi with a friend!      │
│                                     │
│  📱 → 📱  Transfer via Bluetooth     │
│  No data needed!                    │
│                                     │
│  [Share Now]  [Maybe Later]         │
└─────────────────────────────────────┘
```

---

### Option 8: SD Card Loading

| Criterion | Assessment |
|-----------|------------|
| Download size | ✅ 0 — pre-loaded |
| First-launch time | ✅ Instant |
| Mobile data | ✅ Zero |
| Works offline | ✅ Yes |
| User experience | ✅ Familiar — like buying a memory card with music |
| Technical complexity | ⚠️ Medium — SD card detection, model path management |
| Distribution | ❌ Requires physical distribution network |

**Verdict: NICHE BUT VALUABLE for specific markets.** In Kenya, SD cards with pre-loaded content (music, videos) are sold in markets and by street vendors. This model could work for Msaidizi in partnership with:
- Phone retailers (bundle Msaidizi SD card with new phone sales)
- M-Pesa agents (who already serve as informal tech support)
- Community health workers / SACCO offices

**Cost:** A 1GB SD card costs ~100-200 KSh ($0.75-$1.50) in Kenya. Pre-loading models is a one-time manufacturing step.

**Recommendation:** Explore as a Phase 2 distribution strategy after initial launch.

---

## Recommended Architecture

### The Three-Layer Model

```
Layer 1: INSTANT (bundled in APK, ~55MB)
├── Whisper tiny (INT8) — voice input
├── Piper TTS (small voice) — voice output
├── App code + UI
└── Language: Swahili + English voice

Layer 2: SMART (downloaded, ~450MB)
├── Qwen 0.8B (Q4_K_M GGUF) — reasoning
└── Downloaded via: mobile data / mobile data / P2P / SD card

Layer 3: EXTENDED (future, optional)
├── Additional languages
├── Better voice quality
├── Domain-specific knowledge
└── Downloaded on demand
```

### Graceful Degradation

The app must work at every layer, with clear communication about what's available:

```
App State          | Voice In | Voice Out | Reasoning | Data Cost
-------------------|----------|-----------|-----------|----------
Layer 1 only       | ✅       | ✅        | ❌        | ~$0.04
Layer 1 + 2        | ✅       | ✅        | ✅        | ~$0.40
Layer 1 + 2 + 3    | ✅       | ✅        | ✅+       | Variable
```

### Smart Download Manager

```kotlin
// Pseudocode for the download strategy
class ModelDownloadManager {

    fun suggestDownloadStrategy(context: Context): DownloadStrategy {
        val hasmobile data = isOnmobile data()
        val dataBalance = estimateDataBalance() // Check Safaricom/Airtel
        val storageFree = getFreeStorageMB()
        val timeOfDay = LocalTime.now()

        return when {
            // Best case: mobile data download
            hasmobile data && storageFree > 600 ->
                DownloadStrategy.WIFI_NOW

            // Night time: offer scheduled download (Safaricom has cheaper night bundles)
            !hasmobile data && timeOfDay in 0..5 ->
                DownloadStrategy.SCHEDULED_NIGHT

            // Low data: offer P2P transfer
            dataBalance < 200 ->
                DownloadStrategy.P2P_TRANSFER

            // Has data but cautious: show cost estimate
            !hasmobile data && dataBalance in 200..1000 ->
                DownloadStrategy.MOBILE_WITH_CONSENT

            // Has plenty of data
            !hasmobile data && dataBalance > 1000 ->
                DownloadStrategy.MOBILE_NOW

            // Default: suggest mobile data or P2P
            else ->
                DownloadStrategy.WAIT_FOR_WIFI
        }
    }
}
```

### Night Data Bundle Exploitation

Safaricom and Airtel offer cheaper "night bundles" (typically 12AM-6AM). Smart move:

- App detects if user has a night bundle active
- Suggests: "Download tonight while you sleep? Costs only 5 KSh!"
- Schedule download for 1AM
- User wakes up with full app capability

---

## Distribution Strategy

### Primary: Google Play Store
- 55MB APK with bundled voice models
- Play Asset Delivery for Qwen (optional channel)
- Standard for users who already use Play Store

### Secondary: Direct APK Distribution
- Host APK on Msaidizi website
- Share via WhatsApp links, SMS
- Users can install directly (enable "Unknown Sources")
- No Play Store dependency

### Tertiary: Peer-to-Peer
- "Share Msaidizi" feature built into app
- Bluetooth / mobile data Direct / ShareIt
- Export APK + model files as a single package
- Verify integrity on import

### Quaternary: Physical Distribution (Phase 2)
- SD cards pre-loaded with models
- Distributed through: phone shops, M-Pesa agents, SACCO offices
- Partnership opportunity with Safaricom/Airtel (zero-rated download)

---

## Zero-Rating Partnership Opportunity

**Game-changer if achievable:** Partner with Safaricom to zero-rate Msaidizi downloads.

- Safaricom has 44M+ subscribers in Kenya
- They already zero-rate M-Pesa, Wikipedia, health info
- Msaidizi serves informal workers — Safaricom's core market
- Model download (~450MB) becomes free for users
- Safaricom gets goodwill + data habit formation

**Approach:** Apply for Safaricom's developer program or approach their corporate social responsibility team. Frame Msaidizi as digital inclusion for informal workers.

---

## RAM Management on 2GB Phones

This is the hardest technical constraint. A $50 phone with 2GB RAM has ~800MB-1GB available after Android + system apps.

**Model RAM footprint:**
| Model | Quantization | Disk | RAM (est.) |
|-------|-------------|------|------------|
| Whisper tiny | INT8 | 39MB | ~60MB |
| Piper small | ONNX | 20MB | ~40MB |
| Qwen 0.8B | Q4_K_M | 450MB | ~500MB |

**Total if all loaded:** ~600MB RAM. This is tight but feasible if:
1. Models are loaded/unloaded dynamically (not all at once)
2. Qwen is loaded only when reasoning is needed, then unloaded
3. Whisper and Piper are loaded on-demand for voice interaction
4. Aggressive memory management — kill Qwen when app goes to background

**Architecture:**
```
Voice mode:  Whisper (60MB) + Piper (40MB) = 100MB RAM ✅
Reasoning:   Qwen (500MB) — other models unloaded = 500MB RAM ✅
Background:  Nothing loaded = 0MB RAM ✅
```

**Never:** Load all three simultaneously on a 2GB phone. Use a service model where each capability is a separate process that starts/stops on demand.

---

## Cost Analysis for the User

### Scenario: Valentine's Mum on Safaricom

| Action | Data Cost (KSh) | Time | Experience |
|--------|----------------|------|------------|
| Download APK | 4-5 KSh (~$0.04) | 2-3 min | ✅ Quick, cheap |
| Use voice features | 0 KSh | Instant | ✅ Works immediately |
| Download Qwen (mobile) | 40-50 KSh (~$0.40) | 8-12 min | ⚠️ Acceptable if she opts in |
| Download Qwen (mobile data) | 0 KSh | 5-8 min | ✅ Best case |
| Download Qwen (P2P) | 0 KSh | 3-5 min | ✅ No cost |
| Use full app | 0 KSh | Instant | ✅ Offline forever |

**Total cost to get fully working:** 45-55 KSh (~$0.40-0.50) on mobile data, or 4-5 KSh ($0.04) with mobile data/P2P for Qwen.

Compare to: A daily matatu ride costs 50-100 KSh. This is affordable.

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| User never downloads Qwen | App is still useful with voice-only mode. Prompt gently. |
| Download interrupted | Robust resume logic. Support partial downloads. |
| Phone runs out of storage | Check storage before download. Offer to clear cache. |
| Model file corrupted | SHA-256 verification on download + on load |
| User shares corrupted model via P2P | Checksum verification on import. Reject bad files. |
| Old model version in circulation | Version stamp on model files. Prompt update when needed. |
| App killed during download | Use Android WorkManager for background download. Resume on relaunch. |

---

## Implementation Roadmap

### Phase 1: MVP (Week 1-4)
- [ ] Bundle Whisper tiny (INT8) + Piper small in APK
- [ ] Implement graceful degradation (voice works without Qwen)
- [ ] Basic download manager for Qwen (mobile data + mobile data)
- [ ] Progress UI with cost estimate

### Phase 2: Smart Downloads (Week 5-8)
- [ ] Implement P2P model sharing
- [ ] Night bundle detection and scheduled download
- [ ] Device tier detection (RAM/storage) for model selection
- [ ] Play Asset Delivery integration

### Phase 3: Distribution Expansion (Week 9-12)
- [ ] Direct APK hosting + WhatsApp share links
- [ ] SD card pre-loading pilot (partner with 2-3 phone shops)
- [ ] Zero-rating partnership outreach to Safaricom/Airtel
- [ ] Model version management system

### Phase 4: Optimization (Ongoing)
- [ ] A/B test download prompts (timing, wording, cost framing)
- [ ] Analyze drop-off rates at each stage
- [ ] Explore more aggressive quantization (Q2 for ultra-low-end)
- [ ] Consider Qwen 0.5B as fallback for 2GB RAM devices

---

## Decision Matrix — Final Scoring

| Option | Size | Launch | Data | Offline | UX | Complexity | Distribution | **Total** |
|--------|------|--------|------|---------|-----|------------|--------------|-----------|
| 1. Full bundle | 1 | 1 | 1 | 5 | 2 | 5 | 2 | **17** |
| 2. mobile data | 5 | 4 | 5 | 3 | 2 | 3 | 4 | **26** |
| 3. Mobile data | 3 | 2 | 2 | 4 | 2 | 3 | 4 | **20** |
| **4. Tiered** | **4** | **5** | **5** | **4** | **5** | **3** | **5** | **31** |
| 5. Split APK | 4 | 4 | 4 | 4 | 3 | 2 | 3 | **24** |
| 6. Play Bundle | 4 | 3 | 4 | 4 | 3 | 3 | 2 | **23** |
| 7. P2P | 5 | 3 | 5 | 4 | 4 | 3 | 4 | **28** |
| 8. SD card | 5 | 5 | 5 | 4 | 4 | 3 | 1 | **27** |

**Winner: Option 4 (Tiered Bundle)** — scored 31/35.

---

## Final Recommendation

**Bundle voice models in APK. Download the brain later. Let users share.**

This is how you make Msaidizi work for Valentine's mum:

1. **She downloads a 55MB app** — costs less than a text message.
2. **It talks to her immediately** — in Swahili, in her voice, on her $50 phone.
3. **When she's ready, the brain arrives** — via data, mobile data, or a friend's Bluetooth.
4. **It never leaves her stranded** — every feature works offline, at every stage.
5. **She can share it** — one mum to another, no data needed.

That's not just a bundling strategy. That's respect.

---

*"The best technology is the one that works where people are, not where we wish they were."*
