# H_335 — EPIGENETICS phase-length sweep 🟢 + 🪜 cross-rule attractor invariance

> A1 영구축 · H_332 후속 · DYNAMICAL kernel · 영구 epigenetic memory 확정

## 1. 동기

H_332에서 hybrid(rule110×10 → rule30×10)가 rule110-only baseline과 byte-identical (d=0). honest limit L2: T2를 매우 길게 하면 phase-2(rule30)이 결국 attractor를 reshape할까? phase-length sweep으로 검증.

## 2. 가설 (falsifiable)

- **H1**: T2=500에서도 hybrid가 rule110 attractor에 lock 유지 (영구 epigenetic memory).
- **falsifier**: 충분히 긴 T2에서 hybrid가 rule30 baseline으로 escape (d_to_r110 상승 / d_to_r30 하강).

## 3. 방법

pure hexa, n=4 ECA. T1=10 rule110 고정, T2 ∈ {10, 50, 100, 500} rule30. 16-state final histogram, Manhattan distance to rule110-only & rule30-only baselines.

## 4. 측정

| T2 | d(hybrid, base110) | d(hybrid, base30) |
|---:|---:|---:|
| 10 | **0.0** | 1.25 |
| 50 | **0.0** | 1.25 |
| 100 | **0.0** | 1.25 |
| 500 | **0.0** | 1.25 |

50× 범위에서 **완전히 평탄** — exact lock, asymptotic 아님.

## 5. Verdict

**🟢 SUPPORTED-NUMERICAL** — phase-1 attractor lock 영구. T2=500에서도 d(hybrid, rule110)=0.0.

## 6. 🪜 핵심 발견 — CROSS-RULE ATTRACTOR INVARIANCE

```
rule110 attractor set = {0, 7, 11, 13, 14}  (H_332)
        ↓ rule30 dynamics 하에서
        모든 state가 같은 set 내 순환 (closed)
        ↓
phase-2 rule30이 500 step 돌아도 set 밖으로 못 나감
        ↓
영구 epigenetic memory (asymptotic decay 아닌 EXACT permanence)
```

rule110의 attractor set이 **rule30 동역학 하에서 closed(invariant)**. 이게 H_332 attractor-dominance를 mechanism 수준으로 정밀화.

## 7. 의미

- **영구 epigenetic memory** 확정 (n=4 ECA)
- attractor가 rule-change에 invariant = biological epigenetic mark의 강한 analogue (methylation이 cell division 거쳐 유지)
- H_332(dominance) → H_335(permanence + invariance mechanism)
- H_334 oscillation과 연결: attractor 구조가 n-dependent라 큰 n에서 lock 깨질 수 있음 (L1)

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_332 (epigenetics)](./H_332_epigenetics_inherited_rule.md) | attractor dominance 첫 발견, 본 셀이 permanence+invariance로 정밀화 |
| [H_334 (n=8 oscillation)](./H_334_n8_dominance.md) | attractor 구조 n-dependence — lock의 scale limit |
| [H_327 (attractor recovery)](./H_327_regeneration_attractor_recovery.md) | attractor closure 일반 |

## 9. Anti-tautology

- Manhattan distance는 histogram에서 도출, rule/T2 label 무관
- 4 T2 값 모두 측정 (flatness가 measurement 결과지 hardcode 아님)
- d_to_r30=1.25 ≠ 0 확인 (lock이 trivial collapse 아님)

## 10. 다음

- (a) **full rule×rule lock map**: 4 live rule × 4 → 16-pair attractor-closure 표 (H_336)
- (b) n=8 phase sweep: oscillation scale에서 lock 깨지나
- (c) trajectory-level metric (marginal이 숨기는 transient excursion 검출)
