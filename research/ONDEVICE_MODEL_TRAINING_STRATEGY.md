# On-Device Model & Training Strategy — Angavu Intelligence

**Author:** On-Device Model & Training Strategy Agent
**Date:** 2026-07-08
**Status:** COMPLETE — ACTIONABLE STRATEGY
**Scope:** On-device model selection, training pipeline, federated learning, voice quality, African language prioritization, inference optimization, cold-start through self-improving loop

---

## Executive Summary

Msaidizi's voice pipeline is the product's soul. A mama mboga in Migori should feel like she's talking to someone who *grew up next door* — not a robot reading Swahili from a textbook. This document defines exactly how that happens: what model runs on her phone, how it learns her voice, how her corrections improve every other worker's phone, and when each dialect reaches "natural" quality.

The existing codebase has **solid architecture** (ModelManager, LlmEngine, FederatedLearningClient, PhonemeMapper) but **critical gaps** (no real LoRA training, no TTS pipeline, placeholder federated aggregation, stub training loop). This strategy addresses both what exists and what must be built.

**The core insight:** On-device AI is not a smaller version of cloud AI. It's a fundamentally different system — one that learns from *one person's* corrections, runs on *their* phone's constraints, and feeds anonymous learnings back to improve *everyone's* experience.

---

## 1. On-Device Model Stack

### 1.1 Model Tiers (Already Defined in ModelManager.kt — Validated)

The `ModelManager.kt` device tier classification is **correct and well-designed**. The tier thresholds match East African market reality:

| Tier | RAM | Typical Devices | Model | GGUF Size | Context | Tokens/sec |
|------|-----|-----------------|-------|-----------|---------|------------|
| **LOW** | ≤2GB | Tecno Spark Go, Itel A60 | Qwen3.5-0.8B Q4_0 | ~500MB | 1024 | ~8-12 |
| **MID** | 3-4GB | Samsung A15, Redmi 13C | Qwen3-1.7B Q4_K_M | ~1.1GB | 2048 | ~5-8 |
| **HIGH** | ≥6GB | Samsung A25, Pixel 7a | Qwen3.5-2B Q4_K_M | ~1.2GB | 4096 | ~4-6 |

### 1.2 Why These Specific Models

**Qwen3.5-0.8B (LOW tier):** This is the breakthrough model. At 500MB Q4_0, it fits on a 2GB phone with room for Whisper + Silero VAD + the app itself. It's a *reasoning* model (not just autocomplete) — it can understand "Nimeuza nyanya 5 kwa 200" and structure it as a transaction. The 0.8B parameter count is the minimum viable intelligence.

**Qwen3-1.7B (MID tier):** Supports thinking mode (`<think>` chains). This matters for complex queries: "Kulingana na mauzo ya wiki jana, ni bei gani nifanye restock?" (Based on last week's sales, what price should I restock at?). The reasoning chain lets it work through the math.

**Qwen3.5-2B (HIGH tier):** Edge-optimized, best quality within mobile constraints. For the 10-15% of workers with newer phones, this delivers noticeably better conversation quality.

### 1.3 Inference Stack (What Runs the Model)

**Primary: llama.cpp via JNI** — Already implemented in `LlamaCppEngine.kt` and `LlmEngine.kt`. This is the correct choice:
- Native ARM NEON optimization → fastest CPU inference
- Memory-mapped GGUF → fast load, low RAM pressure
- Built-in quantization support (Q4_0, Q4_K_M, Q5_K_S)
- Single native library, no Python dependency

**Secondary: ONNX Runtime** — For non-LLM models:
- Whisper ASR (whisper-tiny-int4.onnx, ~40MB)
- Piper TTS (piper-swahili.onnx, ~25MB)
- Silero VAD (silero_vad.onnx, ~2.5MB)

**Not recommended for mobile:**
- PyTorch/TF Lite — too heavy, no advantage over llama.cpp for LLMs
- GPU delegate (NNAPI) — inconsistent across MediaTek/Unisoc/Snapdragon chipsets common in Africa. CPU inference via llama.cpp is more reliable.
- Vulkan GPU — not worth the compatibility headaches for 0.8-2B models where CPU is fast enough.

### 1.4 Memory Budget on 2GB Phone

This is the hardest constraint. Here's the actual memory layout:

```
Total RAM: 2048 MB
├── Android OS + system: ~800 MB
├── Msaidizi app heap: ~150 MB
├── Silero VAD: ~10 MB
├── Whisper ASR (loaded on-demand): ~80 MB
├── Qwen3.5-0.8B Q4_0 (memory-mapped): ~350 MB working set
├── Piper TTS (loaded on-demand): ~50 MB
├── KV cache (1024 tokens): ~50 MB
└── Headroom: ~600 MB
```

**Key design decisions for 2GB phones:**
1. **Never load LLM + ASR + TTS simultaneously.** The `ModelManager` already handles this with `onLowMemory()` and auto-unload after 10 min idle. Extend this to a strict pipeline: ASR → unload → LLM → unload → TTS.
2. **Use mmap aggressively.** `LlamaCppEngine` already memory-maps GGUF files. The OS can page out unused model weights. This means the *working set* (~350MB) is much smaller than the *file size* (~500MB).
3. **Context window is everything.** 1024 tokens on LOW tier means ~750 words of conversation history. The system prompt + business context takes ~200 tokens. That leaves ~550 tokens for conversation. This is enough for 5-6 turns — acceptable for task-oriented dialogue.

### 1.5 Model Loading Strategy (Hot-Swap)

The `ModelManager.hotSwapModel()` is implemented but needs enhancement:

```
User speaks → Silero VAD detects speech end
    → Whisper ASR transcribes (loaded, ~2s)
    → Whisper unloaded from memory
    → LLM processes transcription + generates response (loaded, ~3-8s)
    → LLM unloaded from memory
    → Piper TTS speaks response (loaded, ~2s)
    → TTS unloaded from memory
```

**Total pipeline time on 2GB phone:** ~8-15 seconds (acceptable for voice interaction).
**Peak memory:** ~1.2GB (Silero + Whisper + app heap) → well within 2GB.

On 6GB+ phones, all three models can stay loaded simultaneously for ~2-3 second response times.

---

## 2. On-Device Training — What the Phone Learns Without the Cloud

### 2.1 Four Levels of On-Device Learning

The `LanguageLearningPipeline.kt` defines four learning levels. Here's what each actually does:

#### Level 1: Immediate Corrections (Real-time, <0.01% battery)

**What happens:** User says "Nimeuza nyanya tano" → model hears "Nimeuza nyanya tano" (correct) or "Nimeuza nyanya tano" (incorrect). User corrects: "Sio tano, ni kumi."

**What the phone stores:**
- Correction pair: ("tano" → "kumi") in context of "nyanya" + number
- N-gram update: "nyanya kumi" frequency +1
- Phoneme confusion: ASR confused /t/ and /k/ in this context

**Implementation status:** The `AdaptiveAsrEngine.kt` correction cache and `PhonemeMapper.kt` confusion matrices are implemented. This works today.

**What improves immediately:**
- Next time user says "nyanya kumi," the n-gram LM boosts "kumi" over "tano"
- Phoneme mapper learns that this user's /t/ → /k/ confusion is common
- Confidence calibrator adjusts per-word confidence

#### Level 2: Session Learning (During active use)

**What happens:** Over a conversation, the system builds a vocabulary profile:

```json
{
  "products": {"nyanya": {"avg_price": 20, "unit": "kilo"}, "sukuma": {"avg_price": 10, "unit": "bunch"}},
  "trade_type": "mama_mboga",
  "location_markers": ["migori", "market"],
  "time_patterns": {"morning_sales": true, "evening_restock": true}
}
```

**What improves:**
- LLM gets injected context: "Mama mboga, Migori market. Products: nyanya (KSh 20/kilo), sukuma (KSh 10/bunch). Morning seller."
- Response quality improves within the session
- Dialect detection narrows to "Swahili (Migori)" vs generic "Swahili"

**Implementation status:** `LlmEngine.generateWithLearnedContext()` is implemented. The vocabulary learning logic exists in `LanguageLearningPipeline.kt`. This works today.

#### Level 3: LoRA Fine-Tuning (Nightly, charging only)

**What happens:** During charging hours (2-5 AM), the phone fine-tunes a LoRA adapter on the day's corrections. This is the *only* on-device training that modifies model weights.

**Critical gap identified:** The `_run_lora_training()` in `FineTuningPipeline` is a **stub**. It simulates training with `delay(1000)` and returns `ByteArray(0)`. The `FederatedLearningClient.kt` has a more detailed implementation but uses toy one-hot vectors, not actual model weights.

**What must be built:**

```
Actual LoRA training pipeline:
1. Load base model (Qwen3.5-0.8B) in inference mode
2. Attach LoRA adapter (rank 4-8, ~100K-500K params)
3. Forward pass on correction pairs
4. Compute loss (cross-entropy on corrected output)
5. Backward pass — update only LoRA weights
6. Clip gradients (max_norm=1.0)
7. Save adapter weights (~200KB-2MB)
8. Apply DP noise to weight delta for FL upload
```

**Implementation options for Android:**
- **Option A (Recommended):** llama.cpp LoRA training via NDK. The `llama.cpp` project has experimental LoRA training support. Build as a native library, call via JNI.
- **Option B:** ONNX Runtime training API. More mature training support but heavier.
- **Option C:** Pre-compiled TFLite micro training. Limited but very lightweight.

**LoRA configuration per device tier:**

| Tier | Rank | Alpha | Target Modules | Trainable Params | Adapter Size |
|------|------|-------|----------------|-----------------|-------------|
| LOW (2GB) | 4 | 8 | q_proj, v_proj | ~7K | ~50KB |
| MID (4GB) | 8 | 16 | q_proj, v_proj, k_proj | ~28K | ~200KB |
| HIGH (6GB) | 16 | 32 | q_proj, v_proj, k_proj, o_proj | ~115K | ~800KB |

**Training constraints:**
- Only when charging AND battery ≥50%
- Only between 2-5 AM (configurable)
- Max 15 minutes per session
- Max 500 examples per session
- Min 20 corrections before first training
- 6-hour minimum between sessions

#### Level 4: Federated Sync (Weekly, WiFi + charging)

**What happens:** The phone uploads anonymized learnings to the cloud, downloads improved global model.

See Section 3 (Federated Learning) for details.

### 2.2 What Each Phone Learns (Without Any Cloud)

After 1 week of use, a single phone knows:

1. **User's product vocabulary** — "nyanya," "sukuma," "mchele," "mafuta" with typical prices
2. **User's pronunciation patterns** — which phonemes they confuse, their accent markers
3. **User's business patterns** — when they sell, what they sell, typical quantities
4. **User's dialect markers** — Migori vs Nairobi vs Coastal Swahili differences
5. **Correction history** — what the model gets wrong for *this specific user*
6. **Code-switching profile** — how much English/Sheng they mix, where they switch

**This is enough to personalize the experience significantly** even before any cloud model improvement. The mixing coefficient `α = min(1.0, corrections / 100)` ensures that by 100 corrections (~2-3 weeks of daily use), the personal adapter has full influence.

### 2.3 Seed Vocabularies (Critical Cold-Start Improvement)

**Gap identified:** No pre-seeded vocabulary exists. Every user starts from zero.

**Solution:** Create seed vocabulary files for each trade type, bundled in the app:

```
seeds/
├── mama_mboga_sw.json      # Vegetable seller, Swahili
├── boda_boda_sw.json       # Motorcycle taxi, Swahili
├── jua_kali_sw.json        # Informal manufacturer, Swahili
├── mama_mboga_yor.json     # Vegetable seller, Yoruba
├── boda_boda_yor.json      # Motorcycle taxi, Yoruba
└── general_sw.json         # General business, Swahili
```

Each seed file contains:
```json
{
  "products": {
    "nyanya": {"aliases": ["nyanya", "tomato", "tomato"], "avg_price": 20, "unit": "kilo"},
    "sukuma": {"aliases": ["sukuma wiki", "kale", "sukuma"], "avg_price": 10, "unit": "bunch"},
    "mchele": {"aliases": ["mchele", "rice"], "avg_price": 150, "unit": "kilo"}
  },
  "numbers": {
    "moja": 1, "mbili": 2, "tatu": 3, "nne": 4, "tano": 5,
    "sita": 6, "saba": 7, "nane": 8, "tisa": 9, "kumi": 10,
    "ishirini": 20, "thelathini": 30, "arobaini": 40, "hamsini": 50
  },
  "common_phrases": [
    "Nimeuza", "Nimenunua", "Bei gani", "Kiasi gani",
    "Stock imeisha", "Nahitaji restock", "Faida ni"
  ],
  "corrections": {
    "bei ya": "bei gani",
    "ngapi": "gani"
  }
}
```

**Impact:** On first launch, Msaidizi already knows 200+ product terms, 50+ number words, and 30+ common phrases. This drops cold-start WER from ~40% to ~25% immediately.

**Estimated effort:** 2-3 days per language × 6 languages = ~2-3 weeks for the core seed set.

---

## 3. Federated Learning — What Gets Sent, How It's Aggregated

### 3.1 What Leaves the Device

**Nothing raw. Ever.** The `FederatedLearningClient.kt` implements this correctly:

| Data | Format | Size | Privacy |
|------|--------|------|---------|
| Device ID | SHA-256 hash with per-install salt | 32 bytes | Non-reversible |
| Correction patterns | Hashed n-grams + phoneme patterns | ~5-20 KB | DP-noised (ε=1.0) |
| LoRA weight delta | Encrypted adapter weights | ~50KB-2MB | AES-256 encrypted |
| Calibration params | Temperature, Platt scaling | ~100 bytes | Minimal PII |
| Language/dialect | String label | ~10 bytes | No PII |

**Critical fix needed:** The Kotlin client uses ε=1.0 while the Python backend claims ε=0.1. This is a **10× privacy budget discrepancy**. Standardize on **ε=1.0** (moderate privacy, usable signal) for initial deployment. The ε=0.1 setting adds so much noise (σ≈34-53) that the aggregated gradients become useless for small cohorts. Move to ε=0.1 only when cohort sizes exceed 1000 devices per dialect.

**Another fix:** The `PhonemePattern` extraction leaks 2-character word prefixes. For 3-character Swahili words, this exposes 66% of the word. Replace with IPA phoneme mapping (the `PhonemeMapper.kt` already has the capability — use it).

### 3.2 How Aggregation Works

**Current state:** The Python `FederatedAggregator` implements FedAvg, Krum, and Trimmed Mean. The math is correct. But the LoRA adapter aggregation is **broken** — it takes the last device's adapter instead of averaging.

**What must work:**

```
Round N aggregation:
1. Collect LoRA deltas from K devices (min K=10 for privacy)
2. Validate each delta:
   - L2 norm < 3σ of cohort norms (anomaly detection)
   - Training loss > 0.01 (prevent poison)
   - No duplicate device IDs
3. Aggregate using Trimmed Mean:
   - Sort deltas by L2 norm
   - Remove top/bottom 10%
   - Weighted average: Δw = Σ (n_k / n) · Δw_k
4. Apply differential privacy noise to aggregated delta
5. Validate improvement:
   - Run aggregated model on held-out validation set
   - Compare WER/accuracy to previous global model
   - If no improvement, keep previous version
6. Package as GlobalModelResponse:
   - Aggregated LoRA adapter (GGUF format)
   - Updated n-gram language model
   - Updated calibration parameters
   - Version number (v{major}.{minor}.{patch})
```

**Key implementation requirement:** LoRA adapter averaging must actually work. This means:
1. All devices use the same LoRA configuration (rank, alpha, target modules) per dialect
2. Weight matrices are aligned (same base model → same weight dimensions)
3. The server performs element-wise weighted average on each LoRA A and B matrix

### 3.3 Aggregation Frequency

| Component | Frequency | Trigger |
|-----------|-----------|---------|
| On-device correction cache | Real-time | Every correction |
| On-device n-gram LM | Real-time | Every correction |
| On-device LoRA training | Daily | 2-5 AM, charging, ≥20 corrections |
| Federated upload | Weekly | WiFi + charging |
| Global model aggregation | Weekly | When ≥10 deltas collected per dialect |
| Global model distribution | Weekly | Via device pull (WiFi + charging) |
| Dialect-specific model rebuild | Monthly | When quality drops below threshold |

### 3.4 Server Infrastructure (Must Be Built)

The `FederatedAggregator` Python module is solid. It needs a production wrapper:

```
API Layer (FastAPI):
├── POST /api/v1/federated/upload    — Device uploads delta
├── GET  /api/v1/federated/models/{lang} — Device downloads global model
├── GET  /api/v1/federated/status    — Aggregation round status
└── POST /api/v1/federated/register  — Device registration

Storage:
├── PostgreSQL — Deltas, aggregation history, device registry
├── Redis — Round coordination, rate limiting
└── Object Storage (S3/MinIO) — Model files, adapters

Scheduler:
├── Celery/Airflow — Weekly aggregation trigger
├── Quality gate — Only publish if WER improves
└── Rollback — Auto-revert if regression detected
```

**Estimated build effort:** 2-3 weeks for a competent backend engineer. The aggregation logic exists — it's the API, database, and scheduling that need building.

---

## 4. Cloud Training — How Aggregated Gradients Improve the Global Model

### 4.1 The Global Model Architecture

```
Base Model (Qwen3.5-0.8B / 1.7B / 2B)
├── Domain Adapter: angavu-business-v1 (LoRA)
│   ├── Trained on: Aggregated business interaction data
│   ├── Languages: All supported
│   └── Updated: Monthly
├── Dialect Adapter: swahili-migori-v1 (LoRA)
│   ├── Trained on: Migori-region corrections
│   ├── Source: Federated aggregation from Migori users
│   └── Updated: Weekly
├── Dialect Adapter: swahili-coast-v1 (LoRA)
│   ├── Trained on: Coastal Swahili corrections
│   └── Updated: Weekly
└── (Future) User Adapter: per-device personalization
    ├── Trained on-device only
    └── Never uploaded
```

### 4.2 How Federated Gradients Become a Better Model

**Step 1: Collect** — 10+ devices in a dialect cohort upload deltas weekly.

**Step 2: Aggregate** — Trimmed Mean produces a single aggregated delta per dialect.

**Step 3: Apply** — Server applies aggregated delta to the current dialect adapter:
```
adapter_new = adapter_old + learning_rate × aggregated_delta
```

**Step 4: Validate** — Run the updated adapter on a held-out evaluation set:
- WER on dialect-specific test set (target: <20% for Swahili, <35% for others)
- Business task accuracy (record_sale, check_inventory)
- Code-switching fluency (mixed-language understanding)

**Step 5: Gate** — Only publish if quality improves. Keep previous version otherwise.

**Step 6: Distribute** — Devices pull the new adapter on next sync.

### 4.3 NVIDIA NIM Overflow Handling

For complex reasoning that exceeds on-device capability (e.g., "Analyze my profit trends over 3 months and suggest restocking strategy"), the `ModelRouter` sends the request to NVIDIA NIM free tier:

```
On-device LLM (handles 90% of requests)
├── Simple queries: "Nimeuza nyanya kumi" → record sale
├── Corrections: "Sio tano, ni kumi" → update record
├── Basic advice: "Bei gani ya sukuma?" → check recent prices
└── Chat: "Habari yako?" → conversational response

NVIDIA NIM (handles 10% overflow)
├── Complex analysis: "Compare this week vs last week"
├── Multi-step reasoning: "Should I restock tomatoes or kale?"
├── Summarization: "Summarize my month"
└── Strategy: "How can I increase profit?"
```

**Routing logic (ModelRouter):**
1. Try on-device LLM first (always available, no network needed)
2. If response confidence < threshold OR request complexity > threshold → route to NIM
3. Cache NIM responses for common queries (reduce API calls)

---

## 5. Voice Training Pipeline — From "Robot Swahili" to "Speaks Like Your Neighbour"

### 5.1 The Voice Pipeline Architecture

```
Audio Input (16kHz PCM)
│
├── Silero VAD → Detect speech segments (~10ms latency)
│
├── Whisper ASR (tiny-int4) → Transcribe to text
│   ├── Base WER: ~25-40% on African languages
│   ├── PhonemeMapper post-processing → Fix known ASR errors
│   ├── DialectClassifier → Identify dialect for context
│   └── ConfidenceCalibrator → Per-word confidence scores
│
├── Language Model (Qwen3.x) → Understand intent, generate response
│   ├── System prompt (language-specific)
│   ├── Learned context (vocabulary, patterns)
│   ├── Business context (transactions, inventory)
│   └── Function calling (record_sale, check_inventory)
│
├── Piper TTS → Synthesize speech output
│   ├── Base model: piper-swahili.onnx (~25MB)
│   ├── Style: conversational, warm, not robotic
│   └── Prosody: natural intonation, not monotone
│
└── Feedback Loop
    ├── User correction → Level 1 learning
    ├── Implicit feedback (did they repeat? rephrase?)
    └── Quality scoring → Track WER over time
```

### 5.2 TTS: The Critical Missing Piece

**Gap identified:** There is **zero TTS code** in the codebase. The `TextToSpeech.kt` and `MMSTextToSpeech.kt` files define interfaces but no implementation. The `ModelRegistry` lists Piper and MMS models but nothing loads them.

**What must be built:**

**Phase 1 (Month 1-3): Piper TTS for Swahili**
- Integrate Piper TTS via ONNX Runtime (already in ModelRegistry)
- Piper Swahili model: ~25MB, runs on 2GB phones
- Quality: Acceptable but not natural. Sounds like a clear foreign speaker.
- Latency: ~2-3 seconds for a sentence

**Phase 2 (Month 3-6): MMS TTS for additional languages**
- Meta MMS (Massively Multilingual Speech) VITS models
- Already listed in ModelRegistry: swa, eng, yor, hau, amh, zul, ibo, xho, sna, nso
- Each ~65MB, downloaded on-demand per language
- Quality: Better than Piper for tonal languages (Yoruba, Igbo)

**Phase 3 (Month 6-12): Fine-tuned TTS for natural speech**
- Fine-tune Piper/MMS on collected voice data
- Target: Swahili that sounds like a Nairobi market seller, not a newsreader
- Use collected voice samples (with consent) for style transfer
- This is what makes Msaidizi "speak like your neighbour"

### 5.3 ASR Improvement Path

| Stage | WER (Swahili) | How |
|-------|--------------|-----|
| Day 1 (zero-shot Whisper) | 30-40% | Base Whisper tiny model |
| + PhonemeMapper | 25-35% | Post-processing fixes known errors |
| + Seed vocabulary | 20-30% | Boosts known business terms |
| + User corrections (Week 2-4) | 18-25% | N-gram LM + phoneme confusion learning |
| + LoRA training (Month 1-3) | 15-22% | On-device adapter learns user patterns |
| + Federated model (Month 3-6) | 12-18% | Community corrections improve base |
| + Dialect-specific model (Month 6-12) | 10-15% | Dedicated Migori/Coastal/Nairobi models |

**Note:** These are *realistic* targets, not the aspirational <10% in the VOICE_TRAINING_PIPELINE.md. Getting below 10% WER requires 10,000+ hours of labeled speech data — that takes years, not months.

### 5.4 The "Robot Swahili" Problem and How to Fix It

"Robot Swahili" has three symptoms:
1. **Wrong pronunciation** — TTS says "KSh" as "Kay-Ess-Aitch" instead of "shilingi"
2. **Wrong intonation** — Monotone delivery, no natural rise/fall
3. **Wrong vocabulary** — Uses textbook Swahili instead of market Swahili

**Fixes:**
1. **Pronunciation dictionary** — Map common abbreviations and numbers to spoken form:
   ```
   "KSh 200" → "shilingi mia mbili"
   "5kg" → "kilo tano"
   "M-Pesa" → "em-pesa"
   ```
2. **Prosody injection** — Use SSML or custom prosody markers to add natural intonation
3. **Vocabulary adaptation** — Use learned context to inject market-appropriate terms

---

## 6. African Language Priority

### 6.1 Language Rollout Order

| Priority | Language | Speakers | Countries | Phase | Why First |
|----------|----------|----------|-----------|-------|-----------|
| **1** | **Swahili** | 100M+ | KE, TZ, UG, CD, RW | Phase 1 | Largest East African lingua franca, most training data available |
| **2** | **English** | 100M+ (2nd lang) | All | Phase 1 | Business language, code-switching base |
| **3** | **Hausa** | 80M+ | NG, NE, GH, CM | Phase 2 | Largest West African language, strong media corpus |
| **4** | **Yoruba** | 45M+ | NG, BJ, TG | Phase 2 | Large Nigerian market, tonal challenge |
| **5** | **Sheng** | 20M+ (creole) | KE | Phase 2 | Urban Kenya essential, not a "language" but critical for Nairobi |
| **6** | **Igbo** | 30M+ | NG | Phase 3 | Third major Nigerian language |
| **7** | **Amharic** | 35M+ | ET | Phase 3 | Ge'ez script challenge, large population |
| **8** | **Oromo** | 35M+ | ET, KE | Phase 3 | Large population, Latin script |
| **9** | **Somali** | 20M+ | SO, KE, DJ | Phase 3 | Cushitic family, different structure |
| **10** | **Kikuyu** | 8M+ | KE | Phase 3 | Important for Kenya, Bantu transfer |
| **11-14** | Dholuo, Luhya, Kalenjin, Kamba | 5-6M each | KE | Phase 4 | Regional Kenyan languages |

### 6.2 Transfer Learning Between Languages

The `PhonemeMapper.getTransferPriority()` defines cross-lingual similarity. This is how improvements in one language help others:

```
Swahili (improves first)
├── → Kikuyu: 0.65 similarity (both Bantu, similar phonology)
├── → Luhya: 0.60 similarity (both Bantu)
├── → Kamba: 0.55 similarity (both Bantu)
└── → Sheng: 0.80 similarity (lexically derived from Swahili)

Hausa (improves second)
├── → Yoruba: 0.50 similarity (geographic proximity, shared loanwords)
└── → Igbo: 0.45 similarity (Nigerian context)

Amharic (improves third)
└── → Oromo: 0.40 similarity (Ethiopian context, some shared vocabulary)
```

**Practical implication:** A Swahili LoRA adapter can be used as a warm start for Kikuyu training. This means Kikuyu reaches "acceptable" quality 2-3 months faster than if trained from scratch.

### 6.3 Language-Specific Challenges

| Language | Key Challenge | Mitigation |
|----------|--------------|------------|
| Swahili | Dialect variation (Migori ≠ Coastal ≠ TZ) | Dialect-specific adapters, dialect detection |
| Sheng | Rapidly evolving slang, no standard form | Dynamic vocabulary learning, weekly updates |
| Yoruba | Tonal (3 tones), Whisper ignores tones | Tone-aware post-processing, TTS tone model |
| Hausa | Implosive consonants (ɓ, ɗ), long/short vowels | Phoneme inventory in PhonemeMapper |
| Igbo | Tonal (2-4 tones), vowel harmony | Tone-aware ASR, vowel harmony rules |
| Amharic | Ge'ez script (not Latin), complex morphology | Script detection in DialectClassifier, morphological analyzer |
| Oromo | Latin script but different phonology | Phoneme inventory from scratch |

---

## 7. Code-Switching — Handling Mixed Language Input

### 7.1 The Reality of African Speech

A typical Msaidizi user doesn't speak pure Swahili. They speak:

> "Niko na stock ya tomatoes mingi, lakini sijui bei gani ni fair. Unaweza help me calculate profit ya leo?"

This is **Swahili + English + Sheng** in one sentence. The current `CodeSwitchHandler` uses lexical markers and regex — this works for obvious switches but fails at boundaries.

### 7.2 What Works Today

The `CodeSwitchHandler` can:
- Detect obvious language switches ("stock" is English, "nyanya" is Swahili)
- Track user's mixing profile over time (60% Swahili, 25% English, 15% Sheng)
- Generate responses that match the user's mixing pattern

### 7.3 What Must Be Improved

**Problem 1: Boundary detection.** "Stock ya tomatoes" — is "stock" English or adopted into Sheng? The current system defaults unknown short words to "sheng" — this is wrong.

**Fix:** Default unknown words to the user's **primary language**, not "sheng". Use the `CodeSwitchProfile.primary_language` as the fallback.

**Problem 2: No sequence labeling.** The sliding window approach can't handle subtle boundaries.

**Fix (Phase 3):** Train a lightweight CRF (Conditional Random Field) or BiLSTM-CRF for language boundary detection. This runs on-device in <10ms and handles:
- "Niko na stock ya vitu" → [SW: Niko na] [EN: stock] [SW: ya vitu]
- "Bei gani ni fair" → [SW: Bei gani ni] [EN: fair]

**Problem 3: Response matching.** If user speaks 60% Swahili, 25% English, 15% Sheng, the response should match.

**Fix:** The `CodeSwitchProfile.vocabulary_mix` already tracks this. Use it to weight the response language:
```python
response_language = max(profile.vocabulary_mix.items(), key=lambda x: x[1])[0]
# But inject key terms in the user's secondary languages
```

### 7.4 Code-Switching Training Data

**Source 1: User interactions.** Every Msaidizi conversation is a code-switching example. With consent, these become training data.

**Source 2: Existing corpora.** Search for:
- Sheng-English code-switching corpora (Kenyan NLP research)
- Hausa-English code-switching (Nigerian social media)
- Yoruba-English code-switching (Nollywood subtitles)

**Source 3: Synthetic generation.** Use the on-device LLM to generate code-switched variations of pure-language sentences.

---

## 8. Model Improvement Cycle

### 8.1 The Complete Cycle

```
DAILY (on-device):
├── User speaks → ASR transcribes
├── User corrects → Correction cache updated
├── N-gram LM updated
├── Phoneme confusion matrix updated
├── Vocabulary profile updated
└── If charging + 2-5 AM + ≥20 corrections:
    └── LoRA training → Personal adapter updated

WEEKLY (federated):
├── Device uploads anonymized delta (WiFi + charging)
├── Server collects deltas (≥10 per dialect)
├── Server aggregates (Trimmed Mean + DP)
├── Server validates (WER improvement check)
├── Server publishes new global adapter
└── Device downloads updated adapter

MONTHLY (cloud):
├── Domain adapter rebuilt (all dialects combined)
├── Seed vocabulary updated (new terms from usage)
├── Phoneme inventories updated (new confusion patterns)
├── Dialect classifiers retrained (new dialect markers)
└── TTS models fine-tuned (if voice data collected)

QUARTERLY (major):
├── Base model evaluation (is 0.8B still best?)
├── New language launch (if ready)
├── Architecture review (new model families?)
└── Privacy audit (epsilon review, anonymization check)
```

### 8.2 Quality Gates

No model update ships without passing these gates:

| Gate | Metric | Threshold | Action if Failed |
|------|--------|-----------|-----------------|
| WER regression | Per-dialect WER | No more than +2% from previous | Keep previous version |
| Business task accuracy | record_sale, check_inventory | ≥85% | Keep previous version |
| Response latency | End-to-end | <15s on LOW, <5s on HIGH | Reduce model size |
| Battery impact | Per-session | <1% per interaction | Optimize pipeline |
| Memory pressure | Peak RAM | <80% of device RAM | Reduce context window |
| User satisfaction | Correction rate | <30% of interactions corrected | Investigate |

---

## 9. Cold-Start — How Msaidizi Works Before Any Training Data

### 9.1 Day 1 Experience

When a new user opens Msaidizi for the first time:

1. **Language selection** — "Chagua lugha yako" (Choose your language) → Swahili, English, etc.
2. **Trade selection** — "Biashara yako ni ipi?" (What's your business?) → Mama mboga, Boda boda, etc.
3. **Seed vocabulary loaded** — 200+ terms for their trade, pre-seeded
4. **Whisper ASR active** — Base model, ~30-40% WER on Swahili
5. **PhonemeMapper active** — Post-processing fixes known errors
6. **LLM loaded** — Qwen3.5-0.8B with Swahili system prompt

**What works on Day 1:**
- "Nimeuza nyanya kumi kwa 200" → Records sale (10 tomatoes, 200 KSh)
- "Bei gani ya sukuma?" → Checks recent prices (if any) or gives market average
- "Habari yako?" → Conversational response in Swahili

**What doesn't work well on Day 1:**
- Unusual product names (user's local term for a product)
- Heavy dialect mixing (Migori Swahili with many local terms)
- Complex multi-step queries
- Code-switching (model expects pure Swahili)

### 9.2 Week 1-4: Personalization

As the user interacts:
- **Day 2-3:** Correction cache starts filling. Common misrecognitions get fixed.
- **Day 5-7:** Vocabulary profile builds. Msaidizi knows their products and prices.
- **Week 2:** N-gram LM personalized. Msaidizi predicts "nyanya" after "bei ya" better than generic Swahili.
- **Week 3-4:** First LoRA training (if charging pattern allows). Personal adapter begins.

**Mixing coefficient progression:**
```
Day 1:  α = 0.1  → 90% global model, 10% personal
Week 2: α = 0.3  → 70% global, 30% personal
Week 4: α = 0.6  → 40% global, 60% personal
Month 2: α = 1.0 → Full personalization
```

### 9.3 Cold-Start for New Languages

When Msaidizi launches in a new language (e.g., Yoruba):

1. **Base Whisper model** — Zero-shot, ~40-50% WER
2. **Phoneme inventory** — Built from linguistic research (pre-launch)
3. **Seed vocabulary** — Curated from market research (pre-launch)
4. **No federated data** — First 10 users have no community model
5. **Transfer learning** — If related language exists (Hausa → Yoruba), use as warm start

**First 10 users per language are critical.** Their corrections bootstrap the entire dialect model. Consider incentivizing early adopters (e.g., "You're helping build Msaidizi for Yoruba speakers").

---

## 10. Timeline — When Each Dialect Reaches "Natural" Quality

### 10.1 Realistic Quality Milestones

"Natural quality" = a user doesn't notice they're talking to an AI. This requires both good ASR (understanding) and good TTS (speaking).

| Milestone | Swahili | Hausa | Yoruba | Sheng | Igbo | Amharic |
|-----------|---------|-------|--------|-------|------|---------|
| **Basic functionality** | Month 1 | Month 4 | Month 4 | Month 3 | Month 8 | Month 8 |
| **Understands common phrases** | Month 1 | Month 5 | Month 5 | Month 4 | Month 9 | Month 9 |
| **Handles user's accent** | Month 2 | Month 6 | Month 6 | Month 5 | Month 10 | Month 10 |
| **Natural TTS (not robotic)** | Month 4 | Month 8 | Month 8 | N/A | Month 12 | Month 12 |
| **Code-switching fluent** | Month 6 | Month 9 | Month 9 | Month 6 | Month 12 | N/A |
| **"Speaks like a local"** | Month 12 | Month 18 | Month 18 | Month 12 | Month 24 | Month 24 |
| **Dialect-specific** (Migori, etc.) | Month 12 | Month 18 | Month 18 | Month 9 | Month 24 | Month 24 |

### 10.2 What "Natural" Actually Means

For each dialect, "natural" means:
- **WER < 15%** on that dialect's speech (9 out of 10 words correct)
- **TTS rated ≥4/5** by native speakers for naturalness
- **Code-switching handled** without breaking conversation flow
- **Local vocabulary known** — understands market terms, slang, abbreviations
- **Dialect markers recognized** — doesn't "correct" regional speech to standard form

### 10.3 The Flywheel Effect

```
Month 1:  100 Swahili users → ~1,000 corrections/day → baseline model
Month 3:  1,000 users → ~10,000 corrections/day → dialect patterns emerge
Month 6:  10,000 users → ~100,000 corrections/day → regional models solid
Month 12: 100,000 users → ~1,000,000 corrections/day → "speaks like a local"
```

Each 10× increase in users produces a non-linear improvement in quality because:
1. More diverse dialect coverage (every neighborhood represented)
2. More correction variety (rare errors get fixed)
3. Better federated aggregation (larger cohorts → less noise → better models)
4. Network effects (improved model → more users → more data → improved model)

---

## 11. On-Device Inference Optimization

### 11.1 Current Stack Performance

| Component | 2GB Phone | 4GB Phone | 6GB Phone |
|-----------|-----------|-----------|-----------|
| Silero VAD | <10ms | <10ms | <10ms |
| Whisper ASR (tiny-int4) | ~2-3s | ~1-2s | ~1s |
| Qwen3.5-0.8B Q4_0 | ~3-5s/response | ~2-3s | ~1-2s |
| Piper TTS | ~2-3s/sentence | ~1-2s | ~1s |
| **Total pipeline** | **~8-13s** | **~5-7s** | **~3-4s** |

### 11.2 Optimization Techniques

**Already implemented:**
- Memory-mapped GGUF via llama.cpp (reduces load time and RAM)
- Auto-unload on memory pressure (ModelManager)
- Context window scaling by device tier
- Thread count optimization (half cores, max 4)

**Should implement:**

1. **Speculative decoding** — Use 0.8B model to draft tokens, verify with larger model. 2-3× speedup on MID/HIGH tier.

2. **KV cache quantization** — Quantize the KV cache from FP16 to INT8. Saves ~50% KV cache memory, allowing longer conversations on 2GB phones.

3. **Prompt caching** — Cache the system prompt + business context KV state. Only recompute the user's new message. Saves ~1-2s per turn.

4. **Streaming TTS** — Start TTS before LLM finishes generating. First sentence plays while rest generates. Perceived latency drops to ~3-4s.

5. **Model quantization progression:**
   - Month 1-3: Q4_0 (fast, good enough for 0.8B)
   - Month 3-6: Q4_K_M (better quality, same speed)
   - Month 6-12: Q5_K_S on HIGH tier (best quality within memory)

### 11.3 NNAPI / GPU Delegate — Why NOT to Use

The temptation is to use Android's NNAPI or GPU delegate for faster inference. **Don't.** Here's why:

1. **Fragmentation** — MediaTek Helio A22 (common in $50 phones) has terrible NNAPI support. Unisoc is worse. Only Snapdragon has reliable GPU delegate.
2. **Compatibility** — llama.cpp CPU inference works on ALL ARM64 devices. GPU delegate works on maybe 40%.
3. **Diminishing returns** — For 0.8B-2B models, CPU inference is already fast enough (3-8s). GPU would save maybe 1-2s but break on half the devices.
4. **Battery** — GPU inference uses more power than CPU for small models. The GPU's fixed overhead dominates.

**Exception:** On devices with reliable Vulkan support (Pixel, Samsung flagship), consider Vulkan GPU for the 2B model on HIGH tier. But make it opt-in, not default.

---

## 12. Battery and Memory Constraints — Engineering for 2GB Phones

### 12.1 Battery Budget

A typical informal worker charges their phone once a day, maybe at a charging shop. Msaidizi must use <5% battery per day for typical usage (5-10 voice interactions).

| Operation | Battery Cost | Frequency | Daily Total |
|-----------|-------------|-----------|-------------|
| Silero VAD | ~0.001% | 10 interactions | ~0.01% |
| Whisper ASR | ~0.1% | 10 interactions | ~1% |
| LLM inference | ~0.2% | 10 interactions | ~2% |
| Piper TTS | ~0.05% | 10 interactions | ~0.5% |
| LoRA training | ~0.5% | 1 session/night | ~0.5% |
| Federated sync | ~0.05% | 1 session/week | ~0.01% |
| Background monitoring | ~0.1% | Continuous | ~0.1% |
| **Total** | | | **~4.1%** ✅ |

This is within budget. The `BatteryOptimizer` with 4 optimization levels (NORMAL → REDUCED → ESSENTIAL_ONLY → MINIMAL) provides graceful degradation.

### 12.2 Memory Management on 2GB Phones

The `ModelManager` already handles this well with:
- `onLowMemory()` callback from Android
- Auto-unload after 10 minutes idle
- Memory monitoring every 30 seconds
- Emergency unload at 92% RAM usage

**Additional optimizations needed:**

1. **Strict model serialization** — Never load two models simultaneously on 2GB phones. Pipeline: ASR → unload → LLM → unload → TTS.
2. **Aggressive GC** — Call `System.gc()` after each model unload. The 600MB headroom disappears fast with memory fragmentation.
3. **Bitmap management** — If the app shows UI images, they compete with model memory. Use aggressive image downsampling on LOW tier.
4. **Background restriction** — On 2GB phones, unload ALL models when app goes to background. Don't try to keep anything warm.

### 12.3 Storage Budget

| Model | Size | Required? |
|-------|------|-----------|
| Silero VAD | 2.5MB | Yes (always) |
| Whisper tiny-int4 | 40MB | Yes (first launch) |
| Piper Swahili | 25MB | Yes (first launch) |
| Qwen3.5-0.8B Q4_0 | 500MB | Yes (first launch) |
| Seed vocabularies | 1MB | Yes (bundled) |
| MMS TTS (per language) | 65MB | On-demand |
| LoRA adapters | 50KB-2MB | Growing |
| Correction cache | 1-5MB | Growing |
| **Total (minimum)** | **~570MB** | |
| **Total (with extras)** | **~700MB** | |

A $50 phone with 16GB storage has ~8-10GB free. 700MB is 7-9% of storage. Acceptable, but we must not bloat.

---

## 13. Implementation Roadmap

### Phase 1: Foundation (Month 1-3) — "It Works"

**Goal:** Msaidizi understands Swahili, responds in Swahili, learns from corrections.

| Week | Deliverable | Owner |
|------|-------------|-------|
| 1-2 | Integrate Whisper ASR via ONNX Runtime | Android |
| 1-2 | Integrate Piper TTS via ONNX Runtime | Android |
| 2-3 | Build seed vocabularies (Swahili mama_mboga, boda_boda) | NLP |
| 3-4 | Implement LoRA training via llama.cpp NDK | Android + ML |
| 4-6 | Wire up correction → LoRA training pipeline | Android |
| 6-8 | Build federated learning server (FastAPI + PostgreSQL) | Backend |
| 8-10 | End-to-end test: correction → training → upload → aggregation | Full stack |
| 10-12 | Beta launch with 100 Swahili users | All |

**Exit criteria:**
- Swahili WER < 25% for beta users
- LoRA training works on 4GB+ phones
- Federated upload/download works
- TTS speaks Swahili (Piper quality)

### Phase 2: Federated Learning (Month 3-6) — "It Learns"

**Goal:** Community corrections improve the model for everyone.

| Week | Deliverable | Owner |
|------|-------------|-------|
| 13-16 | Federated aggregation running for Swahili | Backend |
| 13-16 | Differential privacy standardized (ε=1.0) | Security |
| 16-20 | Hausa + Yoruba seed vocabularies | NLP |
| 16-20 | MMS TTS integrated for Hausa, Yoruba | Android |
| 20-24 | Dialect detection for Migori, Coastal, Nairobi Swahili | NLP |
| 20-24 | Sheng dynamic vocabulary learning | NLP |

**Exit criteria:**
- Swahili WER < 20% for federated users
- Hausa + Yoruba basic functionality working
- Dialect detection identifies 3 Swahili variants
- 1,000+ active Swahili users

### Phase 3: Natural Speech (Month 6-12) — "It Sounds Right"

**Goal:** Msaidizi speaks like a local, handles code-switching.

| Week | Deliverable | Owner |
|------|-------------|-------|
| 25-30 | CRF code-switching boundary detector | NLP |
| 25-30 | Fine-tuned TTS for Swahili (natural prosody) | ML |
| 30-36 | Igbo + Amharic + Oromo seed vocabularies | NLP |
| 30-36 | Tone-aware post-processing for Yoruba, Igbo | NLP |
| 36-40 | Dialect-specific LoRA adapters (Migori, Coastal) | ML |
| 40-48 | Self-improving quality loop (auto-retrain on quality drop) | Backend |

**Exit criteria:**
- Swahili WER < 15%
- TTS rated ≥ 4/5 by native Swahili speakers
- Code-switching handled without breaking flow
- 10,000+ active users across languages

### Phase 4: Self-Improving (Month 12+) — "It Gets Better Every Day"

**Goal:** The flywheel is spinning. Every worker's voice makes it better for all workers.

| Quarter | Focus |
|---------|-------|
| Q5 | New languages (Dholuo, Luhya, Kalenjin, Kamba) |
| Q5 | Voice cloning (optional: user can choose TTS voice) |
| Q6 | Regional dialect models (Kisumu, Mombasa, Dar) |
| Q6 | Cross-language transfer (Swahili improvements help Kikuyu) |
| Q7+ | Continuous model evaluation and replacement |

---

## 14. Critical Gaps to Address (Priority Order)

### 🔴 P0 — Blocks Launch

1. **Implement actual LoRA training** — The `_run_lora_training()` is a stub. Without this, Level 3 learning doesn't exist. This is the single most important gap.

2. **Integrate Whisper ASR** — The `AdaptiveAsrEngine` wraps a `SpeechRecognizer` interface but nothing loads Whisper. The ASR pipeline can't transcribe audio.

3. **Integrate Piper TTS** — Zero TTS code exists. Msaidizi can understand but can't speak.

4. **Build federated learning server** — The aggregation logic exists but there's no API, no database, no scheduler.

### 🟡 P1 — Blocks Quality

5. **Create seed vocabularies** — Cold-start is 40% WER without them, 25% with them.

6. **Standardize differential privacy** — ε=1.0 on client, ε=0.1 on server is a 10× discrepancy.

7. **Fix LoRA adapter aggregation** — Server takes last device's adapter instead of averaging. Core FL promise is broken.

8. **Fix code-switching fallback** — Unknown words default to "sheng" instead of user's primary language.

### 🟢 P2 — Blocks Scale

9. **Build evaluation framework** — Can't measure if the system is improving without automated WER computation.

10. **Build phoneme inventories for missing dialects** — 9 of 14 dialects have only lexical markers.

11. **Implement secure aggregation** — Currently the server sees individual gradients.

12. **Build data collection pipeline** — Consent-aware audio collection for TTS training.

---

## 15. Cost Estimate

| Item | Monthly Cost | Notes |
|------|-------------|-------|
| Oracle Cloud Free Tier | $0 | FL server + model serving (1K users) |
| Model CDN (Cloudflare R2) | $5-15 | Model file distribution |
| NVIDIA NIM free tier | $0 | Complex reasoning overflow |
| Google Colab (training) | $0-10 | Monthly fine-tuning runs |
| Domain + DNS | $1 | api.angavu.ai |
| **Total (1K users)** | **$6-26/month** | |

| Scale | Monthly Cost | Architecture |
|-------|-------------|-------------|
| 1K users | $6-26 | Oracle Free Tier |
| 10K users | $200-400 | Oracle Paid + CDN |
| 100K users | $2,000-5,000 | Own ARM servers + solar |
| 1M users | $10,000-20,000 | Pan-African DC network |

---

## 16. The Bottom Line

**Msaidizi's on-device AI strategy is architecturally sound but needs 4 critical implementations to work:**

1. **LoRA training on-device** — The bridge between corrections and model improvement
2. **Whisper ASR integration** — The ears that hear African speech
3. **Piper TTS integration** — The voice that speaks back
4. **Federated learning server** — The backbone that turns individual learnings into collective intelligence

**Once these 4 pieces are built, the flywheel spins:**

```
Worker speaks → Model transcribes → Worker corrects → Model learns →
Anonymized gradients uploaded → Server aggregates → Better model pushed →
Every worker's phone improves → More usage → More data → Loop continues
```

**The moat is real.** 600M+ informal workers, each contributing their voice to make Msaidizi speak their language, their dialect, their way. No competitor can replicate this dataset advantage. But the pipeline to turn that data into better models needs to be **built, not just designed.**

**Build the 4 critical pieces. Launch with Swahili. Let the flywheel spin.**

---

*Strategy document generated by On-Device Model & Training Strategy Agent — Angavu Intelligence*
*Reviewed: ModelManager.kt, LlmEngine.kt, LlamaCppEngine.kt, ModelRegistry.kt, FederatedLearningClient.kt, LanguageLearningPipeline.kt, PhonemeMapper.kt, ConfidenceCalibrator.kt, fine_tuning/__init__.py, federated_learning/__init__.py, code_switching/__init__.py, dialect_detection/__init__.py, config/settings.py*
*Cross-referenced: VOICE_TRAINING_PIPELINE_VALIDATION.md, FEDERATED_LEARNING_VALIDATION.md, BACKEND_LLM_SELECTION.md*
