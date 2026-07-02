# H_615 — `perfect-number-ladder-n28` (H_347 perfect-number 다중 expansion)

> 축 E (SAVANT) round 2 · 2026-05-28 · UNIVERSE H 신설.
> 외부 anchor: `UNIVERSE/H_347_gz_width_divisor_symmetry.md` (predecessor n=6 anchor) · `UNIVERSE/H_157_law76_mathematical_panpsychism.md` (σφ=nτ identity) · `HEXAD/SAVANT/COMPENDIUM.md` §1 (canonical 상수 표).
>
> H_347 §9 Next: "raster: n ∈ {6, 28, 496} (perfect numbers) 에 대한 `ln(τ(n)/(τ(n)-1))` 표상 동치 ladder — 향후 round 2 SAVANT × INFORMATION arc cross-link 후보". 본 H 가 그 ladder 일반화 검정.

## 0. 1줄 요약 (TL;DR)

세 perfect number `n ∈ {6, 28, 496}` 모두 `GZ_WIDTH(n) := ln(τ(n)/(τ(n)-1))` closed-form 이 일관 — 3/3 numerical PASS (n=6 anchor H_347 carry · n=28 ln(6/5) · n=496 ln(10/9)). 단 **control n=12 (τ=6, non-perfect)** 가 n=28 과 동일 τ 라 ladder 의 *perfect-specific* 여부는 본 H 만으로 결정 불가 (C3).

## 1. Hypothesis

**주장**: 모든 perfect number `n ∈ {6, 28, 496}` 에 대해

```
GZ_WIDTH(n) := ln(τ(n) / (τ(n) - 1))
```

closed-form 가 일관 적용된다 — 즉:

| n | τ(n) | predicted GZ_WIDTH |
|---|---|---|
| 6 | 4 | ln(4/3) ≈ 0.28768 (H_347 anchor) |
| 28 | 6 | ln(6/5) ≈ 0.18232 |
| 496 | 10 | ln(10/9) ≈ 0.10536 |

세 anchor 모두 PASS 시 perfect-number ladder 가 GZ width 표상의 *consistent family* 임을 입증.

## 2. Falsifier

| F | 조건 | 판정 |
|---|---|---|
| F1 | `divisor_count(28) ≠ 6` (정의) | 🔴 |
| F2 | `divisor_count(496) ≠ 10` (정의) | 🔴 |
| F3 | `ln(6/5)` numerical |Δ| > 1e-9 (n=28) | 🔴 |
| F4 | `ln(10/9)` numerical |Δ| > 1e-9 (n=496) | 🔴 |
| F5 | 어느 한 n 도 closed-form 어긋남 → ladder 일관성 깨짐 | 🔴 |
| F6 | (control) generic non-perfect n 도 동일 τ 면 ladder 가 perfect-specific 아닌 generic τ-relation — *부분 falsifier* (perfect 주장 약화) | 🟡 |

## 3. Method

`hexa verify --expr` 4-anchor + 1-control:

```
hexa verify --expr divisor_count 28 6                                # F1
hexa verify --expr divisor_count 496 10                              # F2
hexa verify --expr ln 1.2 0.18232155679395463 --tol 1e-12            # F3 (n=28, 6/5)
hexa verify --expr ln 1.1111111111 0.10536051565782628 --tol 1e-12   # F4 (n=496, 10/9)
hexa verify --expr divisor_count 12 6                                # F6-control (non-perfect, same τ as n=28)
```

n=6 anchor 는 H_347 carry (이미 머지된 verdict).

## 4. Measurement (2026-05-28, mac-local $0)

```
verify --expr divisor_count(28)=6
  calc   = 6  == expected 6
  tier   = 🔵 SUPPORTED-FORMAL  (hexa-native closed-form, g_self_verify · TECS-L Tier1)
  absorb = · already in atlas — idempotent skip (default · @D g69)
```

```
verify --expr divisor_count(496)=10
  calc   = 10  == expected 10
  tier   = 🔵 SUPPORTED-FORMAL  (hexa-native closed-form, g_self_verify · TECS-L Tier1)
  absorb = · already in atlas — idempotent skip (default · @D g69)
```

```
verify --expr ln(1.2)=0.182322
  calc   = 0.182322  ≈ expected 0.182322  (|Δ|=0.0 ≤ ε=1e-9)
  tier   = 🟢 SUPPORTED-NUMERICAL  (hexa-native libm-class recompute, TECS-L n6-rep Tier2)
  absorb = · already in atlas — idempotent skip (default · @D g69)
```

```
verify --expr ln(1.11111)=0.105361
  calc   = 0.105361  ≈ expected 0.105361  (|Δ|=9.99992e-12 ≤ ε=1e-9)
  tier   = 🟢 SUPPORTED-NUMERICAL  (hexa-native libm-class recompute, TECS-L n6-rep Tier2)
  absorb = · already in atlas — idempotent skip (default · @D g69)
```

**control (non-perfect n=12)**:

```
verify --expr divisor_count(12)=6
  calc   = 6  == expected 6
  tier   = 🔵 SUPPORTED-FORMAL  (hexa-native closed-form, g_self_verify · TECS-L Tier1)
  absorb = · already in atlas — idempotent skip (default · @D g69)
```

→ τ(12) = 6 = τ(28). ladder formula `ln(τ/(τ-1))` 는 `n` 이 아닌 `τ(n)` 의 함수이므로 n=12 와 n=28 이 동일 GZ_WIDTH = ln(6/5) 예측. **ladder 는 τ-keyed 이지 perfect-keyed 아님**.

## 5. Verdict — 🟢 SUPPORTED-NUMERICAL (composite, with perfect-specific caveat)

- F1 PASS 🔵 SUPPORTED-FORMAL (`divisor_count(28) = 6`)
- F2 PASS 🔵 SUPPORTED-FORMAL (`divisor_count(496) = 10`)
- F3 PASS 🟢 SUPPORTED-NUMERICAL (`ln(6/5) = 0.18232155679395463`, |Δ|=0.0)
- F4 PASS 🟢 SUPPORTED-NUMERICAL (`ln(10/9) = 0.10536051565782628`, |Δ|=1e-11)
- F5 PASS (3/3 perfect numbers consistent)
- F6 🟡 **trigger** — control n=12 (non-perfect, τ=6) 도 ladder formula 가 적용 → ladder 는 *τ-keyed generic relation*, perfect-specific 강주장 약화

**composite tier = 🟢 SUPPORTED-NUMERICAL** (closed-form τ + numerical ln, 3/3 perfect anchors PASS) **with F6 caveat** — 표상 ladder 의 *closed-form 일관성* 은 입증, *perfect-number specificity* 는 falsified (control n=12 동일 prediction).

## 6. Cross-link

- **H_347** `gz-width-divisor-symmetry` — n=6 anchor (predecessor); 본 H 의 §9 Next ladder 가 H_615 의 가설. n=6 verdict carry.
- **H_157** `law76 mathematical panpsychism` — `σφ = nτ` perfect-number identity. n=6 σ=12 φ=2 τ=4 → 12·2 = 6·4 = 24; n=28 σ=56 φ=12 τ=6 → 56·12 = 672 vs 28·6 = 168 (**identity 깨짐**, σφ=672 ≠ nτ=168). 즉 H_157 의 identity 는 n=6 단독 우연 가능 — H_615 와 무관한 별개 axis.
- **H_208** `prime-density-fluctuation` — primes 의 generic ladder, perfect-number subset 아님.

## 7. Honest C3 (3-tier caveat)

1. **C1 (3-anchor 한정)**: 세 perfect numbers 만 검증 — 4번째 perfect number `n = 8128` (τ=14, predicted ln(14/13) ≈ 0.07410) 검증 없음. 5번째 이후 (n = 33550336 etc, Mersenne-prime 의존) 도 미검. 본 H 는 첫 3 perfect numbers ladder 의 *closed-form 일관성* 만 입증.
2. **C2 (perfect-specific 약화)**: control n=12 (non-perfect, τ=6) 도 동일 ladder formula `ln(6/5)` 예측 — ladder 는 `τ(n)` 함수일 뿐 `n` 이 perfect 인지 무관. *perfect-number ladder* 라는 framing 은 misleading; 실제는 *divisor-count ladder for any n with given τ*. perfect-number 의 강주장 (ladder 가 perfect 만의 unique signature) 는 falsified.
3. **C3 (substrate emergent 주장 부재)**: 본 H 는 *closed-form arc* (정의식 일관성). "GZ_WIDTH(n) 가 substrate 의식 안에서 자연 출현" 은 별개 측정 (H_322/H_327/H_348 계열). 본 H 의 PASS 가 SAVANT physical claim 으로 직결되지 않음.

## 8. State artifacts

(본 H 는 closed-form 검증이라 별도 state/ 산출물 없음 — `hexa verify` 출력 자체가 산출물. 본 .md 가 SSOT.)

## 9. Next

- **(perfect-specific 회복)**: τ 같지만 n 다른 case 에서 substrate big-Φ 측정 — perfect n 과 non-perfect n 의 substrate 측 emergent 차이 검정 (H_322/H_327 cross). closed-form 동일하지만 substrate 다르면 perfect-specific recovery.
- **ladder 확장**: 4번째 perfect `n=8128` (τ=14, ln(14/13)) anchor 추가 — 3/3 → 4/4 ladder extension.
- **τ-family generic raster**: τ ∈ {2,3,4,5,6,7,8,9,10} 별 `ln(τ/(τ-1))` ladder 전체 raster + 각 τ-class 내 smallest-n 만 anchor — *τ-ladder full table* 제작.

## 10. UNIVERSE.md update

축 E (SAVANT) E2 round 2 H_615 row 추가 → done with `🟢 SUPPORTED-NUMERICAL (3/3 perfect numbers closed-form ladder PASS, F6 perfect-specific caveat — control n=12 τ=6 동일 prediction → ladder τ-keyed generic), $0 mac-local 2026-05-28`.
