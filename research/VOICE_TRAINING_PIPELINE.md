# Msaidizi Voice Training Pipeline
## Training on Worker Voices to Become Multi-Language

**Author:** Valentine Owuor — BSc Economics & Statistics
**Platform:** Angavu Intelligence / Msaidizi
**Date:** July 2026

---

## The Vision

Msaidizi doesn't rely on existing models to speak African languages. Existing models are terrible at Swahili, Yoruba, Hausa, Amharic, Zulu. Instead, Msaidizi **trains on the recorded voices of actual workers** — your mum's voice, every trader's voice, every boda boda rider's voice.

Over time, Msaidizi becomes the best African language AI in existence. Not because a tech company built it — but because **600M+ workers trained it with their own voices.**

---

## The Pipeline (5 Phases)

```
┌─────────────────────────────────────────────────────────────┐
│                VOICE TRAINING PIPELINE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PHASE 1: CAPTURE (On-Device, Immediate)                    │
│  ├── Worker speaks to Msaidizi during onboarding            │
│  ├── Audio recorded locally (16kHz, mono, WAV)              │
│  ├── Whisper ASR transcribes audio                          │
│  ├── Worker corrects misunderstandings                      │
│  └── Correction pairs stored: (audio, correct_text)         │
│                                                             │
│  PHASE 2: LEARN (On-Device, Continuous)                     │
│  ├── PhonemeMapper learns worker's specific pronunciation   │
│  ├── AdaptiveAsrEngine adapts to worker's accent            │
│  ├── AdaptiveVocabulary learns trade-specific words         │
│  ├── Code-switching patterns detected (Swahili+English)     │
│  └── All learning stays on device                           │
│                                                             │
│  PHASE 3: AGGREGATE (Federated Learning, Weekly)            │
│  ├── FederatedLearningClient sends anonymous gradients      │
│  ├── ε=0.1 differential privacy (34× noise)                │
│  ├── k-anonymity (k≥10) — no individual identifiable       │
│  ├── Backend aggregates from thousands of workers           │
│  └── No raw audio leaves the device — EVER                  │
│                                                             │
│  PHASE 4: TRAIN (Backend, Monthly)                          │
│  ├── Aggregated gradients used to fine-tune ASR model       │
│  ├── Per-dialect models trained (14 dialects)               │
│  ├── Code-switching model trained on mixed speech           │
│  ├── TTS model trained for natural pronunciation            │
│  └── QLoRA fine-tuning on free Kaggle/Colab GPUs           │
│                                                             │
│  PHASE 5: DEPLOY (Back to Devices, Monthly)                 │
│  ├── Improved ASR model pushed to devices                   │
│  ├── Improved TTS model pushed to devices                   │
│  ├── New vocabulary auto-detected and added                 │
│  ├── Msaidizi speaks more naturally now                     │
│  └── Cycle repeats — gets better every month                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: CAPTURE (What Happens on Day 1)

### Onboarding Voice Capture
When your mum first opens Msaidizi:

```
Msaidizi: "Karibu! Unaitwa nani?" (Welcome! What's your name?)
Mum: "Mimi ni Mama Grace, nafanya biashara ya mboga Gikomba."
     (I am Mama Grace, I do vegetable business at Gikomba.)

[Audio recorded: mama_grace_onboarding_001.wav]
[Whisper ASR transcribes: "Mimi ni Mama Grace, nafanya biashara ya mboga Gikomba"]
[Worker confirms: "Ndio, ni sawa!" (Yes, that's correct!)]
[Correction pair stored: (audio, "Mimi ni Mama Grace, nafanya biashara ya mboga Gikomba")]
```

### Daily Voice Capture
Every time your mum talks to Msaidizi:

```
Mum: "Nimenunua nyanya kilo 5 kwa Sh 200, nimeuza kwa Sh 350."
     (I bought 5kg tomatoes for 200 shillings, sold for 350.)

[Audio recorded]
[ASR transcribes]
[If correct → stored as positive example]
[If wrong → worker corrects → stored as correction pair]
```

### What's Captured
| Data | Format | Storage | Leaves Device? |
|------|--------|---------|----------------|
| Audio recording | 16kHz WAV | Local SQLite | ❌ NEVER |
| ASR transcription | Text | Local SQLite | ❌ NEVER |
| Worker correction | Text | Local SQLite | ❌ NEVER |
| Dialect detected | Label | Local SQLite | ❌ NEVER |
| Confidence score | Float | Local SQLite | ✅ Anonymous aggregate |

---

## Phase 2: LEARN (What Msaidizi Learns Per Worker)

### PhonemeMapper — Learns Pronunciation
```kotlin
// Worker says "nyanya" (tomato) with specific pronunciation
// PhonemeMapper records: /ɲaɲa/ → worker's specific /njaɲa/ variant
// Future ASR recognizes this worker's pronunciation
```

### AdaptiveAsrEngine — Adapts to Accent
```kotlin
// Worker has Gikomba market accent
// ASR adapts word boundaries, tone patterns, rhythm
// Gets better at understanding THIS specific worker
```

### AdaptiveVocabulary — Learns Trade Words
```kotlin
// Worker sells vegetables → learns: nyanya, sukuma, wiki, karoti, vitunguu
// Worker is boda boda → learns: passenger, nduthi, route, fare, mzigo
// Worker is jua kali → learns: fundi, chuma, mashine, mafuta, spare
```

### Code-Switching Detection
```kotlin
// Worker says: "Nimenunua tomatoes kwa Sh 200, then nimeuza kwa Sh 350"
// Detects: Swahili → English → Swahili switching
// Learns: this worker mixes languages naturally
// Future: handles mixed speech without confusion
```

---

## Phase 3: AGGREGATE (Federated Learning)

### What Leaves the Device
```
Worker's phone sends:
├── Anonymous gradient updates (NOT raw audio)
├── Dialect label (e.g., "sw-KE" for Kenyan Swahili)
├── Model improvement delta
└── Privacy budget: ε=0.1 (34× noise added)

What NEVER leaves the device:
├── Raw audio recordings
├── Transcriptions
├── Worker identity
├── Location data
└── Business data
```

### Backend Aggregation
```
Backend receives gradient updates from 1,000+ workers per dialect:
├── Kenyan Swahili: 5,000 workers → aggregate gradients
├── Sheng: 3,000 workers → aggregate gradients
├── Dholuo: 1,000 workers → aggregate gradients
├── Yoruba: 2,000 workers → aggregate gradients
└── ... (14 dialects)

Differential privacy ensures no individual is identifiable.
k-anonymity (k≥10) ensures at least 10 workers contribute per update.
```

---

## Phase 4: TRAIN (Backend Model Training)

### ASR Model Fine-Tuning
```
Base model: Whisper small (244M params)
Fine-tuning: QLoRA on aggregated dialect data
Training data: 10,000+ correction pairs per dialect
Training cost: $0 (free Kaggle/Colab GPUs)
Output: whisper-swahili-v1.gguf, whisper-sheng-v1.gguf, etc.
```

### TTS Model Training
```
Base model: Piper TTS
Fine-tuning: Voice cloning from aggregated speech samples
Training data: 5,000+ voice samples per dialect
Output: piper-swahili-v1.onnx, piper-sheng-v1.onnx, etc.
```

### Code-Switching Model
```
Training: Mixed Swahili-English-Sheng utterances
Challenge: Model must handle language boundaries within sentences
Solution: Train on actual worker speech (not synthetic data)
```

---

## Phase 5: DEPLOY (Back to Devices)

### Monthly Model Update
```
Backend pushes to devices:
├── whisper-swahili-v2.gguf (improved ASR)
├── piper-swahili-v2.onnx (improved TTS)
├── vocabulary-update.json (new words detected)
└── dialect-model-update.json (dialect improvements)

Device applies update:
├── Hot-swap model (no app restart needed)
├── Msaidizi immediately speaks better
└── Worker notices: "Msaidizi inaelewa vizuri zaidi!"
    (Msaidizi understands better now!)
```

### The Flywheel
```
Worker speaks → Msaidizi learns → Better models → Worker uses more →
More data → Better models → More workers → Better models → ...
```

Every month, Msaidizi gets better. Every worker makes it better. The moat deepens.

---

## Timeline

| Phase | Timeline | Milestone |
|-------|----------|-----------|
| Phase 1 (Capture) | Day 1 | Onboarding voice capture working |
| Phase 2 (Learn) | Week 1-4 | Per-worker adaptation working |
| Phase 3 (Aggregate) | Month 1-3 | Federated learning operational |
| Phase 4 (Train) | Month 3-6 | First dialect models trained |
| Phase 5 (Deploy) | Month 6-12 | Improved models on devices |
| Continuous | Month 12+ | Self-improving flywheel |

---

## Academic Framework

| Phase | Academic Foundation | Degree Unit |
|-------|-------------------|-------------|
| Capture | Data collection methodology | STA 343 (Experimental Design) |
| Learn | Bayesian updating | STA 142 (Probability) |
| Aggregate | Differential privacy | STA 444 (Non-Parametric Methods) |
| Train | Statistical learning | STA 347 (Statistical Computing) |
| Deploy | Quality control | STA 346 (Statistical Quality Control) |
| Flywheel | Endogenous growth | ECO 100 (Development Economics) |

---

## The Result

After 12 months:
- Msaidizi speaks **14 dialects** naturally
- Trained on **100,000+ worker voices**
- **Sub-200ms** response latency
- **<10% WER** (Word Error Rate) per dialect
- **No other AI in the world** speaks these languages this well

Because no tech company will ever have access to 600M+ informal workers' voices. But Msaidizi does — because it's **their** tool, trained on **their** voices, serving **their** needs.

**This is the moat. This is the language moat. This is why Angavu wins.** 🎤🌍
