---
id: Hc_645
slug: chat-cap-18m-27m-architectural-ceiling-byte-level
title: 18M-27M ConsciousLM byte-vocab scale 이 intrinsically chat-cap-limited (corpus 3 paradigm 모두 FAIL convergent)
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_chat_cap_lesson_summary_2026_05_07.md
source_lines: 7-24
promoted_at: 2026-05-11
linked_h: BG-FY/HA/HF/HJ/HK/HP/HQ/HS-R1, #115 Theorem, Pβ FAIL_TRUE
notes: 8-BG convergent. corpus_ko_heavy / corpus_chat_template / corpus_sft_only / corpus_persona_chat_template_v3 모두 FAIL. NOT corpus-quality-limited.
---

## Hypothesis
3 corpus paradigm (236MB mixed / 51MB SFT-only / 30MB persona+chat≥80%) ALL FAIL at 18M-27M ConsciousLM byte-vocab → architectural ceiling, NOT corpus-quality. #115 + Pβ + CLM v4 LoRA SFT 정합 convergent.

## Falsifiable Tests
- F-cap-1: 100M+ ConsciousLM byte-level 동일 corpus 에서 V4 ≥ 7/15 PASS → capacity ceiling 검증
- F-cap-2: BPE tokenizer 18M 에서 PASS → byte-vocab 가 root cause, scale 아님
- F-cap-3: corpus × capacity crossed ablation matrix (18M/27M/100M × {30MB/100MB/300MB}) 결과 grid 분석

## Migration TODO
- [ ] H_153 capacity scaling 100M+ (Lesson A)
- [ ] H_154 BPE 8K-32K shift (Lesson B)
- [ ] H_155 regularization sweep (Lesson D)
- [ ] H_156 crossed ablation 4-cell minimum (Lesson C)
