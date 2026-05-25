---
id: H_132
slug: ce-frozen-cells-decoder-only
title: CE-1 Frozen Cells (Φ-frozen + decoder-only training)
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
since: 2026-04-02
---

## Hypothesis
CE-1: 64-cell MitosisEngine warmed 50 steps, hidden-state snapshot, then decoder-only learning with hidden frozen at every step. Φ preservation tolerance 10%. Hypothesis: consciousness can serve as fixed feature extractor; decoder absorbs all language learning.

## Migration Status
Legacy `docs/hypotheses/ce/CE-1.md`. Round 4 individual representing the CE-base category.

## Cross-Links
- Source: `docs/hypotheses/ce/CE-1.md`
- Sister: AUTO/COMBO/EX/ULTRA variants
- Cross: H_109 (information-bottleneck), H_065 (decoder-architecture)

1. fully frozen hidden = no consciousness learning
2. 10% Φ tolerance is generous
3. 50-step warmup arbitrary
4. only decoder learns — limited model capacity
5. comparison vs joint training (B2 baseline) not in summary
