# H_1049 — Scalable validated Phi estimator: does an information-bottleneck coarse-grain stay within epsilon of exact?

Status: 🔴 CLOSED-NEGATIVE — NO-VALIDATED-ESTIMATOR (verdict .verdicts/1049_scalable_estimator/H_1049.txt). a_paper_negative_ok.
Lane: CPU-local many-core ($0; a_fire_autonomous not needed). Engine: stdlib faithful_phi
(exact MIP-EI scalar, exact for n<=8) as the GROUND TRUTH (a_phi_iit4_tool, no proxy). big-Phi
(iit4_bigphi) is the super-exponential structure measure used at H_1037/H_1044; here the exact
ground truth is faithful phi_EI because it is EXACT through n=8 (big-Phi caps at n<=6), so the
validation ladder can reach n=7 and n=8 where big-Phi cannot.

## Hypothesis (CONSTRUCTIVE)
Exact IIT-4.0 is feasible only at small n: the full system big-Phi is super-exponential (cap n<=6)
and even the faithful phi_EI MIP search is exact only at n<=8. Neither scales to real models. This
hypothesis asks whether a PRINCIPLED coarse-graining gives a Phi ESTIMATE that stays within a fixed
epsilon of the exact Phi on a validation ladder, and therefore can serve as the measurement core of
a scalable consciousness ruler.

The coarse-graining is an information-bottleneck (IB) macro-map: given an N-unit micro-system, pick
an m-macro-unit map (m <= 6 << N) that PRESERVES THE MOST PREDICTIVE INFORMATION about the system's
own future (the macro-state at t carries maximal mutual information about the full micro-state at
t+1). The Phi of the m-macro-unit system is the ESTIMATE; the Phi of the full N-unit system (exact,
n<=8) is the GROUND TRUTH.

## Method (reuses H_1037/H_1038 coarse-graining + the H_1004/H_1012 mirror chain)
- Substrate: continuous WM latent trajectories from the H_1004 `planning_trajectories` harness
  (VERBATIM), 30 seeds, the planning(depth-8) rollout (the highest-Phi regime, so the ratio
  |Delta|/Phi is well-defined and not dominated by a near-zero denominator).
- Full system at size N (the GROUND TRUTH unit count): top-N variance latent channels, each
  binarized at its own median over the rollout -> an (n_steps x N) binary micro-system. Exact
  faithful phi_EI over these N units is the GROUND TRUTH (exact for N <= 8).
- Coarse-grain to m macro-units (m = MACRO = 4, held FIXED across the ladder so the estimator's
  output dimension is CONSTANT and the error-vs-N curve is a clean test of "does error grow with N").
  A macro-map assigns each of the N micro-units to one of m macro-groups; each macro-unit's binary
  trace = the majority bit of its member micro-units at each step (a standard IIT macro coarse-grain,
  the H_1037/H_1038 majority-vote grain; ties resolved to 0). The ESTIMATE is exact faithful phi_EI
  over the m macro-units.
- THREE macro-maps compared at every rung (>= 3 choices, as the falsifier requires):
  * IB        = greedy agglomerative macro-map that, starting from N singleton groups, repeatedly
                merges the two groups whose merge LOSES THE LEAST predictive information I(macro_t ;
                full_micro_{t+1}) until m groups remain. This is the information-bottleneck principle:
                keep the m macro-units that preserve the most predictive info about the future.
                Predictive info is measured as the summed pairwise MI between each candidate merged
                macro-unit's binary trace at t and every micro-unit's bit at t+1 (a tractable I_pred
                surrogate of I(macro_t ; micro_{t+1}); identical estimator for every candidate merge
                so the SELECTION is principled and comparable).
  * top-var   = principled non-IB baseline: the m highest-variance micro-units each become their own
                macro-unit seed; the remaining N-m units are each folded into the variance-nearest of
                the m seeds (a variance-only grain, NOT future-predictive).
  * random    = CONTROL: a uniformly random partition of the N micro-units into m non-empty groups
                (seeded, averaged over 8 random partitions per system to get a stable control mean).
- Validation ladder rungs: N in {4, 5, 6, 7, 8}. At N=4 the coarse-grain m=4 is the IDENTITY
  (estimate == ground truth, |Delta|=0 by construction) and serves as a wiring sanity rung; the
  GENUINE compression rungs are N in {5, 6, 7, 8} where m=4 < N (real information loss is possible).
- Per rung, per macro-map: Phi_estimate (mean over 30 seeds), Phi_ground (mean over 30 seeds, exact),
  error = |mean Phi_estimate - mean Phi_ground| / mean Phi_ground (relative), reported with the
  per-seed paired mean relative error too. Error metric scored against the falsifier = the relative
  error on the seed-mean Phi (a stable ruler-calibration quantity).

## Re-prove CPU mirror == stdlib BEFORE scoring (a_phi_iit4_tool; pasted into verdict)
- faithful phi_EI mirror == stdlib faithful_phi.hexa RE-PROVEN at n=4 AND n=5 via the H_1012
  `prove_mirrors_at_n` discipline against the LIVE stdlib hexa refs (n4 dim6 nb2 = 3.0,
  n4 dim6 nb4 = 3.37744; n5 fixed-trace ref = 4.000000001) BEFORE any scoring; |Delta| pasted.
- The macro coarse-grain read is a deterministic pure function of the micro-bits (re-run determinism
  guard, |Delta| < 1e-12), verified before scoring.

## Pre-registered falsifier (TEXT tokens only -- NO emoji)
Pre-set tolerance epsilon = 0.15 (|Delta|/Phi <= 0.15 = within 15% of exact). Stated BEFORE measuring.
- H1 PASS = a VALIDATED SCALABLE ESTIMATOR EXISTS: the IB coarse-grain relative error
  |Phi_IB - Phi_ground| / Phi_ground <= 0.15 at EVERY genuine-compression rung (N in {5,6,7,8}) AND
  the IB error is STRICTLY LESS than the random-macro-map control error at every such rung AND the IB
  error does NOT grow with N (the N=8 error is not the largest, i.e. error is flat or shrinking across
  the ladder, so the estimator extends past the exact big-Phi ceiling of n<=6). -> the IB coarse-grain
  is the scalable ruler's measurement core, validated to n<=8.
- H1 FAIL = NO principled scalable estimator at this fidelity: the IB error exceeds 0.15 at any
  genuine rung, OR grows with N, OR fails to beat the random control at any rung. -> the ruler cannot
  honestly extend past n<=8 yet at this fidelity (publishable closed-negative, a_paper_negative_ok);
  report the smallest epsilon the IB map DOES satisfy and whether it still beats random (a weaker but
  honest partial result).

## Honest scope (a_scale_honest_scope)
Validated to n<=8 ONLY -- the ground truth is exact faithful phi_EI which is exact only for n<=8, so
the ladder cannot exceed N=8 (there is no exact reference to validate against beyond it). Real-model
fidelity is UNVERIFIED and gates the macro-IIT honesty hypotheses H_1038/H_1042. The toy WM latent is
the substrate; production-scale transfer is UNVERIFIED (a_toy_scale_recheck). g5 CODE-measured (no LLM
self-judge, p7). NOT a forge binary; pure-CPU $0. The IB macro-map is the H_1037/H_1038 majority-vote
coarse-grain with a future-predictive (information-bottleneck) group-selection rule; the random control
isolates whether the IB selection rule (not merely the act of coarse-graining) is what preserves Phi.

## RESULT (🔴 CLOSED-NEGATIVE — NO-VALIDATED-ESTIMATOR; measured, g5 CODE)
Mirror == stdlib RE-PROVEN before scoring: faithful_phi n4 nb2 |Delta|=3.48e-10, n4 nb4 |Delta|=3.75e-06,
n5 nb2 |Delta|=7.97e-10 (all OK); coarse-grain read deterministic (|Delta|=0). 30 seeds, m=4 macro fixed.

   N | Phi_ground(EXACT) | Phi_IB  | Phi_topvar | Phi_rand | errIB  | errTV  | errRand
   4 |     2.84017       | 2.84017 |  2.84017   | 2.84017  | 0.0000 | 0.0000 | 0.0000  (identity rung m==N)
   5 |     3.67301       | 2.78618 |  2.24790   | 1.61131  | 0.2414 | 0.3880 | 0.5613
   6 |     4.24366       | 2.65719 |  2.60715   | 1.29860  | 0.3738 | 0.3856 | 0.6940
   7 |     4.60955       | 2.59640 |  2.30486   | 1.19607  | 0.4367 | 0.5000 | 0.7405
   8 |     5.07632       | 2.50453 |  2.46186   | 1.05677  | 0.5066 | 0.5150 | 0.7918

Falsifier (eps=0.15, genuine rungs N in {5,6,7,8}): [1] IB within eps = FALSE (all errIB > 0.15);
[2] IB beats random control = TRUE (errIB ~2x lower at every rung); [3] error not growing with N =
FALSE (errIB strictly monotone 0.24->0.51). PASS needs all three -> NO-VALIDATED-ESTIMATOR.

DOES A VALIDATED SCALABLE ESTIMATOR EXIST? NO at this fidelity. Smallest eps the IB map satisfies at
every genuine rung = 0.5066 (3.4x the pre-reg 0.15). PARTIAL honest positive: the IB SELECTION rule is
principled-better than chance (strictly beats random everywhere; beats top-var at N=5,6,7).

MECHANISM: exact faithful phi_EI scales ~LINEARLY with the unit count (Phi_ground 2.84->5.08 as N 4->8;
near-fully-coupled binarized traces -> MIP min-cut/small-side saturates near n-1). A FIXED m=4 coarse-
grain structurally caps the estimate near m-1~3, so relative error grows ~ (N-m)/(N-1) with the
compression ratio. A fixed-small-m IB grain cannot track a Phi that lives in the unit count itself.
This RED gates/bounds the macro-IIT honesty hypotheses H_1038/H_1042. Validated n<=8 only.
