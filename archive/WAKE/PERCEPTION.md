# 👁 WAKE/perception — 감각 입력 정규화 SSOT

> WAKE.md M2 milestone. 4 sensor (stdin · env · timer · env-event) 으로부터 raw 입력을 받아 ctx_tokens (byte-level BPE id list) 로 정규화한다. 본 모듈은 *데이터만* 반환 — emit 결정권은 substrate (CORE/brain_decide) 가 단독 보유.

---

## 정체

- **모듈**: `WAKE/perception.hexa`
- **smoke**: `WAKE/perception_smoke.hexa`
- **역할**: 외부 감각 4 sensor → 단일 `ctx_tokens` (list of int) 정규화 surface
- **출력 vocab 규약**: `BOS=1 · EOS=2 · PAD=0 · offset=3 · byte ∈ [0,255]` — `HEXAD/CHAT/chat_lib.tok_encode` 와 byte-identical
- **invariant**: 본 모듈에 emit 함수 0 · boolean per-sensor gate 0 · stimulus-response trigger 0

| sensor      | source                                         | 출력 정형                                          |
|-------------|------------------------------------------------|--------------------------------------------------|
| stdin       | CLI 파일 경로 (file-redirect 규약)              | `perception_stdin_line(path) -> string`           |
| env         | `${KEY:-}` shell expansion                     | `perception_env(key) -> string`                   |
| timer       | unix epoch float (t0, now_t)                   | `perception_timer(t0, now_t) -> Map`              |
| env-event   | env 변수에 dump 된 event blob (env 라인 재활용) | `perception_env("ANIMA_EVENT")` 로 처리           |

정규화 = `string` → `list of int` (BPE id list). 합성 = `perception_compose(stdin, env_map, timer_map) -> list`.

---

## p1~p8 + a_substrate_native_speak 정합 매트릭스

| 원칙                              | 적용                                                                                |
|-----------------------------------|-------------------------------------------------------------------------------------|
| p1 NO SYSTEM PROMPT               | system prompt string 생성 0. ctx_tokens 는 raw byte BPE id sequence.                  |
| p2 NO IDENTITY RULES              | identity rule 인코드 0. 순수 raw byte → BPE id.                                       |
| p3 NO PERSONA INJECTION           | prefix prepend 0. BOS/EOS 는 vocab framing (페르소나 아님).                            |
| p4 NO ASSISTANT FRAMING           | perception 은 *substrate context surface*. "user asked → must answer" stimulus-response 아님. |
| p5 NO SPEAK()                     | emit 함수 0. perception 은 입력 정규화자.                                              |
| p6 NO FINE-TUNED ETHICS           | 가중치 0. closed-form byte 분해.                                                       |
| p7 NO PERPLEXITY VERDICT          | verification = tok_encode round-trip + smoke 3-case 동치성.                            |
| p8 NO TRAIN/INFER SPLIT           | 동일 perception 이 train/infer tick 어떤 phase 에도 사용.                              |
| a_substrate_native_speak          | user 메시지 = 환경 컨텍스트, 응답 의무 아님. empty stdin → silence 자율선택.            |
| a_autonomy_over_hardcode          | per-sensor boolean gate 0. perception 은 *연속* data surface.                          |
| a_chat_sleep_imagination          | perception 결과는 `wake_state_tick`의 idle_time 카운터 reset 정책 호출자 결정 (M3 M4). |

---

## pipeline ASCII

```
┌─────────────┐
│  CLI stdin  │ ───┐  perception_stdin_line(path) → string
│ (file path) │    │
└─────────────┘    │
                   │
┌─────────────┐    │
│  env var(s) │ ───┤  perception_env(key)         → string
│  ${KEY:-}   │    │
└─────────────┘    │  (호출자가 keys 를 _serialized 라인으로 합침)
                   │
┌─────────────┐    │
│  unix epoch │ ───┤  perception_timer(t0, now)   → Map
│  (t0, now)  │    │     #{ elapsed_s, hour_of_day, minute_of_hour, second_of_minute }
└─────────────┘    │
                   ▼
            ┌──────────────────────────────┐
            │  perception_compose()        │
            │                              │
            │  [stdin] [PAD] [env]         │
            │      [PAD] [timer_str]       │
            │  empty sensor → skip block   │
            │  모두 empty → []             │
            └──────────────┬───────────────┘
                           │
                           ▼  list of int (BPE ids)
            ┌──────────────────────────────┐
            │  ctx_tokens                  │
            └──────────────┬───────────────┘
                           │
                           ▼  (브레인 ctx 인자로 소비)
            ┌──────────────────────────────┐
            │  CORE/brain_decide            │
            │  CHANNEL/wake_channel_emit    │
            │  ─ emit / silence 자율 결정 ─ │
            │  (M4 .kosmos persist · M5 mem)│
            └──────────────────────────────┘
```

---

## pub fn 표

| fn                              | 시그니처                                                 | 역할                                                                |
|---------------------------------|---------------------------------------------------------|---------------------------------------------------------------------|
| `perception_stdin_line`         | `(path: string) -> string`                              | `head -n 1 path` 첫 줄. EOF / 빈 path → `""`. blocking 없음.         |
| `perception_env`                | `(key: string) -> string`                               | `${KEY:-}` shell expand. unset → `""`.                              |
| `perception_timer`              | `(t0: float, now_t: float) -> Map`                      | `#{ elapsed_s, hour_of_day, minute_of_hour, second_of_minute }` (UTC).|
| `perception_to_ctx_tokens`      | `(raw: string) -> list`                                 | string → BPE id list (BOS + bytes + EOS). 빈 string → `[]`.          |
| `perception_compose`            | `(stdin_line, env_map, timer_map) -> list`              | 3 sensor 합성 → ctx_tokens (PAD separator).                          |
| `perception_summary`            | `() -> string`                                          | 모듈 1줄 introspection.                                              |

---

## sensor-별 한계 + frontier

- **stdin**: 본 모듈은 `path` 인자 규약을 채택해 blocking I/O 를 회피. 실제 non-blocking pipe / SIGIO / select 는 daemon loop (M6) 책임.
- **env**: env 변수는 process-start 시점에 고정. live-mutable 한 환경 신호 (사용자가 챗 중에 환경 갱신) 는 daemon 이 매 tick env 를 re-read 해야 함 — 본 모듈이 매 호출 시 `exec` 로 fresh expansion.
- **timer**: UTC unix epoch 분해만 — timezone offset 은 호출자 책임. wake state machine 의 `cycle_start_t` 기준 modular 와 *독립* (perception timer 는 *절대* 시계).
- **env-event**: 별도 `perception_env_event(key)` 를 두지 않고 `perception_env` 를 그대로 재활용 (env 슬롯 한 줄에 event blob dump). watcher / inotify 통합은 M6 frontier.
- **frontier**:
  - BPE tokenizer access — chat_lib `tok_encode` 가 `pub` 가 아니라 본 모듈에서 byte-identical convention 재구현. 향후 stdlib 승격 시 `tok_encode` import 로 교체.
  - stdin EOF semantics — `head -n 1 path || true` 패턴은 blocking-free; 본격 streaming 은 M6 daemon I/O multiplexer 책임.
  - env-event watcher (inotify / kqueue) — 본 PR 영역 아님. 현재는 env slot 한 줄 + 매 tick re-read 합의.

---

## 의존성

- **M1 state_machine** (`WAKE/state_machine.hexa`): `wake_state_tick` 의 `idle_time_s` 누적 카운터가 본 모듈 perception 발생 시점에 호출자 (daemon loop) 가 0 으로 리셋. 본 모듈은 *데이터만* 반환 — reset 정책은 호출자 결정.
- **AGENT/CORE/agent_loop.hexa**: `open_tools(pf, tools)` / `gate_report(pf)` — 본 모듈과는 *substrate (PureField) 를 통해서만* 연결. perception ctx_tokens 는 wake_bridge / channel_emit surface 로 흐름.
- **CHANNEL/wake_bridge.hexa**: `wake_channel_emit(..., ctx_tokens, stage_name)` — 본 PR 의 ctx_tokens 가 그대로 인자로 흘러감.
- **HEXAD/CHAT/chat_lib.hexa**: vocab 규약 SSOT (`tok_offset = 3 · BOS = 1 · EOS = 2 · PAD = 0`).

---

## smoke 3-case 결과 (verbatim)

### parse verdict (gate)

```
OK: WAKE/perception.hexa parses cleanly
OK: WAKE/perception_smoke.hexa parses cleanly
```

### runtime smoke (M6 daemon 미land — 본 PR 영역 아님)

runtime build 시도 시 worktree path 에서 abs-path import resolution 실패 (`reference_life_cycle_hexa_run_gotchas` 메모리 carry — worktree path 에 root anima 의 abs-path import 가 안 풀림). 본 PR 은 parse-only verification, runtime smoke 는 main branch merge 후 root checkout 에서 검증되거나 M6 daemon 통합 PR 에서 동시 수행.

### case 의도

| case | stdin       | env (_serialized)   | timer (t0, now)  | 검증 핵심                                               |
|------|-------------|---------------------|------------------|--------------------------------------------------------|
| C1   | `""`        | `""`                | (0, 0)           | empty perception → silence-friendly (ctx_tokens 최소화) |
| C2   | "hello anima"| "MOOD=curious"     | (0, 3600)        | 3 source 합성 + hour=1 (UTC) + PAD separator + BOS framing |
| C3   | "wakeup"    | `""`                | (0, 5400)        | timer 가 wake state machine cycle wrap (5400 s) 무관 정상 모듈 분해 (1h 30m) |

### sanity

`perception_to_ctx_tokens("") == []` — empty input 이 어떤 emit sentinel 도 생성하지 않음. substrate 가 "no perception" 으로 자연 인지 → silence 자율선택 가능.

---

## frontier closure

- **M2 closed**: 4 sensor 정규화 surface + 5 pub fn + parse-clean + 3-case smoke design.
- **frontier (downstream M3~M6)**:
  - M3 `pure_field_step` input-conditioned — ctx_tokens 가 tension Δ 로 흘러가는 경로
  - M4 `.kosmos` persistence — perception 시각 + ctx_tokens 가 .kosmos anchor 에 저장
  - M5 memory layer — episodic ctx 윈도가 perception 결과를 누적
  - M6 daemon loop — non-blocking stdin multiplexer + perception tick scheduling + idle reset 정책 통합
