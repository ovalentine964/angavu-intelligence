# Open-Source Models Deep Dive — Angavu Intelligence

**Research Date:** July 7, 2026  
**Researcher:** Angavu Intelligence Research Team  
**Purpose:** Comprehensive evaluation of ALL major open-source model families for Angavu's four use cases: on-device reasoning, cloud reasoning, economic/statistical analysis, and African language support.

---

## Executive Summary

The open-source AI landscape in mid-2026 is radically different from 2024. **MoE architectures dominate**, Apache 2.0 licensing is the norm, and open-weight models have closed most of the gap with proprietary systems. For Angavu's needs, **Qwen 3.5 and Gemma 4 are the strongest candidates** — Qwen for its unmatched multilingual coverage (201 languages including Swahili) and size range, Gemma 4 for its edge-optimized variants and true Apache 2.0 license.

**Key Finding:** No open-source model has strong native support for Yoruba, Hausa, Amharic, or Zulu. Fine-tuning on African language data is **mandatory** regardless of base model choice.

---

## 1. Qwen Family (Alibaba)

### Overview
The Qwen family is the most comprehensive open-source model ecosystem in 2026, spanning from 0.6B to 397B parameters. All dense models use **Apache 2.0** licensing.

### Model Lineup

| Model | Params | Context | License | Release | Key Strengths |
|-------|--------|---------|---------|---------|---------------|
| **Qwen3-0.6B** | 0.6B dense | 32K | Apache 2.0 | Apr 2025 | Smallest, on-device |
| **Qwen3-1.7B** | 1.7B dense | 32K | Apache 2.0 | Apr 2025 | On-device, mobile |
| **Qwen3-4B** | 4B dense | 32K | Apache 2.0 | Apr 2025 | Rivals Qwen2.5-72B performance |
| **Qwen3-8B** | 8B dense | 128K | Apache 2.0 | Apr 2025 | Strong general purpose |
| **Qwen3-14B** | 14B dense | 128K | Apache 2.0 | Apr 2025 | Cloud sweet spot |
| **Qwen3-32B** | 32B dense | 128K | Apache 2.0 | Apr 2025 | High capability |
| **Qwen3-30B-A3B** | 30B total/3B active (MoE) | 128K | Apache 2.0 | Apr 2025 | MoE efficiency |
| **Qwen3-235B-A22B** | 235B total/22B active (MoE) | 128K | Apache 2.0 | Apr 2025 | Frontier reasoning |
| **Qwen3.5-0.8B** | 0.8B dense | 256K | Apache 2.0 | Mar 2026 | Latest small, on-device |
| **Qwen3.5-2B** | 2B dense | 256K | Apache 2.0 | Mar 2026 | Mobile sweet spot |
| **Qwen3.5-4B** | 4B dense | 256K | Apache 2.0 | Mar 2026 | Edge deployment |
| **Qwen3.5-9B** | 9B dense | 256K | Apache 2.0 | Mar 2026 | Desktop/edge server |
| **Qwen3.5-27B** | 27B dense | 256K | Apache 2.0 | Mar 2026 | Server deployment |
| **Qwen3.5 (397B)** | 397B total/17B active (MoE) | 1M | Apache 2.0 | Feb 2026 | Frontier multimodal agent |

### Key Capabilities

- **Multilingual:** 119 languages (Qwen3), 201 languages (Qwen3.5) — **includes Swahili** ✅
- **Reasoning:** Hybrid thinking/non-thinking modes. Qwen3-235B matches DeepSeek-R1 on benchmarks
- **Fine-tuning:** Excellent ecosystem — Unsloth, LoRA, QLoRA all well-supported
- **ARM Performance:** Good — llama.cpp and MLC-LLM support for ARM inference
- **On-device:** Qwen3.5-0.8B and 2B run on Android phones with 2-4GB RAM
- **Context:** Qwen3.5 small models support 256K tokens

### African Language Support

| Language | Support Level | Notes |
|----------|-------------|-------|
| Swahili | ✅ Explicit | Listed in Qwen3 119 languages |
| Yoruba | ⚠️ Partial | Not explicitly listed; may have some coverage |
| Hausa | ⚠️ Partial | Not explicitly listed |
| Amharic | ❌ Not listed | Likely minimal support |
| Zulu | ❌ Not listed | Likely minimal support |

### Angavu Score: **88/100**

**Strengths:** Widest size range, Apache 2.0, 201 languages, excellent fine-tuning ecosystem  
**Weaknesses:** African languages beyond Swahili are weak; Chinese-focused origin may bias training data

---

## 2. Gemma Family (Google)

### Overview
Google's Gemma family underwent a **major licensing shift** in April 2026 — moving to true Apache 2.0 (previously used custom Google terms). Gemma 4 is built from Gemini 3 internals and is the strongest per-byte open model.

### Model Lineup

| Model | Params | Context | License | Release | Key Strengths |
|-------|--------|---------|---------|---------|---------------|
| **Gemma 3 270M** | 270M dense | 32K | Gemma TOU | Aug 2025 | Hyper-efficient, IoT |
| **Gemma 3 1B** | 1B dense | 32K | Gemma TOU | Mar 2025 | Basic on-device |
| **Gemma 3 4B** | 4B dense | 128K | Gemma TOU | Mar 2025 | Mobile deployment |
| **Gemma 3 12B** | 12B dense | 128K | Gemma TOU | Mar 2025 | Edge server |
| **Gemma 3 27B** | 27B dense | 128K | Gemma TOU | Mar 2025 | Single-GPU leader |
| **Gemma 4 E2B** | 2B effective | 128K | Apache 2.0 | Apr 2026 | Edge/mobile, multimodal |
| **Gemma 4 E4B** | 4B effective | 128K | Apache 2.0 | Apr 2026 | Edge, better reasoning |
| **Gemma 4 26B-A4B** | 26B total/4B active (MoE) | 256K | Apache 2.0 | Apr 2026 | Efficient server |
| **Gemma 4 31B** | 31B dense | 256K | Apache 2.0 | Apr 2026 | Frontier reasoning |

### Key Capabilities

- **Multilingual:** 140+ languages (Gemma 3), broad coverage
- **Reasoning:** Gemma 4 31B: 89.2% AIME 2026, 84.3% GPQA Diamond — frontier-level
- **Multimodal:** ALL Gemma 4 variants are natively multimodal (text + image + video + audio)
- **Edge:** E2B/E4B run on **5GB RAM** at 4-bit quantization — fits $50 phones
- **Fine-tuning:** Good ecosystem, Google provides official guides
- **ARM:** Good support via MediaPipe, TensorFlow Lite, MLC-LLM
- **License:** Gemma 4 is Apache 2.0 (true OSI-approved). Gemma 3 uses custom Google terms.

### African Language Support

| Language | Support Level | Notes |
|----------|-------------|-------|
| Swahili | ✅ Supported | Part of 140+ languages |
| Yoruba | ⚠️ Limited | Likely some coverage via multilingual training |
| Hausa | ⚠️ Limited | Not explicitly tested |
| Amharic | ⚠️ Limited | Not explicitly tested |
| Zulu | ⚠️ Limited | Not explicitly tested |

### Angavu Score: **85/100**

**Strengths:** Apache 2.0 (Gemma 4), natively multimodal, excellent edge models (E2B/E4B), strong reasoning  
**Weaknesses:** Gemma 3 uses restrictive Google TOU; African languages not a focus area; Google may change terms

---

## 3. Xiaomi MiMo Family

### Overview
Xiaomi's MiMo family exploded in popularity in 2026 — MiMo-V2-Pro is the **#1 model by traffic on OpenRouter**, processing 4.79T tokens/week. The family focuses on reasoning and coding.

### Model Lineup

| Model | Params | Context | License | Release | Key Strengths |
|-------|--------|---------|---------|---------|---------------|
| **MiMo-V2-Flash** | 309B total/15B active (MoE) | 256K | MIT | Dec 2025 | Efficient reasoning |
| **MiMo-V2-Pro** | 1T+ total/42B active (MoE) | 1M | Bespoke | Mar 2026 | #1 on OpenRouter |
| **MiMo-V2.5 Pro** | 1T+ (improved) | 1M | Bespoke | Apr 2026 | Latest frontier |
| **MiMo-V2.5 DFlash** | ~309B (improved) | 256K | MIT | Apr 2026 | Latest efficient |
| **MiMo-V2-Omni** | 310B/15B active | 256K | Bespoke | Mar 2026 | Multimodal (text+image+audio) |

### Key Capabilities

- **Reasoning:** MiMo-V2-Flash: 94.1% AIME 2025, 83.7% GPQA Diamond. Strong coding: 73.4% SWE-bench
- **Pricing:** MiMo-V2-Pro: $1/M input, $3/M output — competitive
- **Context:** Up to 1M tokens (Pro variants)
- **Fine-tuning:** Good — MIT-licensed Flash variant is fully fine-tunable
- **ARM:** MoE architecture makes it efficient; 15B active params manageable on ARM

### African Language Support

| Language | Support Level | Notes |
|----------|-------------|-------|
| Swahili | ⚠️ Limited | Not explicitly trained for |
| Yoruba | ❌ Not supported | Not in training data |
| Hausa | ❌ Not supported | Not in training data |
| Amharic | ❌ Not supported | Not in training data |
| Zulu | ❌ Not supported | Not in training data |

### Angavu Score: **72/100**

**Strengths:** MIT license (Flash), #1 market adoption, excellent reasoning/coding, competitive pricing  
**Weaknesses:** No African language focus, Pro variant uses restrictive license, no small on-device variants, too large for $50 phones

---

## 4. MiniMax Family

### Overview
Shanghai-based MiniMax released M1 in June 2025 — the first large-scale hybrid-attention reasoning model. Followed by M2.5 and M2.7 in early 2026.

### Model Lineup

| Model | Params | Context | License | Release | Key Strengths |
|-------|--------|---------|---------|---------|---------------|
| **MiniMax-M1** | 456B total/10B active (MoE) | 1M | Open-weight | Jun 2025 | First hybrid-attention reasoning |
| **MiniMax-M2.5** | 230B/10B active | ~200K | Proprietary | Early 2026 | 80.2% SWE-bench |
| **MiniMax-M2.7** | ~230B/10B active | 205K | Proprietary | Mar 2026 | 56.22% SWE-Pro, 50x cheaper than Opus |

### Key Capabilities

- **Reasoning:** M2.7: 85.2% GPQA Diamond, 86.3% AIME 2025
- **Cost:** M2.7: $0.30/M input, $1.20/M output — extremely cheap
- **Context:** M1 supports 1M tokens
- **Architecture:** Hybrid attention (linear + softmax) — very efficient for long context

### African Language Support
- **Not a focus.** MiniMax models are primarily English/Chinese optimized.

### Angavu Score: **55/100**

**Strengths:** Extremely low cost, strong reasoning, efficient architecture  
**Weaknesses:** No on-device variants, no African language support, M2.5/M2.7 are proprietary/closed, M1 license is restrictive

---

## 5. Kimi Family (Moonshot AI)

### Overview
Moonshot AI's Kimi K2 (July 2025) and K2.5 (2026) are **1T-parameter MoE models** that rival GPT-5 on benchmarks. K2 uses Modified MIT license. K2.5 is currently the strongest open-weight model overall.

### Model Lineup

| Model | Params | Context | License | Release | Key Strengths |
|-------|--------|---------|---------|---------|---------------|
| **Kimi K2** | 1T total/32B active (MoE) | 262K | Modified MIT | Jul 2025 | Agentic intelligence |
| **Kimi K2 Thinking** | 1T/32B active | 262K | Modified MIT | Nov 2025 | 99.1% AIME, 44.9% HLE |
| **Kimi K2.5** | 1T/32B active | 262K | Modified MIT | 2026 | #1 open-weight: 87.6% GPQA, 76.8% SWE-bench |

### Key Capabilities

- **Reasoning:** K2.5: 87.6% GPQA Diamond, 96.1% AIME 2025, 99.0% HumanEval — **best-in-class**
- **Agentic:** 200-300 consecutive tool calls without intervention
- **Coding:** 76.8% SWE-bench Verified — frontier-level
- **License:** Modified MIT — broad commercial use with attribution

### African Language Support
- **Not a primary focus.** Primarily English/Chinese, with some multilingual capability.

### Angavu Score: **65/100**

**Strengths:** Best reasoning open-weight model, excellent coding, strong agentic capabilities  
**Weaknesses:** No small variants (32B active minimum), Modified MIT has attribution requirement, no African language focus, too large for on-device

---

## 6. DeepSeek Family

### Overview
DeepSeek's January 2025 R1 release was a watershed moment — training cost just $294K for reasoning capabilities rivaling GPT-4. The family has expanded significantly.

### Model Lineup

| Model | Params | Context | License | Release | Key Strengths |
|-------|--------|---------|---------|---------|---------------|
| **DeepSeek-R1** | 671B total/37B active (MoE) | 128K | MIT | Jan 2025 | Chain-of-thought reasoning |
| **DeepSeek-R1 Distilled** | 1.5B–70B dense | 128K | MIT | Jan 2025 | Smaller reasoning models |
| **DeepSeek V3** | 685B/37B active (MoE) | 128K | MIT | Dec 2025 | IMO gold medal |
| **DeepSeek V3.2** | 685B/37B active | 128K | MIT | Dec 2025 | Improved |
| **DeepSeek V4-Pro** | 1.6T/49B active (MoE) | TBD | TBD | Apr 2026 | Latest frontier |
| **DeepSeek V4-Flash** | 284B/13B active (MoE) | TBD | TBD | Apr 2026 | Efficient |

### Key Capabilities

- **Reasoning:** R1: 71.5% GPQA Diamond, 74.0% AIME. V3: IMO gold medal
- **Cost:** V3.2: $0.28/M tokens — extremely cheap via API
- **License:** MIT — fully permissive
- **Distilled variants:** 1.5B, 7B, 8B, 14B, 32B, 70B — good size range

### African Language Support

| Language | Support Level | Notes |
|----------|-------------|-------|
| Swahili | ⚠️ Limited | Some capability via multilingual training |
| Others | ❌ Not focused | Primarily English/Chinese |

### Angavu Score: **68/100**

**Strengths:** MIT license, cheap API, strong reasoning, distilled variants for on-device  
**Weaknesses:** No small MoE variants under 13B active, African languages not a focus, no on-device optimized variants

---

## 7. Llama Family (Meta)

### Overview
Meta's Llama 4 (April 2025) introduced MoE architecture and natively multimodal capabilities. **Important:** Llama 4 uses a **Community License** with a 700M MAU threshold — NOT Apache 2.0.

### Model Lineup

| Model | Params | Context | License | Release | Key Strengths |
|-------|--------|---------|---------|---------|---------------|
| **Llama 4 Scout** | 109B total/17B active (16-expert MoE) | **10M** | Llama 4 Community | Apr 2025 | Largest context in open-source |
| **Llama 4 Maverick** | 400B total/17B active (128-expert MoE) | 1M | Llama 4 Community | Apr 2025 | Strong multimodal |
| **Llama 4 Behemoth** | 2T total/288B active (MoE) | 128K | Llama 4 Community | Preview | Frontier |

### Key Capabilities

- **Context:** Scout: **10M tokens** — largest in open-source
- **Multimodal:** Natively multimodal (text + image)
- **Reasoning:** Maverick: 69.8% GPQA Diamond, 65.0% SWE-bench
- **License:** ⚠️ **Community License** — commercial use restricted for >700M MAU. NOT Apache 2.0.

### African Language Support

| Language | Support Level | Notes |
|----------|-------------|-------|
| Swahili | ✅ Supported | Part of broad multilingual training |
| Others | ⚠️ Limited | Better than most Chinese models |

### Angavu Score: **62/100**

**Strengths:** Massive context window (10M), good multilingual, strong ecosystem  
**Weaknesses:** **Restrictive license** (700M MAU cap), no small on-device variants, 17B active params too large for $50 phones

---

## 8. Mistral Family (Mistral AI)

### Overview
France's Mistral AI has been a consistent open-source contributor. Mistral 3 (Dec 2025) and Mistral Small 4 (2026) are their latest releases, all under Apache 2.0.

### Model Lineup

| Model | Params | Context | License | Release | Key Strengths |
|-------|--------|---------|---------|---------|---------------|
| **Ministral 3B** | 3B dense | 32K | Apache 2.0 | Dec 2025 | Tiny, efficient |
| **Ministral 8B** | 8B dense | 32K | Apache 2.0 | Dec 2025 | Good balance |
| **Mistral 3 14B** | 14B dense | 128K | Apache 2.0 | Dec 2025 | Strong dense model |
| **Mistral Large 3** | 675B total/41B active (MoE) | 128K | Apache 2.0 | Dec 2025 | Frontier MoE |
| **Mistral Small 4** | 119B total/6.5B active (MoE) | 256K | Apache 2.0 | 2026 | Efficient MoE |

### Key Capabilities

- **License:** All Apache 2.0 — fully permissive ✅
- **Multilingual:** Best-in-class non-English/non-Chinese multilingual performance
- **Edge:** Ministral 3B and 8B for on-device deployment
- **Efficiency:** Mistral Small 4: 6.5B active params from 119B total — very efficient

### African Language Support
- Mistral explicitly targets **multilingual conversations** (non-English/Chinese focus)
- Better European language coverage; African languages still limited

### Angavu Score: **70/100**

**Strengths:** Apache 2.0, good multilingual, efficient MoE, edge-friendly small models  
**Weaknesses:** African languages not a primary focus, smaller ecosystem than Qwen/Llama

---

## 9. Other Notable Models

### Phi-4 Family (Microsoft)

| Model | Params | Context | License | Key Strengths |
|-------|--------|---------|---------|---------------|
| **Phi-4-mini** | 3.8B dense | 16K | MIT | Text tasks, on-device |
| **Phi-4-multimodal** | 5.6B dense | 16K | MIT | Speech + vision + text |
| **Phi-4-reasoning-plus** | 14B dense | 16K | MIT | 93.1% GSM8K, reasoning |

- **Angavu relevance:** Good for on-device (3.8B/5.6B fit phones), MIT license, but limited African language support
- **Score: 60/100**

### Falcon Family (TII, UAE)

| Model | Params | Context | License | Key Strengths |
|-------|--------|---------|---------|---------------|
| **Falcon 3** | 180B | 32K | Open | Arabic/African focus |
| **Falcon-Arabic** | Based on Falcon 3 | 32K | Open | Arabic + multilingual |
| **Falcon-H1** | Various | 32K | Open | Hybrid architecture |

- **Angavu relevance:** Best **Arabic** language support; some African language coverage via Arabic overlap
- **License:** Open-weight but check specific terms
- **Score: 50/100** (good for Arabic markets, limited for Sub-Saharan African languages)

### GLM-5 Family (Zhipu AI)

| Model | Params | Context | License | Key Strengths |
|-------|--------|---------|---------|---------------|
| **GLM-5** | 744B/40B active (MoE) | 200K | MIT | 91.2% GPQA Diamond |
| **GLM-5.2** | 744B/40B active | 200K | MIT | #1 open-weight reasoning |
| **GLM-4.7** | 355B/32B active | 200K | MIT | 95.7% AIME |

- **Angavu relevance:** MIT license, strongest reasoning benchmarks, but no on-device variants and no African language focus
- **Score: 55/100**

### GPT-oss-120B (OpenAI)

| Model | Params | Context | License | Key Strengths |
|-------|--------|---------|---------|---------------|
| **gpt-oss-120b** | 117B/5.1B active (MoE) | 128K | Apache 2.0 | OpenAI's first open model |

- **Angavu relevance:** Apache 2.0, fits single H100, but 5.1B active still too large for $50 phones
- **Score: 50/100**

### Nemotron (NVIDIA)

| Model | Params | Context | License | Key Strengths |
|-------|--------|---------|---------|---------------|
| **Nemotron Ultra 253B** | 253B dense | 128K | NVIDIA Open | 76.0% GPQA |
| **Nemotron 3 Super 120B** | 120B/12B active (MoE) | 128K | NVIDIA Open | 60.47% SWE-bench |

- **Angavu relevance:** Good enterprise focus, but NVIDIA-specific optimization
- **Score: 45/100**

### Step 3.5 Flash (StepFun)

| Model | Params | Context | License | Key Strengths |
|-------|--------|---------|---------|---------------|
| **Step-3.5-Flash** | 196B/11B active (MoE) | 262K | Proprietary | #3 on OpenRouter by volume |

- **Angavu relevance:** Free tier on OpenRouter, but proprietary license
- **Score: 40/100**

---

## Comprehensive Comparison Table

| Model | Total Params | Active Params | Context | License | African Lang | Reasoning (GPQA) | On-Device | ARM Perf | Fine-Tune | Cost | Score |
|-------|-------------|---------------|---------|---------|-------------|-----------------|-----------|----------|-----------|------|-------|
| **Qwen3.5-2B** | 2B | 2B | 256K | Apache 2.0 | ⚠️ 201 langs | Good | ✅ 2GB | ✅ | ✅ LoRA | Free | **82** |
| **Qwen3.5-9B** | 9B | 9B | 256K | Apache 2.0 | ⚠️ 201 langs | Good | ❌ | ✅ | ✅ LoRA | Free | **80** |
| **Qwen3-14B** | 14B | 14B | 128K | Apache 2.0 | ⚠️ 119 langs | Good | ❌ | ✅ | ✅ LoRA | Free | **85** |
| **Qwen3-235B-A22B** | 235B | 22B | 128K | Apache 2.0 | ⚠️ 119 langs | Excellent | ❌ | ⚠️ | ✅ | Free | **88** |
| **Gemma 4 E2B** | 2B eff | 2B | 128K | Apache 2.0 | ⚠️ 140+ | Good | ✅ 5GB | ✅ | ✅ | Free | **84** |
| **Gemma 4 E4B** | 4B eff | 4B | 128K | Apache 2.0 | ⚠️ 140+ | Better | ❌ 5GB | ✅ | ✅ | Free | **82** |
| **Gemma 4 31B** | 31B | 31B | 256K | Apache 2.0 | ⚠️ 140+ | Excellent | ❌ | ✅ | ✅ | Free | **87** |
| **Gemma 4 26B-A4B** | 26B | 4B | 256K | Apache 2.0 | ⚠️ 140+ | Good | ❌ | ✅ | ✅ | Free | **80** |
| **MiMo-V2-Flash** | 309B | 15B | 256K | MIT | ❌ | Excellent | ❌ | ✅ | ✅ | Free | **72** |
| **MiMo-V2-Pro** | 1T+ | 42B | 1M | Bespoke | ❌ | Excellent | ❌ | ⚠️ | ⚠️ | $1/$3/M | **68** |
| **Kimi K2.5** | 1T | 32B | 262K | Mod. MIT | ❌ | Best-in-class | ❌ | ⚠️ | ✅ | Free | **65** |
| **DeepSeek R1** | 671B | 37B | 128K | MIT | ⚠️ | Excellent | ❌ | ⚠️ | ✅ | Free | **68** |
| **DeepSeek V3.2** | 685B | 37B | 128K | MIT | ⚠️ | Good | ❌ | ⚠️ | ✅ | $0.28/M | **66** |
| **DeepSeek R1 14B** | 14B | 14B | 128K | MIT | ⚠️ | Good | ❌ | ✅ | ✅ | Free | **70** |
| **Llama 4 Scout** | 109B | 17B | 10M | Community | ⚠️ | Good | ❌ | ✅ | ✅ | Free | **62** |
| **Mistral Small 4** | 119B | 6.5B | 256K | Apache 2.0 | ⚠️ | Good | ❌ | ✅ | ✅ | Free | **70** |
| **Mistral 3 14B** | 14B | 14B | 128K | Apache 2.0 | ⚠️ | Good | ❌ | ✅ | ✅ | Free | **72** |
| **Phi-4-mini** | 3.8B | 3.8B | 16K | MIT | ❌ | Good | ✅ | ✅ | ✅ | Free | **60** |
| **Phi-4-multimodal** | 5.6B | 5.6B | 16K | MIT | ❌ | Good | ⚠️ | ✅ | ✅ | Free | **58** |
| **GLM-5.2** | 744B | 40B | 200K | MIT | ❌ | Best | ❌ | ⚠️ | ✅ | Free | **55** |
| **MiniMax-M2.7** | ~230B | 10B | 205K | Proprietary | ❌ | Excellent | ❌ | ✅ | ❌ | $0.30/$1.20 | **55** |
| **Falcon 3** | 180B | - | 32K | Open | ⚠️ Arabic | Moderate | ❌ | ✅ | ✅ | Free | **50** |
| **Nemotron Ultra** | 253B | 253B | 128K | NVIDIA Open | ❌ | Good | ❌ | ✅ | ✅ | Free | **45** |

---

## African Language Deep Dive

### The Critical Gap

**No major open-source model has strong native support for African languages beyond Swahili.** This is Angavu's biggest challenge and biggest opportunity.

### Language Support Matrix

| Language | Speakers | Qwen3 | Gemma 3/4 | Llama 4 | DeepSeek | Mistral 3 | Falcon |
|----------|----------|-------|-----------|---------|----------|-----------|--------|
| **Swahili** | 100M+ | ✅ Explicit | ✅ Supported | ✅ Supported | ⚠️ Partial | ⚠️ Partial | ⚠️ Via Arabic |
| **Yoruba** | 45M+ | ⚠️ Partial | ⚠️ Limited | ⚠️ Limited | ❌ | ❌ | ❌ |
| **Hausa** | 80M+ | ⚠️ Partial | ⚠️ Limited | ⚠️ Limited | ❌ | ❌ | ⚠️ Via Arabic |
| **Amharic** | 57M+ | ❌ Not listed | ⚠️ Limited | ❌ | ❌ | ❌ | ❌ |
| **Zulu** | 27M+ | ❌ Not listed | ⚠️ Limited | ⚠️ Limited | ❌ | ❌ | ❌ |
| **Igbo** | 45M+ | ❌ Not listed | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Oromo** | 36M+ | ❌ Not listed | ❌ | ❌ | ❌ | ❌ | ❌ |

### Recommended African Language Strategy

1. **Base model with best multilingual foundation:** Qwen3.5 (201 languages) or Gemma 4 (140+ languages)
2. **Fine-tune on African language corpora:** Use datasets from Masakhane, AfroXLMR, etc.
3. **Swahili is the easiest win:** Already supported in Qwen3; needs enhancement, not bootstrapping
4. **Yoruba/Hausa need dedicated fine-tuning:** ~10-50K high-quality parallel examples needed
5. **Amharic/Zulu are hardest:** Script challenges (Amharic Ge'ez) and limited digital corpora

---

## Final Recommendations for Angavu Intelligence

### 1. On-Device Model (for $50 phones, ≤2GB RAM)

**Primary: Qwen3.5-0.8B** (Apache 2.0, 256K context, 201 languages)  
**Fallback: Gemma 4 E2B** (Apache 2.0, 128K context, multimodal, 5GB at 4-bit — may need INT4 quantization for 2GB)

**Why Qwen3.5-0.8B:**
- 0.8B parameters = ~500MB at INT4 quantization — fits in 2GB RAM with room for OS
- 256K context window (longest for its size class)
- 201 languages including Swahili
- Apache 2.0 license
- Excellent fine-tuning support (Unsloth, LoRA)
- Designed for on-device deployment from ground up

**Why Gemma 4 E2B as fallback:**
- Natively multimodal (voice + vision) — future-proof for Angavu's voice-first strategy
- Apache 2.0 license
- 128K context
- Google's edge inference optimizations (MediaPipe, LiteRT)

### 2. Cloud Model (for ARM servers, 14B-32B range)

**Primary: Qwen3-14B** (Apache 2.0, 128K context, 119 languages)  
**Secondary: Gemma 4 31B** (Apache 2.0, 256K context, frontier reasoning)  
**Tertiary: Mistral 3 14B** (Apache 2.0, 128K context, strong multilingual)

**Why Qwen3-14B as primary:**
- 14B dense = fits on ARM servers with 4-8GB RAM (INT4 quantized)
- Apache 2.0 license — zero legal risk
- 119 languages with Swahili support
- Strong reasoning with thinking/non-thinking modes
- Best fine-tuning ecosystem in the market
- Runs efficiently on ARM via llama.cpp, MLC-LLM

**Why Gemma 4 31B as secondary:**
- Frontier reasoning (84.3% GPQA Diamond)
- 256K context
- Natively multimodal
- Apache 2.0
- Requires more RAM (~16GB at INT4) but fits ARM servers

**Why Mistral 3 14B as tertiary:**
- Best non-English/non-Chinese multilingual performance
- Apache 2.0
- Good European language coverage (French, Portuguese — relevant for West Africa)
- 14B = same footprint as Qwen3-14B

### 3. Fine-Tuning Strategy

**Phase 1: Swahili Enhancement (Months 1-3)**
- Base: Qwen3.5-0.8B (on-device) + Qwen3-14B (cloud)
- Data: 50K Swahili informal economy examples (chama records, market prices, M-Pesa transactions)
- Method: LoRA/QLoRA via Unsloth
- Expected improvement: 40-60% → 80%+ on Swahili informal economy tasks

**Phase 2: Yoruba + Hausa (Months 3-6)**
- Base: Same models
- Data: 20K parallel examples per language (English ↔ Yoruba/Hausa)
- Sources: Masakhane, NLLB, Opus parallel corpora, local data collection
- Method: Continued LoRA training with language-specific adapters

**Phase 3: Amharic + Zulu (Months 6-12)**
- Base: Same models
- Challenge: Amharic Ge'ez script, limited digital corpora
- Strategy: Partner with Ethiopian/South African universities for data collection
- Use multilingual adapter approach (language-specific LoRA adapters)

**Phase 4: Economic/Statistical Fine-tuning (Months 3-9)**
- Base: Qwen3-14B (cloud) with thinking mode
- Data: Financial reports, inflation data, exchange rates, informal economy patterns
- Focus: Time series reasoning, forecasting, anomaly detection
- Method: Full fine-tune on economic reasoning data + LoRA for specific markets

### 4. Fallback Chain

```
On-Device:
  Primary:   Qwen3.5-0.8B (Apache 2.0, 201 langs)
  Secondary: Gemma 4 E2B (Apache 2.0, multimodal)
  Tertiary:  Phi-4-mini 3.8B (MIT, good reasoning)

Cloud:
  Primary:   Qwen3-14B (Apache 2.0, 119 langs, excellent fine-tuning)
  Secondary: Gemma 4 31B (Apache 2.0, frontier reasoning)
  Tertiary:  Mistral 3 14B (Apache 2.0, best multilingual)
  Overflow:  DeepSeek R1 14B (MIT, strong reasoning)

API Fallback (when self-hosted is insufficient):
  Primary:   DeepSeek V3.2 ($0.28/M — cheapest)
  Secondary: MiMo-V2-Pro ($1/$3/M — most popular)
  Tertiary:  Kimi K2.5 (free API tier available)
```

### 5. Licensing Strategy

**Rule: Apache 2.0 or MIT ONLY for production deployment.**

| License | Risk Level | Angavu Use |
|---------|-----------|------------|
| Apache 2.0 | ✅ Zero | Full commercial use, no restrictions |
| MIT | ✅ Zero | Full commercial use, attribution only |
| Modified MIT (Kimi) | ⚠️ Low | Check attribution requirements |
| Llama Community | ⚠️ Medium | 700M MAU cap — plan for scale |
| Gemma TOU (v3) | ⚠️ Medium | Restrictive — avoid for production |
| Bespoke (MiMo Pro) | ❌ High | Read every clause before use |

---

## Model Family Strengths Summary

| Use Case | Best Model | Why |
|----------|-----------|-----|
| **On-device ($50 phone)** | Qwen3.5-0.8B | 0.8B params, 256K context, 201 langs, Apache 2.0 |
| **Cloud (ARM server)** | Qwen3-14B | 14B dense, Apache 2.0, great fine-tuning, 119 langs |
| **Frontier reasoning** | Gemma 4 31B | 84.3% GPQA, Apache 2.0, multimodal |
| **Best reasoning overall** | Kimi K2.5 / GLM-5.2 | 87.6% GPQA / 91.2% GPQA, but no small variants |
| **Cheapest API** | DeepSeek V3.2 | $0.28/M tokens |
| **Most adopted** | MiMo-V2-Pro | #1 on OpenRouter, 4.79T tokens/week |
| **African languages** | Qwen3.5 | 201 languages, Swahili explicit |
| **Multimodal** | Gemma 4 | Natively multimodal all sizes |
| **Arabic markets** | Falcon 3 | Best Arabic language support |

---

## Key Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| African language quality is poor | High | Budget for dedicated fine-tuning; partner with Masakhane |
| License changes (Google, Meta) | High | Stick to Apache 2.0 / MIT only |
| ARM inference speed insufficient | Medium | Use MoE models (Qwen3-30B-A3B); optimize with MLC-LLM |
| Model updates break fine-tuning | Medium | Pin model versions; maintain adapter library |
| On-device models too weak | Medium | Plan for hybrid: on-device for simple tasks, cloud for complex |

---

## Sources

- Qwen3 blog: https://qwenlm.github.io/blog/qwen3/
- Gemma 4 blog: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- Open-Source AI Landscape April 2026: https://www.digitalapplied.com/blog/open-source-ai-landscape-april-2026-gemma-qwen-llama
- Open-Weight vs Closed-Source 2026: https://www.digitalapplied.com/blog/open-weight-vs-closed-source-ai-models-q2-2026
- Thunder Compute Best Open Source LLMs July 2026: https://www.thundercompute.com/blog/best-open-source-llms
- Onyx Best Open Source LLMs 2026: https://onyx.app/insights/best-open-source-llms-2026
- Featherless Best Open-Source LLMs 2026: https://featherless.ai/blog/best-open-source-llms-2026
- Small Language Models Guide: https://www.digitalapplied.com/blog/small-language-models-business-guide-gemma-phi-qwen
- Mistral 3 announcement: https://mistral.ai/news/mistral-3/
- MiniMax-M1 GitHub: https://github.com/MiniMax-AI/MiniMax-M1
- MiMo-V2-Flash GitHub: https://github.com/xiaomimimo/MiMo-V2-Flash
- Kimi K2 arXiv: https://arxiv.org/abs/2507.20534
- Falcon-Arabic: https://huggingface.co/blog/tiiuae/falcon-arabic
- DeepSeek R1 Africa implications: https://carnegieendowment.org/posts/2025/03/deepseek-ai-implications-africa

---

*Research completed July 7, 2026. The open-source AI landscape evolves rapidly — this document should be updated quarterly.*
