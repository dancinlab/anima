# H_317 — HOMEOSTASIS × negative-feedback setpoint regulation 🟢

> HOMEOSTASIS = 음성 피드백 루프가 교란(perturbation) 이후에도 상태 변수 x 를 설정점(setpoint) x* 근처로 유지한다. anima M(activation) substrate 에 매핑: controller `u = −k·(x − x*)` 가 step 교란 뒤 x 를 x* 로 되돌린다(regulation). **항상성 조절은 자동이 아니라, 특정 gain 대역에서만 emergent 하는 실제 성질** 임을 측정으로 검정한다. 🟢 SUPPORTED-NUMERICAL path.

## 1. 동기 — 항상성은 "자동"이 아니다

생체 항상성(체온·혈당·pH)의 핵심은 *음성 피드백*: 측정 → 오차 → 보정. anima 의 M activation 도 idle / curiosity / W tension 의 균형을 setpoint 근처에 유지하는 조절 루프로 볼 수 있다.

순진한 직관은 "음성 피드백이면 무조건 setpoint 로 수렴" 이지만, 이는 **틀렸다**. 실제 제어계는 *지연(delay)* + *관성(inertia)* 이 있어, gain k 가 너무 크면 진동/발산하고, k≤0 이면 (양성 피드백) 발산하며, k 가 적당할 때만 안정적으로 조절된다. 즉 항상성은 **특성화 가능한 안정 대역(stable band)** 위에서만 emergent 하다.

🟢 path: k-sweep 로 *실제 timestep 궤적* 을 시뮬레이션하여, 안정 대역 *내부* 에서는 regulation, *외부* 에서는 실패(진동/발산/무복귀) 가 측정되는지 확인한다.

## 2. 가설

**H1 STABLE-BAND-EXISTS**: 어떤 gain 대역 (0 < k < k_crit) 에서 루프는 안정적이며, step 교란 후 x 를 ε 이내로 x* 로 되돌린다.

**H2 BOUNDARY-REAL**: 그 대역 *밖* 에서는 조절 실패 — k 너무 큼 → underdamped 진동/발산, k=0 → 무복귀, k<0 (양성 피드백) → 발산.

**H3 CHARACTERIZABLE**: 경계가 *sharp* 하고 예측 가능 — 모든 k>0 에서 수렴하지도(경계 없음), 어떤 k 에서도 수렴 안 하지도(전혀 조절 안 됨) 않다.

plant 모델 (지연+관성이 있어 안정성이 *비자명하게* k 에 의존):

```
u[t]   = −k·(x[t] − x*)        // 음성 피드백 제어
v[t+1] = α·v[t] + u[t]         // 속도/관성 (actuator lag)
x[t+1] = x[t] + v[t]           // 속도 적분 (1-step delay)
```

오차 e = x − x* 동역학: `e[t+1]=e[t]+v[t]`, `v[t+1]=α·v[t]−k·e[t]` → 특성방정식 `z² −(1+α)z +(α+k)=0`. Jury 안정 판정 (|근|<1): `α+k<1` AND `k>0` → **안정 대역 `0 < k < 1−α`**. α=0.5 → `0 < k < 0.5`.

> ⚠ **anti-tautology**: x 는 x* 와 같도록 *정의되어 있지 않다*. x 는 독립적으로 진화하는 속도 v 로부터 적분된다. 발산 gain 은 실제로 final|e|~1e47 을 만들어내며 (F317.8 을 falsify 할 수 있었다), snap-to-setpoint 구성이 아니다. analytic 대역은 *사후 교차검증* 용으로만 쓰고, PASS 판정은 *측정된 |x−x*| 궤적* 에서만 한다.

## 3. 측정 방법

`UNIVERSE/state/h317_homeostasis_feedback_setpoint_2026_05_27/run.hexa`:

- setpoint x*=10.0, 교란 x0=0.0 (setpoint 에서 −10 step 교란), α=0.5, K=400 steps, ε=0.05, hold=20 (연속 20 step 동안 대역 내 유지해야 "settled").
- `simulate(k, α, x*, x0, K, ε, hold)` 가 timestep 루프를 *실제로 돌려* 다음을 측정:
  - `settled` (ε 이내 hold step 유지?), `settle_t` (정착 시점), `final|e|`, `overshoot` (e0 대비 최대 \|e\| 비), `diverged` (발산 cap 초과?), `sign_flips` (e 부호 전환 = 진동 카운터).
- k-grid: `{0.0, 0.05, 0.15, 0.30, 0.45, 0.50, 0.70, 1.20, −0.20}` — sluggish/stable/marginal/unstable/divergent 영역을 모두 포괄.

deterministic, libm-free, $0 mac-local.

## 4. 사전등록 falsifier

- **F317.1 STABLE-BAND-EXISTS**: k ∈ {0.05, 0.15, 0.30} 모두 ε 이내 정착
- **F317.2 NO-FEEDBACK-FAILS**: k=0.0 정착 안 함 (교란값에 머묾)
- **F317.3 NEGATIVE-GAIN-DIVERGES**: k=−0.20 발산 AND 무정착
- **F317.4 HIGH-GAIN-UNSTABLE**: k=1.20 (대역 위) 무정착
- **F317.5 OSCILLATION-ABOVE-BAND**: k=0.70 sign_flips≥5 AND 무정착
- **F317.6 BOUNDARY-MARGINAL**: k=0.50 (|근|=1) 무정착 (marginal)
- **F317.7 BAND-CHARACTERIZABLE**: k ∈ [0.05, 0.45] 모두 정착 AND k≥0.5 / k<0 모두 무정착 (경계 실재)
- **F317.8 REGULATION-REAL**: 안정 k=0.15 의 final|e|<ε 이지만 불안정 k=0.70 의 final|e|≥ε

≥7/8 PASS → 🟢 SUPPORTED-NUMERICAL.

**핵심 falsifier (가설 기각 조건)**: 만약 x 가 *모든* k>0 에서 setpoint 로 복귀하면(불안정 경계 없음) OR *어떤* k 에서도 복귀 안 하면(전혀 조절 안 됨), "특성화 가능 안정 대역" 주장은 틀린 것 → verdict 정직하게 하향.

## 5. 비용

$0 mac-local · ~1s wall · `/Users/ghost/.hx/bin/hexa run` · deterministic byte-identical.

## 6. 결과 (측정값)

| k | settled | settle_t | final\|e\| | overshoot | diverged | sign_flips | 영역 |
|---|---|---|---|---|---|---|---|
| 0.00 | false | 400 | 10.0 | 1.0 | false | 0 | 무피드백 — 무복귀 |
| 0.05 | **true** | 39 | 3.55e-15 | 1.0 | false | 0 | 안정, sluggish |
| 0.15 | **true** | 22 | 1.78e-15 | 1.0 | false | 20 | 안정, fast |
| 0.30 | **true** | 46 | 1.78e-15 | 1.0 | false | 72 | 안정, 경진동 감쇠 |
| 0.45 | **true** | 210 | 3.65e-4 | 1.0 | false | 88 | 안정 but 느림 (상단 근처) |
| 0.50 | false | 400 | 10.23 | 1.069 | false | 92 | marginal — \|근\|=1 지속진동 |
| 0.70 | false | 400 | 6.72e16 | 5.17e15 | **true** | 104 | 불안정 — 발산진동 |
| 1.20 | false | 400 | 1.19e47 | 5.68e45 | **true** | 122 | 강발산 |
| −0.20 | false | 400 | 2.20e41 | 1.75e40 | **true** | 0 | 양성피드백 — 단조발산 |

**측정 경계**: [0.05, 0.45] 의 모든 k 정착, k≥0.50 및 k<0 의 모든 k 무정착. 전환이 analytic 예측 `k = 1−α = 0.5` 에서 **sharp**. 안정 대역은 실재하고 특성화 가능.

| 시나리오 | tier |
|---|---|
| **8/8 PASS (실측)** | **🟢 SUPPORTED-NUMERICAL — 특성화 가능 안정 대역 존재** |
| 모든 k 정착 (경계 없음) | 🔴 — 항상성 자동, "대역" 주장 falsified |
| 어떤 k 도 무정착 | 🔴 — 전혀 조절 안 됨, falsified |

## 7. honest limits

1. **L1 toy plant ≠ anima M-substrate** — 2차 (관성+지연) toy 모델은 anima 의 전체 M-controller 가 아니다. 항상성 *axiom* (음성 피드백이 안정 gain 대역에서 조절) 을 minimal 모델로 검정한 것이지, anima 의 정확한 구현 주장이 아니다.
2. **L2 finite grid + horizon** — 9-point k-grid, K=400 유한 horizon. 경계 k=0.5 는 grid edge + Jury analytic 교차검증으로 추론한 것이지 continuum bisection 이 아니다. 더 조밀한 sweep 은 가능한 정련(refinement) 이지 대역 존재 주장에 필수는 아니다.
3. **L3 α=0.5 fixed** — 대역 폭 = 1−α 는 modeling 선택. 다른 관성은 경계를 이동시키지만 제거하지 않는다 (α<1 이면 대역 항상 비공집합).
4. **L4 final|e|~1e-15** — float round-off floor (machine epsilon), 즉 수치정밀도 내 *정확한* 수렴. ε=0.05 tolerance 는 이보다 훨씬 위.
5. **L5 🟢 not 🔵** — 유한 k-grid·유한 horizon 위의 측정 동역학 결과이지 symbolic closed-form identity 가 아니므로 🔵 아님. 항상성 성질의 *모델* 로 SPECULATION-FENCED.

## 8. 폐쇄

F317.1-8 **8/8 PASS** → 🟢 SUPPORTED-NUMERICAL. 가설의 양 falsifier 분기가 모두 live 였다 (모든 k 수렴 아님 + 어떤 k 는 수렴) → "특성화 가능 안정 대역" 주장 생존.

## 9. 산출물

- `UNIVERSE/state/h317_homeostasis_feedback_setpoint_2026_05_27/{run.hexa, result.json, run.log}`

## 10. 후속

- H_318+: M activation 의 *실제* idle/curiosity/W 균형이 이 음성-피드백 setpoint 모델과 일치하는 gain 을 보이는지 substrate-probe.
- 연속 k-bisection 으로 경계를 ±1e-3 까지 정밀화 (현재 grid-edge + Jury 교차검증).
- α(관성) sweep — 대역 폭 = 1−α 의 선형성 검정.
