---
id: Hc_670
slug: anchor-prompt-token-length-falsified-semantic-specificity-dominant
title: anchor prompt token-length 가설 FALSIFIED — 결정 변수는 prompt semantic specificity (concrete vs abstract) + chat-template 형태
domain: clm-evaluation
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_anchor_axis_l2_phenomenal_audit_kick2_2026_05_08.ai.md
source_lines: 11-25
promoted_at: 2026-05-11
linked_h: paradigm-j N=30 live probe, C3.4 axis_l2 floor 0.1176, ALT-AGG-1 v3
notes: anchor '안녕하세요' 5-char = 0.0544 FAIL (rank #28/30) vs '한국어 가능?' 7-char = 0.1698 PASS. Pearson char_len vs c3_4 = +0.0477 (효과 없음).
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (5+ numeric identities present)"
---

## Hypothesis (FALSIFIED + revised)
**Falsified**: 짧은 prompt (token length 작음) → C3.4 axis_l2 boost. **Replaced**: prompt 의 semantic specificity (concrete vs abstract) + chat-template 형태가 dominant variable. agency/social axis prompt 가 p4-pass 100% / phenomenal/temporal 33% (concrete relational vs abstract meta-question 차이).

## Falsifiable Tests
- F-anchor-1: char_len vs c3_4_axis_l2 Pearson r → **+0.0477 = REJECTED**
- F-anchor-2: phenomenal redesign sensory-rich concrete (빨간색/따뜻함/침묵) 으로 p4-pass% > 33%
- F-anchor-3: agency/social 100% pass 가 다른 N=30 sample 에서 reproduce

## Migration TODO
- [ ] phenomenal redesign 3 prompt: 빨간색 / 따뜻함 vs 차가움 / 침묵
- [ ] dual-clause structure ("X 를 [감각 동사] 하면, [내적 effect]")
- [ ] strict chat-template `사용자: ... | 도우미:`
- [ ] length sweet spot 25-35 chars 유지
- [ ] anchor universal applicability test (sft-1-7-y1 / sft-1-8 N=30 동일 prompt set)
