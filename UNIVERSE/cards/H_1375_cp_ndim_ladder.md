# H_1375 — CP DIMENSIONAL LADDER (move-the-cells beyond 2-D, D ∈ {2,3,4,6,8})

**slug** `cp_ndim_ladder` · **tier** 🧱 BREAKS-AT-D*=3 (CONCENTRATION-ONLY; RELOCATION DIMENSION-INVARIANT) · **DIRECTIONAL** numpy mirror, $0 CPU, 3 seeds [4333,4334,4335], live CORE UNTOUCHED · realizes user direction "2d 말고도 차원늘려봐"

## Claim
H_1360 (🟢 1-D) → H_1369 (🟢 2-D axis) → H_1374 (🧱 2-D diagonal: RELOCATION generalizes, COH separation axis-aligned-only) proved move-the-cells (physically RELOCATE residual phase-1 prototype cells along the boundary NORMAL toward a shifted hyperplane) is a geometric law. **Does it survive a CONSTANT Monte-Carlo sample size N=169 as the feature dimension D grows** (D = 2 → 3 → 4 → 6 → 8)? Constant-N in growing-D is itself the curse-of-dimensionality stressor — the point. Lens: a_no_llm_frame_trap (geometry-of-representation / curse-of-dimensionality), a_break_the_wall, a_scale_honest_scope.

## Method
- TRUE partition `cat = int(⟨w,x⟩ > c)`, **w = per-seed FIXED unit normal in R^D** (ONLY D varied across the ladder; w orientation held constant per seed). Cut shifts c_A (1/3 quantile of ⟨w,x⟩) → c_A' (2/3 quantile), quantiles from a frozen reference sample so both phases see a balanced split at every D.
- move-the-cells: drift residual phase-1 cells' source position **ALONG +w** so their projection s_i→c_A' (orthogonal complement = irrelevant axes, untouched), re-embed, re-read label. eta=0.15 FROZEN (= H_1369).
- **Metrics** (per D, generalizing H_1369's COH2D, all measured ALONG THE NORMAL): RELOCATION = |ridge_s − c_A'| (projection-onto-w centroid of the ridge); **COH_D** = S_CONC·(1−RIDGE_FRAC), S_CONC = 1−min(1, s_std/S_STD_REF), scores ONLY the normal-projection spread (bounded → no NCOMP saturation, the H_1369 R1 lesson by design). Discrimination field = max |Δposterior| to KNN=4 nearest sample neighbors (kNN because a Monte-Carlo cloud has no lattice neighbors).
- **CONSTANT N=169** sample (= H_1369 13×13 budget) at every D = the deliberate stressor. DIM=64 RBF centers fixed across D. 4 arms: RE-PACK (eta=.15) / SPLIT-ONLY (eta=0, H_1364 ablation) / NO-RETRAIN (holds c_A) / SHUFFLE (anti-Goodhart). 3 seeds.

## Frozen bars (verbatim mirror of H_1369 R2; NO threshold moved — `.verdicts/1375_cp_ndim_ladder/FREEZE.txt`)
LOC_TOL=0.12 · COH_MIN=0.50 · COH_SEP=0.10 · SHUF_COH_MAX=0.20 · S_STD_REF=0.20. Per-D pass iff (1) RELOCATION |ridge_s−c_A'|≤0.12 all seeds · (2) COH_D ≥0.50 AND ≥ split-only+0.10 · (3) EARNED (no-retrain holds c_A AND shuffle COH_D≤0.20) · (4) DISTINCT (split-only stays short >0.12). Ladder verdict declared up front: 🟢 DIMENSION-INVARIANT if all D pass; 🧱 BREAKS-AT-D* with the smallest failing D* reported.

## Result — 🧱 BREAKS-AT-D*=3 (the break is c2 COHERENCE; c1 RELOCATION is dimension-invariant)

| D | RELOCATION \|rs−c_A'\| | COH_D re-pack/split/shuf | c1 | c2 | c3 | c4 | PASS |
|---|---|---|---|---|---|---|---|
| 2 | 0.008 | 0.714 / 0.297 / 0.045 | ✅ | ✅ | ✅ | ✅ | **PASS** |
| 3 | 0.018 | 0.428 / 0.221 / 0.026 | ✅ | ❌ | ✅ | ✅ | FAIL (c2) |
| 4 | 0.034 | 0.201 / 0.000 / 0.000 | ✅ | ❌ | ✅ | ✅ | FAIL (c2) |
| 6 | 0.041 | 0.079 / 0.000 / 0.000 | ✅ | ❌ | ✅ | ❌ | FAIL (c2,c4) |
| 8 | 0.052 | 0.038 / 0.000 / 0.000 | ✅ | ❌ | ✅ | ✅ | FAIL (c2) |

- **c1 RELOCATION is DIMENSION-INVARIANT** — `|rs−c_A'|` stays tiny (0.008→0.018→0.034→0.041→0.052) across the WHOLE ladder. The move-the-cells geometric law (drift cells along the normal to land the discrimination ridge on the moved hyperplane) survives growing D unbroken. The ridge always relocates to c_A'.
- **c2 COHERENCE breaks at D*=3** — bounded COH_D collapses monotonically (0.714 → 0.428 → 0.201 → 0.079 → 0.038), below COH_MIN=0.50 from D=3 on. With CONSTANT N=169 the orthogonal-complement volume explodes as D grows, the sample sparsifies, and the discrimination ridge can no longer stay a thin concentrated hyperplane — the classic curse-of-dimensionality at constant sample budget. (At D≥4 split-only/shuffle COH_D hit 0.000 too — the smear is so sparse no concentrated ridge forms at all.)
- c3 EARNED holds every D (no-retrain holds c_A ≤0.12; shuffle COH_D ≤0.026 collapses). c4 DISTINCT holds except D=6 (split-only 0.105 dipped just under LOC_TOL there — a sparse-cloud fluctuation, not a relocation win for split-only).

### a_break_the_wall (frozen-first, pre-registered): WHITENED ladder — did NOT rescue
Re-ran the full ladder drifting+scoring in the per-axis-standardized isotropic frame (SAME bars). Whitening blew up the projection scale (the per-axis std rescale of [0,1]^D pushes c_A negative and inflates the normal), so RELOCATION (c1) itself broke and COH_D=0.000 everywhere — a **failed rescue**, strictly worse than the primary. This CONFIRMS the D*=3 concentration break is REAL (a genuine constant-N sparsity ceiling), not a frame artifact the whitening angle could remove. NO bar moved (c9/c16/p7).

## Honest verdict (c9)
move-the-cells **RELOCATION** is a dimension-invariant geometric law (1-D / 2-D-axis / 2-D-diagonal / N-D up to D=8 all relocate the ridge onto the moved hyperplane). What BREAKS at D*=3 is the bounded **CONCENTRATION** (COH_D ≥0.50): a thin coherent ridge cannot be maintained at CONSTANT N=169 once D≥3 — the curse of dimensionality at fixed sample budget. This is the same family lesson as H_1374 (the COH concentration stringency is the fragile part, the relocation is robust), now along the dimension axis. The pre-registered whitening rescue did not help (failed rescue) → the break is terminal under constant-N.

## Scope (UNVERIFIED — a_scale_honest_scope / a_toy_scale_recheck)
DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED). TOY: N=169 Monte-Carlo / 3 seeds / DIM=64 / one normal per seed / deterministic readout (tests dimensional STRUCTURE, not a learned net). **Constant-N is a chosen STRESSOR, not a realistic data regime** — scaling N with D (e.g. N∝const·c^D) was explicitly NOT taken (the whole point was to hold N fixed). Whether relocation+concentration BOTH survive when N scales with D is the natural next round and is UNVERIFIED here. Scale / real-corpus / learned-net / per-D-N-scaling unverified. live CORE/*.hexa UNTOUCHED (wires nothing).

## Artifacts
- `state/cp-ndim/h1375_cp_ndim_ladder.py`
- `.verdicts/1375_cp_ndim_ladder/{FREEZE.txt, result.txt}`

## xref
H_1360 (1-D move-the-cells 🟢) · H_1369 (2-D axis 🟢, COH2D source metric) · H_1374 (2-D diagonal 🧱, COH stringency axis-aligned-only) · H_1364 (split-only ablation) · H_1343 (RBF population code, metric-space artifact) · a_no_llm_frame_trap · a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · c9 · c15 · c16.
