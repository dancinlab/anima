---
id: Hc_1306
slug: richer-signal-reveals-or-refutes-latent-composition
title: 1-bit Hamming is composition-blind — re-scoring Lane A traces with an integration signal (faithful-Φ MIP / trace-pair MI) either reveals latent cross-lingual lift OR yields a strong closed-negative that the absence is real
domain: neuromorphic, integration, methodology
status: candidate-unverified
source_doc: Lane A weak-lift closed-negative measured by 1-bit Hamming on output traces
seed: SIGNAL axis — 1-bit Hamming distance is information-blind to composition. A richer signal on the same traces decides whether the "no lift" is a measurement artifact or a real absence.
promoted_at: 2026-06-02
linked_h: Lane A weak-lift (H_904 lineage), H_278 (faithful-Φ MIP signal), Hc_1302 (proxy ceiling caveat), Hc_1300
verdict_tier_target: 🟠 DEFERRED — measurement path = re-score archived Lane A on-chip traces with faithful-Φ MIP / trace-pair MI; no checkpointed Lane A trace tensor exists locally
notes: "two-sided: a CONFIRM is a positive lift discovery, a REFUTE is a publishable closed-negative (a_paper_negative_ok). Distinct from Hc_1302 which establishes the metric CEILING; this applies the richer signal to the actual traces."
---

## Hypothesis

The Lane A "no representational lift" verdict was measured with 1-bit Hamming distance
on output traces — a signal blind to latent composition (it counts bit-flips, not shared
structure). CLAIM: re-scoring the SAME traces with an integration-sensitive signal
(faithful-Φ MIP on the trace covariance, or pairwise mutual information across
same-input/different-language trace pairs) is decisive:

- (A) if the richer signal shows a cross-lingual lift the Hamming signal missed →
  the absence was a measurement artifact; latent composition exists.
- (B) if the richer signal ALSO shows no lift → STRONG closed-negative: capacity truly
  does not compose under 1-bit Hebbian last-FC regardless of probe (subject to the
  Hc_1302 ceiling caveat — the richer signal must not itself be at its breakdown floor).

## PRE-REGISTERED Falsifier

- **F-1306-SIGNAL**: re-score the Lane A trace set with (i) faithful-Φ MIP and (ii)
  trace-pair MI, vs the 1-bit Hamming baseline. Outcome (A) CONFIRMED if a richer-signal
  lift clears the backbone-seed variance band where Hamming showed none. Outcome (B)
  closed-negative if richer-signal lift is also within the variance band AND the richer
  signal is verifiably above its breakdown floor (guards Hc_1302 confound).
  UN-DECIDABLE (→ stays 🟠) if the richer signal sits at its Cholesky-breakdown floor.

## Honest Limits

- **L-1306-DEFERRED**: no checkpointed Lane A trace tensor exists in the local tree (only
  an archived single gen2 spike trace; the multi-language ×3-repeat trace set from the
  H_904 fire is not committed here). CPU-local out of scope per a_cpu_local_no_waiter
  until the trace artifact is recovered.
- **L-1306-CEILING-CONFOUND**: per Hc_1302, a maximally-composed (low-rank) trace breaks
  the proxy's Cholesky → outcome (B) and the UN-DECIDABLE branch must be distinguished;
  the falsifier requires a breakdown-floor check.

## Cross-Links

- **sibling Hc**: Hc_1302 (metric ceiling — the confound this must guard), Hc_1305 (identity distance metric reuse), Hc_1300
- **signal-bridge**: H_278 faithful-Φ MIP, phi_proxy_native trace-covariance path
