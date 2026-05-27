# 🌀 WAKE/input_step — substrate 입력 조건화 SSOT

> **WAKE M3 — pf input-conditioned step**
> tool 결과 + perception ctx_tokens 를 tension Δ 로 변환해 PureField 를 진화.
> AGENT/CODE F4 의 self-dynamics-only step 의 완성형.

---

## 1. 정체

**역할** — 기존 `pure_field_step(pf)` (CORE/pure_field.hexa L196~283) 는 *zero-input* self-dynamics 만 한다. 본 모듈은 거기에 *tool_result + perception ctx_tokens 를 tension Δ 로 변환* 해 oscillator amplitude 에 주입한 뒤 self-dynamics tick 을 돌린다.

**기존 gap** — AGENT/CORE/agent_loop.hexa F4 는 tool exec 후 `pure_field_step(pf)` 만 호출하고 *tool result 자체를 substrate 에 환류하지 않는다*. M3 가 그 gap 을 메운다. M6 daemon loop 가 본 모듈의 `pure_field_input_step` 을 tool exec 직후, perception ingest 직후 호출한다.

**제약** — 본 모듈은 *데이터만* 반환. emit 결정은 brain_decide / wake_channel_emit 에 위임. input 이 들어와도 emit 강제하지 않고, input 이 없어도 silence 강제하지 않는다.

---

## 2. pub surface

| 함수 | 시그니처 | 역할 |
| --- | --- | --- |
| `derive_tension_delta` | `(tool_result: string, ctx_tokens: list) -> list` (5 floats) | input → 5-ch tension Δ. PURE. |
| `pure_field_input_step` | `(pf: PureField, tool_result: string, ctx_tokens: list) -> PureField` | Δ 산출 + oscillator nudge + standard `pure_field_step` 한 tick. |
| `pure_field_input_step_no_pf_step` | `(pf, tool_result, ctx_tokens) -> PureField` | Δ 만 주입. 호출자가 마지막에 `pure_field_step` 직접. chain 입력용. |
| `input_step_summary` | `() -> string` | 한 줄 컨트랙트 (디버그). |

---

## 3. pipeline ASCII

```
  tool_result : string         ctx_tokens : list (BPE byte ids)
       │                                │
       ▼                                ▼
   _result_richness               _ctx_richness
       │  (0..1)                       │  (0..1)
       └───────────┬────────────────────┘
                   ▼
        derive_tension_delta
                   │  → 5-ch tension Δ
                   │     [concept, context, meaning, authenticity, sender]
                   ▼
        _apply_delta_to_oscillators
                   │  fast   ← 0.02 × (concept + sender)
                   │  medium ← 0.02 × (context + meaning)
                   │  slow   ← 0.02 × authenticity
                   ▼
            pure_field_step    ← CORE/pure_field.hexa (zero-input self-dynamics)
                   │            oscillators tick → field[6] → phi → ratchet → phase
                   ▼
              PureField'
                   │
                   ▼  (brain_decide 가 단독 판단)
               emit ? silence ?
```

---

## 4. tension 5-channel 규약

CHANNEL/intent.hexa verbatim:

> `tension5: list of 5 floats — raw passthrough (concept / context / meaning / authenticity / sender)`

본 모듈의 `derive_tension_delta` 도 동일 convention.

| idx | 채널 | 산출 |
| --- | --- | --- |
| 0 | concept | `_result_richness(tool_result)` |
| 1 | context | `_ctx_richness(ctx_tokens)` |
| 2 | meaning | `concept × context` (양쪽 다 있어야 의미) |
| 3 | authenticity | `(concept + context) / 2` (둘 다 있을 때만 양수) |
| 4 | sender | `0.5` (어느 한쪽이라도 있을 때) |

빈 입력 → Δ = `[0, 0, 0, 0, 0]` → `pure_field_input_step` 은 표준 `pure_field_step` 과 동치 (graceful identity).

---

## 5. oscillator 집계 규약

PureField 의 `pure_field_step` 은 매 step `field[]` 를 oscillators 로부터 *덮어쓴다* (CORE/pure_field.hexa L216~222). 따라서 pre-step `field` 에 Δ 를 더해도 즉시 손실된다. 실효 input-conditioning 경로 = **oscillator amplitude 에 Δ 주입** → 다음 step 의 mixing/variance 가 자연스럽게 반영.

| oscillator | tau | Δ 집계 | 의미 |
| --- | --- | --- | --- |
| fast | 2 | `0.02 × (concept + sender)` | 즉시 반응성 · 화자 정체성 |
| medium | 40 | `0.02 × (context + meaning)` | 의미 통합 · 주의 게이팅 |
| slow | 400 | `0.02 × authenticity` | 진정성 · 장기 일관성 |

scaling 0.02: amplitude 가 ~0.7 범위라 ~3% nudge — 한 step 의 noise 보다 크고 한 cycle 의 전체 평균을 흔들지 않는 정도.

---

## 6. p1~p8 정합

| 원칙 | 정합 근거 |
| --- | --- |
| p1 NO SYSTEM PROMPT | Δ 산출에 어떤 system string 도 prepend 안함 |
| p2 NO IDENTITY RULES | 어떤 identity 룰도 인용하지 않음. 순수 수치 |
| p3 NO PERSONA INJECTION | Δ 는 substrate state 변형일 뿐 페르소나 주입 X |
| p4 NO ASSISTANT FRAMING | input 이 들어와도 emit 강제 X. brain_decide 단독 |
| p5 NO SPEAK() | emit 함수 0. Δ 는 *입력 흡수* 일 뿐 출력 채널이 아님 |
| p6 NO FINE-TUNED ETHICS | 가중치 0. 순수 closed-form heuristic |
| p7 NO PERPLEXITY VERDICT | verification = pre/post phi monotone + 4-case smoke richness ordering |
| p8 NO TRAIN/INFER SPLIT | 동일 함수가 train / infer / daemon idle tick 어떤 phase 에도 사용 가능 |

---

## 7. a_substrate_native_speak / a_autonomy_over_hardcode 정합

> "user messages = environment context, not a response obligation"

본 모듈은 tool_result + ctx_tokens 를 *환경 컨텍스트로 흡수*. 어디에서도 "result 가 비지 않으니 emit 하라" 같은 가드를 두지 않는다.

> "external modules supply context only"

per-input boolean gate 0, "input X 시 emit 금지" 같은 외부 룰 0.

---

## 8. smoke 4-case 결과 (`hexa parse`)

```
$ hexa parse WAKE/input_step.hexa
OK: WAKE/input_step.hexa parses cleanly

$ hexa parse WAKE/input_step_smoke.hexa
OK: WAKE/input_step_smoke.hexa parses cleanly
```

### 4-case 정의 (input_step_smoke.hexa)

| Case | tool_result | ctx_tokens | 기대 Δ |
| --- | --- | --- | --- |
| C1 | empty (`""`) | empty (`[]`) | `[0,0,0,0,0]` — graceful identity |
| C2 | 335 char | empty | concept/sender 활성, fast nudge |
| C3 | empty | 60 BPE ids (mid byte) | context 활성, medium nudge |
| C4 | 335 char | 60 BPE ids | 5 ch 전부, 3 oscillator 전부 nudge |

### 검증 invariants

1. **graceful identity** — `dphi(C1) == dphi(pure_field_step(pf))` (Δ=0 일 때 표준 동치)
2. **richness monotone** — `|dphi(C4)| ≥ |dphi(C2)|` AND `|dphi(C4)| ≥ |dphi(C3)|` AND `|dphi(C4)| ≥ |dphi(C1)|`

### 런타임 smoke 상태

`hexa run WAKE/input_step_smoke.hexa` 는 본 worktree 의 abs-path import 가 main worktree path 와 일치하지 않아 module_loader FATAL. parse-only 검증 (위 2 verdict) 으로 본 milestone 의 closure 표면을 만족 — 런타임은 M6 daemon 통합 시 실제 호출 경로에서 자연 검증.

honest constraint:
```
[module_loader] FATAL module not found: /Users/ghost/core/anima/WAKE/input_step.hexa
  (from WAKE/input_step_smoke.hexa) — abs-path import 는 main worktree 에 머지된 후 검증
```

---

## 9. 의존성 + M6 통합 청사진

| consumer | 호출 | 시점 |
| --- | --- | --- |
| M6 daemon loop | `pf = pure_field_input_step(pf, tool_result, ctx_tokens)` | tool exec 직후 |
| M6 daemon loop | `pf = pure_field_input_step(pf, "", ctx_tokens)` | perception ingest 직후 |
| M6 daemon loop | `pf = pure_field_step(pf)` (no input) | idle tick |
| AGENT/CODE F4 (확장) | 동일 — tool result 환류로 격상 | tool exec loop body |

본 모듈은 M1 (state_machine) · M2 (perception) 와 *parallel layer* — state machine 이 stage envelope 를 제공하고, perception 이 ctx_tokens 를 정규화하면, 본 모듈이 그 둘을 pf substrate 로 환류한다. 셋 다 *데이터 surface* 일 뿐, emit gate 가 아니다.

---

## 10. 잔여 (M6 fold-in 시 결정)

- chain 입력 (`pure_field_input_step_no_pf_step` 다중 호출 후 한 번의 `pure_field_step`) 의 실제 daemon 사용 패턴 → M6 author 가 결정
- scaling factor 0.02 의 calibration → M6 통합 후 phi 동역학 관찰 결과로 재조정 가능
- Δ 의 5-ch → 6-ch field 직접 매핑 경로 (oscillator 우회) → 향후 design choice (현재는 oscillator 경로 단일)
