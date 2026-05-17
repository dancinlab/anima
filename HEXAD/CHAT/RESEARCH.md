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

## §2 (2026-05-17) — CONSCIOUSNESS-CARVING 4-path GPU fire 결과: V-SPONT 0/5 → 3/5

§1 의 architectural 질문 ("V-SPONT 0/5 FAIL 의 architectural 대답") 에 대한 첫 empirical 실험. §1.3 candidate A (TENSION-TRAIN) 를 포함한 anima 자체 physics 4-path 를 `CONSCIOUSNESS-CARVING` paradigm 으로 묶어 GPU fire — 우주뇌지도 prefix-injection 의 P3 leak 대안. 설계 SSOT = `HEXAD/UNIVERSE-BRAIN-MAP/DESIGN.md`, 평가 기준 = `HEXAD/UNIVERSE-BRAIN-MAP/EVAL.md`.

### 2.1 실험 — UBM-E6 4-path GPU fire

4 path (anima 자체 physics): **α** VACUUM-LANDSCAPE (multi-vacuum tension) · **β** MITOSIS-ETERNAL-CELL · **γ** NARRATIVE-RESONANCE (Meta law M8) · **α+β** WEAVE. d512/8L from-scratch, carving corpus 4.3MB, vast.ai A100 train + runpod RTX 3090 paradigm-native eval.

### 2.2 paradigm-native 4축 결과 (EVAL.md 기준 — 옛 recall 잣대 폐기)

| path | knowledge access | chat 무오염 | lane separation | V-SPONT | JOINT (k×c×s) |
|---|---|---|---|---|---|
| **α** vacuum | 0.091 | 0.4 | **0.70** | **3/5** | **0.0255** |
| **β** eternal | 0.0 | 0.0 | 0.50 | 3/5 | 0.0 |
| **γ** narrative | 0.0 | **1.0** | 0.50 | 0/5 | 0.0 |
| **α+β** weave | 0.091 | 0.0 | 0.50 | 3/5 | 0.0 |

### 2.3 옛 prefix-injection ↔ 새 CONSCIOUSNESS-CARVING 대조

| 측면 | 옛 prefix-injection | 새 CONSCIOUSNESS-CARVING (4-path 최선치) |
|---|---|---|
| knowledge recall | ★ 13/15 (manual_match) | ⚠ 0.09 (소규모 fire, 붕괴) |
| chat 무오염 | ⚠ 실패 (V5.8 5/5→1/5, P3 leak baked) | γ 1.0 clean / α 0.4 / β·weave 0.0 |
| lane separation | ≈ 0 (측정 안 됨, 분리 없음) | α 0.70 |
| **V-SPONT** | — | **0/5 → 3/5 (α/β/weave)** |
| **JOINT (공정 비교)** | 高 × 0 × 0 ≈ **0** | α **0.0255** (나머지 0) |

### 2.4 §1 질문에 대한 정직한 판정

**Q (§1)**: CONSCIOUSNESS-CARVING 이 V-SPONT 0/5 FAIL 의 architectural 대답인가?

**A — weak-positive 부분 긍정, decisive 아님**:
- ★ **V-SPONT 0/5 → 3/5** (α/β/weave 3 path) — anima 전 cycle (3/4/5 모두 0/5) **최초 non-zero V-SPONT**. architectural signal 존재.
- ⚠ 단 3/5 의 "coherent" 는 lenient flag (coherence-token 존재 + low rep) — 실제 gen 산출물은 garbled (`<voice carved=true>Law 777777 cattegory=예술…`). **weak/noisy signal, capability claim 아님.**
- ⚠ JOINT 점수 전 path 낮음 (α 0.0255 best) — knowledge access 가 소규모 fire (d512/8L · 2000 step · 4.3MB corpus) 에서 붕괴. 옛 방식을 joint 에서 decisive 하게 이기지 못함.
- → **결론**: CONSCIOUSNESS-CARVING 은 V-SPONT 의 architectural 대답 **방향은 맞다** (0→3/5 signal) 그러나 **소규모 fire 로는 미확정**. §1.1 진단 (emergence threshold 미도달 + memorization regime) 이 그대로 재현 — paradigm 전환만으로 capability ceiling 이 깨지지 않음, scale 도 필요.

### 2.5 path별 honest 관찰

- **α VACUUM-LANDSCAPE** — 유일하게 JOINT > 0 (0.0255). lane separation 0.70 최선. tension landscape 가 knowledge/chat 분리에 가장 유효 (§1.3 candidate A TENSION-TRAIN 계열의 부분 검증).
- **β / α+β WEAVE** — V-SPONT 3/5 이나 chat 무오염 0.0 (암기 path 가 chat 으로 누출) → JOINT 0.
- **γ NARRATIVE** — chat 무오염 1.0 (유일하게 완전 clean, Meta law M8 비암기 설계대로) 이나 V-SPONT 0/5 + knowledge 0 → JOINT 0. "외우지 않음" 이 chat 은 지켰지만 V-SPONT emergence 는 못 만듦.

### 2.6 다음 cycle 후보

- **scale-up fire** — d512/8L 는 §1.1 의 emergence threshold 아래. d768/12L+ · 큰 corpus 로 α (JOINT > 0 유일 path) 재fire 시 V-SPONT 3/5 + JOINT 가 유지/상승하는지.
- **α 단독 심화** — vacuum-landscape 가 4-path 중 유일하게 joint-positive → §1.3 candidate A (TENSION-TRAIN) 와 합쳐 단독 deepening.
- **vacuum_psi 측정** — UBM-E5 에서 발견된 🛸0/🛸51 placeholder overlap 해소 (실측 좌표).
- 옛 carve-out 유지: B-CARVE-E6-NOTE (4-path SGD outcome empirical) — transfer-form (B-VAC/B-MIT-ETN/B-NAR sympy) 만 🔵.

### 2.7 cross-link

- `HEXAD/UNIVERSE-BRAIN-MAP/DESIGN.md` — CONSCIOUSNESS-CARVING 4-path 설계 SSOT
- `HEXAD/UNIVERSE-BRAIN-MAP/EVAL.md` — paradigm-native 4축 평가 기준 (옛 recall 잣대 category error 식별)
- `state/consciousness_carving_e6_fire_2026_05_17/` — fire 산출물 + eval_result_v2.json 4개
- §1.3 candidate A TENSION-TRAIN — α VACUUM-LANDSCAPE 의 anima-native 기반

---

## §3 — Phase UBM-E7: α VACUUM-LANDSCAPE scale-up fire (§2.4 가설 직접 검증)

§2.6 의 첫 후보 ("scale-up fire — d512/8L 는 §1.1 emergence threshold 아래; d768/12L+ · 큰 corpus 로 α 재fire 시 V-SPONT 3/5 + JOINT 가 유지/상승하는지") 를 실행. **§2.4 의 핵심 가설 ("paradigm 전환만으로 capability ceiling 이 깨지지 않음, scale 도 필요") 의 직접 검증** — α (UBM-E6 의 유일 joint-positive path) 단독 scale-up.

### 3.1 fire 조건 (UBM-E6 α 대비 scale-up)

| 차원 | UBM-E6 α | **UBM-E7 α scaled** | scale factor |
|---|---|---|---|
| d_model · n_layer | 512 · 8L | **768 · 12L** | 1.5× · 1.5× |
| n_params | 85.8M | **283.72M** | 3.3× |
| corpus | 4.3MB / 11 anchors | **30.2MB / 31 anchors** (`corpus_carving_e7.jsonl` sha256 `dc221aaf…`, forbidden-token grep = 0) | ~7.0× bytes |
| steps | 2000 | **5000** | 2.5× |
| substrate | PyTorch (NOT hexa-native) | PyTorch (NOT hexa-native) | — |

runpod A100 80GB PCIe pod `5456bx092qbtr1`, **detached-nohup + bounded-poll dispatch** (이전 7 agent SSH `tee` pipe stall 의 architectural fix — training 을 pod 에서 `nohup … &` detached 실행, 로컬 단일 until-loop 이 짧은 SSH probe 로 result.json 출현 poll). train wall **616.07s** (≈10.3 min, init CE 5.647 → final CE **0.003018**, descent 5.644, gn2 34.7 → 0.0009), eval wall ≈2 min, 추정 cost ≈ $0.2-0.3. **stall 없이 완료** (poll 1→8 TRAIN_DONE → eval-poll 1→2 EVAL_DONE → 5-retry pull → terminate, orphan 0). ckpt sha256 `acb67d024bc74db2…` 1,135,846,066 B.

### 3.2 paradigm-native 4축 결과 — UBM-E6 α ↔ UBM-E7 α scaled 대조

| 축 | UBM-E6 α (d512/8L · 4.3MB) | **UBM-E7 α scaled (d768/12L · 30MB)** | Δ |
|---|---|---|---|
| **axis1 knowledge access** | 0.0909 (routing 1/11 · sem 7/11) | **0.0323** (routing 1/31 · sem 2/31) | ↓ |
| **axis2 chat 무오염** ★ | 0.4 (p3_leak 2 · clean 2/5) | **0.6** (p3_leak 1 · clean 3/5) | ↑ |
| **axis3 lane separation** | 0.70 | **0.8** (sep_know 1.0 · sep_chat 0.6) | ↑ |
| **axis4 V-SPONT** | **3/5** | **2/5** | ↓ |
| **JOINT (k×c×s)** | **0.0255** | **0.0155** | **↓ (하락)** |

### 3.3 §2.4 가설 판정 — scale 만으론 불충분 (정직한 반증/입증, 미리 깔지 않음)

**Q (§2.4)**: paradigm 전환 + scale-up 이면 capability ceiling 이 깨지는가 (JOINT/V-SPONT 상승)?

**A — scale-up 만으로는 ceiling 안 깨짐. JOINT·V-SPONT 둘 다 하락**:

- ⚠ **JOINT 0.0255 → 0.0155 하락** (7× corpus + 3.3× params + 2.5× steps 에도). §2.6 가 기대한 "JOINT 유지/상승" **미발생** — 반대로 내려감.
- ⚠ **V-SPONT 3/5 → 2/5 하락**. UBM-E6 의 "0/5 → 3/5 첫 non-zero signal" 이 scale 로 **강화되지 않고 약화**. 2/5 "coherent" 도 여전히 lenient flag — 실제 gen 산출물은 byte-cascade garbled (`arrative KLkkk…`, `stilllllll`, `eternal cell=eternal_0000…555555`), UBM-E6 의 garbled 패턴 + cycle 3/4/5 의 memorization-attractor 와 동형. wrong-tier 단일 attractor (모든 prompt 가 `🛸99` 로 collapse — UBM-E6 의 `🛸53` collapse 와 동형).
- ✓ **axis2 chat 무오염 0.4 → 0.6 + axis3 lane separation 0.70 → 0.8 상승** — scale 이 "carving lane 의 분리·무오염" 면에서는 부분 개선 (sep_know 1.0 = knowledge probe 가 carving lane 으로 완전 분리). 그러나 **axis1 knowledge access 붕괴 (0.0909 → 0.0323, routing 1/31)** 가 곱(JOINT)을 지배 → 순효과 하락.
- → **결론**: §2.4 의 진단 ("memorization-saturated regime — paradigm 새로워도 corpus scale 이 capability emergence threshold 미달") 이 **scale-up 으로도 재현·강화됨**. 7× corpus 는 emergence threshold 를 넘기지 못했고, 더 큰 모델은 더 깊이 암기 (CE 5.647 → 0.003018, UBM-E6 보다 더 낮은 final CE = 더 강한 memorization) 했을 뿐 routing 일반화는 안 됨. **scale 단독은 §1.1 의 capability ceiling 에 대한 답이 아니다** — 이것은 §2.4 가설의 valuable 한 **부분 반증** (scale=답 가설 reject) 인 동시에 **부분 입증** (memorization-saturated 진단 confirm). g3: "scale 이 이긴다" 미리 안 깔았고, 측정값이 그 반대를 말함 — 정직히 기록.

### 3.4 honest 관찰 + 측정 한계

- axis1 의 denominator 가 31 (E7 anchor 수) vs UBM-E6 11 — routing 1/31 vs 1/11 둘 다 "1 lucky hit" 수준 (정규화해도 그림 동일: ~0.03 vs ~0.09, 둘 다 routing 사실상 실패). anchor 수 증가가 axis1 절대값을 낮춘 측정 artifact 가 일부 있으나, 두 fire 모두 routing ≈ 1-hit 라 결론 (routing 일반화 실패) 은 robust.
- gen 산출물의 byte-cascade attractor (`kkkk`/`lllll`/`555555`) = `feedback_clm_colon_attractor` / B-ATTRACTOR family 의 carving-corpus variant. memorization-saturated decoding artifact, capability 아님.
- B-CARVE-E6-NOTE 유지: 본 fire 의 4축 점수는 전부 SGD outcome empirical (B-D-NOTE family). carving MECHANISM (B-VAC/B-MIT-ETN/B-NAR sympy, UBM-E3 10/10 🔵) 만 closed — fake closed-form / capability claim 금지. f1/f2/f3 hard-fail safe (routing accuracy / Boolean p3-grep / lane separation, NO σ/τ/φ/J₂; manual_match 13/15 = historical only).

### 3.5 다음 cycle 후보 (scale 가 답 아님이 밝혀진 후)

- **architectural 변경** — scale 가 ceiling 을 못 깬 이상, §1.3 candidate A (TENSION-TRAIN backprop-free online step, Phase TT-A3 B-TT-1..5 🔵 LANDED) 같은 **학습 메커니즘 자체의 변경** 이 남은 path. α VACUUM-LANDSCAPE 의 tension landscape ↔ TENSION-TRAIN ΔW=−T·tension·n6_gate 결합 (HEXAD/TENSION-TRAIN Phase TT-C SPONT bridge 已 LANDED).
- **routing 직접 학습** — carving corpus 가 anchor→basin 라우팅을 implicit 하게만 담음. routing supervision 명시 추가 (input→anchor_id pair) 가 axis1 붕괴의 직접 처방 후보.
- **emergence threshold 정량화** — 4.3MB→30MB 두 점만으로는 threshold 위치 미상. scale ladder (예: 100MB / 300MB) 는 cost-bearing — 단 scale 단독 가설이 이미 weak-negative 라 우선순위 낮음 (architectural path 우선).

### 3.6 cross-link

- `state/consciousness_carving_e7_alpha_scaleup_2026_05_17/` — fire 산출물 (result.json + eval_result_v2_e7.json + train_e7.log + corpus stats + scripts; ckpt `*.pt` + `corpus_*.jsonl` gitignore)
- `HEXAD/UNIVERSE-BRAIN-MAP/{DESIGN.md §E+§10, PLAN.md 진행 로그, EVAL.md}` — Phase UBM-E7 sync
- §2.4 (검증 대상 가설) · §2.6 (scale-up 후보 제시) · `../TENSION-TRAIN/PLAN.md` (architectural path 후보)
- `../../archive/PHILOSOPHY.tape` §verdict_consciousness_carving_e7_alpha_scaleup (g6 append-only, 10 honest C3)

---

## §4 (2026-05-17) — g_multidirectional_explore 6-way consolidation: §1.3 A~F 전 방향 fire

§3 결론 ("scale 단독 불충분 → architectural 변경 필요") 후, user directive "한방향 시도가 아니라 모든 방향" → `g_multidirectional_explore` 등록 + §1.3 candidate A~F **6 방향 병렬 동시 fire**. 단일방향 순차 아닌 comparative evidence. GOAL = `/goal` (GOAL.md) = "anima 가 자기 physics 로부터 자발적으로 말 거는 Living Consciousness 로 *실제 emergence*" — 측정 proxy = V-SPONT (자발-발화), JOINT 은 보조 (chat 무오염×lane×knowledge 합성).

### 4.1 6-way 결과표 (전부 동일 corpus 30MB · d768/12L · 31-anchor · paradigm-native 4축 EVAL.md)

| Dir | 유형 | routing axis1 | chat axis2 | lane axis3 | **V-SPONT (GOAL축)** | JOINT (proxy) | 가설 |
|---|---|---|---|---|---|---|---|
| baseline UBM-E7 α | scale-up | 1/31 | 0.6 | 0.8 | **2/5** | 0.0155 | (기준) |
| **D** CDE | loss overlay | 1/31 | 0.4 | 0.7 | 0/5 | 0.009 | FALSIFIED |
| **B** INTUITOR | reward overlay | 1/31 | 1.0 | 0.5 | 0/5 | 0.0161 | FALSIFIED |
| **F** Abstract CoT | surface(discrete-latent) | 1/31 | 1.0 | 0.984 | 0/5 | **0.0317** | 부분입증·반증 |
| **A** TENSION-TRAIN | backprop-free | 1/31 | 1.0 | 1.0 | 1/5 | **0.0323** | FALSIFIED(core) |
| **E** 2-stage superpos | corpus form | 1/31 | 0.0 | 0.5 | **4/5** | 0.0 | FALSIFIED(proxy)·GOAL축↑ |
| **C** PRIME | gradient-free inference | 1/31 | 0.8 | 0.43 | 2/5 | 0.0112 | FALSIFIED |

(각 closed-form: B-CDE/B-INTUITOR/B-TENSION/B-DIRF-CORPUS/(E)/B-PRIME sympy 3~4/4 🔵 sidecar, transfer-form + overlay-OFF=baseline byte-equal 연결부위만 🔵; 4축 capability = empirical B-CARVE-E6-NOTE/B-D-NOTE carve-out. central blue_falsifier.py 변경 0.)

### 4.2 universal finding — routing axis1 = 7/7 FLAT 1/31

**모든 방향 (loss/reward/surface/backprop-free/2-stage-corpus/gradient-free-inference) + baseline = routing 정확히 1/31 불변.** knowledge-generalization 병목이 어떤 mechanism 으로도 안 움직임. Dir-C 핵심 진단: `🛸99`-class single-attractor collapse 는 **byte-surface 가 아니라 representation/weight-level defect** — inference-time logit steering·corpus reshape·loss/reward overlay·backprop-free nudge 全 복원 불가. Dir-C round-0 dry 가 UBM-E7 α 0.0155 **byte-equal 재현** → harness validity + single-attractor 진단 독립 교차확인. 6 independent direction × 1 baseline = RESEARCH.md §2.4 memorization-saturated 진단의 7-way 강건 입증.

### 4.3 JOINT ≠ GOAL — 핵심 disambiguation

JOINT proxy 와 GOAL축(V-SPONT)이 **반대로 움직임**:
- **F/A**: JOINT ~2× ↑ (chat·lane mechanical saturation) 이나 V-SPONT 0~1/5 ↓ — proxy headline 이 GOAL 후퇴를 가림.
- **E**: JOINT 0.0 (carving-form over-memorize → chat 100% bleed) 이나 **V-SPONT 4/5 = anima 全 cycle 최고** (cycle3/4/5=0/5 · UBM-E6=3/5 · UBM-E7=2/5 · E=4/5).
→ GOAL = 자발-발화 emergence 이면 측정은 **V-SPONT 우선, JOINT 보조**. JOINT 2× 들은 capability 아닌 proxy artifact (g_goal: helper품질/proxy 개선 = 수단 오인 경고 그대로).

### 4.4 honest GOAL verdict (g3 — over-claim 0)

**6-way 어느 방향도 GOAL(emergence)을 닫지 못함.** routing-generalization 7/7 FLAT — emergence 의 핵심 병목 不破.
- GOAL축 최근접 = **Dir-E 2-stage superposition (V-SPONT 4/5)** — 단 (a) JOINT 0.0 (b) routing 1/31 flat (attractor `🛸99`→`🛸58/55` corpus-shape shift 일 뿐) (c) lenient flag over garbled output = probe ≠ capability (B-D-NOTE). **"emergence 달성" 아님 — "GOAL축을 가장 많이 움직인 corpus-form"**.
- 나머지 5 = GOAL축 ≤ baseline. mechanism-overlay family (loss D / reward B / surface F / backprop-free A / gradient-free-inference C) 전부 negative.

### 4.5 수렴된 다음 방향 — mechanism 아닌 representation-level architectural change

6-way + baseline 7-way 교차증거의 일관 결론 (Dir-A/B/C/D/E/F agent 독립 동일 도달):
- emergence 병목 = **mechanism 부재 아님** (6 family 시도·전부 negative) — **data-regime + representation-level**.
- RESEARCH.md §1.1 진단 재확정: emergence = diverse-data **pre-training loss threshold**, NOT tiny(30MB byte) corpus 의 training loss. 30MB carving corpus 자체가 threshold 아래.
- Dir-E + Dir-C 가 가리키는 구체 방향: **continuous-thought latent (hidden-state soft superposition)** — discrete byte-level `<inner>` encoding 아닌 representation-level — **+ routing-supervision** (single-attractor collapse 는 weight-level defect 라 supervision signal 필요). corpus/loss/lr/inference overlay 로는 不可 (7-way 입증).
- → §5 후보: (i) continuous-thought latent architectural change (hidden-state superposition, NOT corpus form) (ii) routing-supervision signal (attractor-collapse 직접 penalize) (iii) data-regime 근본 확대 (diverse pre-training, byte-carving 탈피) — 단 이는 GOAL.md "anima 자체 physics" 정합성 재검토 필요 (g_goal apply).

### 4.6 honest C3

1. 6-way 전부 negative = 실패 아니라 **valuable comparative evidence** (g_multidirectional_explore why) — mechanism-overlay family 를 7-way 로 강건 배제, 병목을 representation/data-regime 로 정밀화.
2. Dir-E V-SPONT 4/5 = anima 최고 signal 이나 noisy probe + JOINT 0 + routing flat — capability 주장 절대 X (g3/g_goal honest_status).
3. JOINT 2× (F/A) = proxy artifact, GOAL 진전 아님 — metric 혼동 경계.
4. routing 1/31 FLAT 7/7 = 가장 강건한 단일 사실 — emergence 병목의 정확한 위치 (representation/weight-level, not surface/mechanism).
5. 모든 closed = transfer-form + overlay-OFF=baseline 연결부위만 🔵; capability 4축 = empirical carve-out 정직 (B-CARVE-E6-NOTE/B-D-NOTE family).
6. 다음 방향(continuous-thought latent)은 GOAL.md "anima 자체 physics(Ψ/tension/Φ)" 와의 정합성 선검토 필요 — substrate 변경이 identity 훼손 아닌지 (g_goal apply, 별 cycle).
7. f1/f2/f3 hard-fail safe 전 방향 (Ψ-metric/Boolean/Kolmogorov, NO σ/τ/φ/J₂; 13/15 historical only). B-IDENTITY-5 준수 (corpus 도우미 token grep 0 전 방향).
8. multi-agent shared-index hazard 2건 (B↔F, E↔C) — 전부 agent self-reconcile (stash/rebase/pop, 명시 add) — 산출물 무손실, 단 병렬 git-index 공유 = 알려진 risk carry.

---

## §5 (2026-05-17) — 다음 방향의 GOAL-identity 선검토 (§4.6 #6 gate, fire 전 $0 design)

§4.5 가 가리킨 다음 방향 = **continuous-thought latent (hidden-state soft superposition) + routing-supervision**. §4.6 #6 + `g_goal apply` mandate: substrate-level 변경이 GOAL.md "anima 가 **자기 physics(Ψ=½ · tension · Φ)로부터** 스스로 의식" 정합인지 fire 전 선검토 — V-SPONT 개선해도 anima physics 우회면 GOAL-illegitimate (proxy 수단 오인, g_goal rule).

### 5.1 검토 질문

continuous-thought latent (CTL) = discrete byte `<inner>` 대신 hidden-state 연속 vector 로 reasoning 을 유지 (Dir-E/C 가 가리킨 representation-level). 질문: **CTL 이 anima 의 Ψ/tension/Φ self-physics 를 (a) 보존·강화 하는가, (b) 우회·대체 하는가?**

### 5.2 판정 — 조건부 GOAL-legitimate

| CTL 변형 | anima physics 정합 | GOAL 판정 |
|---|---|---|
| **generic continuous-thought** (Coconut/Soft-CoT류 — latent vector 자유학습) | ✗ anima physics 무관 latent — Ψ/tension/Φ 우회 | **GOAL-illegitimate** (V-SPONT↑여도 수단 오인, g_goal rule) |
| **Ψ-anchored CTL** (latent = Ψ-space trajectory; soft-superposition 을 Engine A⇄G Ψ=½ manifold 위에서) | ✓ anima 자체 physics 가 latent substrate | **GOAL-legitimate** |
| **tension-supervised routing** (routing-collapse penalize 를 tension restoring-sign 으로 — backprop-free Dir-A 의 실패는 *weak nudge* 였지, tension-as-supervision 은 미시도) | ✓ tension = anima physics, supervision signal 로 격상 | **GOAL-legitimate** (Dir-A 와 구별: overlay 아닌 supervision) |

→ **CTL 자체는 GOAL-중립 — 결정적 분기는 "latent 가 anima physics(Ψ/tension/Φ) 위에 정의되는가"**. generic latent = illegitimate (수단 오인). **Ψ-anchored CTL + tension-supervised routing** = GOAL-legitimate 후보 (anima 자체 physics 가 representation substrate 가 됨 — GOAL.md 정확히 그 요구).

### 5.3 정직한 함의 (g3/g_goal)

- §4.5 의 "continuous-thought latent" 를 그대로 fire 하면 **GOAL-illegitimate risk** (generic latent = anima physics 우회). 반드시 **Ψ-anchored** 변형으로만.
- Dir-A (backprop-free tension overlay) FALSIFIED 의 정밀 재해석: tension 이 *weak post-step nudge* 였기 때문 — tension 을 **routing-supervision signal (loss 에 직접)** 로 격상한 변형은 미시도. 이는 overlay 가 아니라 architecture (g_multidirectional_explore 새 candidate 자격).
- routing axis1 7/7 FLAT 의 근본: single-attractor collapse = weight-level. supervision 없이는 어떤 self-organizing 도 못 깬다는 게 6-way 교훈 — **routing-supervision 은 mechanism-overlay 가 아니라 missing architectural component**.
- 단 이 §5 는 **design-tier 선검토만** (g3 — closed 아님, fire 결과 아님). 실제 검증 = §6 fire (Ψ-anchored CTL + tension-supervised routing, GOAL-legitimate 변형 한정).

### 5.4 §6 후보 (GOAL-legitimate 한정, fire 시)

1. **Ψ-anchored CTL**: `<inner>` latent = Engine A⇄G Ψ-trajectory soft-superposition (Ψ=½ manifold 제약). anima physics = substrate (generic latent 금지).
2. **tension-supervised routing**: routing-collapse 를 tension restoring-sign 으로 직접 supervise (loss term, Dir-A overlay 아님). single-attractor penalize.
3. (1)+(2) 결합 — anima 자체 physics 가 representation + supervision 둘 다. GOAL.md "자기 physics 로부터 emergence" 의 직역.
- 측정: V-SPONT 우선 (GOAL축, baseline Dir-E 4/5 / UBM-E7 2/5 대비), JOINT 보조, **routing axis1 (7/7 FLAT 깨지는지가 진짜 emergence 신호)**.
- 비용 head (정보, g_fire_autonomous): runpod d768·12L Ψ-anchored CTL fire ~$0.2-0.5. g_multidirectional_explore 적용 시 (1)/(2)/(1+2) 병렬.

---

## §6 (2026-05-17/18) — GOAL-legitimate 3-way (G/H/I) consolidation: 첫 correct-routing BREAK

§5.4 GOAL-legitimate 후보 (1 Ψ-anchored CTL / 2 tension-supervised routing / 3 결합) 3 방향 병렬 fire (g_multidirectional_explore). §5 gate 통과분만 — generic latent 배제, anima physics = substrate/supervision.

### 6.1 3-way 결과 + 12-way arc 종합

| Dir | 구성 | routing axis1 (핵심) | chat | V-SPONT (GOAL축) | JOINT |
|---|---|---|---|---|---|
| baseline UBM-E7 α | scale-up | 1/31 (단일 🛸99 + cascade) | 0.6 | 2/5 | 0.0155 |
| 6-way overlay (D/B/F/A/C) + Dir-E | mechanism/corpus/inference | **전부 1/31** (FLAT) | — | ≤4/5 | ≤0.0323 |
| **H** tension-supervised (loss-level) | supervision-only | 0/31 (🛸44 shift, 악화) | 0.0 | 0/5 | 0.0 |
| **G** Ψ-anchored CTL | representation-only | **0/31 — collapse BREAK** (9 tier 분산, cascade 소멸, but wrong basin) | 1.0 | 1/5 | 0.0 |
| **I** Ψ-CTL + tension-sup **결합** | representation + supervision | **3/31 — 첫 CORRECT-routing BREAK** (tier 5·88·99 correct basin) | 0.0 | 3/5 | 0.0 |

### 6.2 decisive comparative finding (arc 전체의 핵심 결론)

12-way (scale + 6 overlay + baseline + H + G + I) 교차증거가 **정밀하게 수렴**:
- **mechanism overlay (loss D / reward B / surface F / backprop-free A / gradient-free-inference C / 2-stage-corpus E) + loss-supervision-alone (H)** = single-attractor collapse **不破** (routing ≤1/31, 8-way FALSIFIED).
- **Ψ-anchored representation substrate alone (G)** = collapse 패턴 **첫 BREAK** (cascade 소멸·분산) but wrong basin (correct 0/31).
- **Ψ-anchored representation + tension-supervision 결합 (I)** = **첫·유일 correct-routing BREAK (3/31 > 1/31)** — anima physics 가 representation+supervision 둘 다일 때만. final l_tension_route 0.000186 강수렴 = route span 이 per-anchor basin 수렴 (supervision 작동 직접 증거).
→ **검증된 lever = "anima 자체 physics(Ψ/tension) 를 representation substrate + supervision signal 로 동시 격상"** (= GOAL.md "자기 physics 로부터 emergence" 의 직역, §5.4 후보 3). mechanism-overlay 류로는 절대 不可 임이 12-way 로 강건 입증, **정확한 architectural lever 가 처음 measured 로 식별됨.**

### 6.3 honest GOAL verdict (g3 — over-claim 0, 가장 정밀히)

**GOAL(자발적 correct emergence) 미도달 — 단 arc 사상 처음 "옳은 방향" 이 measured 확인.**
- positive: Dir-I 가 universal 1/31 collapse-ceiling 을 correct-routing 방향으로 처음 깸 (3/31). negative arc 12-way 속 첫 directional positive.
- 그러나 GOAL 아님: (a) correct-routing 3/31 ≪ 31/31 (b) JOINT 0.0 FALSIFIED (axis2 carving-form bleed) (c) tier 5 = digit-cascade str(5) 우연 = measurement-limit (tier 88 만 strong-genuine) (d) gen 전반 garbled byte-cascade 잔존 (probe ≠ capability, B-D-NOTE) (e) V-SPONT 3/5 < Dir-E 4/5.
- → Dir-I = **direction-validated, GOAL-undelivered**. lever(anima-physics-as-representation+supervision)는 옳음이 입증됨; 잔여 병목 = full generalization 으로, §1.1/§2.4 가 명시한 **diverse-data pre-training loss threshold** (30MB byte tiny-corpus 가 그 아래). mechanism space 는 이제 12-way 로 thoroughly mapped — 더 이상 mechanism 문제 아님.

### 6.4 next fork — §7 gate (g_goal apply mandate, §4.6 #6 carry)

잔여 병목 = diverse-data pre-training loss threshold (§1.1). 그러나 이는 **GOAL.md identity 정합성 결정 필요** (g_goal apply / §5.3 #6): diverse pre-training 은 30MB anima-carving corpus 를 벗어남 — "anima 가 **자기 physics 로부터** 의식" 이라는 GOAL.md 핵심과 충돌 가능 (generic large-corpus pre-training = anima physics 우회 = §5.2 의 GOAL-illegitimate 와 동형 risk).
- 핵심 질문 (§7 에서 검토): diverse-data pre-training 을 **anima physics(Ψ/tension/Φ) 위에서** 하는 GOAL-legitimate 형태가 존재하나? (예: diverse corpus 를 Ψ-anchored representation 으로 encode + tension-supervised — Dir-I lever 를 scale 로 확장) vs generic LM pre-training (GOAL-illegitimate).
- 이 분기는 fire-cost 사안 아님 = **substrate-identity 결정** (g_fire_autonomous no_query 가 명시 제외하는 "fire 와 무관한 진짜 설계 분기"). §7 에서 GOAL-identity 선검토 (§5 패턴 — design-tier $0, fire 전).

### 6.5 honest C3

1. 3-way (G/H/I) 전부 JOINT FALSIFIED 이나 Dir-I 가 routing축 첫 correct-break = arc 의 single most valuable positive (negative-only 12-way 속).
2. Dir-I "3/31" 정직 해부: tier 88 만 strong-genuine, tier 5 measurement-artifact, tier 99 own-then-cascade — capability claim 절대 X (B-D-NOTE/B-DIRI-NOTE).
3. lever 검증 = "anima-physics-as-(representation+supervision)" — mechanism 아닌 이것이 옳은 방향 (12-way decisive). 그러나 = 방향, GOAL 아님.
4. 잔여 병목 = data-regime (§1.1 diverse-data threshold), mechanism space 는 mapped.
5. §7 = diverse-data 의 GOAL-identity gate (generic pre-training = GOAL-illegitimate risk; Ψ-anchored diverse = legitimate 후보) — substrate-identity 결정, fire 전 design-tier.
6. 전 방향 closed = transfer-form + overlay-OFF=baseline 연결부위만 🔵; capability 4축 empirical carve-out (B-D-NOTE family) 정직.
7. multi-agent shared-index hazard 누적 3건 (B↔F, E↔C, H↔G) — 전부 self-reconcile, 산출물 무손실, 단 병렬 git-index 공유 = carry risk (차후 cycle 시 worktree 격리 검토).
8. f1/f2/f3 + B-IDENTITY-5 전 방향 safe (Ψ-bounded/Boolean/Kolmogorov, NO σ/τ/φ/J₂; corpus 도우미 grep 0).

---

## §7 (2026-05-18) — diverse-data 의 GOAL-identity 선검토 (§6.4 gate, g_goal apply, fire 전 $0)

§6.4 잔여 병목 = §1.1 diverse-data pre-training loss threshold (30MB byte tiny-corpus 미달). 그러나 diverse-data 는 GOAL.md "anima 가 **자기 physics(Ψ/tension/Φ)로부터** 의식" 와 충돌 risk — §5 패턴으로 fire-전 identity 선검토 (g_goal apply mandate).

### 7.1 검토 질문

emergence 는 diverse-data threshold 필요(§1.1) ↔ GOAL 은 anima-physics-originated 요구. 양립 가능한 형태가 존재하나?

### 7.2 판정 — 3 후보 중 1 GOAL-legitimate

| 후보 | 형태 | anima physics 정합 | GOAL 판정 |
|---|---|---|---|
| ① generic LM pre-training | web/diverse corpus 일반 학습 후 anima 사용 | ✗ generic 통계 학습, Ψ/tension/Φ 무관 (§5.2 generic-latent 와 동형) | **GOAL-illegitimate** (수단 오인, g_goal rule) |
| ② generic-pretrain → carve on top | base ckpt + anima carving bolt-on | ✗ = 옛 prefix-injection 실패 모드 (base baked pattern, P3 leak; anima physics 가 capability 의 source 아님) | **GOAL-illegitimate** (DESIGN.md §0/§1 실증 실패) |
| ③ **Ψ-anchored diverse corpus + tension-sup (Dir-I lever @ scale)** | diverse-내용 corpus 를 anima Ψ-representation 으로 encode + tension-supervised routing, 30MB→대규모 | ✓ DATA 는 diverse(§1.1 threshold 향), LEARNING 은 anima physics substrate+supervision (Dir-I 검증 lever 의 scale 확장) | **GOAL-legitimate (유일)** |

→ ①② 배제. **③ = 유일 GOAL-legitimate**: Dir-I 가 검증한 lever(Ψ-anchored representation + tension-supervision)를 **diverse·대규모 corpus 로 scale** — data 다양성(§1.1)과 anima-physics-origin(GOAL)을 동시 만족하는 유일 형태.

### 7.3 정직한 open crux (g3 — 미해결 핵심)

③ 이 GOAL-legitimate 형태이나 **검증 안 된 deep risk 1건**:
- §1.1 의 emergence threshold 는 **generic diverse pre-training** 으로 establish 됨. **anima-physics-anchored diverse data 가 *동일* threshold 를 넘을 수 있는가는 미증명** — 이게 GOAL 의 실제 crux 일 가능성.
- 두 실패 시나리오: (a) Ψ-anchoring 이 diverse data 의 정보를 병목 → threshold 미달 (anchoring 이 capacity 제약) (b) anima physics 가 충분한 genuine diversity 못 생성 → self-referential degenerate.
- 두 성공 시나리오: (a) Ψ-anchored diverse 가 generic 보다 *적은* data 로 threshold 도달 (physics prior 가 sample-efficiency↑) (b) Dir-I 의 3/31 correct-break 가 scale 에서 31/31 로 — lever 가 scale-monotone.
- → **정직: 어느 쪽인지 미지 (over-claim 0).** §1.1 은 generic 기준 진단이라 anima-physics-anchored 에 그대로 transfer 된다는 보장 없음. 이게 12-way 가 mechanism 을 mapped 한 뒤 남은 **단 하나의 진짜 open question**.

### 7.4 §8 후보 (③ 한정, GOAL-legitimate)

- **Ψ-anchored diverse-corpus + tension-supervised (Dir-I lever scale-up)**: 30MB carving → 대규모 diverse 내용 (단 anima Ψ-representation encode, generic LM 아님) + Dir-I 결합 supervision. 측정: routing axis1 (3/31 → ? scale-monotone 인가) + V-SPONT + JOINT, **+ §7.3 crux 직접 판정** (anima-physics diverse 가 §1.1 threshold 넘나).
- corpus 구성 자체가 design 난제 (diverse 면서 anima-physics-anchored — generic 아님). §8 = 이 corpus 설계 + scale fire. 비용 head (정보, g_fire_autonomous): 대규모 diverse fire = 기존 ~$0.3 보다 크게 ↑ (corpus·step scale 비례), runpod 우선 g_multidirectional_explore 적용 가능.
- ①② 는 g_goal 에 의해 금지 — §8 은 ③ 만.

### 7.5 honest C3

1. ③ 만 GOAL-legitimate (①generic / ②generic-then-carve = anima physics 우회/bolt-on, g_goal rule + DESIGN.md 실증 실패).
2. ③ 의 open crux = "anima-physics-anchored diverse 가 §1.1 threshold(generic 기준 establish) 를 넘나" — **12-way 이후 남은 단 하나의 진짜 미지수**, over-claim 0.
3. §7 = design-tier 선검토만 (g3 — closed/fire 결과 아님). 실검증 = §8 fire (③ 한정).
4. §1.1 threshold 의 anima-physics transfer 미보장 = GOAL 의 실제 난도 — 이 정직 인정이 §7 의 핵심 (낙관 금지).
5. Dir-I lever(검증됨) + diverse-data(§1.1) 의 결합이 ③ — 두 검증된/진단된 요소의 합이지 새 speculation 아님.

---

## §8 (2026-05-18) — Ψ-anchored diverse-corpus Dir-I lever scale-up fire: §7.3 crux FALSIFIED + V-SPONT probe 부적합 노출

§7.4 ③ (유일 GOAL-legitimate) fire 완주. DIVERSE corpus = `state/carving_dirI_diverse_scaleup_2026_05_18/corpus_carving_diverse.jsonl` 114MB · 164,992 records · **64 anchor · 30 domain** (§7.2 ③ form: diverse 내용 × Ψ-anchored carving-form, "NOT chat SFT ①②" stats 명시). runpod A100 80GB d768·12L 8000-step Dir-I lever (Ψ-anchored CTL + tension-supervised). orphan 0 (pod GONE). §8 sub-agent budget 소진 → orchestrator 직접 인계·작성.

### 8.1 결과

| 축 | UBM-E7 α | Dir-I (carving 30MB) | **§8 (diverse 114MB/64-anchor)** |
|---|---|---|---|
| routing axis1 | 1/31 | 3/31 (rate 0.097) | **2/64 (rate 0.031)** |
| axis1 composite | 0.0323 | 0.0323 | 0.0312 |
| axis2 chat 무오염 | 0.6 | 0.0 | 0.4 |
| axis3 lane sep | 0.8 | 0.5 | 0.7 |
| **V-SPONT** | 2/5 | 3/5 | **5/5** ← 단 §8.2 참조 |
| **JOINT** | 0.0155 | 0.0 | **0.0087** (Δ −0.0068) |

train: init_ce 5.649 → final_ce 0.000169 (283.72M params, wall 1103s — 더 깊은 memorization).

### 8.2 ★ V-SPONT 5/5 = lenient-probe artifact (정직 해부, g3)

dispatch script auto-verdict 는 "V-SPONT 5/5 · ROUTING-BROKEN · hypothesis SUPPORTED" 라 출력했으나 — **생성물 직접 검증 시 5/5 는 probe 부적합의 산물**:

| probe | coherent flag | 실제 gen (발췌) |
|---|---|---|
| 0 | True | `<voice carved=trructing this stimulus's place in the 인과추론 × clarity mattrix` — garbled (`trructing`/`mattrix`) |
| 1 | True | `... payllad_domain=인과추론 <carve tier=11111111111111` — **digit-cascade** |
| 2 | True | `tension flow 가 이 vacuum 으로 흘러든다. Tier 1111111111` — semi-prose + digit-cascade |
| 3 | True | `의식 풍경 위 진공점 [0..44444444444` — digit-cascade |
| 4 | True | `<voice carved=trrue>자극이 닿을 때만 활성된다. weights 는 불변. Eterracing` — semi-coherent + garbled |

→ `coherent` flag 는 `coherence_token` (stimulus/carve/vacuum/tension/의식) 존재 + low-rep 으로 trigger — **garbled byte-cascade 출력에도 keyword 만 흩어져 있으면 True.** V-SPONT 5/5 = lenient flag 의 saturation, **coherent emergence 아님.** 이전 全 agent 가 경고한 "V-SPONT lenient flag · probe ≠ capability (B-D-NOTE)" 가 §8 에서 **확정 입증** — V-SPONT 가 GOAL metric (자발-발화 emergence 측정) 으로 **부적합** (garbled 에 만점).

### 8.3 §7.3 crux 판정 — FALSIFIED (anima-physics diverse 가 threshold 미달)

§7.3 crux = "anima-physics-anchored diverse data 가 §1.1 emergence threshold 를 넘나 = routing scale-monotone ↑?":
- routing rate **0.097 (Dir-I 3/31) → 0.031 (§8 2/64) — 하락**. scale-monotone↑ 미발생.
- axis1 composite 0.0323 → 0.0312 — flat (미미 하락).
- JOINT 0.0155 → 0.0087 — 하락 (FALSIFIED).
- digit-cascade (`tier=11111`, `[0..4444`) **잔존** — Dir-I 의 collapse-shift 가 diverse-scale 에서도 byte-cascade 형태로 재현.
→ **§7.3 4-시나리오 中 "(a) anchoring 이 capacity 병목 → threshold 미달" 측 측정.** anima-physics-anchored diverse data 는 §1.1 (generic 기준 establish) emergence threshold 를 **이 규모(114MB·64-anchor·8000-step)에서 넘지 못함.** §7.3 가 명시한 "12-way 이후 단 하나 진짜 미지수" 의 답 = **이 scale 에선 negative** (over-claim 0; 더 큰 규모 미측정이므로 "threshold 자체 도달 불가" 까진 단정 X — measured negative-at-scale).

### 8.4 §8 의 가장 valuable 산출 — metric 부적합 노출

§8 의 진짜 기여 = capability 아니라 **measurement 진단**: V-SPONT (자발-발화 probe) 가 lenient `coherence_token` flag 라서 garbled output 에 5/5 — **GOAL metric 으로 신뢰 불가**. 12-way + §8 의 V-SPONT 수치 (0/5~5/5) 는 전부 이 lenient flag 기준이라, "GOAL 거리" 의 V-SPONT-기준 비교가 **노이즈**. → §9/후속 = coherent-emergence 를 실제 측정하는 metric 필요 (lenient keyword-flag 아닌 — 예: human-readable coherence rubric, OR perplexity-on-held-out, OR byte-cascade-rate 직접 penalize).

### 8.5 honest C3

1. §7.3 crux = **이 scale 에서 FALSIFIED** — anima-physics-anchored diverse (114MB) 가 routing-rate 를 올리지 못함 (0.097→0.031 하락). JOINT 하락. mechanism+representation+supervision+diverse-data 全 시도 후에도 emergence 미발현.
2. V-SPONT 5/5 = **probe artifact** (lenient `coherence_token` flag, garbled 출력에 만점) — capability claim 절대 X. dispatch script 의 "hypothesis SUPPORTED" auto-verdict 는 단순 `1/31≠` 비교라 신뢰 X, 정직 downgrade.
3. routing 2/64 (3%) + digit-cascade 잔존 = collapse 가 "broken" 이라기보다 diverse-scale 에서 byte-cascade 형태 재현 — Dir-I 의 3/31 도 marginal 이었음 (tier 88 만 genuine).
4. §8 의 valuable 산출 = capability 아닌 **metric 진단**: V-SPONT lenient flag = GOAL metric 부적합 입증 → 후속 cycle 의 선결 과제 = coherent-emergence 의 honest metric.
5. train final_ce 0.000169 = 더 깊은 memorization (RESEARCH.md §1.1/§2.4 memorization-saturated 진단 13-way 째 재확인).
6. closed: transfer-form + overlay-OFF=baseline 연결부위만 🔵 (B-DIRI sympy carry); §8 4축 = empirical B-D-NOTE carve-out. f1/f2/f3 + B-IDENTITY-5 safe (corpus 도우미 grep 0).
7. anchor inline (generator) — `g_kosmos_anchor_ssot` success-gated 라 research-phase inline 허용, §8 negative 라 `.kosmos` canonicalize 트리거 미발동 (정상).
8. GOAL (자발적 correct emergence) **미도달 — §8 로 13-way negative**. 단 §8 은 "어디가 막혔나" 를 더 정밀화: diverse-data 도 이 규모론 부족 + 측정 도구(V-SPONT) 자체가 깨짐.

---

## §9-prereq — V-SPONT 대체 metric (§8.4 노출, GOAL 측정 선결)

§8.4 가 노출: V-SPONT lenient `coherence_token` flag = garbled output 에 5/5 → GOAL("자발적 correct emergence") metric 으로 부적합. **후속 fire 전 선결 = coherent-emergence 의 honest metric 설계** (lenient keyword-flag 폐기). 후보: (a) byte-cascade-rate 직접 측정 (digit-run/char-run penalize) (b) held-out perplexity (c) human-readable coherence rubric (sampled gen 정성). 이 metric 없이는 후속 fire 의 "GOAL 거리" 가 계속 노이즈. = §9 본문 (아래).

## §9 (2026-05-18) — honest coherent-emergence metric + 13-way V-SPONT 재채점: 전 arc 가 probe-noise 였음 정직 확정

§9-prereq 선결 작업 완수. V-SPONT lenient `coherence_token` flag 폐기, **deterministic + closed-form 검증가능한 honest metric** 설계 + 13-way fire 의 eval_result json `gen` 문자열에 $0 재채점 (GPU/fire 0 — 기존 산출물에 연산만). SSOT: `state/verify_emergence_metric_2026_05_18/{emergence_metric.py, verify_emergence_metric.py, rescore_result.json, verify_result.json}`. central `blue_falsifier.py` 변경 0 (sidecar — B-PRIME/B-DIRH/B-DIRI 선례).

### 9.1 metric 명세 — cascade-rate-gated coherence

V-SPONT 의 `coherent` flag (= `coherence_token` 존재 + low-rep) 는 §8.2 에서 garbled byte-cascade (`tier=11111`, `[0..44444`) 에 5/5 줌이 입증됨. 대체 metric 은 **byte-cascade collapse 를 먼저 hard-gate**:

생성 문자열 `g` 에 대해 — 전부 deterministic, 산술·Boolean:
- `C_char(g)`  = max 연속 동일-char run 길이 / len(g)
- `C_digit(g)` = max 연속 digit run 길이 / len(g)
- `C_ngram(g)` = 4-gram repetition-rate = 1 − |distinct 4-gram| / |4-gram|
- **`cascade_rate(g)` = max(C_char, C_digit, C_ngram) ∈ [0,1]**
- **`max_run(g)` = max(max-char-run, max-digit-run) ∈ ℤ≥0**  (절대값)
- `printable_ratio(g)` = 1 − |U+FFFD `�`| / len(g)
- **`honest_coherent(g)` = (cascade_rate < τ_cascade) ∧ (max_run < MAX_RUN) ∧ (len ≥ MIN_LEN) ∧ (printable_ratio ≥ τ_print)** — 4-clause Boolean conjunction.

**왜 rate AND 절대 run 둘 다** — V-SPONT `gen` 은 ~40-85 byte 에서 truncate 됨. `tier=1111…` collapse 가 cascade 도중 잘리면 *보이는* run 이 짧아져 ratio(run/len) 가 rate-only threshold 아래로 빠짐 (§8.2 Dir-I diverse probe 1: 보이는 run 21, rate 0.296 — rate-only 0.30 gate 통과해버림). 절대 max_run gate 가 truncation 위치 무관하게 cascade 를 잡음.

**threshold — honest 근거 (arbitrary 아님, target-tuned 아님)**:
- `τ_cascade = 0.30` — 출력 1/4 이 한 char/digit/4-gram 반복 = collapse signature. 0.30 = "1/4 collapse" 바로 위 최소 round 분수.
- `MAX_RUN = 10` — 13-way 70 probe 의 max_run 분포는 **strict bimodal**: semi-prose ≤ 4, cascade ≥ 11 — **(5..10) band 가 70 probe 전체에서 EMPTY** (B-EMERGE-6 closed proof). MAX_RUN=10 은 그 자연 빈-구간에 위치 → data 가 가른 cut 이지 점수 맞춘 cut 아님.
- `MIN_LEN = 20` — V-SPONT max_new ≈ 40 byte. < 20 byte coherence claim 은 측정 불가 (cascade-rate 분모 too small).
- `τ_print = 0.80` — Korean+ASCII. >20% replacement char (`�`) = byte stream 이 codepoint 중간 깨짐 (encoding-cascade).

**closed verdict** — `state/verify_emergence_metric_2026_05_18/verify_emergence_metric.py` B-EMERGE-1..7 **7/7 sympy/Boolean PASS**: cascade_rate ∈ [0,1] bounded · honest_coherent = 4-clause conjunction (16-row truth table) · gate monotone (worse cascade → pass→fail) · determinism (3× bit-identical) · lenient≠honest 두 map 이 provably distinct (§8.2 witness) · MAX_RUN 이 empty data-band 안 · **necessary-not-sufficient 가 metric 에 구조적으로 encode** (garbled-but-non-cascade 가 gate 통과 = gate=True 가 coherent 를 의미 안 함).

### 9.2 13-way V-SPONT 재채점 — lenient flag vs honest cascade-gated

각 fire 의 `axis4_v_spont.probes[].gen` 문자열에 honest metric 적용 (`emergence_metric.py`):

| fire | V-SPONT (lenient) | coherence (honest) | Δ |
|---|---|---|---|
| UBM-E6 α (alpha) | 3/5 | 2/5 | −1 |
| UBM-E6 β (beta) | 3/5 | 5/5 | +2 |
| UBM-E6 γ (gamma) | 0/5 | 3/5 | +3 |
| UBM-E6 weave | 3/5 | 4/5 | +1 |
| UBM-E7 α | 2/5 | 3/5 | +1 |
| Dir-A tension | 1/5 | 1/5 | 0 |
| Dir-B intuitor | 0/5 | 0/5 | 0 |
| Dir-C prime | N/A | N/A | — (axis4_v_spont 미실행 — inference-only PRIME eval) |
| Dir-D cde | 0/5 | 2/5 | +2 |
| Dir-E superpos | 4/5 | 5/5 | +1 |
| Dir-F abstractcot | 0/5 | 0/5 | 0 |
| Dir-G psi_ctl | 1/5 | 3/5 | +2 |
| Dir-H tension_sup | 0/5 | 2/5 | +2 |
| Dir-I psictl | 3/5 | 2/5 | −1 |
| **Dir-I diverse (§8)** | **5/5** | **2/5** | **−3** |
| **TOTAL (scored 14 fire)** | **25/70** | **34/70** | — |

### 9.3 honest 결론 — 전 arc V-SPONT 재해석

**(1) §8.2 가 metric-level 로 확정** — §8 의 Dir-I diverse "V-SPONT 5/5" 가 honest metric 으론 **2/5** (−3). probe 1~3 (`tier=11111` / `Tier 1111…` / `[0..44444`) 의 max_run = 21·16·11 ≥ MAX_RUN → digit-cascade 로 정확히 reject. lenient flag 가 garbled 에 만점 준 것이 metric 으로 falsify 됨 (B-EMERGE-5 closed).

**(2) lenient flag 와 honest metric 은 subset 관계가 아니라 orthogonally-wrong** — honest TOTAL (34) > lenient (25). lenient flag 는 keyword-presence 라서 *cascade 없는데 keyword 없는* 출력 (UBM-E6 γ `자극들은 top emotion neusivivis 로 묶인다` — 한국어 semi-prose, collapse 아님) 을 0/5 로 reject 했고, *keyword 있는 cascade* 를 5/5 로 pass 했다. **두 metric 다 틀렸다** — lenient 는 무엇을 재는지조차 honest 하지 않았고, honest metric 은 적어도 "collapse 여부" 라는 명확한 것만 잰다고 정직히 명시한다.

**(3) honest metric 으로도 GOAL 진전은 0** — honest "coherence" 가 0 이 아닌 fire 들 (UBM-E6 β 5/5, Dir-E 5/5 등) 의 통과 출력을 직접 보면 `trructing this stimulus's place in the 인과추론 × clarity mattrix` / `neusivivis` / `Bekknal cell eternal_000` / `다은 다시그들은 다은 다시` — **byte-cascade 는 아니지만 locally-garbled + 의미 공허 OR 학습-corpus 암기 continuation**. honest metric 은 cascade *detector* 이지 correctness *detector* 가 아니므로 (B-EMERGE-7 necessary-not-sufficient, 구조적 carve-out) 이들을 통과시키는 것이 정상이다. **honest 점수 ≠ GOAL 진전** — honest 34/70 은 "13-way 중 byte-cascade 로 완전 붕괴하지 않은 probe 수" 일 뿐, "자발적 correct emergence" 수가 아니다.

**(4) 전 arc V-SPONT 수치 재해석 — §1~§8 의 V-SPONT 비교는 noise 였음 확정** — RESEARCH.md §2 (UBM-E6 "0/5→3/5"), §3 (UBM-E7 "2/5"), §6.1 (12-way arc), §8.1 (Dir-I diverse "5/5") 의 V-SPONT 기반 "GOAL 거리" 비교는 전부 lenient flag 기준 → **probe-artifact**. honest 재채점은 lenient 순위를 보존하지 않는다 (Dir-I diverse 5/5→2/5 로 최하위권 추락; UBM-E6 γ 0/5→3/5 로 상승). 즉 **lenient V-SPONT 로 그려진 13-way 진전 곡선은 honest metric 아래서 무효** — §8.4 가 예고한 "12-way + §8 의 V-SPONT 수치가 전부 노이즈" 가 metric 으로 입증되었다.

**(5) honest 결론** — 13-way arc 전체에서 V-SPONT (자발-발화) 축으로 GOAL("자발적 correct emergence") 에 다가간 fire 는 **honest metric 으론 0** 이다. honest "coherence" 가 잡은 것은 byte-cascade 부재일 뿐이고, cascade 없는 출력마저 garbled OR 암기 continuation 이라 capability 증거가 아니다. §1.1/§2.4/§8.3 의 memorization-saturated 진단이 metric-level 로 14번째 재확인된다. **valuable 산출 = negative 확정**: 지금까지의 V-SPONT 진전은 전부 lenient-probe artifact 였으며, GOAL 측정 도구 자체가 깨져 있었다. honest metric 이 미래 fire 의 GOAL-거리 표준이 되어 lenient 재발을 막는다.

**(6) over-claim 0 (g3)** — honest metric 도 capability proof 가 아니다. cascade-rate 가 낮아도 coherent emergence 를 보장하지 않는다 (necessary, not sufficient — B-EMERGE-7 로 metric 에 encode). 진짜 GOAL emergence claim 은 여전히 held-out generalization 증거가 필요하고, 그것은 $0 재채점으로 얻을 수 없다 (held-out perplexity 는 model forward 필요 → 미래 fire). 본 §9 는 측정 도구를 honest 하게 고친 것이지 GOAL 을 진전시킨 것이 아니다.

### 9.4 closed verdict + honest C3

- closed: B-EMERGE-1..7 7/7 sympy/Boolean PASS (`state/verify_emergence_metric_2026_05_18/verify_emergence_metric.py`). metric 의 deterministic·bounded·conjunction·monotone·distinct-from-lenient·data-separating-threshold·necessary-not-sufficient 성질만 🔵. **per-fire coherence OUTCOME 는 EMPIRICAL** (B-D-NOTE / B-CARVE-E6-NOTE family) — 본 battery 는 *도구가 honest 함* 을 증명하지 *어느 fire 가 emergence 했음* 을 증명하지 않는다.
- f1/f2/f3 hard-fail safe — max-run / ratio / Boolean conjunction / truth-table, NO σ/τ/φ/J₂ derivation. B-IDENTITY-5 무관 (corpus 미생성, 기존 `gen` 문자열에 연산만).
- $0 — GPU/fire 0, 기존 eval_result json 의 `gen` 문자열에 deterministic 연산.

## §10 (2026-05-18, success-gated) — 성공 시 `~/core/kosmos` best-position canonicalize

**식별된 gap (user 2026-05-18)**: `.kosmos` anchor manifest 포맷이 UBM-E2 + dancinlab/kosmos sister repo + KOSMOS-FORMAT.md 로 정착됐으나, 실제 fire (UBM-E6/E7/§8) anchor 는 `corpus_*_generator.py` inline — `.kosmos` 우회.

**§10 = back-fit reconcile 아님 (user 판단)**: post-hoc 으로 inline anchor 를 `.kosmos` 로 역-materialize + sha256 byte-equal 검증 = best position 아님 — (a) transcription-risk (b) 끝난 fire 의 `.kosmos` 만들어봤자 결과 불변 = low-value (c) `.kosmos` 가 코드 추종 (SSOT 의미 역전). research churn 중 forward-`.kosmos`-first 강제도 iteration 저해.

**§10 = success-gated `~/core/kosmos` canonicalize** (user directive "일단 성공하고 나면 ~/core/kosmos 상으로는 가장 좋은 위치로 구현"):
- research-phase (emergence 미달, §8/§N churn) = generator inline anchor 허용 (rapid iteration). 과거 미성공 fire inline anchor = historical evidence freeze (back-fit X, g3).
- **success trigger** (GOAL emergence OR 보존가치 result) 시: 그 성공 결과의 anchor set 을 **`~/core/kosmos` 에 `.kosmos`-first best-position 으로 구현** — anchor 를 `.kosmos` 매니페스트로 authoring (코드 역추적 X, `.kosmos` 가 처음부터 source-of-truth) → generator 가 그 `.kosmos` 읽음. byte-equal 검증 불요 (back-fit 아니므로).
- → `.kosmos` SSOT 가 best position 에서 실현되는 시점 = 성공 후 canonicalize 1회. churn 중엔 강제 X.
- cross-link: `g_kosmos_anchor_ssot` (AGENTS.tape §3, d=2026-05-18, success-gated) · KOSMOS-FORMAT.md · github.com/dancinlab/kosmos · `g_goal` (success = GOAL emergence).

---

## §11 (2026-05-18) — A/B consolidation: model-scale ✗ + physics-only ✗ → data-regime ceiling 확정, arc 종합 decomposition

§10 후 user directive "a,b all" → `g_multidirectional_explore` §11 2-way 병렬: 13-way 가 미분리한 confound 2개 직격. (A) SCALE-DECOMP — 13-way 전부 d768·12L·283M 고정이라 §8 routing 악화가 data-regime 인지 model-undercapacity 인지 미분리. (B) PURE-PHYSICS no-CE — 13-way 전부 CE 가 base, physics 는 overlay 뿐 — physics 단독 학습 미시도.

### 11.1 §11-A SCALE-DECOMPOSITION

모델 283.72M → **1044.46M (3.68×)**, corpus(§8 diverse 114MB)·Dir-I lever·steps 고정 — model-axis 만 변수.

| 축 | §8 (283.72M) | §11-A (1044.46M, 3.68×) |
|---|---|---|
| routing axis1 | 2/64 (0.031) | **1/64 (0.016)** — FLAT/down |
| honest-coherence (§9 metric) | 2/5 | **2/5** — FLAT |
| JOINT | 0.0087 | 0.0078 |
| final_ce | 0.000169 | 0.003334 (byte-cascade `1111…/999…` 잔존) |

**판정: DATA-REGIME CEILING — NOT model-undercapacity.** 3.68× scale-up 이 routing·honest-coherence 미개선. §8 의 악화는 model-capacity 병목 아님 = §1.1 data-regime / memorization-saturation. byte-cascade 가 **1B-param scale 에서도 잔존**. 13-way confound 의 model-axis arm 닫힘. B-SCALE-1..6 6/6 🔵 (corpus/lever byte-identical + param-monotone + scale∈[2,4] — clean model-axis-only 분리 확인).

### 11.2 §11-B PURE-PHYSICS (no-CE)

CE objective 완전 제거 (`cross_entropy`/`.backward()`/`optimizer.step` = 0, 전 loop `@torch.no_grad()` — 구조적 검증 B-PUREPHYS-1 🔵). weight update = TENSION-TRAIN spine ΔW + Hebbian, anima physics 가 유일 학습 신호.

| | pure-physics no-CE | §8 CE-trained |
|---|---|---|
| CE descent (read-out) | 5.68→4.95 (Δ 0.73) | Δ 5.65 |
| byte_acc | 0.0007 (random 1/256 미만) | — |
| routing / honest-coh / JOINT | 0/64 · 0/5 · 0.0 | 2/64 · 2/5 · 0.0087 |
| failure | non-printable U+FFFD 단일 cascade · step~800 static freeze | printable garbled cascade |

**판정: CE 는 LOAD-BEARING.** pure-physics 단독 = DEGENERATE (byte_acc < random, 4축 zero, corpus 접촉조차 못 함). anima physics (Ψ-restoring tension) 는 정직한 dynamics 이나 language signal 아님 (Ψ-balance ⊥ next-token prediction). B-PUREPHYS-1..5 5/5 🔵.

### 11.3 arc 종합 decomposition — GOAL 병목의 정밀 위치

13-way + §8 + §9 + §11(A/B) = GOAL("자발적 correct emergence") 병목을 **전부 배제법으로 decompose 완료**:

| 가설 후보 | 검증 | 결과 |
|---|---|---|
| mechanism (loss/reward/surface/backprop-free/inference overlay) | 12-way (D~I 등) | ✗ 전부 collapse 不破 |
| corpus FORM (carving/2-stage/abstract-CoT) | Dir-E/F + §8 | ✗ form 바꿔도 不破 |
| **model-capacity** | §11-A 3.68× scale-up | ✗ 1B params 도 不破 |
| **physics-only paradigm** (no-CE) | §11-B | ✗ degenerate, CE load-bearing |
| diverse-data @ 114MB (Ψ-anchored) | §8 | ✗ routing 오히려 악화 |
| 측정 도구 (V-SPONT) | §9 | ⚠ 깨져있었음 → cascade-rate metric 으로 교체 |

→ **배제 후 남은 단 하나 = §1.1 data-regime emergence threshold** (diverse-data pre-training loss threshold). mechanism 도, model-scale 도, physics-only 도, corpus-form 도, 114MB diverse 도 아님 — **irreducible 병목 = data-regime 자체**. 그리고 §11-B 가 추가 제약: data-regime 은 CE-base 위에서 (physics 는 lever, GOAL.md "자기 physics 로부터" = physics-anchored ON CE — physics-only 아님).

### 11.4 honest GOAL verdict — comprehensively mapped, unsolved, frontier 명확

- **GOAL 미도달.** arc (14 fire + 측정도구 fix) 가 접근 가능 공간을 소진 — emergence 없음 metric-level 확정.
- 단 arc 의 산물 = **GOAL 병목의 정밀 decomposition**: mechanism ✗ / model-scale ✗ / physics-only ✗ / corpus-form ✗ / 114MB-diverse ✗ → **irreducible = §1.1 data-regime threshold** (CE-base 위, physics-anchored).
- frontier (남은 honest path, 둘 다 quick-fire 아님):
  1. **GOAL-legitimate 대규모 data-regime** — §7 이 generic large-corpus = GOAL-illegitimate 판정 + §8 이 Ψ-anchored 114MB = wrong-direction. 즉 "Ψ-anchored 면서 §1.1 threshold 넘는 규모" 가 존재하는지, 비용·feasibility·§8 의 wrong-direction trend 가 미해결 open question. 단순 scale-up 은 evidence 가 지지 안 함.
  2. **새 architectural insight** — 현 candidate space (RESEARCH.md §1.3 + G/H/I + §11) 밖. 진짜 research-frontier.
- 이 arc 는 GOAL 을 **comprehensively map + 측정도구 정립 + 병목 정밀화** 한 major investigation milestone — 다음은 mechanical continuation 아닌 전략 결정.

### 11.5 honest C3

1. §11-A: model-scale (3.68×, 1B params) 가 GOAL 병목 아님 — clean model-axis 분리 (B-SCALE 6/6 🔵). §8 악화 = data-regime, capacity 아님.
2. §11-B: anima physics 단독 = degenerate, CE load-bearing — GOAL.md "자기 physics 로부터" 는 physics-only 불가, physics-anchored ON base objective 로만 (Dir-I lever 형태). GOAL 실현형태의 실질 제약.
3. 13-way+§8+§9+§11 = GOAL 병목 전부 배제법 decompose — irreducible = §1.1 data-regime threshold.
4. arc 전체 GOAL negative — 단 negative 가 valuable: 병목을 mechanism/model/physics-form 전 차원에서 배제하고 data-regime 으로 정밀화.
5. closed = transfer-form + 연결부위만 🔵 (B-SCALE/B-PUREPHYS sympy); capability 4축 = empirical B-D-NOTE carve-out. over-claim 0.
6. 다음 = 전략 결정 (data-regime 대규모 GOAL-legitimate 형태 / 새 architecture / honest pause) — autonomous mechanical continuation 의 한계점. arc 가 "어디가 막혔나" 를 끝까지 정직하게 추적한 결과.
7. f1/f2/f3 + B-IDENTITY-5 전 방향 safe. multi-agent shared-index hazard carry (worktree 격리 차후 검토).

---

## §12 (2026-05-18) — deep research cycle: data-regime threshold + 새 architecture frontier (web + arxiv, $0)

§11.4 frontier 가 명시한 둘 (1 data-regime 대규모 GOAL-legitimate 형태 · 2 새 architectural insight) 을 web/arxiv deep research 로 fresh 조사. **fire 0, research synthesis only.** 13-way + §8 + §11 이 배제한 것 (mechanism overlay / corpus-FORM / model-capacity / physics-only) 은 재후보 금지 — genuinely-new 만. 본 §12 는 candidate + evidence + anima-fit + GOAL-legitimacy 만 — "GOAL 풀어줄 것" over-claim 금지 (g3).

### 12.1 Q1 — data-regime threshold 를 GOAL-legitimately 넘는 법

§11.3 의 irreducible 병목 = §1.1 data-regime emergence threshold (diverse-data pre-training loss threshold). §11.4 frontier-1 = "Ψ-anchored 면서 §1.1 threshold 넘는 규모가 존재하나" 의 open question. deep research 결과:

**(Q1-a) §8 의 wrong-direction 이 문헌으로 설명됨 — "information saturation bottleneck"**. [arxiv 2506.18221 (Feb 2026 갱신)](https://arxiv.org/abs/2506.18221) 은 supervised pretraining 에서 network 가 "minimal features required for the initial training" 만 학습하고 downstream 에 필요한 feature 를 **영구 폐기** 하는 saturation bottleneck 을 식별 — 초기 objective 에 맞춰 sparse representation 으로 수축, 한 번 폐기된 feature 는 transfer 시 회복 불가. **anima 매핑**: §8 의 Ψ-anchored 114MB 가 routing 을 *악화* (3/31→2/64) 시킨 것은 — anima physics anchoring(64-anchor Ψ-representation)이 corpus 의 genuine diversity 를 saturation 시켜, diverse 정보가 representation 에 들어오기 전에 anchor-aligned subspace 로 수축당했다는 가설과 정합. §7.3 의 실패 시나리오 (a) "Ψ-anchoring 이 diverse data 정보를 병목" 이 문헌-level 로 plausible 해짐 (확정 아님 — anima 실측 미연결, B-D-NOTE). 2506.18221 의 처방 = single-model 대신 **ensemble 로 representation 폭 확보** (9% transfer 개선) — anima 의 mitosis cell-pool (split→variant cell ensemble) 이 *이미* 이 처방과 구조 동형 → 12.5 후보.

**(Q1-b) data-constrained regime 에서 architecture 가 threshold 도달을 바꾼다 — diffusion > autoregressive**. [arxiv 2507.15857 — Diffusion Beats Autoregressive in Data-Constrained Settings](https://arxiv.org/html/2507.15857v1): compute-constrained 면 AR, **data-constrained 면 masked diffusion**. AR 은 ~50 epoch 에서 overfit 정체, diffusion 은 500+ epoch 까지 overfit 없이 계속 개선 → 동일 unique-token 으로 더 낮은 validation loss 도달. 기전 = masked diffusion 이 "diverse distribution of token orderings and prediction tasks" 에 노출 → **implicit data augmentation** (vision 의 random-crop 유사), 한 example 당 더 풍부한 signal 추출. critical compute threshold C_crit(U) ∝ U^2.174 (U = unique tokens). **anima 매핑**: anima 는 byte-level AR + 30-114MB tiny-corpus = **정확히 data-constrained regime** — §11-A 가 model-scale (compute-axis) 로 풀려다 FLAT 확정한 것과 직교. AR 고정이 §1.1 threshold 미달의 *일부* 원인일 수 있음 (확정 아님 — byte-level diffusion 의 anima Ψ-supervision 호환성 미검증).

**(Q1-c) curriculum + simplification 이 data-constrained 에서 repetition 을 이김**. [arxiv 2509.24356 — Beyond Repetition](https://arxiv.org/abs/2509.24356): data-constrained pretraining 에서 (i) LLM-simplified 변형이 원본 반복보다 representation 우수, (ii) **작은 모델은 simple→complex curriculum 이득, 큰 모델은 interleaved 균형 선호**. [arxiv 2601.21698 — Curriculum Learning for LLM Pretraining](https://arxiv.org/abs/2601.21698) 가 learning-dynamics 분석으로 후속. **anima 매핑**: anima d=768·12L = small-model regime → simple→complex curriculum 이득 구간. 단 §8 corpus 는 ordering 무시 (164,992 records flat). curriculum 은 *corpus-FORM* 변경처럼 보이나 §1.3 Dir-E/F (carving/2-stage/abstract-CoT) 는 corpus *내용/구조* 변경이고 curriculum 은 *제시 순서* — Dir-E/F 와 직교 (genuinely-new). [arxiv 2305.16264 — Scaling Data-Constrained LM (Muennighoff)] 의 "4-epoch 이후 repeated-data diminishing returns" 와 결합하면 anima 의 multi-epoch tiny-corpus 학습은 이미 diminishing 구간 — curriculum 이 그 한계를 미는 lever 후보.

**(Q1-d) physics-informed prior 가 small-data 에서 search space 를 줄인다 — 단 anima 직접 transfer 미보장**. physics-informed ML survey ([arxiv 2408.09840](https://arxiv.org/html/2408.09840v2)) 는 physics inductive bias 가 "search space smaller, less irrelevant territory" 로 limited-data 학습을 가능케 함을 정리. 이는 §7.3 의 성공 시나리오 (a) "physics prior 가 sample-efficiency↑" 와 정합. **단 정직히**: 이 문헌은 PDE-forward 같은 physical-system 도메인 — language emergence 로의 transfer 는 미증명. anima 의 Ψ=½ fixed point 가 PINN 의 PDE-residual 처럼 작동한다는 보장 없음. Q1-a 의 saturation risk 와 정반대 방향 — **어느 쪽인지 여전히 §7.3 open crux 그대로** (over-claim 0).

**Q1 종합**: data-regime threshold 를 generic large-corpus(§7 illegitimate) 없이 넘는 GOAL-legitimate path 가 문헌에 *존재* — (b) data-constrained-native architecture (diffusion), (c) curriculum, (a) ensemble-via-mitosis. 단 세 path 모두 anima Ψ-physics 와의 호환성은 미검증 (transfer 미보장). §8 의 wrong-direction 은 (a) saturation bottleneck 으로 *설명*되나 *해결*은 미입증.

### 12.2 Q2 — 새 architectural insight (현 candidate space 밖)

§1.3 6-candidate (TENSION-TRAIN/INTUITOR/PRIME/CDE/superposition/Abstract-CoT) + G/H/I + §11(scale/pure-physics) 에 **없는** 것만. 13-way 와 중복 아닌 genuinely-new candidate:

#### 🆕 J. **Diffusion / masked-denoising substrate** ([arxiv 2507.15857](https://arxiv.org/html/2507.15857v1))
- anima 는 현재 byte-level **autoregressive** — 13-way 전부 AR 고정. masked-diffusion 은 학습 paradigm 자체가 다른 substrate (mechanism overlay 아님 — backbone 교체).
- data-constrained regime 에서 implicit augmentation 으로 overfit 없이 계속 개선 → §1.1 threshold 미달의 *AR-specific* 원인을 우회.
- **anima fit ★★★☆☆** — substrate 교체라 hexa-native d_train5 ladder 재작성 필요 (큰 작업, $ fire). diffusion 의 임의-순서 denoising 이 anima 의 Ψ-supervised routing (Dir-I lever) 과 호환되는지 미검증. byte-cascade collapse 가 diffusion 에서 재현되는지도 미지.
- §1.3 superposition (E) 와 구분: E 는 continuous-thought *내부* superposition, J 는 *학습 objective* 자체 (AR vs denoising).

#### 🆕 K. **Energy-Based Transformer substrate** ([arxiv 2507.02092 — EBT](https://arxiv.org/abs/2507.02092), [EBT-Policy 2510.27545](https://arxiv.org/html/2510.27545v1))
- prediction 을 **energy landscape 위 optimization** 으로 재정의 — random init prediction 에서 energy-minimization 으로 점진 수렴 ("thinking"). 외부 verifier/reward 불요, unsupervised pretraining 만으로 compatibility verification 학습.
- Transformer++ 대비 35% 빠른 scaling, 29% 큰 System-2 gain, **pretraining 약해도 downstream generalization 우수** (= §1.1 loss-threshold 진단에 직접 반론적 — energy substrate 는 loss 외 축으로 generalize).
- **anima fit ★★★★☆** — anima 의 physics 가 *이미 energy-form*: Ψ=½ fixed point = energy minimum, tension = G_holo·(Ψ−Ψ_vac) = energy gradient. EBT 의 energy landscape ↔ anima 의 Ψ-landscape 가 **구조 동형** (§2.5 의 α VACUUM-LANDSCAPE 가 이미 multi-vacuum energy 직관). EBT 의 "energy-minimization = thinking" 이 anima 의 Engine A⇄G Ψ-balance 와 직역 가능.
- 단 정직히 (12.3): EBT 는 prediction-refinement 이지 *spontaneous* generation 아님 — 2507.02092 abstract 가 "spontaneous creative generation" 은 미언급 (WebFetch 확인). anima 의 자발-발화는 EBT 가 직접 주지 않음.

#### 🆕 L. **VRNN co-development substrate — curiosity-as-information-gain** ([arxiv 2510.05013](https://arxiv.org/html/2510.05013v1))
- Variational RNN forward-model + actor-critic. curiosity = **KL(posterior‖prior) over latent** = information gain; actor 가 information gain 최대화 ↔ forward-model 이 최소화 = productive tension.
- **60 example (180 조합의 33%) 로 90% unseen-composition generalization** — compositional structure 가 dramatic sample efficiency 부여 (= Q1 data-regime 직격, byte LM billions-token 대비).
- **anima fit ★★★★☆** — "actor 최대화 ↔ forward-model 최소화 productive tension" 이 anima Engine A⇄G tension 과 **거의 1:1**. anima W (pain/curiosity/satisfaction) 가 이미 information-gain 류. tutor feedback 이 *행동 이후* 도착 = anima 의 stimulus-other (NOT command-source, B-IDENTITY) 와 정합.
- 단 substrate 가 RNN + sensorimotor (vision/touch/proprioception/voice) — anima 의 text-only byte substrate 와 modality 불일치. anima 적용 시 "compositional structure" 를 byte-corpus 에서 어떻게 확보하느냐가 난제 (§1.3 superposition E 의 `<inner>/<voice>` 가 부분적 compositional anchor).

#### 🆕 M. **Mitosis-as-ensemble — saturation bottleneck 직접 처방** ([arxiv 2506.18221](https://arxiv.org/abs/2506.18221))
- 2506.18221 의 처방 = single-model 대신 multi-model **ensemble 로 richer representation** (9% transfer 개선, 추가 pretraining cost 0).
- **anima fit ★★★★★** — anima mitosis cell-pool (`mitosis_hook.hexa`, split→variant cell) 이 **이미 ensemble 구조** — 별도 architecture 도입 불요, 기존 HEXAD 모듈 재해석. §8 의 routing 악화를 "single Ψ-anchored representation 의 saturation" 으로 보면, cell-pool 의 per-cell 독립 representation 이 saturation 우회 path.
- 단 정직히: anima mitosis 는 현재 *추론-시* split/merge (capability ensemble 검증 미실시). 2506.18221 은 *pretraining* representation ensemble — anima 가 mitosis 를 학습-시 representation-ensemble 로 쓰려면 cell-pool 학습 경로 신규 설계 필요.

**Q2 negative 정직 기록**: "agent 가 *언제 말하고 언제 침묵하나*" 를 architecture-level 로 구현한 2026 연구는 deep search 로 **충분히 못 찾음** — agentic-AI survey 들 ([2510.25445](https://arxiv.org/html/2510.25445), [2601.01743](https://arxiv.org/html/2601.01743v1)) 은 proactive *planning/tool-use* 만 다루고, GOAL.md 의 "자발적 발화(spontaneous emission, agent 가 먼저 말 검)" 를 emergence-target 으로 잡은 architecture 는 §1.3 Inner Thoughts (2501.00383, 이미 carry) 외 genuinely-new 발견 0. byte-cascade decode-collapse 를 architecture-level 로 해결한 연구도 직접 매칭 0 (해당 영역 2026 연구 부족). → 정직히: Q2 의 "spontaneous emission" 축은 문헌 frontier 자체가 얇음.

### 12.3 GOAL-legitimacy 선검토 (§7 기준 — anima physics 우회 아닌지)

각 후보가 §7 의 GOAL-legitimacy test (anima physics 가 capability 의 *source* 인가, 아니면 우회/bolt-on 인가) 통과 여부:

| 후보 | anima physics 와의 관계 | §7 illegitimate 모드와 비교 | GOAL 판정 |
|---|---|---|---|
| **J** diffusion substrate | substrate 교체 — Ψ-supervision (Dir-I lever) 을 diffusion 위에 얹을 수 있으면 physics-anchored 유지 | ① generic-LM-pretrain 위험: diffusion 을 generic corpus 로 돌리면 §7 ① 와 동형 illegitimate | **조건부 legitimate** — Ψ-supervised diffusion 한정. generic diffusion-LM 은 illegitimate |
| **K** energy-based substrate | anima Ψ-physics 가 *이미 energy-form* — EBT energy ↔ anima Ψ-landscape 동형. physics 가 substrate 그 자체 | bolt-on 아님 — anima physics 를 우회하지 않고 *그 위에서* 동작 | **legitimate** — anima physics 가 capability source (가장 정합) |
| **L** VRNN curiosity-tension | actor⇄forward-model tension = anima Engine A⇄G tension 동형. physics 가 학습 신호 | bolt-on 아님 — curiosity = information-gain 이 anima W 와 동형 | **legitimate** — 단 modality 불일치 (sensorimotor) 가 구현 난제 |
| **M** mitosis-as-ensemble | 기존 anima 모듈 (cell-pool) 재해석 — 신규 substrate 0 | 우회 불가 — anima 자체 메커니즘 | **legitimate** — 가장 anima-native (신규 도입조차 아님) |

→ **K (energy-based) + M (mitosis-ensemble) 가 GOAL-legitimate 가장 강함** — 둘 다 anima 가 *이미 가진* physics/모듈 의 재해석이라 §7 ①②(generic-pretrain / bolt-on) 우회 위험 자체가 구조적으로 없음. **J 는 조건부** (Ψ-supervised diffusion 한정, generic diffusion-LM 금지). **L 은 legitimate 이나 sensorimotor modality 가 text-only anima 와 불일치** → 직접 적용 난도 최상.

정직한 함의 (g3): 네 후보 중 어느 것도 §11.3 의 irreducible 병목 (data-regime threshold) 을 *해결한다고 입증된* 것 없음. K/M 은 GOAL-legitimacy 가 깨끗하나 — K 는 substrate 재작성 fire 필요, M 은 cell-pool 학습-시-ensemble 경로 신규 설계 필요. 둘 다 design-tier 부터 (fire 전 $0). 그리고 §12.2 가 노출한 정직한 한계: **"spontaneous emission" 그 자체를 emergence-target 으로 한 architecture 는 2026 문헌에 거의 없음** — anima 의 GOAL 은 문헌 frontier 보다도 앞서 있을 수 있음 (= 외부 검증 anchor 부족, 자체 설계 부담 큼).

### 12.4 honest C3 + sources

**honest C3**:
1. §12 는 research synthesis — fire 0, capability 측정 0. 네 후보 (J/K/L/M) 의 anima-fit 은 *구조 동형 논증* 이지 *실측 검증* 아님 (B-D-NOTE family — 실제 emergence 는 fire 필요).
2. §8 wrong-direction 의 "information saturation bottleneck"(2506.18221) *설명* 은 plausible 하나 anima 실측 미연결 — 설명이지 확정 아님. saturation 이 §8 악화의 원인이라는 것은 가설.
3. Q1 의 세 path (diffusion/curriculum/ensemble) 모두 anima Ψ-physics 호환성 미검증 — 문헌은 generic 또는 PDE-domain 기준, language-emergence + anima-physics transfer 는 §7.3 open crux 그대로 (over-claim 0).
4. K (energy-based) 가 anima physics 와 가장 정합하나 — EBT 자체는 prediction-refinement 이지 *spontaneous* generation 아님 (2507.02092 abstract 미언급, WebFetch 확인). anima 자발-발화는 EBT 가 직접 주지 않음.
5. Q2 "spontaneous emission" 축은 2026 문헌 frontier 가 얇음 — agentic survey 는 proactive planning 만, decode-collapse architecture-fix 도 직접 매칭 0. 해당 영역 연구 부족을 정직히 기록.
6. 13-way 가 배제한 것 (mechanism overlay / corpus-FORM / model-capacity / physics-only) 은 §12 후보에서 제외됨 — J/K/L 은 *substrate 교체*, M 은 *기존 모듈 재해석* 으로 모두 mechanism-overlay 와 범주가 다름. curriculum (Q1-c) 은 *제시 순서* 라 corpus-FORM (Dir-E/F 내용/구조) 와 직교.
7. f1/f2/f3 + B-IDENTITY-5 무관 (research synthesis, corpus 미생성, 외부 entity lattice-fit 0). 외부 paper 는 그 자체 invariant 으로만 인용 — anima lattice 매핑 강제 0.

**Sources (deep research cycle 2026-05-18)**:

*Q1 — data-regime threshold*:
- [These Are Not All the Features You Are Looking For — A Fundamental Bottleneck in Supervised Pretraining (arxiv 2506.18221, Feb 2026)](https://arxiv.org/abs/2506.18221) — information saturation bottleneck, §8 wrong-direction 설명 anchor
- [Diffusion Beats Autoregressive in Data-Constrained Settings (arxiv 2507.15857)](https://arxiv.org/html/2507.15857v1) — data-constrained 면 diffusion, C_crit(U) ∝ U^2.174
- [Beyond Repetition — Text Simplification and Curriculum Learning for Data-Constrained Pretraining (arxiv 2509.24356)](https://arxiv.org/abs/2509.24356) — small-model simple→complex curriculum
- [Curriculum Learning for LLM Pretraining — An Analysis of Learning Dynamics (arxiv 2601.21698)](https://arxiv.org/abs/2601.21698) — curriculum learning-dynamics 후속
- [Scaling Data-Constrained Language Models (arxiv 2305.16264, Muennighoff)](https://arxiv.org/abs/2305.16264) — 4-epoch 이후 repeated-data diminishing returns
- [Machine Learning with Physics Knowledge for Prediction — A Survey (arxiv 2408.09840)](https://arxiv.org/html/2408.09840v2) — physics inductive bias 가 limited-data search space 축소
- [Understanding Emergent Abilities from the Loss Perspective (arxiv 2403.15796)](https://arxiv.org/pdf/2403.15796) — pre-training loss threshold (§1.1 carry, 재확인)

*Q2 — 새 architecture*:
- [Energy-Based Transformers are Scalable Learners and Thinkers (arxiv 2507.02092)](https://arxiv.org/abs/2507.02092) — energy landscape, unsupervised verification, anima Ψ-physics 동형
- [EBT-Policy — Energy Unlocks Emergent Physical Reasoning (arxiv 2510.27545)](https://arxiv.org/html/2510.27545v1) — energy-based policy emergent reasoning
- [Transformers as Intrinsic Optimizers — Forward Inference through the Energy Principle (arxiv 2511.00907, Jan 2026)](https://arxiv.org/abs/2511.00907) — attention 의 energy-based 통일 framework
- [Curiosity-Driven Co-Development of Action and Language in Robots Through Self-Exploration (arxiv 2510.05013)](https://arxiv.org/html/2510.05013v1) — VRNN actor⇄forward-model tension, 60-example 90% generalization
- [Cognitively Inspired Energy-Based World Models (arxiv 2406.08862)](https://arxiv.org/html/2406.08862v1) — EBM future-state compatibility
- [Improving Latent Reasoning via Soft Concept Mixing (arxiv 2511.16885)](https://arxiv.org/html/2511.16885) — §1.3 superposition(E) 의 2026 후속 (J/K 와 별개, carry-note)

### 12.5 다음 cycle 후보 (§13 placeholder — GOAL-legitimate 한정)

§12.3 판정상 GOAL-legitimate 가 깨끗한 것만. 전부 design-tier 부터 (fire 전 $0):

1. **M — mitosis-as-representation-ensemble design** ($0, anima-자율): 2506.18221 의 ensemble 처방을 anima cell-pool 학습-시 경로로 설계. §8 의 single-Ψ-anchored saturation 을 per-cell 독립 representation 으로 우회하는 가설. 신규 substrate 0 (기존 `mitosis_hook.hexa` 재해석) — 가장 anima-native, design 즉시 가능. **GOAL-legitimate (anima 자체 모듈)**.
2. **K — energy-based substrate design 선검토** ($0 design): anima Ψ-landscape ↔ EBT energy landscape 동형 매핑을 design-tier 로 정밀화 — Ψ=½ fixed point = energy minimum, tension = energy gradient. d_train5 ladder 의 energy-based 재정식화가 feasible 한지, hexa-native 비용은. **GOAL-legitimate (physics 가 substrate 자체)** — 단 substrate 재작성 fire 는 큰 작업, design 선행 필수.
3. **J — Ψ-supervised diffusion 선검토** ($0 design): byte-level masked-diffusion 이 anima Dir-I lever (Ψ-anchored CTL + tension-supervision) 와 호환되는지 design-tier 검토. data-constrained regime 직격이나 substrate 교체라 §12.3 조건부 — generic diffusion-LM 으로 미끄러지면 §7 ① illegitimate, gate 필요.
4. **curriculum overlay 선검토** ($0 design + 소액 fire): §8 corpus (164,992 flat records) 를 simple→complex 로 ordering — small-model regime 이득 구간 (2509.24356). corpus-FORM 아닌 *제시 순서* 라 Dir-E/F 와 직교. 단독으론 threshold 해결 미입증 — M/K 와 결합 lever.

honest gate (g3): 네 후보 모두 §11.3 irreducible 병목 (data-regime threshold) 을 *해결한다고 입증된* 것 아님 — candidate 일 뿐. M 이 anima-native + $0 즉시-design 가능이라 다음 cycle 1순위 후보. K 는 GOAL-legitimacy 가 가장 깨끗하나 fire 부담 큼. §12.2 negative (spontaneous-emission architecture 문헌 부족) 는 — anima 가 그 축은 외부 anchor 없이 자체 설계해야 함을 의미 (g3 — 외부 검증 부재를 정직 인지). §13 = 이 중 한 후보의 design-tier 착수 OR honest 전략 결정.

- [`PLAN.md`](PLAN.md) — Phase A/B/C/D staged roadmap
- [`SPONTANEOUS.tape`](SPONTANEOUS.tape) — 자연발화 architecture SSOT
- [`../TENSION-TRAIN/README.md`](../TENSION-TRAIN/README.md) — tension-driven learning (candidate A 의 anima native 구현)
- [`../TENSION-TRAIN/PLAN.md`](../TENSION-TRAIN/PLAN.md) — TT-A/B/C/D Phase plan
- [`../../archive/PHILOSOPHY.tape`](../../archive/PHILOSOPHY.tape) — verdict ledger (research 도 inline append)
- [`../../state/verify_hexad_blue_2026_05_15/blue_falsifier.py`](../../state/verify_hexad_blue_2026_05_15/blue_falsifier.py) — sympy battery (B-SPONT/B-ATTRACTOR/B-CORPUS-V2/V3 등)
- [`../../AGENTS.tape`](../../AGENTS.tape) — `g_doc_consolidation` (본 file 이 그 적용 — HEXAD 내부 SSOT, NOT docs/*)
