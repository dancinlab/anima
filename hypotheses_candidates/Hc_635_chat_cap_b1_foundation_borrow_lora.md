---
id: Hc_635
slug: chat-cap-b1-foundation-borrow-lora-polyglot-ko
title: B1 — Polyglot-Ko-1.3B + LoRA on BG-HK 30MB persona corpus 가 first SIMPLE_STACK_PASS
domain: clm-architecture
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_chat_cap_brainstorm_deepdive_2026_05_07.md
source_lines: 52-93
promoted_at: 2026-05-11
linked_h: BG-FY/HA/HF/HJ 18M byte-level FAILED, BG-IY F-IY-1 prereq
notes: Superseded by BG-JA-EXT post-BG-IY (corpus_mismatch F-IY-4). Lesson Q + L 종료 후 SFT 레인 reject 됨. archival reasoning.
verified_at: 2026-05-12
verify_decision: MATH_PASS_NEEDS_ANCHOR
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (6+ numeric identities present) | F=3"
---

## Hypothesis
EleutherAI/polyglot-ko-1.3b frozen + LoRA r=16/alpha=32 on q/v/o/gate/up/down_proj target + BG-HK 30MB persona_chat_template_v3 (≥80% chat-template + 100% persona prefix) SFT (lr=2e-4, batch=1, grad_accum=8, 600 steps, warmup 30) 이 V4 ≥ 7/15 stable + zero cycle + manual ≥ 10/15.

## Falsifiable Tests
- F-JC-1: V4 ≥ 7/15 + zero cycle + manual ≥ 10/15 stable ≥ 200 steps → PASS
- F-JC-2: V4 0/15 → foundation-borrow paradigm 무효 → Stage 2 fallback
- F-JC-3: V4 ≥ 5 but persona-cycle ≥ 5 → persona-prefix collapse 잔존

## Migration TODO
- [ ] Superseded by BG-JA-EXT (Polyglot-Ko-1.3B + LoRA spec at state/anima_ja_ext_polyglot_ko_lora_2026_05_07/spec.md)
- [ ] Mac MPS bitsandbytes-mps 호환성 검증
- [ ] LoRA r=16 sweep
