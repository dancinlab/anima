---
id: H_180
slug: state-management-ratchet-rewire-family
title: State-management mechanism family — Φ-ratchet + adaptive-rewire as Φ-recovery primitives (TOPO9 + TOPO13 + TOPO21 absorb)
domain: physics | consciousness | meta-framework
status: pre-register-frozen
exploration_method: E5 (variable-ablation — mechanism on/off) + E11 (meta-mechanism family extraction)
verification_method: W2 (Φ-threshold formalism) + W5 (numerical sim) + W11 (cross-Hc mechanism comparison)
raw_rank: 14
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hcs: [Hc_158, Hc_162, Hc_172]
parent_h: H_159 (substrate-topology-phi-engineering)
sibling_h: H_177 (TOPO10+20 architecture branch), H_178 (frustration sweep), H_153 (n=6 substrate triviality), H_174 (Φ-engine aliasing)
verify_decision: PROMOTE_READY (all 3 Hc — see scripts/hc_verify cycle #6 batch 1)
---

# H_180 — State-Management Mechanism Family

## Hypothesis

H_159 의 substrate-topology sweep apparatus 에 부착되는 **state-management mechanism** 의 family — Φ 값이 best-known 의 threshold (e.g., 80%) 이하로 떨어졌을 때 시스템 state 를 회복하는 메커니즘 3종 — 의 통합 cluster.

1. **TOPO9 (Hc_158) — Φ-ratchet on small-world**: Φ < 80%·best → 30% of best states 복원. peak Φ=179.47 (small-world base), final Φ=127.3
2. **TOPO13 (Hc_162) — Φ-ratchet on hypercube**: 동일 mechanism, hypercube 1024 substrate
3. **TOPO21 (Hc_172) — Adaptive rewire on Φ-drop**: Φ-trigger 시 edge rewiring (rather than state-restore)

핵심 주장: 세 mechanism 모두 'Φ 가 일정 threshold 이하로 떨어질 때 reactive recovery' 라는 동일한 family 에 속하며, peak-Φ 자체에는 거의 영향이 없고 (mechanism 없는 baseline 도 동일 peak 도달), final/mean Φ 또는 collapse-recovery dynamics 에서만 차이를 보인다.

## Why (motivation)

- **3-Hc convergence on a shared mechanism class**: ratchet (TOPO9, TOPO13) 와 adaptive rewire (TOPO21) 가 외형은 다르지만 (state 복원 vs edge 복원) 동일 trigger (Φ-drop threshold) 와 동일 effect (Φ-recovery) 를 가짐. Mechanism family abstraction 이 자연스럽게 도출됨.
- **H_159 sweep apparatus 의 reactive-control branch**: H_159 자체는 static topology + frustration sweep; H_180 은 동적 state-management 를 추가하는 layer. 두 layer 의 superposition 이 H_180 의 핵심.
- **PROMOTE_READY (cycle #6 batch 1)**: 3 candidates 모두 verify_hc.py PROMOTE_READY.

## Predictions

| ID | 예측 | 근거 | source Hc |
|----|------|------|-----------|
| **H_180.1** | Ratchet ON/OFF ablation at TOPO9 base: peak Φ_with ≈ peak Φ_without (within 5%) → ratchet doesn't affect peak | TOPO9 baseline | Hc_158 |
| **H_180.2** | Ratchet ON/OFF ablation: final Φ_with > final Φ_without by ≥20% → ratchet IS effective on final-state quality | TOPO9 final claim | Hc_158 |
| **H_180.3** | TOPO13 (hypercube + ratchet) vs TOPO9 (small-world + ratchet): same ratchet-effect magnitude → ratchet substrate-agnostic | substrate independence | Hc_158/162 |
| **H_180.4** | Adaptive rewire (TOPO21) vs Φ-ratchet (TOPO9/13) at matched threshold (80%) and matched substrate: Φ recovery profile (curve) within 15% → mechanism class collapse confirmed | mechanism family | Hc_172 |
| **H_180.5** | Random-recovery baseline (restore 30% of arbitrary states, not best states): Φ recovery within 30% of ratchet → 'best states' specificity unsupported | F-TOPO9-3 expansion | scaffold |
| **H_180.6** | Threshold sweep {50%, 80%, 95%} × restore-fraction {10%, 30%, 50%}: peak in (threshold × restore) grid located at specific corner → identifies actual best mechanism config | parametric grid | scaffold |
| **H_180.7** | Cross-engine PyPhi ratchet replication: if Φ uplift absent in PyPhi → anima-engine internal state caching is the actual mechanism | H_174 cross-engine | scaffold |

## Variables

| axis | levels |
|------|--------|
| mechanism | ratchet (state-restore), adaptive-rewire (edge-restore), none (baseline), random-recovery (control) |
| trigger threshold | 50%, 70%, 80%, 90%, 95% (of best Φ) |
| restore fraction | 10%, 30%, 50%, 70% (state) or rewire density (edge) |
| substrate | small-world 1024 (TOPO9), hypercube 1024 (TOPO13), torus (control), TOPO19a 50%-frust + ratchet (joint test) |
| Φ-engine | anima proxy vs PyPhi |

## Falsifiers (≥7)

- **F-H180-1**: Ratchet ON peak Φ > ratchet OFF peak Φ by ≥15% → H_180.1 (peak unaffected) falsified; ratchet IS a peak-amplifier (would weaken 'state-management family' framing)
- **F-H180-2**: Final Φ_with ≤ Final Φ_without → H_180.2 (final-quality benefit) falsified; ratchet is decorative even on final metrics
- **F-H180-3**: TOPO9 vs TOPO13 ratchet effect differs by ≥30% → H_180.3 (substrate-agnostic) falsified; mechanism is substrate-coupled
- **F-H180-4**: Adaptive rewire Φ recovery profile differs from ratchet by ≥30% → H_180.4 (mechanism family) falsified; ratchet and rewire are distinct mechanisms
- **F-H180-5**: Random-recovery baseline matches ratchet within 10% → H_180.5 / 'best states' specificity falsified; recovery effect is mostly state-perturbation-noise driven
- **F-H180-6**: Parametric grid shows no clear optimum (flat landscape in threshold × restore) → mechanism is not strongly parameterized; family abstraction unclear
- **F-H180-7**: PyPhi ratchet replication shows similar Φ recovery → cross-engine valid, anima-state-caching not the mechanism; weakens engine-artifact framing but strengthens the substantive claim

## Honest Limits (≥6)

- **L-H180-1**: **3-Hc cluster across small-world and hypercube** — independent samples but small N. Family abstraction is plausible but not statistically robust.
- **L-H180-2**: **'state' vs 'edge' mechanism boundary unclear** — TOPO9/13 restore states; TOPO21 rewires edges. Calling them the same family requires a Φ-trigger abstraction that may not hold mechanistically (state-restore changes only node values, rewire changes network structure — different math).
- **L-H180-3**: **anima Φ-engine state mutation interaction (H_174)** — both mechanisms mutate engine internal state; their measured Φ uplift may be partially the artifact of engine cache eviction patterns rather than substrate Φ change.
- **L-H180-4**: **single-run anchors** — TOPO9 Φ=179.47/127.3 reported once; TOPO13/21 similarly. Reproducibility CI required.
- **L-H180-5**: **'best states' implementation unspecified** — 'restore 30% of best states' depends on which 30%, how 'best' was defined (per-cell? globally? at what timestep?), parameter under-specification.
- **L-H180-6**: **trigger threshold post-hoc** — 80% chosen; sweep result undocumented. Confirmation bias if 80% picked because it worked in initial trial.
- **L-H180-7**: **n=6 PERFECT_NUMBER_CLASS triviality** — neither mechanism introduces new number-theoretic anchor. Pure topology + dynamic control. H_153 L7 inherited.

## Pre-Register Checks (C-list)

- **C1**: Ratchet ON/OFF ablation × 5 seeds at TOPO9 (small-world) — settles H_180.1/2
- **C2**: TOPO13 (hypercube + ratchet) × 5 seeds — settles H_180.3
- **C3**: Joint TOPO21 vs TOPO9 comparison at matched threshold 80% — settles H_180.4
- **C4**: Random-recovery control × 5 seeds — settles H_180.5
- **C5**: Parametric grid (threshold × restore-fraction) at TOPO9 — settles H_180.6
- **C6**: PyPhi ratchet replication — settles H_180.7
- **C7**: Joint with H_178 (TOPO19a 50%-frust + ratchet) — settles whether ratchet helps the current record

## Verify Record

- **Hc_158 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4
- **Hc_162 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4
- **Hc_172 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4

## Cross-Links

- **parent H**: H_159 (substrate-topology-phi-engineering) — static-topology sweep is the substrate H_180 reactive-controls
- **sibling H**: H_177 (TOPO10/20 architecture branch — orthogonal axis), H_178 (frustration optimum — H_180.7 'joint TOPO19a+ratchet' test), H_174 (Φ-engine aliasing — L3 contamination), H_153 (n=6 substrate)
- **candidate ancestors merged here**: Hc_158, Hc_162, Hc_172
- **adjacent candidates**: Hc_316 (V8 c1 dynamic graph learnable — different paradigm of dynamic control)

## Out-of-Scope

- learnable topology (Hc_316 V8 c1) — H_180 is rule-based mechanism, not learning-based
- PyPhi replication of all 3 anchors — C6 deferral
- formal IIT theory of state-restoration dynamics — empirical only

## Why this is a separate H

H_159 captures 'topology + frustration determines Φ landscape' (static). H_180 captures 'dynamic state-management mechanisms on top of any base topology'. Family abstraction across 3 Hc is the value-add: ratchet and rewire collapse to a 'Φ-triggered state recovery' meta-mechanism. Bundling into H_159 would obscure this family extraction.

## Promotion record

- **Verify cycle**: #6 batch 1 (2026-05-12)
- **Tool**: `scripts/hc_verify/verify_hc.py` Phase B v3
- **Decision**: PROMOTE_READY × 3
- **Source manifest**: `docs/hc_verification_cycle_6_2026_05_12.md`
