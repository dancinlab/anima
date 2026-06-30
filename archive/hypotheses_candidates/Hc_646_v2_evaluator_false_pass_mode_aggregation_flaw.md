---
id: Hc_646
slug: v2-evaluator-false-pass-mode-aggregation-flaw
title: V2 surface metric false PASS root cause = mode-aggregation flaw (greedy persona cycle + sample mode RNG ANY-mode aggregate = surface PASS)
domain: clm-evaluation
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_chat_cap_lesson_summary_2026_05_07.md
source_lines: 51-77, 95-99
promoted_at: 2026-05-11
linked_h: BG-HQ step 500 V2=8/10 false PASS, BG-HU step 800 V2=8/15, V3 6-cell strict
notes: Lesson H ★★★. V3 per-mode strict 가 해소. 8-BG retroeval + 15-BG SSOT 입증.
verified_at: 2026-05-12
verify_decision: MATH_PASS_NEEDS_ANCHOR
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (3+ numeric identities present) | F=3"
---

## Hypothesis
V2 ANY-mode aggregation 이 greedy persona prefix dump cycle + sample mode RNG surface c2_2/c2_3/c2_4 random hit 으로 PASS 산출. 동일 모델 두 generation mode 가 양립 불가능 PASS/FAIL signal 동시 산출 → V2 false PASS 본질 = mode-aggregation logic flaw. V3 per-mode strict (C3.1 persona_cycle_count=0 + C3.2 4-gram <5 even sample + C3.3 syllable Jaccard ≥0.05 + C3.4 manual proxy + V2 prerequisite) 가 해소.

## Falsifiable Tests
- F-V2-1: V3 strict PASS 가 manual review 와 ≥ 90% agreement
- F-V2-2: V3 strict 적용 후에도 false PASS 발견 시 → V4+ 필요
- F-V2-3: BG-HQ/HU 외 다른 V2 PASS verdict 가 V3 retroeval 에서 모두 0/N 확인

## Migration TODO
- [ ] mandate: V3 6-cell schema default chat-cap evaluator
- [ ] V2 + V3 parallel evidence mandatory for chat-cap PASS claim
- [ ] cells_v3 (6-cell) + cells_v3_legacy (4-cell) preserve raw#15 additive
