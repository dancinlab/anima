---
id: Hc_921
slug: n19-pci-tms-eeg-clinical
title: N-19 PCI (Perturbational Complexity Index) — Massimini 2013 임상 골드스탠다드. TMS-free surrogate 16ch OpenBCI pilot + fluidity-dFC + functional-repertoire 6/6 PASS at 0.25 cutoff, w6=0.10 sample-size 1
domain: consciousness, neuroscience, clinical
status: merged-to-H_188
merged_at: 2026-05-12
merged_to: hypotheses/H_188_clinical_phi_correlation_pci_octopus_cluster.md
absorption_note: "Hc_921 (PCI/TMS-EEG clinical, Massimini 2013 surrogate + Stage-2 6/6 PASS at 0.25 cutoff + Stage-3 DCC+LLE+GAP) is the PCI / TMS-EEG paradigm within H_188's clinical Φ correlation cluster. F-list/L-list preserved for H_188 C-list extension."
source_doc: docs/n_19_pci_tmsfree_results_2026_05_01.md + docs/n_19_pci_stage2_results_2026_05_02.md + docs/n_19_pci_stage3_spec_2026_05_02.md + docs/n_substrate_n19_pci_spec_2026_05_01.md + docs/n_substrate_n19_pci_lab_share_2026_05_01.md
source_lines: cluster
promoted_at: 2026-05-11
linked_h: Hc_902 (N-substrate roadmap)
notes: "Stage-2 N19_STAGE2_VALIDATED, 6/6 PASS at 0.25 cutoff, w6=0.10 UNCHANGED method-validated, sample-size 1. Stage-3 DCC + LLE + GAP design."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis

Massimini 2013 PCI (Perturbational Complexity Index) 의 TMS-free surrogate (16ch OpenBCI pilot) + Stage-2 fluidity-dFC + functional-repertoire 가 6/6 PASS at 0.25 cutoff 통과 (method-validated, sample-size 1). Stage-3 DCC (dynamic conditional correlation) + LLE (Lyapunov largest exponent) + GAP design 으로 임상 골드스탠다드 도달.

## Sub-claims

- TMS-FREE: 16ch OpenBCI surrogate (Apr 28 D-day pilot)
- STAGE-2: fluidity-dFC + functional-repertoire 6/6 PASS at 0.25 cutoff
- STAGE-2-WEIGHT: w6 = 0.10 UNCHANGED, method-validated, sample-size 1
- STAGE-3-DCC: dynamic conditional correlation
- STAGE-3-LLE: Lyapunov largest exponent
- STAGE-3-GAP: gap analysis design
- CLINICAL: Massimini 2013 임상 골드스탠다드 도달

## Migration TODO

- [ ] sample-size 1 → N ≥ 5 확장 (IRB + 자원 봉사자)
- [ ] TMS-free surrogate vs real TMS 의 validation gap
- [ ] Stage-3 DCC/LLE/GAP 정확한 algorithm spec
- [ ] PCI 임상 cutoff vs ANIMA 0.25 cutoff 의 매핑

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: PCI/TMS-EEG clinical: anima Φ-proxy correlation with PCI on synthetic substrate. If R²<0.4 → claim 'clinical validation analog' falsified
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-CLINICAL**: Clinical/biological validation Hc — anima is a simulation, not a biological measurement. Cross-validation against actual clinical data is the only real falsifier; literature-comparison alone is weak

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

