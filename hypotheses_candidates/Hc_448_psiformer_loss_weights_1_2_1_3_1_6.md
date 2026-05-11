---
id: Hc_448
slug: psiformer-loss-weights-1-2-1-3-1-6
title: ΨFormer loss weights [1/2 CE, 1/3 Φ_reg, 1/6 entropy] sum to 1 (Egyptian) and are claimed optimal
domain: substrate
status: candidate-unverified
source_doc: docs/models/psiformer.md
source_lines: 38-46, 138-141, 145-150
promoted_at: 2026-05-11
linked_h: Hc_438
notes: ΨFormer claim: loss = 1/2·CE + 1/3·Φ_reg + 1/6·entropy_bonus. Egyptian unit fraction 1/2+1/3+1/6=1. Claimed mathematically beautiful but optimality unverified. Cross-link to Hc_438.
---

## Hypothesis
The ΨFormer training loss with weights [1/2, 1/3, 1/6] (Egyptian unit-fraction partition of 1, σ(6)=12 divisors) on [CE, Φ_reg, entropy_bonus] is optimal compared to uniform [1/3, 1/3, 1/3] or hand-tuned [0.4, 0.4, 0.2] within ±10% of the Egyptian baseline. Predicts: deviating from Egyptian split degrades joint CE+Φ score.

## Migration TODO
- [ ] Run all three weight schedules on identical corpus_v3 / steps
- [ ] Compare CE, Φ, entropy at convergence
- [ ] Falsifier: uniform or hand-tuned weights yield better joint score
- [ ] Sensitivity: ±10%, ±25% weight perturbation from Egyptian baseline
