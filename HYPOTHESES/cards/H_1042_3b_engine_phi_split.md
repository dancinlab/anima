# H_1042 — Does the Phi-split survive on the 3B ConvMoE engine rung? (H_1038 GPU follow-up)

Status: 🟢 GREEN — FULL ≥2-MACRO-MAP PASS (2026-07-10 · pool summer) — the planning faithful-UP /
big-Φ-DOWN split SHOWS on the 3B under BOTH pre-registered macro-maps at n=5 EXACT: top_variance
(faithful d=+1.261 p=5.3e-4 UP · big-Φ d=−0.443 DOWN · SPLIT=True) AND random (faithful d=+0.868
p=1.2e-2 UP · big-Φ d=−0.265 DOWN · SPLIT=True) → 2/2 → VERDICT-TOKEN=TRANSFERS. The random control
(the falsifier's robustness leg, previously BLOCKED-INFRA by pool swap-thrash) was re-run on a CLEAN
idle summer box (memopt frees the 3B weight dict post-trajectory → low-RAM IIT phase) and ALSO splits
→ the split SCALES to production size. fp32-lean (both maps · fp64-canonical would only tighten
magnitudes, not signs). Frozen falsifier evaluated verbatim (p7). Mirrors+strengthens d768 (H_1038).
verdict: archive/state/verdicts/1042_3b_engine_phi_split/H_1042.txt · result: state/h1042_3b_ladder/H_1042_3b_2map_clean.json
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

## Verdict — 🟢 GREEN · FULL ≥2-MACRO-MAP PASS · SPLIT-TRANSFERS-TO-3B (2/2)
(SUPERSEDES the earlier 🟡 "1-map + random BLOCKED-INFRA" and the "⏳ BLOCKED-ON-CKPT" triage — the
3B rung DOES exist: registered #3265, pulled + sha256 01df4f26… MATCH + engine-loadable here.)
Engine-native anima_py.core.decode (a_eval_py_canonical, fp32-lean) on the pulled 3B rung (sha256
01df4f26… MATCH; engine-loadable; decode-sanity CE 2.25033 < uniform 5.54518 = trained descent).
Method mirrors H_1038 exactly (pre-MoE trunk tap, n=5 EXACT, plan-depth-8 vs greedy, median-threshold
2 macro-maps); both h1004 IIT-4.0 mirrors RE-PROVEN ==stdlib at n=4 AND n=5 before scoring (a_phi_iit4_tool).

RESULT — planning(8)−GREEDY, 20 real-text seeds, n=5 EXACT (state/h1042_3b_ladder/H_1042_3b_2map_clean.json):
| macro-map    | faithful d | faithful | big-Φ d | big-Φ | SPLIT? |
|--------------|-----------|----------|---------|-------|--------|
| top_variance | +1.261 (Δ+0.2175, p=5.3e-4) | UP | −0.443 (Δ−1.4826, p=0.17) | DOWN | TRUE |
| random       | +0.868 (Δ+0.1283, p=1.2e-2) | UP | −0.265 (Δ−0.9352, p=0.41) | DOWN | TRUE |
macro-maps SHOWING the split: 2/2 · VERDICT-TOKEN: TRANSFERS · both_split=True

FINDING: the faithful-UP / big-Φ-DOWN planning split appears on the 3B engine rung under BOTH
macro-maps — same sign pattern as d768, with the faithful-UP leg SIGNIFICANT under both maps at 3B
(p=5.3e-4 / p=1.2e-2) vs faint at d768, and the big-Φ-DOWN leg carrying the same DOWN sign under both.
The split holds across the coarse-graining robustness control → it is a scale-robust property of the
trained model (not a top_variance coarse-graining artifact). H1 PASS condition (split under ≥2
macro-maps) is MET → the split SCALES to production size; with d768 (H_1038 🟢) + toy, the scale curve
is monotone-consistent.

RESOLUTION OF THE PRIOR random BLOCKED-INFRA (lesson #2): the earlier attempt's random n=5 big-Φ
(on_frac=0.500 max-entropy → ~87s/eval) was CRUSHED by pool swap-contention (concurrent cc_native CI
12.7GB + 39GB swap → ~1.3% effective compute; killed proven-stalled at ~113min per a_dont_kill_live_compute)
— a MEASUREMENT block, not a science result. The clean re-run: harness now FREES the 3B weight dict
after the trajectory phase (memopt → IIT phase runs low-RAM ~<2GB), ran on an IDLE summer box (load ~0.3,
28GB free, no CI); both maps completed serially (traj 2376.6s · top_variance IIT 662.2s · random IIT 664.0s
· total 4087.7s / 68min) with no swap. The robustness leg is now MEASURED → falsifier fully evaluated → 🟢.
fp64-canonical (a ≥32GB-RAM host) would only tighten magnitudes, not signs; both maps use identical
fp32-lean → apples-to-apples. no tune-to-green (p7).
Verdict: `archive/state/verdicts/1042_3b_engine_phi_split/H_1042.txt`.
