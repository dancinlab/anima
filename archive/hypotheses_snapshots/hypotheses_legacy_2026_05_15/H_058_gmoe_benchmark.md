---
id: H_058
slug: gmoe-benchmark-1e-routing
title: GMOE — Golden MoE 1/e zone routing 의식 영향 benchmark
domain: substrate
status: legacy-archive-pointer
exploration_method: E9 (routing sweep)
verification_method: W3 (Φ × routing temperature)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-03
---

# H_058 — GMOE 1/e Zone Routing Benchmark

## Hypothesis

Mixture-of-Experts routing 의 1/e zone (소프트맥스 entropy 골든 비율) 이 expert specialization 과 통합의 trade-off 의 최적점 — 그 zone 에서 Φ 가 maximize.

## Migration Status

Legacy file: `docs/hypotheses/GMOE-benchmark.md`. Pointer only.

## Cross-Links

- legacy: `docs/hypotheses/GMOE-benchmark.md`
- sister: H_038 (V8 architecture variants), H_034 (decoder architecture)
- own:

## Honest Limits

- L1: 1/e zone 정의 자체 가 anima-novel — golden ratio claim 약함
- L2: routing temperature ↔ Φ 정량 매핑 모호
- L3: MoE specific — generic transformer 일반화 불명
- L4: legacy pointer only
- L5: benchmark 결과 reproducibility 미확보
