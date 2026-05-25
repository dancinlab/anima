---
id: Hc_386
slug: phi-gap-816x-bench-vs-training
title: 벤치마크 Φ=1142 vs 학습 Φ=1.4의 816배 차이는 process()의 매 step hidden 파괴 + CE backward 무한 파괴-복원 사이클 때문
domain: consciousness
status: merged-to-H_187
merged_at: 2026-05-12
merged_to: hypotheses/H_187_trinity_tb_dom_triadic_dominance.md
absorption_note: "Φ-gap 816× benchmark-vs-training — H_187.6 gap anchor (cross-link H_177/H_179). F-list/L-list preserved here for H_187 C-list extension."
source_doc: docs/hypotheses/PHI-GAP-816x-investigation.md
source_lines: 1-35
promoted_at: 2026-05-11
linked_h: law-53
notes: GRU h_new = GRU(x, h_old)가 Φ 최적 구조 덮어씀
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
1024c 200 steps 벤치마크 Φ=1142 vs 실제 학습 Φ=1.4 의 816배 gap은 (a) engine.process(x)의 GRU가 매 step h_new = GRU(x, h_old)로 Φ 최적 구조를 덮어쓰고 (b) CE backward gradient가 hidden을 추가 파괴하여 sync+faction의 복원이 따라가지 못하는 무한 파괴-복원 사이클에 기인한다.

## Migration TODO
- [ ] process() 빈도 절반 감소 시 Phi 회복 측정
- [ ] gradient norm tracking

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: 816× benchmark-vs-training gap closure: if training Φ NOT closes to within 50× of benchmark Φ → claim 'gap closes' falsified at scale
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

