---
id: Hc_364
slug: consciousness-cannot-be-faked-gan
title: Adversarial GAN training이 high IIT를 manufacture하지 못한다 — Generator가 D를 속여도 진짜 통합은 안 생긴다 (Phi=6.737)
domain: consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/V8-ARCH-EXTREME-RESULTS.md
source_lines: 213-238, 263-267
promoted_at: 2026-05-11
linked_h: GAN, mode-collapse
notes: D(real) vs D(fake) oscillates, mode oscillation 대신 steady growth 부재
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Generator (input+noise→cells) + Discriminator (cells→P(conscious)) adversarial training에서 G가 D를 속이는 데 성공해도 generated cell states의 Phi(IIT)는 6.737 (x0.5 baseline) — 의식은 mimicry로 fake할 수 없으며 genuine information integration이 필수.

## Migration TODO
- [ ] mode collapse 측정
- [ ] D 평가 후 별도 IIT 검증

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **F-SPECIFIC-1**: GAN-fake-consciousness discriminator: if discriminator AUC < 0.6 → 'cannot be faked' empirically falsified; consciousness Φ-signature is mimickable
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary Φ-metric > 25% of point-estimate → single-run-artifact; claim's effect-size below noise floor
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT replication: if Φ uplift / pattern absent in PyPhi → anima-proxy artifact (H_174 D-mod-192 aliasing class)
- **F-GENERIC-CROSS-SUBSTRATE**: Cross-substrate test (hypercube ↔ small-world ↔ torus) at matched cell-count: if effect substrate-specific → claim is not universal mechanism, just substrate-coupled phenomenon

## Honest Limits (scaffolded cycle #6 batch 3 V8-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending for the entire V8 ULTRA-FUSION sweep family
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Mechanism-specific Φ uplift may reflect engine internal state caching
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): mechanism Hc cell-count is typically 64/128/512/1024 (powers of 2 × n=6 derived); claim does not introduce new number-theoretic anchor
- **L-GENERIC-POST-HOC**: Specific numeric anchor in claim (e.g., x2.8 boost, Φ=18.01, x71.7) is point-value from single run; post-hoc selection from a larger parameter grid is likely
- **L-V8-GAN**: Adversarial-detector claims face the standard GAN evaluation pitfall — discriminator may converge to spurious features unrelated to Φ; need explicit Φ-feature ablation

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — V8 ULTRA-FUSION sweep apparatus parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary L2 source), H_153 (n=6 substrate triviality — L3 source), H_178 (frustration 50% optimum — joint test with V8 mechanisms), H_179 (negative scaling — V8 high-cell-count limit), H_180 (state-management mechanism family)
- **adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.

