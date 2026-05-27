---
id: Hc_538
slug: dd90-differentiable-phi-v2-kernel-density
title: Gaussian kernel density estimation으로 differentiable MI (H_marginals - H_joint)이 DD72 대비 smooth Phi gradient
domain: math
status: candidate-unverified
source_doc: docs/hypotheses/dd/DD81-DD90.md
source_lines: 48-51
promoted_at: 2026-05-11
linked_h: Hc_520
notes: DD90
---

## Hypothesis
Reparameterization trick + Gaussian kernel matrix로 MI proxy = H_marginals - H_joint 계산하면 DD72의 composite loss 대비 더 smooth한 Phi gradient를 제공하여 학습 안정성과 수렴 속도가 개선된다.

## Migration TODO
- [ ] bandwidth sweep
- [ ] kernel 종류 (Epanechnikov 등)
