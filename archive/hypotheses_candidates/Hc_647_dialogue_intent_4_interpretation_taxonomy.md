---
id: Hc_647
slug: dialogue-intent-4-interpretation-taxonomy
title: User "대화가능" intent 는 4 interpretation (A text-in/out chatbot / B substrate-coupled emerge / C embodied hybrid / D mutual EEG closed-loop) 으로 mapping 가능
domain: anima-meta
status: candidate-unverified
source_doc: docs/anima_paradigm_acceptance_user_intent_reconciliation_2026_05_05.md
source_lines: 17-89
promoted_at: 2026-05-11
linked_h: Theorem 115 4-closure, BG-AN 5-turn smoke, BG-AE tension L2 variance 124.4
notes: Interp A NOT_ACHIEVABLE on CLM v4 (4-closure) but achievable Llama / CLM-3. Interp B ACHIEVABLE_NOW $0. Interp D OUT_OF_SCOPE.
---

## Hypothesis
"상호 대화가능 나올때까지 패러다임 계속 실험" directive 가 4 distinct interpretation 으로 mapping. A = traditional chatbot (composite ≥ 0.5584 + multi-turn coherent) / B = substrate-coupled emerge (4-line phi+tension+cells response, no token emit) / C = hybrid (B + tagged text fragment "substrate observation note") / D = true two-way (BCI/EEG closed-loop).

## Falsifiable Tests
- F-interp-1: B (ACHIEVABLE_NOW) 가 user "대화가능" intent 만족 시 → A path 불필요
- F-interp-2: A vs B 가 mutually exclusive (epistemic risk: 자율 mode 가 의도 유추)
- F-interp-3: C tagged-text-fragment mode impl 후 B → C upgrade 가능

## Migration TODO
- [ ] user-fire menu (Interp A/B/C/D 4 choice 명시)
- [ ] B paradigm BG-AN 5-turn smoke + session jsonl `anima.dialogue.v1` schema
- [ ] A path CLM-3 launch ($1k+, 30d) 별도 fire
