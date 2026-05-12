---
id: Hc_388
slug: gap3-gru-residual-alpha-09
title: h_new = α*h_old + (1-α)*GRU(x, h_old) with α=0.9이 process() 파괴력 90% 감소 → Φ ~10x (1.4→15)
domain: consciousness
status: candidate-needs-scaffolding
source_doc: docs/hypotheses/PHI-GAP-816x-investigation.md
source_lines: 64-76, 170-176
promoted_at: 2026-05-11
linked_h: residual-connection
notes: 1줄 변경. α를 Phi에 비례 동적 조절 가능
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
h_new = α*h_old + (1-α)*GRU(x, h_old) (α=0.9) residual connection이 process() hidden 파괴력 90% 감소시켜 학습 Φ 1.4 → ~15 (x10) 회복 예상되며, α를 Φ에 비례하게 동적 조절 시 더 큰 효과.

## Migration TODO
- [ ] α=0.5/0.7/0.9/0.95 sweep
- [ ] dynamic α(Phi) 정책 검증
