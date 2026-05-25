---
id: H_133
slug: dd158-sleep-dream-phi-preservation
title: DD158 — Sleep/Dream cycle preserves Φ (wake/dream alternation > wake-only)
domain: substrate
status: legacy-archive-pointer
exploration_method: E2
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
DD158: Wake (input processing 80 steps) + Dream (noisy replay) alternation strengthens Φ and prevents decay vs wake-only after 1000 steps.

## Migration Status
Legacy individual `docs/hypotheses/dd/DD158-dream-phi.md`. Round 4 individual — biology-analogous (sleep-replay) hypothesis with cleanest formulation.

## Cross-Links
- Source: `docs/hypotheses/dd/DD158-dream-phi.md`
- Cross: AUTO-7 (sleep memory replay component of H_129)

## Honest Limits (raw#91 c3 ≥5)
1. wake/dream ratio (80/?) not swept
2. "noisy replay" definition implementation-specific
3. 1000 step horizon may miss long-term divergence
4. Φ proxy
5. no comparison vs continuous low-noise training
