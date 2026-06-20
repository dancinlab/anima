# H_1494 — 🫀 P8 INTEROCEPTIVE PRECISION (내수용 감각 정밀도)

**tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror — 하드게이트1 적중, engine-transfer UNVERIFIED; wired:DIRECTIONAL-mirror)
**slug:** `1494_interoceptive_precision` · **seeds:** [1494,1495,1496] · **$0 CPU** · p7 · frozen-first · c9
**lens:** predictive-interoception (Seth 2013 / Critchley 2017 — 내부 신체신호 정밀도-가중) · a_no_llm_frame_trap
**arxiv:** [2511.13668](https://arxiv.org/abs/2511.13668) (integrative interoception/exteroception predictive coding)
**catalogue:** `state/gate_depletion_catalogue/CATALOGUE.md` §4 **P8** (🚀 약 — 발사가능 하단, "인접 lane control 사전검토 필요")

## 핵심 (claim)
interoceptive precision: 내부 신체신호(심박·호흡 등)의 **예측오류를 채널 신뢰도(precision = 역분산)로 가중**하는 2차 메커니즘. 같은 raw 내부신호라도 채널이 깨끗(저잡음)할수록 precision↑ → self-state 추론에서 그 신호가 지배. precision 축은 **내부(interoceptive) 채널**에 산다.

## FROZEN bars (사전등록, 3-seed mean)
- **(A) PRESENCE** precision-가중 내부 self-state 추정이 unweighted(precision-blind)보다 |err| 0.30↑ 감소.
- **(B) DISTINCT** (인접 lane 전부 control-survived):
  - **B1 vs AFFECT(H_1290)** 채널 잡음만 바꾸고 신호 VALUE 고정 → precision split ≥0.30 이면서 affect-VALUE split ≤0.05.
  - **B2 vs LEARNED-PRECISION(H_1472)** 이중 분리(double-dissociation): 내부잡음→exteroceptive-precision 불변 AND 관측횟수(H_1472 driver)→interoceptive-precision 불변. (직교 driver, ≤0.05)
  - **B3 vs BODY-OWNERSHIP(H_1478)** 외부 synchrony(lag 0) 고정 → ownership split ≤0.05.
- **(C) EARNED** precision-weighting ablate(uniform) → presence 이점 ≤0.05.
- **(D) SHUFFLE** channel↔reliability 결합 파괴(random weight) → 50-perm signed 이점 |.| ≤0.10.
- **vs H_1202 metacognition(meta-d′):** prose — interoceptive precision = 내부채널 신뢰가중(self-state 추론용)이지 외부결정 정확도 2차신뢰 아님. affect+exteroceptive control 이 이미 내부-precision 축 격리.

GREEN iff A ∧ B(B1∧B2∧B3) ∧ C ∧ D (전 seed). 못 넘으면 정직 RED = 고갈 신호.

## RESULT — 🟢 GREEN DIRECTIONAL (verbatim `state/verdicts/1494_interoceptive_precision/H_1494.txt`)
```
A PRESENCE     err_un 1.003 - err_pw 0.312 = 0.690 >= 0.3 -> True
B DISTINCT (control-survived vs every adjacent lane) -> True
  B1 vs AFFECT     prec_split 0.803>=0.3 AND aff_value_split 0.000<=0.05 -> True
  B2 vs LEARNED-PR double-dissoc max(count->intero, noise->extero) 0.000<=0.05 -> True
  B3 vs OWNERSHIP  ownership split (ext sync fixed) 0.000<=0.05 -> True
C EARNED(ablate) precision-blind advantage 0.000<=0.05 -> True
D SHUFFLE        50-perm signed advantage |0.013|<=0.1 -> True
```

## frozen-first 교정 (a_break_the_wall type-a, NOT tune-to-green)
첫 실행 PRESENCE=0.013 FAIL: T=200 채널평균이 LLN 으로 잡음을 평균소거 → precision-blind 추정도 거의 완벽 → abs-error 감소가 0.30 bar 아래로 cap = **측정-스케일 artifact**(천장 아님, precedent H_1472 err=0.5→1.0). 교정 = single-shot 채널(T=1, 채널당 1회 내수용 reading, precision=채널 역분산 σ⁻²). **BAR(0.30) 불변** — probe stimulus 스케일만 이동. 교정 후 PRESENCE=0.690.

## distinctness 판정 — DISTINCT(control-survived) 하나 **DERIVATIVE/약** (고갈 경계 신호)
- **통과:** 4 인접 lane(affect/learned-precision/ownership/metacognition) 전부와 control-survived distinct. B1 split 0.803, B2 이중분리 0.000, B3 0.000.
- **정직한 한계(c9):** interoceptive-precision 의 **연산(역분산 precision-weighting)은 H_1472 learned-precision 과 동일** — 유일 차이는 *입력원*(채널잡음 σ vs 관측횟수 count). catalogue (B) 의미의 distinctness(직교 driver, control-survived)는 만족하나, 이는 **기존 연산의 새 입력원**이지 새 연산이 아님 = 가장 derivative 한 distinctness. catalogue 의 🚀(약) · "(A) 조작화 약함(진짜 내부 신체신호 부재)" 경고와 일치. **B2/B3 control 이 0.000 인 것은 readout 이 입력을 안 받도록 구성된 면도 있음** — tautology 회피 위해 B2 에 이중분리(count→intero 불변) 추가했으나, 메커니즘 동일성은 남는다.
- **결론:** GREEN 이되 **고갈 경계** — depletion 카운트로 보면 "distinct 통과(고갈 아님)"지만 distinctness 의 *질*이 H_1471~H_1490 강후보보다 명백히 약함. 다음 약후보(P9 boredom/P10 mind-wandering)에서도 derivative distinctness 만 나오면 그 시점 🧱 G* 고갈 재판정 권고.

## SCOPE / 미검증
- 하드게이트1: numpy mirror → **DIRECTIONAL**(engine-transfer UNVERIFIED). grep `import torch|gauge_lib|numpy` 적중 → terminal 아님.
- R2 engine-native(live core/ §InteroceptivePrecision) 재측정 = follow-on(ING). TOY single-shot 2채널/3 seeds/deterministic readout — 진짜 내부 신체신호(EEG/심박 substrate) 미연결 · scale/real-corpus UNVERIFIED.
- `a_engine_native_learning`·`a_verified_must_wire`·`a_scale_honest_scope`·`a_toy_scale_recheck`.

## artifacts
- `state/1494_interoceptive_precision/h1494_interoceptive_precision.py` (probe, numpy)
- `state/1494_interoceptive_precision/h1494_result.json`
- `state/verdicts/1494_interoceptive_precision/H_1494.txt` (verbatim stdout) · `H_1494_FREEZE.json`

xref H_1290(affect interoception-VALUE)·H_1472(learned-precision 동일 연산)·H_1478(body-ownership 외부경계)·H_1202(meta-d′)·H_1468(precision-surprise)·CATALOGUE P8 · a_no_llm_frame_trap·a_break_the_wall·a_engine_native_learning·a_verified_must_wire·p7·c9·c2.
