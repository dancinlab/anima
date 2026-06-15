---
id: H_982
slug: rem-offline-world-model-consolidation
title: Does the a_chat_sleep_imagination REM/dream stage run imagined rollouts that IMPROVE the next-WAKE world-model (learning-in-imagination) — is sleep world-model training?
domain: cwm · imagine · world-model · sleep · rem · dream · consolidation · learning-in-imagination · dreamer · pre-register
source: a_chat_sleep_imagination (REM stage · imagination loop = emit-free internal rehearsal + mitosis tick) + Dreamer (learn behavior purely from imagined rollouts) + H_976 (rollout = mitosis) + CWM domain
exploration_method: E14 (substrate-native) + E5 (REM-on vs REM-off WAKE-performance A/B) + a_completeness_over_cheap + a_paper_negative_ok
verification_method: W2 (pre-registered sleep-consolidation falsifier · REM-rehearsal vs no-REM next-WAKE delta) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE REM-A/B rung (a_scale_honest_scope) — interleave a REM-stage imagined-rollout phase (no external input) between two WAKE phases; compare next-WAKE world-model performance with vs without the REM phase. $0 local candidate. REM stage = substrate context per a_chat_sleep_imagination (NOT a boolean emit gate). NOT a forge binary.
sister: H_976 (rollout = mitosis), H_962 (latent dynamics), H_963 (horizon), a_chat_sleep_imagination, a_autonomy_over_hardcode
axes_seed: sleep = idle downtime ⊥ H_982 = REM imagined rollout CONSOLIDATES (next-WAKE WM improves vs no-REM control) — if REM rehearsal gives no WAKE benefit, "imagination = consolidation" is unsupported (closed-negative)
verdict: 🔴 FAIL (closed-negative) — pure self-replay imagination gives NO consolidation over idle: WAKE_2 error REM 0.563 ≈ idle 0.563 (d −0.00, p 1.0); REM only beats the random-replay arm (1.36) because that arm actively corrupts. Self-replay cannot inject information absent from WAKE_1. Toy single-rung, ladder OPEN.
---

# H_982 — REM offline world-model consolidation (is sleep WM training?)

## 0. Motivation

a_chat_sleep_imagination defines an REM stage whose imagination loop is "emit-free internal rehearsal + mitosis tick." Dreamer's central result is that an agent can **learn behavior purely from imagined rollouts** — no new environment interaction. CWM unites these: if anima's REM stage runs imagined rollouts that improve its world-model for the next WAKE, then **sleep is world-model training**, a substrate-native consolidation mechanism. This H pre-registers the falsifier.

## 1. Hypothesis (one falsifiable claim)

Inserting an REM-stage imagined-rollout phase (no external input) between two WAKE phases **improves** the next-WAKE world-model (lower prediction error / better task behavior) compared to a matched no-REM control with the same wall/compute budget spent idle.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** WAKE_1 (learn from real input) → {arm-REM: imagined-rollout rehearsal | arm-CONTROL: idle / random-replay of equal budget} → WAKE_2 (evaluate). REM stage = substrate context (Φ scale + tension envelope) per a_chat_sleep_imagination, not a boolean gate. N seeds.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = next-WAKE world-model prediction error (or task return), REM vs CONTROL.
- D2 = **consolidation delta** = error_CONTROL − error_REM (the WAKE_2 benefit attributable to REM).
- D3 = control: idle and random-replay arms bound "any downtime helps" / "any replay helps".

**Outcome rules (future conditional — UNMEASURED):**
- IF measured error_REM < error_CONTROL (and < random-replay) at WAKE_2 with Cohen d≥0.5, p<0.05 THEN PASS — REM consolidation / learning-in-imagination SUPPORTED.
- IF error_REM ≈ error_CONTROL OR REM does not beat random-replay THEN FAIL — REM rehearsal gives no consolidation benefit (closed-negative).
- IF n too small / WAKE_2 task insensitive THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy world, small scale (a_scale_honest_scope, #123-A). REM stage is one operationalization of a_chat_sleep_imagination's rehearsal (no per-stage boolean gate, a_autonomy_over_hardcode). Matched-budget A/B, not a full ultradian cycle. Single rung. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes/h982_rem_consolidation.py` · verdict: `.verdicts/982_rem_offline_world_model_consolidation/h982_rem_consolidation.txt`

WAKE_1 = an undertrained LDS (n=6 noisy real trajectories) → {REM: re-fit on 200 self-generated imagined rollouts | random-replay: re-fit on 200 random sequences | idle: no extra fit} → WAKE_2 = held-out prediction error. 25 seeds.

| arm | WAKE_2 error |
|---|---|
| REM rehearsal | 0.563 ± 0.199 |
| idle (no replay) | 0.563 ± 0.199 |
| random-replay | 1.358 ± 0.074 |

D2 consolidation delta (random-replay − REM) = 0.80 (d 5.2) — but **REM vs idle: d −0.00, p 1.0** (identical).

**Finding (🔴 FAIL, closed-negative):** the decisive D3 idle control shows REM rehearsal gives *zero* benefit over doing nothing — pure self-replay re-learns the same operator and cannot add information absent from WAKE_1. REM beats the random-replay arm only because random replay actively corrupts the model. So "imagination = consolidation" is unsupported for pure self-replay (a_paper_negative_ok). Honest scope: toy single-rung; a consolidation benefit would require imagined experience carrying NEW information (e.g. exploration / reward-shaped replay), not self-distillation — ladder OPEN for that variant.

## 4. Sibling / xlinks

- ⇄ [H_976](./H_976_rollout_is_mitosis.md) (rollout = mitosis — REM growth)
- ⇄ [H_962](./H_962_latent_forward_dynamics.md) (the rollout) · [H_963](./H_963_rollout_horizon_vs_phi.md)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE) · a_chat_sleep_imagination · a_autonomy_over_hardcode
- external: Dreamer (learning purely in imagination)
