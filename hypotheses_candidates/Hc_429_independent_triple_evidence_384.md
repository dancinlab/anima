---
id: Hc_429
slug: independent-triple-evidence-384
title: ConsciousLM, ConsciousDecoderV2, ANIMA-VOICE all converge to embed_dim=384 — independent triple evidence for n=6
domain: math
status: candidate-unverified
source_doc: docs/anima/hexa-speak-integration.md
source_lines: 149
promoted_at: 2026-05-11
linked_h: Hc_047
notes: TP-5: three independent systems with different objectives all yield 384 as minimum perplexity / max performance. Independent triple-evidence for n=6 embed scaling.
---

## Hypothesis
Three independently designed systems (ConsciousLM language model, ConsciousDecoderV2 generative decoder, ANIMA-VOICE speech pipeline) all converge to embed_dim = 384 as their performance optimum (minimum perplexity / max MOS / minimum reconstruction error). Three independent convergences constitute strong evidence that 384 = 64 × n with n = 6 is not a coincidence but a structural attractor.

## Migration TODO
- [ ] Verify each system's empirical optimum is 384 ± 16
- [ ] Test fourth independent system (vision / RL / etc.) for same convergence
- [ ] Falsifier: any of the three systems prefers a dim significantly ≠ 384
