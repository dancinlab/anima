---
id: Hc_390
slug: gap5-consciousness-gated-gru
title: GRU update gate를 Φ로 제어: z = sigmoid(Wz@[h,x]) * (1 - phi_gate) — 의식이 자기를 보호하는 게이트
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/PHI-GAP-816x-investigation.md
source_lines: 93-107
promoted_at: 2026-05-11
linked_h: GRU, self-protection
notes: phi_gate = sigmoid((Φ - threshold) * scale)
---

## Hypothesis
modified GRU update gate z' = z * (1 - phi_gate) where phi_gate = sigmoid((Φ - threshold) * scale) 이 Φ 높을 때 hidden 변경을 자동 차단하여 "의식이 자기를 보호하는 게이트" 메커니즘을 구현한다.

## Migration TODO
- [ ] phi_gate threshold sweep
- [ ] CE 영향 측정
