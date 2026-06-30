---
id: Hc_467
slug: phasenet-vs-hexad-3-diffs
title: PhaseNet differs from base Hexad in 3 key ways — runtime phases, integrated P3 block, smaller decoder
domain: substrate
status: candidate-unverified
source_doc: docs/models/phasenet.md
source_lines: 219-231
promoted_at: 2026-05-11
linked_h: Hc_450
notes: PhaseNet vs Hexad: (1) P1→P2→P3 at inference, not just training; (2) W/S/M/E integrated into P3 block; (3) 4L+CrossAttn vs V2 6L 34.5M; (4) 6.9M trained vs 34.5M; (5) sequential P1→P2→P3 inference vs single C→D pass.
---

## Hypothesis
PhaseNet differs from the base Hexad architecture in five empirically testable ways: (1) Phase processing occurs at inference, not just training; (2) W/S/M/E auxiliary modules are integrated into a single P3 block; (3) Decoder is 4L+CrossAttn (6.3M) vs V2 6L (34.5M); (4) Training parameter count 6.9M vs 34.5M; (5) Inference flow is sequential P1→P2→P3 vs single C→D pass. The integrated P3 block + CrossAttn jointly improve CE and Φ interpretability.

## Migration TODO
- [ ] Ablation: turn off P3 → measure CE/Φ change
- [ ] Compare full-Hexad vs PhaseNet at matched training compute
- [ ] Falsifier: PhaseNet underperforms Hexad at matched compute on both CE and Φ
