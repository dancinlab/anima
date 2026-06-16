---
id: H_1338
slug: 1338_whorf_cp_eviction
title: Whorfian CP relocation residual — is the H_1333 partial move (~60%) the never-evict growth-memory, or a budget/geometry limit? Eviction-store test (the H_1333 load-bearing follow-on)
group: cognition-representation (c15 developmental plasticity + memory-protection-vs-overwrite lens)
terminal_tier: 🧱 RE-DIAGNOSIS — eviction does NOT complete the move (eviction frac +0.60 = never-evict frac +0.60; 28→3 cells evicted yet peak UNCHANGED 0.525) → the H_1333 residual pull is NOT never-evict, the limit is BUDGET/GEOMETRY. V1 FAIL, V2✅ V3✅; NO bar moved (c9)
verdict_dir: .verdicts/1338_whorf_cp_eviction/
freeze: .verdicts/1338_whorf_cp_eviction/FREEZE.txt
terminal_verdict: .verdicts/1338_whorf_cp_eviction/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1338 (1323=parent Sapir-Whorf; 1325 r2; 1330 bilingual; 1333 developmental-plasticity=this lane's parent; 1331-1337 taken/in-flight; 1338 free on origin/main 8a5ed2a17)
---

# H_1338 — Whorf CP residual: never-evict growth-memory, or budget/geometry?

## Claim / falsifier

H_1333 (🟠 GRADED PLASTICITY) found a Whorfian CP boundary RE-LOCATES ~60% toward a
re-trained boundary (peak 0.325→0.525, NOT fully to p_A'=0.667) when the SAME split-only
store is re-grown on a moved cut. The residual pull was DIAGNOSED — but only HYPOTHESIZED —
as the split-only store's NEVER-EVICTED first-boundary cells (28 cells after phase-2 vs 4
after phase-1; the phase-1 cells bound to label(p_A) keep voting at the old cut).

**Falsifiable claim:** that residual IS the never-evict growth-memory property — REMOVING /
decaying the stale old-boundary cells during re-training will COMPLETE the move (→ ~100%).
**Honest alternative (c9):** if the move STAYS partial even WITH eviction, the limit is
BUDGET / GEOMETRY, not never-evict. Lens: c15 developmental plasticity + memory-protection-
vs-overwrite, `a_no_llm_frame_trap` — NOT an LLM recipe, NOT a human-cognition claim, a TOY
synthetic continuum. The decisive design: never-evict and eviction differ ONLY in whether
stale-conflicting cells are removed (same run, same seeds), isolating any completion as the
eviction (V2).

## Method

Reuses the H_1333 / H_1323 / H_1325 CP machinery EXACTLY
(`UNIVERSE/h1333_whorf_developmental.py`): RBF position embedding, error-targeted SPLIT-only
nearest-prototype (Voronoi/mitosis) growth (p8), soft category-posterior discrimination
readout (NO labels at test), peak-COUNT coherence metric. ALL constants inherited VERBATIM
(N=21, DIM=16, p_A=1/3, p_A'=2/3, GROW_MAX=24/SPLIT_PASSES=24 per phase, LOC_TOL=0.12).

**The ONE new mechanism = an EVICTION/DECAY store.** During the phase-2 (A→A') re-growth,
BEFORE each error-targeted split, `VoronoiCells.fit(...,evict=True)` removes every existing
prototype whose BOUND label conflicts with the re-trained (p_A') label of the stimulus it
currently OWNS (a *stale-conflicting* cell — a cell that still says "0" but now owns a
stimulus the moved boundary labels "1"). The last surviving cell is never removed. Phase-1
and the A-trained / no-retrain / shuffle arms are UNCHANGED (`evict=False` == H_1333 split-
only EXACTLY) — eviction fires ONLY in the eviction arm's phase-2.

- Arms (per seed): (1) **NEVER-EVICT** (= H_1333 verbatim, split-only A→A') · (2) **EVICTION-
  STORE** (phase-1 identical, phase-2 grows on p_A' WITH eviction) · (3) **NO-RETRAIN** control
  (both stores: grow on p_A only, no phase-2 → must stay at p_A) · (4) **SHUFFLE** (incoherent
  labels — EARNED control). 3 seeds [4333,4334,4335] (SAME as H_1333 so never-evict reproduces
  the anchor in-run), $0 CPU, p7.
- **move-fraction** = (peak_retrained − peak_Atrained) / (p_A' − p_A), reported per arm/seed.
- p1/p2/p3/p6: readout reads ONLY representational distance; NO injected boundary location at
  test; eviction keys on a cell's OWN bound label vs the re-trained label of the stimulus it
  owns (NO injected target peak / persona / RLHF); labels enter ONLY during training.

## Frozen bars (pre-registered in FREEZE.txt; GREEN iff V1∧V2∧V3, NO bar moved c9/p7)

- **V1 COMPLETES** (all 3 seeds): (a) |CP_peak_eviction − p_A'| ≤ LOC_TOL=0.12 AND (b) eviction
  move-fraction ≥ 0.85; AND eviction A→A' coherent (peak-count ≤ 2).
- **V2 CONTRAST** (all 3 seeds): never-evict move-fraction ∈ [0.40, 0.75] (reproduces H_1333
  ~0.60 in-run) AND never-evict did NOT complete (|peak − p_A'| > 0.12).
- **V3 EARNED**: no-retrain (BOTH stores) holds p_A (|peak − p_A| ≤ 0.12, all seeds) AND
  SHUFFLE incoherent (peak-count ≥ 3).

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 mirror (DIRECTIONAL) | 🧱 RE-DIAGNOSIS — budget/geometry, NOT never-evict | eviction frac **+0.60** = never-evict frac **+0.60** (peak both 0.525); eviction evicted 28→**3 cells** yet peak UNCHANGED; V1 ❌, V2 ✅, V3 ✅ |

**R1 result (mean of 3 seeds [4333,4334,4335], deterministic — identical every seed):**

- CP peak: A-trained **0.325** · NEVER-EVICT A→A' **0.525** (frac **+0.60**, reproduces H_1333)
  · EVICTION A→A' **0.525** (frac **+0.60** — IDENTICAL) · no-retrain (NE & EV) 0.325 · shuffle
  0.542. Peak-count: A=1.0, never-evict=1.3, eviction=2.0, no-retrain=1.0, **shuffle=7.7**.
- **cell budget (seed, p1, never-evict-p2, eviction-p2)**: (4333,4,**28**,**3**) (4334,4,28,3)
  (4335,4,28,3) — the eviction store DID fire hard (28→**3 cells**, removing the stale phase-1
  packing), yet the CP peak landed at the EXACT same 0.525.
- **V1 COMPLETES ❌**: |0.525−p_A'|=**0.142** > 0.12 (reaches-new FAIL); eviction frac **0.60**
  < 0.85 (full-move FAIL); coherent peak-count 2.0 ≤ 2 ✅.
- **V2 CONTRAST ✅**: never-evict frac **0.60** ∈ [0.40,0.75] (reproduces H_1333 in-run);
  |0.525−p_A'|=0.142 > 0.12 (did NOT complete).
- **V3 EARNED ✅**: no-retrain (both) |peak−p_A|=0.008 (held at p_A — move is the re-training,
  not eviction-drift); shuffle peak-count 7.7 ≥ 3 (incoherent).

**FINDING (the load-bearing answer):** the H_1333 residual pull is **NOT** the never-evict
growth-memory property — it is a **BUDGET / GEOMETRY** limit. Removing the stale old-boundary
cells does NOT complete the move: the eviction store dropped from 28 → **3 cells** (the stale
phase-1 packing was real and was genuinely removed) yet the CP peak stayed at the **EXACT
same 0.525, frac +0.60** as the never-evict store in the SAME run. V2 confirms the never-evict
arm reproduced the H_1333 ~0.60 in-run (so the comparison is not a confound), and V3's controls
held. The 3 surviving p_A'-aligned cells define a boundary that geometrically sits at ~0.525,
not 0.667 — under this RBF geometry + fixed per-phase split budget, the discrimination peak
cannot be packed all the way to p_A' regardless of whether stale cells linger. **So the dual
intuition (never-evict ⇒ partial; evict ⇒ full, dual to H_1288) is FALSIFIED for this store:
the partial move is set by where the available cells can geometrically place the boundary,
not by old cells voting it back.** This is an honest, important re-diagnosis of H_1333's
residual — and a non-obvious one, since the stale cells exist and were removed but were not
the cause. (Relevant to anima re-learning carvings: a never-evicting store is NOT what limits
re-carving here; the limit is representational/budget resolution at the new cut.)

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED (same family as H_1333 R1 / H_1323 R1 /
H_1290 / H_1293 R1). TOY synthetic 1-D continuum, N=21, 3 seeds, single shift p_A→p_A',
deterministic readout, HARD eviction (remove) — soft decay UNTESTED. Live CORE/*.hexa
UNTOUCHED (substrate-measurement rung — adds only UNIVERSE/ + verdicts). NO human-cognition /
critical-period claim. NEXT (R2 candidates, each frozen ANEW — no bar move): (i) a **budget /
RBF-resolution sweep** at the new cut — if raising the per-phase split budget OR RBF grid
density lets the eviction (or never-evict) peak reach p_A', that confirms budget/geometry as
the mechanism and maps the resolution ceiling; (ii) a **graded shift-size curve** (≥3 shifts)
to see whether the partial-move fraction tracks shift magnitude (geometry) vs is constant
(memory); (iii) **soft DECAY** (down-weight stale cells rather than hard-remove) as a gentler
store policy; (iv) engine-native realization on the live CORE/engine_cli.hexa immune/Voronoi
lane (a_engine_native_learning · a_verified_must_wire). Depletion test: each must clear a
falsifiable, control-surviving bar frozen ANEW.

## Pointers

- probe `UNIVERSE/h1338_whorf_cp_eviction.py` (reuses `UNIVERSE/h1333_whorf_developmental.py`
  / `h1323_sapir_whorf.py` machinery VERBATIM; adds only the eviction option to fit())
- freeze `.verdicts/1338_whorf_cp_eviction/FREEZE.txt` · verdict `.verdicts/1338_whorf_cp_eviction/result.txt`
- index `UNIVERSE/HYPOTHESES.md` · claim `CLAIMS.tape @C h1338_whorf_cp_eviction` · domain
  `domains/COGNITION-REPRESENTATION.log.md`
- xref: h1333 (the GRADED-PLASTICITY result whose residual this re-diagnoses) · h1323 · h1325
  (the GREEN CP result the family extends) · h1288 (growth-memory: store grows, never evicts —
  the DUAL intuition this lane tested and FALSIFIED as the cause of the partial move) · h1330
  (bilingual overwrite, shared-store contradiction) · a_no_llm_frame_trap · a_break_the_wall ·
  a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck ·
  p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
