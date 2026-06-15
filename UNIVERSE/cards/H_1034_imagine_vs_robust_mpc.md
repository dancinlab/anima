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
status: measured
verdict: 🟢 GREEN — IMAGINE-BEATS-ROBUST-MPC-TOO. On the H_964 continuous hidden-velocity station-keeping toy, imagine-rollout (CEM through anima's OWN learned LDS world model) is STILL >= a ROBUST scenario/SAA tube-MPC (N_SCEN=16 process-noise draws/candidate, given the TRUE dynamics AND the disturbance model) at BOTH deep depths {8,16}: the pre-registered robust_gap = robust-MPC(d) - imagine(d) is -0.0261 @ d=8 and -0.1128 @ d=16, both <= GAP_TOL=0.05, so the robust MPC does NOT beat imagine at deep horizon by the frozen rule (depths where robust beats imagine by >GAP_TOL = []). Robustifying the true planner barely moved its return (naive->robust improvement only +0.0012 @ d=16) and the robust MPC STILL degrades with depth exactly like the naive one (robust d=2 -0.2697 -> d=16 -0.8734; naive d=2 -0.2623 -> d=16 -0.8746) — so H_1027's deep-MPC failure was NOT process-noise-brittleness (which a scenario/tube MPC would fix) and imagine's deep-horizon win is NOT a weak-baseline artifact. The vectorized naive-MPC reproduces H_1027 bit-for-bit (-0.3715/-0.2623/-0.3205/-0.4847/-0.8746). At d=16 imagine leads the robust MPC by +0.113 return (Welch p=3.4e-17, Cohen d=-2.46). The H_1027 imagine>=MPC advantage at depth is REAL on this toy. TOY single rung, $0 CPU-local; scenario-tube robustification only (min-max/CVaR/explicit-tube UNVERIFIED); scale-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool n/a (behavior return only, no Φ). Verdict file: .verdicts/1034_imagine_vs_robust_mpc/H_1034.txt
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

## 4. measurement (2026-06-08)
Reused the H_1027 env + learned `LDSWorldModel(delay=3, act_dim=2)` (ridge on the SAME greedy-oracle
demos, NEVER given the true dynamics) + CEM machinery + `AnimaImaginePlanner` imagine-rollout + the
naive noise-free true-MPC + the N_RUNS=40 × EP_PER_RUN=60 protocol VERBATIM. The ONLY added component
is `cem_plan_robust` — the frozen scenario/SAA tube-MPC (N_SCEN=16 process-noise draws/candidate,
common random numbers across the population per CEM iteration). The three CEM planners are VECTORIZED
over the population (and scenarios for robust); the vectorization is **bit-identical** to the H_1027
scalar definitions (verified max abs diff = 0.0 across the whole ladder, and the vectorized naive-MPC
reproduces the H_1027 return curve exactly), preserving the frozen semantics and rng draw shapes — it
is a pure speed optimization (robust d=16 ~165 ms → ~1.6 ms/call). Script:
`UNIVERSE/h1034_imagine_vs_robust_mpc.py`. Raw stdout: `.verdicts/1034_imagine_vs_robust_mpc/H_1034.txt`.

### depth ladder (MPC depth == imagine horizon; mean return, 0 = optimal; bootstrap CI)
| depth d | naive-MPC M (CI) | ROBUST-MPC M (CI) | imagine-rollout M (CI) | robust_gap = robust−imag | Welch p / Cohen d | naive→robust | verdict @ GAP_TOL=0.05 |
|---|---|---|---|---|---|---|---|
| 1  | -0.3715 [-0.3896,-0.3532] | -0.3702 [-0.3843,-0.3573] | -0.3790 [-0.3962,-0.3623] | **+0.0088** | p=4.3e-01 d=+0.176 | +0.0013 | imag≥robust |
| 2  | -0.2623 [-0.2729,-0.2512] | -0.2697 [-0.2780,-0.2614] | -0.2684 [-0.2768,-0.2604] | **-0.0013** | p=8.3e-01 d=-0.048 | -0.0074 | imag≥robust |
| 4  | -0.3205 [-0.3288,-0.3120] | -0.3174 [-0.3261,-0.3078] | -0.3167 [-0.3252,-0.3084] | **-0.0007** | p=9.1e-01 d=-0.025 | +0.0031 | imag≥robust |
| **8**  | -0.4847 [-0.4941,-0.4755] | -0.4787 [-0.4896,-0.4679] | -0.4526 [-0.4613,-0.4434] | **-0.0261** | p=5.4e-04 d=-0.808 | +0.0060 | **imag≥robust (DEEP)** |
| **16** | -0.8746 [-0.8924,-0.8562] | -0.8734 [-0.8888,-0.8575] | -0.7606 [-0.7729,-0.7483] | **-0.1128** | p=3.4e-17 d=-2.458 | +0.0012 | **imag≥robust (DEEP)** |

- **deep-tail decision {8,16}:** robust_gap = [-0.0261, -0.1128], both ≤ GAP_TOL=0.05 → depths where
  the robust MPC beats imagine by more than tolerance = **[] (none)**. PASS / IMAGINE-BEATS-ROBUST-MPC-TOO.
- **robustification barely helped the true planner:** naive→robust return improvement is +0.0013 /
  -0.0074 / +0.0031 / +0.0060 / +0.0012 over the ladder — essentially zero. The scenario/tube MPC,
  given the TRUE dynamics AND the disturbance model, is statistically indistinguishable from the naive
  noise-free MPC at every depth.
- **the robust MPC degrades with depth EXACTLY like the naive one:** naive curve
  [-0.372,-0.262,-0.321,-0.485,-0.875] vs robust curve [-0.370,-0.270,-0.317,-0.479,-0.873] — both
  best at d=2 and monotonically worse past it. So H_1027's deep-MPC failure was **NOT**
  process-noise-brittleness (which a tube MPC is designed to fix); robustness does not rescue it.
- **imagine pulls away at depth:** at d=16 imagine beats the robust MPC by +0.113 return
  (Welch p=3.4e-17, Cohen d=-2.46) — a large, highly significant lead.

## 5. finding / verdict
**🟢 GREEN — IMAGINE-BEATS-ROBUST-MPC-TOO.** The H_1027 result ("imagine-rollout ≥ the same-depth
true-MPC, and beats it at deep horizon") is **NOT** an artifact of a brittle (noise-free,
single-scenario) MPC baseline. Against a ROBUST scenario/SAA tube-MPC — given the TRUE dynamics AND
the disturbance model, optimizing EXPECTED return over N_SCEN=16 sampled process-noise realizations —
imagine-rollout is still ≥ the robust MPC at BOTH deep depths {8,16} (robust_gap ≤ GAP_TOL by the
frozen rule), and at d=16 it leads by +0.113 (Cohen d=-2.46, p=3.4e-17).

The decisive honest detail: robustifying the true MPC **barely changed its returns** (naive→robust
improvement ≈ 0 at every depth) and the robust MPC **still degrades with depth in lock-step with the
naive MPC** (both best at d=2, both ≈-0.87 at d=16). This refutes the H_1034 hypothesis that the
deep-horizon MPC failure was disturbance-brittleness: a scenario/tube MPC is exactly the fix for that
and it does not help. The residual interpretation is that the deep CEM-MPC's loss is **search/landscape
difficulty** — optimizing a long open-action sequence over the TRUE (stiff DRAG=1.0 double-integrator)
dynamics where small early actions compound — whereas imagine plans through a **smoother regularized
ridge-fit learned transition** whose decoded cost landscape is easier for the same CEM budget. The
imagine advantage at depth is REAL on this toy, not a weak-baseline artifact.

Δ-vs-H_1027: H_1027 closed TRACKS-ALL-DEPTHS and read the deep imagine>MPC as the noise-free MPC
over-committing to brittle plans; H_1034 adds the robust baseline and shows that read was wrong about
the *mechanism* (it is not process-noise brittleness) but the *direction* holds even harder against a
stronger planner — imagine ≥ robust-MPC, decisively at depth. TOY single rung, $0 CPU-local;
scenario-tube robustification only (min-max / CVaR / explicit-tube invariant set UNVERIFIED — a
different robustification could still move the verdict); scale-transfer UNVERIFIED (a_scale_honest_scope
· a_toy_scale_recheck). g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool n/a (behavior return
only, no Φ claim).

## 6. sibling / xlinks
to [H_1027](./H_1027_imagine_rollout_depth_ladder.md) · [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · [H_1025](./H_1025_continuous_imagine.md) · CWM/CWM.md
