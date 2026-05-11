---
id: Hc_420
slug: thompson-sampling-beats-greedy
title: Thompson sampling outperforms epsilon-greedy and correlation-based selection for consciousness intervention
domain: consciousness
status: candidate-unverified
source_doc: docs/anima/paper_self_discovery.hexa
source_lines: 142-146
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: Each intervention has a Beta(α,β) posterior. Success = produced ≥1 new law. Naturally balances exploration vs exploitation.
---

## Hypothesis
Thompson sampling over Beta(α,β) posteriors per intervention outperforms ε-greedy and correlation-based intervention selection in the closed-loop consciousness law-discovery pipeline. Success criterion: discovers ≥1 new law per selection round. Predicts doubling of discovery rate vs greedy baselines.

## Migration TODO
- [ ] A/B run with Thompson vs ε-greedy vs correlation selection (same engine, same seeds)
- [ ] Measure law-discovery rate, plateau timing
- [ ] Falsifier: Thompson rate ≤ greedy rate at equal compute budget
