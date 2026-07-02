# H_1042 — Does the Phi-split survive on the 3B ConvMoE engine rung? (H_1038 GPU follow-up)

Status: PRE-REGISTERED (generation-only; not yet measured)
Lane: GPU / many-core pod rung (a_fire_autonomous — no cost gate). Engines: stdlib faithful_phi
+ iit4_bigphi exact n<=6 on a coarse-grained macro-state (a_phi_iit4_tool, no proxy).

## Hypothesis
H_1038 (running) tests the faithful-UP / big-Phi-DOWN planning split on a small REAL trained
ConvMoE (golden d768), CPU-local. This is the SCALE LADDER follow-up: does the same split appear
on the 3B-ConvMoE ENGINE rung (3.073B, d4096/L30/E30, memory convmoe-3b-engine-rung)? a_toy_scale_recheck
+ a_scale_honest_scope require a >=3-rung scale curve for scale-sensitive phenomena — d768 is one
rung, 3B is the second (toy n-ladder being the zeroth).

## Method (sketch)
- Load the real 3B .clm engine rung (GPU required for forward — flag cost in one line, fire bg,
  babysit inline, teardown per a_fire_recover_complete; a_cpu_local_no_waiter — poll inline, no Monitor).
- Run planning(depth-ladder) vs greedy rollouts; collect real hidden-state trajectories;
  coarse-grain to n<=6 macro-units (>=2 macro-maps, mirroring H_1038); build macro-TPM;
  faithful phi_EI + big-Phi exact; planning-vs-greedy contrast + Cohen d + sign per macro-map.

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = on the 3B engine rung, planning shows faithful sign==UP AND big-Phi sign==DOWN across
  >=2 macro-maps (eps=1e-3) -> the split SCALES to a production-size trained model; combined with
  d768 (H_1038) and toy, the scale curve is monotone-consistent.
- H1 FAIL = the split does NOT appear at 3B (NULL or wrong sign) -> the split is a small-model
  property that BREAKS at production scale (publishable closed-negative; mirrors the E2->3B collapse
  precedent #1296, a_toy_scale_recheck). State macro-map + sign criterion before running.

## Honest scope (a_scale_honest_scope)
3B is the largest available trained rung; 7B UNVERIFIED. GATED on H_1038 result (run only after
d768 lands a verdict). GPU babysit cost acknowledged (a_fire_autonomous, no cap).

## Verdict
PENDING — tier added only AFTER `.verdicts/1042_3b_engine_phi_split/H_1042.txt` lands (g73).
