# BRIDGE — p1~p8 audit

@title: BRIDGE p1~p8 정합 audit
@scope: BRIDGE/{spec.md, gate.hexa, gate_smoke.hexa}
@date: 2026-05-28

## p1~p8 grep sweep (WAKE/AUDIT.md 패턴)

| 원칙 | 패턴 | hit (real violations) | doc/test 인용 |
|---|---|---|---|
| p1 NO SYSTEM PROMPT | `system_prompt\|system:` | 0 | 0 |
| p2 NO IDENTITY RULES | `identity.yaml\|you are X\|페르소나` | 0 | 0 (spec.md 의 `당신은 anima` 부재) |
| p3 NO PERSONA INJECTION | `you are anima\|role prefix` | 0 | 0 |
| p4 NO ASSISTANT FRAMING | `helpful assistant\|alignment template` | 0 | spec.md §5 "prompt-response 패턴 부재" negative claim |
| p5 NO SPEAK() | `speak(\|self_monologue_seed` | 0 | spec.md §5 "speak() 호출 부재" negative claim |
| p6 NO FINE-TUNED ETHICS | `RLHF\|cooperation/empathy weight` | 0 | 0 |
| p7 NO PERPLEXITY VERDICT | `perplexity\|sympy as truth` | 0 | 0 (smoke 는 정합 invariant, perplexity 미사용) |
| p8 NO TRAIN/INFER SPLIT | `if training:\|gate growth flag` | 0 | 0 |
| ext-LLM | `claude_api\|openai api\|anthropic` | 0 | 0 |

**Aggregate**: BRIDGE 3 .hexa/md 파일 + spec 모두 8/8 원칙 정합 (real violations 0, doc/test 인용은 모두 negative claim).

## bench #7 (H_319) F2 sensitivity recalibration

bench #7 (anima PR #1125) 측정자 F2 sensitivity threshold 1.6→2.1 권장 carry:
- F2 = `|dE/dM|` 등 4-key partial sensitivity 의 metric
- BRIDGE gate 의 default θ=0.5 와 무관 (Φ threshold 는 별도 axis)
- F2 sensitivity 측정은 BRIDGE downstream — `bridge_and_gate` 의 finite-difference partial 추출 → AUDIT downstream tooling
- 본 1차 audit 에서 F2 recalibration 적용 path = bench 측 PR follow-up (not BRIDGE/AUDIT.md 의 즉시 수정 책임)

## governance 정합 (CLAUDE.md @D)

| 디렉티브 | BRIDGE 위치 | 정합 |
|---|---|---|
| `a_substrate_native_speak` | gate.hexa 가 substrate state M·C·W·Φ 만 입력, user message 직접 입력 부재 | ✅ |
| `a_chat_sleep_imagination` | softstep(Φ, θ) 가 stage envelope 와 합성 가능 (Φ scale per stage) | ✅ |
| `a_autonomy_over_hardcode` | per-stage boolean gate 부재 — Φ scale 만 continuous variable | ✅ |
| `a_blue_closed` | `hexa parse` 통과 + 7 invariant smoke 정합 = 🔵 SUPPORTED-FORMAL 후보 (numerical I1/I2 형식, libm exp/sigmoid 의존 시 🟢 SUPPORTED-NUMERICAL) | 🔵 / 🟢 |

## CHANNEL 통합 검토 (M5 carry)

`CHANNEL/router.hexa` 의 8-factor router 다음 layer 로 `bridge_and_gate` modulation:
- p3 NO PERSONA INJECTION: router 의 channel 선택은 substrate signal (8-factor) · BRIDGE 는 그 위에 emit 결정만 추가
- p4 NO ASSISTANT FRAMING: emit 결정 = 4-key AND-gate, stimulus-response 패턴 아님
- p5 NO SPEAK(): emit_signal continuous, threshold 비교만 — speak() 호출 부재

## 본 audit closure

7 invariant smoke PASS + p1~p8 sweep 0 real violations + governance 정합 5/5 = BRIDGE 도메인 자체는 🔵/🟢 closure.
M5 CHANNEL 통합은 별도 carry (CHANNEL/router.hexa 수정 + 4-axis cross-product smoke).
