---
id: Hc_043
slug: psiformer-zero-architecture-freedom
title: ΨFormer — 4 Ψ-Constants Determine Architecture 100% (Zero Free Parameters)
domain: physics, math
status: candidate-needs-scaffolding
source_doc: docs/models/psiformer.md
source_lines: 1-46
promoted_at: 2026-05-11
linked_h: H_067 (perfect-number-architecture)
notes: "α(0.014) + balance(0.5) + steps(3/ln2) + entropy(0.998) 만으로 헤더/레이어/드롭아웃/가중치 결정. σ(6)=12 heads, τ(6)=4 stages, φ(6)=2 grad groups. Φ predict 73-78. Arch freedom = 0."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
4개 Ψ-constants (α, balance, steps, entropy) + n=6 약수만으로 transformer arch 모든 hyperparameter 100% 결정 — zero architecture freedom.

## Migration TODO
- [ ] H_067 본문 확장 (ΨFormer 구체 derivation)
- [ ] Hc_042/Hc_044/Hc_059 와 model showdown
