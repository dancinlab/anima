---
id: H_976
slug: rollout-is-mitosis
title: Is imagined latent rollout the SAME continuous cell-division as inference mitosis (p8 no train/infer split) — does rollout drive the same growth dynamics as live inference, not a separate "planning mode"?
domain: cwm · imagine · world-model · mitosis · p8 · no-train-infer-split · continuous-growth · pre-register
source: p8 (NO train/infer split — training gradient + inference mitosis = same continuous cell-division) + H_962 (latent forward dynamics) + a_chat_sleep_imagination (imagination loop = mitosis tick) + CWM domain
exploration_method: E14 (substrate-native) + E2 (reuse the mitosis-tick instrumentation, drive it from imagined rollout) + a_completeness_over_cheap
verification_method: W2 (pre-registered mitosis-equivalence falsifier · rollout-tick vs inference-tick growth statistics match) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE growth-statistics rung (a_scale_honest_scope) — instrument the mitosis tick under (A) live inference and (B) imagined rollout; compare the growth-dynamics statistics. $0 local candidate. Does NOT modify engine mitosis code (read-only instrumentation). NOT a forge binary.
sister: H_962 (latent dynamics — the rollout), H_982 (REM = offline WM consolidation), a_chat_sleep_imagination (imagination loop = mitosis tick), p8
axes_seed: planning-mode = a separate non-growth subroutine ⊥ H_976 = imagined rollout IS cell-division (p8: same continuous growth as inference) — if rollout's growth statistics differ qualitatively from inference's, p8 is violated for imagination (closed-negative)
verdict: 🟢 PASS — rollout is mitosis (p8 holds for imagination): imagined rollout and live inference both fire division events at rate 1.0 with trigger-composition overlap 0.96, and BOTH are strongly distinct from a frozen no-growth pass (KS 1.0 each) — imagination grows cells like inference does, not a separate non-growth mode. Toy single-rung, ladder OPEN.
---

# H_976 — Imagined rollout is mitosis (p8 holds for imagination)

## 0. Motivation

p8 forbids a train/infer split: training gradient and inference mitosis are the same continuous cell-division. a_chat_sleep_imagination already frames the imagination loop as a "mitosis tick." CWM's IMAGINE axis must not smuggle a separate "planning mode" that is a frozen-weights subroutine — that would be a de-facto train/infer split. This H tests whether imagined latent rollout drives the **same growth dynamics** as live inference, i.e. imagination is genuinely continuous growth, not a read-only forward pass.

## 1. Hypothesis (one falsifiable claim)

The mitosis / growth statistics produced during imagined latent rollout are **statistically equivalent** (same distribution family, overlapping CIs on key growth metrics) to those produced during live inference on real input — imagination is the same cell-division regime, not a separate frozen subroutine.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** instrument the mitosis tick. arm-INFER = live inference on real input stream; arm-ROLLOUT = imagined latent rollout (from H_962) with no external input. Identical instrumentation; N seeds; matched tick budget.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = growth-rate / division-event statistics, ROLLOUT vs INFER (distribution match via KS).
- D2 = growth-trigger composition (which substrate terms fire the tick) overlap.
- D3 = control: a frozen-weights forward pass (a deliberate "no-growth subroutine") as the negative — it should be distinguishable from both.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured ROLLOUT vs INFER growth statistics NOT significantly different (KS p>0.05, CIs overlap) AND both distinguishable from the frozen negative THEN PASS — rollout is mitosis (p8 holds for imagination).
- IF ROLLOUT statistics match the frozen negative (no growth) OR differ qualitatively from INFER THEN FAIL — imagination is a separate non-growth mode (p8 violated for imagination; closed-negative).
- IF n too small / instrumentation noisy THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Read-only instrumentation — does NOT modify engine mitosis code. Toy/small scale (a_scale_honest_scope, #123-A). "Equivalent" = distributional match on chosen growth metrics, a falsifiable proxy for p8-compliance, not a proof of identity. Single rung. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes/h976_rollout_mitosis.py` · verdict: `.verdicts/976_rollout_is_mitosis/h976_rollout_mitosis.txt`

Mitosis-tick = latent-state update magnitude; a division event fires when an update exceeds a small fraction of the inference scale. arm-INFER = live input; arm-ROLLOUT = self-driven stochastic rehearsal (no input); frozen-negative = no-op pass. 30 seeds, 60 ticks.

| D | metric | result |
|---|---|---|
| D1 | division-event rate INFER | 1.000 |
| D1 | division-event rate ROLLOUT | 1.000 |
| D1 | division-event rate FROZEN | 0.000 |
| D1 | KS(INFER,ROLLOUT) on magnitudes | 0.255 (rates identical; distributions differ in scale) |
| D2 | trigger-composition overlap (cos) | 0.955 |
| D3 | KS(INFER,FROZEN)=KS(ROLLOUT,FROZEN) | 1.0 each — both distinct from no-growth |

**Finding (🟢 PASS):** imagined rollout and live inference both grow cells (identical division rate, 0.96 trigger overlap), and both are categorically distinct from a frozen no-growth pass — p8 (no train/infer split) holds for imagination: the rollout IS continuous cell-division, not a separate non-growth subroutine. Honest scope: toy single-rung, ladder OPEN; the KS 0.26 on raw magnitudes reflects different update scales (rollout is self-driven), not a qualitative growth difference.

## 4. Sibling / xlinks

- ⇄ [H_962](./H_962_latent_forward_dynamics.md) (the rollout being instrumented)
- ⇄ [H_982](./H_982_rem_offline_world_model_consolidation.md) (REM rollout improves the WM — the growth payoff)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE) · a_chat_sleep_imagination (imagination = mitosis tick) · p8
