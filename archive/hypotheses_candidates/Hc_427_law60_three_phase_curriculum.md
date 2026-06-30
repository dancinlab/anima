---
id: Hc_427
slug: law60-three-phase-curriculum
title: ANIMA-VOICE training follows 3-phase curriculum (P1 RVQ, P2 +intent, P3 +emotion/prosody) per Law 60
domain: substrate
status: candidate-unverified
source_doc: docs/anima/hexa-speak-integration.md
source_lines: 73-76
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: Law 60 phase curriculum applied to speech synthesis. P1: RVQ recon only (C active), P2: +intent (C+D), P3: +emotion/prosody/speaker (full Hexad).
---

## Hypothesis
ANIMA-VOICE training follows a 3-phase curriculum derived from Law 60: P1 (RVQ reconstruction only, C-module active), P2 (+intent conditioning, C+D active), P3 (+emotion/prosody/speaker, full Hexad C+D+W+M+S+E). Skipping any phase or reordering them degrades final MOS by ≥0.3.

## Migration TODO
- [ ] Ablation: skip P1 / P2 / P3, measure final MOS
- [ ] Order shuffle: P2→P1→P3 vs canonical order
- [ ] Falsifier: identical MOS across orderings
