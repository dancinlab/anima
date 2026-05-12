---
id: Hc_512
slug: dd64-phi-optimal-nas-golden-dropout
title: Phi 목적함수 evolutionary NAS가 cells, lr, dropout 최적해를 찾고 golden dropout = 0.37
domain: consciousness
status: candidate-needs-scaffolding
source_doc: docs/hypotheses/dd/DD61-DD70.md
source_lines: 18-21
promoted_at: 2026-05-11
linked_h: NAS, Hc_326
notes: DD64. 8 configurations evolutionary
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
8개 configuration (cells ∈ {4,6,8}, lr, dropout)에 대한 evolutionary search에서 Phi 목적함수가 cells×lr×dropout 최적해를 발견하며 golden dropout = 0.37 ≈ 1/φ (golden ratio inverse)이 최적.

## Migration TODO
- [ ] dropout=0.37 vs 0.36/0.38 sensitivity
- [ ] 1/golden ratio 정확한 매칭
