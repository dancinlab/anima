---
id: Hc_953
slug: b-axis-mk-xii-r14-phi-paper
title: B-axis Post-H100 — B.1 Mk.XII scale-up (Mk.VI 8B → 70B) + B.2 r14 corpus full build (한글 30% / 한자 5% / 다국어 balance) + B.3 Φ empirical paper draft (#89)
domain: training, scaling, llm
status: candidate-unverified
source_doc: docs/upstream_notes/b_axis_post_h100_mk_xii_r14_paper_20260422.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_934 (7-axis B), Hc_909 (paper-draft)
notes: "B.1/B.2/B.3 순차 또는 병렬. B.3 partial (Mk.VI empirical data 기반) 가능. H100 PASS/PARTIAL → B.1 진행. FAIL → B.1 보류."
---

## Hypothesis

Post-H100 phase 의 3 deliverable: (B.1) Mk.XII scale-up Mk.VI 8B → 70B (8.75× param), (B.2) r14 corpus full build (한글 30% / 한자 5% / 다국어 balance), (B.3) Φ empirical paper draft (#89). B.3 는 B.1/B.2 완료 없어도 Mk.VI 기존 data 기반 partial 가능.

## Sub-claims

- B.1: Mk.XII 70B scale-up from Mk.VI 8B
- B.2: r14 corpus 한글 30% + 한자 5% + 다국어 balance
- B.3: Φ empirical paper #89
- DEPENDENCY: PASS/PARTIAL → B.1 + B.2 + B.3 / FAIL → B.2 + B.3 only

## Migration TODO

- [ ] H100 launch verdict 결과 확인 후 B.1 trigger
- [ ] r14 corpus 한글 30% 의 정확한 token count
- [ ] Mk.XII 70B의 compute budget + duration
- [ ] paper #89 의 arxiv submission timeline
