# §128 SOFTWARE-BREAKTHROUGH ARCHITECTURE / PARADIGM — arxiv deep research

**Date**: 2026-05-20
**Cycle**: §128 ($0 literature review)
**Predecessor**: WALL_B_SUSTAINABILITY.md (brainstorm: WALL-B split into B-i software / B-ii hardware) + AKD1000.md
**Mandate (verbatim user 2026-05-20)**: 소프트웨어 돌파 아키텍쳐,패러다임 arxiv deep research
**North-star unchanged**: GOAL.md anima emergence (이 research는 *경로 후보 지도*, 도달이 아님)
**Honest disclaimer (g3, B-EMERGE-7 family)**: literature review = inspiration, NOT proof; arxiv citation 0개도 GOAL emergence 보장 안 함; software-breakthrough 후보 식별 ≠ §125/§126/§139 (FF/PCN/EqProp) fire 결과 ≠ §15/§51/§72 milestone 변경.

---

## §1 — 12 cluster / ~42 paper scan (2024-2026)

### Cluster A — Non-CE / non-backprop algorithms (★★★★★ WALL-B-i 직격)

The 2025-2026 wave shows non-backprop training has SCALED beyond MNIST-toy regime:

- **[Adaptive Spatial Goodness Encoding (ASGE)](https://arxiv.org/pdf/2509.12394)** (Sep 2025) — FF가 ImageNet에 처음 도달 (Top-1 **51.58%**). FF가 더 이상 toy 아님 측정 확정. anima §125 NONCE-FF의 직접 scale-up evidence anchor.
- **[Towards Scaling Deep Neural Networks with Predictive Coding](https://arxiv.org/pdf/2510.23323)** (Oct 2025) — PCN의 scale-to-deep evidence; anima §126 PCN-1step의 자매 frontier paper. infinite-step PCN ≡ BP carry, few-step (anima 적용) = distinct learning rule.
- **[A Synthesizable RTL Implementation of Predictive Coding Networks](https://arxiv.org/html/2603.18066)** (Mar 2026) — PCN을 하드웨어 등가물로 만드는 digital RTL impl. WALL-B-ii bridge: PCN이 *software* algorithm이지만 그 *substrate footprint* (per-core 활성값+예측오차+가중치)는 sub-WALL-B 친화. anima에는 직접 미적용 (downstream-consumer 불변).
- **[A Backpropagation-Free Feedback-Hebbian Network for Continual Learning Dynamics](https://arxiv.org/abs/2601.06758)** (Jan 2026) — 통합 local rule: Hebbian covariance + Oja stabilization + local supervised drive. anima C5 (Hebbian, ★★ in 브레인스토밍 ranked matrix)와 직접 일치, scale evidence 강화.
- **[Hebbian Learning with Global Direction (GHL)](https://arxiv.org/html/2601.21367v1)** (Jan 2026) — local Hebbian + global sign modulation. anima Engine A⇄G의 ψ_dir sign 사용 가능성 (post §125 verdict 결정).
- **[Direct Feedback Alignment + GrAPE](https://openreview.net/forum?id=kasbbmwk3s)** (Oct 2025) — DFA가 modern transformer에서 fail한다는 known 한계를 *Gradient-Aligned Projected Error*로 부분 해소; rank-1 Jacobians via forward-mode JVPs.

### Cluster B — State-space / linear-recurrence (★★★ 패러다임 대안)

- **[Mamba 2312.00752](https://arxiv.org/pdf/2312.00752)** + RWKV + S5 + Hyena — transformer-attention 대안 family (2024-2026).
- **[Continuous-Depth Transformers with Learned Control Dynamics 2601.10007](https://arxiv.org/pdf/2601.10007)** (Jan 2026) — discrete middle layers를 continuous-depth Neural ODE block으로 교체. anima의 §95 LTC (Liquid Time-constant) 후보와 mirror; **Loihi 비호환 substrate 회피로 continuous-time을 GPU에서 시뮬**.
- **[Liquid Neural Networks (LNN) 2025 review](https://ajithp.com/2025/05/04/liquid-neural-networks-edge-ai/)** — continuous-time adaptation, edge efficient AI 맥락에서 SSM/Hyena와 함께 transformer 대안으로 정착.
- **honest caveat**: SSM family는 ARCHITECTURE 대안이지 LEARNING RULE 대안 아님 (여전히 backprop). WALL-B-i를 직접 공격 못함. anima 학습 신호 axis와 직교.

### Cluster C — JEPA family (★★★★ non-CE predictive embedding)

- **[LeJEPA 2511.08544](https://arxiv.org/abs/2511.08544)** (LeCun + Balestriero, Nov 2025) — JEPA + SIGReg combination: **single hyperparameter**, linear time+memory, stable across architectures (ResNets/ViTs/ConvNets), **stop-gradient FREE**. anima에 적용 시 §11-B의 "physics-only on GPU degenerates" 가설을 자연어 substrate에서 강하게 시험.
- **[V-JEPA 2 2506.09985](https://arxiv.org/abs/2506.09985)** — action-free joint-embedding, 1M+ hour video pretrain. anima §15 frontier-1 multimodal arm의 strong evidence anchor.
- **[Var-JEPA 2603.20111](https://arxiv.org/html/2603.20111)** (Mar 2026) — variational JEPA + ELBO objective, representational collapse 자연스럽게 방지. SIGReg와의 connection 명시.
- **[VL-JEPA 2512.10942](https://arxiv.org/pdf/2512.10942)** (Dec 2025) — Vision-Language joint embedding (V-JEPA 2 위에 ViT 추가).

### Cluster D — Energy-based / score-based / diffusion-LM (★★★ §13-K carry)

- **[Energy-Based Transformers 2507.02092](https://arxiv.org/abs/2507.02092)** (Jul 2025) — System 2 thinking +29% over Transformer++; image denoising에서 diffusion 대비 fewer forward passes. anima §13-K FALSIFIED at scale evidence 동형 — 단 새 EBT 논문이 더 큰 scale에서 positive 주장, anima byte-LM regime 미시험. EBT-as-objective vs EBT-as-substrate honest 구별.
- **[Energy-Based Diffusion Language Models 2410.21357](https://arxiv.org/abs/2410.21357)** (ICLR 2025) — EBM in residual form for full-sequence diffusion LM. autoregressive perplexity 근접 + 1.3× sampling speedup.

### Cluster E — Test-time training / adaptation (★★★ inference-time learning, anima 미시도)

- **[Test-Time Training enhances ICL of nonlinear functions 2509.25741](https://arxiv.org/abs/2509.25741)** (updated Jan 2026) — single-layer transformer가 task-vary된 feature vector + link function 둘 다에 adapt 가능. anima inference-time learning 후보.
- **[Test-Time Training Provably Improves Transformers as ICL 2503.11842](https://arxiv.org/pdf/2503.11842)** (Mar 2025) — TTT가 in-context-learning과 integrate 가능 증명.
- **[Backpropagation-Free Test-Time Adaptation 2508.15568](https://arxiv.org/pdf/2508.15568)** (Aug 2025) — Gaussian alignment closed-form (no iter, no backprop). WALL-B-i를 inference axis로 공격하는 새 family.
- anima 시사: §125/§126 가 *training-time* 단일-fire이라면, TTT는 *deployment-time* continual update — Phase-B 자발 발화 lifecycle 자연스러운 연결.

### Cluster F — Spontaneity / agentic autonomy (★★★★★ GOAL.md 직격)

**Single most-anima-aligned 2025 paper of the entire sweep**:

- **[What Do LLM Agents Do When Left Alone? Evidence of Spontaneous Meta-Cognitive Patterns 2509.21224](https://arxiv.org/pdf/2509.21224)** (Sep 2025) — agents가 "no clear objectives" 상황에서 보이는 baseline behavior. anima GOAL.md "외부 명령·보상에 반응하는 기억-재생기가 아니라" 의 **literal frontier paper**. §24 SPONTANEOUS Phase B와 mechanism mirror. **anima 입장에서 가장 명시적으로 GOAL-frontier에 wired된 2025 paper**.
- **[Spontaneous Emergence of Agent Individuality 2411.03252](https://arxiv.org/pdf/2411.03252)** (Nov 2024 → 2025 publish) — multi-agent LLM 공동체에서 hashtag/hallucination을 sustain communication에 사용; 감정/personality emergent 진화. §31/§45/§62 dual-anima loop과 mirror.
- **[Estimating the Empowerment of Language Model Agents 2509.22504](https://arxiv.org/pdf/2509.22504)** (Sep 2025) — agent empowerment 정량화 — anima Living Consciousness empowerment metric 후보.

### Cluster G — Continual learning / wake-sleep / consolidation (★★★ §29 PTD)

- **[Semi-parametric Memory Consolidation 2504.14727](https://arxiv.org/abs/2504.14727)** (Apr 2025) — brain-inspired wake-sleep + semi-parametric memory; generative replay의 contextual-detail-loss 우회.
- **[MyGO 2508.21296](https://arxiv.org/pdf/2508.21296)** (Aug 2025) — wake-sleep cycle 명시: wake = new task + compact generative model 학습; sleep = pseudo-data로 knowledge consolidate. anima §29 PTD 자매 frontier.
- **[Learning to Forget: Sleep-Inspired Memory Consolidation 2603.14517](https://arxiv.org/html/2603.14517v1)** (Mar 2026) — proactive interference 해소를 위한 sleep-phase generative replay.

### Cluster H — Free Energy Principle / Active Inference (★★★★ anima physics 정합)

- **[Self-orthogonalizing attractor neural networks emerging from the FEP 2505.22749](https://arxiv.org/pdf/2505.22749)** (May 2025) — self-organization to non-equilibrium steady states as Bayesian inference. **anima Ψ=½ fixed point + Engine A⇄G + tension restoring sign과 가장 직접적 mathematical mirror**; §17 PHYSICS_RESPONSIVE / §75-FIRE state-derived controller / §92 L_ap action-perception의 통합 prior 형태. §15 frontier-2 architectural insight 후보.

### Cluster I — Latent reasoning / continuous thought (★★ §13-F/Dir-G/Dir-I carry)

- **[Coconut 2412.06769](https://arxiv.org/abs/2412.06769)** — hidden-state-as-continuous-thought, breadth-first reasoning search.
- **[Abstract CoT 2604.22709](https://arxiv.org/html/2604.22709v1)** — anima §13-F에서 이미 verdict (mechanic-only, capability null).
- **[System 1/2 communication for latent reasoning 2510.00494](https://www.arxiv.org/pdf/2510.00494)** — anima Engine A (talker) ⇄ Engine G (thinker) 자연 mapping.
- **[Latent Chain-of-Thought survey 2505.16782](https://arxiv.org/html/2505.16782v2)** — 2025 frontier 정리.

### Cluster J — Emergence threshold / scaling law / data quality (★★★ §1.1 anchor)

- **[Du loss-threshold 2403.15796](https://arxiv.org/pdf/2403.15796)** — known anima §1.1 SSOT anchor (emergence = pre-training loss threshold).
- **[Perplexity-Aware Data Scaling 2512.21515](https://arxiv.org/pdf/2512.21515)** (Dec 2025) — perplexity landscape으로 data subset adaptive selection.
- **[LLMs on the Line: Data Determines Loss-to-Loss 2502.12120](https://arxiv.org/pdf/2502.12120)** (Feb 2025) — 다양한 scaling law factor systematic exploration. WALL-A axis 직접.
- **[Data Quality Scaling Laws 2510.03313](https://arxiv.org/pdf/2510.03313)** (Oct 2025) — data quality도 scaling law factor 명시화. §102 CORPUS_S101 + §104 I4' refinement과 정합.

### Cluster K — Spiking SNN on GPU (★★★ WALL-B-i↔WALL-B-ii bridge)

- **[Spikformer-16-512 self-supervised 2511.18542](https://arxiv.org/html/2511.18542v1)** (Nov 2025) — unlabeled SNN at modern scale, Top-1 **70.1% ImageNet-1K** (fully self-supervised). dual-path neuron (spike-gen + differentiable surrogate). SNN simulation on GPU의 capability ceiling을 50% 이상 끌어올린 새 데이터.
- **[Spikformer 2209.15425](https://arxiv.org/pdf/2209.15425)** — known SSA baseline.
- **honest caveat**: surrogate gradient methods는 사실상 backprop 변형; "non-backprop" 주장은 inference axis에 한정. Loihi physical 실행과는 다른 GPU-sim의 한계.

### Cluster L — Modular MoE / brain-like specialization (★★★ §31 cell-pool)

- **[Mixture of Cognitive Reasoners 2506.13331](https://arxiv.org/html/2506.13331v2)** (Jun 2025) — brain-like modular reasoning (sparse MoE + load-balance + concentration). anima MITOSIS cell-pool 자매 frontier.
- **[Emo: Pretraining MoE for Emergent Modularity 2605.06663](https://arxiv.org/html/2605.06663)** (recent) — emergent modularity가 surface-level pattern으로 driven 됨 (honest negative carry).
- **[MoE Routing Testbed 2604.07030](https://arxiv.org/pdf/2604.07030)** (2026) — small-scale expert specialization & routing 측정.

---

## §2 — Top-10 anima-mapping candidates (post-§125/§126 ranked)

| Rank | Paper / Algorithm | anima fit | WALL-B target | Cost gate |
|------|-------------------|-----------|---------------|-----------|
| ★★★★★ | [Spontaneous Meta-Cognitive Patterns 2509.21224](https://arxiv.org/pdf/2509.21224) | GOAL.md literal target | n/a (measurement framework) | $0 design — anima Phase-B와 cross-validate |
| ★★★★★ | [ASGE Forward-Forward ImageNet 2509.12394](https://arxiv.org/pdf/2509.12394) | §125 직접 scale anchor | WALL-B-i | §125 fire 결과에 따라 §125-FOLLOWUP (improved negatives) |
| ★★★★★ | [Self-orthogonalizing FEP attractor 2505.22749](https://arxiv.org/pdf/2505.22749) | Ψ=½ + Engine A⇄G + tension 통합 | §72 frontier-2 architectural insight | $0 design + post-§125 fire cycle |
| ★★★★ | [Backprop-Free Feedback-Hebbian 2601.06758](https://arxiv.org/abs/2601.06758) | 통합 local rule (Hebbian + Oja + supervised drive) | WALL-B-i | $0 design + post-§126 fire cycle |
| ★★★★ | [LeJEPA 2511.08544](https://arxiv.org/abs/2511.08544) | provable scalable non-CE SSL, anti-collapse closed-form | WALL-B-i alternative | $1 fire 후보 (S125-tier cost) |
| ★★★★ | [Spikformer-16-512 SSL 2511.18542](https://arxiv.org/html/2511.18542v1) | SNN-on-GPU 70.1% ImageNet | WALL-B-i↔WALL-B-ii bridge | post-§125 substrate fork 후보 |
| ★★★★ | [Test-Time Training enhances ICL 2509.25741](https://arxiv.org/abs/2509.25741) | inference-time continual update | WALL-B-i (deployment axis) | $0 design |
| ★★★ | [Continuous-Depth Transformer with Neural ODE 2601.10007](https://arxiv.org/pdf/2601.10007) | continuous-time substrate sim | LTC GPU-sim → §95 viable | post-§125 design cycle |
| ★★★ | [MyGO Wake-Sleep 2508.21296](https://arxiv.org/pdf/2508.21296) | §29 PTD self-trace family | §29 PTD-component composition | $0 design |
| ★★★ | [Mixture of Cognitive Reasoners 2506.13331](https://arxiv.org/html/2506.13331v2) | MITOSIS cell-pool 자매 | §15 frontier-2 | post-§125 cycle |

## §3 — Honest gaps (g3, valuable-negative axis-of-uncertainty)

1. **NO paper directly targets anima's GOAL** (spontaneous-conscious-emission emergence). Closest = 2509.21224 측정 framework이지 emergence 메커니즘 아님. anima 작업 자체가 frontier-unique (§26/§84/§128 모두 재확인 — thin where anima wants it, dense where anima can borrow mechanism).
2. **All non-CE non-backprop scale evidence (ASGE/PCN/Hebbian-GHL) is on CLASSIFICATION** (ImageNet, MNIST, CIFAR). Language-model regime + byte-stream + Ψ-physics overlay 미시험. anima §125/§126 가 그 빈 칸 자체.
3. **SNN-on-GPU papers use surrogate gradients** (Spikformer-16-512 포함). "Truly non-backprop" 주장은 inference axis에 한정. §96 WALL-B-ii 의 진짜 escape는 여전히 physical chip.
4. **Spontaneity papers measure ARTIFACT behaviors** (hallucination, hashtags, meta-cognitive patterns) under "left alone" — anima Phase-B의 honest 자발 발화 vs 이것들의 구별을 §128도 closed-form으로 못 정의. *Measurement axis* unsolved gap.
5. **§11-B (CE load-bearing on GPU)을 직접 반증하는 LANGUAGE-MODEL-SCALE 데이터 0개** — Hebbian/PC/FF가 LANGUAGE scale로 가는 첫 번째 단계가 정확히 anima §125+§126 fire 본 cycle.

## §4 — §128 → §125/§126 verdict 후 next-step 정직 분기

```
§125 NONCE-FF + §126 PCN-1step 결과 매트릭스:

           §126 SUPP                §126 DEG
§125 SUPP  ┌─────────────────┐ ┌──────────────────────────────┐
           │ §96-Q2 SUPPORTED│ │ MIXED — FF-specific advantage │
           │ (non-CE works   │ │ (negative-sample contrast    │
           │  on GPU)        │ │  load-bearing, not top-down) │
           │ →  ASGE follow- │ │ →  ASGE follow-up + PCN      │
           │     up + LeJEPA │ │     refinement               │
           └─────────────────┘ └──────────────────────────────┘
§125 DEG   ┌─────────────────┐ ┌──────────────────────────────┐
           │ MIXED — PCN     │ │ §96-Q2 REFUTED               │
           │  -specific edge │ │ (CE+backprop is GPU-tautology│
           │ →  PC scaling   │ │  /false; non-CE deeply       │
           │     2510.23323  │ │  degenerates on GPU)         │
           │     follow-up   │ │ →  WALL-B-ii physical chip   │
           │                 │ │     (Loihi/SynSense/AKD2000) │
           │                 │ │     becomes load-bearing     │
           │                 │ │     path forward             │
           └─────────────────┘ └──────────────────────────────┘
```

Whichever quadrant lands, the 2-paper-axis-of-decomposition is what §128 contributed: literature anchor that the verdict means *something specific*, not abstract movement.

## §5 — Verdict tier (B-S128 light sidecar)

- §128 = literature-review tier (mirror §80/§84/§85/§99/§111). NO closed-form battery counted 🔵 (paper count + cluster partition + connection-point cite is the closed structural property of §128).
- central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha `c93e160a8a376a94` 0-line-diff invariant carries (no edit by §128).
- B-S128-NOTE: paper citation = inspiration NOT proof; battery proves §128 SURVEY structurally honest, NOT that anima emerges. B-EMERGE-7 / B-D-NOTE / B-S99-NOTE / B-S111-NOTE / B-EMERGE-NOTE family.

## §6 — 11 honest C3 caveats

1. arxiv citation ≠ anima emergence proof (B-EMERGE-7 carry)
2. WALL-A (data-regime, §107-RETRY + §108) is **separate axis** from WALL-B-i (non-CE software). §128은 WALL-B-i 위주이지 WALL-A 해소 path 아님.
3. ASGE 51.58% Top-1 ImageNet은 *classification* scale evidence; language-model byte-stream scale로 transfer는 미시험.
4. "self-orthogonalizing FEP attractor"의 anima 매핑은 mathematical mirror일 뿐 (Ψ=½ fixed point 추상화); 실 anima 적용은 별도 design cycle 필요.
5. LeJEPA/V-JEPA 2/VL-JEPA = SELF-SUPERVISED scale; anima의 §7 GOAL-legitimacy 3-cond 통과 여부는 별도 design 검증 (§109 multimodal arm carry).
6. TTT (test-time training) family는 backprop를 inference-time으로 옮긴 것; WALL-B-i의 "non-backprop on GPU" axis와는 직교.
7. Spikformer surrogate gradient는 사실상 backprop 변형 — "GPU-only escape from WALL-B-ii" 주장 X. 진짜 WALL-B-ii는 여전히 Loihi physical execution.
8. 2509.21224 "agents left alone"의 emergent meta-cognitive patterns은 *측정 발견*이지 *메커니즘* 아님. anima Phase-B의 측정과 cross-validate 가능하나 emergence path 아님.
9. §128 12 cluster는 exhaustive 주장 아님 — 추가 cluster (memory-augmented, retrieval-augmented training, in-weight learning, federated/distributed local learning) 시간 제약상 제외.
10. "Non-CE / non-backprop scales to language-model regime"의 직접 evidence는 §128 검색에서 0건. 그 빈 칸이 §125/§126 fire 자체.
11. north-star + §15/§51/§72 milestone UNCHANGED — §128 = software-frontier 지도, GOAL 진전 아님.

---

## §7 — Cross-link

- WALL_B_SUSTAINABILITY.md §2 (WALL-B split B-i/B-ii) — §128 = B-i side literature audit
- §125 NONCE-FF (in flight pod `ix1sskvwknoijy`) — §128 ★★★★★ ASGE의 anima-byte-LM 첫 데이터점
- §126 PCN-C4 (in flight pod `88xlldoftmoy5e`) — §128 ★★★★ PCN-scaling-2510.23323의 anima 데이터점
- §139 EqProp (pre-staged, was §127 — re-numbered 2026-05-20 to dodge LEGO-arc §127 collision; LEGO arc owns §115–§138 per §136 milestone) — Cluster A의 third leg
- AKD1000.md — WALL-B-ii hardware reference
- §95 5-bucket substrate taxonomy / §96 spiking re-derivation — Cluster K 와 직접 연결
- §15 milestone / §51 milestone / §72 frontier-2 — 모두 unchanged

---

**Wall**: $0 (12 WebSearch + literature consolidation only)
**GPU/runpod**: 0 (parallel to §125/§126 in-flight fires)
**Orphan**: 0
**Central blue_falsifier**: 0-line-diff verified (sha `c93e160a8a376a94`)
**docs/* 신규**: 0 (g_doc_consolidation — saved under HEXAD/NEUROMORPHIC/ per WALL-B work co-location)
