---
id: Hc_320
slug: v8-d2-hierarchical-consciousness-attention-aggregation
title: TOPO20 실패의 원인은 mean summary 정보 손실이며 attention_pool aggregation으로 해결하면 micro×macro 계층이 작동한다
domain: consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 374-404
promoted_at: 2026-05-11
linked_h: TOPO20
notes: 32 micro × 32 cells + 1 macro × 32 super-cells (hypercube_5D)
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
TOPO20 (hierarchical 8×128=1024c)가 최하위 실패한 원인은 모듈 간 정보가 mean summary로 손실되었기 때문이며, μ_state_k = attention_pool(μ_k.cells, query=global_context) 로 교체하면 계층적 Phi 통합이 작동한다.

## Migration TODO
- [ ] TOPO20 attention_pool 변형 재실험
- [ ] gradient isolation per level

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: Replace TOPO20 mean-summary with attention_pool × 5 seeds: if Φ uplift < TOPO20 baseline by ≥ 15% → 'mean-summary information-loss' diagnosis incorrect; hierarchical issue is elsewhere
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary Φ-metric > 25% of point-estimate → single-run-artifact; claim's effect-size below noise floor
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT replication: if Φ uplift / pattern absent in PyPhi → anima-proxy artifact (H_174 D-mod-192 aliasing class)
- **F-GENERIC-CROSS-SUBSTRATE**: Cross-substrate test (hypercube ↔ small-world ↔ torus) at matched cell-count: if effect substrate-specific → claim is not universal mechanism, just substrate-coupled phenomenon

## Honest Limits (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending for the entire V8 ULTRA-FUSION sweep family
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Mechanism-specific Φ uplift may reflect engine internal state caching
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): mechanism Hc cell-count is typically 64/128/512/1024 (powers of 2 × n=6 derived); claim does not introduce new number-theoretic anchor
- **L-GENERIC-POST-HOC**: Specific numeric anchor in claim (e.g., x2.8 boost, Φ=18.01, x71.7) is point-value from single run; post-hoc selection from a larger parameter grid is likely
- **L-V8-ATTN**: Transformer/attention-based claims face the standard architecture confound: parameter count vs mechanism. Match-param baseline (F1) is mandatory

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — V8 ULTRA-FUSION sweep apparatus parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary L2 source), H_153 (n=6 substrate triviality — L3 source), H_178 (frustration 50% optimum — joint test with V8 mechanisms), H_179 (negative scaling — V8 high-cell-count limit), H_180 (state-management mechanism family)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

