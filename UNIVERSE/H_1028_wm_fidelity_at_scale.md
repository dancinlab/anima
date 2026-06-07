---
id: H_1028
slug: wm-fidelity-at-scale
title: Does a larger / longer-trained learned world-model widen the imagine-rollout planning horizon (push h* out) and close any residual gap to a deep MPC — i.e. does WM forward-fidelity scale the reachable optimum?
domain: cwm · world-model · imagine · planning · model-fidelity · scaling · gpu · pre-register
source: H_1021 (parity was inference-DEPTH limited, NOT WM-quality limited, on the toy LDS model) + H_1027 (model-error-limited horizon h*) — whether INCREASING WM fidelity moves h* is the scaling question
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric) — train a ladder of learned WMs of increasing capacity / data / training; for each, measure imagine-rollout's reachable horizon h* (H_1027) and gap to a deep MPC
verification_method: W2 (pre-registered fidelity-vs-horizon falsifier · WM fidelity ladder x imagine-rollout horizon) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
verdict: 🔴 FIDELITY-DOESNT-HELP (closed-negative, a_paper_negative_ok)
measured_at: 2026-06-07
---

# H_1028 — does WM forward-fidelity scale the reachable optimum?

## 0. motivation
H_1021 found the toy LDS world-model was ALREADY accurate enough to plan to a depth-4 optimum;
H_1027 posits a model-error-limited horizon $h^*$. The scaling question closes the loop: if we make
the learned WM more faithful (bigger / more data / longer training), does $h^*$ move out and the gap
to a DEEP MPC close? This is the bridge from the toy result to "bigger world-model = better
imagination" — and the natural GPU rung of the CWM control arc.

## 1. hypothesis
Imagine-rollout's reachable horizon $h^*$ (and the depth of optimum it can match) increases
monotonically with the learned model's measured multi-step forward fidelity — model fidelity, not
inference depth alone, sets the ceiling at scale.

## 2. pre-registered falsifier (frozen 2026-06-07)
Train a pre-frozen ladder of learned WMs (increasing capacity/data/epochs). For each, measure (a)
multi-step forward fidelity and (b) the imagine-rollout horizon $h^*$ + gap to a deep MPC (H_1027
protocol). Regress $h^*$ / optimum-depth on fidelity. GPU likely for the larger rungs
(a_fire_autonomous — state est. cost, dispatch).
- PASS = FIDELITY-SCALES-HORIZON : $h^*$ / matched-optimum-depth rises monotonically with WM fidelity.
- FAIL = FIDELITY-DOESNT-HELP : higher fidelity does not extend $h^*$ (the limit is the planner or the
  task, not the model; closed-negative, a_paper_negative_ok).

## 3. honest scope
Multi-rung; the largest rungs are GPU (a_fire_autonomous, no cost gate). No Phi claim
(a_phi_iit4_tool n/a). Toy-to-production transfer UNVERIFIED until a real env is used
(a_scale_honest_scope). Lane tag = Lane-P/G as appropriate.

## 5. method (measured 2026-06-07)
Ran `UNIVERSE/h1028_wm_fidelity_at_scale.py` (g5 CODE-measured, p7-honest; no LLM self-judge).
The H_1027 protocol VERBATIM over the pre-frozen 5-rung WM fidelity ladder (R0_crippled .. R4_high,
co-varying delay × n_train × ridge × injected model-noise). Per rung: fit the LDS world-model,
measure (a) k-step open-loop forward fidelity `F = 1/(1+mean_k err(k))`, (b) the same-depth
true-CEM-MPC vs imagine-rollout depth ladder, and locate `h*` = deepest contiguously-tracked depth
(gap MPC(d)−imagine(d) ≤ GAP_TOL=0.05, no earlier break). Then Spearman-regress `h*` on `F`.

**Precision reduction (a_scale_honest_scope — NOT a falsifier change).** The original sizes
(N_RUNS=40, EP_PER_RUN=60, CEM_POP=64, CEM_ITERS=5, FWD_TEST=200) over-sized the prior run (it
crawled ~1h45m to only rung0/depth2, then the orphan died). After the branch vectorized the CEM
population and a measured 1-cell cost probe (full ladder ≈ 100 s wall), the run used Monte-Carlo
precision knobs **N_RUNS=16, EP_PER_RUN=30, CEM_POP=48, FWD_TEST=100**. The frozen FALSIFIER is
untouched: the **5 fidelity rungs R0..R4** (the axis under test), **GAP_TOL=0.05**, **CEM_ITERS=5**
and the **full depth ladder DEPTHS={1,2,4,8,16}** are all PRESERVED. **No GPU / pod** was used — the
WMs are tiny closed-form ridge fits; the whole ladder ran $0 CPU-local serial (g0,
a_cpu_local_no_waiter). Wall-time ≈ 2 min.

## 6. measurement + finding

Verdict: **🔴 FIDELITY-DOESNT-HELP** — closed-negative against the pre-registered
FIDELITY-SCALES-HORIZON claim (a_paper_negative_ok). Verdict file:
`.verdicts/1028_wm_fidelity_at_scale/H_1028.txt`.

Cross-rung fidelity-vs-h* table (fidelity F = 1/(1+mean forward err); h* = deepest tracked depth):

| rung         | delay | n_train | fidelity F | mean_fwd_err | h* |
|--------------|-------|---------|-----------:|-------------:|---:|
| R0_crippled  | 1     | 20      | 0.6572     | 0.5217       | 0  |
| R1_underfit  | 2     | 30      | 0.0880     | 10.3674      | 0  |
| R2_partial   | 2     | 80      | 0.5134     | 0.9478       | 0  |
| R3_good      | 3     | 200     | 0.5822     | 0.7178       | 16 |
| R4_high      | 3     | 400     | 0.8675     | 0.1528       | 16 |

- **fidelity-sorted h\* sequence (low F → high F): `[0, 0, 16, 0, 16]`** — NOT monotone.
- h\* monotone-non-decreasing in fidelity = **False** (the falsifier requires monotone).
- h\* strictly extends (top-F h\*=16 > bottom-F h\*=0) = True, but monotonicity fails.
- **Spearman h\* ~ fidelity r = +0.5774 (p = 0.308)** — positive but NOT significant.
- Spearman h\* ~ mean_fwd_err r = −0.5774 (p = 0.308).
- every rung tracks ALL depths (h\*==16 for all) = False (so it is NOT the H_1027 trivial case).

**Finding.** The three low-fidelity rungs (R0, R1, R2) all break at the very first depth (h\*=0 —
the imagine planner cannot match even a depth-1 true-MPC), while the two high-fidelity rungs (R3,
R4) track the same-depth MPC at EVERY depth out to d=16 (h\*=16). So fidelity clearly *gates* the
horizon at the extremes — but the relationship is **not the monotone scaling the hypothesis
predicted**, for two reasons measured here: (i) the scalar fidelity F is itself **non-monotone in
the deliberate degradation axis** — R1_underfit's delay-2/low-data fit diverges catastrophically by
k=16 (forward_err≈45), giving it the LOWEST F=0.088 even though R0_crippled (delay-1, structurally
velocity-blind) has a higher F=0.657 because its errors stay bounded; and (ii) there is a **sharp
threshold, not a smooth ramp** — h\* jumps 0→16 between R2 (F=0.513, h\*=0) and R3 (F=0.582, h\*=16)
with nothing in between, so no rung exhibits the predicted "finite small h\* that extends out as
fidelity rises". When sorted by F the sequence interleaves to `[0,0,16,0,16]`, breaking
monotonicity (R2 at F=0.513 has h\*=0 but lower-F R0 at F=0.657… i.e. R0 has higher F yet h\*=0
too). The reachable horizon is therefore **fidelity-gated but not fidelity-graduated** on this toy
env: below a fidelity threshold the imagine planner is useless (h\*=0); above it, it tracks
everything (h\*=16). This deterministically rules out the smooth-monotone FIDELITY-SCALES-HORIZON
axis as stated.

**Honest scope (a_scale_honest_scope · a_toy_scale_recheck).** TOY single env, single closed-form
WM family, ladder OPEN. The threshold/saturation behaviour means a finer fidelity grid AND a
harder/lower-noise env (where deep open-loop accuracy matters and the optimum sits at intermediate
depth) could still expose a graduated fidelity-limited h\*; a genuinely larger deep-net high-fidelity
rung on GPU remains UNVERIFIED. The verdict is scoped to the measured toy ladder. $0 CPU-local, NO
GPU/pod used.

## 4. sibling / xlinks
to [H_1027](./H_1027_imagine_rollout_depth_ladder.md) · [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · CWM/CWM.md · two-7b-lanes-distinction
