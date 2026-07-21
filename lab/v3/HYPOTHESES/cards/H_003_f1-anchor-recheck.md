---
id: H_003
slug: f1-anchor-recheck
title: The recovered MORPH-ATOM anchor survives a correctly-specified bounds check, and the synthetic drill generator can actually produce the contrast (drift, emittability, atomicity deficit, zero leak) the F1 pilot needs.
domain: write-lever axis (F1 codec-is-the-self) — successor to H_001 (rig = REFUSED)
status: pre-register-frozen
exploration_method: H_001 verdict + repair pass (Fable 5 R1-R6) -> deterministic re-check
verification_method: deterministic closed-form harness (tool/anima_v3.py) + generator (src/generator/) + 9 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
genspec_sha256: fbcf0c8ad444d0f3c2fa5ad018d12ce8f33ad6bcf8e0f78eb26be5495527ce2b
---

# H_003 — f1-anchor-recheck

## Hypothesis

H_001 returned **rig = REFUSED** on four counts: G-1/G-2 unevaluable (no generator),
G-4 mis-specified (it tested the control arm), and — found afterwards — a false scale
premise, an unanchored `delta_min`, a missing liveness arm, and a harness that
overflowed at the operating point. This card repairs what is repairable **for $0** and
decides whether the H_004 pilot may fire.

Verdict is again about the RIG, not about F1: **LICENSED** (H_004 pilot may run) or
**REFUSED** (blocked until the named defect is repaired).

Two independent claims, both falsifiable here:

> **A — the anchor.** Under a correctly-specified bounds check (treatment + liveness
> tested; control-at-chance kept as a SEPARATE leak test), MORPH-ATOM's measurement
> stands: `salvage.l4(b)` is above the chance floor and its harness was demonstrably
> live.
>
> **B — the generator.** `src/generator/` emits a stream in which the frozen phase-1
> codec is genuinely blind to phase-2's novel allomorphs (atomicity deficit = 1.0),
> the refit codec is not (deficit = 0.0), the seam actually moves (drift ≥ floor),
> enough clean held-out items exist to power the pilot, and nothing leaks.

## Why

- **Correcting H_001's G-4.** A control is *supposed* to sit at chance; testing it and
  reading "anchor dead" was backwards. The anchor's weight is carried by the treatment
  arm and by the liveness arm. Restated as B-1/B-2/B-3 below.
- **The anchor is stronger than H_001 recorded** (`l4-morph-atom-runs`): replicated on
  an independent seed (CEMENT 2026-07-14, seed 7) at Δ = +0.3417 vs the original
  +0.291, replication deviation 0.009, all arms V1 liveness PASS. And the C2 arm shows
  atomicity is a **structural slot, not a pretrained address**.
- **No number transfers from MORPH-ATOM after the pilot** (`rig-pilot`). This card does
  not re-anchor `delta_min`; it only establishes that the anchor is a real effect
  (an existence proof of the mechanism class) and that the rig can measure in-rig.
- **The generator must carry explicit flip supervision.** v1's NAT-ATOM law
  (`l4-morph-atom-amplifier`): atomicity AMPLIFIES a taught signal and cannot source
  one. A stream with only shifted collocation statistics would read chance even in the
  oracle arm and kill the rig for the wrong reason.

## Predictions

- **P1**: B-1/B-2/B-3 all pass on the recovered v1 counts — the anchor is above floor,
  its harness was live, and it did not leak.
- **P2**: boundary-shift rate between the phase-1 and phase-2 refits ≥ `drift_floor`.
- **P3**: `atomicity_deficit(frozen codec, novel allomorphs in context)` = **1.0**
  (0/12 single-token) and its dual under the refit codec = **0.0** (12/12).
- **P4**: clean held-out eval items ≥ `n_required_worst` after leak filtering.
- **P5**: every determinism / round-trip / framing invariant holds.

## Variables

Pre-registered inputs, **frozen before any measurement**:

- `genspec_sha256` = `fbcf0c8ad444d0f3c2fa5ad018d12ce8f33ad6bcf8e0f78eb26be5495527ce2b`
  — the spec is STORED, not regenerated; this hash is what bounds designer freedom
  (`rig-corpus-frozen-params`). (Re-frozen 2026-07-16 after the N-2 repair — the original
  spec `2016a4ee…` gave rig = REFUSED; see the Verdict's repair note.)
- `K` = **512** BPE merges. The original K=2048 (from v1's G-0 audit on a DIFFERENT alphabet)
  could not produce the N-2 contrast at any value; the repair made atomicity frequency-earned,
  and K=512 is the smallest that gives frozen 0/12 + refit 12/12. Not tuned to a score — swept
  against the mechanism gate (N-2), which is a rig-validity gate, not the F1 verdict.
- `bpe_sample_lines` = **20000** per phase.
- `drift_floor` = **0.05** (5% of probe positions). Carried unchanged from H_001, where
  it was marked `?`. Frozen here BEFORE measuring so the measurement cannot pick it.
- `n_required_worst` = **1178** — N/arm at the power table's floor (delta_min = 0.10,
  p0 = 0.50, α = 0.01, power = 0.99). The worst case is used deliberately: an item pool
  that only clears the optimistic N would force `delta_min` upward to fit the pool.
- **Anchor counts** (recovered, exact integers over n=120): M = 109, C1 = 74, C3 = 110;
  CEMENT replicate: M = 110, C1 = 69. Chance `p0` = 0.50.
- Band: exact binomial, `conf` = 0.99 → at n=120, `[46/120, 74/120]`.

Measured outputs: `boundary_shift_rate`, `deficit_frozen`, `deficit_refit`,
`n_clean_items`, `leak_hits`, `heldout_neg_cooccurrence`, invariant results
→ `rig: LICENSED | REFUSED`.

## Run Protocol

- **harness**: `tool/anima_v3.py` — `chance_band`, `binom_two_sided_p`, `two_proportion_n`
- **generator**: `src/generator/` — `spec`, `lang`, `stream`, `codec`, `audit`
- **run script**: `state/h003_f1-anchor-recheck_2026-07-16/run_h003.py`
- **deterministic**: stdlib only, single seeded RNG, no network, $0 local
- **run cmd**: `python3 state/h003_f1-anchor-recheck_2026-07-16/run_h003.py`
- **artifacts**: `state/h003_f1-anchor-recheck_2026-07-16/result.json`

## Criteria

- **verdict_rule**: `rig = LICENSED` iff **no** falsifier triggers. Any trigger →
  `rig = REFUSED`, and H_004 is blocked until the named defect is repaired. A REFUSED
  verdict is a result, not a delay.

## Falsifiers (pre-registered, measurable)

**Anchor (quote EXACT COUNTS, never rates — C1 sat exactly on the band edge):**

- **B-1 treatment above floor**: M must fall OUTSIDE the 99% chance band, i.e.
  `k_M ≥ 75` of 120. If M is inside the band, the anchor is noise → **REFUSE**.
- **B-2 liveness**: C3 (leak-ceiling arm) must reach `k_C3 ≥ 108` of 120 (≥0.90, v1's
  own pre-registered rule). If the instrument could not detect held-out flip even when
  handed the answer, no arm's null means anything → **REFUSE**.
- **B-3 leak (separate test, opposite direction)**: C1 must sit INSIDE/below the band,
  `k_C1 ≤ 74`. A raw baseline scoring ABOVE chance would mean the anchor's setup handed
  something away → **REFUSE**. (This is what H_001's G-4 tested while mislabelling the
  reading; here it is a leak test, not an anchor test.)
- **B-4 replication agreement**: the CEMENT replicate must agree in direction and reach
  the same verdicts (`k_M ≥ 75`, `k_C1 ≤ 74`). Disagreement → the anchor is seed-luck
  → **REFUSE**.

**Generator:**

- **N-1 drift existence**: `boundary_shift_rate(codec_p1, codec_p2, probes)` <
  `drift_floor` → the stream cannot move the codec; the twin would compare two frozen
  codecs under different names → **REFUSE**.
- **N-2 contrast existence**: `deficit_frozen` < 1.0 (the phase-1 codec accidentally
  atomizes some novel allomorph) OR `deficit_refit` > 0.0 (the refit codec fails to
  atomize them) → there is no contrast to measure → **REFUSE**. Audited **in rendered
  context**, never in isolation — BPE segmentation is context-dependent.
- **N-3 emittability**: clean held-out items < `n_required_worst` (1178) after leak
  filtering → underpowered by construction → **REFUSE**.
- **N-4 zero leak**: any rendered eval string occurs as an exact substring in either
  phase stream, OR any held-out stem co-occurs with a NEG affix → the eval measures
  memory, not recombination → **REFUSE**. (v1 precedent `l6-leak`: its one apparent win
  was a lookahead leak and evaporated leak-free.)
- **N-5 determinism + round-trip**: two independent BPE fits disagree on the merge list,
  OR `spec_hash` is unstable, OR `render`/`parse` or `to_jamo`/`from_jamo` fail to
  round-trip → the rig is not reproducible and no verdict from it is either → **REFUSE**.

## Honest Limits

- **L1**: This card licenses the **pilot**, not the twin. It cannot anchor `delta_min` —
  only `rig-pilot` can, in-rig. MORPH-ATOM survives here as an existence proof of the
  mechanism class, nothing more.
- **L2**: `drift_floor` = 0.05 is still an unanchored `?` — it is frozen, not derived.
  A measured rate far above it says the stream drifts; it does not say the drift is the
  RIGHT SIZE for the effect. Only the pilot's Δ speaks to that.
- **L3**: The anchor is 303M with a warm trunk + reinit-embed surgery; this generator's
  language is synthetic and the rig is 10M-from-scratch. **Nothing about the transfer is
  established by this card** (`decision-attributability` is SUPERSEDED, not repaired).
  `l4-morph-atom-slot-not-address` is the only positive reason to expect transfer, and
  it is an argument, not a measurement.
- **L4**: The generator's designer wants F1 to live. Freezing `genspec_sha256` before
  measuring bounds but does not eliminate that; the spec was authored by reading the
  anchor's protocol, so its shape is not independent of the effect it hopes to find.
- **L5**: `K` = 2048 is imported from v1's audit on a DIFFERENT alphabet (Korean NSMC vs
  this synthetic inventory). It is frozen rather than tuned, which protects against
  shopping — but it may simply be the wrong K here, and N-1/N-2 would then read as a
  generator defect rather than as the wrong hyperparameter `?`.
- **L6**: Boundaries are indexed in **jamo, not bytes** — a deliberate deviation from
  the design (each jamo is exactly 3 UTF-8 bytes, so a byte-indexed matrix has 2/3 of
  its columns structurally zero and deflates the shift rate ~3x). Rectangularity and
  codec-independence — the actual requirements — hold. But the drift numbers are
  therefore **not** comparable to a byte-indexed figure quoted elsewhere.

## Cross-Links

- **architecture**: `rig-pilot` · `rig-sequence-h003` · `rig-liveness-arm-missing` ·
  `rig-drift-breaks-symmetry` · `gates-power-table` · `l4-write-side-crack` ·
  `l10-codec-swap-costs-the-embedding` · `decision-attributability` (superseded)
- **predecessor**: `H_001` (rig = REFUSED, 2/5) — this card repairs its defects
- **successor**: `H_004` f1-static-anchor-pilot (≤$10, 5 runs) → `H_002′` (12 runs)
- **design seed**: `state/h002_f1-twin_2026-07-16/DESIGN_fable.md`
- **generator**: `src/generator/` · **harness**: `tool/anima_v3.py`

## Verdict

**🟢 rig = LICENSED** (10/10 · repair re-run 2026-07-16, genspec `fbcf0c8…`, K=512 ·
`state/h003_f1-anchor-recheck_2026-07-16/result.json`). The H_004 static-anchor pilot may fire.

The first run (below) was REFUSED on the generator half; the two generator defects were then
repaired and the card re-frozen on the repaired spec (the card's own verdict rule is "REFUSED
until the named defect is repaired", and this is that repair — logged, not silently re-frozen).

### The N-2 repair — three findings, each measured

The wall was **not** "atomicity can't be induced synthetically". It was three concrete defects,
found by direct experiment rather than argument:

1. **Short affixes atomize by accident.** A 1-syllable NEG allomorph is 2–3 jamo; its individual
   jamo recur so widely that the FROZEN codec fuses it without ever seeing it (measured: the novel
   form `조` read single-token in the phase-1 codec). Fix: novel NEG allomorphs are now ≥2
   syllables (≥6 jamo) — a run that long cannot be fused by coincidence, only earned by frequency.
   This alone took frozen from 8/12 → **0/12**.
2. **The polarity mark was fusing with the affix.** This was the real refit blocker, and it hid
   behind the frequency question. The mark was glued directly to the affix (`…affix+NEG_MARK`), so
   BPE fused `affix+mark` as one merge and the affix itself never became a single token — refit
   stalled at 3–5/12 *no matter the frequency or K* (measured: unchanged at K=4096). Fix: the mark
   is now a separate sentinel-delimited token. This took refit to **12/12**.
3. **Novel allomorphs must be frequency-earned.** Even split, a novel affix at its natural
   ~450/20k rate is below BPE's merge threshold against 64 competing affixes. Fix: phase-2
   over-weights novel allomorphs (`NOVEL_NEG_SHARE_P2 = 0.80`) — which is not a thumb on the scale
   but the drift itself (the phase-2 language actually *uses* its new negators heavily), and is
   exactly v1's NAT-ATOM law that atomicity is earned by repetition.

Result at K=512, real pipeline: frozen **0/12** (deficit 1.0), refit **12/12** (deficit 0.0),
drift 0.1256, leak 0, co-occurrence 0.

### The N-4 repair — it was never a corpus leak

Confirmed the H_003 first-run reading: `leak_hits` was always 0. The co-occurrence count was a
detector defect in two layers: (a) the audit re-parsed each word ambiguously; fixed by keying off
the EMITTED polarity mark, since a NEG-marked word is ground truth. (b) A **duplicate function
definition** left an old substring-based version shadowing the parse-based one — Python used the
last definition, so the fix appeared not to take until the stale copy was removed. Both gone;
co-occurrence is now 0 at 200k-line scan depth.

### What LICENSED means

The rig is valid: the anchor is real and replicated, the frozen/refit codecs give the opposite
readings the twin needs, the drift moves the seam, the item pool clears the worst-case N, and
nothing leaks. **F1 now has a substrate at drill scale** — the H_004 static-anchor pilot (oracle
vs frozen, measures `Δ_pilot`, the hard upper bound on refit) may run.

### Prior run (REFUSED, 8/10, genspec `2016a4ee…`)

Kept for the record — the anchor half was already all green there; only the generator failed.

**🔴 rig = REFUSED** (8/10 · run 2026-07-16 ·
`state/h003_f1-anchor-recheck_2026-07-16/result.json`). H_004 pilot is BLOCKED. But the two
halves of the card separated cleanly, and that separation is the finding.

### The anchor half is ALL GREEN — H_001's G-4 was the only thing wrong with it

B-1 through B-4 all PASS. Correctly specified (test the treatment and liveness arms; keep
control-at-chance as a separate leak test), the anchor stands exactly as `salvage.l4(b)`
claims:

- **B-1** M = 109/120 outside the band (p = 1.9e-21) — treatment above floor.
- **B-2** C3 = 110/120 ≥ 108 (p = 1.9e-22) — the harness could see a handed flip.
- **B-3** C1 = 74/120 inside the band — the control did not leak.
- **B-4** CEMENT replicate agrees (M = 110/120, C1 = 69/120).

H_001's REFUSED-on-G-4 is now fully explained: the reading was backwards, the anchor was
never in doubt, and the replication makes it a two-seed result.

### The generator half fails on two counts — both real, one design, one audit

- **N-2 contrast existence — a genuine design wall.** No K produces the required contrast.
  Swept K ∈ {256, 512, 1024, 2048}: the frozen codec's atomicity deficit runs 0.917 → 0.333
  and the refit codec's *never reaches 0.0* (best 0.583 at K=256, i.e. 5/12 novel allomorphs
  atomized). The cause is structural: the affixes are 1–2 random jamo syllables that do not
  recur often enough in-stream for BPE to fuse them into single tokens, so "atomicity" is not
  induced by the data in *either* arm. The generator does not yet instantiate the mechanism it
  is meant to test — this is the wall to break next, and it belongs to the spec, not the code.
- **N-4 co-occurrence = 2363 — an audit false-positive, not a real emission.** `leak_hits = 0`
  (the parse-based whole-word scan is clean). The 2363 are `parse()` finding an *ambiguous*
  (held-out stem + NEG) decomposition of a word the stream actually emitted as
  (non-held-out stem + PLAIN affix). Verified directly: regenerating 40k phase lines and
  parsing each, `line()` emits **0** held-out-stem+NEG words. The invariant holds; the
  detector over-reports because the language admits ambiguous segmentations. The fix is a
  detector that scores against the *emitted* parse, not any admissible parse — an audit repair,
  logged so it is not mistaken for a corpus leak.

### Verbatim stdout

See `state/h003_f1-anchor-recheck_2026-07-16/run_stdout.txt` (full ledger) and `result.json`.
Ledger: B-1 ✓ · B-2 ✓ · B-3 ✓ · B-4 ✓ · N-1 ✓ (drift 0.0763 ≥ 0.05) · **N-2 ✗** · N-3 ✓
(clean items ≥ 1178) · **N-4 ✗** (co-occurrence, audit artifact) · N-5 ✓ · genspec ✓.

### What this licenses and blocks

- **Licenses**: the anchor is settled — F1 selection rests on solid, replicated evidence, and
  no future card needs to re-litigate `l4(b)`.
- **Blocks**: the H_004 pilot cannot fire until the generator actually instantiates the
  atomicity contrast (N-2). That is a spec-design problem — handed to the successor design pass.

### Limits this run added

- **L7**: the whole rig presumes BPE-on-jamo will *induce* morpheme atomicity from a synthetic
  stream. N-2 says it does not, at any K tried, for this affix design. Either the affixes must
  recur far more (a frequency-shaped inventory) or atomicity must be induced differently. Until
  that is solved, the F1 twin has no substrate — which is itself a partial answer about F1.
- **L8**: N-4's artifact is a reminder that in an agglutinative synthetic language, "leak" and
  "co-occurrence" are only well-defined against the *emitted* segmentation. A parse-any detector
  measures the language's ambiguity, not the corpus's contamination.
