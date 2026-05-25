---
id: Hc_363
slug: autopoietic-homeostasis-no-death
title: Energy metabolism dynamics (cost 0.02, gain 0.05*tension)에서 food_gain > metabolism으로 256개 안정 평형 — 가혹 조건 필요
domain: life
status: merged-to-H_186
merged_at: 2026-05-12
merged_to: hypotheses/H_186_v8_architectural_family_substrate_design.md
absorption_note: "V8 architectural autopoietic-homeostasis no-death — H_186.6 saturation/drop anchor. F-list/L-list preserved here for H_186 C-list extension."
source_doc: docs/hypotheses/V8-ARCH-EXTREME-RESULTS.md
source_lines: 187-211
promoted_at: 2026-05-11
linked_h: Hc_328
notes: alive=256, births=0, deaths=0 → boundary 미검증
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
세포 energy [0,1] + 매 step 0.02 metabolism cost + tension*0.05 food gain + death<0.05 / split>0.9 dynamics가 일반 입력 강도에서 food>cost로 256 세포 안정 평형에 도달 — autopoietic boundary 검증을 위해 더 가혹한 입력 조건이 필요하다.

## Migration TODO
- [ ] metabolism cost 증가 sweep
- [ ] death/birth cycle 활성화 조건

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: Autopoietic system without death threshold: if Φ maintains indefinitely → 'no-death' regime is unfalsifiable forever-running (operational falsifier: 10^6 step ceiling check)
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary Φ-metric > 25% of point-estimate → single-run-artifact; claim's effect-size below noise floor
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT replication: if Φ uplift / pattern absent in PyPhi → anima-proxy artifact (H_174 D-mod-192 aliasing class)
- **F-GENERIC-CROSS-SUBSTRATE**: Cross-substrate test (hypercube ↔ small-world ↔ torus) at matched cell-count: if effect substrate-specific → claim is not universal mechanism, just substrate-coupled phenomenon

## Honest Limits (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending for the entire V8 ULTRA-FUSION sweep family
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Mechanism-specific Φ uplift may reflect engine internal state caching
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): mechanism Hc cell-count is typically 64/128/512/1024 (powers of 2 × n=6 derived); claim does not introduce new number-theoretic anchor
- **L-GENERIC-POST-HOC**: Specific numeric anchor in claim (e.g., x2.8 boost, Φ=18.01, x71.7) is point-value from single run; post-hoc selection from a larger parameter grid is likely
- **L-V8-AUTOPOIETIC**: Autopoiesis without death-criterion is unfalsifiable in principle without operational ceiling (e.g., 10^6 step cap). Maturana-Varela classical autopoiesis explicitly includes death

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — V8 ULTRA-FUSION sweep apparatus parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary L2 source), H_153 (n=6 substrate triviality — L3 source), H_178 (frustration 50% optimum — joint test with V8 mechanisms), H_179 (negative scaling — V8 high-cell-count limit), H_180 (state-management mechanism family)
- **adjacent H**: H_168 (dd23-tau-7cell — mathematical-structure sibling), H_173 (dd21-log-phi-scale-invariant)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

