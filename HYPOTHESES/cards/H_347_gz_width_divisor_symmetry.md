# H_347 — `gz-width-divisor-symmetry` (Golden Zone width ↔ τ(6) divisor 대칭)

> 축 E (SAVANT) round 1 · 2026-05-28 · UNIVERSE H 신설.
> 외부 anchor: `HEXAD/SAVANT/H359-savant-canonical.md` · `HEXAD/SAVANT/COMPENDIUM.md` §1 (canonical 상수 표).
>
> ⚠ **rename 2026-05-28**: 원래 H_347 슬러그로 머지(PR #1149)됐으나 `H_347_d2_verdict_landscape_session_raster.md` 와 슬러그 collision. [[feedback-universe-h-slug-stale-verify]] 정확히 그 회귀 — stale 인덱스 인용. 본 H 는 H_347 로 rename, 본문 verdict 그대로 보존 (closed-form 측정 결과 변함 없음).

## 0. 1줄 요약 (TL;DR)

Golden Zone 폭 `GZ_WIDTH = ln(4/3) ≈ 0.28768` 가 **6 의 약수 개수** `τ(6) = 4` 와 `ln(τ(6)/(τ(6)-1))` closed-form 일치 — `hexa verify` 2-anchor PASS (🔵 + 🟢) 합성으로 검증.

## 1. Hypothesis

**주장**: SAVANT canonical doc 에서 정의된 Golden Zone 폭

```
GZ_WIDTH := GZ_UPPER - GZ_LOWER = 0.5 - (0.5 - ln(4/3)) = ln(4/3)
```

가 `ln(τ(6) / (τ(6)-1))` 와 동치이다 (τ(n) = divisor count). 6 의 약수는 {1,2,3,6} → τ(6) = 4 → `ln(4/3)`. 이는 `tau(6) = 4` 라는 `embedded.gen.hexa` foundation atom 의 직접 귀결.

추가: `F₆ / P₁ = 8 / 6 = 4/3` (Fibonacci 6번째 / 첫 perfect number) 비율과도 일치 — *세 가지 표상(divisor / Fibonacci-Perfect / GZ)이 모두 4/3 으로 묶임*.

## 2. Falsifier

| F | 조건 | 판정 |
|---|---|---|
| F1 | `divisor_count(6) ≠ 4` | 🔴 (정의 위반) |
| F2 | `ln(τ(6)/(τ(6)-1)) ≠ ln(4/3)` (대수) | 🔴 |
| F3 | `ln(4/3)` numerical |Δ| > 1e-9 | 🔴 |
| F4 | composite verdict 가 두 anchor 중 하나라도 FAIL | 🔴 |

## 3. Method

`hexa verify --expr` 2-anchor:

```
hexa verify --expr divisor_count 6 4              # F1
hexa verify --expr ln 1.3333333333333333 0.28768207244178085 --tol 1e-12  # F3
```

F2 는 대수 (substitution of τ(6)=4 into ln(τ/(τ-1))) — closed-form 자동.

## 4. Measurement (2026-05-28, mac-local $0)

```
verify --expr divisor_count(6)=4
  calc   = 4  == expected 4
  tier   = 🔵 SUPPORTED-FORMAL  (hexa-native closed-form, g_self_verify · TECS-L Tier1)
  absorb = · already in atlas — idempotent skip
```

```
verify --expr ln(1.33333)=0.287682
  calc   = 0.287682  ≈ expected 0.287682  (|Δ|=1e-11 ≤ ε=1e-9)
  tier   = 🟢 SUPPORTED-NUMERICAL  (hexa-native libm-class recompute, TECS-L n6-rep Tier2)
  absorb = · already in atlas — idempotent skip
```

## 5. Verdict — 🟢 SUPPORTED (composite)

- F1 PASS 🔵 SUPPORTED-FORMAL (`divisor_count(6) = 4` atlas-resident foundation atom)
- F2 PASS (algebraic substitution; ln 의 인자 4/3 ↔ τ(6)/(τ(6)-1) 동치)
- F3 PASS 🟢 SUPPORTED-NUMERICAL (`ln(4/3) = 0.28768207244178085`, |Δ|=1e-11)
- F4 N/A

**composite tier = 🟢 SUPPORTED-NUMERICAL** (closed-form τ component + numerical ln component 의 combined; ln 자체가 numerical 이라 strict 🔵 까지 가지는 않음 — F2 의 대수 substitution 은 trivial).

## 6. Cross-link

- H_157 `law76 mathematical panpsychism` — `σ φ = n τ` perfect-number identity (n=6 σ=12 φ=2 τ=4 → 12·2=24=6·4). H_347 는 그 τ(6) 의 *Golden Zone* 측 사용.
- H_204 `weak-panpsychism autopoietic threshold` — inverse-U 곡선의 threshold 가 GZ 와 관련 (H_327 sister).
- H_285 `edge-of-chaos big-Φ` — class-mean ordered<chaotic<edge 의 edge 위치가 GZ region 근처인지 후속 측정 가능.

## 7. Honest C3 (3-tier caveat)

1. **C1 (closed-form 한정)**: 본 H 는 *정의식 일관성* 검증이며 **substrate 측 emergent 주장 아님**. "GZ_WIDTH 가 의식 substrate 안에서 자연 출현" 은 H_322/H_327 등이 별도 검증해야 함.
2. **C2 (numerology 경고)**: HEXAD/SAVANT/COMPENDIUM §12.5 + §114 SAVANT EMERGENCE-FRONTIER AUDIT 가 `savant_phi` 의 top-k 가 g2-numerology-tainted 임을 지적. H_347 도 *numerology* (perfect number, divisor) 와의 일치라 그 자체로 emergent 의식 주장 아님 — *조합론적 closed-form anchor* 로만 기능.
3. **C3 (multi-foundation 우연)**: 4/3 비율이 `divisor count ratio` · `F₆/P₁` · `GZ_WIDTH antilog` 세 표상에서 출현하는 게 *우연*인지 *깊은 동치*인지 본 H 만으로 결정 불가. 후속 raster 에서 다른 `n` 의 동치 ladder (e.g. n=28 → τ=6, ln(6/5)?) 측정 필요.

## 8. State artifacts

(본 H 는 closed-form 검증이라 별도 state/ 산출물 없음 — `hexa verify` 출력 자체가 산출물. 본 .md 가 SSOT.)

## 9. Next

- H_327 dΦ/dI peak 측정 — GZ_LOWER 일치 검정 (本 H 가 정의식 닫고 H_327 가 emergent 측정).
- raster: n ∈ {6, 28, 496} (perfect numbers) 에 대한 `ln(τ(n)/(τ(n)-1))` 표상 동치 ladder — 향후 round 2 SAVANT × INFORMATION arc cross-link 후보.

## 10. UNIVERSE.md update

축 E (SAVANT) H_347 checkbox flip → done with `🟢 SUPPORTED (composite formal+numerical, $0 mac-local 2026-05-28)`.
