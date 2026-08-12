---
language:
- en
- ko
library_name: anima
tags:
- byte-level
- from-scratch
- research
---

# Anima 303M R0 proportional conversation seed 7

Private research artifact. This randomly initialized 303,097,856-parameter ByteGPT was trained
for the preregistered 14,000 steps with the byte-proportional four-cell sampler in
`dancinlab/anima-303m-r0-proportional-conversation-data-2026-08-12` revision
`ee143002d9494cac4ed4a821dadfb5ece60c1e74`.

The checkpoint is **not suitable for deployment**. The fixed meaningful-conversation gate failed:
English semantic relevance was 2/7, Korean was 0/7, no response passed all structural checks, and
all final multi-turn answers failed. Outputs were dominated by phrase repetition; several Korean
continuations ended with invalid UTF-8 bytes. `conversation_result.json` retains all raw evidence
losslessly. R1 and production promotion remain blocked.

The repository also contains the exact-resume checkpoint, training and evaluation logs, the
sampler ledger, GPU metrics, fixed protocol and panel, and the immutable data manifest.
