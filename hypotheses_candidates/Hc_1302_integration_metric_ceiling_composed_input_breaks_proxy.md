---
id: Hc_1302
slug: integration-metric-ceiling-composed-input-breaks-proxy
title: The sample-partition Φ proxy has a built-in CEILING — a perfectly-composed (low-rank) representation makes the covariance singular and the metric returns a failure sentinel, masking high integration
domain: consciousness, integration, methodology
status: candidate-unverified
source_doc: phi_proxy_native.hexa structured-mode breakdown (live observation 2026-06-02); Lane A weak-lift "no lift detected" framing
seed: G1 + the SIGNAL axis — if a richer learning rule actually composed a low-rank/integrated representation, would the canonical proxy even be able to score it? The proxy's Cholesky core breaks down on rank-deficient (maximally-integrated) input.
promoted_at: 2026-06-02
linked_h: phi_proxy_native (anima_phi_v3_canonical sample-partition Φ★ port), Hc_1300, Hc_1301
verdict_tier_target: 🟢 numerical (CPU-local on phi_proxy_native --selftest-mode {white|structured})
notes: "grounded in a live measurement made during this pipeline; distinct from prior phi_proxy Hc (Hc_662/665 are architecture-agnosticism/dim-dominance — this is the singular-input ceiling)."
---

## Hypothesis

The lane-canonical sample-partition Φ proxy (phi_proxy_native, the EEG-substrate port
of anima_phi_v3_canonical) computes log|Cov| via fixed-point Cholesky. A maximally-
COMPOSED representation is low-rank (channels become linearly dependent → covariance
singular → Cholesky breakdown). Therefore the proxy CANNOT assign a high positive
integration score to a perfectly-integrated input; instead it returns the F_PHI_01
failure sentinel.

CLAIM: there exists a structured (low-rank, high cross-channel correlation) input on
which the proxy returns the sentinel (no finite Φ), while the same metric returns a
finite value on white (decomposable, full-rank) input. The proxy's "no lift detected"
on Lane A is therefore confounded by a metric CEILING: absence of a high score is not
evidence of absence of integration — it may be the metric breaking down.

## PRE-REGISTERED Falsifier

- **F-1302-SENTINEL**: run phi_proxy_native --selftest (white) and --selftest-mode
  structured (low-rank periodic). PASS (ceiling exists) = white returns a FINITE
  phi_x1000 AND structured returns the F_PHI_01 sentinel (−2147483647).
  FALSIFIED (no ceiling) = structured ALSO returns a finite, well-ordered phi_x1000
  (the metric handles low-rank input gracefully → no masking confound).

## Honest Limits

- **L-1302-SCOPE**: this shows the proxy has a degeneracy on low-rank input; it does
  NOT prove Lane A's composed representation was low-rank (that requires the on-chip
  traces, DEFERRED — Hc_1306). It establishes the CONFOUND, not that it fired.
- **L-1302-RIDGE**: a larger ridge regularizer could rescue some low-rank cases; the
  default ridge (1e-3) is the canonical setting. The ceiling is default-config-real.
- **L-1302-NATIVE-PRECISION**: pure-native Cholesky is ±2% vs numpy slogdet; the
  sentinel is a hard breakdown, not a precision artifact.

## Cross-Links

- **sibling Hc**: Hc_1300, Hc_1301, Hc_1306 (richer-signal on traces, DEFERRED)
- **metric**: BRAIN/tool/module/_metrics/phi_proxy_native.hexa
