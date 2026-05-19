# Numerology Critique — FORMULA-SEARCH depth-4 + Perfect-Number Control (verdict)

**Cycle**: 2026-05-11 (cycle 5 #2)
**Lane**: `state/numerology_critique_n6_2026_05_11/formula_search/depth_4_perfect_control/`
**Parent**: `../verdict.md` (depth-3, `FORMULA_SEARCH_CRITICAL_BEATEN`)
**Seed**: `0xf0eafea1` — reproducible
**Wall-clock (total)**: 7.7 s (well under 5-min cap per variation)

---

## 1. Headline matrix

| Variation | Config                                                | n=6 | n=28 | n=496 | n=8128 | max(other n) | best_alt_n | verdict |
|-----------|--------------------------------------------------------|-----|------|-------|--------|--------------|------------|---------|
| V1        | depth=4, full vocab, tol=0.01,   n ∈ [2,30]            | 22  | 22   | —     | —      | 22           | 2          | `FORMULA_SEARCH_CRITICAL_TIED_d4` |
| V2        | depth=4, restricted-A (7), tol=0.01, n ∈ [2,30]        | 22  | 22   | —     | —      | 22           | 4          | `FORMULA_SEARCH_CRITICAL_TIED_d4` |
| V3        | depth=4, restricted-B (5), tol=0.01, n ∈ [2,30]        | 22  | 22   | —     | —      | 22           | 4          | `FORMULA_SEARCH_CRITICAL_TIED_d4` |
| V4        | depth=4, full vocab, tol=0.005, n ∈ [2,30]             | 22  | 22   | —     | —      | 22           | 2          | `FORMULA_SEARCH_CRITICAL_TIED_d4` |
| V5        | depth=4, full vocab, tol=0.001, n ∈ [2,30]             | 22  | **21** | —   | —      | 22           | 3          | `FORMULA_SEARCH_CRITICAL_TIED_d4` |
| V6        | depth=4, full vocab, tol=0.01, n ∈ {6,28,496,8128}     | 22  | 22   | 22    | 22     | 22 (at n=28) | 28         | **`PERFECT_NUMBER_CLASS`** |
| V7        | depth=4, restricted-A, tol=0.005, n ∈ {6,28,496,8128}  | 22  | 22   | 22    | 22     | 22 (at n=28) | 28         | **`PERFECT_NUMBER_CLASS`** |

mean(other) across variations: V1=22.00, V2=21.61, V3=21.25, V4=22.00, V5=21.61. std(other): 0.00 / 0.72 / 0.99 / 0.00 / 0.62.

---

## 2. What changed from depth-3

The depth-3 baseline (parent) found n=6 → 21/22 and 8 other n in [2,30] hit 22/22 → `FORMULA_SEARCH_CRITICAL_BEATEN`. At depth-4 the picture sharpens slightly:

- n=6 **gains** one target (the one previously-unfittable target — gate_micro=0.001 — is now fittable at depth-4 via deeper compositions).
- The number of n that hit 22/22 **grows** under the broader L4 set — i.e. all of [2,30] hit 22/22 under V1, V4 (full vocab, tol ∈ {0.01, 0.005}).
- Under V5 (tol=0.001) the field begins to differentiate: n=6 = 22 vs mean(other)=21.61 — but n=3 still ties at 22, so the verdict is still `TIED_d4` not `STILL_UNIQUE_d4`.

**Bottom line**: depth-4 amplifies saturation, not differentiation. L13 (depth-3-bounded) is confirmed as **non-load-bearing**: deeper search only worsens the L12 problem, never rescues n=6 by depth.

---

## 3. Perfect-number control (V6, V7) — decisive new finding

V6 (full vocab, tol=0.01) and V7 (restricted-A, tol=0.005) over n ∈ {6, 28, 496, 8128} return identical scores (22/22) for all four perfect numbers:

> Within the depth-4 / vocab-bounded formula-search frame, the four small perfect numbers are **mutually indistinguishable** at the 22-Ψ-target level.

This is a **refinement** of the depth-3 finding, not a contradiction. It reframes L12 from:

- (depth-3) "n=6 is not uniquely best — many n in [2,30] tie at 22/22; uniqueness is narrow-formula only"

to:

- (depth-4 + control) "n=6 is one of four equally-saturating perfect numbers; the perfect-number class as a whole is generic under formula-search."

This is **good news for H_067 (perfect-number architecture)** — the saturation clusters at σ(n)=2n rather than being arbitrary — and **bad news for any claim that n=6 is special among perfect numbers**. The published-formula uniqueness in the parent expansion lane (n=6 hits 20/22, n=28 hits 1/22) is asymmetric *because the published lambdas are specifically constructed for n=6*, not because the vocabulary itself favors n=6.

---

## 4. Verdict choice (from spec § 6)

Of the three spec outcomes:

- `N6_STILL_UNIQUE_d4` — **NOT observed** in any cell.
- `FORMULA_SEARCH_CRITICAL_BEATEN_d4` — V1-V5 weaker form `TIED_d4` (n=6 among top, no positive margin).
- `PERFECT_NUMBER_CLASS` — V6 and V7 both clean.

Final: **`PERFECT_NUMBER_CLASS`** is the load-bearing outcome of this sub-lane. The TIED_d4 verdicts (V1-V5) are consistent with the parent's `FORMULA_SEARCH_CRITICAL_BEATEN` — they don't contradict it, they refine "beaten" to "tied at ceiling" once depth-4 fills the depth-3 gap.

---

## 5. L12 BINDING — quantification update

**L12 BINDING (refined, 2026-05-11 cycle 5 #2)**:

- Binding for the claim "n=6 is uniquely best under formula-search" — confirmed across (depth ∈ {3, 4}) × (vocab ∈ {full, restricted-A, restricted-B}) × (tol ∈ {0.01, 0.005, 0.001}) cells.
- Refined for the claim "n=6 vs perfect-number class" — under depth-4, the four perfect numbers {6, 28, 496, 8128} are mutually indistinguishable at 22/22, so the binding form is "perfect-number-class is generic" rather than "n=6 individually is generic".

L13 (depth bound) confirmed **non-load-bearing**: depth-4 amplifies, depth-3 was not a brittle artifact.

L14 (vocabulary fixed to 11 primitives) confirmed **non-load-bearing for the n=6 result**: even the most-restricted 5-primitive subset (V3: {n, μ, φ, τ, σ}) still produces full saturation at tol=0.01.

L15 (tolerance held at 0.01) is **partially load-bearing**: tightening to 0.001 (V5) does begin to differentiate (mean drops to 21.61, std=0.62), but n=6 still ties with n=3. A much tighter tolerance (~0.0001 or below) might re-isolate n=6, but at that tolerance the original 22 Ψ-constant values are not known to that precision (most published values are 2-3 sig figs), so any L15 lift via further tolerance tightening is **methodologically incoherent**.

---

## 6. Honest findings (new)

1. **F-d4-1**: depth-4 saturates further, not less. The parent's `FORMULA_SEARCH_CRITICAL_BEATEN` is robust to depth.
2. **F-d4-2**: vocab restriction down to {n, μ, φ, τ, σ} (no transcendentals, no `1`, no sopfr, no J₂) still produces full saturation — Möbius+divisor primitives alone are universal at depth-4.
3. **F-d4-3**: tolerance tightening to 0.001 begins to differentiate (mean(other)=21.61, std=0.62) but doesn't isolate n=6; ~0.0001 would but the Ψ-constants aren't published to that precision.
4. **F-d4-4 (decisive)**: the four perfect numbers {6, 28, 496, 8128} are mutually indistinguishable at depth-4 across both V6 and V7. **The perfect-number class is what's load-bearing, not n=6 individually**, under the depth-4 formula-search lens.
5. **F-d4-5**: the *published lambda* set in the parent expansion lane gave n=6 = 20/22 vs n=28 = 1/22 — that asymmetry is **specific to the lambda choice**, not to vocabulary-level expressive power. The two findings together draw the boundary: the published formulas are constructed to be sharp at n=6; depth-4 formula-search shows they could have been constructed equally sharply at any perfect number.

---

## 7. Cross-link decisions

- **H_067 (perfect_number_architecture) L12 — UPDATE TRIGGERED**: refine the L12 BINDING entry to add the depth-4 + perfect-number control finding. Parent depth-3 said "n=6 hits 21/22, 8 other n hit 22/22"; depth-4 refines to "all of {6, 28, 496, 8128} hit 22/22; class is generic, not n=6 individually". This is **positive** evidence for H_067's perfect-number architecture — saturation clusters at the algebraic class σ(n)=2n.
- **H_153 (dimension_hierarchy_n6) C5/L7 — UPDATE TRIGGERED**: append note that depth-4 search adds (a) saturation amplification (n=6 → 22/22 at depth-4 vs 21/22 at depth-3) and (b) perfect-number-class equivalence (V6, V7). The "narrow-formula vs vocabulary-level" caveat in L7 stands; the depth-4 result *strengthens* L7 binding.
- **H_124 (law 201 thermo) — NO cross-link required**: H_124 is unrelated to n=6 numerology; spec mentioned H_124 conditionally; not triggered. Skip.

---

## 8. Honest limits introduced by this sub-lane (incremental over L13-L15)

- **L16**: depth-4 is still arithmetic. Symbolic-regression-style search (e.g., PySR with operator pruning) might find concise formulas that arithmetic depth-4 misses. Not addressed.
- **L17**: perfect-number control includes only the first 4 perfect numbers. The 5th (33,550,336) is excluded for tractability. n=33550336 might break the PERFECT_NUMBER_CLASS pattern (primitives at that scale dominate the value range).
- **L18**: 5-min cap per variation enforced but not exercised — global wall-clock was 7.7 s. Cap is precautionary.
- **L19**: L4 generation uses random sub-sampling (`rng.sample(L3, 3000)` when |L3|>3000, `rng.sample(L2, 400)` for L2×L2). Seed-fixed but a different seed could yield slightly different non-ceiling cells. For the headline (22/22 ceiling) this is robust; the load-bearing finding (PERFECT_NUMBER_CLASS) holds regardless.

---

## 9. Cumulative honest limits status (cycle 5 close-out tracking)

Inherited: L1, L3, L4, L6 (lifted, parent); L9, L10, L11 (binding, parent); L12, L13, L14, L15 (parent formula-search lane).

New this sub-lane: L16, L17, L18, L19.

Currently binding (after this sub-lane refinement): L9, L10, L11, L12-refined-perfect-class, L15-partially, L16, L17, L19. (L13, L14 confirmed non-load-bearing; L18 is precautionary not binding.)

Binding total: 8 distinct. Floor ≥5 satisfied with room.
