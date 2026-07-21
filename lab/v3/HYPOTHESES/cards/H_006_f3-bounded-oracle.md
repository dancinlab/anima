---
id: H_006
slug: f3-bounded-oracle
title: Does a k-BOUNDED hindsight extract of day t retain the (unbounded) oracle-diary ceiling H_005 anchored? If ceiling(k≤4096B) ≤ shuffle floor on both anchored streams, the bottlenecked-diary premise is REFUSED and the F3 twin is cancelled at $0. The winning extracts become the twin's oracle-select inputs.
domain: prediction-error-action axis (F3) — gates the F3 diary twin (H_007) before any training spend
status: pre-register-frozen
exploration_method: H_005 ANCHORED + Fable F3-twin design D4 (a $0 precursor that gates the compute)
verification_method: $0 deterministic conditional-bpb estimators (H_005 machinery) + top-lines hindsight extraction + 5 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_006 — f3-bounded-oracle

## Hypothesis

H_005 anchored the UNBOUNDED oracle-diary ceiling (full day t as summary). Its own limit L1: a
k-BOUNDED extract might not retain it. Before training a model to LEARN extraction (the twin H_007,
which needs real compute), measure whether HINDSIGHT extraction at budget k can capture the ceiling
at all — the $0 precursor that gates the spend.

> **ceiling(k)** = bpb(P | tail) − bpb(P | tail + hindsight-top-lines-of-day-t up to k bytes),
> measured against the H_005 shuffle floor. If a hindsight-optimal k-bounded extract cannot beat
> the floor, no LEARNED k-token diary will (hindsight ≥ learned) → the bottleneck is doomed.

A $0 pre-check already found (`NOTE_diary-size-precursor.md`): naive first-k extraction captures
only 7%/18%/62% of anima's +0.27 ceiling at 1K/4K/16K bytes, and deduped-tokens HURTS. So the
signal is distributed and needs SMART extraction — this card measures the hindsight upper bound.

Outcome: **ANCHORED** (ceiling(k) > floor on an anchored stream for some k ≤ 4096 → bounded diary
viable, twin licensed, extracts emitted) · **F3-BOUNDED-REFUSED** (ceiling(4096) ≤ floor + ε on
both anchored streams → MI incompressible below context scale → twin cancelled, $0 spent) ·
**INVALID** (blind instrument).

## Why

- Institutionalizes L11 Corollary B and H_005 L1: measure the bounded ceiling BEFORE the training
  spend. Kills the twin for $0 if the bottleneck is doomed.
- Artifact chaining: the winning extracts are written to `state/h006…/extracts/` and are LITERALLY
  the ORACLE-SELECT arm inputs of H_007 — the precursor builds the twin's ceiling arm.
- Hindsight top-lines is a LOWER BOUND on the true bounded oracle (greedy ≤ optimal), so a positive
  is decisive (existence proof); a null is suggestive (could be the greedy selector's fault), in
  which case the twin's own oracle arm becomes the decider.

## Predictions

- **P1** ceiling(4096) > floor on ≥1 anchored stream (anima/hexa-lang) `?`.
- **P2** ceiling(k) increases with k (more budget captures more) `?`.
- **P3** the planted-latent liveness stream recovers ~its full ceiling at k ≥ block size.

## Variables (frozen)

- **streams**: anima (verdict-bearing, the H_005 strict anchor), hexa-lang (confirm). sidecar
  EXCLUDED (21 days, under-powered in H_005).
- **geometry**: W=4096, P=2048 (H_005 verbatim, for comparability).
- **budgets** k ∈ {64, 256, 1024, 4096} bytes.
- **extraction**: score each line of `day_t[:-W]` by its marginal lift (bpb reduction when appended
  to the tail), rank descending, take top lines up to k bytes. Selection estimator = gzip (fast);
  ceiling measured with markov6 (order-aware, the H_005 authority) + ppm confirm.
- **shuffle floor**: H_005's adjacency-breaking permutation; ε = 0.02 bpb.

## Run Protocol

- **harness**: `tool/anima_v3.py`; reuses `state/h005…/run_h005.py` (`day_chunks`, `cond_bpb`,
  `cond_bpb_ppm`, `cond_bpb_markov`, `_shuffle`, `planted_latent_stream`).
- **run script**: `state/h006_f3-bounded-oracle_2026-07-16/run_h006.py`
- **artifacts**: `.../result.json` + `.../extracts/<stream>_<day>.txt` (the twin's oracle inputs)
- **deterministic**: stdlib only, $0.

## Criteria

- **verdict_rule**: **ANCHORED** iff liveness PASS AND ceiling(k) − floor > ε on ≥1 anchored stream
  for some k ≤ 4096, on the order-aware estimator (markov6), ppm-confirmed. **F3-BOUNDED-REFUSED**
  iff ceiling(4096) − floor ≤ ε on BOTH anchored streams. Else per the triggered falsifier.

## Falsifiers (pre-registered)

- **B-1 the kill**: ceiling(4096) − floor ≤ ε on BOTH anchored streams → bounded-diary premise
  REFUSED → the F3 twin is cancelled ($0 saved; F3's k-bottleneck instantiation is dead even though
  the unbounded MI is real).
- **B-2 liveness**: the planted-latent stream must recover ≥ 5ε ceiling at k ≥ its block size, else
  the extractor/instrument is blind → **INVALID**.
- **B-3 monotonicity bounds**: ceiling(k) must be non-decreasing in k within noise; a large ceiling
  at tiny k with none at large k → selection artifact → **INVALID**.
- **B-4 estimator agreement**: markov6 and ppm must sign-agree on ceiling(4096) − floor on the
  verdict stream, else **PENDING(instrument)**.
- **B-5 leak**: no top-line extract may occur verbatim in the P prefix it helps predict (that would
  be copying, not compression) → drop + report; systematic → **INVALID** (`l6-leak`).

## Honest Limits

- **L1** top-lines greedy is a LOWER bound on the bounded oracle; a null is suggestive, not decisive
  (the twin's learned/oracle arms are the final decider). A positive is decisive.
- **L2** the git-stream proxy limit inherited from H_005 (a developer-project system, not an agent).
- **L3** line-granular extraction is coarser than a token-granular diary; a real diary could do
  better, so this is conservative for the kill.

## Cross-Links

- **architecture**: `components.F3` · `verification-h005` · `salvage.l11-*` · `l6`
- **predecessor**: `H_005` (ANCHORED) · **successor**: `H_007` f3-diary-twin (needs MPS, $0 cash)
- **precursor note**: `state/h005…/NOTE_diary-size-precursor.md`
- **design seed**: F3-twin design (Fable) — to be saved under `state/h006…/`

## Verdict

**🔴 F3-BOUNDED-REFUSED (text/token diary) — twin CANCELLED at $0** (run 2026-07-16 ·
`state/h006_f3-bounded-oracle_2026-07-16/result.json`). The pre-registered kill B-1 triggered on
both anchored streams. The precursor did its job — it killed the ~12h training twin before it cost
anything.

### What ran

Per day-pair, each line of day t (beyond the tail) was scored by its marginal gzip lift, the top
lines up to budget k were taken (hindsight-optimal per-line selection), and ceiling(k) was measured
with markov6 (ppm confirm) against the H_005 shuffle floor. Line-structured planted-latent liveness
PASSED (0.366 at k≥1024). 144 extracts emitted.

| k (bytes) | anima markov6 over-floor | anima ppm | reading |
|---|---|---|---|
| 64 | +0.000 | +0.000 | nothing |
| 256 | +0.0005 | +0.011 | ~0 |
| 1024 | +0.003 | +0.004 | ~0 |
| 4096 | **+0.012** | **+0.019** | below ε = 0.02 |

hexa-lang is likewise below ε (markov6 −0.009, ppm +0.026 — disagree). The full-day (unbounded)
ceiling was **+0.27** (H_005); a hindsight 4096-byte extract retains **~4%** of it.

### The finding

The day-specific MI is **distributed across the whole day (median 83 KB), not localizable to a small
extract** — 5% of the day's bytes captures ~4% of the ceiling (roughly linear, i.e. uniform, not
concentrated). A hindsight top-lines selector — a LOWER bound on any bounded diary — captures almost
nothing at k ≤ 4096. Per the pre-registered B-1, the bottlenecked-diary premise is REFUSED and the
F3 twin (H_007) is CANCELLED. $0 spent instead of ~12 h of training.

### Honest scope — what this does and does not kill

- **KILLS**: F3's PRIMARY formulation — a k-TOKEN readable-text diary (`F3.how`: "m is
  hard-bottlenecked to k tokens"). A readable diary of ≤4 KB of the day's own text carries
  essentially none of the day-specific self. This is the diary as F3 literally proposed it.
- **DOES NOT cleanly kill**: a CONTINUOUS learned bottleneck (`F3.how`'s parenthetical "or a k-dim
  vector" — Fable's twin used 8×256 continuous m). A learned continuous encoding is a HIGHER bound
  than text extraction and is not directly measured here. BUT the distributed-MI finding is a real
  headwind: if the signal is genuinely uniform across 83 KB, a small continuous bottleneck faces the
  same compression wall, and Fable's twin-as-designed is undermined anyway — its ORACLE arm was the
  text extracts, now shown near-floor, so it could not have anchored a meaningful delta_min.
- **Card L1 honesty**: greedy top-lines is a lower bound, so a learned text diary is a slightly
  higher bound. But the margin needed (0.012 → a real effect ≫ 0.02) is large, and the burden of
  proof has shifted heavily against the bounded diary.

### Consequence for the campaign

The F3 DIARY line, in both its readable-token form (refuted) and its twin-as-designed form
(oracle arm near-floor), is **spent at $0** — the third campaign line terminated by cheap structural
analysis (after F1's terminal and the write-lever axis). The remaining live residue is narrow: a
high-capacity continuous bottleneck that beats a distributed-MI wall, which no cheap test can settle
and which faces a documented headwind. The honest next move is a campaign re-decision, not another
F3 rig.

### Verbatim stdout

See `state/h006_f3-bounded-oracle_2026-07-16/result.json` (all k, both streams, both estimators,
liveness, ledger).

_F3-BOUNDED-REFUSED: the k-token text diary is dead at $0; the twin is cancelled; the continuous-m
residue faces the distributed-MI headwind. Campaign re-decision is the live frontier._
