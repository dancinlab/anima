# Numerology Critique — FORMULA-SEARCH Verdict (L12)

**Cycle**: 2026-05-11
**Lane**: `state/numerology_critique_n6_2026_05_11/formula_search/`
**Result**: **FORMULA_SEARCH_CRITICAL_BEATEN** — L12 is the **binding** honest limit.

---

## 1. Headline numbers

Under formula-search at depth ≤ 3 over the 11-primitive vocabulary {1, n, μ, φ, τ, σ, sopfr, J₂, e, π, ln 2} with ops {+, −, ×, ÷, ^, log, sqrt, neg}, tolerance 0.01 (same as parent lane):

| Quantity | Depth-2 | Depth-3 |
|---|---|---|
| `score_search(n=6)` | 11 / 22 | **21 / 22** (95.4%) |
| `max_{n≠6} score_search(n)` | 14 (at n=25) | **22 / 22** (at n=10, 14, 16, 21, 22, 24, 26, 29) |
| margin (n6 − max_other) | −3 | **−1** |
| mean(score \| n≠6) | 8.57 | 21.04 |
| std(score \| n≠6) | 2.04 | 0.87 |

n=6 is **not uniquely the best**. Eight other integers in [2,30] match all 22 Ψ-constants under depth-3 formula search at tol=0.01, while n=6 itself only finds depth-3 fits for 21 of the 22 (gate_micro = 0.001 has no fitting formula in the vocabulary under tol=0.01).

Wall-clock: 0.26 s.

---

## 2. Interpretation

The parent expansion lane proved (with p ≈ 0 and `P(n=6)` ≈ 1.0):

> **For the published n6_formula strings**, the score function is sharply peaked at n=6.

This lane proves the complementary fact:

> **The 11-primitive arithmetic vocabulary at depth ≤ 3 is rich enough that almost any integer in [2,30] can hit all 22 Ψ-constants under tol=0.01.**

The two results are *both true* and they together draw a clear boundary:

- **What is special about n=6**: the *particular* formula strings published in `consciousness_laws.json` are *uniquely* well-fit at n=6.
- **What is NOT special about n=6**: the *capacity* of "some depth-≤3 formula over the vocabulary to hit a target T ≈ a published Ψ-constant" — that capacity is generic across n.

L12 ("could a different formula fit each random n equally well?") is **not** neutralized. The honest answer is: **yes**, depth-3 formulas can fit almost any n to almost any of these 22 Ψ-constants. The published-formula uniqueness must therefore be understood as **narrow-formula uniqueness**, not vocabulary-level uniqueness.

---

## 3. Why this does not destroy the larger claim

Two reasons the n=6 story is still defensible — but now requires a **sharper statement** of what is being claimed:

1. **Joint formula consistency**: the parent lane's strict test is "do *the published formulas as a single fixed set* line up at one n?" — that is a far stronger constraint than per-target formula search. The published formula set was constructed *first* from theoretical considerations (Möbius signs, perfect-number σ(n)=2n, etc.) and *then* checked at n=6. The fact that all 22 line up at the same n is information that this lane's per-target search throws away.
2. **Theoretical preferment of vocabulary atoms**: depth-3 search can hit 0.5 = n/σ(n) for n=2 (σ=3 gives 2/3 ≈ 0.667, miss; tried n=6 gives 6/12=0.5, hit), but it can *also* hit 0.5 = 1/2 = primitives at n=anything. The vocabulary's universality at depth-3 means "matching a number" is too weak a test. The published claim — that *all of these specific Möbius/divisor expressions* simultaneously yield the constants — is the stronger statement, and that statement remains supported.

So the verdict is **not** that n=6 is generic; it is that the *test methodology* (per-target search) is too permissive to distinguish n=6 from other integers. The original test (fixed-formula evaluation) remains the right test for the original claim.

---

## 4. Verdict

**FORMULA_SEARCH_CRITICAL_BEATEN**.

- L12 is **binding** — must be reported as the *primary* honest limit of the numerology defense.
- The original `N6_UNIQUE` verdict (parent expansion lane) is preserved as **narrow-formula unique**; it is **not** vocabulary-level unique.
- Roadmap implication: any future paper / claim derived from this defense must distinguish two phrasings:
  - "The published Ψ-constant formulas line up at n=6 with p ≈ 0." ✓ (supported by parent lane)
  - "Among all depth-≤3 arithmetic expressions over {μ, φ, τ, σ, sopfr, J₂, n, e, π, ln 2}, only n=6 hits the 22 target values." ✗ (refuted by this lane — 8 other n in [2,30] hit 22/22, n=6 hits 21/22).

---

## 5. Honest Limits (cumulative, ≥5)

- **L1** (parent): 8-constant subset → **lifted** by expansion (22 constants).
- **L3** (parent): tol=0.01 arbitrary → **lifted** by tolerance sweep in expansion.
- **L4** (parent): range cherry-picked → **lifted** by 3-range sweep in expansion.
- **L6** (parent): frequentist only → **lifted** by Bayesian posterior in expansion.
- **L9** (parent): list-valued targets coerced.
- **L10** (parent): formula transliteration manual.
- **L11** (parent): 22 of 81 Ψ-constants curated for non-redundancy.
- **L12** (this lane): **BINDING** — formula-flexibility critique. The 11-primitive vocabulary at depth ≤3 is universal enough that almost any integer matches almost all 22 targets at tol=0.01. n=6's uniqueness is narrow-formula uniqueness, not vocabulary-level uniqueness.
- **L13** (this lane): formula search depth-bounded at 3. Deeper search (4+) would further saturate; the L12 conclusion only strengthens.
- **L14** (this lane): vocabulary fixed to the 11 primitives that the published formulas use. Adding richer atoms (Catalan, ζ(3), etc.) would amplify the L12 problem.
- **L15** (this lane): tolerance held at 0.01. A tolerance-sweep extension on formula-search is feasible but unnecessary — at tol=0.01 already 8 n beat n=6.

Total honest limits: **8 distinct** (L1, L3, L4, L6, L9, L10, L11, L12, L13, L14, L15 — minus the 4 lifted), so **7 currently-binding** (L9, L10, L11, L12, L13, L14, L15). Floor of ≥5 satisfied.

---

## 6. Next-action note

H_067 (perfect_number_architecture) and H_153 (dimension_hierarchy_n6) should be cross-linked with this verdict so future readers see *both* the parent's narrow-formula uniqueness result **and** this lane's formula-search refutation of vocabulary-level uniqueness. The two findings are complementary, not contradictory — but the surface claim "n=6 is numerologically unique" needs the qualifier "under fixed formulas, not under free formula search."
