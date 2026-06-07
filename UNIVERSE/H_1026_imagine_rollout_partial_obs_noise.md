---
id: H_1026
slug: imagine-rollout-partial-obs-noise
title: Under partial observation PLUS observation noise, does planning through anima's learned world-model still match the MPC optimum, or does learned-model forward-error compound and break the H_1021 parity?
domain: cwm · world-model · imagine · planning · partial-observation · noise · robustness · control · pre-register
source: H_1021 (imagine-rollout reaches MPC parity on a noiseless hidden-velocity env) — the env hides velocity but observations are otherwise clean; real perception is noisy + partially observed
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric) — add observation noise + a deeper partial-observation horizon to the H_964-style env; the learned WM must filter/infer the hidden state from noisy history before planning
verification_method: W2 (pre-registered placement falsifier · imagine-rollout vs a noise-aware MPC/belief reference · ladder vs single-step) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1026 — imagine-rollout under partial-obs + noise

## 0. motivation
H_1021's parity was on a clean (noiseless) env that merely HID velocity. The CWM perceive step must
handle noisy, partially-observed input. Noise compounds through a learned forward model over a
planning horizon; the open question is whether anima's learned WM still recovers enough hidden
state to plan to the optimum, or whether forward-error accumulation breaks parity (and at what
noise level the break onsets).

## 1. hypothesis
With observation noise + partial observation, imagine-rollout through the learned WM still reaches
the noise-aware MPC/belief reference band up to a characterizable noise threshold; beyond it,
forward-model error compounds and parity degrades gracefully (not catastrophically).

## 2. pre-registered falsifier (frozen 2026-06-07)
Add a pre-frozen observation-noise sweep to the hidden-state env. Reference = a noise-aware MPC (or
a Kalman/belief-MPC) on the true dynamics+noise model. anima = the learned WM (must infer state
from noisy history) planned via imagine-rollout. Multi-seed.
- PASS = NOISE-ROBUST-PARITY : imagine-rollout stays within the reference band up to a stated noise
  level, and a monotone degradation curve (not a cliff) beyond it.
- FAIL = NOISE-BREAKS-PARITY : parity is lost even at low noise / degrades catastrophically (closed-
  negative, a_paper_negative_ok) — bounds H_1021 to noiseless control.

## 3. honest scope
Toy; learned model trained on demos, not given the true noise model. No Phi claim (a_phi_iit4_tool
n/a). Scale-transfer + real-sensor noise UNVERIFIED (a_scale_honest_scope).

## 4. sibling / xlinks
to [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · [H_1025](./H_1025_imagine_rollout_continuous_action.md) · CWM/CWM.md · cwm-control-imagine-rollout
