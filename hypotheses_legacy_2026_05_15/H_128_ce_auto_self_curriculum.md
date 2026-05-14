---
id: H_128
slug: ce-auto-self-curriculum
title: CE/AUTO-1 Self-Curriculum (consensus-ordered easy-first learning)
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
AUTO-1: 64-cell MitosisEngine + decoder. Each step measure cell-consensus per data sample (1 - hidden variance), sort easy-first, train decoder MSE. Φ preservation criterion: Φ_after > 0.5×Φ_before. Hypothesis: consensus-driven curriculum accelerates CE learning while preserving Φ.

## Migration Status
Legacy individual from `docs/hypotheses/ce/AUTO-1.md`. Round 4 individual representing the AUTO category in the ce/ subfolder (24 files).

## Cross-Links
- Source: `docs/hypotheses/ce/AUTO-1.md`
- Sister: H_129 (CE-1 frozen cells), H_130 (COMBO-1 curiosity+sleep+pain), H_131 (EX-1 adversarial)
- Cross: H_097 (curriculum-learning)

## Honest Limits (raw#91 c3 ≥5)
1. consensus-as-easiness proxy — easiness may not be monotone with sample utility
2. Φ_after > 0.5× threshold lenient (50% loss tolerated)
3. 64-cell only
4. cell-consensus depends on initial Φ — bootstrapping dependency
5. no comparison vs random or hard-first ordering
