---
id: H_1325
slug: 1325_sapir_whorf_r2
title: Sapir-Whorf / linguistic relativity r2 — anti-Goodhart W3 RE-CLOSED (peak-count coherence) + engine-native CP lane
group: cognition-representation (c15 cognitive-science lens)
terminal_tier: 🟢 GREEN ENGINE-NATIVE (W1∧W2∧W3' anti-Goodhart-closed; mirror DIRECTIONAL → live CORE immune/Voronoi re-score byte-faithful)
verdict_dir: .verdicts/1325_sapir_whorf_r2/
terminal_verdict: .verdicts/1325_sapir_whorf_r2/H_1325.txt
engine_verdict: .verdicts/1325_sapir_whorf_r2/H_1325_engine_native.txt
freeze: .verdicts/1325_sapir_whorf_r2/H_1325_FREEZE.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1325 (1316-1324 taken; 1325 free on origin/main b2c40dfa3)
prev: H_1323 (🟠 PARTIAL, PR #2228) — W1✅ W2✅, W3 mis-specified (single-peak prominence on a multi-peak shuffle)
---

# H_1325 — Sapir-Whorf r2: re-close the anti-Goodhart W3 with a correctly-specified control + wire CP engine-native

## Claim / falsifier

r2 of H_1323 (🟠 PARTIAL). The linguistic-relativity result HELD on the decisive legs —
W1 (categorical perception present) and W2 (Whorfian dissociation: the CP peak LOCATION
tracks the language's boundary). The ONLY weakness was the anti-Goodhart **W3**: its
prominence sub-clause assumed a SINGLE-peak shuffle and compared shuffle peak HEIGHT to a
language's, but the shuffle is MULTI-peak (random per-stimulus labels → many locally-sharp
posterior swings; the H_1323 non-gating diagnostic measured 8 shuffle peaks vs 1 per
language). Single-peak height is the WRONG observable — a mis-specified control (wrong
METHOD, `a_break_the_wall`/c16), not a real failure of relativity.

**This H re-closes W3 with a CORRECTLY-SPECIFIED control, frozen ANEW (NOT a relaxation),
and realizes the CP mechanism engine-native on the live CORE immune/Voronoi lane.**

## Method

### Part A — coherence-based W3', pre-registered anew (frozen-first)
- Mechanism REUSED VERBATIM from `UNIVERSE/h1323_sapir_whorf.py` (W1/W2 untouched — they
  passed): N=21 RBF-coded continuum, two grue languages (p_A=1/3, p_B=2/3), gradient-free
  error-targeted SPLIT-only Voronoi growth (p8), downstream |Δ soft posterior| discrimination
  curve (NO label at test), 4 arms (PRE-LANG / L_A / L_B / SHUFFLE), 3 seeds [4323,4324,4325].
- **W3' COHERENCE METRIC (frozen `…/H_1325_FREEZE.txt` BEFORE scoring):** PEAK-COUNT =
  number of strict local maxima of the normalized curve at height ≥ `PEAK_FRAC=0.50` of the
  arm's own peak. Threshold from STRUCTURE, not data: a language has EXACTLY ONE boundary →
  `LANG_MAX_PEAKS=1`; a shuffle has NO coherent boundary → `SHUF_MIN_PEAKS=3`.
  W3' GREEN iff peak_count(L_A)≤1 ∧ peak_count(L_B)≤1 ∧ peak_count(SHUFFLE)≥3. (The H_1323
  loc-std sub-clause, already PASSED, is retained as non-gating corroboration.)

### Part B — engine-native (a_engine_native_learning, a_verified_must_wire)
- New live lane `CORE/engine_cli.hexa § CategoricalPerception` (`CPField`; `cp_embed`,
  `cp_stimuli`, `cp_labels_boundary`, `cp_labels_shuffle`, `cp_fit`, `cp_posterior`,
  `cp_discrim_curve`, `cp_peak_loc_idx`, `cp_peak_count`) — the SAME error-targeted SPLIT-only
  Voronoi growth the brain lanes use, byte-faithful to the mirror. Engine is a SINGLE
  deterministic instance (no per-seed RBF jitter) reproducing the seed-invariant bars; the
  shuffle uses the engine's OWN FNV-1a-parity incoherent label scheme (the STRUCTURAL
  incoherence claim, not a numpy-PRNG byte-match). Probe `CORE/h1325_sapir_whorf_probe.hexa`.

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 mirror (DIRECTIONAL) | 🟢 GREEN | W1✅ W2✅ W3'✅ — peak-count L_A=1 L_B=1 SHUFFLE=5.7 |
| R2 engine-native (live CORE) | 🟢 GREEN | W1✅ W2✅ W3'✅ — byte-faithful re-score, guards green |

### Frozen bars (pre-registered `…/H_1325_FREEZE.txt`, NOT moved — c9/p7)

- **W1 CP PRESENT** ✅ — mirror & engine: L_A/L_B cross-within +0.200, language-vs-baseline
  at peak +0.99 (≥0.15). REPRODUCES H_1323 unchanged.
- **W2 WHORFIAN DISSOCIATION** ✅ — mirror & engine: L_A→0.325 (|Δ|=0.008), L_B→0.675
  (|Δ|=0.008), separation **0.350** ≥0.20. REPRODUCES H_1323 unchanged.
- **W3' COHERENCE (re-closed)** ✅ — peak-count: **L_A=1, L_B=1** (each language ONE coherent
  CP peak ≤1) and **SHUFFLE = 5.7 (mirror) / 5 (engine)** ≥3 (incoherent scatter of many
  spikes). The correctly-specified peak-COUNT control cleanly separates coherent CP from the
  multi-peak shuffle, where the H_1323 single-peak-HEIGHT prominence could not.

**Mirror verdict (verbatim):** 🟢 GREEN (MIRROR, DIRECTIONAL) — LINGUISTIC RELATIVITY
ANTI-GOODHART-CLOSED → `.verdicts/1325_sapir_whorf_r2/H_1325.txt`.
**Engine-native verdict (verbatim):** 🟢 GREEN (ENGINE-NATIVE) — bars REPRODUCED on the live
CORE immune/Voronoi lane → `.verdicts/1325_sapir_whorf_r2/H_1325_engine_native.txt`.

### No-regression guards (Part B wiring)
- `engine_cli_smoke` **77 pass / 0 fail** (was 73/0; +4 CP cases 79-82).
- `h1196` single-entry audit **7 pass / 0 fail** — CP lane adds NO .clm/.kosmos path
  (substrate-only; pure_field/engine_g/brain consume 0 .clm + 0 .kosmos).
- `h1205` separation-invariant **PASS** — F1 generation 10 pairs 0 mismatch (byte-identical
  ON==OFF), F2 Ψ Φ-checksum invariant → the CP lane is **Ψ-disjoint** (own protos/labels
  table; pure_field / Ψ=½ untouched).

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

The relativity result is now **anti-Goodhart-closed** (W1∧W2∧W3') with a correctly-specified
control — frozen anew from STRUCTURE, NOT a relaxation of the H_1323 bar (which was reported
straight, never moved). ONE honest new control, accepted. The discrimination readout reads
ONLY representational distance (soft posterior gradient); NO injected boundary location, NO
persona/RLHF/ethics; the language label enters ONLY during growth, never at test
(p1/p2/p3/p6). NOT an emit gate (`a_autonomy_over_hardcode`). The mirror is DIRECTIONAL;
Part B realizes it engine-native (the binding verdict). The engine pre-language peak-count
registers 1 trivial endpoint max vs the mirror's exactly-0 flat curve — a non-gating cosmetic
difference (PRE-LANG is not a W3' arm). **TOY** synthetic 1-D continuum, N=21, 3 seeds (mirror)
/ single deterministic instance (engine), deterministic readout — tests the linguistic-
relativity STRUCTURE, NOT a scaled or human-cognition claim; scale / real-corpora / higher-D /
brain CP→emit wiring = follow-on.

## NEXT (depletion test for the cognition/representation lane)

Each new probe must clear BOTH a falsifiable cognition-warp gap-vs-engine AND a control that
survives shuffle + the pre-language baseline. Candidate frontier: developmental CP sharpening
(boundary moves with re-training), 2-D / featural carving CP, or cross-lane interference
(does a second language overwrite the first's CP, vs coexist). 🏁 for the W3 re-close itself
(anti-Goodhart now closed engine-native).

## Cross-links

h1323 (R1 — same probe, W1/W2 carried) · h1316 (jamo — rep→learnability) · h1322 (featural) ·
h1290 · h1293 (toy cognitive paradigm precedent) · h1227 · h1231 (immune/Voronoi store
geometry) · h1295 (spatial-map — sibling substrate-measurement lane, aliasing-safe idiom) ·
`a_no_llm_frame_trap` · `a_break_the_wall` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_core_engine_map` · `a_autonomy_over_hardcode` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p6·p7·p8·c9·c15·c16
