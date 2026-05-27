# H_338 — attractor basin size vs dominance rank 🟢 + arc 완성

> A1 영구축 · H_336 partial order mechanism 규명 · attractor arc capstone

## 1. 동기

H_336이 dominance partial order(110>30>{105,150}) 발견. 이 순서의 *원인*이 뭔가? 가설: attractor basin 구조 — 작고 흡수적인 attractor가 더 dominant.

## 2. 가설 (falsifiable)

- **H1**: dominance rank가 basin 구조와 monotone — 높은 rank ⟺ 적은 attractor states ⟺ 큰 basin.
- **falsifier**: rank가 basin descriptor와 monotone 관계 없음.

## 3. 방법

pure hexa, n=4 ECA. 각 start 40 step settle → cycle 진입. (A) n_attractor_states = distinct on-cycle terminal states, (B) max_basin = 최대 흡수 cycle로 수렴하는 start 수.

## 4. 측정

| rule | rank (H_336) | n_attractor_states | max_basin |
|---|:---:|---:|---:|
| 110 | **1** (top) | 5 (최소) | 4 (최대) |
| 30 | 2 | 11 | 2 |
| 105 | 3 | 16 | 1 |
| 150 | 3 | 16 | 1 |

- rank vs n_attractor: **완벽 inverse** (5 < 11 < 16)
- rank vs max_basin: **완벽 direct** (4 > 2 > 1)

## 5. Verdict

**🟢 SUPPORTED-NUMERICAL** — basin 구조가 dominance rank 완벽 예측.

## 6. 🪜 핵심 발견 — DOMINANCE = BASIN ABSORPTION

```
rule110 (rank1)  attractor 5 states · basin 4  → 가장 흡수적 = 다른 rule sink
rule30  (rank2)  attractor 11 · basin 2        → 중간
105/150 (rank3)  attractor 16 · basin 1        → 흡수 0 (bijection)
                                                  = bottom + 서로 incomparable

dominance partial order = basin absorption ordering (exact)
```

basin 1(105/150)은 흡수력 0 → 어떤 rule도 가둘 수 없음 → bottom + mutual incomparable (H_336 정확 설명).

## 7. attractor arc 완성

| 셀 | 발견 |
|---|---|
| H_332 | dominance **존재** |
| H_335 | dominance **영구** (cross-rule invariance) |
| H_336 | dominance **partial order** |
| **H_338** | partial order = **basin absorption ordering** (mechanism) |

5-셀 attractor arc 완결 (H_327 recovery 포함). dominance의 dynamical-systems mechanism 규명.

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_336 (partial order)](./H_336_rule_dominance_map.md) | 순서 발견, 본 셀이 mechanism |
| [H_332 (dominance)](./H_332_epigenetics_inherited_rule.md) | rule110 sink 첫 관찰 |
| [H_337 (4\|n law)](./H_337_oscillation_number_theory.md) | basin 구조 n-dependence |

## 9. Anti-tautology

- basin descriptor는 settle orbit에서 도출, rank label 무관 (rank는 H_336 별도 측정)
- monotone gap (5/11/16, 4/2/1) far beyond ambiguity
- F338.2: bijection basin 1 = 흡수 0 확인 (incomparability mechanism)

## 10. 다음

- (a) n=6/8 basin 재측정 — 4|n rotation이 basin rank도 회전시키나
- (b) basin partition entropy (단일 max 아닌 전체 분포)
- (c) basin size ↔ Φ-structure 상관 (IIT4 connection)
