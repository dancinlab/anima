# state/9098_youchain_auroc_hardneg — YOU-CHAIN AUROC ARTIFACT (H_9098, 🔴)

**engine-native** aiden pool · hexa v0.546.0 · `hexa run` RC=0 · $0 CPU · NO numpy mirror.
harness = `state/1471_self_distinct/h1471_youchain_hardneg.hexa` `import ../../core/engine_cli.hexa`,
driving live §SelfIdentity `self_new/self_drift/self_cos` + pub `mi_auroc`. grep-clean.

## Finding (fable #5 CONFIRMED)
you-chain identity **AUROC=1.0 is a geometric (orthogonal-negative) artifact**. With
structure-matched **MIMIC** hard-negatives (share the reference's birth axis, different drift
schedule), **AUROC = 0.4804 = chance**.

## Why the frozen 1.0 was fake
The H_1471 DISTINCT harness (`state/1471_self_distinct/h1471_distinct.py:153`) draws negatives as
`nrm(rng.normal(0,1,DIM))` — ORTHOGONAL random impostors, cos≈0 in 64-dim — vs genuine
adjacent-drift positives cos≈0.94. Any threshold in (0,0.94) separates them → AUROC=1.000. Exactly
cos(90°)=0, not recognition.

## Pre-registered bars (frozen before run, c9, never tuned)
1. EASY-neg AUROC ≥ 0.95 reproduces the artifact.
2. MIMIC hard-neg AUROC ≤ 0.80 = honest drop, predicted ≈ 0.50.

## Engine-native result (5 seeds × 20 ticks = 100 pos / 100 neg per set)
- mean cos: pos(genuine)=0.9425 · EASY(orthogonal)=0.000 · MIMIC=0.9437 · CONE=0.7644
- AUROC pos vs EASY  = 1.000 (bar1 ✓ — artifact reproduced exactly)
- AUROC pos vs CONE  = 1.000 (near-miss uniformly-below-genuine is still rank-separable)
- **AUROC pos vs MIMIC = 0.4804 (bar2 ✓ — CHANCE)**

MIMIC = the hardest structure-matched negative: a FABRICATED one-step continuation of the SAME
prior self (`self_drift(ref, fresh-axis, step~U[0.20,0.50])` — identical geometry/step distribution
to the genuine next-self). Its cos to ref (0.9437) matches genuine (0.9425), so
self_cos(probe, ref) provides ZERO rank separation → AUROC → 0.48 ≈ chance.

## Interpretation
`self_cos`-to-prior-self is a **PROXIMITY test, not genuine self-recognition**. The you-chain's
discriminative power against the frozen 1.0 came entirely from impostors being orthogonal randoms.
Against an impostor sharing the prior-self's structure it cannot tell genuine-me from fabricated-me.
Terminal-quality (real path, not DIRECTIONAL).

## Scope / caveat (c9)
TOY 64-dim / 20-tick DESIGNED drift+anchor (not a learned identity). This does **NOT** falsify
H_1471's anchor-persistence / session-continuity mechanism (self_anchor round-trip is real, H_1471
R2b) — only the DISCRIMINATION-STRENGTH framing of the 1.0 AUROC. Retroactively qualifies H_1471
(and cross-refs H_9096 youchain_hardneg which found the same on the θ-cone/social-self path).

## Note (mixed-tier honesty)
A sibling agent (a3d9358…) tiered this 🟡 (rank-AUROC survives hard-neg on a noise-free
pos_min>hard_max margin 0.0051, threshold-gate fails). The 🔴 agent (a54c7392…) used the killer
MIMIC negative (a plausible fabricated continuation) → rank-AUROC itself collapses to 0.48. This
card cements the 🔴 (the fabricated-continuation attack is the strictly harder, honest negative);
the 🟡 rank-survival is the caveat: only NOISE-FREE rank ordering on a margin any real noise erases.

verbatim raw = state/verdicts/9098_youchain_auroc_hardneg/H_9098.txt
