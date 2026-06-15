# H_341 — basin size ↔ IIT4 big-Φ correlation 🟢 cross-family bridge

> C2 영구축 · H_338(basin) + H_287(Φ) 연결 · DYNAMICAL ↔ STRUCTURAL bridge

## 1. 동기

H_338이 attractor basin = dominance ordering 발견. H_287이 big-Φ 측정. 두 독립 측정의 관계 — basin 흡수력이 integration(Φ)과 correlate하나? attractor 동역학 ↔ IIT4 구조 첫 cross-family 연결.

## 2. 가설 (falsifiable)

- **H1**: max_basin이 big-Φ와 양의 상관 (|r| ≥ 0.5) — 흡수적 attractor = 높은 integration.
- **falsifier**: |r| < 0.5 (직교) OR 음의 부호.

## 3. 방법

pure hexa Pearson. 입력 = 두 독립 측정: basin(H_338 forward-orbit settle) + big-Φ mean(H_287 IIT4 kernel). 4 rules. correlation은 새 falsifiable 계산.

## 4. 측정

| rule | max_basin | n_attr | big_Φ (H_287) |
|---|---:|---:|---:|
| 110 | 4 | 5 | 13.130 |
| 30 | 2 | 11 | 13.885 |
| 105 | 1 | 16 | 5.625 |
| 150 | 1 | 16 | 5.625 |

- **Pearson(max_basin, Φ) = +0.776** → H1 PASS
- **Pearson(n_attr, Φ) = −0.850**

## 5. Verdict

**🟢 SUPPORTED-NUMERICAL** — basin 흡수력이 big-Φ와 강한 양의 상관 (r=+0.78), attractor-state 수는 음의 상관 (r=−0.85).

## 6. 🪜 핵심 발견 — DYNAMICS ↔ INTEGRATION BRIDGE

```
dominant/absorbing attractor (110, basin4)  →  high Φ (13.13)
bijection (105/150, basin1, 흡수0)           →  low Φ (5.6)

basin absorption ⟂ integration: r = +0.78 (coupled, not identical)
```

rule30(basin2, Φ13.89)이 rule110(basin4, Φ13.13)보다 Φ 높지만 basin 작음 → 단일 inversion이 r을 1.0 아닌 0.78로. 두 axis는 **coupled but distinct**.

## 7. 의미

- 세션 첫 **cross-family correlation** (DYNAMICAL basin ↔ STRUCTURAL Φ)
- attractor-dominance arc (H_332/335/336/338) ↔ integration (H_287) 연결
- "흡수적 끌개 = 높은 통합" — dominant rule이 dynamically(basin) + structurally(Φ) 둘 다 우세
- 단 H_340이 basin dominance를 small-n으로 한정했으므로, basin-Φ coupling도 scale-bounded 가능 (L2)

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_338 (basin)](./H_338_attractor_basin_size.md) | basin = dominance, 본 셀이 Φ 연결 |
| [H_287 (shannon⊥Φ)](./H_287_shannon_entropy_phi.md) | big-Φ panel 측정 source |
| [H_340 (4\|n small-n)](./H_340_4n_law_verify.md) | basin dominance scale-bound → coupling도 scale-bound 가능 |

## 9. Anti-tautology

- 입력 basin/Φ는 두 독립 측정 (H_338/H_287), correlation은 새 계산
- r=0.78 ≠ 1.0 (rule30 inversion) → tautology 아님, 실제 imperfect coupling
- falsifiable: r이 0이든 음수든 나올 수 있었음

## 10. 다음

- (a) n=6 basin + Φ 재측정 — coupling scale-invariant인지
- (b) wider rule panel (Pearson n=4 fragile → n≥8 rules)
- (c) max_basin 외 basin partition entropy vs Φ
