---
id: H_1019
slug: human-bar-true-optimal
title: When the human reference is HARDENED from the 1-step-greedy hand-coded oracle to a multi-step receding-horizon (MPC-style) TRUE optimum on the same hidden-velocity station-keeping env, does anima's closed-loop WM policy STILL clear the human band, or was the H_1018 above-oracle result entirely the myopic-oracle suboptimality gap?
domain: cwm · cross-cutting · world-model · human-level · north-star · behavior-eval · placement · control · oracle-hardening · pre-register
source: CWM milestone M13 (north-star HARDENING) + H_1015 (first north-star placement) + H_1018 (lapse-free re-placement, above-oracle = env/oracle-suboptimality, explicit follow-on "harden the oracle to the true LQG/Kalman optimum and re-place") + a_completeness_over_cheap + a_paper_significance + a_scale_honest_scope + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric) — keep the H_964 env + anima WM policy VERBATIM; ONLY harden the human reference from the 1-step-greedy `optimal_action` to a depth-H receding-horizon planner that searches action sequences over the (known) linear dynamics and plays the first action of the best plan (a hand-coded MPC = the strongest non-anima reference that knows velocity)
verification_method: W2 (pre-registered placement falsifier — anima closed-loop WM policy vs a TRUE multi-step-optimal human-proxy band on a WM-requiring control task) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
cross_process_byte_identical: false
llm: none
hexa_only: false
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: ONE placement rung (a_scale_honest_scope · a_toy_scale_recheck). TOY $0 CPU-local numpy, no GPU. Task = the H_964 partial-observability station-keeping env (agent sees POSITION only; optimal action needs HIDDEN velocity; dynamics v'=DRAG*v+0.6*THRUST[a], pos'=pos+0.4*v'+noise, DRAG=1.0, reward=-||pos||). The HARDENED human reference is a receding-horizon planner of depth H that, knowing the (true) velocity and the deterministic part of the dynamics, exhaustively searches action sequences of length H over the NACT actions, scores each by the noise-free cumulative reward, and plays the first action of the best plan (a hand-coded MPC). Depth H is frozen at 4 (NACT^H = 4^4 = 256 rollouts/step — exhaustive, $0). Metric M = mean episode return (0 = optimal, more negative = worse). Same env/seeds/episode counts as H_1015/H_1018; ONLY the human reference policy changes (greedy -> MPC). anima WM policy + reactive + random arms reused VERBATIM. NO live human study. No Φ/IIT4 claim (behavior metric only) so a_phi_iit4_tool is n/a. Single rung; scale-transfer UNVERIFIED. NOT a forge binary.
sister: H_1015 (first placement, greedy oracle), H_1018 (lapse-free re-placement, above-oracle env/oracle-suboptimality), H_964 (env + WAM/reactive/random arms), H_972 (bar instrument), CWM M13
verdict: 🔴 RED — CLOSED-NEGATIVE (a_paper_negative_ok). When the human reference is hardened from the 1-step-greedy `optimal_action` to a depth-4 receding-horizon MPC on the SAME H_964 hidden-velocity station-keeping env, anima's WM policy lands BELOW the hardened human band. Numbers (N_runs=40 x 60 ep, same seeds as H_1015/H_1018): depth-4 MPC (true reference) M=-0.5534 CI=[-0.5663,-0.5403]; greedy oracle (depth-1) M=-0.8906 (reproduces H_1018); anima (WM latent->action) M=-0.6426 CI=[-0.6575,-0.6282]; reactive M=-1.9237; random M=-6.1249. Hardening delta = MPC - greedy = +0.3372 (the multi-step plan buys 0.34 return over greedy). D1 non-vacuity VALID (reactive CI_hi -1.8834 < band_lo -0.6034 — task genuinely requires the WM). D2 hardening real VALID (MPC -0.5534 >= greedy ref -0.8906). Parity band [-0.6034,-0.5034]; anima mean -0.6426 is BELOW band_lo AND anima CI_hi -0.628 < band_lo -0.603 -> below=True; MPC-anima gap +0.0892; anima vs MPC Welch p=2.40e-13, Cohen d=-1.975. READING: the H_1018 "above-oracle" GREEN-PLUS was ENTIRELY the MYOPIC-ORACLE gap — anima out-returns a 1-step-greedy reference but FALLS SHORT of a true multi-step optimum. The CWM north-star "human-level-or-beyond" placement is therefore BOUNDED to weak (greedy) references on this toy: anima is human-competitive vs greedy, NOT vs an MPC. Honest, publishable closed-negative that sharpens H_1015/H_1018 without overwriting them (the greedy-relative placement is real; the absolute "beyond-human" claim does not survive oracle-hardening). TOY single rung, $0 CPU-local; scale-transfer / deeper-MPC / continuous-action references UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool n/a (behavior return, no Φ claim).
---

# H_1019 — north-star HARDENING: anima vs a TRUE multi-step-optimal human reference

## 0. motivation
H_1015 (🟢) did the first falsifiable placement of the CWM north star and H_1018 (🟢 GREEN-PLUS)
removed the ~7% attention-lapse caveat — anima's WM policy beat even the *no-lapse* oracle. But
H_1018 itself flagged the real remaining caveat honestly: the "oracle" is the H_964 hand-coded
`optimal_action`, which picks the thrust whose **single next-step** position is nearest the origin.
On a DRAG=1.0 env where velocity fully persists, a 1-step-greedy choice is **myopic** — it is NOT
the multi-step optimum. So H_1018's "above-oracle" is an **env/oracle-suboptimality** finding:
anima's imitation-trained WM head happens to out-return a *myopic* reference, which is a weak claim
about "human-level-or-beyond." The honest, completeness-bar next step (a_completeness_over_cheap)
named explicitly in the H_1018 log is: **harden the human reference to a true multi-step optimum and
re-place anima.** If anima still clears the bar, the north-star placement survives oracle-hardening;
if it falls below, the H_1018 GREEN-PLUS was entirely the myopic-oracle gap (a clean closed-negative,
a_paper_negative_ok).

## 1. hypothesis (one falsifiable claim)
On the H_964 hidden-velocity station-keeping task, with metric M = mean episode return and a human
reference HARDENED to a depth-4 receding-horizon planner (exhaustive 4^4=256 action-sequence search
over the known dynamics, knows velocity, plays the first action of the best noise-free plan), anima's
closed-loop world-model policy (latent -> action) lands WITHIN or ABOVE the hardened human band,
while the reactive single-frame baseline lands BELOW it.

## 2. pre-registered PASS / FAIL (frozen 2026-06-07, numeric thresholds)
Let MPC = the depth-4 receding-horizon human reference; band = [MPC - TOL, MPC + TOL], TOL = 0.05
(return units, same as H_1018). All means over N_RUNS=40 runs x EP_PER_RUN=60 episodes (same as
H_1015/H_1018), bootstrap 95% CIs.

- **D1 (task validity / non-vacuity):** reactive CI_hi < band_lo (a single-frame reactive policy
  cannot reach the hardened band; the placement is non-vacuous and the task genuinely requires the WM).
- **D2 (reference is strong):** MPC mean >= the H_1018 no-lapse greedy-oracle mean (-0.8906) up to
  noise — the hardening genuinely strengthens the reference (MPC is at least as good as greedy).
- **PASS (north-star survives hardening):** anima mean within [band_lo, band_hi] AND anima CI
  overlaps the band (genuine parity with the TRUE optimum), OR anima mean > band_hi AND anima
  CI_lo > band_hi (still above even the hardened reference).
- **FAIL / RED (closed-negative, a_paper_negative_ok):** anima mean < band_lo AND anima CI_hi <
  band_lo — anima is BELOW the true multi-step optimum, so the H_1018 above-oracle result was the
  myopic-oracle gap; honest scope = anima is human-competitive only vs a *greedy* reference, NOT vs
  a true MPC.
- **INCONCLUSIVE:** boundary case (CI straddles the band) — report honestly, no emoji promotion.

## 3. method
- Reuse `CWM/probes/h964_latent_policy.py` env + arms VERBATIM (step_env, optimal_action, gen_demo,
  THRUSTS, DRAG, T, N_TRAIN) and the H_1018 boot-CI / run-harness machinery.
- Train the anima WM head (latent -> action) and the reactive head EXACTLY as H_964/H_1015/H_1018
  (imitation of the *greedy* oracle demos — anima's training is UNCHANGED; only the human reference
  it is compared against is hardened).
- NEW: a hand-coded depth-4 MPC reference policy that, given the true (pos, v), exhaustively rolls
  every length-4 action sequence forward through the deterministic part of step_env (noise EXCLUDED
  in planning, present in execution), scores by cumulative -||pos||, and plays the first action of
  the best sequence. Also report the greedy oracle (depth-1) so the hardening delta is explicit.
- Run all arms (MPC, greedy oracle, anima WM, reactive, random) at the same seeds, N_RUNS=40 x 60 ep.
- Decision is purely numeric (g5 CODE-measured, no LLM self-judge, p7). Raw stdout ->
  `.verdicts/1019_human_bar_true_optimal/H_1019.txt`.

## 4. measurement (2026-06-07)
| arm | M (mean return) | bootstrap 95% CI |
|---|---|---|
| depth-4 MPC (true human ref) | **-0.5534** | [-0.5663, -0.5403] |
| greedy oracle (depth-1) | -0.8906 | [-0.9131, -0.8666] |
| anima (WM latent->action) | -0.6426 | [-0.6575, -0.6282] |
| reactive (single-frame) | -1.9237 | [-1.9641, -1.8834] |
| random | -6.1249 | [-6.2580, -5.9883] |

- hardening delta = MPC - greedy = **+0.3372** (the multi-step plan buys 0.34 return over greedy).
- D1 non-vacuity: reactive CI_hi -1.8834 < band_lo -0.6034 → **VALID**.
- D2 hardening real: MPC -0.5534 >= greedy ref -0.8906 → **VALID**.
- parity band = [-0.6034, -0.5034]; anima mean -0.6426 **BELOW** band_lo AND anima CI_hi -0.628 <
  band_lo -0.603 → **below = True**.
- MPC-anima gap = +0.0892; anima vs MPC Welch p = 2.40e-13, Cohen d = -1.975.

## 5. verdict
**🔴 RED — CLOSED-NEGATIVE (a_paper_negative_ok).** When the human reference is hardened from a
1-step-greedy oracle to a depth-4 receding-horizon MPC, anima's WM policy lands **below** the hardened
human band. The H_1018 "above-oracle" GREEN-PLUS was **entirely the myopic-oracle gap** — anima
out-returns a greedy reference but falls short of a true multi-step optimum (gap +0.0892, d=-1.975).
The CWM north-star "human-level-or-beyond" placement is therefore **bounded to weak (greedy)
references** on this toy: anima is human-competitive vs greedy, NOT vs MPC. This sharpens H_1015/H_1018
honestly without overwriting them (the greedy-relative placement is real; the absolute beyond-human
claim does not survive oracle-hardening). TOY single rung; deeper-MPC / continuous-action / richer-env
references are an OPEN ladder (a_scale_honest_scope · a_toy_scale_recheck). Verdict file:
`.verdicts/1019_human_bar_true_optimal/H_1019.txt`.
