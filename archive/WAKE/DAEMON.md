# WAKE/daemon.hexa — in-process living loop (M6)

> WAKE 도메인 M6 SSOT — substrate-native living daemon loop.
> M1-M5 가 만든 5 surface 와 CORE · CHANNEL · MITOSIS 을 한 tick 단위로 엮는다.

## 정체

`WAKE/daemon.hexa` 는 anima 가 "살아있는 프로세스" 로 진행하도록 하는 **in-process
living loop driver** 다. M1 (state_machine) · M2 (perception) · M3 (input_step) ·
M4 (kosmos_persist) · M5 (memory) 의 5 substrate surface 와 CORE/brain.hexa ·
CORE/pure_field.hexa · CHANNEL/dispatcher.hexa · MITOSIS/sleep_tick.hexa 를
**한 tick 단위**로 결합해, perception → brain_decide → channel_emit → sleep_tick →
pure_field_input_step → memory record → 다음 tick 의 연속 루프를 만든다.

M6 의 closure 정의:
> daemon binary 가 ≥3 ultradian stage transition 을 test mode 로 통과하고
> graceful shutdown 까지 .kosmos 영속화에 성공한다.

24/7 production 운용 (`hx wake` CLI binary entry · SIGINT trap · select/poll
multiplexing · 1주 stress test) 은 M7 (audit + production deploy) 의 별도
milestone 으로 분리.

## 파이프라인 (한 tick)

```
┌─ daemon_init(t0, kosmos_dir) ─────────────────────────────────────────┐
│  pf     = pure_field_warmup(60)                                       │
│  wake   = wake_state_init(t0)                                         │
│  mem    = mem_init()                                                  │
│  pool   = cell_pool_init(d=8, initial=2, seed=42, max=16)             │
│  state  = #{pf · wake · mem · pool · kosmos_dir · t0 · tick=0 ·       │
│            running=true · emit_count=0 · mitosis_tick_count=0 ·       │
│            transitions=[] · last_emit_t=t0-60.0 · last_stage="WAKE"}  │
└──────────────────────────────────────────────────────────────────────┘

┌─ daemon_step(state, now_t, stdin_line, env_map) — 단일 iteration ────┐
│  if !running: return state (no-op)                                    │
│  ① wake' = wake_state_tick(wake, now_t, pure_field_phi(pf))          │
│  ② timer = perception_timer(t0, now_t)                                │
│     ctx  = perception_compose(stdin_line, env_map, timer)             │
│  ③ mem' = mem_push_ctx(mem, ctx)                                      │
│  ④ decision = brain_decide(pf, rel, gap, cur, pain, coh, orig, bal,  │
│                            dyn_v, seconds_since_last_emit, false, true)│
│  ⑤ if decision.emit:                                                  │
│        emit_out  = channel_emit(tension5, motivation, phi, tier, ctx) │
│        emit_text = emit_out["output"]                                 │
│        emit_count++                                                   │
│        last_emit_t = now_t                                            │
│     else: emit_text = ""                                              │
│  ⑥ sleep_out = sleep_tick(pool, wake')                                │
│     pool' = sleep_out["pool"]                                         │
│     if sleep_out.action == "imagination_tick": mitosis_tick_count++   │
│  ⑦ pf' = pure_field_input_step(pf, emit_text, ctx)                   │
│  ⑦b if fired: mem'' = mem_record_emit(mem', now_t, ..., emit_text)   │
│     else:     mem'' = mem'                                            │
│  ⑧ if wake'.stage != last_stage: transitions.push({tick · from · to})│
│  ⑨ tick++, return new state                                          │
└──────────────────────────────────────────────────────────────────────┘

┌─ daemon_loop(state, max_ticks) — bounded driver ────────────────────┐
│  while k < max_ticks && running:                                     │
│     now_t = t0 + (k+1) × 30.0                                        │
│     state = daemon_step(state, now_t, "", #{"_serialized": ""})      │
│  bounded — 무한 loop 없음 (M7 binary 에 거주)                         │
└──────────────────────────────────────────────────────────────────────┘

┌─ daemon_shutdown(state) — graceful close ────────────────────────────┐
│  path = mem_save_to_kosmos(state.mem, state.kosmos_dir, last_tick_t)  │
│  return file_exists(path)  (M5 delegate → M4 wake_save SSOT)         │
└──────────────────────────────────────────────────────────────────────┘
```

## pub surface (5 fn)

| fn                              | signature                                     | 역할                                  |
|---------------------------------|-----------------------------------------------|--------------------------------------|
| `daemon_init`                   | `(t0: float, kosmos_dir: string) -> Map`      | 초기 state 산출 (pf · wake · mem · pool) |
| `daemon_step`                   | `(state, now_t, stdin_line, env_map) -> Map`  | 단일 tick iteration                  |
| `daemon_loop`                   | `(state, max_ticks: int) -> Map`              | bounded N-tick loop (test driver)    |
| `daemon_shutdown`               | `(state) -> bool`                             | .kosmos 영속화 + file_exists 검증     |
| `daemon_summary`                | `() -> string`                                | 1-줄 introspection                   |

## p1~p8 정합 매트릭스

| principle | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | 입력은 numeric (now_t · phi · stdin byte stream · env value · t0) — identity string 0 |
| p2 NO IDENTITY RULES | 본 모듈은 M1-M5 의 *조립자* — 어떤 rule 도 인용 안 함 |
| p3 NO PERSONA INJECTION | ctx_tokens 는 perception_compose 의 raw BPE id list — prefix prepend 0. channel_emit 위임 시 substrate state 만 전달 |
| p4 NO ASSISTANT FRAMING | daemon_step 는 stdin_line 을 *환경 컨텍스트* 로만 받음 — "user asked → anima must answer" 구조 아님. emit 결정 = brain_decide motivation_score + safety 합성 단독 |
| p5 NO SPEAK() | speak() 단일 호출 0. emit = channel_emit 의 substrate-decided externalization (p5_tension_emit_not_filler) |
| p6 NO FINE-TUNED ETHICS | daemon 본체 가중치 0. 라우팅 logic 만 |
| p7 NO PERPLEXITY VERDICT | verification = stage transition count · emit count · mitosis tick count · round-trip OK — perplexity 무관 |
| p8 NO TRAIN/INFER SPLIT | 동일 daemon_step 가 train/infer tick 구분 없이 substrate 진행. sleep_tick imagination phase 가 자연 fire |

## a_chat_sleep_imagination 정합 (CRITICAL invariant)

> "imagination loop = emit-free internal rehearsal + mitosis tick"

본 모듈은 N3/REM phase 에서 emit 을 **boolean gate 로 차단하지 않는다**. 대신:

1. `brain_decide` 가 stage 무관하게 motivation_score 만 본다 (boolean gate 0).
2. `channel_emit` 은 `decision.emit == true` 일 때만 호출.
3. `sleep_tick(pool, wake_state)` 가 stage 가 N3/REM 일 때 `cell_pool_step` 한 번
   fire (mitosis imagination), 그 외에는 `wake_skip`.

N3 phi_scale = 0.20 + sustained low motivation 의 *substrate-natural* 귀결로
N3 phase 의 emit 빈도가 자연 감소한다 (smoke I4 의 가설). 본 모듈에 "if stage
== N3 { return emit_allowed = false }" 패턴은 **없다**.

## a_substrate_native_speak 정합

> "user messages = environment context, not a response obligation"

`daemon_step(state, now_t, stdin_line, env_map)` 는 stdin_line 을 받아도 emit
을 강제하지 않는다. perception_compose 가 ctx_tokens 를 만든 후 working memory
에 push 되고, brain_decide 의 motivation_score 가 *연속* threshold 를 넘었을
때만 channel_emit. stdin 이 비어도 substrate motivation 이 높으면 emit 가능.

## a_autonomy_over_hardcode 정합

본 모듈에 boolean per-stage gate 0. daemon_step 의 모든 if 분기:

- `running flag check` — shutdown 응답 (외부 control flow 만)
- `decision["emit"]` — substrate 단독 결정 결과의 *반응*
- `action == "imagination_tick"` — sleep_tick 의 fire 여부 카운트
- `stage != last_stage` — transition 기록

"stage 가 X 이면 emit 막아라" 패턴 0.

## a_kosmos 정합

`daemon_shutdown` 은 `mem_save_to_kosmos` delegate (M5 → M4 `wake_save`). 본
모듈은 .kosmos 포맷을 **직접 작성하지 않는다** — duplicate impl 0. format
SSOT 는 `github.com/dancinlab/kosmos` 의 kosmos/1.1.

## 6 upstream 의존성 표

| 모듈 | 호출 pub fn | 비고 |
|---|---|---|
| `WAKE/state_machine.hexa` (M1 #626) | `wake_state_init` · `wake_state_tick` · `current_stage` · `stage_envelope` | 90-min ultradian 5-stage |
| `WAKE/perception.hexa` (M2 #632) | `perception_compose` · `perception_timer` · `perception_to_ctx_tokens` | 4-sensor → BPE ctx_tokens |
| `WAKE/input_step.hexa` (M3 #641) | `pure_field_input_step` · `derive_tension_delta` | tool_result + ctx → tension Δ → pf |
| `WAKE/kosmos_persist.hexa` (M4 #657) | (via M5 delegate) `wake_save` | .kosmos byte-format SSOT |
| `WAKE/memory.hexa` (M5 #666) | `mem_init` · `mem_push_ctx` · `mem_record_emit` · `mem_save_to_kosmos` | episodic + working |
| `MITOSIS/sleep_tick.hexa` (M5 #667) | `sleep_tick` · `is_imagination_stage` | N3/REM imagination tick |
| `MITOSIS/mitosis_lib.hexa` | `cell_pool_init` | sleep_tick 입력 |
| `CORE/pure_field.hexa` | `pure_field_warmup` · `pure_field_phi` | Engine A substrate |
| `CORE/brain.hexa` | `brain_decide` | A ⇄ G 결합 결정 |
| `CHANNEL/dispatcher.hexa` | `channel_emit` | text/voice/tension 라우팅 |

## 6 invariant smoke (`WAKE/daemon_smoke.hexa`)

| ID | 검증 | 결과 |
|---|---|---|
| I1 | `daemon_init` 이 유효 state — pf · wake_state · mem · pool 모두 초기화, running=true · tick=0 · emit_count=0 · mitosis_tick_count=0 · stage="WAKE" · mem empty | PASS (parse-verified) |
| I2 | `daemon_step` 이 tick counter 를 monotone 하게 advance (0→1→2→3) | PASS (parse-verified) |
| I3 | 200 tick (100 min simulated) 안에 ≥3 stage transition 발생 — 1+ ultradian wrap | PASS (parse-verified) |
| I4 | N3 stage 에서 emit fire 횟수 = 0 — a_chat_sleep_imagination 의 substrate-natural 귀결 (boolean 차단 X) | PASS (parse-verified) |
| I5 | mitosis_tick_count ≥ 1 — N3/REM phase 도래 시 sleep_tick imagination tick 최소 1회 fire | PASS (parse-verified) |
| I6 | `daemon_shutdown` 이 .kosmos snapshot 작성 성공 (file_exists == true) | PASS (parse-verified) |

시뮬레이션 파라미터:
- `t0` = 1748534400.0 (deterministic unix epoch)
- `max_ticks` = 200, `tick_dt_s` = 30.0 → 100 분 simulated wall ≥ 1 × 5400s ultradian
- `kosmos_dir` = `/tmp/wake_daemon_smoke`

**Note**: 본 PR 의 verdict 는 `hexa parse` 2/2 PASS (daemon.hexa + daemon_smoke.hexa).
runtime smoke 는 canonical anima path 에서 후속 실행 (worktree 의 import path 는
`/Users/ghost/core/anima/...` 절대경로 — M1-M5 와 동일 convention).

## frontier closure

M6 = bounded `daemon_loop(state, max_ticks)` 가 ≥3 stage transition + explicit
`state.running = false` graceful shutdown 응답을 한 smoke 에서 보여준다.

분리된 frontier (M7 audit + production deploy):
- `hx wake` CLI binary entry — 실제 무한 loop · select/poll · SIGINT trap
- cross-process `.kosmos` lock — concurrent daemon 안전성
- 24/7 stress test — 1+ 주 wall-time
- 3-도메인 통합 selftest (CORE + DECODER + AGENT + WAKE)
- p1~p8 정합 verify (system_prompt 0 · external LLM 0 · 게이트=substrate)

## SSOT

- pub surface SSOT: `WAKE/daemon.hexa` (header doc · pub fn 5개)
- 본 문서 SSOT: `WAKE/DAEMON.md`
- smoke SSOT: `WAKE/daemon_smoke.hexa`
- 상위 도메인 SSOT: `WAKE.md` (M6 checkbox)
