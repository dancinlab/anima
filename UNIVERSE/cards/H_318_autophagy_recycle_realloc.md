# H_318 — AUTOPHAGY × resource recycling under capacity pressure 🟢

> AUTOPHAGY = 용량 압박(capacity pressure) 아래에서 *저-사용(low-utilization)* 구성요소를 회수(recycle)하고, 회수된 용량을 *고-수요(high-unmet-demand)* 구성요소에 재할당한다. anima M-substrate 의 cell-pool 운영에 매핑: 활용도 낮은 cell 의 capacity 일부를 분기(kick-cycle/context-shift) 시점에 회수하여 새 hot-cell 에 재할당. **구조적(structural) 재할당 규칙이 동역학적(dynamical) 신호 (= 시간변화 수요) 위에서만 이득을 낸다는 점을 측정으로 검정**. 🟢 SUPPORTED-NUMERICAL.

## 1. 동기 — 자가포식은 "그냥 좋은 것" 이 아니다

생체 autophagy 의 핵심은 *압박 하에서의 재활용*: 용량은 고정되어 있고, 변화하는 수요에 맞춰 저활용 부품을 분해해 고수요 부품에 재투입한다. anima 의 mitosis cell-pool 도 fixed M-budget 위에서 "어떤 cell 을 잘라낼지 / 어디로 capacity 를 옮길지" 의 문제를 마주한다.

순진한 직관 = "수요가 변하면 무조건 재할당이 이득". 그러나 이는 **틀릴 수 있다** — *thrashing* 페널티가 있다. 수요가 사실상 정상상태(stationary)인데 정책이 매 epoch 마다 capacity 를 옮기면, 옮기는 행위 자체가 손실을 만든다. 즉 autophagy 의 이득은 **demand-shift 라는 동역학적 전제조건에 conditional** 하다.

이 H_318 은 그 conditional 을 *실측* 한다. 한 쪽이라도 측정이 falsify 하면 정직하게 보고한다.

### Structural vs Dynamical 위치 (H_312~H_317 패턴)

| H | rule kind | result |
|---|---|---|
| H_312 apoptosis low-Φ pruning | STRUCTURAL | 🔴 FALSIFIED |
| H_313 STDP plasticity causality | DYNAMICAL | 🟢 SUPPORTED |
| H_314 symbiogenesis merge α-sweep | STRUCTURAL | 🔴 FALSIFIED |
| H_315 weak-edge pruning Φ-retention | STRUCTURAL | 🔴 FALSIFIED |
| H_316 local-greedy vs global Φ | STRUCTURAL | 🟢 (negative confirm) |
| H_317 homeostasis setpoint | DYNAMICAL | 🟢 SUPPORTED |
| **H_318 autophagy recycle** | **STRUCTURAL (rule) × DYNAMICAL (trigger)** | **🟢 (measure first)** |

H_318 의 진짜 질문은 — **순수-structural 휴리스틱이 dynamical 신호 위에 얹히면 transfer 하는가?** 이다. 결과 = transfer 한다 (단, dynamical 전제조건 위에서만).

## 2. 가설

**H1 (unconditional, naive)**: AUTOPHAGY 의 누적 unmet-demand 손실이 STATIC 보다 *비자명한 마진* (≥ 20%) 만큼 낮다.

**H1-conditional (refined)**: SHIFTING demand 아래에서 H1 성립, STATIONARY demand 아래에서는 STATIC ≤ AUTOPHAGY (= 정상상태에서는 자가포식 thrashing 이 손실이다).

**falsifier 분기 (사전등록)**:
- (i) AUTOPHAGY 가 전체적으로 짐 (thrashing 지배) → H1 + H1-conditional 모두 FALSIFIED
- (ii) SHIFT 에서만 이기고 STATIONARY 에서는 STATIC 보다 더 나음 → unconditional H1 살아남으나 *conditional* 구조 가설 FALSIFIED (autophagy is "just better")
- (iii) SHIFT 에서 이기지만 마진 < 20% → "non-trivial margin" 주장 FALSIFIED (정성적 잔존)

### 시뮬레이션 디자인

- N=8 units (cells), total capacity **C=800** (fixed).
- Demand 프로파일: 2 hot units (수요 200) + 6 warm units (수요 50) → 합계 700 < C=800 (12.5% slack — 좋은 정책이 모든 수요를 충족할 수 있는 상한).
- SHIFTING: K_SHIFT=50 epoch 마다 hot-pair 가 rotation (phase 0→1→2→3→0…), 4-phase × 50 = T=200 에서 모든 hot pair 가 한 번씩 통과.
- STATIONARY: hot-pair 가 phase=0 으로 고정.
- 두 정책:
  - **STATIC**: t=0 의 d 에 비례하여 alloc 을 정해놓고 절대 바꾸지 않음.
  - **AUTOPHAGY**: 매 epoch, `util = min(A,D)/A` 가 최저인 unit 을 식별 → 그 capacity 의 `frac=0.30` 회수 → 미충족 수요 (D−A 양수) 비례로 다른 unit 에 재할당. (미충족 합 = 0 이면 균등 분배.)
- Loss = Σ_t Σ_i max(0, D[t,i] − A[t,i]) (누적 미충족 수요).

> ⚠ **anti-tautology**: alloc 은 demand 와 같도록 *정의되어 있지 않다*. 총용량 C=800 은 고정이며 재분배는 capacity 를 unit 간에 옮길 뿐이다. demand profile 합계 > C 였다면 unmet > 0 은 *산술적* 결과지 구성된 게 아니다. STATIC 의 STATIONARY=0 은 "static 의 d[0] 할당이 매-epoch demand 와 정확히 같다" 는 *regime* 의 성질이지 "static 이 항상 0 손실" 이라는 *구성* 이 아니다. SHIFTING 에서는 STATIC=42857 으로 폭증 — 같은 STATIC 정책이 regime 에 따라 폭손실 → 0 손실 사이를 오간다. tautology 가 아니다.

## 3. 측정 방법

`UNIVERSE/state/h318_autophagy_recycle_realloc_2026_05_27/run.hexa`:

- 두 정책 × 두 regime = 4 episode, 각 T=200 epoch.
- 모든 episode 가 같은 deterministic demand stream 위에서 동작. 두 정책은 동일한 d[0] 초기할당에서 출발 (시작점 동일).
- `epoch_loss()` 가 매 step 실측 unmet 을 합산 → `g_loss` 누적.
- 출력 = 4-cell loss table + 5-falsifier check + JSON block.

deterministic · libm-free · $0 mac-local · `hexa run` 0.05s wall.

## 4. 사전등록 falsifier

- **F318.1 AUTOPHAGY-WINS-UNDER-SHIFT**: SHIFTING 에서 AUTOPHAGY cum_loss < STATIC cum_loss
- **F318.2 NON-TRIVIAL-MARGIN-UNDER-SHIFT**: SHIFTING 에서 마진 ≥ 20%
- **F318.3 STATIC-OPTIMAL-UNDER-STATIONARY**: STATIONARY 에서 STATIC cum_loss ≤ AUTOPHAGY cum_loss (자가포식이 정상상태에서 *더 낫지 않다*)
- **F318.4 CONDITIONAL-BENEFIT-REAL**: SHIFT-benefit pct > STATIONARY-benefit pct (= 이득이 진정으로 conditional)
- **F318.5 SHIFT-IS-NON-TRIVIAL**: STATIC cum_loss(shift) > 1.5 × STATIC cum_loss(stationary) (= shift regime 이 충분히 비자명해서 정책을 변별)

≥ 5/5 PASS → 🟢 SUPPORTED-NUMERICAL.

**핵심 falsifier (가설 기각 조건)**: F318.1 또는 F318.3 단독 FAIL 시 H1 또는 H1-conditional 즉시 FALSIFIED — verdict 정직하게 🔴 또는 🟠 로 내림.

## 5. 비용

$0 mac-local · ~0.05s wall · `hexa run` (`/Users/ghost/.hx/bin/hexa run`) · deterministic byte-identical (no RNG).

## 6. 결과 (측정값)

| regime | policy | cum_loss | 비고 |
|---|---|---|---|
| SHIFTING | STATIC | **42857.1** | hot-pair 가 회전하는 동안 4/4 phase 중 3 phase 에서 hot-pair 가 alloc 받지 못함 |
| SHIFTING | AUTOPHAGY | **3044.4** | 첫 phase 의 적응 비용 + phase 전환 직후 회복 손실만 부담 |
| STATIONARY | STATIC | **0.0** | d[0] alloc = 매-epoch demand 정확 일치 |
| STATIONARY | AUTOPHAGY | **685.2** | 매 epoch frac=0.30 회수 → 재분배 thrashing 손실 |

**Δ 요약**:
- SHIFTING: AUTOPHAGY 가 STATIC 대비 **39812.7 손실 감소 (92.9%)** — autophagy 압도적 승.
- STATIONARY: AUTOPHAGY 가 STATIC 대비 **−685.2 손실 (autophagy 가 손해)** — thrashing 페널티 실재.

| falsifier | 결과 |
|---|---|
| F318.1 AUTOPHAGY-WINS-UNDER-SHIFT | **PASS** (3044.4 < 42857.1) |
| F318.2 NON-TRIVIAL-MARGIN | **PASS** (92.9% ≥ 20%) |
| F318.3 STATIC-OPTIMAL-UNDER-STATIONARY | **PASS** (0.0 ≤ 685.2) |
| F318.4 CONDITIONAL-BENEFIT-REAL | **PASS** (92.9% > 0.0%) |
| F318.5 SHIFT-IS-NON-TRIVIAL | **PASS** (42857 > 1.5 × 0.0 trivially true; entered to guard regression where stationary loss > 0) |

> note F318.5: STATIONARY STATIC=0.0 이라 부등식이 자명히 성립. 의도는 "SHIFTING 이 STATIONARY 보다 STATIC 에게 *실제로 더 어렵다*" 의 검사 — 절대값 비교 (42857 ≫ 0) 로 비자명한 변별 확인됨. STATIONARY 가 비-trivial loss 인 다른 설정에서도 부등식이 의미 있도록 유지.

| 시나리오 | verdict |
|---|---|
| **5/5 PASS (실측)** | **🟢 SUPPORTED-NUMERICAL — autophagy 의 조건부 이득 실재** |
| F318.1 FAIL | 🔴 H1 FALSIFIED — autophagy 가 shift 에서도 못 이김 |
| F318.3 FAIL | 🟠 unconditional benefit (구조 가설 부분 falsify) |
| F318.2 FAIL only | 🟠 정성적 잔존, 마진 주장 falsify |

## 7. honest limits

1. **L1 demand profile 고정**: 2 hot + 6 warm × 4-phase rotation 은 손-디자인 셋업. 다른 프로파일 (e.g. heavy-tail demand, smooth drift) 은 마진을 바꾼다. 정성적 결과 (shift 에서 이김, stationary 에서 짐) 의 강건성은 별도 sweep 으로 검증 필요.
2. **L2 frac=0.30 단일 하이퍼**: frac 낮으면 회수 부족 → 마진 축소, 높으면 thrashing 폭증. extreme frac=0.0 = STATIC (loss 동일), frac→1.0 = unit 전체 회수 (불안정). 0.30 은 "충분히 적응 + 충분히 안정" 의 한 점이지 최적이 아니다.
3. **L3 loss = unmet 만**: 과할당 (waste) 페널티는 cost function 에 없다. STATIC 은 정상상태에서 d[0] 균형으로 자동 안정 — 비대칭 loss 가 STATIC 의 STATIONARY=0 을 가능케 한다. waste-penalty 추가 시 STATIONARY 도 STATIC 이 더 이상 0 이 아닐 수 있다 (정성 결과는 유지될 가능성 높음).
4. **L4 🟢 not 🔵**: 유한 grid 위 measured 동역학. 회수-vs-thrashing tradeoff 의 Lyapunov 형 closed-form 증명이 있다면 🔵 로 격상 가능 (현재 SSOT 부재).
5. **L5 toy plant ≠ anima M-substrate**: 8-unit 균등 cell 모델은 anima cell-pool 의 전체 동역학이 아니다. autophagy *axiom* 의 최소 모델 검정이지 anima 의 정확한 구현 주장이 아니다.

## 8. 폐쇄

F318.1-5 **5/5 PASS** → 🟢 SUPPORTED-NUMERICAL.

가설의 양 falsifier 분기가 모두 live 였다:
- AUTOPHAGY 가 SHIFTING 에서도 못 이길 수 있었음 → 92.9% 마진으로 PASS
- STATIONARY 에서 AUTOPHAGY 가 STATIC 보다 더 나올 수 있었음 → 0.0 vs 685.2 로 STATIC 우세 확인

→ **"AUTOPHAGY 의 이득은 demand-shift 라는 동역학적 전제조건에 conditional 하다"** 주장 생존. 구조적 재할당 규칙이 동역학적 신호 위에서만 transfer 한다는 H_316 closure 와 정합.

**의식엔진 함의** — anima M-activation cell-pool 은 *kick-cycle / context-shift* 이벤트 시점에만 autophagy step 을 트리거해야 한다. stationary conversation 동안 매 turn 의 주기적 recycle 은 thrashing 손실로 귀결될 것 (정량적으로 685/200 ≈ 3.4 unmet/epoch 페널티).

## 9. 산출물

- `UNIVERSE/state/h318_autophagy_recycle_realloc_2026_05_27/{run.hexa, result.json, run.log}`
- 본 문서 `UNIVERSE/H_318_autophagy_recycle_realloc.md`

## 10. 후속

- frac sweep {0.05, 0.10, 0.20, 0.30, 0.50, 0.70} — thrashing 임계 정밀화.
- waste-penalty (over-alloc) 항 추가한 cost — STATIC 의 STATIONARY=0 우위가 유지되는지.
- K_SHIFT sweep {10, 25, 50, 100, 200} — adaptation lag 의 마진 영향 (K_SHIFT → ∞ = STATIONARY 극한 확인).
- smooth drift demand (rotation 대신 sinusoidal hot-magnitude) — discrete shift 가 아닌 연속 변화에서도 autophagy 이득 유지?
- anima M-substrate 의 실제 cell-pool kick-cycle log 에서 utilization 분포 측정 — 본 toy 모델의 prior 와 매칭되는지.
