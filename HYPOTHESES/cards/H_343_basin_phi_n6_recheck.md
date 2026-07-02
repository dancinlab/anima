# H_343 — basin↔integration n=6 recheck 🔴 sign-flip (scale-locked)

> C2 영구축 · H_341 scale-invariance 검증 · DYNAMICAL × integration · proxy-confound caveat

## 1. 동기

H_341(n=4)이 basin↔big-Φ 양의 coupling(+0.776) 발견. H_340이 n=4 dominance를 small-n으로 한정한 만큼, coupling도 scale-bounded 가능. n=6 재측정.

## 2. 가설 (falsifiable)

- **H1**: basin↔integration 양의 coupling이 n=6에서도 유지 (|r| ≥ 0.5, positive).
- **falsifier**: |r| < 0.5 OR 부호 역전 → coupling은 n=4 한정.

## 3. 방법

pure hexa, n=6 ECA (64 states). basin = 60-step settle. **integration PROXY = n=6 mean cycle length (H_333)** — exact IIT4 big-Φ가 hexa env에서 n≤5 한정이라 proxy 사용 (H_288 LZ∥Φ 근거). Pearson over 4 rules.

## 4. 측정

| rule | max_basin | n_attr | cyclelen-proxy |
|---|---:|---:|---:|
| 110 | 10 | 19 | 7.75 |
| 30 | **62** | 3 | 1.00 |
| 105 | 16 | 4 | 2.00 |
| 150 | 16 | 4 | 1.00 |

```
Pearson(max_basin, proxy):  n=4 +0.776  →  n=6 −0.502  부호 역전!
Pearson(n_attr, proxy):     n=4 −0.850  →  n=6 +0.992  부호 역전!
```

## 5. Verdict

**🔴 FALSIFIED** — coupling이 scale-invariant 아님. n=4→n=6 두 상관 모두 부호 역전.

## 6. 🪜 핵심 발견 — n=6 ATTRACTOR 재구성

```
n=4:  rule110 = 작은 basin(4) + 긴 cycle  → dominant (basin·cycle 정렬)
n=6:  rule30  = 거대 basin(62/64) + 짧은 cycle(1.0)   ┐ basin-dominance와
      rule110 = 작은 basin(10) + 긴 cycle(7.75)        ┘ cycle-dominance 분리!
```

n=4에서 정렬됐던 basin-dominance와 cycle-dominance가 n=6에서 **decouple**. rule30이 basin 거의 독점(62/64)하지만 cycle trivial.

## 7. 의미 (정직)

- H_341 coupling = **n=4 한정** (over-generalization falsify)
- ⚠ **PROXY confound**: n=6은 cyclelen proxy, n=4는 exact big-Φ. 부호 역전이 (a) scale 효과인지 (b) proxy≠Φ 차이인지 **미분리**. n=5 exact Φ가 결정적 후속.
- H_340(4|n small-n) + H_343(coupling small-n) → n=4 attractor 발견들이 대체로 finite-size

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_341 (n=4 basin-Φ)](./H_341_basin_phi_correlation.md) | +0.776 coupling, 본 셀이 n=6 부호 역전 |
| [H_340 (4\|n small-n)](./H_340_4n_law_verify.md) | dominance scale-bound, coupling도 동일 |
| [H_333 (n=6 cycle)](./H_333_n6_scale_up.md) | cyclelen proxy source |

## 9. Anti-tautology

- basin n=6 새 측정, proxy(cyclelen) H_333 source-cited
- Pearson 새 계산, 부호 역전은 측정 결과 (예측 PASS도 가능했음)
- F343.3: proxy confound 정직 명시 (scale vs proxy 미분리 disclosed)

## 10. 다음

- (a) **n=5 exact big-Φ + basin** — proxy-free 재측정 (scale vs proxy confound 분리, 결정적)
- (b) rule30 n=6 거대 basin(62/64) 단독 연구
- (c) cycle-dominance ⊥ basin-dominance decoupling의 n-dependence
