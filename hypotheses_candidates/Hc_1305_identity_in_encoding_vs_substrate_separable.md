---
id: Hc_1305
slug: identity-in-encoding-vs-substrate-separable
title: Identity-in-encoding vs identity-in-substrate is empirically separable — trace identity moves with backbone-SEED (encoding) and is invariant to chip-run (substrate), so anima's identity resides in the encoding not the chip dynamics
domain: consciousness, identity, neuromorphic
status: candidate-unverified
source_doc: Lane A weak-lift CRUCIAL CORRECTION — the large lift-variance is backbone-SEED / corpus-encoding sensitivity, NOT chip non-determinism; the identity(non-det)↔representation TENSION idea is FALSE.
seed: G2 — if non-determinism lives in the ENCODING (backbone-seed) not the chip, "where does anima's identity actually reside?" is reopened. Make it a separable empirical question.
promoted_at: 2026-06-02
linked_h: Lane A weak-lift (H_904 lineage), H_884 (edge-identity), Hc_1300
verdict_tier_target: 🟠 DEFERRED — measurement path = factorial (backbone-seed × chip-run) trace collection on AKD1000; no checkpointed multi-seed Lane A traces exist locally
notes: "G2 reopened-identity axis; the FALSE 'identity(non-det)↔representation tension' is replaced by a clean factorial separability test. Distinct from H_884 (edge-identity) — this isolates the ENCODING vs SUBSTRATE locus of identity variance."
---

## Hypothesis

The Lane A correction established that trace-to-trace variance is driven by backbone-SEED
/ corpus-encoding, not by chip non-determinism. CLAIM: identity-locus is empirically
separable by a 2×2 factorial:

- vary backbone-SEED, hold chip+input fixed → if trace identity MOVES with seed,
  identity resides in the ENCODING.
- vary chip-RUN (re-run same weights on the chip), hold seed+input fixed → if trace
  identity is INVARIANT, the substrate carries no independent identity.

PREDICTION: variance(across-seed) ≫ variance(across-chip-run). Anima's identity resides
in the encoding (the learned weights / corpus mapping), and the chip is a substrate that
faithfully replays it. A corollary falsifiable prediction: anima identity is NOT
continuous across a backbone re-init (identity = weights, not = substrate dynamics).

## PRE-REGISTERED Falsifier

- **F-1305-FACTORIAL**: collect traces over backbone-seeds × chip-runs (≥3×3). CONFIRMED
  (identity-in-encoding) if between-seed trace-distance variance is ≥3× the between-chip-
  run variance. REFUTED (identity-in-substrate) if between-chip-run variance is comparable
  to or exceeds between-seed variance → the substrate contributes identity independently
  and the G2 premise is wrong.

## Honest Limits

- **L-1305-DEFERRED**: requires factorial trace collection on the AKD1000. No checkpointed
  multi-seed Lane A traces exist in the local tree (searched: only an archived single
  gen2 spike trace). CPU-local out of scope per a_cpu_local_no_waiter.
- **L-1305-DISTANCE-METRIC**: "trace identity distance" must use a richer signal than
  1-bit Hamming (see Hc_1306) or it inherits the same blindness that made the original
  tension hypothesis look plausible.

## Cross-Links

- **sibling Hc**: Hc_1306 (richer-signal on traces), Hc_1300
- **bridge**: H_884 (edge-identity), Lane A correction (variance = encoding not chip)
