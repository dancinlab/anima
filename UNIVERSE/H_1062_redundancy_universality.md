# H_1062 — redundancy-universality (generality test of H_1039's causal mechanism)

**Status: PRE-REGISTERED (falsifier + FROZEN thresholds locked BEFORE scoring).**
substrate = CPU-mirror (numpy), stdlib IIT-4.0 engines (h1004), $0 CPU, 0-pod.

## Background
H_1039 (prior REDUNDANCY-CAUSAL, GREEN) established that Williams-Beer (WB) redundancy CAUSALLY
drives the planning Phi-sign-split (faithful phi_EI UP / big-Phi DOWN): de-redundifying the
planning channels via ZCA / Gram-Schmidt (>=97% Dred cut) COLLAPSES the split while it
HOLDS on the matched control. **BUT that was demonstrated for PLANNING interventions ONLY.**

## Open question
Is redundancy the **UNIVERSAL** driver of the faithful-phi-UP / big-Phi-DOWN sign-disagreement,
or is the split **planning-SPECIFIC**? Test whether OTHER, non-planning interventions
that act on the same toy channel substrate ALSO produce a redundancy-gated sign-split.

## Design (reuse H_1039 / H_1017 harness UNMODIFIED)
Substrate = the GREEDY baseline latent matrix `Hg` from `h1004.planning_trajectories(seed,
depth)` (the NON-planning rollout; the planning ladder `Hp` is NOT used as a phi-intervention
here -- it is only reused for the reproduce-H_1039 check). For each NON-planning intervention
we transform the CONTINUOUS top-variance channel matrix (the exact channels
`_top_variance_channels` selects) BEFORE median-binarization, then measure
INTERVENTION-vs-BASELINE contrast (intervened reads - un-intervened baseline reads), 30 seeds.

Four NON-planning phi-raising interventions on the continuous channel matrix `X` (n_steps x n_units):
- **(i) ema** -- temporal-smoothing / recurrence: `X[t] <- a X[t] + (1-a) X[t-1]`, a=0.5 (induces temporal redundancy).
- **(ii) gain** -- logit-temperature / sharpening: `X <- tanh(g * zscore(X))`, g=2.5 (per-channel sharpen).
- **(iii) pool** -- attention-style channel pooling: `X <- (1-b) X + b * mean_over_channels(X)`, b=0.5 (cross-channel mixing).
- **(iv) lowrank** -- low-rank mixing: `X <- X @ M`, `M = (1-c) I + c (11^T/k)`, c=0.6 (shared rank-1 component).

For EACH intervention vs its matched (un-intervened) baseline, measure:
- (a) sign-split: faithful phi_EI direction (UP iff contrast > +SIGN_EPS) vs big-Phi direction
  (DOWN iff contrast < -SIGN_EPS); `SPLIT present iff (faith UP AND big DOWN)`.
- (b) WB I_min redundancy-margin it induces (the H_1017/H_1039 PID Dred -- an
  intervention-VALIDATION variable, **NOT a Phi proxy**; Phi from stdlib mirrors only).
- (c) de-redundify (ZCA primary + Gram-Schmidt robustness, H_1039 operators UNMODIFIED)
  applied to the intervened channels -> does the split COLLAPSE (SPLIT->False)?
- Cross-intervention: does the redundancy-margin RANK-PREDICT split magnitude
  ACROSS all interventions (Spearman rho)? Split magnitude = `faith_contrast - big_contrast`
  (large positive when faithful-UP & big-DOWN together; the signed split size).

## Engines (a_phi_iit4_tool -- NO proxy)
faithful phi_EI + big-Phi via the stdlib IIT-4.0 CPU mirrors (h1004), RE-PROVEN == stdlib EXACT
6dp at n=4 AND n=5 (h1012.prove_mirrors_at_n) BEFORE scoring. MI in BITS:
MI = H(A)+H(B)-H(A,B), log2 (H_1043 nats-bug lesson). WB PID = Williams-Beer (2010) I_min,
exact pure-numpy on the SAME bits -- the intervention-validation variable, NOT a Phi proxy
(H_1039 lesson). n<=5; big-Phi scored at n=4 EXACT (super-exponential); n=5 mirror-proven.

## FROZEN thresholds (locked before scoring -- NO goalpost move)
- `SIGN_EPS = 1e-3` (sign-eps; same as H_1039).
- split-def: `SPLIT present iff (faith_contrast > +SIGN_EPS) AND (big_contrast < -SIGN_EPS)`.
- `RED_REDUCTION_THRESHOLD = 0.20` -- de-redundify removes redundancy iff
  `|Dred_dered| <= 0.20*|Dred_intervention|` (>=80% cut), per intervention (H_1039 verbatim).
- `SPEARMAN_BAR = 0.7` -- cross-intervention redundancy->split-magnitude Spearman rho >= 0.7
  required for "redundancy rank-predicts split across interventions".
- `N_SEEDS = 30`, `PLAN_DEPTH = 8` (only for the reproduce-H_1039 check), Cohen-d reported.

## PRE-REGISTERED FALSIFIER (frozen; TEXT tokens only)
**H1-UNIVERSAL = REDUNDANCY-UNIVERSAL** iff ALL of:
1. the sign-split appears in **>=2** non-planning interventions, AND
2. in EACH split-bearing intervention, de-redundifying (ZCA primary, GS robustness
   consistent) COLLAPSES the split (SPLIT->False) while removing >=80% of the Dred, AND
3. the redundancy-margin RANK-PREDICTS split magnitude across ALL interventions
   (Spearman rho >= SPEARMAN_BAR = 0.7).
-> redundancy is the UNIVERSAL split driver, not planning-specific.

**H1 FAIL = SPLIT-IS-PLANNING-SPECIFIC** (closed-negative, a_paper_negative_ok) iff ANY:
- the split is ABSENT in the non-planning interventions (<2 show it), OR
- de-redundifying does NOT collapse it where present, OR
- redundancy does NOT rank-predict split across interventions (Spearman rho < 0.7).
-> H_1039's redundancy-causal claim is BOUNDED to planning; the split is planning-specific.

Report the per-intervention {split? · de-redundify-collapses? · induced Dred} table AND
the cross-intervention Spearman rho vs 0.7 EITHER WAY. NO goalpost move.

## Guards / constraints
- REUSE `h1039_redundancy_causal.py` (_zca_whiten, _gram_schmidt, _binarize_median,
  _top_variance_channels, pid_system, substrate_reads-style) + h1004 engines + h1012 mirror
  prover, all by REAL MODULE NAME (no importlib custom-name; H_1038 fork-unpickle lesson).
- reproduce-H_1039 check BEFORE scoring: planning split holds on control (faith UP / big-Phi DOWN)
  AND de-redundify (ZCA) collapses it -- confirm the harness reproduces H_1039.
- p3/p6/p7: generic toy channel substrate, no persona. SERIAL only -- NO multiprocessing.Pool;
  `if __name__`-guard. 30 seeds, FROZEN thresholds.
- a_scale_honest_scope / a_toy_scale_recheck: TOY n<=5 rung; production scale UNVERIFIED. g5 (p7).
- $0 CPU-local, 0 GPU, 0 pod.

## Artifacts
- `UNIVERSE/h1062_redundancy_universality.py`
- `.verdicts/1062_redundancy_universality/H_1062.txt` (raw stdout: mirror n4,5 + reproduce-H_1039
  + per-intervention table + cross-intervention Spearman + FROZEN thresholds + PASS/FAIL).

xref: h1039-redundancy-causal · phi-measure-dependence-paper
