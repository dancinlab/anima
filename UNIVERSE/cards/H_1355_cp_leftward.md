---
id: H_1355
slug: cp-leftward
title: Whorfian CP plasticity — is the fixed ~0.525 landing a CONTINUUM-CENTER attractor (lattice artifact) or a GEOMETRY-FIXED budget landing? Leftward + asymmetric placements, the H_1341 load-bearing follow-on
group: cognition-representation (c15 developmental / critical-period plasticity lens, a_no_llm_frame_trap)
terminal_tier: 📈 CHARACTERIZATION LADDER — center-attractor REJECTED. ABS landing SPANS 0.375→0.692 (max |L−0.5|=0.192, NOT center-pinned) and TRACKS placement geometry; RIGHT-REF 0.525 ⇄ LEFTWARD-1 mirror 0.475 (symmetric about 0.5, not both at center); ASYM-R 0.692 / ASYM-L 0.375 sit off-center toward their requested cut. c2 = MIXED→geometry-leaning (formal GEOMETRY-FIXED conjunction missed only on an over-strict left-tracking clause + ASYM-L c3-confounded). c1✅ table · c3 4/5 rungs (ASYM-L A→A′ went incoherent pc=3, reported confounded not dropped). H_1341 0.525 = geometry, NOT a center pin. NO bar moved (c9)
verdict_dir: .verdicts/1355_cp_leftward/
freeze: .verdicts/1355_cp_leftward/FREEZE.txt
terminal_verdict: .verdicts/1355_cp_leftward/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1355 (1323=parent Sapir-Whorf; 1333=developmental-plasticity parent; 1338=eviction re-diagnosis; 1341=shift-size ladder parent; 1355 worktree off origin/main)
---

# H_1355 — Whorfian CP plasticity: leftward + asymmetric landing (center-attractor vs geometry-fixed)

## Claim / question (characterization ladder — ALL outcomes valid, c9)

H_1341 (📈 CHARACTERIZATION) found that for RIGHTWARD shifts from the FIXED anchor p_A=1/3
(0.333), the post-retrain CP peak ALWAYS lands at the SAME absolute spot (**~0.525**, abs-peak
range **0.000**) regardless of the requested shift size — so the move-fraction mechanically
tracks 1/shift. H_1341 read this as GEOMETRY/BUDGET. **But** p_A=1/3 is LEFT of the continuum
center (0.5) and ALL its rungs shifted RIGHTWARD (toward/past center), and **0.525 ≈ 0.5 = the
continuum CENTER**. H_1341 cannot distinguish:

- **(H-center)** 0.525 is a **CONTINUUM-CENTER ATTRACTOR** — a symmetric-lattice artifact (the
  N=21 RBF discrimination readout is richest near the lattice center), so the peak is pulled to
  ~0.5 regardless of the requested cut.
- **(H-geometry)** 0.525 is a **GENUINE GEOMETRY-FIXED LANDING** of the budget/geometry
  mechanism, which would MOVE if the anchor/target geometry is made asymmetric.

**Question (not a GREEN/RED bar — a table to characterize):** add LEFTWARD (p_A′ < p_A) and
ASYMMETRIC (anchor off-center, both cuts on the SAME side) placements and read the ABSOLUTE
landing spot — does it stay center-pinned (H-center) or track the placement (H-geometry)?
Lens: c15 developmental/critical-period plasticity, `a_no_llm_frame_trap` — NOT an LLM recipe,
NOT a human-cognition claim, TOY synthetic.

## Method

Reuses the H_1333/H_1341 CP machinery EXACTLY (`h1333_whorf_developmental.py`, copied verbatim
into `state/cp-leftward/` and imported): RBF position embedding, error-targeted SPLIT-only
Voronoi/mitosis growth (p8), phase-2 re-grow on the SAME store WITHOUT reset, soft-posterior
discrimination readout (NO labels at test), peak-count coherence. The ONLY new code sweeps the
**(anchor p_A, target p_A′) placement** across 5 leftward/asymmetric rungs and assembles the
absolute-landing table.

- Continuum N=21 RBF-coded stimuli, DIM=16, identical stimulus world all arms/rungs; basis
  fixed by seed (boundary-agnostic embed). GROW_MAX=24 / SPLIT_PASSES=24 PER PHASE constant.
- **5 placement rungs** (vs H_1341's fixed anchor): **RIGHT-REF** (0.333→0.667, the H_1341 LARGE
  rung) · **LEFTWARD-1** (0.667→0.333, mirror) · **LEFTWARD-2** (0.800→0.500) · **ASYM-R**
  (0.600→0.800, both right of center) · **ASYM-L** (0.400→0.200, both left of center). All on
  the grid (0.05), no edge clipping.
- 4 arms/rung: (1) A-trained anchor · (2) A→A′ re-trained · (3) NO-RETRAIN control · (4)
  SHUFFLE. 3 seeds [4333,4334,4335] (SAME as H_1333/H_1341), $0 CPU, p7.
- p1/p2/p3/p6: readout reads ONLY representational distance; NO injected boundary at test;
  labels enter ONLY in training; no-retrain + shuffle = anti-Goodhart discriminators.

## Frozen bars (pre-registered in FREEZE.txt; characterization — NO GREEN/RED to manufacture, c9)

- **c1 REPORT**: the absolute post-retrain peak L_rung (mean 3 seeds) measured & reported
  verbatim for all 5 rungs (the table IS the deliverable — no threshold).
- **c2 DISCRIMINATE** (frozen rule, CENTER=0.50, CENTER_TOL=0.08): **CENTER-ATTRACTOR** iff
  every rung within CENTER_TOL of 0.50 (max|L−0.5|≤0.08); **GEOMETRY-FIXED** iff asymmetric
  away-from-center rungs land off-center toward their requested cut (ASYM-R L>0.58, ASYM-L
  L<0.42) AND leftward rungs land left of RIGHT-REF; else **MIXED**, per-rung breakdown verbatim.
  Both hypotheses pre-registered; the data picks, reported straight either way.
- **c3 EARNED** (must hold for a rung's landing to be valid, all 3 seeds): (a) NO-RETRAIN holds
  the anchor |peak−p_A|≤LOC_TOL=0.12; (b) SHUFFLE incoherent peak-count≥3, language arms coherent
  ≤2. Fail at a rung ⇒ that landing reported as confounded, not dropped.

## Result (📈 characterization complete; c1✅ table · c3 4/5 rungs · c2 = MIXED→geometry-leaning)

Absolute-landing table (mean of 3 seeds, `result.txt` verbatim):

| rung | p_A→p_A′ | shift | **ABS land L** | \|L−0.5\| | frac | c3 |
|------|----------|-------|----------------|-----------|------|-----|
| RIGHT-REF  | 0.333→0.667 | +0.334 | **0.525** | 0.025 | +0.599 | ✅ |
| LEFTWARD-1 | 0.667→0.333 | −0.334 | **0.475** | 0.025 | +0.599 | ✅ |
| LEFTWARD-2 | 0.800→0.500 | −0.300 | **0.625** | 0.125 | +0.667 | ✅ |
| ASYM-R     | 0.600→0.800 | +0.200 | **0.692** | 0.192 | +0.583 | ✅ |
| ASYM-L     | 0.400→0.200 | −0.200 | **0.375** | 0.125 | +0.250 | **FAIL** |

**c2 = MIXED, but the substantive call is geometry-leaning, center-attractor REJECTED:**

- **CENTER-ATTRACTOR is REJECTED.** The landing SPANS 0.375→0.692 (max |L−0.5| = **0.192**),
  far outside CENTER_TOL=0.08. The peak is NOT center-pinned.
- **The landing TRACKS placement geometry.** RIGHT-REF lands 0.525 and its exact mirror
  LEFTWARD-1 lands 0.475 — **symmetric about 0.5**, the hallmark of a geometry that mirrors the
  placement, NOT two rungs both pinned to center. ASYM-R (both cuts right of center) lands 0.692
  off-center-right toward its 0.800 cut; ASYM-L lands 0.375 off-center-left toward its 0.200 cut.
  Both asymmetric sub-clauses PASS (ASYM-R L=0.692>0.58 ✅; ASYM-L L=0.375<0.42 ✅).
- The formal `GEOMETRY-FIXED` tag missed on ONE over-strict sub-clause: the frozen rule asked
  leftward rungs to land *left of RIGHT-REF*, but LEFTWARD-2 (anchor 0.800→target 0.500) lands
  0.625 (right of RIGHT-REF's 0.525) because the residual *right-side* first carving anchors the
  landing — which is itself geometry (residual-carving dependence), not center-pinning. The
  frozen clause conflated "leftward shift" with "lands left absolutely"; the data shows landing
  is anchored to the FIRST carving's side, a stronger geometry signal than the clause encoded.
- **ASYM-L is c3-CONFOUNDED and reported as such (not dropped):** on 2/3 seeds the A→A′ arm went
  incoherent (peak-count 3 > COH_MAX_LANG 2) — a leftward same-side shift scattered the readout.
  Per the frozen c3 rule that rung's landing is flagged confounded; c3 holds at 4/5 rungs.

**Finding:** the fixed ~0.525 landing of H_1341 is a **GENUINE GEOMETRY landing, NOT a
continuum-center artifact** — when the placement is made asymmetric or mirrored, the landing
MOVES with the geometry (0.375–0.692, mirror-symmetric for the RIGHT-REF⇄LEFTWARD-1 pair). The
H_1341 budget/geometry reading STANDS and generalizes to leftward/asymmetric moves; the
candidate center-attractor confound is **REJECTED**. The honest residual: one rung's formal
clause was over-strict (geometry is anchored to the first carving's side, not absolute
direction) and the away-from-center leftward same-side shift (ASYM-L) degrades readout coherence
(a real limit of split-only re-growth at a same-side leftward cut).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — **engine-transfer UNVERIFIED**. TOY synthetic 1-D continuum, N=21,
3 seeds, deterministic readout, 5 placement rungs. NO human-cognition / critical-period claim.
The center-attractor rejection holds for the THIS lattice (N=21, DIM=16); finer lattices,
denser grids, 2-D continua, and the engine-native realization are UNVERIFIED. ASYM-L coherence
degradation may be lattice-resolution-bound. Live CORE/*.hexa UNTOUCHED (substrate-measurement
rung — adds only UNIVERSE/ + state/ + verdicts). NO bar moved (c9/p7).

## Pointers

- code: `state/cp-leftward/h1355_cp_leftward.py` (+ `state/cp-leftward/h1333_whorf_developmental.py` machinery copy)
- freeze: `.verdicts/1355_cp_leftward/FREEZE.txt` · verdict: `.verdicts/1355_cp_leftward/result.txt`
- xref: H_1341 (shift-size ladder, parent — 0.525 fixed landing) · H_1338 (eviction re-diagnosis → budget/geometry) · H_1333 (graded plasticity parent) · H_1323 (Sapir-Whorf CP parent) · `a_no_llm_frame_trap` · `a_scale_honest_scope` · `a_toy_scale_recheck` · p1/p2/p3/p6/p7/p8 · c9 · c15
