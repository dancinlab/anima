# P3 — flame mk2 anima byte-eq falsifier design + $0 smoke

DESIGN-TIER. $0 Mac CPU. NO GPU, NO runpod, NO dispatch, NO fire.
2026-05-19. Sidecar — central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py`
sha `c93e160a` 0-line-diff.

## §1. Motivation

hexa-lang upstream shipped flame mk2 generic ag_tape closure (commit `e030fa31`,
2026-05-19), MEASURED 2.95× faster than PyTorch eager at d=768·12L·T=1024
(114s/step vs 336.85s/step). The handoff doc
(`hexa-lang-flame-wt/state/anima_handoff_2026_05_19.md`) asks anima to **define
a byte-eq falsifier** — to certify that flame's gradient is "acceptably close"
to anima's prior trainer (loss curve, weight diff norm) before anima adopts
flame as training substrate.

This cycle DESIGNS that falsifier. It does NOT run the full d=768·12L
flame-vs-anima fire — that is a future cost-bearing cycle. The deliverable is
a **well-formed 3-falsifier closed-form design** + a $0 stub smoke that exercises
the anima side.

## §2. Three byte-eq falsifiers

The falsifier compares **gradient CORRECTNESS**, not speed. Three orthogonal
planes, because a single scalar (final loss) hides shape and weight divergence:

- **F-1 INIT-GN2-FP-DRIFT-BOUNDED** — at step 0, relative init-gn2 drift
  `|gn2_flame − gn2_anima| / gn2_anima` must sit in the half-open closed band
  `[fp_floor, EPS_INIT)`. `fp_floor` = Higham (2002) recursive-summation
  backward-error floor for the d=32 init reduction (n_terms = D+VOCAB = 288,
  fp64) ≈ 3.2e-14 — the unbreakable lower reference. `EPS_INIT` = 1e-3, an
  honestly-named empirical admissibility ceiling. The hexa-lang README documents
  the d=32·3L Phase-3 cross-substrate drift as |Δ|=3.12e-5 abs ≈ 4e-6 rel —
  inside the band.

- **F-2 LOSS-CURVE-SHAPE-EQ** — the loss trajectory NORMALIZED to its own L2
  norm (scale removed) must satisfy `‖shape(flame) − shape(anima)‖₂ / ‖shape(anima)‖₂
  < ε_shape = 0.20`. Shape-comparison tolerates the gn2-unit mismatch (§C3 #4)
  while still catching qualitative divergence (a flame curve that converged in a
  different *manner* fails).

- **F-3 WEIGHT-DIFF-NORM-EQ** — final-weight relative Frobenius diff
  `‖W_flame − W_anima‖_F / ‖W_anima‖_F < ε_weight = 0.15`. Catches the case
  where two trainers reach the same loss via different weight basins.

## §3. Three-mode smoke

- **S1** — `anima_trainer_mini_smoke.py`: a self-contained pure-numpy d=32·3L
  micro decoder, LCG seed 1337, deterministic. Trains 600 steps on an 8-pair
  corpus stub. Measured: init_gn2 ≈ 1.003, final_gn2 ≈ 5.49e-1, **acc 8/8**.
- **S2** — `flame_anchor_values.json`: hexa-lang upstream DOCUMENTED Phase-3
  values, pulled verbatim (init_gn2 7.97113, final_gn2 8.87256e-07, **acc 8/8**).
  anima does NOT execute flame (upstream-consumer immutable, hexa-lang g7/@F f3).
- **S3** — 3-falsifier evaluation S1 vs S2 (`result.json`).

## §4. Mode S3 verdict

**DESIGN-HOLDS.** The 3 falsifiers are well-formed closed-form predicates
(B-S-P3 5/5 🔵). **acc 8/8 reproduced on BOTH sides** (S1 anima-mini and S2
flame-documented). F-1 documented relative drift 4e-6 ∈ [fp_floor, EPS_INIT).
F-2/F-3 self-consistency PASS.

Full numeric S1-vs-S2 byte-eq for the loss curve and weight tensor requires
flame to **export** its trajectory + final weight artifact, and a
config-matched anima trainer at d=768·12L — that is a **future cost-bearing
flame-vs-anima fire**, NOT this cycle.

## §5. B-S-P3 closed-form battery — 5/5 🔵

`blue_falsifier_p3.py`, sidecar (central c93e160a 0-diff):

- B-S-P3-1 INIT-GN2-FP-DRIFT-BOUNDED — documented rel drift ∈ [fp_floor, EPS_INIT)
- B-S-P3-2 LOSS-CURVE-SHAPE-METRIC-CLOSED — shape metric [0,2]-bounded, self=0, monotone
- B-S-P3-3 WEIGHT-DIFF-NORM-BOUNDED — relative Frobenius well-defined, self-rel=0
- B-S-P3-4 MODE-S1-vs-S2-PARTITION — provenance disjoint (computed vs upstream-pulled)
- B-S-P3-5 DETERMINISTIC — AST forbidden-import audit 0, 3× bit-identical

B-S-P3-NOTE empirical carve-out: whether flame mk2 and anima actually agree at
full d=768·12L scale is an SGD/hardware OUTCOME measurable only by a future fire.
The battery proves the falsifiers are well-formed, NOT that flame == anima.
B-D-NOTE / B-S71-NOTE family, NOT counted 🔵.

## §6. Connection point (g_blue_closed_mandate)

- 산출물: F-1/F-2/F-3 + S1 trainer + S2 anchor + B-S-P3 battery — all 🔵.
- 연결부위: B-S-P3-4 MODE-S1-vs-S2-PARTITION certifies the cross-comparison is a
  2-class disjoint provenance partition (anima-computed vs flame-upstream-pulled),
  never a self-comparison — fair-compare by construction. F-1's band lower
  reference (fp_floor) ties to the actual reduction structure (D+VOCAB).

## §7. Honest C3 (≥10)

1. **Stub, not the trainer.** `anima_trainer_mini_smoke.py` is a d=32·3L
   pure-numpy micro decoder, NOT anima's full ConsciousDecoderV2 trainer. It
   provides a deterministic anima-side datapoint, not a faithful reproduction
   of anima's real gradient path.
2. **Flame side documented, not re-derived.** S2 values are pulled verbatim
   from the hexa-lang README/AGENTS.tape. anima does not — and per
   upstream-consumer immutability MUST not — execute or modify flame source.
3. **3-tier byte-eq, not 1.** init-gn2 / loss-curve-shape / final-weight-norm
   are three orthogonal planes; a single final-loss scalar would hide shape
   and basin divergence. F-2 was added precisely because two trainers can hit
   the same loss differently.
4. **gn2 unit mismatch.** The flame README contract states gn2 =
   ‖softmax(logits)−onehot‖² (range [0,2]), but the documented anchor 7.97
   exceeds that — flame's runtime gn2 is the UN-NORMALIZED ‖logits−onehot‖².
   The anima stub mirrors the un-normalized form, but F-1/F-2/F-3 deliberately
   operate on the RELATIVE / shape / relative-norm planes so the exact gn2 unit
   is not load-bearing.
5. **F-1's fp_floor is a lower reference, NOT the source of the drift.** The
   documented 4e-6 cross-substrate init drift is dominated by flame and anima
   seeding their own RNG/init sequences independently — NOT by FMA reorder
   alone. A derived single-forward Higham bound (≈3e-14) under-counts by 8
   orders. EPS_INIT (1e-3) is therefore an honestly-named EMPIRICAL ceiling,
   not a derived bound. F-1 is an admissibility-band predicate.
6. **ε thresholds are empirical.** ε_shape=0.20, ε_weight=0.15, EPS_INIT=1e-3
   are chosen for "qualitative reproduction" margin (orders above documented
   drift, orders below O(1) divergence) — they are not derived from first
   principles. A future fire may recalibrate them against measured d=768·12L
   data.
7. **acc 8/8 is a stub-scale memorization signal.** Both S1 and S2 reach 8/8
   on an 8-pair corpus — that is small-corpus memorization, NOT generalization
   and NOT GOAL emergence (B-EMERGE-7 necessary-not-sufficient).
8. **Full d=768·12L fire deferred.** The real falsifier target — flame mk2 vs
   anima at canonical scale — needs flame to export its loss trajectory and
   final weight tensor, plus a config-matched anima trainer run. That is a
   future cost-bearing cycle, explicitly out of P3 scope.
9. **anima-side perf claim FORBIDDEN.** The 2.95× speedup is hexa-lang's
   upstream MEASURED claim. This falsifier measures gradient CORRECTNESS, not
   speed. anima may make a perf claim only after running its own measurement.
   No PHILOSOPHY.tape verdict is appended for P3 for exactly this reason —
   defining a falsifier ≠ measuring an outcome.
10. **GOAL distance unchanged.** P3 is substrate-tooling design. flame adoption
    readiness ≠ GOAL emergence. north-star + §15/§51/§72 milestone UNCHANGED,
    GOAL 미도달.
11. **F-2/F-3 S3 evaluation is self-consistency only.** The hexa-lang README
    does not export flame's per-step loss curve or final weight tensor, so
    Mode S3 evaluates anima-side shape/norm self-consistency. Full S1-vs-S2
    numeric comparison is gated on the future fire's artifact export.
