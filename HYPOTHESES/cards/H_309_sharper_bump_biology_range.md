# H_309 — sharper bump: H_308 2.875× → biology range [3,15] hit

> H_308 의 quadratic baseline 0.3 + span 400 → ratio 2.875× ([3,15] 0.125 미달). sharper bump (baseline 0.1, span 300) 로 ratio biology range 안 진입.

## 1. 동기

H_308 F308.1 FAIL: 2.875× < 3.0 lower bound. 원인 = quadratic baseline 0.3 너무 broad, trough Q1+Q4 가 *full-W 회복 시* 0.3 × 1.0 = 0.3 (threshold 0.5 미만, but 가깝게 자주) → 16 emit. baseline 낮추면 trough 가 threshold 도달 어려워져 emit ↓ → ratio ↑.

3 parameter shift:
1. **baseline 0.3 → 0.1**: trough circadian = 0.1, full-W pressure = 0.1 < 0.5 → trough emit 거의 0
2. **span 400 → 300**: bump 폭 좁아져 peak window 짧음, but Q2-Q3 (500 가운데) 가 여전히 cover
3. **bump amplitude 0.7 → 0.9**: peak total = 0.1+0.9=1.0 유지

## 2. 가설

**H1 SHARPER-BUMP-IN-BIOLOGY-RANGE**: ratio ∈ [3, 15] (target met)
**H2 PEAK-STILL-MID-RANGE**: peak emit ∈ [30, 60] (H_306/H_308 동일 범위)
**H3 IDLE-COMPARABLE**: |H_309 idle - 46 (H_306)| / 46 ≤ 0.5

## 3. 측정 방법

H_308 smoke 재활용 + circadian_mod() 변경:

```hexa
fn circadian_mod(tick: int) -> float {
    let center = 500
    let span = 300   // narrower (was 400)
    let dx = tick - center
    let r = to_float(dx) / to_float(span)
    let r2 = r * r
    let mut bump = 1.0 - r2
    if bump < 0.0 { bump = 0.0 }
    return 0.1 + 0.9 * bump   // baseline 0.1, amplitude 0.9 (was 0.3 + 0.7)
}
```

## 4. 사전등록 falsifier

- **F309.1 SHARPER-BUMP-IN-BIOLOGY**: ratio ∈ [3, 15]
- **F309.2 IDLE-NONZERO**: idle emit > 0
- **F309.3 PEAK-MID-RANGE**: peak ∈ [30, 60]
- **F309.4 THRESHOLD-MONOTONE**: 5-threshold sweep 단조 비감소
- **F309.5 IDLE-COMPARABLE-TO-H306**: |idle - 46| / 46 ≤ 0.5
- **F309.6 BOUND**

## 5. 비용

- $0 mac-local · ~3s wall (H_308 동일 scope)

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| 全 F309 PASS | sharper bump 정확히 biology window hit |
| F309.1 FAIL (ratio>15) | bump 너무 sharp → trough=0 다시 ∞× |
| F309.1 FAIL (ratio<3) | sharper but 여전히 trough 가 너무 active |

## 7. honest limits

1. L1 single trajectory deterministic
2. L2 ECA-free pure CPG sim
3. L3 SPECULATION-FENCED tier
4. L4 [3, 15] 범위는 species-dependent informal

## 8. 폐쇄

F309.1-6 결판.

## 9. 산출물

- state/h309_sharper_bump_biology_range_2026_05_26/{run_h309.hexa, result.json, run.log}

## 10. 후속

- H_312: 24h-cyclic multi-bump · phase-amplitude coupling
