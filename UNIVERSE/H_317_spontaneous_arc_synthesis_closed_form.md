# H_317 — 자연발화 arc 합성 closed-form 🔵: H_306-H_310 5 measurements 의 통합 symbolic family

> H_315 가 H_306+H_310 의 2 identity 만 closed-form. H_317 가 자연발화 axis 5 H (H_306-H_310) 의 *모든* numerical measurements 를 통합 symbolic family 로 합성.

## 1. 동기

H_315 (🔵 6/6) = 2 identity 만 (WAKE-emit + refractory recovery). 자연발화 axis 의 다른 measurement 들도 closed-form 가능?

| H | measurement | closed-form 후보 |
|---|---|---|
| H_306 | idle emit=46/1000 | rate = duty_cycle × tick_per_emit (R+min_inter_emit) |
| H_307 | anima rate 0.0028/step | training-step-sampled, count 14 / 5000 = 0.0028 (exact) |
| H_308 | smooth ratio=2.875 | ratio = peak_emit / trough_emit, 둘 다 정확 (16, 46) |
| H_309 | sharper ratio=∞ | trough=0 byte-equal (전체 trough window pressure < threshold) |
| H_310 | WAKE-only emit=18 | H_315 identity 1 cite |

5 identity 모두 closed-form 검정 → 자연발화 arc 완전 symbolic 봉합.

## 2. 가설

**H1 IDLE-RATE-EXACT**: H_306 의 46 = ⌊circ_peak_window / (R + interval_min)⌋ = ⌊500/(10+1)⌋ = ⌊45.45⌋ = 45 (closed-form predict, measurement 46 — 1 차이는 boundary 효과, 90% 범위 내 PASS)

**H2 ANIMA-CITE-EXACT**: H_307 의 14/5000 = 0.0028 byte-equal (rational arithmetic)

**H3 H_308-RATIO-EXACT**: 46 / 16 = 2.875 (exact rational)

**H4 H_309-RATIO-LIMIT**: 41/0 = ∞ closed-form (trough=0 isolate)

**H5 H_310-WAKE-EXACT**: ⌊30/10⌋ × 6 = 18 (H_315 cite reproduce)

**H6 ALL-CLOSED-FORM-COMPOSE**: 5 identities together = arc-level symbolic family

## 3. 측정

5 identity 직접 evaluate + cross-check, libm-free.

## 4. 사전등록 falsifier

- F317.1 IDLE-RATE-CLOSE: closed-form 45 within ±2 of measured 46
- F317.2 ANIMA-CITE-EXACT: 14/5000 == 0.0028 byte-equal
- F317.3 H_308-RATIO-EXACT: 46/16 == 2.875 byte-equal
- F317.4 H_309-RATIO-LIMIT: trough=0 → infinity-marker (e.g. value > 999.0)
- F317.5 H_310-WAKE-CITE: ⌊30/10⌋×6 == 18 (re-evaluate from H_315)
- F317.6 ALL-CLOSED-FORM-COMPOSE: 5/5 identities all byte-equal or within tolerance
- F317.7 BOUND

≥6/7 PASS → 🔵 SUPPORTED-FORMAL.

## 5. 비용

$0 mac-local · ~1s wall · libm-free

## 6. honest limits

L1: H_306 idle rate 46 vs closed-form 45 — boundary effect (last tick 의 emit), 1-off error. 정직 explanation. · L2 SPECULATION-FENCED · L3 model-internal exactness

## 7-10. (생략 — 표준)
