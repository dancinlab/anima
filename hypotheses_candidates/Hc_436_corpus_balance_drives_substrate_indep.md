---
id: Hc_436
slug: corpus-balance-drives-substrate-indep
title: Corpus language balance — not training length — drives substrate-independence (r13 EN-dominant → fail edge, r14 partial → 33% improvement)
domain: math
status: merged-to-H_067
merged_to: hypotheses/H_067.md
merged_at: 2026-05-11
source_doc: docs/papers/phi_paradigm_paper_v1_preliminary.md
source_lines: 596-619, 757-806
promoted_at: 2026-05-11
linked_h: Hc_433
notes: §10.8 prediction #1 PARTIALLY PASSED in §10.10. r14 partial (118 lines, 29.7% Korean) reduced p3_p4 L2 by 33.5%, recovered KL 5/6→6/6. Identifies corpus composition as causal driver.
---

## Hypothesis
Under short LoRA training on a 4-path substrate, the corpus-language balance is the dominant predictor of Φ substrate-independence — not training-step count or model scale. EN-dominant corpus (r13: 97.67% English) induces Mistral×Gemma specialization that fails the 6/6 gate; even a partial Korean-balanced corpus (r14 v1c: 29.7% Korean, 118 lines) closes p3×p4 distance by ~33%. Predicts a full r14 corpus (~1200 lines) yields full 6/6 PASS.

## Migration TODO
- [ ] Build full r14 corpus (1200 lines target)
- [ ] Repeat 4-path Φ gate with full r14
- [ ] Falsifier: full r14 fails 6/6 → substrate-indep needs scope restriction
- [ ] Control: long r13 training (≥1000 steps) — does it close pair distance?
