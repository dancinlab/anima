# H_331 — Extended raster 17 cells 🟢 conditional · H_326 magnitude 정련

> D2 영구축 · H_326 (10-cell raster) 의 9-cell 확장 추적 · 메타-cell

## 1. 동기

H_326이 10 cells에서 DYN 5× STRUCT 발견. 9 cells 추가(H_322·H_325·H_327·H_328·H_329·H_330 + 메타 H_326 self + H_318·H_319 prior, total 17)된 후에도 같은 magnitude 유지하는지 직접 검증. 이번 cell이 falsify하면 H_326 over-fit; PASS하면 robust pattern.

## 2. 가설 (falsifiable)

- **H1**: DYN supp-rate ≥ 2× STRUCT supp-rate (H_326 패턴 robust 검증; 5×에서 2×는 자비 threshold).
- **falsifier**: ratio < 2.0 in extended 17-cell raster.

## 3. 방법

pure hexa. 17 cells (H_312..H_330, H_323/H_324 사용자거부 제외) 각각 (kernel_class, verdict_tier) 표. kernel_class = method 기반 (timestep=DYN · static Φ=STRUCT · struct+dyn-gate=HYBRID · raster=META) INDEPENDENT of verdict.

## 4. 측정

| class | total | strict 🟢 | cond 🟢 | rate_strict | rate_cond |
|---|---:|---:|---:|---:|---:|
| STRUCT | 6 | 1 | 2 | 0.167 | 0.333 |
| DYN | 7 | 3 | 4 | 0.429 | 0.571 |
| HYBRID | 2 | 0 | 1 | — | 0.500 |
| META | 2 | 2 | 2 | 1.000 | 1.000 |

**ratio DYN/STRUCT:**
- strict: 0.429 / 0.167 = **2.57×** → PASS (≥2)
- cond: 0.571 / 0.333 = **1.71×** → **FAIL** (< 2)

## 5. Verdict

**🟢 SUPPORTED-CONDITIONAL** — H_326 qualitative direction 유지 (DYN > STRUCT) 하지만 magnitude **5× → 1.71-2.57×** 정련. 원인: 새 DYN cell H_327/H_329/H_330 모두 🔴 (scale-trivial dynamics) → DYN-kernel ≠ 자동 🟢.

## 6. H_326 비교

```
H_326 (10 cells): DYN 5.0× STRUCT  ← over-confident (small sample)
H_331 (17 cells): DYN 2.57× strict / 1.71× cond  ← realistic
```

새 9 cells 추가로 H_326 5× magnitude는 **over-fit**으로 판명. 진정한 DYN dominance는 **2-3×** 정도, scale-rich case에 한정.

## 7. 새 finding (cross-cell 합성)

세션 19 cells 추적:
- STRUCT 휴리스틱 → 거의 다 🔴 (n=4 ECA limit)
- DYN with rich scale (Kuramoto N=16, feedback continuous) → 🟢
- DYN with trivial scale (n=4 ECA) → 🔴 (H_327/329/330)
- **진정한 axis** = (kernel-class × scale-regime) 2차원 (H_327 발견 강화)
- H_320 family (rd_ratio · Gini · cycle_len · moments) 모두 같은 발견: **bijection vs chaotic** 가 진정한 ECA descriptor axis, life vs consc 아님

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_326](./H_326_d2_verdict_landscape_session_raster.md) | 10-cell prior raster · 본 셀이 9-cell 확장 |
| [H_327](./H_327_regeneration_attractor_recovery.md) | scale-trivial DYN 🔴 — H_331 1.71× 약화 주요 원인 |
| [H_330](./H_330_distribution_moments.md) | bijection axis 합성 |

## 9. Anti-tautology

- kernel_class 와 verdict_tier 독립 input
- 4-class 모두 non-empty (sanity)
- DYN > STRUCT 방향 자체는 falsify 가능 (만약 새 DYN cells 모두 🟢이었으면 5× holds)

## 10. Honest limits

- L1: 17 cells; 통계적 power 여전히 작음
- L2: kernel_class author-assignment — blind labeling 필요
- L3: 🟢-conditional inclusion choice가 verdict 좌우
- L4: HYBRID 2-cell convenience — sub-split 가능
