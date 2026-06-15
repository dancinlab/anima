# H_342 — 4|n law crossover 정밀화 🔴 crossover는 n=11 밑 (2차 자기 정정)

> B1 영구축 · H_340 후속 · 4|n law crossover 정밀 측정 · DYNAMICAL kernel · 정직한 자기 정정 2차

## 1. 동기

H_337이 4|n ⟺ rule30 dominant 법칙 발견 (5/5 at n∈{4,6,8,10,12}). H_340이 이를 n≤12 small-n artifact로 정정 (n≥14에서 rule30 무조건 dominant, 1219@14). 그렇다면 crossover는 **정확히 어디?** H_340의 다음-항목 (a)를 실행: n∈{11,12,13,14} 측정. n=11,13은 **홀수 ring** (even-N bipartite 구조 없음 — 새 parity class), n=12는 4-div, n=14는 2×7 (H_340에서 rule30 1219 확인).

## 2. 가설 (falsifiable)

- **H1**: rule110이 이 범위 어딘가(n∈{11,12,13,14})에서 아직 LEAD하고, n=14로 갈수록 lead가 줄어 rule30이 이김. **rule110이 마지막으로 이기는 가장 큰 n** = crossover.
- **falsifier**:
  - rule110이 {11,12,13,14} 어디서도 안 이기면 (n=11부터 이미 rule30 dominant) → crossover는 **n=11 밑**.
  - rule110이 n=14에서도 이기면 → **H_340이 틀림**.

## 3. 방법

pure hexa, ECA periodic ring. Floyd period detection (memory-free). **FULL enumeration n≤13** (2^11=2048, 2^12=4096, 2^13=8192 starts, stride 1) · n=14는 stride 8 (2048 samples). cap 16384. cycle length는 실제 Floyd orbit에서 측정 — n/rule label 무관, 결과가 crossover를 어디든 배치 가능 (anti-tautology).

## 4. 측정

| n | factor | ring | 4\|n | r30 | r110 | dom | lead(r30/r110) |
|---:|---|:---:|:---:|---:|---:|---|---:|
| 11 | 11 (prime) | 홀수 | ✗ | **120.74** | 83.24 | rule30 | 1.45× |
| 12 | 2²×3 | 짝수 | ✓ | **95.42** | 10.28 | rule30 | 9.28× |
| 13 | 13 (prime) | 홀수 | ✗ | **436.55** | 348.69 | rule30 | 1.25× |
| 14 | 2×7 | 짝수 | ✗ | **1211.04** | 41.70 | rule30 | 29.04× |

**rule30이 4개 n 전부 dominant** — rule110은 어디서도 안 이김.

## 5. Verdict

**🔴 FALSIFIED (H1)** — rule110은 {11,12,13,14} 어디서도 안 이김. n=11에서 이미 rule30 dominant (120.7 vs 83.2). 따라서 crossover는 **n=11 밑** (n=10~11 사이). H1 예측 (rule110 still leads, lead shrinks toward 14)은 falsified.

부수 확인: rule110이 n=14에서도 안 이김 (1211 vs 41.7, 29×) → **H_340 재확인**. stride-8 r30=1211 ≈ H_340 stride-16 r30=1219 → cross-validated.

## 6. 🪜 핵심 발견 — CROSSOVER는 n=10~11 사이 (4|n law 유효 window = n≤10)

```
n≤10:  rule110이 4∤n(n=6,10)에서 이김 (H_337) — 4|n law 성립
n=11~14: rule30 무조건 dominant (이번 셀 측정)
       r30: 120.7@11 · 95.4@12 · 436.5@13 · 1211@14
       r110: 83.2@11 · 10.3@12 · 348.7@13 · 41.7@14

→ crossover = n=10 과 n=11 사이 (NOT n=12~14)
→ n=11(4∤11)에서 이미 rule30이 이김 → H_337 law는 n=11에서 이미 깨짐
→ 4|n law의 실측 유효 window = n≤10 (NOT n≤12)

홀수 ring(11,13)은 rule110을 가장 가깝게 유지 (lead 1.45×·1.25×)
짝수 ring(12,14)은 rule30 lead 폭증 (9.3×·29×) — 짝수일수록 chaos 우세
```

H_340은 "4|n law = n≤12 artifact"라 했으나, 이번 측정은 그것조차 over-claim임을 보임: **n=11에서 이미 깨짐** → 진짜 window는 n≤10.

## 7. 의미 (정직한 자기 정정 2차)

- H_340의 "crossover는 n=12~14 사이" 암시를 **이번 셀이 n=10~11 사이로 정정** — H_337 law의 실측 유효 window는 n≤12가 아니라 **n≤10**
- n=11 (4∤11, 홀수 prime)에서 rule30이 이미 이김 → number-theoretic control(4|n)이 n=11에서 이미 작동 안 함
- 홀수 ring(11,13)에서 lead가 최소(1.25~1.45×) — rule110의 universal 구조가 홀수에서 rule30에 가장 근접하지만 **여전히 패배**
- paper(bijection-vs-life-axis)의 4|n 주장 caveat을 "n≤12 tested" → **"n≤10 tested"**로 추가 정정 필요
- 진짜 asymptotic 그림 재확인: chaotic class III(rule30)이 n≥11에서 longest cycle 독점, gap은 n 증가에 따라 폭증

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_340 (4\|n large-n)](./H_340_4n_law_verify.md) | n≤12 artifact 발견, 본 셀이 crossover를 n=10~11로 정밀화 |
| [H_337 (4\|n law)](./H_337_oscillation_number_theory.md) | law 발견, 본 셀이 실측 window를 n≤10으로 정정 |
| [H_334 (oscillation)](./H_334_n8_dominance.md) | oscillation = finite-size 확정 |

## 9. Anti-tautology

- cycle length는 실제 Floyd orbit에서 측정, n/rule label 무관
- H1이 pre-registered (rule110 leads somewhere in {11..14}, shrinking)였고 정직하게 FAIL 기록
- FULL enumeration n≤13 (sampling noise 0) · n=14 stride-8가 H_340 stride-16 재현 (1211 vs 1219)
- 결과가 crossover를 n≤11·11~14·>14 어디든 배치 가능했음 — 실측이 "n≤11 밑"으로 결정

## 10. 다음

- (a) **하한 pin**: n=9,10 측정 — rule110이 마지막으로 이기는 정확한 n (H_337은 n=10 rule110-lead 주장, 재측정으로 bracket 닫기)
- (b) rule30 cycle-length growth rate 정량 (120→436→1211: exponential? n^k?)
- (c) paper caveat "n≤10 tested regime"으로 추가 정정
- (d) 홀수 ring에서 rule110이 가장 근접한 이유 — 홀수 ring의 bipartite-free 구조가 rule110 universal 패턴 유지에 유리한지
