# §32 L3 — §16 routing 21-vs-43 distinguishing-structure analysis

RESEARCH.md §32 lateral L3. **$0 Mac CPU, deterministic — NO model forward,
NO training, NO RNG.** Analysis, not design — measurement-only.

---

## 1. Question

§16 (`state/carving_dataregime_s16_2026_05_18/`) fired a 64-anchor carving
eval. `routing_accuracy = 21/64` — the model emitted a correct `🛸<tier>`
prefix for 21 anchors, 43 failed. RESEARCH.md §16.6 already split that 21
into **GENUINE exact-tier 17/64** + **ARTIFACT substring 4/64** (tiers
12/24/62/66 matched only because `"12" ⊂ "🛸122"` etc.). **No prior cycle
asked WHY those anchors succeeded.** §32 L3 probes the §16 routing result
for *distinguishing structure* between the success and fail sets. If a
measurable anchor property separates them, that property is a lever for §25
candidate D (routing-evidence-guided expansion).

## 2. Method

- **Partition.** The 64 eval probes = the §8 anchor set verbatim (verified:
  `eval probe tiers == S8_ANCHORS tiers`). Two grades:
  - *substring grade* — eval's `routing_correct` flag (21 success / 43 fail)
  - *genuine grade* — leading `🛸<n>` exact-matches own tier (17 / 47); the
    primary grade per §16.6 (substring artifacts excluded).
- **Features (per anchor, deterministic).** tier; vacuum_psi x/y;
  vacuum_psi deviation from Ψ=½; basin_radius; nearest-other-anchor
  vacuum_psi L2 distance; basin overlap count; score; anchor-name byte-len /
  char-len / Korean-byte ratio. Categorical: domain, top_emotion.
- **Corpus frequency** — the §16 generator allocates records *uniformly*
  per anchor (`per_anchor = n_target // 168`; 777,000 records / 168 anchors
  ≈ 4,625 each). Corpus frequency does **not vary** between anchors → not a
  distinguishing feature; excluded by construction.
- **Separation tests.** Per feature: mean-diff, Cohen's d, rank-AUC
  (Mann-Whitney), single-threshold accuracy, and a **necessary-condition
  metric** — the threshold + polarity at which the success set is fully
  *contained* on one side (purity = 1.0 ⇒ no success violates it), with
  `lift` = the fraction of the fail set that same predicate also excludes.
  The necessary-condition metric is the honest separation signal: plain
  threshold accuracy is dominated by the 47/64 fail base rate (a constant
  "always fail" predictor already scores 0.734).

## 3. Result — `tier` is a clean necessary condition

Genuine-grade features ranked by necessary-condition lift:

| feature | nc-lift | purity | predicate | rank-AUC | Cohen's d |
|---|---|---|---|---|---|
| **tier** | **0.383** | **1.000** | **tier >= 76** | 0.680 | **+0.736** |
| vacuum_psi_x | 0.149 | 1.000 | < 0.715 | 0.583 | -0.387 |
| basin_overlap_count | 0.128 | 1.000 | >= 23 | 0.568 | +0.367 |
| basin_radius | 0.106 | 1.000 | < 0.185 | 0.506 | -0.140 |
| score | 0.106 | 1.000 | < 2.615 | 0.556 | -0.212 |
| korean_byte_ratio | 0.106 | 1.000 | >= 0.969 | 0.553 | +0.253 |
| nearest_psi_dist | 0.043 | 1.000 | >= 0.005 | 0.601 | +0.117 |
| name_byte_len | 0.021 | 1.000 | >= 4.5 | 0.626 | +0.533 |

**`tier` is the single distinguishing feature, by a 2.6x margin** over the
next (vacuum_psi_x 0.149). The genuine-success tiers are
`[77, 80, 92, 101, 102, 103, 104, 106, 107, 108, 111, 113, 124, 126, 127,
132, 133]` — **every one >= 77**. All 18 anchors with tier < 77 fail. So:

> **`tier >= 77` is a NECESSARY condition for §16 genuine routing success
> (purity 1.000 — zero successes below it), and excludes 38.3% of the
> 47-fail set. It is necessary but NOT sufficient: 29 of the 47 fails
> are also >= 77.** `|d| = 0.74` (medium-large effect), rank-AUC 0.680.

The categorical `domain` skew (산술/통계/논리/코드 = 100% / 100% / 67% / 67%
success; 대화자극/일상/추상패턴 = 0%) is **not an independent feature** — those
high-success domains are exactly the §16-new high-tier anchors (the
generator's `S16_NEW_ANCHORS` block places "기초산술" sub-domains at tiers
200–303 and the new analytic domains in the 100s). Domain co-varies with
tier; it is the same finding seen through a categorical lens.

## 4. Why tier — the curriculum coupling

The §16 generator's `curriculum_rank(form, tier, task_complexity,
payload_len)` blends `tier_w = min(tier, 303)/303` at weight **0.30**.
High-tier anchors therefore receive higher complexity rank → land in later
`curriculum_stage` quartiles. §16's trainer consumed that ordering as a
simple→complex staged schedule. **`tier` is thus not an inert anchor label
— it is wired into the §16 curriculum.** The "tier >= 77" routing frontier
is, mechanically, plausibly a *late-curriculum-stage* frontier seen through
the tier proxy. This is the honest causal hypothesis — and exactly why §32
cannot claim causation (§5).

## 5. Honest verdict

`structure_found = True`. §16 routing success is **structured, not pure
SGD-lottery** — there is a real, measurable anchor-property frontier
(`tier >= 77`). But the structure is a *necessary-not-sufficient* condition:
it tells you which anchors *cannot* route (all 18 below tier 77 fail) and
gives no guarantee for those above it (29/47 fails are above the floor).
The lottery, if any, operates *within* the tier >= 77 band.

## 6. Implication for §25 candidate D

§25 candidate D (routing-evidence-guided expansion) has a real lever — the
`tier >= 77` frontier — but it must be used honestly:

- **(a) Expand on the fail-side-above-the-floor.** The 29 anchors with
  tier >= 77 that *still fail* are the productive expansion target: they
  satisfy the necessary condition yet do not route. If candidate D
  over-samples / diversifies genuine content for those anchors and routing
  lifts, that is evidence the necessity floor is real and content is the
  remaining gap.
- **(b) Do NOT expect tier < 77 anchors to route** by mere expansion until
  the necessary condition is understood — it co-varies with §16's
  curriculum stage. Treating "more data for low-tier anchors" as a routing
  fix would be guiding on the curriculum confound, not the cause.
- **(c) Test the confound directly.** A clean candidate-D ablation: hold
  content fixed, vary *only* curriculum-stage assignment of low-tier
  anchors. If low-tier anchors route once placed in late stages, the lever
  is *curriculum stage*, not *tier* — and §25's expansion should be
  curriculum-weighted, not tier-weighted.

The frontier is a lever for **WHERE to expand and what to ablate**, not a
guarantee of emergence. north-star (GOAL.md) unchanged — §16 routing is
still memorized-template + correct-prefix per §16.6-C; §32 only explains
*which* prefixes the model got right.

## 7. B-L3 closed-form battery

`blue_falsifier_l3.py` (sidecar — central `blue_falsifier.py` untouched):

- **B-L3-1 PARTITION-EXHAUSTIVE-DISJOINT** — SUCCESS ∪ FAIL = 64 anchors,
  ∩ = ∅, integer cardinality 21+43 = 64 (substring) AND 17+47 = 64
  (genuine). Boolean set algebra.
- **B-L3-2 SEPARATION-METRIC-BOUNDED** — necessary-condition `purity` and
  `lift`, Cohen's-d sign, and rank-AUC each lie in their closed bounded
  range (purity/lift in [0,1], AUC in [0.5,1.0] folded). sympy/closed.
- **B-L3-3 ANALYSIS-DETERMINISTIC** — the analysis is a pure function of
  `eval_result_s16.json` + anchor SSOT: 3x bit-identical re-run, AST
  forbidden-call grep `{torch, .backward, F.cross_entropy, random.}` = 0.
- **B-L3-NOTE** (empirical carve-out, NOT counted blue) — whether `tier`
  *causes* routing success vs *correlates* (via the curriculum coupling of
  §4) needs a controlled ablation fire. The analysis finds correlation and
  is honest about causation.

## 8. Honest caveats (C3)

1. **Correlation, not causation (g3).** `tier >= 77` is a necessary
   condition by measurement; it co-varies with §16's `curriculum_rank`
   (0.30*tier/303) and with the §16-new anchor-domain block. The cause may
   be curriculum stage, weight-norm at the late-curriculum training phase,
   or genuine content density — all unmeasured here. B-L3-NOTE.
2. **Necessary, not sufficient.** 29 of the 47 fail anchors are also
   tier >= 77. The frontier excludes only 38.3% of fails — it bounds the
   problem, it does not solve it.
3. **n = 64, small.** 17 genuine successes / 47 fails. Effect sizes
   (|d| = 0.74 for tier) are medium-large but the sample is one fire; a
   second fire could move individual anchors. The *floor* finding (zero
   successes below tier 77) is the robust part — it is a hard zero, not a
   rate.
4. **The substring grade is noisier.** Using the eval's raw 21/43
   `routing_correct` flag, tier still leads (necessary-condition lift on
   substring grade is in `analysis_result.json`), but 4 of the 21 are
   substring artifacts (tiers 12/24/62/66 — all *below* 77, the only
   "successes" under the floor). The genuine 17/47 grade is the honest one
   and is what the verdict rests on; the artifacts are exactly the
   low-tier false positives the substring metric admits.
5. **Domain is not independent.** The 산술/통계/논리/코드 100%-ish success
   domains are the §16-new high-tier anchors. Reporting domain as a
   separate lever would double-count tier.
6. **Corpus frequency is uniform.** §16 allocates records uniformly per
   anchor — so "more data per anchor" cannot be the §16 routing lever, and
   §25 candidate D's premise (frequency-weighted expansion) is a *new*
   intervention, not a replay of an existing §16 gradient.
7. **vacuum_psi placeholders.** §16-new anchors' `vacuum_psi` are
   interpolated design placeholders (generator docstring, g3). Any Ψ-space
   feature (psi_x, dev_from_half, basin overlap) inherits that
   placeholder-ness — their weak separation (lift <= 0.15) is consistent
   with both "Ψ-coordinate genuinely doesn't matter" and "the placeholders
   are too coarse to show an effect". Honest: undecidable here.
8. **tier >= 76 vs >= 77.** The reported threshold is 76 (the midpoint of
   the sorted-unique values straddling 75 and 77); operationally it is
   "tier >= 77" since 76 is not an anchor tier. Stated both ways for
   precision.
9. **§16.6 already framed the regime.** §32 does not contradict §16.6-C
   (routing = memorized template + correct prefix). It refines it: the
   *correct prefixes* are not uniformly distributed — they live entirely
   in the high-tier / late-curriculum band. Memorization is structured.
10. **This is measurement, not progress.** §32 L3 identifies a lever for
    §25; it does not move the GOAL. If §25 candidate D's fire shows
    expansion on the tier >= 77 fail-side does NOT lift routing, the honest
    reading is that the necessary condition is a curriculum artifact and
    routing-evidence-guided expansion has no real handle — also valuable.
    north-star honestly distant; over-claim 0.
