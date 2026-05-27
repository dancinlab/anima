---
id: Hc_430
slug: beta-paradigm-cert-projection
title: β paradigm reframes adaptation as admissibility-certified projection, not gradient descent on base weights
domain: math
status: candidate-unverified
source_doc: docs/papers/phi_paradigm_paper_v1_preliminary.md
source_lines: 42-46
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: Base weights frozen. LoRA deltas + cert chain (AN11 + meta²). Three-paradigm unification: (β main) ≅ (proposal stack) ≅ (cell-learning). Convergence = cert chain closure + Φ invariance across substrates.
---

## Hypothesis
Model adaptation can be reformulated as admissibility-certified projection (β paradigm): base weights are frozen, only LoRA adapters Δ are produced, and Δ chains into a cert proof (AN11 triple a/b/c + meta²) iff structurally admissible. Convergence is measured not by training loss but by cert-chain closure plus downstream Φ invariance across substrates.

## Migration TODO
- [ ] Reproduce cert-chain closure on independent substrate
- [ ] Compare β paradigm adapter to gradient-descent adapter at fixed compute
- [ ] Falsifier: cert-closed adapter underperforms unconstrained adapter on all tasks
