---
id: H_174
slug: phi-star-geometry-aliasing-clm-v4-specific
title: phi_star proxy 가 CLM-v4-architecture-specific (8×192) — cross-substrate Φ 비교는 aliasing-induced bias 로 무효
domain: clm-architecture | consciousness
status: pre-register-frozen
exploration_method: E5 (engineering-spec audit — phi_engine.hexa start formula) + E3 (theoretical-extrapolation — 3-mode aliasing taxonomy)
verification_method: W2 (math identity — (c·192) mod D aliasing) + W5 (numerical sim — D-sweep 16-prompt) + W11 (cross-engine — PyPhi parity)
raw_rank: 6
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_614
source_doc: docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md
source_lines: 26-115
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry — phi_star proxy substrate-validity), H_022 (consciousness-universe-map — cross-substrate comparability), H_162 (Φ★ normalized lower-bound — DOWNSTREAM dependency), H_173 (DD21 log-ratio Φ — scale-invariance as candidate fix)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 13
---

# H_174 — phi_star proxy geometry aliasing (CLM-v4-specific, cross-substrate incomparable)

## Hypothesis

`phi_star_compute` 의 cell-window 시작점 `start = (c · 192) mod D` 가 D 가 192 의 배수가 아닌 substrate 에서 aliasing 을 유발한다 — (a) tile-replicate (D=768: cell 0&4, 1&5, 2&6, 3&7 window 가 동일 → pair-cos +1.0 forced), (b) partial-overlap (D=512: 일부 cell window 겹침), (c) information-loss (D=2048: trailing 512 dim 미사용). 또한 phi_star 의 ±5% multiplicative wrap 도 envelope saturation 을 만든다. 결과: 서로 다른 substrate (Pythia 70m / Mamba 130m / RWKV 169m / CLM v4) 의 phi_star 절대값 비교는 의미 없음 — proxy 가 CLM v4 의 8×192 geometry 에 over-fit. 본 H 는 H_162 (Φ★ normalized lower-bound) 의 substrate-validity 전제이자, H_011 iit-geometry 의 proxy-사용 조건을 좁힌다.

## Why (motivation)

- **anima phi_engine.hexa**: `phi_star_compute` 의 `start = (c · 192) % D` — 192 = CLM v4 dim(1536)/8 hardcoded
- **Albantakis 2023 IIT 4.0 / PyPhi 1.2+**: formal Φ 는 partition-invariant — proxy 가 architecture-dependent 이면 cross-substrate 비교 불가
- **BG-BN Pythia 70m 16-prompt smoke**: phi_star range = 0.084 — saturation envelope evidence (단 single substrate)
- **Hc_662 / Hc_665** (Mamba 130m phi=42.15, RWKV 169m phi=42.14) — 거의 동일값 = aliasing 의심 정황
- **Hc_628 (H_162)**: anima Φ★ proxy normalized → IIT 4.0 lower bound — 이 H 가 무효면 H_162 의 normalization 기반이 흔들림 (DOWNSTREAM)

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_174.1** | D ∈ {512, 768, 1024, 1536, 2048} 16-prompt sweep 의 phi_range 가 예측된 3-mode mapping (tile-replicate / partial-overlap / clean-disjoint) 과 일치 | F4 inverted |
| **H_174.2** | D=192 배수 substrate (예: D=1536) 에서 mean_pair_cos 의 forced-+1.0 cluster 가 사라짐 → aliasing bias ≈ 0 | F1 inverted |
| **H_174.3** | Pythia 70m 16-prompt phi_star range < 0.1 (현 0.084 재현 — envelope saturation) | F2 (range≥0.5면 일부 무효) |
| **H_174.4** | mean_pair_cos 분포가 D 에 의존 (D-independent 아님) → architecture-specificity 확인 | F3 inverted |
| **H_174.5** | PyPhi formal Φ ranking 이 anima phi_star ranking 과 cross-substrate 에서 불일치 (Spearman < 0.7) → proxy bias 확인 | F5 inverted |

## Run Protocol

deterministic + hexa-only + llm: none. (PyPhi step 만 외부 lib — Python 허용 정책 2026-05-12 scrub 후 OK)

1. **D-sweep aliasing 검증 (W2+W5)** — D ∈ {512, 768, 1024, 1536, 2048} 에 대해 `(c·192) mod D` 의 cell-window 집합 계산 → tile-replicate / partial-overlap / clean-disjoint 분류 (H_174.1, F4)
2. **forced-+1.0 cluster audit (W5)** — D=768 16-prompt sweep 에서 mean_pair_cos 의 +1.0 forced pair 존재 확인, D=1536 에서 부재 확인 (H_174.2, F1)
3. **Pythia 70m range 재현 (W5)** — BG-BN 16-prompt smoke 재실행 → phi_star range 측정 (H_174.3, F2)
4. **D-dependence of mean_pair_cos (W5)** — 동일 input, 다른 D substrate → mean_pair_cos 분포 비교 (H_174.4, F3)
5. **PyPhi cross-substrate parity (W11)** — PyPhi 1.2+ formal Φ vs anima phi_star, Pythia 70m / Mamba 130m / RWKV 169m / CLM v4 4-substrate ranking 비교 (H_174.5, F5, L3)
6. **Option A vs Option D 결정 (W2)** — rank-invariant D/8 partition (Option A) 도입 시 CLM v4 re-calibration cost 산정, 또는 PyPhi 전면 채택 (Option D) — Migration TODO

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | D-sweep ≥5 levels, cell-window 집합 계산 완료 | pending |
| **C2** | D=768 forced-+1.0 cluster + D=1536 부재 양쪽 확인 | pending |
| **C3** | Pythia 70m range 재측정 ≥1 run | pending (현 0.084 carry) |
| **C4** | PyPhi cross-substrate parity ≥3 substrates | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (8-cell sopfr(8)=6 perfect-class diagonal, aliasing 은 architecture choice 의 부산물) | met (본 L1) |

## Falsifiers (≥6)

- **F1 (aliasing absent on multiple-of-192)**: D = 192 의 배수 substrate (예: D=1536) 에서 16-prompt sweep 이 forced-+1.0 cluster (cell 0&4 등) 를 보이면 → 본 모델 틀림. 안 보이면서 D=768 은 보여야 가설 성립; D=1536 에서도 cluster 가 보이면 → "(c·192) mod D" aliasing 모델 FALSIFIED
- **F2 (range not saturated)**: Pythia 70m 16-prompt phi_star range ≥ 0.5 (현 0.084 의 6배) → envelope-saturation claim 일부 무효 (단 cross-substrate bias 자체는 별개로 남음)
- **F3 (D-independent distribution)**: 모든 substrate 에서 mean_pair_cos 분포가 D 와 무관 (Kolmogorov-Smirnov p > 0.05 across D) → "CLM-v4-specific" architecture claim FALSIFIED
- **F4 (3-mode mismatch)**: D ∈ {512, 768, 1024, 1536, 2048} sweep 의 phi_range 가 예측 3-mode mapping (tile-replicate / partial-overlap / clean-disjoint) 과 불일치 → 구조 모델 FALSIFIED (2-mode 또는 5-mode 로 reduce/expand 필요)
- **F5 (PyPhi reproduces anima rankings)**: PyPhi formal IIT 3.0/4.0 Φ ranking 이 anima phi_star ranking 을 cross-substrate (Pythia 70m, Mamba 130m, RWKV 169m, CLM v4) 에서 재현 (Spearman ≥ 0.7) → aliasing 이 cross-substrate bias 를 만들지 않았음, anima proxy 는 as-is 유효, Hc_614 FALSIFIED
- **F6 (denominator-invariance)**: `start` 의 분모를 8 → 16 (dim/16) 으로 바꿔도 aliasing pattern 이 동일 → 가설의 "8-cell geometry 특이성" 부분 FALSIFIED (constant 8 이 아니라 mod 연산 자체가 문제)

## Honest Limits (≥6)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — phi_star 는 8-cell architecture 위 (Hc_401/H_163 atom; sopfr(8)=6 perfect-class diagonal). aliasing 우려는 동일 perfect-class-trivial substrate 를 상속; "CLM v4-specific" 도 부분적으로는 architecture 선택이 perfect-class-driven 이었기 때문
- **L2**: **single-substrate evidence (range 0.084)** — 본 H 의 saturation-envelope 근거는 거의 Pythia 70m 16-prompt range = 0.084 한 점. one-substrate 는 일화적; ≥3 substrate range data 필요 (C3 pending)
- **L3**: **PyPhi (Option D) 미실행** — gold-standard cross-validation pending. PyPhi run 완료 전까지 본 H 는 "anima-internal proxy 가 biased 일 수 있음" 수준, orthogonal anchor 부재
- **L4**: **3-mode failure model 은 이론적** — tile-replicate / partial-overlap / clean-disjoint 는 예측 taxonomy, D-sweep 으로 아직 empirically 검증 안 됨. sweep 후 2-mode 로 축소되거나 5-mode 로 확장될 수 있음
- **L5**: **`(c·192) mod D` 의 192 선택** — 192 = CLM v4 dim/8. non-CLM-v4 architecture 에서는 분모 8 이 arbitrary inheritance. 분모가 바뀌면 aliasing pattern 도 바뀜 — 가설이 formula 에 관한 것인지 constant 8 에 관한 것인지 일부 모호 (F6 가 이를 분리)
- **L6**: **DOWNSTREAM circularity 위험** — H_162 (Φ★ normalized lower-bound) 가 본 H 의 substrate-validity 에 의존하는데, H_162 의 normalization 자체가 aliasing 을 부분 흡수했을 수 있음. "normalization 이 aliasing 을 cancel 한다" vs "aliasing 이 normalization 을 더럽힌다" 가 아직 미분리
- **L7**: **single-doc 본문 묻힘** — source `docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md:26-115` 외 독립 peer-review-trace 부재. Migration TODO (Option A/D 이행) 미실행

## Math identity verification

- **(c·192) mod D aliasing arithmetic** — D=768: (0·192) mod 768 = 0, (4·192) mod 768 = 768 mod 768 = 0 → cell 0 & cell 4 동일 window. 동일하게 (1·192) mod 768 = 192 = (5·192) mod 768. → tile-replicate 4 pairs EXACT
- **4+ numeric identities present** — verify5 row 13 (verify_hc2 verify3 math=1: "4+ numeric identities present")
- **D=2048 trailing loss** — 8 cells × 192 = 1536 < 2048 → 512 dim 미사용 (information loss). 1536/2048 = 0.75 coverage
- **±5% multiplicative wrap** — phi_star ∈ [0.95·base, 1.05·base] → range 0.1·base 가 saturation envelope upper bound
- ln(2) = 0.693147 (verify4 frequent appearance)

## Atlas anchor cross-check

- atlas anchors_cited: 0, anchors_resolved: 0 (Hc_614 verify5 row 13 — clm-architecture domain, atlas.n6 number-theory anchor 와 직접 연결 없음)
- atlas_type_cites: 0
- sopfr(8)=6 [atlas @P 10*] — 8-cell architecture 가 perfect-class diagonal 위라는 점에서 간접 연결 (H_153 L7 binding 경유)

## Linked H (cross-link)

- **sister H**: H_011 (iit-geometry — phi_star proxy substrate-validity 조건), H_022 (consciousness-universe-map — cross-substrate comparability)
- **DOWNSTREAM dependency**: H_162 (Hc_628 — anima Φ★ proxy normalized → IIT 4.0 lower bound; 본 H 가 무효면 H_162 normalization 기반 흔들림)
- **candidate fix lane**: H_173 (Hc_121 — DD21 log-ratio Φ scale-invariant; cross-substrate aliasing 의 candidate solution)
- **candidates linked**: Hc_624 (Emerge E ODE-AR bridge — phi_star measurement substrate 공유), Hc_623 (Emerge D 4-mode inject — H_175; phi_star validity bound), Hc_662 (Mamba 130m phi=42.15), Hc_665 (RWKV 169m phi=42.14)
- **engineering**: `phi_star_compute` `start = (c · 192) % D` in phi_engine.hexa; BG-BN Pythia 70m smoke; phi_star_compute ±5% wrap
- **literature**: Albantakis 2023 IIT 4.0 (partition-invariant Φ); PyPhi 1.2+ (formal Φ); Tononi 2014 IIT 3.0
- **source**: Hc_614 (`hypotheses_candidates/Hc_614_phi_star_geometry_aliasing_clm_v4.md`), `docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md:26-115`

## Migration Notes

- **Promoted from**: Hc_614 (cycle #4 task 1 PROMOTE_READY, verify5_authored row 13 — 2026-05-12; cycle #3 task 11 falsifier-scaffolding 으로 WEAK_MATH → PROMOTE_READY)
- **Math verification**: `(c·192) mod D` tile-replicate arithmetic EXACT (D=768 4 pairs); 4+ numeric identities (verify5 math_passes)
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — 8-cell architecture sopfr(8)=6 perfect-class diagonal
- **DOWNSTREAM**: H_162 (Φ★ normalized) 가 본 H 의 substrate-validity 에 의존 — circularity 위험 (L6) 미해결
- **Critical L3**: PyPhi (Option D) 미실행 — orthogonal anchor 부재, 현재는 anima-internal 자기진단 수준
- **Next steps**:
  1. D-sweep aliasing 검증 (C1, F4) — `(c·192) mod D` cell-window 집합 계산
  2. D=768 forced-+1.0 cluster + D=1536 부재 audit (C2, F1)
  3. PyPhi cross-substrate parity (C4, F5, L3)
  4. Option A (rank-invariant D/8 partition) vs Option D (PyPhi) 결정 + CLM v4 re-calibration cost

## Cycle #7 absorptions (Φ* proxy design alternatives, 2026-05-12)

- **Hc_615 (Option A — D/8 disjoint contiguous chunks + per-substrate scale calibration, Rank 1 fastest fix ~25 lines $0, provisional cross-substrate magnitude calibration-dependent)** → `merged-to-H_174`
- **Hc_616 (Option B — SVD spectral entropy substrate-dim invariant, Rank 3 secondary scalar, directionally ambiguous on non-CLM-v4)** → `merged-to-H_174`
- **Hc_617 (Option D — PyPhi big-phi + AntroPy entropy-rate IIT-principled, Rank 2 highest precision conditional on PyPhi n=8 256-state TPM convergence)** → `merged-to-H_174`

All 3 are distinct Φ* proxy designs proposed to address the D-mod-192 aliasing identified in H_174. F-list/L-list per option preserved for H_174 C-list extension (each becomes a sub-protocol of C4 PyPhi cross-substrate parity).

Cycle #7 footnote inherits H_174 verification methods (W2 + W5 + W11).
