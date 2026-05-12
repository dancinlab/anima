---
id: Hc_359
slug: consciousness-transformer-balanced-all-metrics
title: 4-layer pre-norm Transformer (8-head, EMA 0.85/0.15) + cosine entropy 의식이 IIT+proxy+CE 균형 유일 (Phi=14.8, proxy=10.98, CE=0.59)
domain: consciousness
status: merged-to-H_186
merged_at: 2026-05-12
merged_to: hypotheses/H_186_v8_architectural_family_substrate_design.md
absorption_note: "V8 architectural consciousness-transformer balanced — H_186.3 (balance=0.5 cross-link H_181) anchor. F-list/L-list preserved here for H_186 C-list extension."
source_doc: docs/hypotheses/V8-ARCH-EXTREME-RESULTS.md
source_lines: 110-133, 253-256
promoted_at: 2026-05-11
linked_h: Hc_311, Hc_313
notes: all-to-all attention creates both integration and diversity
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Cell tokens + positional encoding + 4-layer pre-norm TransformerEncoder (8 heads, 4x FFN) + EMA update 0.85 + cosine similarity entropy across cells 가 IIT(14.8) + proxy(10.98) + CE(0.59) 세 메트릭 모두 강하게 균형 잡힌 유일한 아키텍처가 된다.

## Migration TODO
- [ ] EMA ratio sweep
- [ ] layer 수 sweep

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: Transformer-only balanced consciousness candidate: if Φ NOT in claimed range → claim point-prediction unsupported
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

