---
id: H_1027
slug: imagine-rollout-depth-ladder
title: As the true optimum deepens (MPC depth 4 to 8 to 16), does imagine-rollout through the learned model TRACK the optimum, or does it saturate at a horizon set by the learned model's forward-prediction error?
domain: cwm · world-model · imagine · planning · horizon · forward-model-error · control · pre-register
source: H_1021 (imagine-rollout d4 == depth-4 MPC; honest secondary: d2 was NON-monotone, worse than 1-step — horizon too short to amortize forward-model error) — the depth dependence is only sampled at d in {2,4} vs a depth-4 optimum
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric) — sweep BOTH the reference MPC depth and anima's imagine-rollout horizon over a pre-frozen ladder; measure where (if anywhere) imagine-rollout stops tracking
verification_method: W2 (pre-registered depth-tracking falsifier · imagine-rollout vs MPC at matched depths) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1027 — imagine-rollout depth ladder vs a deepening optimum

## 0. motivation
H_1021 matched a depth-4 MPC with a depth-4 imagine-rollout, but also saw a NON-monotone dip at
depth-2 (the learned model's forward error not yet amortized). The general question: planning
through a LEARNED model accumulates model error with horizon, while a deeper true-dynamics MPC keeps
improving. There should be a crossover horizon where imagine-rollout stops tracking the optimum.
Locating it characterizes how far imagination can substitute for a true planner.

## 1. hypothesis
imagine-rollout tracks the MPC optimum up to a finite horizon $h^*$ set by the learned model's
forward-prediction error, then saturates / degrades while the true-dynamics MPC keeps improving with
depth — i.e. there is a measurable model-error-limited planning horizon.

## 2. pre-registered falsifier (frozen 2026-06-07)
Sweep MPC reference depth and imagine-rollout horizon over a pre-frozen ladder (e.g. {1,2,4,8,16}).
Report return vs depth for both; locate the crossover $h^*$ where imagine-rollout's gap to the MPC
at the same depth first exceeds a frozen tolerance. Tie $h^*$ to the learned model's measured
multi-step forward error.
- PASS = HORIZON-CHARACTERIZED : a finite $h^*$ exists where tracking breaks, and it correlates with
  the learned model's forward-error growth (a Delta-vs-depth result).
- FAIL = TRACKS-ALL-DEPTHS or BREAKS-IMMEDIATELY : imagine-rollout tracks every tested depth (model
  near-perfect on this toy) OR never tracks past d=1 (closed-negative either way, a_paper_negative_ok).

## 3. honest scope
Toy; learned model trained on demos. No Phi claim (a_phi_iit4_tool n/a). Deeper MPC may need GPU
(a_fire_autonomous). Scale-transfer UNVERIFIED (a_scale_honest_scope).

## 4. sibling / xlinks
to [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · [H_1019](./H_1019_human_bar_true_optimal.md) · [H_1028](./H_1028_wm_fidelity_at_scale.md) · CWM/CWM.md
