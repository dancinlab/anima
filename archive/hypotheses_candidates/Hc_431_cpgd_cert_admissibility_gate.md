---
id: Hc_431
slug: cpgd-cert-admissibility-gate
title: Cert-Projected Gradient Dance (CPGD) — gradients gated by cert admissibility, not loss threshold
domain: math
status: candidate-unverified
source_doc: docs/papers/phi_paradigm_paper_v1_preliminary.md
source_lines: 94-99
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: Within LoRA delta gradients run, but the gate is AN11/meta² admissibility check. Steps producing inadmissible Δ are rejected, optimizer rolled back. Optimizer moves only where cert chain remains closed.
---

## Hypothesis
Within the LoRA delta space, gradient steps are gated by AN11/meta² cert-chain admissibility, not by loss thresholds. Inadmissible steps trigger rollback. The optimizer "dances" — moving only along the manifold where the cert chain remains closed. Predicts cert-gated training yields more reproducible, more substrate-portable adapters than loss-thresholded training.

## Migration TODO
- [ ] Reproduce CPGD on independent substrate pair
- [ ] Measure rollback frequency vs convergence speed
- [ ] Compare adapter portability (cert-gated vs loss-gated) on transfer tasks
- [ ] Falsifier: no portability advantage at matched compute
