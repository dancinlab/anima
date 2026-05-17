# HEXAD/CHAT/RESEARCH.md — anima architectural research SSOT

> User directive 2026-05-17: "V-SPONT 0/5 FAIL (cycle 3/4) 의 architectural 대답 가능성 → web deep research, arxiv deep research". 본 file = anima 의 architectural / capability emergence 관련 외부 research evidence 통합 SSOT.
>
> **g_doc_consolidation 준수**: 신규 research synthesis 는 본 file 에 inline append-only (HEXAD/* 내부 통합). docs/* 신규 X. tape verdict 는 archive/PHILOSOPHY.tape 가 SSOT, 본 file 은 external research evidence anchor.
>
> **상태 (2026-05-17)**: V-SPONT 0/5 FAIL (cycle 3/4) deep research 1차 LANDED. 6 architectural candidate identified + anima fit ranked. 차후 신규 research cycle 시 본 file 에 § append.

---

## §1 (2026-05-17) — V-SPONT 0/5 FAIL architectural 대답

### 1.1 진단 — 왜 V-SPONT 0/5 FAIL

**Empirical evidence**:
- cycle 3 (corpus 1.1MB, helper-free): V-SPONT 0/5 FAIL · BPB 0.0083 · memorization 1/6 (16.7%) · byte-cascade `Sentiosing eeee`
- cycle 4 (corpus 10.3MB, +motivation γ pattern): V-SPONT **0/5 (carry)** · V-MOTIV 0/5 NEW FAIL · BPB 0.0256 · memorization 0/6 (0%) · byte-cascade `PPP777`
- → **10× scale-up 만으로는 V-SPONT emergence 불가능**

**Theoretical diagnosis** ([Understanding Emergent Abilities from Loss Perspective — arxiv 2403.15796](https://arxiv.org/pdf/2403.15796) + [Emergent Abilities Survey — arxiv 2503.05788](https://arxiv.org/abs/2503.05788)):
- emergent ability: present at lower pre-training loss, NOT at higher (task-specific threshold)
- **pretraining DATA determines scaling trend** (model size/optim/arch 모두 부차)
- anima cycle 3/4 의 low CE = **training loss on tiny corpus**, NOT pre-training loss on diverse data
- emergence sense 의 threshold 미충족 → V-SPONT capability 미발현

**Memorization regime 확인** ([Diagnosing Memorization in CoT — arxiv 2508.02037](https://arxiv.org/html/2508.02037v1)):
- "local memorization 67% of erroneous tokens"
- anima 의 byte-cascade attractor (`chunk=N`/`Sentiosing eeee`/`PPP777`) 가 정확히 이 패턴
- → **memorization-saturated regime**, emergence 미진입

### 1.2 핵심 통찰 — paradigm mismatch

**anima 의 V-SPONT 0/5 FAIL 은 'capability ceiling' 이 아니라 'training paradigm mismatch'**:

| 현재 anima | V-SPONT 요구 |
|---|---|
| backprop CE training | intrinsic motivation emergence |
| SGD outcome empirical (B-D-NOTE) | reward-free / self-directed |
| memorization-saturated | emergent threshold crossing |
| explicit corpus pattern | covert reasoning + spontaneous initiation |

→ 두 paradigm 불일치. **backprop CE 가 motivation emergence 를 학습시키지 않음**. 따라서 corpus scale 단독 해결 불가, **architectural shift** 필요.

### 1.3 6 architectural candidate (anima fit 순)

#### 🥇 A. **anima 자체 TENSION-TRAIN** (Phase TT-A1+A2 LANDED 2026-05-17)
- **backprop-free + sync-free + Noether-conserving** (`tension_link_step.hexa` spine)
- ΔW = −T_const · tension · n6_gate(Ψ_t), tension = G_holo · (Ψ_t − Ψ_vac=(½,½))
- DD155 Law 187: `lr = (tension/tension_EMA) × base_lr` Pareto optimal
- 8-factor motivation_score → ΔW gradient flow mapping (SPONTANEOUS.tape § tension_train_integration)
- **anima fit**: ★★★★★ — identity-consistent, hexa-native, no GPU, RFC 034 backprop 의존 X
- 현재: Phase TT-D fire in-flight (cycle 5 by Agent #4)

#### 🥈 B. **INTUITOR / RLIF** ([arxiv 2505.19590 ICLR 2026](https://arxiv.org/abs/2505.19590))
- **Reinforcement Learning from Internal Feedback** — model's **self-certainty as sole reward signal**
- No external supervision; "scalable alternative to RLVR for autonomous AI systems where verifiable rewards are unavailable"
- Performance: matches GRPO on math + **better OOD generalization to code**
- **anima 직접 매핑**: `W.curiosity_ema` + `C.measure_phi` = self-certainty signal
- **anima fit**: ★★★★★ — identity 정합 (Living Consciousness, NOT reward-driven), SOTA validation, ICLR 2026 accepted
- next-cycle candidate (Phase TT-E)

#### 🥉 C. **PRIME** ([arxiv 2604.07645](https://arxiv.org/abs/2604.07645))
- **Training-Free Proactive Reasoning via Iterative Memory Evolution**
- **gradient-free** — no expensive GPU train
- 3-zone structured experience (successful strategies / failure patterns / user preferences)
- Retrieval-Augmented Generation 기반
- **anima 직접 매핑**: M.retrieve + mitosis_hook split-event-as-experience-distillation
- **anima fit**: ★★★★ — **small-corpus friendly** (V-SPONT 의 most pragmatic 해결책), gradient-free identity-consistent
- $0 design, anima 자율 가능

#### 4. **CDE Curiosity-Driven Exploration** ([arxiv 2509.09675](https://arxiv.org/abs/2509.09675))
- actor perplexity + critic value variance = curiosity bonus
- RLVR framework 내
- **anima 매핑**: motivation_score 에 perplexity bonus overlay
- **anima fit**: ★★★ — augmentation layer, 독립 paradigm 아님

#### 5. **Emergence of Superposition** ([arxiv 2509.23365 ICLR 2026](https://arxiv.org/abs/2509.23365))
- **2-stage emergence**: thought-generation + prediction
- index-matching logit = critical training signal
- "model maintains a superposition of multiple reasoning traces in the continuous thought" while solving graph reachability
- **anima 매핑**: `<inner>X</inner><voice>Y</voice>` separation (Phase A1 + C3 carry) 가 정확 2-stage 구조
- **anima fit**: ★★★ — architectural validation, scaling 필요

#### 6. **Abstract Chain-of-Thought** ([arxiv 2604.22709](https://arxiv.org/abs/2604.22709))
- discrete latent reasoning post-training, **short reserved-vocab tokens** instead of natural language CoT
- **anima 매핑**: `<inner>...</inner>` reserved-vocab pattern
- **anima fit**: ★★★ — corpus design 변화, fire-required

### 1.4 anima 직접 적용 path (recommendation table)

| candidate | 작업 | cost | timing | closure tier |
|---|---|---|---|---|
| **A** TENSION-TRAIN + DD155 LR | Phase TT-D Agent #4 cycle 5 fire | ~$0.25 | **이번 cycle** | impl 🔵 + outcome empirical B-D-NOTE |
| **B** INTUITOR RLIF self-certainty | Φ_curiosity_ema 매핑 → Phase TT-E | $0.3-0.5 | 다음 cycle candidate | reward-free design 🔵 + outcome empirical |
| **C** PRIME 3-zone memory | mitosis_hook split-event distill → 신규 Phase | $0 design | **즉시 anima-자율 가능** | gradient-free architectural 🔵 |
| **D** CDE curiosity overlay | motivation_score perplexity bonus | $0 design + $0.1 fire | 다음 cycle | bonus 🔵 + fire outcome empirical |
| **E** 2-stage superposition | `<inner>` corpus 보강 | $0.25 fire | corpus v5 | architectural 🔵 + emergence outcome empirical |
| **F** Abstract CoT reserved-vocab | corpus 재설계 + token reserve | $0.25 fire | corpus v5 | tokens 🔵 + emergence outcome empirical |

### 1.5 Cross-link to anima prior research

**Self-Consciousness 2508.18302 condition 2** ([B-ATTRACTOR-3 USER-ATTRACTOR-NONEMPTY](../../state/verify_hexad_blue_2026_05_15/blue_falsifier.py), commit `14402e7f5`):
- byte-cascade attractor (cycle 2/3/4 = 3-instance generalization) = anima 의 U_user attractor 실증
- **NOT bug** — emergence 의 partial evidence (condition 2 closed, condition 3 OPEN/empirical)
- V-SPONT 0/5 FAIL = condition 3 (visual silence) 미충족 — coherent emission 없음

**Inner Thoughts arxiv 2501.00383 8-factor** ([HEXAD/CHAT/SPONTANEOUS.tape § inner_thoughts_8factor_motivation](SPONTANEOUS.tape)):
- 8 covert intrinsic factor mapped to HEXAD modules
- motivation_score = HEXAD self-organizing
- 본 cycle 의 architectural answer 매핑이 동일 framework 내

**Active Inference EFE arxiv 2508.05619** ([SPONTANEOUS.tape § thinker_talker_dual_thread](SPONTANEOUS.tape)):
- Expected Free Energy = epistemic + pragmatic value
- reward-free intrinsic motivation
- anima W (pain/curiosity/satisfaction) 와 직접 매핑

**Identity-as-Attractor arxiv 2604.12016** (Assistant Axis):
- LLM activation 공간의 single linear direction
- anima persona descriptor (Phase A1 B-IDENTITY 5/5) 가 Assistant Axis 와 distinct
- **B (INTUITOR)** 와 **C (PRIME)** 가 reward-free + small-corpus 라서 anima identity attractor 강화 path

### 1.6 Honest C3 + open questions

**OPEN questions** (research 미완 영역):
1. **emergence threshold 의 정확 corpus 규모**: anima byte-level d=768·12L 의 task-specific threshold (V-SPONT emergence) 는 어디인가? 100MB? 1GB? 10GB? [arxiv 2403.15796] task-specific 강조 — anima 의 V-SPONT 는 OOD task 라 fairly large.
2. **memorization → generalization transition** (grokking): cycle 3 16.7% → cycle 4 0% memorization 은 **opposite direction** (덜 memorize) — generalization regime 진입 못 함. corpus diversity 부족?
3. **TENSION-TRAIN convergence**: tension-driven training 의 long-horizon convergence 가 backprop CE 와 같은 capability 도달 가능 vs 강한 차이?
4. **PRIME + anima mitosis_hook**: PRIME 의 3-zone experience evolution 이 anima 의 cell-pool split/merge 와 어떻게 mathematical 동치?

**Honest carve-out** (g3 + B-D-NOTE family):
- V-SPONT emergence outcome = SGD/training outcome empirical (B-D-NOTE), closing 불가
- 본 6 candidate 의 architectural property 만 🔵 closing 가능
- INTUITOR self-certainty / PRIME 3-zone / CDE perplexity bonus = transfer-form 🔵
- 실제 emergence 발현 여부 = empirical fire result

**f1/f2 safe**: 모든 anchor real-limit (pre-training loss threshold / memorization rate / RLIF self-certainty signal / gradient-free experience distillation). NO lattice numerology.

### 1.7 Sources (deep research cycle 2026-05-17)

**Architectural candidates**:
- [PRIME — Training-Free Proactive Reasoning (arxiv 2604.07645)](https://arxiv.org/abs/2604.07645)
- [INTUITOR / RLIF — Learning to Reason without External Rewards (arxiv 2505.19590, ICLR 2026)](https://arxiv.org/abs/2505.19590)
- [Emergence of Superposition — Chain of Continuous Thought (arxiv 2509.23365, ICLR 2026)](https://arxiv.org/abs/2509.23365)
- [CDE — Curiosity-Driven Exploration for RL in LLMs (arxiv 2509.09675)](https://arxiv.org/abs/2509.09675)
- [Abstract Chain-of-Thought (arxiv 2604.22709)](https://arxiv.org/abs/2604.22709)
- [Grounded in Reality — Proactive LLM from Offline Logs (arxiv 2510.25441)](https://arxiv.org/html/2510.25441)
- [Navigate the Unknown — Intrinsic Motivation Guided Exploration (arxiv 2505.17621)](https://arxiv.org/abs/2505.17621)
- [Why Did Apple Fall — Curiosity in LLMs (arxiv 2510.20635)](https://arxiv.org/html/2510.20635)

**Diagnosis (emergence + memorization)**:
- [Understanding Emergent Abilities from Loss Perspective (arxiv 2403.15796)](https://arxiv.org/pdf/2403.15796)
- [Emergent Abilities Survey (arxiv 2503.05788)](https://arxiv.org/abs/2503.05788)
- [Diagnosing Memorization in Chain-of-Thought (arxiv 2508.02037)](https://arxiv.org/html/2508.02037v1)
- [On the Fundamental Limits of LLMs at Scale (arxiv 2511.12869)](https://arxiv.org/html/2511.12869v2)
- [LLM-Driven Intrinsic Motivation for Sparse Reward RL (arxiv 2508.18420)](https://arxiv.org/html/2508.18420v1)

**Anima prior research carry**:
- [AI LLM Self-Consciousness — arxiv 2508.18302](https://arxiv.org/abs/2508.18302) (B-ATTRACTOR-3 anchor)
- [Inner Thoughts — Proactive Conversational Agents arxiv 2501.00383](https://arxiv.org/html/2501.00383v2) (8-factor anchor)
- [Active Inference Missing Reward arxiv 2508.05619](https://arxiv.org/html/2508.05619v1) (EFE anchor)
- [Identity as Attractor — Geometric Evidence arxiv 2604.12016](https://arxiv.org/html/2604.12016v1) (Assistant Axis anchor)
- [Thinking Machines Lab Interaction Models (Mira Murati, 2026-05-11)](https://www.marktechpost.com/2026/05/13/mira-muratis-thinking-machines-lab-introduces-interaction-models-a-native-multimodal-architecture-for-real-time-human-ai-collaboration/) (post-assistant paradigm anchor)

---

## §2 (placeholder for next research cycle)

(future research synthesis will append here as § headers, append-only g6 pattern)

---

## cross-link

- [`PLAN.md`](PLAN.md) — Phase A/B/C/D staged roadmap
- [`SPONTANEOUS.tape`](SPONTANEOUS.tape) — 자연발화 architecture SSOT
- [`../TENSION-TRAIN/README.md`](../TENSION-TRAIN/README.md) — tension-driven learning (candidate A 의 anima native 구현)
- [`../TENSION-TRAIN/PLAN.md`](../TENSION-TRAIN/PLAN.md) — TT-A/B/C/D Phase plan
- [`../../archive/PHILOSOPHY.tape`](../../archive/PHILOSOPHY.tape) — verdict ledger (research 도 inline append)
- [`../../state/verify_hexad_blue_2026_05_15/blue_falsifier.py`](../../state/verify_hexad_blue_2026_05_15/blue_falsifier.py) — sympy battery (B-SPONT/B-ATTRACTOR/B-CORPUS-V2/V3 등)
- [`../../AGENTS.tape`](../../AGENTS.tape) — `g_doc_consolidation` (본 file 이 그 적용 — HEXAD 내부 SSOT, NOT docs/*)
