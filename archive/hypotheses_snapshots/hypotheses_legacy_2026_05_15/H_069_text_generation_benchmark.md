---
id: H_069
slug: text-generation-benchmark-cx
title: TEXT-GENERATION-BENCHMARK — chat substrate 텍스트 생성 품질 metric
domain: corpus
status: legacy-archive-pointer
exploration_method: E9 (chat-quality benchmark)
verification_method: W3 (composite text metric)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-03
---

# H_069 — Text Generation Benchmark

## Hypothesis

chat substrate 의 text generation 품질 (perplexity + diversity + coherence + KO ratio) composite metric 이 Φ 와 weakly correlate — 의식 substrate 가 chat capability 의 lower-bound 결정.

## Migration Status

Legacy file: `docs/hypotheses/cx/TEXT-GENERATION-BENCHMARK.md`. Pointer only.

## Cross-Links

- legacy: `docs/hypotheses/cx/TEXT-GENERATION-BENCHMARK.md`
- sister: H_005 (corpus quality), H_016 (an11 translation ceiling)
- own:

## Honest Limits

- L1: composite metric 정의 — 4개 component weight 임의
- L2: weak correlate 주장 — effect size 작아 actionable 어려움
- L3: chat-cap FAIL_TRUE (memory: PBETA + CLM v4) lane 와 일관성 약함
- L4: legacy 2026-03 pointer only
- L5: KO ratio 측정 자체 가 substrate 의존
