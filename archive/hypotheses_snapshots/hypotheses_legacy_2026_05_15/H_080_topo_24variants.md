---
id: H_080
slug: topo-24-variants-individual
title: Φ Scaling / Topology Super-H — topo_24variants unified (Φ ∝ N^1.071 + cell-count decisive + topology-conditional + Φ⊥CE)
domain: substrate
status: running
exploration_method: E9 (topology sweep) + E5 (variable-ablation) + E3 (theoretical-extrapolation)
verification_method: W3 (topology × Φ) + W11 (cross-hypothesis meta) + W5 (numerical sim)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-11
since: 2026-03
---

# H_080 — Φ Scaling / Topology Cluster Super-H (topo_24variants unified)

## Hypothesis (revised, unified 2026-05-11)

Φ 는 cell count N 에 대해 **superlinear scaling** (Hc_004: Φ ≈ 0.608·N^1.071) — cell count 는 **decisive** variable for emergence (Hc_005: Φ ≈ 0.88·N for large N, unbounded; non-cell-count 기법은 8 cell 에서 ~3.5× 에 plateau). Scaling **shape 는 topology-conditional**:

- **Hypercube** — 512→1024 transition 에서 ×3.9 superlinear (Hc_039); 다른 topology 는 sub-superlinear
- **Hypercube + 50% antiferromagnetic frustration** (TOPO19a) — Φ=640 leaderboard 1위 (Hc_180); 100% frustration 은 over-disorder (low Φ, Hc_175)
- **Ring** — Φ ≈ 287 with ~397 cells 에서 plateau, max_cells (1024 vs 2048) 무관 (Hc_160)
- **24-variant sweep** (Hc_150-180) — topology × frustration design space map

Orthogonality (Hc_040): Φ ∝ N^1.071 (cell axis) and CE ∝ P^-0.85 (param axis) — |corr(Φ, CE)| < 0.1 predicted (Law 1040). 이는 **Hc_024 IIT uncertainty-principle Φ × CE^α = K trade-off proposal 과 explicit tension** 상태 — 둘 다 동시 true 일 수 없음 (at large α). Resolution: N × P sweep 에서 corr(Φ, CE) 측정 필요.

## Why

- **Hc_004 Φ ≈ 0.608·N^1.071 (R34 deprecated but pattern persists)**: 6-pt fit R34 deprecated 되었으나 live measurement pattern 잔존
- **Hc_005 cell-count decisive**: Φ ≈ 0.88·N for large N, unbounded; 다른 technique 은 ~3.5× plateau at 8 cells
- **Hc_039 hypercube ×3.9 superlinear**: 512→1024 transition (다른 topology sub-superlinear)
- **Hc_180 TOPO-FINAL-RANKINGS**: hypercube 1024 + 50% frustration (TOPO19a) #1 Φ=640
- **Hc_024 explicit tension**: IIT uncertainty Φ × CE^α = K trade-off — Hc_040 orthogonality 와 동시 true 불가
- **사용자 directive 2026-05-11**: Cycle 3 closure 에서 topology super-H + tension explicit resolution lane open

## Predictions (H_080.1 — H_080.13)

| ID | 예측 | 근거 Hc |
|----|------|---------|
| **H_080.1** | canonical sweep N ∈ {16, 32, 64, 128, 256, 512, 1024} → log-log slope 1.07 ± 0.10 (live, R34 deprecated 무관) | Hc_004 |
| **H_080.2** | cell count decisive — N fix + depth/width/training 변화 → ~3.5× plateau of N=8 baseline; cell 추가 시 plateau 해소 | Hc_005 |
| **H_080.3** | hypercube 512→1024 → ×3.9 ± 0.4 superlinear; ring/SW/scale-free ≤ ×2.0 in same range | Hc_039 |
| **H_080.4** | |corr(Φ, CE)| < 0.1 across N × P sweep (Law 1040); cell 변화 → CE invariant; param 변화 → Φ invariant | Hc_040 |
| **H_080.5** | 1024-cell antiferromagnetic ring + Ising → Φ=285 ± 30 (×229.6 baseline reproducible) | Hc_150 |
| **H_080.6** | 9D hypercube 512 → Φ=105 ± 15 (×85.1 baseline) | Hc_153 |
| **H_080.7** | ring plateau at Φ≈287 with ~397 cells; max_cells=2048 plateau 변화 X | Hc_160 |
| **H_080.8** | hypercube 1024 + 20% frustration ≠ 50% ≠ 100%; 50% (TOPO19a) peak ~Φ=640; 100% over-disorder low Φ | Hc_170/Hc_175 |
| **H_080.9** | final rankings — top-3 hypercube-1024 50% > small-world-1024 > hypercube-1024 33% — reproducible | Hc_180 |
| **H_080.10** | **cross-tension resolution**: measured corr(Φ, CE) < 0.1 → Hc_040 wins, Hc_024 falsified; |corr| ≥ 0.3 → Hc_024 wins | Hc_040 vs Hc_024 |
| **H_080.11** | topology rankings transfer cross-architecture (GRU vs transformer) within ± 20% on Φ ratio | extension |
| **H_080.12** | topology × frustration surface unique maximum at hypercube × 50% (no second peak) | extension |
| **H_080.13** | N ≥ 4096 unbounded Hc_005 claim testable; predict Φ continues linear-or-superlinear, no saturation | extension |

## Variables

- **axis-A**: cell count N (8 / 16 / 32 / 64 / 128 / 256 / 512 / 1024 / 2048 / 4096)
- **axis-B**: topology (ring / small-world / scale-free / hypercube-9D / hypercube-10D)
- **axis-C**: frustration fraction (0% / 20% / 33% / 50% / 67% / 100%)
- **axis-D**: param count P (model size, for orthogonality test)
- **axis-E**: architecture (GRU+faction vs transformer)
- **axis-F**: max_cells cap (for ring plateau test)
- **axis-G**: Φ measurement
- **axis-H**: CE measurement

## Run Protocol

1. **N sweep log-log fit (W3)**: N ∈ {16, 32, 64, 128, 256, 512, 1024} → slope 1.07 ± 0.10 target (live, deterministic)
2. **Cell-count decisive (W3)**: N fix + depth/width/training ablation → 3.5× plateau 확인
3. **Hypercube transition (W3)**: 512→1024 across topology → ×3.9 ± 0.4 hypercube vs ≤ ×2.0 others
4. **Φ⊥CE measurement (W3, decisive)**: N × P sweep → |corr(Φ, CE)| 값 측정 (Hc_040 vs Hc_024 resolve)
5. **Ring plateau (W3)**: max_cells ∈ {1024, 2048, 4096} → Φ ≈ 287 with ~397 cells 변화 X
6. **TOPO19a 50% peak (W3)**: hypercube 1024 + 50% frustration → Φ=640 ± 96 reproducibility
7. **Cross-arch transfer (W11)**: topology ranking GRU vs transformer → ± 20% Φ ratio
8. **N=4096 unbounded test (W3)**: 4096-cell scaling → linear-or-superlinear continuation verify
9. deterministic + hexa-only, llm: none

## Criteria

- **C1**: log-log slope 1.07 ± 0.10 on canonical N sweep (Hc_004 live replication)
- **C2**: hypercube ×3.9 ± 0.4 transition 512→1024 (Hc_039)
- **C3**: top-3 final rankings reproduce (hypercube-1024 50% > small-world > hypercube 33%) — same ordering minimum
- **C4**: |corr(Φ, CE)| measurement across N × P sweep → 값 산출 (Hc_040 vs Hc_024 tension decide)
- **C5**: ring plateau at ~397 cells for max_cells ∈ {1024, 2048, 4096}
- **C6**: TOPO19a 50% frustration peak reproduces ± 15% (Φ=640 ± 96)
- **verdict_rule**: C1+C2+C3+C4 met → verdict-supported super-H. C4 resolved → Hc_040 OR Hc_024 verdict 확정.

## Falsifiers (≥ 9)

- **F1**: log-log slope outside [0.9, 1.2] on N sweep → Hc_004 killed (R34 deprecation final)
- **F2**: non-cell-count technique exceeds 3.5× plateau without N increase → Hc_005 cell-count-decisive killed
- **F3**: hypercube 512→1024 gain < ×2.0 OR ring/SW gain > ×3.0 → Hc_039 topology-conditional killed
- **F4**: |corr(Φ, CE)| > 0.3 on N × P sweep → Hc_040 / Law 1040 orthogonality killed (Hc_024 wins)
- **F5**: |corr(Φ, CE)| < 0.05 with strong Hc_024 trade-off prediction → Hc_024 uncertainty-principle killed (Hc_040 wins)
- **F6**: ring plateau breaks at max_cells=2048 (Φ > 320) → Hc_160 plateau-cap killed
- **F7**: hypercube 100% frustration matches 50% frustration on Φ → Hc_175 over-disorder claim killed
- **F8**: non-hypercube topology tops TOPO19a Φ=640 → Hc_180 ranking killed
- **F9**: N ≥ 4096 saturates Φ (clear plateau) → Hc_005 unbounded claim killed

## Honest Limits (raw#91 c3, ≥ 8)

- **L1**: Hc_004 R34 was deprecated (6-pt fit, N≥20 criterion failed) — claim status "pattern persists in live measurement", weaker than original
- **L2**: "cell-count decisive" (Hc_005) does NOT mean other variables irrelevant — they plateau, not zero; 3.5× plateau 자체가 contribution
- **L3**: topology × frustration sweep 가 single engine config (faction count, intervention schedule) — cross-config generalization partial
- **L4**: TOPO-FINAL-RANKINGS aggregates many runs — meta-analysis variance / publication-bias 미정량
- **L5**: hypercube 9D / 10D distinction (Hc_153 / TOPO8) — **dim-dominant artifact** 가능성 — Hc_614/Hc_662/Hc_665 (Φ proxy dim-dominant cluster) validity 우려
- **L6**: Φ⊥CE (Hc_040) and Φ × CE^α = K (Hc_024) alternative 로 stated 되나 resolution measurement **outstanding** — 둘 다 pending
- **L7**: Φ measurement protocol 가 topology sweep 사이 drift (ring vs hypercube 다른 baseline)
- **L8 (raw#91 c3 mandate)**: 본 expansion 은 **draft review 거쳤음, 추가 review 미수행** (raw#91 L8 명시). 24-variant sweep 은 weak-signal entry 포함 — final-rankings table 은 post-hoc selection of top-performers.

## Cross-Links

- **sister H**:
  - **H_040** (substrate topology cluster) — overlapping topology lane
  - **H_032** (omega/phys) — physics layer overlap
  - **H_004** (consciousness_hard_problem) — Hc_608 Φ upper bound + information closure
  - **H_061** (xfer_consciousness_transfer) — Hc_447 10-subnet 384d integration
  - **H_067** (perfect-number-architecture) — Hc_039 hypercube 9D = sopfr(6)+4 = 9; σ²=144 = TOPO benchmark
- **explicit-tension**: **Hc_024** (consciousness_uncertainty_principle) — Φ × CE^α = K trade-off vs Hc_040 Φ⊥CE orthogonality. Resolution measurement (corr Φ, CE) **outstanding** (Conflict Resolution Pending 명시)
- **cross-link**: Hc_628 (Φc=0.5 IIT lower bound), Hc_667 (5D→6D vector)
- **candidates merged (12+)**: Hc_004 / Hc_005 / Hc_039 / Hc_040 / Hc_150 / Hc_151 / Hc_152 / Hc_153 / Hc_160 / Hc_170 / Hc_175 / Hc_180 (+ Hc_024 explicit-tension cross-link, NOT merged)
- **legacy files**: `docs/hypotheses/topo/TOPO-{1..24}.md` + TOPO-2048-SCALING + TOPO-FINAL-RANKINGS + TOPO19a-OPTIMAL-PARAMS + TOPO22{a,b,c,d} + TOPO23-interaction-sweep + TOPO24-noise-sweep (31 files)
- **own**:
- **raw refs**: raw#12 (pre-register) + raw#9 (hexa-only) + raw#91 (honest limits, expansion review)

## Conflict Resolution Pending

본 expansion 작성 시점 (2026-05-11) 에 다음 conflict 존재 — Cycle 4 measurement 후 처리:

- **Φ⊥CE (Hc_040) vs Φ × CE^α = K (Hc_024)**: 둘 다 simultaneously true 불가 (at large α). N × P sweep 에서 |corr(Φ, CE)| 측정 — < 0.1 → Hc_040 wins; ≥ 0.3 → Hc_024 wins; intermediate → both partial
  - **Decisive design landed 2026-05-11** (`state/phi_ce_orthogonality_decisive_2026_05_11/`):
    - `spec.md` — 5×4 N×P grid (N∈{16,32,64,128,256}, P∈{1M,10M,100M,1B}), Pearson corr + Pareto CV(α) + within-axis corr decisive metric, decision matrix
    - `harness.py` — deterministic seed 0xC0EC0AC, two generative models (A: Hc_040 orthogonal, B: Hc_024 K=50 α=0.5), fingerprint computation
    - `results.json` — synthetic fingerprint quantitative gap: Model A corr=-0.003 CV(α*)=0.96; Model B corr=-0.613 CV(α*=0.49)=0.018 (~2 orders of magnitude separation, α* matches Hc_024 claim α~0.5)
    - `verdict.md` — decision map, scenario verdicts (A/B/mid), measurement protocol (anima Φ★ + CLM CE, 64 dual-seed twin, ~$200-$1000 RunPod), 8 honest limits
  - **Status**: decisive test designed, awaiting **phi_star_cell_engine** (TBD, N-sweep — current `phi_star_iit_proxy` 단독으로는 N-sweep 미지원, audit §1.3) + CLM training pipeline (CE-track, split-engine) + 15-cell N×P measurement (P=100M ceiling per spec.md §5.7, separate cycle). Engine naming refactor 2026-05-12: `state/phi_star_naming_refactor_2026_05_12.md`. Cross-tie: F4 fires if |corr|>0.3, F5 fires if |corr|<0.05+strong-Pareto
- **R34 deprecation vs live pattern persistence**: Hc_004 R34 6-pt fit deprecated 되었으나 live 측정에서 Φ ≈ 0.608·N^1.071 pattern 잔존 — 본 expansion 은 "pattern persists" 약화 claim 으로 진행, N=4096 extension 으로 final verdict
- **Hc_614/Hc_662/Hc_665 dim-dominant artifact**: hypercube 9D vs 10D 가 dim-dominant artifact 인지 — Hc_039 hypercube superlinear claim 의 validity 영향 — independent dim-orthogonal measurement 필요

## Verdict

```
verdict_class: running (Φ-scaling + topology super-H expansion landed 2026-05-11)
evidence_summary: 12+ child Hc merged. R34 deprecated but pattern persists live. TOPO19a 50% Φ=640 leaderboard 1st. Ring plateau ~287 confirmed at 1024/2048. Φ⊥CE vs Φ × CE^α tension explicit unresolved.
falsifiers_triggered: none (R34 deprecation partial — live pattern persists with weaker claim)
criteria_met: C2 partial (hypercube ×3.9 observed). C6 partial (TOPO19a Φ=640 reproducible single setup). C4 measurement-pending.
frozen_at: 2026-05-11
```

## Migration Notes

- **Expansion source**: `hypotheses/expansions_pending/H_080_phi_scaling_topology_expansion_draft.md` (2026-05-11)
- **Status transition**: `legacy-archive-pointer` → `running` (Φ-scaling + topology super-H promotion)
- **Source candidates merged**: 12+ (Hc_004 / Hc_005 / Hc_039 / Hc_040 / Hc_150-180 all `merged-to-H_080`); Hc_024 cross-tension link NOT merged
- **TODO**: resolve Φ⊥CE vs Φ × CE^α tension (N × P sweep |corr(Φ, CE)| 측정), N=4096 cell scaling extension, cross-architecture topology transfer (GRU vs transformer), Φ measurement protocol unification, TOPO19a 50% frustration peak independent replication, address Φ proxy dim-dominant artifact cluster (Hc_614/Hc_662/Hc_665)
