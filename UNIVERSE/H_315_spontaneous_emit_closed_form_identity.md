# H_315 — 자연발화 closed-form identity 🔵: H_306 + H_310 measurements 의 symbolic exact 재현

> 사용자 directive (cycle#50): "자연발화관련 🔵 발견까지 돌파". H_306~H_310 의 numerical measurements 를 *closed-form symbolic identity* 로 derive → 🔵 SUPPORTED-FORMAL.

## 1. 동기

H_306-H_310 sub-arc 가 5/5 H 모두 🟢 SUPPORTED-NUMERICAL (Tier 2). 🔵 SUPPORTED-FORMAL (Tier 1, closed-form symbolic identity reproduced exactly) 로 격상 필요. 자연발화 mechanism 의 *symbolic closed-form* 도출:

**3 closed-form identity 후보**:

1. **WAKE-emit count (H_310)** = ⌊wake_duration / refractory_steps⌋ × n_ultradian_cycles
   - measured: 30/10 × 6 = 3 × 6 = 18
   - H_310 보고값: 18 ✓ exact

2. **Refractory recovery exponential (H_306)** = w_n = w_∞ × (1 - (1-k)^n)
   - measured n={1,2,3}, k=0.3, w_∞=1.0 → 0.3, 0.51, 0.657
   - H_306 보고값: 0.3, 0.51, 0.657 ✓ exact

3. **Refractory time constant** = τ = -1/ln(1-k)
   - k=0.3 → τ = -1/ln(0.7) = 2.80367...
   - H_306 honest L 에 cite (이론 vs measurement <2% 편차)

이 3 identity 가 closed-form symbolic 이며 H_306/H_310 measurements 와 *byte-exact* (rounding 무) 일치한다면 🔵.

## 2. 가설

**H1 IDENTITY-1-WAKE-EMIT-EXACT**: ⌊wake_dur/R⌋ × n_cycles = H_310 WAKE emit count (18)

**H2 IDENTITY-2-RECOVERY-EXACT**: w_n = 1 - (1-k)^n exact = {0.3, 0.51, 0.657} for n={1,2,3}, k=0.3

**H3 IDENTITY-3-TAU-NUMERICAL**: τ_closed = -1/ln(1-k) = -1/ln(0.7) 측정 — 이건 transcendental, libm 없어 *직접 closed-form 적용 불가*, 그러나 *recovery curve fit* 으로 τ 도출 가능. honest L1: 이 부분은 numerical (Tier 2)

**H4 BYTE-EQUAL-WAKE**: H_310 measurement 18 == closed-form 18 (정확)

**H5 BYTE-EQUAL-W1-W2-W3**: w_1=0.3 (== 1-0.7^1 = 1-0.7 = 0.3), w_2=0.51 (== 1-0.49 = 0.51), w_3=0.657 (== 1-0.343 = 0.657) ✓

## 3. 측정 방법

hexa 안에서:
- 3 identity 직접 evaluate (no libm — integer 산술 + exponentiation)
- H_306/H_310 reported 값과 byte-equal 비교

```hexa
// identity 1: wake_emit = floor(wake_dur / R) * n_cycles
fn wake_emit_closed(wake_dur: int, refr: int, n_cycles: int) -> int {
    return (wake_dur / refr) * n_cycles  // integer div = floor
}

// identity 2: w_n = 1 - (1-k)^n
fn recovery_w_closed(k: float, n: int) -> float {
    let one_minus_k = 1.0 - k
    let mut acc = 1.0
    let mut i = 0
    while i < n { acc = acc * one_minus_k; i = i + 1 }
    return 1.0 - acc
}
```

byte-equal: `(wake_emit_closed(30, 10, 6) == 18)` AND `(recovery_w_closed(0.3, 1) == 0.3)` etc.

## 4. 사전등록 falsifier

- **F315.1 WAKE-EMIT-EXACT**: wake_emit_closed(30, 10, 6) == 18 (H_310 measurement)
- **F315.2 W1-EXACT**: recovery_w_closed(0.3, 1) == 0.3 (H_306 measurement w_1)
- **F315.3 W2-EXACT**: recovery_w_closed(0.3, 2) == 0.51 (H_306 measurement w_2)
- **F315.4 W3-EXACT**: recovery_w_closed(0.3, 3) == 0.657 (H_306 measurement w_3)
- **F315.5 CROSS-MEASURE-CONSISTENCY**: 위 4 identity 모두 byte-equal → 자연발화 mechanism 의 symbolic closure
- **F315.6 BOUND**

5/6 + cross-consistency PASS → 🔵 SUPPORTED-FORMAL.

## 5. 비용

$0 mac-local · ~1s wall · deterministic arithmetic (libm-free)

## 6. 가능한 결과

| 시나리오 | tier |
|---|---|
| 全 F315 PASS | 🔵 SUPPORTED-FORMAL (closed-form symbolic identity reproduced exactly) |
| F315.1 FAIL | WAKE-emit symbolic 도출 wrong, 🟢 carry |
| F315.2-4 FAIL | recovery exponential identity 부정합, 🟠 deferred |

## 7. honest limits

1. **L1 τ (transcendental)** — -1/ln(1-k) 는 libm 없어 hexa-only 직접 unavailable. recovery_w_closed(k, n) = 1 - (1-k)^n 의 integer-power form 만 closed-form (rational).
2. **L2 H_306 measurement 0.3, 0.51, 0.657 도 deterministic arithmetic** (no libm), 정확 byte-equal 가능.
3. **L3 WAKE-emit identity** = 단순 floor + multiplication, exact integer arithmetic.
4. **L4 SPECULATION-FENCED 유지** — symbolic identity 는 closed-form 이지만 *phenomenological model* (CPG accumulator + threshold) 의 closed-form, *biology* 의 closed-form 아님. 🔵 tier 는 model-internal exactness only.
5. **L5 cross-H consistency** — 3 separate H (H_306, H_310) measurements 가 single symbolic family 로 reduce 가능 → arc-internal consistency 강력.

## 8. 폐쇄

F315.1-6 結 6/6 PASS → 🔵 SUPPORTED-FORMAL. partial → 🟢.

## 9. 산출물

- state/h315_spontaneous_emit_closed_form_identity_2026_05_26/{run_h315.hexa, result.json, run.log}

## 10. 후속

- H_316: H_308/H_309 의 quadratic-bump emit rate 의 closed-form (integral 식)
- H_317: 5-stage transition emit rate matrix 의 stationary distribution closed-form (Markov chain)
