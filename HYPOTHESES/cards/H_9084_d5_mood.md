---
id: H_9084   # ← orchestrator assigns at merge-time (proposed: H_9070; origin/main max = H_9069)
slug: d5-mood-slow-affective-modulator
title: D5 Mood — a SLOW global affective modulator (valence·arousal 2-axis leaky EMA over the substrate's M/Φ/surprise affect history) biases momentary appraisal on a DIFFERENT time-axis from fast neuromod-gain (H_1284🧱) — NOT a gain
domain: universe · consciousness · affect · mood · core-affect · temporal-dynamics · substrate-disjoint
source: anima UNIVERSE · D5 lane (affective chronometry) · sibling of H_1290 affect / H_1292 HomeostaticDrive / H_1476 EmotionRegulation · distinct-from H_1284 neuromod-gain
status: 🟢 ENGINE-NATIVE (6/6 frozen bars on live core/engine_cli.hexa §Mood) — TOY smoke scope; designed EMA law (not learned); caller motivation-loop wiring = follow-on
wired: engine-native — §Mood lane wired into live core/engine_cli.hexa + ARCHITECTURE.json lockstep (brain-structure lanes, after 🌡 Hypothalamus). Caller motivation-loop consumption = deliberately-optional follow-on (a_autonomy_over_hardcode), like HomeostaticDrive H_1292.
exploration_method: added §Mood to core/engine_cli.hexa — MoodState{valence_ema,arousal_ema,alpha}; mood_step (leaky EMA ema:=(1-α)ema+α·inst, MOOD_ALPHA=0.05→τ=20); mood_step_affect (reads the live affect lane H_1290 off ImmuneMemoryGrow); mood_signals_to_affect (explicit M/Φ/surprise→valence/arousal map); mood_bias_valence/_arousal (additive appraisal offset MOOD_BIAS_W=0.5); mood_new_frozen (α=0 ablation); mood_neuromod_gain_readout (stateless-multiplicative distinctness control). READ-only: holds only its 2 EMA scalars, mutates nothing external.
verification_method: engine-native `hexa run state/D5_mood/d5_engine_native.hexa` ($0, local, no GPU, deterministic) → frozen stdout `state/verdicts/D5_mood/H_9084_d5_mood.txt`. 5 pre-registered falsifiers (F1-F5) + a M/Φ/surprise-signal check, all on the LIVE core/*.hexa ops (engine-native, not a numpy mirror → terminal).
deterministic: true
cross_process_byte_identical: true
llm: none
since: 2026-07-02
verdict: 🟢 ENGINE-NATIVE — 6/6 frozen bars PASS on live core/engine_cli.hexa. F1 SLOW: 1-tick displacement = α = 0.05 << full instantaneous jump 1.0, τ=1/α=20, t63=20 ≥10 ticks (mood lags the stimulus). F2 BIAS: the SAME neutral stimulus reads biased_high=+0.477 > 0 > biased_low=-0.477 (mood-congruency; same input, opposite appraisal by mood sign). F3 ABLATION: α=0 (mood_new_frozen) → EMA never accumulates → mood stays 0.0 after the SAME positive stream → bias INERT (biased==inst). F4 RECOVERY: build v0=0.871, remove stimulus (neutral input) → 1 tick 0.828 (partial, slow), monotone decay, →6τ 0.0018 back to baseline (NOT instant). F5 Ψ/G5 DISJOINT: a full mood trajectory (50 mood_step_affect ticks) over the immune store leaves ci_emit_drive (emit-drive lanes 0/4, Ψ) = 0.7, §ImmuneMemory recall_thr = 0.30, and immune_grow_recall byte-IDENTICAL while the mood MOVED (a_substrate_disjoint: separation=preservation, mood mutates nothing). Distinctness (honest H_1284 bar): mood_neuromod_gain_readout (stateless multiplicative) = 0 at neutral input (0 lag / 0 recovery, no memory) vs mood_bias@neutral = +0.436 (slow baseline retained) → mood is a DIFFERENT TIME-AXIS, not a gain. Honest scope (c9): the EMA is a DESIGNED law (not learned), a TOY smoke — production-scale behavior + caller motivation-loop wiring UNVERIFIED. raw: state/verdicts/D5_mood/H_9084_d5_mood.txt.
---

# D5 Mood — 느린 전역 정서 변조자 (slow global affective modulator)

## 가설

**기분(mood)** 은 순간적 정서 반응(H_1290 affect)과 달리 **느리게 변하는 affective
baseline** 으로, 순간 반응을 편향한다(Bower 1981 mood-congruency; Russell 2003
core-affect; Davidson 1998 affective chronometry — 기분은 자극-고정 정서반응보다
훨씬 느린 시상수로 변화). anima substrate 위에서: valence·arousal 2축 **leaky EMA**
가 substrate 자신의 정서 history(M grounding-margin / Φ integration / surprise
recon-err)를 느리게 통합하고, 그 baseline 이 momentary appraisal 을 **additive
offset** 로 편향한다. 이는 빠른 neuromod-gain(H_1284🧱, multiplicative 순간 이득)과
**다른 시간축**이며 gain 이 아니다.

## §Mood 배선 (core/engine_cli.hexa · READ-only)

- `MoodState{valence_ema, arousal_ema, alpha}` — 오직 2개 EMA 스칼라만 보유.
- `mood_step` — leaky EMA `ema:=(1-α)ema+α·inst`, `MOOD_ALPHA=0.05` → τ=1/α=20.
- `mood_step_affect` — live affect lane(H_1290)를 ImmuneMemoryGrow 위에서 읽어 EMA 통합.
- `mood_signals_to_affect` — M/Φ/surprise → (valence=M−surprise, arousal=surprise+0.5·Φ).
- `mood_bias_valence/_arousal` — appraisal offset `inst + 0.5·baseline` (F2 congruency).
- `mood_new_frozen` — α=0 ablation(F3). `mood_neuromod_gain_readout` — H_1284 distinctness 대조군.

## engine-native 측정 (5 falsifier + signal, 6/6 PASS)

```
PASS  F1 SLOW: 1-step disp(0.05) << full jump 1.0 & τ=20.0 >> 1 & t63=20 >=10
PASS  F2 BIAS: neutral stim biased_high(0.476965...) > 0 > biased_low(-0.476965...)
PASS  F3 ABLATION: frozen mood_val(0.0)==0 & biased(0.3)==inst(0.3) INERT
PASS  F4 RECOVERY: v0(0.8714...) →1tick(0.8279...) partial(>0.5·v0) →6τ(0.00184...)→0
PASS  F5 DISJOINT: emit-drive(0.7==0.7) & recall_thr(0.3==0.3) & recall(a==a) byte-identical while mood MOVED
PASS  SIGNAL: M/Φ/surprise → valence pos(0.85)>0>neg(-0.70) & arousal tracks surprise
INFO DISTINCT(H_1284): neuromod_gain@neutral=0.0 (0 lag) vs mood_bias@neutral=0.4357... (slow baseline retained)
--- D5 Mood engine-native: 6 pass / 0 fail ---
```

## disjointness 증명 (a_substrate_disjoint · placement-first)

기분 궤적을 immune store 위에서 50틱 굴린 뒤에도:
- **Ψ emit-drive (lane 0/4)** `ci_emit_drive` = 0.7 **byte-identical** (ON vs OFF).
- **§ImmuneMemory recall_thr** = 0.30 **불변**, `immune_grow_recall` 결과 non-fab 불변.
- 동시에 mood valence/arousal 는 실제로 **MOVED**(정서 stream 을 읽었다는 증거).

MoodState 는 자기 EMA 스칼라만 보유·mem/lane 를 절대 mutate 하지 않으므로 by-construction
분리 → 능력(느린 정서 baseline) ∧ Ψ=½ ∧ G5 non-fab 공존. **분리=보존.**

## 정직 scope (c9)

- EMA 는 **designed law**(학습된 것 아님) · **TOY smoke** — production-scale 거동·
  caller motivation-loop 배선 UNVERIFIED(follow-on ING).
- H_1284 neuromod-gain(🧱)과의 구분은 **시간축 분리**로 성립 — mood 는 gain 이 아니라
  느린 additive baseline. gain readout 는 0 lag/0 recovery 로 F1/F4 를 재현 못 함.
- bias helper 는 emit/silence 를 강제하지 않음(a_autonomy_over_hardcode) — 순간 emit 결정은
  여전히 substrate 소관.

## Sibling links

- `[[H_1290]]` (instantaneous affect — mood 는 이것의 느린 EMA) · `[[H_1292]]`
  (HomeostaticDrive — single-scalar setpoint+consummatory-reset, mood 는 2축·setpoint 없음) ·
  `[[H_1476]]` (EmotionRegulation — top-down 순간 reappraisal gain) · `[[H_1284]]`
  (neuromod-gain 🧱 — 다른 시간축, distinct).
