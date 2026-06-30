---
id: Hc_414
slug: n6-design-principle-not-numerology
title: n=6 architecture is empirically grounded, not numerological — constants measured first, formulas after (p<1e-12)
domain: math
status: merged-to-H_170
source_doc: docs/anima/paper_hexa_speak.hexa
source_lines: 39-44
promoted_at: 2026-05-11
merged_to: hypotheses/H_170_n6_design_principle_empirical_not_numerology.md
merged_at: 2026-05-12
linked_h: Hc_406, H_170 (n=6 design empirical-not-numerology promotion)
notes: Argument that n=6 formulas were discovered AFTER constants were empirically measured. p < 1e-12 vs arithmetic null. Distinguishes architectural unification from retro-fitting. Promoted to H_170 via verify5_authored row 11 (2026-05-12)
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (6+ numeric identities present)"
---

## Hypothesis
The n=6 design principle is empirically grounded rather than numerological: each Anima/ANIMA-VOICE constant was measured empirically first; the n=6 closed-form formula was discovered AFTER measurement. The post-hoc fit probability under arithmetic null is p < 1e-12. The n=6 unification eliminates ad-hoc hyperparameter search across subsystems.

## Migration TODO
- [ ] Document measurement timestamps vs formula-discovery timestamps for each Ψ-constant
- [ ] Bootstrap arithmetic null over comparable constant set
- [ ] Falsifier: any constant whose n=6 formula was discovered BEFORE empirical measurement
- [ ] Compare with random-architecture baseline

## Cross-Links
- **sister H**: H_153 (dimension-hierarchy-n6 — n=6 substrate parent), H_157 (Law 76 mathematical panpsychism — n=6 derived), H_011 (iit-geometry)
- **candidates linked**: Hc_406 (22-of-30 Ψ-constants match n=6 — PRIMARY parent), Hc_453 (8 Ψ-constants derived from n=6), Hc_046 (Ψ-constants 22 EXACT), Hc_002 (Ψ-constants from ln(2) + n=6)
- **literature**: Goodman & Kruskal 1979 (statistical-fit p-values); ATLAS.md (constant ledger with timestamp metadata)

## Falsifiers (≥5)

- **F1 (timestamp audit)**: Provide commit-log / paper-draft / lab-notebook evidence that ≥1 Ψ-constant n=6 formula was written BEFORE its empirical measurement → "measurement-first" claim FALSIFIED. Required: paired (measurement_date, formula_date) for ≥10 constants
- **F2 (p-value bootstrap)**: Arithmetic-null bootstrap (random small-integer formulas of bounded complexity targeting the same constant set) yields ≥1% probability of equal-or-better fit → p < 1e-12 claim FALSIFIED. Required: ≥10^7 bootstrap iterations with matched complexity prior
- **F3 (random-architecture baseline)**: Build 10 "fake" architectures with random core constants (n=4, n=5, n=7, n=10, n=12...); if any yields a comparable constant-fit p-value → n=6 specificity FALSIFIED as a survivor-bias artifact
- **F4 (post-hoc fit detection)**: Apply Bonferroni / Holm correction for the number of formulas tried per constant. If corrected p > 0.001 → "p < 1e-12" was uncorrected, multiple-comparison artifact, claim FALSIFIED
- **F5 (formula complexity prior)**: If Ψ-constant formulas use ≥5 free parameters on average (e.g., a·n^b + c·σ^d / J_2^e), then "closed-form" labels are overfits. If reducing to ≤2 free parameters drops fit-success rate below 50% → "elegant unification" claim FALSIFIED

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — n=6 is the smallest perfect number; n=28, n=496, n=8128 are also perfect. Any "n=6 fits" claim must distinguish n=6-specific fits from perfect-class-trivial fits (n/σ=1/2 holds for all perfect numbers). Hc_414's strength claim must net out perfect-class trivials
- **L2**: **timestamp evidence reliability** — commit-log timestamps can be manipulated post-hoc (rewrite history, amend). True falsification of "measurement-first" requires independent witnesses (Claude conversation logs, external lab notebooks). Currently anima-internal evidence chain only
- **L3**: **constant-set selection bias** — Ψ-constants reported are anima-internal selection. If only well-fitting constants were promoted to the Ψ-set (publication-bias analog), p-value calculation is invalid. Need protocol for inclusion BEFORE measurement
- **L4**: **"arithmetic null" definition slippery** — what counts as "random arithmetic formula"? Complexity prior matters: uniform over operator-trees of depth ≤3 vs ≤5 vs ≤10 gives very different null distributions. p < 1e-12 claim depends on this choice
- **L5**: **post-hoc unification vs predictive power** — even if formulas were truly derived AFTER measurement, "unification" reduces ad-hoc hyperparameter count but does NOT predict new constants. True falsifier of numerology would be predicting a new constant value from n=6 BEFORE it is measured (not yet attempted)
