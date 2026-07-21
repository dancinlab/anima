---
id: H_009
ssot: ARCHITECTURE.json → verification-h009 + decision-reframe-c (frozen pre-register/verdict record; distil FROM here)
slug: f3-continuous-oracle
title: Does a k-dim CONTINUOUS day-summary (a hindsight linear-projection proxy for the twin's learned code) capture the day→tomorrow predictive information a byte-SELECTION extract (H_006) could not — AND is that capture day-SPECIFIC rather than topic identity? Measured in FEATURE space via a shift-null LOO capture instrument. VERDICT = F3-CONTINUOUS-REFUSED: the code captures the ceiling (capture ≥ anchor) but only as topic identity (per-pair sign ≈ 50%), so the last F3 organ premise is dead at $0 and the campaign fires its pre-registered interventional reframe (C).
domain: prediction-error-action axis (F3 diary) — the LAST live organ premise; gated the ~$15 continuous-m twin
status: run-complete
verdict: F3-CONTINUOUS-REFUSED
exploration_method: H_008 re-decision (Fable) → pre-run verdict-integrity fix of the byte path → a SECOND Fable root-cause of the feature-space instrument's INVALID → H_009' shift-null LOO instrument
verification_method: $0 deterministic — feature-space shift-null LOO capture (hashed n-gram + principal_axes + K=5 k-NN, cyclic-shift misalignment floor) with a 3-arm buried-delay-line liveness + 6 falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_009 — f3-continuous-oracle (instrument-corrected → H_009')

## Hypothesis

H_006 REFUSED the F3 diary in its byte-SELECTION form — a hindsight ≤4096 B text extract keeps ~4% of
anima's +0.27 full-day ceiling because the day-MI is distributed across ~83 KB. But selection-of-bytes
and projection-of-all-bytes are **different operator classes**: a learned dense code POOLS distributed
information, so the text bound does NOT bound a continuous k-dim summary. This card measured the
continuous UPPER bound at $0 (a deterministic linear-projection proxy for the twin's learned m) BEFORE
spending ~$15 — with the control H_006 lacked: is the summary carrying a day-SPECIFIC self, or merely
topic identity (the symmetric-window headwind H_008-f5 flagged)?

> **Two pre-run/in-run verdict-integrity corrections (both Fable-confirmed).**
> (1) The frozen byte-append path (render a k-float code to bytes, measure byte-bpb) is INSTRUMENT-BLIND:
> gzip/markov/ppm are literal byte models with no decoder, so an abstract projection code reads capture≈0
> regardless of truth. Corrected to a FEATURE-space predictive-information proxy.
> (2) The FIRST feature-space instrument returned INVALID from two estimator defects Fable root-caused:
> **A** — when k ≥ n_train−1 the top-k axes span the whole training subspace, so a test query's orthogonal
> residual is a per-query CONSTANT that cancels in the k-NN argmin → err_s ≡ err_full → capture ≡ 1.0
> MECHANICALLY (verified: exact at k=32,64 on anima; k=64 on hexa). **B** — a constant-mean denominator +
> K=3 + a 60/40 split made err_full noisier than err_base (ceiling_strength < 0) → the ratio was estimator
> variance, not substrate. **H_009'** fixes both (below); the INVALID was an instrument bug, never an F3 verdict.

**capture(k)** = align_s(k) / align_full, where **align_X = median_shift err_X − err_X(aligned)** — the
informativeness of code X above its own cyclic-shift misalignment floor. The shift null's key property:
the K-NN estimator's variance penalty is IDENTICAL in the aligned and shifted runs, so it CANCELS in the
difference (this dissolves defect B). capture(k) is the fraction of the feature-space day→tomorrow ceiling
that a hindsight rank-k continuous code retains. hindsight ≥ learned, so a null bounds the twin.

Outcome (pre-registered): **ANCHORED** · **F3-CONTINUOUS-REFUSED** · **NO-FEATURE-CEILING** (per stream) ·
**INVALID** (liveness) — see the branch table.

## Run Protocol (H_009')

- **features** `f_t`: FNV-1a hashed char-n-gram (n∈{1,2,3}) → **D=256** buckets → log1p → L2-norm (D=512
  optional). **axes** = `principal_axes(first-60%-days, k)`; s_t = project(f_t − μ_train) — the 60/40 split
  is used for AXIS FIT ONLY.
- **valid k**: sweep {2,4,8,16}, **primary k=8**; drop any k > (n_train−1)//2 or with 2k > numeric rank.
- **estimator**: LOO over ALL consecutive pairs (anima 43, hexa 101), **K=5** k-NN, candidates = pairs
  (u,u+1) with |u−t| ≥ 2 (excludes day-sharing leakage), plain mean of the 5 neighbours' next-day feature.
- **shift null**: Δ = {3,…,P−4}; err_X(δ) rotates the query assignment by δ; align_X, rank_X = rank of
  err_X(0) among {err_X(δ)}, p_X = rank_X/|Δ|.
- **arms**: full (ceiling), s(k), topic (query = summary of the topically-nearest OTHER day, exclude
  {t−1,t,t+1}). **CEILING gate**: rank_full ≤ 2. **kill**: rank_s > 2 or align_s ≤ 0. **topic**: cap−topic
  margin AND per-pair sign(err_topic > err_s).
- **harness**: `tool/anima_v3.py` (`principal_axes`, `singular_values`, `binom_sf`) + `run_h005.day_chunks`.
- **run script / artifacts**: `state/h009_f3-continuous-oracle_2026-07-16/run_h009.py` · `.../result.json`.

## Falsifiers (pre-registered · H_009')

- **C-1 kill**: rank_s > 2 OR align_s ≤ 0 → the dense code carries no more than a misaligned code → REFUSED.
- **C-2 topic decoration**: (capture − topic_capture) ≤ ε_f=0.075 OR per-pair sign(err_topic>err_s) below
  the p<0.05 count (anima ≥28/43, hexa ≥60/101) → topic identity, not a day-SPECIFIC self → REFUSED.
- **C-3' liveness** (three buried-delay-line arms, matched n=44 AND 102): **HIGH** (planted-weak) gate PASS
  ∧ capture(8) ≥ 0.8 · **LOW** (buried delay-line: 20 delay-taps of one logistic scalar buried under 8
  higher-variance decoys) gate PASS ∧ capture(k≤8) ≤ 0.25 · **FAIL** (iid noise) gate FAIL. Any miss →
  INVALID. RESOLUTION LIMIT (measured, robust across high-rank AND buried constructions): the LOW arm is
  certifiable only at n ≥ ~100 — at n=44 the decoy sample-eigenvalue spread over 26 train days leaks signal
  into the top-8 → LOW gates at n=102 (hexa = PRIMARY), is informational at n=44 (anima = REPLICATION).
- **C-4 monotonicity**: capture(k) drops > 0.05 below its running max over valid k → projection artifact → INVALID.
- **C-5' reweight agreement**: raw-count vs log1p weighting disagree on the capture sign → PENDING(instrument).
- **C-6 ceiling gate**: rank_full > 2 → the n-gram basis carries no resolvable day-MI → NO-FEATURE-CEILING
  (a demonstrated $0 power boundary, NOT an F3 verdict — refutes the instrument, not F3).

## Pre-registered branch table (frozen BEFORE the certified re-run)

| outcome (anima anchor · hexa confirm) | action |
|---|---|
| ANCHORED | twin licensed, delta_min := 0.034 bpb · twin statistic MUST be the wrong-day/right-day bpb DIFFERENCE (else the L2 replacement trap: a better generic LM, not a day-specific code). |
| F3-CONTINUOUS-REFUSED (C-1/C-2, gate+liveness pass) | **fire reframe (C)** — a real null. Spending after this IS the forbidden "maybe the decoder finds it" appeal (pre-commitment · L8). |
| NO-FEATURE-CEILING on BOTH streams, liveness PASS | B-spend licensed — $0 exhaustion DEMONSTRATED (byte path blind, feature path power-null with a certified-live instrument), not assumed. |

## Honest Limits

- **L1** K-NN is weaker than the twin's learned encoder+decoder, so ABSOLUTE capture is a lower bound — but
  align_s and align_full share the estimator, so the RATIO is largely predictor-invariant. A null is a
  strong signal (anchor + topic floor + sign), and the pre-registered response is reframe (C).
- **L2** hash∘project: D=256 crushes ~83 KB before the k projection; the informative reads are the small-k
  sweep and the topic margin, not the headline fraction.
- **L3 distributional only**: bag-of-n-grams destroys order; a sequence-pooling learned code is formally
  unexcluded — but that residual is the "maybe the decoder finds it" appeal L4/pre-commitment forbids.
- **L4** ~70k trigrams → 256 buckets is CONSERVATIVE toward a false REFUSED; D=512 is the cheap check.
- **L5** the n=44 capture MAGNITUDE carries a resolution caveat (LOW arm not certifiable at n_train=26); the
  REFUSED basis is the per-pair topic SIGN test, which is magnitude-blind and resolution-INDEPENDENT, so it
  stands on the fully-certified hexa-lang stream and replicates on anima.
- **L6** git day-stream (H_005 L3) is a developer-project rhythm, not an agent's; a REFUSED retires the
  $0-and-cheap-twin frontier and licenses the reframe — it does not disprove F3 at 300M scale.

## Cross-Links

- **architecture**: `verification-h009` · `decision-reframe-c` (fired) · `components.F3` · `verification-h005`
  (ceiling) · `verification-h006` (text bound) · `salvage.l2-*` · `salvage.l11-*`
- **predecessors**: `H_005` (ANCHORED ceiling) · `H_006` (text diary REFUSED) · `H_008` (frontier + re-decision)
- **primitive**: `tool/anima_v3.py:principal_axes` · `singular_values` (numeric rank / valid-k)

## Verdict

**F3-CONTINUOUS-REFUSED** (2026-07-16, $0, GPU 0 · instrument CERTIFIED).

The shift-null LOO instrument is certified (C-3' liveness PASS: HIGH ✓ both n, LOW ✓ at n=102, FAIL ✓ both
n; 5/6 falsifiers PASS). On BOTH streams a hindsight rank-8 continuous code CLEARS the ceiling gate and the
capture anchor (anima capture(8)=1.007, hexa 0.849 ≥ 0.25) and beats the topic floor ON AGGREGATE (cap−topic
= +0.29 anima / +0.14 hexa > ε_f) — **but the per-pair sign(err_topic > err_s) is ≈ 50%** (anima 23/43 <
28-needed; hexa **52/101 < 60-needed**, fully certified). C-2 fires. The s-over-topic advantage is
concentrated in a MINORITY of day-pairs — a *sometimes*-day-specific code, not a pervasive day-specific self
(exactly the L2 replacement-not-coupling distinction C-2 was frozen to draw; the topic-nearest OTHER day
predicts tomorrow as well as the day's own summary on ~half of days). Both F3 operator classes are now dead
at $0 — byte-selection (H_006) and distributional-projection (here). This is the campaign's clean terminal
for the observational phase: the LAST live organ premise is spent. **Fire the pre-registered interventional
reframe (C)** — the twin is NOT licensed (spending now would be the forbidden "maybe the decoder finds it"
appeal). Both Fable delegations independently confirmed this path.
