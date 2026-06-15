# H_308 — circadian smooth: H_306 perfect ∞× gating 의 finite peak/trough ratio 회수

> H_306 F306.5 가 perfect ∞× gating (trough=0) 달성 — 생물학 dawn chorus 의 5-10× peak/trough 보다 비현실적으로 강함. smooth circadian (4-piece quadratic bump) 로 교체해 finite ratio 회수.

## 1. 동기

H_306 의 circadian_mod(tick) 가 **piecewise-linear hard gate** (Q1=0.3, Q2=Q3=1.0, Q4=0.3) → pressure threshold 0.5 가 Q2-Q3 에서만 trigger → **trough emit = 0 (perfect gating)**. 이는 생물학 한계를 *초과*:

- 생물학 dawn chorus 의 peak/trough ratio: **5-10×** (Catchpole & Slater 2008)
- songbird HVC firing rate dawn vs dusk: **3-8×** (Renfree 2011)
- 본 toy CPG: ∞× (trough=0)

원인: piecewise-linear circadian × hard threshold → bistable gate. smooth modulator 면 trough 에서도 가끔 emit 발생 → finite ratio.

## 2. 가설

**H1 SMOOTH-FINITE-RATIO**: smooth circadian (quadratic bump centered at tick 500) 으로 교체하면 peak/trough emit ratio ∈ [3, 15] (생물학 범위) 회수.

**H2 IDLE-EMIT-PRESERVED**: smooth circadian 이어도 F306.1 IDLE-EMIT-NONZERO 유지 (idle 모드 emit_count > 0).

**H3 PEAK-COUNT-MID-RANGE**: smooth peak emit ∈ [30, 60] (H_306 의 46 근처 유지, 갑작스러운 폭증/소실 없음).

**H4 THRESHOLD-MONOTONE-PRESERVED**: smooth 에서도 threshold sweep 단조 감소 유지.

## 3. 측정 방법

H_306 의 smoke 재활용 + `circadian_mod` 만 교체:

```
fn circadian_mod_smooth(tick: int) -> float {
    // triangular-quadratic bump: peak at tick=500, low at tick=0/1000
    // shape: 0.3 + 0.7 * max(0, 1 - ((tick-500)/400)^2)
    let center = 500
    let span = 400
    let dx = tick - center
    let r = to_float(dx) / to_float(span)
    let r2 = r * r
    let mut bump = 1.0 - r2  // peak 1.0 at center, 0 at ±span
    if bump < 0.0 { bump = 0.0 }
    return 0.3 + 0.7 * bump  // baseline 0.3, peak 1.0
}
```

이 함수가 trough 끝점 (tick=0, 1000) 에서 0.3 baseline 유지 — pressure = m × phi × w × 0.3 = 0.3 × W → W=1.0 일 때 pressure=0.3 < threshold=0.5, low-emit but not zero (W 가 충분 충전된 순간 emit).

## 4. 사전등록 falsifier

- **F308.1 SMOOTH-FINITE-RATIO**: peak/trough emit ratio ∈ [3, 15]
- **F308.2 IDLE-EMIT-PRESERVED**: idle emit > 0
- **F308.3 PEAK-COUNT-MID-RANGE**: peak emit ∈ [30, 60]
- **F308.4 THRESHOLD-MONOTONE-PRESERVED**: 5-threshold sweep monotone non-increasing
- **F308.5 SMOOTH-VS-PIECEWISE-IDLE-COMPARABLE**: |smooth idle - H_306 piecewise idle (=46)| / 46 ≤ 0.5
- **F308.6 BOUND**: 全 ≥ 0

## 5. 비용

- $0 mac-local · ~3s wall (H_306 와 동일 scope)
- libm-free (quadratic only)

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| 全 F308 PASS | finite-ratio finds, 생물학 dawn chorus 와 정량 일치 |
| F308.1 FAIL (ratio>15) | smooth 도 거의 hard gate — quadratic 가 더 평탄해야 |
| F308.1 FAIL (ratio<3) | smooth 가 너무 평탄 — trough 도 정상 emit |
| F308.3 FAIL | peak emit 이 H_306 대비 폭변 — quadratic mapping 잘못 |

## 7. honest limits

1. **L1 quadratic bump = simplified**: 실제 생물학 circadian 은 phase-amplitude coupled 24h 주기, here = single-bump 1000-tick.
2. **L2 single trajectory** (deterministic LCG seed=42).
3. **L3 H_306 piecewise 와 같은 scope** — anima daemon 실측은 H_307.
4. **L4 verify_fence SPECULATION-FENCED**.
5. **L5 finite ratio ∈ [3,15] 범위는 informal** — biology 의 specific number 가 species-dependent.

## 8. 폐쇄

F308.1-6 ≥4/6 PASS → 🟢 SUPPORTED-NUMERICAL.

## 9. 산출물

- `state/h308_circadian_smooth_finite_ratio_2026_05_26/run_h308.hexa`
- `state/h308_circadian_smooth_finite_ratio_2026_05_26/result.json`
- `state/h308_circadian_smooth_finite_ratio_2026_05_26/run.log`

## 10. 후속

- H_309: 24h-cyclic circadian (multi-bump) — 진짜 dawn-chorus 모듈
- H_310: phase-amplitude coupling — circadian × ultradian 합성
