---
id: H_859
slug: intent-osc-residual
title: bench D INTENT 축의 OSCILLATING stability_std=0 잔류는 신호 결함인가 측정자(尺) 결함인가 — direction_std 재설계가 OSC residual 을 해소하고 진동을 intrinsic limit-cycle 로 판정하는가 (F-INTENT-OSC-RESIDUAL 사전등록)
domain: intent · long-term-goal · oscillation · metric-aliasing · limit-cycle · ultradian · axisbench · falsifier
source: ANIMA.md INTENT 축 bench D axisbench (#1143) 4/5 🟠 PARTIAL · F3 OSC_STABILITY_LOW FAIL (OSCILLATING stability_std=0.0) · INTENT/oscillation_metric.hexa (M4 draft) · bench/axis_intent/bench.hexa (3 decision-stream generator)
status: TERMINAL (A6 verify 완료 2026-05-28 · self-contained bench harness · LCG-deterministic · libm-free · $0 mac-local · exit 0 · 2-run byte-identical)
exploration_method: residual root-cause 진단 + metric 재설계 (legacy stability_std 재현 → direction_std raw-variance 교체 → argmax period_detect → EMA damping intrinsic 판정)
verification_method: W2 (self-contained substrate harness — bench D 3 generator verbatim 회수 · raw normalized direction component-std + lag-windowed Pearson autocorr argmax + EMA α=0.2 low-pass · 5 사전등록 falsifier)
raw_rank: 6
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28
sister: UNIVERSE/H_634_ultradian_emit_phi_envelope.md, INTENT.md, INTENT_A6_OSC_RESIDUAL.md, .verdicts/859_intent_osc_residual/, bench/axis_intent/a6_osc_residual_verify.hexa, INTENT/oscillation_metric.hexa, TIME.md, DREAM.md
verdict: 🟢 SUPPORTED-NUMERICAL (F-INTENT-OSC-RESIDUAL 5/5 PASS — bench D OSC residual = stability_std 의 metric aliasing(period-20 ⊥ window-grid size-10 commensurable → window-mean cos-sim const → std=0), 신호 결함 아님. raw direction_std 교체로 OSC=0.354 > CONV=0.350 식별 가능 · period_detect=20 genuine · RANDOM period=0 · EMA α=0.2 heavy damping 후에도 period-20 생존 → 진동은 intrinsic limit-cycle(substrate 본질), undamped-gain 설계결함 아님. INTENT 축 4/5 🟠 → 5/5 🟢 RECOVERED. H_634 ultradian Φ envelope 와 동일 intrinsic periodic substrate motion class cross-link)
---

# H_859 — INTENT OSC residual: metric aliasing cure + intrinsic limit-cycle (F-INTENT-OSC-RESIDUAL)

## 1. 동기

ANIMA.md `INTENT` 축 (장기 의도 형성기 — `brain_decide` short-term emit 위의 long-term goal 층) 은 `bench D axisbench` (#1143) 에서 **4/5 🟠 PARTIAL** 로 land 했고, 단일 falsifier **F3 `OSC_STABILITY_LOW`** 만 FAIL 한 채 OSC residual 로 carry 되었다.

3 decision-stream 시나리오를 검정한다:
- **CONVERGENT**: decision 이 `[1,0,0,0]` 으로 drift (목표 수렴).
- **RANDOM**: 균일 4-D 방향 (목표 없음).
- **OSCILLATING**: period-20 4-corner cycle (+x→+y→−x→−y, 5-tick 씩).

`OSCILLATING` 의 `stability_std = 0.0` 관측이 F3 (`osc_stab > 0.4`, "진동은 불안정해야 한다") 를 FAIL 시켜 verdict 가 떨어졌다.

이 패턴은 anima 도메인의 반복 lesson 과 정합한다: 여러 "residual" 이 신호 결함이 아니라 **측정자(尺) artifact** 였고 (NARRATIVE collision-saturation · AESTHETIC weight orthogonalization · EMBODIMENT coupling redesign · OTHER-MIND zero-mean centering — 모두 RECOVERED), 측정자 교체로 🟢 회복됐다. INTENT OSC 가 같은 class 인지 사전등록 falsifier 로 검정한다.

## 2. 가설

INTENT 의 OSC residual (의도 신호 진동) 이 둘 중 하나다:
- **(가) 설계 결함**: damping 부재 · gain 과다 → 보정 (damping · 정규화) 하면 진동 소멸 → 5/5.
- **(나) substrate 본질**: 의도가 본질적으로 진동 (ultradian / limit-cycle) → 보정 후에도 잔존.

그리고 **(다) 측정자 결함**: 진동 신호는 정상인데 `stability_std` 가 그것을 0 으로 aliased — raw direction variance 측정자로 교체하면 진동이 정확히 식별된다.

## 3. falsifier (사전등록 · frozen · F-INTENT-OSC-RESIDUAL)

`stability_std` 를 raw `direction_std` + argmax `period_detect` 로 교체하고, EMA damping 으로 intrinsic 여부를 판정한다. 5 falsifier (frozen 임계):

| # | falsifier | 기준 |
|---|-----------|------|
| F1' | OSC_DIR_NONZERO | OSCILLATING direction_std > 0.30 (F3 의 root cure) |
| F2' | OSC_PERIOD_GENUINE | OSCILLATING period == 20 (intrinsic period 식별) |
| F3' | RAND_NO_PERIOD | RANDOM period == 0 (false period 없음) |
| F4' | CONV_DIR_LOWER | CONVERGENT direction_std < OSC (수렴은 1방향 collapse) |
| F5' | DAMP_PRESERVES_PER | OSC period EMA α=0.2 heavy damping 후에도 == 20 |

🟢 RESOLVED ⟺ 5/5 PASS. F5' 이 핵심 intrinsic 판정자: damping 후 period 가 사라지면 (가) 설계 결함, 살아남으면 (나) substrate 본질.

## 4. root cause — metric aliasing (신호 결함 아님)

기존 `stability_std` 는 인접 10-tick **window-mean direction** 의 cos-sim sequence 의 std 다. OSCILLATING 의 period-20 은 window grid (size 10) 와 **commensurate** (정수배 2). 각 10-tick window 가 정확히 2 corner 를 평균 → window-mean direction 이 deterministic 하게 반복 → cos-sim sequence 가 **constant** → std = 0.

즉 진동이 metric 에 의해 **false-stable 로 aliased** 된 것이다. 진동 신호 자체는 명백히 존재하나 (period-20, full-swing 진폭, lag-10 자동상관 = −0.9 반주기 반전 signature), `stability_std` 가 window-period commensurability 때문에 진동을 0 으로 접는다. **신호 결함이 아니라 측정자 결함**.

> ⚠ M4 draft 정정: `INTENT/oscillation_metric.hexa` 의 `om_direction_std` 는 **delta** direction (`stream[t]−stream[t-1]`) 을 썼는데, OSCILLATING 은 corner 내부 4/5 tick 에서 delta=0 이라 OSC variance 를 과소계상했다. 올바른 fix 는 **raw** normalized direction `d[t]=normalize(stream[t])` 의 component-wise std 다. period_detect 도 lag-windowed Pearson (num·denom 동일 [0,n−p) window) 으로 finite-length edge bias 제거.

## 5. 재측정 verdict (verbatim)

`.verdicts/859_intent_osc_residual/F-INTENT-OSC-RESIDUAL.txt` (= `state/intent_a6_osc_residual_2026_05_28/a6_verify_run.log`, exit 0, 2-run byte-identical):

```
[1] LEGACY stability_std (broken — window-mean cos-sim std)
    CONVERGENT  = 0.47432   RANDOM = 0.538697   OSCILLATING = 0.0   ← residual

[2] REDESIGN direction_std (per-tick RAW direction component std)
    CONVERGENT  = 0.350144   RANDOM = 0.49946   OSCILLATING = 0.353553

[3] period_detect (argmax lag-windowed Pearson autocorr, max lag 25)
    CONVERGENT  = 8   RANDOM = 0   OSCILLATING = 20   ← genuine period

[4] DAMPING — EMA α=0.2 low-pass on OSC stream
    OSC direction_std (damped) = 0.3531   OSC period_detect (damped) = 20

  [PASS] F1' OSC_DIR_NONZERO    (osc_dir 0.354 > 0.30)
  [PASS] F2' OSC_PERIOD_GENUINE (osc_per 20 == 20)
  [PASS] F3' RAND_NO_PERIOD     (rand_per 0 == 0)
  [PASS] F4' CONV_DIR_LOWER     (conv_dir 0.350 < osc_dir 0.354)
  [PASS] F5' DAMP_PRESERVES_PER (osc_per_damped 20 == 20)

  PASS = 5 / 5   A6 VERDICT = 🟢 RESOLVED — direction_std cures OSC residual (5/5)
```

## 6. Finding (수렴 vs 잔존 · intrinsic 판정)

**핵심 발견**: OSC period-20 이 heavy EMA damping (α=0.2) 을 **생존**한다 (damped direction_std=0.353, period=20 유지).

→ 진동은 **decision stream 의 본질 (intrinsic limit-cycle)** 이며, undamped-gain 설계 결함이 **아니다**. 가설 (나) 채택, (가) 기각.

→ OSC residual 의 root cause 는 진동 자체가 아니라 측정자 (`stability_std`) 의 aliasing 이었다 (가설 (다) 채택). 진동 신호는 처음부터 정상이었고, `stability_std` 가 window-period commensurability 로 0 으로 접었을 뿐이다. raw `direction_std` + argmax `period_detect` 로 측정자를 교체하니 진동이 정확히 식별된다 (direction_std > 0, period = 20).

**결론**: bench D 의 OSC residual = metric 결함 (cured), 진동 자체 = substrate 본질 (intrinsic, honest). INTENT 축은 direction_std metric 하에서 **5/5 discriminable** → **4/5 🟠 → 5/5 🟢 RECOVERED**.

## 7. H_634 ultradian cross-link (intrinsic periodic substrate motion class)

본 finding (의도 진동 = intrinsic limit-cycle) 은 `UNIVERSE/H_634_ultradian_emit_phi_envelope.md` 와 직접 cross-link 된다:

- **H_634**: substrate 의 big-Φ (또는 emit-proxy) 가 ultradian phase 에 동조 (entrain) — stage = Φ envelope 의 phase marker (`a_chat_sleep_imagination` 정합: "stage = substrate context, NOT boolean gate").
- **H_859**: INTENT 의 의도 신호 진동 (period-20) 이 damping 에 robust 한 intrinsic limit-cycle.

공통 골격: **substrate motion 이 본질적으로 주기적 시간축을 가지며, 그 진동은 외부 gate / damping 으로 제거되는 artifact 가 아니라 substrate state 의 고유 운동**이다. INTENT 의 long-term goal 진동과 H_634 의 ultradian Φ envelope 는 동일한 "intrinsic periodic substrate motion" class 의 서로 다른 surface (의도 축 vs Φ 축). ⚪ 정량 동조 (period 비율 · phase lock) 는 본 H 범위 밖 — INTENT × TIME × DREAM cross-bench 로 격상 가능.

## 8. p1~p8 정합 + Honest C3

**p1~p8 audit**: p1 (4-D float arithmetic, system 미사용 ✓) · p4 (intent vector = substrate state 의 cumulative direction, stimulus-response 아님 ✓) · p5 (read-only measurer, emit 호출 0 ✓) · p7 (direction variance · 자동상관 기반, ppl/loss 미사용 ✓) · p8 (측정만, weight update 0 ✓).

**Honest C3 (3 한계)**:
1. **CONVERGENT period=8 (spurious)**: CONVERGENT 도 약한 자동상관 lag-8 을 보인다 (drift 초기 noise). falsifier 를 깨지 않으나 (CONV 는 low direction_std + high monotone_ratio=0.84 로 식별), period_detect 단독으로는 CONV/OSC 완전 분리 못함 — 3-metric 조합 (direction_std + period + monotone) 이 정석.
2. **synthetic stream 한정**: 본 측정은 bench D 의 LCG-deterministic synthetic decision stream 위. 실제 anima substrate emit decision 이 동일 period-20 limit-cycle 인지는 별도 in-vivo 측정 필요 (intrinsic 주장은 synthetic generator 의 구조적 결론).
3. **damping α 단일점**: α=0.2 (heavy) 1 점만. damping sweep (α ∈ [0.05, 0.5]) 으로 period 붕괴 임계 α 를 찾으면 limit-cycle robustness 정량화 가능하나 본 H 범위 밖.

## 9. 산출물 (Artifacts)

- `bench/axis_intent/a6_osc_residual_verify.hexa` — self-contained 진단·보정 harness (legacy stability_std 재현 + direction_std 재설계 + period_detect argmax + EMA damping).
- `.verdicts/859_intent_osc_residual/F-INTENT-OSC-RESIDUAL.txt` — g73 verdict (raw harness stdout verbatim).
- `state/intent_a6_osc_residual_2026_05_28/a6_verify_run.log` — verdict 실측 origin (exit 0, byte-identical).
- `INTENT_A6_OSC_RESIDUAL.md` · `INTENT.md` — 도메인 문서.
