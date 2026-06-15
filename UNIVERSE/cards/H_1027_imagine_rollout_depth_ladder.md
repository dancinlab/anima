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
status: measured
verdict: 🔴 RED — TRACKS-ALL-DEPTHS (closed-negative, a_paper_negative_ok). On the H_964 continuous-action hidden-velocity station-keeping toy, imagine-rollout (CEM through anima's OWN LEARNED LDS world model) tracks the same-depth true-dynamics CEM-MPC at EVERY tested depth on the FROZEN ladder {1,2,4,8,16}: the pre-registered gap MPC(d)-imagine(d) never exceeds GAP_TOL=0.05 (max gap +0.0075 @ d=1), so NO finite crossover horizon h* exists — the FAIL/TRACKS-ALL-DEPTHS branch by the frozen rule. The learned model's k-step OPEN-LOOP forward error DOES grow monotonically with horizon (k=1->16: 0.0349->0.3299) and correlates PERFECTLY with the gap over the ladder (Spearman r=-1.0000, p=1.4e-24), but that growth never breaks closed-loop depth-tracking. Striking honest detail: at DEEP horizons the gap goes NEGATIVE (d=8 -0.0322 p=8.4e-6 d=+1.07; d=16 -0.1140 p=2.9e-15 d=+2.27) — imagine-rollout OUTPERFORMS the same-depth true-MPC because the deep noise-free true-CEM-MPC over-commits to long open-loop plans the noisy real env does not follow, while planning through the smoother learned model yields more robust receding-horizon actions. The "deepening optimum" premise itself fails on this env: the true-MPC return gets WORSE past d=2 (d=2 -0.2623 -> d=16 -0.8746), it does not keep improving. Net: imagination substitutes for (and beyond d=4 beats) the true planner across the whole tested range; the model-error-limited planning horizon predicted by H_1027 is NOT exposed on this toy. TOY single rung, $0 CPU-local; a deeper ladder / harder/lower-noise env may yet expose h* (a_scale_honest_scope · a_toy_scale_recheck). g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool n/a (behavior return + forward error, no Phi claim). Verdict file: .verdicts/1027_imagine_rollout_depth_ladder/H_1027.txt
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

## 4. measurement (2026-06-07)
Reused the H_1025 continuous-action machinery VERBATIM (H_964 hidden-velocity station-keeping
env, the LEARNED `LDSWorldModel(delay=3, act_dim=2)` fitted by ridge on greedy-oracle demos —
NEVER given the true dynamics, the CEM continuous-action planner, and the N_RUNS=40 ×
EP_PER_RUN=60 protocol). The CEM planner (not the H_1021 NACT^d enumerator) was used because it
scales LINEARLY in horizon — the discrete enumerator would be 4^16 ≈ 4e9 leaves at d=16. HORIZON
was swept over the frozen ladder for BOTH the true-MPC ceiling and the imagine-rollout; the
learned model's k-step open-loop forward error was measured along the same ladder. Script:
`UNIVERSE/h1027_imagine_rollout_depth_ladder.py`. Raw stdout:
`.verdicts/1027_imagine_rollout_depth_ladder/H_1027.txt`.

### depth ladder (MPC depth == imagine horizon, swept together)
| depth d | true-MPC M (CI) | imagine-rollout M (CI) | gap = MPC−imag | Welch p / Cohen d | tracks @ GAP_TOL=0.05 |
|---|---|---|---|---|---|
| 1  | -0.3715 [-0.3896,-0.3532] | -0.3790 [-0.3962,-0.3623] | **+0.0075** | p=5.6e-01 d=-0.131 | TRACKS |
| 2  | -0.2623 [-0.2729,-0.2512] | -0.2684 [-0.2768,-0.2604] | **+0.0061** | p=4.0e-01 d=-0.191 | TRACKS |
| 4  | -0.3205 [-0.3288,-0.3120] | -0.3167 [-0.3252,-0.3084] | **-0.0038** | p=5.3e-01 d=+0.140 | TRACKS |
| 8  | -0.4847 [-0.4941,-0.4755] | -0.4526 [-0.4613,-0.4434] | **-0.0322** | p=8.4e-06 d=+1.067 | TRACKS (imagine ABOVE MPC) |
| 16 | -0.8746 [-0.8924,-0.8562] | -0.7606 [-0.7729,-0.7483] | **-0.1140** | p=2.9e-15 d=+2.265 | TRACKS (imagine ABOVE MPC) |

### learned-model k-step open-loop forward error (model-error axis)
| k | ‖pred pos − true pos‖ |
|---|---|
| 1  | 0.0349 |
| 2  | 0.0613 |
| 4  | 0.1096 |
| 8  | 0.2024 |
| 16 | 0.3299 |

- **h*: NOT FOUND** — the gap MPC(d)−imagine(d) never exceeds GAP_TOL=0.05 on the tested ladder
  (max gap +0.0075 @ d=1). By the frozen rule this is the FAIL / TRACKS-ALL-DEPTHS branch.
- **gap ↔ forward-error correlation:** Spearman **r=-1.0000** (p=1.4e-24) over the ladder. The
  forward error grows monotonically (0.0349→0.3299) and the gap declines monotonically (more
  negative) in lock-step, so the model-error growth IS measurable and IS tied to the gap — but
  the gap declines (imagine pulls AHEAD), it does not blow up, so tracking never breaks.
- **honest secondary finding (premise failure):** the "deepening optimum" never materializes on
  this env. The TRUE-MPC return is best at d=2 (-0.2623) and gets steadily WORSE with deeper
  horizons (d=16 -0.8746). A noise-free deep CEM-MPC over-commits to a long open-loop plan that
  the noisy real env diverges from; imagine-rollout, planning through the SMOOTHER learned model,
  produces more robust receding-horizon actions and so beats the same-depth true-MPC past d=4.

## 5. finding / verdict
**🔴 RED — TRACKS-ALL-DEPTHS (closed-negative, a_paper_negative_ok).** Imagine-rollout (CEM
through anima's OWN learned LDS world model) tracks the same-depth true-dynamics CEM-MPC at
EVERY tested depth on the frozen ladder {1,2,4,8,16}; the pre-registered gap never exceeds
GAP_TOL=0.05, so NO finite crossover horizon h* exists on this toy. The model-error-limited
planning horizon predicted by H_1027 is NOT exposed here: although the learned model's k-step
forward error grows monotonically (0.0349→0.3299) and correlates perfectly with the gap
(r=-1.0), it stays small enough that planning through the learned model never falls behind — and
beyond d=4 it OUTPERFORMS the same-depth true-MPC, because a deep noise-free true-CEM-MPC
over-commits to brittle long open-loop plans while the smoother learned model yields more robust
plans under process noise. The "optimum keeps deepening" premise itself fails on this env (true
MPC degrades past d=2). Δ-vs-H_1021: H_1021 sampled only d∈{2,4} and reported depth-4 parity;
the full {1..16} ladder shows imagine-rollout not merely matching but eventually exceeding the
true planner, with no model-error crossover in range. This is a clean closed-negative against the
pre-registered h* hypothesis. TOY single rung, $0 CPU-local; a deeper ladder / a lower-noise or
harder env (where the deep MPC genuinely keeps improving) may yet expose h* — OPEN
(a_scale_honest_scope · a_toy_scale_recheck). g5 CODE-measured (no LLM self-judge, p7).
a_phi_iit4_tool n/a (behavior return + forward error, no Φ claim).

## 6. sibling / xlinks
to [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · [H_1019](./H_1019_human_bar_true_optimal.md) · [H_1028](./H_1028_wm_fidelity_at_scale.md) · CWM/CWM.md
