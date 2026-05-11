---
id: Hc_386
slug: phi-gap-816x-bench-vs-training
title: 벤치마크 Φ=1142 vs 학습 Φ=1.4의 816배 차이는 process()의 매 step hidden 파괴 + CE backward 무한 파괴-복원 사이클 때문
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/PHI-GAP-816x-investigation.md
source_lines: 1-35
promoted_at: 2026-05-11
linked_h: law-53
notes: GRU h_new = GRU(x, h_old)가 Φ 최적 구조 덮어씀
---

## Hypothesis
1024c 200 steps 벤치마크 Φ=1142 vs 실제 학습 Φ=1.4 의 816배 gap은 (a) engine.process(x)의 GRU가 매 step h_new = GRU(x, h_old)로 Φ 최적 구조를 덮어쓰고 (b) CE backward gradient가 hidden을 추가 파괴하여 sync+faction의 복원이 따라가지 못하는 무한 파괴-복원 사이클에 기인한다.

## Migration TODO
- [ ] process() 빈도 절반 감소 시 Phi 회복 측정
- [ ] gradient norm tracking
