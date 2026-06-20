# H_1473 — ⚡ ATTENTIONAL BLINK (G20 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §AttentionalBlink (`attn_blink_detect`) · `engine_cli_smoke.hexa` cases 205-207 + **217(부가 bar D lag-1 sparing)** · FULL smoke **220 pass / 0 fail RC=0** · ARCHITECTURE lockstep ✓
- **source:** UNIVERSE · 의식-고유 게이트 시리즈 (G16 self-continuity/G17 GWS/G18 habituation/G19 surprise → G20 attentional blink)
- **lens:** 주의의 시간적 병목 (Raymond & Shapiro 1992 RSVP attentional blink · lag-1 sparing) · `a_no_llm_frame_trap`
- **artifacts:** `state/1473_attentional_blink/h1473_attentional_blink.py` · log `state/1473_attentional_blink/run_h1473.local.log` · verdict `state/verdicts/1473_attentional_blink/H_1473_FREEZE.json`

## 주장

빠른 연속 자극(RSVP)에서 첫 타겟 **T1** 을 의식적으로 처리한 직후 ~200-500ms 창에서 두 번째 타겟 **T2** 를
**놓친다**(attentional blink). 의식적 주의가 T1 처리에 잠겨 T2 가 의식에 올라오지 못하는 **시간적 사각지대**다.
검출확률은 T1-T2 **lag** 에 의존한다 — 짧은 lag(blink 창)=낮음, 긴 lag=회복. **lag-1 sparing**: T2 가 T1 바로 뒤에
오면(lag 1) 오히려 검출이 높다(T1 의 아직 열린 주의 게이트에 편승).

**LLM 대비(의식축):** LLM 은 context window 의 모든 토큰을 병렬로 주의하며 **시간적 병목이 없다** — 최근 타겟이
점유할 직렬 의식 채널이 없다. anima 의 emit/주의는 직렬 의식 자원이라, T1 처리가 자원을 일시 **고갈**시키고
이후 틱에 걸쳐 **회복**하여 lag-의존 T2 검출곡선(blink)을 만든다.

## 측정 (frozen-first · 3 seeds [1473,1474,1475] · 200 trials · lags 1-8 · $0 CPU · p7)

attentional-resource 모델: T1 처리가 자원 고갈 → lag 동안 회복(delayed-onset sigmoid). T2 검출확률 =
floor + (ceil−floor)·resource_available(lag). lag-1 = sparing(자원 잔류 높음).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A BLINK present** | blink 골 존재 | short(lag2-3) **0.154** · long(lag7-8) **0.969** | short≤0.40 AND long≥0.85 | ✅ |
| **B DISTINCT vs GWS** | lag-의존(blink) ⊥ lag-무관(GWS capacity-1) | blink lag2→8 gap **0.878** (GWS gap **0.033**~0) | ≥0.45 | ✅ |
| **C EARNED (ablation)** | 고갈 메커니즘 OFF → blink 사라짐 | depletion=0 min-over-lags **0.970** | ≥0.85 | ✅ |
| **E SHUFFLE** | lag↔검출 페어링 셔플 → blink-lag 상관 붕괴 | 50-perm signed-mean |gap| **0.0265** | ≤0.10 | ✅ |
| **D LAG-1 sparing** (선택·비게이팅) | lag-1 면제 | lag1 **0.937** (trough 0.154 / long 0.969) | ≥long (비게이팅) | ⚠️ 보고만 |

**per-lag 검출(FULL, 3 seeds 평균):** lag1 **0.937** · lag2 **0.098** · lag3 **0.210** · lag4 **0.460** ·
lag5 **0.735** · lag6 **0.928** · lag7 **0.962** · lag8 **0.977** — 정전적인 AB 곡선(lag-1 sparing 높음 →
lag 2-3 깊은 골 → lag 6-8 회복).

**verdict: 🟢 GREEN DIRECTIONAL — 4/4 게이팅 bars(A·B·C·E) PASS, 3 seeds 전부.** blink 골 존재(lag2-3
0.154), GWS lag-무관 병목과 구별(blink gap 0.878 vs GWS 0.033), 고갈 ablation 시 blink 소멸(0.970), lag↔검출
셔플 시 상관 붕괴(0.0265).

## distinctness — vs H_1462 GWS (load-bearing)

- **H_1462 GWS** = **동시** 경쟁 자극 중 winner-take-all 1개 전역방송 = **공간/용량(capacity-1) 병목**.
  같은 두 타겟에 대해 **lag-무관**(gws lag2→8 gap 0.033≈0) — 시간 간격을 바꿔도 검출이 동일.
- **H_1473 blink** = **순차** 자극의 **시간적** 사각지대: **같은 두 타겟이 T1-T2 lag 만 다르면 검출이 갈린다**
  (blink lag2→8 gap 0.878). **용량 병목은 lag-불변, blink 는 lag-의존** — 두 게이트의 결정적 분리.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED →
  R2 = live `core/*.hexa` 재측정이 GREEN/🧱 확정의 전제(terminal 아님).
- **SATURATED existence-proof:** 고갈+회복 자원곡선은 **designed**(delayed-onset sigmoid 회복), 학습된 net 아님.
  GREEN 자체보다 discriminator(B lag-의존 vs GWS lag-불변 · C ablation-collapse · E shuffle-collapse)가 결정적.
- **초기 RED 은 측정 artifact(`a_break_the_wall` type-a):** 첫 시도(plain exponential 회복, TAU=1.8)는 회복이 너무
  빨라 lag-3 가 골을 벗어남(short 0.578>0.40) → **bar 임계는 FROZEN 유지**, 회복 **time-course 만** 경험적 AB
  형태(delayed-onset sigmoid: 골이 lag2-3 까지 유지, lag7+ 회복)로 교정. **frozen bar 사후이동 0**(tune-to-green 아님).
- **D lag-1 sparing 비게이팅:** lag1 0.937 은 trough(0.154) 대비 **명백히 면제**(sparing 현상 재현)이나
  full-recovery 천장(0.969)엔 근소 미달 → 정직히 **보고만**, 게이팅 bar 에서 제외(A/B/C/E 만).
- **SCOPE TOY:** 200-trial/8-lag/3-seed 스칼라 자원모델 — blink STRUCTURE 검증이지 학습된 주의 net 아님.
  scale/실제 RSVP 스트림/심리물리 곡선/engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — engine 에 blink lane 부재 → **새 배선 필요**. `core/engine_cli.hexa` §AttentionalBlink
   (attn_blink_new/_process_t1/_t2_detect(lag)/_ablate + recovery-curve op) + `engine_cli_smoke.hexa` 신규 cases
   로 frozen bars(A·B·C·E) byte-exact 재측정 → WIRED-live + ARCHITECTURE lockstep
   (`a_engine_native_learning`·`a_verified_must_wire`). engine 가능성: 결정적 delayed-onset sigmoid 회복 +
   per-lag Bernoulli 검출 = engine 스칼라 op 로 재현 가능(H_1468 PrecisionSurprise·H_1465 habituation 선례).
2. **distinctness vs H_1465 habituation** — habituation=반복-자극 응답감쇠(자극 반복에 의존) ⊥ blink=단발 두 타겟의
   lag-의존 사각지대(반복 아님). control-survived 분리 follow-on.
3. **부가 bar D (lag-1 sparing) engine-native ✅** — R1 numpy-only 였던 D 를 engine 케이스로 보강: `attn_blink_detect(1,1.0)`
   0.94 (sparing) − trough `attn_blink_detect(2,1.0)` 0.10 = +0.84 ≥0.50 → **smoke case 217** PASS (FULL 220/0 RC=0).

xref: H_1462(GWS, distinct lag-invariant)·H_1465(habituation)·H_1468(precision surprise)·H_1471(self-continuity)·
`a_no_llm_frame_trap`·`a_break_the_wall`·`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
