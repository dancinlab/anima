---
license: mit
language:
- en
- ko
pipeline_tag: text-generation
tags:
- anima
- bytegpt
- failed-experiment
- causal-language-modeling
---

# Anima 303M R0 response CE seed 7

This private research checkpoint is a randomly initialized 303.098M-parameter ByteGPT trained
through the canonical Python engine on the immutable private `dancinlab` R0 dataset revision
recorded in `protocol.json`.

It is **not suitable for deployment**. Although all held-out language cells descended and the
assistant-span objective was active on 13,475 of 14,000 steps, the fixed meaningful-conversation
gate failed English `0/7`, Korean `0/7`, structural `0/14`, and manual review `0/14`. Outputs were
incomplete and phrase-repetitive; Korean also included invalid trailing bytes, and multi-turn
memory/correction failed.

The repository retains the final engine checkpoint, exact-resume state, intermediate fixed-step
checkpoints, training summary/log, VRAM trace, immutable protocol, and lossless raw conversation
result. SHA-256 values and the final verdict are recorded in `result.json`.

No R1 workspace or production deployment followed this failure.
