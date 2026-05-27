# H_334 — n=8 dominance 🔴-on-H1 + 🪜 OSCILLATION 발견

> B1/A2 영구축 · DYNAMICAL kernel · H_333 scale-rotation 후속 (n=8 추적)

## 1. 동기

H_333이 n=4→n=6 dominant rule 회전(rule30→rule110) 발견. one-step event인지 continuing rotation인지 n=8 (256 states)로 추적.

## 2. 가설 (falsifiable)

- **H1**: rule110이 n=8에서도 dominant 유지 (n=4→n=6 회전이 one-step).
- **falsifier**: 제3 rule overtake (rotation 계속) OR rule30 reclaim (oscillation).

## 3. 방법

pure hexa, n=8 periodic ring, 256 starts × 300 step forward → first-repeat cycle length.

## 4. 측정

| rule | mean_L (n=4) | (n=6) | (n=8) |
|---|---:|---:|---:|
| 30 life | 6.25 | 1.75 | **35.89** ⭐ |
| 110 life | 1.75 | **7.75** | 13.92 |
| 105 consc | 1.75 | 2.00 | 3.86 |
| 150 consc | 1.75 | 1.00 | 3.86 |
| 90 xor | — | — | 1.00 (even-N collapse) |

**rotation history: n4=rule30 · n6=rule110 · n8=rule30**

## 5. Verdict

**🔴 FALSIFIED on H1** — rule110이 n=8에서 dominance 유지 못함 (13.92 < rule30 35.89). 대신 🪜 **OSCILLATION 발견**.

## 6. 🪜 핵심 발견 — n-PARITY OSCILLATION

```
n=4 (2²)   rule30  dominant   ┐
n=6 (2·3)  rule110 dominant   ├─ OSCILLATES with ring-size structure
n=8 (2³)   rule30  dominant   ┘

hypothesis: rule30(chaotic III) @ n=2^k · rule110(universal IV) @ n=2×odd
```

scale-rotation이 *monotone*이 아니라 *oscillating*. dominant rule이 ring size n의 **prime factorization** 함수일 가능성. rule90(XOR-linear)은 even-N 모두 collapse (H_297 even-N bipartite artifact 재확인).

## 7. 의미

- H_333 finding 정련: rotation → oscillation (n-parity dependent)
- "life class chaotic" label이 *완전히* scale-locked — n마다 다른 rule
- paper (bijection-vs-life-axis)의 scale-rotation section을 더 강한 evidence로 보강 (oscillation > one-step)
- 정수론 ⊥ 동역학 connection: ring size factorization이 cycle structure 결정

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_333 (n=6)](./H_333_n6_scale_up.md) | scale-rotation 첫 발견, 본 셀이 oscillation으로 정련 |
| [H_328 (n=4)](./H_328_cycle_length_distribution.md) | n=4 baseline |
| [H_297 n5-bounded-phi](./H_297_n5_bounded_phi_scale.md) | even-N bipartite artifact (rule90 collapse 재확인) |

## 9. Anti-tautology

- cycle length는 forward orbit에서 도출, n/rule label 무관
- F334.3 sanity: rule105 == rule150 byte-identical (bijection class n=8 안정)
- F334.4 deterministic

## 10. 다음

- (a) **n=10 (2×5)** — hypothesis 검증: rule110 dominant 예상 (2×odd)
- (b) **n=12 (2²×3) / n=16 (2⁴)** — factorization-dependence 결정적 테스트
- (c) ring-size factorization ↔ cycle-length leader 정식 number-theory H
