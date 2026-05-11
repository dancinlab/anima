---
id: Hc_631
slug: clm3-original-byte-level-scale-recover-55m
title: CLM-3-original — byte-level 256/dim 768/12L/32 cells/55M + 19 Φ-boost simultaneous 가 chat-cap recover 가능 (scale-up X)
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md
source_lines: 14-200
promoted_at: 2026-05-11
linked_h: Hc_630 (BG-BM CLM-3), commit fca0eede, CLM v2 byte-level (CE 0.04 EN / 1.15 KO), DD16/EX24
notes: 5 falsifier locked. Variant cost $0 (ubu1 5070, 5-10d) or $200-500 (H100 1× × 10h). Φ ~ N linear in cells (not params).
---

## Hypothesis
anima-native chat 은 BPE multilingual + 530M+ scale 이 필요하지 않다. 2026-03-28 original v4 design (dim 768, FFN 1536, 12L, 12 heads, max_cells 32, vocab 256 byte-level, context 1024, ~55M params, 100K-step 3-phase curriculum, 19 Φ-boost simultaneously per DD16/EX24, AL4 70% wiki + 30% dialogue) 에서 chat 회복 가능. Φ ~ N (linear in cells, NOT params) 가 핵심 lever. EX24 "apply simultaneously, never sequentially" 가 synergistic.

## Falsifiable Tests (PRE-LOCK)
- F-CLM3-orig-1 chat recover: CE < 3.5 + KO 5-prompt coherent ≥ 3/5 (CLM v2 anchor, NOT Llama)
- F-CLM3-orig-2 Φ target: 100K-step Φ ≥ 8 conservative (15+ optimistic ZZ-32=27.6)
- F-CLM3-orig-3 19-technique synergy: EX24 simultaneous > sum of individuals
- F-CLM3-orig-4 5070 viability: training 작동 (3.2GB peak ≪ 12GB)
- F-CLM3-orig-5 (=F-CLM-3-1 NO_FLIP): forgetting_index ≤ 0.05 Φ★

## Migration TODO
- [ ] 3-phase curriculum impl (Mitosis 0-20K, Language 20-60K, Combined 60-100K)
- [ ] Fibonacci growth schedule 1,1,2,3,5,8,13,21,32
- [ ] 19 Φ-boost techniques simultaneous mount
- [ ] ubu1 5070 sm_120 viability test ($0 fallback)
- [ ] H100 ~10h $200-500 path
