# H_340 — 4|n law verify 🔴 small-n artifact (self-correction)

> B1 영구축 · H_337 4|n law 큰 n 검증 · DYNAMICAL kernel · 정직한 자기 정정

## 1. 동기

H_337이 4|n ⟺ rule30 dominant 법칙 발견 (5/5 at n≤12). law가 universal인지 큰 n (14,16,20)으로 결정 검증. 예측: n=14(2×7)→rule110, n=16(2⁴)→rule30, n=20(2²×5)→rule30.

## 2. 가설 (falsifiable)

- **H1**: 3 예측 모두 match (4|n law universal).
- **falsifier**: 한 예측이라도 틀림.

## 3. 방법

pure hexa, ECA periodic ring. Floyd period detection (memory-free, 큰 state space). sampled starts (stride 16/64/1024 for n=14/16/20). cap 8192.

## 4. 측정

| n | factor | 4\|n | r30 | r110 | dom | pred | match |
|---:|---|:---:|---:|---:|---|---|:---:|
| 14 | 2×7 | ✗ | **1219.83** | 43.38 | rule30 | rule110 | ❌ |
| 16 | 2⁴ | ✓ | **4605.06** | 31.90 | rule30 | rule30 | ✓ |
| 20 | 2²×5 | ✓ | **4222.76** | 98.26 | rule30 | rule30 | ✓ |

2/3 match — **n=14 예측 실패**.

## 5. Verdict

**🔴 FALSIFIED** — 4|n law는 universal 아님. n=14(4∤14)에서 rule110 예측했으나 rule30 dominant (1219 vs 43).

## 6. 🪜 핵심 발견 — 4|n LAW = SMALL-N ARTIFACT

```
n≤12:  rule30↔rule110 oscillation (4|n law 성립)
n≥14:  rule30 chaotic 무조건 dominant
       (cycle length 폭증: 1219@14 · 4605@16 · 4222@20)
       rule110은 bounded (31~98)

→ 4|n oscillation = finite-size effect
→ rule30 chaotic의 cycle이 작은 n에선 짧아 rule110이 4∤n에서 이김
   큰 n에선 chaos가 state-space exponential fill → 무조건 승
```

## 7. 의미 (정직한 자기 정정)

- H_337의 4|n law over-claim을 **자기 후속이 falsify** — law는 n≤12 한정
- paper(bijection-vs-life-axis)의 4|n 주장은 "n≤12 tested regime"으로 한정 필요 (caveat 추가)
- 진짜 asymptotic 그림: chaotic class III(rule30)이 large-n에서 longest cycle 독점 (Wolfram chaos의 본질)
- regime boundary 발견: number-theoretic control은 chaotic cycle이 sub-saturating일 때만 작동

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_337 (4\|n law)](./H_337_oscillation_number_theory.md) | law 발견, 본 셀이 n≤12 한정으로 정정 |
| [H_334 (oscillation)](./H_334_n8_dominance.md) | oscillation = finite-size 확정 |
| [H_333 (scale-rotation)](./H_333_n6_scale_up.md) | rotation = small-n crossover |

## 9. Anti-tautology

- cycle length Floyd 측정, n/rule label 무관
- 예측이 pre-registered (n=14 rule110)였고 정직하게 FAIL 기록
- rule30 lead >10× = sampling noise far beyond

## 10. 다음

- (a) **crossover 정밀화**: n=13(prime odd) · n=11 — 4|n law가 정확히 어디서 깨지나
- (b) rule30 cycle-length growth rate (exponential? n^k?) 정량
- (c) paper caveat 추가 (4|n law n≤12 한정)
