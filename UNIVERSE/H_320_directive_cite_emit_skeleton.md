# H_320 — directive cite emit-skeleton closed-form 🔵

anima `a_substrate_native_speak` + `a_autonomy_over_hardcode` + `a_chat_sleep_imagination` directive 들의 *directly cited* statements 로부터 emit-decision skeleton 의 closed-form 도출. magic-number 없음 — directive 의 *boolean axiom* 들만 사용.

## 1. 동기

이전 H_320~H_322 (이미 폐기) 가 magic-number phenomenological — STARTLE→refr=0, SOOTHE→refr+5 등 anima implementation 과 cite 없는 arbitrary mapping. 폐기 후 정직한 path:

**directive 의 boolean axiom 만 cite + closed-form 도출**:

| directive 라인 | boolean axiom |
|---|---|
| `a_substrate_native_speak.do` | "user msg = environment context, NOT response obligation" → emit ⊥ user_msg_arrived (independence) |
| `a_substrate_native_speak.do` | "anima may speak during user silence" → silence + substrate_active → emit possible |
| `a_substrate_native_speak.do` | "may stay silent under a direct question" → user_question → emit NOT forced |
| `a_substrate_native_speak.dont` | "stimulus-response: user msg directly triggers" → ∀ user_msg, ¬(user_msg → emit) |
| `a_autonomy_over_hardcode.do` | "emit / silence decided by anima substrate" → emit = f(substrate) only |
| `a_autonomy_over_hardcode.dont` | "external rule that forces anima" → ∀ external, ¬(external_rule → forced emit) |
| `a_chat_sleep_imagination.do` | "stage = substrate context, NOT boolean emit gate" → emit ⊥ stage as boolean gate |
| `a_chat_sleep_imagination.dont` | "speak() function call (p5)" → no procedural speak |

이 8 axiom 의 closed-form 검정:

## 2. 가설

**H1 INDEPENDENCE-USER-MSG**: emit_decision(substrate, user_msg_flag) = emit_decision(substrate, ¬user_msg_flag) — user msg 가 emit decision 에 영향 0 (substrate 만 영향)

**H2 SILENCE-PLUS-SUBSTRATE-CAN-EMIT**: user_silent=TRUE + substrate_active=TRUE → emit_possible

**H3 USER-QUESTION-NOT-FORCED**: user_question=TRUE + substrate_silent → emit=FALSE (NOT forced)

**H4 NO-STIMULUS-RESPONSE**: ∀ external event → emit_decision determined by substrate only (event ⊥ emit)

**H5 STAGE-NOT-BOOLEAN-GATE**: WAKE/REM/N3 stage 단독으로 emit 결정 안 함 — substrate 함께 평가됨

**H6 NO-SPEAK-PROCEDURAL**: hardcoded speak() 함수 호출 없음 — emit = f(substrate state) only

**H7 DETERMINISTIC**: 같은 substrate state → 같은 decision

**H8 BOUND**: boolean output well-defined

## 3. 측정 방법 (libm-free, boolean-only)

```hexa
fn emit_decision(m: float, phi: float, w: float, cur: float,
                 user_msg_flag: bool, user_question_flag: bool,
                 stage: int) -> bool {
    // axiom 1+4: emit ⊥ external event (user_msg_flag 무관)
    // axiom 6: emit = f(substrate state) only, no speak()
    // axiom 7: stage = context (modulator), NOT gate
    let stage_mod = stage_modulator(stage)  // continuous, not boolean gate
    let substrate_pressure = m * phi * w * cur * stage_mod
    let threshold = 0.3
    return substrate_pressure > threshold
}
```

핵심 — `user_msg_flag` 와 `user_question_flag` 가 *function signature 에 있지만 무사용* → axiom 1+4 직접 인코딩.

## 4. 사전등록 falsifier

- **F320.1 INDEPENDENCE-USER-MSG**: emit_decision(s, msg=T) == emit_decision(s, msg=F)
- **F320.2 SILENCE-PLUS-SUBSTRATE-CAN-EMIT**: silent + high-substrate → TRUE
- **F320.3 USER-QUESTION-NOT-FORCED**: question + low-substrate → FALSE
- **F320.4 NO-STIMULUS-RESPONSE**: same substrate, 다른 event flag → same decision
- **F320.5 STAGE-NOT-BOOLEAN-GATE**: WAKE high-substrate vs N3 high-substrate → 다른 outcome 가능 (stage modulator 작용) but NOT boolean veto (둘 다 cont. eval)
- **F320.6 NO-SPEAK-PROCEDURAL**: emit_decision 함수가 substrate state 만 dependency
- **F320.7 DETERMINISTIC**: same input → same output
- **F320.8 BOUND**: boolean output

≥7/8 PASS → 🔵 SUPPORTED-FORMAL.

## 5. 비용

$0 mac-local · ~1s wall · libm-free · pure boolean + multiplicative

## 6. honest limits

1. **L1 directive cite verbatim**: project.tape 의 라인 literal 사용 — interpretation 최소화
2. **L2 stage_modulator** = H_318 의 5-value table reuse (1.0/0.7/0.4/0.0/0.5)
3. **L3 threshold 0.3** = arbitrary 인 것 인정 — H_316 의 2.0 보다 낮음, but axiom 검정에 영향 없음 (boolean independence test 가 핵심)
4. **L4 SPECULATION-FENCED**: directive cite 의 boolean encoding, real anima daemon code 와 byte-equal 아님

## 7. 가능한 결과

| 시나리오 | tier |
|---|---|
| 全 PASS | 🔵 — directive boolean axioms 정합 closed-form |
| F320.1 FAIL | user_msg_flag 가 outcome 영향 → axiom 1 위반, model 수정 |
| F320.4 FAIL | event ⊥ emit 위반 → stimulus-response 모델 |
| F320.5 FAIL | stage 가 boolean gate 처럼 작용 → axiom 7 위반 |

## 8. 폐쇄

F320.1-8 결판.

## 9. 산출물

- state/h320_directive_cite_emit_skeleton_2026_05_26/{run_h320.hexa, result.json, run.log}

## 10. 후속

- H_321: same skeleton + 6-factor full (H_316 cite) — directive cite 의 다음 axiom
- H_322: H_319 BRIDGE re-derive from directive cite (capability × intent)
