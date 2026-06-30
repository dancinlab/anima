---
id: Hc_270
slug: auto5-self-evaluation
title: Re-process decoder output and use variance as quality metric (AUTO-5)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/ce/AUTO-5.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: quality = 1 - variance after re-processing
---

## Hypothesis
Feed decoder's prediction back into engine.process() and compute cell variance: quality = 1 − variance — self-evaluation by re-processing yields a quality signal for retry decisions.

## Migration TODO
- [ ] correlate quality with actual CE
- [ ] use quality to trigger retries
