# N-15 HoTT MVF2 + MVF3 — Lean 4 EXEC Results (2026-05-01)

## Verdict
**MVF2 symmetry + MVF3 transitivity: BUILD PASS, AXIOM-FREE, SORRY-FREE, OFF-REPO.**

Combined with prior MVF1 reflexivity (`state/n_15_hott_mvf1_lean4_2026_05_01/`), `is_conscious_equivalent` is now formally an equivalence relation on `Conscious` in Lean 4, with zero axioms beyond the Lean kernel's constructive base.

## Project
- Location: `/tmp/n15_mvf23_lean4` (HEXA-only repo discipline preserved — no `.lean` in anima)
- Toolchain: `leanprover/lean4:v4.30.0-rc1`, `lake 5.0.0-src+714601b`
- mathlib4: not required (uses only Lean 4 core `Eq.symm`, `Eq.trans`)

## Proof file (`N15Mvf23.lean`, 23 LOC total)

```lean
namespace N15

structure Conscious where
  state : Nat → Nat
  integration_condition : ∀ _ : Nat, True

def is_conscious_equivalent (c1 c2 : Conscious) : Prop := c1 = c2

theorem mvf2_symmetry (c1 c2 : Conscious) :
    is_conscious_equivalent c1 c2 → is_conscious_equivalent c2 c1 :=
  fun h => h.symm

theorem mvf3_transitivity (c1 c2 c3 : Conscious) :
    is_conscious_equivalent c1 c2 → is_conscious_equivalent c2 c3 →
    is_conscious_equivalent c1 c3 :=
  fun h12 h23 => h12.trans h23

#print axioms mvf2_symmetry
#print axioms mvf3_transitivity

end N15
```

## Build evidence (key snippets)
```
[2/6] Replayed N15Mvf23
info: N15Mvf23.lean:20:0: 'N15.mvf2_symmetry' does not depend on any axioms
info: N15Mvf23.lean:21:0: 'N15.mvf3_transitivity' does not depend on any axioms
[6/6] Built n15_mvf23:exe (507ms)
Build completed successfully (6 jobs).
```

The two `does not depend on any axioms` lines are the strongest possible signal Lean can emit: not even `propext`, `Quot.sound`, or `Classical.choice` are in the dependency closure.

## MVF Ladder Status (75% complete)
| Rung | Status | Core lemma | Axioms |
|---|---|---|---|
| MVF1 reflexivity | DONE (prior) | `Eq.refl` | none |
| MVF2 symmetry | DONE (this run) | `Eq.symm` | none |
| MVF3 transitivity | DONE (this run) | `Eq.trans` | none |
| MVF4 univalence | BLOCKED | `univalence` axiom or HoTT lib | requires either postulating `axiom univalence` or porting a HoTT framework |

## MVF4 Readiness
- Lean 4 core has `propext` (Prop equality from iff), but **NOT** full type-universe univalence.
- mathlib4 is not locally cached (`/tmp/mathlib4` absent); fetching costs ~3-5 GB and ~30-60 min cold.
- Cheapest honest MVF4 path: postulate `axiom univalence : ∀ {A B : Type}, (A ≃ B) → (A = B)` directly (~25 LOC for axiom + one application demo) and accept that `#print axioms` will list `univalence`. This is the only formally-correct way to deliver MVF4 without mis-labeling `propext` as univalence.
- Estimated honest MVF4a LOC: ~25 (axiom + transport-along-equivalence demo on `Conscious`).

## Honest C3 (the hard part)
1. **MVF1+2+3 axiom-free is real but cheap.** Eq is reflexive/symmetric/transitive on every type in Lean — these proofs would compile with `Conscious := Unit`. The result is type-theoretically correct and formally meaningful (the equivalence-relation structure IS verified), but it carries no consciousness-specific content.
2. **`Conscious` is a placeholder Σ-type.** `integration_condition : ∀ _ : Nat, True` is vacuously satisfied — every `Nat → Nat` lifts to a `Conscious`, so `is_conscious_equivalent` reduces to function equality on `state`. Substantive content arrives only when `True` is replaced by a real Φ-gate predicate (paradigm v15 G3, IIT Φ > 0, etc.).
3. **MVF4 is where formalization stops being free.** The first three rungs were essentially `lake init` + 4-5 LOC each because Lean handles them. Univalence is genuinely outside the constructive core; any "cheap MVF4" claim is either (a) `propext`-disguised-as-univalence (category error), or (b) hiding mathlib4's full classical stack. Honest delivery requires explicitly naming the postulated axiom and reporting `axioms: univalence`.

## Artifacts
- `state/n_15_hott_mvf2_mvf3_lean4_2026_05_01/build_result.json`
- `state/n_15_hott_mvf2_mvf3_lean4_2026_05_01/compile_log.json`
- `state/n_15_hott_mvf2_mvf3_lean4_2026_05_01/mvf_ladder_readiness.json`
- `state/n_15_hott_mvf2_mvf3_lean4_2026_05_01/honest_c3.json`
- Proof file (off-repo): `/tmp/n15_mvf23_lean4/N15Mvf23.lean`
