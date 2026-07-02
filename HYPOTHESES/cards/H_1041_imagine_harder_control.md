# H_1041 — Does imagine-rollout still beat MPC on a HARDER control task? (H_1034 generalization)

Status: PRE-REGISTERED (generation-only; not yet measured)
Lane: zero-cost CPU toy. g5 CODE-measured (a_phi_iit4_tool N/A — control-return metric).

## Hypothesis
H_1034 (prior GREEN) showed imagine-rollout (CEM/Dreamer through a learned world-model) still
beats a ROBUST (scenario/tube) MPC at deep horizon on a stiff double-integrator — the deep-MPC
failure was CEM landscape difficulty, not process-noise brittleness. That was ONE task (linear
stiff dynamics). This generalizes: does the imagine-beats-MPC advantage HOLD on a genuinely
harder control problem (nonlinear dynamics AND/OR partial observability)?

## Method (sketch)
- New environments: (a) a nonlinear swing-up / cart-pole-style task, (b) a partially-observed
  variant (state hidden, only noisy observations) requiring belief tracking.
- Same three planners as H_1034 (naive-MPC on true dynamics, robust tube-MPC, imagine-rollout
  through a learned WM), same depth ladder {1,2,4,8,16}, same return metric, >=30 seeds.

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = on the harder task(s), at deep horizon {8,16} imagine-rollout's mean return still
  leads the best MPC by > GAP_TOL = 0.05 (Welch p < 1e-3) -> the imagine advantage GENERALIZES
  beyond the stiff-linear H_1034 case.
- H1 FAIL = on a harder task the MPC baseline catches or beats imagine at deep horizon -> the
  H_1034 advantage was task-specific to stiff-linear CEM-landscape difficulty (honest scoped
  negative; the mechanism, not the headline, is what transfers). State GAP_TOL + the exact
  harder-task spec before running.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)
Toy single-rung per task; scenario-tube robustification only (min-max/CVaR UNVERIFIED);
scale-transfer UNVERIFIED. Bit-identical vectorized planners must reproduce H_1034 before scoring.

## Verdict
🔴 RED — IMAGINE-ADVANTAGE-IS-TASK-SPECIFIC (closed-negative, a_paper_negative_ok). Measured
2026-06-09, $0 CPU-local, 0 pods. Verdict gate: `.verdicts/1041_imagine_harder_control/H_1041.txt`.

reproduce-H_1034 = PASS (bit-identical): re-ran the H_1034 planners, curve matched the stored
verdict exactly (naive/robust/imag at d∈{1,2,4,8,16}) BEFORE scoring H_1041.

On BOTH genuinely harder tasks an MPC baseline CATCHES/BEATS imagine at deep horizon {8,16}
(lead = imagine − best-MPC; PASS needs lead > GAP_TOL=0.05 AND Welch p<1e-3 at d∈{8,16}):

| task | d=8 lead | d=16 lead | result |
|------|----------|-----------|--------|
| A — nonlinear pendulum swing-up (angle-only obs, ω hidden) | −0.8336 (p=1.7e-61) | −0.8883 (p=3.9e-58) | MPC beats imagine |
| B — partial-obs + obs-noise station-keeping (Kalman-belief MPC) | −29.29 (p=9.1e-76) | −22.93 (p=1.4e-69) | MPC beats imagine |

Task A is the clean, interpretable FAIL: both MPCs plan on the EXACT nonlinear true dynamics, while
imagine's learned WM is a LINEAR LDS that cannot capture the sin(θ) gravity term — so the MPC's
true-model advantage now matters and it leads by ≈0.8 at depth. Task B FAILs even harder (the linear
WM diverges under heavy observation noise while the MPCs get the optimal Kalman belief), reinforcing
the direction though that magnitude reflects WM breakdown more than a close contest.

Read: the H_1034 "imagine beats MPC at deep horizon" was SPECIFIC to stiff-LINEAR CEM-landscape
difficulty — where a noise-free deep CEM-MPC over-commits to a brittle plan but a smoother learned
LDS does not. When the true dynamics are nonlinear, or the optimal belief (Kalman) is available, a
true-model MPC reclaims the deep-horizon lead. The MECHANISM (robust / expected-return planning beats
a brittle noise-free landscape) transfers; the HEADLINE (imagine > MPC) does NOT generalize beyond the
stiff-linear toy. TOY single rung per task; scenario-tube + Kalman-belief variants only; scale-transfer
UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). a_phi_iit4_tool n/a.
