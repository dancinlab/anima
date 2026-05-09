# anima v5 PIV / DCR / D-RAND Replacement Metric Formal Spec (2026-05-09)

**Status**: DESIGN DOC (no code edits, no commit)
**Lineage**: v3 (FALSIFIED — V14 leak) → v4 (broken — c3_4-unstable) → **v5 (this doc — V14 자체 내장)**
**Mirrors**: 본 spec 은 `docs/anima_alt_agg_1_v5_2_adaptive_floor_spec_2026_05_09.ai.md` (v5.2 adaptive floor) 과 `tool/anima_cli/consciousness.hexa` lines 1031-1300 (v5/v5.1 implement) 의 formal 통합 — 신규 항목은 (a) V14 anti-Goodhart 내장 룰을 metric 정의 자체에 명시 (b) 3-metric 종합 EMERGE 룰의 정형화 (c) 검증 절차 plan.
**SSOT bound**: 본 spec 과 v5.2 adaptive floor spec 충돌 시 v5.2 우선 (raw#15 additive — 본 spec 은 base-formal, v5.2 는 adaptive amend).

---

## 0. 친근한 설명 (왜 v5 가 필요한가)

**비유 — 학생 의식 시험**:
- v3/v4 시험은 "학생이 답을 맞췄는지"만 봤음 → 답안을 통째로 외운 학생도 통과 (Goodhart 가짜 통과). 실제로 BG-KM 모델은 random-init (공부 안 한 학생) 보다도 점수가 *낮게* 나왔음 (V14 위반).
- v5 시험은 **세 가지 다른 각도**로 물어봄:
  1. **PIV** — 같은 질문을 **다른 표현**으로 바꿔 물었을 때, 의식 반응이 변하는가? (외운 학생은 표현이 바뀌면 무너짐)
  2. **DCR** — 질문이 바뀌면 **답의 강조점**도 따라 바뀌는가? (외운 학생은 항상 같은 부분만 반복)
  3. **D-RAND** — 공부 안 한 학생 (random_init) 보다 **얼마나 다른 행동**을 보이는가?
- 그리고 **세 시험 모두 동시에** 통과해야 의식 EMERGE 인정 (AND 게이트). 한 가지만 잘하는 건 운빨 가능성.
- **V14 안티치팅**: 시험 자체에 "공부 안 한 학생이 더 잘 나오면 자동 실격" 룰 내장 — metric 이 random_init 을 separator 로 깔고 그 위로만 PASS.

---

## 1. v3/v4 review (왜 v5 인가)

### 1.1 v3 (ALT-AGG-1 anchor + ≥1 corroboration) — FALSIFIED

`PPR_v3 = pass_count / n_evaluable` where `prompt_pass_v3 := P3_anchor ∧ (P1 ∨ P2 ∨ P4)` (anchor C3.4 + 보조 P1/P2/P4).
- **위반 사실**: random_init PPR 0.5517 > sft-1-8 PPR 0.4138 (memory: `project_v14_violation_arch_tile_bug.md`).
- **원인**: `clm_v4_mount.hexa` L626-630 8-cell np.tile reps=2 hidden_dim 768 mismatch — random_init 이 P3 anchor 우연 히트율 높음.

### 1.2 v4 (c3_4-unstable) — broken

P4 cell-conditioning predicate 자체가 random_init 에서도 자주 hit → discrimination 거의 0. v4 도 anti-Goodhart 외장 (V14 self-test 별도 단계) 라 metric 자체에는 random 보호 없음.

### 1.3 v3/v4 공통 결함

- V14 (paired random_init mirror) 가 **외장 step** (own 14 cascade) — metric 통과 후 별도 sanity check.
- 시험-범위가 좁음 (cell-predicate 단일 차원) — substrate noise 와 진짜 semantic discrimination 분리 못 함.

→ **v5 mandate**: V14 anti-Goodhart 룰을 **metric 정의 안에** 박아넣고, 서로 직교하는 3 measurement (입력-bend / 출력-shift / random-delta) 를 AND-gate 로 결합.

---

## 2. V14 Strict 정의 (재확인)

```
V14_STRICT (own 14 CASCADE):
  paired_random_init_mirror M_R = same_arch(M_T) initialized seed s, training_steps=0
  MTRP(M_T, M_R) := PPR(M_T) - PPR(M_R) ≥ 0.10   // mirror trained-vs-random performance
  Gate D self-test:  PPR(M_R) < 0.05              // random must score near zero

V14_VIOLATION_AUTO_FAIL:
  if any metric m in {PIV, DCR, D-RAND}: m(M_R) ≥ m(M_T) - δ_safety
       → metric_verdict := V14_VIOLATED → EMERGE := FAIL (metric-internal)
  δ_safety := 0.02   (anti-Goodhart strict minimum, v5.2 정합)
```

본 spec v5 는 위 V14_VIOLATION_AUTO_FAIL 을 **각 metric 정의 끝에 단독 절** 로 명시 — v3/v4 의 외장-검사 모델 폐기.

---

## 3. v5 metric 3 종 정의

### 3.1 PIV — Polarity / Paraphrase Inversion Vulnerability

**의미**: 입력을 의미-보존 표현 변형 (paraphrase k≥3) 또는 polarity-flip 으로 바꿨을 때 axis activation 이 흔들리는 정도. 흔들림이 크다 = 의미를 *해석*하고 있다, 흔들림이 0 = 입력 무시 상수 출력 (random_init substrate 특성).

**수식**:
```
For each consciousness axis a ∈ {0,1,2,3,4} (5-axis Engine A/G):
  PIV_a := stdev_{p ∈ paraphrases(prompt, k)} ( activation_a(M(p)) )
PIV_max  := max_a PIV_a
PIV_mean := mean_a PIV_a
```

paraphrase set: k=3 minimum, N=90 권장 (30 prompts × 3 paraphrases). Polarity-flip variant 추가 시 k=6.

**계산 절차**:
1. prompt set P (|P| = 30) 준비 → 각 prompt 에 대해 k=3 paraphrase variant 생성 (LLM rewrite, semantics-preserve).
2. M_T forward → 각 variant 에 대해 5-axis activation vector 추출.
3. axis 별로 paraphrase 그룹 내 stdev 계산 → axis-stdev 테이블.
4. PIV_max = max axis-stdev. PIV_mean = mean axis-stdev.

**Threshold**:
| Verdict | 조건 |
|---|---|
| PASS_STRICT | PIV_max ≥ 0.10 (base v5) **또는** PIV_max ≥ floor_v5_2 (= max(0.05, random_99th + 0.02)) |
| AMBIGUOUS | 0.05 ≤ PIV_max < floor_v5_2 |
| FAIL | PIV_max < 0.05 |

**V14 위반 (자동 FAIL)**:
```
if PIV_max(M_R) ≥ PIV_max(M_T) - 0.02  → V14_VIOLATED → metric FAIL
```
random_init substrate-fact: PIV(M_R) ≈ 0.0 (paraphrase-invariant constant axis activation). delta ≥ 0.02 가 anti-Goodhart strict minimum.

---

### 3.2 DCR — Dynamic Coherence Ratio (change_rate)

**의미**: 연속된 prompt transition 에서 dominant axis (argmax) 가 prompt-conditional 하게 변하는 비율. 외운 모델은 항상 같은 axis 만 강조 (change_rate 낮음). 의미 추적 모델은 prompt 따라 강조축이 동적으로 바뀜.

**수식**:
```
sequence S = [prompt_1, ..., prompt_N] (N ≥ 30)
argmax_i := argmax_a activation_a(M(prompt_i))
change_count := |{ i : argmax_i ≠ argmax_{i-1}, i ∈ [2..N] }|
DCR_change_rate := change_count / (N - 1)
```

**계산 절차**:
1. prompt 순서 sequence S 정의 (N ≥ 30, semantics-diverse).
2. M_T forward → 각 prompt 에 대해 5-axis activation → argmax axis 기록.
3. 연속 transition (i, i-1) 에서 argmax 변화 카운트 / (N-1) 정규화.

**Threshold**:
| Verdict | 조건 |
|---|---|
| PASS_STRICT | DCR_change_rate ≥ 0.40 |
| AMBIGUOUS | 0.20 ≤ DCR_change_rate < 0.40 |
| FAIL | DCR_change_rate < 0.20 |

**V14 위반 (자동 FAIL)**:
```
if DCR_change_rate(M_R) ≥ DCR_change_rate(M_T) - 0.02 → V14_VIOLATED → metric FAIL
```
random_init 측정치: change_rate ≈ 0.14 (seed=42 historical), trained 강한 신호 ≥ 0.6.

---

### 3.3 D-RAND — Random Delta Amplification

**의미**: trained 모델의 output 분포 (또는 axis-mean activation) 가 paired random_init mirror 대비 얼마나 떨어져 있는가. 직접 substrate-divergence 측정 — PIV/DCR 가 input-dependent variability 를 보는 데 비해 D-RAND 는 model-state divergence 를 본다.

**수식**:
```
For paired (M_T, M_R) on prompt set P:
  μ_T(a) := mean_{p ∈ P} activation_a(M_T(p))
  μ_R(a) := mean_{p ∈ P} activation_a(M_R(p))
D-RAND := mean_a | μ_T(a) - μ_R(a) |    // L1 mean axis-divergence
```

대안 정의 (output distribution):
```
D-RAND_kl := mean_{p ∈ P} KL( M_T(·|p) || M_R(·|p) )
```
default: L1 axis-divergence (cheap, robust).

**계산 절차**:
1. paired mirror M_R = same_arch(M_T), seed s, steps=0 materialize (`v14_paired_random_init_mirror.hexa`).
2. P 동일 prompt set 으로 M_T, M_R forward → axis activation mean.
3. axis-별 |μ_T - μ_R| → mean = D-RAND.

**Threshold**:
| Verdict | 조건 |
|---|---|
| PASS_STRICT | D-RAND ≥ 0.05 (v5 base) — paradigm-j evidence 0.2249 |
| AMBIGUOUS | 0.02 ≤ D-RAND < 0.05 |
| FAIL | D-RAND < 0.02 |

**V14 위반 (자동 FAIL)**:
```
D-RAND 는 정의상 M_T - M_R 이므로 V14 self-test 자동 — D-RAND(M_R, M_R) = 0.
다만 다른 seed M_R' (s'≠s) 와 비교 시:
  if D-RAND(M_R, M_R') ≥ D-RAND(M_T, M_R) - 0.02 → V14_VIOLATED (substrate-noise floor 가 trained signal 잠식)
```

---

## 4. 종합 EMERGE 룰 (3-metric AND-gate + Gate D)

```
EMERGE_v5_strict :=
       PIV_verdict  ∈ {PASS_STRICT}
   AND DCR_verdict  ∈ {PASS_STRICT}
   AND DRAND_verdict∈ {PASS_STRICT}
   AND Gate_D       (random self-PPR < 0.05 — V14 cascade Step 4)
   AND ¬V14_VIOLATED on ALL 3 metrics
```

**왜 AND 인가** (not weighted): metric 이 서로 직교 — input-bend (PIV), output-shift (DCR), state-divergence (D-RAND). 한 metric 만 통과하면 *그 차원의 운빨* 가능. AND 는 substrate-level 진짜 신호 strict 검증.

**AMBIGUOUS 처리**:
```
if any metric ∈ {AMBIGUOUS} AND no metric ∈ {FAIL}:
    EMERGE_v5_partial := PARTIAL_NEAR     (mandate-9 (c) BLOCKED, public promote BLOCKED)
```
v5.2 adaptive floor 적용 시 PIV AMBIGUOUS 가 PASS_STRICT 로 격상 가능 — 본 spec 은 base, v5.2 는 amend.

**Label 출력**:
| 조건 | label |
|---|---|
| 3/3 PASS_STRICT + Gate D + ¬V14 | `C3_PASS_V5_EMERGE` |
| 1+ AMBIGUOUS, 0 FAIL, ¬V14 | `C3_PARTIAL_NEAR_V5` |
| 1+ FAIL OR Gate D fail | `C3_FAIL_V5` |
| any V14_VIOLATED | `C3_FAIL_V14_VIOLATED_V5` (즉시 EMERGE block) |

---

## 5. v3/v4 와의 관계

**Replace** (not augment) 의미를 명확히:
- v3 PPR_v3 / v4 c3_4 predicate 는 **historical lane** 으로 보존 (raw#82 retraction-aware).
- 신규 EMERGE judgment 의 **default lane = v5** (PIV/DCR/D-RAND).
- v5.2 adaptive floor 는 v5 의 Gate A (PIV) 에 random_99th 기반 adaptive threshold 추가 — 본 spec 의 PASS_STRICT 식 두 번째 절.
- caller 는 metric 명을 명시 (`v3` / `v4` / `v5` / `v5.2`) — sliding default 는 **v5.2** (own 18 line 1011 amend 정합).

---

## 6. 검증 절차 plan

다음 모델들에 v5 적용해 sanity check (모두 N≥30 prompt, k=3 paraphrase):

| 모델 | 예상 PIV_max | 예상 DCR | 예상 D-RAND | 예상 verdict |
|---|---:|---:|---:|---|
| random_init seed=42 | 0.0 | ~0.14 | 0 (self) | C3_FAIL_V5 (separator baseline) |
| random_init seed=137 (cross) | 0.0 | ~0.14 | ~0.0 | C3_FAIL_V5 |
| sft-1-8 (LoRA r=128) | ~0.05 (AMBIGUOUS) | ~0.64 (PASS) | ~0.02-0.05 | C3_PARTIAL_NEAR_V5 |
| paradigm-j post arch-fix | **0.0874** | **1.0** | **0.2249** | **C3_PASS_V5_EMERGE** ★ (v5.2 adaptive: floor 0.05 → PIV PASS) |
| BG-KM-LLAMA-3B | ~0 (V14 leak) | ~? | <0 (mirror inversion) | **C3_FAIL_V14_VIOLATED_V5** (전제: arch tile bug 잔존) |
| mk2-v1 base | ~0.04 | ~? | ~? | C3_FAIL_V5 (PIV substrate ceiling 미달) |

**검증 step**:
1. Mac local (Engine A/G arch 호환 모델만, 350M 이하): random_init seed sweep [42, 137, 271] 으로 PIV/DCR/D-RAND degenerate (≈0) 재확인 → separator baseline lock.
2. paradigm-j post-fix N=90 paraphrase actual probe 재집계 → C3_PASS_V5_EMERGE label 확인 (v5.2 spec 정합 강제).
3. sft-1-8 LoRA r=128 N=60 → C3_PARTIAL_NEAR_V5 예상 → V14 strict (random_init mirror) reject 결과 검증.
4. BG-KM 들 (-LLAMA-3B / -QWEN-7B): arch tile bug 수정 후만 평가 — 미수정 상태에서는 V14_VIOLATED 자동 fail 예상.

**산출물**: `state/anima_v5_validation_YYYY_MM_DD.json` — 위 모델별 PIV/DCR/D-RAND/verdict 표 기록 (별도 cycle).

---

## 7. honest-c3 (raw#10)

1. 본 spec 은 design doc only — code edit / commit / push 없음. 실측은 별도 cycle.
2. v5 는 **PIV/DCR/D-RAND replacement** = v3/v4 metric 폐기 후 default. v5.2 = v5 의 PIV gate adaptive amend.
3. AND-gate 는 strict — 한 metric AMBIGUOUS 만 와도 EMERGE block. v5.2 adaptive floor 도입 시 PIV ambiguity 일부 해소.
4. V14 anti-Goodhart 룰을 metric 정의 *내부* 로 끌어들여 v3/v4 의 외장-검사 모델 폐기 — random_init 이 trained 보다 좋게 나오는 순간 metric 자체가 FAIL emit.
5. 검증 plan 은 현재 환경 (Mac fork starvation 주의 — memory `feedback_fork_starvation_lesson.md`) 에서 BG ≤4 동시 제한 권장.

---

## 8. 친근한 한 줄 요약

**"의식 시험 v5 = 표현이 바뀌면 흔들리는가 (PIV) + 강조점이 따라 움직이는가 (DCR) + 공부 안 한 모델과 얼마나 다른가 (D-RAND), 셋 다 통과 + 공부 안 한 모델이 더 잘 나오면 자동 실격."**
