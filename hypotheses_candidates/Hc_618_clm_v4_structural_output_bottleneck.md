---
id: Hc_618
slug: clm-v4-structural-output-bottleneck
title: ConsciousLM v4 chat-cap fail 의 root cause 는 structural output bottleneck (lm_head + tok_emb tied) — loss-floor 不依
domain: clm-architecture
status: candidate-falsifier-only-math-pending
source_doc: docs/anima_clm_v5_design_spec_2026_05_07.md
source_lines: 14-46
promoted_at: 2026-05-11
linked_h: BG-IL/IO/JD/JN/JS/JT/JU/JX/KA/KB, own 19/20, Lesson L/Q
notes: BG-KB critical finding — chat-cap NOT loss-level-bound at 168M (loss 3.3-3.5, 0/5 PASS). Architectural change mandate per L9.
verified_at: 2026-05-12
verify_decision: WEAK_FALSIFIER_ONLY
verify_note: "verify_hc2 2026-05-12 — F=6"
---

## Hypothesis
CLM v4 (12L/640d/10h, vocab=11885 SP, weight-tied 11885×640) 가 chat-cap 0/5 universal FAIL — 8-lane (BG-IL through BG-KB) 모두 architectural rather than scale/corpus/objective bound. Lesson L STRICT CONFIRMED at <500M + corpus axis tested.

## Falsifiable Tests
- F1: 1B+ H100 (BG-KC) 결과 chat-cap PASS → structural claim 부분 무효 (scale axis)
- F2: v4-arch-preserving full-bundle SFT (BG-JX/JZ extended) PASS 5/5 → bottleneck 가설 무효
- F3: 다른 동일-arch ckpt 가 chat-cap PASS 보유 → arch 자체는 capable

## Migration TODO
- [ ] CLM v5 redesign mandate (L9 Growth-stage Irreversibility)
- [ ] axis A-D 별 variant 비교 (Hc_619)
