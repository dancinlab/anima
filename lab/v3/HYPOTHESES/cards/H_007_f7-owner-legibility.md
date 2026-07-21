---
id: H_007
ssot: ARCHITECTURE.json → verification-h007 (superseded by verification-h008-f7; frozen verdict record, distil FROM here)
slug: f7-owner-legibility
title: Does the owner's real message stream carry predictable, HIGH-DIMENSIONAL cross-session structure — the premise F7 (curiosity/EIG) and F5 (trajectory) both need? If cross-session lift ≤ shuffle floor OR the owner-self collapses to effective rank ~1, the owner-substrate families are REFUSED for want of a high-dimensional other to model.
domain: prediction-error-action axis (F7 living-by-not-knowing-you) + time-trajectory (F5) — the owner-interaction substrate
status: pre-register-frozen
exploration_method: H_006 terminal (F3 diary spent) + the $0 discovery of a real owner-agent transcript stream
verification_method: $0 deterministic conditional-bpb (H_005 machinery) + effective-rank gate + 5 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_007 — f7-owner-legibility

## Hypothesis

F7 ("living by not knowing you") bets the reason to speak is **measurable ignorance about a
specific external other (the owner), and a map of that ignorance is HIGH-DIMENSIONAL** (not the
1-bit collapse that killed v1). F5 (trajectory) needs the same substrate: a real owner-interaction
stream with day/session structure. Both premises are testable at $0 on the owner's actual message
history — before building any curiosity organ.

> Two quantities on the genuine-owner-message stream (chunked by session, chronological):
> **(1) legibility** = cross-session over-floor conditional-bpb lift (H_005 method: does the owner's
> past predict their future beyond generic register?); **(2) dimensionality** = participation ratio
> of the session-representation vectors (is the predictable owner-self high-dimensional, or does it
> collapse to "the owner always says X" = the v1 one-bit failure?).

Outcome: **ANCHORED** (legibility > floor AND rank > floor → a high-dimensional legible owner-self
exists; F7/F5 premise live) · **F7-REFUSED** (legibility ≤ floor → the owner stream is
unpredictable register, nothing to be curious about) · **RANK-COLLAPSE** (legible but rank ~1 → the
owner-self is 1-bit; F7's high-dimensionality claim dies = the v1 seam-h9229 failure) · **INVALID**.

## Why

- The F3 diary line is spent (H_006). The remaining `fd-true-axes` families that live on the
  owner-interaction substrate (F7 curiosity, F5 trajectory, and F8's owner-model) all presume the
  owner is a legible, high-dimensional other. Measure that premise at $0 first (the H_005/H_006
  discipline: premise before organ).
- A real owner-agent transcript stream exists on disk (`~/.claude/projects/*/*.jsonl`, ~51 MB of
  genuine owner typing across 769 sessions) — discovered 2026-07-16. The remaining axes are NOT
  compute-blocked; they are $0-checkable on this substrate.
- Escapes L11: measures a property of the STREAM (the owner), contrasts no representation arms.

## Predictions

- **P1** cross-session legibility > floor `?` (the owner's past predicts their future).
- **P2** session-representation participation ratio > 2 `?` (high-dimensional, not 1-bit).

## Variables (frozen)

- **stream**: genuine owner messages from `~/.claude/projects/*/*.jsonl` — `type=="user"`, text
  content, EXCLUDING tool_result blocks and hook/system noise (lines matching
  `^(\s*<|Caveat:|\[Request interrupted|# |Contents of|system-reminder|<command-)`). Chunked by
  session file, ordered by mtime. ≥100 sessions with ≥ W+P bytes.
- **geometry**: W=4096 tail, P=2048 prefix (H_005 verbatim).
- **estimators**: markov6 (authority) + ppm (confirm) + gzip (reported); shuffle floor; ε=0.02 bpb.
- **rank**: participation ratio of per-session byte-class feature vectors (the H_005
  `participation_ratio` on session features); floor **2.0** (strictly above the v1 one-bit seam).

## Run Protocol

- **harness**: `tool/anima_v3.py` + `state/h005…/run_h005.py` estimators.
- **run script**: `state/h007_f7-owner-legibility_2026-07-16/run_h007.py`
- **artifacts**: `.../result.json`
- **deterministic**: stdlib only, $0 (no message CONTENT is copied into the repo — only aggregate
  bpb/rank numbers; the owner's words stay on their own disk · privacy).

## Criteria

- **verdict_rule**: **ANCHORED** iff legibility over-floor > ε on the order-aware estimators AND
  participation ratio > 2.0. **F7-REFUSED** iff legibility over-floor ≤ ε. **RANK-COLLAPSE** iff
  legible but PR ≤ 2.0. Else per the triggered falsifier.

## Falsifiers (pre-registered)

- **O-1 the kill**: cross-session legibility over-floor ≤ ε on the order-aware estimators → the
  owner stream carries no predictable cross-session self → F7/F5 owner-premise **REFUSED**.
- **O-2 rank collapse (L1)**: legible but participation ratio ≤ 2.0 → the owner-self is a one-bit
  seam (the v1 seam-h9229 failure) → F7's high-dimensionality claim **DEAD**.
- **O-3 liveness**: a planted high-dimensional legible stream must read ANCHORED through the same
  instrument, else **INVALID**.
- **O-4 bounds**: session-order-shuffled stream must read legibility ≈ 0 (that is the floor).
- **O-5 estimator agreement**: markov6 and ppm sign-agree on legibility, else **PENDING(instrument)**.

## Honest Limits

- **L1** the git/transcript stream is the owner's DIRECTIVE voice (terse commands), not their full
  self; legibility here is a lower bound on a richer interaction.
- **L2** session-boundary chunking is coarse; a finer temporal grain might show more or less structure.
- **L3** a positive premise does NOT build the F7 organ — it licenses designing it (curiosity/EIG
  needs a trained owner-model, real compute); a null retires the whole owner-substrate corner at $0.
- **L4** byte-class features for the rank gate are coarse; a rank collapse on them is suggestive, a
  high rank is a lower bound on the true dimensionality.

## Cross-Links

- **architecture**: `components.F7` · `components.F5` · `components.F8` · `salvage.l1-one-bit-seam`
  · `verification-h005` · `verification-h006` · `salvage.l11-*`
- **predecessor**: `H_006` (F3 diary spent) · **method**: `H_005`/`H_006`
- **substrate**: `~/.claude/projects/*/*.jsonl` (genuine owner messages)

## Verdict

**🟡 PENDING / BORDERLINE-WEAK-POSITIVE → SUPERSEDED by H_008 (f7-owner-clean) = 🔴 REFUSED.** This
card's single-grain borderline (below) was the last open premise on the owner substrate. The clean
re-run under `H_008` — text-like liveness (the markov artifact fixed, liveness now PASSES) measured on
BOTH grains — resolves it to a kill: the owner is **high-dimensional XOR legible, never both on the
same grain** (per-session PR 2.29 but not legible; per-day legible markov3 +0.145 / markov8 +0.176 but
PR 1.75 = the v1 one-bit seam). The F7/F5/F8 owner-substrate premise is **REFUSED**, not borderline.
See `HYPOTHESES/cards/H_008_frontier-fanout.md` and `verification-h008-f7`.

_Original single-grain borderline reading retained below as the record of its time (seed-of-record);
the resolving verdict is H_008-f7._

**🟡 PENDING / BORDERLINE-WEAK-POSITIVE** (run 2026-07-16 · $0). The owner-substrate exists and is
rich, but its premise reads right at both thresholds — neither a clean anchor nor a clean kill.

### What ran

Extracted genuine owner typing from `~/.claude/projects/*/*.jsonl` (type==user text, excluding
tool_result blocks + hook/system noise) → **241 sessions ≥ 6144 B**, chunked chronologically. NO
message content was written into the repo — only aggregate numbers (privacy).

- **legibility** (markov6 over-floor, cross-session vs shuffle) = **+0.0207** — marginally above
  ε = 0.02 (essentially at the noise floor).
- **owner-self participation ratio** = **2.27** — marginally above the 2.0 one-bit floor.

### The honest reading

Both signals sit RIGHT AT their pre-registered thresholds. The owner's stream — terse directive
commands, mostly — is only marginally more predictable across sessions than a shuffled baseline, and
only marginally high-dimensional. This is a **weak positive**: the owner is a *legible, more-than-
one-bit* other, but barely — nowhere near anima's F3 signal (over-floor +0.22).

### The liveness caveat (why PENDING, not a clean verdict)

The pre-registered O-3 liveness control read negative under markov6 (−0.03), which would force INVALID.
Diagnosed as an ESTIMATOR-SPECIFIC ARTIFACT, not an owner finding: the planted-latent liveness stream
is high-entropy RANDOM bytes, and markov6's order-6 model behaves oddly on it, whereas the SAME planted
stream reads a clean +6.66 over-floor under gzip. Real text (the owner stream) is low-entropy, where
markov6 works — but the liveness control must be rebuilt TEXT-like (per-estimator) before the markov6
owner number is fully trustworthy. So the formal verdict is PENDING(instrument), not ANCHORED.

### What this establishes and what it leaves open

- **Establishes**: a real owner-interaction substrate exists on disk (~51 MB genuine typing, 241
  usable sessions) — the remaining `fd-true-axes` families (F7 curiosity, F5 trajectory, F8
  owner-model) are NOT compute-blocked; they are $0-checkable here.
- **Leaves open**: whether the owner premise is genuinely positive. The numbers lean weak-positive
  (legible, rank 2.27) but sit at the thresholds, and the markov6 liveness needs a text-like rebuild.
  A clean re-run (text-like liveness + ppm confirm + finer temporal grain) resolves it.

### Resume target

Rebuild the liveness as a TEXT-like planted stream (low-entropy, so markov6 handles it), add the ppm
confirm, and re-measure the owner premise at a finer grain (sub-session / per-day rather than
per-session-file). If it holds above threshold → F7/F5 premise LIVE, design the curiosity/trajectory
organ (needs a trained owner-model = real compute). If it collapses to the floor → the owner-substrate
corner joins the terminated pile. Recorded to ING.

_Borderline weak-positive (legibility 0.021 ≈ ε, rank 2.27 ≈ floor); markov6 liveness needs a
text-like rebuild. The owner substrate is real and $0-checkable — the premise is not yet cleanly
resolved._
