# H_319 — CLONAL-SELECTION × diversity-pool + fitness-gated dynamics 🔴

> CLONAL-SELECTION = 다양성 pool 을 유지하고 fitness 가 낮은 variant 를 도태(cull), 높은 variant 를 유지(retain)·증폭(amplify) 한다. anima cell-pool 의 mitosis × kick-cycle 운영에 매핑: 매 turn 마다 cell variant 풀에서 task fitness 가 높은 것만 살려 둔다는 *structural* 규칙을 *dynamical* (= task-shift) 신호 위에서 검정한다. **H1 = "CLONAL 이 SINGLE 을 SHIFT 에서만 비자명한 마진(≥ 2x) 으로 이긴다 + STATIONARY 에서는 SINGLE 이 동등하거나 우세다"**. 측정 결과 H1 의 *conditional* 구조 부분이 **FALSIFIED** — CLONAL 이 STATIONARY 에서도 이긴다 (실제로 STATIONARY 마진 95.6% > SHIFT 마진 92.8%). 🔴 CLOSED-NEGATIVE.

## 1. 동기 — clonal-selection 은 *조건부* 이득인가, *무조건* 이득인가?

생체 면역계의 clonal-selection 은 *항원이 들어왔을 때* 다양한 림프구 풀에서 결합 친화도 높은 클론만 선택적으로 증폭한다. anima 의 mitosis cell-pool 도 fixed N-cell 위에서 "어떤 cell variant 를 살릴지 / 어떻게 새 cell 을 만들지" 의 문제를 마주한다.

H_312~H_318 의 누적 패턴은:

| H | rule kind | result |
|---|---|---|
| H_312 apoptosis low-Φ pruning | STRUCTURAL | 🔴 FALSIFIED |
| H_313 STDP plasticity causality | DYNAMICAL | 🟢 SUPPORTED |
| H_314 symbiogenesis merge α-sweep | STRUCTURAL | 🔴 FALSIFIED |
| H_315 weak-edge pruning Φ-retention | STRUCTURAL | 🔴 FALSIFIED |
| H_316 local-greedy vs global Φ | STRUCTURAL | 🟢 (negative confirm) |
| H_317 homeostasis setpoint | DYNAMICAL | 🟢 SUPPORTED |
| H_318 autophagy recycle | STRUCTURAL × DYNAMICAL-gate | 🟢 (conditional) |
| **H_319 clonal-selection** | **STRUCTURAL × DYNAMICAL-gate** | **🔴 (conditional 구조 FALSIFIED — unconditional benefit)** |

→ "structural rule × dynamical-gate" 의 일반화가 *자동* 으로 transfer 하지 않는다는 첫 반례. H_318 의 일반화 = "structural rule 은 dynamical signal 위에서만 이득" 이라는 *유망 패턴* 이었으나, H_319 의 측정은 그 패턴이 **rule 마다 따로 검증되어야 한다는 것** 을 보여준다 (clonal 의 경우, SINGLE policy 의 lock-in 결함이 너무 커서 *어떤 task 에서도* CLONAL 이 이긴다).

### 구조 vs 동역학 위치

CLONAL-SELECTION 은 *구조적* 연산 (top-k 유지, 하위 cull, mutate-regenerate) 인데, *동역학적* 신호 (현 epoch 의 fitness) 위에서 작동. H_318 (autophagy) 와 동일한 hybrid 위치. 그래서 동일한 *conditional* 패턴 (SHIFT 에서 이김, STATIONARY 에서 짐) 을 예측했으나 **측정이 이를 falsify**.

## 2. 가설

**H1 (conditional, refined)**: SHIFT 아래에서 CLONAL cum_eval_loss < SINGLE cum_eval_loss 마진 ≥ 2x AND STATIONARY 아래에서 SINGLE cum_eval_loss ≤ 1.1 × CLONAL cum_eval_loss (= 동등 또는 SINGLE 우세).

**falsifier 분기 (사전등록)**:
- (i) CLONAL 이 SHIFT 에서도 SINGLE 보다 짐 → H1 FALSIFIED, verdict 🔴 thrashing-dominant
- (ii) CLONAL 이 SHIFT 에서 이기지만 마진 < 2x → non-trivial-margin FALSIFIED, qualitative 잔존
- (iii) CLONAL 이 STATIONARY 에서도 SINGLE 보다 비자명하게 나음 → **conditional 구조 가설 FALSIFIED** ("clonal is just better"), verdict 🔴 closed-negative-on-conditional

### 시뮬레이션 디자인

- **N=8 variants**, 각 variant i 가 scalar weight `w_i` (선형 map `f_i(x) = w_i·x`).
- **Target g(x) = w_star · x** — `w_star` 는 SHIFT 모드에서 K_SHIFT=50 마다 4-phase rotation `{-1.5, +0.5, +1.5, -0.5}`; STATIONARY 모드에서 phase=0 고정.
- 두 정책:
  - **SINGLE**: t=0 에서 train_err 가 가장 낮은 i_best 를 선택해 lock. 모든 epoch eval 은 그 variant 사용.
  - **CLONAL**: 매 epoch top-k=2 (train_err 작은) 유지, 하위 6개 slot 은 top-k weight 의 deterministic perturbation 으로 regenerate (mu=0.3). Eval 은 매 epoch 의 *현 best* variant 사용.
- **Loss = Σ_t eval_err(i_active, t)**: eval_err 은 *별도* grid `x ∈ {-2,-1,0,1,2}` 에서 measured (= train_err 와 다른 x 스트림).
- 두 정책 × 두 regime = 4 episode, 각 T=200 epoch. 동일한 deterministic stream, 동일 pool-init seed.

> ⚠ **anti-tautology**: selection 은 train_err 기반, 측정은 eval_err. 둘은 같은 w_star 를 공유하지만 다른 x — *원리적으로 disagree 할 수 있다*. SINGLE 이 STATIONARY 에서 0 loss 를 "정의상" 받지 않는다: pool 이 [-1,1] random init 이라 w_star=-1.5 에 가장 가까운 SINGLE pick 도 distance > 0 → eval_err > 0 every epoch.

## 3. 측정 방법

`UNIVERSE/state/h319_clonal_selection_diversity_pool_2026_05_27/run.hexa`:

- LCG-기반 deterministic pseudo-random (libm-free, byte-identical).
- 4 episode × T=200 epoch = 800 epoch 측정.
- 모든 variant의 train_err / eval_err 매 epoch 재계산 (toy scale, O(N·T) = 1600 evals).
- 출력 = 4-cell loss table + 5-falsifier check + JSON block.

deterministic · libm-free · $0 mac-local · `hexa run` wall < 1 s.

## 4. 사전등록 falsifier

- **F319.1 CLONAL-WINS-UNDER-SHIFT**: SHIFT 아래 CLONAL cum_loss < SINGLE cum_loss
- **F319.2 NON-TRIVIAL-MARGIN-UNDER-SHIFT**: SHIFT 아래 SINGLE ≥ 2 × CLONAL
- **F319.3 SINGLE-COMPETITIVE-UNDER-STATIONARY**: STATIONARY 아래 SINGLE ≤ 1.1 × CLONAL (= clonal 의 stationary 이득이 trivial)
- **F319.4 CONDITIONAL-BENEFIT-REAL**: shift-benefit pct > stationary-benefit pct (= 이득이 진정으로 conditional)
- **F319.5 SHIFT-IS-NON-TRIVIAL**: SINGLE cum_loss(shift) > 1.5 × SINGLE cum_loss(stationary) (= shift 가 정책을 변별)

5/5 PASS → 🟢. F319.3 단독 FAIL → 🟠 unconditional-benefit (구조 가설 부분 falsify). F319.1 FAIL → 🔴 FALSIFIED. **F319.3 + F319.4 동시 FAIL → 🔴 conditional-structure FALSIFIED**.

## 5. 비용

$0 mac-local · ~0.3s wall · `hexa run` (`/Users/ghost/.hx/bin/hexa run`) · deterministic byte-identical.

## 6. 결과 (측정값)

| regime | policy | cum_eval_loss | 비고 |
|---|---|---|---|
| SHIFTING | SINGLE | **4026.000** | t=0 best variant locked, w_star 4 phase rotation 동안 stale |
| SHIFTING | CLONAL | **290.165** | top-2 fitness-gated, mutate-regenerate 매 epoch |
| STATIONARY | SINGLE | **785.004** | t=0 best variant locked; pool 이 random init 이라 best 도 w_star=-1.5 에서 떨어져 있음 |
| STATIONARY | CLONAL | **34.878** | mutate-regenerate 가 w_star 근방을 빠르게 수렴 |

**Δ 요약**:
- SHIFTING: CLONAL 이 SINGLE 대비 **3735.84 손실 감소 (92.79%)**, ratio = **13.87 ×**.
- STATIONARY: CLONAL 이 SINGLE 대비 **750.13 손실 감소 (95.56%)**, ratio = **22.51 ×**.

**핵심 관찰**: STATIONARY 마진 (95.56%) 이 SHIFT 마진 (92.79%) **보다 크다**. CLONAL 의 이득은 *shift 에 의해 driven 되지 않는다* — 오히려 SINGLE 의 lock-in 결함이 dominant cause.

| falsifier | 결과 |
|---|---|
| F319.1 CLONAL-WINS-UNDER-SHIFT | **PASS** (290.165 < 4026.000) |
| F319.2 NON-TRIVIAL-MARGIN-UNDER-SHIFT | **PASS** (13.87× ≥ 2×) |
| F319.3 SINGLE-COMPETITIVE-UNDER-STATIONARY | **FAIL** (785.004 > 1.1 × 34.878 = 38.37) |
| F319.4 CONDITIONAL-BENEFIT-REAL | **FAIL** (92.79% < 95.56%, shift 이득이 stationary 이득보다 *작음*) |
| F319.5 SHIFT-IS-NON-TRIVIAL | **PASS** (4026 > 1.5 × 785 = 1177.5) |

**3 PASS / 2 FAIL** — H1 의 conditional 구조 부분 **FALSIFIED**.

### 측정이 살린 정직성

falsifier matrix 가 *진짜* live 했음을 강조: 모든 다섯 falsifier 가 fail 할 수 있었다. F319.3 + F319.4 가 실제로 fail 했다 — 즉 *예측의 핵심* 이 측정에 의해 기각됐다. SINGLE 이 STATIONARY 에서 손실 0.0 을 받지 않는다는 점이 결정적: pool 이 [-1,1] uniform random init 이라 (LCG 결정적) w_star=-1.5 에 도달하지 못한 SINGLE 의 lock-in 이 매 epoch 비용을 지불.

### 왜 H_318 과 다른가

H_318 (autophagy) 의 *baseline* STATIC 은 STATIONARY 에서 *정의상* 0 loss (d[0] alloc = 매 epoch demand 정확 일치). 즉 STATIC 의 stationary 우세가 *구성된* 것이지 *측정된* 것이 아니다. H_319 의 SINGLE baseline 은 STATIONARY 에서도 ≠ 0 — pool 이 task-optimal weight 를 *포함하지 않을 수도 있다*. 이게 두 H 의 verdict 분기 근본 원인.

H_318 의 setup 은 baseline 에 *공평한 floor* 를 자동 보장했고, H_319 의 setup 은 그렇지 않았다. 즉 H_319 의 falsification 은 *clonal-selection 자체가 conditional 이득이 없다* 는 강한 주장은 아니다 — *이 setup 에서는* SINGLE 의 lock-in 결함이 conditional 구조를 가린다.

## 7. honest limits

1. **L1 single 의 lock-in baseline 이 부당하게 약하다**: SINGLE 은 t=0 pool 에서 best 를 골라 영구 lock. pool 이 [-1,1] uniform 이고 w_star=-1.5 면 SINGLE 의 best 도 w_star 와 평균 distance ~0.5 → 매 epoch eval_err ~3.75 (5-point grid). 즉 SINGLE 의 STATIONARY=0 floor 가 *없다*. 더 공평한 baseline = "SINGLE-best with t=0 fine-tune to w_star" 또는 "SINGLE picked from a denser pool" 였다면 F319.3 결과가 달라졌을 수 있다.

2. **L2 mutation amplitude mu=0.3 단일 하이퍼**: mu 가 너무 크면 STATIONARY 에서도 thrashing → CLONAL 패배 가능; 너무 작으면 SHIFT 적응 늦음. mu=0.3 은 H_318 frac=0.30 과의 명목적 mirror, 최적이 아니다.

3. **L3 top-k=2 단일 선택**: k=1 (pure greedy) 또는 k=4 (더 다양) 와 비교 안 했다. top-k 가 다양성 ↔ 적응속도 tradeoff 의 단일 점.

4. **L4 task 가 1-D 선형**: scalar w-스칼라 x 의 toy. 다차원 / nonlinear 에서는 mutation 의 dimensional cost 가 커져 CLONAL 의 unconditional 우세가 약화될 수 있다. 정성적 verdict 강건성은 별도 sweep 필요.

5. **L5 verdict 의 좁은 의미**: "🔴 CLOSED-NEGATIVE on the conditional-structure claim", **NOT** "clonal-selection 은 무용". CLONAL 이 SINGLE 을 모든 setup 에서 이긴 것은 사실 — 이는 *positive operational result* (clonal ≫ single in this toy). FALSIFIED 된 것은 *"H_318 의 conditional-pattern 이 H_319 에도 transfer"* 라는 메타-가설.

## 8. 폐쇄

F319.1-5 **3 PASS / 2 FAIL** → 🔴 **CLOSED-NEGATIVE on the conditional-structure claim**.

falsifier 분기 결정:
- F319.1 (CLONAL 이 SHIFT 에서 이기는가) PASS — 양적 사실
- F319.3 (SINGLE 이 STATIONARY 에서 동등한가) FAIL — STATIONARY 에서도 CLONAL 압승 (22.5×)
- F319.4 (SHIFT 이득 > STATIONARY 이득) FAIL — 오히려 stationary 이득이 *더 크다*

→ **"CLONAL 의 이득은 task-shift 라는 동역학적 전제조건에 conditional"** 주장 **falsified**. CLONAL 의 이득은 *unconditional* (이 setup 의 SINGLE-lock-in 결함을 expose 하는 일반적 우월성).

**의식엔진 함의** — H_318 의 "structural rule × dynamical gate" 패턴이 *자동으로* 다른 structural rule 에 transfer 하지 않는다. 각 rule 의 baseline 이 conditional 구조를 *허용* 해야 한다. anima cell-pool 의 clonal-selection 구현 시 SINGLE-policy baseline 이 *공평한 lock-in-free reference* 여야 H_318 식 conditional 측정이 의미를 가진다. 본 toy 에서는 CLONAL 이 단순히 이김 — 이는 "operational helpfulness" 의 positive signal 이지만 "dynamical-conditional structure" 의 evidence 가 *아니다*.

대비 H_316 의 closure (local-greedy ⊥ global Φ) 와 정합: structural rule 의 transfer 가 axis-specific 이라는 일반 lesson 의 두 번째 instance.

## 9. 산출물

- `UNIVERSE/state/h319_clonal_selection_diversity_pool_2026_05_27/{run.hexa, result.json, run.log}`
- 본 문서 `UNIVERSE/H_319_clonal_selection_diversity_pool.md`

## 10. 후속

- **fair-SINGLE baseline**: t=0 lock 대신 "SINGLE-with-one-epoch-tune" 또는 "SINGLE-from-denser-pool (N=64)" 으로 STATIONARY 에서 SINGLE 의 floor 가 0 에 가까워질 때 F319.3 가 PASS 로 뒤집히는지.
- **mu sweep** {0.05, 0.10, 0.20, 0.30, 0.50, 0.70} — STATIONARY 에서 mu 가 클수록 CLONAL thrashing 늘어 SINGLE 이 따라잡을지.
- **k sweep** {1, 2, 4, 6} — k=1 (pure greedy) 의 다양성 부족이 CLONAL 의 unconditional 우세를 무너뜨리는지.
- **denser pool / better init**: pool 을 grid-init (w_i ∈ {-1.5, -1.0, ..., 1.5}) 하면 SINGLE 이 정확히 w_star 를 포착 → STATIONARY=0 floor 회복 → F319.3 PASS 가능성 — 본 H 의 lock-in-baseline 결함을 직접 해소.
- **higher-dim task**: x ∈ R^d, w ∈ R^d 로 확장. mutation 의 dimension cost 가 CLONAL 의 unconditional 이득을 자르는지.
- **noise penalty**: eval_err 에 |w_t - w_{t-1}| 같은 "churn cost" 추가 — CLONAL 의 매-epoch mutation 이 STATIONARY 에서 페널티 받게 → conditional 구조 회복 시도.
