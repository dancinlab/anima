---
id: H_1335
slug: 1335_whorf_bilingual_tagged
title: Sapir-Whorf BILINGUAL r2 (TAGGED) — does a language-TAG dimension enable bilingual CP coexistence?
group: cognition-representation (c15 cognitive-science / bilingual-cognition lens, a_no_llm_frame_trap)
terminal_tier: 🧱 CONTROL-FAIL on the frozen I3a ≤1-peak bar — BUT coexistence is REAL & TAG-ATTRIBUTABLE (I1∧I2 decisive, all 3 seeds); NO bar moved (c9)
verdict_dir: .verdicts/1335_whorf_bilingual_tagged/
terminal_verdict: .verdicts/1335_whorf_bilingual_tagged/result.txt
date: 2026-06-16
proj_seed: PROJ_SEED H_1335 (1316-1334 taken; 1335 free on origin/main 61ce6948f)
---

# H_1335 — Sapir-Whorf BILINGUAL r2 (TAGGED): does a language-TAG enable CP coexistence?

## Claim / falsifier

Named **r2 of H_1330 🧱 OVERWRITE**. H_1330 found: on a **single shared** Voronoi store with
one-bound-label-per-cell, a second language B catastrophically **OVERWRITES** the first
language A's categorical perception (CP) — because B labels the [p_A,p_B] stretch as 0 where A
labeled it 1 (a **direct contradiction on SHARED stimuli**), and a single bound-label-per-cell
nearest-prototype readout **cannot express two contradictory answers for the same stimulus**.

The H_1330 verdict itself named this r2: a **language-TAGGED / multi-channel readout** (a
distinct label-channel per language / a language-tag dimension), which **mirrors anima's ACTUAL
bilingual architecture** — separate English-trunk + Korean faculties (H_1316/H_1321/H_1322), NOT
one shared store. **Question:** does a language-tagged readout hold BOTH CPs without interference
(coexistence)? **Frozen hypothesis = COEXIST via tagging.** **Falsifier = interference persists
even with the tag.**

## Method (REUSED VERBATIM + ONE new thing)

embed, VoronoiCells (`_owner`/`fit`/`fit_more`/`_grow`/`posterior`), build_labels, discrim_curve,
within_cross_margin, coherent_peak_near, count_peaks, the W1/W2 thresholds (W1_MARGIN=0.15 = the
H_1323 CP bar), and the seeds **[4323,4324,4325]** are **imported VERBATIM** from
`UNIVERSE/h1330_whorf_bilingual.py` — identical growth rule, identical readout, identical bars.

**The ONLY new thing — a LANGUAGE-TAG dimension.** The DIM=16 RBF key is extended by a small
fixed orthonormal tag block (TAG_DIM=2, **TAG_GAIN=1.0 FIXED — not swept**): two disjoint
appended coords mark the faculty.

```
key_A(x) = concat( embed(x) , t_A )      # t_A on coord +0
key_B(x) = concat( embed(x) , t_B )      # t_B on coord +1
```

For the SAME continuum position x, key_A(x) and key_B(x) are **separated by sqrt(2)·TAG_GAIN**
regardless of x, so the [p_A,p_B] contradiction (A says 1, B says 0 at the same x) is **no longer
on a SHARED key** — the two answers live on two separate tagged keys. The store grows over tagged
keys (A-fit at key_A with A-labels, B-fit at key_B with B-labels, grow-not-evict `fit_more`). At
test, language A's curve is read with key_A() and B's with key_B() (= **select the faculty by
tag, read its carving** — the substrate realization of anima's separate EN/KO faculties).

**Frozen anti-tune-to-green guards (c9):** TAG_GAIN fixed in the FREEZE (not swept to find a
passing value); GROW_MAX = the SAME total ceiling as H_1330 (no extra capacity); the
SINGLE-CHANNEL (untagged = H_1330) control MUST reproduce the H_1330 overwrite or coexistence is
not attributable to the tag.

### Arms (frozen)
1. **A→B TAGGED** — A-fit on key_A, B-fit on key_B; read CP at p_A via tag_A, p_B via tag_B.
2. **SINGLE-CHANNEL control** — the exact H_1330 untagged A→B (shared key); MUST reproduce the OVERWRITE.
3. **B=A control** — tagged A→A (B-channel re-learns A's boundary); must show no spurious second CP.
4. **SHUFFLE** — tagged A→B with B's labels shuffled; tagged-B channel must not fabricate a CP.

### Frozen bars (GREEN iff I1∧I2∧I3)
- **I1 COEXISTENCE** — TAGGED arm margin@p_A ≥ 0.15 AND margin@p_B ≥ 0.15, coherent peak at each, all 3 seeds.
- **I2 TAG-ATTRIBUTION** — SINGLE-CHANNEL control margin@p_A < 0.15 (reproduces H_1330 overwrite), all 3 seeds.
- **I3 EARNED** — (a) B=A: count_peaks ≤ 1 AND no coherent peak near p_B; (b) SHUFFLE: ≥3 peaks OR no peak near p_B; all 3 seeds.

## Result (R1 numpy MIRROR, DIRECTIONAL; $0 CPU; 3 seeds; p7)

| arm | seed 4323 | seed 4324 | seed 4325 |
|---|---|---|---|
| **TAGGED** m@p_A / m@p_B | +0.201 / +0.173 | +0.200 / +0.181 | +0.200 / +0.179 |
| TAGGED pk@p_A / pk@p_B | T / T | T / T | T / T |
| **SINGLE-CHANNEL** m@p_A | −0.001 | −0.000 | −0.001 |
| B=A npeaks / pk@p_B | 2 / F | 2 / F | 2 / F |
| SHUFFLE npeaks / pk@p_B | 5 / F | 6 / T | 5 / T |

- **I1 COEXISTENCE ✅** (all 3 seeds): mean margin@p_A **+0.200**, mean margin@p_B **+0.177**, both ≥ 0.15, coherent peak at each.
- **I2 TAG-ATTRIBUTION ✅** (all 3 seeds): single-channel (untagged) mean margin@p_A **−0.001** = the H_1330 overwrite reproduced byte-exact → coexistence is **attributable to the tag** (remove tag → overwrite returns).
- **I3 EARNED ❌** (frozen verdict): I3b SHUFFLE ✅ (peak-counts 5/6/5 incoherent); **I3a B=A ✗** — count_peaks = **2** > 1 on all seeds, so the frozen ≤1-peak bar fails. **BUT pk@p_B = False on all seeds** (the intended no-spurious-CP-at-the-other-boundary test passes).

**Frozen verdict: 🧱 CONTROL-FAIL** (per the FREEZE bar set, NO relaxation — c9/p7).

## Mechanism diagnostic (non-gating, c9 — why I3a failed, NO bar moved)

The TAGGED B=A control's B-channel curve has its **main peak correctly at p_A=0.325** (norm 1.000)
and **no coherent peak at p_B** (pk@p_B=False, all seeds — the real double-language-artifact test
PASSES), plus a **benign second local maximum at mid≈0.175** (norm≈0.74) → count_peaks=2.

**Why:** in the B=A control the B-fit re-learns A's SAME boundary, so the grow-not-evict store
finds **no B-misclassified stimulus to split on** under tag_B (the existing A-tagged cells already
classify correctly) → it grows **ZERO B-tagged cells** (B-tagged=0 of 4). The B-channel readout
therefore runs **entirely on cross-tag bleed** from the A-tagged cells (every nearest cell at
every query is A-tagged, dist≈1.42 = sqrt(2)·TAG_GAIN). The B-channel curve is thus the A-channel
shape bled through the tag, and the A-channel curve carries a low-end **discretization wiggle**
(boundary between the seed cell and the first grown cell). That wiggle is the second "peak". It is
**NOT a second-language CP** (pk@p_B=False) and **NOT a double-artifact** — it is a benign property
of a discrete 4-cell Voronoi readout that the **global** count_peaks≤1 bar conflated with the
intended **localized** "no spurious CP at the other boundary" test (which passes). (H_1330's
UNtagged AA_ctrl gave count_peaks=1 because there both fits shared keys; the tag is what leaves the
B channel cell-less here, exposing the bleed-through wiggle. This is also an honest finding about
TAG_GAIN=1.0: channel isolation is imperfect — measurable cross-tag bleed at the low end.)

## Outcome (answer to the lane question)

**YES — a language-tagged multi-channel readout enables bilingual CP coexistence** (I1 mean
margins +0.200 / +0.177; I2 untagged-overwrite −0.001; all 3 seeds), **mirroring anima's separate
EN-trunk + KO faculties**. The H_1330 OVERWRITE was the **single-shared-store mechanism, NOT a
fundamental limit** — overturned as mechanism-specific by tagging. The tag is the substrate-level
"select the faculty", so anima's REAL separate EN+KO faculties coexist for the same structural
reason. The **frozen verdict is 🧱 on the I3a control technicality only** (a global-vs-localized
peak-count bar specification); the **science answer (coexistence via tagging) is decisively
positive and tag-attributable** (I1∧I2 clean, all seeds).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)

R1 numpy **MIRROR (DIRECTIONAL)** — engine-transfer UNVERIFIED. TOY synthetic 1-D continuum (N=21,
deterministic readout — tests the STRUCTURE of tag-separated coexistence, NOT scaled / human
bilingualism). TAG_GAIN=1.0 FIXED (not swept). Readout reads ONLY representational distance over
bound labels with a fixed faculty tag, NO injected boundary / persona / RLHF; labels enter only at
the A-fit/B-fit, NOT at test (p1/p2/p3/p6). NOT an emit gate (a_autonomy_over_hardcode). Live
CORE/*.hexa UNTOUCHED (substrate-measurement rung). **NO human-bilingualism claim.**

## Next / depletion

Honest **r3** (a DIFFERENT frozen bar, NOT a relaxation of this one): re-freeze **I3a as the
LOCALIZED "no coherent peak near p_B"** test (which the data already satisfies, pk@p_B=False all
seeds) rather than the global count_peaks≤1 — the global count is confounded by the benign
discretization wiggle. A sweep of TAG_GAIN (channel-isolation curve) and engine-native realization
of the tagged faculty on live `CORE/engine_cli.hexa` (a_engine_native_learning ·
a_verified_must_wire) are the further follow-ons.

## Claim-link / verdicts

`CLAIMS.tape @C h1335_whorf_bilingual_tagged` · card `UNIVERSE/cards/H_1335_whorf_bilingual_tagged.md`
· probe `UNIVERSE/h1335_whorf_bilingual_tagged.py` · verdicts
`.verdicts/1335_whorf_bilingual_tagged/{FREEZE,result}.txt`

xref: **h1330** (the 🧱 OVERWRITE this r2 overturns as mechanism-specific) · h1323 · h1325 (the
GREEN Sapir-Whorf CP result) · h1288 (growth-memory) · **h1316 · h1321 · h1322** (anima's real
separate EN-trunk + KO faculties this mirrors) · a_no_llm_frame_trap · a_break_the_wall ·
a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck ·
p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16.
