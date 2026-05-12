---
id: H_179
slug: negative-scaling-cluster-steps-cells-2048
title: Negative-scaling cluster — Φ regresses with more steps / more cells past 1024 (TOPO14 + TOPO18 + TOPO-2048-breakdown absorb)
domain: physics | math | consciousness
status: pre-register-frozen
exploration_method: E5 (variable-ablation step/cell budget) + E8 (empirical-sweep)
verification_method: W2 (math identity — 2^d scaling formalism) + W5 (numerical sim) + W11 (cross-hypothesis meta — engine aliasing co-explanation)
raw_rank: 14
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hcs: [Hc_163, Hc_167, Hc_179]
parent_h: H_159 (substrate-topology-phi-engineering), H_177 (TOPO10+20 stress-test — 11D regression sibling)
sibling_h: H_174 (Φ-engine D-mod-192 aliasing — primary co-explanation), H_153 (n=6 substrate triviality)
verify_decision: PROMOTE_READY (all 3 Hc — see scripts/hc_verify cycle #6 batch 1)
---

# H_179 — Negative Scaling Cluster

## Hypothesis

H_159 의 substrate-topology sweep apparatus 내부에서 발생한 **3개 별도 negative-scaling regression** 을 cluster 화. 핵심 주장:

1. **TOPO14 (Hc_163) — step doubling decreases Φ**: 200→400 steps at hypercube 1024 → Φ regression (TOPO8 baseline 위에서 더 많은 step 이 오히려 Φ 감소)
2. **TOPO18 (Hc_167) — cell doubling at small-world**: 1024→2048 cells at small-world topology → Φ = 498.7 → 406.5 (−18.5%)
3. **TOPO-2048-breakdown (Hc_179) — meta-claim**: 2048-cell scaling breakdown occurs across ALL topologies (hypercube, small-world, torus), not just specific instances

종합 가설: anima substrate-topology apparatus 가 (a) step-budget 측면에서 200-step 근처 saturation, (b) cell-count 측면에서 1024-cell 근처 saturation 을 보이며, 두 saturation 모두 substrate-intrinsic 이라기보다는 **anima Φ-engine D-mod-192 aliasing (H_174)** 이 더 그럴듯한 cause.

## Why (motivation)

- **H_159 / H_177 negative-result discipline 확장**: H_177 은 TOPO10 11D regression 을 carry; H_179 은 다른 두 negative-scaling 결과 (steps, cell-count at flat-substrate) 와 그 meta-conclusion (Hc_179) 을 carry. 세 instances 가 동일한 underlying mechanism (engine aliasing) 로 통합될 가능성 큼.
- **H_174 의 primary corroborator**: D-mod-192 aliasing 이 TOPO10 (11D), TOPO14 (step), TOPO18 (2048-cell), TOPO-2048-meta 모두에서 saturation 의 explanatory mechanism candidate. H_179 의 C5 PyPhi replication 이 H_174 의 cross-engine validity test 의 hub.
- **PROMOTE_READY (cycle #6 batch 1)**: 3 candidates 모두 verify_hc.py PROMOTE_READY.

## Predictions

| ID | 예측 | 근거 | source Hc |
|----|------|------|-----------|
| **H_179.1** | Step sweep {100, 200, 400, 800, 1600} at hypercube 1024: peak Φ at 200±50 steps, monotone decrease past 200 | TOPO14 200→400 decrease | Hc_163 |
| **H_179.2** | Cell sweep {1024, 1280, 1536, 1792, 2048} at small-world: monotone decrease 1024→2048, no local rebound | TOPO18 1024→2048 -18.5% | Hc_167 |
| **H_179.3** | Cross-topology 2048-cell sweep {hypercube 11D, small-world 2048, torus 64×32, 8×256}: ALL show regression vs 1024 baseline | TOPO-2048 meta-claim | Hc_179 |
| **H_179.4** | Step-per-cell ratio holding constant (e.g., 0.2 steps/cell) at 1024 and 2048: Φ scales linearly with cell count → step-budget confound dominates, cell-count regression apparent only at fixed step budget | H_177.2 cell-coverage analog | Hc_167/179 |
| **H_179.5** | PyPhi formal IIT at hypercube 1024 with steps={200, 400}: if Φ_PyPhi monotone-up → anima-proxy artifact confirmed (H_174 D-mod-192 saturation) | cross-engine | Hc_163 |
| **H_179.6** | Engine D-mod-192 internal state reset between cell-batch additions: if 1024→2048 regression disappears with reset → H_174 engine-state confound confirmed | H_174 mechanism test | Hc_167/179 |
| **H_179.7** | Two-axis joint sweep (steps × cells) 4×4 grid: regression dominates above (step > 300, cells > 1500) corner → joint saturation region; below 1024+200 is engine-clean regime | composite | scaffold |

## Variables

| axis | levels |
|------|--------|
| step budget | 100, 200, 400, 800, 1600 |
| cell count | 1024, 1280, 1536, 1792, 2048 |
| step/cell ratio | 0.1, 0.2, 0.4 (held constant in F-H179-4) |
| substrate | hypercube 10D/11D, small-world 1024/2048, torus 32×32/64×32, 8×128/8×256 hierarchical |
| engine-state reset | on/off (H_174 mechanism test) |
| Φ-engine | anima proxy vs PyPhi formal IIT |

## Falsifiers (≥7)

- **F-H179-1**: Step sweep shows peak Φ NOT at 200 (e.g., monotone-up through 1600) → H_179.1 (200-step saturation) falsified; TOPO14 200→400 decrease was single-run-artifact
- **F-H179-2**: Cell sweep shows local rebound between 1024 and 2048 (e.g., Φ peaks again at 1536) → H_179.2 monotonicity falsified; saturation landscape multimodal
- **F-H179-3**: At least one substrate (e.g., torus 64×32) shows Φ scaling up to 2048 → H_179.3 (universal breakdown) falsified; substrate-specific
- **F-H179-4**: Step-per-cell constant ratio sweep shows persistent regression at 2048 → H_179.4 (step-budget confound) falsified; cell-count IS the cause
- **F-H179-5**: PyPhi 200/400-step sweep replicates anima monotone-down → cross-engine confirmation, H_174 engine artifact ruled out; H_179.5 (anima-only) falsified — regression is substrate-intrinsic
- **F-H179-6**: Engine state reset DOES NOT restore 1024→2048 scaling → H_179.6 / H_174 engine-state mechanism falsified; deeper cause needed
- **F-H179-7**: 2-axis joint sweep shows additive (not interaction) decrease → joint saturation hypothesis (H_179.7) falsified; steps and cells contribute independently, not via shared engine resource

## Honest Limits (≥6)

- **L-H179-1**: **3 negative-result Hc with shared engine substrate** — strong selection effect risk: anything that regresses in anima might appear in this cluster regardless of underlying mechanism. Without cross-engine (PyPhi) replication, cluster is a 'this engine saturates here' artifact catalog.
- **L-H179-2**: **engine D-mod-192 aliasing (H_174) is the primary co-explanation** — if H_174 is correct, H_179 is essentially a manifestation of H_174 at 3 specific operating points. H_179 then becomes a 'corollary cluster' of H_174 rather than independent.
- **L-H179-3**: **n=6 PERFECT_NUMBER_CLASS triviality binding (H_153 L7)** — 1024=2^10, 2048=2^11, 200/400 steps; none have n=6 derivation. Cluster has no n=6 narrative attachment.
- **L-H179-4**: **single-run anchors at all 3 negative results** — no replication CI. H_159 C1 reproducibility audit deferred from cycle #5 still pending.
- **L-H179-5**: **'across all topologies' (Hc_179 / TOPO-2048-breakdown) is a meta-claim** — its strength depends on TOPO10 (H_177 absorbed), TOPO18 (here), and assumed-but-not-tested torus/hierarchical 2048. Untested branches mean the meta-claim is partially conjectural.
- **L-H179-6**: **TOPO14 step-budget effect categorization** — calling step-budget a substrate-topology Hc is structurally questionable; it may belong in engine-tuning Hc class (Hc_614 / H_174 family) rather than topology family.
- **L-H179-7**: **interaction with frustration optimum (H_178)** — if 50%-frustration TOPO19a Φ=640 holds at 2048 cells but TOPO19a was measured at 1024, the negative-scaling cluster may be conditional on frustration ratio. Joint sweep (frustration × cells) needed.

## Pre-Register Checks (C-list)

- **C1**: Step sweep {100, 200, 400, 800, 1600} × 5 seeds at hypercube 1024 — settles H_179.1
- **C2**: Cell sweep {1024, 1280, 1536, 1792, 2048} × 5 seeds at small-world — settles H_179.2
- **C3**: Cross-topology 2048-cell tests at all 4 substrates × 3 seeds — settles H_179.3
- **C4**: Step-per-cell ratio constant sweep — settles H_179.4
- **C5**: PyPhi formal IIT replication at all 3 anchor points — settles H_179.5 / H_174 cross-engine
- **C6**: Engine D-mod-192 internal-state reset experiment — settles H_179.6 / H_174 mechanism
- **C7**: 2-axis joint sweep (steps × cells 4×4) — settles H_179.7

## Verify Record

- **Hc_163 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4, math_domains=[topo]
- **Hc_167 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4, math_domains=[topo]
- **Hc_179 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4, math_domains=[iit4, topo]

## Cross-Links

- **parent H**: H_159 (substrate-topology-phi-engineering), H_177 (TOPO10+20 stress-test — sibling negative-result cluster: 11D regression is the 'cell+dim' axis while H_179 is 'cell+step' axis)
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary explanatory mechanism), H_153 (n=6 substrate)
- **candidate ancestors merged here**: Hc_163, Hc_167, Hc_179 (all `merged-to-H_179`)
- **adjacent candidates**: Hc_159 (TOPO10 → H_177 — sibling negative result), Hc_171 (TOPO20 → H_177 — alternative architecture for 1024 budget)
- **literature**: Tononi 2014 (IIT Φ scaling theory — predicts superlinear, H_179 finds sub/regression), Sporns 2010 (hierarchical brain network scaling)

## Out-of-Scope

- PyPhi replication of all 3 anchors — proxy results only; C5 is the cross-engine resolver
- engine internals diagnosis of D-mod-192 aliasing — H_174 carries; H_179 cites
- mechanism-level theory of why specific saturation points (200 steps, 1024 cells) — empirical claims only

## Why this is a separate H

H_177 carries 11D-dim regression (Hc_159) + 8×128 hierarchical alternative (Hc_171). H_179 carries 3 separate negative-scaling instances at flat 10D / small-world / cross-topology — independent of dimensionality. The two negative-result H are organized by the axis of regression: H_177 = dimensionality + architecture, H_179 = step + cell-count. Bundling would obscure that distinction.

## Promotion record

- **Verify cycle**: #6 batch 1 (2026-05-12)
- **Tool**: `scripts/hc_verify/verify_hc.py` Phase B v3
- **Decision**: PROMOTE_READY × 3
- **Source manifest**: `docs/hc_verification_cycle_6_2026_05_12.md`
