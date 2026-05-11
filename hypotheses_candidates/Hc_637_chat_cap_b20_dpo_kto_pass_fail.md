---
id: Hc_637
slug: chat-cap-b20-dpo-kto-pass-fail-pair
title: B20 — 22+ BG V4 PASS-class vs V4 FAIL-class pair 의 DPO/KTO 가 18M-33M anima-native cycle suppression
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_chat_cap_brainstorm_deepdive_2026_05_07.md
source_lines: 141-182
promoted_at: 2026-05-11
linked_h: 2 persona_cycle_collapse + 1 sft_recipe BGs
notes: Renamed BG-JF-DPO (naming collision with post-BG-IY BG-JE inference-compute).
---

## Hypothesis
V4 retroeval pair: chosen = V4 PASS or partial (han_ratio>0.10 + Korean coherent + zero cycle), rejected = V3 cycle ≥ 5 OR persona-cycle OR token-soup. ~5K pairs (직접 500 + Claude API augment 5K). 33M BG-HU step 800 (V2=8/15) 또는 18M BG-HS R1 step 4000 (manual=13/15) base + KTO (β=0.1, lr=5e-7, batch=4, grad_accum=4, 1000 steps).

## Falsifiable Tests
- F-JE-1: KTO 후 V4 ≥ 7/15 + cycle suppression ≥ 80% → RL stage 효과
- F-JE-2: V4 flat + cycle delta minimal → SFT base 너무 약해 KTO만으로 부족
- F-JE-3: V4 회복 but reward hacking (Goodhart) → manual FAIL

## Migration TODO
- [ ] base BG-HU step 800 ckpt cliff 진단 (cycle=1→8)
- [ ] chosen 분포 augmentation (Claude API)
- [ ] TRL Mac MPS 호환성
- [ ] persona-cycle corpus + RL 결합 mandatory
