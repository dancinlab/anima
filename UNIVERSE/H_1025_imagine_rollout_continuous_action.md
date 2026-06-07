---
id: H_1025
slug: imagine-rollout-continuous-action
title: Does imagine-rollout (planning through anima's learned world-model) reach MPC parity on a CONTINUOUS-action control env, or does the discrete-action enumerator that worked in H_1021 fail to transfer to a continuous action space?
domain: cwm · world-model · imagine · planning · model-predictive-control · continuous-action · control · pre-register
source: H_1021 (imagine-rollout d4 reaches depth-4 MPC parity, p=0.26 — on a DISCRETE-action toy via a receding-horizon enumerator) — continuous-action generality untested
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric) — replace the discrete enumerator with a continuous-action planner (CEM / gradient / sampling-MPC) THROUGH anima's learned forward model; keep a continuous-action MPC as the optimum reference + reactive/random floors
verification_method: W2 (pre-registered placement falsifier · imagine-rollout vs continuous MPC band · ladder vs single-step) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1025 — imagine-rollout on continuous actions

## 0. motivation
H_1021 closed the human-bar gap via imagine-rollout, but on a DISCRETE action space where a
receding-horizon ENUMERATOR (4^4 rollouts) is feasible. Real embodied control is continuous; the
CWM @goal (act on silicon/SW) needs continuous-action planning through the learned model. Whether
planning-through-the-learned-WM still reaches the optimum when the action space is continuous (and
must be searched by CEM / gradient / sampling, not enumerated) is the next generality test.

## 1. hypothesis
On a continuous-action control env, imagine-rollout (a continuous-action planner THROUGH anima's
learned forward model) reaches the continuous-action MPC reference band — planning-through-the-
learned-model is not specific to enumerable discrete actions.

## 2. pre-registered falsifier (frozen 2026-06-07)
Build a continuous-action variant of the hidden-state control env (or adopt a standard toy LQG).
Reference = a continuous-action MPC (CEM/iLQR) on the TRUE dynamics. anima = the same learned
forward model planned with a continuous-action search. Multi-seed, $0 CPU (or GPU if the search is
heavy — a_fire_autonomous). Ladder: single-step head -> imagine-rollout -> MPC ceiling -> floors.
- PASS = CONTINUOUS-PARITY : imagine-rollout lands within the continuous MPC band (tolerance frozen).
- PARTIAL/FAIL = CONTINUOUS-GAP : imagine-rollout beats single-step but misses the band (search /
  forward-model error compounds in continuous space; closed-negative, a_paper_negative_ok).

## 3. honest scope
Toy single rung; the learned model is trained on the SAME demos (not given true dynamics). No Phi
claim (a_phi_iit4_tool n/a). Scale-transfer + real-robot UNVERIFIED (a_scale_honest_scope).

## 4. sibling / xlinks
to [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · [H_1019](./H_1019_human_bar_true_optimal.md) · CWM/CWM.md · cwm-control-imagine-rollout
