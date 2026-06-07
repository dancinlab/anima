---
id: H_1028
slug: wm-fidelity-at-scale
title: Does a larger / longer-trained learned world-model widen the imagine-rollout planning horizon (push h* out) and close any residual gap to a deep MPC — i.e. does WM forward-fidelity scale the reachable optimum?
domain: cwm · world-model · imagine · planning · model-fidelity · scaling · gpu · pre-register
source: H_1021 (parity was inference-DEPTH limited, NOT WM-quality limited, on the toy LDS model) + H_1027 (model-error-limited horizon h*) — whether INCREASING WM fidelity moves h* is the scaling question
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric) — train a ladder of learned WMs of increasing capacity / data / training; for each, measure imagine-rollout's reachable horizon h* (H_1027) and gap to a deep MPC
verification_method: W2 (pre-registered fidelity-vs-horizon falsifier · WM fidelity ladder x imagine-rollout horizon) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1028 — does WM forward-fidelity scale the reachable optimum?

## 0. motivation
H_1021 found the toy LDS world-model was ALREADY accurate enough to plan to a depth-4 optimum;
H_1027 posits a model-error-limited horizon $h^*$. The scaling question closes the loop: if we make
the learned WM more faithful (bigger / more data / longer training), does $h^*$ move out and the gap
to a DEEP MPC close? This is the bridge from the toy result to "bigger world-model = better
imagination" — and the natural GPU rung of the CWM control arc.

## 1. hypothesis
Imagine-rollout's reachable horizon $h^*$ (and the depth of optimum it can match) increases
monotonically with the learned model's measured multi-step forward fidelity — model fidelity, not
inference depth alone, sets the ceiling at scale.

## 2. pre-registered falsifier (frozen 2026-06-07)
Train a pre-frozen ladder of learned WMs (increasing capacity/data/epochs). For each, measure (a)
multi-step forward fidelity and (b) the imagine-rollout horizon $h^*$ + gap to a deep MPC (H_1027
protocol). Regress $h^*$ / optimum-depth on fidelity. GPU likely for the larger rungs
(a_fire_autonomous — state est. cost, dispatch).
- PASS = FIDELITY-SCALES-HORIZON : $h^*$ / matched-optimum-depth rises monotonically with WM fidelity.
- FAIL = FIDELITY-DOESNT-HELP : higher fidelity does not extend $h^*$ (the limit is the planner or the
  task, not the model; closed-negative, a_paper_negative_ok).

## 3. honest scope
Multi-rung; the largest rungs are GPU (a_fire_autonomous, no cost gate). No Phi claim
(a_phi_iit4_tool n/a). Toy-to-production transfer UNVERIFIED until a real env is used
(a_scale_honest_scope). Lane tag = Lane-P/G as appropriate.

## 4. sibling / xlinks
to [H_1027](./H_1027_imagine_rollout_depth_ladder.md) · [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · CWM/CWM.md · two-7b-lanes-distinction
