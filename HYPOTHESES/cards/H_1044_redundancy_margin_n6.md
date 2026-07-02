# H_1044 — Does the redundancy-margin predictor hold at n=6 EXACT? (H_1020 robustness ladder)

Status: PRE-REGISTERED (generation-only; not yet measured)
Lane: GPU / many-core pod rung (n=6 EXACT big-Phi; a_fire_autonomous). Engines: stdlib
faithful_phi + iit4_bigphi + Williams-Beer I_min PID (a_phi_iit4_tool, no proxy).

## Hypothesis
H_1020 (prior GREEN) established the redundancy-margin predictor (planning's PID redundancy-margin
+25.07 vs controls <=+7.48) is ROBUST at n=5, where the SURFACE coupling-magnitude predictor
(H_1014/H_1016) is only an n=4 artifact. H_1037 just extended the SIGN-SPLIT itself to n=6 EXACT
(6/6 binning). This closes the matching gap for the PREDICTOR: does the redundancy-margin predictor
ALSO survive at n=6 EXACT, or does it (like the coupling predictor at n=4->5) decay one rung up?

## Method (sketch)
- Reuse the H_1037 n=6 EXACT many-core harness (96-core pod) + the H_1020 PID redundancy-margin
  computation. For planning vs controls at n=6, compute the Williams-Beer I_min redundancy margin
  + the surface coupling-magnitude predictor, 30 seeds, on the same EXACT substrate.
- Re-prove CPU mirror == stdlib at n=4,5 before scoring (as H_1037 did).

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = at n=6 EXACT the redundancy-margin predictor still SEPARATES planning from all controls
  (planning margin > max control margin + a pre-set gap) -> the redundancy-margin predictor is
  robust through n=6, strengthening the H_1020 result into a >=3-rung (n=4,5,6) ladder.
- H1 FAIL = at n=6 the redundancy-margin predictor NO LONGER separates planning from controls ->
  it was an n<=5 artifact like the coupling predictor was at n<=4 (publishable closed-negative,
  a_paper_negative_ok). Also report whether the coupling predictor stays dead at n=6. State the
  separation gap before running.

## Honest scope (a_scale_honest_scope)
n=6 = largest EXACT rung; n=7 infeasible-cap. Toy n-ladder; production-scale UNVERIFIED. Shares the
H_1037 operational lessons (orphan-pod survival, inline-poll babysit, mandatory teardown).

## Verdict
PENDING — tier added only AFTER `.verdicts/1044_redundancy_margin_n6/H_1044.txt` lands (g73).
