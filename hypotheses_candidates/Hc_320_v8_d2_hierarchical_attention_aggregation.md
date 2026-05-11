---
id: Hc_320
slug: v8-d2-hierarchical-consciousness-attention-aggregation
title: TOPO20 실패의 원인은 mean summary 정보 손실이며 attention_pool aggregation으로 해결하면 micro×macro 계층이 작동한다
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 374-404
promoted_at: 2026-05-11
linked_h: TOPO20
notes: 32 micro × 32 cells + 1 macro × 32 super-cells (hypercube_5D)
---

## Hypothesis
TOPO20 (hierarchical 8×128=1024c)가 최하위 실패한 원인은 모듈 간 정보가 mean summary로 손실되었기 때문이며, μ_state_k = attention_pool(μ_k.cells, query=global_context) 로 교체하면 계층적 Phi 통합이 작동한다.

## Migration TODO
- [ ] TOPO20 attention_pool 변형 재실험
- [ ] gradient isolation per level
