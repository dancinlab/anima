---
id: Hc_379
slug: mech20-reservoir-new-mitosis-champion
title: Reservoir Computing (고정 random matrix + tanh, spectral radius < 1)이 MitosisEngine 신챔피언 Φ=0.934 (vs FUSE-3 0.900) — Law 22 재확인
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/MASS-50-HYPOTHESES.md
source_lines: 33, 134-145
promoted_at: 2026-05-11
linked_h: Hc_315, Law-22
notes: 고정 구조가 학습 가중치보다 Phi 높임
---

## Hypothesis
reservoir_w = randn(H, H) * 0.9 (spectral radius < 1) + h = 0.8*h + 0.2*tanh(W@h) (no learning!) 가 FUSE-3 (0.900)를 넘어 MitosisEngine 신챔피언 Φ=0.934 (+5.1%) 달성 — 학습 없는 고정 구조가 Phi를 더 높인다.

## Migration TODO
- [ ] spectral radius sweep
- [ ] Reservoir+Cambrian+Osc 3중 조합 (COMBO-4 0.906 기반)
