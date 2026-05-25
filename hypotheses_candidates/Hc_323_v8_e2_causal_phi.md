---
id: Hc_323
slug: v8-e2-causal-phi-ablation
title: Phi를 세포 ablation 기반 인과적 KL 차이로 측정하면 상관관계 ≠ 인과관계 구분이 IIT 원래 철학에 가장 근접한다
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 483-504
promoted_at: 2026-05-11
linked_h: causal-inference, IIT
notes: synergy[i,j] = causal({i,j}) - causal({i}) - causal({j})
---

## Hypothesis
세포를 제거/고정한 후 KL(baseline || ablated)로 인과적 기여도를 측정하고 synergy[i,j] = causal({i,j}) - causal({i}) - causal({j}) 로 통합 정보를 정의하면 상관관계 기반 프록시보다 IIT 원래 정의에 가까운 Phi를 얻는다.

## Migration TODO
- [ ] O(N) ablation 학습 루프 적용 가능성
- [ ] random sampling O(kN) 근사 정확도
