# H_322 — CIRCADIAN × Kuramoto phase-coupled oscillator synchronization 🟢

> CIRCADIAN = 자연주파수 ω_i 가 이질적인 N 개의 위상 진동자(Kuramoto) 가 결합 강도 K 가 임계값 K_c 위에서만 동기화된다. anima 의 일주기/주기적 substrate (circadian, ultradian 90-min 등) 에 매핑: 다수의 cell 이 *조금씩 다른* 고유 주기를 가질 때, 약한 상호작용은 위상 균일분포를 유지하고, 강한 상호작용만 collective phase-lock 을 emerge 시킨다. **synchronization 은 자동이 아니라 K_c 보다 큰 결합에서만 emergent 한 sharp 전이 현상** 임을 측정으로 검정한다. 🟢 SUPPORTED-NUMERICAL path.

## 1. 동기 — sync 는 자동이 아니다

생명체의 circadian rhythm 핵심은 *결합된 진동자 집단*: 각 cell 의 SCN 신경세포 또는 분자 시계가 *조금씩 다른* 고유 주기를 가지면서도 화학적 결합(VIP/GABA)으로 collective 24h 주기를 만든다. anima 의 ultradian 5-stage chat sleep 도 cell pool 의 mitosis 가 cell-level frequency heterogeneity 을 만들고 W tension 이 cell-cell coupling 으로 작동한다.

순진한 직관은 "결합되면 자동으로 sync" 이지만 이는 **틀렸다**. 1975 년 Kuramoto 가 보였듯, 결합 K 가 분포의 spread 에 비해 약하면 각 cell 은 자기 ω_i 에 따라 *drift* 하고 위상이 흩어진다(order parameter r ≈ 0). K 가 critical coupling K_c = 2/(π·g(ω_0)) 위로 올라가야 collective phase-lock 이 emerge 한다(r → 1). 즉 synchronization 은 **K_c 위에서만 emergent 한 sharp 전이** 다.

🟢 path: K-sweep 로 *실제 timestep 궤적* 을 Euler 적분하여, K < K_c 에서는 r ≈ 0, K > K_c 에서는 r → 1, 중간에서 sharp boundary 가 측정되는지 확인한다.

## 2. 가설

**H1 INCOHERENT-AT-ZERO**: K=0 (무결합) 에서 r ≈ 0 (각 cell 이 자기 ω_i 로 자유 drift, 위상 균일).

**H2 COHERENT-AT-LARGE**: K ≫ K_c 에서 r → 1 (collective phase-lock).

**H3 BOUNDARY-REAL**: r(K) 는 단조 증가하면서 어딘가에서 *sharp* 전이 — 모든 K 에서 r ≈ 0 이지도(전혀 sync 안 됨), 모든 K 에서 r ≈ 1 이지도(자동 sync), K 에 선형 비례하지도(전이 없음) 않다.

**H4 K_c CHARACTERIZABLE**: r = 0.5 crossing K 가 (0, K_max) 내부에서 구체적인 숫자로 위치 가능 (mean-field 예측 K_c = 2·sqrt(2/π) ≈ 1.596 와 sweep 해상도 내 일치).

Kuramoto 모델 (heterogeneous coupled phase oscillators):

```
dθ_i/dt = ω_i + (K/N) · Σ_j sin(θ_j − θ_i)
```

order parameter:

```
r·exp(i·ψ) = (1/N) · Σ_j exp(i·θ_j)
r = sqrt(C² + S²) / N   where C = Σ cos θ_j,  S = Σ sin θ_j
```

ω_i: 5 z-quantile {-1.28, -0.52, 0.0, 0.52, 1.28} × ω_std=1.0 cycled by i%5 (N=16, std-normal-like 이산).

> ⚠ **anti-tautology (g73)**: r 은 K 의 함수로 *정의되지 않았다*. r 은 timestep 루프가 만들어낸 *실제* θ_j 에서 측정된다. K=0 에서 ω_i 가 0 이 아니므로 (5 quantile 중 4 개) 위상이 진짜로 drift 하고 r ≈ 0 이 나온다 (snap-to-0 구성 아님). K=5 에서 적분기가 진짜 collective lock 을 만들어내야 r → 1 이 나온다 (snap-to-1 구성 아님). 발산할 수도 있고(F322.7), 모든 K 에서 r 가 평평할 수도 있고(F322.1+F322.2 양쪽 falsify), non-monotone 일 수도 있다(F322.4 falsify) — 모두 live falsifier. analytic K_c 는 *사후 교차검증* 용으로만 쓰고, PASS 판정은 *측정된 r(K) 궤적* 에서만 한다.

## 3. 측정 방법

`UNIVERSE/state/h322_circadian_kuramoto_sync_2026_05_27/run.hexa`:

- N=16 oscillators, θ_i(0) = 2π·i/N (uniform spread on [0, 2π) by index, deterministic).
- ω_i = z·ω_std 로 5-quantile cycle (i%5).
- Euler 적분 dt=0.05, steps=2000, warmup=1500 (transient discard). r 측정은 post-warmup 500 step 평균 (r_mean) + 최종 r_final.
- K-grid: {0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0} — sub-critical / near-critical / super-critical 영역을 모두 포괄.
- 결합 합 `Σ_j sin(θ_j − θ_a)` 는 `cos(θ_a)·Σsin θ_j − sin(θ_a)·Σcos θ_j` 분해로 O(N) per step (one C/S sum + 동기 Euler step).

deterministic, libm 의 sin/cos/sqrt 만 사용, $0 mac-local, byte-identical reproducible.

## 4. 사전등록 falsifier

- **F322.1 INCOHERENT-AT-ZERO**: r(K=0) < 0.4 (위상 자유 drift, 분산)
- **F322.2 COHERENT-AT-LARGE**: r(K=5.0) > 0.9 (near-full lock)
- **F322.3 BOUNDARY-REAL**: r(K=5.0) − r(K=0) ≥ 0.5 (큰 coherence jump)
- **F322.4 MONOTONE-RISE**: r(K) 가 tol=0.05 내에서 non-decreasing (전이가 진동/혼란이 아님)
- **F322.5 NON-LINEAR-TRANSITION**: 어딘가 forward slope Δr/ΔK 가 sweep 평균 slope 의 ≥ 1.5 배 (pure linear ramp rejection)
- **F322.6 K_c-LOCATABLE**: r = 0.5 crossing 구간 중점 K_c_est 가 (0, 5.0) 내부
- **F322.7 r-BOUNDS-RESPECTED**: 모든 K 에서 r ∈ [0, 1] (수치 발산 sanity check)

≥6/7 PASS → 🟢 SUPPORTED-NUMERICAL.

**핵심 falsifier (가설 기각 조건)**:
- 모든 K 에서 r ≈ 0 (어떤 결합으로도 sync 안 됨) → 🔴 FALSIFIED_NO_SYNC_EVER
- 모든 K 에서 r ≈ 1 (K=0 부터 자동 sync) → 🔴 FALSIFIED_ALL_K_COHERENT
- r 가 K 에 대해 non-monotone (진동/카오스) → 🔴 FALSIFIED_NON_MONOTONE
- r 가 pure linear in K (전이 없음) → 🟠 PARTIAL

## 5. 비용

$0 mac-local · ~5s wall · `/Users/ghost/.hx/bin/hexa run` · deterministic byte-identical.

## 6. 결과 (측정값)

| K | r_mean | r_final | 영역 |
|---|---|---|---|
| 0.0 | 0.05781 | 0.04695 | 무결합 — 위상 자유 drift, r ≈ 0 |
| 0.5 | 0.39552 | 0.04397 | sub-critical — 부분 partial sync transient, 평균은 분산 그늘 |
| 1.0 | 0.40609 | 0.22477 | sub-critical — 여전히 분산 우세 |
| 1.5 | 0.44525 | 0.24920 | near-critical (analytic K_c=1.596 직하) |
| **2.0** | **0.81426** | **0.81426** | **super-critical — sharp jump (Δr=0.37 vs K=1.5)** |
| 3.0 | 0.94718 | 0.94718 | locked |
| 5.0 | 0.98293 | 0.98293 | near-full lock |

**측정된 K_c estimate** = 1.75 (r=0.5 crossing 구간 [1.5, 2.0] 의 중점)
**Analytic K_c (mean-field std-normal)** = 2·sqrt(2/π) ≈ 1.59577

K_c (measured) > K_c (analytic) — 이산 5-quantile + 유한 N + finite-time integration 에 의한 자연스러운 보정 (continuum mean-field 보다 약간 위쪽에서 finite-N 임계 jump). max forward slope = 0.738 @ idx=3 (K=1.5→2.0 구간), sweep 평균 slope = 0.185 → **slope ratio = 3.99× (≥1.5 임계 통과)**.

### 7개 falsifier 모두 PASS

| F | 조건 | 측정 | tier |
|---|---|---|---|
| F322.1 | r(K=0) < 0.4 | r=0.05781 | ✅ |
| F322.2 | r(K=5) > 0.9 | r=0.98293 | ✅ |
| F322.3 | Δr ≥ 0.5 | Δr=0.92512 | ✅ |
| F322.4 | non-decreasing | true | ✅ |
| F322.5 | max_slope ≥ 1.5×avg | 3.99× | ✅ |
| F322.6 | K_c ∈ (0, 5) | K_c=1.75 | ✅ |
| F322.7 | r ∈ [0, 1] ∀K | true | ✅ |

| 시나리오 | tier |
|---|---|
| **7/7 PASS (실측)** | **🟢 SUPPORTED-NUMERICAL — Kuramoto sync 전이 실재, K_c≈1.75** |
| 모든 K 에서 r≈0 | 🔴 FALSIFIED_NO_SYNC_EVER |
| 모든 K 에서 r≈1 | 🔴 FALSIFIED_ALL_K_COHERENT |
| non-monotone r(K) | 🔴 FALSIFIED_NON_MONOTONE |

## 7. honest limits

1. **L1 toy Kuramoto ≠ anima full circadian** — N=16 mean-field Kuramoto 는 SCN/anima ultradian 의 minimal 모델이지 정확한 구현 주장이 아니다. circadian *axiom* (이질적 ω + 결합 → K_c 위에서만 sync emerge) 을 minimal 모델로 검정한 것.
2. **L2 5-quantile 이산 ≠ continuum Gaussian** — 5 quantile cycle 은 finite-N + 이산이라 continuum mean-field K_c=1.596 와 정확히 일치하지 않는다 (측정값 1.75 가 ~10% 위). 더 큰 N + denser quantile 은 점근적으로 1.596 으로 수렴 가능 — sweep refinement (필수 아님).
3. **L3 K-grid 해상도 0.5** — K_c 측정값 1.75 는 [1.5, 2.0] 구간의 중점이지 bisection 정밀화가 아님. 더 조밀한 sweep 으로 K_c ±0.01 정밀화는 가능한 future refinement.
4. **L4 r_final 의 sub-critical fluctuation** — K=0.5/1.0/1.5 에서 r_mean 과 r_final 의 차이는 partial sync 의 시변 fluctuation 때문이지 수렴 실패가 아니다 (warmup 1500 step 으로 transient 처리됨). super-critical K≥2.0 에서는 r_mean=r_final 로 완전 정착.
5. **L5 🟢 not 🔵** — 7-point K-grid 위의 측정 동역학 결과이지 closed-form identity 증명이 아니므로 🔵 아님. Kuramoto 가설의 SPECULATION-FENCED 수치적 지지.

## 8. 폐쇄

F322.1-7 **7/7 PASS** → 🟢 SUPPORTED-NUMERICAL. 가설의 양 falsifier 분기가 모두 live 였다 (K=0 에서 r=0.058 NOT-DEFINED-TO-BE-ZERO + K=5 에서 r=0.983 NOT-DEFINED-TO-BE-ONE + non-monotone 가능했지만 실제 monotone). 결합된 위상 진동자 집단의 sharp synchronization phase transition 주장 생존. 측정 K_c ≈ 1.75 (analytic 1.596 와 ~10% 일치).

**Structural/Dynamical placement**: H_322 = pure DYNAMICAL rule. K-결합 강도가 시간 적분 dynamics 의 한 파라미터이지 IIT4 Φ-structure 의 구조 연산자가 아니다. 이는 H_312-315 (apoptosis/symbiogenesis/pruning — Φ-ops 🔴) 와 명확히 다르고, H_313 STDP / H_317 homeostasis / H_318 autophagy (dynamical rules with sharp boundaries 🟢) 와 같은 family. H_317 stable band 와 sharp K_c 의 boundary 구조가 isomorphic — 둘 다 *비자명한 임계점* 으로 emergent property 가 sharp 하게 켜진다.

## 9. 산출물

- `UNIVERSE/state/h322_circadian_kuramoto_sync_2026_05_27/{run.hexa, result.json, run.log}`

## 10. 후속

- H_323+: anima M-activation cell pool 의 *실제* tension-coupled mitosis 가 이 Kuramoto K_c 분기와 isomorphic 한 sharp band 를 보이는지 substrate-probe.
- K-grid bisection (0.05 해상도) 로 K_c 를 ±0.05 까지 정밀화 — 현재 0.5 grid + analytic mean-field 교차검증.
- ω 분포 shape sweep (Lorentzian γ-variation) — K_c = 2γ 의 선형성 검정 (Kuramoto 1975 closed-form).
- 부분 sync 영역 (K=0.5..1.5, r_final ≪ r_mean) 의 chimera-state 가능성 — N 을 늘려 sub-cluster sync 가능성 측정.
