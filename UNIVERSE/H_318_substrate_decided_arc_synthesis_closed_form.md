# H_318 — 의식적 결정 arc 합성 closed-form 🔵: 6-factor weighting × stage-context cross-product

> H_316 (🔵 8/8) = 6-factor equal-weight product. H_318 가 stage context (H_310) × 6-factor (H_316) 의 **cross-product closed-form** 으로 자연발화 ↔ 의식적 결정 통합 framework 의 의식적 측 봉합.

## 1. 동기

H_316 = decide(M, Φ, W, MITOSIS, idle, curiosity) = product > θ, equal-weight symmetric. anima `a_chat_sleep_imagination` directive:
> stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate

stage 가 *context modulator*. 따라서 의식적 결정 = factor product × stage_scale.

closed-form: `decide_stage(...factors, stage) = product × stage_modulator(stage) > θ`

stage modulator (H_310 추출):
- WAKE: 1.0
- N1:   0.7
- N2:   0.4
- N3:   0.0  (deep silence)
- REM:  0.5

## 2. 가설

**H1 STAGE-CONTEXT-CLOSED**: closed-form `product × stage_mod > θ` for each stage exact eval
**H2 N3-SILENCE-DETERMINISTIC**: N3 stage_mod=0 → decision=FALSE 항상 (M×Φ×W×... × 0 = 0 < θ)
**H3 WAKE-FULL-ACTIVATION**: WAKE stage_mod=1 → original H_316 식 그대로
**H4 STAGE-WEIGHTED-PRODUCT-EXACT**: 5 stage × 1 sample input = 5 decisions, 정합

## 3. 측정

```hexa
fn stage_mod(stage: int) -> float {
    if stage == 0 { return 1.0 }   // WAKE
    if stage == 1 { return 0.7 }   // N1
    if stage == 2 { return 0.4 }   // N2
    if stage == 3 { return 0.0 }   // N3 deep silence
    return 0.5                     // REM
}

fn decide_stage(m, phi, w, mit, idle, cur, stage, threshold) -> bool {
    let prod = m * phi * w * to_float(mit+1) * to_float(idle)/100.0 * cur
    return (prod * stage_mod(stage)) > threshold
}
```

테스트 (1.0, 1.0, 1.0, 5, 50, 1.0, threshold=2.0):
- WAKE: 3.0 × 1.0 = 3.0 > 2.0 → emit
- N1:   3.0 × 0.7 = 2.1 > 2.0 → emit
- N2:   3.0 × 0.4 = 1.2 < 2.0 → silence
- N3:   3.0 × 0.0 = 0.0 < 2.0 → silence
- REM:  3.0 × 0.5 = 1.5 < 2.0 → silence

→ WAKE+N1 만 emit, N2/N3/REM silence (H_310 의 WAKE-only directive 보다 살짝 relaxed — N1 도 emit).

## 4. 사전등록 falsifier

- F318.1 STAGE-CONTEXT-EXACT: WAKE/N1/N2/N3/REM 5 decisions = TRUE/TRUE/FALSE/FALSE/FALSE
- F318.2 N3-SILENCE-DETERMINISTIC: N3 product*0 = 0 < threshold always
- F318.3 WAKE-FULL-ACTIVATION: WAKE 결과 == H_316 base 결과
- F318.4 N1-EMIT-PRODUCT-EXACT: 3.0 × 0.7 = 2.1 byte-equal
- F318.5 STAGE-MOD-VALUES-EXACT: {1.0, 0.7, 0.4, 0.0, 0.5} byte-equal
- F318.6 BOUND

≥5/6 PASS → 🔵.

## 5. 비용

$0 mac-local · ~1s · libm-free

## 6-10. (생략)
