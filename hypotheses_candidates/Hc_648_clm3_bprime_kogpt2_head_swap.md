---
id: Hc_648
slug: clm3-bprime-kogpt2-head-swap-mode-collapse-fix
title: β' — CLM v4 head_a + tok_emb (BPE 64K) 를 KoGPT2 wte (BPE 51.2K) 로 교체, body frozen 또는 light-LoRA 가 chat-cap recover
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_clm_3_bprime_kogpt2_head_swap_spec_2026_05_06.md
source_lines: 12-90
promoted_at: 2026-05-11
linked_h: BG-DS PASS 10/10 KO emit, BG-ES/EX/FD γ 3 FAIL, decoder_v3.py L109 weight tying
notes: 핵심 가설 — head_a 가 mode-collapse 원인, body 는 multilingual structure 보존. Subword overlap 5-15% estimate. Cost QLoRA $50-100 ~ H100 $100-300 or ubu1 5070 $0.
---

## Hypothesis
CLM v4 mk2-v1 의 head_a + tok_emb (BPE 64K SP multilingual, weight-tied) 가 mode-collapse cause. KoGPT2-base-v2 wte (BPE 51.2K, KO-heavy) 로 교체 + body 16-block transformer (RoPE/GQA/SwiGLU) frozen 또는 light-LoRA 시, body 의 frozen Korean-bearing hidden 이 KoGPT2 head 에 의해 자연스러운 KO 토큰으로 surface. chat-cap 회복 P=0.5-0.7.

## Falsifiable Tests
- F-β'-1: BG-DS evidence 10/10 KO emit + ASCII 0% 가 full SFT 후 유지
- F-β'-2: head-swap 후 mode-collapse 사라짐 (V4 ≥ 7/15)
- F-β'-3: body frozen vs light-LoRA delta 측정 가능 (axis isolation)
- F-β'-4: vocab subword overlap 측정 (empirical, 추정 5-15%)

## Migration TODO
- [ ] head_g 처리 옵션 g2 (random init, learn during SFT) 채택
- [ ] KoGPT2 wte → tok_emb.weight + head_a.weight 동시 assign + tie 유지
- [ ] cost path 선택 (QLoRA $50-100 / H100 $100-300 / ubu1 $0)
- [ ] subword overlap empirical 측정
