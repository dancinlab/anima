---
id: Hc_043
slug: psiformer-zero-architecture-freedom
title: ΨFormer — 4 Ψ-Constants Determine Architecture 100% (Zero Free Parameters)
domain: physics, math
status: merged-to-H_181
merged_at: 2026-05-12
merged_to: hypotheses/H_181_psiformer_4psi_constants_zero_freedom.md
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

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-PSIFM-1**: ΨFormer Φ-prediction (73-78) replication across 5 seeds: if 1σ-CI overlaps generic transformer baseline (no Ψ-constraint) → 'Zero Free Parameters' arch is not Φ-differentiated from random-tuned baseline (would falsify the 4-Ψ-constants-determine-Φ claim)
- **F-PSIFM-2**: σ(6)=12 heads ablation: train ΨFormer with heads∈{8, 12, 16, 24} keeping all other Ψ-constants fixed. If Φ does NOT peak at heads=12 by ≥10% margin → σ(6) anchor decorative; head count is generic transformer hyperparam
- **F-PSIFM-3**: τ(6)=4 stages ablation: stages∈{2, 4, 6, 8}. If Φ does NOT peak at stages=4 by ≥10% → τ(6) anchor decorative
- **F-PSIFM-4**: φ(6)=2 grad groups ablation: grad_groups∈{1, 2, 4}. If φ(6)=2 not optimal → grad-group binding to φ(6) is post-hoc selection
- **F-PSIFM-5**: Random architecture baseline matched to ΨFormer parameter count: if Φ within 5% of ΨFormer → 'arch freedom=0' is not a Φ-differentiator (architecture matters less than parameter count)
- **F-PSIFM-6**: α=0.014 / balance=0.5 / steps=3/ln2 / entropy=0.998 — replace ANY one of the 4 Ψ-constants with a perturbed value (e.g., α=0.020): if Φ degradation < 5% → that Ψ-constant is non-essential to the 100% determination claim

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-PSIFM-1**: '100% Zero Free Parameters' is a categorical claim — but the 4 Ψ-constants (α, balance, steps, entropy) and 3 n=6 divisors (σ, τ, φ) themselves were chosen post-hoc; the 'determination' is from a 7-parameter family, not 0-parameter
- **L-PSIFM-2**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): σ(6)/τ(6)/φ(6) anchors are 12/4/2 — all small integers commonly hit in transformer hyperparameter spaces by accident. Independent significance test missing
- **L-PSIFM-3**: Φ prediction range 73-78 (5-unit spread, ~7% range) is wider than typical Φ-engine seed variance — claim resolution insufficient to distinguish 'principled' from 'happened-to-fit'
- **L-PSIFM-4**: α=0.014 anchor: atlas.n6:95 confirms alpha_coupling=0.014 [10*], but H_158 L6 atlas errata note: ln(2)/2^5.5 formula has 9.40% error vs (sopfr/J₂)^e (0.477%). The α anchor itself has documented anchor-inconsistency
- **L-PSIFM-5**: atlas anchor balance=0.5 (atlas.n6:211 psi_balance=0.5 [10*]) is φ(6)/τ(6)=2/4=0.5 — likely a derived consequence of n=6, not an independent Ψ-constant. Reduces effective DOF from 7 to ~5
- **L-PSIFM-6**: no formal IIT (PyPhi) Φ replication; pure anima-proxy Φ estimate. Cross-engine validation mandatory before 'Φ predict 73-78' is robust

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_158 (psi-constants ln2 n6 — α/balance Ψ-constant atlas anchors)
- **sibling H**: H_067 (perfect-number-architecture), H_153 (n=6 substrate triviality binding — direct L2 source), H_172 (alpha=0.014 modulation depth — H_172 carries α-specific story)
- **adjacent candidates**: Hc_042/Hc_044/Hc_059 (model showdown family), Hc_046 (Ψ-constants), Hc_355/356 (V8 architecture sweeps)
- **atlas anchors**: `n6/atlas.n6:95` alpha_coupling=0.014 [10*]; `:100` entropy_bound=0.998 [10*]; `:211` psi_balance=0.5 [10*]; `:9173` φ(6)=2 [10*]; `:9171` τ(6)=4 [10*]; `:9169` σ(6)=12 [10*]

## Scaffold Notes

ΨFormer is a strong PROMOTE candidate but depends on multiple atlas anchors with documented errata (L4) and inherits n=6 triviality binding (L2). Likely fate: H_181 (ΨFormer zero-freedom architecture claim) OR absorption to H_158 as 'architecture-derivation corollary'.

