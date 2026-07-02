---
id: H_1360
slug: 1360_cp_geometric_repack
title: Whorfian CP relocation — does a GEOMETRIC RE-PACK (physically MOVE the residual phase-1 prototype POSITIONS toward p_A' during A→A' retrain, NOT raise budget or down-weight votes) recover a COHERENT single CP peak AT p_A' where the H_1340 budget-sweep AND the H_1352 soft-decay BOTH could not? The THIRD orthogonal lever (geometry), closing the budget/decay/geometry trilemma.
group: cognition-representation (c15 developmental-plasticity + memory-protection-vs-overwrite lens, a_no_llm_frame_trap, a_break_the_wall)
terminal_tier: 🟢 GREEN (MIRROR, DIRECTIONAL) — CARVING RELOCATION IS MOVE-THE-CELLS. At the FIXED LOW budget (DIM=16/GROW2=24, EQUAL to H_1352, eta=0.15), physically DRIFTING the residual phase-1 prototype positions toward p_A' lands the CP peak AT p_A' (|peak−p_A'| 0.144→**0.002**, frac +0.57→**+1.01**, all 3 seeds) AND restores a SINGLE COHERENT peak (peak-count 4.3→**1.0**) — the gate H_1340 (budget, pc 4.3→7.0) AND H_1352 (decay, pc 15.7) BOTH FAILED. c1 ✅ c2 ✅ c3 ✅ c4 ✅. NO-RETRAIN held p_A (0.002), SHUFFLE collapsed (pc 18.0 — moving cells does NOT fabricate a peak). The residual was a GEOMETRIC-PLACEMENT problem all along; budget (count) and decay (weight) were the WRONG MECHANISM. The 3-lever question CLOSES positively. NO bar moved (c9)
verdict_dir: .verdicts/1360_cp_geometric_repack/
freeze: .verdicts/1360_cp_geometric_repack/FREEZE.txt
terminal_verdict: .verdicts/1360_cp_geometric_repack/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1360 (1323=parent Sapir-Whorf; 1333=developmental-plasticity grandparent; 1338=eviction RE-DIAGNOSIS; 1340=budget-sweep DEEPER-LIMIT; 1341=shift-ladder; 1352=soft-decay DEEPER-LIMIT parent; 1355=leftward geometry; 1360 free on origin/main)
---

# H_1360 — Whorf CP relocation: geometric re-pack (move the cells)

## Claim / falsifier

H_1340 (🧱 budget) and H_1352 (🧱 soft-decay) are TWO exhausted walls. Budget buys peak-DISTANCE
toward the moved cut p_A' but DESTROYS coherence (peak-count 4.3→7.0, never ≤2). Decay relocates
the peak EVEN BETTER (frac +0.88, |peak−p_A'| 0.044) but coherence collapses HARDER (peak-count
4.3→**15.7**). **Both follow-ons exposed the SAME decisive cause** (named verbatim in the H_1352
card): the phase-1 prototypes are NEVER PHYSICALLY RELOCATED — they SIT at the old cut and inject
secondary discrimination peaks. Budget drowns them with new cells (distance↑, coherence↓); decay
quiets their VOTE but not their geometric presence (distance↑↑, coherence↓↓). The H_1352 card
names the ONLY untried lever: *"A genuinely coherent full relocation needs the old cells to MOVE
or be re-positioned (GEOMETRIC re-pack), not merely down-weighted or out-voted."*

**Falsifiable claim:** at a FIXED LOW budget (= H_1340 R0_base / H_1352, DIM=16/GROW2=24, NO
budget inflation), physically DRIFTING the residual phase-1 prototype POSITIONS toward p_A' during
A→A' re-training (move the CELLS in feature space, not their weight or count) recovers a COHERENT
full relocation: the CP peak lands AT p_A' AND peak-count returns to ~1. **Depletion alternative
(c9):** if moving the cells ALSO fails coherence → CP relocation is INTRINSICALLY partial-or-
incoherent under this RBF geometry, THREE orthogonal levers (budget=count, decay=weight,
re-pack=geometry) exhausted → terminal 🧱. Lens: c15 developmental plasticity +
memory-protection-vs-overwrite, `a_no_llm_frame_trap` / `a_break_the_wall` — NOT an LLM recipe,
NOT a human-cognition claim, a TOY synthetic continuum.

## Method

Reuses the H_1333/H_1340/H_1352 CP machinery EXACTLY (`state/universe-probes/h1333_whorf_developmental.py`,
IMPORTED verbatim): RBF position embedding, error-targeted SPLIT-only Voronoi/mitosis growth (p8),
soft category-posterior discrimination readout (NO labels at test), peak-COUNT coherence metric.
The ONE new mechanism = a **`RepackCells`** subclass that tracks each cell's SOURCE continuum
position + BIRTH PHASE. Phase-1 reuses the base `fit()` VERBATIM (then records source positions).
Phase-2 is re-implemented with the SAME H_1333 split criterion, but after EACH phase-2 split every
residual phase-1 cell's source position drifts `pos_i ← pos_i + η·(p_A'−pos_i)` (clamped at p_A',
no overshoot), the cell is RE-EMBEDDED at the drifted position, and its label is RE-READ from p_A'.
Phase-2 cells are born at their own split positions and do NOT drift. With η=0.0 the store is
byte-identical to H_1333/H_1340 R0_base (so the NO-REPACK arm reproduces the anchor IN-RUN).
Budget held at H_1340 R0_base LOW (DIM=16/GROW2=24, EQUAL to H_1352) — the ONLY change is drift.

- Arms (per seed, same low budget): (1) **NO-REPACK** (η=0.0 = anchor) · (2) **RE-PACK** (η=0.15,
  FROZEN) · (3) **NO-RETRAIN** control (p_A only, no phase-2/drift → must hold p_A) · (4)
  **SHUFFLE+repack** (permuted phase-2 labels + drift → must collapse: drift toward p_A' must NOT
  manufacture a coherent peak from noise). 3 seeds [4333,4334,4335] (SAME as H_1333/H_1338/H_1340/
  H_1352), $0 CPU, p7. A NON-GATING **re-pack-ladder** {0.10,0.15,0.25} is reported as a knife-edge
  diagnostic; the GATE is scored ONLY at η=0.15.
- p1/p2/p3/p6: the re-pack keys on a cell's BIRTH PHASE + own source position only (structural);
  readout reads ONLY representational distance; NO injected boundary location at test (labels
  re-read from the SAME p_A' that trains phase-2 cells, NO injected target peak / persona / RLHF);
  labels enter ONLY during training. NO-RETRAIN + SHUFFLE = the anti-Goodhart discriminators;
  NO-REPACK (must stay partial+incoherent in-run) isolates the geometric drift as the lever.

## Frozen bars (pre-registered in FREEZE.txt; GREEN iff c1∧c2∧c3∧c4, NO bar moved c9/p7)

- **c1 RELOCATES**: re-pack |peak−p_A'| ≤ LOC_TOL=0.12 on all 3 seeds.
- **c2 COHERENT** (load-bearing): re-pack mean peak-count ≤ 2 (the gate budget H_1340 AND decay
  H_1352 BOTH FAILED — H_1340 4.3→7.0, H_1352 15.7).
- **c3 EARNED**: (3a) no-retrain holds p_A (|peak−p_A|≤0.12) AND (3b) shuffle collapses (mean
  peak-count ≥ 3).
- **c4 vs-PRIOR**: (4a) re-pack peak-count ≤ 2 < every H_1340 rung (≥4.3) AND < H_1352 (15.7) AND
  (4b) re-pack |peak−p_A'| ≤ 0.081 (best H_1340 rung) — coherent AND close at equal/lower budget.

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 mirror (DIRECTIONAL) | 🟢 GREEN — carving relocation is MOVE-THE-CELLS | re-pack lands peak AT p_A' (|peak−p_A'| 0.144→**0.002**, frac +0.57→**+1.01**, all 3 seeds) AND single coherent peak (peak-count 4.3→**1.0**); H_1340 (pc 4.3→7.0) AND H_1352 (pc 15.7) both failed coherence. c1 ✅ c2 ✅ c3 ✅ c4 ✅ |

**R1 result (mean of 3 seeds [4333,4334,4335], deterministic):**

| arm | peak | \|peak−p_A'\| | frac | peak-count |
|---|---|---|---|---|
| NO-REPACK (η=0.0, anchor) | 0.523 | 0.144 | +0.57 | 4.3 |
| **RE-PACK (η=0.15)** | **0.669** | **0.002** | **+1.01** | **1.0** |
| NO-RETRAIN (control) | 0.331 | — (\|peak−p_A\|=0.002) | — | — |
| SHUFFLE+repack (control) | — | — | — | 18.0 |

Re-pack-ladder (NON-GATING): η=0.10 → 0.002 / pc 1.0 · η=0.15 → 0.002 / pc 1.0 (gate) · η=0.25 →
0.002 / pc 1.0. Robust across the ladder — NOT a knife-edge: any drift rate carries the cells home.

- **c1 RELOCATES ✅**: per-seed |peak−p_A'| = [0.002, 0.002, 0.002], all ≤ 0.12. The peak lands
  ESSENTIALLY ON p_A' (frac +1.01 — a FULL relocation, where budget reached +0.762 and decay +0.88
  but both incoherently).
- **c2 COHERENT ✅** (load-bearing): mean peak-count **1.0** — a single coherent CP peak on every
  seed. The gate H_1340 (≥4.3) and H_1352 (15.7) NEVER met. Moving the cells off the old cut
  ELIMINATES the residual secondary peaks that budget/decay could only fight.
- **c3 EARNED ✅**: (3a) no-retrain |peak−p_A| = 0.002 all seeds (held p_A, no drift). (3b) shuffle
  mean peak-count 18.0 ≥ 3 (incoherent — drifting cells toward p_A' did NOT fabricate a coherent
  peak from permuted labels; the coherence is EARNED by the real boundary, not the move).
- **c4 vs-PRIOR ✅**: (4a) re-pack peak-count 1.0 ≤ 2 < H_1340's 4.3 AND H_1352's 15.7 — coherent
  where BOTH prior levers scattered. (4b) re-pack |peak−p_A'| 0.002 ≤ 0.081 — closer than the best
  high-budget H_1340 rung, at EQUAL (H_1352) / LOWER (vs H_1340 high rungs) budget.

**FINDING.** The geometric re-pack RECOVERS a coherent full relocation that NEITHER budget (H_1340)
NOR decay (H_1352) could: at the SAME low budget, drifting the residual phase-1 prototype POSITIONS
toward p_A' lands a single CP peak (peak-count 1.0) essentially ON the moved cut (frac +1.01). This
**closes the budget/decay/geometry trilemma positively**: the relocation residual was a GEOMETRIC-
PLACEMENT problem all along — the old cells sitting at the old cut. Budget tried to out-count them
(distance↑ coherence↓), decay tried to out-vote them (distance↑↑ coherence↓↓), but the only fix
was to MOVE them. `a_break_the_wall` vindicated: the H_1340/H_1352 walls were the WRONG MECHANISM
(weight/count manipulations of a fixed geometry), not a true ceiling — change the geometry and the
wall dissolves. The SHUFFLE control confirms the move does not fabricate (pc 18.0), the NO-RETRAIN
control confirms it is the re-training not drift (held p_A). NO bar moved (c9/p7).

## Honest scope (a_scale_honest_scope / a_toy_scale_recheck)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED (same family as H_1333/H_1338/H_1340/H_1352
R1). TOY synthetic continuum N=81 / 3 seeds / single shift p_A→p_A' / one frozen REPACK_ETA=0.15
(ladder-robust); deterministic readout (tests the geometric-re-pack STRUCTURE, not a learned
drift). The re-pack re-reads each drifted cell's label from p_A' (a structural store update keyed
on birth-phase + position, NO injected target peak); the coherence is earned (shuffle collapses).
NO human-cognition claim. Real-corpus / multi-shift / leftward re-pack / a LEARNED (gradient)
drift vs this deterministic rule / engine-native §CategoricalPerception wiring (move-the-cells in
the live A⇄G immune store, `a_verified_must_wire`) = follow-on. Live CORE/*.hexa UNTOUCHED.

## Pointers

- code: `state/cp-geometric-repack/h1360_cp_geometric_repack.py` (imports `state/universe-probes/h1333_whorf_developmental.py` verbatim)
- freeze: `.verdicts/1360_cp_geometric_repack/FREEZE.txt` · result: `.verdicts/1360_cp_geometric_repack/result.txt`
- index: `UNIVERSE/HYPOTHESES.jsonl` (id H_1360) · claim: `CLAIMS.tape` @C h1360_cp_geometric_repack
- xref: H_1323 (parent Sapir-Whorf CP) · H_1333 (developmental plasticity 🟠) · H_1338 (eviction 🧱) · H_1340 (budget-sweep 🧱) · H_1341 (shift-ladder 📈) · H_1352 (soft-decay 🧱 parent — named this lever) · H_1355 (leftward geometry 📈) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · p7 · p8
