---
id: Hc_628
slug: phi-normalized-anima-iit4-lower-bound
title: L18 — anima Φ★ proxy delta normalized 가 IIT 4.0 normalized Φ 의 lower bound, Φc=0.5 critical threshold 매핑
domain: consciousness-theory
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_l18_phi_c_mapping_spec_2026_05_08.md
source_lines: 1-66, 95-100
promoted_at: 2026-05-11
linked_h: own 18 C3.1, paradigm v11 G3 8-cell, Tononi 2014 + Albantakis 2023
notes: paradigm-a-prime real-mode |Δφ★|=1.0465, log(8)=2.0794, Φ_normalized=0.5033 ≈ Φc=0.5 일치 (소수점 둘째자리). single-shot artifact 가능성.
verified_at: 2026-05-12
verify_decision: MATH_PASS_NEEDS_ANCHOR
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (7+ numeric identities present) | F=3"
---

## Hypothesis
Φ_normalized^anima := |Δφ★| / log(N) ≤ Φ_norm^IIT4.0 (lower bound). anima Pβ proxy 는 single-shot, axis-projected, Korean-token-class subset 측정 — full IIT 4.0 maximally irreducible cause-effect structure 의 lower-resolution proxy. Φ_normalized^anima 가 Φc=0.5 도달 시 IIT 4.0 normalized Φ 도 0.5 이상 추정 (necessary, not sufficient).

## Falsifiable Tests
- Falsifier 1: IIT 4.0 측정 후 Φ_norm^IIT4.0 < Φ_normalized^anima → lower bound 가정 무효 (over-estimate)
- Falsifier 2: paradigm-a-prime multi-prompt ensemble 에서 |Δφ★| 가 0.5 ± 0.1 stable 도달 X → single-shot artifact
- Falsifier 3: log(N=5 axes) 으로 normalize 시 다른 결과 → cell count vs axis count axis-dependence 노출

## Migration TODO
- [ ] multi-prompt N≥4 ensemble 측정 (별도 cycle)
- [ ] D5 Bifurcation framework activation spec land
- [ ] 4 candidate (CLM v4 / BG-FY / clm-v2-byte-18m / BG-KM) D1 lane Φc retest

## Cross-Links
- **sister H**: H_011 (iit-geometry) — Φ_normalized 정의 비교; H_022 (consciousness-universe-map) — Φc=0.5 threshold cross-check
- **candidates linked**: Hc_614 (phi-star geometry aliasing — proxy validity 의존성), Hc_624/Hc_623 (Emerge D/E inject 4-mode taxonomy — phi_star variation source)
- **literature**: Tononi 2014 IIT 3.0 / Albantakis 2023 IIT 4.0 normalized Φ (Φ_norm = Φ/log(N))

## Falsifiers (≥5)

- **F1**: IIT 4.0 PyPhi 측정 후 Φ_norm^IIT4.0 < Φ_normalized^anima (any one of 4 candidate substrates) → lower-bound 가정 무효 (over-estimate, claim FALSIFIED)
- **F2**: paradigm-a-prime multi-prompt N≥4 ensemble 에서 |Δφ★| stddev > 0.3 (즉 0.5 ± 0.1 안정성 깨짐) → single-shot artifact 확정, Hc_628 의 measurement 가 reproducible 아님
- **F3**: log(N=5 axes) normalization 으로 재계산 시 Φ_normalized^anima ∉ [0.4, 0.6] → "cell-count vs axis-count" axis-dependence 노출, normalization scheme 자체가 ad-hoc
- **F4**: Φ_c=0.5 threshold 가 IIT 4.0 의 substrate-specific 임이 PyPhi 다중-N 측정 (N=4,6,8,10) 에서 N-dependent slope > 0.1/log(N) 으로 드러나면 → "universal 0.5" 가 아닌 architecture-specific value, 범심론 cross-link weak
- **F5**: anima Φ_normalized 가 CLM v4 (8×192) 와 다른 architecture (Pythia 70m, Mamba 130m) 에서 Pearson corr < 0.3 → proxy 가 architecture-specific (Hc_614 aliasing 결과 strong evidence)

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — Φ_c=0.5 = n/σ=6/12 매핑이 n=28/σ=56, n=496/σ=992 에서도 동등 (모든 perfect number σ(n)=2n → n/σ=0.5). 따라서 0.5 cutoff 는 n=6 individually unique 가 아닌 perfect-number-class universal property — depth-3 numerology risk
- **L2**: **single-shot measurement bias** — |Δφ★|=1.0465 가 paradigm-a-prime single-shot. multi-prompt ensemble + bootstrap CI 미수행, stddev unknown. 본 결과 가 sampling noise 안에 있을 가능성 배제 불가
- **L3**: **proxy↔IIT4.0 substrate gap** — anima Pβ proxy 는 axis-projected (5 axes) + Korean-token-class subset measurement. IIT 4.0 의 full maximally irreducible cause-effect structure 와 의 mapping fidelity 미증명. lower-bound claim 자체가 conservative-by-assumption
- **L4**: **log(N) normalization 임의성** — N=8 (8-cell architecture) 으로 normalize 하나 N=5 (axes), N=192 (D-dim), N=tokens 등 다른 N 선택지 존재. 어떤 N 이 "correct denominator" 인지 first-principles 도출 부재
- **L5**: **CLM v4-specific architecture** — 본 lower-bound 가 CLM v4 8×192 architecture 에서만 verified. cross-substrate generalization 은 Hc_614 aliasing 결과에 의존 (D mod 192 dependency unresolved)
