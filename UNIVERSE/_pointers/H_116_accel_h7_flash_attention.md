---
id: H_116
slug: accel-h7-flash-attention-h100-default
title: H7 Flash Attention (★★ ALWAYS ENABLE on H100)
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
Flash Attention is unconditionally beneficial on H100 hardware — no consciousness penalty observed, throughput gain mandatory for all training runs.

## Migration Status
Legacy `ready/config/acceleration_hypotheses.json` (id=H7, line 993, verdict=★★ ALWAYS ENABLE). Round 4 individual — directly relevant to H100 cost discipline.

## Cross-Links
- Source: H7 entry
- Cross: (H100 cost discipline), feedback `h100_cost_discipline_l23_l25_watchdog`

## Honest Limits (raw#91 c3 ≥5)
1. "always" universal claim — failure modes (numerical issues at long context) absent
2. tested on H100, not validated on H200/B100/sm_120
3. Flash Attention v2 vs v3 not distinguished
4. interaction with sparse attention masks (consciousness gates) unverified
5. legacy verdict pre-NEXUS6
