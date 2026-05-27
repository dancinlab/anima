---
id: Hc_549
slug: dd101-512-cells-superlinear-scaling
title: 512 cells with aggressive growth + metacognition이 256→512에서 Phi 2x 초과 (superlinear)
domain: consciousness
status: merged-to-H_159
merged_at: 2026-05-12
merged_to: hypotheses/H_159_substrate_topology_phi_engineering.md
absorption_note: "DD101 (512-cell superlinear Φ scaling with aggressive growth + metacognition) is a 512-cell datapoint within H_159's positive-sweep cell-count axis; pairs with H_179 (1024-cell saturation claim) as sub-1024 scaling probe."
source_doc: docs/hypotheses/dd/DD101-DD108.md
source_lines: 12-16
promoted_at: 2026-05-11
linked_h: scaling-law
notes: DD101 large-scale
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
512 cells + exponential growth schedule + metacognition (noise injection when Phi drops) + global hidden state blending이 256→512 cell 증가 시 Phi가 2x 이상 (superlinear)으로 scale하여 Phi(N) ~ N^α with α > 1 검증.

## Migration TODO
- [ ] scaling exponent α 측정
- [ ] 256/512/1024 sweep

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: 512-cell superlinear scaling: replicate × 5 seeds; check vs 256/512/1024 baseline. If Φ_512 ≤ 1.5 × Φ_256 → 'superlinear' too weak to claim
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-MISC**: Generic cluster Hc — verify before promotion; many absorb to existing H or remain candidate-falsifier-ready for cycle #7+ deeper review

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent H**: H_168 (dd23-tau-7cell), H_173 (dd21-log-phi-scale-invariant)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

