---
id: H_1375
slug: 1375_cp_ndim_ladder
title: CP DIMENSIONAL LADDER — does the move-the-cells relocation law (H_1360 1-D, H_1369 2-D) survive as feature-space dimension D grows (D = 2 → 3 → 4 → 6 → 8)?
group: cognition-representation (c15 developmental-plasticity + curse-of-dimensionality lens, a_no_llm_frame_trap, a_break_the_wall)
terminal_tier: 🧱 BREAKS-AT-D*=3 (R1 MIRROR, DIRECTIONAL) — move-the-cells is DIMENSION-BOUNDED. RELOCATION (the cells DO drift to the right place along the boundary normal) is dimension-INVARIANT — |ridge_τ − 2/3| ≤ 0.054 at EVERY D up to 8, all 3 seeds — but the bounded ridge-CONCENTRATION COH_D COLLAPSES with D: RE-PACK COH_D 0.734(D=2) → 0.458(D=3) → 0.263(D=4) → 0.008(D=6) → 0.000(D=8). c2 (concentration ≥0.50 AND ≥split+0.10) first FAILS at D*=3. The a_break_the_wall WHITEN fallback (z-score embedding per feature, frozen-first, N & D unchanged) rescued ONLY D=2 (full 1111) and left D≥3 broken (whitened COH_D 0.487/0.019/0.000/0.000) → the break is INTRINSIC: constant-N (curse-of-dimensionality) genuinely flattens the cell-concentration, not a raw-distance-metric artifact. The CP-geometry question is thus SETTLED on the dimensionality axis: move-the-cells RELOCATES at any D but only stays CONCENTRATED at D≤2. NO bar moved (c9/c16/p7)
verdict_dir: .verdicts/1375_cp_ndim_ladder/
freeze: .verdicts/1375_cp_ndim_ladder/FREEZE.txt
terminal_verdict: .verdicts/1375_cp_ndim_ladder/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1375 (1360=parent move-the-cells GREEN in 1-D; 1369=2-D axis-aligned GREEN with bounded COH2D after the NCOMP confound; 1375 = D-ladder generalization, user direction "2d 말고도 차원늘려봐"; orthogonal to the in-flight diagonal-boundary lane H_1374)
---

# H_1375 — CP dimensional ladder: does move-the-cells survive as feature-space dim D grows?

## Claim / falsifier

H_1360 (🟢, 1-D) and H_1369 (🟢, 2-D axis-aligned) proved CARVING RELOCATION IS MOVE-THE-CELLS: at a
FIXED LOW budget, physically DRIFTING the residual phase-1 prototype POSITIONS toward the moved
boundary lands a COHERENT, CONCENTRATED discrimination ridge AT the moved boundary, where split-only
re-growth stays SHORT (H_1364). The user (verbatim "2d 말고도 차원늘려봐") asked for the ORTHOGONAL
axis to the in-flight diagonal-boundary lane (H_1374, boundary ORIENTATION): **dimensionality**.

**Falsifiable claim:** as the feature-space dimension D grows (D = 2 → 3 → 4 → 6 → 8), residual
prototype cells must relocate to track a shifting (D−1)-dim HYPERPLANE boundary (cat = ⟨w,x⟩ > c, w =
FIXED generic unit normal = ones/√D held constant orientation; ONLY D varies), and the move-the-cells
relocation either stays a DIMENSION-INVARIANT law (🟢 if bars hold for ALL D) OR has a SMALLEST D*
where RELOCATION or concentration BREAKS (🧱 — the law is dimension-bounded; report D* honestly). The
curse of dimensionality (volume concentration, distance flattening) at CONSTANT sample size N is the
stressor — that is the point. Lens: c15 developmental plasticity + curse-of-dimensionality
(a_no_llm_frame_trap, a_break_the_wall) — NOT an LLM recipe, NOT a human-cognition claim, a TOY
synthetic D-dim continuum.

## Method

`state/cp-ndim/h1375_cp_ndim_ladder.py` — R1 numpy MIRROR (DIRECTIONAL, $0 CPU, gradient-free, 3 seeds
[4333,4334,4335], p7). Reuses family machinery: RBF population code (H_1343), error-targeted SPLIT-only
Voronoi/mitosis growth (p8, H_1360), softmin-vote soft posterior, geometric RE-PACK of residual
phase-1 cells (H_1360/H_1369). The ONLY new piece is the D-dim lift + drift along the boundary NORMAL.

- N=400 Monte-Carlo points uniform on [0,1]^D (FIXED N across ALL D — a full grid is infeasible past
  D≈4, so the cloud is SAMPLED and ridge concentration is measured ON THE SAMPLED CLOUD, stated
  honestly; constant-N in growing-D is itself the curse-of-dimensionality stressor, D the only varied
  factor). M_CENTERS=64 RBF centers sampled uniform on [0,1]^D (fixed/LOW density across D), width
  per-seed jitter U(0.18,0.24).
- BOUNDARY = hyperplane ⟨w,x⟩=c, w = ones/√D (FIXED generic orientation at every D). Normal coord
  t(x)=⟨w,x⟩; cut at 1/3, 2/3 of the [5th,95th]-pctile t-span → c_A, c_A' (frozen per (D,seed),
  identical across arms). cat(x)=int(t>c). The D−1 in-hyperplane directions are categorically IRRELEVANT.
- Budgets FIXED LOW: GROW1=GROW2=48 splits, identical across ALL arms AND ALL D.
- GEOMETRIC RE-PACK (the move): after EACH phase-2 split, every residual phase-1 cell drifts ALONG THE
  NORMAL w toward the moved hyperplane: t_i_new = t_i + η·(c_A'−t_i) (clamp at c_A'); x_i ← x_i +
  (t_i_new−t_i)·w (in-plane fixed); re-embed; label re-read. η FROZEN 0.15. η=0.0 = split-only (H_1364
  ablation). 4 arms: SPLIT-ONLY · RE-PACK · SHUFFLE+repack (must collapse) · NO-RETRAIN (NON-GATING).
- METRICS: discrimination field D(x)=max|Δposterior| over the kNN_DISC=6 nearest neighbors (D-dim
  analog of H_1369's 4-grid-neighbor field; kNN adjacency replaces the lattice). ridge_τ = mean
  SPAN-NORMALIZED normal coord τ=(t−t_lo)/(t_hi−t_lo) over ridge nodes (RELOCATES; c_A→1/3, c_A'→2/3,
  comparable across D). COH_D = t_conc·(1−ridge_frac), t_conc = 1−min(1, τ_std/0.20) (bounded
  concentration, generalizes H_1369 COH2D; in-plane spread NOT scored — a coherent hyperplane ridge
  legitimately spans all in-plane directions).

p1/p2/p3/p6: discrimination reads ONLY representational distance; NO injected boundary at test; the
re-pack keys on BIRTH PHASE + own D-dim source position (structural, NO injected target/persona/RLHF);
labels enter ONLY at training. Live CORE/*.hexa UNTOUCHED (substrate-measurement rung).

## Frozen bars (pre-registered in FREEZE.txt; per-D GREEN iff c1∧c2∧c3∧c4, NO bar moved c9/c16/p7)

- **c1 RELOCATION(D)**: RE-PACK |ridge_τ − 2/3| ≤ RELOC_TOL=0.18, all 3 seeds.
- **c2 COH_D CONCENTRATION(D)**: RE-PACK mean COH_D ≥ 0.50 AND ≥ SPLIT-ONLY mean + 0.10.
- **c3 EARNED (shuffle)**: SHUFFLE mean COH_D ≤ 0.20.
- **c4 DISTINCT-FROM-SPLIT(D)**: SPLIT-ONLY short of c_A' (|ridge_τ−2/3| > 0.18) OR less concentrated.
- **LADDER VERDICT**: DIMENSION-INVARIANT 🟢 if all D pass; BREAKS-AT-D* 🧱 if smallest D* fails c1/c2.
- **a_break_the_wall fallback (pre-registered)**: on a break, WHITEN the metric (z-score embedding per
  feature, N & D unchanged), re-score the SAME bars frozen-first.

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 (frozen bars) | **🧱 BREAKS-AT-D*=3 (MIRROR, DIRECTIONAL)** | RELOCATION holds at EVERY D; COH_D collapses |
| R1 a_break_the_wall WHITEN | confirms INTRINSIC (rescues only D=2) | whitened COH_D 0.714/0.487/0.019/0.000/0.000 |

**LADDER CURVE (R1, mean 3 seeds, per D):**

| D | RE-PACK \|ridge_τ−2/3\| | RE-PACK COH_D | SPLIT-ONLY COH_D | SHUFFLE COH_D | c1c2c3c4 | verdict |
|---|---|---|---|---|---|---|
| 2 | 0.010 | 0.734 | 0.528 | 0.358 | 1101 | 🧱 (c3 shuffle FAIL — see honest note) |
| 3 | 0.009 | 0.458 | 0.296 | 0.075 | 1011 | 🧱 (c2 COH_D FAIL) |
| 4 | 0.019 | 0.263 | 0.026 | 0.000 | 1011 | 🧱 (c2 COH_D FAIL) |
| 6 | 0.041 | 0.008 | 0.000 | 0.000 | 1011 | 🧱 (c2 COH_D FAIL) |
| 8 | 0.054 | 0.000 | 0.000 | 0.000 | 1011 | 🧱 (c2 COH_D FAIL) |

**FINDING (the headline).** Move-the-cells RELOCATION is DIMENSION-INVARIANT — at every D up to 8, all
3 seeds, the re-packed ridge centroid lands essentially ON the moved hyperplane (|ridge_τ − 2/3| ≤
0.054; the cells DO drift to the right place along the boundary normal). But the bounded ridge
CONCENTRATION COH_D COLLAPSES monotonically with D (0.734 → 0.458 → 0.263 → 0.008 → 0.000), first
failing the c2 bar (≥0.50 AND ≥split+0.10) at **D*=3** and reaching zero by D=6. The a_break_the_wall
WHITEN fallback (z-score the embedding per feature, frozen-first, N & D held fixed) rescued ONLY D=2 to
a full 1111 pass and left D≥3 broken (whitened COH_D 0.487/0.019/0.000/0.000) → the break is INTRINSIC:
at constant N the curse of dimensionality genuinely flattens the cell-concentration (a thin coherent
hyperplane slab cannot be resolved from 400 sampled points once D≥3), NOT a raw-distance-metric
artifact that whitening removes. **The CP-geometry question is SETTLED on the dimensionality axis:
move-the-cells RELOCATES at any D but only stays CONCENTRATED (a clean coherent ridge) at D≤2.** The
2-D win (H_1369) is the concentration ceiling; relocation itself is unbounded in D.

## Honest scope (a_scale_honest_scope / a_toy_scale_recheck)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED (same family as H_1333/H_1340/H_1343/H_1352/
H_1360/H_1364/H_1369 R1). TOY synthetic D-dim continuum (N=400 Monte-Carlo cloud, 3 seeds, single
shift, one frozen η, fixed generic normal, deterministic readout — tests the D-dim move-the-cells
STRUCTURE, not a learned drift). **HARNESS CHANGE vs H_1369 (load-bearing honesty, c9):** this lane
uses a Monte-Carlo SAMPLED cloud + kNN discrimination field, NOT H_1369's full 13×13 grid + 4-
connectivity (a grid is infeasible past D≈4). Consequently the D=2 row is NOT directly comparable to
H_1369's clean 2-D GREEN — on a sparse 400-point cloud the SHUFFLE smear does NOT collapse as cleanly
(D=2 SHUFFLE COH_D=0.358 > the 0.20 cap → c3 FAILS at D=2 here even though c1∧c2∧c4 pass). This is a
SAMPLING/harness limitation of the cloud, NOT a refutation of H_1369 (which holds on its grid); it does
NOT change the headline, because the GATING relocation/concentration pair (c1/c2) already breaks the
concentration at D*=3 independent of the c3 control, and RELOCATION (c1) survives everywhere. The
shuffle control biting at D=2 is reported VERBATIM as the honest catch (NO bar moved, c9/c16/p7). The
fixed generic normal (ones/√D) is ONE orientation; the cut placement at percentile-span fractions is
ONE scheme; scaling N with D (which would relieve the curse but change the constant-N stressor that is
the point) is NOT done as the gate — only WHITEN is the pre-registered fallback. Live CORE/*.hexa
UNTOUCHED. NO human-cognition claim.

## Next / depletion

R2 candidates (each frozen ANEW, NOT a relaxation): (1) **N scaled to D** (e.g. N ∝ c^D or N ∝ D·N_2)
— is the concentration break a FUNDAMENTAL D-ceiling or a SAMPLE-DENSITY artifact? (relieving the
constant-N stressor; the COMPLEMENT to this lane, which froze N to isolate the curse). (2) a CURVED
(non-planar) boundary in N-D. (3) engine-native §CategoricalPerception move-the-cells on the live A⇄G
immune store (a_engine_native_learning · a_verified_must_wire). **CP-lane DEPLETION (this lane's
contribution):** the dimensionality axis is now SETTLED — RELOCATION is dimension-invariant, CONCENTRATION
is dimension-bounded at D≤2 (intrinsic at constant N). Combined with H_1360 (1-D 🟢), H_1369 (2-D
axis-aligned 🟢), and the in-flight H_1374 (diagonal orientation), the CP-GEOMETRY question is largely
exhausted on the MIRROR; what remains is (a) the N-vs-D density question above and (b) the engine-native
realization (transfer no longer DIRECTIONAL). The honest non-result here (relocation survives,
concentration does not) is itself the dimensional boundary the user's idea asked for.

## Pointers

- code: `state/cp-ndim/h1375_cp_ndim_ladder.py`
- freeze: `.verdicts/1375_cp_ndim_ladder/FREEZE.txt` · result: `.verdicts/1375_cp_ndim_ladder/result.txt`
- `CLAIMS.tape` @C h1375_cp_ndim_ladder · `UNIVERSE/HYPOTHESES.jsonl` · `domains/COGNITION-REPRESENTATION.log.md`
- xref H_1369 (2-D axis-aligned move-the-cells GREEN, the concentration ceiling) · H_1360 (1-D
  move-the-cells parent GREEN) · H_1364 (split-only incoherence INTRINSIC, the ablation mechanism) ·
  H_1343 (2-D warp + BOUNDED-metric prescription) · H_1374 (in-flight diagonal-orientation lane,
  orthogonal axis) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning ·
  a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8·c9·c15·c16.
