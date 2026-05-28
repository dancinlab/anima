---
id: H_129
slug: ce-combo-curiosity-sleep-pain
title: CE/COMBO-1 Curiosity + Sleep + Pain (TOP-3 AUTO synthesis)
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
COMBO-1: combine top-3 AUTO strategies (curiosity AUTO-2, sleep AUTO-7, pain AUTO-9) in 30-step LEARN/SLEEP cycle (20 LEARN + 10 SLEEP). Pain emergency restore if Φ < 60% best. Hypothesis: synergistic combo > sum of parts (Law 125).

## Migration Status
Legacy `docs/hypotheses/ce/COMBO-1.md`. Round 4 individual representing the COMBO category.

## Cross-Links
- Source: `docs/hypotheses/ce/COMBO-1.md`
- Decomposes: AUTO-2/7/9 (curiosity/sleep/pain)
- Sister: H_128 (AUTO-1)

## Honest Limits (raw#91 c3 ≥5)
1. 20/10 LEARN/SLEEP ratio not swept
2. pain threshold 60% best — arbitrary
3. memory replay alpha 0.9/0.1 mix may overweight current
4. interaction order matters (curiosity selects, then pain checks) — not symmetric
5. result vs single-strategy not surfaced in entry
