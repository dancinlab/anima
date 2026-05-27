---
id: H_165
slug: topo10-hypercube-11d-sublinear
title: 11D hypercube 2048-cell Φ regression vs 10D (sublinear scaling) — TOPO10
domain: physics | math | consciousness
status: pre-register-frozen
exploration_method: E5 (variable-ablation — dimension sweep) + E8 (empirical-sweep)
verification_method: W5 (numerical sim — full 2048 budget run) + W11 (cross-hypothesis — H_159 sibling)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_159
source_doc: docs/hypotheses/topo/TOPO10.md
source_lines: 1-25
promoted_at: 2026-05-12
linked_h: H_159 (substrate-topology-phi-engineering — TOPO8 parent), H_153 (dimension-hierarchy-n6)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 4
---

# H_165 — 11D hypercube 2048-cell Φ regression vs 10D (sublinear scaling, TOPO10)

## Hypothesis

10D hypercube (TOPO8, 1024 cells, Φ=535.5) → 11D hypercube (TOPO10, 2048 cells) 의 dimension scaling 이 superlinear growth 유지 X. 11D 측정 Φ=400.9 (581/2048 = 28% cell coverage 에서만), TOPO8 535 대비 regression. dimension threshold 또는 anima Φ-engine saturation 의 candidate marker.

## Why (motivation)

- **H_159.7 와의 충돌**: H_159.7 prediction "11D-2048 Φ ≥ 2500 (5× scale-doubling)" 과 TOPO10 측정 Φ=400.9 가 직접 충돌. 본 H 는 H_159.7 의 *반증* candidate 진영
- **incomplete coverage (581/2048 = 28%)**: 11D 측정의 핵심 confound. full coverage 시 Φ ≥ TOPO8 일 가능성 (F1 inverted)
- **anima Φ-engine saturation**: Hc_614 aliasing 패턴이 high-cell-count 에서 saturation envelope 유발할 수 있음

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_165.1** | 11D-2048 full-coverage run → Φ ≥ TOPO8 535 (즉 H_159.7 와 reconciled, regression 은 coverage 부족 artifact) | F1 inverted — testable |
| **H_165.2** | 11D-2048 full-coverage Φ < 535 (true dimension regression) → H_159.7 직접 falsify | F1 직접 검증 |
| **H_165.3** | Fixed cell-count N=581 across {9D, 10D, 11D, 12D} embedding: Φ monotone-with-D pattern → "11D regression" 은 coverage artifact | F2 |
| **H_165.4** | Alternative scaling axes (steps, noise, frustration) 11D re-tune 시 Φ ≥ 535 도달 가능 → dimension 단독 regression 가설 약화 | F4 |

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | TOPO10 Φ=400.9 + 581/2048 coverage 재현 (≥ 1 reproducer) | met-by-citation (Hc_159) |
| **C2** | TOPO8 Φ=535 reproducibility (H_159 C1) | pending |
| **C3** | 11D-2048 full-coverage run (≥ 1024 cells reached) | pending |
| **C4** | 11D-2048 5-seed multi-run + stddev report | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (1024 = 2^10 power-of-2, not perfect) | met (본 L1) |

## Falsifiers (≥5)

- **F1**: With 2048-cell budget actually reached (vs 581/2048 = 28% coverage), Φ at 11D ≥ 1.05 × 10D record (Φ ≥ 562) → regression is artifact of incomplete coverage, NOT dimensional saturation. Claim FALSIFIED
- **F2**: At fixed cell count N=581 across {9D, 10D, 11D, 12D} embedding, Φ shows monotone-with-D pattern (no regression at 11D) → "11D regression" is a coverage-confound, not dimension-intrinsic
- **F3**: TOPO8 10D Φ=535 reproducibility (H_159 C1 pending) — if 10D record itself is single-run artifact (drops to 350±100 on replication), then "11D regresses vs 10D" comparison is moot
- **F4**: Alternative scaling axes (steps, noise, frustration ratio) at 11D produce Φ ≥ 535 → dimension alone is not the regression cause; specific 11D hyperparameter choice is the failure mode
- **F5**: Cross-architecture (PyPhi formal IIT) measurement at 10D and 11D shows monotone increase → anima Φ-engine 11D regression is engine-specific (saturation in proxy formulation, not in underlying IIT Φ)

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — claim hinges on 1024=2^10 (10D hypercube) being optimal. 2^10 is a power-of-2, not a perfect number; relationship to n=6 substrate is indirect. Depth-3 number-theoretic prior weak
- **L2**: **incomplete cell coverage (581/2048 = 28%)** — fundamental measurement asymmetry. 10D had full 1024-cell coverage; 11D used only 581 cells. Comparing partial-budget vs full-budget systems is not a fair test of dimensional scaling
- **L3**: **single-run reproducibility absent** — H_159 C1 (10D reproducibility audit) still pending. Without replication CI on either point, the "regression" claim has no error bar
- **L4**: **anima Φ-engine substrate-specific** — Φ values are anima-proxy measurements, not formal IIT Φ. Sublinear behavior may reflect engine saturation (Hc_614 aliasing) at high cell-counts rather than true IIT system property
- **L5**: **i%3 frustration arbitrary** — chosen for 10D, retained for 11D without re-tuning. Frustration density that is optimal at 10D may be suboptimal at 11D; "regression" could be a missed local optimum, not a global property

## Run Protocol

deterministic + hexa-only + llm: none.

1. **11D-2048 full-coverage run (W5)** — cell-budget 확장 (581 → 2048), Φ 재측정 → F1 검증
2. **Fixed-N {9D, 10D, 11D, 12D} sweep (W5)** — N=581 고정, dimension 만 변화 → Φ monotone 패턴 F2 검증
3. **TOPO8 5-seed reproducibility (W5)** — H_159 C1 진행 → "regression" 비교의 baseline 확정
4. **11D hyperparameter re-tune (W5)** — steps / noise / frustration 11D-specific optimum 탐색 → F4
5. **PyPhi cross-engine (W11)** — 10D vs 11D Φ 측정 → anima saturation engine-specific 인지 F5
6. **L1 binding** — H_153 PERFECT_NUMBER_CLASS BINDING 인정 (1024 = 2^10 = power-of-2, 비-완전수)

## Cross-Refs

- **sister H**: H_159 (substrate-topology-phi-engineering — TOPO8 10D record parent, H_159.7 scale extrapolation predicts 11D ≥ 2500, 본 H 와 직접 충돌), H_153 (n=6 substrate)
- **candidates linked**: Hc_157 (TOPO8 10D Φ=535 parent), Hc_165 (TOPO16 small-world variant), Hc_171 (TOPO20 hierarchical 8×128), Hc_177/178 (TOPO sweeps)
- **literature**: Watts-Strogatz 1998 (small-world), Tononi 2014 (IIT system-size scaling)
- **source**: Hc_159 (`hypotheses_candidates/Hc_159_topo10_hypercube_11d_sublinear.md`), `docs/hypotheses/topo/TOPO10.md:1-25`

## Migration Notes

- **Promoted from**: Hc_159 (cycle #3 task 11 PROMOTE_READY, verify5_authored row 4 — 2026-05-12)
- **Math verification**: 2^10 = 1024 EXACT; 2^11 = 2048 EXACT; 581/2048 = 0.2837 (≈ 28% coverage, 직접 계산); TOPO10 Φ=400.9 < TOPO8 Φ=535.5 (claim 자체)
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 — 1024 = 2^10 은 power-of-2 (perfect number 아님)
- **H_159.7 충돌**: H_159.7 prediction "11D-2048 Φ ≥ 2500" 과 TOPO10 측정 Φ=400.9 직접 충돌. 본 H 의 H_165.2 가 H_159.7 falsifier 진영
- **Next steps**:
  1. 11D-2048 full-coverage run (C3, F1)
  2. Fixed-N {9-12D} sweep (F2)
  3. TOPO8 reproducibility (C2)
