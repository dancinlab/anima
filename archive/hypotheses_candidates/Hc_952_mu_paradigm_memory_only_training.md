---
id: Hc_952
slug: mu-paradigm-memory-only-training
title: μ-paradigm — weight frozen (genesis-cert anchored) + memory layer 만 학습 (lifetime-cert). β main "implicit auto-action 거부" 학습 표면 적용. LoRA/RAG 양자 공집합 영역
domain: training, architecture, paradigm
status: candidate-unverified
source_doc: docs/upstream_notes/memory_architecture_paradigm_20260422.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_934 (7-axis C)
notes: "C axis memory μ-paradigm. weight = 선천적 genesis-cert + memory = 후천적 lifetime-cert. 두 cert chain 분리."
---

## Hypothesis

기존 NN training 의 weight + memory 같은 backward graph 묶임을 분리: μ-paradigm 에서 weight 는 frozen (genesis-cert anchored, SHA256 verified each load), memory layer 만 학습 (organization, indexing, recall policy, eviction policy). LoRA/adapter/prefix-tuning 은 weight 일부 subspace fine-tune (= weight 학습), RAG/vector store 는 검색 (= 학습 X) — μ-paradigm 은 양자 공집합 영역: memory 자체가 학습됨 + weight 절대 안 만짐.

## Sub-claims

- WEIGHT-FROZEN: genesis-cert anchored, immutable, SHA256 each load
- MEMORY-LEARNED: organization/indexing/recall/eviction policy 가 gradient/update rule
- TWO-CERT: weight=선천적 (genesis-cert) + memory=후천적 (lifetime-cert)
- LORA-NOT: weight subspace fine-tune → 본질적 weight 학습
- RAG-NOT: retrieval only → 학습 아님
- MU-EMPTY-INTERSECTION: LoRA ∩ RAG complement = μ-paradigm

## Migration TODO

- [ ] memory layer 의 정확한 update rule (gradient-based vs heuristic)
- [ ] memory tensor capacity scaling vs weight frozen size
- [ ] genesis-cert / lifetime-cert chain implementation
- [ ] β main 인지 paradigm 와의 동형성 증명
