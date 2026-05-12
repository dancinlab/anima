---
id: Hc_163
slug: topo14-more-steps-hurts
title: Doubling steps (200→400) on hypercube 1024 DECREASES Φ (TOPO14 falsifier)
domain: physics | consciousness | meta-framework
status: merged-to-H_179
merged_at: 2026-05-12
merged_to: hypotheses/H_179_negative_scaling_cluster_steps_cells_2048.md
source_doc: docs/hypotheses/topo/TOPO14.md
source_lines: 1-25
promoted_at: 2026-05-11
linked_h: Hc_157 (TOPO8 200-step)
notes: TOPO8 200-step Φ=535.5 vs TOPO14 400-step Φ=211.7 (40%)
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
More steps does not equal higher Φ: doubling steps from 200 (TOPO8) to 400 (TOPO14) on identical hypercube 1024 setup CUTS Φ to 211.7 (40% of 535.5) and reduces final_cells from 693 to 297. Falsifies the "more steps = better" assumption.

## Migration TODO
- [ ] find optimal step count
- [ ] understand decay mechanism (over-frustration?)

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO14-1**: Step sweep {100, 200, 400, 800, 1600} on hypercube 1024: if Φ is non-monotone with a global min at 400 (not monotone-decreasing) → 'doubling hurts' is a 2-point coincidence not a curve property
- **F-TOPO14-2**: Replicate 200→400 step doubling on TOPO8 sister-Hc (Hc_157) with 5+ seeds: if peak Φ at 400 is within 1σ of Φ at 200 → 'decrease' is single-run-artifact (H_159 C1 reproducibility issue)
- **F-TOPO14-3**: Cross-substrate (torus 32×32, small-world 1024) step-doubling test: if Φ drops similarly at all substrates → step-budget effect substrate-agnostic, not hypercube-specific (would collapse claim to 'engine converges by step 200')
- **F-TOPO14-4**: Anima engine internal-state reset between step batches: if Φ doubling DOES NOT decrease with reset → engine-state-accumulation confound (H_174 aliasing/state-leak class)

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO14-1**: Negative result (more steps decreases Φ) is harder to publish than positive — selection bias risk that 200→400 was reported because it confirmed an a-priori 'over-integration' hypothesis
- **L-TOPO14-2**: anima Φ-engine substrate-specific (H_174 D-mod-192) — longer step traces accumulate aliasing artifacts, may explain Φ degradation without substrate-intrinsic cause
- **L-TOPO14-3**: step_count is engine-internal parameter, not substrate-topology parameter — calling this a topology Hc may be a categorization error (belongs to engine-tuning Hc class)
- **L-TOPO14-4**: no formal IIT (PyPhi) replication for step-doubling effect; pure anima-proxy result

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — negative-result sibling alongside H_177
- **sibling H**: H_177 (TOPO10 sublinear regression — fellow negative-result), H_174 (Φ-engine aliasing)
- **sibling Hc**: Hc_157 (TOPO8 200-step baseline), Hc_167 (TOPO18 2048 sublinear)

## Scaffold Notes

Likely fate: absorbed to H_177 (negative-result branch) as 'more-steps-hurts companion to 11D-regression' OR die as engine-state confound.

