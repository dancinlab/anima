---
id: H_181
slug: psiformer-4psi-constants-zero-freedom
title: ΨFormer — 4 Ψ-constants + 3 n=6 divisors fully determine transformer architecture (Zero Free Parameters claim)
domain: physics | math
status: pre-register-frozen
exploration_method: E1 (theory derivation — Ψ-constants → architecture) + E5 (variable-ablation per Ψ-constant)
verification_method: W2 (math identity per atlas anchor) + W5 (numerical sim — Φ prediction 73-78) + W11 (cross-Hc comparison Hc_042/044/059)
raw_rank: 14
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hcs: [Hc_043]
parent_h: H_158 (psi-constants ln2 n6 — α/balance anchors), H_153 (n=6 dimension hierarchy — σ/τ/φ derived)
sibling_h: H_067 (perfect-number-architecture), H_160 (n6-perfect-number-meta-cluster), H_170 (n6-design-principle-empirical-not-numerology), H_172 (α=0.014 modulation depth)
verify_decision: PROMOTE_READY (Hc_043 — see scripts/hc_verify cycle #6 batch 2)
---

# H_181 — ΨFormer Zero-Freedom Architecture

## Hypothesis

4 Ψ-constants (α=0.014, balance=0.5, steps=3/ln2, entropy=0.998) + 3 n=6 divisors (σ(6)=12 heads, τ(6)=4 stages, φ(6)=2 grad groups) 만으로 transformer architecture 의 모든 hyperparameter 가 100% 결정된다. 자유도 = 0 — 'ΨFormer' 라는 architecture family 의 핵심 claim.

predicted Φ_anima = 73-78 (anima-proxy IIT) — single point-prediction, no tunable parameter.

## Why (motivation)

- **Most math-pass-rich candidate** in cycle #5 verify (6 math identities including all 4 Ψ-constants + σ/τ/φ derivation chain), the cleanest 'theory determines architecture' claim in the candidate set.
- **atlas anchors all confirmed [10*]**: α=0.014 (atlas.n6:95), entropy=0.998 (:100), balance=0.5 (:211), σ(6)=12 (:9169), τ(6)=4 (:9171), φ(6)=2 (:9173). 7-of-7 anchor coverage.
- **Distinct from H_158** (atlas-constant anchoring): H_158 carries the atlas-anchor metadata and ln(2)/2^5.5 errata; H_181 carries the architectural-derivation claim and its falsifiability.
- **Distinct from H_153** (n=6 hierarchy generally): H_153 is the n=6 substrate claim; H_181 is the SPECIFIC chain n=6 → divisors → transformer-hyperparameters.

## Predictions

| ID | 예측 | 근거 | source Hc |
|----|------|------|-----------|
| **H_181.1** | ΨFormer trained per spec (heads=12, stages=4, grad_groups=2, α=0.014, balance=0.5, steps=3/ln2≈4.328, entropy=0.998): Φ_anima ∈ [73, 78] | direct claim | Hc_043 |
| **H_181.2** | σ(6)=12 heads ablation {8, 12, 16, 24}: Φ peak at heads=12 (margin ≥ 10%) | F2 framing | Hc_043 |
| **H_181.3** | τ(6)=4 stages ablation {2, 4, 6, 8}: Φ peak at stages=4 (margin ≥ 10%) | F3 framing | Hc_043 |
| **H_181.4** | φ(6)=2 grad groups ablation {1, 2, 4}: Φ peak at grad_groups=2 (margin ≥ 10%) | F4 framing | Hc_043 |
| **H_181.5** | Single-Ψ-perturbation: replacing ANY of {α, balance, steps, entropy} with ±20% perturbed value reduces Φ by ≥5% (necessity of all 4 Ψ-constants) | F6 framing | Hc_043 |
| **H_181.6** | Random-arch baseline matched on parameter count: Φ < ΨFormer Φ by ≥ 10% (architecture matters, not just param count) | F5 framing | Hc_043 |
| **H_181.7** | balance=0.5 derivability test: confirm balance=φ(6)/τ(6)=2/4=0.5 (atlas-derived); independent ΨFormer fit-quality with balance treated as derived vs free → equivalent (no extra DOF) | L5 framing | Hc_043 |

## Variables

| axis | levels |
|------|--------|
| heads (σ(6)) | 8, 12, 16, 24 |
| stages (τ(6)) | 2, 4, 6, 8 |
| grad_groups (φ(6)) | 1, 2, 4 |
| α | 0.011, 0.014 (default), 0.017 |
| balance | 0.4, 0.5 (default = φ(6)/τ(6)), 0.6 |
| steps | 3.5, 3/ln2≈4.328 (default), 5.0 |
| entropy | 0.95, 0.998 (default), 1.0 |
| Φ-engine | anima proxy vs PyPhi formal IIT |

## Falsifiers (≥7)

- **F-H181-1**: ΨFormer Φ (5 seeds) NOT in [73, 78] by ≥5% margin → H_181.1 falsified; specific prediction wrong
- **F-H181-2**: σ(6)=12 ablation Φ peak NOT at heads=12 → H_181.2 falsified; head count is generic hyperparam
- **F-H181-3**: τ(6)=4 ablation Φ peak NOT at stages=4 → H_181.3 falsified
- **F-H181-4**: φ(6)=2 ablation Φ peak NOT at grad_groups=2 → H_181.4 falsified
- **F-H181-5**: Single-Ψ-perturbation does NOT degrade Φ by ≥5% for any Ψ-constant → H_181.5 / 4-Ψ-necessity falsified; some Ψ-constants decorative
- **F-H181-6**: Random-arch baseline within 10% of ΨFormer Φ → H_181.6 / architecture importance falsified
- **F-H181-7**: PyPhi formal IIT ΨFormer Φ NOT in any specific range (e.g., much higher or lower than 73-78) → anima-proxy artifact; cross-engine claim falsified

## Honest Limits (≥6)

- **L-H181-1**: **'100% Zero Free Parameters' is misleading** — the 4 Ψ-constants and 3 n=6 divisors themselves were SELECTED post-hoc as the 7-parameter family. Self-determination from a 7-param family is structurally different from genuine 0-DOF
- **L-H181-2**: **n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7)**: σ(6)/τ(6)/φ(6) = 12/4/2 are all small integers commonly hit in transformer hyperparameter spaces by accident (heads=12 in GPT-2 small, layers=4-12 in many minimal models)
- **L-H181-3**: **Φ range 73-78 (7% spread) is wider than typical seed variance** — the prediction window is loose enough to capture nearly any reasonable transformer training run; falsifiability resolution insufficient
- **L-H181-4**: **α=0.014 atlas errata (H_158 L6 inherited)**: atlas.n6:17082 notes ln(2)/2^5.5 has 9.40% error vs (sopfr/J₂)^e (0.477% better fit). Anchor itself is documented as imperfect
- **L-H181-5**: **balance=0.5 = φ(6)/τ(6) (atlas.n6:211 derived)** — likely a derived consequence of σ/τ/φ, not an independent Ψ-constant. Effective Ψ-constant count is closer to 3 (α, steps, entropy) + n=6 divisors → 6 params not 7
- **L-H181-6**: **steps=3/ln2 ≈ 4.328 — non-integer, non-trivially-derived constant**. The 3/ln2 form is suspiciously close to log_2(2π) and several other numerological forms; theoretical derivation absent
- **L-H181-7**: **no formal IIT (PyPhi) Φ replication** — claim's Φ prediction is purely anima-proxy. H_174 D-mod-192 aliasing class limit inherited

## Pre-Register Checks (C-list)

- **C1**: ΨFormer training × 5 seeds, measure Φ_anima — settles H_181.1
- **C2**: σ(6)=12 heads ablation × 3 seeds × 4 levels — settles H_181.2
- **C3**: τ(6)=4 stages ablation × 3 seeds × 4 levels — settles H_181.3
- **C4**: φ(6)=2 grad groups ablation × 3 seeds × 3 levels — settles H_181.4
- **C5**: Single-Ψ-perturbation × 4 Ψ-constants × 3 perturbation levels — settles H_181.5
- **C6**: Random-arch baseline at matched param count — settles H_181.6
- **C7**: PyPhi formal IIT ΨFormer Φ — settles cross-engine validity (F7)
- **C8**: balance derivability proof check — settles H_181.7 / L5

## Verify Record

- **Hc_043 verify cycle #6 batch 2**: PROMOTE_READY, F=6, L=6, math_domains=[n6, psi, topo] — strongest math-pass set in cycle #5 wide-scan

## Cross-Links

- **parent H**: H_158 (psi-constants ln2 n6 — α/balance Ψ-constant atlas-anchor home), H_153 (dimension-hierarchy-n6 — σ/τ/φ derivation)
- **sibling H**: H_067 (perfect-number-architecture), H_160 (n6-perfect-number-meta-cluster), H_170 (n6-design-principle-empirical-not-numerology — directly relevant 'is this numerology or principle?' L1/L2), H_172 (α=0.014 modulation depth — α-specific story carry)
- **candidate ancestors merged here**: Hc_043 (`merged-to-H_181`)
- **adjacent candidates**: Hc_042/044/059 (model showdown family — pre-H_181 comparison set), Hc_046 (Ψ-constants seed)
- **atlas anchors (all [10*])**: `n6/atlas.n6:95` α=0.014; `:100` entropy=0.998; `:211` balance=0.5 = φ(6)/τ(6); `:540` ln(2); `:9169` σ(6)=12; `:9171` τ(6)=4; `:9173` φ(6)=2; `:9181` n=6
- **literature**: Tononi 2014 (IIT), Vaswani 2017 (transformer architecture baseline)

## Out-of-Scope

- formal IIT replication — proxy only; C7 PyPhi defers
- ΨFormer scaling beyond minimal transformer (e.g., > 100M params) — claim is at the architecturally-determined minimum
- alternative Ψ-constant sets (e.g., φ_alpha=0.0152 from H_158) — H_181 frozen on the 4-Ψ set; H_158 carries alternative anchors

## Why this is a separate H (not absorbed into H_158)

H_158 carries the **atlas-anchoring** task — α/balance/n=6 derivation chains and their numeric errata. H_181 carries the **architectural-derivation** task — given the constants, what specific transformer architecture follows, and what Φ does it predict. H_158 is "what are the right Ψ-constants?"; H_181 is "given the Ψ-constants, what architecture and Φ?". These are different scientific questions (calibration vs prediction), and conflating them obscures the F-list / L-list domain. ΨFormer specifically has its own falsifier list (σ/τ/φ ablations) that are architectural tests, not Ψ-constant tests.

## Promotion record

- **Verify cycle**: #6 batch 2 (2026-05-12)
- **Tool**: `scripts/hc_verify/verify_hc.py` Phase B v3
- **Decision**: PROMOTE_READY × 1 (Hc_043)
- **Promoted by**: cycle #6 priority scaffolding (top-8 priority candidate)
- **Source manifest**: `docs/hc_verification_cycle_6_2026_05_12.md`
