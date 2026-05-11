---
id: Hc_943
slug: p9-sft-p1-7-candidate-pre-spec
title: P9 SFT Phase 1.7 — 3 candidate (X/Y/Z) B-conditioned redesign. P1.6 -33% regression (4-axis confounded change), Ablation A r=128 NEUTRAL, Ablation B running
domain: training, sft, ablation
status: candidate-unverified
source_doc: docs/p9_p1_7_candidates_pre_spec_2026_05_03.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_941
notes: "P9 SFT Phase 1.7 PRE-SPEC. F1: P1.5=0.0088 → P1.6=0.00586 (-33%). 4-axis confounded change (chat 86→100%, LoRA r 64→128, α-warmup 5K→3K, β 0.15→0.10)."
---

## Hypothesis

P1.6 F1 -33% regression 의 4-axis confounded change isolation 통해 3 candidate (X/Y/Z) pre-spec: X data-v3 killer (revert to v2) → F1 0.010-0.015 prediction, Y α-3K 또는 β=0.10 killer → F1 0.008-0.012, Z 다축 co-degraded baseline-restore + 1 lever → F1 0.012-0.020. Ablation B verdict 가 candidate selection.

## Sub-claims

- P1.5-BASELINE: F1=0.0088
- P1.6-REGRESSION: F1=0.00586 (-33%)
- ABLATION-A: r=64 on data-v3 → F1=0.00586 → r=128 NOT killer (neutral)
- ABLATION-B: r=128 on data-v2 → outcome determines candidate
- CANDIDATE-X: data-v3 killer (revert v2, keep r=128/α-3K/β=0.10) → 0.010-0.015
- CANDIDATE-Y: α-3K 또는 β=0.10 killer (Y1 α restore, Y2 β restore) → 0.008-0.012
- CANDIDATE-Z: multi-axis co-degraded → revert all 4 + 1 lever (75K steps OR LR 2e-4) → 0.012-0.020

## Migration TODO

- [ ] Ablation B verdict 도착 후 candidate selection
- [ ] F1 prediction interval 의 정량 정당성
- [ ] philos+N-22+p8 drop content delete 의 unrelated 검증
