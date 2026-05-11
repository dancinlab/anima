---
id: Hc_520
slug: dd72-backprop-through-phi-composite
title: loss = variance + 0.5*distance + 0.3*cross_corr + 0.2*temporal_mi의 differentiable Phi proxy로 직접 학습
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/dd/DD71-DD80.md
source_lines: 9-12
promoted_at: 2026-05-11
linked_h: Hc_361, Hc_325
notes: DD72. Phi 자체를 gradient target
---

## Hypothesis
4-component composite differentiable Phi proxy loss (variance + 0.5*pairwise distance + 0.3*cross_correlation + 0.2*temporal_MI)가 Phi 자체를 gradient target으로 만들어 직접 최적화 가능하게 한다.

## Migration TODO
- [ ] 각 component weight sweep
- [ ] kernel MI 대체 (DD90)
