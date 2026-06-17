# Bench #4 — TURING-MITOSIS (얼룩말 무늬 분열)

> UNIVERSE H_344 (Gierer-Meinhardt Turing pattern, 1D ring, ρ_c≈6 🟢 6/6) 의 anima MITOSIS cell-grid 2D 적용 — 32×32 토러스에서 RD 시뮬레이션 재현 + critical ratio 측정.

## 1. 동기 — 1D ring 의 Turing threshold 가 2D 격자에서도 같은 ρ_c 를 주는가?

H_344 는 1D ring (N=32) 에서 Gierer-Meinhardt 반응-확산 시뮬레이션으로 Turing 불안정 임계비 ρ_c≈6 을 측정했다 (var=1e-3 crossing). 이 벤치는 동일 모델을 **2D 32×32 주기경계 토러스**로 확장하여:

1. 패턴이 1D 단면이 아닌 *2D 점/줄무늬* 로 출현하는지 확인하고,
2. ρ_c 가 1D 와 같은 ~6 근방에 잡히는지 비교하고,
3. spatial autocorrelation 으로 패턴 wavelength 를 측정한다.

H_344 의 두 falsifier 분기(no-pattern-ever vs grows-for-all-ratios)에 더해 본 벤치는 **ρ_c-out-of-range** (ρ_c < 4 또는 > 8) 를 추가 falsifier 로 둔다 — 2D 가 1D 보다 *훨씬 다른* threshold 를 보이면 가설(차원-불변)이 약화된다.

## 2. 가설

- **H1 SYMMETRIC-STAYS-UNIFORM**: ρ=1 에서 var(u) < 1e-4 (대칭 control, Turing 불가능).
- **H2 ASYMMETRIC-BREAKS-SYMMETRY**: ρ=15 에서 var(u) > 1e-2 (강한 비대칭, 유한진폭 패턴).
- **H3 THRESHOLD-EXISTS**: var(u) 가 1e-3 을 가로지르는 ρ_c ∈ (1, 15) 가 측정 가능.
- **H4 MONOTONE-IN-RATIO**: var(u)(ρ) 는 tol 내 non-decreasing.
- **H5 BOUNDED-FINITE**: 모든 ρ 에서 var 유한 (NaN/발산 없음).
- **H6 DETERMINISTIC**: ρ=1 재적분이 byte-identical.
- **HX RHOC-IN-H344-RANGE**: ρ_c ∈ [4, 8] (H_344 1D 측정값 6 ± 2).

## 3. 모델

```
∂u/∂t = Du · lap2d(u) + u²/v − u     (활성자: 단거리 자기촉매)
∂v/∂t = Dv · lap2d(v) + u²     − v   (억제자: 장거리 억제)

lap2d(x)_{i,j} = x_{i-1,j} + x_{i+1,j} + x_{i,j-1} + x_{i,j+1} − 4·x_{i,j}
```

공간균일 정상상태 u*=v*=1. 2D 5-point Laplacian, 주기경계 토러스.

**측정량**:
- `var_u` = (1/N²) · Σ (u_ij − ū)² spatial variance of final u-field.
- `mean_u`
- `peak_lag` = radial autocorrelation 의 첫 비자명 peak 의 lag (in cells) — 패턴 wavelength.

**ρ_c 추출**: var_u(ρ) 가 1e-3 을 가로지르는 ρ 구간의 중점 (선형보간).

## 4. 측정 방법

`bench/turing_mitosis/bench.hexa`:

- N=32×32 (=1024 cells × 2 species), 주기경계.
- Discrete 5-point Laplacian on torus.
- IC (deterministic, NO RNG): u=v=1 + cell (16,16) 에 u += 0.01. 모든 ρ 에 동일 seed.
- Synchronous Euler, dt=0.005, steps=30000 → T=150.
- Du=0.5 fixed, Dv = ρ·Du sweep ρ ∈ {1, 2, 4, 6, 8, 10, 15} (7 ratios).
- 수치안정: 2D 확산 CFL `4·max(Dv)·dt = 4·7.5·0.005 = 0.15 < 1` 만족.
- Determinism: ρ=1 을 두 번 적분, var byte-identical 확인.

$0 Mac local CPU · ~수분 wall · `hexa run` · deterministic.

## 5. 사전등록 falsifier

- **F1 SYMMETRIC-STAYS-UNIFORM**: var_u(ρ=1) < 1e-4
- **F2 ASYMMETRIC-BREAKS-SYM**: var_u(ρ=15) > 1e-2
- **F3 THRESHOLD-EXISTS**: ρ_c ∈ (1, 15) 발견됨
- **F4 MONOTONE-IN-RATIO**: var_u(ρ) tol 내 non-decreasing
- **F5 BOUNDED-FINITE**: 모든 var 유한 (NaN 없음)
- **F6 DETERMINISTIC**: ρ=1 재적분 byte-identical
- **EXTRA RHOC-IN-RANGE**: ρ_c ∈ [4, 8] (H_344 1D 측정값과 일치)

≥5/6 PASS + ρ_c ∈ [4,8] → 🟢 SUPPORTED-NUMERICAL (1D↔2D 차원-불변 Turing threshold).
≥5/6 PASS + ρ_c ∉ [4,8] → 🟠 ORANGE (mechanism 작동하나 차원에 따른 ρ_c 차이 있음).
<5/6 PASS → 🔴 다양한 분기 (NO_PATTERN_EVER / NO_THRESHOLD / NON_MONOTONE / NON_DETERMINISTIC).

## 6. 산출물

- `bench/turing_mitosis/bench.hexa` — 시뮬레이션 코드.
- `bench/turing_mitosis/result.json` — 측정 SSOT (ρ-sweep var/mean/peak_lag, ρ_c, verdict).
- `bench/turing_mitosis/run.log` — verbatim stdout (ASCII pattern viz 포함).
- `bench/turing_mitosis/README.md` — 본 문서.

## 7. honest limits

1. **L1 toy GM ≠ anima full morphogenesis** — N=32×32 GM 는 형태형성의 minimal 토이 모델이지 anima substrate 의 정확한 morphogenesis 구현 주장이 아님. 메커니즘 (확산 비대칭 → 자발 대칭깨짐 + threshold) 의 2D 시연.
2. **L2 ρ-grid 거침** — 7-point grid {1,2,4,6,8,10,15} 의 분해능 ±1. ρ_c bisection (e.g. {5, 5.5, 6, 6.5, 7}) 으로 ±0.25 정밀화는 future refinement.
3. **L3 GM-model-specific ρ_c** — ρ_c 값은 이 GM 파라미터(μ_u=μ_v=1)에 한정. 다른 활성자-억제자(Schnakenberg, Gray-Scott) 는 다른 ρ_c.
4. **L4 🟢 not 🔵** — 수치 동역학 측정, closed-form 선형안정성 분산관계 분기 증명 아님. 🔵 path = `λ(q²)` max_q Re λ > 0 의 해석적 ρ_c 도출 (future).
5. **L5 peak_lag 분해능** — N/2=16 까지 정수 lag, sub-cell 정밀도 없음.

## 8. 폐쇄

verbatim stdout + `result.json` 측정값 SSOT. verdict + ρ_c 는 본 README 가 아니라 `run.log` / `result.json` 이 권위.
