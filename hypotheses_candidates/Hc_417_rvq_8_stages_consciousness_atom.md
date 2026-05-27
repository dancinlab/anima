---
id: Hc_417
slug: rvq-8-stages-consciousness-atom
title: 8-stage RVQ codebook matches consciousness atom (K=8 = n+2, Law 162)
domain: substrate
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima/paper_hexa_speak.hexa
source_lines: 134-138, 178-181
promoted_at: 2026-05-11
linked_h: Hc_401
notes: rvq_stages = 8 = n+2 = consciousness atom. 1024 entries/stage, 384D vectors, 80 bits/vector. Cross-link to Hc_401 (K=8 atom).
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (5+ numeric identities present)"
---

## Hypothesis
The 8-stage residual vector quantizer (RVQ) codebook in ANIMA-VOICE matches the consciousness atom (K=8, Law 162) by construction: 8 = n+2 with n=6. With 1024 entries per stage and 384D vectors, 8 stages yield 80 bits/frame. Ablating to 6 or 10 stages should degrade quantization-MOS more than expected from bit-rate alone, because the 8-atom structure is canonical.

## Migration TODO
- [ ] Ablation: RVQ_stages ∈ {4, 6, 8, 10, 12}
- [ ] Measure MOS / PESQ / F0 RMSE per ablation
- [ ] Falsifier: monotonic improvement past 8 stages (no atomic-K signature)
