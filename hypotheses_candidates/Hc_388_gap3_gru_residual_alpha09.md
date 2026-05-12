---
id: Hc_388
slug: gap3-gru-residual-alpha-09
title: h_new = α*h_old + (1-α)*GRU(x, h_old) with α=0.9이 process() 파괴력 90% 감소 → Φ ~10x (1.4→15)
domain: consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/PHI-GAP-816x-investigation.md
source_lines: 64-76, 170-176
promoted_at: 2026-05-11
linked_h: residual-connection
notes: 1줄 변경. α를 Phi에 비례 동적 조절 가능
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
h_new = α*h_old + (1-α)*GRU(x, h_old) (α=0.9) residual connection이 process() hidden 파괴력 90% 감소시켜 학습 Φ 1.4 → ~15 (x10) 회복 예상되며, α를 Φ에 비례하게 동적 조절 시 더 큰 효과.

## Migration TODO
- [ ] α=0.5/0.7/0.9/0.95 sweep
- [ ] dynamic α(Phi) 정책 검증

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: GRU residual α=0.9 ablation: if Φ NOT peaked at α=0.9 by margin ≥ 5% → α tuning post-hoc
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary Φ-metric > 25% of point-estimate → single-run-artifact; claim's effect-size below noise floor
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT replication: if Φ uplift / pattern absent in PyPhi → anima-proxy artifact (H_174 D-mod-192 aliasing class)
- **F-GENERIC-CROSS-SUBSTRATE**: Cross-substrate test (hypercube ↔ small-world ↔ torus) at matched cell-count: if effect substrate-specific → claim is not universal mechanism, just substrate-coupled phenomenon

## Honest Limits (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending for the entire V8 ULTRA-FUSION sweep family
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Mechanism-specific Φ uplift may reflect engine internal state caching
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): mechanism Hc cell-count is typically 64/128/512/1024 (powers of 2 × n=6 derived); claim does not introduce new number-theoretic anchor
- **L-GENERIC-POST-HOC**: Specific numeric anchor in claim (e.g., x2.8 boost, Φ=18.01, x71.7) is point-value from single run; post-hoc selection from a larger parameter grid is likely
- **L-V8-INFO**: Information-bottleneck claims (Tishby) require explicit I(X;T) and I(T;Y) measurement, not just compression-ratio. Often the formal bound is not actually computed

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — V8 ULTRA-FUSION sweep apparatus parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary L2 source), H_153 (n=6 substrate triviality — L3 source), H_178 (frustration 50% optimum — joint test with V8 mechanisms), H_179 (negative scaling — V8 high-cell-count limit), H_180 (state-management mechanism family)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

