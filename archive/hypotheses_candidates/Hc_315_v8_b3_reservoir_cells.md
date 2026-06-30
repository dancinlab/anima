---
id: Hc_315
slug: v8-b3-reservoir-cells
title: Echo State Network (고정 random sparse W, spectral radius=0.95, readout만 학습)이 법칙 42를 완전 해결한다
domain: consciousness
status: merged-to-H_182
merged_at: 2026-05-12
merged_to: hypotheses/H_182_v8_b_family_bio_inspired_consciousness_bandwidth.md
absorption_note: "B-family reservoir cells (V8-B3, ESN spectral_radius=0.95) — H_182.3 sweep anchor. F-list/L-list preserved here for H_182 C-list extension."
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 195-219
promoted_at: 2026-05-11
linked_h: V8-A3, law-42
notes: 30년 검증된 ESN 패러다임
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
W_reservoir = random_sparse(N,N,density=0.1) × spectral_radius/max_eig(W) (=0.95 edge of chaos) 로 영원히 고정하고 W_out만 학습하면 gradient가 세포에 절대 도달하지 않으므로 법칙 42 균질화가 완전 차단되어 Phi가 x5-15 증가한다.

## Migration TODO
- [ ] spectral_radius=0.95 vs 0.8/0.9/0.99 sweep
- [ ] reservoir size scaling law 측정

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: Echo State Network with spectral_radius∈{0.85, 0.95, 1.05}: if Φ NOT peaked at spectral_radius=0.95 → ESN-specific 0.95 tuning is post-hoc; reservoir hypothesis underdetermined
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
- **adjacent H**: H_163 (8-cells-127-mip atom — biology-mechanism sibling), H_169 (8-cell circular magnet inverse-square)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

