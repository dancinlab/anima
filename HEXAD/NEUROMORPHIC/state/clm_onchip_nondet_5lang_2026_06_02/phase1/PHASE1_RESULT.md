# Lane A Phase-1 — Lift Signal Resolution (live AKD1000)

**Question.** The prior N-unit paged depth ladder (commits 90b29bcb6/a9e54140d/7d7a4d999)
found the representational LIFT (composed-all-units margin − frozen-head-L1-only margin,
in cross-lingual concept bits) was a NOISE-LIMITED weak-positive at 25 anchors (per-seed
slope +0.15..+0.43 but sign-unstable per N). **Does it survive past the noise floor at 10× corpus?**

**Method.** IDENTICAL paged depth ladder mechanism + IDENTICAL `concept_margin` metric as the
prior script (one FC unit chip-resident at a time on the live AKD1000, page weights off to host,
binarize, next unit; composed = every unit `fit()`s on chip, frozen_head = only L1 fits). Only
the corpus size and seed count vary. 3 backbone seeds {20260602,20260603,20260604}, N∈{2,3,4,5}.

**Corpus.** 25-anchor = the prior toy corpus (5 concepts × 5 langs). Big = **250 anchors
(50 concepts × 5 langs)**, a subsample of the FULL FLORES-200 dev+devtest 5-way line-aligned
parallel build (CC-BY-SA-4.0, 2009 concepts available; source
`hexa-lang-clm-h911-scale/testdata_prod/parallel.limen`). REAL data, not synthetic, not scraped.
Limen sha256 `cdb1fdb926ee3326…`.

**Device (verbatim).** akida 2.19.1 · device BC.00.000.002 · IpVersion.v1 · pi5-akida. NO sw fallback.

## Side-by-side lift (composed − frozen, bits), per-N mean [min..max] std over 3 seeds

| N | 25-anchor mean [band] std · signstable | 250-anchor mean [band] std · signstable |
|---|---------------------------------------|-----------------------------------------|
| 2 | +0.029 [−0.296..+0.480] 0.329 · **UNSTABLE** | −0.837 [−1.036..−0.643] 0.160 · stable− |
| 3 | −0.587 [−0.920..−0.296] 0.257 · stable− | −0.773 [−0.981..−0.408] 0.259 · stable− |
| 4 | −0.192 [−0.760..+0.320] 0.443 · **UNSTABLE** | −0.883 [−0.897..−0.871] 0.011 · stable− |
| 5 | −0.515 [−1.392..−0.032] 0.621 · stable− | −0.811 [−1.119..−0.217] 0.420 · stable− |

- mean per-N seed band (std): **25-anchor 0.4124 → 250-anchor 0.2125 (shrank ~2×)**
- within-seed OLS slope of lift vs N: 25-anchor mean −0.124; **250-anchor mean −0.003 (flat, NOT positive)**
- all 24 rungs (2 sizes × 4 N × 3 seeds) `learned_hw=True` — capacity GREEN holds at 10×.

## Verdict: **COLLAPSE-NULL**

At 10× corpus the seed band shrinks ~2× and the lift becomes **sign-stable NEGATIVE at every N**
(composed margin is *worse* than frozen-head), with a flat (~0) depth slope. The prior 25-anchor
weak-positive slope was a **small-sample artifact** of the 0.41-bit noise floor. With the noise
floor halved, no positive representational lift emerges — composition adds depth CAPACITY (every
paged unit learns on silicon) but **no cross-lingual representational lift**; deeper on-chip
plasticity on the paged units slightly *degrades* the concept margin relative to a single learned head.

## Lane A strategy implication

The paging primitive **composes capacity-only, with no representational lift** at this depth on
the last-FC-plastic mechanism. Do NOT proceed to P2 (depth+width) expecting composition to buy
cross-lingual representation for free — last-FC-only on-chip plasticity per paged unit does not
build composed cross-lingual structure; the deeper units re-binarize away the L1 head's linkage.
A genuine lift requires changing the mechanism (feature-level plasticity beyond last-FC, or a
linkage-preserving inter-unit map), not merely more anchors or more depth.
