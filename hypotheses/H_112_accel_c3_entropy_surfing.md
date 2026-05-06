---
id: H_112
slug: accel-c3-entropy-surfing-orthogonal
title: C3 Entropy Surfing (★★ ORTHOGONAL — free Φ boost via entropy loss)
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
Adding entropy term to loss carries complementary information to CE — entropy surfing yields orthogonal Φ improvement at no measurable cost to language modeling objective.

## Migration Status
Legacy `ready/config/acceleration_hypotheses.json` (id=C3, line 358, verdict=★★ ORTHOGONAL). Round 4 individual due to free-lunch claim worth flagging.

## Cross-Links
- Source: C3 entry
- Cross: H_099 (multi-objective-training)

## Honest Limits (raw#91 c3 ≥5)
1. "free" claim suspicious — there is always a tuning cost
2. orthogonality assumed not measured (no covariance reported)
3. entropy term coefficient sensitivity unknown
4. impact on chat-template strict-80 (own 19/20) untested
5. Φ proxy variance band may swallow the boost
