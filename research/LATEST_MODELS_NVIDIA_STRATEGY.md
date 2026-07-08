# Latest Models & NVIDIA API Strategy for Angavu Intelligence

**Date:** 2026-07-08  
**Prepared for:** Angavu Intelligence Founder  
**Context:** Africa's 600M+ informal workers — AI operating system  

---

## 1. NVIDIA NIM API — Models, Free Tier & Pricing

### What's Available (as of July 2026)

NVIDIA NIM (build.nvidia.com) hosts **100+ models** as inference microservices. Key models include:

| Model Family | Specific Models on NIM | Architecture |
|---|---|---|
| DeepSeek | V4 Pro (1.6T/49B active), V4 Flash (284B/13B active) | MoE |
| GLM | GLM-5.2 (753B, MoE) | MoE |
| Kimi | K2, K2.7 Code (1T/32B active) | MoE |
| Qwen | Various Qwen 3.x models | Dense/MoE |
| Gemma | Gemma 4 family (E2B, E4B, 12B, 27B) | Dense |
| Llama | Llama 4 Scout/Maverick | MoE |
| Mistral/Devstral | Devstral 2 | Dense |
| Nemotron | Nemotron 3 Ultra (550B/55B active) | MoE |
| MiniMax | M3 | MoE |

### Free Tier (Critical for Angavu)

- **Free API access** is available on build.nvidia.com for experimentation
- **Rate limit: 40 RPM** (requests per minute) on free tier — severely limiting for production
- Free tier is **for evaluation only**, not production use
- No explicit "startup credits" program found — NVIDIA's free tier is the main avenue
- Models available free: DeepSeek V4 Flash, GLM-5.2, Kimi K2, Gemma 4, Llama 4, Nemotron, etc.

### Pricing

- NVIDIA NIM pricing is **usage-based** (per token) for production
- Specific per-token pricing varies by model — not publicly listed in a single page
- For production use, NVIDIA routes through cloud partners or self-hosted NIM containers
- **Self-hosted NIM** is free (you bring your own GPU infrastructure)

### African Language Support

- **None of the NIM-hosted models have verified African language training data** (Swahili, Yoruba, Hausa)
- DeepSeek, Qwen, GLM are trained primarily on Chinese + English + major European languages
- Gemma 4 is "natively multilingual" but focuses on ~140 languages — unclear African language coverage
- **This is Angavu's core differentiator** — no cloud API will have this built in

### Fine-Tuning Support

- NIM supports fine-tuning via NVIDIA NeMo framework
- Self-hosted NIM containers can be fine-tuned on custom data
- Fine-tuning requires significant GPU resources (not free tier)

---

## 2. Qwen 3.6 — Alibaba's Latest

### Models Released (April 2026)

| Variant | Parameters | Active Params | Context | License |
|---|---|---|---|---|
| Qwen3.6-Plus | Hosted only | — | 1M tokens | Proprietary (API) |
| Qwen3.6-27B | 27B dense | 27B | 128K | Apache 2.0 |
| Qwen3.6-35B-A3B | 35B total | **3B active** (MoE) | 262K | Apache 2.0 |

### Key Details
- **Qwen3.6-27B**: Flagship open-source dense model, strong coding performance
- **Qwen3.6-35B-A3B**: MoE with only 3B active params — **extremely efficient**
- **Qwen3 Coder Next**: 80B total / 3B active, Apache 2.0, optimized for coding agents
- Qwen 3.7 Max also exists (flagship, API-only, 50% off promotional pricing)
- Alibaba shut down the free tier of Qwen API (as of April 2026)

### Oracle Cloud Free Tier Feasibility
- **Qwen3.6-35B-A3B (3B active)**: ✅ Can run on 24GB RAM with quantization (INT4/INT8)
- **Qwen3.6-27B**: ⚠️ Tight fit — needs ~14GB at INT4, possible but limited headroom
- **Qwen3 Coder Next (80B/3B active)**: ✅ 3B active params can run on 24GB

### African Language Support
- Qwen trained on 29+ languages, primarily Chinese/English/European/Asian
- **No specific African language training data confirmed**
- Multilingual capability exists but Swahili/Yoruba/Hausa quality is unverified

### Fine-Tuning
- Apache 2.0 license — fully fine-tunable
- Qwen has excellent fine-tuning ecosystem (LoRA, QLoRA well-supported)

---

## 3. GLM 5.2 — Zhipu AI

### Specifications
| Spec | Value |
|---|---|
| Total Parameters | **753B** |
| Architecture | MoE (Mixture of Experts) |
| Active Parameters | ~50-70B estimated per token |
| Context Window | **1M tokens** |
| License | **MIT** (fully permissive) |
| Released | June 2026 |
| Developer | Zhipu AI (Z.ai), Beijing |

### Performance
- **Competes with Claude Opus 4** on coding benchmarks
- Kilo Bench: 53.0% (top-tier open-weight)
- Strong on SWE-Bench, software engineering, long-horizon agent tasks
- Available on NVIDIA NIM as GLM-5.2-FP8

### Oracle Cloud Free Tier Feasibility
- **❌ Cannot self-host** — 753B params requires hundreds of GB VRAM
- Even INT4 quantization would need ~200GB+ RAM
- Must use API access (NVIDIA NIM or Zhipu's own API)

### African Language Support
- **No confirmed African language training**
- Primarily Chinese/English focused

### Fine-Tuning
- MIT license — legally unrestricted fine-tuning
- But impractical to fine-tune without massive GPU cluster

---

## 4. Kimi K2.7 Code — Moonshot AI

### Specifications
| Spec | Value |
|---|---|
| Total Parameters | **1 trillion** |
| Architecture | MoE |
| Active Parameters | **32B per token** |
| Context Window | 262K tokens |
| License | Modified MIT |
| Released | June 12, 2026 |
| Developer | Moonshot AI |

### Performance
- **Kilo Bench: 60.7%** (highest among open-weight models as of July 2026)
- Coding-focused, agentic capabilities
- Native multimodal MoE
- 10x performance leap on NVIDIA GB200 NVL72

### Oracle Cloud Free Tier Feasibility
- **❌ Cannot self-host** — 1T params, even 32B active needs significant VRAM
- 32B active at INT4 ≈ 16GB — technically possible on 24GB but very tight with overhead
- Best accessed via API

### African Language Support
- **No confirmed African language training**

### Fine-Tuning
- Modified MIT — check specific terms, generally permissive for commercial use

---

## 5. MiniMax M3

### Specifications
| Spec | Value |
|---|---|
| Total Parameters | Not publicly disclosed (likely 300B-1T range) |
| Architecture | MoE with MSA (MiniMax Sparse Attention) |
| Context Window | **1M tokens** |
| License | Open weights (specific license TBD) |
| Released | June 1, 2026 |
| Developer | MiniMax |

### Performance
- Kilo Bench: 47.6%
- SWE-Bench Pro: 59.0%
- Terminal-Bench 2.1: 66.0%
- **First open-weight model with frontier coding + 1M context + native multimodality**
- Supports image and video input, can operate desktop computers
- MSA architecture: per-token compute is 1/20th of previous-gen at 1M context

### Oracle Cloud Free Tier Feasibility
- **❌ Likely cannot self-host** — frontier-class model, probably needs 100GB+ RAM
- Must use API

### African Language Support
- **No confirmed African language training**

---

## 6. DeepSeek V4 (Latest)

### Models (April 2026)

| Variant | Total Params | Active Params | Context | License |
|---|---|---|---|---|
| DeepSeek V4 Pro | **1.6T** | **49B** | 1M tokens | MIT |
| DeepSeek V4 Flash | **284B** | **13B** | 1M tokens | MIT |

### Key Details
- V4 Pro: Flagship model, advanced reasoning + coding
- V4 Flash: Efficiency-optimized, fast inference, 1M context
- Both MIT licensed — fully permissive
- Available on NVIDIA NIM

### Oracle Cloud Free Tier Feasibility
- **V4 Flash (13B active)**: ✅ Feasible at INT4 quantization (~7-8GB for active params, but total model is 284B so routing tables add overhead). Realistically needs 32-64GB RAM for the full MoE model.
- **V4 Pro (49B active)**: ❌ Not feasible on 24GB RAM
- **Note**: MoE models need ALL parameters in memory even though only a subset activates. 284B at INT4 = ~142GB. **Cannot run on 24GB.**

### African Language Support
- **No confirmed African language training**
- Chinese/English primary, with some multilingual capability

---

## 7. Gemma 4 — Google's Latest

### Models (April 2026)

| Variant | Parameters | Target |
|---|---|---|
| Gemma 4 E2B | **2B** | Mobile/IoT |
| Gemma 4 E4B | **4B** | Mobile/Laptop |
| Gemma 4 12B | **12B** | General |
| Gemma 4 27B | **27B** | Server |

### Key Details
- **Purpose-built for on-device agentic workflows**
- QAT (Quantization-Aware Training) variants for mobile/laptop efficiency
- Natively multimodal (text, image, video, audio)
- "Byte for byte, the most capable open models"
- Available on NVIDIA NIM and Google AI Edge Gallery
- Gemma 3n also exists — natively multilingual

### Oracle Cloud Free Tier Feasibility
- **E2B (2B)**: ✅ Easily runs on any device
- **E4B (4B)**: ✅ Runs on 24GB RAM comfortably
- **12B**: ✅ Runs on 24GB RAM (INT4 ≈ 6-7GB)
- **27B**: ⚠️ Tight at INT4 (~14GB), possible with limited headroom

### African Language Support
- Gemma 3n is "natively multilingual" — **best bet among open models for African languages**
- Google has invested in African language datasets (via Google Translate, etc.)
- **Gemma likely has the best African language support of all models listed here**

### Fine-Tuning
- Google provides fine-tuning guides and Colab notebooks
- Gemma models are designed for fine-tuning
- License: Google's Terms of Use (permissive for commercial use, some restrictions)

---

## 8. Mistral Latest

### Models (2026)

| Model | Notes |
|---|---|
| **Devstral 2 (2512)** | Coding-focused, open-weight, available on NIM |
| Mistral Large | Proprietary flagship |
| Magistral | Reasoning-focused model (if released) |

### Key Details
- Devstral 2 is Mistral's main open-weight coding contribution in 2026
- Available on NVIDIA NIM
- Mistral has shifted toward proprietary models for frontier capabilities

### Oracle Cloud Free Tier
- Devstral 2 size unclear — likely 70B+ range, may be tight on 24GB

### African Language Support
- **No confirmed African language training**
- European languages (French, German, Spanish) are strong — French could help for West/Central Africa

---

## 9. Llama Latest — Meta

### Models (2025-2026)

| Model | Parameters | Architecture | Context |
|---|---|---|---|
| Llama 4 Scout | 17B active (109B total) | MoE (16 experts) | 10M tokens |
| Llama 4 Maverick | 17B active (400B total) | MoE (128 experts) | 1M tokens |
| **Muse Spark** | Proprietary (April 2026) | Unknown | Unknown |

### Key Details
- Llama 4 released April 2025 — multimodal, MoE architecture
- **Muse Spark** (April 2026): Meta's new proprietary model under "Superintelligence Labs" — marks shift away from pure open-source
- Llama 4 Scout fits on a single H100 GPU
- Llama Community License — free for <700M monthly active users

### Oracle Cloud Free Tier Feasibility
- **Llama 4 Scout (109B total, 17B active)**: ❌ 109B at INT4 ≈ 55GB, exceeds 24GB
- Must use smaller Llama models (Llama 3.x 8B variants) or API

### African Language Support
- Llama 3/4 trained on **30+ languages** including some African languages
- **Swahili is confirmed** in Llama training data
- Better African language support than most Chinese models

---

## 10. Comparative Summary

| Model | Params (Total/Active) | Self-Host on 24GB? | License | African Lang | API Cost |
|---|---|---|---|---|---|
| AfriqueQwen-14B | 14B/14B | ✅ Yes | Apache 2.0 | ✅ Fine-tuned | Free (self-host) |
| Qwen3.6-35B-A3B | 35B/3B | ✅ Yes | Apache 2.0 | ❌ Unverified | Alibaba API |
| Qwen3.6-27B | 27B/27B | ⚠️ Tight | Apache 2.0 | ❌ Unverified | Alibaba API |
| Gemma 4 E4B | 4B/4B | ✅ Yes | Google ToS | ⚠️ Possible | Free on device |
| Gemma 4 12B | 12B/12B | ✅ Yes | Google ToS | ⚠️ Possible | Free on device |
| Gemma 4 27B | 27B/27B | ⚠️ Tight | Google ToS | ⚠️ Possible | NIM free tier |
| DeepSeek V4 Flash | 284B/13B | ❌ No | MIT | ❌ Unverified | NIM free tier |
| DeepSeek V4 Pro | 1.6T/49B | ❌ No | MIT | ❌ Unverified | NIM paid |
| GLM 5.2 | 753B/~60B | ❌ No | MIT | ❌ Unverified | NIM free tier |
| Kimi K2.7 Code | 1T/32B | ❌ No | Modified MIT | ❌ Unverified | NIM free tier |
| MiniMax M3 | ~500B+/unknown | ❌ No | Open weights | ❌ Unverified | API |
| Llama 4 Scout | 109B/17B | ❌ No | Llama Community | ✅ Swahili | NIM free tier |

---

## 11. STRATEGY RECOMMENDATION

### The Constraint
> "Zero paid APIs for core functionality"

This is a **hard constraint** and a **competitive moat**. It means Angavu must self-host everything that touches core user workflows.

### The Hybrid Strategy: "Self-Hosted Core + Free-Tier Intelligence Boost"

#### Tier 1: Core (Self-Hosted, Zero Cost, Always Available)
**AfriqueQwen-14B** on Oracle Cloud Free Tier
- 14B parameters, fine-tuned for African languages
- Runs comfortably on 4 OCPUs + 24GB RAM
- Handles: daily tasks, language understanding, basic reasoning, UI interactions
- **This is the heart of Angavu — never goes down, never costs money, never sends data to third parties**

#### Tier 2: Enhanced (Self-Hosted, Zero Cost)
**Add one efficient self-hosted model for coding/technical tasks:**
- **Qwen3.6-35B-A3B** (3B active, Apache 2.0) — runs on 24GB RAM with quantization
- Or **Gemma 4 12B** (Google ToS, runs on 24GB) — best multilingual support
- Handles: code generation, technical reasoning, structured output

#### Tier 3: Intelligence Boost (NVIDIA NIM Free Tier, 40 RPM)
**Use NVIDIA NIM free tier for complex reasoning tasks that exceed self-hosted capability:**
- **GLM 5.2** or **DeepSeek V4 Flash** for complex multi-step reasoning
- **Kimi K2.7 Code** for advanced coding tasks
- **Rate limit: 40 RPM** — sufficient for non-real-time complex tasks
- Use case: complex business plan generation, multi-step financial analysis, advanced troubleshooting
- **Not for core loop** — only for tasks where 14B model says "I need help"

#### Tier 4: Aspirational (Future)
- Apply for NVIDIA Inception program (startup accelerator — may offer GPU credits)
- Apply for Google for Startups Cloud credits
- Monitor Alibaba Qwen free tier re-launch

### Architecture Decision

```
┌─────────────────────────────────────────────┐
│              Angavu User Request             │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│     AfriqueQwen-14B (Self-Hosted, Core)     │
│     Handles 90% of requests                  │
│     African languages, daily tasks, UI       │
└──────────┬──────────────────┬───────────────┘
           │                  │
    Simple task          Complex task
           │                  │
           ▼                  ▼
┌─────────────────┐  ┌────────────────────────┐
│  Respond Directly│  │ Can I handle this?     │
│  (90% of cases)  │  │ (14B self-assessment)  │
└─────────────────┘  └───────┬────────────────┘
                             │
                      Yes ──┘└── No (complex)
                      │            │
                      ▼            ▼
              ┌──────────────┐  ┌──────────────────┐
              │ Respond      │  │ NVIDIA NIM Free   │
              │ (fallback)   │  │ GLM 5.2 / DeepSeek│
              └──────────────┘  │ / Kimi K2.7       │
                               │ 40 RPM limit      │
                               └──────────────────┘
```

### Why This Works for Angavu

1. **Zero paid APIs for core** ✅ — AfriqueQwen-14B handles all core workflows
2. **African language excellence** ✅ — Fine-tuned model, not generic
3. **Data sovereignty** ✅ — User data never leaves Angavu's infrastructure for core tasks
4. **Intelligence ceiling raised** ✅ — NVIDIA NIM free tier for occasional complex tasks
5. **Cost: $0/month** ✅ — Oracle free tier + NVIDIA free tier
6. **Resilience** ✅ — If NVIDIA free tier degrades, core still works perfectly

### What NOT to Do

- ❌ **Don't make NVIDIA NIM a dependency** — 40 RPM is too low for production
- ❌ **Don't try to self-host 753B+ models** — impossible on free tier
- ❌ **Don't use Alibaba Qwen API** — they killed the free tier
- ❌ **Don't chase the biggest model** — 14B fine-tuned > 753B generic for African languages

### Action Items

1. **Immediate**: Continue AfriqueQwen-14B as primary model
2. **This week**: Sign up for NVIDIA NIM free tier, test GLM 5.2 and DeepSeek V4 Flash
3. **This month**: Evaluate Qwen3.6-35B-A3B or Gemma 4 12B as secondary self-hosted model
4. **Ongoing**: Apply for NVIDIA Inception, Google for Startups, Oracle for Startups programs
5. **Monitor**: Qwen 3.7 free tier, new MoE models that might fit in 24GB

### The Bottom Line

**Self-hosted core + free API boost is the right strategy.** Angavu's "zero paid APIs" principle is not just a cost constraint — it's a product differentiator. Users trust a platform that keeps their data local. The 14B model, fine-tuned for African languages, will outperform any 753B generic model on Swahili, Yoruba, and Hausa tasks. Use NVIDIA NIM as an occasional intelligence boost, not a crutch.

---

*Research conducted 2026-07-08 via web search and official documentation. Model availability and pricing change frequently — verify before committing.*
