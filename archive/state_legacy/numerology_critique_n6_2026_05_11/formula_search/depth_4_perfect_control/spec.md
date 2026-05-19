# Numerology Critique — FORMULA-SEARCH depth-4 + Perfect-Number Control (L12 quantification)

**Cycle**: 2026-05-11 (cycle 5 #2)
**Lane**: `state/numerology_critique_n6_2026_05_11/formula_search/depth_4_perfect_control/`
**Parent**: `../simulate.py` (depth-3 baseline; verdict `FORMULA_SEARCH_CRITICAL_BEATEN`)
**Goal**: Quantify the **boundary** at which L12 becomes binding by sweeping (depth, vocabulary, tolerance) AND introduce a **perfect-number control** (n ∈ {6, 28, 496, 8128}) so the n=6 result can be compared decisively against its three nearest theoretical cousins.

---

## 1. Why depth-4 + perfect-number control

The parent depth-3 lane returned `FORMULA_SEARCH_CRITICAL_BEATEN`: 8 other n in [2,30] hit 22/22 at tol=0.01, while n=6 hits 21/22. That verdict is robust, but it leaves three open questions:

1. **Does depth-4 amplify the saturation?** If yes, L13 is also binding (depth bound is not load-bearing). If no, depth-3 was already at the saturation ceiling.
2. **Does restricted vocabulary preserve the n=6 result?** If pulling transcendentals {e, π, ln2} out causes n=6 to remain top while others drop, the published-formula-uniqueness argument gains ground.
3. **What happens when n is restricted to perfect numbers?** {6, 28, 496, 8128} are the four known small perfect numbers (σ(n) = 2n). If n=6's score is matched by 28/496/8128, the result is "perfect-number-class uniqueness" rather than "n=6 uniqueness".

Each variation is one cell of the (depth × vocab × tol × n-range) cube.

---

## 2. Variations

| ID | depth | vocab | tol   | n-range            | rationale |
|----|-------|-------|-------|--------------------|-----------|
| V1 | 4     | full (11) | 0.01  | [2,30]             | depth-4 baseline — does deeper search saturate more? |
| V2 | 4     | restricted-A (7: 1,n,μ,φ,τ,σ,sopfr) | 0.01 | [2,30] | drop transcendentals; does that re-tighten? |
| V3 | 4     | restricted-B (5: n,μ,φ,τ,σ) | 0.01  | [2,30] | most restricted — Möbius+divisor only |
| V4 | 4     | full | 0.005 | [2,30]             | tighten tolerance ×2 — does n=6 advantage emerge? |
| V5 | 4     | full | 0.001 | [2,30]             | tighten tolerance ×10 — extreme |
| V6 | 4     | full | 0.01  | {6, 28, 496, 8128} | **perfect-number control** at full vocab |
| V7 | 4     | restricted-A | 0.005 | {6, 28, 496, 8128} | **perfect-number control** tightened |

**Time budget**: 5 min per variation cap. On early termination, report partial coverage % (#n completed / total).

---

## 3. Vocabulary subsets

- **full** (11): `1, n, μ, φ, τ, σ, sopfr, J₂, e, π, ln2`
- **restricted-A** (7): `1, n, μ, φ, τ, σ, sopfr` (drops {J₂, e, π, ln2})
- **restricted-B** (5): `n, μ, φ, τ, σ` (drops {1, sopfr, J₂, e, π, ln2})

Restricted-B is the "pure number-theoretic core" — anyone arguing that the published n6_formula vocabulary is fair must accept restricted-B as the most-defensible minimal vocabulary.

---

## 4. Depth-4 layer construction

Building on the depth-3 layer-sets {L1, L2, L3}, define:

```
L4 = unary(L3) ∪ (L3 BIN L1) ∪ (L1 BIN L3) ∪ (L2 BIN L2)
```

This is one-side ≤depth-3, plus the L2×L2 cross to capture symmetric depth-4 expressions like `(σ/τ) × (φ/sopfr)`. L4 may be much larger than L3; we set hard cap at `|L4| ≤ 200_000` (random sample if exceeded) to bound wall-clock.

---

## 5. Perfect-number control rationale

H_067 (perfect_number_architecture) asserts that n=6 is significant because σ(6)=12=2·6. The next three perfect numbers (28, 496, 8128) share the same algebraic property. If formula-search saturates equally across {6, 28, 496, 8128}, then the L12 finding refines to: **the perfect-number class as a whole is generic under formula search** (not that n=6 specifically is non-unique). This is a sharper, more publishable form of L12.

---

## 6. Verdict criteria

Three possible outcomes per variation:

- **N6_STILL_UNIQUE_d4**: `score(6) ≥ max_{other} + 2` AND `score(6)/22 ≥ 0.85`. L12 partially lifted at this (depth, vocab, tol) cell.
- **FORMULA_SEARCH_CRITICAL_BEATEN_d4** (same as parent): some `n ≠ 6` matches or exceeds `score(6)`. L12 remains binding.
- **PERFECT_NUMBER_CLASS** (V6/V7 only): `score(6) ≈ score(28) ≈ score(496) ≈ score(8128)` within ±1, and they dominate (≥85%). L12 refines to "perfect-number-class uniqueness".

Per variation we emit one of these three labels plus the headline numbers.

---

## 7. L12 BINDING quantification update

If V4 or V5 returns `N6_STILL_UNIQUE_d4`, L12 quantification update is required:

> **L12 BINDING (revised)**: binding at tol ≥ X but lifted at tol < X.

If V6/V7 returns `PERFECT_NUMBER_CLASS`, L12 quantification refines:

> **L12 BINDING (revised)**: binding for "n=6 individual" but lifted for "n ∈ {perfect numbers}".

Otherwise L12 quantification stays "binding across all depth-4 (vocab × tol × range) cells tested".

---

## 8. Execution

```
python3 state/numerology_critique_n6_2026_05_11/formula_search/depth_4_perfect_control/simulate.py
```

Writes `results.json` (per-variation matrices) and `verdict.md` (one of the three outcomes).

Seed: `0xF0EAFEA1` (same as parent for reproducibility).

---

## 9. New honest limits introduced by this lane

- **L16**: depth-4 is still arithmetic; sympbolic-regression-style search (e.g., PySR) might find concise formulas that arithmetic depth-4 misses. Not addressed.
- **L17**: perfect-number control uses only the first 4 perfect numbers. The 5th (33550336) is excluded for tractability — primitives at that scale would dominate the layer-set value range and cause numerical noise.
- **L18**: 5-min cap per variation; early-termination variations report partial coverage and are not directly comparable.
