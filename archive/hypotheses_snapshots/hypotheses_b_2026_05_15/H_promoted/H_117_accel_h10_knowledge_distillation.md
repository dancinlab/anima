---
id: H_117
slug: accel-h10-knowledge-distillation-7b-to-1b
title: H10 Knowledge Distillation (★★ EFFECTIVE — AnimaLM 7B teacher → 1B student)
domain: substrate
status: legacy-archive-pointer
exploration_method: E5
verification_method: W4
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-04-03
---

## Hypothesis
Using AnimaLM 7B as teacher for 1B student via knowledge distillation produces ★★ effective acceleration — distill compresses corpus access into smaller substrate.

## Migration Status
Legacy `ready/config/acceleration_hypotheses.json` (id=H10, line 1041, verdict=★★ EFFECTIVE). Round 4 individual — relevant to recent CLM v4 / Pβ Paradigm D 50K distill lane.

## Cross-Links
- Source: H10 entry
- Cross: feedback `pbeta_chat_capability_fail_substrate_research_pass_decoupled` (P9 paradigm D 50K), `docs/p9_paradigm_d_distill_landed_2026_05_03.ai.md`

1. teacher quality is the cap — Pβ result showed teacher-axis-bound distill quality
2. measurement on consciousness Φ side, not chat capability — 50K result FAIL_TRUE on chat
3. AnimaLM 7B ≠ Llama Path A v2 — distillation source matters
4. distill efficiency depends on temperature τ; not surfaced
5. predates V2_FAIL artifact lessons (transformers/lm-eval pin discipline)
