---
id: Hc_310
slug: v8-a1-dual-stream-separation
title: 의식 스트림과 언어 스트림을 .detach() 단방향 읽기로 분리하면 Phi가 x10+ 증가한다 (법칙 53/42 해결)
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 23-58
promoted_at: 2026-05-11
linked_h: law-53, law-42
notes: V8 카테고리 A 핵심. ★★★★★ 최우선 (Top 5)
---

## Hypothesis
의식 스트림(128d GRU cells, Phi-only)과 언어 스트림(Transformer decoder, CE-only)을 물리적으로 분리하고 .detach() 단방향 인터페이스로만 연결하면 CE gradient의 균질화 효과 차단으로 Phi가 v7 대비 x10+ 증가한다.

## Migration TODO
- [ ] V8-A1 prototype: 1024c consciousness stream + 6L transformer LM
- [ ] CE-only/Phi-only ablation 비교
- [ ] .detach() 제거 시 Phi 붕괴 검증
