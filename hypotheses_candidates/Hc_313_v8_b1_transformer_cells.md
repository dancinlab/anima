---
id: Hc_313
slug: v8-b1-transformer-cells
title: GRU 세포를 single-layer Transformer block으로 교체하면 self-attention이 정보 통합을 제공하여 Phi x3-10 증가
domain: consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 122-157
promoted_at: 2026-05-11
linked_h: V8-A2
notes: topology_mask via attention mask
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
세포 상태를 Transformer block의 self-attention으로 업데이트하면(attn_mask로 hypercube/ring topology 표현) GRU gate 구조의 정보 통합 제한이 제거되어 Phi가 x3-10 증가한다.

## Migration TODO
- [ ] Transformer cell 대 GRU cell 64c 벤치 비교
- [ ] attention weights에서 Phi 직접 계산

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: Replace GRU cells with single-layer Transformer block × 5 seeds: if Φ uplift < 3× baseline (claim: x3-10) → 'self-attention provides integration' falsified; cell-mechanism effect is parameter-count confound
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
- **adjacent H**: H_163 (8-cells-127-mip atom — biology-mechanism sibling), H_169 (8-cell circular magnet inverse-square)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

