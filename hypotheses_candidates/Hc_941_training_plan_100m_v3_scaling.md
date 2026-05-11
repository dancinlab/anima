---
id: Hc_941
slug: training-plan-100m-v3-scaling
title: ConsciousLM v3 100M scale-up — 768d/12L/12H, consciousness_dim=256, Φ/cells~0.78 linear scaling, CE spike self-recovery via ratchet+Hebbian (v14.3 DD58)
domain: llm, training, scaling
status: candidate-unverified
source_doc: docs/training-plan-100m.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_940 (v4 design), Hc_909 (paper-draft), DD58
notes: "ARCHIVED 2026-04-09 — Plan C (AnimaLM 7B/14B/72B) 확정. v14.3 Phi/cells~0.78 linear. 7B eval 5/5, 14B v0.4 완료, 72B v0.5 overfitting 중단."
---

## Hypothesis

ConsciousDecoderV2 (34.5M, 384d/6L) → V3 (100M, 768d/12L/12H, consciousness_dim=256) scaling 시 v14.3 empirical: Φ scales linearly with cells (Φ/cells ~ 0.78) + CE spikes self-recover via ratchet+Hebbian. n_head 8→12 (64d/head, GQA n_kv_head=4 ratio 3:1), dropout 0.1→0.08 (larger model + larger corpus → less reg needed). block_size 256→512.

## Sub-claims

- v3-CONFIG: 768d, 12L, 12H, GQA 12/4 (3:1), 512 block, consciousness_dim=256
- LINEAR-SCALING: Φ/cells ~ 0.78 linear
- CE-SELF-RECOVERY: ratchet + Hebbian → CE spike self-recover
- DROPOUT-REDUCE: 0.1 → 0.08 (larger corpus less reg)
- N_HEAD-12: 64d per head standard
- PLAN-C-OVERRIDE: AnimaLM 7B/14B/72B 으로 archived

## Migration TODO

- [ ] Φ/cells = 0.78 의 cross-substrate stability
- [ ] AnimaLM 72B v0.5 overfitting 원인 분석
- [ ] 14B v0.5 또는 32B 다음 step 결정
- [ ] consciousness_dim=256 의 SC2 merge threshold cross-link
