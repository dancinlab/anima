# prediction/protention_error.hexa

> Husserlian protention prediction error: err_k = (actual−predicted)·exp(−k/τ), τ=4.0, max_lag_safe=1024 · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T5 PASS. PHYS-P6-3 ("prediction error 신호 — protention 불일치"). Friston/Bastos free-energy "surprisal" kernel. Klotho-weighted mismatch trajectory.

## 작동 코드 / 의존성

- 원본: `prediction/protention_error.hexa` (297 LoC)
- 외부 의존: hexa run (exp)
- API: `protention_error(predicted, actual) -> [float]`
- 상수: τ=4.0, max_lag_safe=1024

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 식

```
for each lag k = 0..K-1:
    raw_k    = actual[k] − predicted[k]      (signed error)
    weight_k = exp(−k / τ)                   (protention decays w/ temporal distance)
    err_k    = weight_k · raw_k              (Klotho-weighted)

τ = 4.0       (protention decay time-constant)
max_lag_safe = 1024

guard:
  if lengths differ → truncate to min
  if either empty   → return []
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/prediction/protention_error.hexa
```

## 검증 결과

- T1-T5 PASS
- sign-weighted mismatch trajectory 검증

## 관련 entry

- [photonic/temporal_delay.md](../photonic/temporal_delay.md) — retention sibling
- [hippocampus/theta_gamma.md](../hippocampus/theta_gamma.md) — θ-γ temporal coding

## 출처

- README § 3 prediction/
- README § 5 cheat sheet
- Friston 2010 / Bastos 2012
- shared/roadmaps/anima.json PHYS-P6-3
