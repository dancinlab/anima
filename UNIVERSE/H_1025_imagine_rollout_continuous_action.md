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
status: measured
verdict: 🟢 CONTINUOUS-PARITY (PASS) — imagine-rollout (CEM through anima's LEARNED world-model) lands WITHIN the continuous-action CEM-MPC band
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

## 4. measurement (2026-06-07 · g5 CODE-measured · CPU-mirror numpy · $0 · no GPU)
Script `UNIVERSE/h1025_imagine_rollout_continuous_action.py` · raw stdout
`.verdicts/1025_imagine_rollout_continuous_action/H_1025.txt`. Continuous variant of the H_964
hidden-velocity station-keeping env: observation = position (2-D), velocity HIDDEN; action =
CONTINUOUS 2-D thrust vector in [-1,1]^2; reward = -||pos|| (stay near origin). anima's LEARNED
forward model = LDSWorldModel(delay=3, act_dim=2) fitted by ridge on greedy-oracle demos (NEVER
given true dynamics). imagine-rollout = CEM (pop=64, iters=5, elite=8, horizon=4) THROUGH the
learned model — the continuous analogue of H_1021's 4^d enumerator. Reference ceiling = the SAME
CEM run over the TRUE dynamics. N=40 runs × 60 episodes/run. Pre-registered TOL=0.05.

Ladder (mean ± std, bootstrap CI; metric M = mean return, 0 = optimal):

| arm | M | CI |
|---|---|---|
| CEM-MPC horizon=4 (CEILING, true dyn) | **-0.3196** | [-0.3277, -0.3114] |
| anima imagine-rollout (CEM, **learned WM**) | **-0.3144** | [-0.3222, -0.3062] |
| anima single-step head (latent→action) | -0.3949 | [-0.4028, -0.3873] |
| continuous greedy 1-step oracle | -0.3602 | [-0.3725, -0.3475] |
| reactive (obs→action, floor) | -1.7436 | [-1.7815, -1.7054] |
| random (floor) | -7.4668 | [-7.6143, -7.3190] |

Parity band [P-TOL, P+TOL] = **[-0.3696, -0.2696]** (P=-0.3196, TOL=0.05).
- D1 non-vacuity: reactive CI_hi -1.7054 < band_lo -0.3696 ✓ (band is hard to reach).
- D2 strong reference: MPC -0.3196 ≥ continuous greedy 1-step -0.3602 ✓ (real ceiling).
- D3 search genuine: imagine vs single-step head Welch p=9.78e-23, d=3.10 ✓ (CEM is doing real work).

## 5. finding — 🟢 CONTINUOUS-PARITY (PASS)
imagine-rollout reaches **M=-0.3144, INSIDE the continuous CEM-MPC parity band [-0.370, -0.270]**
(CI [-0.322, -0.306] overlaps the band; MPC-imagine gap = -0.0052, i.e. imagine even edged the
true-dynamics MPC by a hair, well within noise: Welch p=0.39, d=0.20). It IMPROVES over the
single-step head by **+0.0805** (p=9.8e-23, d=3.10).

The pre-registered PASS condition (imagine-rollout within the continuous MPC band) is met:
**planning-THROUGH-the-learned-model is NOT specific to enumerable discrete actions.** A
continuous-action CEM search through anima's OWN learned LDS world-model recovers near-optimal
control on a continuous-action env, generalizing the H_1021 discrete result. The CONTINUOUS-GAP
falsifier (search / forward-model error compounding in continuous space) is REJECTED: the learned
model is faithful enough (1-step decode sanity: true pos [-0.014,-0.025] vs pred [0.020,0.024])
that CEM through it tracks the true-dynamics MPC.

Honest scope (a_scale_honest_scope): TOY single rung — 2-D point-mass, delay-3 LDS WM, horizon-4
CEM, $0 CPU; scale-transfer + real-robot UNVERIFIED. No Φ claim (a_phi_iit4_tool n/a). The MPC
and imagine planners share the SAME CEM hyperparameters, so the only difference is the model
(true vs learned) — a clean isolation of forward-model fidelity.

## 6. sibling / xlinks
to [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · [H_1019](./H_1019_human_bar_true_optimal.md) · CWM/CWM.md · cwm-control-imagine-rollout
