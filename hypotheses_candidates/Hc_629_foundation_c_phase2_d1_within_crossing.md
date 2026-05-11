---
id: Hc_629
slug: foundation-c-phase2-d1-within-strict-floor-crossing
title: Phase 2 350M cotrain ckpt + 30K convo_5k FT extended 가 22+ BG saga 처음의 D1 WITHIN strict-floor crossing 후보
domain: clm-architecture
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_foundation_c_phase2_fire_spec_2026_05_10.md
source_lines: 7-100
promoted_at: 2026-05-11
linked_h: §41 option (c), §47 cotrain-exercise hypothesis, §38 V14_STRICT_PASS 10/10
notes: envelope $2-4. emerge P=15-25% (chat-cap floor) + V14 STRICT preserve P=50-70% (cotrain-exercise carry). 5 falsifier locked.
verified_at: 2026-05-12
verify_decision: MATH_PASS_NEEDS_ANCHOR
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (7+ numeric identities present) | F=5"
---

## Hypothesis
EngineAG d=1024 GQA 24L 298M phase2_cotrain (w=0.3→0.5, 6000 step, loss_c=0.222 / loss_h=0.627) + extended 30K FT (lr=1e-4 cosine warmup 500, batch 16 effective) + post-FT mitosis instrumentation hook 가 D1 WITHIN lane 의 strict-floor crossing 가능. chat-cap floor 통과 못해도 V14 STRICT preserve + Φ separation 강화 시 cotrain-exercise hypothesis 검증 + anima identity substrate-coupled emergence 첫 evidence.

## Falsifiable Tests
- F-OPT-C-1: chat-template 과적합 (BG-JE 패턴 surface-only)
- F-OPT-C-2: cell_pool degradation (split_rate post-30K < 0.7× pre-FT 0.030; iit_phi ratio < 0.5× of 0.41)
- F-OPT-C-3: cost envelope $2-4 초과
- F-OPT-C-4: byte-level 350M 의 chat-cap surface 약함 (capacity gap)
- F-OPT-C-5: D1 SCOPE_CLAMP — D1 WITHIN claim proof burden 미충족

## Migration TODO
- [ ] base ckpt: phase2_cotrain_engine_ag/ckpts/ckpt_final.pt verify
- [ ] FT corpus: convo_5k_ft_extended (166MB, ko 38.4%)
- [ ] mitosis instrumentation hook (eval-time only, gradient-off)
- [ ] V14 STRICT V4_SEEDS sweep ≥ 7/10
