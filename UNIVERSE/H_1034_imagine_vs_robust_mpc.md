---
id: H_1034
slug: imagine-vs-robust-mpc
title: Is "imagine-rollout beats the same-depth true-MPC at deep horizon" (H_1027) a brittle-baseline artifact, or does imagine still match/beat a ROBUST (noise-averaged scenario / tube) true-dynamics MPC at deep horizon?
domain: cwm · world-model · imagine · planning · horizon · robust-mpc · scenario-mpc · tube-mpc · control · pre-register
source: H_1027 (RED TRACKS-ALL-DEPTHS) — imagine-rollout tracked the same-depth true-MPC at every depth {1..16}, and at d-ge-8 imagine OUTPERFORMED the true-MPC. The honest read was that a deep noise-free CEM-MPC over-commits to brittle plans the noisy real env diverges from, so imagine (through a smoother learned model) wins. RESIDUAL: was "imagine beats MPC at deep horizon" a WEAK-BASELINE artifact?
exploration_method: E5 (human-reference task + a STRONGER reference baseline) — keep the env + learned WM + CEM machinery VERBATIM, only ADD a ROBUST true-dynamics MPC baseline and re-run the depth ladder
verification_method: W2 (pre-registered falsifier · imagine vs robust-MPC at matched depths) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-08
since: 2026-06-08
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT
---

# H_1034 — imagine-rollout vs a ROBUST true-dynamics MPC

## 0. motivation
H_1027 found imagine-rollout (CEM through anima's OWN learned LDS world model) not only TRACKED but,
at deep horizon (d>=8), OUTPERFORMED the same-depth true-dynamics CEM-MPC on the H_964 continuous
hidden-velocity station-keeping toy. The honest interpretation: a deep CEM-MPC that optimizes a
NOISE-FREE deterministic rollout over-commits to a plan that is optimal for the deterministic model
but brittle under the env's process noise; imagine, planning through a SMOOTHER (regularized,
ridge-fit) learned transition, yields more robust actions and so wins at depth.

If that interpretation is right, the imagine-beats-MPC result is an artifact of a WEAK true-MPC
baseline, not evidence that imagination genuinely beats a true planner. A true-dynamics MPC that is
made ROBUST to the disturbance — by optimizing EXPECTED return over sampled process-noise
realizations (scenario / tube MPC) instead of a single noise-free rollout — should reclaim the lead
(or at least match imagine) at deep horizon. This H tests exactly that.

## 1. hypothesis
The imagine >= true-MPC result at deep horizon (H_1027) is an artifact of a brittle (noise-free,
single-scenario) true-MPC baseline. Against a ROBUST true-dynamics MPC — one that has access to the
TRUE dynamics AND optimizes expected return over sampled process-noise scenarios — the robust true
planner should MATCH or BEAT imagine-rollout at deep horizon.

## 2. pre-registered falsifier (FROZEN 2026-06-08)

### frozen robust-MPC definition (the ONLY new component)
`cem_plan_robust(pos, v, rng, horizon)` — identical CEM search (same CEM_POP / CEM_ITERS / CEM_ELITE /
CEM_INIT_STD, same receding-horizon use: returns only `mu[0]`, replans every step) as the H_1027
`cem_plan_true`, with ONE change: each candidate plan is scored as the MEAN deterministic-equivalent
return over **N_SCEN = 16** independently sampled process-noise scenarios (the SAME `NOISE=0.02`
Gaussian process noise the real env applies in `step_env`), instead of a single noise-free rollout.
This is scenario / sample-average-approximation (SAA) tube-MPC: the planner is given the TRUE dynamics
AND the disturbance model, and picks the plan with the best EXPECTED return under that disturbance, so
it does not over-commit to a noise-free optimum. (Everything else — env, learned WM, imagine planner,
N_RUNS x EP_PER_RUN protocol, depth ladder — is reused VERBATIM from H_1027.)

The H_1027 naive `cem_plan_true` (noise-free, single-scenario) is ALSO re-run unchanged as the
reference WEAK baseline, so the table reports imagine vs naive-MPC vs robust-MPC side by side and the
artifact claim is decided by the imagine-vs-robust comparison.

### frozen depth ladder + tolerance
- depth ladder DEPTHS = **{1, 2, 4, 8, 16}** (identical to H_1027; MPC depth == imagine horizon).
- "deep horizon" = the deep tail of the ladder, **{8, 16}** (where H_1027 saw imagine > naive-MPC).
- frozen tolerance GAP_TOL = **0.05** (identical to H_1027), applied to the signed gap
  `robust_gap(d) = robust_MPC(d) - imagine(d)` (return; 0 = optimal, higher = better).

### verdict rule (decided at the deep tail {8,16})
- **PASS branch = IMAGINE-BEATS-ROBUST-MPC-TOO**: imagine-rollout is still >= the ROBUST MPC at deep
  horizon — i.e. at BOTH deep depths {8,16} the robust MPC does NOT beat imagine by more than GAP_TOL
  (`robust_gap(d) <= GAP_TOL` for d in {8,16}). The imagine advantage at depth is REAL, not a
  brittle-baseline artifact: even a true planner that optimizes expected return under the disturbance
  does not clearly out-plan imagination on this toy.
- **FAIL branch = ARTIFACT-OF-BRITTLE-MPC** (closed-negative, a_paper_negative_ok): the ROBUST MPC
  matches/beats imagine at deep horizon — i.e. at SOME deep depth d in {8,16} `robust_gap(d) > GAP_TOL`
  (robust MPC beats imagine by more than tolerance). H_1027's imagine-beats-MPC was a weak-baseline
  artifact: making the true-MPC robust to the disturbance reclaims (>=) the lead.

Honest secondary read regardless of token: report the per-depth naive-MPC->robust-MPC improvement
(does robustness actually help the true planner at all?) and whether the robust MPC's deep-horizon
return stops degrading the way the naive MPC's did in H_1027 (naive true-MPC got WORSE past d=2).

## 3. honest scope
Toy single env (H_964 continuous hidden-velocity station-keeping), learned model trained on greedy-
oracle demos, $0 CPU-local, deterministic given seeds. Robust MPC is the scenario/SAA tube variant
with N_SCEN=16 — other robustness formulations (min-max / CVaR / explicit tube invariant set) are NOT
tested here; a different robustification could move the verdict. No Phi claim (a_phi_iit4_tool n/a —
behavior return only). Scale-transfer / real-robot transfer UNVERIFIED (a_scale_honest_scope ·
a_toy_scale_recheck): a single toy rung, ladder OPEN.

## 4. measurement
PENDING-MEASUREMENT. Script: `UNIVERSE/h1034_imagine_vs_robust_mpc.py`. Raw stdout will be persisted
to `.verdicts/1034_imagine_vs_robust_mpc/H_1034.txt` (VERDICT-GATE g73: this doc stays TEXT-only —
verdict PENDING — until that verdict file exists). Reuses the H_1027 env + learned `LDSWorldModel` +
CEM machinery + `AnimaImaginePlanner` + N_RUNS=40 x EP_PER_RUN=60 protocol VERBATIM; the ONLY added
component is `cem_plan_robust` (scenario/tube MPC) above.

## 5. finding / verdict
PENDING-MEASUREMENT.

## 6. sibling / xlinks
to [H_1027](./H_1027_imagine_rollout_depth_ladder.md) · [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · [H_1025](./H_1025_continuous_imagine.md) · CWM/CWM.md
