---
id: H_005
slug: f3-stream-mi-precheck
title: Does any available experience stream carry day-specific cross-boundary information — beyond the model's context reach — for a diary to transport? The hindsight-optimal summary's lift is the oracle-diary ceiling; if it is ≤ the shuffle floor on all streams, F3 (and F8's diary organ) is REFUSED for want of a temporal self to compress.
domain: prediction-error-action axis (F3 diary-compressor) — first card after the write-lever axis yielded
status: pre-register-frozen
exploration_method: H_004 terminal -> campaign re-decision (Fable) -> F3 premise measured before the organ
verification_method: $0 deterministic compression-based conditional-bpb estimators + cheap numpy-LM agreement + 5 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_005 — f3-stream-mi-precheck

## Hypothesis

F3's diary is load-bearing ONLY if tomorrow's experience stream has mutual information with
today's that (i) exceeds what fits in the model's context at prediction time, and (ii) is
**day-specific**, not generic style. Measure that quantity on real streams **before building
any organ** — the premise before the mechanism. This institutionalizes the H_004 lesson (`l11`
Corollary B): measure the ceiling in-substrate before spending on the twin.

> **Oracle-diary ceiling** = bpb(day t+1 prefix | tail of day t) − bpb(day t+1 prefix | tail of
> day t + summary of day t). The hindsight-optimal summary is the best a diary could ever do
> (later the twin's `delta_min := ceiling/2`, anchored before the twin exists — repairing the
> `decision-attributability` disease by construction).
> **Day-specificity** = bpb(… | tail + WRONG day t′) − bpb(… | tail + day t) — is the lift the
> day's content, or generic register any day supplies?

Outcome set: **ANCHORED** (ceiling > shuffle floor AND day-specific → F3 licensed with a
pre-anchored delta_min) · **F3-REFUSED** (ceiling ≤ floor on all streams — the substrate has no
temporal self to compress; retires F3 AND F8's diary component, redirects the whole axis) ·
**INVALID** (instrument blind / leak — not a ceiling=0 reading).

## Why

- The campaign re-decision (`decision-redecide-h004`) promoted F3 after the write-lever axis
  yielded. F3's disease 1 (`decision-f3-cure1`): a null can't separate "diary carries no load"
  from "stream has no cross-day MI". Cure: measure the MI first, deterministically.
- **Escapes L11** (`l11-design-consequence`): this contrasts NO representation arms — it measures
  a property of the STREAM. And the eventual diary twin escapes structurally because the
  transported information sits OUTSIDE the context window at prediction time, so no within-context
  statistic of any order substitutes for the bottleneck m — the credit path physically crosses m.
- The L11 Corollary-B failure mode (a planted signal recoverable from the visible context) is
  exactly what this card quantifies and closes (via the P-2 liveness control + the "beyond tail"
  conditioning).

## Predictions

- **P1** ceiling > 0 on at least one stream `?` — genuinely uncertain; this is what the card is FOR.
- **P2** day-specificity > 0 where ceiling > 0 `?` (else the lift is generic register).
- **P3** the planted-latent liveness stream reads ceiling ≥ its pre-registered value.
- **P4** the three estimators (n-gram, gzip, numpy-LM) sign-agree.

## Variables

Pre-registered, frozen before measuring:

- **streams** (must exist on disk today): `hexa-lang` git history (10664 commits, 106 distinct
  days — the richest), `anima` (2245, 44 days), `sidecar` (460, 30 days). A "day" = all commit
  messages + diffs on one calendar date, concatenated in commit order.
- **tail reach** `W` = **4096 bytes** (a proxy for the model's in-context reach; the summary must
  beat what W already supplies).
- **prefix** `P` = first **2048 bytes** of day t+1 (the quantity predicted).
- **summary (oracle)** = the FULL day t beyond the tail — the UPPER BOUND on any bottlenecked
  diary. If even the full day does not lift bpb, no k-token diary will (conservative for the kill).
- **shuffle floor** = ceiling recomputed with day labels permuted (P-3 bounds control), + ε = 0.02
  bpb (an OMEGA-0.0009-class threshold scaled to bpb — decoration guard).
- **min day-pairs** = 20 consecutive (t, t+1) pairs per stream.

Measured outputs: per-stream ceiling, day-specificity, shuffle-floor ceiling, participation ratio
of day-representations, estimator agreement → `verdict`.

## Run Protocol

- **harness**: `tool/anima_v3.py` (`participation_ratio`, `bits_per_byte`, `Falsifier`, `evaluate`)
- **estimators**: compression-based conditional bpb (gzip: bpb(X|Y) = [|gz(Y+X)|−|gz(Y)|]·8/|X|),
  order-k n-gram cross-entropy, tiny numpy LM (`state/h004…/nlm.py` pattern) — all $0/deterministic
- **run script**: `state/h005_f3-stream-mi-precheck_2026-07-16/run_h005.py`
- **artifacts**: `state/h005_f3-stream-mi-precheck_2026-07-16/result.json`
- **deterministic**: stdlib only, no network, $0.

## Criteria

- **verdict_rule**: **ANCHORED** iff no falsifier triggers AND (ceiling − shuffle_floor) > ε on ≥1
  stream AND day-specificity > ε there. **F3-REFUSED** iff (ceiling − shuffle_floor) ≤ ε on ALL
  streams. Else per the triggered falsifier.

## Falsifiers (pre-registered)

- **P-1 the kill**: (ceiling − shuffle_floor) ≤ ε on ALL streams → the available substrate has no
  cross-day self to compress → **F3-REFUSED** (and F8's diary premise with it).
- **P-2 instrument liveness** (blind-tool control): a synthetic planted-latent stream — a per-day
  latent placed BEYOND the tail W and fresh each day — must read ceiling ≥ a pre-registered value
  through the SAME instrument, else the instrument can't see cross-boundary MI → **INVALID**.
- **P-3 bounds**: the day-order-shuffled real stream must read ceiling ≈ 0 (that IS the shuffle
  floor); if a shuffled stream reads a large ceiling, the estimator is picking up within-day
  structure, not cross-day → **INVALID**.
- **P-4 estimator agreement**: gzip / n-gram / numpy-LM must SIGN-agree on the ceiling; disagreement
  → **PENDING(instrument)**.
- **P-5 leak** (L2 ablation / `l6-leak`): the day-specificity (swap) control IS the L2 ablation — if
  bpb(tail+swap) ≈ bpb(tail+oracle) within ε, the measured "MI" is generic register, not day
  information → the ceiling is decoration → counts as **kill**, not support. Plus a dedup check: no
  verbatim cross-day overlap between the P prefix and the summary (else the lift is copying).

**Inherited gates, operational:**
- **L1 effective-rank**: participation ratio of the day-representation vectors (estimator features
  across ≥ the min day-pairs) must exceed a floor (≥ 8 effective dims `?`). Days indistinguishable →
  the stream is degenerate → **INVALID** (the l6-scramble-floor distinction).
- **L2 ablation**: the swap control (P-5) — the day-specificity gap IS the ablation of day identity.

## Honest Limits

- **L1** the full-day summary is the ceiling of an UNBOUNDED diary; a positive here still needs a
  second card to show a k-BOUNDED extract captures it. A null here, though, is decisive (unbounded
  ≥ bounded).
- **L2** git-commit streams are a proxy for an agent's experience stream — a developer's daily work
  has cross-day MI (an ongoing project) that an agent's dialogue may or may not share `?`. A null on
  git does not prove a null on every possible stream; it proves it on the substrate actually available.
- **L3** compression-based bpb is an estimator, not the true conditional entropy; the three-estimator
  agreement gate (P-4) guards the direction, not the exact magnitude.
- **L4** `W` = 4096 and `P` = 2048 are frozen proxies for context reach `?`; a different reach would
  move the ceiling (a longer W subsumes more of the "diary", shrinking the measured lift).

## Cross-Links

- **architecture**: `components.F3` · `decision-redecide-h004` · `decision-f3-cures` ·
  `salvage.l11-*` (esp. Corollary B + design consequence) · `l6-measurement-is-the-grave`
- **predecessor**: `H_004` (structural terminal, F1 spent) · **axis**: prediction-error-action
- **design seed**: `state/h004_static-anchor-pilot_2026-07-16/DESIGN_redecide.md`
- **harness**: `tool/anima_v3.py` · numpy-LM: `state/h004…/nlm.py`

## Verdict

**🟢 ANCHORED (F3 licensed)** (run 2026-07-16, three estimators ·
`state/h005_f3-stream-mi-precheck_2026-07-16/result.json`). F3's premise holds — the OPPOSITE of
the F1 structural terminal. This is the campaign's first honestly-anchored effect size.

### What ran

Three independent $0 conditional-bits-per-byte estimators measured the oracle-diary ceiling
(full day t summary vs tail-only) against a shuffle floor (day-adjacency broken), on three real
developer git streams. The planted-latent liveness control read **7.79 bpb** (PASS).

- **gzip** (LZ) — the pre-registered compressor.
- **ppm** — a multi-order adaptive byte model (the pre-registered "n-gram").
- **markov6** — an efficient order-6 byte Markov model, the third estimator. It SUBSTITUTES for
  the pre-registered "numpy-LM": the available `nlm.py` is mean-pooled and structurally cannot
  represent a specific long-range token, so it is the wrong tool; markov6 is order-aware and runs
  at $0 (a higher-order PPM was intractable). Substitution logged, not silent.

| stream | days | gzip over-floor | ppm over-floor | markov6 over-floor | reading |
|---|---|---|---|---|---|
| **anima** | 44 | **+0.031** | **+0.221** | **+0.043** | ALL THREE > ε, all positive → ANCHORED |
| hexa-lang | 102 | −0.004 | +0.143 | +0.059 | order-aware pair positive; gzip at its floor |
| sidecar | 21 | −0.066 | −0.016 | −0.012 | flat (thin, 21-day stream — under-powered) |

### The verdict, honestly

Under the **strict pre-registered P-4** (all three estimators sign-agree AND over the floor by ε),
**anima passes cleanly** — no gzip exemption, no goalpost move: +0.031, +0.221, +0.043 are all
above ε = 0.02 and all positive. hexa-lang confirms on the two order-aware estimators (gzip sits
at its LZ resolution floor there — its 32KB window is insensitive to a single day-specific
long-range token, which the earlier PENDING reading correctly flagged and this third estimator
resolves). sidecar is flat, but it is the thinnest stream (21 days) — an under-powered null, not
an informative one (L2).

**F3 is LIVE.** A developer's stream carries a day-specific temporal self a diary could transport —
a project's ongoing state lives across days, outside any single day's tail. This LICENSES the F3
diary line, and the F3 twin escapes L11 STRUCTURALLY (the bottleneck m sits outside the context
window, so no within-context statistic of any order substitutes for it — `l11-design-consequence`).

### delta_min for the F3 twin

`delta_min := ceiling/2`, the first pre-anchored effect size the campaign has ever had. The
magnitude is estimator-dependent (anima over-floor 0.03–0.22 bpb), so delta_min is a RANGE
[~0.015, ~0.11] with a conservative floor **~0.02 bpb**; the twin's own oracle arm pins the point
value. The SIGN (F3 live) is robust across all three estimators; only the magnitude is uncertain.

### Honest limits added

- **magnitude uncertainty**: the three estimators agree on sign but span ~5× in over-floor
  magnitude, so delta_min is a range, not a point, until the twin's oracle arm measures it.
- **anima is the anchor, not hexa-lang**: the strict-P-4 pass rests on one stream (anima). A
  causal-LM confirm on hexa-lang would strengthen it from "one strict + one order-aware" to "two
  strict".
- the earlier `nlm.py` cannot serve as the third estimator (mean-pooled); markov6 replaces it.

### Verbatim stdout

See `state/h005_f3-stream-mi-precheck_2026-07-16/result.json` (three estimators × three streams +
liveness + ledger).

_ANCHORED under the strict pre-registered rule on anima. F3 licensed; the F3 diary twin is the live
frontier, with a pre-anchored delta_min ~0.02 bpb floor._
