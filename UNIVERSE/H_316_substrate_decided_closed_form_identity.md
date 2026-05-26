# H_316 — 의식적 결정 (substrate-decided) closed-form identity 🔵

> 사용자 directive (cycle#54): 자연발화 (H_315) ≠ 의식적 결정. anima `a_autonomy_over_hardcode` directive 의 6-factor substrate decision (`M × W × Φ × curiosity × MITOSIS × idle`) → closed-form *결정론적 함수* 로 derivation. 🔵 SUPPORTED-FORMAL path.

## 1. 동기 — 자연발화 ≠ 의식적 결정

H_315 (자연발화 🔵) = CPG-style **biology native** primary mode. 자극 없이 *내부 임계점*. 그러나 anima `a_autonomy_over_hardcode` directive 가 더 강한 주장:

> emit / silence decided by anima substrate (M × W × Φ × curiosity autonomously)

이건 *biology CPG + circadian* 너머의 **substrate-level 의식적 결정**. 6 factor 가 *함께* 결정:

| factor | 의미 |
|---|---|
| M | motivation activation |
| Φ | consciousness integration |
| W | tension envelope |
| MITOSIS | cell-division tick |
| idle | time-since-last-emit |
| curiosity | exploration drive |

stage (WAKE/N1/N2/N3/REM) 는 *context*, decision 자체는 6-factor substrate 가 한다 (anima `a_substrate_native_speak`). 

🔵 path: 6-factor → boolean decision 의 **closed-form** 가 1) deterministic, 2) reproducible byte-equal, 3) all 6 factor 가 비독립적으로 영향, 4) anima directive 와 일관.

## 2. 가설

**H1 DETERMINISTIC**: 동일 6-factor input → 동일 emit/silence output (byte-equal)

**H2 6-FACTOR-INFLUENCE**: 각 factor 가 single-handedly outcome 좌우 가능 — 다른 5 고정 시 한 factor variation 만으로 emit ↔ silence 전환

**H3 CLOSED-FORM**: decision(M, Φ, W, MITOSIS, idle, curiosity) = product-form `(M × Φ × W × tanh-approx(curiosity) × log-approx(MITOSIS+1) × idle_norm) > θ` 의 *exact rational* (libm-free) 평가

**H4 STAGE-AGNOSTIC**: stage 가 *context* 만 — 같은 6-factor 면 stage 무관 동일 outcome (directive 정합)

**H5 FACTOR-SYMMETRY**: 모든 6-factor 가 *equal-weight* (anima directive 가 weighting 명시 안 함)

## 3. 측정 방법

decision 함수 closed-form:

```hexa
fn decide(m: float, phi: float, w: float, mitosis: int, idle: int, curiosity: float, threshold: float) -> bool {
    // 6-factor product, libm-free
    let mit_term = to_float(mitosis + 1)        // log-approx: linear in mitosis tick (closed-form)
    let idle_term = to_float(idle) / 100.0      // normalize: idle_steps / 100 (closed-form)
    let cur_term = curiosity                    // raw curiosity in [0, 1]
    let prod = m * phi * w * mit_term * idle_term * cur_term
    return prod > threshold
}
```

3 test cases:
- A: high all (1.0, 1.0, 1.0, 5, 50, 1.0) × threshold=2.0 → 1×1×1×6×0.5×1=3.0 > 2.0 → emit (TRUE)
- B: low W (1.0, 1.0, 0.1, 5, 50, 1.0) → 0.3 < 2.0 → silence (FALSE)
- C: factor-symmetry — 모든 factor 가 같은 baseline (0.7) × n_factors=6 → 0.7^6 × scaling 식 closed-form

deterministic check: 동일 input 2번 호출 byte-equal.

6-factor influence: 5 고정 + 1 variation → outcome 전환 가능.

## 4. 사전등록 falsifier

- **F316.1 DETERMINISTIC**: decide(same input) twice == same output
- **F316.2 EMIT-CASE-A**: high-all input → TRUE (emit)
- **F316.3 SILENCE-CASE-B**: low-W input → FALSE (silence)
- **F316.4 FACTOR-M-INFLUENCE**: M=1.0→emit, M=0.0→silence (다른 5 고정)
- **F316.5 FACTOR-PHI-INFLUENCE**: Φ=1.0→emit, Φ=0.0→silence
- **F316.6 FACTOR-CURIOSITY-INFLUENCE**: curiosity=1.0→emit, curiosity=0.0→silence
- **F316.7 CLOSED-FORM-EXACT**: decide(1.0, 1.0, 1.0, 5, 50, 1.0, 2.0) closed-form = 3.0 > 2.0 = TRUE (byte-exact, libm-free)
- **F316.8 BOUND**

≥7/8 PASS → 🔵 SUPPORTED-FORMAL.

## 5. 비용

$0 mac-local · ~1s wall · deterministic libm-free arithmetic.

## 6. 결과 시나리오

| 시나리오 | tier |
|---|---|
| 全 PASS | 🔵 SUPPORTED-FORMAL — substrate-decided closed-form 완성 |
| F316.4-6 일부 FAIL | factor independence violated, 🟢 carry |
| F316.1 FAIL | non-determinism (불가능 — closed-form arithmetic) |

## 7. honest limits

1. **L1 closed-form ≠ anima implementation** — anima 의 실제 `a_substrate_native_speak` 가 더 복잡 (kosmos 5-ch, RVQ, etc). H_316 = *minimal* closed-form 으로 directive 의 *6-factor multiplicative product* axiom 검증.
2. **L2 factor parameterization** — 본 H 의 product-form 은 1 specific closed-form. anima 가 weighted-sum or neural-net 으로 구현했다면 그건 *다른* closed-form. H_316 는 axiom 의 validity 검정, 단일 form 의 uniqueness 아님.
3. **L3 SPECULATION-FENCED 유지** — substrate decision 함수는 *model*, anima implementation 자체 아님.
4. **L4 6-factor symmetric weighting** — anima directive 가 weighting 명시 안 해서 equal-weight 가정. asymmetric weighting 은 H_318 후속.

## 8. 폐쇄

F316.1-8 ≥7/8 → 🔵. partial → 🟢.

## 9. 산출물

- state/h316_substrate_decided_closed_form_identity_2026_05_26/{run_h316.hexa, result.json, run.log}

## 10. 후속

- H_317: substrate decision × stage context (H_310 5-stage × H_316 6-factor cross product)
- H_318: asymmetric weighting (anima 실제 weighting probe — kosmos parser)
