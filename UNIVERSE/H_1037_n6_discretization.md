# H_1037 — does discretization-invariance of the planning Phi sign-split ALSO hold at n=6 EXACT?

Follow-up of H_1024 (SIGN-DISCRETIZATION-INVARIANT, 6/6 binnings @ n=4) and H_1022
(SPLIT-PERSISTS-N6+, the split STRENGTHENS through n=6 EXACT for the single median binning).

## Hypothesis

H_1024 established (at toy n<=5, scored at n=4) that the planning-induced sign-disagreement
— faithful phi_EI RAISES the MIP-EI scalar while system big-Phi LOWERS Phi_s — survives all
six binning schemes (nb in {2,3,4} x {equal_width, quantile}). H_1022 established the split
STRENGTHENS through n=6 EXACT (Cohen d -1.83@n4 -> -2.28@n5 -> ~-3.60@n6) but ONLY for the
single median (nb=2/quantile) discretization. Residual question this rung closes:

  does discretization-invariance ALSO hold at n=6 EXACT?

We re-run the H_1024 6-binning robustness sweep at n=6 EXACT, using the H_1022 many-core
exact big-Phi machinery (360 EXACT big-Phi+faithful evals = 6 binnings x 30 seeds x 2
conditions, fanned over all pod cores).

## Method

- Substrate, world-model, planning(depth-8) vs GREEDY generator: H_1024 / H_1012 / H_1004 VERBATIM.
- Engines: real stdlib IIT-4.0 — big-Phi = `hexa-lang/stdlib/consciousness/iit4_bigphi.hexa`
  (system Phi_s over the MIP); faithful_phi = `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`
  (MIP-EI scalar) — via their h1004 CPU mirrors, RE-PROVEN == stdlib at n=4 AND n=5 BEFORE
  scoring (`prove_mirrors_at_n`, H_1012 discipline). NEVER a proxy (a_phi_iit4_tool).
- The ONLY thing that varies: the discretization grid (nb in {2,3,4} x {equal_width, quantile}),
  PRE-FROZEN, no post-hoc selection. Each top-variance channel -> nb ordered levels by scheme
  -> binary node bit = (level >= ceil(nb/2)) -> ONE binary sequence -> BOTH engines.
- 30 seeds per binning (matches H_1012/H_1017/H_1024). n=6 EXACT (both engines exact).
- Pickling fix vs the original H_1022 run: engines imported under their REAL module names
  (proper sys.modules entries) + forced 'fork' start method, so forked Pool workers re-find
  the engine functions (the original h1022 log showed `Can't pickle ... import of module
  'h1022' failed`).

## Pre-registered falsifier (frozen before scoring; TEXT tokens only)

Per-scheme sign criterion (the EXACT criterion, stated before running): a binning PRESERVES
the sign-disagreement at n=6 iff the planning(depth-8) - GREEDY contrast has
faithful_phi sign == UP (contrast > +eps) AND big-Phi sign == DOWN (contrast < -eps),
with eps = 1e-3 (the H_1024 signword convention). A scheme FLIPS if that joint condition
fails (either measure NULL, or the wrong sign).

- H1 PASS = at n=6 EXACT the sign-disagreement (faithful phi_EI RAISES, system big-Phi
  LOWERS for planning vs greedy) holds for ALL 6 binning schemes -> 6/6 schemes preserve
  the sign-disagreement at n=6 -> discretization-invariance CONFIRMED AT SCALE.
- H1 FAIL = ANY scheme flips -> the n<=5 invariance was a small-n artifact (publishable
  closed-negative, a_paper_negative_ok).

## Honest scope (a_scale_honest_scope)

n=6 is the LARGEST EXACT rung; n=7 EXACT is INFEASIBLE-CAP (the 2^(n-1) MIP bipartition
search + super-exponential distinction set explode; H_1022 used a SAMPLED MC big-Phi
estimator at n=7, validated |Delta|=0.0000 at n<=5). Verdict scoped to n<=6 EXACT. g5
CODE-measured (no LLM self-judge, p7). Pure-CPU exact, NOT a forge binary.

## Verdict

PENDING — verdict tier added here only AFTER `.verdicts/1037_n6_discretization/H_1037.txt`
lands (verdict-gate g73).
