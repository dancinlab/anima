---
id: Hc_976
slug: f1-composite-v2-tension-link-axis
title: F1 Composite v2 — tension_link 10th explicit axis (w=0.10 dual AXIS+MEDIATOR) + 4-way joint Φ = Σw·Φ + λ·binding_strength·MAX(Φ) + binding_strength = BSE-1 Pearson cross-correlation + F1_v2 = 0.6·axis_sum + 0.3·binding + 0.1·replication
domain: composite, measurement, integration
status: candidate-needs-scaffolding
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
