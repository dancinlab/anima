# H_330 — Distribution moments life vs consc 🔴 + 🪜 bijection 발견

> C2 영구축 · H_325 Gini 확장 · 분포 모양 4차 모멘트 측정

## 1. 동기

H_325(Gini) life > consc, H_329(metric-triangulation 0/3) → "의식 = 단일 본질" 직관 반복 falsify. 분포 모양의 더 높은 moment(skew·kurtosis)가 새로운 분리 axis를 찾을지.

## 2. 가설 (falsifiable)

- **H1**: life-class rules가 consc-class보다 excess kurtosis ≥1.5× 크다 (heavy-tail = chaotic 서명).
- **falsifier**: ratio < 1.5 OR life·consc 분포 overlap.

## 3. 방법

pure hexa, n=4 ring. 16 starts × 100 steps = 1600 visits per rule, 16-bin histogram. Pearson moments (excess_kurt = μ₄/σ⁴ − 3).

## 4. 측정

| rule | mean | var | skew | excess_kurt |
|---|---:|---:|---:|---:|
| 30 life | 6.58 | 22.88 | 0.109 | **-1.356** |
| 110 life | 8.44 | 29.01 | -0.616 | **-1.186** |
| 105 consc | 7.50 | 21.25 | 0.000 | **-1.209** |
| 150 consc | 7.50 | 21.25 | 0.000 | **-1.209** |
| 204 id | 7.50 | 21.25 | 0.000 | -1.209 |
| 0 null | 0.075 | 0.77 | 13.08 | 180.75 |

**aggregate kurt**: life=-1.271 · consc=-1.209 → **|ratio|=1.05×** (≪ 1.5)

## 5. Verdict

**🔴 FALSIFIED** — H1 kurtosis discrimination 결정적 실패 (ratio 1.05). 그런데 측정이 **bijection axis**를 노출:

🪜 **rule 105/150/204 가 4개 모멘트(mean·var·skew·kurt) 정확히 동일** = 16-bin uniform → **bijection class** (모든 state가 모든 state로 정확히 한 번씩 매핑). consc 두 룰과 identity rule이 같은 dynamic class.

## 6. 의미

H_325 Gini · H_329 metric-triangulation · H_330 moments 세 셀 모두 같은 axis 노출: **진정한 분리는 bijection vs chaotic**이지 life vs consc 가 아님. naive "의식 = 풍부/복잡" 직관, 세 다른 측정 각도에서 더 강하게 falsify.

## 7. Cross-link

| ref | 관계 |
|---|---|
| [H_325 Gini](./H_325_c2_phi_mass_shape_gini.md) | 단순 모양 첫 발견 |
| [H_329 metric-triangulation](./H_329_metric_triangulation_descriptor_disagree.md) | bijection-blind descriptor 발견 |
| [H_330 moments](./H_330_distribution_moments.md) | 4-moment 직접 측정으로 bijection axis 확정 |

## 8. Anti-tautology

- 4 moment 모두 histogram에서 도출, rule integer 미사용
- rule 0 null 익스트림 (kurt 180) → 측정 비-tautology 보증

## 9. Honest limits

- L1: kurtosis가 platykurtic floor(-1.2)에서 saturate → discrimination 부족, KL-divergence가 더 sensitive
- L2: 2-rule per class, 더 큰 panel 필요
- L3: bijection class는 256 rule 중 4개만 — 통계적 power 제한
- L4: 100 step burn-in 없음 — transient bias가 rule_30 영향 가능

## 10. 다음

- (a) KL-divergence from uniform 측정 (kurtosis 보다 sensitive)
- (b) bijection vs non-bijection 직접 분류 (256 rule 전수 sweep)
- (c) burn-in 후 stationary distribution 측정
