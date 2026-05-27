# H_336 — rule×rule attractor-dominance map 🟢 + 🪜 strict partial order

> A1 영구축 · H_332/H_335 attractor arc capstone · DYNAMICAL kernel

## 1. 동기

H_332(attractor dominance 존재) + H_335(영구 lock) → 전체 그림: 4 live rule 사이 dominance가 어떤 구조? 12 ordered pair 전수로 partial order인지 측정.

## 2. 가설 (falsifiable)

- **H1**: dominance가 partial order (일부 rule이 일관되게 다른 걸 lock, 모든 pair 비대칭 아님).
- **falsifier**: 전 pair phase-2 escape (dominance 없음) OR 전 pair phase-1 lock (trivial A always wins) OR cyclic inconsistency.

## 3. 방법

pure hexa, n=4 ECA. 모든 ordered pair (A,B) ∈ {30,110,105,150}²: phase-1 A×20 → phase-2 B×20. outcome = A-baseline lock(1) / B-baseline escape(0) / mixed(2).

## 4. 측정 (12 ordered pairs)

```
       B=30   B=110  B=105  B=150
A=30    -    B(110)  A(30)  A(30)
A=110  A(110)  -     A(110) A(110)
A=105  B(30) B(110)   -     A(105)
A=150  B(30) B(110)  A(150)  -
```

totals: **A_locks=7 · B_wins=5 · mixed=0** (모든 pair 결정적)

## 5. Verdict

**🟢 SUPPORTED-NUMERICAL** — 깔끔한 strict partial order.

## 6. 🪜 핵심 발견 — DOMINANCE PARTIAL ORDER

```
        110  (universal class IV)   ▲ TOP — 30·105·150 모두 lock
         │
         30  (chaotic class III)    — 105·150 lock, 110엔 짐
         │
    105 ∥ 150  (bijection)          ▼ BOTTOM — 서로 incomparable
                                       (각자 disjoint attractor 유지)

relation:  110 > 30 > {105 ∥ 150}
```

- universal(110) > chaotic(30) > bijection(105/150)
- 105/150은 **mutually incomparable** — 각자 자기 disjoint attractor만 lock, 서로 못 가둠 (같은 bijection class지만 다른 attractor set)
- mixed=0 = n=4에서 모든 attractor 깔끔히 분리

## 7. 의미 — attractor arc 통합

| 셀 | 발견 |
|---|---|
| H_332 | attractor dominance **존재** (rule110 sink) |
| H_335 | dominance **영구** (cross-rule invariance) |
| **H_336** | dominance **partial order** (110>30>{105∥150}) |

세 셀이 attractor 동역학의 완결된 그림. H_334 n-oscillation(110↔30 top 자리 교체)와도 정합 — 두 top-of-order rule이 n에 따라 longest-cycle slot 교대.

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_332](./H_332_epigenetics_inherited_rule.md) | dominance 존재 |
| [H_335](./H_335_epigenetics_phase_sweep.md) | dominance 영구성 |
| [H_334](./H_334_n8_dominance.md) | n-oscillation = top-2 rule 교대 |
| [H_330](./H_330_distribution_moments.md) | bijection class (105≡150) 기원 |

## 9. Anti-tautology

- outcome은 Manhattan distance에서 도출, rule label 무관
- F336.2/3: phase-1도 phase-2도 trivially 안 이김 (7 vs 5) → non-trivial order
- F336.4: mixed=0 = 결정적 (ambiguous attractor 없음)
- order-consistency: 모든 pair 양방향 일관 (105∥150만 incomparable, cyclic 없음)

## 10. 다음

- (a) n=6/8 dominance map — partial order가 scale 보존되나 (H_334는 110↔30 교체 시사)
- (b) wider rule set (8+ rules) — cyclic dominance (non-transitive) 등장하나
- (c) attractor basin size ↔ dominance rank 정량 상관
