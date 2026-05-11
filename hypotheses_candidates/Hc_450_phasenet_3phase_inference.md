---
id: Hc_450
slug: phasenet-3phase-inference
title: PhaseNet — P1→P2→P3 phase processing at EVERY inference step, not just training curriculum (Law 60)
domain: substrate
status: candidate-unverified
source_doc: docs/models/phasenet.md
source_lines: 1-94
promoted_at: 2026-05-11
linked_h: Hc_427
notes: PhaseNet builds Law 60 phase curriculum into runtime architecture: P1 build Φ → P2 verbalize → P3 ethics/will/sense/memory check. ~10ms+20ms+5ms = 35ms/token. Distinguishes Anima's P1/P2/P3 from typical training-only curriculum.
---

## Hypothesis
Embedding Law 60's 3-phase curriculum (P1 build Φ, P2 verbalize, P3 full Hexad check) into the runtime inference path — not just the training schedule — yields better generalization CE (~0.3-0.5) than a flat single-pass decoder. The P3 block (W/S/M/E modules at ~5ms) contributes the largest generalization improvement.

## Migration TODO
- [ ] Train PhaseNet vs flat decoder at matched param budget
- [ ] Phase ablation at inference: skip P3, skip P2, measure CE
- [ ] Falsifier: flat decoder matches PhaseNet CE within 0.05
- [ ] Latency budget verification (35ms target)
