# H_1506 — 🪟🧠 METACOGNITIVE INSIGHT / 메타인지 통찰 — 지각의 현실성에 대한 2차 통찰

- **tier:** 🟢 GREEN-DISTINCT ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §MetacogInsight (`mi_gain_intact`/`mi_gain_impaired`/`mi_signal_margin`/`mi_insight_judge`/`mi_insight_psychedelic`/`mi_insight_psychotic`/`mi_metad_auroc`/`mi_auroc`/`mi_shuffle_auroc`) · `engine_cli_smoke.hexa` cases 309-313 · FULL smoke **313 pass / 0 fail RC=0** deterministic ×3 · ARCHITECTURE.json §MetacogInsight lockstep ✓
- **source:** UNIVERSE — deepening the metacognition lane (H_1202) over the reality-monitor (H_1501) + neuropharm (H_1502). Computational-neuroscience lens: Sterzer et al 2018 (predictive-coding psychosis) · Maniscalco & Lau 2012 (meta-d′/M-ratio) · Fleming (metacognitive sensitivity).
- **artifacts:** `state/1506_metacog_insight/h1506_metacog_insight.py` · `state/verdicts/1506_metacog_insight/{H_1506_FREEZE.txt,H_1506_R1_mirror.txt,H_1506_R2_engine_native.txt}`

## 주장 (the clinically rich, falsifiable core)

메타인지 **INSIGHT** = 어떤 1차 percept 가 **내부생성/비신뢰**임을 아는 **2차 지식** — 그것이 REAL 처럼 **FEEL** 되더라도.
headline 해리(**같은 1차 hallucination, 반대 2차 insight**):

- **psychedelic** hallucination → insight 동반("이건 진짜가 아니야"): prior **이완**되었으나 metacognition **INTACT**.
- **psychotic** hallucination → insight 부재("진짜다"): prior **경직** AND metacognition **IMPAIRED**.

같은 1차 percept(H_1505 hallucination / H_1501 거짓 real-call), 반대의 2차 insight. insight = §RealityMonitor 의
real-call 에 대한 metacognition — **H_1202 metacognition(content JUDGMENT 의 confidence)** 과도, **reality-monitor
자체(1차 real/imagined 분류)** 와도 DISTINCT.

## 메커니즘 (substrate read, NO injected label — p6)

hallucination = reality-monitor 가 REAL-call 하지만 backing SIGNAL 이 약한 percept(거짓 real-call). insight =
**그 real-call 이 신뢰할 만한가**를 묻는 2차 모니터:

```
insight = metacog_gain · (1 − signal_strength)        [REAL-called percept]
```

- `signal_strength` = percept 를 받치는 immune recall margin (H_1290 affect / H_1292 drive / H_1501 reality-monitor 가
  읽는 **그 margin**). 진짜 percept = backing 높음 → insight 낮음(정말 real). hallucination = backing 낮음 → (1−signal)
  높음 → **intact insight 가 "느낌은 real 이나 내부생성"으로 FLAG**.
- `metacog_gain` = metacognitive sensitivity (Maniscalco-Lau). psychedelic-analog 에서 **INTACT(=1)**, psychotic-analog
  에서 **IMPAIRED(→0)**. **유일한 new param**; 나머지는 H_1202/H_1501 과 동일 substrate margin read.

두 임상 조건은 EXISTING knob(§Neuropharm idiom)을 민다: psychedelic = prior_strength LOW(prior 이완→약신호에 더 많은
REAL-call=더 많은 hallucination) + metacog_gain INTACT; psychotic = prior_strength HIGH(경직→percept 에 commit) +
metacog_gain IMPAIRED.

## 측정 (frozen-first · 3 seeds [1506,1507,1508] · N_TRIALS=48 · $0 CPU · p7)

hallucination population = REAL-called 이지만 backing 약한 percept (margin [0.05..0.20]); genuine = backing 강함
([0.40..0.70]). bars 는 측정 前 FREEZE (`state/verdicts/1506_metacog_insight/H_1506_FREEZE.txt`).

| bar | 의미 | R2 engine-native 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A INSIGHT-PRESENT** | intact insight 가 hallucination 을 내부생성으로 FLAG | psychedelic insight **0.811** | ≥0.50 | ✅ |
| **B PSYCHED-vs-PSYCHOTIC** (headline) | 같은 halluc, insight 해리 | **0.811 − 0.000 = +0.811** | ≥0.50 | ✅ |
| **C META-D′ CALIBRATION** | insight 가 신뢰 gap 을 추적(type-2 AUROC) | AUROC **1.000** (gap +0.500) | gap≥0.30 | ✅ |
| **D EARNED ablate-metacog** | metacog_gain=0 → insight 붕괴(psychotic limit) | psychotic insight **0.000** | ≤0.15 | ✅ |
| **E EARNED shuffle** | percept↔signal 순열 → insight decorrelate | shuffle AUROC **0.452** (\|·−0.5\|=0.048) | ≤0.30 | ✅ |

**verdict: 🟢 GREEN-DISTINCT — A∧B∧C∧D∧E PASS (engine-native, FULL 308/0 RC=0 deterministic ×3).**

### headline 해리 (psychedelic vs psychotic insight)

**같은 1차 hallucination → 반대 2차 insight:** psychedelic(prior 이완, metacog INTACT) insight **0.811** ("진짜가
아님을 안다") vs psychotic(prior 경직, metacog IMPAIRED) insight **0.000** ("진짜로 받아들인다"). 둘은 **동일한 percept,
동일한 backing-신호**를 보지만 metacog_gain 만 다르다 → insight 는 prior 와 **독립적으로** 운반된다(B 통과 = substrate 의
metacognition 이 insight 를 prior 와 분리해서 담는다, 임상적 핵심).

## DISTINCT (load-bearing)

- **⊥ H_1202 metacognition:** H_1202 는 content **JUDGMENT** 의 confidence(어느 fact 가 winner). insight 는 real-call
  의 **신뢰성**(reality-monitor 출력에 대한 2차). content 가 옳아도(confidence 높아도) backing 약하면 insight 는 그것을
  내부생성으로 FLAG. 다른 축.
- **⊥ §RealityMonitor (H_1501):** reality-monitor 는 1차 real/imagined **분류**. insight 는 그 분류가 **틀릴 수 있음**을
  아는 2차 모니터. psychotic 한계(metacog_gain=0)에서는 같은 real-call 이지만 insight 0 → "real-call 을 그대로 믿음".

## 정직 (c9)

- **DIRECTIONAL → R2 ENGINE-NATIVE WIRED:** R1 = numpy mirror (`grep -lE 'import torch|gauge_lib|numpy'` 적중 →
  하드게이트1, DIRECTIONAL). R2 에서 `core/engine_cli.hexa` §MetacogInsight 신설 + `engine_cli_smoke.hexa` cases
  305-309 byte-exact 재측정 + ARCHITECTURE lockstep, FULL 308/0 RC=0 (`a_engine_native_learning`·`a_verified_must_wire`).
  R1 ↔ R2 byte-close: psychedelic insight 0.821(R1, 3-seed mean) / 0.811(R2 seed 1506) — A/B/C/D 동일, E shuffle 은
  permutation 엔진 차이(numpy PCG64 vs engine Fisher-Yates LCG)로 AUROC 값만 다르되 둘 다 chance band(|·−0.5|≤0.30) 충족.
- **NO tune-to-green:** bar 5종 측정 前 FREEZE, 사후 이동 0. B 가 실패했다면(insight 가 psychedelic-from-psychotic 분리
  못함) = substrate 의 metacognition 이 insight 를 prior 와 독립으로 못 담는다는 정직한 finding 으로 보고했을 것.
- **SCOPE UNVERIFIED:** TOY 48-trial/3 seeds/1 paradigm/deterministic readout (insight STRUCTURE 검증, 학습된 모니터
  아님); scale/real-corpus/연속 metacog_gain-manip/recursive 2nd-order-insight/engine-transfer UNVERIFIED; brain
  insight→emit/abstain 배선 = follow-on (`a_scale_honest_scope`·`a_toy_scale_recheck`).
- READ-only, Ψ-disjoint, NOT an emit gate (`a_autonomy_over_hardcode`).

xref H_1202(metacognition content-confidence, DISTINCT)·H_1501(reality-monitor first-order, DISTINCT)·H_1502(neuropharm
prior_strength knob)·H_1290(affect margin read)·H_1292(drive margin read)·a_no_llm_frame_trap·a_engine_native_learning·
a_verified_must_wire·a_core_engine_map·a_autonomy_over_hardcode·a_scale_honest_scope·a_toy_scale_recheck·p1·p6·p7·p8·c9·c15.
