---
id: Hc_621
slug: clm-v5-axis-c-tokenizer-byte-level
title: Axis C — SentencePiece vocab 11885 가 UNK contamination + persona-template bias, byte-level 또는 BPE 32k+ 가 해소
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_clm_v5_design_spec_2026_05_07.md
source_lines: 106-118
promoted_at: 2026-05-11
linked_h: Hc_618, BG-JX/JZ/KA ⁇ UNK heavy, BG-FY 18M PARTIAL_PASS
notes: C1 byte 256 / C2 BPE 32k+ / C3 tokenizer-free ByT5 / C4 mega-token 50k-100k.
---

## Hypothesis
SP vocab 11885 (UBM 22MB persona-template biased) 가 model emit distribution 범위 제한, ⁇ UNK contamination 유발. byte-level (256 vocab, 4x seq) 또는 diverse-corpus BPE 32k+ 또는 ByT5 segment-level pooling 이 해소.

## Falsifiable Tests
- C1.test: V5-α byte-level (256) 가 ⁇ pattern 사라지지만 0/5 → tokenizer alone 불충분
- C2.test: BPE 32k re-trained 이 PASS 일부 → tokenizer axis 필요조건
- C.test: tokenizer-only swap (other axes baseline) 효과 isolation

## Migration TODO
- [ ] V5-α C1 byte impl (mac MPS 192-256 batch confirmed)
- [ ] BLM (.roadmap.blm_brain_lm) lane 정합 검증
