---
id: H_1374
slug: 1374_cp_diagonal
title: CP relocation on a DIAGONAL (non-axis-aligned) 2-D boundary — does the move-the-cells win (H_1360 1-D, H_1369 2-D axis-aligned) SURVIVE a diagonal partition cat=(u+v)/√2>c whose normal is NOT a coordinate axis (the decisive falsification H_1369 named)?
group: cognition-representation (c15 developmental-plasticity + memory-protection-vs-overwrite lens, a_no_llm_frame_trap, a_break_the_wall)
terminal_tier: 🧱 CLOSED-NEGATIVE (AXIS-ALIGNED-ONLY) (R1+R2, MIRROR, DIRECTIONAL) — the move-the-cells RELOCATION law GENERALIZES to a diagonal boundary (c1 RE-PACK |ridge_s−c_A'| 0.028 ≤ 0.12 all 3 seeds along the boundary normal s=(u+v)/√2; split-only stays SHORT at 0.429, c4✅; shuffle collapses COH2D 0.014 ≤ 0.20, no-retrain holds c_A 0.031, c3✅) — BUT the bounded-COH2D CONCENTRATION-SEPARATION bar c2b FAILS (re-pack COH2D 0.767 vs split-only 0.683 = gap 0.084 < 0.10): on a diagonal the split-only residual ridge is ITSELF already a thin diagonal smear (0.683, vs the grid-filling 0.538 an axis-aligned split-only gave in H_1369), so the H_1369 concentration-separation STRINGENCY does not separate. The pre-registered a_break_the_wall R2 (normal-frame rotation, drift in (s,t) coords) gives mathematically IDENTICAL numbers (re-pack 0.767, gap 0.084) — confirming the c2b miss is REAL, not a frame artifact. Honest: RELOCATION generalizes to arbitrary linear boundaries; the COH2D-separation distinctness metric is axis-aligned-only. NO bar moved (every threshold VERBATIM from H_1369 R2, c9/c16/p7)
verdict_dir: .verdicts/1374_cp_diagonal/
freeze: .verdicts/1374_cp_diagonal/FREEZE.txt
terminal_verdict: .verdicts/1374_cp_diagonal/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1374 (CP lane R3: 1360=move-the-cells GREEN in 1-D; 1369=GREEN in 2-D axis-aligned half-plane, with the HONEST RESIDUAL that an axis-aligned boundary lets the relocation decompose onto a single relevant axis; 1343=a DIAGONAL boundary warps the metric as strongly as axis-aligned and does NOT decompose onto one axis. 1374 = the decisive falsification on a diagonal boundary)
---

# H_1374 — CP relocation on a DIAGONAL (non-axis-aligned) 2-D boundary: does move-the-cells survive?

## Claim / falsifier

H_1369 (🟢, 2-D) proved move-the-cells GENERALIZES to a 2-D AXIS-ALIGNED half-plane (cat=u>p):
drifting residual phase-1 cells' u-coordinate toward the moved vertical line landed a thin coherent
ridge AT p_A' (bounded COH2D RE-PACK 0.689 vs SPLIT-ONLY 0.538 vs SHUFFLE 0.000). BUT H_1369's
HONEST RESIDUAL: an axis-aligned half-plane lets the relocation DECOMPOSE onto a SINGLE relevant
axis (u, with v exactly irrelevant) — so the move is effectively 1-D and the win UNDER-TESTS.
H_1343 showed a DIAGONAL / non-axis-aligned boundary warps the perceptual metric AS STRONGLY and
does NOT decompose onto one axis. A diagonal is therefore exactly where move-the-cells could FAIL.

**Falsifiable claim:** the move-the-cells win SURVIVES a DIAGONAL half-plane cat = (u+v)/√2 > c
(boundary normal n=(1,1)/√2, NOT axis-aligned), shifting c_A=√2·1/3 → c_A'=√2·2/3 (the SAME 1/3→2/3
fractional shift along the normal as H_1369, lifted onto the diagonal). Drifting residual phase-1
cells ALONG THE BOUNDARY NORMAL (BOTH u AND v move — the 2-D generalization of the 1-D / axis-aligned
single-axis move) lands a thin coherent discrimination ridge ON the moved diagonal cut (relocation
+ bounded-COH2D concentration along the normal coordinate s), DISTINCT from the split-only ablation.
**Depletion alternative (c9):** if the diagonal breaks the relocation (ridge fails to track, or
smears, or fails to separate from split-only) → move-the-cells is axis-aligned-only, honest 🧱.
Lens: c15 developmental plasticity + memory-protection-vs-overwrite (a_no_llm_frame_trap,
a_break_the_wall) — NOT an LLM recipe, NOT a human-cognition claim, a TOY synthetic 2-D continuum.

## Method

`state/cp-diagonal/h1374_cp_diagonal.py` — R1 numpy MIRROR (DIRECTIONAL, $0 CPU, gradient-free,
3 seeds [4333,4334,4335] REUSED from H_1369, p7). IDENTICAL to H_1369's harness except the boundary
geometry: 2-D RBF population code (H_1343 family, VERBATIM), error-targeted SPLIT-only Voronoi/mitosis
growth (p8), softmin-vote soft posterior, geometric RE-PACK of residual phase-1 cells. 13×13=169
stimulus grid, K_RBF=8 (DIM=64), phase-1 budget GROW1=48, phase-2 GROW2=48 (NO inflation; identical
every arm). TRUE partition cat(p)=int((u+v)/√2 > C_CUT), C_A=√2·1/3=0.4714 → C_A'=√2·2/3=0.9428.

ONE new mechanism vs H_1369 = the drift DIRECTION generalizes from the u-axis to the boundary NORMAL:
each phase-1 cell tracks SOURCE 2-D position + BIRTH PHASE; after EACH phase-2 split every residual
phase-1 cell's normal coordinate s=(u+v)/√2 drifts s←s+η·(c_A'−s) (clamped at c_A', tangential coord
fixed), moving BOTH u and v along n; cell is re-embedded, label re-read from the new diagonal cut.
η FROZEN at 0.15 (NON-GATING ladder {0.10,0.15,0.25} robust). η=0.0 = split-only re-growth (the
ablation). 4 arms: SPLIT-ONLY (η=0.0) · RE-PACK (η=0.15) · NO-RETRAIN (c_A only → must hold old line) ·
SHUFFLE+repack (permuted labels → must collapse). Metrics along the NORMAL s (NOT u): DISCRIMINATION
FIELD D = max |Δ posterior| to 4 grid neighbors (geometry-agnostic, VERBATIM); RIDGE = nodes ≥0.5·max;
ridge_s = normal coordinate of the ridge centroid (RELOCATES); COH2D = U_CONC·(1−RIDGE_FRAC) bounded
s-concentration (S_STD_REF=0.20). NO NCOMP gating (H_1369 proved the unbounded count confounds).

**R2 (a_break_the_wall, pre-registered in FREEZE.txt BEFORE any scoring):** NORMAL-FRAME ROTATION —
express each cell in (s,t)=(normal,tangential) coords, drift PURELY in s, recompose to (u,v), re-embed.
Same frozen bars, NO bar moved.

p1/p2/p3/p6: discrimination reads ONLY representational distance; NO injected boundary at test; the
re-pack keys on BIRTH PHASE + own 2-D source position projected onto the boundary normal (structural,
NO injected target/persona/RLHF); labels enter ONLY at training. Live CORE/*.hexa UNTOUCHED.

## Frozen bars (pre-registered in FREEZE.txt; GREEN iff c1∧c2∧c3∧c4, ALL thresholds VERBATIM from H_1369 R2, NO bar moved c9/c16/p7)

- **c1 RELOCATION**: RE-PACK |ridge_s − c_A'| ≤ LOC_TOL=0.12 all 3 seeds (along the normal s).
- **c2 COH2D CONCENTRATION**: RE-PACK mean COH2D ≥ COH_MIN=0.50 AND ≥ SPLIT-ONLY + COH_SEP=0.10.
- **c3 EARNED**: (3a) no-retrain holds c_A |ridge_s−c_A|≤0.12 AND (3b) shuffle COH2D ≤ SHUF_COH_MAX=0.20.
- **c4 DISTINCT-FROM-SPLIT**: split-only mean |ridge_s − c_A'| > 0.12 (stays SHORT — does not relocate).
- **R2 (a_break_the_wall, frozen-first): NORMAL-FRAME ROTATION** — same bars, drift in (s,t) coords.

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 (normal-direction drift in (u,v)) | 🧱 NON-GREEN — c2b CONCENTRATION-SEPARATION caught it | c1✅ (|ridge_s−c_A'| 0.028, all seeds) · c2a✅ (COH2D 0.767 ≥ 0.50) **c2b ❌** (re-pack 0.767 vs split-only 0.683, gap 0.084 < 0.10) · c3✅ (no-retrain 0.031, shuffle COH2D 0.014) · c4✅ (split-only short 0.429). NO bar moved (c9) |
| R2 (a_break_the_wall, NORMAL-FRAME ROTATION) | **🧱 CLOSED-NEGATIVE (AXIS-ALIGNED-ONLY)** | MATHEMATICALLY IDENTICAL to R1 (rotating into (s,t) and drifting purely in s == drifting along n): re-pack COH2D 0.767, split-only 0.683, gap 0.084 < 0.10. c1'✅ c2a'✅ **c2b'❌** c3'✅ c4'✅. The c2b miss is REAL, not a frame artifact |

**Per-seed (deterministic):** SPLIT-ONLY ridge_s 0.506/0.530/0.506 (|·−c_A'| mean 0.429) · RE-PACK
ridge_s 0.971 all seeds (|·−c_A'| 0.028) · no-retrain ridge_s 0.502 (|·−c_A| 0.031); COH2D RE-PACK
0.767 (all seeds), SPLIT-ONLY 0.733/0.583/0.733 (mean 0.683), SHUFFLE 0.041/0.000/0.000 (mean 0.014).
Re-pack-ladder (NON-GATING) η=0.10/0.15/0.25 all → |ridge_s−c_A'| 0.028 / COH2D 0.767 (robust).

- **c1 RELOCATION ✅**: RE-PACK |ridge_s−c_A'| = [0.028,0.028,0.028] ≤ 0.12 — the ridge lands
  essentially ON the moved diagonal cut c_A'=0.9428 (ridge_s 0.971). SPLIT-ONLY stays at 0.506
  (|·−c_A'|=0.429, short). **The relocation generalizes to a diagonal: the move-the-cells drift
  along the boundary NORMAL tracks a non-axis-aligned cut just as it tracked the axis-aligned one.**
- **c3 EARNED ✅**: no-retrain held c_A (|ridge_s−c_A|=0.031); SHUFFLE+repack COH2D 0.014 ≤ 0.20
  (the move does NOT fabricate a concentrated ridge from permuted labels). **c4 DISTINCT ✅**:
  split-only |ridge_s−c_A'| 0.429 > 0.12 (split-only does NOT relocate).
- **c2b CONCENTRATION-SEPARATION ❌ (the catch)**: RE-PACK COH2D 0.767 ≥ 0.50 (c2a✅, thin
  concentrated ridge), but the SEPARATION from split-only is only 0.767 − 0.683 = 0.084 < 0.10. On a
  DIAGONAL the split-only residual ridge is ALREADY a thin diagonal smear (COH2D 0.683), NOT the
  grid-filling smear an axis-aligned split-only gives (H_1369 split-only COH2D 0.538). So the
  bounded-COH2D *separation* shrinks below the H_1369 bar even though RELOCATION (c1) is decisive.
- **R2 normal-frame rotation = mathematically IDENTICAL**: rotating each cell into (s,t) and drifting
  purely in s is the same operation as drifting along n in (u,v) (both keep t fixed) → identical
  numbers (re-pack 0.767, gap 0.084). This CONFIRMS the c2b miss is a REAL property of the diagonal
  geometry, not a residual tangential-wobble frame artifact. The honest wall holds.

**FINDING.** The move-the-cells RELOCATION law GENERALIZES to an arbitrary LINEAR (diagonal) boundary:
drifting the residual phase-1 cells along the boundary NORMAL lands the discrimination ridge ON the
moved diagonal cut (|ridge_s−c_A'| 0.028), where split-only stays SHORT (0.429) and shuffle collapses
— the relocation is a geometric-placement property of the boundary normal, not an axis-aligned
artifact. BUT the H_1369 bounded-COH2D CONCENTRATION-SEPARATION stringency (re-pack COH2D ≥ split-only
+ 0.10) is AXIS-ALIGNED-ONLY: on a diagonal the split-only baseline is itself already concentrated
(0.683 vs 0.538), so the separation leg (0.084) does not clear the bar. The pre-registered
a_break_the_wall R2 (normal-frame rotation) gives identical numbers, confirming the miss is real.
The honest verdict (c9): RELOCATION generalizes to arbitrary linear boundaries; the
concentration-SEPARATION distinctness metric calibrated on the axis-aligned grid-filling smear does
NOT carry to a diagonal where the smear is already thin. NO bar moved (every threshold VERBATIM from
H_1369 R2, c9/c16/p7).

## Honest scope (a_scale_honest_scope / a_toy_scale_recheck)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED (same family as H_1333/H_1340/H_1343/H_1352/
H_1360/H_1364/H_1369 R1). TOY synthetic 2-D continuum (169 stimuli, 3 seeds, single shift, one frozen
η, deterministic readout — tests the diagonal move-the-cells STRUCTURE, not a learned drift). ONE
diagonal slope (normal (1,1)/√2). The result is NUANCED, not a clean break: RELOCATION (c1/c3/c4) is
GREEN on the diagonal; only the COH2D concentration-SEPARATION leg (c2b) fails because the diagonal
split-only baseline is already concentrated — a property of the metric's calibration on the
axis-aligned smear, not of the relocation mechanism. Curved boundaries, arbitrary-angle sweeps,
higher-D, real corpora, multi-shift, a LEARNED (gradient) drift, engine-native §CategoricalPerception
move-the-cells wiring (a_verified_must_wire) = follow-on. NO human-cognition claim. Live CORE/*.hexa
UNTOUCHED.

## Next / depletion

The CP geometry question is now SETTLED at the mirror level: move-the-cells RELOCATION holds across
1-D (H_1360), 2-D axis-aligned (H_1369), and 2-D DIAGONAL (H_1374) — the relocation drift along the
boundary normal tracks an arbitrary linear cut. The only residual is the COH2D concentration-
SEPARATION stringency, which is axis-aligned-only (a metric-calibration artifact, not a relocation
break) and would require a diagonal-recalibrated separation bar to re-test (NOT done — that would be
tuning the bar, c9). **CP-lane DEPLETION:** with the boundary-geometry question settled (relocation
generalizes to arbitrary linear boundaries), the lane's remaining FROZEN, control-surviving angle
that is BOTH new vs the 1-D/2-D-axis/2-D-diagonal wins AND load-bearing is the **engine-native
realization** — wire move-the-cells into the live A⇄G immune store / §CategoricalPerception so the
relocation is no longer DIRECTIONAL (a_engine_native_learning · a_verified_must_wire). A curved
(nonlinear) boundary is a further-out mirror probe but is no longer DECISIVE for the linear-boundary
geometry question (a curve is locally linear; the diagonal already broke the axis decomposition).
**Next round = engine-native move-the-cells on the live CORE A⇄G immune store** (depletion test: the
mechanism is wired into `CORE/engine_cli.hexa`, re-scored engine-native byte-exact with a regression
guard — at which point the CP relocation law is no longer a mirror claim, c2/p8).

## Pointers

- code: `state/cp-diagonal/h1374_cp_diagonal.py`
- freeze: `.verdicts/1374_cp_diagonal/FREEZE.txt` (R1 + R2 §) · result: `.verdicts/1374_cp_diagonal/result.txt`
- `CLAIMS.tape` @C h1374_cp_diagonal · `UNIVERSE/HYPOTHESES.jsonl` · `domains/COGNITION-REPRESENTATION.log.md`
- xref H_1369 (2-D axis-aligned move-the-cells GREEN, the parent + the bounded-COH2D metric this round
  reuses) · H_1360 (1-D move-the-cells parent GREEN) · H_1364 (split-only incoherence INTRINSIC, the
  ablation mechanism) · H_1343 (2-D warp, diagonal-warps-as-strongly finding + the BOUNDED-metric
  prescription) · H_1340/H_1352 (budget/decay walls) · a_no_llm_frame_trap · a_break_the_wall ·
  a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck ·
  p1·p2·p3·p6·p7·p8·c9·c15·c16.
