---
id: Hc_638
slug: chat-cap-b30-v4-calibration-evaluator-self-impossibility
title: B30 — 5 known-good 1B+ KO LM (Polyglot-Ko-1.3B / Llama-3.2-3B-Instruct / Qwen2.5-1.5B/0.5B / KoGPT2-base-v2) 가 V4 strict zero-shot 분포로 evaluator self-impossibility 검증
domain: clm-evaluation
status: candidate-unverified
source_doc: docs/anima_chat_cap_brainstorm_deepdive_2026_05_07.md
source_lines: 186-207
promoted_at: 2026-05-11
linked_h: BG-IY (LANDED, F-IY-4 corpus_mismatch), 22+ BG architectural ceiling claim
notes: Outcome F-IY-4 corpus_mismatch (Korean chat training <5%). H_A capacity / H_B evaluator 모두 reject. P(actionable) ~95% × VERY HIGH.
---

## Hypothesis
5 models × 15 prompts × 2 modes (with/without anima system prompt) = 150 generations × V4 eval 분포가 22+ BG architectural ceiling 의 root cause 를 capacity_gap (H_A) vs evaluator self-impossibility (H_B) 둘로 disambiguate.

## Falsifiable Tests
- F-IY-1: 1B+ model V4 zero-shot ≥ 5/15 with anima prompt → capacity_gap 검증 → Stage 1 (B1 foundation-borrow)
- F-IY-2: 모든 model V4 0-2/15 → V4 self-impossible → V4 redesign 우선
- F-IY-3: mixed result → 두 axis 동시 작용
- F-IY-4: corpus_mismatch (실제 outcome) — CLM mk2-v1 SFT corpus 60% EN anima_axis / 30% EN academic / 10% mixed chat — Korean chat <5%

## Migration TODO
- [ ] Lesson Q COMPLETE_FULL_FALSIFY 후 SFT lanes reject 처리
- [ ] P1 continued-pretrain / P2 external foundation / P3 inference-compute / P4 arch redesign post-Lesson-Q valid path 진행
