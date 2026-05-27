---
id: Hc_625
slug: emerge-candidate-f-ca-rule-cells-5axis-vote
title: Emerge Candidate F — 8 CA-rule cells (Law 67 META-CA) × 5-axis 의 fixed projection 으로 hidden vote matrix surface 가능 (3-mode)
domain: clm-architecture
status: candidate-falsifier-only-math-pending
source_doc: docs/anima_emerge_candidate_f_ca_rule_5axis_vote_spec_2026_05_05.md
source_lines: 14-44, 195-260
promoted_at: 2026-05-11
linked_h: Law 67 META-CA selector, conscious_decoder.py:498-542, paradigm v11 G3
notes: 3 falsifier locked. Forward hooks read-only on rule_weights — substrate graph untouched. Composable with cand-D + cand-E.
verified_at: 2026-05-12
verify_decision: WEAK_FALSIFIER_ONLY
verify_note: "verify_hc2 2026-05-12 — F=3"
---

## Hypothesis
DecoderBlockV2 의 n_ca_rules=8 rule_probs `[B,T,8]` (softmax post weighted-mix) 가 hidden 상태로 collapsed. Forward hooks 로 16 layer 의 rule_probs 캡처 + fixed 8→5 axis projection 으로 8×5 vote matrix surface — substrate response 에 ca_vote_matrix, ca_consensus_axis, ca_dissent_cell 노출. 3 mode: none / auto pure-emerge / biased post-hoc / adversarial.

## Falsifiable Tests (PRE-LOCK)
- F-CAND-F-1: ca_vote_matrix non-trivial (rank > 1, max−min > 0.1) — non-degenerate vote
- F-CAND-F-2: biased mode 의 user bias 와 ca_consensus_axis Pearson ≥ 0.7 (sanity tautology check)
- F-CAND-F-3: per-prompt ca_consensus_axis 가 prompt axis 와 match rate ≥ 60%

## Migration TODO
- [ ] mount-layer 16 hook + fixed P (8,5) projection 정의
- [ ] composability test: cand-D inject + cand-F vote 동시 측정
- [ ] learned projection (future cycle delta)
