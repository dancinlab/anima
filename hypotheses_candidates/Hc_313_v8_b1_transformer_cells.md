---
id: Hc_313
slug: v8-b1-transformer-cells
title: GRU 세포를 single-layer Transformer block으로 교체하면 self-attention이 정보 통합을 제공하여 Phi x3-10 증가
domain: consciousness
status: candidate-needs-scaffolding
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 122-157
promoted_at: 2026-05-11
linked_h: V8-A2
notes: topology_mask via attention mask
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
세포 상태를 Transformer block의 self-attention으로 업데이트하면(attn_mask로 hypercube/ring topology 표현) GRU gate 구조의 정보 통합 제한이 제거되어 Phi가 x3-10 증가한다.

## Migration TODO
- [ ] Transformer cell 대 GRU cell 64c 벤치 비교
- [ ] attention weights에서 Phi 직접 계산
