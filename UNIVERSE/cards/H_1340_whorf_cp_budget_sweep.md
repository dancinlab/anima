---
id: H_1340
slug: 1340_whorf_cp_budget_sweep
title: Whorfian CP relocation ceiling — does raising the phase-2 split budget + RBF grid density let the re-located CP peak REACH the moved cut p_A'? Budget/geometry sweep (the H_1338 re-diagnosis follow-on)
group: cognition-representation (c15 developmental plasticity + representational-resolution lens, a_no_llm_frame_trap, a_break_the_wall)
terminal_tier: 🧱 DEEPER LIMIT — budget/geometry is INCOMPLETE. Raising phase-2 budget+RBF density moves the peak DISTANCE monotonically toward p_A' (frac +0.575→+0.762, |peak-p_A'| 0.144→0.081) BUT the discrimination COHERENCE collapses (peak-count 4.3→7.0, never ≤2) so NO rung delivers a coherent single CP peak AT p_A'. B1 ❌ (coherence gate), B2 ✅ monotone, B3 ✅ reproduces H_1338. NO bar moved (c9)
verdict_dir: .verdicts/1340_whorf_cp_budget_sweep/
freeze: .verdicts/1340_whorf_cp_budget_sweep/FREEZE.txt
terminal_verdict: .verdicts/1340_whorf_cp_budget_sweep/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1340 (1323=parent Sapir-Whorf; 1333=developmental-plasticity grandparent; 1338=eviction RE-DIAGNOSIS parent; 1341=shift-size ladder sibling; 1340 free on origin/main 3176fadc0)
---

# H_1340 — Whorf CP relocation ceiling: budget / RBF-density sweep

## Claim / falsifier

H_1338 (🧱 RE-DIAGNOSIS) found that EVICTING the stale phase-1 cells did NOT complete the
H_1333 partial CP relocation (peak stayed 0.525, frac +0.60 even with cells 28→3) and
**DIAGNOSED — but only HYPOTHESIZED** — the residual pull as **BUDGET / GEOMETRY** (RBF
resolution + a fixed per-phase split budget), NOT a never-evict growth-memory.

**Falsifiable claim:** if raising the phase-2 (re-training) split budget AND the RBF grid
density at the moved boundary lets the relocated CP peak REACH p_A' (cross into a coherent
single peak with |peak−p_A'| ≤ LOC_TOL), the residual IS budget/geometry and the resolution
ceiling is MAPPED (`a_break_the_wall`). **Honest alternative (c9):** if the peak stays short
regardless of budget/density, the budget/geometry diagnosis is itself INCOMPLETE — a deeper
limit. Lens: c15 developmental plasticity + representational-RESOLUTION, `a_no_llm_frame_trap`
— NOT an LLM recipe, NOT a human-cognition claim, a TOY synthetic continuum.

## Method

Reuses the H_1333 / H_1338 CP machinery EXACTLY (`UNIVERSE/h1333_whorf_developmental.py`,
IMPORTED verbatim): RBF position embedding, error-targeted SPLIT-only Voronoi/mitosis growth
(p8), soft category-posterior discrimination readout (NO labels at test), peak-COUNT coherence
metric. A **LADDER of joint (RBF-density DIM, phase-2 split budget GROW2) rungs** applied ONLY
to the phase-2 (A→A') re-growth; phase-1 (the p_A carving) is FIXED at the H_1333/H_1338
baseline budget (24) on EVERY rung, so the never-evicted phase-1 packing (the H_1338 residual)
is IDENTICAL across rungs — the ONLY thing that changes per rung is how much budget/density the
RE-TRAINING gets. N_STIM FIXED at 81 (finer than H_1338's 21; constant = not a confound). NO
eviction (split-only never-evict store), since H_1338 already showed eviction is not the lever.

- Rungs (≥3, `a_scale_honest_scope`): R0_base (DIM16/GROW2 24 = H_1338 baseline) · R1 (32/96) ·
  R2 (48/192) · R3 (64/384) · R4_high (96/768). 3 seeds [4333,4334,4335] (SAME as H_1338 so R0
  reproduces the anchor in-run), $0 CPU, p7. move-fraction = (peak_relocated − peak_Atrained) /
  (p_A' − p_A), per rung/seed.
- p1/p2/p3/p6: readout reads ONLY representational distance; NO injected boundary location at
  test; DIM/GROW2 are STRUCTURAL store-capacity knobs (NO injected target peak / persona / RLHF).
  The R0 baseline + monotonicity bars are the anti-Goodhart legs.

## Frozen bars (pre-registered in FREEZE.txt; GREEN iff B1∧B2∧B3, NO bar moved c9/p7)

- **B1 RELOCATES**: at SOME rung (lowest = mapped ceiling), all 3 seeds reach p_A'
  (|peak−p_A'| ≤ LOC_TOL=0.12) AND that rung stays COHERENT (mean peak-count ≤ 2).
- **B2 EARNED-MONOTONE**: mean move-fraction non-decreasing R0→R4 (slack 0.01) AND total span
  (frac@R4 − frac@R0) ≥ TRACK_TOL=0.10.
- **B3 BASELINE-REPRO**: R0 reproduces the H_1338 partial — frac ∈ [0.40,0.75] AND
  |peak−p_A'| > 0.12, all 3 seeds.

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 mirror (DIRECTIONAL) | 🧱 DEEPER LIMIT — budget/geometry INCOMPLETE | peak-DISTANCE crosses LOC_TOL at R2+ (|peak-p_A'| 0.144→0.081, frac +0.575→+0.762, monotone) BUT COHERENCE collapses (peak-count 4.3→7.0, never ≤2) ⇒ no coherent single peak AT p_A'. B1 ❌, B2 ✅, B3 ✅ |

**R1 result (mean of 3 seeds [4333,4334,4335], deterministic):**

| rung | DIM | GROW2 | peak | \|peak−p_A'\| | frac | peak-count | dist≤0.12 all-seed |
|---|---|---|---|---|---|---|---|
| R0_base | 16 | 24 | 0.523 | 0.144 | +0.575 | 4.3 | False |
| R1 | 32 | 96 | 0.548 | 0.119 | +0.650 | 5.0 | False |
| R2 | 48 | 192 | 0.560 | 0.106 | +0.688 | 5.0 | **True** |
| R3 | 64 | 384 | 0.573 | 0.094 | +0.725 | 5.7 | **True** |
| R4_high | 96 | 768 | 0.585 | 0.081 | +0.762 | 7.0 | **True** |

- **B1 RELOCATES ❌**: although the peak-DISTANCE crosses LOC_TOL on all 3 seeds from R2
  onward (|peak−p_A'| ≤ 0.12), the COHERENCE gate is NEVER met — peak-count is 4.3 at R0 and
  RISES with budget to 7.0 at R4_high (all ≫ 2). So no rung delivers a *coherent single* CP
  peak AT p_A'; the high-budget store packs many cells and produces a SCATTERED multi-peak
  discrimination profile, not a clean relocated CP. (peak-count is inflated vs H_1338 partly
  because N_STIM=81 gives more midpoints, but it is scored against the SAME frozen COH_MAX_LANG=2.)
- **B2 EARNED-MONOTONE ✅**: frac climbs monotonically +0.575→+0.650→+0.688→+0.725→+0.762,
  span +0.187 ≥ 0.10 — the peak-distance move IS budget-driven, not a fluke.
- **B3 BASELINE-REPRO ✅**: R0 per-seed frac [0.562, 0.60, 0.562] ∈ [0.40,0.75] and
  |peak−p_A'| [0.148,0.135,0.148] > 0.12 — reproduces the H_1338 partial in-run.

**FINDING (the load-bearing answer):** the H_1338 budget/geometry diagnosis is **PARTIAL but
INCOMPLETE**. Raising the phase-2 split budget + RBF grid density DOES nudge the relocated peak
DISTANCE monotonically toward p_A' (frac +0.575→+0.762; |peak−p_A'| 0.144→0.081, crossing the
LOC_TOL distance threshold from R2 up) — so resolution/budget IS one real lever, confirming part
of H_1338. BUT it FAILS to produce a coherent single CP peak AT p_A': as budget grows the
discrimination curve becomes MORE scattered (peak-count 4.3→7.0), so the frozen coherence gate
is never cleared and B1 fails. **The relocation ceiling is therefore NOT a pure resolution
limit that more budget removes — pouring in budget/density buys distance but destroys coherence,
leaving the residual never-evicted phase-1 packing co-present with the new packing as a
persistent secondary peak.** This is an honest re-re-diagnosis: budget/geometry is a real but
INSUFFICIENT lever; a clean full relocation needs a different mechanism (e.g. soft DECAY /
down-weighting of the residual packing, or a coherence-preserving re-pack) than simply raising
resolution. Sibling H_1341 (shift-size ladder) independently found the partial FRACTION tracks
shift magnitude (geometry-driven) — H_1340 adds that even at high resolution the move stays
incoherent, so neither pure-budget nor pure-shift-geometry fully closes it.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED (same family as H_1333 R1 / H_1338 R1 /
H_1323 R1). TOY synthetic 1-D continuum, N_STIM=81, 3 seeds, single shift p_A→p_A',
deterministic readout (tests the STRUCTURE of the resolution ceiling, not a learned re-trainer).
Live CORE/*.hexa UNTOUCHED (substrate-measurement rung — adds only UNIVERSE/ + verdicts). The
peak-count coherence threshold (frozen COH_MAX_LANG=2) is N_STIM-sensitive (more midpoints → more
candidate peaks); B1 reads it verbatim and honestly. NO human-cognition / critical-period claim.
NEXT (R2 candidates, each frozen ANEW — no bar move): (i) **soft DECAY** store (down-weight the
residual phase-1 packing during re-training, rather than relying on raw budget) — the H_1338
follow-on (iii) re-pointed by THIS deeper-limit result as the most promising lever to recover a
COHERENT relocation; (ii) a **coherence-aware re-pack** (prune the residual secondary peak); (iii)
engine-native realization on the live CORE/engine_cli.hexa immune/Voronoi lane
(a_engine_native_learning · a_verified_must_wire). Depletion test: each must clear a falsifiable,
control-surviving bar frozen ANEW.

## Pointers

- probe `UNIVERSE/h1340_whorf_cp_budget_sweep.py` (IMPORTS `UNIVERSE/h1333_whorf_developmental.py`
  machinery VERBATIM; adds only the joint (DIM,GROW2) phase-2 sweep ladder)
- freeze `.verdicts/1340_whorf_cp_budget_sweep/FREEZE.txt` · verdict
  `.verdicts/1340_whorf_cp_budget_sweep/result.txt`
- index `UNIVERSE/HYPOTHESES.jsonl` · claim `CLAIMS.tape @C h1340_whorf_cp_budget_sweep` · domain
  `domains/COGNITION-REPRESENTATION.log.md`
- xref: h1338 (the eviction RE-DIAGNOSIS whose budget/geometry hypothesis this tests and finds
  INCOMPLETE) · h1333 (the GRADED-PLASTICITY result this lane characterizes) · h1341 (sibling
  shift-size ladder, geometry-driven fraction) · h1323 · h1325 (the GREEN CP result the family
  extends) · h1288 (growth-memory: store grows, never evicts) · a_no_llm_frame_trap ·
  a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope ·
  a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
