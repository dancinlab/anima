---
id: H_1021
slug: imagine-rollout-vs-mpc
title: Does giving anima a MULTI-STEP IMAGINE ROLLOUT through its OWN learned world-model (Dreamer-style model-predictive control through the LEARNED forward model, instead of the H_1019 single-step ridge head) close the gap to the depth-4 MPC reference on the H_964 hidden-velocity station-keeping env — or does the learned model's forward-error compound over the horizon?
domain: cwm · cross-cutting · world-model · imagine · planning · model-predictive-control · human-level · north-star · behavior-eval · control · pre-register
source: H_1019 (🔴 CLOSED-NEG: anima single-step ridge head M=-0.6426 falls BELOW the depth-4 MPC band [-0.6034,-0.5034], gap +0.0892, d=-1.98 — "anima's WM policy is a single-step ridge-imitation head; it beats myopic oracles but not a true multi-step planner") + CWM @goal (perceive -> latent state -> IMAGINE -> act) + a_completeness_over_cheap + a_paper_significance + a_scale_honest_scope + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric) — keep the H_964 env + the depth-4 MPC reference + the reactive/random floors VERBATIM; keep anima's H_1019 single-step ridge head as the baseline rung; ADD anima's OWN learned action-conditioned forward model (LDSWorldModel trained by regression on the SAME greedy-oracle demos — a LEARNED model, NOT the true dynamics) and plan THROUGH it with a receding-horizon enumerator (Dreamer/MPC-through-the-learned-model)
verification_method: W2 (pre-registered placement falsifier — anima imagine-rollout vs the depth-4 MPC band, ladder against the H_1019 single-step WM) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
cross_process_byte_identical: false
llm: none
hexa_only: false
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: ONE placement rung (a_scale_honest_scope · a_toy_scale_recheck). TOY $0 CPU-local numpy, no GPU. Task = the H_964 partial-observability station-keeping env VERBATIM (agent sees POSITION only; optimal action needs HIDDEN velocity; v'=DRAG*v+0.6*THRUST[a], pos'=pos+0.4*v'+noise, DRAG=1.0, reward=-||pos||). The depth-4 MPC reference (M=-0.5534, the oracle CEILING), the reactive single-frame floor, and the random floor are reused VERBATIM from H_1019. anima's single-step ridge head (latent->action, M=-0.6426) is the baseline rung. NEW: anima's OWN learned action-conditioned world model — an LDSWorldModel(delay=3, act_dim=NACT) fitted by ridge regression on the SAME greedy-oracle demonstration trajectories (obs + action one-hots); its learned transition A and decoder C are anima's LEARNED forward model. The imagine-rollout planner enumerates all NACT^d action sequences, rolls the LEARNED A forward conditioned on each candidate action, decodes each imagined latent via C to a predicted position, scores by cumulative -||predicted pos||, and plays the first action of the best imagined plan (receding horizon). Crucially the planner uses the LEARNED model, NOT the true step_env dynamics (that would just BE the MPC). Depths d in {2,4}. Metric M = mean episode return (0 = optimal). Same env/seeds/episode counts as H_1019 (N_RUNS=40 x EP_PER_RUN=60). NO live human study. No Phi/IIT4 claim (behavior metric only) so a_phi_iit4_tool is n/a. Single rung; scale-transfer UNVERIFIED. NOT a forge binary.
sister: H_1019 (single-step ridge head below the MPC band — the residual this addresses), H_1015 / H_1018 (greedy-relative placement), H_964 (env + WAM/reactive/random arms + LDSWorldModel), H_972 (bar instrument), CWM M13
verdict: 🟢 GREEN — PASS, GAP CLOSED (inference-DEPTH limit). Giving anima a multi-step IMAGINE ROLLOUT through its OWN learned action-conditioned world model (Dreamer-style receding-horizon MPC THROUGH the learned forward model, NOT the true dynamics) CLOSES the H_1019 gap to the depth-4 MPC reference. Numbers (N_runs=40 x 60 ep, same seeds as H_1019): depth-4 MPC ceiling (true dynamics) M=-0.5534 CI=[-0.5663,-0.5403]; anima imagine-rollout d=4 (through the learned model) M=-0.5635 CI=[-0.5745,-0.5518] — WITHIN the parity band [-0.6034,-0.5034] (within_band=True, ci_overlaps=True), gap to MPC only +0.0101, anima-d4 vs MPC Welch p=0.261 d=-0.253 (statistically indistinguishable from the true optimum); anima single-step WM (H_1019 rung) M=-0.6426 CI=[-0.6575,-0.6282]; anima imagine-rollout d=2 M=-0.6745 (SLIGHTLY WORSE than single-step — short imagined horizons hurt: forward-model error not yet outweighed by lookahead); greedy oracle -0.8906; reactive floor -1.9237; random floor -6.1249. D1 non-vacuity VALID (reactive CI_hi -1.8834 < band_lo -0.6034). D2 hardening real VALID (MPC -0.5534 >= greedy ref -0.8906). D3 rollout-is-genuine VALID (imagine-d4 vs single-step WM Welch p=1.96e-12, d=1.889 — the rollout is real model-planning, not a relabeled head). imagine-d4 lift over single-step WM = +0.0791 (improves=True, p=1.96e-12). READING: the H_1019 closed-negative was an INFERENCE-DEPTH limit, NOT a WM-quality limit — anima's LEARNED world model was already accurate enough to plan through; H_1019 simply never gave anima the IMAGINE step (it acted single-step). Planning over a depth-4 horizon THROUGH the learned model recovers near-optimal control and reaches the true depth-4 MPC band. This validates the CWM @goal loop perceive->latent->IMAGINE->act: imagination, not just a bigger model, closes the human-bar gap. The non-monotone ladder (d2 worse than 1-step, d4 in-band) is itself a finding: a horizon TOO SHORT to amortize the learned-model's forward error is worse than acting reactively on the latent. Δ-vs-H_1019: the gap that H_1019 ruled "below the multi-step optimum" is RECOVERED by imagine-rollout. TOY single rung, $0 CPU-local; scale-transfer / deeper-MPC / continuous-action / learned-model-fidelity-at-scale UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool n/a (behavior return, no Φ claim).
---

# H_1021 — does planning THROUGH anima's LEARNED world-model close the H_1019 gap?

## 0. motivation
H_1019 (🔴 CLOSED-NEG) hardened the human reference to a depth-4 receding-horizon MPC (true
multi-step optimum, M=-0.5534, band [-0.6034,-0.5034]) and found anima's WM policy (M=-0.6426)
falls BELOW the band (gap +0.0892, d=-1.98). The diagnosis in H_1019 is explicit: **anima's WM
policy is a single-step ridge-imitation head — it maps the current latent directly to one action
and acts greedily; it beats myopic oracles but not a true multi-step planner.** The CWM @goal,
however, is perceive -> latent state -> **IMAGINE** -> act: anima is supposed to plan through its
world model, not act one step at a time. H_1019 never gave anima that imagine step. H_1021 asks the
direct follow-on: if anima plans over a horizon by rolling its OWN LEARNED world-model forward
(Dreamer-style model-predictive control THROUGH the learned forward model — NOT the true dynamics),
does the gap close? Two clean outcomes, both publishable: (a) it closes -> the H_1019 gap was an
inference-DEPTH limit, not a WM-QUALITY limit (the world model was good enough; anima just was not
using it to plan). (b) it does not close -> the learned model's forward-prediction error COMPOUNDS
over the horizon, so planning through it cannot recover the true optimum (a model-error finding,
a_paper_negative_ok) — the gap is a WM-fidelity limit, not merely an inference-depth one.

## 1. hypothesis (one falsifiable claim)
On the H_964 hidden-velocity station-keeping task, with metric M = mean episode return, an anima
agent that plans by **receding-horizon imagined rollout through its OWN learned action-conditioned
world model** (enumerate NACT^d action sequences, roll the LEARNED transition A forward, decode via
C, score cumulative -||predicted pos||, play the first action of the best plan) lands WITHIN or ABOVE
the depth-4 MPC parity band, i.e. planning through the learned model recovers near-optimal control —
closing the H_1019 single-step gap.

## 2. pre-registered PASS / FAIL (frozen 2026-06-07, numeric thresholds)
Reference CEILING = depth-4 MPC mean P (recomputed this run; H_1019 had P=-0.5534). band = [P - TOL,
P + TOL], TOL = 0.05 (return units, same as H_1018/H_1019). All means over N_RUNS=40 runs x
EP_PER_RUN=60 episodes (same seeds as H_1019), bootstrap 95% CIs. The single-step WM head is the
H_1019 rung (re-measured here; expect ~-0.6426). "imagine-d2" / "imagine-d4" = the imagine-rollout
planner at depths 2 and 4.

- **D1 (task validity / non-vacuity):** reactive CI_hi < band_lo (a single-frame reactive policy
  cannot reach the band; the task genuinely requires the WM). [reused from H_1019]
- **D2 (reference is strong):** MPC mean P >= the greedy no-lapse oracle mean (-0.8906) up to noise
  (the reference is a true multi-step optimum, not a myopic one). [reused from H_1019]
- **D3 (the rollout is genuine model-planning, not a relabeled head):** imagine-d4 must DIFFER from
  the single-step WM head by more than CI noise in at least one direction — otherwise the "rollout"
  is doing nothing and the comparison is vacuous (report INCONCLUSIVE if so).
- **PASS (gap closed — inference-depth limit):** imagine-d4 mean within [band_lo, band_hi] AND its
  CI overlaps the band (genuine parity with the true optimum), OR imagine-d4 mean > band_hi AND its
  CI_lo > band_hi (above the hardened reference). The H_1019 gap was an inference-DEPTH limit.
- **PARTIAL (improves but misses — model-error-bounded, a_paper_negative_ok):** imagine-d4 mean is
  ABOVE the single-step WM mean by more than CI noise (planning helps) BUT imagine-d4 mean < band_lo
  AND its CI_hi < band_lo (still below the MPC band). The learned model's forward error compounds
  over the horizon — the gap is a WM-fidelity limit, not purely an inference-depth one.
- **FAIL / RED (planning through the learned model does NOT help — closed-negative,
  a_paper_negative_ok):** imagine-d4 mean is NOT above the single-step WM mean (<= it up to CI
  noise) AND imagine-d4 < band_lo — the learned model is not accurate enough to plan through at all;
  imagined rollouts give no actionable advantage over the single-step head.
- **INCONCLUSIVE:** boundary case (CI straddles the band, or D3 fails) — report honestly, no emoji
  promotion.

## 3. method
- Reuse `CWM/probes/h964_latent_policy.py` env + arms VERBATIM (step_env, optimal_action, gen_demo,
  THRUSTS, DRAG, VSTEP, T, N_TRAIN, NACT, ODIM) and the H_1019 boot-CI / run-harness machinery
  (episode_return signature, run_agent, make_mpc, make_greedy, make_random, make_reactive,
  make_wam, the depth-4 MPC reference policy `mpc_action`).
- Train the single-step anima WM head (latent -> action) and the reactive head EXACTLY as
  H_964/H_1015/H_1018/H_1019 (imitation of the greedy oracle demos — anima's single-step training is
  UNCHANGED).
- NEW: fit anima's OWN learned action-conditioned forward model — `LDSWorldModel(ODIM, delay=3,
  act_dim=NACT)` fitted by ridge regression on the SAME greedy-oracle demonstration trajectories
  (observation seqs + action one-hots). This yields a LEARNED transition A (z_{t+1} ~ A[z_t; a_t])
  and a LEARNED decoder C (z -> position). This is anima's learned model — fitted ONLY from demos,
  never given the true step_env.
- NEW: the imagine-rollout planner. At each control step, take the current delay-embedded latent z
  (from the position history anima has observed), enumerate every length-d action sequence
  (NACT^d leaves), roll the LEARNED A forward conditioned on the candidate actions, decode each
  imagined latent via C to a predicted position, score by cumulative -||predicted pos|| (noise-free,
  in imagination), and play the FIRST action of the best imagined plan (receding horizon). The
  planner NEVER calls step_env in planning — it plans through the learned model only.
- Run all arms (depth-4 MPC ceiling, single-step WM, imagine-d2, imagine-d4, reactive, random) at
  the same seeds, N_RUNS=40 x 60 ep. Report the ladder.
- Decision is purely numeric (g5 CODE-measured, no LLM self-judge, p7). Raw stdout ->
  `.verdicts/1021_imagine_rollout_vs_mpc/H_1021.txt`. VERDICT-GATE: TEXT tokens only until that
  file exists.

## 4. measurement (2026-06-07)
| arm | M (mean return) | bootstrap 95% CI |
|---|---|---|
| depth-4 MPC (CEILING, true dynamics) | **-0.5534** | [-0.5663, -0.5403] |
| anima imagine-rollout d=4 (LEARNED model) | **-0.5635** | [-0.5745, -0.5518] |
| anima imagine-rollout d=2 (LEARNED model) | -0.6745 | [-0.6902, -0.6581] |
| anima single-step WM (H_1019 rung) | -0.6426 | [-0.6575, -0.6282] |
| greedy oracle (depth-1) | -0.8906 | [-0.9131, -0.8666] |
| reactive (single-frame, floor) | -1.9237 | [-1.9641, -1.8834] |
| random (floor) | -6.1249 | [-6.2580, -5.9883] |

- parity band = [-0.6034, -0.5034] (P=-0.5534, TOL=0.05).
- D1 non-vacuity: reactive CI_hi -1.8834 < band_lo -0.6034 → **VALID**.
- D2 hardening real: MPC -0.5534 >= greedy ref -0.8906 → **VALID**.
- D3 rollout-is-genuine: imagine-d4 vs single-step WM Welch p=1.96e-12, d=1.889 → **VALID** (the
  rollout is real model-planning, not a relabeled head).
- imagine-d4 mean -0.5635 → within_band=**True**, ci_overlaps=**True**, below=False, above=False.
- imagine-d4 vs single-step WM delta = **+0.0791** (improves=True, p=1.96e-12).
- MPC − imagine-d4 gap = **+0.0101**; imagine-d4 vs MPC Welch p=0.261, Cohen d=-0.253
  (**statistically indistinguishable from the true optimum**).
- LADDER (single-step → imagine-d2 → imagine-d4 → MPC ceiling → floors):
  -0.6426 → -0.6745 → **-0.5635** → -0.5534 → (reactive -1.9237, random -6.1249).
  NON-MONOTONE: depth-2 is slightly WORSE than the single-step head — a horizon too short to
  amortize the learned model's forward-prediction error is worse than acting reactively on the
  latent; depth-4 lookahead clears it and reaches the band.

## 5. verdict
**🟢 GREEN — PASS, GAP CLOSED (inference-DEPTH limit).** Planning THROUGH anima's OWN learned
world model (depth-4 receding-horizon imagined rollout, Dreamer-style MPC through the LEARNED
forward model — never the true dynamics) reaches M=-0.5635, **WITHIN** the depth-4 MPC parity band
[-0.6034,-0.5034] and statistically **indistinguishable** from the true optimum (gap +0.0101,
p=0.261). The H_1019 closed-negative (single-step WM -0.6426 below the band) was therefore an
**INFERENCE-DEPTH** limit, **NOT a WM-quality** limit: anima's learned model was already accurate
enough to plan through; H_1019 simply never gave anima the IMAGINE step. This is a clean
Δ-vs-H_1019 result that validates the CWM @goal loop perceive→latent→IMAGINE→act — **imagination,
not a bigger model, closes the human-bar gap.** It sharpens (does not overwrite) H_1019: the
single-step head genuinely falls short of the multi-step optimum (H_1019 holds), and adding the
imagine step recovers it (H_1021). Honest secondary finding: the non-monotone depth ladder (d2
worse than 1-step) shows a horizon too short to amortize learned-model forward error underperforms
even reactive-on-latent. TOY single rung, $0 CPU-local; deeper-MPC / continuous-action /
learned-model-fidelity-at-scale are an OPEN ladder (a_scale_honest_scope · a_toy_scale_recheck).
Verdict file: `.verdicts/1021_imagine_rollout_vs_mpc/H_1021.txt`.
