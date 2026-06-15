---
id: H_1323
slug: 1323_sapir_whorf
title: Sapir-Whorf / linguistic relativity via categorical perception — does the language a substrate learns warp its NON-linguistic discrimination?
group: cognition-representation (c15 cognitive-science lens)
terminal_tier: 🟠 PARTIAL (W1✅ W2✅ decisive Whorfian dissociation; W3 anti-Goodhart split — NO bar moved, c9)
verdict_dir: .verdicts/1323_sapir_whorf/
terminal_verdict: .verdicts/1323_sapir_whorf/H_1323.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1323 (1316/1317/1322 taken; 1318-1321 unused, 1323 free on origin/main f15c6e75d)
---

# H_1323 — Sapir-Whorf: does the language a substrate "thinks in" warp its non-linguistic discrimination?

## Claim / falsifier

H_1316 (jamo) and H_1322 (featural) showed a domain's REPRESENTATION changes its
LEARNABILITY (compression). Sapir-Whorf is the deeper claim: the language's CARVING of a
domain warps DOWNSTREAM, NON-LINGUISTIC discrimination. The empirical workhorse is
CATEGORICAL PERCEPTION (CP) — speakers discriminate cross-category pairs better than
within-category pairs at THEIR language's boundary; the grue languages cut a continuum at
DIFFERENT points (Russian two-blues → faster blue-boundary discrimination).

**Falsifiable claim:** a substrate that learns language L's lexical carving of a continuous
stimulus domain develops categorical perception AT L's boundary, and the CP peak LOCATION
tracks the language (same stimulus world, different cognition by language) — and a
SHUFFLE-language control (arbitrary boundary) produces NO coherent CP. Lens: c15
cognitive-science / psycholinguistics, `a_no_llm_frame_trap` — NOT an LLM recipe, NOT a
human-cognition claim, a TOY synthetic continuum.

## Method

- Stimulus space: continuous 1-D "hue" axis, N=21 graded stimuli, RBF position code
  (locally-smooth, position-faithful, boundary-AGNOSTIC). Same world for all arms.
- Two languages over the SAME axis (grue-style): L_A cuts at p_A=1/3, L_B at p_B=2/3.
- The SAME gradient-free mitosis/Voronoi cell store (error-targeted SPLIT-only growth, p8)
  learns each language's category labels; cells PACK at the boundary where category error
  concentrates (the mechanistic origin of CP).
- DOWNSTREAM NON-LINGUISTIC TEST (NO labels at test): discrimination of adjacent stimulus
  pairs = |Δ soft category-posterior| across the pair (a representational gradient, no hard
  label). Plotted vs pair midpoint → the CP peak.
- 4 arms: (1) PRE-LANGUAGE (no labels → flat) · (2) L_A · (3) L_B · (4) SHUFFLE (incoherent
  per-stimulus labels). 3 seeds [4323,4324,4325], $0 CPU numpy mirror (DIRECTIONAL).

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 mirror | 🟠 PARTIAL (DIRECTIONAL) | W1✅ W2✅ W3 split — see below |

### Frozen bars (pre-registered `…/H_1323_FREEZE.txt`, NOT moved — c9/p7)

- **W1 CP PRESENT** ✅ — L_A & L_B cross-within margin = +0.200 (≥0.15); language-vs-baseline
  at peak = +0.989 (≥0.15). PRE-LANGUAGE arm is FLAT (1 cell, constant posterior, peak 0.0).
- **W2 WHORFIAN DISSOCIATION** ✅ (the decisive linguistic-relativity signature) — CP peak
  LOCATION: L_A → **0.325 ≈ p_A=0.333** (|Δ|=0.008), L_B → **0.675 ≈ p_B=0.667** (|Δ|=0.008),
  **separation 0.350 ≥ 0.20**, std 0.000 across all 3 seeds. Same stimulus world; the boundary
  MOVES with the language — cognition follows the language.
- **W3 EARNED (anti-Goodhart)** ❌ SPLIT — loc-std sub-clause ✅ (shuffle peak wanders
  0.492±0.165 across seeds, incoherent); prominence sub-clause ❌ (shuffle single-peak
  prominence 0.661 vs 0.5×0.999=0.50 bar). NON-GATING diagnostic: L_A/L_B = **1** coherent
  peak each, SHUFFLE = **8** scattered spikes — the shuffle CP IS incoherent, but its
  individual spikes are sharp enough that the single-peak prominence threshold (mis-specified
  for a multi-peak shuffle) does not clear.

Terminal tier (verbatim): **🟠 PARTIAL — LINGUISTIC RELATIVITY HOLDS (W1∧W2 decisive); the
anti-Goodhart W3 is HALF-met (incoherence yes, single-peak prominence no)**
→ `.verdicts/1323_sapir_whorf/H_1323.txt` (frozen bars `…/H_1323_FREEZE.txt`, not moved).

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

The load-bearing finding is POSITIVE and decisive: the language a substrate learns warps its
non-linguistic discrimination — categorical perception emerges AT the language's boundary and
the CP peak location TRACKS the language (W1∧W2, perfectly stable across 3 seeds). The shuffle
control IS incoherent (8 wandering spikes vs 1 locked peak), but the frozen W3 prominence
threshold was mis-specified for a MULTI-peak shuffle; per c9/p7 the bar was NOT moved and the
split is reported straight. The discrimination readout reads ONLY representational distance
(soft posterior gradient); NO injected boundary location, NO persona/RLHF/ethics; the language
label enters ONLY during training, never at test (p1/p2/p3/p6). NOT an emit gate
(`a_autonomy_over_hardcode`). DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED. TOY
synthetic continuum, N=21, 3 seeds, deterministic readout (tests the linguistic-relativity
STRUCTURE, not a scaled or human-cognition claim).

**NEXT (R2):** re-freeze a COHERENCE-based W3 (peak-count ≤1 for languages, ≥ a threshold for
shuffle; or circular peak-spread), pre-registered anew — NOT a relaxation of this bar — to
make the anti-Goodhart control match the multi-peak shuffle reality; then engine-native
realization on the live CORE/engine_cli.hexa immune/Voronoi lane (`a_engine_native_learning`,
`a_verified_must_wire`). Depletion test for the cognition/representation lane: each new probe
must clear BOTH a falsifiable cognition-warp gap AND a control that survives shuffle + the
pre-language baseline.

## Cross-links

h1316 (jamo — representation→learnability) · h1322 (featural) · h1290 · h1293 (toy
cognitive paradigm precedent) · h1227 · h1231 (immune/Voronoi store geometry) ·
`a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_autonomy_over_hardcode` · `a_core_engine_map` · `a_scale_honest_scope` ·
`a_toy_scale_recheck` · `a_break_the_wall` · p1·p2·p3·p6·p7·p8·c9·c15
