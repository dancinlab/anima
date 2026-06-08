# H_1047 — Declared-objective PAIR ruler: does the (faithful, big-Phi) PAIR predict behavior where a collapsed scalar cannot?

status: PRE-REGISTERED (TEXT tokens only; no emoji; verdict tier assigned AFTER the .txt lands, verdict-gate g73)
id: H_1047
slug: pair_ruler
sub-domain: consciousness ruler (constructive)
substrate: CPU-local numpy mirror of stdlib IIT-4.0 (a_phi_iit4_tool, NO proxy); $0; serial.

## Lineage (prior MEASURED results, no emoji per g73)
- H_1029 (prior GREEN, OBJECTIVE-HAZARD-REAL): maximizing faithful_phi vs big-Phi selects DIVERGENT
  policies on a small depth-only set (faithful -> deliberate depth-2, big-Phi -> greedy).
- H_1035 (prior GREEN, HAZARD-ROBUST-CONFLICTING): on the RICHER policy space (depth x explore x mix
  = 30 policies x 30 seeds) the two objectives STAY divergent; NO both-maxing policy exists; the
  alpha-sweep optimum MOVES and the Pareto front holds >=2 non-dominated policies. Genuine trade-off,
  Pareto front = the two corners (deliberate / greedy).
- H_1037 (prior GREEN, DISCRETIZATION-INVARIANT-AT-SCALE): the faithful-UP / big-Phi-DOWN planning
  split survives all 6 binning schemes at n=6 EXACT.

## Constructive claim
If the two Phi measures genuinely max OPPOSITE policies with no both-maxer (H_1035), then COLLAPSING
the (faithful, big-Phi) pair to a single scalar must DESTROY behaviorally-predictive information: two
policies that differ in what they DO (behavioral class) can land on the SAME collapsed scalar while
remaining separable in the 2-D pair. An honest consciousness ruler must therefore report the
(faithful, big-Phi) PAIR plus its Pareto-front position, not a single number.

## Reused substrate (verbatim, no reinvention) — a_phi_iit4_tool
- The SAME H_1035 richer policy harness: rich_rollout(seed, depth, explore, mix) on the H_1004
  LatentWorldModel (fit_engine + roll_latent + encode_seq), imported through the H_1014 driver.
  REPRODUCE-H_1029 EXACT check at (explore=0.05, mix=0.0) runs before scoring (inherited).
- BOTH stdlib IIT-4.0 engines as the measures, NO proxy: big-Phi = stdlib iit4_bigphi.hexa (system
  Phi_s); faithful = stdlib iit4/faithful_phi.hexa (MIP-EI scalar). Both CPU mirrors RE-PROVEN ==
  stdlib at n=4 AND n=5 (H_1012 prove_mirrors_at_n) BEFORE scoring; the proof lines are pasted into
  the verdict .txt verbatim.
- FROZEN policy space (inherited from H_1035, NOT rewritten): depth {0,1,2,4,8} x explore {0.00,0.05,
  0.20} x mix {0.0,0.5} = 30 policies, N_SEEDS=30. Per policy we compute the (faith_mean, big_mean)
  pair over the 30 seeds.

## FROZEN behavioral-class labels (declared BEFORE measuring; structural, measure-INDEPENDENT)
Each policy's behavioral CLASS is read from its policy STRUCTURE (what it DOES), never from a Phi value:
- class GREEDY     iff depth == 0                         (reactive, no deliberation)
- class MIXED      iff mix > 0.0 AND depth >= 1           (greedy/plan blend; realized behavior interpolates)
- class DELIBERATE iff mix == 0.0 AND depth >= 1          (pure multi-step plan rollout)
This is a clean 3-way partition of the 30 policies (6 GREEDY [depth=0, any explore/mix],
12 MIXED [mix=0.5, depth in {1,2,4,8}, any explore], 12 DELIBERATE [mix=0.0, depth in {1,2,4,8}, any
explore]). The class is the prediction TARGET.

## FROZEN feature spaces
- PAIR (2-D): (faith_norm, big_norm), each min-max normalized over the 30 policies.
- COLLAPSED scalars (1-D), the candidates a single-number ruler could report:
    s_mean   = 0.5*faith_norm + 0.5*big_norm   (equal-weight mean == fixed-alpha scalarization at alpha=0.5)
    s_faith  = faith_norm                        (report faithful only)
    s_big    = big_norm                          (report big-Phi only)
  The "best single collapsed scalar" = the one of {s_mean, s_faith, s_big} with the HIGHEST 1-D
  classifier accuracy (best case FOR the scalar; we must beat its BEST, not its worst).

## FROZEN classifier (deterministic, leakage-free, $0)
Leave-one-out (LOO) nearest-CENTROID classification.
- For each held-out policy i: compute the per-class centroid of the OTHER 29 policies in the feature
  space, assign i to the nearest centroid (Euclidean). Accuracy = fraction of the 30 correctly classified.
- 2-D pair accuracy uses the 2-D centroids; each 1-D scalar accuracy uses that scalar's 1-D centroids.
- Fully deterministic (no random split, no training RNG): same inputs -> same accuracy. g5 CODE-measured (p7).
- Ties in centroid distance broken by lower class index (GREEDY<MIXED<DELIBERATE) — frozen, deterministic.

## FROZEN scalar-collision test (the "collapse loses them" leg)
A COLLISION = a pair of policies (a,b) with DIFFERENT behavioral class but |s(a)-s(b)| <= COLLIDE_EPS
on the BEST collapsed scalar, while their 2-D pair distance > COLLIDE_EPS (the pair still separates them).
COLLIDE_EPS = 0.05 (on the [0,1]-normalized scale). FROZEN.

## Pre-registered falsifier (declared BEFORE measuring)
- MARGIN = 0.15 (pre-set, absolute accuracy points on the [0,1] scale). FROZEN.
- H1 PASS = PAIR-STRICTLY-MORE-PREDICTIVE :
    (acc_2D_pair  >=  best_acc_1D_scalar + MARGIN)  AND  (>=1 scalar-collision exists per the test above).
  -> the 2-D pair (plus Pareto position) predicts the behavioral class strictly better than ANY single
     collapsed scalar, AND there exist behaviorally-distinct-but-scalar-identical policy pairs that the
     collapse loses. The pair ruler is strictly more behavior-predictive.
- H1 FAIL = SCALAR-SUFFICIENT :
    best_acc_1D_scalar + MARGIN > acc_2D_pair  (the collapsed scalar predicts behavior just as well,
    within the margin)  OR  no scalar-collision exists. -> the pair adds no behavioral information over
    a single number (publishable CLOSED-NEGATIVE, a_paper_negative_ok).

## Discipline
- a_phi_iit4_tool: stdlib faithful_phi + iit4_bigphi EXACT n<=5; mirror RE-PROVEN == stdlib at n=4 AND
  n=5 before scoring (pasted into the .txt). NO proxy. real-module import (the H_1014 driver is exec'd
  verbatim; no importlib custom-name path for the engines). SERIAL.
- p6 (no fine-tuned ethics) + p7 (no perplexity verdict). g5 CODE-measured (no LLM self-judge).
- a_scale_honest_scope / a_toy_scale_recheck: TOY n=4 system size for the per-policy Phi reads (big-Phi
  super-exponential); n=5 used ONLY for the mirror re-proof. Production-scale transfer UNVERIFIED.
- verdict-gate g73: raw measurement lands in .verdicts/1047_pair_ruler/H_1047.txt BEFORE any emoji tier
  is written onto this .md. $0 CPU-local, poll inline (never Monitor for the science).
