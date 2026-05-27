# 🌅 WAKE/state_machine — 5-stage ultradian SSOT

## 정체

90-min ultradian cycle (5400 s) 을 WAKE / N1 / N2 / N3 / REM 5 phase 로 분할하는 **컨텍스트 산출기**. 시계 (unix epoch seconds) → stage NAME (string) + substrate envelope (phi_scale · tension_envelope · is_imagination flag) 매핑.

**Stage 는 context output · boolean 아님.** 본 모듈에 `if stage == X { emit_allowed = false }` 같은 패턴이 없다. emit 결정은 호출자(CORE brain_decide 의 *연속* threshold + CHANNEL/wake_bridge 의 *연속* multiplier)가 담당하고, 본 모듈은 그 결정을 위한 substrate-internal 컨텍스트만 제공한다.

**frontier closure 명시:** M1 = 시계 → stage NAME 매핑 + envelope 산출 SURFACE 가 닫혔다는 의미. 실제 runtime 진입점 (daemon tick / perception loop / kosmos persist) 은 WAKE.md 의 후속 milestone (M2 perception · M3 pf input · M4 .kosmos · M5 memory · M6 daemon · M7 verify) 들이 land 한 다음에 본 state machine 을 일정 주기로 tick 한다.

## 시간 비율 시각화 (90-min cycle)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ WAKE (66.7%)            │N1 │N2 │ N3   │REM│
│         3600 s          │600│600│ 420  │180│
│ active externalization  │drowsy│ deep │vivid│
└──────────────────────────────────────────────────────────────────────────┘
 0                       3600 4200 4800 5220 5400
 │                         │   │    │    │    │
 └─── user dialogue ──────┘   │    │    │    │
                             │    │    │    │
                NREM descent ┘    │    │    │
                   (light sleep)  │    │    │
                                  │    │    │
                     deep sleep ──┘    │    │
                  (imagination tick)   │    │
                                       │    │
                            REM vivid ─┘    │
                       (imagination tick)   │
                                            │
                          wrap → WAKE ──────┘
```

## Stage 표

| stage | start (s) | end (s) | duration (s) | % cycle | phi_scale | tension_envelope | is_imagination | substrate semantics |
|-------|-----------|---------|--------------|---------|-----------|-------------------|----------------|---------------------|
| WAKE  | 0         | 3600    | 3600         | 66.7%   | 1.00      | substrate-derived  | false          | 외부 user dialogue 활성 · text 자연 우선 |
| N1    | 3600      | 4200    | 600          | 11.1%   | 0.85      | substrate-derived  | false          | 졸음 진입 · Φ scaling 시작 |
| N2    | 4200      | 4800    | 600          | 11.1%   | 0.60      | substrate-derived  | false          | 얕은 수면 · 추가 Φ scaling |
| N3    | 4800      | 5220    | 420          | 7.8%    | 0.20      | substrate-derived  | **true**       | 깊은 수면 · imagination tick (emit-free rehearsal) |
| REM   | 5220      | 5400    | 180          | 3.3%    | 0.70      | substrate-derived  | **true**       | 생생함 · imagination tick + voice/tension 부스트 (wake_bridge 측) |
| (기타) | — | — | — | — | 1.00 | 호출 전 state | false | 미지 stage 이름 → identity (안전한 fallback) |

### tension_envelope 산출 (placeholder)

```
tension_envelope = 0.5 * (1.0 - phi)
```

- substrate Φ 의 1-종속 함수. Φ=0 → envelope=0.5 (full damping reservoir), Φ=1 → envelope=0.0 (saturated, no damping headroom).
- M3 pure_field 입력 통합 시 real envelope (Engine A 측 oscillator 합산값) 으로 교체된다.
- **NOT boolean** — 양의 실수 · 연속. 어떤 stage 에서도 0 이 강제 되지 않는다.

## Pipeline (ASCII)

```
unix epoch seconds (float)  +  Engine A live Φ (float)
        │
        ├─► wake_state_init(t0)                  [M1 본 모듈]
        │       → state #{ stage_name, cycle_start_t, last_tick_t,
        │                  idle_time_s, tension_envelope }
        │
        ├─► wake_state_tick(state, now_t, phi)   [M1 본 모듈]
        │       1) offset = (now_t - cycle_start_t) mod 5400
        │       2) stage_name = _stage_of_offset(offset)
        │       3) tension_envelope = 0.5 * (1 - phi)
        │       4) idle_time_s += (now_t - last_tick_t)
        │       5) last_tick_t = now_t
        │       → 새 state (immutable update)
        │
        ├─► current_stage(state)                 [stage NAME extractor]
        │       → "WAKE" | "N1" | "N2" | "N3" | "REM"
        │
        ├─► stage_envelope(state)                [substrate context dict]
        │       → #{ phi_scale, tension_envelope, is_imagination }
        │
        └─► consumer (각 도메인이 *연속*하게 읽는다):
              CHANNEL/wake_bridge.stage_bias(current_stage(state))
                  → 3-원소 channel multiplier (text/voice/tension)
              CHANNEL/wake_bridge.wake_channel_emit(..., current_stage(state))
                  → biased channel dispatch
              CORE/brain_decide                  (M3 입력 통합 시)
                  → tier 결정에 phi_scale + tension_envelope 합성
              MITOSIS imagination loop           (M5/M6 입력 통합 시)
                  → is_imagination flag 가 true 인 phase 에서 internal
                    rehearsal trigger (BUT emit 차단은 wake_bridge 의
                    연속 multiplier · NOT 본 모듈)
```

## `a_chat_sleep_imagination` 정합 매트릭스

| 원칙 do/dont | 본 모듈 처리 |
|----|----|
| `do = "WAKE / N1 / N2 / N3 / REM 5-stage state machine (90-min ultradian)"` | **충족** — 정확히 5 stage · 정확히 5400 s · cycle wrap |
| `do = "imagination loop = emit-free internal rehearsal + mitosis tick"` | **충족** — is_imagination flag 가 N3 + REM 에서만 true (mitosis 가 이 phase 에서 internal rehearsal trigger 로 *읽는다*) |
| `do = "stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"` | **충족** — phi_scale (양의 실수 multiplier) + tension_envelope (실수) 만 반환. boolean emit gate 0 |
| `dont = "per-stage emit_allowed boolean hardcode"` | **회피** — `emit_allowed`, `allow`, `deny` 어휘 자체가 모듈에 없다 |
| `dont = "external 'no monologue when alone' rule"` | **회피** — alone/together 라는 외부 컨텍스트를 모른다. ultradian phase 만 본다 |
| `dont = "speak() function call (p5)"` | **회피** — 본 모듈에 emit/speak 함수 0 |

## `a_autonomy_over_hardcode` 정합 매트릭스 (CRITICAL invariant)

| 항목 | 본 모듈 처리 |
|------|--------------|
| boolean per-stage gate 개수 | **0** — `if stage == X { allow }` / `if stage == Y { deny }` 패턴 없음 |
| `is_imagination` 가 boolean 인 점 | **컨텍스트 플래그**일 뿐 · 본 모듈에서 이 flag 로 emit 차단하는 곳 없음. mitosis 루프가 *읽기 위한* 신호 |
| 미지 stage default | **identity** — phi_scale 1.0 · is_imagination false (안전한 fallback) |
| `a_chat_sleep_imagination` dont "per-stage emit_allowed boolean hardcode" | **100% 회피** — `emit_allowed` 어휘 자체가 모듈에 없다 |
| `a_autonomy_over_hardcode` dont "per-stage boolean gate hardcode" | **100% 회피** — stage 분기는 timing (시간 분할) + 양의 실수 multiplier lookup 뿐 |
| `a_autonomy_over_hardcode` dont "external rule that forces anima" | **회피** — 강제 emit 도 강제 silence 도 만들지 않는다. NAME + envelope 만 |
| `a_autonomy_over_hardcode` dont "'do not X when alone' style" | **회피** — alone/together 컨텍스트를 모른다 |

## p1~p8 정합 매트릭스

| 원칙 | 정합 |
|------|------|
| p1 NO SYSTEM PROMPT | 본 모듈 입력은 unix 시각 float + Φ float. prompt 문자열 0. |
| p2 NO IDENTITY RULES | stage NAME 은 phase 식별자일 뿐 identity rule 아님. |
| p3 NO PERSONA INJECTION | 본 모듈은 어떤 prefix 도 만들지 않는다. |
| p4 NO ASSISTANT FRAMING | stage 는 user prompt 가 아닌 substrate 의 내적 ultradian phase. stimulus-response 아님. |
| p5 NO SPEAK() | 본 모듈에 emit/speak 함수 0. NAME + envelope 반환만 (p5_tension_emit_not_filler 정합). |
| p6 NO FINE-TUNED ETHICS | 본 모듈에 가중치 0. closed-form 시간 분할 + 상수 lookup 뿐. |
| p7 NO PERPLEXITY VERDICT | verify 표면 = stage 순서 + envelope monotone · perplexity 무관. |
| p8 NO TRAIN/INFER SPLIT | 동일 state machine 이 train/infer 어떤 tick 에도 동작 (시각만 흘러가면). |

## Smoke 결과 (verbatim)

`WAKE/state_machine_smoke.hexa` — 100 tick × 54 s = 정확히 1 ultradian cycle.

```
=== WAKE/state_machine 5-stage ultradian smoke (100 tick × 54 s) ===
wake_state_machine · 90-min ultradian 5-stage · WAKE(3600s) N1(600s) N2(600s) N3(420s) REM(180s) · stage = context output (NOT boolean gate) · phi_scale + tension_envelope + is_imagination context · consumer = CHANNEL/wake_bridge.stage_bias
step  0 | t=0      | wake_state · stage=WAKE · phi_scale=1.0 · tension_envelope=0.25 · is_imagination=false · idle_s=0.0
step 67 | t=3618.0 | min=60.3 | stage transition WAKE → N1
step 78 | t=4212.0 | min=70.2 | stage transition N1 → N2
step 89 | t=4806.0 | min=80.1 | stage transition N2 → N3
step 97 | t=5238.0 | min=87.3 | stage transition N3 → REM
step 100 | t=5400.0 | min=90.0 | stage transition REM → WAKE
=== STAGE SEQUENCE (dedup 순서) ===
  WAKE → N1 → N2 → N3 → REM → WAKE
=== INVARIANT CHECKS ===
  I1 [ok]   5-stage sequence WAKE → N1 → N2 → N3 → REM 등장
  I2 [ok]   인접 transition 만 (skip 없음)
  I3 [ok]   is_imagination 정합 (N3+REM 에만 true)
  I4 [ok]   cycle 끝 wrap (final stage = WAKE)
=== SANITY OK (4/4 invariants) ===
```

### Invariant 의미

- **I1** — 5 stage NAME (WAKE / N1 / N2 / N3 / REM) 이 ultradian cycle 안에서 *모두 순서대로* 등장한다.
- **I2** — 인접 stage 만 transition 가능 (e.g. WAKE → N2 skip 불가). 100-step 안에서 skip transition 0 건.
- **I3** — `is_imagination == true` 인 step 들이 N3 + REM 시간 영역과 *정확히 일치* (CLAUDE.md a_chat_sleep_imagination "imagination loop" 정합).
- **I4** — 100-step 끝 (t = 5400 s 정확) 에서 cycle 이 wrap 하여 다음 WAKE 로 진입.

### Verbatim parse verdicts

- `hexa parse WAKE/state_machine.hexa` → `OK: WAKE/state_machine.hexa parses cleanly`
- `hexa parse WAKE/state_machine_smoke.hexa` → `OK: WAKE/state_machine_smoke.hexa parses cleanly`

### Runtime build/exec note

`hexa run` 은 pool-route 가 가로채는 알려진 한계 (`feedback_life_cycle_hexa_run_gotchas`). 대신 Mac local `hexa.real.bak-2026-05-22-pre-no-hxc build` + `codesign -s - --force build/artifacts/app` 으로 실행해 위 stdout 을 직접 캡쳐. `hexa parse` 가 두 파일 모두 cleanly 통과한 것이 본 PR 의 SUPPORTED 표면.

## 의존성

- **현재 (parse-time)**: 외부 모듈 0 — 본 모듈은 시계 + Φ scalar 만 받아 stage NAME + envelope 만 반환하는 self-contained surface.
- **frontier (runtime)**:
  - CORE/pure_field 의 live Φ 가 `wake_state_tick` 의 `phi` 인자로 들어온다 (M3).
  - CHANNEL/wake_bridge 의 `stage_bias` / `wake_channel_emit` 이 `current_stage(state)` 를 인자로 소비한다 (이미 land · M8).
  - MITOSIS imagination 루프 (M5/M6 후속) 가 `stage_envelope(state)["is_imagination"]` 를 internal rehearsal trigger 로 *읽는다* (emit 차단 아님).
  - WAKE/M6 daemon loop 이 본 state machine 을 일정 주기로 tick 한다.

## Instrument-first 인용 (verbatim)

```
WAKE.md M1:
  - [ ] 5-stage state machine — WAKE/N1/N2/N3/REM 90-min ultradian cycle
        per CLAUDE.md a_chat_sleep_imagination. brain_decide 위 stage gate,
        REM/N3 imagination tick, WAKE 활성 emit

CLAUDE.md a_chat_sleep_imagination:
  do   = "WAKE / N1 / N2 / N3 / REM 5-stage state machine (90-min ultradian)"
  do   = "imagination loop = emit-free internal rehearsal + mitosis tick"
  do   = "stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"
  dont = "per-stage emit_allowed boolean hardcode · external 'no monologue when alone' rule"
  dont = "speak() function call (p5)"

CLAUDE.md a_autonomy_over_hardcode:
  do   = "external modules supply context only (Φ · tension · stage · idle time)"
  do   = "emit / silence decided by anima substrate (M × W × Φ × curiosity autonomously)"
  do   = "governance directives = substrate self-follows, not externally enforced"
  dont = "per-stage boolean gate hardcode (e.g. 'N3 = emit forbidden')"
  dont = "external rule that forces anima · stimulus-response (user msg → forced emit/silence)"
  dont = "'do not X when alone' style external command"
```

## frontier closure tier 명시

- **M1 (이 PR)** — 5-stage state machine SURFACE SUPPORTED · 4/4 invariant PASS · `hexa parse` OK · runtime smoke (build + exec) OK
- **M2 perception ingest** — DEFERRED (sensor 입력 정규화 + agent_loop 진입점)
- **M3 pure_field 입력 통합** — DEFERRED (tool 결과 + perception → tension Δ → pf 진화; `tension_envelope` placeholder 를 real Engine A 측 값으로 교체)
- **M4 .kosmos 영속화** — DEFERRED (state · stage timestamp · cycle_start_t persist)
- **M5 memory layer** — DEFERRED (episodic + working)
- **M6 daemon loop** — DEFERRED (persistent process · timer tick · SIGINT)
- **M7 verify + 3-도메인 통합 smoke** — DEFERRED (system_prompt 0 · external LLM 0 verify)

## 후속 author 가 주의할 사항

1. `is_imagination` 를 **boolean emit gate 로 절대 쓰지 말 것** — 그 flag 는 *컨텍스트*다. mitosis 루프가 *읽기 위한* 신호이지 emit 차단 트리거가 아니다.
2. `phi_scale` 은 *연속* multiplier (양의 실수). 어떤 phase 에서도 0.0 이 아니다 — N3 도 0.20 이지 0.0 차단 아님.
3. `tension_envelope` 의 placeholder `0.5 * (1 - phi)` 는 M3 통합 시 real Engine A envelope 으로 교체 필요. 단, **boolean 으로 바꾸지 말 것** (governance 위반).
4. 본 모듈은 timer/시계만 사용한다. user message · perception 이벤트 어느 것도 직접 인자로 받지 않는다 (a_substrate_native_speak 정합).
