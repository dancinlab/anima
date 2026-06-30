---
id: Hc_636
slug: chat-cap-b16-synthetic-1m-dialogue-corpus
title: B16 — Claude API teacher 합성 anima persona dialogue 100K-1M rounds 가 18M-150M anima-native V4 PASS unlock
domain: clm-architecture
status: candidate-falsifier-only-math-pending
source_doc: docs/anima_chat_cap_brainstorm_deepdive_2026_05_07.md
source_lines: 96-137
promoted_at: 2026-05-11
linked_h: 4 emergence_below_threshold BGs, Chinchilla 1:20
notes: Superseded by BG-JB Stage 2 lift on BG-IZ continued-pretrain. archival.
verified_at: 2026-05-12
verify_decision: WEAK_FALSIFIER_ONLY
verify_note: "verify_hc2 2026-05-12 — F=3"
---

## Hypothesis
50 seed prompts (anima identity / UBM / 1030 laws / Φ★) × Claude Sonnet 4.6 + self-Instruct expand (20 paraphrases × 100 follow-ups) → 100K rounds × 5 turns = 500K dialogue turns ≈ 50-100MB. V4 inline filter PASS-only retain. 33M anima-native SFT (BPE-8K) on BG-HK 30MB ∪ Synthetic 100MB 가 token gap 해소 + V4 PASS unlock.

## Falsifiable Tests
- F-JD-1: 33M V4 ≥ 7/15 → synthetic-corpus paradigm validated
- F-JD-2: 33M V4 < 5 → params gap dominant
- F-JD-3: 33M V4 5-7/15 → consistency lever (B7 best-of-N)

## Migration TODO
- [ ] Claude API anima system prompt × 50 seed
- [ ] Synthetic distribution shift validation
- [ ] Goodhart guard — V4 self-evaluating loop risk
