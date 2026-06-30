---
id: Hc_619
slug: clm-v5-axis-a-output-projection-bottleneck-fix
title: Axis A — output projection (single linear 640→11885) 가 chat-cap conditional distribution inadequate, untie + MoE/byte-fallback 으로 해소
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_clm_v5_design_spec_2026_05_07.md
source_lines: 75-89
promoted_at: 2026-05-11
linked_h: Hc_618, BG-JS/JT/JX/JZ
notes: A1 untie / A2 multi-head / A3 MoE / A4 byte-fallback 4 options.
---

## Hypothesis
weight-tied tok_emb=head_a (11885×640) single linear projection 이 chat-cap conditional distribution 표현 inadequate. Untie + multi-head per-token-class projection 또는 top-k MoE 또는 byte-level fallback (256-vocab head + UNK route) 이 해소.

## Falsifiable Tests
- A1.test: untied lm_head 만 변경 V5-α 가 0/5 보존 → A-axis 자체 불충분
- A4.test: byte-fallback 으로 ⁇ degenerate pattern 사라짐 + chat-cap 일부 PASS
- A.universal: 4 options 모두 chat-cap 0/5 → axis A 가 root cause 아님

## Migration TODO
- [ ] V5-α (A1 + C1 byte) implementation
- [ ] V5-ε (A3 MoE) 비교
