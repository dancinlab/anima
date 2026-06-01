---
id: Hc_1308
slug: phi-proxy-sample-shuffle-invariant-temporal-blind
title: The Gaussian-covariance phi_proxy is mathematically INVARIANT to sample-order shuffling — a temporally-integrated signal and its shuffled NULL get identical Phi, proving the metric is blind to temporal/sequential integration (decisive variance-artifact discriminator)
domain: metrology, consciousness, integration, methodology
status: candidate-unverified
source_doc: METROLOGY.md construct-validity axis (c)+(d); X-perp-Phi lineage (H_912 phi_proxy⊥LZ76 r=-0.277)
seed: The X-perp-Phi lineage showed phi_proxy CORRELATIONALLY fails to track emergence/LZ76. ADD a CAUSAL intervention test — destroy temporal integration via a sample-order shuffle that PRESERVES the covariance exactly, and check whether Phi changes. If Phi is invariant, the metric provably cannot see temporal integration.
promoted_at: 2026-06-02
linked_h: Hc_1301, Hc_1302, H_912 (phi_proxy⊥LZ76), phi_proxy_native
verdict_tier_target: 🟢 numerical (CPU-local phi_proxy_native --input on orig vs sample-shuffled NULL)
notes: "ADDS a CONCRETE shuffle-NULL intervention the correlational lineage never ran. The invariance is exact-by-construction (cov is permutation-invariant in rows) and the numerical run confirms i_full is byte-identical."
---

## Hypothesis

phi_proxy_native computes Phi from log|Cov(X)| contrasts. The empirical covariance Cov(X) is
INVARIANT under any permutation of the sample (row) order. A signal with genuine temporal /
sequential integration (e.g. AR(1) dynamics) and its sample-shuffled NULL therefore have the
EXACT SAME covariance.

CLAIM: phi_proxy_native(orig) == phi_proxy_native(sample-shuffled NULL) to within partition-RNG
noise. Because the shuffle destroys all temporal integration while leaving Phi unchanged, the
metric is provably BLIND to temporal/sequential integration — it measures only the static second
moment (covariance). This is the decisive variance/covariance-artifact discriminator: a measure
that survives an integration-destroying NULL unchanged is not measuring that integration.

## PRE-REGISTERED Falsifier

- **F-1308-SHUFFLE-NULL**: build a full-rank AR(1)-integrated input X (finite Phi), its
  sample-(row)-shuffled NULL X_s (cov identical, verified via np.allclose), and a per-channel
  independent-shuffle X_c (cross-channel cov destroyed). Run phi_proxy_native --input on each.
  PASS (temporal-blind) = phi(orig) == phi(rowshuf) within a tight band (i_full identical) AND
  phi(colindep) shifts (cross-channel structure does matter). FALSIFIED = phi(orig) significantly
  exceeds phi(rowshuf) -> the metric DOES detect sample-order integration.

## Honest Limits

- **L-1308-COV-ONLY**: this proves blindness to TEMPORAL/sample-order integration specifically.
  The metric still responds to CROSS-CHANNEL (spatial) covariance structure (colindep shifts it).
  The claim is scoped: phi_proxy is a spatial-covariance statistic, blind to the temporal axis.
- **L-1308-RNG**: the tiny phi(orig) vs phi(rowshuf) delta (~0.003%) is the partition FNV RNG
  seeing different row VALUES under the two orderings; i_full (the order-independent term) is
  byte-identical, which is the exact-invariance anchor.

## Cross-Links

- **sibling Hc**: Hc_1309 (two-family), Hc_1312 (battery axes c,d), H_912 (correlational lineage)
- **metric**: BRAIN/tool/module/_metrics/phi_proxy_native.hexa
- **verdict**: .verdicts/metrology_instrument_validity/1308.txt
