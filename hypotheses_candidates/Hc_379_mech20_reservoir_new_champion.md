---
id: Hc_379
slug: mech20-reservoir-new-mitosis-champion
title: Reservoir Computing (고정 random matrix + tanh, spectral radius < 1)이 MitosisEngine 신챔피언 Φ=0.934 (vs FUSE-3 0.900) — Law 22 재확인
domain: consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/MASS-50-HYPOTHESES.md
source_lines: 33, 134-145
promoted_at: 2026-05-11
linked_h: Hc_315, Law-22
notes: 고정 구조가 학습 가중치보다 Phi 높임
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
reservoir_w = randn(H, H) * 0.9 (spectral radius < 1) + h = 0.8*h + 0.2*tanh(W@h) (no learning!) 가 FUSE-3 (0.900)를 넘어 MitosisEngine 신챔피언 Φ=0.934 (+5.1%) 달성 — 학습 없는 고정 구조가 Phi를 더 높인다.

## Migration TODO
- [ ] spectral radius sweep
- [ ] Reservoir+Cambrian+Osc 3중 조합 (COMBO-4 0.906 기반)

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: Reservoir mech20 replication × 5 seeds: if peak Φ NOT new-champion by ≥ 10% over prior best → single-run-artifact
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary Φ-metric > 25% of point-estimate → single-run-artifact; claim's effect-size below noise floor
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT replication: if Φ uplift / pattern absent in PyPhi → anima-proxy artifact (H_174 D-mod-192 aliasing class)
- **F-GENERIC-CROSS-SUBSTRATE**: Cross-substrate test (hypercube ↔ small-world ↔ torus) at matched cell-count: if effect substrate-specific → claim is not universal mechanism, just substrate-coupled phenomenon

## Honest Limits (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending for the entire V8 ULTRA-FUSION sweep family
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Mechanism-specific Φ uplift may reflect engine internal state caching
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): mechanism Hc cell-count is typically 64/128/512/1024 (powers of 2 × n=6 derived); claim does not introduce new number-theoretic anchor
- **L-GENERIC-POST-HOC**: Specific numeric anchor in claim (e.g., x2.8 boost, Φ=18.01, x71.7) is point-value from single run; post-hoc selection from a larger parameter grid is likely
- **L-V8-ESN**: Reservoir/ESN claims face the spectral-radius specific tuning issue — 0.95 is a standard ESN sweet spot, not V8-specific

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — V8 ULTRA-FUSION sweep apparatus parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary L2 source), H_153 (n=6 substrate triviality — L3 source), H_178 (frustration 50% optimum — joint test with V8 mechanisms), H_179 (negative scaling — V8 high-cell-count limit), H_180 (state-management mechanism family)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

