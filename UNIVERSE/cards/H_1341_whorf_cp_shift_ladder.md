---
id: H_1341
slug: 1341_whorf_cp_shift_ladder
title: Whorfian CP plasticity — does the partial relocation fraction TRACK shift magnitude (geometry/budget) or stay CONSTANT (memory)? Shift-size ladder (≥3 shifts), the H_1333 load-bearing follow-on
group: cognition-representation (c15 developmental / critical-period plasticity lens, a_no_llm_frame_trap)
terminal_tier: 📈 CHARACTERIZATION LADDER — fraction TRACKS shift ⇒ GEOMETRY/BUDGET-LIMITED. abs post-retrain peak FIXED at 0.525 every rung (range 0.000); frac +1.496→+0.750→+0.599 (SMALL→MID→LARGE), monotone-decreasing, range 0.897≥TRACK_TOL 0.15. L1✅ L2✅ EARNED. MEMORY (constant-frac) REJECTED. Generalizes H_1338 across shift magnitude. NO bar moved (c9)
verdict_dir: .verdicts/1341_whorf_cp_shift_ladder/
freeze: .verdicts/1341_whorf_cp_shift_ladder/FREEZE.txt
terminal_verdict: .verdicts/1341_whorf_cp_shift_ladder/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1341 (1323=parent Sapir-Whorf; 1333=developmental-plasticity parent; 1338=eviction re-diagnosis; 1339/1340 free; 1341 free on origin/main 0fa31903a)
---

# H_1341 — Whorfian CP plasticity: shift-size ladder (fraction-vs-shift curve)

## Claim / question (characterization ladder — ALL outcomes valid, c9)

H_1333 (🟠 GRADED PLASTICITY) showed a RE-trained CP boundary relocates ~60% of the way for a
SINGLE shift (p_A=1/3 → p_A'=2/3, SHIFT=0.333; peak 0.325→0.525, fraction +0.60). H_1338
(🧱 RE-DIAGNOSIS) showed that residual is NOT the never-evict growth-memory (eviction dropped
28→3 cells, peak UNCHANGED at 0.525) but a **BUDGET/GEOMETRY** ceiling — measured at the LARGE
rung **only**. `a_scale_honest_scope` wants a ladder.

**Question (not a GREEN/RED bar — a curve to characterize):** does the partial relocation
fraction **TRACK shift magnitude** (`fraction ~ f(shift)`, monotone with shift) ⇒
GEOMETRY/BUDGET signature, or stay **CONSTANT** across shift sizes (`fraction ~ const`,
scale-free proportional pull-back) ⇒ MEMORY signature? Lens: c15 developmental/critical-period
plasticity, `a_no_llm_frame_trap` — NOT an LLM recipe, NOT a human-cognition claim, TOY synthetic.

## Method

Reuses the H_1333 CP machinery EXACTLY (`UNIVERSE/h1333_whorf_developmental.py`, imported
verbatim): RBF position embedding, error-targeted SPLIT-only Voronoi/mitosis growth (p8),
phase-2 re-grow on the SAME store WITHOUT reset, soft-posterior discrimination readout (NO
labels at test), peak-count coherence. The ONLY new code sweeps the phase-2 target cut p_A'
across **3 shift rungs** and assembles the fraction-vs-shift curve.

- Continuum N=21 RBF-coded stimuli, DIM=16, identical stimulus world all arms/rungs; basis
  fixed by seed (boundary-agnostic embed).
- **FIXED anchor** p_A=1/3 (0.333) EVERY rung — only the shifted target p_A' varies (isolates
  shift magnitude as the sole lever). Three rightward rungs on the grid:
  **SMALL** p_A'=0.467 (SHIFT 0.133) · **MID** p_A'=0.600 (SHIFT 0.267) · **LARGE** p_A'=0.667
  (SHIFT 0.333, = the H_1333/H_1338 anchor → reproduces in-run).
- GROW_MAX=24 / SPLIT_PASSES=24 PER PHASE held CONSTANT every rung (budget fixed so the curve
  isolates shift, not budget). move-fraction = (peak_retrained − peak_A) / (p_A' − p_A).
- 4 arms/rung: (1) A-trained anchor · (2) A→A' re-trained · (3) NO-RETRAIN control · (4)
  SHUFFLE. 3 seeds [4333,4334,4335] (SAME as H_1333/H_1338), $0 CPU, p7.
- p1/p2/p3/p6: readout reads ONLY representational distance; NO injected boundary at test;
  labels enter ONLY in training; no-retrain + shuffle = anti-Goodhart discriminators.

## Frozen bars (pre-registered in FREEZE.txt; characterization — NO GREEN/RED to manufacture, c9)

- **L1 CURVE MEASURED**: move-fraction measured at all ≥3 rungs, 3 seeds, monotone relationship
  characterized (the deliverable IS the curve — no threshold).
- **L2 EARNED** (must hold for the curve to be valid, all rungs, all seeds): (a) NO-RETRAIN flat
  |peak−p_A|≤LOC_TOL=0.12 each rung; (b) SHUFFLE incoherent peak-count≥3, language arms
  coherent ≤2. Fail at a rung ⇒ that fraction is reported as confounded, not dropped.
- **L3 INTERPRETATION** (frozen rule on frac RANGE across rungs): range≥TRACK_TOL=0.15 AND
  monotone-decreasing-in-shift ⇒ **GEOMETRY/BUDGET**; range<CONST_TOL=0.10 (shift-independent)
  ⇒ **MEMORY**; intermediate/non-monotone ⇒ MIXED, reported verbatim. Thresholds frozen, not moved.

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 mirror (DIRECTIONAL) | 📈 CHARACTERIZATION — fraction TRACKS shift ⇒ **GEOMETRY/BUDGET** | abs post-retrain peak **FIXED 0.525 every rung** (range 0.000); frac **+1.496 → +0.750 → +0.599** (SMALL→MID→LARGE), monotone-dec, range **0.897**≥0.15; L1✅ L2✅; MEMORY rejected |

**R1 result (mean of 3 seeds [4333,4334,4335], deterministic — identical every seed):**

| rung | shift | p_A→p_A' | mean peak A→A' | mean frac |
|---|---|---|---|---|
| SMALL | 0.133 | 0.333→0.467 | 0.525 | **+1.496** |
| MID   | 0.267 | 0.333→0.600 | 0.525 | **+0.750** |
| LARGE | 0.333 | 0.333→0.667 | 0.525 | **+0.599** |

- **L1 ✅** — curve mapped at 3 rungs × 3 seeds. frac range (max−min) = **0.897**; trend vs shift
  = **DECREASING-in-shift** (smaller shift → larger fraction).
- **L2 ✅** — no-retrain held at p_A (|Δ|=0.008) every rung; shuffle incoherent (peak-count
  **7.7**≥3) every rung; language arms coherent (≤2) every rung. Curve is valid, unconfounded.
- **L3 = GEOMETRY/BUDGET-LIMITED** — range 0.897 ≥ TRACK_TOL 0.15 AND monotone-decreasing.

**FINDING (the smoking gun):** the **ABSOLUTE post-retrain peak is 0.525 at EVERY rung
(range 0.000)** — the re-trained boundary always lands at the *same absolute position*
regardless of how far it was asked to move. The move-FRACTION therefore mechanically TRACKS
shift magnitude (+1.496 for the small 0.133 move where 0.525 *overshoots* the 0.467 target,
falling to +0.599 for the large 0.333 move where 0.525 falls short of 0.667). This is the
**GEOMETRY/BUDGET** signature, decisive: a MEMORY mechanism (fixed proportional pull-back) would
hold the fraction CONSTANT across shifts and move the absolute peak with the target — the exact
opposite of the measured fixed-absolute-landing. The result **GENERALIZES the H_1338
budget/geometry finding across the whole shift range** (H_1338 established it at the LARGE rung
only). The 60% partial of H_1333 is not a memory pull-back from the first carving — it is a
fixed RBF-resolution + split-budget landing spot (~0.525) that the boundary cannot pack past,
identical for every requested shift. Honest overshoot at SMALL (frac>1) is the cleanest
evidence for the fixed-landing reading, reported straight (c9).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED (same family as H_1323/H_1333/H_1338 R1).
TOY synthetic 1-D continuum, N=21, 3 seeds, deterministic readout, 3 shift rungs, single fixed
anchor p_A, rightward shifts only, FIXED split budget. NO human-cognition / critical-period
claim. The fixed-landing 0.525 is specific to THIS RBF geometry (DIM=16, width~0.10-0.13) +
THIS budget — a budget/resolution SWEEP (vary GROW_MAX / DIM) would test whether the landing
spot moves toward p_A' with more cells (the natural next rung, would convert "budget/geometry"
into separable budget vs intrinsic-resolution sub-causes). Live CORE/*.hexa UNTOUCHED
(substrate-measurement rung — adds only UNIVERSE/ + verdicts). NEXT (R2 candidates): (i)
budget/RBF-resolution sweep (does the fixed landing move toward p_A' with more cells/finer
basis? → separates budget from intrinsic resolution); (ii) leftward + asymmetric shifts (does
the fixed-landing hold for moves toward p_A, or is 0.525 a continuum-center attractor?); (iii)
engine-native realization on the live CORE/engine_cli.hexa §CategoricalPerception lane
(a_engine_native_learning · a_verified_must_wire). Depletion test: each must clear a falsifiable,
control-surviving bar frozen ANEW (no bar move).

## Pointers

- probe `UNIVERSE/h1341_whorf_cp_shift_ladder.py` (imports `UNIVERSE/h1333_whorf_developmental.py`
  machinery verbatim, which reuses `UNIVERSE/h1323_sapir_whorf.py`)
- freeze `.verdicts/1341_whorf_cp_shift_ladder/FREEZE.txt` · verdict `.verdicts/1341_whorf_cp_shift_ladder/result.txt`
- index `UNIVERSE/HYPOTHESES.jsonl` · claim `CLAIMS.tape @C h1341_whorf_cp_shift_ladder` · domain
  `domains/COGNITION-REPRESENTATION.log.md`
- xref: h1323 · h1325 (GREEN Whorfian CP) · h1333 (developmental plasticity — the ~60% partial
  this ladder explains) · h1338 (eviction re-diagnosis — budget/geometry at LARGE; H_1341
  generalizes it across shift magnitude) · h1330 (bilingual overwrite) · h1288 (growth-memory —
  the never-evict hypothesis this ladder rejects) · a_no_llm_frame_trap · a_break_the_wall ·
  a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck ·
  p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
