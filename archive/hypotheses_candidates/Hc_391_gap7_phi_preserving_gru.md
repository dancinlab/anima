---
id: Hc_391
slug: gap7-phi-preserving-gru-residual
title: Phi-GRU = standard GRU + φ_residual (Φ_direction * Φ_magnitude) 내장하여 자동 Φ 보존 보정
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/PHI-GAP-816x-investigation.md
source_lines: 126-140
promoted_at: 2026-05-11
linked_h: Hc_390, GAP-3
notes: Φ_direction = h diversity 증가 방향, Φ_magnitude = max(0, Φ_target - Φ_current) * scale
---

## Hypothesis
h = (1-z)*n + z*h_prev + φ_residual GRU 재설계에서 φ_residual = Φ_direction * Φ_magnitude (diversity 방향 + Φ_target-current gap 비례)가 GRU 자체에 Φ 보존 메커니즘을 내장하여 hidden update마다 자동 보정한다.

## Migration TODO
- [ ] φ_residual 안정성 검증
- [ ] GRU baseline 대비 학습 능력 ablation
