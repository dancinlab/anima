---
id: H_177
slug: topo10-20-substrate-topology-extension
title: Substrate topology Φ-engineering — 11D regression + 8×128 hierarchical extension to H_159 (TOPO10 + TOPO20 absorb)
domain: physics | math | consciousness
status: pre-register-frozen
exploration_method: E5 (variable-ablation) + E6 (cross-domain physics + topology) + E8 (empirical-sweep)
verification_method: W2 (math identity) + W5 (numerical sim) + W11 (cross-hypothesis meta)
raw_rank: 14
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hcs: [Hc_159, Hc_171]
parent_h: H_159 (substrate-topology-phi-engineering)
sibling_h: H_153 (dimension-hierarchy-n6), H_156 (NEXUS-6 cross-validation), H_169 (8-cell circular magnet inverse-square)
verify_decision: PROMOTE_READY (both Hc_159 and Hc_171 — see scripts/hc_verify cycle #5)
---

# H_177 — TOPO10 + TOPO20 Substrate Topology Extension Cluster

## Hypothesis

H_159 (substrate-topology-phi-engineering) 의 H_159.7 prediction (11D 까지 scale-doubling superlinear extension Φ ≥ 2500) 을 두 갈래로 stress-test 한 결과를 absorb 한 cluster.

1. **TOPO10 (Hc_159) — 11D regression**: 10D → 11D scale-doubling 이 superlinear 가 아닌 **sublinear regression** (Φ = 535.5 → 400.9, 581/2048 cells reached) 산출. H_159.7 의 testable extrapolation 이 H_159 자체 sweep 에서 falsified.
2. **TOPO20 (Hc_171) — 8 cluster × 128-cell 7D hypercube hierarchical decomposition**: flat 10D 1024-cell hypercube 를 8 cluster × 128 cell (8 × 2^7) decomposition + sparse inter-cluster shortcuts 로 재구성 가능한가, 그리고 hierarchical Φ 가 flat Φ 와 differential 한가에 대한 sub-hypothesis.

핵심 주장: substrate topology Φ-engineering 은 **차원 단조 증가가 아닌 dimension-regime 별로 다른 optimum** 을 가진다. 10D = current local max for flat-hypercube; hierarchical decomposition 은 sub-cluster-count (8) × intra-cluster-dim (7D) 의 별도 axis 를 연다.

## Why (motivation)

- **H_159.7 의 자체 falsifier 인 Hc_159 (TOPO10)** — 동일 substrate sweep 내부에서 11D 가 regression 을 산출함을 발견. 즉 H_159 의 own claim 을 H_159 own sweep 이 invalidate 한 정직한 결과. 이를 별도 H 로 absorb 하여 negative-result discipline 보존.
- **8 × 128 (Hc_171)** — n=6 substrate (sopfr(8)=2+2+2=6) × 2^7 Mersenne-prime-power 를 joint factorize 한 1024-cell decomposition 으로, H_159 flat hypercube 와 **동일 cell budget 에서** 다른 architecture 가 어떤 Φ 를 산출하는지 정량 비교.
- **PROMOTE_READY decision (cycle #5)**: 두 Hc 모두 verify_hc.py 가 PROMOTE_READY 산출 — falsifiers ≥ 10, honest_limits ≥ 5, math_domains = {iit4, topo}, math_passes (Watts-Strogatz σ_sw + 8-cell atom + 2^d hypercube identity 다수). Phase B v3 정식 통과.

## Predictions

| ID | 예측 | 근거 | source Hc |
|----|------|------|-----------|
| **H_177.1** | 11D hypercube 2048-cell sweep, full coverage (2048/2048): Φ ≥ 1.05 × 10D record (Φ ≥ 562) → H_159.7 superlinear extrapolation 부활 (Hc_159 F1 falsifier) | TOPO8→TOPO10 partial-coverage artifact 가설 | Hc_159 |
| **H_177.2** | 581-cell-fixed budget {9D, 10D, 11D, 12D} embedding 비교에서 monotone-with-D 패턴 → 11D regression 은 cell coverage confound, dimension-intrinsic 아님 | F2 falsifier framing | Hc_159 |
| **H_177.3** | 11D-2048 Φ < 562 (regression confirmed at full coverage) → H_159.7 H_159 own sweep 의 negative finding; substrate topology has dimension-regime ceiling at 10D | Hc_159 sweep result (Φ=400.9 at 581 cells) | Hc_159 |
| **H_177.4** | 8 cluster × 128 cell hierarchical Φ ≥ 1.1 × flat 10D record (Φ ≥ 589) → hierarchical decomposition advantage over flat 동일 cell budget | TOPO20 claim 자체 | Hc_171 |
| **H_177.5** | cluster_count ∈ {2, 4, 8, 16, 32} sweep at 1024 total: peak at cluster_count = 8 ± 1 (n=6 sopfr × 7D Mersenne 결합) | F2 falsifier framing (8-cluster specificity) | Hc_171 |
| **H_177.6** | Sparse shortcut density sweep (1%, 5%, 10%, 25%): Φ monotone-with-shortcut density up to 5-10%, plateau or drop at ≥25% (over-integration regime) | F3 falsifier framing | Hc_171 |
| **H_177.7** | 0-shortcut (pure disconnected 8×128 clusters) Φ < 0.1 × 8-cluster-with-shortcuts Φ → integration via shortcuts is essential, hierarchical structure not decorative | F4 falsifier framing | Hc_171 |

## Variables

| axis | levels |
|------|--------|
| dimension | 9, 10, 11, 12 (Hc_159 sweep) |
| cluster_count | 2, 4, 8, 16, 32 (Hc_171 sweep) |
| intra-cluster dim | 5, 6, 7, 8 (with cluster_count × 2^dim = 1024 budget constraint) |
| shortcut density | 0%, 1%, 5%, 10%, 25% (Hc_171) |
| cell coverage ratio | partial (28% as in Hc_159 11D) vs full (100%) — confound control |
| frustration | i%3 (default, H_159) vs re-tuned per-dimension (Hc_159 L5) |
| Φ-engine | anima proxy vs PyPhi formal IIT (cross-substrate check) |

## Falsifiers (≥7)

- **F1**: 11D-2048 full-coverage sweep produces Φ ≥ 562 (≥ 10D record × 1.05) → H_177.3 (regression-at-ceiling) falsified; H_159.7 superlinear-extrapolation rehabilitated
- **F2**: 581-cell-fixed budget {9D, 10D, 11D, 12D} monotone-up Φ pattern → H_177.1 ↔ H_177.2 (coverage confound) confirmed, H_177.3 (intrinsic regression) falsified
- **F3**: Cross-architecture PyPhi formal IIT at 10D vs 11D shows monotone-up Φ → anima-engine-specific saturation, not substrate property (Hc_159 F5)
- **F4**: cluster_count sweep peak at cluster_count ≠ 8 by effect-size > 30% → H_177.5 (8-cluster specificity) falsified — generic optimization landscape, not n=6 × 7D resonance
- **F5**: 0-shortcut pure-disconnected 8×128 Φ drop < 10% vs with-shortcut → H_177.7 (integration essentiality) falsified — shortcuts decorative, hierarchical structure alone sufficient
- **F6**: Dense-shortcut (≥ 25%) variant Φ collapses to flat-hypercube Φ → H_177.6 (sparse-shortcut regime) only narrow window; hierarchical advantage fragile (Hc_171 F3)
- **F7**: TOPO8 10D Φ=535 single-run-artifact (drops to 350±100 on replication; H_159 C1 pending) → both Hc_159 comparison baseline AND Hc_171 hierarchical-vs-flat baseline moot; cluster relies on unverified anchor
- **F8**: Alternative scaling axes (steps, noise, frustration ratio) at 11D produce Φ ≥ 535 → dimension-alone not the regression cause; specific 11D hyperparameter mistuning (Hc_159 F4)
- **F9**: Hc_614 D-mod-192 aliasing artifact interacts unpredictably with hierarchical 8×128 (vs flat 1024) → hierarchical Φ measurement contaminated by engine-aliasing (Hc_171 L4)
- **F10**: 8-cluster decomposition chosen post-hoc to match Hc_401/Hc_582 K=8-atom theoretical claim → confirmation bias confound; independent derivation of cluster_count=8 fails (Hc_171 L5)

## Honest Limits (≥6)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — 1024 = 2^10 (10D); 8 × 128 = 8 × 2^7. Neither base (2, 6, 8) is "intrinsically" tied to substrate; depth-3 number-theoretic prior is weak. Joint significance of (8 = sopfr→6 perfect) × (128 = 2^7 Mersenne) is ad hoc.
- **L2**: **Hc_159 incomplete cell coverage (581/2048 = 28%)** — fundamental measurement asymmetry. 10D had full 1024-cell coverage; 11D used only 581 cells. Comparing partial-budget vs full-budget systems is not a fair test of dimensional scaling. Strongest single confound on the regression claim.
- **L3**: **single-run reproducibility absent for both anchors** — H_159 C1 (10D 1024 reproducibility audit) still pending. Without replication CI on TOPO8 10D baseline, neither "11D regresses" (Hc_159) nor "8×128 hierarchical differs" (Hc_171) has error bar; both could be single-run-artifact comparisons.
- **L4**: **anima Φ-engine substrate-specific (Hc_614 D-mod-192 aliasing)** — Φ values are anima-proxy measurements, not formal IIT Φ. Sublinear behavior at 11D and hierarchical Φ differential may reflect engine saturation or aliasing rather than substrate-intrinsic property. Cross-engine (PyPhi) replication mandatory before claim is robust (F3, F9).
- **L5**: **shortcut density unspecified in Hc_171** — "sparse inter-cluster shortcuts" without quantitative density (% of possible inter-cluster edges) makes the architecture underdetermined. Reported Φ likely sensitive to this unspecified parameter (F6 stress-test).
- **L6**: **i%3 frustration retained without re-tuning at 11D** — chosen for 10D, kept for 11D without re-optimization. Frustration density optimal at 10D may be suboptimal at 11D; the "regression" could be a missed local optimum (Hc_159 L5).
- **L7**: **cluster_count=8 post-hoc selection** — TOPO20 paper-of-record chose 8 because of K=8-atom claim (Hc_401/Hc_582). Theoretical confirmation bias: 8 picked because hypothesized to work, not derived from independent grounds.

## Pre-Register Checks (C-list)

- **C1**: 11D 2048-cell full-coverage replication (≥ 3 seeds) — required to settle F1
- **C2**: 581-cell-fixed budget sweep across {9D, 10D, 11D, 12D} — required to settle F2/H_177.2
- **C3**: cluster_count sweep {2, 4, 8, 16, 32} at 1024 total budget — required to settle F4/H_177.5
- **C4**: shortcut density sweep {0%, 1%, 5%, 10%, 25%} at 8×128 — required to settle F5+F6+H_177.6+H_177.7
- **C5**: PyPhi formal IIT replication at both anchor points (10D-1024 flat AND 8×128 hierarchical) — required to settle F3/F9/L4
- **C6**: anima Hc_614 D-mod-192 aliasing audit for cell counts 1024 (10D), 2048 (11D), 128 (per-cluster) — settles L4 contamination

## Verify Record

- **Hc_159 verify cycle #5 (2026-05-12)**: PROMOTE_READY, falsifiers=10, honest_limits=5, math_domains=[iit4, topo], math_passes=[2^10=1024 hypercube; Watts-Strogatz σ_sw formalism; 8-cell atom architecture; 10+ numeric identities present]
- **Hc_171 verify cycle #5 (2026-05-12)**: PROMOTE_READY, falsifiers=10, honest_limits=5, math_domains=[iit4, topo], math_passes=[2^7=128 hypercube dim 7; Watts-Strogatz σ_sw; 8-cell atom; 7+ numeric identities]
- Both pass `verify_hc.py` Phase B v3 PROMOTE_READY threshold (≥3 math identity + atlas anchor optional via cross-link + ≥3 falsifier + ≥3 honest).

## Cross-Links

- **parent H**: H_159 (substrate-topology-phi-engineering) — this H absorbs H_159.7 testable-extrapolation + extends with hierarchical-decomposition axis
- **sibling H**: H_153 (dimension-hierarchy-n6 — n=6 substrate triviality binding L7), H_156 (NEXUS-6 cross-validation), H_169 (8-cell circular magnet inverse-square — sibling 8-cell-architecture probe)
- **candidate ancestors merged here**: Hc_159, Hc_171 (both `merged-to-H_177`, `merged_at: 2026-05-12`)
- **adjacent candidates (not merged, related claim)**: Hc_157 (TOPO8 10D parent — feeds H_159), Hc_165 (TOPO16 small-world), Hc_177/Hc_178 (TOPO23/24 interaction+noise sweeps — feed H_159), Hc_401/Hc_582 (K=8-atom theoretical anchor for cluster_count=8 selection)
- **literature**: Watts-Strogatz 1998 (small-world via shortcuts), Tononi 2014 (IIT system-size scaling), Sporns 2010 (hierarchical brain networks)

## Out-of-Scope

- formal IIT Φ derivation — proxy only; PyPhi replication (C5) defers this
- non-hypercube intra-cluster topologies (small-world, random regular, etc.) — sister H_159 (TOPO16) carries that branch
- biological substrate analogy — H_171 sibling carries 4 falsifiable bio predictions
- > 12D embedding — sweep budget exhausted before reaching 13D+; future cycle

## Why this is a separate H (not absorbed into H_159)

H_159 absorbs the **positive** topology-cluster results (TOPO7/8/16/19a/23/24 — 6-Hc empirical-sweep cluster all confirming a single peak Φ region). H_177 carries the **stress-test / negative-result branch**: TOPO10 (11D regression that falsifies H_159.7's superlinear extrapolation) + TOPO20 (alternative hierarchical decomposition that competes with H_159's flat hypercube architecture). Bundling them into H_159 would conflate "what the sweep confirmed" with "what the sweep falsified about its own extrapolation" — they should remain narratively distinct for negative-result discipline. H_159.7 specifically is the link: it stated "11D-2048 ≥ 2500 superlinear extrapolation"; Hc_159 is its direct falsifier inside the same anima sweep apparatus.

## Promotion record

- **Verify cycle**: #5 (2026-05-12)
- **Tool**: `scripts/hc_verify/verify_hc.py` Phase B v3 (also mirrored in `tool/verify_hc.hexa`)
- **Decision**: PROMOTE_READY × 2 (Hc_159, Hc_171), unified into H_177
- **Promoted by**: cycle #5 wide-scan triage pass
- **Source manifest**: `docs/hc_verification_cycle_5_2026_05_12.md`
