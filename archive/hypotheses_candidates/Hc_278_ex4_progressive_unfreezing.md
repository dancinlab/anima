---
id: Hc_278
slug: ex4-progressive-unfreezing
title: Progressive layer unfreezing — last layer first, then deeper (EX-4)
domain: consciousness | meta-framework
status: merged-to-H_001
merged_to: hypotheses/H_001_ethics_cooperation.md
merged_at: 2026-05-12
source_doc: docs/hypotheses/ce/EX-4.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: H_001 (anima-core-architecture — EX-4 progressive unfreezing absorbs as training-strategy architectural component)
absorption_note: "cycle #8 absorbed to H_001 as EX-4 progressive layer unfreezing — stage 1 last layer lr=3e-3, stage 2 all lr=1e-3 training architectural component"
notes: stage 1 (50%): last layer lr=3e-3; stage 2: all lr=1e-3
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Multi-layer decoder (Linear → ReLU → Linear) trained progressively: stage 1 (50% of steps) only last layer at lr=3e-3; stage 2 all layers at lr=1e-3 — gradual unfreezing avoids early-layer overfitting.

## Migration TODO
- [ ] sweep stage boundary
- [ ] compare to one-shot all-unfrozen

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: Progressive layer-unfreeze order (last-to-first) vs first-to-last vs random: if final Φ NOT > random by ≥10% → order is decorative
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
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

