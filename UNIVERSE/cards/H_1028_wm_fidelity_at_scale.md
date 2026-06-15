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
measured_at: 2026-06-07
verdict: 🔴 RED — FIDELITY-DOESNT-HELP (closed-negative, a_paper_negative_ok). On a 5-rung pre-frozen WM fidelity ladder (capacity × data × ridge × injected model-noise: R0 crippled → R4 high-fit) over the H_964 continuous-action hidden-velocity station-keeping toy — reusing the H_1025/H_1027 CEM imagine-rollout planner, true-dynamics CEM-MPC, k-step open-loop forward-error measurement and N_RUNS=40×EP_PER_RUN=60 protocol VERBATIM (CEM population vectorized, verified BIT-IDENTICAL to the H_1027 scalar loop, max-diff 0.00e+00 across depths {1,2,4,8,16}) — the reachable imagine-rollout horizon h* (deepest contiguously-tracked depth at GAP_TOL=0.05) does NOT rise monotonically with the WM's MEASURED multi-step forward fidelity. Indexed by the measured scalar fidelity F=1/(1+mean_k err), h* = [0,1,16,0,16] (low→high F; monotone-nondecreasing=False; Spearman h*~F r=+0.4743 p=0.42, n=5): the literal pre-registered FIDELITY-SCALES-HORIZON claim is REFUTED. KEY SECONDARY FINDING (the why): open-loop forward error is NOT a faithful planning-fidelity proxy — R0_crippled (delay=1, structurally cannot recover the hidden velocity) GAMES the metric by collapsing predictions toward the origin so ‖pred−true‖ stays small on this near-origin task (mean_err 0.50 → deceptively HIGH F=0.666) yet is useless for planning (gap +33.5 at d=1, h*=0), while R1_underfit has a huge k=16 error blowup (47.6) but still plans (gaps ~0.2). When instead ordered by the CONSTRUCTED capacity/data/training ladder R0..R4, h* = [0,0,1,16,16] — monotone-nondecreasing=True, extending 0→16: more capacity/data/training DOES push the horizon out, but the open-loop-forward-error scalar fails to rank-order it because a degenerate WM scores low error by collapsing. So the low-fidelity end DOES expose finite small h* (0,0,1) that the high end (16,16) extends (the test H_1027's single high-fidelity WM could not surface), but NOT as a clean function of the measured-fidelity metric. Net closed-negative against FIDELITY-SCALES-HORIZON AS STATED, with the actionable lesson planning-fidelity ≠ open-loop forward accuracy. TOY single env, ladder OPEN (a_scale_honest_scope · a_toy_scale_recheck). $0 CPU-local, NO GPU needed (g0 — tiny closed-form ridge WMs; vectorization made the 5-rung deep ladder run in ~5 min). g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool n/a (behavior return + forward error, no Φ claim). Verdict file: .verdicts/1028_wm_fidelity_at_scale/H_1028.txt
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

## 4. measurement (2026-06-07)
Reused the H_1025/H_1027 continuous-action machinery VERBATIM — the H_964 hidden-velocity
station-keeping env (position-only obs, hidden velocity a delay-embedding latent must recover),
the CEM true-dynamics MPC (deep-MPC ceiling), the CEM imagine-rollout planner THROUGH a learned
`LDSWorldModel`, the k-step open-loop forward-error measurement, the depth ladder {1,2,4,8,16}
with GAP_TOL=0.05, and the N_RUNS=40 × EP_PER_RUN=60 protocol. The ONLY new axis is **WM
fidelity**: a 5-rung PRE-FROZEN ladder spanning under-fit → high-fit, co-varying delay-embedding
depth (capacity), demo count (data), ridge (regularization) and injected post-fit Gaussian
model-noise (direct fidelity degradation). The CEM population was vectorized over the population
axis (the pure-Python per-population loop was >90 min wall for the 5-rung deep ladder); the
vectorized planners were verified **bit-identical** (max-diff 0.00e+00 at every depth) to the
H_1027 scalar loop before any measurement, so the speedup changes no numbers (a_wall_first).
Per rung: (a) k-step forward fidelity, (b) imagine-rollout h* + gap-to-same-depth-MPC, then
regress h* on fidelity. Script: `UNIVERSE/h1028_wm_fidelity_at_scale.py`. Raw stdout:
`.verdicts/1028_wm_fidelity_at_scale/H_1028.txt`.

### pre-frozen WM fidelity ladder (frozen 2026-06-07)
| rung | delay | n_train | ridge | model-noise | mean fwd err | scalar F = 1/(1+err) | k=16 fwd err |
|---|---|---|---|---|---|---|---|
| R0_crippled | 1 |  20 | 1.0   | 0.20 | 0.5011 | 0.6662 | 0.383 |
| R1_underfit | 2 |  30 | 0.3   | 0.08 | 10.9034 | 0.0840 | 47.557 |
| R2_partial  | 2 |  80 | 0.05  | 0.03 | 0.8970 | 0.5271 | 2.107 |
| R3_good     | 3 | 200 | 0.005 | 0.01 | 0.7176 | 0.5822 | 2.386 |
| R4_high     | 3 | 400 | 0.001 | 0.00 | 0.1508 | 0.8690 | 0.335 |

### reachable horizon h* per rung (deepest contiguously-tracked depth, GAP_TOL=0.05)
| rung | scalar F | h* | per-depth gaps {1,2,4,8,16} |
|---|---|---|---|
| R0_crippled | 0.6662 | **0**  | +33.45 +27.95 +26.40 +24.77 +22.41 (origin-collapse: useless planner) |
| R1_underfit | 0.0840 | **0**  | +0.200 +0.151 +0.180 +0.230 +0.955 |
| R2_partial  | 0.5271 | **1**  | +0.033 +0.098 +0.159 +0.291 +0.607 |
| R3_good     | 0.5822 | **16** | -0.004 +0.007 +0.012 +0.010 -0.029 |
| R4_high     | 0.8690 | **16** | +0.005 +0.004 -0.005 -0.032 -0.104 |

- **h* indexed by MEASURED scalar fidelity F (low→high):** `[0, 1, 16, 0, 16]` —
  monotone-nondecreasing = **False**; Spearman h*~F **r=+0.4743 (p=0.42, n=5)**. The
  pre-registered FIDELITY-SCALES-HORIZON claim (h* monotone in measured forward fidelity) is
  **REFUTED**.
- **h* indexed by the CONSTRUCTED capacity/data/training ladder (R0..R4):** `[0, 0, 1, 16, 16]`
  — monotone-nondecreasing = **True**, extending **0 → 16**.

## 5. finding / verdict
**🔴 RED — FIDELITY-DOESNT-HELP (closed-negative, a_paper_negative_ok).** By the literal frozen
criterion, the reachable horizon h* does NOT rise monotonically with the WM's *measured* forward
fidelity (`[0,1,16,0,16]`, non-monotone, Spearman r=+0.47 p=0.42). The honest *why* — the key
secondary finding — is that **open-loop forward error is not a faithful planning-fidelity
proxy**: the crippled delay=1 rung (R0) cannot recover the hidden velocity and *games* the
metric by collapsing predictions toward the origin, scoring a deceptively-high fidelity F=0.666
on this near-origin station-keeping task while being completely useless for planning (gap +33.5
at d=1, h*=0); conversely R1_underfit posts a huge k=16 forward-error blowup (47.6) yet still
plans (gaps ~0.2). When the rungs are instead ordered by the way they were *constructed*
(increasing capacity/data/training, R0→R4), h* `[0,0,1,16,16]` DOES extend monotonically from 0
to 16 — so more model capacity/data/training genuinely pushes the imagine-rollout horizon out,
but the *open-loop-forward-error metric fails to rank-order it* because a structurally-degenerate
WM achieves low error by collapsing rather than by being right. Net: a clean closed-negative
against FIDELITY-SCALES-HORIZON *as stated* (measured-forward-fidelity-indexed), with the
actionable lesson that **planning fidelity ≠ open-loop forward accuracy** — a multi-step
closed-loop or planning-relevant fidelity metric (not ‖pred−true‖) is needed to predict h*.
Δ-vs-H_1027: H_1027's single already-high-fidelity WM tracked all depths (no h* in range); this
ladder confirms the low-fidelity end DOES expose finite small h* (0,0,1) that the high end
(16,16) extends — but only along the construction axis, not the measured-error axis. **No GPU
was used or needed** (g0): the WMs are tiny closed-form ridge fits; population-vectorization made
the full 5-rung deep ladder run in ~5 min CPU-local, deterministic given seeds, polled inline
(a_cpu_local_no_waiter). TOY single env, ladder OPEN — a deep-net high-fidelity GPU rung and a
planning-relevant fidelity metric remain UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).
g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool n/a (behavior return + forward error,
no Φ claim).

## 6. sibling / xlinks
to [H_1027](./H_1027_imagine_rollout_depth_ladder.md) · [H_1021](./H_1021_imagine_rollout_vs_mpc.md) · CWM/CWM.md · two-7b-lanes-distinction
