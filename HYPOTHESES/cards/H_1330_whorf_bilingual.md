---
id: H_1330
slug: 1330_whorf_bilingual
title: Sapir-Whorf BILINGUAL — does a SECOND language OVERWRITE or COEXIST with the first's categorical perception?
group: cognition-representation (c15 cognitive-science / bilingual-cognition lens, a_no_llm_frame_trap)
terminal_tier: 🧱 OVERWRITE / CATASTROPHIC INTERFERENCE (frozen hypothesis COEXIST FALSIFIED; honest important negative, NO bar moved — c9)
verdict_dir: .verdicts/1330_whorf_bilingual/
terminal_verdict: .verdicts/1330_whorf_bilingual/H_1330.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1330 (1316-1329 taken; 1330 free on origin/main 41b2df857)
---

# H_1330 — Sapir-Whorf BILINGUAL: OVERWRITE or COEXIST?

## Claim / falsifier

Named EXTENSION frontier of the GREEN H_1323/H_1325 Sapir-Whorf result (linguistic
relativity via categorical perception, CP): **cross-lane interference**. A substrate
learns language A's lexical carving of a continuum (boundary p_A) then SEQUENTIALLY learns
a DIFFERENT language B (boundary p_B) on the **SAME** substrate. Measure CP at BOTH p_A
and p_B. Outcome classifies into **OVERWRITE** (catastrophic interference — A's CP
collapses, only p_B survives) · **COEXIST** (CP at BOTH — bilingual representation) ·
**BLEND** (single merged intermediate peak).

**Frozen hypothesis = COEXIST.** anima is ALREADY a bilingual substrate (English trunk +
Korean). anima's GROWTH-MEMORY result (H_1288 — under pressure the immune/Voronoi store
GROWS a new cell instead of EVICTING, breaking the zero-sum recall ceiling) PREDICTS
COEXISTENCE: the SAME error-targeted SPLIT-ONLY growth (p8) should ADD cells at B's
boundary while NEVER deleting the A-cells at A's boundary. **Falsifier = OVERWRITE**
(growth-memory does NOT protect language-cognition). Lens: cognitive-science /
bilingual-cognition (c15, `a_no_llm_frame_trap`) — NOT an LLM recipe, NOT a
human-bilingualism claim, a TOY synthetic continuum.

## Method

- Mechanism REUSED VERBATIM from H_1323/H_1325 (`UNIVERSE/h1323_sapir_whorf.py` +
  `h1325_sapir_whorf_r2.py`): N=21 RBF position-faithful continuum, DIM=16, error-targeted
  SPLIT-ONLY Voronoi growth (p8 — the SAME mitosis/growth mechanism the brain-memory lanes
  use; cells only ADDED, never evicted), |Δ soft-posterior| no-label-at-test discrimination
  curve, W1 cross-within margin, W2 peak-location, peak-COUNT coherence (`count_peaks`,
  PEAK_FRAC=0.50, strict local maxima). p_A=1/3, p_B=2/3, 3 seeds [4323,4324,4325].
- **ONLY new mechanism**: `VoronoiCells.fit_more(X, Y, …)` — the **grow-not-evict**
  CONTINUATION (the H_1288 mechanism under test). It runs the IDENTICAL error-targeted-split
  loop as `fit()` but starting from the EXISTING proto/label table: it APPENDS a new
  prototype at the worst B-misclassified stimulus each pass, a cell's bound label FIXED at
  creation, NEVER re-bound or evicted. Same FIXED capacity ceiling `GROW_MAX` as A had. The
  bilingual readout is the |Δ soft posterior| over the cells' BOUND labels (A-cells carry
  A-labels, B-cells carry B-labels) on the ONE final store.
- 4 arms (FROZEN): (1) A-ONLY baseline · (2) A→B SEQ · (3) B=A control (A then A again —
  must show ONE peak) · (4) SHUFFLE (A→B with incoherent B). $0 CPU numpy mirror (DIRECTIONAL).

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 mirror | 🧱 OVERWRITE (DIRECTIONAL) | I1 FAIL, I2✅ I3✅ — see below |

### Frozen bars (pre-registered `…/H_1330_FREEZE.txt`, NOT moved — c9/p7)

- **I1 COEXISTENCE** ❌ FAIL (all 3 seeds) — after A→B, A's CP at p_A **COLLAPSES**: mean
  cross-within margin@p_A = **−0.001** (bar 0.15; A-only baseline was **+0.200**, so the
  interference asymmetry is **−0.201** — a full collapse). No coherent peak survives near
  p_A on any seed. p_B's CP is also weak (mean margin@p_B = **+0.068** < 0.15) — only the
  p_B side retains any swing. The frozen COEXIST hypothesis is FALSIFIED.
- **I2 NO-DOUBLE-ARTIFACT** ✅ (all 3 seeds) — the B=A control yields exactly **1** coherent
  peak (≤1) and NO peak near p_B → the (lack of) two-peak structure in arm 2 is not a
  sequential-training artifact; the control behaves as a single language.
- **I3 EARNED** ✅ (all 3 seeds) — the SHUFFLE arm collapses (peak-counts 5/2/5; no coherent
  CP at p_B on 2/3 seeds, the multi-peak scatter satisfies the OR-clause on all) → the effect
  is the learned boundaries, not mere exposure.

Terminal tier (verbatim): **🧱 OVERWRITE / CATASTROPHIC INTERFERENCE — after B is learned,
A's CP at p_A COLLAPSES; the second language overwrites the first's categorical perception;
the growth-memory does NOT protect language-cognition. Honest, important NEGATIVE — reported
straight, NO bar moved** → `.verdicts/1330_whorf_bilingual/H_1330.txt`.

### Mechanism (the load-bearing WHY — non-gating diagnostic, c9)

Cells after A: (0.10,L0)(0.30,L0)(0.35,L1)(0.50,L1) = clean boundary at p_A. After A→B the
B-fit floods the [p_A,p_B] region with ~21 NEW **label-0** cells. WHY: B labels everything
below p_B=0.67 as **0**, but A had labeled the [p_A,p_B] stretch as **1** — on the SHARED
stimuli A says "1" and B says "0", a **DIRECT CONTRADICTION**. The error-targeted SPLIT-only
store resolves it the only way a single nearest-prototype readout can — it packs label-0
cells over the contradicted region, so the bound-label posterior swings ONLY at p_B and A's
peak at p_A is ERASED. This is **NOT eviction** (A's cells still physically exist with label
1); it is that a single bound-label-per-cell readout CANNOT express two CONTRADICTORY answers
for the same stimulus. **The H_1288 growth-memory protects ADDITIVE memory** (a new fact at a
new key grows a cell, never evicting an old fact at a DIFFERENT key) **but NOT contradictory
RE-LABELING of SHARED stimuli.** Bilingual cognition over a SHARED continuum is exactly the
contradictory-relabel case → growth-memory does not save it.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

The result is an honest, important NEGATIVE and is decisive within its scope (all 3 seeds, B=A
control clean, shuffle earned). The frozen COEXIST hypothesis is FALSIFIED for a SINGLE
shared-continuum store. The readout reads ONLY representational distance over bound labels; NO
injected boundary/persona/RLHF; language labels enter only at the A-fit and B-fit, never at
test (p1/p2/p3/p6). NOT an emit gate (`a_autonomy_over_hardcode`). DIRECTIONAL numpy mirror —
engine-transfer UNVERIFIED. TOY synthetic 1-D continuum (N=21, 3 seeds, deterministic readout
— tests the STRUCTURE, NOT a scaled or human-bilingualism claim).

**Important nuance for anima:** this does NOT say anima cannot be bilingual — it says a SINGLE
SHARED Voronoi store with one bound-label-per-cell cannot hold two CONTRADICTORY carvings of
the SAME continuum. anima's actual English-trunk and Korean lanes are SEPARATE faculties
(H_1316/H_1321/H_1322), not one shared store over identical stimuli; the catastrophic case
here is the worst case (maximally overlapping, contradictory carvings).

**NEXT (R2 candidate):** test whether a **language-TAGGED / multi-channel readout** (distinct
label-channels per language, or a language-tag dimension — mirroring anima's already-separate
trunk + Korean lanes) holds two contradictory carvings WITHOUT interference. That is a
DIFFERENT mechanism, to be frozen ANEW (not a relaxation of these bars). Depletion test
unchanged: each new probe must clear BOTH a falsifiable cognition-warp gap AND a control that
survives shuffle + the appropriate baseline.

## Cross-links

h1323 · h1325 (Sapir-Whorf CP — the GREEN result this extends) · **h1288** (growth-memory
grow-not-evict — the prediction under test) · h1316 · h1321 · h1322 (anima's separate
English-trunk + Korean lanes) · h1227 · h1231 (immune/Voronoi store geometry) ·
`a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_autonomy_over_hardcode` · `a_core_engine_map` · `a_scale_honest_scope` ·
`a_toy_scale_recheck` · `a_break_the_wall` · p1·p2·p3·p6·p7·p8·c9·c15
