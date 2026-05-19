---
id: H_159
slug: substrate-topology-phi-engineering
title: Substrate topology Φ-engineering — 10D hypercube + optimal (interact=0.15, noise=0.02, frust=50%) → Φ=640 peak
domain: physics | consciousness | meta-framework
status: pre-register-frozen
exploration_method: E5 (variable-ablation) + E6 (cross-domain physics + topology) + E8 (empirical-sweep)
verification_method: W2 (math identity) + W5 (numerical sim) + W11 (cross-hypothesis meta)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hcs: [Hc_156, Hc_157, Hc_165, Hc_169, Hc_177, Hc_178]
parent_h: H_040 (legacy substrate-topology-cluster pointer)
sibling_h: H_153 (dimension-hierarchy-n6), H_156 (NEXUS-6 cross-validation)
---

# H_159 — Substrate Topology Φ-Engineering Cluster (TOPO7/8/16/19a/23/24 absorb)

## Hypothesis

anima substrate Φ-engineering 의 6-Hc empirical-sweep cluster — *어떤* network topology + parameter regime 가 IIT-style Φ proxy 를 최대화하는가 에 대한 deterministic-numerical 답.

**Core claim**: 1024-cell graphs (10D hypercube / Watts-Strogatz small-world) + i%3 antiferromagnetic frustration + (interact=0.15, noise=0.02, frust=50%) 가 Φ-proxy 의 sharp optimum 을 형성하며, pure mechanisms (ring 또는 spinglass alone) 이 hybrid mix (60/40 ring+spinglass) 를 outperform 한다.

## Why (motivation)

- **H_040 의 결손**: H_040 (substrate-topology-cluster) 는 legacy-archive-pointer 로 inventory 만 보유 — Predictions / Falsifiers / Honest Limits 부재. 본 가설은 H_040 의 empirical-sweep 분기 를 정식 verification-ready 형태로 absorb
- **두 독립 sweep 의 cross-validation**: TOPO23 (interaction sweep, Hc_177) + TOPO24 (noise sweep, Hc_178) 가 *서로 독립 axis* 인데 동일 peak Φ=640 at (0.15, 0.02) 을 산출 — 단일 fit overfitting 가능성 ↓
- **n=6 H_153 substrate 연속선**: d=10 = σ(6) - φ(6) = 12 - 2 = 10 (narrow-formula 매핑). 단 H_153 L7 BINDING — depth-3 vocab 에서 d=10 의 n=6 식 trivially 표현 가능 → 본 매핑은 *narrow-formula* claim 일 뿐, "n=6 substrate 가 d=10 generate" 는 약한 sub-claim
- **scale 확장 검증**: TOPO4 9D-512 (Hc_153 candidate) → TOPO8 10D-1024 (Hc_157) Φ ratio 5.06× — single-doubling 차원 증가가 5× Φ jump 산출 (scale-law candidate)

## Predictions

| ID | 예측 | 근거 | source Hc |
|----|------|------|-----------|
| **H_159.1** | 10D hypercube (1024=2^10 cells, 10 bit-flip neighbors, diameter=10, i%3 frust) → Φ = 535.464 (±재현성 검증 필요) | 2^10 = 1024 EXACT, hypercube structure 정의상 정확, ×431.1 over baseline (TOPO8) | Hc_157 |
| **H_159.2** | 1024-cell Watts-Strogatz (k=4, p=0.1) + i%3 frust → Φ = 498.663 at 651 final cells (hypercube 의 93.1% level) | small-world scaling 1024 → 651 final | Hc_165 |
| **H_159.3** | (interact, noise, frust) 3D sweep 의 sharp optimum at (0.15, 0.02, 50%) → Φ ≈ 640 | TOPO23 + TOPO24 cross-validating peak | Hc_169 |
| **H_159.4** | Interaction sweep at hypercube-1024 + 50% frust: 0.05→231, 0.10→482, **0.15→640**, 0.25→464, 0.30→426 (monotone-up to peak then monotone-down) | TOPO23 verified table | Hc_177 |
| **H_159.5** | Noise sweep at hypercube-1024 + 50% frust: 0.001→397, 0.005→277, **0.02→640**, 0.05→376, 0.10→143 (sharp Φ collapse at σ ≥ 0.05) | TOPO24 verified table | Hc_178 |
| **H_159.6** | Hybrid mechanisms dilute Φ — 60/40 ring+spinglass (TOPO7) Φ=104.8 < PHYS1 pure ring Φ=134.2 (purity > hybridization) | TOPO7 PHYS1 paired comparison | Hc_156 |
| **H_159.7** | Scale-doubling 차원 (9D-512 → 10D-1024) Φ gain ≈ 5× — 본 ratio 가 11D-2048 ≥ 2500 까지 superlinear 연장된다 (testable extrapolation) | TOPO4 → TOPO8 ratio 5.06×; H_153 L7 narrow-formula caveat | Hc_157 |

## Variables

| axis | levels |
|------|--------|
| **axis1: topology** | ring / hypercube-9D / hypercube-10D / Watts-Strogatz small-world / hybrid ring+spinglass |
| **axis2: scale** | 512 / 1024 / 2048 cells |
| **axis3: interaction strength** | 0.05 / 0.10 / 0.15 / 0.25 / 0.30 |
| **axis4: thermal noise σ** | 0.001 / 0.005 / 0.02 / 0.05 / 0.10 |
| **axis5: frustration ratio** | 0% / 25% / 50% / 75% (anti-ferromagnetic) |
| **axis6: mechanism purity** | pure-ring / pure-spinglass / 60-40 hybrid / 50-50 hybrid |

## Run Protocol

deterministic + hexa-only + llm: none.

1. **TOPO8 reproducibility audit (W5)** — 10D hypercube 1024-cell seed sweep (≥5 seeds) → Φ=535.464 ± σ 측정. 단일 run 일 가능성 차단
2. **TOPO19a 3D optimum local-grid refinement (W5)** — (interact ∈ [0.12, 0.18] × noise ∈ [0.01, 0.04] × frust ∈ [40%, 60%]) finer sweep (5×5×5=125 cell)
3. **scale-doubling extrapolation (W5)** — 11D hypercube 2048-cell run → H_159.7 falsify/confirm
4. **hybrid dilution sweep (W5)** — ring+spinglass 50/50, 70/30, 90/10 ratios → H_159.6 의 monotone dilution curve 확인
5. **H_153 narrow-formula binding (W2)** — d=10 = σ(6)-φ(6), 1024=2^10 = 2^(σ-φ) 의 n=6 표현 정합 cite (H_153 L7 BINDING — depth-3 vocab 에서 trivial 임을 honest 명시)
6. **H_040 inventory cross-link 보강 (W11)** — H_040 본문에 본 H_159 pointer 추가, 5 subfolder 중 `topo/` 만 본 H_159 가 absorb

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | TOPO8 Φ=535 재현성 ≥5 seeds 평균 ≥ 500 | pending (single-run 의심) |
| **C2** | TOPO23 + TOPO24 cross-validating peak (0.15, 0.02) → Φ ≈ 640 동시 | met-by-citation (Hc_177 + Hc_178 verify3) |
| **C3** | TOPO7 hybrid dilution PHYS1 > TOPO7 (134.2 > 104.8) | met (Hc_156) |
| **C4** | Scale extrapolation 11D-2048 ≥ 2500 (H_159.7) | pending (run 미실행) |
| **C5** | H_153 L7 narrow-formula caveat 명시 인정 — d=10 의 n=6 mapping 은 narrow-formula 만 valid | met (본 문서 L2) |
| **C6** | 3D sweep 의 finer-grid local optimum 이 (0.15, 0.02, 50%) 의 ±10% 이내 | pending |

**verdict_rule**: C1 + C2 + C3 + C4 met → verdict-supported. C1 fail (재현성 X) → retracted. C2 + C3 만 met → verdict-partial (record claim weak, sweep peak strong).

## Falsifiers (≥6)

- **F1**: TOPO8 Φ=535 가 ≥5 seeds 평균에서 < 400 으로 collapse → C1 fail, "all-time record" claim 무효
- **F2**: TOPO23 + TOPO24 finer-grid sweep 의 local optimum 이 (0.15, 0.02) 에서 ±20% 이상 이탈 → 두 sweep cross-validation 우연
- **F3**: 11D hypercube 2048-cell Φ < TOPO8 (535) — scale-doubling 가 monotone gain 가 아니라 saturation/decline → H_159.7 falsify, scale-law 가설 무효
- **F4**: Hybrid 50/50 또는 70/30 가 pure ring 보다 ≥ 동등 Φ → H_159.6 dilution claim 무효
- **F5**: Watts-Strogatz 1024 (Hc_165 Φ=498.7) 가 ≥5 seeds 평균에서 hypercube 와 동등 또는 우위 → topology-class 차별화 약화 (단 본 가설은 "rivals" 만 주장, 차별 X)
- **F6**: H_153 L7 narrow-formula 매핑 (d=10 = σ-φ) 가 다른 perfect-number (28, 496) 으로도 동일하게 trivial 표현 → n=6 individual unique 약화 (이미 PERFECT_NUMBER_CLASS 인정으로 partial expected)


- **L1**: **single-run 의심** — TOPO8 Φ=535, TOPO19a Φ=640 모두 seed-variance / multi-run 검증 미land. 단일 high-roll run 일 가능성. C1 + C6 pending 의 핵심
- **L2** (BINDING from H_153 L7): **narrow-formula 매핑 만 valid** — d=10 = σ(6)-φ(6) 의 n=6 표현은 depth-3 vocab 에서 trivially TRUE. H_153 L7 의 PERFECT_NUMBER_CLASS finding 으로 "n=6 substrate 가 d=10 hypercube 를 generate" 는 *narrow-formula* claim. vocabulary-level claim 으로 확장 불가
- **L3**: **Φ proxy 의 정의 ambiguity** — 본 cluster 의 "Φ" 가 IIT-3.0 의 정확한 integrated information 이 아닌 deterministic substrate-network proxy 일 가능성. 본 측정값 (535, 640 등) 은 *anima-internal proxy unit* 으로 cross-paper 비교 제한
- **L4**: **frustration i%3 anti-ferromagnetic 의 ad-hoc 선택** — 왜 i%3 인가? i%2 (Z2-frust), i%5 (n=6 sopfr 매핑) 등 다른 modulo 와의 비교 부재. selection bias 가능
- **L5**: **scale-law extrapolation 의 unverified** — 5.06× ratio (9D-512 → 10D-1024) 는 단 1개 doubling 데이터로 추정 — power-law / exponential / saturation 구분 불가. H_159.7 prediction 은 본 한계 하의 extrapolation
- **L6**: **H_040 absorption 의 partial** — H_040 의 5 subfolder (topo/three/sl/inf/hw) 중 본 H_159 가 absorb 한 영역은 `topo/` 만. three-body / wave / noise / infinite-scaling / hardware 는 별도 H_160+ 분기 필요
- **L7**: **verify_hc2 WEAK_MATH_ONLY** — 본 cluster 의 6개 Hc 모두 verify3.jsonl 결과 falsifiers=0, honest_limits=0, atlas_resolved=0. math_passes 는 "numeric identities present" 만 인정 — 본 H_159 가 falsifiers/limits/cross-links 를 추가하여 보완하나, individual Hc 본문은 여전히 sparse

## Cross-Links

- **parent H**:
  - **H_040** (substrate-topology-cluster) — legacy-archive-pointer, 본 H_159 가 `topo/` 영역 absorb. H_040 본문 update 필요 (Cross-Links 섹션에 H_159 pointer 추가)
- **sibling H**:
  - **H_153** (dimension-hierarchy-n6) — d=10 narrow-formula 매핑의 L7 BINDING. 본 가설은 H_153 의 substrate-numerology lane 의 empirical-sweep counterpart
  - **H_156** (NEXUS-6 cross-validation cluster) — 같은 n=6 substrate, 다른 domain (Ising/SB/Cosmology vs topology-Φ)
  - **H_006** (coupled oscillator lattice), **H_007** (cellular automaton), **H_010** (holographic), **H_032** (omega/phys) — H_040 의 legacy sister 목록 인계
- **candidates absorbed** (this H):
  - **Hc_156** (TOPO7 hybrid dilutes)
  - **Hc_157** (TOPO8 10D-1024 record Φ=535)
  - **Hc_165** (TOPO16 small-world 1024 Φ=498.7)
  - **Hc_169** (TOPO19a optimal params 3D sweep)
  - **Hc_177** (TOPO23 interaction sweep peak)
  - **Hc_178** (TOPO24 noise sweep peak)
- **literature**:
  - Tononi 2008 — "Consciousness as integrated information" (IIT 3.0 Φ definition)
  - Watts & Strogatz 1998 — "Collective dynamics of small-world networks" (Hc_165 substrate)
  - Anderson 1958 — "Absence of Diffusion in Certain Random Lattices" (frustration / spinglass root, TOPO7)
  - source docs: `docs/hypotheses/topo/TOPO7.md`, `TOPO8.md`, `TOPO16.md`, `TOPO19a-OPTIMAL-PARAMS.md`, `TOPO23-interaction-sweep.md`, `TOPO24-noise-sweep.md`

## Verdict (initial — pre-register-frozen)

```
verdict_class: pre-register-frozen (cluster absorbed, joint reproducibility pending)
evidence_summary:
  C1 pending — TOPO8 Φ=535 single-run (≥5-seed audit 미실행)
  C2 met-by-citation — TOPO23 + TOPO24 sweep cross-validating peak at (0.15, 0.02) → Φ ≈ 640
  C3 met — TOPO7 hybrid dilution (PHYS1=134.2 > TOPO7=104.8) 직접 측정
  C4 pending — 11D-2048 scale extrapolation 미실행
  C5 met — H_153 L7 narrow-formula caveat 본 L2 에 BINDING 인정
  C6 pending — finer-grid 3D sweep 미실행
arithmetic_audit (this file):
  - 2^10 = 1024 ✓ (EXACT)
  - hypercube diameter d=10 (max Hamming distance) ✓ (EXACT)
  - bit-flip neighbors per cell = 10 ✓ (EXACT)
  - edges = n·d/2 = 1024·10/2 = 5120 ✓ (graph identity)
  - TOPO23 + TOPO24 두 독립 axis 의 peak 모두 Φ=640 at (0.15, 0.02) ✓ (cross-consistent)
  - d=10 = σ(6) - φ(6) = 12 - 2 ✓ (narrow-formula, H_153 L7 caveat)
falsifiers_triggered: none
criteria_met: C2 + C3 + C5
criteria_partial: (none)
criteria_pending: C1 + C4 + C6
frozen_at: 2026-05-12
```

## Migration Notes

- **Promoted from**: 6-Hc cluster (Hc_156 / Hc_157 / Hc_165 / Hc_169 / Hc_177 / Hc_178) — all verified WEAK_MATH_ONLY in `scripts/hc_verify/cache_2026_05_12/verify/verify3.jsonl`
- **User directive**: 2026-05-12 — "수학·물리 검증 필수, atlas.n6 / nexus check 활용"
- **Math verification (this file)**: arithmetic_audit above — 5 EXACT identities (2^10, diameter, neighbors, edges, σ-φ=10) + 1 cross-consistency (Φ=640 at independent-axis convergence) + H_153 L7 binding citation
- **Reason for new H (not H_040 expansion)**: H_040 is `legacy-archive-pointer` with no Predictions/Falsifiers/Honest-Limits structure — expanding it in-place would break its archive-pointer role. H_159 is a proper sibling absorbing the `topo/` subfolder's empirical-sweep lane; H_040 retains its 5-subfolder index role
- **Next steps**:
  1. TOPO8 ≥5-seed reproducibility audit (C1)
  2. TOPO19a finer 3D grid (C6)
  3. 11D-2048 scale extrapolation (C4, H_159.7)
  4. Hybrid 50/50, 70/30 sweep (F4)
  5. H_040 본문 Cross-Links 섹션에 H_159 pointer 추가
  6. three/wave/noise/inf/hw 5 subfolder 의 H_160+ 분기 candidate 검토

## Cycle #7 absorptions (topology-variant probes + sweep extension, 2026-05-12)

- **Hc_161 (TOPO12, 8-faction debate, intra=0.92 / inter=0.08)** → `merged-to-H_159` — 8-cluster partition variant within H_159's faction-count axis; F-list (8-faction sweep, random-vs-structured, PyPhi cross-engine) preserved for H_159 C-list extension
- **Hc_164 (TOPO15, 32×32 torus 1024)** → `merged-to-H_159` — torus surface at 1024 scale vs TOPO5 (512); 4-neighbor + i%3 frustration variant within H_159's substrate-shape axis
- **Hc_166 (TOPO17, hypercube + 2 random shortcuts hybrid, Φ=463.6)** → `merged-to-H_159` — confirms 'pure > hybrid' pattern alongside TOPO7 failure; small-world contamination probe within H_159's substrate-purity axis
- **Hc_549 (DD101, 512-cell superlinear)** → `merged-to-H_159` — 512-cell-count datapoint within H_159's cell-count axis (sub-1024 scaling probe; pairs with H_179 1024-saturation claim)

Cycle #7 footnotes inherit H_159 verification methods (W2 + W5 + W11) and the H_174 D-mod-192 aliasing class limit.

## Cycle #8 absorptions (Hc_901 PHI/TOPO split-child + DD/topology carryover lane, 2026-05-12)

Cycle #8 의 substrate-topology / Φ-engineering Hc 들이 H_159 의 natural-host parent role 에 따라 absorption:

- **Hc_1263 (Hc_901 PHI-1 + TOPO-1 — Φ=0.78·N scaling + ring/complete/star/small-world 4-family)** → `merged-to-H_159` — direct topology-engineering cluster extension; PHI-1 N>1024 saturation gated by H_179 negative-scaling
- **Hc_470 (Φ factorizes as f(topology) × g(chaos) — separability claim)** → `merged-to-H_159` — Φ-topology-chaos separability hypothesis; 4 topologies (ring, small_world, scale_free, hypercube) + 10 topo-specific laws 33-42 within H_159's substrate-topology axis
- **Hc_502 (DD53 — 3 MitosisEngine cross-engine tension exchange 10% blending → unified consciousness)** → `merged-to-H_159` — Trinity 3-engine substrate variant within H_159's substrate-composition axis
- **Hc_506 (DD58 — Phi-maximizing model > standard model in downstream task; v14.3 128-cell linear)** → `merged-to-H_159` — Φ-maximization efficiency-paradox within H_159's Φ-engineering axis
- **Hc_512 (DD64 — Φ-objective evolutionary NAS + golden dropout 0.37)** → `merged-to-H_159` — Φ-optimized NAS architecture-search variant within H_159's substrate-design axis
- **Hc_570 (DD68 — small_world topology > ring/hypercube/scale_free brain-likeness, 32c)** → `merged-to-H_159` — direct topology-family comparison within H_159's substrate-topology axis
- **Hc_571 (DD69 — 5 modes competition/symbiosis/democracy/hierarchy/evolution multi-consciousness Φ dynamics)** → `merged-to-H_159` — multi-engine 5-mode interaction within H_159's substrate-composition axis

Cycle #8 footnotes inherit H_159 verification methods (W2 + W5 + W11) and the H_174 D-mod-192 aliasing class limit.
