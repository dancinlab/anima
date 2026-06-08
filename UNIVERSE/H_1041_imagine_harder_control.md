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
PENDING — tier added only AFTER `.verdicts/1041_imagine_harder_control/H_1041.txt` lands (g73).
