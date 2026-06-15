---
id: H_1333
slug: 1333_whorf_developmental
title: Whorfian categorical perception — developmentally PLASTIC or RIGID? Does the language-warped CP boundary RE-LOCATE when the substrate is re-trained on a shifted cut?
group: cognition-representation (c15 developmental / critical-period lens)
terminal_tier: 🟠 PARTIAL — GRADED PLASTICITY (peak relocated fraction +0.60; D1 strict FAIL by 0.008, D2✅ D3✅; NO bar moved, c9)
verdict_dir: .verdicts/1333_whorf_developmental/
freeze: .verdicts/1333_whorf_developmental/FREEZE.txt
terminal_verdict: .verdicts/1333_whorf_developmental/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1333 (1323 taken by parent Sapir-Whorf; 1324-1332 unused in COGNITION-REPRESENTATION; 1333 free on origin/main 61ce6948f)
---

# H_1333 — Whorfian CP: developmentally plastic or rigid?

## Claim / falsifier

H_1323/H_1325 (🟢 GREEN engine-native) showed a substrate develops categorical perception
(CP) AT its language's boundary — the Whorfian dissociation: the CP peak LOCATION tracks the
language cut (L_A→p_A, L_B→p_B, same stimulus world, different cognition by language).

**Falsifiable claim:** that learned CP boundary is DEVELOPMENTALLY PLASTIC — when the SAME
substrate is RE-trained on a SHIFTED boundary of the SAME language (cut moved p_A→p_A'), the
CP peak RE-LOCATES to the new cut, rather than rigidly staying where first learned. Lens: c15
developmental / critical-period plasticity, `a_no_llm_frame_trap` — NOT an LLM recipe, NOT a
human-cognition / critical-period claim, a TOY synthetic continuum. The honest alternatives
are equally valid (c9): RIGID (first-carving primacy — peak stuck at p_A), or GRADED (peak
moves part-way — report the fraction).

## Method

Reuses the H_1323/H_1325 CP machinery VERBATIM (`UNIVERSE/h1323_sapir_whorf.py`): RBF
position embedding, error-targeted SPLIT-only Voronoi/mitosis prototype growth (p8), soft
category-posterior discrimination readout (NO labels at test), and the H_1323→R2 COHERENCE
metric (peak-count at ≥0.5 of an arm's own peak). The ONE new mechanism = **phase-2
re-growth**: the SAME store is grown FURTHER on the MOVED labels WITHOUT reset (split-only ⇒
old cells persist ⇒ a RIGID outcome is a genuine possible result, never designed away).

- Continuum N=21 RBF-coded stimuli, DIM=16, identical stimulus world all arms.
- Initial language A cut p_A=1/3 (0.333); re-trained boundary p_A'=2/3 (0.667); SHIFT=0.333.
- GROW_MAX=24 / SPLIT_PASSES=24 PER PHASE (same fixed budget as H_1323; phase-2 re-growth gets
  a fair, non-inflated budget to relocate within).
- 4 arms: (1) A-trained · (2) A→A' re-trained (phase-1 on p_A, phase-2 grow further on p_A')
  · (3) NO-RETRAIN control (identical to 1, read at the same protocol point, no phase-2) ·
  (4) SHUFFLE (incoherent labels — EARNED control). 3 seeds [4333,4334,4335], $0 CPU, p7.
- p1/p2/p3/p6: readout reads ONLY representational distance in the learned prototype space; NO
  injected boundary location at test; labels enter ONLY during training. The no-retrain +
  shuffle arms are the anti-Goodhart discriminators.

## Frozen bars (pre-registered in FREEZE.txt; GREEN iff D1∧D2∧D3, NO bar moved c9/p7)

- **D1 PLASTIC** (all 3 seeds): (a) |CP_peak_retrained − p_A'| ≤ LOC_TOL=0.12 AND (b)
  |CP_peak_retrained − p_A| ≥ MIN_MOVE=0.20; AND A→A' stays coherent (peak-count ≤ 2).
- **D2 CONTROL**: no-retrain keeps peak at p_A (|peak−p_A| ≤ 0.12) AND A-trained reproduces
  H_1323 (|peak−p_A| ≤ 0.12), all 3 seeds.
- **D3 EARNED**: SHUFFLE incoherent (peak-count ≥ 3) AND language arms coherent (peak-count ≤ 2).

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 mirror (DIRECTIONAL) | 🟠 PARTIAL — GRADED PLASTICITY | peak 0.325→0.525 (fraction relocated **+0.60**); D1 FAIL by 0.008, D2✅ D3✅ |

**R1 result (mean of 3 seeds [4333,4334,4335], deterministic — identical every seed):**

- CP peak location: A-trained **0.325** (≈p_A=0.333) · A→A' re-trained **0.525** · no-retrain
  **0.325** · shuffle 0.542. Peak-count: A=1.0, A→A'=1.3, no-retrain=1.0, **shuffle=7.7**.
- **D1 PLASTIC ❌ (by a hair)**: (a) |0.525−p_A'|=**0.142** > LOC_TOL 0.12 (missed by 0.022);
  (b) |0.525−p_A|=**0.192** < MIN_MOVE 0.20 (missed by **0.008**); coherent peak-count 1.3 ≤ 2 ✅.
- **D2 CONTROL ✅**: no-retrain |peak−p_A|=0.008 (held at p_A — the move IS the re-training, not
  drift); A-trained |peak−p_A|=0.008 (reproduces H_1323).
- **D3 EARNED ✅**: shuffle peak-count 7.7 ≥ 3 (incoherent); language arms 1.0/1.3/1.0 ≤ 2 (coherent).

**FINDING:** the language-warped CP boundary is **GRADED-PLASTIC**, not rigid. After re-training
on a moved boundary the CP peak relocated **0.60 of the way** (0.325→0.525) toward p_A',
deterministically on all 3 seeds, while the no-retrain control held at p_A (isolating the move
to the re-training) and the shuffle control stayed incoherent. The peak did NOT clear BOTH
strict D1 sub-bars (it landed 0.142 short of p_A' and 0.192 off p_A, missing MIN_MOVE by 0.008),
so D1 is FAIL — but the substantive result is a SUBSTANTIAL relocation, NOT first-carving
rigidity. The mechanistic cause of the incomplete move (c9): split-only growth NEVER removes
the old-boundary cells, so the residual phase-1 packing at p_A pulls the peak back from a full
move; the store re-packs at p_A' (28 cells after phase-2 vs 4 after phase-1) but cannot erase
the old swing. Relevant to anima learning/relearning carvings: a re-carving substantially
re-locates the boundary but a never-evicting store leaves a residual pull from the first cut
(consistent with the H_1288 growth-memory / H_1330 overwrite-on-shared-store findings).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED (same family as H_1323 R1 / H_1290 /
H_1293 R1). TOY synthetic 1-D continuum, N=21, 3 seeds, single shift p_A→p_A', deterministic
readout (tests the STRUCTURE of plasticity, not a learned re-trainer). NO human-cognition /
critical-period claim. Live CORE/*.hexa UNTOUCHED (substrate-measurement rung — adds only
UNIVERSE/ + verdicts). NEXT (R2 candidates): (i) a graded SHIFT-SIZE curve (≥3 shifts) to map
the plasticity fraction vs shift magnitude; (ii) an EVICTION / decay variant of the store to
test whether removing stale old-boundary cells completes the move (would distinguish "graded
because never-evict" from "graded because budget"); (iii) engine-native realization on the live
CORE/engine_cli.hexa §CategoricalPerception lane (a_engine_native_learning · a_verified_must_wire).
Depletion test: each must clear a falsifiable, control-surviving bar frozen ANEW (no bar move).

## Pointers

- probe `UNIVERSE/h1333_whorf_developmental.py` (reuses `UNIVERSE/h1323_sapir_whorf.py` machinery)
- freeze `.verdicts/1333_whorf_developmental/FREEZE.txt` · verdict `.verdicts/1333_whorf_developmental/result.txt`
- index `UNIVERSE/HYPOTHESES.md` · claim `CLAIMS.tape @C h1333_whorf_developmental` · domain
  `domains/COGNITION-REPRESENTATION.log.md`
- xref: h1323 · h1325 (the GREEN result extended) · h1330 (bilingual overwrite, shared-store
  contradiction) · h1288 (growth-memory: store grows, never evicts — the mechanism behind the
  residual pull) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning ·
  a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
