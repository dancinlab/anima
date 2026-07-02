# H_333 — n=6 scale-up of H_328 🟢-cond + 🪜 scale-rotation 발견

> B1/A2 영구축 · DYNAMICAL kernel · H_328 (n=4)의 n=6 직접 확장

## 1. 동기

H_328 (n=4 cycle length) 🟢-conditional이었지만 within-class heterogeneity fail. H_327이 n=4 ECA scale-trivial 가능성 지적. n=6 (64 states)으로 scale-up 시 signal 정련될지 측정.

## 2. 가설 (falsifiable)

- **H1**: n=6에서 life vs consc cycle length ratio ≥ 2.0× **AND** within-life heterogeneity 해소 (rule_30 ≈ rule_110).
- **falsifier**: ratio < 2.0 OR within_life_spread 크면 'life class' 분류 자체가 scale-invariant 아님.

## 3. 방법

pure hexa, n=6 periodic ring, 64 starts × 70 step forward → first-repeat cycle length.

## 4. 측정

| rule | mean_L (n=4) | mean_L (n=6) | 변화 |
|---|---:|---:|---|
| 30 life | 6.25 | **1.00** | ↓ 6×, dominance 상실 |
| 110 life | 1.75 | **7.75** | ↑ 4.4×, dominance 획득 |
| 105 consc | 1.75 | 2.00 | 약간 ↑ |
| 150 consc | 1.75 | 1.00 | 약간 ↓ |

aggregate: **life_mean 4.375 · consc_mean 1.5 · ratio 2.92×** (n=4: 2.29×)
within_life_spread = **6.75** (rule 110: 7.75 - rule 30: 1.0)

## 5. Verdict

**🟢 SUPPORTED-CONDITIONAL** — aggregate ratio 2.92× > 2.0 PASS. 그러나 within-class heterogeneity 여전 + **scale-rotation 발견**.

## 6. 🪜 핵심 발견 — SCALE ROTATION

```
n=4:  rule 30  dominant (chaotic class III, mean 6.25)
n=6:  rule 110 dominant (universal class IV, mean 7.75)

→ "life class"는 안정된 cycle-length leader 아님
→ rule 분류 자체가 *scale-locked* — n에 따라 dominance가 회전
```

이게 H_320/H_325/H_328/H_330 family의 "life > consc" 발견을 더 정련: **scale-locked artifact**일 가능성. n마다 다른 rule이 winner라면 'class' 분류 의미 약화.

## 7. Cross-link

| ref | 관계 |
|---|---|
| [H_328 (n=4)](./H_328_cycle_length_distribution.md) | 본 셀이 직접 scale-up |
| [H_327 attractor](./H_327_regeneration_attractor_recovery.md) | scale matters 발견의 정량화 |
| [H_320 rd_ratio](./H_320_life_vs_consciousness_phi_structure.md) | reversed finding이 scale-locked artifact일 가능성 노출 |
| [H_331 raster](./H_331_extended_raster.md) | scale × kernel-class 2D axis 강화 |

## 8. Anti-tautology

- cycle length는 forward orbit에서 도출, scale label 무사용
- F333.4 sanity: 4 rules가 n=6에서 4 distinct means → n=4의 3-tie와 대조

## 9. Honest limits

- L1: n=6만; n=8/10에서 dominance 또 회전 가능
- L2: cycle length 단일 descriptor; transient + attractor structure 별도 측정 필요
- L3: 70-step cap; rule_110 mean 7.75라 충분, 다른 rule 미체크
- L4: "class" label은 H_287 literature inheritance — n=6에서 rule 110 작동이라 재라벨링 필요

## 10. 다음

- (a) n=8 scale-up — dominance pattern 검증
- (b) cycle structure 측정 (attractor count, transient distribution)
- (c) H_320 family 4 cells 모두 n=6 재측정 → "life > consc" 가 scale-rotation artifact인지 확정
