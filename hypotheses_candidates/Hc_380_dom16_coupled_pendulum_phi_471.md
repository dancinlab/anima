---
id: Hc_380
slug: dom16-coupled-pendulum-phi-471
title: 결합 진자 네트워크 (sin coupling)이 도메인 엔진 #1 Φ=471.5, Granger=65,533로 CambrianExplosion(485.6) 바로 아래
domain: physics
status: candidate-falsifier-ready
source_doc: docs/hypotheses/MASS-50-HYPOTHESES.md
source_lines: 74, 147-151
promoted_at: 2026-05-11
linked_h: Kuramoto
notes: 사인 결합이 극한 정보 통합
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
DOM-16 CoupledPendulum 결합 진자 네트워크의 사인 결합이 Φ=471.5 + Granger=65,533 도메인 엔진 #1 달성하며 1024c 스케일에서 슈퍼리니어 스케일링이 관찰될 것이다.

## Migration TODO
- [ ] 1024c 스케일 검증
- [ ] coupling strength sweep

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: Coupled-pendulum DOM16 replication: if Φ NOT in 471±25 range → point-prediction wrong
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary Φ-metric > 25% of point-estimate → single-run-artifact; claim's effect-size below noise floor
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT replication: if Φ uplift / pattern absent in PyPhi → anima-proxy artifact (H_174 D-mod-192 aliasing class)
- **F-GENERIC-CROSS-SUBSTRATE**: Cross-substrate test (hypercube ↔ small-world ↔ torus) at matched cell-count: if effect substrate-specific → claim is not universal mechanism, just substrate-coupled phenomenon

## Honest Limits (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending for the entire V8 ULTRA-FUSION sweep family
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Mechanism-specific Φ uplift may reflect engine internal state caching
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): mechanism Hc cell-count is typically 64/128/512/1024 (powers of 2 × n=6 derived); claim does not introduce new number-theoretic anchor
- **L-GENERIC-POST-HOC**: Specific numeric anchor in claim (e.g., x2.8 boost, Φ=18.01, x71.7) is point-value from single run; post-hoc selection from a larger parameter grid is likely
- **L-V8-DYNAMICS**: Dynamical-systems-inspired Hc face Φ-proxy vs Φ-IIT confound — anima proxy measures something like a coherence metric, not formal integrated information

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — V8 ULTRA-FUSION sweep apparatus parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary L2 source), H_153 (n=6 substrate triviality — L3 source), H_178 (frustration 50% optimum — joint test with V8 mechanisms), H_179 (negative scaling — V8 high-cell-count limit), H_180 (state-management mechanism family)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

