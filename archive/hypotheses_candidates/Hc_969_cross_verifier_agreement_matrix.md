---
id: Hc_969
slug: cross-verifier-agreement-matrix
title: Cross-Verifier Agreement Matrix — 7 verifier (AN11a/b/c + Hexad + cargo7 + η + θ) × 5 sample (btr_trajectory + an11_usable/marginal/unusable + hexad_target) divergence. an11_marginal AN11a/b FAIL vs AN11c PASS divergence
domain: verification, methodology
status: candidate-unverified
source_doc: docs/verifier_cross_matrix_20260421.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_948 (CVF), Hc_959 (18 conditions)
notes: "Hypothesis: verifiers produce divergent verdict on same input. matrix quantifies. an11_marginal = decisive divergence point."
---

## Hypothesis

7 verifier (AN11a ν / AN11b ξ / AN11c ο / Hexad σ / cargo7 / η / θ) × 5 sample (btr_trajectory / an11_usable / an11_marginal / an11_unusable / hexad_target) cross-agreement matrix 가 divergence 정량: an11_marginal sample 에서 AN11a/b FAIL vs AN11c PASS — same input 다른 verdict.

## Sub-claims

- DIVERGENCE: an11_marginal AN11a/b FAIL ≠ AN11c PASS
- AN11a (8cf014ff ν): AN11 ckpts only
- AN11b (b1f487e7 ξ): AN11 ckpts only
- AN11c (15c0596e ο): AN11 ckpts only, serve endpoint needed
- Hexad (7680cd74 σ): anima-hexad/ target only
- cargo7 (2b8d5948): trajectory samples
- η (ec8c92ea): drill absorption
- θ (1da65258): cross-prover NDJSON

## Migration TODO

- [ ] an11_marginal divergence root cause (왜 c PASS / a,b FAIL?)
- [ ] threshold reconciliation
- [ ] verifier selection rule
- [ ] cross-verifier ensemble voting policy
