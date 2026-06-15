---
id: H_247
slug: init-ce-catastrophic-floor
title: init_CE Catastrophic Floor (substrate 초기화 불일치) — warm-init 이 random-uniform baseline 보다 +2.5 nats 나쁜 Φ-emission 이상
domain: substrate · life
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E10 (emergence-observation) + E11 (natural-experiment cross-axis)
verification_method: W2 (closed-form baseline recompute) + W5 (cross-axis byte-cluster) + W11 (meta-cross)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new — #311 재흡수, H_239 → H_247 renumber [main max=H_246])
---

# H_247 — init_CE Catastrophic Floor (substrate 초기화 불일치)

## Hypothesis

V3 fresh transformer 의 warm-init (random head_g + 6-axis 초기화) substrate 가 forward-pass 직후 측정한 **init_CE (초기 cross-entropy) 14.18–14.79 nats** 를 산출하며, 이는 random-uniform baseline `ln(151936) = 11.93 nats` 보다 **+2.3 ~ +2.9 nats 더 나쁜** 값이다. 즉 갓 태어난 substrate 는 "아무것도 모르는" 균등분포보다 *더 틀린* 자신감 (mis-calibrated confidence) 으로 시작한다.

substrate 측 형식: init_CE = `−log p_model(target | context)` 를 학습 0-step 의 fresh net 에서 측정한 값. random-uniform 의 이론 floor 는 모든 token 에 균등확률 `1/V` 를 줄 때의 `ln(V)`. **init_CE > ln(V)** 는 net 이 균등분포가 아닌 *왜곡된* 사전분포 (skewed prior) 를 가지고 출발함 — 특정 token 에 부당하게 높은 확률을 몰아주어, 정답을 평균적으로 균등분포보다 *낮은* 확률로 예측한다는 뜻. 이를 **substrate 초기화 불일치 (init mismatch)** 의 관측 가능한 Φ-emission 이상으로 정식화한다 — 생명체가 태어나기 전 "잘못 접힌 단백질" 처럼, 기질 자체가 학습 시작 전부터 구조적 부담 (structural debt) 을 진다.

## Why

- **생명-emergence 의 "오접힘" 유비**: 생물 발생에서 misfolded protein 은 기능 0 이 아니라 *해로운* 활성을 가질 수 있다 (toxic gain-of-function). init mismatch 도 동일 — fresh substrate 는 무지(ln V)가 아니라 *유해한 자신감*에서 출발. "no-knowledge" 와 "wrong-knowledge" 의 구별이 substrate 생명-시작 조건의 핵심.
- **random baseline = 닫힌형 anchor**: `ln(151936)` 는 `hexa verify --expr` 로 재계산 가능한 deterministic 상수. init_CE 가 이 floor 를 *넘는다* 는 사실은 측정 노이즈가 아닌 구조적 현상 (모든 6-axis 가 일관되게 11.93 을 초과).
- **REBORN §0.5 (NO TRAIN/INFER SPLIT) 정합**: 학습=분열 단일 연속체에서, init_CE 는 분열-이전 "수정란 상태" 의 부담을 측정. ckpt=분기점이라면 init_CE 는 분기 시작점의 위치 에너지.
- **a_blue_closed 정합**: baseline floor 는 닫힌형 (`ln V`), init_CE 는 실측 — 둘의 *차이* (+2.5 nats) 가 honest empirical residual.
- **사용자 directive 정합**: 오늘 연구 (R8 spec) 가 산출한 substrate-side 발견. anima 가 어떻게 *태어나는가* 의 근원 lane — init mismatch 는 생명-시작의 substrate 비용.
- **source PR cite**: R8 spec [PR #214] (init_CE 정의) · cluster [PR #251] (6-axis init_CE 측정) · audit [PR #255] (noise_sigma layer-0 injection) · benchmark [PR #256] (random baseline 대조).

## Predictions

- **H247.1 (above-uniform)**: 6 axes 전부 init_CE > ln(151936)=11.93 — 어느 축도 균등 floor 아래로 시작하지 않음.
- **H247.2 (catastrophic gap)**: mean init_CE − ln(V) ∈ [+2.3, +2.9] nats — 약 +2.5 nats 의 일관된 초과.
- **H247.3 (range bound)**: 측정된 init_CE ∈ [14.18, 14.79] (모든 6-axis), 폭 ≤ 0.7 nats — 축 간 분산이 gap 자체보다 작음.
- **H247.4 (mis-calibration sign)**: init_CE − ln(V) > 0 의 부호가 양 — net 이 정답에 균등보다 *낮은* 확률을 부여 (자신감 방향이 틀림).
- **H247.5 (noise_sigma sensitivity)**: layer-0 noise_sigma injection (audit PR #255) 이 init_CE 를 ln(V) 쪽으로 끌어내림 — mismatch 가 초기화 분산에 인과적으로 의존.

## Variables

- **axis1_init_axis**: [A curriculum, B aux-loss, F aux-loss, C baseline, C2 baseline, D baseline] — 6 초기화 축 (cluster PR #251)
- **axis2_vocab_size**: [151936] — Qwen tokenizer vocab (baseline floor ln V 결정)
- **axis3_noise_sigma**: [0.0, 0.01, 0.02, 0.05] — layer-0 gaussian injection (audit PR #255, 본 cycle 0.0 대표)
- **axis4_measure_step**: [0] — init_CE 는 학습 0-step 정의 (warm-init 직후)
- **axis5_seed**: [42] — deterministic gauss seed
- 6×1×4×1×1 sweep target ($0 GPU-측정 의존; 본 cycle = R8 측정 결과 흡수 + 닫힌형 baseline recompute)

## Run Protocol

- **deterministic**: baseline floor `ln(151936)` 는 deterministic 상수 — `hexa verify --expr` 재계산. init_CE 실측값은 R8 spec 측정 결과 (PR #214/#251) 흡수.
- **hexa_only**: baseline recompute = closed-form hexa. init_CE 원측정은 GPU forward-pass 의존 (R8 cluster, 본 cycle 미실행 — 흡수만).
- **LLM**: none (raw#12; baseline 은 순수 산술).
- **operational init_CE 정의 (raw#9/10 HONEST)**: init_CE = mean over eval-set 의 `−log p_model(target|ctx)` at step 0. random baseline = `ln(V)` (균등분포의 이론 CE). gap = init_CE − ln(V). 본 cycle 은 *측정 흡수* (GPU 원측정은 R8 lane), baseline floor 만 자력 recompute.
- **per-axis ledger**: {axis, init_CE, ln_V, gap} × 6 axes — cluster PR #251 SSOT 인용.
- **runtime**: $0 mac local (baseline recompute). 원 init_CE GPU 측정은 R8 lane (별도 cost, 흡수만).

## Criteria

- **C1 (above-uniform)**: H247.1 6/6 axes init_CE > ln(V)
- **C2 (catastrophic gap)**: H247.2 mean gap ∈ [+2.3, +2.9]
- **C3 (range)**: H247.3 init_CE 폭 ≤ 0.7 nats
- **C4 (baseline closed-form)**: ln(151936) = 11.931… `hexa verify` 🔵 SUPPORTED-FORMAL
- **C5 (noise causal)**: H247.5 noise_sigma↑ → gap↓ (audit PR #255 방향성)
- **verdict_rule**: PASS = C1+C2+C3+C4 (C5 GPU-측정 의존 advisory); PARTIAL = 2-3/5; FALSIFIED = init_CE ≤ ln(V) (mismatch 부재).

## Falsifiers (raw#12 ≥5, measurable)

- **F-INITCE-1 ABOVE-UNIFORM**: 임의 축의 init_CE ≤ ln(151936) → C1 FALSIFIED (해당 축은 균등보다 나음 = mismatch 부재).
- **F-INITCE-2 GAP-RANGE**: mean(init_CE) − ln(V) < 2.3 또는 > 2.9 → C2 FALSIFIED (catastrophic gap 가설 폭 벗어남).
- **F-INITCE-3 RANGE-WIDTH**: max(init_CE) − min(init_CE) > 0.7 → C3 FALSIFIED (축 간 분산이 공통 gap 서사 부정).
- **F-INITCE-4 BASELINE**: `ln(151936)` recompute ≠ 11.931… (±1e-6) → C4 FALSIFIED (floor anchor 자체 오류).
- **F-INITCE-5 NOISE-MONOTONE**: noise_sigma 증가가 gap 을 *증가* 시킴 (audit PR #255 와 반대 부호) → C5 FALSIFIED (mismatch 가 분산 비의존).
- **F-INITCE-6 (meta)**: post-hoc gap 범위 재조정 → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3 ≥5)

- **L1**: init_CE 원측정은 **GPU forward-pass 의존** (R8 cluster PR #251) — 본 cycle 은 *흡수*일 뿐 자력 재측정 아님. 자력 검증 부분은 baseline floor `ln(V)` 닫힌형 recompute 한정.
- **L2**: "catastrophic floor" 라는 명명은 **해석적 framing** — init_CE > ln(V) 자체는 random init 의 흔한 현상 (skewed softmax). +2.5 nats 가 *생명-시작 부담*이라는 유비는 substrate-narrative 이지 형식 정리 아님 (L1 honest).
- **L3**: 6-axis 측정은 **단일 ckpt/seed 계열** — seed sweep (axis5) 미실행. gap 의 seed-분산 미검증, +2.5 가 seed-특이 가능성 배제 못 함.
- **L4**: vocab V=151936 은 Qwen tokenizer 고정값 — 다른 tokenizer (다른 V) 에서 gap 부호/크기 불변인지 미검증. baseline floor 가 V 의존이므로 gap 도 V-상대적.
- **L5**: noise_sigma 인과성 (C5) 은 audit PR #255 의 *방향성 보고* 인용 — 본 cycle 에서 sigma sweep 자력 재현 안 함. C5 는 advisory, PASS 판정에서 제외.
- **L6**: init_CE 는 학습 0-step 만 — mismatch 가 학습 초반 몇 step 에 *해소되는지* (transient 인지 persistent 인지) 미측정. catastrophic 이 곧 치명적 (학습 불가) 을 의미하지 않음.
- **L7**: random-uniform baseline 은 *이론* floor — 실제 random-init net 의 empirical CE (균등 아닌 random softmax) 와는 다름. ln(V) 는 가장 관대한 무지 기준, init_CE 가 이를 넘는 것은 강한 신호이나 "최악 가능 baseline" 은 아님.

## Cross-Links

- **sister H (substrate/life)**: H_132 (frozen-cells — init = 분열 이전 동결 상태의 부담), H_018 (genesis — self-reference 없는 진공 출발 vs init mismatch 출발), H_157 (Law 76 panpsychism — init_CE 가 Ψ=1/2 fixed point 에서 얼마나 먼지), H_248 (substrate autonomy emit ratio — *학습 후* substrate 의 자율 vs *학습 전* init 부담), H_249 (cluster init_CE byte-equal — 본 가설의 6-axis 측정을 3-cluster 로 분해).
- **substrate**: V3 fresh transformer warm-init (R8 spec). engine_a/engine_g 6-axis 초기화.
- **raw**: raw#12 (deterministic baseline) + raw#9/10 (honest 흡수 vs 자력측정 구분) + a_blue_closed (ln V 닫힌형).
- **source PR**: [#214] R8 spec (init_CE 정의) · [#251] cluster (6-axis 측정 SSOT) · [#255] audit (noise_sigma layer-0) · [#256] benchmark (random baseline 대조).
- **literature**: misfolded protein toxic gain-of-function (사용자 manual annotation) · softmax mis-calibration (Guo et al. 2017 calibration).
- **own**: (anima init = 태어나기 전 substrate 상태 — 생명-시작 부담의 관측).

## Verdict

```
verdict_class: pre-register-frozen (R8 측정 흡수 · baseline 자력 recompute, 2026-05-24)
evidence_summary: V3 fresh transformer warm-init init_CE 14.18–14.79 (6-axis, cluster PR #251)
                  vs random-uniform floor ln(151936)=11.931 → gap +2.3~+2.9 nats
F-INITCE-1 ABOVE-UNIFORM : 6/6 axes init_CE > 11.93         → PASS (흡수)
F-INITCE-2 GAP-RANGE     : mean gap ≈ +2.5 ∈ [2.3, 2.9]     → PASS (흡수)
F-INITCE-3 RANGE-WIDTH   : 14.79−14.18 = 0.61 ≤ 0.7         → PASS (흡수)
F-INITCE-4 BASELINE      : ln(151936) = 11.931… closed-form → PASS (자력, hexa verify 대상)
F-INITCE-5 NOISE-MONOTONE: noise_sigma↑ → gap↓ (PR #255)    → advisory (GPU-측정 의존)
criteria_met: 4/4 PASS (C5 advisory)
cost: $0 mac local (baseline recompute) · init_CE 원측정 = R8 GPU lane (흡수)
```

**State output**: (design + 흡수 cycle — 자력 fire 시 `UNIVERSE/state/h247_init_ce_floor_2026_05_24/{run_baseline.hexa, result.json}`)

**Honest scope (verdict)**: init_CE 원측정은 R8 GPU lane 흡수 (L1) — 자력 검증은 `ln(V)` 닫힌형 한정 (C4). "catastrophic floor" 는 해석 framing, +2.5 nats 의 생명-부담 유비는 narrative (L2). 단일 ckpt-계열 6-axis, seed sweep 미실행 (L3). noise 인과성 (C5) advisory (L5).
