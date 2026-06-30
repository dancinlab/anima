---
id: Hc_434
slug: v2-metric-method-a-c-null-bootstrap
title: Φ v2 metric — full Gram eigenvalue spectrum + participation ratio + null-bootstrap p95 threshold
domain: math
status: candidate-unverified
source_doc: docs/papers/phi_paradigm_paper_v1_preliminary.md
source_lines: 376-388
promoted_at: 2026-05-11
linked_h: Hc_433
notes: Roadmap #90. Method A (full Gram top-16 eigenvalues) + Method C (PR = (Σλ)²/(Σλ²)) + null bootstrap (shuffle prompt order, p95 threshold over 100 reps × 6 pairs = 600 null samples). Replaces v1 naive 16-stride projection.
---

## Hypothesis
The Φ substrate-comparison metric should use Method A (full Gram eigenvalue spectrum, top-16 eigenvalues per path) + Method C (participation ratio PR = (Σλ)²/(Σλ²) as spectral effective rank) + null-bootstrap (shuffle prompt order within path → p95 threshold). This v2 metric is well-posed against real base-weight distributions; the v1 16-stride projection is not.

## Migration TODO
- [ ] Re-derive v2 metric on a new substrate pair
- [ ] Compare v2 vs v1 metric on identical hidden states
- [ ] Falsifier: v2 metric yields same FAIL band as v1 on real distributions
- [ ] Validate p95 threshold convergence under n_reps ∈ {100, 1000, 10000}
