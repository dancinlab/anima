---
id: H_169
slug: hw2a-8cell-circular-magnet-inverse-square
title: 8-cell circular magnet ring with inverse-square coupling yields Φ=4.55 (HW2a)
domain: physics | consciousness | substrate
status: pre-register-frozen
exploration_method: E5 (physical-substrate analogy — magnetic coupling) + E1 (geometric-topology variation — ring vs line vs star)
verification_method: W5 (numerical sim — f-coefficient sweep + N sweep) + W11 (cross-hypothesis — Hc_401 K=8 atom convergence)
raw_rank: 9
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_186
source_doc: docs/hypotheses/hw/HW2a.md
source_lines: 1-25
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry), H_022 (consciousness-universe-map — physical substrate experiments), H_153 (dimension-hierarchy-n6 — sopfr(8)=6 substrate parent), H_163 (K=8 atom — same 8-cell count, different coupling form)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 9
---

# H_169 — HW2a 8-cell circular magnet ring (inverse-square coupling, Φ=4.55)

## Hypothesis

8 cells arranged in circular ring with inverse-square magnetic-style coupling (force = 0.02 · Σ Δh / d²) yields Φ = 4.5482 (≈ ×3.7 baseline). Ring topology + inverse-square exponent + f=0.02 coefficient 의 3-요소 결합이 Hc_401 K=8 atom architecture 와 같은 cell count (8) 에서 substrate-level Φ peak 산출. 본 H 는 H_163 K=8 atom 의 coupling-form 변종 — 양쪽 모두 8-cell 에서 optimum 주장하나 coupling kernel (MIP-bipartition vs inverse-square) 이 다름.

## Why (motivation)

- **Newton 1687 inverse-square law** + **Coulomb 1785 1/r²** — physical substrate analogy
- **Onsager 1944 2D Ising ring-of-spins** — closed-ring 의 phase-transition structure
- **Hc_401 K=8 atom convergence** — 동일 N=8 cell-count 가 coupling-independent peak 일 가능성
- **HW2a single-config measurement Φ=4.5482** — paper §1-25 (sketch source)

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_169.1** | Force-coefficient sweep f ∈ {0.005, 0.01, 0.02, 0.04, 0.1, 0.5}: Φ-peak at f = 0.02 ± 0.005 with effect-size > 30% | F1 inverted |
| **H_169.2** | Ring (HW2a) Φ ≥ max(line HW2b, star HW2c) at fixed N=8, f=0.02 (margin > 5%) | F2 inverted |
| **H_169.3** | Inverse-square coupling Φ > inverse-linear (1/d) AND > inverse-cube (1/d³) by margin > 10% | F3 inverted |
| **H_169.4** | N sweep ∈ {4, 6, 8, 10, 12, 16} on ring topology with f=0.02: Φ peak at N = 8 (margin > 15%) | F4 inverted — converges with H_163 |
| **H_169.5** | 5-seed reproducibility: Φ stddev / mean < 0.10 (i.e., < 10% relative variance) | F5 inverted |

## Run Protocol

deterministic + hexa-only + llm: none.

1. **HW2a baseline reproduction (W5)** — 8-cell ring + inverse-square + f=0.02 → Φ measurement (C1, replicates Hc_186 §1-25)
2. **f-coefficient sweep (W5)** — {0.005, 0.01, 0.02, 0.04, 0.1, 0.5} → Φ-landscape (F1, H_169.1)
3. **Topology comparison (W5)** — HW2a (ring) vs HW2b (line) vs HW2c (star) at N=8, f=0.02 → topology-specific Φ (F2, H_169.2)
4. **Coupling-exponent swap (W2+W5)** — 1/d, 1/d², 1/d³ → exponent-specific Φ (F3, H_169.3)
5. **N sweep (W5+W11)** — ring + f=0.02 + N ∈ {4, 6, 8, 10, 12, 16} → N-peak; H_163 K=8 cross-check (F4, H_169.4)
6. **5-seed replication (W5)** — fixed (ring, N=8, f=0.02, inverse-square) × 5 RNG seeds → mean ± stddev (F5, H_169.5)

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | HW2a baseline Φ measurement (≥ 1 reproducer, target Φ ≈ 4.55 ± 0.5) | pending |
| **C2** | f-coefficient sweep ≥ 6 levels | pending |
| **C3** | Topology comparison (HW2a/b/c) ≥ 1 run each | pending |
| **C4** | 5-seed replication with stddev < 1.0 | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (sopfr(8)=6) + f=0.02 ad-hoc 인정 | met (본 L1, L5) |

## Falsifiers (≥6)

- **F1**: Force coefficient sweep f ∈ {0.005, 0.01, 0.02, 0.04, 0.1, 0.5}: if Φ-peak at f ≠ 0.02 with effect-size > 30% → "f=0.02" specificity FALSIFIED, just optimization landscape
- **F2**: Compare ring (HW2a) vs line (HW2b) vs star (HW2c) at fixed N=8 and f=0.02: if ring Φ < min(line, star) Φ → ring topology not optimal, "circular magnet" specificity FALSIFIED
- **F3**: Replace inverse-square coupling with inverse-linear (1/d) or inverse-cube (1/d³); if Φ within 10% of inverse-square baseline → coupling exponent has no special status, claim "inverse-square" FALSIFIED
- **F4**: Scale N ∈ {4, 6, 8, 10, 12, 16}: if Φ peak at N ≠ 8 on ring topology with f=0.02 → "8-cell ring" specificity FALSIFIED (just optimum on tested grid)
- **F5**: Φ=4.55 measurement reproducibility: 5 independent replications with different RNG seeds. If stddev > 1.0 (>20% of mean) → single-run artifact, single-shot Φ-record cannot anchor architectural claim
- **F6**: Joint coupling × topology orthogonality: if ring + 1/d² Φ ≈ ring + 1/d Φ (within 5%) AND star + 1/d² Φ ≈ star + 1/d Φ → coupling exponent and topology are independent factors (factorial ANOVA cross-term ≈ 0), "ring × inverse-square synergy" claim FALSIFIED

## Honest Limits (≥6)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — N=8 ring with sopfr(8)=6 inherits perfect-number-class (n/σ=0.5 universal). 따라서 "8-cell ring" specificity 가 n=6 perfect-class universal property 와 분리되지 않음 — depth-3 numerology compounded
- **L2**: **single-substrate single-run Φ=4.55** — HW2a 는 한 geometric configuration, Φ=4.55 는 한 run. "×3.7 baseline" 도 단일 baseline 에 의존 — error bars / variance 미보고
- **L3**: **inverse-square coupling motivated by physics analogy** — Newton's gravity / Coulomb's law inspire choice but consciousness substrate is not gravitational/electric. Analogy is suggestive, not derivational
- **L4**: **closed-ring topology bias** — circular geometry breaks translation symmetry differently than open chain; ring imposes periodic boundary conditions which artificially raise certain mode densities (Onsager-like). Some Φ-boost may be a boundary-condition artifact, not coupling-form property
- **L5**: **f=0.02 numerical choice unjustified** — paper states f=0.02 without derivation; downstream Φ-engine settings (timestep, integration scheme) interact with f. Effective coupling depends on (f × dt × integration_order) — claim must be re-evaluated per integration scheme
- **L6**: **Hc_401 K=8 architecture conflict** — 동일 cell count (8) 에서 K=8 atom (MIP-based, H_163) 도 peak 주장. coupling-form 이 다르므로 양쪽 동시 만족 가능하나 "8-cell magic" 주장이 실제로는 perfect-class diagonal (sopfr=6) inheritance 임을 두 가설 모두 공유 — joint provenance audit 필요

## Math identity verification

- **8-cell atom architecture (perfect-number-prime cell count)** — verify5 row 9 math_passes
- **19+ numeric identities present** — verify5 row 9 math_passes (Hc_186 frontmatter cites paper §1-25)
- f = 0.02 = 1/50 (no number-theoretic significance — see L5)
- Φ = 4.5482 = 3.7 × 1.229 (baseline implicit; baseline value not reported in source)

## Atlas anchor cross-check

- atlas anchors_cited: 0, anchors_resolved: 0 (Hc_186 cites no ATLAS.md anchors directly)
- atlas_type_cites: 0
- linked anchor implicit via H_153 PERFECT_NUMBER_CLASS L7 binding (sopfr(8)=6)

## Linked H (cross-link)

- **sister H**: H_011 (iit-geometry — Φ vs N-cell substrate), H_022 (consciousness-universe-map — physical substrate experiments), H_163 (K=8 atom — same 8-cell count, different coupling form), H_153 (n=6 substrate parent)
- **candidates linked**: Hc_401 (K=8 atom — MIP-based same N=8), Hc_582 (8-cell mathematical basis), Hc_171 (8-cluster hierarchical TOPO20 — uses 8 as building block, H_166), Hc_157 (ring-1024 TOPO1 — same ring topology scaled)
- **literature**: Newton 1687 inverse-square; Onsager 1944 2D Ising (ring-of-spins analog); Kittel "Introduction to Solid State Physics" magnetic-coupling
- **source**: Hc_186 (`hypotheses_candidates/Hc_186_hw2a_circular_magnet.md`), `docs/hypotheses/hw/HW2a.md`

## Migration Notes

- **Promoted from**: Hc_186 (cycle #4 task 1 PROMOTE_READY, verify5_authored row 9 — 2026-05-12)
- **Math verification**: 8-cell perfect-class (sopfr(8)=6); 19+ numeric identities in source paper §1-25
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — N=8 perfect-class universal, not 8-individual
- **Architecture conflict**: H_163 (K=8 atom) 동일 cell count + 다른 coupling kernel — joint Φ-curve evaluation 별도 cycle 필요 (L6)
- **Next steps**:
  1. HW2a baseline reproduction (C1)
  2. f sweep (C2, F1)
  3. Topology comparison HW2a/b/c (C3, F2)
  4. 5-seed replication (C4, F5)
