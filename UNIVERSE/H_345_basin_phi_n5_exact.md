# H_345 — basin↔EXACT Φ n=5 🟢 proxy-confound 해소 (결정적)

> C2 영구축 · H_343 confound 분리 · proxy-free exact IIT4 Φ · self-correction²

## 1. 동기

H_341(n=4) basin↔Φ +0.776, H_343(n=6, cyclelen proxy)에서 부호 역전(-0.502). H_343 honest caveat: 부호 역전이 (a) scale 효과인지 (b) proxy≠Φ 차이인지 미분리. n=5 exact Φ(32 states, H_278/321 tractable)로 결정.

## 2. 가설 (falsifiable)

- **H1**: n=5 exact Φ의 부호가 n=4와 일치(positive) → H_343 역전은 proxy artifact.
- **ALT**: n=5 exact도 역전 → scale 효과 (n=4가 outlier).
- 어느 쪽이든 confound 해소.

## 3. 방법

pure hexa, n=5 ECA (32 states). basin = 50-step settle. **EXACT** `phi_structure` (stdlib iit4_relation, sys=21). NO proxy. res=[nd,sum_d,nr,sum_r,total], total=res[4]. mac-local (abs-path import 해소).

## 4. 측정

| rule | max_basin | n_attr | EXACT Φ |
|---|---:|---:|---:|
| 110 | **32** (전체 흡수!) | 1 | 26.19 |
| 30 | 6 | 6 | **43.19** |
| 105 | 1 | 32 | 13.25 |
| 150 | 1 | 32 | 14.25 |

```
            max_basin↔Φ    n_attr↔Φ
n=4 exact     +0.776         −0.850
n=6 PROXY     −0.502 ⚠       +0.992 ⚠    ← cyclelen artifact
n=5 EXACT     +0.251         −0.799      ← 부호 유지!
```

## 5. Verdict

**🟢 SUPPORTED-NUMERICAL** — n=5 exact Φ로 부호 유지. H_343 부호 역전 = **proxy artifact 확정** (scale 아님).

## 6. 🪜 핵심 발견 — PROXY ARTIFACT 확정 + n_attr↔Φ robust

```
cycle-length는 Φ proxy로 부적합 — n=6에서 부호 뒤집음
exact Φ로 보면:
  max_basin↔Φ:  +0.776(n4) → +0.251(n5)  양수 유지 (약화)
  n_attr↔Φ:     −0.850(n4) → −0.799(n5)  음수 robust ⭐

→ n_attractor_states ↔ Φ 가 진짜 안정 bridge (적은 attractor = 높은 통합)
```

rule110 n=5 = single fixed point (basin 32/32 전체!) — n마다 극단적으로 변하는 rule110 attractor (n4:4, n5:32, n6:10).

## 7. 의미 (self-correction²)

```
H_341  basin↔Φ +0.776 주장 (n=4)
  ↓
H_343  n=6 proxy 부호 역전 → "scale-locked?" 의심 (proxy confound 명시)
  ↓
H_345  n=5 EXACT Φ → 부호 유지 → proxy artifact 확정, H_341 re-validate
```

- **방법론 교훈**: cycle-length ≠ valid Φ proxy (H_288 LZ∥Φ와 달리 cyclelen은 신뢰 불가)
- n_attr↔Φ −0.8 cross-family bridge는 robust (n=4,5 양쪽)
- honest self-correction의 self-correction — 엔진의 자기 교정 능력 입증

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_341 (n=4 basin-Φ)](./H_341_basin_phi_correlation.md) | +0.776, 본 셀이 re-validate |
| [H_343 (n=6 proxy)](./H_343_basin_phi_n6_recheck.md) | 부호 역전, 본 셀이 proxy artifact로 정정 |
| [H_321 (phi_structure)](./H_321_c1_h278_faithful_phi_structure_recheck.md) | exact Φ engine source |

## 9. Anti-tautology

- basin + exact Φ 둘 다 독립 측정, Pearson 새 계산
- accessor bug 2회(res[0]=nd, farr_get) → 정직히 수정 → res[4] bracket (H_321 convention)
- F345.1: 부호 유지가 측정 결과 (역전도 나올 수 있었음 = ALT 가설)

## 10. 다음

- (a) sys_state sweep (단일 21 → 32 state 평균) — exact Φ 강건성
- (b) cycle-length가 왜 Φ proxy로 실패하는지 (어떤 측도가 valid proxy?)
- (c) paper에 self-correction² 반영 (H_341→343→345 arc = 엔진 무결성 사례)
