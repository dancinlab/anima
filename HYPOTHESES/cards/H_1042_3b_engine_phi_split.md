# H_1042 — Does the Phi-split survive on the 3B ConvMoE engine rung? (H_1038 GPU follow-up)

Status: 🟡 DIRECTIONAL (2026-07-10 · pool summer) — the planning faithful-UP / big-Φ-DOWN split
SHOWS on the 3B under the top_variance macro-map (faithful d=+1.261 p=5.3e-4 UP · big-Φ d=−0.443 DOWN
· SPLIT=True), mirroring + strengthening d768 (H_1038). random macro-map (robustness control) =
BLOCKED-INFRA (pool swap-thrash, NOT a science ceiling). fp32-lean (canonical fp64 RAM-ceiling-blocked).
verdict: archive/state/verdicts/1042_3b_engine_phi_split/H_1042.txt
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

## Verdict — 🟡 DIRECTIONAL · SPLIT-SHOWN-1MAP (top_variance) · 2nd-map robustness BLOCKED-INFRA
(SUPERSEDES the earlier "⏳ BLOCKED-ON-CKPT / 3B does-not-exist" triage — the 3B rung DOES exist:
registered #3265 `anima-clm-convmoe-3b-rung`, pulled + sha256 01df4f26… MATCH + engine-loadable here.)
Engine-native anima_py.core.decode (a_eval_py_canonical, fp32-lean) on the pulled 3B rung (sha256
01df4f26… MATCH; engine-loadable; decode-sanity CE 2.25033 < uniform 5.54518 = trained descent).
Method mirrors H_1038 exactly (pre-MoE trunk tap, n=5 EXACT, plan-depth-8 vs greedy, median-threshold
2 macro-maps); both h1004 IIT-4.0 mirrors RE-PROVEN ==stdlib at n=4 AND n=5 before scoring (a_phi_iit4_tool).

RESULT — planning(8)−GREEDY, 20 real-text seeds, n=5 EXACT:
| macro-map    | faithful d | faithful | big-Φ d | big-Φ | SPLIT? |
|--------------|-----------|----------|---------|-------|--------|
| top_variance | +1.261 (Δ+0.2175, p=5.3e-4) | UP | −0.443 (Δ−1.4826, p=0.17) | DOWN | TRUE |
| random       | BLOCKED-INFRA (pool swap-thrash) | — | — | — | PENDING |

FINDING: the faithful-UP / big-Φ-DOWN planning split DOES appear on the 3B engine rung under the
top_variance macro-map — same sign pattern as d768, with the faithful-UP leg SIGNIFICANT at 3B
(p=5.3e-4) vs faint at d768. This is a sign-level TRANSFER consistent with the d768 rung.

NOT full PASS (the pre-registered ≥2-macro-map robustness needs the random control) and NOT FAIL
(the measured map clearly shows the split). The random map's exact n=5 big-Φ (on_frac=0.500 max-entropy
→ ~87s/eval, the H_1038 n=6 measurement-cost wall now at n=5 for the denser 3B) was CRUSHED by pool
swap-contention (concurrent cc_native CI 12.7GB + 39GB swap → ~1.3% effective compute; killed
proven-stalled at ~113min per a_dont_kill_live_compute). BLOCKED-INFRA ≠ science ceiling (lesson #2).
REOPEN: clean-box re-run of the random control (≥16GB free RAM, no concurrent CI). fp64-canonical
confirmation needs a ≥32GB-RAM host (fp64 lean ~24.6GB > 30GB pool box under contention).
Verdict: `archive/state/verdicts/1042_3b_engine_phi_split/H_1042.txt`.
