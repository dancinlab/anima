---
id: H_1352
slug: 1352_cp_soft_decay
title: Whorfian CP relocation — does a SOFT-DECAY re-pack (down-weight the residual phase-1 cells during A→A' retrain, NOT raise budget) recover a COHERENT full relocation where the H_1340 budget-sweep could not? (the H_1340 DEEPER-LIMIT follow-on R2)
group: cognition-representation (c15 developmental-plasticity + memory-protection-vs-overwrite lens, a_no_llm_frame_trap, a_break_the_wall)
terminal_tier: 🧱 DEEPER LIMIT — relocation COHERENCE survives BOTH levers. Soft-decay (γ=0.80, FIXED LOW budget) relocates the peak BETTER than budget (|peak−p_A'| 0.144→0.044, frac +0.57→+0.88, all 3 seeds ≤LOC_TOL) BUT coherence collapses even HARDER (peak-count 4.3→15.7, vs H_1340's 4.3→7.0) → c1 ✅ c3 ✅ but c2 ❌ c4 ❌(4a✅/4b❌). A clean single CP peak AT p_A' is NOT recovered by decay any more than by budget; the residual is a re-pack/coherence ceiling deeper than either. NO bar moved (c9)
verdict_dir: .verdicts/1352_cp_soft_decay/
freeze: .verdicts/1352_cp_soft_decay/FREEZE.txt
terminal_verdict: .verdicts/1352_cp_soft_decay/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1352 (1323=parent Sapir-Whorf; 1333=developmental-plasticity grandparent; 1338=eviction re-diagnosis; 1340=budget-sweep DEEPER-LIMIT parent; 1341=shift-ladder sibling; 1342=engine-native; 1352 free on origin/main)
---

# H_1352 — Whorf CP relocation: soft-decay re-pack (coherence-preserving?)

## Claim / falsifier

H_1340 (🧱 DEEPER LIMIT) showed that raising the phase-2 split budget + RBF density buys
peak-DISTANCE toward the moved cut p_A' MONOTONICALLY (frac +0.575→+0.762, |peak−p_A'|
0.144→0.081) but DESTROYS discrimination COHERENCE (peak-count 4.3→7.0, never ≤2): **pure
budget cannot deliver a COHERENT full relocation.** H_1340's own verdict named the next
mechanism — "a clean full relocation needs a DIFFERENT mechanism (soft DECAY /
coherence-preserving re-pack), not more resolution."

**Falsifiable claim:** at a FIXED LOW budget (= H_1340 R0_base, DIM=16/GROW2=24, NO budget
inflation), DOWN-WEIGHTING the residual phase-1 prototypes during A→A' re-training (a
soft-decay store, vote weight d_i = γ^(#phase-2 splits after the cell) for phase-1 cells, 1.0
for phase-2 cells) recovers a COHERENT full relocation: the CP peak lands AT p_A' AND peak-count
returns to ~1. **Honest alternative (c9):** if decay does not deliver coherence, relocation may
be intrinsically a coherence/re-pack ceiling deeper than either budget or decay. Lens: c15
developmental plasticity + memory-protection-vs-overwrite, `a_no_llm_frame_trap` /
`a_break_the_wall` — NOT an LLM recipe, NOT a human-cognition claim, a TOY synthetic continuum.

## Method

Reuses the H_1333/H_1338/H_1340 CP machinery EXACTLY (`state/universe-probes/h1333_whorf_developmental.py`,
IMPORTED verbatim): RBF position embedding, error-targeted SPLIT-only Voronoi/mitosis growth
(p8), soft category-posterior discrimination readout (NO labels at test), peak-COUNT coherence
metric. The ONE new mechanism = a **`SoftDecayCells`** subclass: a per-cell decay weight d_i
multiplies into the softmin posterior vote (`P = Σ w_i d_i lab_i / Σ w_i d_i`). Phase-1 cells
decay by γ per subsequent phase-2 split; phase-2 cells stay 1.0; with γ=1.0 the posterior is
**byte-identical** to H_1333/H_1340 (so the NO-DECAY arm reproduces the H_1340 R0_base anchor
IN-RUN). Budget held at H_1340 R0_base LOW (DIM=16/GROW2=24) — the ONLY change is decay.

- Arms (per seed, SAME low budget): (1) **NO-DECAY** (γ=1.0 = H_1340 R0_base anchor) ·
  (2) **SOFT-DECAY** (γ=0.80, FROZEN) · (3) **NO-RETRAIN** control (p_A only, no phase-2/decay →
  must hold p_A) · (4) **SHUFFLE+decay** (permuted phase-2 labels → must collapse). 3 seeds
  [4333,4334,4335] (SAME as H_1333/H_1338/H_1340), $0 CPU, p7. A NON-GATING **decay-ladder**
  {0.70,0.80,0.90} is reported as a knife-edge diagnostic; the GATE is scored ONLY at γ=0.80.
- p1/p2/p3/p6: readout reads ONLY representational distance × structural decay weight; NO
  injected boundary location at test; decay keys on a cell's BIRTH PHASE only (NO injected
  target peak / persona / RLHF); labels enter ONLY during training. NO-RETRAIN + SHUFFLE = the
  anti-Goodhart discriminators; NO-DECAY (must stay partial in-run) isolates decay as the lever.

## Frozen bars (pre-registered in FREEZE.txt; GREEN iff c1∧c2∧c3∧c4, NO bar moved c9/p7)

- **c1 RELOCATES**: soft-decay |peak−p_A'| ≤ LOC_TOL=0.12 on all 3 seeds.
- **c2 COHERENT** (load-bearing): soft-decay mean peak-count ≤ 2 (the gate H_1340 NEVER met).
- **c3 EARNED**: (3a) no-retrain holds p_A (|peak−p_A|≤0.12) AND (3b) shuffle collapses (mean
  peak-count ≥ 3).
- **c4 vs-BUDGET**: (4a) soft-decay |peak−p_A'| ≤ 0.081 (best H_1340 rung) AND (4b) peak-count
  ≤ 2 < every H_1340 rung (≥4.3) — beats budget on BOTH axes.

## Verdict (per round)

| round | tier | key numbers |
|---|---|---|
| R1 mirror (DIRECTIONAL) | 🧱 DEEPER LIMIT — relocation coherence survives BOTH levers | soft-decay RELOCATES better than budget (|peak−p_A'| 0.144→**0.044**, frac +0.57→**+0.88**, all 3 seeds ≤0.12) BUT coherence collapses HARDER (peak-count 4.3→**15.7** vs H_1340 4.3→7.0). c1 ✅ c2 ❌ c3 ✅ c4 ❌ (4a✅ 4b❌) |

**R1 result (mean of 3 seeds [4333,4334,4335], deterministic):**

| arm | peak | \|peak−p_A'\| | frac | peak-count |
|---|---|---|---|---|
| NO-DECAY (γ=1.0, anchor) | 0.523 | 0.144 | +0.57 | 4.3 |
| **SOFT-DECAY (γ=0.80)** | **0.623** | **0.044** | **+0.88** | **15.7** |
| NO-RETRAIN (control) | 0.331 | — (\|peak−p_A\|=0.002) | — | — |
| SHUFFLE+decay (control) | — | — | — | 7.0 |

Decay-ladder (NON-GATING): γ=0.70 → |peak−p_A'|=0.009 / pc 16.7 · γ=0.80 → 0.044 / 15.7 (gate)
· γ=0.90 → 0.106 / 5.7. Monotone tradeoff: more decay = closer peak but MORE scatter.

- **c1 RELOCATES ✅**: per-seed |peak−p_A'| = [0.048, 0.035, 0.048], all ≤ 0.12. Decay
  relocates the peak FURTHER than budget ever did (frac +0.88 > H_1340's best +0.762).
- **c2 COHERENT ❌** (load-bearing): mean peak-count 15.7 ≫ 2. Decay does not restore a single
  peak — it makes the profile **more** scattered, because the soft-decayed phase-1 cells still
  SIT in the store at their old positions and create sharp secondary posterior swings; lowering
  their weight shifts the global argmax toward p_A' but multiplies the number of ≥½-peak
  midpoints.
- **c3 EARNED ✅**: (3a) no-retrain |peak−p_A| = 0.002 all seeds (held p_A, no drift). (3b)
  shuffle mean peak-count 7.0 ≥ 3 (incoherent — decay did NOT fabricate a coherent peak).
- **c4 vs-BUDGET ❌**: (4a ✅) soft-decay |peak−p_A'| 0.044 ≤ 0.081 — decay BEATS budget on
  distance. (4b ❌) soft-decay peak-count 15.7 ≰ 2, far WORSE than every H_1340 rung — decay
  LOSES to budget on coherence.

**FINDING.** Soft-decay is a STRONGER relocation lever than budget on the DISTANCE axis (peak
lands almost exactly on p_A', frac +0.88) but a WORSE one on the COHERENCE axis (peak-count
15.7 vs budget's 7.0). Neither raising resolution (H_1340) nor down-weighting the residual
phase-1 cells (H_1352) recovers a clean single CP peak at the moved cut: **the relocation
coherence residual is deeper than budget OR decay.** The decisive cause — exposed by both
follow-ons — is that the phase-1 prototypes are never PHYSICALLY relocated; they persist at the
old cut and inject secondary discrimination peaks. Budget drowns them with new cells (distance↑,
coherence↓); decay quiets their VOTE but not their geometric presence (distance↑↑, coherence↓↓).
A genuinely coherent full relocation needs the old cells to MOVE or be re-positioned (geometric
re-pack), not merely down-weighted or out-voted. `a_break_the_wall`: the H_1340 budget wall was
the wrong mechanism; H_1352 confirms decay is ALSO the wrong mechanism — both are
weight/count manipulations of a fixed geometry, and the geometry is the real ceiling. NO bar
moved (c9/p7).

## Honest scope (a_scale_honest_scope / a_toy_scale_recheck)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED (same family as H_1333/H_1338/H_1340/H_1341
R1). TOY synthetic continuum N=81 / 3 seeds / single shift p_A→p_A' / one frozen DECAY_GAMMA=0.80;
deterministic readout (tests the soft-decay STRUCTURE, not a learned decay). The 🧱 is a HONEST
pre-registered wall (genuine `a_break_the_wall` attempt — a new mechanism, not a re-run — that
the frozen coherence bar correctly refused to pass). NO human-cognition claim. Real-corpus /
multi-shift / leftward / a GEOMETRIC re-pack (move old prototypes) / engine-native
§CategoricalPerception wiring = follow-on.

## Pointers

- code: `state/cp-soft-decay/h1352_cp_soft_decay.py` (imports `state/universe-probes/h1333_whorf_developmental.py` verbatim)
- freeze: `.verdicts/1352_cp_soft_decay/FREEZE.txt` · result: `.verdicts/1352_cp_soft_decay/result.txt`
- index: `UNIVERSE/HYPOTHESES.jsonl` (id H_1352) · claim: `CLAIMS.tape` @C h1352_cp_soft_decay
- xref: H_1323 (parent Sapir-Whorf CP) · H_1333 (developmental plasticity 🟠) · H_1338 (eviction 🧱) · H_1340 (budget-sweep 🧱 parent) · H_1341 (shift-ladder 📈) · H_1342 (engine-native 🟢) · a_no_llm_frame_trap · a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · p7 · p8
