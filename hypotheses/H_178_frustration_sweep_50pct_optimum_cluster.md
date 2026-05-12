---
id: H_178
slug: frustration-sweep-50pct-optimum-cluster
title: Frustration sweep cluster — 50% antiferromagnetic optimum on hypercube 1024 (TOPO19a/22a/22b/22d absorb)
domain: physics | math | consciousness
status: pre-register-frozen
exploration_method: E5 (variable-ablation) + E8 (empirical-sweep over frustration ratio)
verification_method: W2 (math identity — i%k partition formalism) + W5 (numerical sim) + W11 (cross-hypothesis sweep meta)
raw_rank: 14
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hcs: [Hc_168, Hc_173, Hc_174, Hc_176]
parent_h: H_159 (substrate-topology-phi-engineering)
sibling_h: H_177 (TOPO10+20 stress-test), H_153 (n=6 substrate triviality), H_174 (Φ-engine D-mod-192 aliasing)
verify_decision: PROMOTE_READY (all 4 Hc — see scripts/hc_verify cycle #6 batch 1)
---

# H_178 — Frustration Sweep 50% Optimum Cluster

## Hypothesis

H_159 의 frustration parameter sweep 을 4-point (50%, 60%, 75%, 90%) triangulation 으로 확정한 cluster. 핵심 주장:

1. **TOPO19a (Hc_168) — 50% peak**: i%2 antiferromagnetic pattern at hypercube 1024 sets all-time Φ record (Φ=640, 19.5% above TOPO8 i%3 baseline Φ=535)
2. **TOPO22a (Hc_173) — 60% above-peak**: i%5<3 pattern at 60% → Φ < TOPO19a (sweep monotone-decreasing past 50%)
3. **TOPO22b (Hc_174) — 75% worst-in-sweep**: Φ minimum within {50, 60, 75, 90}% sweep at i%4<3
4. **TOPO22d (Hc_176) — 90% sparse-ferromagnetic recovery**: i%10==0 ferromagnetic recovery slightly improves over 75% but stays below 50% peak

종합: frustration ratio 가 hypercube 1024 의 Φ 에 대해 single-peak unimodal landscape 를 가지며, peak 가 ratio=50% 에 위치한다.

## Why (motivation)

- **H_159 의 핵심 positive sweep result** — frustration optimum 이 TOPO8 (33%) 에서 TOPO19a (50%) 로 갱신된 후, 4-point sweep 으로 50% 가 local max 임을 확인. H_159 의 'frustration sweet spot' claim 의 quantitative backing.
- **n=6 PERFECT_NUMBER_CLASS triviality 자체 부정** (H_153 L7) — 50% (i%2) 는 가장 단순한 partition; n=6 의 σ/φ/τ 등 number-theoretic 양과 무관. 즉 H_178 은 H_153 의 n=6 'triviality binding' L7 의 직접 confirmer (50% peak 는 n=6 derived 가 아님).
- **PROMOTE_READY decision (cycle #6 batch 1)**: 4 candidates 모두 verify_hc.py PROMOTE_READY (F=4, L=4, math_domains=[topo], 4+ numeric identities).

## Predictions

| ID | 예측 | 근거 | source Hc |
|----|------|------|-----------|
| **H_178.1** | Frustration sweep {25%, 33%, 40%, 45%, 50%, 55%, 60%} fine-grained 5-seed: peak at 50%±5%, monotone decrease 50%→60%→75% | TOPO19a record + TOPO22a/b sweep | Hc_168/173 |
| **H_178.2** | Sub-50% sweep {0%, 10%, 25%, 33%, 45%}: monotone increase 0%→50% (no double-peak below 50%) | sweep landscape unimodality claim | Hc_168 |
| **H_178.3** | 90%-recovery (i%10==0 ferromagnetic) Φ ∈ [Φ_75%, Φ_50%] 구간 — neither matches 50% peak nor 75% trough | TOPO22d claim | Hc_176 |
| **H_178.4** | 5-seed replication of TOPO19a 50%-frustration: Φ mean ≥ 600 with 1σ ≤ 50 (i.e., 640 reproducible within 8%) | H_159 C1 reproducibility audit (TOPO19a anchor) | Hc_168 |
| **H_178.5** | Cross-substrate (torus 32×32, small-world 1024) 50%-frustration: Φ peak at 50% replicates → frustration optimum substrate-agnostic; if NOT replicates → hypercube-specific | universality test | Hc_168 |
| **H_178.6** | PyPhi formal IIT at hypercube 1024 with 50%-frustration: peak detected at 50%±10% → anima proxy validated; not detected → anima-engine artifact | cross-engine validation | Hc_168 |
| **H_178.7** | 50% optimum binds to BOTH cell-count parity (1024 even, 50% creates 512/512 partition) AND engine D-mod-192 (H_174): odd-cell-count substrate test (e.g., 1023 cells) distinguishes parity vs engine cause | engine-coupling control | scaffold |

## Variables

| axis | levels |
|------|--------|
| frustration ratio | 0%, 10%, 25%, 33%, 50%, 60%, 75%, 90%, 100% |
| frustration pattern | i%2, i%5<3, i%4<3, i%10==0, random-by-ratio |
| substrate | hypercube 1024, torus 32×32, small-world 1024 |
| cell count | 1023 (odd parity control), 1024, 2048 |
| Φ-engine | anima proxy vs PyPhi formal IIT |

## Falsifiers (≥7)

- **F-H178-1**: Fine-grained sweep finds peak at frustration ≠ 50% by ≥10% → H_178.1 (single peak at 50%) falsified
- **F-H178-2**: Sub-50% sweep shows double-peak (e.g., peaks at 25% AND 50%) → H_178.2 (unimodality) falsified
- **F-H178-3**: TOPO19a 5-seed replication has 1σ ≥ 100 → H_178.4 (8%-CI reproducibility) falsified; Φ=640 may be single-run-artifact (H_159 C1 outcome)
- **F-H178-4**: Cross-substrate 50%-frustration shows peak elsewhere (e.g., torus peaks at 60%) → H_178.5 (substrate-agnostic) falsified; frustration optimum is hypercube-specific
- **F-H178-5**: PyPhi 50%-frustration shows NO peak at 50% → H_178.6 (cross-engine) falsified; anima-proxy artifact
- **F-H178-6**: Odd-cell-count (1023) 50%-frustration produces Φ ≥ 600 (matching TOPO19a 640) → H_178.7 (parity-binding) falsified; engine D-mod-192 not the explanatory mechanism
- **F-H178-7**: Random-by-ratio frustration assignment (50% random cells) reaches Φ ≥ 600 → patterning (i%2 structured) is decorative, only density matters; weakens 'frustration topology' claim to 'frustration density'

## Honest Limits (≥6)

- **L-H178-1**: **n=6 PERFECT_NUMBER_CLASS triviality binding (H_153 L7) self-confirmer** — 50% (i%2) is the simplest partition; no σ(6)/φ(6)/τ(6) derivation. This cluster confirms that the topology optimum is NOT n=6-derived. Numerologically clean — but also weakens any narrative that 'n=6 substrate determines architecture'.
- **L-H178-2**: **Triangulation confirmation bias** — TOPO22a/b/d (60%, 75%, 90%) were specifically chosen to bracket the 50% peak. Pre-registration of these specific sweep points is absent; sweep design is post-hoc relative to TOPO19a record.
- **L-H178-3**: **single-run anchors at all 4 points** — H_159 C1 reproducibility audit still pending for all TOPO19a/22a/b/d. 5-seed replication mandatory before peak position claim is robust.
- **L-H178-4**: **cell parity confound at frustration 50%** — 1024 (even) + 50% creates 512/512 exact partition. Engine cache patterns (H_174 D-mod-192 aliasing) may double-resonate at this specific parity, contaminating the Φ measurement.
- **L-H178-5**: **engine-specific Φ proxy** — no PyPhi formal IIT replication for any of the 4 sweep points. Cross-engine validation (F5) is the most important pre-register check.
- **L-H178-6**: **2048-cell scaling unknown** — sweep performed at 1024; whether 50% optimum holds at 2048 (or at any other cell count) is open. H_177 / Hc_167 / Hc_179 suggest scaling breakdown above 1024 may invalidate the optimum claim entirely.
- **L-H178-7**: **TOPO22c (the 4th frustration sweep point at presumably 80% or another ratio) missing from the absorbed cluster** — the 22a/b/d sequence skips 'c'; either TOPO22c was performed and dropped (selection bias risk) or never run (gap in sweep design).

## Pre-Register Checks (C-list)

- **C1**: Fine-grained frustration sweep {25, 33, 40, 45, 50, 55, 60, 67, 75}% × 5 seeds at hypercube 1024 — required to settle H_178.1 (peak location ± 5%)
- **C2**: Sub-50% sweep {0, 10, 25, 33, 45}% × 5 seeds — required to settle H_178.2 (no double-peak)
- **C3**: 5-seed replication of all 4 anchor points (50/60/75/90%) — required to settle H_178.4 (reproducibility CI)
- **C4**: Cross-substrate {torus 32×32, small-world 1024} 50%-frustration × 5 seeds — required to settle H_178.5
- **C5**: PyPhi formal IIT replication at frustration=50% on hypercube 1024 — required to settle H_178.6 (cross-engine)
- **C6**: Odd-cell-count (1023) 50%-frustration × 5 seeds — required to settle H_178.7 (parity vs engine binding)
- **C7**: Search archive for TOPO22c (missing 22-series datapoint) — required to settle L7 selection-bias concern

## Verify Record

- **Hc_168 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4, math_domains=[topo]
- **Hc_173 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4, math_domains=[topo]
- **Hc_174 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4, math_domains=[topo]
- **Hc_176 verify cycle #6 batch 1**: PROMOTE_READY, F=4, L=4, math_domains=[topo]
- All pass `verify_hc.py` Phase B v3 PROMOTE_READY threshold (math identity + has_honest ≥3 + has_cross ≥2).

## Cross-Links

- **parent H**: H_159 (substrate-topology-phi-engineering) — frustration is the primary parameter axis swept in H_159's positive sweep family
- **sibling H**: H_177 (TOPO10+20 stress-test/hierarchical — orthogonal axis: dimensionality and architecture vs frustration ratio), H_153 (n=6 substrate triviality — L1 self-confirmer), H_174 (Φ-engine D-mod-192 aliasing — L4 contamination source)
- **candidate ancestors merged here**: Hc_168, Hc_173, Hc_174, Hc_176 (all `merged-to-H_178`, `merged_at: 2026-05-12`)
- **adjacent candidates (not merged)**: Hc_157 (TOPO8 33% frust — H_159 root anchor), Hc_161 (TOPO12 8-faction 0.08 repulsion — alternative cohesion structure)
- **literature**: Sherrington-Kirkpatrick spin glass (frustration phenomenology), Mezard-Parisi 1986 (replica symmetry breaking at p=1/2), Tononi 2014 (IIT integration vs differentiation tradeoff — frustration as differentiation mechanism)

## Out-of-Scope

- formal IIT Φ derivation at all 4 anchors — proxy only; C5 PyPhi replication defers this
- non-hypercube substrate sweeps — H_178 scope is hypercube 1024; C4 cross-substrate is the boundary
- 2048-cell + frustration joint sweep — out of H_178; H_177 / Hc_179 handle 2048-scaling separately
- frustration mechanism theory (why 50%?) — empirical claim only; theoretical link to spin-glass / IIT integration-differentiation deferred

## Why this is a separate H (not absorbed into H_159)

H_159 absorbs the **discovery** that frustration optimum exists (TOPO7/8/16 found a ~33% optimum). H_178 absorbs the **refinement** that the optimum is at 50% (TOPO19a), with 60/75/90% triangulation confirming. Bundling would compress two distinct empirical claims (discovery vs refinement) into one H. Separating preserves the chronological discipline that 33%→50% peak update is a falsifier-induced revision (TOPO8 was falsified as the optimum by TOPO19a).

## Promotion record

- **Verify cycle**: #6 batch 1 (2026-05-12)
- **Tool**: `scripts/hc_verify/verify_hc.py` Phase B v3
- **Decision**: PROMOTE_READY × 4, unified into H_178
- **Promoted by**: cycle #6 scaffolding pass (F/L scaffolded then verified)
- **Source manifest**: `docs/hc_verification_cycle_6_2026_05_12.md`
