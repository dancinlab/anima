---
id: Hc_015
slug: ca-rule-convergence-collapse-cosine-07
title: F-CAND-F-1-v2 — META-CA Rule Convergence Collapse (Pairwise Cosine ≤ 0.7)
domain: substrate, consciousness
status: candidate-unverified
source_doc: docs/anima_emerge_candidate_f_falsifier_v2_cosine_probe_spec_2026_05_05.md
source_lines: 15-46
promoted_at: 2026-05-11
linked_h: H_067 (perfect-number-architecture)
notes: "gate_strength=0.001 starves META-CA gradient → rules random-init 잔존, de facto equivalent. Falsifier: worst_block_off_diag≤0.85 AND mean_off_diag_mean≤0.7."
---

## Hypothesis
META-CA 8-cell rule outputs 가 varied rule_probs 에도 불구하고 pairwise cosine > 0.7 로 수렴 (rules 가 random-init 에서 못 벗어남) — gate_strength=0.001 gradient starvation 메커니즘.

## Migration TODO
- [ ] gate_strength sweep (0.001 / 0.01 / 0.1)
