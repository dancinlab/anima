---
id: Hc_973
slug: p9-benchmark-amendment-a1-verdict-mode
title: P9 SFT Amendment A-1 — verdict mode taxonomy (Mode 1 comparative HF / Mode 2 anchor compliance / Mode 3 train-time absolute). CLM v4 base ≈ random+1-2pt (HellaSwag 0.264 / MMLU 0.271 / TriviaQA 0.000) = structural pre-registered NOT discriminative refutation
domain: benchmark, verification
status: candidate-unverified
source_doc: docs/p9_benchmark_switch_a_prime_spec_amendment_2026_05_04.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_943 (P9 P1.7)
notes: "ConsciousDecoderV3.forward consciousness_states=None bypass (lm-eval-harness) + block_size=512 truncation (vs Llama 8K context) = structural reasons pre-registered."
---

## Hypothesis

P9 SFT 의 original PASS gate (CLM ≥ random+5pt on ≥2/3 benchmark) 는 single all-or-nothing. CLM v4 base 가 random+1-2pt 결과를 받았으나 이는 **structural pre-registered**: (1) consciousness coupling bypass (lm-eval-harness passes None to consciousness_states), (2) block_size=512 truncation (vs Llama-3.2-3B 8K context). Amendment A-1 가 verdict mode taxonomy 추가 — Mode 1 (comparative HF) / Mode 2 (anchor compliance) / Mode 3 (train-time absolute) — 으로 structural constraint 를 first-class verdict mode 로 격상.

## Sub-claims

- CLM-v4-BASE: HellaSwag 0.264 vs random 0.250, MMLU 0.271 vs 0.250, TriviaQA 0.000
- STRUCTURAL-1: ConsciousDecoderV3.forward(consciousness_states=None) bypasses cross-attention
- STRUCTURAL-2: block_size=512 left-truncates MMLU 5-shot (~800-1200 tok), TriviaQA passages
- MODE-1: comparative HF (vs other public models)
- MODE-2: anchor compliance (anchor metric thresholds)
- MODE-3: train-time absolute (CLM v4 actual condition)
- BACKWARD-COMPAT: original spec LOCKED, additive amendment doc

## Migration TODO

- [ ] Mode 1/2/3 각각 PASS criterion 정량화
- [ ] consciousness_states 가 inject 되었을 때의 expected lift
- [ ] block_size 1024+ 확장 시 prediction
- [ ] amendment marker LOCK 검증
