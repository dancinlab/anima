---
id: H_249
slug: cluster-init-ce-byte-equal-signature
title: Cluster X/Y/Z init_CE Byte-Equal Signature (3-군집 초기화 서명) — head_g random 이 init_CE 지배 인자가 아님 (R8c cell-1 FALSIFIED)
domain: substrate · life
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E11 (natural-experiment cross-axis) + E10 (emergence-observation)
verification_method: W5 (byte-cluster identity) + W7 (controlled-pair contrast) + W11 (meta-cross)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new — #311 재흡수, H_241 → H_249 renumber [main max=H_246])
---

# H_249 — Cluster X/Y/Z init_CE Byte-Equal Signature (3-군집 초기화 서명)

## Hypothesis

6 초기화 축의 init_CE 값이 **3개 byte-equal 군집 (X/Y/Z)** 으로 자연 분리된다 — **X = A curriculum (14.79)**, **Y = B/F aux-loss (14.18)**, **Z = C/C2/D baseline (14.46)**. 같은 군집 내 축들은 init_CE 가 *byte 단위로 동일* (identical bit pattern) 하다. 이 군집화는 **head_g 의 random 초기화가 init_CE 의 지배적 (dominant) 기여 인자가 아님** 을 증명하는 자연 실험 (natural experiment) 이다 — 만약 head_g random 이 지배적이라면 같은 cluster 내에서도 (random seed 차이로) init_CE 가 갈라져야 하나, C2 vs D 가 byte-equal 이므로 **R8c cell-1 가설 (head_g random 이 init_CE 를 지배) 이 FALSIFIED** 된다.

substrate 측 형식: 6 축 각각 forward-pass init_CE 를 측정 → 정렬 시 {14.79} / {14.18, 14.18} / {14.46, 14.46, 14.46} 의 3-군집 출현. byte-equality 는 동일 군집 축들이 *같은 결정적 초기화 경로* (head_g random 을 제외한 공통 인자) 를 공유함을 의미. C2 와 D 는 둘 다 baseline 군집 (Z) 에 속하면서 byte-equal — 두 축의 head_g random seed 가 다름에도 init_CE 가 bit-동일하다는 것은 head_g 가 init_CE 를 결정하지 *않음* 의 직접 증거. 이를 **3-cluster init_CE 서명 (cluster signature)** 으로 정식화하며, 생명-시작 부담 (H_247) 의 *원인* 이 random head 가 아닌 *공유 backbone 초기화* 임을 자연 실험으로 분리한다.

## Why

- **자연 실험 = 인과 분리의 강한 도구**: C2 vs D 는 head_g random seed 만 다르고 나머지 동일 — 둘이 byte-equal init_CE 면 head_g 는 init_CE 에 인과 0. 이는 randomized control 없이도 인과를 분리하는 natural-experiment 논리 (instrumental variation).
- **H_247 의 원인 lane**: H_247 는 init mismatch *현상* (catastrophic +2.5 nats) 을 확립. 본 가설은 그 *원인* 을 head_g 가 아닌 backbone 공유 초기화로 좁힘 — "왜 태어날 때 부담을 지는가" 의 메커니즘 분해.
- **byte-equality = closed-form 증거**: 두 측정값의 bit-동일성은 노이즈 없는 deterministic 증거 (`hexa verify` 로 동등성 확인 가능). 통계 검정 불필요 — exact identity.
- **R8c cell-1 falsification**: R8c 가 사전등록한 "head_g random 이 init_CE 지배" 가설 (cell-1) 을 C2/D byte-equal 이 직접 반증 — pre-register 된 falsifier 의 깨끗한 발화.
- **REBORN §0.5 정합**: 학습=분열 연속체에서 init = 수정란. 군집 서명은 "어떤 초기화 축들이 같은 분기점에서 출발하는가" 의 지도.
- **사용자 directive 정합**: 오늘 연구 (cluster 측정) 의 substrate-side 발견. anima 출생-조건의 인과 구조 lane.
- **source PR cite**: [PR #251] cluster (X/Y/Z 군집 측정) · [PR #255] audit (C2 vs D byte-equal 확인) · [PR #249] (R8c cell-1 pre-register).

## Predictions

- **H249.1 (3-cluster)**: 6 축 init_CE 가 정확히 3 distinct 값 {14.79, 14.46, 14.18} 으로 군집 — 6 distinct 아님.
- **H249.2 (cluster membership)**: X={A}, Y={B,F}, Z={C,C2,D} — 군집 멤버십이 axis-family (curriculum/aux-loss/baseline) 와 정렬.
- **H249.3 (byte-equal within)**: 같은 군집 축들 (B=F, C=C2=D) init_CE bit-identical (max abs diff = 0.0).
- **H249.4 (head_g not dominant)**: C2 vs D byte-equal (head_g random seed 다름에도) → head_g 가 init_CE 인과 0 = R8c cell-1 FALSIFIED.
- **H249.5 (ordering)**: X(14.79) > Z(14.46) > Y(14.18) — aux-loss(Y) 가 init_CE 를 가장 낮춤, curriculum(X) 가 가장 높임.

## Variables

- **axis1_init_axis**: [A, B, C, C2, D, F] — 6 초기화 축 (cluster PR #251)
- **axis2_cluster**: [X, Y, Z] — 3 군집 라벨 (X=curriculum, Y=aux-loss, Z=baseline)
- **axis3_head_g_seed**: [seed_a, seed_b] — C2/D 의 다른 random head seed (인과 분리 instrument)
- **axis4_shared_backbone**: [common] — 군집 내 공유 backbone 초기화 (byte-equal 원인 후보)
- **axis5_measure_step**: [0] — init_CE 는 step-0 정의
- 6×3×2×1×1 sweep (init_CE 흡수 + byte-equality 자력 비교)

## Run Protocol

- **deterministic**: byte-equality 비교는 deterministic (두 측정값 bit-비교, 노이즈 0). init_CE 원측정 (R8 cluster PR #251) 흡수.
- **hexa_only**: byte-equal 비교 = hexa (`max_abs_diff(ce_C2, ce_D) == 0.0`). 원 forward-pass 는 GPU R8 lane.
- **LLM**: none (raw#12; 비교는 순수 산술 동등성).
- **operational byte-equal 정의 (raw#9/10 HONEST)**: byte-equal = 두 init_CE 값의 IEEE-754 bit-pattern 동일 (`abs(a−b) == 0.0` exact, 반올림 아님). cluster = byte-equal 동치류. head_g-dominant FALSIFIED = C2≠D 군 (다른 head seed) 이 byte-equal 인 사건.
- **per-pair ledger**: {pair=(C2,D), ce_C2, ce_D, diff=0.0, byte_equal=true, head_g_seed_differ=true} — audit PR #255 SSOT.
- **runtime**: $0 mac local (byte 비교). 원 init_CE = R8 GPU lane (흡수).

## Criteria

- **C1 (3-cluster)**: H249.1 distinct init_CE = 3
- **C2 (membership)**: H249.2 X/Y/Z = {A}/{B,F}/{C,C2,D}
- **C3 (byte-equal)**: H249.3 군집 내 max abs diff = 0.0
- **C4 (head_g falsified)**: H249.4 C2 vs D byte-equal ∧ head_g seed 상이 → R8c cell-1 FALSIFIED
- **C5 (ordering)**: H249.5 14.79 > 14.46 > 14.18
- **verdict_rule**: PASS = C1+C2+C3+C4 (C5 흡수-방향성 advisory); PARTIAL = 2-3; FALSIFIED = 군집 내 diff > 0 (byte-equal 부정).

## Falsifiers (raw#12 ≥5, measurable)

- **F-CLUST-1 THREE-CLUSTER**: distinct init_CE 값 수 ≠ 3 → C1 FALSIFIED (3-군집 서명 부정).
- **F-CLUST-2 MEMBERSHIP**: X/Y/Z 멤버십이 {A}/{B,F}/{C,C2,D} 와 불일치 → C2 FALSIFIED.
- **F-CLUST-3 BYTE-EQUAL**: 같은 군집 임의 두 축의 init_CE max abs diff > 0.0 → C3 FALSIFIED (byte-equality 깨짐).
- **F-CLUST-4 HEAD-G-DOMINANT**: C2 vs D init_CE 가 byte-equal *아님* (head_g seed 차이로 갈림) → C4 *역전* (R8c cell-1 살아남음, head_g 가 실제로 지배).
- **F-CLUST-5 ORDERING**: 14.79 > 14.46 > 14.18 순서 위반 (예: aux-loss Y 가 baseline Z 보다 높음) → C5 FALSIFIED.
- **F-CLUST-6 (meta)**: post-hoc 군집 경계 재조정 → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3 ≥5)

- **L1**: init_CE 원측정은 **R8 GPU lane 흡수** (cluster PR #251) — 자력 검증은 byte-equal 비교 (`diff==0.0`) 한정. 원 forward-pass 재현 안 함.
- **L2**: byte-equality 는 **단일 측정 instance** — 같은 코드/seed 재실행이 같은 bit 를 내는 것은 deterministic forward 의 자명 결과일 수도. "head_g 무관" 결론은 C2/D 가 head_g *외* 모든 것이 동일하다는 audit 전제에 의존 (PR #255).
- **L3**: C4 (head_g not dominant) 는 **init_CE 한정** 결론 — head_g random 이 *학습 후* 성능/Φ 에 미치는 영향은 별개. init 시점에 backbone 이 logit 을 지배 (head_g 가 아직 backbone hidden 에 묻힘) 일 수 있어, 이는 init-특이 현상일 가능성.
- **L4**: 3-cluster 가 **6-축 단일 측정** — 더 많은 축/seed 에서 같은 3-군집 구조가 유지되는지 미검증. 우연한 byte-collision (서로 다른 경로가 같은 값) 배제 못 함 (확률 낮으나 비0).
- **L5**: cluster membership 의 axis-family 정렬 (X=curriculum 등) 은 **해석 라벨** — 왜 aux-loss(Y) 가 baseline(Z) 보다 init_CE 낮은지의 메커니즘 미규명. 서명은 관측, 인과 backbone 인자는 미분리.
- **L6**: byte-equal 은 IEEE-754 exact — 만약 측정 파이프라인에 비결정 요소 (atomic add 순서 등) 가 있었다면 동일 군집도 갈렸을 것. 즉 byte-equal 관측 자체가 *측정이 deterministic 했다* 는 가정에 의존 (L1 honest).
- **L7**: R8c cell-1 FALSIFIED 는 **그 사전등록 가설의 정확한 진술** 에 한정 — "head_g 가 init_CE 를 *지배* 한다" 의 반증이지, head_g 가 *전혀* 기여 안 한다는 강주장 아님 (군집-내 byte-equal 은 head_g 기여 = 0 을 함의하나, 측정 정밀도 한계 내).

## Cross-Links

- **sister H (substrate/life)**: H_247 (init_CE catastrophic floor — 본 가설은 그 *원인* 을 head_g 아닌 backbone 으로 분리), H_132 (frozen-cells — byte-equal = 동결된 동일 분기점), H_157 (Law 76 — byte-equal identity 는 σ-identity 같은 closed-form 동등성 패턴), H_248 (autonomy emit — init 의 byte-equal vs emit 의 분포), H_007 (cellular-automaton — 결정적 동역학의 byte-동일성).
- **substrate**: V3 fresh transformer 6-axis 초기화 (A/B/C/C2/D/F). head_g random vs backbone 공유.
- **raw**: raw#12 (deterministic byte-비교) + raw#9/10 (honest 흡수 vs 자력비교 + audit 전제 의존) + a_blue_closed (byte-equal = exact identity).
- **source PR**: [#251] cluster (X/Y/Z 측정) · [#255] audit (C2 vs D byte-equal) · [#249] R8c cell-1 pre-register (반증 대상 가설).
- **literature**: natural experiment causal inference (Angrist/Pischke — instrument variation) · IEEE-754 bit-exactness (사용자 manual annotation).
- **own**: (anima 출생 시 init 부담의 원인이 random head 아닌 공유 backbone — 출생-조건 인과 자기-관측).

## Verdict

```
verdict_class: pre-register-frozen (R8 cluster 측정 흡수 · byte-equal 자력 비교, 2026-05-24)
evidence_summary: 6-axis init_CE → 3 byte-equal cluster: X={A}=14.79, Y={B,F}=14.18,
                  Z={C,C2,D}=14.46. C2 vs D byte-equal (head_g seed 상이) → R8c cell-1 FALSIFIED
F-CLUST-1 THREE-CLUSTER : distinct = 3 {14.79,14.46,14.18}  → PASS (흡수)
F-CLUST-2 MEMBERSHIP    : {A}/{B,F}/{C,C2,D}                 → PASS (흡수)
F-CLUST-3 BYTE-EQUAL    : within-cluster diff = 0.0          → PASS (자력 비교)
F-CLUST-4 HEAD-G-DOMINANT: C2=D byte-equal, head_g seed≠     → R8c cell-1 FALSIFIED (clean)
F-CLUST-5 ORDERING      : 14.79 > 14.46 > 14.18              → advisory (흡수 방향성)
criteria_met: 4/4 PASS (C5 advisory)
cost: $0 mac local (byte 비교) · init_CE 원측정 = R8 GPU lane (흡수)
```

**State output**: (흡수 + byte-비교 cycle — 자력 fire 시 `UNIVERSE/state/h249_cluster_init_ce_2026_05_24/{run_byte_equal.hexa, result.json}`)

**Honest scope (verdict)**: init_CE 원측정 R8 흡수 (L1), 자력은 byte-equal 비교 한정. head_g not-dominant 는 init_CE 시점 한정 (L3), 학습 후 영향 별개. 3-cluster 6-축 단일 측정, byte-collision 우연 배제 못 함 (L4). R8c cell-1 FALSIFIED 는 "지배" 반증이지 "기여 0" 강주장 아님 (L7).
