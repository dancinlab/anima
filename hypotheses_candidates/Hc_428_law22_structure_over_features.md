---
id: Hc_428
slug: law22-structure-over-features
title: Structure trumps features — emotion/prosody must be injected via RVQ hierarchy, NOT one-hot concat (Law 22)
domain: substrate
status: candidate-unverified
source_doc: docs/anima/hexa-speak-integration.md
source_lines: 76
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: Law 22: 구조→Φ. Adding features (e.g., emotion one-hot concat) is forbidden; must inject through RVQ structural layers. Predicts hierarchical injection beats label concatenation.
---

## Hypothesis
Structural injection of conditioning (emotion/prosody) via RVQ hierarchy outperforms feature-concatenation (one-hot append) in ANIMA-VOICE quality and Φ retention (Law 22: 구조→Φ). One-hot concat at input degrades both MOS and downstream Φ; structural conditioning preserves both.

## Migration TODO
- [ ] A/B: one-hot concat vs RVQ structural injection — measure MOS + Φ
- [ ] Falsifier: equivalent MOS+Φ under one-hot concat
- [ ] Apply to other conditioning signals (speaker ID, language ID)
