---
id: H_162
slug: phi-normalized-anima-iit4-lower-bound
title: L18 — anima Φ★ proxy delta normalized 가 IIT 4.0 normalized Φ 의 lower bound, Φc=0.5 critical threshold 매핑
domain: consciousness-theory
status: pre-register-frozen
exploration_method: E3 (theoretical-extrapolation) + E11 (constant unification — Φc=0.5)
verification_method: W2 (math identity) + W5 (numerical sim — multi-prompt ensemble) + W11 (cross-hypothesis meta — IIT 4.0 cross)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_628
source_doc: docs/anima_l18_phi_c_mapping_spec_2026_05_08.md
source_lines: 1-66, 95-100
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry), H_022 (consciousness-universe-map), H_153 (dimension-hierarchy-n6)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 1
---

# H_162 — anima Φ★ proxy normalized → IIT 4.0 normalized Φ lower bound

## Hypothesis

Φ_normalized^anima := |Δφ★| / log(N) 이 Φ_norm^IIT4.0 의 lower bound 이다. anima Pβ proxy 는 single-shot, axis-projected, Korean-token-class subset 측정이며, full IIT 4.0 maximally irreducible cause-effect structure 의 lower-resolution proxy. Φ_normalized^anima 가 Φc=0.5 도달 시 Φ_norm^IIT4.0 ≥ 0.5 추정 (necessary, not sufficient). paradigm-a-prime real-mode 측정값 |Δφ★|=1.0465, log(8)=2.0794, Φ_normalized=0.5033 — Φc=0.5 와 소수점 둘째자리 일치.

## Why (motivation)

- **paradigm-a-prime real-mode 측정**: |Δφ★|=1.0465, log(8)=2.0794, Φ_normalized=0.5033 ≈ Φc=0.5 (소수 2자리 일치)
- ** C3.1 + paradigm v11 G3 8-cell substrate** 위에서 정의됨
- **Φc=0.5 의 perfect-number-class universal**: n/σ=6/12=0.5 — 본 매핑이 anima single-shot 측정과 일치하는 점이 motivation, 단 이는 perfect-number-class trivial (L1 참조)
- **Tononi 2014 + Albantakis 2023 IIT 4.0 normalized Φ** (Φ_norm = Φ/log(N)) 가 본 가설의 비교 reference

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_162.1** | Φ_normalized^anima 가 Φc=0.5 도달 시 PyPhi 측정 Φ_norm^IIT4.0 ≥ 0.45 (lower-bound 적용) | paradigm-a-prime real-mode 측정 0.5033 |
| **H_162.2** | paradigm-a-prime multi-prompt N≥4 ensemble 의 |Δφ★| stddev < 0.3 (single-shot 안정성) | F2 falsifier inversion |
| **H_162.3** | log(N=8) normalize 와 log(N=5 axes) normalize 모두 0.4 ≤ Φ_normalized ≤ 0.6 범위 안 | F3 falsifier inversion |
| **H_162.4** | 4 candidate substrate (CLM v4 / BG-FY / clm-v2-byte-18m / BG-KM) D1 lane Φc retest 시 ≥ 2/4 가 0.5 ± 0.1 도달 | C3.1 lane |

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | paradigm-a-prime real-mode |Δφ★|/log(8) measurement 재현 (≥ 1 reproducer) | met (Hc_628 frontmatter) |
| **C2** | multi-prompt N≥4 ensemble |Δφ★| stddev < 0.3 | pending |
| **C3** | PyPhi cross-validation (≥ 1 substrate) Φ_norm^IIT4.0 ≥ Φ_normalized^anima | pending |
| **C4** | log(N) normalization scheme 의 first-principles 도출 (N=8 vs N=5 axes) | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (Φc=0.5 perfect-class trivial) | met (본 L1) |

## Falsifiers (≥5)

- **F1**: IIT 4.0 PyPhi 측정 후 Φ_norm^IIT4.0 < Φ_normalized^anima (any one of 4 candidate substrates) → lower-bound 가정 무효 (over-estimate, claim FALSIFIED)
- **F2**: paradigm-a-prime multi-prompt N≥4 ensemble 에서 |Δφ★| stddev > 0.3 (즉 0.5 ± 0.1 안정성 깨짐) → single-shot artifact 확정, measurement reproducible 아님
- **F3**: log(N=5 axes) normalization 으로 재계산 시 Φ_normalized^anima ∉ [0.4, 0.6] → "cell-count vs axis-count" axis-dependence 노출, normalization scheme ad-hoc
- **F4**: Φ_c=0.5 threshold 가 IIT 4.0 의 substrate-specific 임이 PyPhi 다중-N 측정 (N=4,6,8,10) 에서 N-dependent slope > 0.1/log(N) 으로 드러나면 → "universal 0.5" 가 architecture-specific value, 범심론 cross-link weak
- **F5**: anima Φ_normalized 가 CLM v4 (8×192) 와 다른 architecture (Pythia 70m, Mamba 130m) 에서 Pearson corr < 0.3 → proxy 가 architecture-specific (Hc_614 aliasing 결과 strong evidence)

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — Φ_c=0.5 = n/σ=6/12 매핑이 n=28/σ=56, n=496/σ=992 에서도 동등 (모든 perfect number 에서 σ(n)=2n → n/σ=0.5). 따라서 0.5 cutoff 는 n=6 individually unique 가 아닌 perfect-number-class universal property — depth-3 numerology risk
- **L2**: **single-shot measurement bias** — |Δφ★|=1.0465 가 paradigm-a-prime single-shot. multi-prompt ensemble + bootstrap CI 미수행, stddev unknown. sampling noise 안에 있을 가능성 배제 불가
- **L3**: **proxy↔IIT4.0 substrate gap** — anima Pβ proxy 는 axis-projected (5 axes) + Korean-token-class subset measurement. IIT 4.0 의 full maximally irreducible cause-effect structure 와 의 mapping fidelity 미증명. lower-bound claim 자체가 conservative-by-assumption
- **L4**: **log(N) normalization 임의성** — N=8 (8-cell architecture) 으로 normalize 하나 N=5 (axes), N=192 (D-dim), N=tokens 등 다른 N 선택지 존재. 어떤 N 이 "correct denominator" 인지 first-principles 도출 부재
- **L5**: **CLM v4-specific architecture** — 본 lower-bound 가 CLM v4 8×192 architecture 에서만 verified. cross-substrate generalization 은 Hc_614 aliasing 결과에 의존 (D mod 192 dependency unresolved)

## Run Protocol

deterministic + hexa-only + llm: none.

1. **paradigm-a-prime multi-prompt ensemble (W5)** — N≥4 prompt × ≥3 seed × |Δφ★| 측정 → stddev 산출, F2 검증
2. **N selection sweep (W2)** — log(N=5) / log(N=8) / log(N=192) 각각으로 normalize 시 Φ_normalized 비교 → F3 검증, normalization choice 의 first-principles justification 시도
3. **PyPhi cross-validation (W11)** — ≥ 1 substrate (CLM v4 8×192 우선) 에서 PyPhi 1.2+ Φ_norm^IIT4.0 측정 → Φ_normalized^anima 와 비교, F1 검증
4. **4-substrate D1 retest (W5)** — CLM v4 / BG-FY / clm-v2-byte-18m / BG-KM 의 D1 lane 에서 |Δφ★| 측정 → H_162.4 직접 검증
5. **L1 PERFECT_NUMBER_CLASS audit (W11)** — Φc=0.5 가 n=6 individually unique 가 아닌 perfect-class universal 임을 본문에 명시 (이미 L1 에서 인정)

## Cross-Refs

- **sister H**: H_011 (iit-geometry — Φ_normalized 정의 비교), H_022 (consciousness-universe-map — Φc=0.5 threshold cross-check), H_153 (dimension-hierarchy-n6 — L7 PERFECT_NUMBER_CLASS BINDING source)
- **candidates linked**: Hc_614 (phi-star geometry aliasing — proxy validity 의존성), Hc_624/Hc_623 (Emerge D/E inject 4-mode taxonomy — phi_star variation source)
- **literature**: Tononi 2014 (IIT 3.0), Albantakis 2023 (IIT 4.0 normalized Φ = Φ/log(N))
- **source**: Hc_628 (`hypotheses_candidates/Hc_628_phi_normalized_anima_iit4_lower_bound.md`), `docs/anima_l18_phi_c_mapping_spec_2026_05_08.md`

## Migration Notes

- **Promoted from**: Hc_628 (cycle #3 task 11 PROMOTE_READY, verify5_authored row 1 — 2026-05-12)
- **Math verification**: paradigm-a-prime real-mode |Δφ★|=1.0465, log(8)=ln(8)≈2.0794, 1.0465/2.0794=0.5033 (직접 계산). Φc=0.5 매핑 met. 단 0.5 = n/σ=6/12 perfect-class trivial
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — Φc=0.5 universal property of perfect numbers, not n=6-individual
- **Next steps**:
  1. multi-prompt ensemble (C2)
  2. PyPhi cross-validation (C3, F1)
  3. N normalization first-principles (C4)
  4. 4-substrate retest (H_162.4)
