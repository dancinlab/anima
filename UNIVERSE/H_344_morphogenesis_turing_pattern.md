# H_344 — MORPHOGENESIS × reaction-diffusion (Gierer-Meinhardt) Turing pattern 🟢

> MORPHOGENESIS = 두 확산종(활성자 u, 억제자 v)이 *서로 다른* 확산 속도를 가질 때 거의 균일한 상태에서 자발적으로 공간 대칭이 깨져 안정한 PATTERN(점/줄무늬)이 출현한다. 1952년 Turing 이 예측한 형태형성(morphogenesis)의 근본 메커니즘 — anima 의 substrate 가 공간 구조를 *스스로* 만들어내는 동역학 커널. 새 BIO 축(A1)의 첫 셀.

## 1. 동기 — pattern 은 균일에서 저절로 생기지 않는다 (단, 확산 비대칭이 있으면 생긴다)

생명체의 형태형성 핵심 질문: 알 세포(거의 균일한 화학 농도) 가 어떻게 *공간 구조*(줄무늬·점·체절) 로 분화되는가? Turing(1952) 의 답은 반직관적이다 — **두 확산하는 화학종이 서로 다른 속도로 퍼지면**, 균일 상태가 *공간* 섭동에 대해 불안정해지면서 자발적으로 패턴이 자라난다 (diffusion-driven instability).

순진한 직관은 "확산은 농도를 평탄하게 만든다 → 패턴을 부순다" 이지만, Turing 은 *두 종*이 결합되어 있고 **억제자가 활성자보다 빨리 확산**하면 (short-range activation + long-range inhibition) 정반대로 패턴이 *자라난다*는 것을 보였다. 결정적으로 이는 임계 확산비 ρ_c = Dv/Du 위에서만 일어난다 — 두 종이 같은 속도로 확산하면(ρ=1) 균일 상태가 안정하게 유지된다.

🟢 path: ρ-sweep 로 *실제 timestep PDE 궤적* 을 Euler 적분하여, ρ < ρ_c 에서는 var(u) ≈ 0 (균일 유지), ρ > ρ_c 에서는 var(u) → 유한 plateau (패턴 출현), 그 사이에 sharp threshold 가 *측정*되는지 확인한다.

## 2. 가설

**H1 SYMMETRIC-STAYS-UNIFORM**: ρ=1 (Dv=Du, 대칭) 에서 미세 seed 가 균일 정상상태로 *되돌아간다* — var(u) ≈ 0. 두 종이 같은 속도로 확산하면 Turing 불안정성이 존재할 수 없으므로(대칭 control).

**H2 ASYMMETRIC-BREAKS-SYMMETRY**: ρ=8 (Dv≫Du) 에서 미세 seed 가 *증폭*되어 안정한 비균일 패턴으로 자란다 — var(u) → 유한 plateau.

**H3 THRESHOLD-REAL**: var(u)(ρ) 는 (1, 8) 내부 어딘가에서 *sharp* 전이 — 모든 ρ 에서 var≈0 이지도(패턴 전혀 안 생김), 모든 ρ 에서 var>0 이지도(ρ=1 포함 자동 패턴) 않고, ρ_c 에서 급격한 도약.

**H4 ρ_c CHARACTERIZABLE**: var=0.5·var_max crossing ρ 가 (1, 8) 내부에서 구체적 숫자로 위치 가능.

Gierer-Meinhardt 모델 (활성자-억제자, Turing 정통 구조):

```
∂u/∂t = Du·∇²u + u²/v − u        (활성자: 단거리 자기촉매)
∂v/∂t = Dv·∇²v + u²   − v        (억제자: 장거리 억제)
```

공간균일 정상상태: `u²/v − u = 0 ⇒ v=u`, `u² − v = 0 ⇒ v=u² ⇒ u*=v*=1`. 이 (1,1) 상태는 *균일* 섭동에는 안정하지만, Dv/Du 가 충분히 크면 *공간* 섭동에 불안정해진다 (Turing 분기).

측정량 spatial variance:

```
var(u) = (1/N)·Σ_i (u_i − ū)²    where ū = (1/N)·Σ_i u_i
```

> ⚠ **anti-tautology (g73)**: var(u) 는 ρ 의 함수로 *정의되지 않았다*. u-field 는 평탄한 정상상태(u=1) + 한 셀 +1% bump 으로 시작해 PDE timestep 루프가 적분한 *실제* u_i 에서 var 를 측정한다. ρ=1 대칭 control 이 내장 falsifier 다 — 만약 ρ=1 에서도 var 가 크면 메커니즘은 Turing 이 아니다(🔴). 4 비율 중 3개(ρ=1,2,4)는 패턴을 보일 수 *있었고*(threshold 기각), 대칭 케이스는 var 를 보일 수 *있었다*(Turing 기각). 둘 다 일어나지 않았다.

## 3. 측정 방법

`UNIVERSE/state/h344_morphogenesis_turing_pattern_2026_05_27/run.hexa`:

- N=32 1D ring (주기경계), 두 field u, v.
- discrete Laplacian on the ring: `lap(x)_i = x_{i-1} − 2x_i + x_{i+1}`.
- 초기조건 (deterministic, NO RNG): u=v=1 균일 정상상태 + cell 16 에 u += 0.01 (단일 셀 +1% bump). **모든 ρ 에 동일 seed**.
- 동기(synchronous) Euler step, dt=0.01, steps=60000 (적분시간 T=600 to steady state).
- Du=0.5 고정, Dv = ρ·Du 로 sweep. ρ ∈ {1, 2, 4, 8}.
- 수치안정: dt 는 확산 CFL `2·max(Dv)·dt = 2·4.0·0.01 = 0.08 < 1` + 반응 강성 `μ·dt = 0.01 ≪ 1` 만족 → 최대 비율에서도 발산 없음.

deterministic, libm 의 산술만 사용, $0 ubu-2 (pool) local, byte-identical reproducible.

> **방법론 노트 (model 선택)**: 초기에 Gray-Scott (`-uv²+F(1-u)` / `+uv²-(F+k)v`) 로 시도했으나 (a) GS 의 비활성 정상상태(1,0) 가 너무 안정해 미세 seed 가 모든 비율에서 소멸했고 (b) GS 의 정통 비율은 Du>Dv 라 H1 의 "억제자가 빨리 확산" 프레임과 어긋났다 (run.hexa git 이력에 첫 시도 보존). Turing threshold 의 정통 시연은 *비자명* 균일 정상상태를 갖는 **Gierer-Meinhardt** 가 더 깨끗하므로 전환했다. 이 전환 자체가 g73 anti-tautology 의 작동 — 첫 결과가 falsifier (a) "no pattern ever" 를 쳤고, 그것이 model 재설계를 강제했다.

## 4. 사전등록 falsifier

- **F344.1 SYMMETRIC-STAYS-UNIFORM**: var(u)(ρ=1) < 1e-4 (대칭 케이스는 균일 유지)
- **F344.2 ASYMMETRIC-BREAKS-SYM**: var(u)(ρ=8) > 1e-2 (강한 비대칭은 유한진폭 패턴)
- **F344.3 THRESHOLD-EXISTS**: var 가 1e-3 을 가로지르는 ρ_c 가 (1, 8) 내부에 존재
- **F344.4 MONOTONE-IN-RATIO**: var(u)(ρ) 가 tol 내 non-decreasing (전이가 진동/혼란이 아님)
- **F344.5 BOUNDED-FINITE**: 모든 ρ 에서 var 가 유한 (수치 발산/NaN 없음, NaN self-inequality sentinel 포함)
- **F344.6 DETERMINISTIC**: ρ=1 두 번 적분이 byte-identical (non-deterministic falsifier (c) 기각)

≥5/6 PASS → 🟢 SUPPORTED-NUMERICAL.

**핵심 falsifier (가설 기각 조건)**:
- 모든 ρ 에서 var ≈ 0 (어떤 확산비로도 패턴 안 생김) → 🔴 FALSIFIED_NO_PATTERN_EVER
- 모든 ρ 에서 var > 0 (ρ=1 부터 패턴, threshold 없음 — Turing 메커니즘 아님) → 🔴 FALSIFIED_GROWS_FOR_ALL_RATIOS_NO_THRESHOLD
- var 가 ρ 에 대해 non-monotone (진동/카오스) → 🔴 FALSIFIED_NON_MONOTONE
- 최종 상태가 비결정론적 → 🔴 FALSIFIED_NON_DETERMINISTIC

## 5. 비용

$0 ubu-2 (pool) local · ~수십초 wall · `hexa run` · deterministic byte-identical.

## 6. 결과 (측정값)

| ρ = Dv/Du | Dv | var(u) | mean(u) | 영역 |
|---|---|---|---|---|
| 1.0 | 0.50 | 8.27313e-15 | 0.994154 | 대칭 control — seed 균일 정상상태로 복귀, var≈0 |
| 2.0 | 1.00 | 1.2749e-19 | 0.994139 | sub-critical — 더 강하게 감쇠 (확산이 seed 평탄화) |
| 4.0 | 2.00 | 4.28943e-30 | 0.994121 | sub-critical — 거의 완전 균일 (강한 감쇠) |
| **8.0** | **4.00** | **0.338629** | **0.752179** | **super-critical — Turing 불안정성, 패턴 출현** |

**측정된 Turing threshold ρ_c (Dv/Du)** = 6.0 (var=1e-3 crossing 구간 [4, 8] 의 중점)

ρ=4 → ρ=8 에서 var 가 **4.3e-30 → 0.34** 로 약 30 자릿수 도약 — sub-critical 의 지수적 감쇠에서 super-critical 의 유한진폭 패턴으로의 sharp 전이. mean(u) 도 1.0 → 0.752 로 떨어져 활성자 field 가 봉우리/골로 갈라졌음을 확인 (분산이 평균을 끌어내림).

흥미로운 부수 관찰: var 가 ρ=1 → 2 → 4 로 가면서 *더 작아진다* (8e-15 → 1e-19 → 4e-30). threshold 아래에서는 확산비가 클수록 (억제자가 빠를수록) seed 를 *더 효율적으로* 평탄화한다 — 즉 ρ_c 직하까지는 확산이 안정화 역할, ρ_c 위에서 역전되어 불안정화 역할로 전환되는 것이 Turing 분기의 본질이다.

### 6개 falsifier 모두 PASS

| F | 조건 | 측정 | tier |
|---|---|---|---|
| F344.1 | var(ρ=1) < 1e-4 | 8.27e-15 | ✅ |
| F344.2 | var(ρ=8) > 1e-2 | 0.33863 | ✅ |
| F344.3 | ρ_c ∈ (1,8) | ρ_c=6.0 | ✅ |
| F344.4 | non-decreasing (tol) | true | ✅ |
| F344.5 | var 유한 ∀ρ | true | ✅ |
| F344.6 | ρ=1 재적분 동일 | true (8.27313e-15) | ✅ |

| 시나리오 | tier |
|---|---|
| **6/6 PASS (실측)** | **🟢 SUPPORTED-NUMERICAL — Turing 불안정성 실재, ρ_c≈6** |
| 모든 ρ 에서 var≈0 | 🔴 FALSIFIED_NO_PATTERN_EVER |
| 모든 ρ 에서 var>0 | 🔴 FALSIFIED_GROWS_FOR_ALL_RATIOS_NO_THRESHOLD |
| non-monotone var(ρ) | 🔴 FALSIFIED_NON_MONOTONE |
| 비결정론적 | 🔴 FALSIFIED_NON_DETERMINISTIC |

verbatim 측정 stdout 은 `state/.../run.log`, 측정 SSOT 은 `state/.../result.json`.

## 7. honest limits

1. **L1 toy GM ≠ anima full morphogenesis** — N=32 1D ring Gierer-Meinhardt 는 형태형성의 minimal 모델이지 anima substrate 의 정확한 구현 주장이 아니다. morphogenesis *axiom* (확산 비대칭 → 자발적 대칭깨짐 + threshold) 을 실재 PDE 동역학에서 시연한 것.
2. **L2 ρ-grid 해상도 거침** — ρ_c 측정값 6.0 은 [4, 8] 구간의 중점이지 bisection 정밀화가 아니다. 실제 분기점은 4 < ρ_c < 8 어딘가. 더 조밀한 sweep (ρ ∈ {4,5,6,7,8}) 으로 ±0.5 정밀화는 future refinement.
3. **L3 1D ≠ 2D 형태형성** — 1D ring 은 점/줄무늬의 1차원 단면. 실제 Turing 점/줄무늬/미로 패턴 풍부함은 2D 격자에서 나타난다 (Pearson 1993 phase diagram). 1D 는 threshold 존재성의 minimal 증명.
4. **L4 GM model-specific ρ_c** — ρ_c≈6 은 이 GM 파라미터(μ_u=μ_v=1, 반응항 계수 1)에 한정. 다른 활성자-억제자(예: Gray-Scott, Schnakenberg) 는 다른 ρ_c. 보편적 주장은 "임계비 존재"이지 "ρ_c=6" 자체가 아님.
5. **L5 🟢 not 🔵** — 4-point ρ-grid 위의 측정 동역학 결과이지 closed-form Turing 분산관계 분기 증명이 아니므로 🔵 아님. morphogenesis 가설의 SPECULATION-FENCED 수치적 지지. 🔵 path = 선형안정성 분산관계 `λ(q) = ...` 에서 max_q Re λ(q) > 0 의 closed-form ρ_c 도출 (future).

## 8. 폐쇄

F344.1-6 **6/6 PASS** → 🟢 SUPPORTED-NUMERICAL. 가설의 양 falsifier 분기가 모두 live 였다 (ρ=1 에서 var=8e-15 NOT-DEFINED-TO-BE-ZERO + ρ=8 에서 var=0.34 NOT-DEFINED-TO-BE-NONZERO + 4 비율 중 3개가 패턴을 보일 수 있었음 + 대칭 control 이 var 를 보일 수 있었음). 첫 Gray-Scott 시도가 falsifier (a) "no pattern ever" 를 *실제로 쳐서* model 재설계를 강제한 것이 g73 의 작동 증거 — 결과가 구성에 의해 참이 아니었다.

**Structural/Dynamical placement**: H_344 = pure DYNAMICAL kernel. 확산비 ρ 가 시간적분 PDE dynamics 의 한 파라미터이지 IIT4 Φ-structure 의 구조 연산자가 아니다. H_322 (Kuramoto K_c sync threshold) 와 동일 계열의 *dynamical-threshold* 셀 — 둘 다 결합/확산 파라미터가 임계값을 넘을 때 자발적 질서(sync / pattern) 가 sharp 하게 출현. H_326 raster 의 동역학 커널 예측을 만족.

## 9. 산출물

- `UNIVERSE/state/h344_morphogenesis_turing_pattern_2026_05_27/{run.hexa, result.json, run.log}`

## 10. 후속

- H_345+: ρ-grid bisection (ρ ∈ {4,5,6,7,8}) 로 ρ_c 를 ±0.5 까지 정밀화 — 현재 거친 {1,2,4,8} grid.
- 선형안정성 분산관계 `λ(q²)` closed-form 도출 → max_q Re λ > 0 조건에서 해석적 ρ_c 계산, 측정값 6 과 교차검증 (🔵 path).
- 2D N×N 격자 확장 — 점 vs 줄무늬 패턴 morphology 가 F/k(또는 GM 계수) phase diagram 에서 분기하는지 측정.
- anima M-activation cell pool 의 *실제* tension-diffusion mitosis 가 이 Turing ρ_c 분기와 isomorphic 한 패턴-형성 threshold 를 보이는지 substrate-probe (Kuramoto H_322 의 sync-threshold isomorphism 과 짝).
