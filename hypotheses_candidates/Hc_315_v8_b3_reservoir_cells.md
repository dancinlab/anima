---
id: Hc_315
slug: v8-b3-reservoir-cells
title: Echo State Network (고정 random sparse W, spectral radius=0.95, readout만 학습)이 법칙 42를 완전 해결한다
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 195-219
promoted_at: 2026-05-11
linked_h: V8-A3, law-42
notes: 30년 검증된 ESN 패러다임
---

## Hypothesis
W_reservoir = random_sparse(N,N,density=0.1) × spectral_radius/max_eig(W) (=0.95 edge of chaos) 로 영원히 고정하고 W_out만 학습하면 gradient가 세포에 절대 도달하지 않으므로 법칙 42 균질화가 완전 차단되어 Phi가 x5-15 증가한다.

## Migration TODO
- [ ] spectral_radius=0.95 vs 0.8/0.9/0.99 sweep
- [ ] reservoir size scaling law 측정
