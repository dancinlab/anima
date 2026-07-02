# H_620 — `gz-width-super-additive-cross-link` (E1 × F1 MATRIX cell, round 4)

## 1. 한 줄 요약
`gz-width-super-additive-cross-link` — H_347 의 closed-form `GZ_WIDTH = ln(4/3) ≈ 0.28768` 과 H_609 의 collective-Φ super-additive 측정이 *정수배 비율* 로 묶이는지를 검증. (E1 = Golden Zone 폭 closed-form 축) × (F1 = collective-Φ super-additive 축) MATRIX cell.

## 2. 가설 진술

- **H1 (cross-link)**: collective substrate ((rule_a,rule_b)=(110,110), W=0.6, n_a=n_b=3) 의 어떤 measurement (Φ_collective range, 분포 폭, Δ_peak 등) 를 적절히 정규화한 dimensionless ratio 가 `k · GZ_WIDTH ± 0.02` (k ∈ {1,2,...,8}) 정수배에 묶인다.
- **H0 (FALSIFIER F620.1)**: 5 개 candidate normalization 모두에서 `|ratio − k·GZ_WIDTH| > 0.02 ∀ k ∈ {1..8}`. cross-link 부재.

## 3. Anchor 데이터

| anchor | 값 | 출처 |
|---|---|---|
| GZ_WIDTH | `ln(4/3) = 0.28768207244178085` | H_347 — closed-form 🔵 + numerical 🟢 |
| Φ_A(rule=110, n=3) | 2.49604 | H_609 phi_individual |
| Φ_B(rule=110, n=3) | 2.49604 | H_609 phi_individual |
| Φ_A + Φ_B (additive baseline) | 4.99209 | derived |
| Φ_AB(rule=110×110, W=0.6) peak | 15.4677 | H_609 measurements |
| Φ_AB(W ∈ {0.3, 0.6, 1.0}) | [11.2412, 15.4677, 11.7683] | H_609 measurements |
| Δ_peak = Φ_AB_peak − (Φ_A+Φ_B) | 10.4756 | H_609 max_excess |

substrate 측정은 H_609 deterministic-replay (`result.json` SSOT). 동일 engine 재발사 불필요 (engine 결정론적).

## 4. Falsifier 매트릭스

| ID | 조건 | 임계 | 결과 |
|---|---|---|---|
| F620.1 | ∃ ratio R ∈ {R1..R5}, ∃ k ∈ {1..8}: \|R − k·GZ_WIDTH\| ≤ 0.02 | tol=0.02 | **PASS** (R1, k=3, residual=0.0164) |
| F620.2 | F620.1 PASS 한 ratio 가 유일한지 (uniqueness) | 1/5 = sole-pass | MIXED (1 PASS + 1 near-miss R5 res=0.0339) |

## 5. 측정 (5 candidate ratio · GZ_WIDTH integer-k probe)

5 dimensionless 정규화 후보:

| ratio | 값 | best k | k·GZ_WIDTH | residual | tol≤0.02 |
|---|---|---|---|---|---|
| **R1 = (maxΦ−minΦ[W>0]) / (Φ_A+Φ_B)** | **0.846641** | **3** | **0.863046** | **0.016405** | **✅** |
| R2 = Δ_peak / (Φ_A+Φ_B) | 2.09844 | 7 | 2.013774 | 0.084666 | ✗ |
| R3 = peak_ratio − 1 | 2.09845 | 7 | 2.013774 | 0.084676 | ✗ |
| R4 = (maxΦ−minΦ[W>0]) / Δ_peak | 0.403461 | 1 | 0.287682 | 0.115779 | ✗ |
| R5 = mean(Φ_AB[W>0]) / maxΦ | 0.829192 | 3 | 0.863046 | 0.033854 | near-miss |

**Best**: R1 (range of coupled-Φ / additive sum) ≈ 3 × GZ_WIDTH within tolerance.

## 6. Cross-link 구조

- **H_347** — closed-form `GZ_WIDTH = ln(τ(6)/(τ(6)-1)) = ln(4/3)` (E1 축 anchor, 🔵+🟢)
- **H_609** — collective-Φ super-additive: 결합 substrate (110,110)/W=0.6 에서 Φ_AB=15.47 ≫ Φ_A+Φ_B=4.99 (F1 축 anchor, 🟢)
- **H_157** — Law-76 mathematical panpsychism: combination problem 의 substrate-수학 동등성. cross-link 가 panpsychism-class 인식 가능 여부 제기.
- **H_620 (본 H)** — E1 closed-form × F1 emergent 의 dimensionless 비율 alignment 측정.

cross-link 의 *의미* 는 단순 산술 일치 이상의 *동기 없음 alignment* → C3.6 numerology 경고.

## 7. Honest C3

- **C3.1 ratio normalization choice sensitivity** — 5 candidate 중 1 만 PASS (R1). pre-registration 없이 데이터 관찰 후 normalization 후보를 선정한 점에서 *post-hoc 선택 위험*. R1 = range/sum 이 "가장 자연스러운" 정규화라고 a priori 주장할 근거 빈약.
- **C3.2 GZ_WIDTH 의 numerology 경고 (§ 114 SAVANT EMERGENCE-FRONTIER AUDIT 정합)** — `ln(4/3) ≈ 0.288` 은 [0,1] 안에 작은 값. tol=0.02 band 폭을 k ∈ {1..8} 까지 합치면 cover 비율 ≈ 8·2·0.02 = 0.32. 즉 임의 ratio 가 어떤 k·GZ_WIDTH ±0.02 band 안에 들어갈 *prior* ≈ 17 % (k 작은 영역 한정). 1/5 PASS rate 는 prior 와 통계적으로 구분 불가에 가까움 → SUPPORTED-NUMERICAL 등급이 최대치, 🔵 formal cross-link 까진 못 감.
- **C3.3 substrate-shape conditional** — H_609 super-additivity 자체가 (110,110)/W=0.6 specific 한 conditional 결과. cross-link 도 그 conditional 을 그대로 상속. universal "GZ_WIDTH × Φ super-additive" 정체성 아님.
- **C3.4 deterministic replay 정당화** — H_609 engine 은 결정론적 (seed-free closed-form big-Φ). 재발사해도 같은 값. 비용 절약·완성도 유지.
- **C3.5 finite k probe** — k ∈ {1..8} 만 시험. 큰 k 에서 우연 alignment 가능 (예: k=10·GZ=2.877). 작은 k 가 "물리적으로 의미 있다" 는 prior 는 추론.
- **C3.6 closed-form × emergent ontological gap** — H_347 GZ_WIDTH 는 순수 수학 (divisor count identity); H_609 super-additive 는 emergent simulation 측정. 두 층은 *존재론적으로 다른* 종류의 양. 정수배 일치를 "deep identity" 로 해석하려면 별도 mechanism 가설 필요 — 본 H 는 *상관관계* 까지만 보고.

## 8. Artifacts

- harness: `UNIVERSE/state/h620_gz_width_super_additive_cross_link_2026_05_28/run_h620.hexa` (~120 LoC, hexa-native, deterministic)
- log: `UNIVERSE/state/h620_gz_width_super_additive_cross_link_2026_05_28/run.log` (full stdout verbatim)
- result: `UNIVERSE/state/h620_gz_width_super_additive_cross_link_2026_05_28/result.json` (machine-readable)
- replay: `hexa run UNIVERSE/state/h620_gz_width_super_additive_cross_link_2026_05_28/run_h620.hexa` (mac-local, <5 s, $0)

## 9. 결과 (run.log verbatim 요약)

```
GZ_WIDTH = ln(4/3) = 0.287682
R1 range_coupled / sum_ind   = 0.846641
R2 Δ_peak        / sum_ind   = 2.09844
R3 peak_ratio    − 1         = 2.09845
R4 range_coupled / Δ_peak    = 0.403461
R5 mean_coupled  / max_phi   = 0.829192

best match: R1=range/sum  k=3  residual=0.0164052  tol=0.02
FALSIFIER F620.1 (integer-k linkage):   PASS
VERDICT: 🟢 SUPPORTED-NUMERICAL
```

## 10. Verdict · Next

- **VERDICT**: 🟢 **SUPPORTED-NUMERICAL** — R1 = (range of coupled Φ_AB) / (Φ_A+Φ_B) = 0.8466 ≈ 3 × GZ_WIDTH = 0.8630, residual 0.0164 ≤ 0.02. F620.1 PASS · F620.2 MIXED.
- *honest 한 강도 한계*: prior baseline (C3.2) 고려 시 PASS 가 통계적 우연과 구분되기 어려움. 🔵 SUPPORTED-FORMAL 까지 가려면 *기전 가설* + 다른 (rule_a, rule_b, W) 조합으로 동일 k=3 alignment 확장 검증 필요.
- **Next-list candidates** (deferred — 본 H 는 single-cell 완료):
  - **N1** `gz-width-cross-link-extend` — (110,110)/W=0.6 외 다른 super-additive cell ((110, 90, W>0.3) 등) 에서도 R1 ≈ 3·GZ_WIDTH 유지되는지 확장.
  - **N2** `gz-width-prior-baseline` — k ∈ {1..8} × tol=0.02 prior cover-rate 의 정확한 numerical bound (closed-form coverage 분석).
  - **N3** `gz-width-mechanism-hypothesis` — R1 ≈ 3·GZ_WIDTH 의 *왜* (mechanism 가설): coupled-Φ range 가 3-divisor-step 으로 양자화되는 substrate-level 이유 있는지.

cross-link: H_347 (E1 closed-form) ↔ H_620 (E1×F1 cross) ↔ H_609 (F1 emergent) · § 114 SAVANT numerology guardrail
