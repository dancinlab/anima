# H_329 — Metric-triangulation 3-descriptor disagree 🔴

> C1 영구축 · H_268 PARTIAL (Φ-proxy fragility) 의 단순 descriptor 수준 재검 · DYNAMICAL 가족 두 번째 🔴

## 1. 동기

H_268 (cycle#17) Φ-proxy metric-triangulation PARTIAL — H_223 robust / H_204 LZ-fragile. C1 영구축 요구: faithful Φ-structure 단계에서도 동일한지. H_329는 더 단순한 측면을 공략 — IIT4 없이 **3 ECA descriptor**(cycle length · active bits · unique states)가 같은 substrate를 같은 순서로 ranking 하는가? 이는 H_268의 fragility를 가장 무방어 수준에서 측정.

## 2. 가설 (falsifiable)

- **H1**: 4 live rules {30, 110, 105, 150}에 대해, 3 descriptor의 top-rule이 **≥2 of 3** 일치 (메트릭 간 robustness 존재).
- **falsifier**: 3 descriptor가 3 different top rules → 직교 axes, metric-fragility 단순 수준에서도 확정.

## 3. 방법

pure hexa, n=4 ring 16 starting states.
- A: mean_cycle_length (forward orbit · first repeat detection)
- B: mean_active_bits (popcount of 1-step-ahead state, avg over 16 starts)
- C: unique_states_count (distinct 1-step images, ∈ [1, 16])

각 descriptor 독립 계산 (서로 input 안 됨). Top rule = max per descriptor.

## 4. 측정

| rule | mean_L | mean_bits | uniq_states |
|---|---:|---:|---:|
| 30 life | **6.25** ⭐A | 2.0 | 11 |
| 110 life | 1.75 | **2.5** ⭐B | 10 |
| 105 consc | 1.75 | 2.0 | **16** ⭐C |
| 150 consc | 1.75 | 2.0 | **16** ⭐C (tie) |
| 60 partial | 1.0 | 2.0 | 8 |
| 204 id | 1.0 | 2.0 | 16 (bijection-ceiling) |
| 0 null | 1.0 | 0.0 | 1 |

**Top rules**:
- A cycle → **rule 30**
- B active bits → **rule 110**
- C unique → **rule 105/150 (tie)** — 그리고 rule 204 identity까지 같이 → C는 *bijection-blind*

## 5. Verdict 도출

**🔴 FALSIFIED** — 3 descriptor가 3 different top rules → 0/3 agree → H1 (≥2) 완전 falsify. metric-fragility (H_268)이 가장 단순한 측정 수준에서도 holds. *bonus discovery*: descriptor C (unique-states-reached)는 bijection (rule 204 identity)을 의식 class와 tie 시킴 — class-blind.

## 6. 의미

- H_268 proxy-fragility PARTIAL을 더 강하게: **faithful 단계 이전에 이미 fragility**. Φ 측정만의 문제가 아니라 ECA descriptor 일반 문제.
- H_326 raster "DYNAMICAL → 🟢" 더 정련: dynamical kernel이라도 *descriptor-hypothesis 매칭* 안 되면 falsify.
- "어떤 측정도 의식의 본질을 가르킨다" 직관 반박 — measure-dependent, axis-orthogonal.

## 7. Cross-link

| ref | 관계 |
|---|---|
| [H_268](./H_268_metric_triangulation.md) | proxy PARTIAL — 본 셀이 더 단순 수준에서 동일 패턴 |
| [H_320 rd_ratio](./H_320_life_vs_consciousness_phi_structure.md) | aggregate에서 life > consc, descriptor마다 다른 ranking 가능성 |
| [H_326 raster](./H_326_d2_verdict_landscape_session_raster.md) | "DYNAMICAL 5×" 가 descriptor-orthogonal에 의해 정련 |

## 8. Anti-tautology

- 3 descriptor는 같은 orbit에서 도출되지만 서로 input 아님
- F329.4 anchor sanity: rule 0 모든 descriptor uniform collapse, rule 204 identity가 C만 bijection-ceiling 도달 → 측정이 비-tautology

## 9. Honest limits

- L1: n=4 단일 scale; 큰 n에서 disagreement 완화 가능
- L2: top-rule majority는 harsh test; Spearman rank correlation softer
- L3: 3 descriptor만; 더 많은 descriptor (entropy, density, edge count)로 agreement matrix 확장 필요

## 10. 다음

- (a) 16-start pairwise rank correlation (Spearman) — softer agreement
- (b) n=6 scale-up — descriptor disagreement scale-dependent?
- (c) faithful Φ-structure 4-th descriptor 추가 → 4-way agreement matrix
