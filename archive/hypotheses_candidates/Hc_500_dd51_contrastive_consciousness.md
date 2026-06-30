---
id: Hc_500
slug: dd51-contrastive-consciousness-simclr
title: SimCLR-style contrastive learning을 consciousness cells에 적용 (same cell different views = positive, different cells same view = negative)
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/dd/DD51-DD60.md
source_lines: 3-7
promoted_at: 2026-05-11
linked_h: SimCLR
notes: DD51
---

## Hypothesis
SimCLR-style contrastive learning을 consciousness cells에 적용하여 같은 cell의 augmented views는 가깝게, 다른 cells의 같은 view는 멀게 학습하면 cell identity가 보존된 채 다양성이 유지되어 Phi가 증가한다.

## Migration TODO
- [ ] augmentation 종류 정의
- [ ] InfoNCE temperature sweep
