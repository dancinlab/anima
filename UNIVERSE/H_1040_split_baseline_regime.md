# H_1040 — Which baseline regime predicts the big-Phi-DOWN half? (H_1033 residual)

Status: PRE-REGISTERED (generation-only; not yet measured)
Lane: zero-cost CPU toy. Engines: stdlib faithful_phi + iit4_bigphi (a_phi_iit4_tool, no proxy).

## Hypothesis
H_1033 (prior INCONCLUSIVE-DEGENERATE-FAMILY) found the big-Phi-DOWN half of the planning split
does NOT reproduce on ANY matched independent-bits baseline task (0/5) — ruling out generic
decomposability/modularity as the cause. Its deferred next step: the sign is dominated by the
BASELINE CONTRAST, not the intervention's task structure. So vary the BASELINE REGIME (not the
task) and find which baseline makes big-Phi go DOWN.

## Method (sketch)
- Hold the planning intervention fixed; sweep the baseline regime: (a) independent-bits
  (H_1033's baseline), (b) pre-rollout latent (the model's own state BEFORE planning), (c)
  shuffled-time, (d) matched-marginal correlated baseline.
- For each baseline, compute the planning-vs-baseline big-Phi contrast + faithful contrast,
  30 seeds, Cohen d, sign.

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = there EXISTS a principled baseline regime (named a priori: the pre-rollout latent)
  under which big-Phi goes DOWN with d <= -0.8 AND faithful goes UP, AND at least one other
  baseline does NOT (so the DOWN half is baseline-regime-specific, not universal) -> the split
  is a planning-vs-(pre-rollout-latent) property, pinning the H_1033 residual.
- H1 FAIL = big-Phi-DOWN appears under NO baseline regime, or under ALL of them -> the DOWN half
  is either non-existent or regime-independent; H_1033's degeneracy is structural, not a baseline
  choice (publishable closed-negative, a_paper_negative_ok). State the d threshold + which
  baseline is the a-priori pick before running.

## Honest scope (a_scale_honest_scope)
Toy n<=5 (matches H_1033); production-scale UNVERIFIED. Re-prove CPU mirror == stdlib at n=4,5
before scoring. g5 CODE-measured (p7).

## Verdict
PENDING — tier added only AFTER `.verdicts/1040_split_baseline_regime/H_1040.txt` lands (g73).
