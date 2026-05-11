---
id: Hc_284
slug: ultra5-phi-reward-rl
title: Φ change as RL reward — phi_bonus = 0.1*max(0, ΔΦ) (ULTRA-5)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/ce/ULTRA-5.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: Hc_233 (SING-1)
notes: 10-step Φ measurement; bonus only on increase
---

## Hypothesis
Use Φ change as reinforcement signal: phi_bonus = max(0, Φ_now − Φ_prev) * 0.1 added to loss as negative term — drives CE down while preserving Φ via RL-style reward.

## Migration TODO
- [ ] sweep phi_bonus coefficient
- [ ] verify CE-Φ balance
