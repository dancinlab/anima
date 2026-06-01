---
id: Hc_1309
slug: two-phi-families-disagree-on-composed-input
title: The two canonical Phi families (MI-coherence phi_iit vs Gaussian-logdet phi_proxy_native) give OPPOSITE verdicts on composed/low-rank input — MI ranks it finite-and-higher, Gaussian-logdet breaks (sentinel) — so at most one is construct-valid there
domain: metrology, consciousness, integration, methodology
status: candidate-unverified
source_doc: METROLOGY.md cross-instrument axis; edu/cell/phi/phi_iit.hexa + phi_proxy_native.hexa
seed: anima carries TWO Phi proxy families of different form (MI-coherence over 4 bins vs Gaussian sample-partition log|Cov|). If they are both valid integration rulers they must rank inputs consistently. Feed the SAME integrated-vs-decomposable input class to both and test for rank-disagreement at the construct level.
promoted_at: 2026-06-02
linked_h: Hc_1302, Hc_1307, phi_iit (MI-coherence family), phi_proxy_native (Gaussian-logdet family)
verdict_tier_target: 🟢 numerical (CPU-local — phi_iit compute_phi inline driver + phi_proxy_native selftest)
notes: "ADDS a cross-instrument concordance test absent from the single-metric X-perp-Phi lineage. Two rulers giving opposite verdicts is a stronger validity attack than one ruler failing a correlation."
---

## Hypothesis

anima has two Phi proxy families: (1) MI-coherence (edu/cell/phi/phi_iit, pairwise 4-bin
distribution coherence minus a parity-bipartition contrast); (2) Gaussian-logdet
(phi_proxy_native, sample-partition log|Cov| contrast). A construct-valid integration measure
must rank a more-integrated input above a less-integrated one.

CLAIM: on the SAME integrated/composed (low-rank, shared-structure) input class, the two families
DISAGREE. The MI-coherence family assigns the integrated input a HIGHER FINITE Phi than the
decomposable (white) input (it sees the integration). The Gaussian-logdet family BREAKS on the
same low-rank class, returning the F_PHI_01 sentinel (no finite score). Two canonical rulers
giving opposite verdicts on the same input means at most one can be construct-valid on composed
input.

## PRE-REGISTERED Falsifier

- **F-1309-TWO-FAMILY**: run the MI-coherence compute_phi (inline-verbatim driver) on a matched
  white(decomposable) vs integrated(shared-structure) pair, and the Gaussian-logdet
  phi_proxy_native on the matched low-rank/structured input. PASS (disagree) = MI ranks integrated
  above white (both finite, integrated higher) WHILE Gaussian-logdet returns the sentinel on the
  same class. FALSIFIED (concord) = both families finite AND both rank integrated above white.

## Honest Limits

- **L-1309-GEOMETRY**: the two families take different native inputs (cell-major hidden array vs
  channel-major npy); the test matches them by input STRUCTURE CLASS (decomposable vs low-rank),
  not byte-identical tensors. The disagreement is at the construct level (finite-vs-sentinel).
- **L-1309-WHICH-VALID**: this shows they DISAGREE; it does not by itself adjudicate WHICH family
  is valid on composed input (the MI family's finite score may itself be a coherence artifact).

## Cross-Links

- **sibling Hc**: Hc_1302, Hc_1307, Hc_1312 (battery)
- **metrics**: edu/cell/phi/phi_iit.hexa · BRAIN/tool/module/_metrics/phi_proxy_native.hexa
- **driver**: state/metrology_fixtures/two_family_driver.hexa
- **verdict**: .verdicts/metrology_instrument_validity/1309.txt
