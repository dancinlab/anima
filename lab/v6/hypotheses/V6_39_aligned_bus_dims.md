<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_39 — the LANE-BUS premise re-read on an aligned bus: **PR = 1.19, the bus is a scalar** 🔴

**origin:** V6_26 is the gate that licensed the whole LANE-BUS engine — "context tension
(composed − reflex) effective rank **PR = 15.3** ⟹ the scalar servo discards ~15 dimensions of real
disagreement". V6_38 found the two lanes were scored on different target bytes, so the gate had to
be re-read. `v6_39_aligned_bus_dims.py`, $0, same model/corpus/estimator. DIRECTIONAL.

## Two independent defects, and both inflate the headline

1. **Mis-alignment** (V6_38): `comp[pos]` predicts `b[pos+1]`, the reflex window predicts `b[pos]`.
2. **Wrong spectrum**: `pr_eff_rank()` computes `(Σσ)² / Σσ²` over **singular values**. The
   participation ratio for "how many dimensions carry the variance" is over the covariance
   **eigenvalues** `λ = σ²`. PR(σ) reads systematically higher and is not a variance dimensionality.

Reproduction first — PR(σ) on the mis-aligned rows returns **15.20**, matching V6_26's 15.3, so the
decomposition below is against a reproduced headline, not a remembered one.

## RESULT

| quantity | PR(σ) = V6_26's estimator | PR(λ) = correct | rank@90% var | mean \|row\| |
|---|---|---|---|---|
| MIS-ALIGNED tension (V6_26) | **15.20** | 2.48 | 6 | 2.468 |
| **ALIGNED tension (corrected)** | 5.80 | **1.19** | **1** | 0.576 |
| composed logit row (reference) | 14.61 | 2.36 | 6 | 7.817 |

```
estimator alone (misaligned, σ → λ):      15.2 → 2.48
alignment alone (σ spectrum, mis → ok):   15.2 → 5.80
both corrected:                           15.2 → 1.19
```

**The tell is the reference row.** The composed logit row *by itself* reads PR(σ) = 14.61 against
the "tension"'s 15.20. V6_26 was not measuring what broad context adds — it was measuring the
dimensionality of a logit row. Once both lanes score the same byte and the spectrum is the variance
spectrum, what context adds is **1.19 effective dimensions, rank 1 at 90% of variance**.

## Reading — 🔴 PREMISE FAILS

LANE-BUS's founding move is "independently-earned lanes meet on a shared pre-softmax logit-row bus,
replacing the scalar A⇄G servo whose effective independent dims = zero". The measured headroom on
that bus is **~1 dimension**. The design's own abort condition, written in `v6_26_lanebus_tension.py`
before the run, was: *"PR ~ 1-2 ⇒ content tension ALSO collapses at the logit row → LANE-BUS is
built on sand."* On the corrected instrument the gate reads exactly that.

This is consistent with V6_38 (companion): a ~1-dim bus has essentially nothing for an emit to
discharge, and none of the 5 commit arms differed in their discharge.

⚠️ **The landed V6_26 instrument no longer runs** — `v6_26_lanebus_tension.py` dies on
`W["V"]` KeyError against the current engine. `instrument-never-run-hides-multiple-bugs`: this one
was run once, on a version whose weights dict still had that key, and the two defects above rode
out with the headline.

## Scope
$0, trained57 (d=64), W=8 reflex, natural held-out EN prose, one estimator family (participation
ratio + variance rank). DIRECTIONAL. What is killed is the *measured license* for a wide logit-row
bus on this model — not the general possibility that a larger model carries more context tension,
which is a scale question this toy cannot decide (`a_toy_scale_recheck`).
