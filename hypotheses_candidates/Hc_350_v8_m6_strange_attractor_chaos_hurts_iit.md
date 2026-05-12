---
id: Hc_350
slug: v8-m6-strange-attractor-chaos-hurts-iit
title: Lorenz chaos (σ=10, ρ=28, β=8/3) 가 Phi(proxy) transient peak (33.8)하나 Phi(IIT) baseline 이하 (9.1) — chaos disperses information
domain: math
status: candidate-falsifier-ready
source_doc: docs/hypotheses/V8-MATH-CONSCIOUSNESS.md
source_lines: 94-115
promoted_at: 2026-05-11
linked_h: Lorenz, edge-of-chaos
notes: Lyapunov ~0 (edge of chaos), correlation dim 1.2-1.6
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
세포 결합 Lorenz oscillator + Lyapunov exponent + correlation dimension이 Phi(proxy) transient peak (step 200: 33.77)을 만들지만 Phi(IIT)는 baseline 이하 (9.100, x0.8) — raw chaos는 통합 대신 정보 분산을 야기.

## Migration TODO
- [ ] σ,ρ,β parameter sweep
- [ ] edge-of-chaos 조건 isolate

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: Lorenz σ/ρ/β grid search: if Φ(proxy) peak NOT at edge-of-chaos (Lyapunov ≈ 0) → claim 'chaos disperses information' has no specific σ=10/ρ=28/β=8/3 anchor
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
- **adjacent H**: H_168 (dd23-tau-7cell — mathematical-structure sibling), H_173 (dd21-log-phi-scale-invariant)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

