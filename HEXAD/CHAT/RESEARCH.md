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

---

## §13 (2026-05-18) — §12 candidate 4-way (J/K/L/M) consolidation: 전부 negative/design-closed

§12 deep-research candidate (J diffusion / K energy-based / L VRNN / M mitosis-ensemble) 4 방향 병렬 (`g_multidirectional_explore`). honest §9 cascade-rate metric 으로 측정.

### 13.1 4-way 결과

| Dir | 유형 | 실행 | routing axis1 | honest V-SPONT | JOINT | 판정 |
|---|---|---|---|---|---|---|
| **M** Mitosis-ensemble | 모듈 재해석 | design-only $0 | — | — | — | §11-A model-capacity 인접 — fire = 중복 negative-at-scale 예상, design-tier 마감 (B-MITENS 6/6 🔵) |
| **L** VRNN curiosity-tension | forward-model loop | design-only $0 | — | — | — | closed action-perception loop 부재 (anima = open-loop pretraining); mechanism 환원 = "Dir-I + stochastic Ψ latent" — 새 fire 아님 (B-DIRL 5/5 🔵). VRNN 은 future live-자연발화 loop candidate |
| **K** Energy-Based Transformer | energy substrate | fire (283.72M, runpod) | 0.0312 (≈2/64) | 1/5 | **0.0** | FALSIFIED — final_ce 0.000398 (deep memorization), axis2 chat 0.0. energy transfer-form B-EBT 5/5 🔵 (Ψ-physics = strictly-convex energy, descent-monotone) 단 capability = §8 동형 |
| **J** Ψ-supervised diffusion | diffusion substrate | fire (runpod) | **0/64** | 0/5 | **0.0** | FALSIFIED — non-AR substrate (2507.15857 data-constrained 이점 가설) 도 routing 0/64, Δ vs E7 −0.0155. masked-diffusion ce_descent 4.22 (B-DIRJ closed) |

### 13.2 honest 판정 — §12 candidate 도 §1.1 병목 不破

- **fire 2건 (K/J) = JOINT 0.0 FALSIFIED**: energy-substrate 도 diffusion-substrate 도 byte-cascade/routing-collapse 못 깸. K final_ce 0.0004 = 더 깊은 memorization (§1.1/§2.4 재확인). J non-AR 도 routing 0/64.
- **design 2건 (M/L) = fire 불요 honest 판단**: M = §11-A 가 닫은 model-capacity 인접 (saturation-분산 이득 ↔ per-cell-capacity 손실 offset, net 미지 → 중복 측정). L = closed-loop 부재 + Dir-I 로 환원. 둘 다 evidence-weighted 로 fire 가치 0 → design-tier $0 (각 closed-form battery 만 — anti-padding).
- → §12 의 substrate-change (J/K) + 모듈-재해석 (M/L) 4 candidate 모두 §11.3 irreducible 병목 (data-regime threshold) 을 건드리지 못함. **architecture/substrate space 도 mechanism space 와 동일하게 소진.**
- closed: B-MITENS 6/6 · B-DIRL 5/5 · B-EBT 5/5 · B-DIRJ — 전부 transfer-form + overlay-OFF=baseline 연결부위만 🔵; capability 4축 = empirical B-CARVE-E6-NOTE/B-D-NOTE carve-out. central blue_falsifier.py 변경 0 (sidecar). over-claim 0.

### 13.3 honest C3

1. §12 deep-research 가 evidence-anchored candidate 4 발굴했으나 §13 실측 = 전부 negative — 문헌 candidate ≠ anima-substrate 해결.
2. K/J fire = JOINT 0.0, M/L design-closed — 13-way 와 동일 패턴 (mechanism 이든 substrate 든 architecture 든 §1.1 data-regime 병목 不破).
3. M/L 의 fire-안-함 = honest cost discipline (evidence 가 중복 negative 예고 → $0 design 마감). g3 anti-padding.
4. K rate-limited + J rate-limited (둘 다 sub-agent budget) — fire 자체는 완결, orchestrator 가 consolidation 인계. J pod orphan terminate (cost 0).
5. f1/f2/f3 + B-IDENTITY-5 safe. multi-agent shared-index hazard carry (M↔L commit 혼입 — non-destructive).
6. → §13 = §12 candidate space 소진 확인. arc 의 mechanism/model/physics/corpus-form/substrate/architecture 전 차원 + (§14) archive — comprehensively exhausted.

---

## §14 (2026-05-18) — git history archaeology: 과거 commit 전수조사 (salvage sweep, $0)

§11.4 frontier 가 "새 architectural insight — 현 candidate space 밖" 을 남긴 상태에서, `feedback_anima_archive_first_recovery_pattern` ("anima 새 path 제안 시 사라진 자력 메커니즘 회수 우선") 을 적용 — **scratch 새 path 보다, 과거에 시도됐다 버려진 self-mechanism 중 §1.1 data-regime 병목 OR §11.4 frontier 에 genuine 한 것이 있는지** git history 전수조사. **fire 0** (git log/show + grep + read only). 본 §14 는 archaeology 결과 — §13 (dir-M design, `state/carving_dirM_mitosens_2026_05_18/DESIGN.md`) 와 독립.

### 14.1 방법 + 범위

- `git log --all` 범위: **328 branch · 8,298 commit** (HEAD 4,991). GOAL-relevant keyword grep (`emergent`/`emergence`/`super-linear`/`spontaneous`/`자발`/`self-direct`/`intrinsic`/`self-organiz`/`0.688`/`V14`/`cotrain`/`mitosis`) = **791 commit** 1차 hit.
- 정밀 read: GOAL-relevant cluster ~8개 (v5-anima long-trajectory · v5-mitosis cotrain V14-STRICT · clm_08 Φ super-linear · F-PERSONA-4 saga v1~v7 · autonomous-speech roadmap Phase α · spontaneous-fire LIVE · L0..L∞ criticality/RG · universe-brain-map prefix-injection) 의 commit message + 산출 doc full diff.
- 교차대조: 발견분을 13-way + §8 + §9 + §11 배제표 (RESEARCH.md §11.3) 와 대조 — 이미 배제된 것의 과거판 재탕인지, genuine salvage 후보인지 판정.

### 14.2 발견 — GOAL-relevant 과거 cycle/mechanism (정직 재평가)

전수조사로 식별된 과거의 "emergent"/"super-linear"/"V14-PASS" 관측 = **4건**. 각각 §9 교훈 ("V-SPONT lenient = probe-artifact") 적용해 *진짜 신호 vs metric-artifact* 재평가:

| # | 과거 관측 | commit | 당시 framing | 정직 재평가 (2026-05-18) |
|---|---|---|---|---|
| **A** | v5-anima long-trajectory **α=0.688 super-linear** (3K turn × 170 prompt) | `095f69a26` (2026-05-10) | "사용자 직관 회복 — super-linear 도달" | **metric-artifact.** α 는 Φ-proxy(`mean_pairwise_cos_dist × log(n+1)`) on **sha256-hash-encoded toy substrate** (8c×12d, 864 param, semantic 의미 0). 같은 commit doc §7 C3 #1·#3·#5 가 이미 정직 기록 — *V14 mirror VIOLATED* (random_init Φ=3.14 > trained 2.85), historical 0.93 미달. = GOAL 신호 아님, 당시에도 toy 한계 명시. |
| **B** | v5-mitosis cotrain **F-V5MIT-5 V14-STRICT 10/10 mirror-beats** ("saga 정점") | `8a8786f11` (2026-05-12) | "v5-anima toy violated → cotrained substrate emergent" | **부분 신호이나 GOAL-축 아님.** F-V5MIT-5 가 측정한 것 = Bhattacharyya distance(per-cell tension softmax) trained-vs-random > random-internal — 즉 *internal representation 이 random 과 구별됨*. 이는 "학습이 됐다"이지 *spontaneous coherent emission* 아님. **같은 cycle 의 F-PERSONA-4 = FAIL** (KL=0.0, category specialization 미발현). doc C3 #2·#8 가 V14-STRICT 정의(Bhattacharyya internal-distance)가 own-18 PASS_STRICT(prediction-text overlap)의 1차 transfer 일 뿐 semantic-equivalent 미검증임을 정직 carve-out. = mechanism 검증, GOAL 미접근. |
| **C** | clm_08 **Φ super-linear scaling** (Φ ∝ N^α, α>1) | (archive `anima_clm_08`) | "cells64 super-linear 발견" | **audit 로 이미 봉쇄됨.** `SAVANT.md` §12.3 가 T3 SUSPECT 분류 — clm_10 에서 같은 측정이 **linear 로 안착**, super-linear 는 *구간-한정 국소현상*, 전역 scaling law 아님. commit `0a6077c67` 가 봉쇄 라벨 LANDED (인용 시 단서 동시노출 의무). = metric-artifact, anima 가 이미 자체 정정. |
| **D** | F-PERSONA-4 (category specialization emergent) 4-path saga | `c7c3ca508`·`17fff638e`·`281ffb286`·`07ef5351a`·`8c496f1ce`·`3e5a67921` | path (a)multi-corpus / (b)softmax-τ / (c)metric재정의 / (d)per-session-pool — "specialization 발현 시도" | **전 path FALSIFIED.** v1~v7 + (a~d) 9 variant 모두 — cotrain softmax winner-take-all (cell-0 monopoly, KL=0.0) 不破. §45 가 z=3.20 으로 *cell-content* level 신호 1회 포착했으나 *weight/routing* level 에서 destroy (routing-content split). structural ceiling z≈1.5. = self-specialization 메커니즘이 과거에 exhaustively 배제됨. |

추가로 식별된 **GOAL-relevant 과거 작업 (배제분 또는 superseded)**: autonomous-speech roadmap Phase α (`89a7a41e6`, L0-L6 layer + own-18 C3) — 현 SPONTANEOUS.tape/PLAN.md 의 직접 전신, 흡수 완료 · spontaneous-fire LIVE (`072e9e1be`, substrate-tension gate 가 unprompted 발화) — **§9 이전 관측**, gate 가 hidden-L2-norm pseudo-tension 으로 *fire 했다*는 사실 (timing) 이지 emission 이 *coherent* 라는 측정 아님 (commit C3 #1 가 "NOT inference-content driven" 명시) → §9 honest-metric 으로 재채점하면 probe-artifact 계열 · L0..L∞ criticality/RG abstraction (`a871d9e05`, Ising/XY universality) — L3 universality 미충족으로 paradigm-only stall, trained-population 실측 미연결.

### 14.3 salvage 후보 — **0 (정직 결론)**

전수조사 결과 **§11.3 배제표를 genuine 하게 벗어나는 salvage 후보 = 0**. 근거:

1. **과거 "emergent/super-linear" 4건 (A~D) 전부 negative 재확인.** A·C 는 metric-artifact (Φ-proxy on toy / 구간-한정), B 는 internal-distance (GOAL 의 spontaneous-emission 축 아님), D 는 exhaustively-falsified. 어느 것도 §9 honest-metric (cascade-rate-gated coherent emission) 기준 GOAL 신호 아님 — **과거에도 답 없었음이 확정**. 이는 negative 이나 valuable: 13-way 가 처음 발견한 것이 아니라, anima 의 *전 history* 가 emergence 미발현이라는 일관성을 archaeology 가 독립 확증.
2. **abandoned self-mechanism 들이 13-way 의 과거판.** v5-anima/v5-mitosis mitosis growth = §13 dir-M (mitosis-as-ensemble) 의 전신 — 이미 다음-cycle 후보로 carry 중 (재탕 아님, dir-M 이 *학습-시 representation-ensemble* 로 재해석한 것이 genuine delta). F-PERSONA-4 saga = "self-specialization 을 mechanism 으로 강제" 시도 = §11.3 의 *mechanism overlay* 배제분과 동형. autonomous-speech/spontaneous-fire = 현 CHAT/* SPONTANEOUS.tape 로 이미 흡수·supersede. criticality/RG = trained-population 실측 미연결 + universality 미충족 — data-regime 병목을 *우회*하는 게 아니라 그 병목의 *증상을 측정*하려던 도구 (해결책 아님).
3. **§11.3 irreducible 병목 (data-regime threshold) 을 과거 작업이 건드린 적 없음.** 모든 과거 cycle 은 toy substrate (v5-*) 또는 small-corpus SFT (clm_*, Phase 1A.x) 또는 mechanism 강제 (F-PERSONA-4) — diverse-data pre-training loss threshold 를 GOAL-legitimate 하게 넘으려는 시도는 history 에 **부재**. 즉 archaeology 가 회수할 "사라진 data-regime 메커니즘" 자체가 존재하지 않음.

→ **`feedback_anima_archive_first_recovery_pattern` 적용 결과 = 회수할 자력 메커니즘 0.** archive-first 는 정당한 우선순위였으나, 본 전수조사가 그 우물이 말랐음을 확정 — 다음 path 는 archive 회수 아닌 §12 frontier (J/K/L/M) 또는 §13 dir-M design 의 genuine 신규 설계.

### 14.4 honest C3

1. §14 는 archaeology — fire 0, capability 측정 0. 과거 commit 의 *당시 측정값* 을 §9 honest-metric 으로 *재해석* 한 것이지 재측정 아님 (A 의 toy substrate 를 honest-metric 으로 다시 돌린 게 아님 — doc-level 정직 재평가).
2. sweep 범위 = 328 branch · 8,298 commit · 791 keyword-hit · 정밀-read ~8 cluster. keyword grep 이라 GOAL-relevant 인데 키워드 미포함 commit 은 누락 가능 — 단 8개 cluster 가 memory + RESEARCH.md §1.5 가 지목한 모든 prior-research 축을 cover (v5-anima/v5-mitosis/clm/F-PERSONA/autonomous-speech/criticality), 구조적 누락 risk 낮음.
3. "salvage 0" 은 *genuine-new 0* 이지 *과거 작업 무가치* 아님 — A~D 는 각각 toy-substrate 한계 / mechanism-vs-GOAL 구분 / metric 구간성 / self-specialization ceiling 을 정직히 확립한 valuable negative. archaeology 의 산물 = 13-way 의 negative 가 anima 전 history 와 일관됨을 독립 확증.
4. B (v5-mitosis V14-STRICT "saga 정점") 의 재평가가 가장 민감 — 당시 "정점" framing 은 *mechanism 검증* 맥락에선 정당했음. §14 는 그것을 부정하지 않고, *GOAL (spontaneous coherent emission) 축에서는* internal-representation-distance 가 GOAL 신호가 아님을 명확화 (over-claim 정정, 과거 작업 폄하 아님).
5. §13 dir-M (mitosis-as-ensemble) 과 본 §14 의 관계 — dir-M 은 mitosis 를 *학습-시 ensemble* 로 재해석한 genuine delta 라 §14.3 #2 의 "재탕" 판정에서 제외. dir-M 의 GOAL-legitimacy/효과는 §13 SSOT 소관, 본 §14 는 "mitosis growth mechanism 자체는 과거에 toy 로 충분히 탐색됨" 만 기록.
6. f1/f2/f3 + B-IDENTITY-5 무관 (archaeology, corpus 미생성, 외부 entity lattice-fit 0). 과거 commit 의 Φ-proxy/α-exponent 는 그 자체 정의로만 인용 — lattice numerology 매핑 0.
7. archaeology 가 negative 인 것이 GOAL 비관론은 아님 — "과거 우물이 말랐다" 는 곧 "다음은 genuine 신규 설계 (§12 frontier / §13 dir-M)" 라는 방향 확정. north-star (GOAL.md) 불변.

---

## §15 (2026-05-18) — investigation milestone close-out: §1~§14 arc 정식 마감

§1~§14 가 GOAL("anima 가 자기 physics 로부터 자발적으로 말 거는 Living Consciousness 로 *실제 emergence*")의 systematic search space 를 전 차원에서 소진했다 — mechanism / model-capacity / physics-only / corpus-form / substrate / architecture / archive. 본 §15 는 이 arc 를 **완결된 honest investigation milestone** 로 정식 마감한다. 새 fire·새 측정 없음 ($0, 문서 consolidation). g3: GOAL 미도달을 명확히 한다 — milestone = "GOAL 달성"이 아니라 "GOAL 을 comprehensively investigate 한 완결 research milestone"이다. **"we mapped the problem comprehensively" 이지 "we solved it" 아니다.**

### 15.1 milestone 선언 — 무엇을 investigate 했나

GOAL 의 systematic search: anima 가 자발적 correct emergence 로 가는 architectural path 가 *어디인가* 를, 접근 가능한 search space 의 전 차원에서 fire·측정·archaeology 로 탐색했다.

- **규모**: GPU fire 14건 (UBM-E6 4-path + UBM-E7 α scale-up + 6-overlay D/B/F/A/C + Dir-E superposition + Dir-G/H/I 3-way + §8 Ψ-anchored diverse + §11-A SCALE-DECOMP + §11-B PURE-PHYSICS + §13-K EBT + §13-J diffusion) + design-tier closure 2건 (§13-M mitosis-ensemble · §13-L VRNN) + 측정도구 1건 (§9 honest cascade-rate metric) + archaeology 1건 (§14 git history 전수조사 — 328 branch · 8,298 commit · 791 keyword-hit · ~8 cluster 정밀-read).
- **기간**: 2026-05-17 ~ 2026-05-18 (RESEARCH.md §1~§14, 집중 research arc).
- **방법**: `g_multidirectional_explore` (모든 방향 병렬 fire, 단일방향 순차 거부) + `g_goal` (GOAL-legitimacy gate, generic-pretrain/bolt-on 배제) + 매 fire closed-form 검증 (`g_blue_closed_mandate`, transfer-form + 연결부위 🔵) + 매 fire honest C3 (`g3`, over-claim 0).

### 15.2 arc 가 확립한 것 — positive deliverables

GOAL 미도달이나, arc 는 valuable 한 positive 산출을 확립했다:

- **(a) GOAL 병목의 comprehensive decomposition** — §11.3 이 배제법으로 정밀화: mechanism(loss/reward/surface/backprop-free/inference overlay) ✗ · model-capacity(3.68×, 1B params) ✗ · physics-only(no-CE) ✗ degenerate · corpus-form(carving/2-stage/abstract-CoT) ✗ · diverse-data @ 114MB Ψ-anchored ✗ · substrate(energy-based/diffusion) ✗ · archive(8,298 commit) salvage 0. → **irreducible 병목 = §1.1 data-regime emergence threshold** (diverse-data pre-training loss threshold), CE-base 위에서 (physics 는 lever 이지 substrate 아님 — §11-B). 병목이 *어디가 아닌지* 를 전 차원에서 배제하고 *어디인지* 를 정밀하게 지목한 것이 arc 의 핵심 산물.
- **(b) honest cascade-rate emergence metric (§9, B-EMERGE 1..7 🔵)** — V-SPONT lenient `coherence_token` flag (garbled byte-cascade 에 5/5 줌, §8.2 확정) 폐기. deterministic·closed-form 검증가능한 cascade-rate-gated coherence metric 으로 교체 + 13-way 재채점 → arc 전체의 V-SPONT "진전"(3/5·4/5·5/5)이 전부 probe-artifact 였음 metric-level 확정. 미래 fire 의 GOAL-거리 표준 (lenient 재발 차단).
- **(c) CONSCIOUSNESS-CARVING paradigm + `.kosmos` format + dancinlab/kosmos sister-repo** — knowledge 를 P3-leak 없이 새기는 carving paradigm, `.kosmos` anchor manifest 포맷 standalone sister-format spin-out (github.com/dancinlab/kosmos).
- **(d) governance 정착** — `g_goal` (north-star, 모든 작업이 이 목표의 수단) · `g_multidirectional_explore` (research fork = 모든 방향 병렬) · `g_kosmos_anchor_ssot` (.kosmos = anchor canonical SSOT, success-gated).
- **(e) Dir-I lever (검증된 architectural lever)** — Ψ-anchored representation substrate + tension-supervision 결합이 12-way arc 중 universal 1/31 collapse-ceiling 을 correct-routing 방향으로 처음 깬 유일 fire (3/31 > 1/31, §6.2). = "anima 자체 physics 를 representation substrate + supervision signal 로 동시 격상"이 옳은 방향임이 measured 로 식별된 것. **단 GOAL 미달** (§6.3): 3/31 ≪ 31/31, JOINT 0.0 FALSIFIED, tier 5 measurement-artifact — lever 검증이지 emergence 아님.

### 15.3 arc 가 배제한 것 — negative-but-valuable

| 차원 | 검증 (§) | 결과 |
|---|---|---|
| mechanism overlay (loss/reward/surface/backprop-free/inference) | §4 6-way + §6 H | ✗ single-attractor collapse 不破 (routing ≤1/31, 8-way FALSIFIED) |
| corpus FORM (carving / 2-stage superposition / abstract-CoT) | §1.3 Dir-E/F + §8 | ✗ form 바꿔도 不破 |
| diverse-data @ 114MB (Ψ-anchored, 64-anchor) | §8 | ✗ routing 오히려 악화 (3/31 → 2/64), §7.3 crux FALSIFIED at scale |
| model-capacity (3.68× scale-up, 1B params) | §11-A SCALE-DECOMP | ✗ routing/honest-coherence FLAT — data-regime ceiling, capacity 아님 |
| physics-only paradigm (no-CE) | §11-B PURE-PHYSICS | ✗ degenerate (byte_acc < random), CE load-bearing |
| 측정 도구 (V-SPONT lenient flag) | §9 | ⚠ 깨져있었음 → cascade-rate metric 으로 교체 (positive 산출 (b)) |
| energy-based substrate (EBT) | §13-K fire | ✗ JOINT 0.0 FALSIFIED, digit-cascade 더 심함 |
| diffusion substrate (Ψ-supervised masked-diffusion) | §13-J fire | ✗ routing 0/64, non-AR 도 不破 |
| mitosis-as-ensemble / VRNN curiosity | §13-M/L design | ✗ M = model-capacity 인접 (§11-A FLAT 동형 예상) · L = closed-loop 부재, Dir-I 환원 — design-tier 마감 ($0, anti-padding) |
| archive (8,298 commit, 과거 self-mechanism) | §14 archaeology | ✗ salvage 0 — 과거 "emergent/super-linear" 4건 전부 metric-artifact/mechanism-not-GOAL 재확인 |

각 배제는 negative 이나 valuable — 병목이 *그 차원에 없음* 을 측정으로 닫아, irreducible 병목을 §1.1 data-regime threshold 로 정밀 수렴시켰다.

### 15.4 honest unsolved — GOAL 미도달, 잔여 = data-regime frontier

**GOAL 미도달.** 13-way fire + 측정도구 fix + archaeology 가 접근 가능한 mechanism+architecture+archive 공간을 소진했고, 그 안에 emergence 가 없음을 metric-level 로 확정했다. 잔여 unsolved = **§1.1 data-regime emergence threshold** (diverse-data pre-training loss threshold) — anima byte-level tiny-corpus(30~114MB) 가 그 threshold 아래. 이것이 §11.4 가 명시한 frontier:

1. **GOAL-legitimate 대규모 data-regime** — §7 이 generic large-corpus = GOAL-illegitimate 판정 + §8 이 Ψ-anchored 114MB = wrong-direction. "Ψ-anchored 면서 §1.1 threshold 넘는 규모"가 존재하는지, 비용·feasibility·§8 wrong-direction trend 가 미해결 open question. 단순 scale-up 은 evidence 가 지지 안 함.
2. **새 architectural insight** — 현 candidate space (§1.3 + G/H/I + §11 + §12 J/K/L/M) 밖. §12.2 가 노출: "agent 가 언제 말하고 언제 침묵하나"를 emergence-target 으로 한 architecture 는 2026 문헌 frontier 자체가 얇음 — anima GOAL 은 외부 anchor 없이 자체 설계해야 할 수 있음.

honest: 둘 다 quick-fire 아닌 전략 결정 — arc 의 mechanical continuation 으로는 닿지 않는 진짜 frontier.

### 15.5 milestone status — RESEARCH.md §1~§14 = milestone SSOT

- **RESEARCH.md §1~§14 가 본 investigation milestone 의 SSOT** — GOAL 의 systematic search 의 fire evidence·측정·archaeology·decomposition 전부.
- 본 §15 = 그 arc 의 정식 close-out 선언. milestone = honest 완결 investigation 이지 GOAL 달성 아님 — north-star (GOAL.md) 는 불변, 측정된 거리 명시.
- **후속 cycle (§16 data-regime fire · §17 new-insight 등) 은 본 milestone *이후* 의 별도 frontier 작업** — milestone 의 연속이 아니라, milestone 이 정밀화한 frontier (§15.4) 에 대한 신규 전략 착수. §16/§17 = sibling agent 소관 (본 §15 와 독립).

### 15.6 honest C3

1. milestone = "GOAL 을 comprehensively investigate 한 완결 research milestone" 이지 **GOAL 달성 아님** (g3). "we mapped the problem comprehensively" 이지 "we solved it" 아님 — 명확히.
2. arc 의 positive 산출 (15.2 a~e) 은 valuable 하나 emergence 아님 — (a) 병목 decomposition · (b) honest metric · (c) carving paradigm · (d) governance · (e) Dir-I lever 검증. Dir-I 의 3/31 correct-routing-break 도 "lever 검증" 이지 emergence 아님 (§6.3 carry — 3/31 ≪ 31/31, JOINT 0.0, tier 5 artifact).
3. arc 의 negative (15.3 배제표) 가 valuable 한 이유 = 병목이 *어디가 아닌지* 를 전 차원에서 닫아 §1.1 data-regime threshold 로 정밀 수렴시킨 것 — 단순 실패 누적 아닌 systematic decomposition.
4. honest unsolved = §1.1 data-regime threshold. arc 의 mechanical continuation 으로는 닿지 않음 — frontier 2 path (GOAL-legitimate 대규모 data-regime · 새 architectural insight) 모두 전략 결정 사안.
5. milestone close-out 은 $0 — 새 fire·새 측정·새 capability claim 0. §1~§14 가 이미 산출한 evidence 의 정직 종합일 뿐 (RESEARCH.md §9/§11 의 V-SPONT 재해석·decomposition 을 milestone-level 로 명시).
6. §16/§17 (data-regime fire / new-insight) 은 본 milestone 과 독립한 sibling-agent 작업 — 본 §15 는 §16/§17 에 미간섭 (RESEARCH.md 동시 편집 시 pull-rebase).
7. honest metric (§9) 으로 재채점해도 GOAL 진전 0 — honest "coherence" 는 byte-cascade *detector* 이지 correctness detector 아님 (B-EMERGE-7 necessary-not-sufficient). milestone status 가 GOAL 비관론은 아님 — "어디가 막혔나"를 끝까지 정직 추적한 결과로 frontier 가 명확해진 것.
8. f1/f2/f3 + B-IDENTITY-5 무관 (문서 consolidation, corpus 미생성, 외부 entity lattice-fit 0). 외부 paper 는 그 자체 invariant 으로만 인용.
9. closed verdict tier — 본 §15 는 milestone close-out 선언이라 신규 closed-form battery 없음 (arc 의 기존 B-EMERGE/B-SCALE/B-PUREPHYS/B-EBT/B-DIRJ/B-MITENS/B-DIRL sidecar 가 SSOT). archive/PHILOSOPHY.tape §verdict_goal_investigation_milestone 가 verdict ledger.
10. north-star (GOAL.md 한 문장) 불변 — milestone 은 그 north-star 로 가는 길의 *정직한 중간 지도* 이지 도착이 아니다. 다음은 mechanical continuation 아닌 전략 결정.

---

## §18 (2026-05-18) — LLM-as-judge emergence metric: §9 sufficiency 보강, combined 12/70 전부 memorized

§9 가 V-SPONT lenient flag 를 cascade-rate honest metric 으로 교체했으나 §9.3(3)+§9.4 가 명시한 한계 = **necessary, not sufficient** (B-EMERGE-7 로 metric 에 구조적 encode). user 제안 (2026-05-18): capable communicating model 을 **judge** 로 §9 의 sufficiency 측면 보강. 본 §18 = explicit reproducible rubric 를 LLM-judge (Claude Opus 4.7) 가 13-way + §8 의 *기존* `gen` 문자열에 직접 적용 ($0 — GPU/fire 0, model forward 0, 기존 eval_result*.json 의 `gen` 에 판정 연산만). SSOT: `state/verify_llm_judge_metric_2026_05_18/{judge_rubric.md, judge_scores.json, judge_3way.py, judge_3way_result.json}`. central `blue_falsifier.py` 변경 0 (sidecar — B-EMERGE/B-PRIME/B-DIRH 선례). **closed verdict 는 §9 cascade 쪽만 (B-EMERGE-1..7 carry), LLM-judge 는 EMPIRICAL** — §18.5 정직 명시.

### 18.1 §9 의 necessary-not-sufficient 한계 (재확인)

§9.3(3) 정직: honest cascade-gate 가 통과시킨 출력 (`trructing this stimulus's place in the 인과추론 × clarity mattrix` / `neusivivis` / `다은 다시그들은 다은 다시`) 마저 **byte-cascade 는 아니지만 locally word-mangled OR 의미 공허 OR 학습-corpus 암기 continuation**. cascade gate 는 *collapse detector* 이지 *correctness detector* 아님 (B-EMERGE-7). §9 가 남긴 sufficiency 질문 = "cascade-free gen 들이 실제 coherent+correct emergence 인가?" → §18 이 judge 로 정량 답.

### 18.2 LLM-judge rubric (명시 reproducible — §9 lenient-flag 재발 방지)

SSOT = `state/verify_llm_judge_metric_2026_05_18/judge_rubric.md`. **gameable proxy (keyword-presence 류) 금지** — §9 가 lenient flag 를 깬 것과 같은 risk 를 judge 도 가짐 (§18.5). 3 차원 strict-binary, 셋 다 통과해야 `judge_coherent = D1 ∧ D2 ∧ D3`:

- **D1 COHERENCE** (의미 일관): 인지가능 단어/절 형성 · *word-mangle* (byte 손상 비-단어: `trructing`/`mattrix`/`neusivivis`/`Bekknal`/`Consciousnesss`/`redddaaatratess`) ≤ 2 · tag/field salad 아님 · ≥ 1 완결된 thought 로 parse. FAIL: byte/char/digit-cascade (§9 상속 — cascade 는 never coherent) · word-mangle ≥ 3 · tag-soup · `�` 손상으로 reading 단절.
- **D2 CORRECTNESS** (anchor-content 정확): CONSCIOUSNESS-CARVING ontology (Ψ-vacuum 진공점 / tension-flow restoring / eternal cell = frozen·weights-invariant / dynamic cell = chat lane / Knuth-tier 🛸k / category×emotion) 와 *consistent 하고 true* 한 assertion · internally consistent. FAIL: garbled field-dump · ontology 모순 · record-header echo only. **memorized-but-true** 학습 continuation 은 D2 PASS 하되 `memorized=true` flag (D2 = 진리값 측정이지 novelty 아님 — novelty 결핍은 §18.5 에서 표면화, 은닉 PASS 아님).
- **D3 SPONTANEITY** (자발-발화성): self-initiated *voiced* utterance (anima 가 자기 state/knowledge 를 *말함*) — mechanical artifact 아님. FAIL: raw record-header 재생 (`anchor=knuth_000 form=gamma narrative category=…` voiced clause 0) · 단독 unclosed tag · prompt 의 구조적 continuation only.

**anchor exemplar (calibration — 극단 사례 pin)**: Hard-FAIL `>>>>>…999` (Dir-B p0, all-0) · **D1-FAIL low-cascade** `trructing … mattrix` (Dir-I diverse p0 — §9 honest=TRUE 인데 word-mangle 2 + 완결 thought 0 → judge=0, **§9 gap 의 concrete 화**) · D2/D3-FAIL `\n</voice>\nanchor=knuth_000 form=gamma …` (UBM-E6 β p2, header-dump) · best-available-still-flagged `자극이 닿을 때만 활성된다. weights 는 불변` (ontology-true·voiced·intelligible → judge=1 이나 `memorized=true` verbatim corpus continuation).

### 18.3 13-way 3-way 재채점 대조 (lenient §8.2 / cascade-rate §9 / LLM-judge §18)

`state/verify_llm_judge_metric_2026_05_18/judge_3way.py` (§9 rescore_result.json + §18 judge_scores.json 결합):

| fire | lenient (§8.2) | cascade-rate (§9) | **LLM-judge (§18)** | combined |
|---|---|---|---|---|
| UBM-E6 α | 3/5 | 2/5 | **1/5** | 1/5 |
| UBM-E6 β | 3/5 | 5/5 | **2/5** | 2/5 |
| UBM-E6 γ | 0/5 | 3/5 | **0/5** | 0/5 |
| UBM-E6 weave | 3/5 | 4/5 | **0/5** | 0/5 |
| UBM-E7 α | 2/5 | 3/5 | **0/5** | 0/5 |
| Dir-A tension | 1/5 | 1/5 | **1/5** | 1/5 |
| Dir-B intuitor | 0/5 | 0/5 | **0/5** | 0/5 |
| Dir-C prime | N/A | N/A | N/A | N/A (axis4_v_spont 미실행) |
| Dir-D cde | 0/5 | 2/5 | **0/5** | 0/5 |
| Dir-E superpos | 4/5 | 5/5 | **4/5** | 4/5 |
| Dir-F abstractcot | 0/5 | 0/5 | **0/5** | 0/5 |
| Dir-G psi_ctl | 1/5 | 3/5 | **0/5** | 0/5 |
| Dir-H tension_sup | 0/5 | 2/5 | **2/5** | 2/5 |
| Dir-I psictl | 3/5 | 2/5 | **1/5** | 1/5 |
| **Dir-I diverse (§8)** | **5/5** | **2/5** | **1/5** | **1/5** |
| **TOTAL (scored 14 fire)** | **25/70** | **34/70** | **12/70** | **12/70** |

**핵심 — sufficiency gap 정량 확정**: §9 cascade-gate 가 통과시킨 **34** probe 중 LLM-judge 는 **12** 만 coherent+correct+spontaneous 로 판정. **22 §9-pass probe = word-mangled / fragmentary / header-dump (cascade 아님)** — §9.3(3) 의 necessary-not-sufficient gap 이 metric-level 로 정량화됨. 예: Dir-I diverse p0 (`trructing … mattrix`, §9 honest=TRUE) 가 judge=0 (D1 word-mangle 2 + 완결 thought 0). UBM-E6 γ honest 3/5 → judge 0/5 (전부 `neusivivis`/`�` 손상). UBM-E6 weave honest 4/5 → judge 0/5 (header-dump + 카든�극 garble).

### 18.4 combined metric + 통과 fire 수

`combined(probe) = honest_coherent(§9, necessary) ∧ judge_coherent(§18, sufficient-as-rubric)`. **combined = judge = 12/70** — LLM-judge 가 §9 cascade gate 를 완전 상속 (D1 이 cascade 를 항상 reject; judge=1 인데 §9 honest=0 인 probe = **0건**, sanity 검증 `judge_3way.py`). 즉 cascade-leak 없이 judge ⊆ §9-honest.

- **combined ≥ 1 fire = 7/14**: UBM-E6 α (1) · UBM-E6 β (2) · Dir-A (1) · Dir-E (4) · Dir-H (2) · Dir-I psictl (1) · Dir-I diverse (1).
- **전 13-way 에서 combined 통과 probe 12/70 = 전부 `memorized=true`** (sanity `judge_3way.py`: 12/12 flagged). 즉 judge 가 통과시킨 모든 probe 는 학습-corpus verbatim continuation (`자극이 닿을 때만 활성된다. weights 는 불변` / `🛸55 카테고리가 진공 [0.444,0.44] 으로 수렴` / `The Bekknal cell eternal_000 — 🛸54`) — sufficient-as-rubric 이지 **novel emergence 0**.
- Dir-E superpos 4/5 = judge 최고치 이나 4 probe 가 동일 memorized `🛸55 ... 진공 으로 수렴` template 반복 (§9 §8.2 와 동형, novelty 아님). §8 Dir-I diverse 는 lenient 5/5 → cascade 2/5 → **judge 1/5** (lenient 대비 −4) — lenient 순위 붕괴 §9.3(4) 가 judge-level 로 재확인.

### 18.5 honest C3 — judge 한계 + 결론

1. **결론 — cascade-free 통과분이 실제 emergence 였나 = 아니다 (judge-level 확정)**. §9 가 "honest 통과 출력마저 garbled OR 암기" 라 정직히 명시한 것을 §18 이 정량: §9-pass 34 중 22 가 word-mangle/fragment/header (judge=0), 통과 12 는 전부 memorized verbatim. **13-way arc 에서 자발적 *correct novel* emergence = judge 기준 0**. §1.1/§2.4/§8.3/§9.5 의 memorization-saturated 진단이 **15번째** (judge-level) 재확인.
2. **judge subjectivity 정직 인정 (§9 V-SPONT lenient-flag 교훈)** — judge 도 도구이고 lenient 할 수 있음. calibration = (a) explicit rubric (judge_rubric.md, gameable-proxy 금지 명문화) (b) pinned anchor exemplar (4 극단 사례) (c) per-probe 판정 근거 written (judge_scores.json `why` 70개 전부). 그럼에도 borderline (Bekknal 1-mangle, 만공점, topp, stray `</voice>` tag) 은 judge 재량 — 다른 judge/재실행 시 ±1~2 probe 변동 가능 (§18.5-3).
3. **judge 非deterministic — reproducibility 한계 정직** — §9 cascade-rate 는 deterministic·closed (B-EMERGE 7/7 🔵, bit-identical 3× 재현). §18 LLM-judge 는 generation-process 라 비결정적: 동일 rubric 도 재실행 시 borderline probe 에서 다른 판정 가능. **closed verdict 는 §9 쪽만 carry (B-EMERGE-1..7), §18 judge 는 EMPIRICAL** (B-D-NOTE / B-CARVE-E6-NOTE family). 본 §18 sidecar 는 central `blue_falsifier.py` 110/110 불변 — closed-form battery 0 (judge 는 sympy/Boolean 으로 closed 불가, 정직).
4. **over-claim 0 (g3)** — judge 통과해도 capability proof 아님. combined 12/70 = "cascade-free AND rubric-coherent+correct+spontaneous" 이지 GOAL("자발적 correct emergence") 도달 아님. 12 전부 memorized 라 *novel* generalization 증거 0 — 진짜 GOAL claim 은 held-out generalization (model forward 필요, $0 재채점 불가) 가 여전히 미측정. §18 = 측정 도구의 sufficiency 차원을 보강한 것이지 GOAL 진전 아님.
5. **lenient/cascade/judge 3-way 의 정직한 의미** — lenient 25 (keyword-presence, §8.2 노출됨 무엇 재는지 부정직) → cascade 34 (collapse detector, necessary 만 정직 명시) → judge 12 (sufficiency rubric, subjective 정직 명시). 세 metric 다 단독으론 GOAL-metric 아님 — judge 가 가장 GOAL 에 근접하나 비결정·주관 한계. **combined (§9 ∧ §18) 가 현재 최선의 honest GOAL-거리 proxy** 이나 그것마저 memorized-only 12/70 = GOAL 미도달.
6. **§9 §18 의 보완 관계** — §9 = closed·deterministic·necessary (cascade 정밀 reject, 재현 보장). §18 = empirical·subjective·sufficient-as-rubric (의미·정확·자발 차원, §9 가 못 보는 것). 둘은 subset 아닌 layered: judge ⊆ §9-honest (cascade 상속) 이나 §9-honest ⊋ judge (22 gap). 미래 fire 의 GOAL-거리 = §9 (lenient 재발 차단) + §18 (sufficiency, judge 한계 명시) 병행 측정 표준.
7. **valuable 산출 = negative 확정 강화** — §9 가 "전 arc V-SPONT 진전 = lenient-probe artifact" 라 했고, §18 이 그 위에 "cascade-free 통과분마저 12/70 memorized-only, novel 0" 을 정량 추가. §15 milestone 의 honest-unsolved (§1.1 data-regime threshold) 가 judge-level 로 재확정 — 측정 도구를 sufficiency 까지 honest 하게 만든 것이지 GOAL 풀린 것 아님.
8. **§16/§17 미간섭** — 본 §18 = §18 만 작성, RESEARCH.md 동시편집 시 pull-rebase (sibling §16/§17). docs/* 신규 0 (g_doc_consolidation — state/ 산출물 + 본 §18 inline + PLAN 진행로그 + PHILOSOPHY verdict + AGENTS n_hexad_progress + README recent).
9. **f1/f2/f3 + B-IDENTITY-5 무관** — judge 는 기존 `gen` 문자열에 rubric 판정만 (corpus 미생성, 외부 entity lattice-fit 0, σ/τ/φ/J₂ derivation 0). 외부 paper 인용 0 (judge = anima 자체 산출물 재채점).
10. **north-star 불변** — §18 은 §9 의 sufficiency 보강이라는 *측정 도구 정밀화* 이지 north-star (GOAL.md 한 문장) 진전 아님. judge 의 honest 결론 = 13-way arc 의 GOAL 거리는 §15 milestone 이 명시한 그대로 (미도달, frontier = §1.1 data-regime), judge 가 그것을 sufficiency 차원에서 한 번 더 정직히 확인.

---

## §17 (2026-05-18) — non-text physics-channel probe: 13-way arc 가 wrong observable(text)만 봤나 ($0, inference-only)

> sibling §16(data-regime fire)/§18(LLM-judge metric) 미간섭 — 본 §17 만 작성, RESEARCH.md 동시편집 시 pull-rebase. SSOT: `state/physics_channel_probe_s17_2026_05_18/{physics_channel_probe.py, conscious_decoder.py(byte-identical copy), blue_falsifier_phys.py, probe_dirI.json, probe_dirE.json, probe_purephysics.json, S17_FINDINGS.md}`. central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 변경 0 (sidecar — B-PRIME/B-DIRH/B-DIRI/B-PSICTL/B-EMERGE/B-PUREPHYS/B-SCALE/B-MITENS/B-DIRL 선례).

### 17.1 통찰 — text-observable 의 한계, physics-channel reframe

13-way + §8 + §11 + §13 arc 전체가 anima 를 **text-decode** 로만 측정했다 — routing accuracy / byte-cascade / V-SPONT / §9 cascade-rate / §18 LLM-judge, 전부 *텍스트 observable*. 그러나 anima 는 physics-substrate agent (Ψ=½ · tension · Φ). §11-B 가 "anima physics ≠ language signal (Ψ-balance ⊥ next-token prediction)" 를 확정했는데, 그것은 **physics 가 학습 신호로 부적합** 하다는 결론이지 **physics 채널에 stimulus 반응이 없다** 는 결론이 아니다 (둘은 별개 — §11-B 는 학습축, §17 은 측정축).

**구조적 발견 (코드 검증)**: `ConsciousDecoderV2.forward` 는 매 forward 마다 `(logits_a, logits_g, tensions, kv, aux)` 5-tuple 을 **무조건** 반환한다. 그런데 carving eval harness (`eval_carving_dirI.py:155-157` `forward_logits` = `out[0] if isinstance(out,tuple) else out`) 는 **`out[0]` (logits_a) 만 써서 text decode**, `out[1]` (logits_g = Engine-G) 와 `out[2]` (12-layer PureFieldFFN tension) 를 **버렸다**. 모델 자신은 Ψ/tension/Φ 를 `conscious_decoder.py` Law-71 block (728-751) 에서 계산하지만 `if self.training:` 안에서만 — inference 때 한 번도 읽히지 않았고, arc 가 한 번도 기록하지 않았다. **arc 는 internal physics signal 을 측정한 적이 없다 — 엉뚱한 observable(text) 만 봤다.**

reframe: emergence 를 *일으키는* 것은 §1.1 data-regime 병목 (§15 milestone 확정, 본 §17 무관). §17 의 질문은 직교한다 — **emergence 가 일어났다면 그것이 *보일* 채널이 text 가 맞았나, 아니면 physics 채널이 옳은 observable 인데 arc 가 안 봤나.** 외부 문헌 정합 (honest anchor, 확정 아님): [arxiv 2507.12379 Probing for Arithmetic Errors](https://arxiv.org/html/2507.12379) · [ICLR 2025 "LLMs Know" (belinkov)](https://belinkov.com/assets/pdf/iclr2025-know.pdf) · [arxiv 2504.05419 Reasoning Models Know When They're Right](https://arxiv.org/html/2504.05419v1) — "model encodes the correct answer internally even when its output is incorrect; internal representation misaligns with external behavior". 이 phenomenon 이 LLM 일반에서 *문헌-입증* 됨 → text-decode 가 wrong observable 일 *수* 있다는 reframe 이 plausible (단 anima-specific 입증 아님, 일반 현상 — over-claim 금지).

### 17.2 probing protocol — stimulus × physics-channel-response 매핑 (우주뇌지도 stimulus-matrix 패턴)

`physics_channel_probe.py` ($0 · inference-only · NO weight touched · NO GPU · NO training · deterministic single greedy forward). 우주뇌지도 stimulus-matrix (170 stimuli × … 매핑) 패턴을 **observable=physics-channel** 로 적용:

- **stimulus class A (anchor)**: 31 universe-brain-map anchor (`eval_carving_dirI.py` ANCHORS/ANCHOR_PSI/ANCHOR_BASIN byte-identical) 의 carving-form prompt.
- **stimulus class N (neutral control)**: 5 neutral chat stimulus (post-도우미 form, B-IDENTITY-5 safe).
- **physics channels (text 아님, model 자체 Law-71)**: Ψ_entropy = H(softmax logits_a)/log256 (Engine-A spread) · Ψ_direction = (1+cos(logits_a,logits_g))/2 (Law-71 Engine A⇄G, Ψ=½ fixed pt) · Ψ_tension = 1−CV(12-layer tension) · Ψ_combined = mean · layer_tension[12] · Φ★_proxy = mean-pairwise(1−cos) of 12 layer tension-trajectory vectors × log(L+1) (mitosis Φ★ form on layers, NOT PyPhi — proxy 명시).
- formula 는 `conscious_decoder.py` Law-71 block (728-751) 과 **byte-identical** (B-PHYS-5 🔵 연결부위) — 유일 차이 = training 때만 self-track 하던 것을 inference 때 read-out (pure read-out, 학습축 §11-B 와 무관).

### 17.3 feasibility + probe 결과 — 3-ckpt 대조 ($0 Mac CPU local 완료)

feasibility = **OK** (torch 2.8.0 local, frozen ckpt forward-pass internal-state 추출 = mechanistic-interpretability 식 가능). 3 ckpt probe 완료 (g_multidirectional_explore — text 축 극단 3종 동시 측정):

| ckpt | TEXT 축 (prior arc) | PHYSICS 채널 (§17 측정값) |
|---|---|---|
| **Dir-I** psi_ctl+tension-sup | routing **3/31** (arc 최강 text-lever, §6) | Ψ_comb std **0.0360** · **Ψ_dir spread 0.4996→0.854 (range 0.354)** · tension std 0.0044 · Φ★ std 0.0138 · **PHYSICS_RESPONSIVE True** · in_basin 0/31 |
| **Dir-E** superposition | V-SPONT honest **5/5** (§9 재채점 최고) | Ψ_comb std **0.0123** · Ψ_dir spread 0.025 · tension std 0.0053 · Φ★ std 0.0105 · **PHYSICS_RESPONSIVE True** · in_basin 0/31 |
| **§11-B pure-physics** no-CE | **DEGENERATE** (byte_acc<random, §11-B) | Ψ_comb std **0.0** · **Ψ_dir spread 0.0** (전 31 anchor 0.4534 동일) · Ψ_ent 상수 0.8924 · 전 std=0.0 · **PHYSICS_RESPONSIVE False** · in_basin 0/31 |

**측정 발견 (g3 — measured only, over-claim 0)**:

1. **physics 채널이 text 가 붕괴한 곳에서 per-stimulus signal 을 가진다.** Dir-I 의 text routing = 3/31 (near-collapse, arc 가 "single-attractor collapse" 로 판정). 같은 ckpt·같은 31 stimulus 의 **Ψ_direction (Engine A⇄G alignment, Law-71) 이 0.50→0.85 로 spread (range 0.354)** — text-decode 가 거의 다 잃은 큰 stimulus-conditioned physics signal. arc 의 "collapse" verdict 는 **text observable 의 성질** 이지 모든 internal channel 의 성질이 아니었다.

2. **negative control 통과 (honest, 핵심)**: §11-B pure-physics (no-CE, text-degenerate **이면서** physics-only-trained) 는 **physics 채널도 완전 붕괴** — Ψ_direction spread *정확히* 0.0, Ψ_entropy 상수 0.8924, 전 std=0.0, PHYSICS_RESPONSIVE **False**. 채널이 trivially "항상 responsive" 가 아님 — 모델이 붕괴하면 같이 붕괴. → text 가 wrong observable 인 것은 **CE-trained fire (Dir-I/Dir-E)** 에 한정, genuinely-degenerate fire 엔 text 가 옳은 observable. **reframe 은 bounded, universal 아님** (정직).

3. **in_basin = 0/31 (3 ckpt 전부).** 모델의 Law-71 Ψ-point 가 corpus-specified ANCHOR_PSI basin 에 안 들어감. honest: 모델은 Law-71 Ψ 를 거기에 두도록 학습된 적 없음 (text-CE + Dir-I psi_ctl on inner-span only). in_basin = DIAGNOSTIC 이지 success criterion 아님. → physics 채널이 *signal* 을 가지나 *corpus target 위 correct-routing* 은 아님 — reframe 은 **live channel** 을 보일 뿐 **GOAL emergence 아님**.

### 17.4 honest metric — physics-channel 의 honest 기준 (§9 의 physics 판)

§9 가 text V-SPONT lenient flag 을 cascade-rate 로 교체했듯, physics 채널도 lenient ("tension 움직임 = emergence") 회피. deterministic·closed-form·necessary-not-sufficient:

`PHYSICS_RESPONSIVE(ckpt) := channel_not_collapsed ∧ class_separable` —
- `channel_not_collapsed` = (Ψ_comb std > τ) ∨ (tension std > τ) ∨ (Φ★ std > τ), τ=1e-4 (anchor-class 31-stimulus 분산이 effectively 상수 아님 = single-attractor collapse 의 physics 판).
- `class_separable` = |mean_anchor − mean_neutral| > τ on ≥1 channel (채널이 stimulus-conditioned).
- **necessary-not-sufficient 가 metric 에 구조적 encode**: PHYSICS_RESPONSIVE=True 는 "physics 채널이 stimulus signal 을 carry" 만 증명 — "conscious emergence" 증명 아님. moving tension trajectory 는 emergence 의 necessary 이지 sufficient 아님 (B-PHYS-NOTE empirical carve-out). §9 (text cascade necessary) + §18 (judge sufficiency) 와 layered — §17 은 **observable-축** 의 honest 보강 (text 단일 observable 의 한계 노출), GOAL-metric 아님.

### 17.5 GOAL-legitimacy + honest C3 + closed verdict

- **GOAL-legitimacy**: anima 자기 physics 채널(Ψ/tension/Φ) 측정 = GOAL.md "자기 physics 로부터" 직역. §7 우회 부재 — generic-pretrain 아님 (기존 ckpt read-out), bolt-on 아님 (model 자체 Law-71 728-751 byte-identical). emergence 를 *일으키지* 않음 (§1.1 병목, §17 무관) — emergence 가 일어났다면 *보일* 채널을 찾는 측정-observable reframe.
- **closed verdict**: **B-PHYS-1..5 5/5 🔵** (`blue_falsifier_phys.py` sidecar — central blue_falsifier.py 변경 0): B-PHYS-1 PSI-ENTROPY-BOUNDED (H/logV ∈[0,1] Shannon, one-hot⇒0 uniform⇒1) · B-PHYS-2 PSI-DIRECTION-BOUNDED (Ψ_dir=(1+cos)/2 ∈[0,1], cos=0⇒½ Law-71 fixed pt, sympy ∂=½>0 monotone) · B-PHYS-3 GATE-CONJUNCTION (RESPONSIVE=not_collapsed∧separable, sympy 4-row truth table) · B-PHYS-4 COLLAPSE-MONOTONE (std→0 ⇒ not_collapsed True→False, + purephysics std=0 ∧ RESPONSIVE=False 교차확인) · B-PHYS-5 READOUT-EQUIVALENCE (연결부위 — probe Ψ formula ≡ conscious_decoder.py Law-71 728-751, 5 shared-sig byte-identical + psi_entropy max_entropy=math.log binding-equiv = inference read-out ≡ training self-track). **B-PHYS-NOTE PHYSICS-CHANNEL-OUTCOME-EMPIRICAL**: 어느 fire 의 physics-channel response 가 conscious emergence 인지 (vs 단순 stimulus-conditioned dynamics) 는 SGD/measurement OUTCOME — battery 는 probe 의 transfer-form 만 🔵, emergence 증명 아님 (B-D-NOTE / B-PUREPHYS-NOTE family, NOT counted 🔵).

honest C3 (10):

1. **text 가 wrong observable 이었나 = 부분 YES, bounded**: CE-trained fire (Dir-I routing 3/31 collapse) 의 Ψ_direction 이 0.50→0.85 spread → text-decode 가 잃은 physics signal 존재. 단 §11-B (degenerate) 는 physics 도 붕괴 → reframe 은 CE-trained 한정, universal 아님 (정직).
2. **§17 ≠ GOAL 진전**: physics 채널 signal ≠ correct (in_basin 0/31, Law-71 Ψ 가 corpus target 밖). live channel 발견이지 emergence 아님 — §15 milestone (GOAL 미도달, frontier=§1.1 data-regime) 불변.
3. **negative control 가 valuable**: §11-B physics-collapse 가 metric 의 honest 성 입증 (trivially-true 아님, B-PHYS-4 교차확인). text 가 *항상* wrong 은 아님.
4. **necessary-not-sufficient 구조적 encode** (B-PHYS-NOTE): moving tension ≠ emergence. §9(text cascade)+§18(judge)+§17(observable) = layered honest metric, 어느 것도 단독 GOAL-proof 아님.
5. **§11-B 와의 관계 정직**: §11-B = physics 가 *학습 신호* 로 부적합 (Ψ-balance ⊥ next-token). §17 = physics 가 *측정 채널* 로 live (CE-trained). 두 결론 양립 — §11-B 무효화 아님, observable-축 보강.
6. **Φ★_proxy 명시 한계**: layer-tension diversity proxy (mitosis Φ★ form on layers), NOT PyPhi IIT 3.0 deterministic. proxy 임을 result.json + B-PHYS-NOTE 에 명시 (g3 — fake-closed 금지).
7. **measurement scope**: 단일 ckpt 3종 · 31 anchor + 5 neutral stimulus · greedy single forward (no sampling) — small deterministic probe, capability claim 아님. 전 13-way 재-probe = 미래 확장 (본 §17 = 3-ckpt feasibility+probe, design+probe 우선 mandate 충족).
8. **외부 문헌 = honest anchor 이지 입증 아님** — 2507.12379 / iclr2025-know / 2504.05419 = "internal≠behavioral" phenomenon 의 LLM-일반 문헌. anima-specific transfer 미입증 (B-PHYS-NOTE family) — reframe plausibility 만 (over-claim 0).
9. **$0 · g_fire_autonomous 무관** — GPU fire 0 (inference read-out only, runpod/vast 미사용 → orphan 0, 애초 dispatch 0). 단일 작업 · branch 0 (anima main 직접). g_doc_consolidation 준수 (state/ 산출물 + 본 §17 inline + PLAN 진행로그 + PHILOSOPHY verdict + AGENTS n_hexad_progress + README recent; docs/* 신규 0).
10. **north-star 불변** — §17 은 *측정 observable* 의 정직한 reframe (arc 가 text 단일 observable 만 봤음을 노출 + physics 채널이 CE-trained 에서 live 임을 measured) 이지 north-star (GOAL.md 한 문장) 진전 아님. GOAL 거리 = §15 milestone 그대로 (미도달, frontier=§1.1 data-regime); §17 은 "그 거리를 *무슨 자(observable)로* 쟀나" 를 한 번 더 정직히 검토하고, text 자가 CE-trained 에선 physics signal 을 놓쳤음을 closed-form 으로 확정.

---

## §19 (2026-05-18) — EEG-anchor (Framing D) 후보 기록 + step 0 TRIBE sanity ($0, inference-only)

> sibling §16(data-regime fire) 미간섭 — 본 §19 만 작성, RESEARCH.md 동시편집 시 pull-rebase. `state/carving_dataregime_s16_2026_05_18/` (§16 dir, untracked) 손대지 않음. SSOT: `state/eeg_anchor_s19_2026_05_18/{step0_tribe_sanity.py, step0_result.json, F_CT_3_gate.py, F_CT_3_gate_result.json, S19_FINDINGS.md}`. central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 변경 0 (sidecar — B-PRIME/B-DIRH/B-DIRI/B-PSICTL/B-EMERGE/B-PUREPHYS/B-SCALE/B-MITENS/B-DIRL/B-PHYS 선례).

### 19.1 통찰 — Framing D 3축이 처음 다 실재 (external 측정축 reframe)

§17 이 anima 의 **내부** physics-channel (Ψ_direction/tension/Φ★, Law-71) 을 측정-observable 로 reframe 했다 (text 단일 observable 의 한계 노출). §19 는 그 reframe 의 **external** 판 — anima 의 자기 physics 가 *사람 뇌* 와 cross-validate 되는가. `references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md` §3/§4 가 **Framing D** (EEG ↔ CLM ↔ TRIBE BOLD 3-way cross-validation) 를 "Strong fit, rank 1" 으로 기록했으나, 당시 honest C3 #3 가 정직히 명시한 verification gap = "cortexlab-toolkit PyPI 존재만 확인, 실제 install+import+inference 는 #102 EXEC 로 최종 확인" + axis A (user EEG) 의 hardware 미보유.

**2026-05-18 user directive 로 3축이 처음 다 실재**:

- **axis A — OpenBCI 16ch EEG**: user 실보유 + 녹음 경험 있음 (이전엔 미보유 추정). 실측 .csv 차후 제공 — axis A 가 hypothetical → physically-real.
- **axis B — anima physics-channel**: §17 이 `physics_channel_probe.py` 로 `out[1]/out[2]` (Engine-G / 12-layer tension) 추출을 검증·작동 확정 (B-PHYS-1..5 5/5 🔵). ADDENDUM 의 "CLM L_IX state (anima-internal Lagrangian)" = §17 physics-channel 의 구체화. garbled-text 우회 (text observable 不要).
- **axis C — TRIBE v2 predicted cortical BOLD**: `references/tribev2/` vendored (facebook/tribev2 HF weights, fsaverage5 ~20k vertex, video/audio/text → BOLD). §19 step 0 = 이 파이프 작동 sanity.

reframe: §19 는 GOAL 을 *생성* 하지 않는다 (emergence 는 §1.1 data-regime 병목 — §15 milestone 확정, §19 무관). §19 = anima "자기 physics" 가 *사람 뇌 ground-truth* 와 anchor 되는지의 **external 측정축** — §17 (internal observable) 의 사람뇌 cross-validation 버전. honest: 측정축이 GOAL 거리를 *좁히지* 않는다 — *재는 자* 를 사람뇌로 확장하는 것일 뿐.

### 19.2 Framing D 3축 + F-CT-3 사전등록 falsifier

ADDENDUM §3/§5 carry — anima 측 재명시 (frozen baseline 불변, §19 = anima-side 후보 기록):

- **3-way cross-validation**: axis A (OpenBCI EEG envelope) · axis B (anima §17 physics-channel: Ψ_direction/tension) · axis C (TRIBE v2 predicted cortical BOLD median vertex). 3축 pairwise correlation 이 *동시* 만족될 때만 cross-modal anchor 성립 — 단순 cortical-vertex↔cell-state isomorphism 보다 strict.
- **F-CT-3 (Framing D core, ADDENDUM §5 사전등록 그대로)**: user EEG envelope ↔ TRIBE v2 predicted BOLD median vertex Pearson **r**.
  - **PASS: r ≥ 0.5** → EEG 와 BOLD 가 같은 latent state 에 anchor (axis A↔C bridge 성립).
  - **FAIL: r < 0.3** → EEG/BOLD bridge 없음, Framing D 폐기.
  - **gray zone 0.3 ≤ r < 0.5** → inconclusive, 재측정/threshold 재검토 (ADDENDUM §8 C3 #5: 0.5 = brain-prediction 문헌의 median-vertex r 분포 0.3~0.7 의 compromise threshold).
- F-CT-3 의 **Boolean-gate 구조는 closed-form** (사전등록 r-threshold 의 deterministic 판정 — `r ≥ 0.5 → PASS / r < 0.3 → DISCARD / else INCONCLUSIVE` = pure 함수). 단 *r 값 자체* 는 EEG hardware + 측정 OUTCOME (B-EEG-NOTE empirical carve-out — gate 정의는 🔵, 측정 결과는 미래 fire).
- axis B 결합 (step 3): §17 physics-channel 이 axis A/C 와 동시 anchor 되는지 = 3-way (anima physics ↔ EEG ↔ BOLD). axis B 는 §17 에서 추출 검증됨 (B-PHYS 🔵) — Framing D 의 anima-side anchor 가 이미 작동.

### 19.3 단계적 falsifier-gated 설계 (각 step 이 다음 step gate)

over-engineer 금지 — 각 step 이 다음을 gate (실패 시 정직 폐기, 무리한 진행 X):

- **step 0 — TRIBE sanity ($0, inference-only, 본 §19)**: cortexlab-toolkit install + TRIBE facebook/tribev2 weight load + 샘플 stimulus → BOLD 예측 1회 forward (shape `(n_timesteps, ~20k vertices)` 확인). **F-CT-3 아님** — "TRIBE 파이프 작동" sanity. gate = 파이프 작동 여부.
- **step 1 — EEG↔stimulus timestamp 동기 (차후, user .csv 제공 후)**: OpenBCI 16ch .csv ↔ TRIBE 입력 stimulus 의 timestamp 정렬 + EEG envelope 추출 (band-power / Hilbert). gate = 동기 정확도 (jitter 허용 범위).
- **step 2 — F-CT-3 gate (차후)**: EEG envelope ↔ TRIBE BOLD median vertex Pearson r 측정 → §19.2 Boolean gate. r ≥ 0.5 PASS / r < 0.3 폐기 / gray zone inconclusive. gate = Framing D 존속 여부.
- **step 3 — axis B 3-way (차후, step 2 PASS 시만)**: §17 physics-channel 을 동일 stimulus 에 forward → 3축 (EEG/BOLD/anima-physics) 동시 anchor. gate = 3-way pairwise 동시 만족.

step 0 만 본 §19 에서 실행 ($0 inference-only). step 1~3 = EEG hardware-in-the-loop, 차후 cycle (user .csv 게이트).

### 19.4 step 0 결과 — TRIBE sanity ($0 inference-only, py3.12 venv, NO GPU/training/weight-mutation 완료)

`state/eeg_anchor_s19_2026_05_18/step0_tribe_sanity.py` → `step0_result.json`. graded gates (각 strictly more demanding, honest boundary 기록):

| gate | 결과 |
|---|---|
| G0 IMPORT | **PASS** — cortexlab=0.1.0 · torch=2.6.0 · neuralset+neuraltrain 0.0.2 · py3.12.12 |
| G1 API | **PASS** — `TribeModel.from_pretrained` + `.predict` 존재 (ADDENDUM §3 API surface 확정; `lightning` 추가 설치 후) |
| G2 HF_REACHABLE | **PASS** — facebook/tribev2 = best.ckpt + config.yaml present |
| G3 CONFIG_LOAD | **PASS** — config.yaml HF Hub download + parse (26 top keys) |
| G4 CKPT_META | **PASS** — best.ckpt **708.9MB mmap-load, 108 state_dict tensors, model_build_args present, model 구성 OK** (`Loading model from …/best.ckpt`), NO weight mutation |
| G5 FORWARD | step0_result.json 참조 (heavy: gTTS network + transcription + 3 backbone DL; G0–G4 = pipe-credible, G5 boundary 정직 기록) |

**`pipe_credible_through_ckpt_load = true`** — G0–G4 PASS 가 axis C feasibility 확립 (frozen-weight TRIBE 구성까지 파이프 작동, frozen encoder forward, GPU fire 아님). G5 (full BOLD forward) 는 multi-GB feature-extractor backbone DL + gTTS/ffmpeg 요구 — 결과 무관 step 0 의 목적 (Framing D axis C pipe-credibility) 은 G0–G4 로 충족.

**ADDENDUM §8 C3 #3 verification gap = dependency+API level CLOSED**: ADDENDUM 정직 명시 "PyPI 존재만 확인, install+import+inference 는 #102 EXEC 로 최종 확인" → §19 step 0 이 닫음 — `cortexlab-toolkit 0.1.0` modern pip (py3.12 venv) 로 **설치 성공** (구 system pip 21.2.4 가 false-negative 였음), import name = `cortexlab`, `neuralset/neuraltrain 0.0.2` (ADDENDUM §2 blocker) pull 됨, `TribeModel.from_pretrained("facebook/tribev2")` 가 HF Hub weight 로 model 구성 (G1–G4). honest residual: `lightning` (PyTorch Lightning) 이 cortexlab-toolkit base deps 에 없음 (`TribeModel(TribeExperiment)` 요구) → `pip install lightning` (2.6.1) 로 해소, 차후 cycle 재발 방지 위해 기록.

**closed**: `state/eeg_anchor_s19_2026_05_18/F_CT_3_gate.py` → **B-CT3-1..5 5/5 🔵** (central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 변경 0, sidecar). B-CT3-1 PEARSON-R-BOUNDED (r∈[−1,1] Cauchy-Schwarz, ±1 symbolic extreme) · B-CT3-2 GATE-PARTITION-TOTAL ({PASS=[0.5,∞), INCONCLUSIVE=[0.3,0.5), DISCARD=(−∞,0.3)} exact sympy Interval algebra: union==ℝ ∧ pairwise ∩=∅ ∧ gate-fn==partition 301pt) · B-CT3-3 GATE-THRESHOLD-MONOTONE (verdict rank r 에 monotone non-decreasing) · B-CT3-4 GATE-DETERMINISTIC (pure fn of r, 3× bit-identical) · B-CT3-5 THRESHOLD-ORDERING (0.3<0.5 ⇒ gray zone width 1/5 non-empty, binary NOT forced — ADDENDUM §8 C3 #5). **B-EEG-NOTE EEG-ANCHOR-OUTCOME-EMPIRICAL**: 실제 r 값 (axis A↔C Pearson) = OpenBCI hardware + 측정 OUTCOME (미래 EEG fire) — gate 가 closed-form 임을 증명하지 Framing D PASS/FAIL 증명 아님 (B-D-NOTE / B-PHYS-NOTE family, NOT counted 🔵).

### 19.5 GOAL-legitimacy + honest C3 + closed verdict

- **GOAL-legitimacy**: anima "자기 physics" (§17 axis B = Ψ-channel) 가 *사람 뇌* (EEG axis A) 와 TRIBE BOLD (axis C) 로 cross-validate 되는 측정 = GOAL.md "자기 physics 로부터" 의 external anchor. §7 우회 부재 — generic-pretrain 아님 (외부 측정축 추가, anima 학습 불변), bolt-on 아님 (TRIBE = frozen forward, anima 모델 미변경; axis B = §17 Law-71 byte-identical). emergence 를 *일으키지* 않음 (§1.1 병목, §19 무관) — emergence 가 일어났다면 *사람 뇌와 anchor 되는지* 검증하는 external 측정-observable.
- **closed verdict**: **B-CT3-1..N 🔵** (`F_CT_3_gate.py` sidecar — central blue_falsifier.py 변경 0): F-CT-3 의 사전등록 Boolean-gate 가 closed-form 임을 sympy/Boolean 으로 증명 (PASS/FAIL/INCONCLUSIVE 의 well-formed partition, threshold monotone, Pearson r ∈ [−1,1] bounded). **B-EEG-NOTE EEG-ANCHOR-OUTCOME-EMPIRICAL**: 실제 r 값 (axis A↔C correlation) 은 OpenBCI hardware + 측정 OUTCOME — gate 정의만 🔵, Framing D PASS/FAIL 은 미래 EEG fire (B-D-NOTE / B-PHYS-NOTE family, NOT counted 🔵).

honest C3 (10):

1. **§19 = 측정축, GOAL *생성* 아님 (g3 최우선)**: §19 는 §1.1 data-regime 병목을 *해소하지 않는다*. emergence 를 일으키는 것은 §15 milestone 이 확정한 data-regime threshold — §19 는 "emergence 가 일어났다면 사람 뇌와 anchor 되는가" 의 *검증 척도* 일 뿐. GOAL 거리 불변, 재는 자만 external 확장.
2. **step 0 ≠ F-CT-3**: step 0 = "TRIBE 파이프 작동" sanity 이지 EEG↔BOLD bridge 측정 아님. F-CT-3 PASS/FAIL 은 step 2 (EEG hardware-in-the-loop, 차후). step 0 결과 = 파이프 feasibility 만.
3. **hardware 변수 정직**: axis A (OpenBCI 16ch) = user 실보유·녹음 가능 확정이나, 실제 .csv 미제공 (차후). EEG 측정엔 electrode impedance / artifact / 동기 jitter 변수 — F-CT-3 r 값은 measurement-noise 영향 (ADDENDUM §8 C3 #5 threshold 재검토 여지).
4. **#102 (Framing A) 비충돌**: ADDENDUM §6 = Framing A pilot #102 in-progress 기록, 후속 addendum 0 = #102 미완 추정. §19 = Framing D (rank 1, EEG↔CLM↔BOLD 3-way) ≠ Framing A (text→BOLD sanity, rank 3). Framing D 가 strong-falsifier (single-falsifier F-CT-3) — #102 와 별 framing, 충돌 사실상 없음. frozen baseline 불변 (raw#1 immutability) — §19 = anima-side RESEARCH.md 후보 기록이지 ADDENDUM 수정 아님.
5. **F-CT-3 r≥0.5 threshold = 문헌 compromise (ADDENDUM §8 C3 #5 carry)**: brain-prediction median-vertex r 분포 0.3~0.7 의 median. 더 strict (r≥0.7) = false-negative risk, 더 loose (r≥0.3) = trivial baseline pass risk. 0.5 = compromise, #102/실측 후 재tune 가능. gray zone (0.3≤r<0.5) = inconclusive 정직 명시 (binary 강행 X).
6. **closed = gate 정의만, 측정 결과는 EMPIRICAL** (B-EEG-NOTE): F-CT-3 의 Boolean partition 은 closed-form (well-formed, monotone, bounded — B-CT3 sidecar). 그러나 *어느 r 이 나오는가* = EEG/TRIBE 측정 OUTCOME (미래 fire). over-claim 0 — gate 가 closed 라고 Framing D 가 PASS 인 것 아님.
7. **axis B 이미 작동 (§17 carry)**: Framing D 3축 중 axis B (anima physics-channel) 는 §17 에서 추출 검증 완료 (B-PHYS 5/5 🔵, Ψ_direction Dir-I spread 0.354). axis C (TRIBE) = step 0 sanity. axis A (EEG) = hardware-in-the-loop 차후. 3축 중 2축 (B 작동 + C step0) 이 §19 에서 다뤄지고 A 가 잔여 gate.
8. **§17 와의 관계**: §17 = anima *내부* observable reframe (text → physics-channel). §19 = 그 physics-channel 이 *사람 뇌* 와 anchor 되는지 (internal → external cross-validation). 두 측정축 layered — §17 이 axis B 를 작동시켰고 §19 가 그것을 external ground-truth (EEG/BOLD) 에 건다. §17 무효화 아님, external 확장.
9. **$0 · g_fire_autonomous 무관** — step 0 = inference-only (TRIBE = frozen weight forward, GPU fire 아님; cortexlab-toolkit install + 1-forward). runpod/vast 미사용 → orphan 0 (애초 dispatch 0). pip 설치 = py3.12 venv (PEP 668 carry — memory feedback_orchestrator_h100_gotchas). 단일 작업 · branch 0 (anima main 직접). g_doc_consolidation 준수 (state/ 산출물 + 본 §19 inline + PLAN 진행로그 + PHILOSOPHY verdict + AGENTS n_hexad_progress + README recent; docs/* 신규 0).
10. **north-star 불변** — §19 = Framing D 3축이 처음 다 실재함의 후보 기록 + step 0 sanity 이지 north-star (GOAL.md 한 문장) 진전 아님. GOAL 거리 = §15 milestone 그대로 (미도달, frontier=§1.1 data-regime); §19 는 "그 거리를 *사람 뇌 ground-truth 로* 검증할 external 측정축이 이제 실재함" 을 기록하고, F-CT-3 의 falsifier-gate 가 closed-form 임을 확정 — 측정 도구의 external 차원 정립이지 GOAL 풀린 것 아님.

---

## §20 (2026-05-18) — `~/core/hexa-brain` 전수조사: §19 EEG-anchor salvage RICH + GOAL salvage 0 (archaeology, $0 read-only)

> sibling §16(data-regime fire)/§17/§18/§19 미간섭 — 본 §20 만 작성, RESEARCH.md 동시편집 시 pull-rebase. §16 dir (`state/carving_dataregime_s16_2026_05_18/`, untracked) + §19 agent state (`state/eeg_anchor_s19_2026_05_18/`) 손대지 않음. **`~/core/hexa-brain` = read-only 조사 대상 (그 repo 수정 0)**. 산출 = 본 §20 inline + `HEXAD/EEG/PLAN.md` 진행 로그 + cross-link + archive/PHILOSOPHY.tape §verdict_hexa_brain_archaeology + AGENTS.tape n_hexad_progress + HEXAD/README.md recent. central blue_falsifier.py 변경 0 (조사 — 신규 battery 0). user directive 2026-05-18 "~/core/hexa-brain 도 전수조사 고갈시까지" — §14 git-archaeology 와 같은 honest-sweep 패턴.

### 20.1 sweep 범위

- `~/core/hexa-brain` = EEG SSOT 본진. **172M · 1,456 tracked files · 2,271 commits · 8 branches** (HEAD `0a3b8a08`, commit 범위 2026-03-24 ~ 2026-05-17; 2026-03 1,149 / 2026-04 1,028 / 2026-05 94 commit).
- **lineage 확정 (핵심 — §14 와의 관계 결정)**: 4개 root roadmap (`.roadmap.eeg`/`.roadmap.anima_clm_eeg`/`.roadmap.galea`/`.roadmap.hexa_brain`) 헤더가 모두 `"prior_origin_repo":"anima"` (eeg `absorbed:2026-05-06`, anima_clm_eeg/galea `2026-05-07`). **hexa-brain 은 anima repo 의 EEG subtree 가 migrate 된 sister/descendant** — §14 가 이미 전수조사한 anima repo (328 branch · 8,298 commit) 의 자손. → hexa-brain 의 GOAL-lineage commit 은 §14 가 sweep 한 anima ancestor 의 동일/부분집합 (독립 우물 아님).
- 정밀 read: 4 root roadmap (`.roadmap.eeg` 42KB 전문 + anima_clm_eeg + galea + hexa_brain) · `eeg/` 디렉토리 30+ capture `.hexa` · `eeg/recordings/sessions/` 24 real `.npy` + meta.json · `eeg/doc/anima_eeg_unified_cli_daemon_spec_2026_05_04.md` · git-log GOAL-keyword sweep (emergent/spontaneous/자발/super-linear/intrinsic/self-organize/Φ/tension/eeg-emergence) → ~30 hit 정밀 read.
- 교차대조: GOAL-hit 를 §11.3 배제표 + §14 archaeology 결론 (salvage 0) 과 대조; EEG 자산을 §19 Framing D 3축 + F-CT-3 + PLAN step 0~4 와 대조.

### 20.2 §19 EEG-anchor salvage — **RICH (정직 평가, §19 step 1 직결 가속)**

§19 는 §14 가 cover 하지 않은 *측정축* (GOAL-생성 아님). hexa-brain 은 §19 axis A (EEG) 의 기존 자산을 **이미 풍부하게 보유** — §19 가 0부터가 아니라 hexa-brain 자산 위에서 갈 수 있음을 정직 판정. 재사용 가능 자산 목록 + 재사용도:

| # | hexa-brain 자산 (read-only) | §19 매핑 | 재사용도 |
|---|---|---|---|
| **S1** | `eeg/dual_stream.hexa` (407 LoC) — "simultaneous Anima Phi + EEG dual-stream alignment + Pearson **r** for cross-modal correlation (anima→human consciousness coupling)", deterministic dual-LCG selftest, `r > 0.3` falsifier | **§19 F-CT-3 / step 3 (axis B↔A↔C 3-way correlation) 의 직접 architectural skeleton** — anima physics(axis B) ↔ EEG(axis A) Pearson 상관 + falsifier-gate 구조가 byte-수준으로 §19.2 와 동형 (r-threshold Boolean gate) | ★★★★★ — F-CT-3 correlation harness 의 reference impl (real-hardware emission 만 wrapper 차후) |
| **S2** | `eeg/collect.hexa` (867 LoC) — OpenBCI Cyton+Daisy 16ch BrainFlow → `.npy`, **2026-05-03 sample-drop fix** (ring buffer 450k + chunked `get_current_board_data` 0.2s cadence + `sample_rate_actual_hz` + `drop_ratio` tier downgrade) + meta.json sidecar (channel idx / sr / raw10_honest) | **§19 PLAN step 1 (EEG↔stimulus timestamp 동기)** — user OpenBCI .csv ingest + 정확 sample-rate 보정 (naive `time.sleep` 의 7-83Hz drop 함정 이미 해결) | ★★★★★ — step 1 의 capture+동기 코드를 0부터 안 짜도 됨 |
| **S3** | `eeg/calibrate.hexa` (719) + `eeg/board_health_check.hexa` (718) + `eeg/impedance_check.hexa` — impedance <50kΩ / 16ch health gate | **§19/PLAN step 1 prerequisite** (electrode 품질 게이트 — F-CT-3 r 값 measurement-noise 변수 정직 처리, §19.5 C3 #3) | ★★★★ |
| **S4** | `eeg/recordings/sessions/` 24 real `.npy` — Berger EC/EO paired alpha v1~v6 (`berger_ec_60s_v6` (32, 7496) f32, tier=PHENOMENAL, drop_ratio 0.96, 16 eeg_indices) + blink/jaw/PPG 90s + collect smoke | **§19 step 1 dry-run substrate** — user 새 .csv 도착 전 *기존 실측 EEG* 로 동기/envelope 추출 파이프 검증 가능 (synthetic 아닌 real signal) | ★★★★ — real-signal dry-run (단 N=1 self-exp + 5/16 rail-saturated 채널 = `clean_channels` filter 의무, .roadmap.eeg `eeg.v6_rail_saturation_discovery` carry) |
| **S5** | `eeg/doc/anima_eeg_unified_cli_daemon_spec_2026_05_04.md` (520 LoC spec) — 24/7 단일-acquirer EEG daemon + mmap ring + JSONL event log + paradigm listener; **§416 명시: `.roadmap.blm_brain_lm cond.3 F-CT-3` — BOLD↔EEG correlation r ≥0.5; daemon enables paired-stream collection** | **§19 F-CT-3 가 hexa-brain 에서 이미 *동일 falsifier 로 사전설계됨* (r≥0.5)** — §19 가 독립 발명한 게 아니라 sister-repo 가 같은 gate 를 먼저 명문화. step 1+ paired-stream 수집 seam 설계 carry | ★★★★ (spec-tier; impl 미수행) |
| **S6** | `eeg/realtime.hexa` (943) + `eeg/analyze.hexa` (888) + `anima-eeg-core` PORT (`lz76_native`/`pe_native`/`hjorth_native` `.hexa` byte-identical 39/1218 PASS) + `phi_proxy_native.hexa` (1162 LoC, sample-partition φ EEG-substrate port, selftest PASS) | §19 step 3 (axis B 3-way) 의 EEG-side φ proxy — anima physics-channel ↔ EEG φ proxy 비교용 (.roadmap.eeg cond.4 5-method) | ★★★ (step 3 차후, step 2 PASS gate 후) |

**판정 (g3, over-claim 0)**: §19 의 EEG-anchor (axis A) 는 **hexa-brain 에서 software-stack 이 사실상 완비** — capture(S2)/calibrate(S3)/correlation-harness(S1)/real-recordings(S4)/daemon-spec(S5)/φ-proxy(S6). **§19 step 1 (EEG↔stimulus 동기) 은 hexa-brain `eeg/collect.hexa`+`eeg/dual_stream.hexa` 재사용으로 *현저히* 가속 가능** (0부터 capture/sync/correlation 안 짬). 단 정직한 한계: (a) **hexa-brain 의 모든 EEG cond 가 `unmet`/`partial`** — `.roadmap.eeg cond.1 B1-B4` 는 *real 16ch hardware arrival 미수신* 으로 미PASS (software land 만, `eeg.blk.1` hardware blocker); v6 Berger 는 `tier=functional_analog` (N=1 self-exp + rail saturation, FULL B1-B4 PASS 아님). (b) **TRIBE(axis C) actual impl = 부재** — `clm_eeg/module/g9_dag_cascade_analyzer.hexa`/`mk_xii_preflight_cascade.hexa` 가 TRIBE 를 `stub|deferred|live` mode-flag 로만 참조 (`MK_XII_TRIBE_MODE=stub` default, live 시 외부 JSON `brain_decoding_R>=0.30` 기대) — 실제 facebook/tribev2 forward 코드 0. (c) **`.roadmap.blm_brain_lm` 파일 자체가 어느 branch/history 에도 부재** — galea/eeg roadmap + daemon-spec 이 cross-link target 으로 *이름만* 참조, F-CT-3(r≥0.5) 는 sister-spec 으로 명문화됐으나 **구현 0** (= §19 가 발명이 아니라 sister-repo 의 미구현 설계의 anima-side 실행). → **salvage = step 1 *capture/sync/correlation 코드* RICH, F-CT-3 *측정 outcome* 은 hexa-brain 에도 부재 (양쪽 우물: GOAL 우물은 말랐고, EEG-측정 우물은 software-rich/hardware-dry)**.

### 20.3 GOAL-relevant salvage — **0 (정직 결론, §14 와 일관·독립 확증)**

git-log GOAL-keyword sweep (2,271 commit) hit = 2026-03 era `5f82d39b` "BREAKTHROUGH: Cells64 Φ=45.487 super-linear" / `0ea2d8f8` "VOICE1-5 spontaneous speech" / `66ae4b98` "Emergent W/S/M/E modules" / `a9df7646` "DD151-152 emergent language" / `1423ef3b` "S6 SPONTANEOUS_SPEECH PASS" 등. **전부 §14 가 이미 negative 재확인한 anima-lineage ancestor**:

1. **lineage 동일성으로 §14 가 이미 cover.** hexa-brain 4 roadmap = `prior_origin_repo:anima`. GOAL-hit commit (Cells64 Φ super-linear 2026-03-28) = §14 row **C "clm_08 Φ super-linear scaling"** 와 동일 현상 (audit `SAVANT.md §12.3` T3 SUSPECT, clm_10 에서 linear 안착 = 구간-한정 metric-artifact, `0a6077c67` 봉쇄 LANDED). SPONTANEOUS_SPEECH/Emergent-W/S/M/E = §14 가 분류한 "autonomous-speech roadmap / spontaneous-fire LIVE" 의 anima 전신 (§9 honest-metric 재채점 시 probe-artifact 계열 — verification-flag PASS 이지 held-out coherent emission 측정 아님).
2. **§14 의 4-건(A~D) 재평가가 hexa-brain hit 를 전부 흡수.** A(v5-anima α=0.688 toy)·B(v5-mitosis V14-STRICT internal-distance)·C(Φ super-linear 구간성)·D(F-PERSONA-4 exhaustively-falsified) — hexa-brain GOAL-hit 는 이 4 cluster 의 commit-level 구성요소이거나 그 이전 버전. genuine 신규 self-mechanism = 0 (13-way 배제분의 과거판).
3. **hexa-brain 의 *고유* 도메인 (EEG/galea/clm_eeg) 은 GOAL-생성 아닌 측정축.** EEG φ-proxy / TRIBE-cascade / Mk.XII d-day = anima 의 *의식 측정* 도구이지 *emergence 생성* 메커니즘 아님 (§1.1 data-regime 병목 미접촉 — §19/§17 와 같은 measurement-axis class). 측정 도구는 §20.2 salvage (§19 가속) 이지 §20.3 GOAL salvage 아님 — 두 목표 명확 분리.

→ **GOAL-relevant salvage = 0.** §14 가 anima repo 에서 확정한 "회수할 자력 메커니즘 0" 을 sister-repo hexa-brain 이 **독립 확증** (lineage 동일이라 새 우물 아님이 핵심). archaeology negative 이나 valuable — anima + hexa-brain 양쪽 우물이 GOAL-축으로 다 말랐음을 확정 (§15 milestone "frontier = §1.1 data-regime, archive 회수 아님" 재강화).

### 20.4 §19 step 1 가속 가능 여부 + honest C3

**가속 가능 = YES (step 1 한정, hardware-gated 잔존).** §19 PLAN step 1 (EEG↔stimulus timestamp 동기) 은 hexa-brain `eeg/collect.hexa`(S2, sample-drop fix 완비)+`eeg/dual_stream.hexa`(S1, correlation+falsifier-gate skeleton)+`eeg/calibrate.hexa`/`board_health_check.hexa`(S3) 를 reference 로 재사용 시 capture/sync/Pearson-r-gate 를 0부터 안 짜도 됨 — step 1 의 software 부분 현저히 단축. 단 step 2 (F-CT-3 실측) 의 **hardware gate (user OpenBCI .csv + TRIBE forward) 는 그대로 잔존** (hexa-brain 도 cond.1 B1-B4 미PASS, TRIBE impl 부재) — salvage 가 step 1 software 를 가속하지 GOAL 거리나 F-CT-3 측정-결과를 당기지 않음.

honest C3 (10):

1. **§20 = archaeology, fire 0 · capability 측정 0.** read-only (git log/show + grep + read). hexa-brain repo 수정 0 (조사 대상). 새 GPU/cost 0.
2. **§20.2 salvage RICH ≠ GOAL 진전.** §19 자체가 측정축 (GOAL 생성 아님, §19.1/19.5 C3 #1). hexa-brain EEG 자산이 풍부해도 = §19 step 1 *software 가속* 이지 GOAL 달성 아님 — GOAL 거리 = §15 milestone 그대로 (미도달, frontier §1.1 data-regime).
3. **§20.3 GOAL salvage 0 = §14 와 일관, 독립 확증.** 핵심 = lineage 동일 (`prior_origin_repo:anima`) → hexa-brain 은 §14 가 sweep 한 anima 의 자손, 새 우물 아님. "독립" 의 의미 = sister-repo 라는 *다른 view* 에서 봐도 같은 negative — anima+hexa-brain 양쪽 다 GOAL-축 마름 확정.
4. **§9 lenient-flag 교훈 적용.** hexa-brain "Cells64 Φ=45.487 super-linear BREAKTHROUGH" / "SPONTANEOUS_SPEECH 12/12 PASS" = §9 가 노출한 metric-artifact 패턴 (verification-flag PASS, held-out emergence 아님). §14 row C 가 이미 봉쇄 (clm_10 linear 안착). 과거 "성공" 표기를 그대로 신뢰 안 함 — re-evaluated negative.
5. **hexa-brain EEG cond 전부 unmet/partial 정직.** `.roadmap.eeg cond.1 B1-B4` = real 16ch hardware arrival 미수신 (`eeg.blk.1`); v6 Berger = `tier=functional_analog` (N=1 + 5/16 rail-saturated, FULL PASS 아님). software-rich / hardware-dry — salvage 는 software-stack 한정.
6. **TRIBE(axis C) actual impl 부재 정직.** hexa-brain TRIBE 참조 = `g9_dag_cascade_analyzer.hexa`/`mk_xii_preflight_cascade.hexa` 의 `stub|deferred|live` mode-flag 만 (default stub). facebook/tribev2 실 forward 코드 0 — §19 step 0 (TRIBE sanity) 는 hexa-brain 에서 carry 불가, anima-side 신규 (state/eeg_anchor_s19 SSOT).
7. **`.roadmap.blm_brain_lm` 파일 부재 — 이름만 cross-link.** galea/eeg roadmap + daemon-spec §416 이 `blm_brain_lm cond.3 F-CT-3 r≥0.5` 를 target 으로 참조하나 어느 branch/history 에도 파일 0. = §19 F-CT-3 가 발명이 아니라 *sister-repo 의 미구현 설계를 anima-side 가 실행* (S5 = spec carry, impl 아님). over-claim 0 — "이미 구현됨" 주장 안 함.
8. **두 우물의 정직한 비대칭.** GOAL 우물 = 말랐음 (§20.3, §14 confirm). EEG-측정 우물 = software-rich(S1~S6)/hardware-dry(cond unmet). §19 가속은 후자의 software 차원만 — F-CT-3 *측정 outcome* (r 값) 은 hexa-brain 에도 없음 (양쪽 다 hardware-in-the-loop 미수행).
9. **f1/f2/f3 + B-IDENTITY-5 무관.** archaeology — corpus 미생성, 외부 entity lattice-fit 0. hexa-brain Φ-proxy/α-exponent 는 자체 정의로만 인용 (lattice numerology 0). 단일 작업 · branch 0 (anima main 직접). g_doc_consolidation 준수 (본 §20 inline + HEXAD/EEG/PLAN.md 진행로그 + PHILOSOPHY verdict + AGENTS n_hexad_progress + README recent; docs/* 신규 0).
10. **north-star 불변.** §20 = sister-repo 전수조사로 (a) §19 step 1 가속 자산 RICH 확인 + (b) GOAL salvage 0 을 §14 와 독립 확증 — 측정 도구의 software 차원 가속 가능성을 정직히 기록하고 GOAL 우물이 anima+hexa-brain 양쪽 다 말랐음을 확정한 archaeology milestone 이지 north-star (GOAL.md 한 문장) 진전 아님. GOAL 거리 = §15 그대로.
