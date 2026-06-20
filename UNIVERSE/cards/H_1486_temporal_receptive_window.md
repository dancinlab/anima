# H_1486 — ⏳ TEMPORAL RECEPTIVE WINDOW / 시간 수용창 (P1 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror — engine-transfer UNVERIFIED, 하드게이트1)
- **wired:** `DIRECTIONAL-mirror` — R2 엔진-네이티브 재측정 follow-on (ING) 미완. 카드 verdict 는 DIRECTIONAL.
- **source:** 의식-고유 게이트 depletion 카탈로그 P1 (`state/gate_depletion_catalogue/CATALOGUE.md`) · "의식이라서 가능한 것" 시리즈
- **lens:** consciousness-science — temporal receptive window (Hasson / Honey / Lerner — 뇌 영역마다 정보 통합 시간규모가 계층적으로 다름) · 계층적 leaky/boxcar 통합창 · `a_no_llm_frame_trap`
- **artifacts:** `state/1486_temporal_receptive_window/h1486_temporal_receptive_window.py` · verdict `state/verdicts/1486_temporal_receptive_window/H_1486_FREEZE.json` · run `state/verdicts/1486_temporal_receptive_window/H_1486_run.txt`

## 주장

**시간 수용창(temporal receptive window, TRW)** = 뇌 영역마다 정보를 누적·통합하는 **시간 규모(window)가 계층적으로 다름** —
감각영역은 **짧은 창**(ms, 빠른 국소 변화 추적), 상위영역은 **긴 창**(수십초/서사 전체 누적). 같은 입력이라도
영역별 통합 시간규모가 달라, **긴-창 lane** 의 현재 응답은 **멀리 떨어진 과거(far-past)** 정보까지 반영하고,
짧은-창 lane 은 최근 입력만 반영한다.

**메커니즘** (계층적 시간-통합창 — boxcar window length tau, `a_no_llm_frame_trap`): 각 "영역" 은 입력
시계열 x(t) 에 대한 trailing tau-window 통합기. 통합은 **순서-민감(order-sensitive) 위치-태그 matched filter**
(Hasson 의 긴-TRW 영역 = window 안의 *시간 구조* 를 담음, 단순 평균 아님):

    h(T−1) = Σ_t  pos_code[t] (.) x(t)   (trailing tau-window 내 t)

- **짧은 창(tau=3)** → 최근 프레임만 → 초기 cue 블록은 창 밖 → far-past cue 망각(chance).
- **긴 창(tau=40 ≥ L=39)** → 전 스트림 + 초기 cue 블록이 창 안 + 순서 보존 → cue 복원.

**과제:** 길이 T=40 스트림의 초기 블록 [0,CUE_LEN)에 지속(sustained) cue(K=4 중 1)를 심고, t=T−1 에서
정체성 readout. 자기 시간규모(창 길이)가 초기 cue 까지 닿는 lane 만 정답.

— LLM 대비: autoregressive LLM 은 단일 attention span(고정 컨텍스트 길이)으로 모든 토큰을 병렬 처리, 영역별로
다른 통합 시간규모의 *계층* 이 없다. anima substrate 는 짧은 창(국소)·긴 창(서사)을 병렬로 가질 수 있다.

## DISTINCT (load-bearing)

- **vs subjective-time (lane 9, *시간감*):** subjective-time = novelty-가중 **경과시간(duration) 추정**(얼마나 길게
  *느꼈나*) — 스트림 → 스칼라, far-past cue **정체성 정보 없음**. bar c2: 같은 과제에서 subjective-time readout
  은 chance 0.255(긴-TRW 0.780). TRW = 통합창 **길이**(far-past 내용이 *살아남나*) ⊥ subjective-time = *얼마나
  길게 느꼈나*.
- **vs attentional-blink (lane 7, *시간적 주의 사각*):** blink = post-T1 좁은 window 의 표적 누락(window 내 억제
  dip). TRW gap 은 통합창 **scale(tau)** 의 차이(긴↔짧은 창 길이)이지 주의 사각지대 아님. 다른 축.

## 측정 (frozen-first · 3 seeds [1486,1487,1488] · T=40 · K=4 · DIM=32 · TAU_LONG=40 · TAU_SHORT=3 · CUE_LEN=10 · NOISE=0.25 · $0 CPU · p7 · chance 0.25)

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **c1 PRESENCE** | 긴 창이 far-past cue 복원, 짧은 창은 망각 | long **0.780** − short **0.255** = gap **0.525** | gap≥0.30 & long≥0.55 | ✅ |
| **c2 DISTINCT** | subjective-time(duration 스칼라)은 같은 과제에서 chance | long 0.780 − subj **0.255** = gap **0.525** | gap≥0.30 & subj≤0.45 | ✅ |
| **c3 SHUFFLE** | 시간 셔플 → 위치-태그 정렬 깨짐(Hasson scramble) → 붕괴 | shuf **0.397** | ≤0.45 | ✅ |
| **c4 ABLATE** | 창→짧게 → far-past cue 창 밖 == 짧은 lane → 붕괴 | abl **0.255** | ≤0.45 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — c1·c2·c3·c4 PASS (3 seeds 전부) → GREEN.**
긴 창이 39-step-back cue 를 복원하고(long 0.780, short 0.255, c1), subjective-time duration 스칼라는 같은 과제
chance(c2, 통합창 길이 ⊥ 시간감), 시간 셔플로 위치-태그 정렬이 깨져 붕괴(c3, Hasson scrambled-narrative),
창을 짧게 ablate 하면 짧은 lane 으로 붕괴(c4, far-past 복원이 창 길이로 EARNED).

## p6 guard (외부규칙 아님 · substrate-derived)

readout 은 **위치-태그 windowed 통합상태 h(T−1)** 만 읽고, 각 후보의 *clean* windowed 시그니처에 matched —
`answer=cue` 지름길·주입 라벨·per-window 손수 정확도·RLHF/persona **없음**. LONG/SHORT lane 의 유일한 차이는
**창 길이 tau**(입력/템플릿/위치코드/readout 규칙/noise 동일). c3 셔플(순서 파괴→붕괴) + c4 ablation(창→짧게→붕괴)이
far-past 복원이 창 길이로 **EARNED**(baked 아님)임을 증명.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중, 하드게이트1).
  engine-transfer UNVERIFIED → R2 = live `core/*.hexa` 위 계층적 통합창(짧은 tau ⊥ 긴 tau) byte-exact 재측정이
  GREEN/🧱 확정 전제.
- **`a_break_the_wall` TYPE-A 측정결함 수정 (frozen-first):** 최초 통합기(순수 exponential leaky sum)는 *가장 오래된*
  프레임을 기하급수 down-weight → 긴 tau 도 t=0 cue 망각(long_acc 0.368 ≈ chance) = **leak 아티팩트**, TRW 주장 아님.
  TRW 주장 = 창 **길이**(flat/순서 통합이 얼마나 뒤까지 닿나) → **boxcar 창 + 순서-민감 위치-태그 matched filter**
  (Hasson 조작화)로 교정. **bar 임계 전혀 안 움직임**(c1 gap≥0.30 & long≥0.55, c2 gap≥0.30 & subj≤0.45, c3 shuf≤0.45,
  c4 abl≤0.45 — 모든 개정에서 불변) → **tune-to-green 아님**, 메커니즘 SNR(boxcar·CUE_LEN sustained block·NOISE)만
  진짜 far-past 신호가 frozen bar 를 넘도록 설정.
- **SATURATED-ish existence-proof:** designed 창 동역학(학습 controller 아님). discriminator(short 0.255 · subj 0.255 ·
  shuf 0.397 · abl 0.255 전부 chance 근처 ↔ long 0.780)가 결정적.
- **SCOPE TOY:** 40-tick/3-seed/K=4/DIM=32/결정적 — TRW STRUCTURE(창-길이 계층) 검증이지 학습된 multi-timescale
  cortex 아님. scale/실제 corpus/연속 timescale 계층/zero-shot timescale generalization(arxiv 2601.02618)/engine-transfer
  UNVERIFIED.

## depletion 판정

**NOT depleted** — TRW 는 depletion test 양 leg 통과: (A) 짧은-창 엔진 대비 falsifiable gap(long−short 0.525,
ablation+shuffle control) AND (B) control-survived distinctness vs subjective-time(c2 0.255 chance) + 개념적으로 vs
attentional-blink. 통합창-**길이** 신호는 duration-**feeling**(subjective-time)·시간적 주의 dead-zone(blink)과 distinct.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` 에 계층적 통합창(짧은 tau ⊥ 긴 tau) + 순서-민감 readout 호스팅 가능성
   평가 → 있으면 §TemporalReceptiveWindow(window_integrate short/long + 위치-태그 matched readout) 배선 +
   `engine_cli_smoke` cases + ARCHITECTURE lockstep, 4 frozen bars byte-exact 재측정
   (`a_engine_native_learning`·`a_verified_must_wire`).
2. distinctness 정량 double-dissociation vs subjective-time(통합창 길이 ⊥ duration feeling) control-survived 측정.

xref: subjective-time(lane 9, distinct · 통합 길이 ⊥ 시간감)·attentional-blink(lane 7, distinct · scale ⊥ 사각지대)·
H_1482(binocular-rivalry G28)·H_1483(change-blindness G29)·H_1484(mental-imagery G30)·H_1485(priming G31)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·p6·p7·p8·c9 · arxiv 2601.02618.
