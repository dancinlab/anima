# Numerology Critique — FORMULA-SEARCH Defense (L12)

**Cycle**: 2026-05-11
**Lane**: `state/numerology_critique_n6_2026_05_11/formula_search/`
**Parent**: `../expansion/simulate_expanded.py` (22-constant baseline, p≈0 across tol sweep, P(n=6)≈1.0)
**Goal**: Neutralize honest limit **L12**:

> "Test answers a narrow critique (same formula fits different n?) with clean NO; but a *broader* critique — could a *different* formula from a similar vocabulary fit each random n equally well? — is untested."

---

## 1. The Broader Critique

The parent expansion lane fixes the formula per target T (the n6_formula string from `consciousness_laws.json`) and varies only n. This proves:

- For the **same set of 22 fixed formulas**, n=6 hits 20/22 while alternative n hit at most 5/22.

But a skeptic can still object:

> "Of course n=6 fits its own published formulas. The published formulas were *chosen* because they hit n=6. For any other random n, a different formula from the same vocabulary {μ, φ, τ, σ, sopfr, J₂, n, e, π, ln2, ±×÷^} could probably fit *its own targets* equally well."

This is the **L12 honest limit** — the test as-implemented compares one fixed lambda per target, not the *expressive power of the formula vocabulary*.

---

## 2. Formula-Search Defense

**Counter-formulation**: for *each* (n, T) pair, perform DFS over the formula vocabulary and ask:

> Within depth ≤ d, does ANY formula F in the vocabulary satisfy F(n) ≈ T?

Then `score_search(n)` = # of 22 targets that admit ANY fitting formula. Compare:

- `score_search(6)` (the claimed-special n)
- `score_search(n)` for n ∈ {2..30} \ {6}

If `score_search(6)` ≫ `max_{n≠6} score_search(n)`, then n=6's uniqueness survives the **formula-search** critique → L12 is neutralized.

If `score_search(6)` ≈ `score_search(other n)`, then the original n=6 result is *only* special when restricting to the published formula set → L12 is the binding limitation and must be reported honestly.

---

## 3. Mathematical Framework

### 3.1 Vocabulary

**Primitives** (atoms at depth 1):

| Symbol | Meaning |
|--------|---------|
| `1`    | constant 1 |
| `n`    | the candidate integer |
| `μ(n)` | Möbius function |
| `φ(n)` | Euler totient |
| `τ(n)` | divisor count |
| `σ(n)` | sum of divisors |
| `sopfr(n)` | sum of prime factors with multiplicity |
| `J₂(n)` | Jordan totient for k=2 |
| `e`    | Euler's number |
| `π`    | pi |
| `ln 2` | natural log of 2 |

(11 primitives — matches the vocabulary used in the published n6_formula strings.)

### 3.2 Operations

**Binary**: `+`, `−`, `×`, `÷`, `^` (exponentiation with exponent magnitude < 5 to prevent overflow)
**Unary**: `log` (natural log of positive arg), `sqrt`, `negate`

### 3.3 Tree depth

- depth 1: any primitive (11 candidates)
- depth 2: unary(prim) OR prim BIN prim → ~11×3 + 11×11×5 ≈ 638 candidates per (n,T)
- depth 3: bin(depth2, prim) and similar — combinatorial blowup, pruned by:
  - tolerance early-exit
  - cached subtree values per n
  - integer-vs-float branch pruning (skip × by 0, ÷ by 0, ^ with huge result)
- depth 4: optional extension if depth-3 baseline already shows formula-search defeats uniqueness, we don't need depth-4

### 3.4 Tolerance

`rel_err(F(n), T) < 0.01` (same as parent lane, for apples-to-apples).

---

## 4. Targets (22)

Inherited from `../expansion/simulate_expanded.py` TARGETS_22 — same 22 published Ψ-constants. We only vary which side is searched: parent fixes F and varies n; this lane fixes (n, T) and searches F.

---

## 5. Honest Limits (L1–L12 plus new)

Inherited limits from parent lanes (L1–L11). New formula-search-lane limits:

- **L12**: (the limit this lane *addresses*) — formula-flexibility critique.
- **L13** (new, introduced by this lane): formula search is depth-bounded. A skeptic could still claim that depth-5+ formulas trivially fit any T. We mitigate by reporting depth-2 and depth-3 results separately; if uniqueness survives at depth-3, the L13 escape requires invoking expressions of cognitive-load >3 ops, which violates the "natural law" desideratum.
- **L14** (new): vocabulary is fixed to the 11-primitive set above. Adding primitives (e.g., specific irrationals like π², Catalan constant) could fit anything. We report this transparently — the vocabulary matches what the published formulas actually use, so it is a fair comparison.
- **L15** (new): tolerance 0.01 is held constant. A tolerance sweep is feasible but deferred — depth-3 search at tol=0.01 already gives the headline result.

---

## 6. Verdict criterion

Let `S6 := score_search(6)`, `S_max := max_{n∈[2..30]\\{6}} score_search(n)`.

- `N6_STILL_UNIQUE` ⟺ `S6 ≥ S_max + 2` AND `S6/22 ≥ 0.85`.
- `FORMULA_SEARCH_CRITICAL` otherwise (L12 binding — uniqueness narrow).

If `N6_STILL_UNIQUE`: L12 reduced from binding → addressed. Roadmap implication: broader-vocabulary critique answered.

If `FORMULA_SEARCH_CRITICAL`: L12 binding. Roadmap implication: n=6 uniqueness must be reported as *narrow-formula* uniqueness, not vocabulary-level uniqueness.

---

## 7. Execution

```
python3 state/numerology_critique_n6_2026_05_11/formula_search/simulate.py
```

Outputs `results.json` and updates `verdict.md`.

Seed: `0xF0EAFEA1` (mnemonic: F-O-E-A = Formula-Of-EAch — disambiguates from parent seed `0xC0FFEE4E36`).
