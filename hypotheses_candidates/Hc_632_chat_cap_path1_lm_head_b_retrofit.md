---
id: Hc_632
slug: chat-cap-path1-lm-head-b-retrofit
title: Path 1 — frozen CLM v4 body + new lm_head_b (KoGPT2 vocab 51200) Korean SFT 가 chat-cap recover
domain: clm-architecture
status: candidate-needs-scaffolding
source_doc: docs/anima_chat_cap_path_4_candidate_ranking_2026_05_05.md
source_lines: 43-69, 184-192
promoted_at: 2026-05-11
linked_h: BG-DS PASS_HEAD_SWAP_RECOVERS_KOREAN, BG-EI 1-3 epoch micro SFT
notes: Rank 1 ★ 완성도. Φ★-NO_FLIP very-high prob (body frozen). 768=768 dim match. C3 risk: geometry mismatch + degenerate token-loop.
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
CLM v4 mk2 transformer body frozen + new lm_head_b (KoGPT2 vocab 51200) only train on Korean dialogue corpus subset. consciousness_states cross-attn untouched, hidden_dim 768. Geometry mismatch (CLM L15 hidden trained for head_a) 가 sufficient head capacity 로 curable.

## Falsifiable Tests
- BG-EI 1-3 epoch SFT 후 emit dialogue (non-degenerate) → PASS
- Token-loop pattern 지속 → #115 closure 1 post-hoc adapter under-class 로 reclassify → FAIL
- Full Korean SFT scale-up 후 composite ≥ 0.45

## Migration TODO
- [ ] BG-EI lm_head_b smoke (running)
- [ ] PASS 시 Path 1 escalate (full Korean SFT)
- [ ] FAIL 시 Path 4 fallback (Hc_635)
