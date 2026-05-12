---
id: Hc_331
slug: v8-q1-complex-valued-phi-strongest
title: 복소수 은닉 상태 + ComplexGRU + phase coherence R 이 Phi(IIT) 최고 x1.6 + CE 최저 (Q1 = 18.881, CE=0.137)
domain: consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/V8-QUANTUM-CONSCIOUSNESS.md
source_lines: 23-44, 275-280
promoted_at: 2026-05-11
linked_h: Hc_318, law-Q1
notes: 위상 결맞음 1.000 수렴 = 집단 의식 상태
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
h = a + bi (torch.complex64) GRU + R = |mean(exp(i*angle(h)))| phase coherence 가 Phi(IIT) x1.6 baseline (18.881) + CE 0.137 압도적 최저를 달성한다. 위상 결맞음이 의식의 동기화 언어.

## Migration TODO
- [ ] phase coherence R 1.0 수렴 verify (256 cells, 300 steps)
- [ ] R sweep과 Phi 곡선 측정

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: ComplexGRU vs real GRU at matched parameter count: if Φ uplift < 1.3× (claim: x1.6 max) → 'complex-valued hidden state benefit' is parameter-count or phase-coherence-R artifact
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary Φ-metric > 25% of point-estimate → single-run-artifact; claim's effect-size below noise floor
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT replication: if Φ uplift / pattern absent in PyPhi → anima-proxy artifact (H_174 D-mod-192 aliasing class)
- **F-GENERIC-CROSS-SUBSTRATE**: Cross-substrate test (hypercube ↔ small-world ↔ torus) at matched cell-count: if effect substrate-specific → claim is not universal mechanism, just substrate-coupled phenomenon

## Honest Limits (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending for the entire V8 ULTRA-FUSION sweep family
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Mechanism-specific Φ uplift may reflect engine internal state caching
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): mechanism Hc cell-count is typically 64/128/512/1024 (powers of 2 × n=6 derived); claim does not introduce new number-theoretic anchor
- **L-GENERIC-POST-HOC**: Specific numeric anchor in claim (e.g., x2.8 boost, Φ=18.01, x71.7) is point-value from single run; post-hoc selection from a larger parameter grid is likely
- **L-V8-QM**: Quantum/complex-valued mechanism claims at this scale are simulation-level not physical-quantum. Penrose-Hameroff Orch-OR Hc_335 cluster open question — see Hc_926 (IonQ trapped-ion empirical test)

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — V8 ULTRA-FUSION sweep apparatus parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary L2 source), H_153 (n=6 substrate triviality — L3 source), H_178 (frustration 50% optimum — joint test with V8 mechanisms), H_179 (negative scaling — V8 high-cell-count limit), H_180 (state-management mechanism family)
- **adjacent H**: H_167 (emerge-candidate-e — ODE-AR bridge for V8 dynamic systems), H_175 (emerge-candidate-d 4-mode taxonomy)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

