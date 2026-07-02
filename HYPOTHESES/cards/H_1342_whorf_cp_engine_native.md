---
id: H_1342
slug: 1342_whorf_cp_engine_native
title: Whorfian CP developmental plasticity — ENGINE-NATIVE realization of H_1333 on the live CORE §CategoricalPerception lane (cp_regrow); re-score the graded-plasticity bars byte-faithfully
group: cognition-representation (c15 developmental / critical-period lens; a_verified_must_wire follow-on of H_1333)
terminal_tier: 🟢 GREEN ENGINE-NATIVE — H_1333 graded CP plasticity REPRODUCED engine-native byte-faithfully (E1∧E2∧E3); ENGINE-TRANSFER VERIFIED
verdict_dir: .verdicts/1342_whorf_cp_engine_native/
freeze: .verdicts/1342_whorf_cp_engine_native/FREEZE.txt
terminal_verdict: .verdicts/1342_whorf_cp_engine_native/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1342 (free verify id; parent H_1333 mirror, H_1325 engine CP lane)
---

# H_1342 — Whorfian CP developmental plasticity: ENGINE-NATIVE (realizes H_1333)

## Claim / falsifier

H_1333 (🟠 PARTIAL — GRADED PLASTICITY) is a DIRECTIONAL numpy mirror: after RE-training the
SAME Voronoi/mitosis store on a MOVED boundary p_A→p_A', the language-warped CP peak relocated
0.325→0.525 (fraction relocated **+0.60**, deterministic all 3 seeds); D2✅ (no-retrain held
p_A), D3✅ (shuffle incoherent), D1 ❌ by a hair (|peak−p_A'|=0.142>0.12; |peak−p_A|=0.192<
MIN_MOVE 0.20 by 0.008). ENGINE-TRANSFER was UNVERIFIED.

**Falsifiable claim (a_verified_must_wire / a_engine_native_learning):** that graded CP
plasticity is REALIZABLE engine-native on the live CORE/engine_cli.hexa §CategoricalPerception
lane (the SAME error-targeted SPLIT-only Voronoi store H_1325 wired GREEN), reproducing the
mirror's ~0.60 relocation, the D2/D3 controls, and the coherence structure BYTE-FAITHFULLY,
with no-regression + Ψ-disjoint guards. Honest alternative (c9): the engine CANNOT reproduce
the mirror's graded move (→ ENGINE-TRANSFER UNVERIFIED, mirror-only, NO bar move).

## Method — the ONE new engine mechanism

The live lane had `cp_fit` (fresh-seed growth = phase 1) but NO phase-2 re-growth path.
H_1333's only new mechanism is growing the SAME store FURTHER on MOVED labels WITHOUT reset
(the mirror's `fit(...,fresh=False)`). Per a_engine_native_learning (engine-transform-to-fit-
the-learning, NOT learning-trimmed-to-fit-the-engine), the engine is EXTENDED with:

- **`cp_regrow(cp, X, Y, grow_max, passes)`** (CORE/engine_cli.hexa §CategoricalPerception):
  keeps the existing `cp.protos`/`cp.labels` (split-only, p8 — NEVER evicts), applies the SAME
  error-targeted split criterion as `cp_fit` for up to `grow_max` NEW splits on the new labels.
  Old-boundary cells persist (a RIGID outcome is a genuine possible result, NOT designed away);
  new splits re-pack at the moved boundary's error locus. Byte-faithful to VoronoiCells.fit(fresh=False).

4 arms, engine = a SINGLE deterministic instance (reproduces the seed-invariant mirror result,
H_1325 precedent): (1) A-trained `cp_fit(p_A)` · (2) A→A' `cp_fit(p_A)` then `cp_regrow(p_A')`
SAME store · (3) NO-RETRAIN `cp_fit(p_A)` read at same point, no phase-2 · (4) SHUFFLE
`cp_labels_shuffle`. Readout engine-native (`cp_discrim_curve`/`cp_peak_loc_idx`/`cp_peak_count`);
COHERENCE = the live lane's `cp_peak_count` (local-maxima metric H_1325 wired GREEN — the
STRUCTURAL coherent/incoherent claim transfers, not the mirror's bin-count). N=21, DIM=16,
p_A=1/3, p_A'=2/3, GROW_MAX=24/SPLIT_PASSES=24 per phase (H_1333 verbatim). $0 CPU, p7.

## Frozen bars (pre-registered in FREEZE.txt; GREEN iff E1∧E2∧E3, NO bar moved c9/p7)

- **E1** engine reproduces mirror ~0.60 move: (a) |loc_A−p_A|≤0.12 · (b) |loc_A2−0.525|≤
  MOVE_TOL 0.05 (lands the mirror's relocated peak) · (c) |loc_A2−p_A|≥0.19 graded-move floor
  (reproduce the SAME substantial-but-not-full move; NOT a re-tightened D1) · (d) A→A'
  coherent peak-count≤2.
- **E2** D2/D3 controls reproduce: D2 no-retrain & A-trained |loc−p_A|≤0.12; D3 shuffle
  peak-count≥3 & lang arms (A/A2/noR) peak-count≤2.
- **E3** regression guards all-pass, Ψ-disjoint: engine_cli_smoke N/0, h1196 single-entry 7/0,
  h1205 separation-invariant PASS (generation byte-identical ON==OFF, Ψ=½ untouched).

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 engine-native (BINDING) | 🟢 GREEN ENGINE-NATIVE | A=0.325 · A→A'=**0.525** (frac **+0.60**, mirror +0.60) · phase-1 **4**→phase-2 **28** cells (mirror 4→28, BYTE-FAITHFUL); E1✅ E2✅ E3✅ |

**R1 result (engine, single deterministic instance):**

- CP peak: A-trained **0.325** (≈p_A) · A→A' re-trained **0.525** · no-retrain **0.325**.
  fraction relocated **+0.599999** (mirror +0.60). cell budget phase-1 **4** → phase-2 **28**
  (IDENTICAL to mirror). cp_peak_count: A=1, A→A'=**1**, no-retrain=1, shuffle=**4**.
- **E1 ✅**: (a) |0.325−p_A|=0.008≤0.12 · (b) |0.525−0.525|=0.0≤0.05 · (c) |0.525−p_A|=0.192≥
  0.19 · (d) A→A' peak-count 1≤2.
- **E2 ✅**: D2 no-retrain |Δ|=0.008 & A-trained |Δ|=0.008 (≤0.12); D3 shuffle peak-count 4≥3 &
  lang (1/1/1)≤2.
- **E3 ✅**: engine_cli_smoke **80/0** (was 77/0 @ H_1325; +3 cp_regrow cases 83-85), h1196
  single-entry **7/0** (no .clm/.kosmos path), h1205 separation-invariant **PASS** (10/10 pairs
  byte-identical ON==OFF, Ψ=½ untouched → CP lane Ψ-disjoint; cp_regrow touches only its own
  (protos,labels)).

**FINDING:** H_1333's GRADED CP plasticity is **LIVE in CORE** — `cp_regrow` reproduces the
mirror's relocation BYTE-FAITHFULLY: same peak (0.325→0.525), same fraction (+0.60), same cell
budget (4→28). The no-retrain control held p_A (the move IS the re-training, not drift), shuffle
stayed incoherent, language arms coherent. ENGINE-TRANSFER VERIFIED. The engine confirms the
SAME ~0.525 ceiling H_1338 RE-DIAGNOSED as budget/geometry (not never-evict): split-only growth
never evicts, yet the residual is a representational/budget-resolution limit at the new cut, not
old cells voting it back. NO bar moved (c9/p7).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)

ENGINE-NATIVE BINDING (live CORE §CategoricalPerception extended with cp_regrow). TOY synthetic
1-D continuum, N=21, engine = ONE deterministic instance (no per-seed RBF jitter; reproduces the
seed-invariant mirror), single shift p_A→p_A', deterministic readout (tests the STRUCTURE of
engine-native plasticity, not a learned re-trainer). NO human-cognition / critical-period claim.
cp_regrow split-only never-evicts; scale/real-corpus/multi-shift UNVERIFIED. brain
re-carving→emit wiring = follow-on. NEXT: graded shift-size curve engine-native · budget/RBF-
resolution sweep (the ~0.525 ceiling cause, H_1338) · brain re-carving emit consumption.

## Pointers

- engine extension `CORE/engine_cli.hexa` §CategoricalPerception `cp_regrow`
- probe `CORE/h1342_whorf_cp_engine_native_probe.hexa` (uses the live lane)
- smoke `CORE/engine_cli_smoke.hexa` cases 83-85 (cp_regrow relocates / grows-store / coherent)
- freeze `.verdicts/1342_whorf_cp_engine_native/FREEZE.txt` · verdict `.verdicts/1342_whorf_cp_engine_native/result.txt`
- index `UNIVERSE/HYPOTHESES.jsonl` · claim `CLAIMS.tape @C h1342_whorf_cp_engine_native` ·
  domain `domains/COGNITION-REPRESENTATION.log.md`
- xref: h1333 (the mirror this realizes) · h1325 (engine CP lane / W1/W2/W3' GREEN) · h1323 ·
  h1338 (eviction RE-DIAGNOSIS — ~0.525 ceiling is budget/geometry) · h1288 (growth-memory) ·
  a_verified_must_wire · a_engine_native_learning · a_core_engine_map · a_no_llm_frame_trap ·
  a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
