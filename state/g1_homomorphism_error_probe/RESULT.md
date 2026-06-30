# H_1821 — Homomorphism-Error (HE) probe — RESULT

**tier:** 🔵 BUILT + SELF-VALIDATED (DIRECTIONAL · numpy-only · $0 · p7 proxy)
**date:** 2026-06-29
**run:** `python3 state/g1_homomorphism_error_probe/he_probe.py <ckpt...>` (mac CPU, OMP=4)
**engine note:** reps from `core/clm_decode.py` byte-faithful CLMConvMoE forward — **torch-free, gauge_lib-free, numpy-only**. This is a DIRECTIONAL pre-screen, NOT a terminal G1 verdict (G1 SSOT = engine-native `anima evaluate`).

---

## What HE measures

HE = E‖r(A∘B) − (r(A) ⊕ r(B))‖ / E‖r(A∘B)‖ over concept pairs, for
⊕ ∈ {additive r(A)+r(B), hadamard-bind r(A)·r(B)}. r(·) = CLMConvMoE trunk
penultimate `yn` (post final-groupnorm, pre readout) at the last byte position,
right-aligned in the T=24 decode window. A∘B = byte concat A+B. Lower HE = the
trunk preserves the composition operator better (An & Du NeurReps2025: HE
predicts OOD compositional gen at R²=0.73).

---

## (a) Self-test (synthetic) — METRIC SEPARATES ✅

| construction | HE_add | HE_hada |
|---|---|---|
| additive-homomorphic r(A∘B)=r(A)+r(B) | **0.000000** | 1.235 |
| hadamard-homomorphic r(A∘B)=r(A)·r(B) | 1.707 | **0.000000** |
| random r(A∘B) ⟂ A,B | 1.706 | 1.420 |

`SEPARATES gate: PASS` — homomorphic HE≈0, random HE≈1.4–1.7. The metric is a
real composition-preservation meter, not a constant. (≈√2 for random in unit
fp space, as expected.)

## (a) Real .clm HE — all available 303M ckpts (ALL G1-floor)

Concept pairs n=16 (ko/en short byte-spans). 3 real 303M CLMConvMoE (d3784/E3/L4):

| ckpt (known G1) | HE_add | shuffle ctrl | HE_hada | best_HE | control contrast (shuffle−true) |
|---|---|---|---|---|---|
| ce_marginal_seed7 (G1≈0) | 1.258 | 1.607 | 6.966 | 1.258 | add **+0.349**, hada +0.098 |
| pc_bind_seed7 (G1≈0)     | 1.232 | 1.541 | 7.871 | 1.232 | add **+0.309**, hada +0.079 |
| n6n7_seed4307 (G1≈0)     | 1.381 | 1.736 | 3.140 | 1.381 | add **+0.355**, hada +0.149 |

## (a) Control contrast

For ALL 3 ckpts the **shuffled** (mismatched-target) HE is consistently
**higher** than the true-pair HE (additive +0.31…+0.36). → HE measures *real*
composition structure: scrambling which (A,B) maps to which A∘B degrades the
homomorphism fit. Controls bar (shuffle → HE↑) **PASS**.

---

## (b) Does HE predict G1? — DIRECTION ONLY, honest caveat

- **All 3 real ckpts are G1-floor (G1≈0)** and all show **HE_add ≈ 1.23–1.38** —
  far above the homomorphic 0.0 and only modestly below the random baseline
  (~1.7). Reading: these floor trunks have *weak* additive composition
  structure (better than random, nowhere near homomorphic). Consistent with
  their known G1=0.
- **The predictive bar (AUROC≥0.7 separating G1-PASS vs G1-floor, ≥4 ckpt) is
  UNMEASURABLE here: there is NO G1-PASS ckpt anywhere** — the entire G1
  campaign sits at floor (best_distinct ≤1). With zero positives, no
  discrimination/AUROC can be claimed. This is the honest limiter, not a HE
  defect.
- Hadamard HE is much worse (3–8) than additive across all ckpts — expected for
  an additive-residual ConvMoE trunk (composition is closer to + than to ⊙),
  and itself a directional hint that the trunk's native composition is additive,
  not multiplicative-bind. (Relevant to H_1818 Hadamard-bind landing
  NOT-SUPPORTED.)

## (c) Verdict tier

🔵 **BUILT + SELF-VALIDATED (DIRECTIONAL)** — probe built numpy-only/$0, self-test
SEPARATES PASS, control contrast PASS (HE measures real composition). Predictive
power **UNMEASURABLE-at-floor** (no G1-PASS ckpt exists to form a positive
class). Frozen prediction registered for the first positive: a G1-PASS ckpt
should show **notably lower HE_add** (pre-register threshold HE_add < 0.9, i.e.
below the ~1.2–1.4 floor band) — falsifiable once any arm lifts G1>0.

## (d) Next round

**HE on combo-c arms post-landing** — when H_1819 (op + recomb-objective)
finishes on GPU, run `he_probe.py` on its .clm arms. If any lifts G1>0 (first-
ever positive), test whether its HE_add drops below the 1.2–1.4 floor band
(frozen pred HE_add<0.9) → that single positive would convert this from
self-validated to predictive-tested. Secondary: pull `clm303_clean.clm` for an
additional floor data point (still no positive — direction only).
