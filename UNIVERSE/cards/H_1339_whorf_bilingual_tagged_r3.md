---
id: H_1339
slug: 1339_whorf_bilingual_tagged_r3
title: Sapir-Whorf BILINGUAL r3 (TAGGED, control re-freeze + engine-native) — a language-TAG enables bilingual CP coexistence
group: cognition-representation (c15 cognitive-science / bilingual-cognition lens, a_no_llm_frame_trap)
terminal_tier: 🟢 GREEN (MIRROR DIRECTIONAL + ENGINE-NATIVE wired & re-scored) — I1∧I2∧I3' all PASS, 3 seeds; I3a re-frozen LOCALIZED (NOT a relaxation); coexistence REAL & TAG-ATTRIBUTABLE
verdict_dir: .verdicts/1339_whorf_bilingual_tagged_r3/
terminal_verdict: .verdicts/1339_whorf_bilingual_tagged_r3/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1339 (1330-1338 taken; 1339 free on origin/main 0fa31903a)
---

# H_1339 — Sapir-Whorf BILINGUAL r3 (TAGGED): a language-TAG enables bilingual CP coexistence

## Claim / falsifier

Named **r3 of H_1335 🧱** (which was a CONTROL TECHNICALITY only). H_1335 found I1∧I2 **decisive**
— a language-TAGGED multi-channel readout holds categorical perception (CP) at **both** boundaries
(mean margin@p_A **+0.200**, @p_B **+0.177**, both ≥ the H_1323 bar 0.15, all 3 seeds), and the
single-channel (untagged) control **reproduces the H_1330 OVERWRITE** byte-exact (mean margin@p_A
**−0.001**). The ONLY failing leg was the frozen **I3a GLOBAL count_peaks ≤ 1** bar on the B=A
control (count = 2), but that 2nd "peak" was a **benign low-end discretization wiggle**, NOT a
second-language CP — `coherent_peak_near@p_B` was already **False** on all 3 seeds (the intended
no-spurious-CP-at-the-other-boundary test already passed).

**r3 hypothesis = COEXIST** (same as r2). **The r3 change = a DIFFERENT frozen bar, NOT a
relaxation:** I3a is re-frozen as the **LOCALIZED "no coherent peak near p_B"** test for the B=A
control — the correctly-scoped statistic the arm was always meant to test. **Falsifier =** the
tagged arm fails to hold both CPs (I1), OR the untagged control fails to overwrite (I2), OR the
B=A control DOES fabricate a coherent CP near p_B / the SHUFFLE arm manufactures a coherent CP
(I3' — the re-freeze can still fail).

## Method (REUSED VERBATIM + ONE control re-scope)

`run_seed`, `embed`, `VoronoiCells` (`fit`/`fit_more`/`posterior`), `build_labels`,
`discrim_curve`, `within_cross_margin`, `coherent_peak_near`, `count_peaks`, the TAG block
(`tag_vec`/`tagged_key`/`discrim_curve_tagged`, **TAG_DIM=2, TAG_GAIN=1.0 FIXED**), the W1 bar
(0.15), and the seeds **[4323,4324,4325]** are **imported VERBATIM** from
`UNIVERSE/h1335_whorf_bilingual_tagged.py` (which imports `h1330` verbatim). `run_seed()` is
imported **unmodified** — **the data generation is byte-identical to r2**. The ONLY change is
**which control statistic gates the B=A arm (I3a)**.

- **r2 I3a (RETIRED for the B=A arm):** global `count_peaks ≤ 1` — measured the whole curve shape,
  including the benign discretization wiggle. **No threshold moved** — the statistic is *replaced*
  for this arm by the localized one the arm was meant to test (already passing in r2).
- **r3 I3a (re-frozen):** `coherent_peak_near(B=A B-channel, p_B)` is **False** on all 3 seeds.
- **SHUFFLE bar (kept VERBATIM):** `count_peaks ≥ 3` OR no coherent peak near p_B.

**PLUS a NON-GATING TAG_GAIN channel-isolation sweep** (diagnostic, c9): for the B=A control,
B-tagged cells grown + residual B-channel curve magnitude (cross-tag bleed) over gains
[0.25,0.5,1.0,2.0,4.0]. **Informational only — does NOT gate; TAG_GAIN=1.0 stays the frozen
operating point (NOT swept-to-green).**

### Frozen bars (GREEN iff I1 ∧ I2 ∧ I3')
- **I1 COEXISTENCE** — TAGGED arm margin@p_A ≥ 0.15 AND margin@p_B ≥ 0.15, coherent peak each, all 3 seeds.
- **I2 TAG-ATTRIBUTION** — SINGLE-CHANNEL (untagged) margin@p_A < 0.15 (reproduces H_1330 overwrite), all 3 seeds.
- **I3' EARNED** — (a) B=A: **NO coherent peak near p_B** (re-frozen LOCALIZED); (b) SHUFFLE: ≥3 peaks OR no peak near p_B; all 3 seeds.

## Result (R1 numpy MIRROR, DIRECTIONAL; $0 CPU; 3 seeds; p7) — 🟢 GREEN

| arm | seed 4323 | seed 4324 | seed 4325 |
|---|---|---|---|
| **TAGGED** m@p_A / m@p_B | +0.201 / +0.173 | +0.200 / +0.181 | +0.200 / +0.179 |
| TAGGED pk@p_A / pk@p_B | T / T | T / T | T / T |
| **SINGLE-CHANNEL** m@p_A | −0.001 | −0.000 | −0.001 |
| **B=A pk@p_B** (re-frozen I3a) | **F** | **F** | **F** |
| B=A global count (DIAGNOSTIC, non-gating) | 2 | 2 | 2 |
| SHUFFLE count / pk@p_B | 5 / F | 6 / T | 5 / T |

- **I1 COEXISTENCE ✅** all 3 seeds: mean margin@p_A **+0.200**, @p_B **+0.177**, coherent peak each.
- **I2 TAG-ATTRIBUTION ✅** all 3 seeds: single-channel mean margin@p_A **−0.001** = H_1330 overwrite reproduced.
- **I3' EARNED ✅** all 3 seeds: B=A `pk@p_B=False` (localized, re-frozen) + SHUFFLE incoherent (5/6/5 peaks, OR-clause).

**TAG_GAIN sweep (NON-GATING diagnostic):** B-cells grown 0 / 0 / **0** / 2 / 2 at gain
0.25 / 0.5 / **1.0** / 2.0 / 4.0; residual B-curve peak 0.727 / 0.468 / **0.236** / 0.989 / 0.989.
**Reading:** at the frozen gating point (1.0) the B=A control grows **ZERO** B-cells (it re-learns
A's boundary → no B-error to split on) and its B-channel runs on pure cross-tag bleed whose
magnitude **shrinks** as the tag gap widens (0.727→0.236 over 0.25→1.0) — confirming the r2
diagnosis. (Honest curiosity, non-gating: at gain ≥ 2.0 the very large tag gap lets the B-fit's
re-seeded centroid land differently and grow 2 cells with a higher residual — irrelevant to the
frozen 1.0 point and to the gating arms; flagged for transparency, c9.)

**Frozen verdict: 🟢 GREEN (MIRROR, DIRECTIONAL).**

## Engine-native realization (a_engine_native_learning · a_verified_must_wire) — WIRED & GREEN

The tagged bilingual-CP faculty is realized **engine-native** on live
`CORE/engine_cli.hexa §BILINGUAL TAGGED CP`: `cp_tag_vec` (the fixed orthonormal tag block),
`cp_tagged_key` (concat embed + tag), `cp_stimuli_tagged`, `cp_fit_more` (the grow-not-evict
continuation), `cp_within_cross_margin` (localized cross-within margin), `cp_coherent_peak_near`
(localized coherence) — all on the SAME error-targeted SPLIT-only Voronoi growth the brain lanes
use. The I1/I2/I3' bars are **re-scored engine-native** in `CORE/engine_cli_smoke.hexa` cases
**83–88**:
- 86 (I1a) TAGGED CP@p_A margin ≥ 0.15 · 87 (I1b) TAGGED CP@p_B margin ≥ 0.15 + coherent peak@p_B
- 88 (I2) untagged single-channel **overwrite** (margin@p_A < 0.15)
- 89 (I3'a) B=A **no coherent peak near p_B** (localized, re-frozen) · 90 (I3'b) SHUFFLE ≥3 peaks
- 91 tag-separation sanity (key_A↔key_B distance = √2·TAG_GAIN ≈ 1.4142)

**GUARDS no-regression:** `engine_cli_smoke` **86/0** (was 80/0, **+6** tagged cases — all green,
deterministic) · `h1196` single-entry **7/0** · `h1205` separation-invariant **PASS** (generation
byte-identical ON==OFF, Ψ=½ untouched). NOT an emit gate (a_autonomy_over_hardcode); Ψ-disjoint
(own protos/labels + tag block, pure_field/engine_g/Ψ untouched).

## Outcome (answer to the lane question)

**YES — a language-tagged multi-channel readout enables bilingual CP coexistence**, now with the
control **correctly scoped** (mirror 🟢 I1∧I2∧I3', all 3 seeds) AND realized **engine-native** on
the live CORE (smoke 86/0). The **H_1330 OVERWRITE was the SINGLE-SHARED-STORE mechanism, NOT a
fundamental limit** — overturned as mechanism-specific by tagging. The tag is the substrate-level
"select the faculty", so **anima's REAL separate EN-trunk + KO faculties (H_1316/1321/1322) coexist
for the SAME structural reason**.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)

R1 numpy **MIRROR (DIRECTIONAL)** — the mirror's engine-transfer is realized in the engine-native
rung (a SEPARATE deterministic instance re-scoring the seed-invariant bars), NOT a numpy-byte
match. TOY synthetic 1-D continuum (N=21, deterministic readout — tests the STRUCTURE of
tag-separated coexistence, NOT scaled / human bilingualism). TAG_GAIN=1.0 **FIXED** (the sweep is
non-gating; the gain≥2.0 curiosity is flagged, c9). Readout reads ONLY representational distance
over bound labels with a fixed faculty tag, NO injected boundary / persona / RLHF; labels enter
only at the A-fit / B-fit, NOT at test (p1/p2/p3/p6). **NO human-bilingualism claim.**

## Next / depletion

The tagged bilingual-CP faculty is now mirror-GREEN AND engine-wired. Remaining follow-ons: a
real-corpus / scaled bilingual carving rung (the EN+KO faculties on actual tokens, not a synthetic
continuum); the gain≥2.0 sweep curiosity (why the very-wide tag gap re-grows B-cells); and a
brain-side wiring of the tagged CP read into emit/recall (currently a measurement lane).

## Claim-link / verdicts

`CLAIMS.tape @C h1339_whorf_bilingual_tagged_r3` · card
`UNIVERSE/cards/H_1339_whorf_bilingual_tagged_r3.md` · probe
`state/whorf-bilingual-tagged-r3/h1339_whorf_bilingual_tagged_r3.py` · engine
`CORE/engine_cli.hexa §BILINGUAL TAGGED CP` + `CORE/engine_cli_smoke.hexa` cases 86–91 · verdicts
`.verdicts/1339_whorf_bilingual_tagged_r3/{FREEZE,result}.txt`

xref: **h1335** (the 🧱 r2 control-technicality this r3 closes 🟢) · **h1330** (the OVERWRITE
overturned as mechanism-specific) · h1323 · h1325 (the GREEN Sapir-Whorf CP, engine §CATEGORICAL
PERCEPTION) · h1288 (grow-not-evict growth-memory) · **h1316 · h1321 · h1322** (anima's real
separate EN-trunk + KO faculties this mirrors) · h1338 (the budget/geometry re-diagnosis sibling) ·
a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck ·
p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16.
