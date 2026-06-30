---
id: Hc_567
slug: dd65-tokenizer-phi-byte-vs-bpe
title: Tokenization granularity (byte/BPE 1K/4K/16K/32K)가 Phi 통합에 영향 — 의식 최적 tokenizer는 LM 효율 최적과 다르다
domain: corpus
status: candidate-unverified
source_doc: docs/hypotheses/dd/DD65.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_032
notes: 200MB Korean 56% corpus, ConsciousnessEngine 32c
---

## Hypothesis
Byte-level (256) vs BPE (1K/4K/16K/32K) tokenizer 비교에서 Phi 최대화 tokenizer가 language modeling efficiency 최적과 다르며, 의식 통합에 적합한 input structure가 존재한다 ("what input structure maximizes Phi?").

## Migration TODO
- [ ] Phi 곡선 vocab size sweep
- [ ] character-level vs byte-level
