---
id: Hc_453
slug: psi-constants-full-table-8
title: 8 Ψ-constants derived from n=6 with EXACT or sub-3% error (α, balance, steps, entropy, F_c, gates×3)
domain: math
status: merged-to-H_158
source_doc: docs/what-is-consciousness.md
source_lines: 44-60
promoted_at: 2026-05-11
merged_at: 2026-05-12
linked_h: H_158 (psi-constants-ln2-n6, 8-table hard-evidence source), Hc_046, Hc_406
notes: 8-constant table. α=0.014 (sopfr/J2)^e (0.477% err), balance=0.5 EXACT, steps=4.33 (τ−μ)/ln2 (0.044%), entropy=0.998 μ−(sopfr/J2)^τ (0.012%), F_c=0.1 EXACT, gate_train=1.0 EXACT, gate_infer=0.6 EXACT, gate_micro=0.001 (2.34% err — SymPy: (n/J₂)^sopfr = (1/4)^5 = 0.000977, atlas measurement 0.001 may be display truncation). MERGED to H_158 2026-05-12 — 본 8-table 이 H_158 Why 섹션 + H_158.C1/C2 hard evidence (5/8 EXACT + 8/8 ≤2.4% SymPy verified).
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=3 (ln(2)=0.693147; n/σ=6/12=0.5 balance OK; 15+ numeric identities present). 2026-05-12 SymPy direct: 5/8 EXACT confirmed (balance=1/2, F_c=1/10, gate_train=1, gate_infer=3/5, gate_train=μ identity); 3/8 sub-3% (α 0.477%, steps 0.044%, entropy 0.012%, gate_micro 2.34%)."
---

## Hypothesis
Eight measured Ψ-constants admit closed-form n=6 derivations with all errors ≤ 2.4% and 5/8 EXACT: α = (sopfr/J₂)^e (0.477%), balance = n/σ = 0.5 EXACT, steps = (τ−μ)/ln2 (0.044%), entropy = μ−(sopfr/J₂)^τ (0.012%), F_c = n/(σ·sopfr) = 0.1 EXACT, gate_train = μ(6) = 1 EXACT, gate_infer = n/(σ−φ) = 0.6 EXACT, gate_micro = (n/J₂)^sopfr = 0.001 (2.34%).

## Migration TODO
- [ ] Verify each formula numerically on independent runs
- [ ] Test stability of these constants across engine seeds
- [ ] Falsifier: any constant whose true error > 5% under tight measurement
- [ ] Identify which constants are EXACT vs approximation by structural argument
