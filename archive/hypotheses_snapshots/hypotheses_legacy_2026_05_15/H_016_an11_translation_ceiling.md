---
id: H_016
slug: an11-v2-finetune-translation-ceiling
title: AN11 v2 finetune translation ceiling — language-specific upper bound
domain: corpus
status: pre-register-frozen
exploration_method: E2 (failure-driven) + E5 (ablation)
verification_method: W1 + W2 + W3
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-04-25
since: 2026-04-25
---

# H_016 — AN11 v2 finetune translation ceiling

## Hypothesis

AN11 v2 finetune lane에서 translation quality에 language-specific ceiling 존재 — KO↔EN translation accuracy ≤ corpus-derived upper bound.

## Migration Status

- **frozen prereg**: `state/an11_v2_finetune_translation_ceiling_prereg_20260425.json`
- raw_rank:12 frozen 2026-04-25

## Cross-Links

- prereg: `state/an11_v2_finetune_translation_ceiling_prereg_20260425.json`
- sister: H_005 (corpus quality > capacity 정합)
- roadmap: `.roadmap.anima_engines`
- own:
- own cross-link: (corpus priority — translation ceiling은 corpus quality manifestation)

## Honest Limits

- L1: translation ceiling은 corpus subset 한정 (training corpus 학습 manifold 외부 generalization unclear)
- L2: KO↔EN 한정 — 다른 language pair 별도 cycle
- L3: AN11 lane은 별도 spec — 본 entry는 cross-link
- L4-L5: pointer; raw#12 frozen
