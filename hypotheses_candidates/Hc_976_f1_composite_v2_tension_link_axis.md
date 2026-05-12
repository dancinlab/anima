---
id: Hc_976
slug: f1-composite-v2-tension-link-axis
title: F1 Composite v2 — tension_link 10th explicit axis (w=0.10 dual AXIS+MEDIATOR) + 4-way joint Φ = Σw·Φ + λ·binding_strength·MAX(Φ) + binding_strength = BSE-1 Pearson cross-correlation + F1_v2 = 0.6·axis_sum + 0.3·binding + 0.1·replication
domain: composite, measurement, integration
status: candidate-falsifier-ready
source_doc: docs/strategic_f1_composite_v2_2026_05_02.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_917 (F1 v1), Hc_963 (master synthesis)
notes: "#92 honest C3 #3 — single-substrate anchored, 4-way joint Φ + binding-strength spec 부재. v2 additive supersede. RED/YELLOW/GREEN 3-tier band."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis

F1 Composite v2 framework 가 tension_link 를 10th explicit axis (w=0.10, BOTH dual role AXIS+MEDIATOR) 로 추가 + 4-way joint Φ binding-strength metric 정의: Φ_joint = Σ w_i·Φ_i + λ·binding_strength·MAX(Φ_i) (Option A_with_mod). binding_strength = BSE-1 Pearson cross-correlation. F1_v2_score = 0.6·axis_sum + 0.3·binding + 0.1·replication. Recompute: ALM 5.4% RED, CLM 16.65% RED, 4-way binding hypothetical 47.65% RED (F2 fires), 4-way + F2 unfire 52.15% YELLOW (첫 plausible).

## Sub-claims

- TENSION-LINK-AXIS: w=0.10 BOTH dual role AXIS+MEDIATOR
- PHI-JOINT: Σ w·Φ + λ·binding_strength·MAX(Φ)
- BSE-1: Pearson cross-correlation primary
- F1-v2-SCORE: 0.6·axis_sum + 0.3·binding + 0.1·replication
- BAND-3-TIER: RED/YELLOW/GREEN
- ALM-RECOMPUTE: 5.4% RED
- CLM-RECOMPUTE: 16.65% RED
- 4-WAY-BINDING-RED: 47.65% RED (F2 fires)
- 4-WAY-UNFIRE-YELLOW: 52.15% YELLOW (first plausible)

## Migration TODO

- [ ] λ binding coefficient 정량
- [ ] BSE-1 Pearson 외 alternative (mutual information, transfer entropy)
- [ ] 10 axis 각 weight 정당성
- [ ] F2 unfire 의 정확한 조건

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: F1 composite tension-link axis: factor-decompose F1. If tension-link contributes < 30% → axis not primary
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

