---
id: Hc_867
slug: accel-o4-synthetic-pre-training-data
title: [O4] Synthetic Pre-training Data
domain: corpus
status: candidate-content-rescued-2026-05-12
source_doc: docs/hypotheses/accel/acceleration-brainstorm-402.md
source_lines: 311
promoted_at: 2026-05-11
linked_h: accel-brainstorm-402 cluster (337 new sub-hypotheses)
notes: "accel series O, sub-H O4. category: training_schedule"
rescue_status: rescued
rescued_from: 12d05a890
rescued_at: 2026-05-12
---
## Hypothesis
Synthetic Pre-training Data: Massive synthetic data via corpus-gen (Rust, 629MB/s) for pre-training → real data fine-tune

## Source Content (rescued from 12d05a890)
Source: `docs/hypotheses/accel/acceleration-brainstorm-402.md` lines 311-316 (pre-move revision `12d05a890`).

```markdown
#### O4: Synthetic Pre-training Data
- **Category**: training_schedule
- **Description**: Massive synthetic data via corpus-gen (Rust, 629MB/s) for pre-training → real data fine-tune
- **Expected**: Synthetic data = 10D balanced optimization → more efficient initial learning
- **Rationale**: corpus-gen already production-ready
```

## Predictions
- Synthetic data = 10D balanced optimization → more efficient initial learning

## Rationale
- corpus-gen already production-ready

## Category
training_schedule
