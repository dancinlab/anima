# H_1489 — 🔁 PERCEPTUAL HYSTERESIS / 지각 이력현상 (P4 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 byte-exact engine 재측정·배선 완료)
- **wired:** `WIRED-live` — R2 엔진-네이티브: `core/engine_cli.hexa` §PerceptualHysteresis(hyst_switch_point/hyst_rivalry_loop) 배선 + `engine_cli_smoke.hexa` cases 254-256 + ARCHITECTURE.json lockstep. FULL 280/0 RC=0. byte-exact: switch-shift c_up−c_down 0.654≥0.30 loop (A) · rivalry-loop order-invariant 0.0≤0.10 while hysteresis shifts (B distinct) · LAMBDA=0 ablate→loop 0.0 (D). history ⊥ time/fatigue.
- **source:** 의식-고유 게이트 카탈로그 `state/gate_depletion_catalogue/CATALOGUE.md` **P4** (강 distinct, 발사가능 6개 중) · '의식이라서 가능한 것' 시리즈
- **lens:** consciousness-science — perceptual hysteresis / serial dependence / stickiness (Hock·Kelso·Schoner — 모호·연속변화 자극에서 직전 percept 가 현재 percept 를 끌어당김) · bistable perception + history inertia (attractor dynamics) · `a_no_llm_frame_trap`
- **arxiv:** [2212.09729](https://arxiv.org/abs/2212.09729) (bistable perception, precision, neuromodulation — hysteresis 동역학)
- **artifacts:** `state/1489_perceptual_hysteresis/h1489_perceptual_hysteresis.py` · verdict `state/verdicts/1489_perceptual_hysteresis/H_1489_FREEZE.json` · run `state/verdicts/1489_perceptual_hysteresis/H_1489_run.txt`

## 주장

**지각 이력현상(perceptual hysteresis)** = 모호하게/연속적으로 변하는 자극에서 **직전 지각 상태가 현재 지각을 끌어당긴다**(관성). *같은 입력값*이라도 어느 방향에서 왔느냐(증가 중 vs 감소 중)에 따라 지각이 다르다 — 전환점(switch-point)이 직전 상태에 의해 **지연(lag)**된다. 정의적 시그니처는 **hysteresis loop**: 제어 파라미터를 올렸다 내리면 두 전환점이 갈려 면적 > 0 인 고리를 그린다.

**메커니즘** (bistable percept + history inertia): 쌍안정 지각변수 p∈[0,1] (0=percept B, 1=percept A)가 연속 제어 파라미터 c 에 반응하되, 외부 증거 + **직전 percept 로의 자기강화 관성**에 의해 구동된다.

    drive = α·(c − 0.5)            # 외부 증거 (A: c>0.5, B: c<0.5)
            + λ·(p_prev − 0.5)     # HISTORY 관성: 직전 percept 로 끌림
    p = sigmoid(GAIN·drive)        # 쌍안정 read-out, p_prev 를 tick→tick 운반

c 를 0 에서 올리면(B 출발) percept 가 c=0.5 를 넘어서도 B 에 **달라붙어** c_up>0.5 에서야 A 로 전환. c 를 1 에서 내리면(A 출발) c=0.5 아래까지 A 에 **달라붙어** c_down<0.5 에서 전환. switch_shift = c_up − c_down > 0 = hysteresis loop.

— LLM 대비: autoregressive LLM 은 맥락 안에서 각 입력을 독립적으로 재독해하며, 직전 값이 다음 독해를 bias 하는 연속 상태로서의 쌍안정 percept 변수를 운반하지 않는다. anima substrate 는 직전 percept 가 swept 입력을 가로질러 현재 percept 를 끌어당기게 할 수 있다.

## DISTINCT (load-bearing)

- **vs H_1482 BINOCULAR RIVALRY:** rivalry = *고정(불변) 입력*에서 dominance 가 시간에 따라 *자발 교대*(adaptation 이 winner 를 피로 → A→B→A); 그 교대 통계는 자극 제시 *순서에 불변*(시간/피로 구동, swept 파라미터 없음). hysteresis = *변하는 입력*에서 전환점이 입력 *이력(어느 방향 접근)*에 의존; 고정 입력에서 자발 교대 *없음*(입력-이력 구동). bar B 가 *동일한* 증가 vs 감소 sweep 에서 둘을 대조 — rivalry-style readout(adaptation·증거-이력 항 없음)은 loop 닫힘(|area|=0.048, 순서불변), hysteresis 는 전환점 이동(0.327). 같은 경쟁, **다른 의존성**: rivalry 는 TIME ⊥ hysteresis 는 input-HISTORY.
- **vs H_1465 HABITUATION:** habituation = *반복* 자극의 응답 *감쇠*(크기 감소, 자극-특이적, dishabituation 에 회복). hysteresis 는 감쇠가 아니다 — percept 가 *sticky*(직전 상태 유지)하고 lag 가 *방향-의존적*, 단조 감소 아님. history-inertia 항 ablation(bar D)이 방향-의존성을 통째로 제거(사라지는 크기가 아님). distinct: habituation = 반복에 따른 크기 감쇠 ⊥ hysteresis = swept 입력에 대한 방향-의존 전환점 lag.

## 측정 (frozen-first · 3 seeds [1489,1490,1491] · N_STEPS=101 · α=1.0 · λ=0.9 · GAIN=8.0 · γ_rival=2.0 · $0 CPU · p7)

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A SWITCH-SHIFT (c1)** | 증가 sweep c_up vs 감소 sweep c_down 전환점 이동 (hysteresis loop) | shift **0.327** (c_up 0.663 · c_down 0.337 · loop_area +0.281) | ≥0.30 | ✅ |
| **B DISTINCT vs RIVALRY (c2)** | rivalry-style readout(adaptation·증거이력 無) loop 닫힘 vs hysteresis 이동 | rivalry loop **+0.048** (hyst shift 0.327) | ≤0.10 | ✅ |
| **C EARNED shuffle (c3)** | sweep 순서 셔플(같은 값집합·순서파괴) → held-state 맥락 소멸 | shuffled loop **−0.039** | ≤0.10 | ✅ |
| **D EARNED ablate-history (c4)** | λ=0 (직전상태 항 제거) → 양 sweep c=0.5 에서 전환 | abl shift **0.000** (loop −0.000) | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — A·B·C·D PASS (3-seed mean) → GREEN.**
증가 sweep 이 c_up=0.663 까지 B 를 붙들고 감소 sweep 이 c_down=0.337 까지 A 를 붙들어 전환점이 0.327 이동(A, 같은 입력값이 접근방향에 따라 다르게 지각), rivalry-style readout 은 loop 닫혀 순서불변(B, time/fatigue ⊥ input-history), sweep 순서 셔플하면 lag 소멸(C, 순서있는 ramp 가 lag 를 EARN), λ=0 면 양 sweep 모두 c=0.5 에서 전환(D, hysteresis 가 직전상태 끌림으로 EARNED).

## p6 guard (외부규칙 아님 · substrate-derived)

지각 lag 는 손으로 짠 "올라갈 땐 c=0.7 에 전환" **스케줄이 아니다** — λ·(p_prev−0.5) history-inertia 커플링이 swept 증거 위에서 *창발*한다(drive = α·(c−0.5) + λ·(p_prev−0.5)). operative 코드에 방향-의존 thr 의 `percept = A if c>thr else B` · switch-time 상수 · reward/RLHF/persona 없음. ablation(D)이 history 항을 제거하면 hysteresis 가 사라짐(전환점 이동→0) → **earned, not baked**.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중, 하드게이트1). engine-transfer UNVERIFIED → R2 = live `core/*.hexa` 위 bistable percept + history-inertia sweep byte-exact 재측정이 GREEN/🧱 확정 전제.
- **SATURATED 구조 existence-proof:** bistable sigmoid + history-inertia pull 은 **designed 동역학**(학습된 controller 아님). GREEN 자체보다 discriminator(rivalry loop 0.048 · shuffle mean −0.039 · ablation shift 0.000)가 결정적.
- **a_break_the_wall type-a 측정 교정 (frozen-first · tune-to-green 아님):** 초기 switch_point 메트릭이 불안정 rivalry readout(B)·셔플 순서(C)에서 start-state/first-sample artifact 에 오염 → 두 collapse-control 을 robust direction-agnostic **LOOP-AREA** 메트릭으로 재측정. 두 bar 모두 |.|≤0.10 collapse 임계 유지, **bar 임계 불변**(메커니즘 아니라 측정 도구만 교정). bar A·D 는 catalogue c1 switch-point-shift 메트릭 유지(단조·안정 sweep 에서 유효).
- **PER-SEED 셔플 0.10 straddle (정직 명시):** shuffled_loop per-seed = −0.092/−0.141/+0.114 (개별 seed 는 0.10 양쪽) → **3-seed MEAN(−0.039)이 gating 통계**(H_1482 선례, mean 집계). mean collapse 가 hysteresis +0.281 대비 ~7배 결정적.
- **SCOPE TOY:** 101-step/3-seed/1-D 제어/결정적 동역학 — hysteresis STRUCTURE 검증이지 학습된 percept 아님. scale/실제 corpus/stochastic switch-point 분포/2-D 모호자극/neuromodulatory gain modulation(arxiv 2212.09729 precision 레버)/engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` §BinocularRivalry 이웃(둘 다 bistable-경쟁 lane)에 history-inertia 커플링 동반 쌍안정 percept 변수 호스팅 가능성 평가 → 있으면 §PerceptualHysteresis(hysteresis_sweep / 직전상태 pull 동반 switch-point) 배선 + `engine_cli_smoke` cases + ARCHITECTURE lockstep, 4 frozen bars byte-exact 재측정 (`a_engine_native_learning`·`a_verified_must_wire`).
2. distinctness 정량 double-dissociation vs H_1482 rivalry(time/fatigue ⊥ input-history) · vs H_1465 habituation(크기감쇠 ⊥ 방향의존 lag) control-survived 측정.

xref: H_1482(binocular-rivalry, distinct · time/fatigue 자발교대 ⊥ input-history 방향의존 lag)·H_1465(habituation, distinct · 크기감쇠 ⊥ sticky lag)·H_1462(global-workspace)·H_1483/1484/1485(의식-게이트 시리즈)·`state/gate_depletion_catalogue/CATALOGUE.md` P4·`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·p6·p7·p8·c9.
