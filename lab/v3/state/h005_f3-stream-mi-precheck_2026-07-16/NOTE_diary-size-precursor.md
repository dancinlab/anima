# $0 precursor: does a k-token bottleneck capture the oracle-diary ceiling? (2026-07-16)

Prompted by Fable's D4 (is there a $0 precursor that gates the twin's compute run). Measured on
anima (the H_005-anchored stream), order-6 Markov estimator, full-day ceiling = +0.2713 bpb.

## Ceiling captured by a bounded-k diary

| diary (k bytes) | naive first-k | deduped-tokens |
|---|---|---|
| 256 B  | +0.0040 (1%)  | +0.0016 |
| 1024 B | +0.0181 (7%)  | +0.0030 |
| 4096 B | +0.0495 (18%) | −0.0316 |
| 16384 B| +0.1676 (62%) | — |

## Finding

- The day-specific signal is **distributed and subtle**: naive extractions (first-k bytes,
  deduped unique tokens) capture almost none of the +0.27 full-day ceiling at small k; deduping
  tokens actively HURTS (the signal is in structure/repetition/context, not vocabulary).
- A k-token diary is therefore viable ONLY with a **learned, non-naive extraction** — which is
  exactly F3's bet (the bottleneck decides what survives). A naive prefix reaches 62% only at 16 KB.
- **Risk for the twin**: if the bottleneck k is small and the learned extraction cannot beat naive
  by much, the diary captures little of the ceiling → F3's k-bottleneck instantiation could fail
  even though the premise (unbounded MI) is anchored. The twin must sweep k and/or use a continuous
  m, and its delta_min floor (~0.02 bpb) is small enough that a modest learned extraction clears it.

## Consequence

This does NOT gate-kill the twin (the signal exists; naive extraction is a lower bound, and the
twin's learned extraction is the point). But it sharpens the twin design: bottleneck k must not be
tiny, continuous m is safer than a few discrete tokens, and the honest kill is "learned diary ≤
no-diary + delta_min" measured against a real trained control — a training run, not a $0 proxy.
