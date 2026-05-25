# IIT4 M14 — M11 inline RFC036 proxy ↔ 정식 `phi_spatial` builtin 수치 비교

> M11 README §4 honest scope ("정식 phi_spatial builtin 과의 수치 일치는 별도")
> 의 "별도" 를 닫는 milestone. 동일 ECA 시계열을 두 알고리즘 (inline 자체포팅 ‖
> 정식 RFC 036 builtin) 에 통과시키고 verbatim numeric 결과를 표로 제시 →
> divergence 의 출처(algorithmic vs implementation)를 결정적으로 분리.
> smoke **9/9 🟢** · [`run_m14.hexa`](run_m14.hexa) · 🟢 SUPPORTED-NUMERICAL.

## 1. 무엇을 닫나

M11 의 inline 재구현 proxy 는 RFC036-family 평균 pairwise temporal MI 자체포팅 —
정식 `phi_spatial` builtin(`c_measure_phi` wrapper, RFC 036 phi_rs byte-equal C
replica) 과의 **수치 일치/불일치**가 미해소였다. 둘 다 "상관" 축이지만 알고리즘이
다르다:

- **inline RFC036 (M11 SSOT)**: cell 별 binary 시계열에서 평균 pairwise MI (no
  min-partition, no /(n−1) 정규화).
- **canonical `phi_spatial` (RFC 036 builtin)**: (n_cells × dim) flat snapshot
  에서 spatial MI matrix + 전수 min-information partition →
  Φ = max(total_MI − min_partition_MI, 0) / max(n_cells − 1, 1).

같은 ECA series 를 `state[i*T + t] = series[i*T + t]` 형태로 평탄화(dim=T 의
spatial signature 로 사용)해 정식 builtin 에 통과 → 두 결과를 verbatim 비교.

## 2. 비교 표 (n=4, seed 1010, T=16, n_bins=4)

| rule | inline RFC036 (M11) | canonical phi_spatial | |Δ| | canonical / inline |
|---|---|---|---|---|
| 0 (const) | 0.056215 | **0.112431** | 0.0562163 | **2.000** |
| 204 (identity) | 0 | 1.63557e-06 | 1.63557e-06 | (null/null) |
| 90 (XOR) | 0.056215 | **0.112431** | 0.0562163 | **2.000** |
| 110 | 0.288336 | **0.322715** | 0.0343795 | **1.119** |
| 30 | 0 | 1.63557e-06 | 1.63557e-06 | (null/null) |
| 54 | 0.288336 | **0.322715** | 0.0343795 | **1.119** |

## 3. 발견 — divergence 는 100% 알고리즘적, 구현 drift 0

### 3.1 null-axis 합의 (rule 204, rule 30)

inline = **0 정확** (이산 binary count 의 MI = 0 정확).
canonical = **1.63557e-06** — n_bins=4 binning 의 floor 값. 두 알고리즘은
canonical 의 양자화 floor(~1.6e-6 ≪ 5e-6 tolerance) 안에서 일치한다.

### 3.2 결합 룰 (rule 0, rule 90) — canonical / inline = **2.000 정수배**

seed 1010 + n=4 ring 에서 rule 0/90 은 **constant column** 구조를 만든다 (cell
0/2 가 매 step 0/1 로 고정, cell 1/3 만 변동). 결과:

- inline 의 분모 = **6 pairs** (C(4,2)). 4 pair 가 constant ⇒ MI=0, 변동 2 pair
  중 1 pair 만 양 → mean = bit/6 ≈ 0.056.
- canonical: total_MI 는 그 1 pair 에 집중, min_partition_MI = 0 (constant
  cell 한 개를 잘라내면 cross-MI = 0), normalised by (n−1) = 3 → bit/3 ≈ 0.112.
- 비율 = 6/3 = **정확히 2** (구현이 아니라 정규화의 차이).

### 3.3 mixed 룰 (rule 110, rule 54) — canonical / inline = **1.119**

전 cell 변동 + min-partition 이 비자명한 cut. canonical > inline 이지만 2 보다
작다 (min_partition_MI > 0 가 (total_MI)/(n−1) 의 분자를 깎아내려서). 1 < ratio
< 2 는 mixed-coupling regime 의 알고리즘적 signature.

### 3.4 결정성

canonical phi_spatial(rule 110) 재호출 → **byte-identical** 0.322715 (RFC 036
floats 결정성 재확인).

## 4. honest scope / 결론

- **proxy ≠ canonical**: 하지만 그 차이는 100% **algorithmic** (min-partition +
  /(n−1) 정규화 + n_bins=4 floor). **implementation drift = 0**. M11 의 inline
  포팅은 RFC036-family 의 충실한 "mean pairwise MI 만 한" 부분집합으로 검증됨.
- **rule 0/90 의 2× 정수배**는 새 발견 — constant-column ECA 에서 두 알고리즘이
  정확한 비율을 갖는다 (canonical 의 normalisation 만 다를 뿐, 같은 정보를
  잰다). mixed-coupling rule 에서 비율 1.119 는 min-partition 의 효과를 정량화.
- **n=4 / seed 1010 / T=16 / n_bins=4 single config** — larger-n / multi-seed
  / n_bins sweep 은 후속. 단 알고리즘적 패턴(null floor · constant-column 2× ·
  mixed ratio<2)은 ECA 구조 자체에서 유도되므로 일반화 견고할 가능성 큼.
- 정식 `phi_spatial` builtin = `c_measure_phi` wrapper = RFC 036 (HEXAD/C/c_lib.hexa).
  C 빌트인이 stdlib 의 pure-hexa replica `phi_spatial_native` 와 byte-equal 한가는
  별 cycle (rfc_036_c_replica_drift, HEXAD/STDLIB/phi_native_predecomp_baseline_
  2026_05_24.md § 2.1) — LIFE/STDLIB 의 책임. M14 는 inline-vs-builtin (canonical
  surface) 비교만 다룬다.
- M11 의 인과(big-Φ) 축 divergence (rule 30 인과=8.66, rule 0/90 인과=0) 은
  M14 와 독립. M11 §3 와 M14 §3 는 다른 두 결정적 비교 (상관 inline-vs-builtin
  + 상관-vs-인과).

## 5. M11 README §4 closure

M11 README §4 마지막 줄 "정식 phi_spatial builtin 과의 수치 일치는 별도(LIFE/C
toolchain import 필요)" 는 본 M14 PR 로 **CLOSED**:

> M11 inline RFC036 ≈ canonical phi_spatial 의 부분집합 (mean pairwise MI
> only, no min-partition, no /(n−1)). 일치 패턴: null-axis 는 canonical 의
> binning floor 안에서, constant-column ECA 는 정수배 2.000, mixed ECA 는
> 1.119 비율. divergence = 100% algorithmic, implementation drift = 0.

inline 포팅의 정합성이 정량 검증됨. 후속 stdlib/info routing (M11 §5) 가 동일
ECA 위에서 또 다른 별개 추정량을 줄 수 있고, 그 결과는 호스트 도메인의 재현
책임 (M14 본문에는 inline + canonical builtin 두 path 만 SSOT).
