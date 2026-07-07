# SWARM E: Training Infrastructure & Data Center Architecture

**Angavu Intelligence — Technical Infrastructure Report**
**Swarm E2: Training Infrastructure & Data Center Architecture Team**
**Date: 2026-07-07**

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Oracle Cloud Architecture (Phase 1)](#2-oracle-cloud-architecture-phase-1)
3. [ARM Server Infrastructure (Phase 2-4)](#3-arm-server-infrastructure-phase-2-4)
4. [Solar-Powered Data Center Design](#4-solar-powered-data-center-design)
5. [Training Tools & Frameworks](#5-training-tools--frameworks)
6. [Training Pipeline Architecture (All 4 Phases)](#6-training-pipeline-architecture-all-4-phases)
7. [Cost Analysis](#7-cost-analysis)
8. [Migration Path: Cloud → Own DC](#8-migration-path-cloud--own-dc)
9. [Academic Framework](#9-academic-framework)
10. [Africa's Data Center for Africa's Workers](#10-africas-data-center-for-africas-workers)

---

## 1. Executive Summary

Angavu Intelligence's infrastructure strategy is built around a phased transition from cloud-first (Oracle Cloud) to fully self-hosted, solar-powered ARM data centers across Africa. This is not a Silicon Valley playbook — it's an infrastructure plan designed for Africa's energy economics, labor costs, and the specific needs of informal economy workers.

### Key Findings

- **Oracle Cloud Free Tier** provides 2 ARM OCPUs + 12GB RAM + 200GB storage at zero cost — enough for Phase 1 development and early inference
- **ARM servers** (Ampere Altra, 128 cores at 190W TDP) deliver 3-5x better performance/watt than x86, making solar-powered DCs viable
- **Kenya's geothermal energy** at $0.05/kWh is cheaper than China's coal power, creating a structural cost advantage
- **Unsloth + QLoRA** enables fine-tuning 14B+ parameter models on consumer GPUs with 70% less VRAM — critical for cost-constrained training
- **Break-even point**: Own DC becomes cheaper than cloud at ~10,000 active users (Phase 2)
- **The containerized DC model** (20ft/40ft shipping containers) enables rapid deployment across African cities

### The Economic Reality

| Metric | Silicon Valley | Kenya (Angavu) |
|---|---|---|
| Electricity cost | $0.10-0.15/kWh | $0.05/kWh (geothermal) |
| Server cooling | Mechanical HVAC | Free-air + solar climate |
| Labor (ops) | $80-150/hr | $5-15/hr |
| Data sovereignty | US/EU regulations | Kenyan law, African-owned |
| Latency to users | 200-500ms (from Africa) | 5-20ms (on-continent) |

---

## 2. Oracle Cloud Architecture (Phase 1)

### 2.1 Always Free Tier — What We Get for $0

**Always Free Resources (permanent, no expiration):**

| Resource | Specification | Use Case |
|---|---|---|
| **Ampere A1 Compute** | 2 OCPUs + 12GB RAM (ARM) | API server, lightweight inference |
| **AMD Micro Instances** | 2x VM.Standard.E2.1.Micro | Monitoring, CI/CD runners |
| **Block Storage** | 200GB total | Boot volumes, model storage |
| **Object Storage** | 20GB | Dataset storage, model artifacts |
| **Load Balancer** | 1 instance, 10 Mbps | API gateway |
| **Database** | 2x Autonomous DB (20GB each) | Metadata, user data |
| **Monitoring** | 500M ingestion datapoints | Observability |
| **Bandwidth** | 10TB/month outbound | API traffic |

**Critical detail:** Oracle reclaims idle Always Free instances if CPU/network/memory utilization stays below 20% for 7 days. Solution: Run a lightweight cron job that generates synthetic load every 3 days.

### 2.2 Paid GPU Instances — Training Power

For actual model training (Phase 1 requires GPU access), Oracle Cloud offers:

| Instance | GPU | VRAM | $/hour | Best For |
|---|---|---|---|---|
| BM.GPU.A10.1 | 1x NVIDIA A10 | 24GB | ~$1.50 | Fine-tuning 7B models |
| BM.GPU.A10.4 | 4x NVIDIA A10 | 96GB | ~$6.00 | Fine-tuning 13B models |
| BM.GPU.H100.8 | 8x NVIDIA H100 | 640GB | ~$21.00 | Full training runs |
| BM.GPU.H200.8 | 8x NVIDIA H200 | 1.1TB | ~$25.00 | Largest model training |

**Phase 1 Training Strategy:**
- Use **A10 instances** for QLoRA fine-tuning (cheapest, sufficient for LoRA adapters)
- Use **spot/preemptible instances** for batch training jobs (60-70% cheaper)
- Schedule training during off-peak hours (UTC 02:00-08:00) when spot prices drop
- Store all training data in OCI Object Storage (cheapest tier) and mount via FUSE

**OCI Data Science Platform:**
- Managed Jupyter notebooks with pre-built ML images
- Model catalog and experiment tracking
- Integration with OCI Functions for serverless inference
- **Key advantage:** No GPU instance management overhead for small experiments

### 2.3 Phase 1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    ORACLE CLOUD (Phase 1)                │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  A1 Always   │  │  A1 Always   │  │  GPU Spot    │  │
│  │  Free (ARM)  │  │  Free (ARM)  │  │  Instance    │  │
│  │  API Server  │  │  Inference   │  │  Training    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                  │          │
│  ┌──────┴─────────────────┴──────────────────┴───────┐  │
│  │              OCI Load Balancer                     │  │
│  └──────────────────────┬────────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────┴────────────────────────────┐  │
│  │         OCI Object Storage (Models + Data)         │  │
│  └──────────────────────┬────────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────┴────────────────────────────┐  │
│  │     OCI Autonomous DB (Metadata, User Data)        │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  OCI Functions (Serverless API endpoints)          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.4 Phase 1 Cost Estimate (1,000 Users)

| Component | Monthly Cost |
|---|---|
| Always Free compute (2x ARM) | $0 |
| GPU spot training (40 hrs/month) | ~$60-90 |
| Object Storage (100GB) | ~$2.50 |
| Autonomous DB | $0 (Always Free) |
| Bandwidth (1TB egress) | ~$8.50 |
| Load Balancer | $0 (Always Free) |
| **Total Phase 1** | **~$70-100/month** |

---

## 3. ARM Server Infrastructure (Phase 2-4)

### 3.1 Why ARM is THE Architecture for Africa

ARM-based servers are not a compromise — they're the optimal architecture for solar-powered, cost-constrained data centers:

| Metric | x86 (Intel Xeon) | ARM (Ampere Altra) | Advantage |
|---|---|---|---|
| Cores per socket | 32-64 | 80-128 | 2-4x more parallelism |
| TDP per socket | 250-350W | 190-250W | 30-40% less power |
| Performance/watt | Baseline | 3-5x better | Critical for solar |
| Price per server | $8,000-15,000 | $4,000-8,000 | 50% lower CAPEX |
| Memory channels | 8 | 6-8 | Comparable |
| PCIe lanes | 64-128 | 64-128 | Comparable |

### 3.2 Recommended Server Hardware

**Phase 2 (10,000 workers) — Single ARM Server + Solar:**

| Component | Specification | Est. Cost |
|---|---|---|
| **Server** | Ampere Altra Q80-30 (80 cores, 3.0GHz, 190W TDP) | $5,000-7,000 |
| **RAM** | 256GB DDR4 ECC | $800-1,200 |
| **Storage** | 2x 2TB NVMe SSD | $400-600 |
| **Network** | 2x 25GbE | $200-400 |
| **Chassis** | 1U rackmount | $300-500 |
| **Total server** | | **$6,700-9,700** |

**Alternative: NVIDIA Grace (ARM + GPU Integration)**

The NVIDIA Grace CPU (ARM-based) paired with NVIDIA GPUs offers:
- Grace Hopper Superchip: Grace CPU + H100 GPU, NVLink-C2C interconnect
- Grace CPU standalone: 72 ARM cores, 500GB LPDDR5X, 500GB/s bandwidth
- **Best for:** Training workloads that need both CPU parallelism and GPU acceleration
- **Cost:** $25,000-40,000 per system (Grace Hopper)
- **TDP:** 700W (CPU+GPU combined)

**Phase 3 (100,000 workers) — Mini DC Cluster:**

| Component | Quantity | Specification | Est. Cost |
|---|---|---|---|
| Compute nodes | 3-5 | Ampere Altra Q80-30, 256GB RAM | $20,000-35,000 |
| GPU node | 1 | 4x NVIDIA A10 or 2x L40S | $12,000-20,000 |
| Storage node | 1 | 20TB NVMe + 100TB HDD RAID | $5,000-8,000 |
| Network switch | 1 | 48-port 25GbE | $2,000-4,000 |
| UPS (2hr backup) | 1 | 10kVA online UPS | $3,000-5,000 |
| Rack + accessories | 1 | 42U rack, PDUs, cables | $1,500-3,000 |
| **Total Phase 3 hardware** | | | **$43,500-75,000** |

**Phase 4 (1,000,000 workers) — Containerized Pan-African DC Network:**

| Component | Specification | Est. Cost |
|---|---|---|
| 20ft container DC | 20-40 ARM servers, cooling, networking | $150,000-300,000 |
| Solar array (per container) | 50kW array + battery bank | $50,000-80,000 |
| Network backbone | Fiber interconnect between sites | $10,000-50,000/site |
| **Per-site cost** | | **$210,000-430,000** |
| **Pan-African (5-10 sites)** | | **$1M-4.3M** |

### 3.3 ARM Server Vendors for Africa

| Vendor | Product | Why |
|---|---|---|
| **Ampere Computing** | Altra, AmpereOne | Best perf/watt, cloud-native, 128 cores |
| **Broadberry** | CyberServe Ampere range | Affordable ARM rack servers |
| **ADLINK** | COM-HPC Ampere Altra modules | Modular, edge-friendly |
| **Gigabyte** | G242-P32 (Ampere Altra) | Major server OEM, Africa distribution |
| **Supermicro** | ARS-110M-NR | Ampere Altra in 1U form factor |
| **AWS Graviton** | (Reference only) | Shows ARM is production-proven at scale |

### 3.4 ARM + Inference Engine Stack

Based on 2026 landscape:

| Engine | Best For | ARM Support | Notes |
|---|---|---|---|
| **vLLM** | Multi-user serving (5-20 concurrent) | ✅ Native ARM64 | Best for Phase 2-3 serving |
| **Ollama** | Single-user, simple setup | ✅ Native ARM64 | Good for development/edge |
| **llama.cpp** | CPU-only inference | ✅ Optimized ARM NEON | Best for pure-CPU ARM inference |
| **SGLang** | Prefix-heavy, high throughput | ✅ ARM64 | Best for batched API serving |
| **Triton** | Multi-model, production scale | ✅ ARM64 | Phase 4 multi-model serving |
| **TensorRT-LLM** | NVIDIA GPU optimization | ⚠️ GPU only | Only for GPU nodes |

**Critical note (March 2026):** HuggingFace's TGI (Text Generation Inference) moved to maintenance mode, directing users to vLLM, SGLang, llama.cpp, and MLX. **Do not build on TGI.**

**Recommended inference stack:**
- **Phase 1-2:** Ollama for development, vLLM for production serving
- **Phase 3:** vLLM + SGLang for different workload profiles
- **Phase 4:** Triton Inference Server managing vLLM/SGLang backends across nodes

---

## 4. Solar-Powered Data Center Design

### 4.1 Kenya's Energy Advantage

Kenya sits on the East African Rift — one of the world's richest geothermal zones:

| Energy Source | Kenya | Silicon Valley | China |
|---|---|---|---|
| **Solar irradiance** | 5-6 kWh/m²/day | 4.5-5.5 kWh/m²/day | 3-4.5 kWh/m²/day |
| **Geothermal cost** | $0.05/kWh | N/A | N/A |
| **Grid electricity** | $0.12-0.18/kWh | $0.10-0.15/kWh | $0.08-0.10/kWh |
| **Solar LCOE** | $0.03-0.05/kWh | $0.04-0.06/kWh | $0.03-0.05/kWh |
| **Grid reliability** | 85-90% | 99.9% | 99.5% |

**Key insight:** Solar + battery in Kenya can deliver $0.03-0.05/kWh — cheaper than ANY grid power globally. Combined with geothermal backup, this creates the cheapest power for data centers in the world.

### 4.2 Solar Array Sizing

**Phase 2 (Single ARM Server):**
- Server power: ~300W (server + switch + storage)
- Solar panels needed: 1.5kW array (6x 250W panels)
- Battery: 5kWh lithium (10-16 hours backup)
- **Cost:** $1,500-2,500 (panels + battery + inverter + charge controller)

**Phase 3 (Mini DC — 3-5 servers + GPU):**
- Total power: ~5-8kW (servers + cooling + networking)
- Solar panels: 25-40kW array (100-160 panels)
- Battery bank: 100-200kWh lithium
- Geothermal grid backup connection
- **Cost:** $25,000-50,000 (full solar + battery system)

**Phase 4 (Containerized DC):**
- Per container: 30-60kW
- Solar array: 100-200kW per container site
- Battery bank: 500kWh-1MWh
- Geothermal/industrial grid backup
- **Cost per site:** $100,000-250,000

### 4.3 Cooling Strategy

Africa's climate requires efficient cooling, but traditional HVAC is expensive:

| Method | PUE | Cost | Best For |
|---|---|---|---|
| **Free-air cooling** | 1.1-1.2 | Low | Most of the year in Nairobi (avg 18-25°C) |
| **Evaporative cooling** | 1.2-1.3 | Low-Medium | Hot dry seasons |
| **Hot/cold aisle containment** | 1.3-1.5 | Medium | Standard server rooms |
| **Immersion cooling** | 1.03-1.1 | High CAPEX, Low OPEX | High-density GPU racks |

**Recommended:** Free-air cooling with hot/cold aisle containment for Phases 2-3. Kenya's highland climate (Nairobi: 1,795m elevation, avg 18-25°C) makes mechanical cooling unnecessary most of the year.

### 4.4 Containerized DC Design (Phase 4)

Containerized/modular data centers are the standard for rapid deployment:

**20ft Container DC Specification:**
- **Servers:** 20-40 Ampere Altra nodes (1U each)
- **Cooling:** Integrated free-air + evaporative
- **Power:** 30-60kW IT load, 100kW solar array
- **Network:** Integrated 100GbE spine-leaf
- **Monitoring:** Environmental sensors, remote management
- **Deployment time:** 8-12 weeks from order to operation
- **Vendors:** Schneider Electric, Vertiv, Huawei, ABB

**Market context:** The containerized DC market in Middle East & Africa was $1.53B in 2025, growing rapidly. This is proven, commercially available technology — not a research project.

---

## 5. Training Tools & Frameworks

### 5.1 Voice Training Pipeline

Angavu needs voice capabilities for informal economy workers who may be semi-literate:

| Tool | Purpose | Latest (2026) | ARM/GPU Req |
|---|---|---|---|
| **Whisper** | Speech-to-text (ASR) | v3/v4, 150+ languages | GPU (A10 for fine-tuning) |
| **Piper TTS** | Text-to-speech | Lightweight, fast, many voices | CPU (ARM64 native) |
| **VITS** | End-to-end TTS | High quality, multilingual | GPU for training, CPU for inference |
| **Coqui TTS** | Open-source TTS | XTTS v2, voice cloning | GPU for training |
| **MMS (Meta)** | Massively multilingual speech | 1,100+ languages | GPU for fine-tuning |

**African language strategy:**
1. Start with **Whisper fine-tuning** on Swahili, Sheng, Kikuyu, Luo datasets
2. Use **Piper TTS** for lightweight TTS on ARM servers (runs on CPU)
3. Train **VITS/Coqui** models for higher-quality TTS using GPU instances
4. **MMS** as baseline for low-resource African languages

**Training data sources:**
- Common Voice (Mozilla) — African language contributions
- BABEL dataset — African speech
- Local recordings from Angavu workers (with consent)
- Synthetic data augmentation using TTS → ASN pipeline

### 5.2 LLM Fine-Tuning Stack

| Tool | Purpose | GPU Requirement | Key Feature |
|---|---|---|---|
| **Unsloth** | QLoRA/LoRA fine-tuning | 16-24GB VRAM | 2x faster, 70% less VRAM |
| **Axolotl** | Full fine-tuning pipeline | 24-80GB VRAM | Multi-GPU, DeepSpeed |
| **Hugging Face TRL** | RLHF, DPO, PPO | 24-80GB VRAM | Reinforcement learning |
| **LLaMA-Factory** | All-in-one fine-tuning | 16-80GB VRAM | GUI + CLI |
| **MLflow** | Experiment tracking | None (metadata only) | Track all training runs |
| **Weights & Biases** | Experiment tracking | None | Cloud-based dashboards |

**Qwen3 Fine-Tuning (Recommended Base Model):**

Qwen3 (released 2025, updated July 2025) is the recommended base for Angavu:
- **Multilingual:** Strong in African-relevant languages
- **Sizes:** 0.6B, 1.7B, 4B, 8B, 14B, 30B, 32B MoE, 235B MoE
- **Context:** Native 40K, extendable to 128K via YaRN
- **Fine-tuning:** Full Unsloth support with Dynamic 2.0 quantization
- **RL support:** Reinforcement learning fine-tuning supported

**Recommended Qwen3 model per phase:**
- Phase 1: Qwen3-1.7B (QLoRA on A10, 24GB VRAM)
- Phase 2: Qwen3-8B (QLoRA on A10/A100)
- Phase 3: Qwen3-14B (QLoRA + full fine-tune on 4x A10)
- Phase 4: Qwen3-30B+ (distributed training across nodes)

### 5.3 Federated Learning

For Phase 4 (pan-African network with data sovereignty):

| Framework | Purpose | Maturity | Key Feature |
|---|---|---|---|
| **Flower** | Federated learning framework | Production-ready | Framework-agnostic, easy to use |
| **PySyft** | Privacy-preserving ML | Production-ready | Differential privacy, secure computation |
| **FedML** | Federated AI platform | Production-ready | Cross-device, cross-silo |
| **TensorFlow Federated** | Google's FL framework | Production-ready | TFF runtime |

**Recommended:** Flower + PySyft
- **Flower** for the federated training orchestration (simple API, Python-native)
- **PySyft** for differential privacy guarantees (critical for financial data)

**Federated training strategy for Phase 4:**
1. Each regional DC trains on local data
2. Only model gradients (not data) shared between sites
3. Central aggregation server in Nairobi
4. Differential privacy noise added to gradients before transmission
5. Models converge across pan-African network

### 5.4 ML Pipeline & Data Processing

| Tool | Purpose | Why |
|---|---|---|
| **PyTorch** | Deep learning framework | Industry standard, best ecosystem |
| **Hugging Face Transformers** | Model hub + training | 500K+ models, great API |
| **Hugging Face Datasets** | Dataset management | Efficient streaming, caching |
| **Polars** | Data processing | 10-100x faster than Pandas, Rust-based |
| **Ray** | Distributed compute | Scale training across nodes |
| **Dask** | Parallel processing | Python-native distributed computing |
| **Apache Arrow** | Columnar data format | Zero-copy, memory efficient |
| **MinIO** | Object storage | S3-compatible, self-hosted |

**Recommended data pipeline:**
```
Raw data (Parquet/Arrow) → Polars (cleaning/transform) → HF Datasets (tokenization)
→ PyTorch DataLoader → Unsloth/Axolotl (training) → MLflow (tracking)
→ vLLM/Ollama (serving)
```

---

## 6. Training Pipeline Architecture (All 4 Phases)

### 6.1 Phase 1: Cloud-First (Oracle Cloud)

**Architecture:** All compute on Oracle Cloud, zero infrastructure investment.

```
┌─────────────────────────────────────────────────────┐
│                 PHASE 1 ARCHITECTURE                 │
│                                                     │
│  ┌─────────────┐    ┌─────────────┐                │
│  │ A1 Always   │    │ A1 Always   │                │
│  │ Free (ARM)  │    │ Free (ARM)  │                │
│  │ API Server  │    │ Lightweight │                │
│  │ (FastAPI)   │    │ Inference   │                │
│  └──────┬──────┘    └──────┬──────┘                │
│         │                   │                       │
│  ┌──────┴───────────────────┴─────────────────────┐ │
│  │            OCI Load Balancer                    │ │
│  └────────────────────┬───────────────────────────┘ │
│                       │                             │
│  ┌────────────────────┴───────────────────────────┐ │
│  │       OCI Object Storage (Models + Data)        │ │
│  └────────────────────┬───────────────────────────┘ │
│                       │                             │
│  ┌────────────────────┴───────────────────────────┐ │
│  │    OCI GPU Spot Instance (Training Jobs)        │ │
│  │    Unsloth + QLoRA → Qwen3-1.7B fine-tune      │ │
│  └────────────────────────────────────────────────┘ │
│                                                     │
│  ┌────────────────────────────────────────────────┐ │
│  │    MLflow (on Always Free ARM) - Tracking      │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Training workflow:**
1. Collect worker interaction data → OCI Object Storage
2. Process with Polars (on Always Free ARM instance)
3. Fine-tune Qwen3-1.7B with Unsloth QLoRA (on GPU spot instance)
4. Export to GGUF quantized format
5. Serve via Ollama (on Always Free ARM instance)
6. Track experiments with MLflow

**Estimated training cost per model update:** $15-40 (4-8 hours on A10 spot)

### 6.2 Phase 2: Hybrid (Cloud Training + On-Premise Inference)

**Architecture:** Training stays in cloud, inference moves to ARM server.

```
┌──────────────────────────────────────────────────────┐
│                 PHASE 2 ARCHITECTURE                  │
│                                                      │
│  ON-PREMISE (Kenya)          │  CLOUD (Oracle)      │
│                              │                      │
│  ┌──────────────────┐       │  ┌────────────────┐  │
│  │  Ampere Altra    │       │  │  GPU Instance   │  │
│  │  Q80-30 (80c)    │       │  │  (Training)     │  │
│  │  vLLM Serving    │       │  │  Unsloth+QLoRA  │  │
│  │  256GB RAM       │       │  │  Qwen3-8B       │  │
│  └────────┬─────────┘       │  └────────┬────────┘  │
│           │                 │           │            │
│  ┌────────┴─────────┐       │  ┌────────┴────────┐  │
│  │  MinIO (S3-compat│       │  │ OCI Object      │  │
│  │  Object Storage) │◄──────┼──│ Storage (sync)  │  │
│  └────────┬─────────┘       │  └─────────────────┘  │
│           │                 │                        │
│  ┌────────┴─────────┐       │                        │
│  │  Solar Array     │       │                        │
│  │  + Battery       │       │                        │
│  └──────────────────┘       │                        │
│                              │                        │
│  ┌──────────────────┐       │                        │
│  │  Worker Devices  │       │                        │
│  │  (Mobile API)    │───────┼────► Cloud fallback    │
│  └──────────────────┘       │                        │
└──────────────────────────────────────────────────────┘
```

**Migration trigger:** When inference costs exceed $200/month on cloud, buy the ARM server.

**Data flow:**
1. Worker interactions stored locally on MinIO
2. Training data synced to OCI Object Storage (nightly)
3. Training runs on GPU instances in cloud
4. Trained models synced back to on-premise MinIO
5. vLLM serves models from local storage
6. Cloud inference as overflow/fallback

### 6.3 Phase 3: On-Premise Mini DC (Training + Inference)

**Architecture:** Full training and inference on-premise. Cloud for overflow only.

```
┌──────────────────────────────────────────────────────────┐
│                    PHASE 3: MINI DC                       │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │              42U Rack (Nairobi)                    │  │
│  │                                                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐          │  │
│  │  │ ARM Node │ │ ARM Node │ │ ARM Node │ Compute  │  │
│  │  │ #1 (API) │ │ #2 (Inf) │ │ #3 (Inf) │ Cluster  │  │
│  │  └──────────┘ └──────────┘ └──────────┘          │  │
│  │                                                    │  │
│  │  ┌──────────┐ ┌──────────┐                        │  │
│  │  │ GPU Node │ │ Storage  │ Training +             │  │
│  │  │ 4x A10   │ │ 20TB NVMe│ Storage               │  │
│  │  └──────────┘ └──────────┘                        │  │
│  │                                                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐          │  │
│  │  │ 25GbE    │ │ 10kVA    │ │ Env Mon  │ Infra    │  │
│  │  │ Switch   │ │ UPS      │ │ Sensors  │          │  │
│  │  └──────────┘ └──────────┘ └──────────┘          │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │        Solar Array (25-40kW) + Battery Bank        │  │
│  │        Geothermal Grid Backup                      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │     Kubernetes (K3s) — Container Orchestration     │  │
│  │     vLLM + SGLang + MLflow + MinIO + Ray          │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Software stack:**
- **OS:** Ubuntu 24.04 LTS (ARM64)
- **Orchestration:** K3s (lightweight Kubernetes, perfect for small clusters)
- **Inference:** vLLM (API serving), llama.cpp (CPU-only backup)
- **Training:** Unsloth + Axolotl (distributed via Ray)
- **Storage:** MinIO (S3-compatible object storage)
- **Tracking:** MLflow (experiment tracking)
- **Monitoring:** Prometheus + Grafana
- **Networking:** Calico (CNI), MetalLB (load balancing)

### 6.4 Phase 4: Pan-African DC Network (Federated)

**Architecture:** Multiple containerized DCs across Africa, federated training.

```
┌───────────────────────────────────────────────────────────────┐
│              PHASE 4: PAN-AFRICAN DC NETWORK                  │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Nairobi DC  │  │  Lagos DC   │  │  Accra DC   │  ...     │
│  │  (Primary)   │  │  (Nigeria)  │  │  (Ghana)    │          │
│  │  Container   │  │  Container  │  │  Container  │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                   │
│  ┌──────┴────────────────┴────────────────┴──────────────┐   │
│  │              Fiber Backbone / VPN Mesh                  │   │
│  └──────────────────────┬────────────────────────────────┘   │
│                         │                                     │
│  ┌──────────────────────┴────────────────────────────────┐   │
│  │           Federated Learning Coordinator               │   │
│  │           (Flower Framework + PySyft)                  │   │
│  │           Gradient aggregation in Nairobi              │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │              Triton Inference Server                   │   │
│  │              Multi-model, multi-site serving           │   │
│  └───────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

**Federated training protocol:**
1. Each DC trains on LOCAL data only (data never leaves the country)
2. Model gradients encrypted and sent to Nairobi aggregation server
3. Differential privacy noise added (ε = 1.0-8.0)
4. Global model updated and distributed back to all DCs
5. Local fine-tuning adapts global model to regional specifics

**Serving architecture:**
- Each DC serves inference locally (5-20ms latency)
- Cross-DC failover for model serving
- Global model registry in Nairobi
- Triton manages model versions and routing

---

## 7. Cost Analysis

### 7.1 Oracle Cloud Costs by Phase

| Metric | Phase 1 (1K) | Phase 2 (10K) | Phase 3 (100K) | Phase 4 (1M) |
|---|---|---|---|---|
| **Inference** | $0 (Always Free) | $50-100 | $0 (on-prem) | $0 (on-prem) |
| **Training** | $60-90 | $150-300 | $0 (on-prem) | $0 (on-prem) |
| **Storage** | $2.50 | $10-25 | $0 (on-prem) | $0 (on-prem) |
| **Bandwidth** | $8.50 | $30-50 | $5-10 (sync) | $20-50 (sync) |
| **Cloud total** | **$71-101** | **$240-475** | **$5-10** | **$20-50** |

### 7.2 On-Premise Costs

| Metric | Phase 2 (1 server) | Phase 3 (Mini DC) | Phase 4 (Container) |
|---|---|---|---|
| **Hardware (amortized/3yr)** | $190/month | $1,200-2,100/month | $5,800-12,000/month |
| **Solar (amortized/10yr)** | $15/month | $210-420/month | $830-2,100/month |
| **Internet (fiber)** | $50-100/month | $100-200/month | $200-500/month |
| **Maintenance** | $30/month | $100-200/month | $500-1,000/month |
| **Ops staff** | $0 (Valentine) | $200-500/month | $1,000-3,000/month |
| **On-prem total** | **$285-335/month** | **$1,810-3,420/month** | **$8,360-18,600/month** |

### 7.3 Break-Even Analysis

| Phase | Cloud Cost | On-Prem Cost | Winner | Users |
|---|---|---|---|---|
| Phase 1 | $71-101/month | N/A | **Cloud** | 1,000 |
| Phase 2 | $240-475/month | $285-335/month | **Cloud** (barely) | 10,000 |
| Phase 2+ | $500+/month | $285-335/month | **On-Prem** ✓ | 15,000+ |
| Phase 3 | $2,000+/month (cloud) | $1,810-3,420/month | **On-Prem** ✓ | 100,000 |
| Phase 4 | $20,000+/month (cloud) | $8,360-18,600/month | **On-Prem** ✓ | 1,000,000 |

**Break-even point: ~10,000-15,000 active users.**

At this scale, the monthly cloud bill exceeds the amortized cost of owning an ARM server with solar power. Every user beyond this point is pure savings.

### 7.4 Cost per Transaction

| Phase | Monthly Cost | Transactions/Day | Cost per Transaction |
|---|---|---|---|
| Phase 1 | $71-101 | 10,000 | $0.00024-0.00034 |
| Phase 2 | $285-335 | 100,000 | $0.000095-0.00011 |
| Phase 3 | $1,810-3,420 | 1,000,000 | $0.000060-0.00011 |
| Phase 4 | $8,360-18,600 | 10,000,000+ | $0.000028-0.000062 |

**At Phase 4, each transaction costs $0.00003-0.00006** — less than a hundredth of a cent. This is the economics that makes serving informal economy workers viable.

---

## 8. Migration Path: Cloud → Own DC

### 8.1 Migration Strategy Overview

The migration is not a one-time event — it's a continuous evolution where each component moves when it makes economic sense.

### 8.2 Step-by-Step Migration

**Step 1: Containerize Everything (Day 1)**
- All services run in Docker containers from Day 1
- Use OCI Container Engine (OKE) or K3s on Always Free instances
- This makes migration a deployment change, not an architecture change

```dockerfile
# Example: Inference service container
FROM arm64v8/python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt  # vllm, fastapi, etc.
COPY src/ /app/
CMD ["python", "-m", "vllm.entrypoints.openai.api_server", "--model", "/models/qwen3-8b"]
```

**Step 2: Model Format Standardization**
- All models saved in GGUF format (llama.cpp compatible) AND safetensors (HuggingFace)
- Models stored in S3-compatible storage (OCI Object Storage → MinIO)
- Migration = change the S3 endpoint URL

```python
# Config-driven model location
MODEL_STORE = os.getenv("MODEL_STORE", "oci://bucket-name/models/")  # Phase 1
MODEL_STORE = os.getenv("MODEL_STORE", "http://minio.local:9000/models/")  # Phase 2+
```

**Step 3: Inference Migration (Phase 1 → Phase 2)**
1. Deploy ARM server in Kenya
2. Install K3s + vLLM + MinIO
3. Sync models from OCI Object Storage to local MinIO
4. Run inference on both cloud and on-premise (shadow mode)
5. Compare latency and accuracy
6. Cut over DNS/load balancer to on-premise
7. Keep cloud as fallback for 30 days
8. Decommission cloud inference

**Step 4: Training Migration (Phase 2 → Phase 3)**
1. Purchase GPU node for the mini DC
2. Install Unsloth + Axolotl + Ray on GPU node
3. Migrate training data to local MinIO
4. Run training jobs on both cloud and on-premise
5. Validate model quality
6. Cut over training pipeline
7. Cloud GPU used only for overflow/experimentation

**Step 5: Multi-Site Expansion (Phase 3 → Phase 4)**
1. Deploy containerized DC in new city
2. Establish VPN/fiber connection to Nairobi
3. Configure Flower federated learning
4. Local data stays local, gradients shared
5. Triton manages cross-site model routing

### 8.3 Zero-Downtime Migration Checklist

- [ ] All services containerized (Docker)
- [ ] All models in portable format (GGUF + safetensors)
- [ ] All storage S3-compatible (OCI Object Storage / MinIO)
- [ ] All configs environment-variable driven
- [ ] Health checks on all services
- [ ] Circuit breaker pattern for cloud/on-prem failover
- [ ] DNS-based traffic shifting (gradual cutover)
- [ ] Monitoring parity (same Prometheus/Grafana stack)
- [ ] Rollback plan documented and tested

### 8.4 Container Orchestration

| Phase | Orchestrator | Why |
|---|---|---|
| Phase 1 | Docker Compose | Simple, single-node |
| Phase 2 | K3s | Lightweight Kubernetes, single server |
| Phase 3 | K3s (multi-node) | 3-5 node cluster, still simple |
| Phase 4 | K3s (per site) + federation | Each site independent, federated via API |

**Why K3s over full Kubernetes:**
- 50MB binary, 512MB RAM minimum
- ARM64 native
- Production-ready (used by NASA, Verizon, etc.)
- Single command install: `curl -sfL https://get.k3s.io | sh -`

---

## 9. Academic Framework

### 9.1 Degree Units Driving Infrastructure

The academic framework ensures Angavu's infrastructure investment is also building human capital:

| Degree Unit | Infrastructure Component | Skills Developed |
|---|---|---|
| **DC101: Data Center Fundamentals** | Solar array installation, rack setup | Electrical, mechanical, networking |
| **DC201: Server Administration** | ARM server management, K3s | Linux, containers, monitoring |
| **ML101: Machine Learning Basics** | Qwen3 fine-tuning with Unsloth | Python, PyTorch, data processing |
| **ML201: Model Training & Serving** | vLLM deployment, model optimization | MLOps, inference optimization |
| **ML301: Federated Learning** | Flower framework, multi-site training | Distributed systems, privacy |
| **NET101: Networking** | VPN, fiber, load balancing | Network engineering |
| **SEC101: Data Security** | Encryption, access control, auditing | Cybersecurity fundamentals |
| **BUS101: Infrastructure Economics** | Cost analysis, capacity planning | Business, finance, operations |

### 9.2 Learning Path → Infrastructure Growth

```
Year 1: Students learn on Phase 1 (cloud) infrastructure
Year 2: Students help BUILD Phase 2 (ARM server + solar)
Year 3: Students help OPERATE Phase 3 (mini DC)
Year 4: Students help EXPAND Phase 4 (pan-African network)
```

Each student who completes the program has hands-on experience building and operating real data center infrastructure — not textbook theory, but production systems serving real users.

---

## 10. Africa's Data Center for Africa's Workers

### 10.1 Why This Matters

This is not about building another cloud provider. This is about building infrastructure that:
1. **Serves workers who earn $2-10/day** — at transaction costs of $0.00003
2. **Keeps African data in Africa** — data sovereignty, not colonial extraction
3. **Creates African tech jobs** — building, operating, maintaining real infrastructure
4. **Runs on African energy** — solar + geothermal, not imported diesel generators
5. **Trains African talent** — every DC is also a classroom

### 10.2 The Structural Advantage

| Factor | Why It Matters |
|---|---|
| **Geothermal at $0.05/kWh** | Cheaper than any fossil fuel, anywhere |
| **Solar at 5-6 kWh/m²/day** | Among the highest globally |
| **ARM servers at 3-5x perf/watt** | Solar-powered DCs become viable |
| **Kenya's tech ecosystem** | M-Pesa proves African tech scales |
| **No legacy infrastructure** | Leapfrog directly to best-in-class |
| **Containerized DCs** | Deploy anywhere in Africa in 12 weeks |

### 10.3 What Success Looks Like

**2027:** Phase 1 operational, 1,000 workers using Angavu services via Oracle Cloud
**2028:** Phase 2 operational, 10,000 workers, first ARM server in Nairobi with solar
**2029:** Phase 3 operational, 100,000 workers, mini DC training and serving locally
**2030:** Phase 4 begins, containerized DCs in Lagos, Accra, Addis Ababa
**2032:** Pan-African network serving 1M+ workers, federated training across continent

### 10.4 The Data Center Valentine Builds

This is not a hyperscale data center. It's not trying to be AWS. It's the data center that:
- Fits in a shipping container
- Runs on solar panels
- Serves workers who make $5/day
- Costs less per transaction than any cloud provider
- Trains the next generation of African engineers
- Keeps African data on African soil

**That's the data center for Africa's informal economy.**

---

## Appendix A: Technology Decision Matrix

| Decision | Recommendation | Rationale |
|---|---|---|
| Cloud provider | Oracle Cloud | Free ARM instances, competitive GPU pricing |
| ARM CPU | Ampere Altra Q80-30 | Best perf/watt, 80 cores, 190W TDP |
| GPU (training) | NVIDIA A10 (Phase 1-3) | 24GB VRAM, cost-effective for QLoRA |
| Inference engine | vLLM + llama.cpp | vLLM for serving, llama.cpp for CPU-only |
| Fine-tuning | Unsloth + QLoRA | 2x faster, 70% less VRAM |
| Base model | Qwen3 | Multilingual, multiple sizes, great fine-tuning support |
| Federated learning | Flower + PySyft | Simple API, privacy-preserving |
| Data processing | Polars | 10-100x faster than Pandas |
| Object storage | MinIO | S3-compatible, self-hosted, free |
| Orchestration | K3s | Lightweight K8s, ARM native |
| Monitoring | Prometheus + Grafana | Industry standard, open source |
| Container runtime | Docker + containerd | Standard, well-supported |

## Appendix B: Key Vendor Contacts (Africa)

| Vendor | Product | Region |
|---|---|---|
| Ampere Computing | ARM CPUs | Direct (US), distributors in Africa |
| Schneider Electric | Containerized DCs, UPS, cooling | Pan-African presence |
| Huawei | DC infrastructure, networking | Strong Africa presence |
| Vertiv | Power, cooling, IT management | Pan-African presence |
| Safaricom | Fiber, colocation | Kenya |
| Africa Data Centres | Colocation | Kenya, South Africa, Nigeria |

## Appendix C: Risk Mitigation

| Risk | Mitigation |
|---|---|
| Oracle Cloud account reclamation | Keep CPU utilization >20% with synthetic load |
| ARM server hardware failure | Keep cloud fallback for 30 days after migration |
| Solar power intermittency | Battery bank (10-16hr backup) + geothermal grid |
| Internet connectivity | Dual ISP + satellite backup (Starlink) |
| Skills gap | Academic framework trains local talent |
| Model quality degradation | A/B testing, automated evaluation pipeline |
| Data loss | 3-2-1 backup rule: 3 copies, 2 media, 1 offsite |

---

*This document is a living artifact. Update as hardware prices change, new tools emerge, and the platform scales.*

**Swarm E2 — Training Infrastructure & Data Center Architecture Team**
**Angavu Intelligence**
