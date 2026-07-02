# G1 MEASURE-ARTIFACT — random-target cheap-gates measured an unlearnable task (2026-07-02)

**READING: MEASURE-ARTIFACT CONFIRMED.** aiden CPU $0, torch=DIRECTIONAL. break-walls (measure-artifact) +
verdict-integrity: the recent cheap-gate methodology used a RANDOM operator-agnostic target, which is
information-theoretically unlearnable for held-out → chance is the CEILING, not a wall to break.

## Same plain trunk (concat-embed MLP, CE), 3 target kinds, 5 seeds
| target | mean held-out acc | over chance (0.125) |
|---|---|---|
| **random** T[fa,fb] (= H_1840/H_6164/H_6162/H_6161/H_1824 methodology) | 0.092 | ≈ chance (FLOOR) |
| struct_add  y=(u[fa]+v[fb]) mod C | 0.800 | +0.67 |
| **struct_nonadd** y=T2[u[fa],v[fb]] (factored K=4 shared latent, NON-additive rule) | **0.978** | +0.85 |

Per-seed struct_nonadd held-out: 0.994 / 1.0 / 1.0 / 0.972 / 0.922 — robust, all train_acc=1.0.

## What this means
- A RANDOM full-rank table T[fa,fb] has NF²=64 independent entries; held-out (fa,fb) entries are independent
  of the training set → NO mechanism (additive, HRR, tensor-product, γ, slot, neurosymbolic) can predict
  them. Chance is the information-theoretic ceiling. The "fair, operator-agnostic" target — adopted to avoid
  RIGGING (H_1840 lesson) — OVER-corrected into an unlearnable task.
- A STRUCTURED target (parts predict whole via a shared rule — which real composition HAS: "red car" =
  red∘car) is recombined by the SAME plain trunk at 98% held-out, NO lever needed. The trunk is not
  inherently incapable of recombination.
- Therefore the recent cheap-gate FLOOR verdicts do NOT evidence lever absence — they tested an unlearnable
  task. Affected (random-target): H_1840 (γ GPU de-authorization), H_6164 (structural-bind), H_6162
  (HE-objective), H_6161 (inhibition), H_1824 (data-coverage). These are MEASUREMENT-INVALID for the
  recombination-lever question and need re-measurement on STRUCTURED (learnable) composition.

## Precise scope (a_toy_scale_recheck; do NOT over-claim the reverse)
This invalidates the SYNTHETIC random-target cheap-gate methodology. It does NOT by itself overturn the
real-model G1=0 on actual text (H_1218 / clm303 / h1129), which is measured on structured real language —
that requires a SEPARATE structure-aware re-test (does the real anima trunk recombine held-out real concept
pairs, given real text has structure?). Two possibilities remain: (a) real anima trunk genuinely fails on
structured real composition (real wall), or (b) the real-G1 metric has its own confound. Follow-on.

## Provenance
toy_structured_target.py, run.log, result.json. aiden RTX5070 host (CPU-only run), OMP=4, $0.
