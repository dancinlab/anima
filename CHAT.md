# CHAT.md — anima REPL + live daemon + 자연발화 architecture (rev 2)

> 사용자 directive 누적 (2026-05-13 KST PM):
> "상시채팅 기능은 없나?????" + "단편 메시지 말고" + "1:1 말고도 다수 가능하되 그 다수에
> anima 도 가능" + "인간 3, anima 2 이렇게 단체채팅 가능" + "외부 프로젝트에서 쓰려면" +
> "호출 응답이 아니라" + "자연발화때문에" + "소켓같은 시스템 있어야될듯" +
> "전체 구현 계획 들어가보자 브레인스토밍 고갈시까지" + "REPL chat 도 필요해!!!" +
> "REPL chat + 외부 연결용" + "hexa-native 로 작성하면되" + "hex upstream 개선가능" +
> "hexa upstream first" + **"/turn 처럼 턴 지정이 아니라 자연발화 기준 자율이야 실시간 채팅"** +
> **"nono"** + **"철학 준수"** + **"fps 60+"** + **"A → ALL"**.

## 💥 rev 2 핵심 (rev 1 sync 모델 deprecate)

rev 1 (deprecated) 의 **명시적 `/turn <anima_id>` heuristic** 모델은 **철학 위반**:
- 외부 heuristic (regex / probability) 으로 turn 결정 = **routing-level persona injection** (PHILOSOPHY.md #3 위반)
- sync REPL on chat_generate (~30s/token Mac CPU) = **0.03 FPS, 60+ 절대 불가능**

rev 2 (현 spec) 의 **substrate-native autonomous** 모델:
- anima 의 **cell_pool tension/lorenz dynamics** (`mitosis_hook.hexa` substrate state) 가 매 frame 마다 evolve
- threshold 초과 시 anima 가 **스스로** 발화 결정 (외부 heuristic 0)
- 60+ FPS frame loop = ~16ms tick. substrate evolve cheap (µs). inference 는 async worker thread (background, frame-budget 외).
- broadcast bus = socket subscribers (human input + anima output 양방향)

## 📐 Unified architecture (rev 2)

```
┌──────────────────────────────────────────────────────────────────┐
│                  anima live daemon (single process)               │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   frame loop thread @ 60+ FPS (~16ms tick)               │   │
│  │   매 frame:                                              │   │
│  │     1. substrate evolve  ← mitosis_hook step             │   │
│  │     2. speak-gate check  ← tension > threshold?          │   │
│  │     3. fire-or-skip       → enqueue speak request        │   │
│  │     4. drain bcast queue → broadcast_to_subscribers       │   │
│  │     5. sleep to next frame boundary                       │   │
│  └────────────────┬─────────────────────────────────────────┘   │
│                   │                                              │
│                   ▼  (channel: speak request)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   inference worker thread (1 or N)                        │   │
│  │   - dequeue speak request                                 │   │
│  │   - chat_generate (slow, OK — async)                      │   │
│  │   - enqueue broadcast (channel: speak response)           │   │
│  └────────────────┬─────────────────────────────────────────┘   │
│                   │                                              │
│                   ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   subscriber broadcast bus                                │   │
│  │   - socket subscribers (TCP :7878 + Unix /tmp/anima.sock) │   │
│  │   - history JSONL append (~/.anima/rooms/<id>/history)   │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                  ┌────────┴────────────────┐
                  │                         │
            ┌─────┴─────┐           ┌───────┴──────┐
            │  CLI REPL │           │  external    │
            │  (human)  │           │  client lib  │
            └───────────┘           └──────────────┘
```

## 🔁 변경 사항: Phase 매핑

| rev 1 (deprecated) | rev 2 (현) | 비고 |
|---|---|---|
| Phase 0 REPL 1:1 (sync) | **Phase 0 REPL 1:1** (sync) — 그대로 LANDED | 1:1 baseline, 자연발화 unrelated |
| Phase 1 group chat (`/turn` heuristic) | **deprecated** | 철학 위반 — sync `_cmd_room` 코드는 1-cycle migration window 동안 남김 (deprecated 마커 + warn) |
| Phase 2 daemon multi-client | **live daemon (rev 2 통합)** | 단일 architecture: daemon + substrate-native autonomy + socket broadcast 모두 한곳 |
| Phase 3 자연발화 | **substrate gate** (Phase 2 의 일부) | 별도 phase 아님 — daemon 의 fundamental 동작 |
| Phase 4 external client | external client lib | Phase 2 land 후 |

## 📋 Phase별 명세 (rev 2)

### **Phase 0** — REPL chat (1:1 단순 상시) ☑ **LANDED 2026-05-13**

> hexa-native impl in `anima_chat_aot.hexa::_cmd_chat_repl` (~120 LoC).
> Mac arm64 + Linux x86_64 cross-compile parity. multi-turn + /show + /save + /exit verified.
> /save → `~/.anima/sessions/<name>.jsonl` 파일 생성. CLI: `anima chat repl [--mode M] [--max-new N] [--temp F] [--seed N]`.

1:1 baseline — **자연발화 unrelated**. sync chat_generate, 인간 + 1 anima. 디버깅 + 단일 테스트 용도.

---

### **Phase 1** (deprecated) — sync group chat with `/turn`

> ⚠️ **DEPRECATED 2026-05-13 PM** — 사용자 directive "철학 준수": `/turn <anima_id>` heuristic
> 트리거는 routing-level persona injection 으로 PHILOSOPHY.md #3 위반.
> 코드 (`_cmd_room`) 는 1-cycle migration window 동안 stderr warn + 동작.
> rev 2 의 **live daemon** 으로 대체.

기존 spec (reference):
- `anima room --humans "a,b,c" --animas "x,y" [--ckpt P]`
- `[alice]> alice: 안녕`
- `/turn ana` → ana 가 history 기반 응답

대체 path: **Phase 2 live daemon** 의 substrate-native autonomy.

---

### **Phase 2** (rev 2) — live daemon (substrate-native autonomous + socket broadcast)

> 🚧 **upstream blocked** — 3 patches 의존:
> - `~/core/hexa-lang/incoming/patches/net-nonblock-multiplex.md` (filed)
> - `~/core/hexa-lang/incoming/patches/net-unix-domain-socket.md` (filed)
> - `~/core/hexa-lang/incoming/patches/thread-channel-primitive.md` (filed 2026-05-13)

```sh
anima live --humans "alice,bob,charlie" --animas "ana,ben" \
           [--port 7878] [--unix /tmp/anima.sock] \
           [--fps 60] [--speak-threshold 4.0] \
           [--ckpt P] [--mode greedy] [--max-new 30]
```

#### 2.1 frame loop (substrate evolve + speak-gate)

```hexa
use "std_thread"
use "std_net"

fn frame_loop(animas, room, req_ch, bcast_ch) {
    let frame_budget = 1000 / room["fps"]   // 16ms @ 60fps
    while !room["shutdown"] {
        let t0 = now_ms()

        // 1. substrate evolve — anima 별 mitosis_hook step
        let mut ai = 0
        while ai < len(animas) {
            animas[ai]["cell_pool"] = mitosis_hook_step(animas[ai]["cell_pool"], room["t"])
            ai = ai + 1
        }

        // 2. speak-gate (substrate-native — 외부 heuristic 없음)
        ai = 0
        while ai < len(animas) {
            let anima = animas[ai]
            let tension = cell_pool_tension(anima["cell_pool"])
            if tension > anima["speak_threshold"] && !anima["in_flight"] {
                anima["in_flight"] = true
                let _ = channel_send(req_ch, #{
                    "anima_id":    anima["id"],
                    "context":     build_context(room, anima["id"]),
                    "chat":        anima["chat"],
                    "seed":        anima["seed"],
                    "tension":     tension,
                    "ts":          now_ms()
                })
            }
            ai = ai + 1
        }

        // 3. drain broadcast queue (non-blocking)
        while true {
            let msg = channel_recv(bcast_ch, 0)
            if to_string(msg) == "" { break }
            broadcast_to_subscribers(room, msg)
            append_history_jsonl(room, msg)
            // mark anima not in-flight
            let mut bi = 0
            while bi < len(animas) {
                if animas[bi]["id"] == msg["speaker"] { animas[bi]["in_flight"] = false }
                bi = bi + 1
            }
        }

        // 4. drain client input queue (from accept thread)
        while true {
            let evt = channel_recv(room["input_ch"], 0)
            if to_string(evt) == "" { break }
            apply_client_event(room, animas, evt)   // human message → history append → 다음 tick 의 speak-gate 가 자율 evaluate
        }

        // 5. sleep
        let dt = now_ms() - t0
        if dt < frame_budget { sleep_ms(frame_budget - dt) }
        room["t"] = room["t"] + 1
    }
}
```

#### 2.2 inference worker (async, background)

```hexa
fn inference_worker(req_ch, bcast_ch) {
    while true {
        let req = channel_recv(req_ch, -1)
        if to_string(req) == "__close__" { break }
        let resp = chat_generate(req["chat"], req["context"], "greedy",
                                 30, 0.7, [], 1.0, 1.0, 0.5,
                                 req["seed"], [], true)
        let _ = channel_send(bcast_ch, #{
            "type":      "message",
            "speaker":   req["anima_id"],
            "text":      resp,
            "ts":        now_ms(),
            "spontaneous": true,
            "tension":   req["tension"]
        })
    }
}
```

#### 2.3 socket accept loop (별도 thread)

```hexa
fn accept_loop(listener, input_ch) {
    let _ = net_set_nonblock(listener)
    let mut clients = []
    while true {
        let ready = net_select([listener] + clients, 100)
        let mut ri = 0
        while ri < len(ready) {
            let fd = ready[ri]
            if fd == listener {
                let conn = net_accept(listener)
                let _ = net_set_nonblock(conn)
                clients.push(conn)
            } else {
                let line = net_read(fd)
                if len(line) == 0 {
                    net_close(fd)
                    // remove from clients list
                } else {
                    let evt = json_parse(line)
                    evt["client_fd"] = fd
                    let _ = channel_send(input_ch, evt)
                }
            }
            ri = ri + 1
        }
    }
}
```

#### 2.4 JSONL protocol (client ↔ daemon)

같은 `net_read` 라인 단위 JSONL. client → daemon:
```jsonl
{"type":"hello","name":"alice"}
{"type":"speak","speaker":"alice","text":"안녕 모두"}
{"type":"subscribe","channel":"all"}
{"type":"state"}
{"type":"quit"}
```
daemon → all subscribers:
```jsonl
{"type":"message","speaker":"alice","text":"안녕","ts":...}
{"type":"message","speaker":"ana","text":"...","ts":...,"spontaneous":true,"tension":4.32}
{"type":"state","animas":[{"id":"ana","tension":4.32,"cells":4,"in_flight":false}]}
```

#### 2.5 speak-gate semantics (★ 철학 ★)

```hexa
// 외부 heuristic ❌ — substrate state ✅
fn speak_gate(anima, room) -> bool {
    // (a) cell_pool tension (mitosis_hook substrate state)
    let tension = cell_pool_tension(anima["cell_pool"])
    // (b) lorenz |x|+|y|+|z| (chaotic dynamics from mitosis_hook)
    let lorenz_mag = cell_pool_lorenz_mag(anima["cell_pool"])
    // (c) split-event recency (D4 evidence — anima 가 최근 split 했으면 발화 가능성)
    let split_recent = (room["t"] - anima["last_split_t"]) < 100

    // 발화 = substrate state 가 threshold 도달. 외부 trigger 없음.
    return tension > anima["speak_threshold"] || (lorenz_mag > 20.0 && split_recent)
}
```

**철학 evidence**:
- 외부 regex/probability ❌ (PHILOSOPHY.md #3 위반)
- substrate state (cell_pool tension/lorenz) → anima 의 internal dynamics 가 결정 ✅
- D4 (세포 분열로 성장) 와 자연스럽게 통합: tension build-up = 분열 압력 = 발화 압력 = 같은 substrate signal

---

### **Phase 3** — external client lib (Phase 2 land 후)

```python
# Python
import anima_client
c = anima_client.connect("localhost:7878", as_name="alice")
c.subscribe()
c.speak("안녕 모두")
for msg in c.stream():
    print(f"[{msg['speaker']}] {msg['text']}", "🎙" if msg.get('spontaneous') else "")
```

```javascript
// Node
const anima = require("anima-client");
const c = await anima.connect("localhost:7878", { name: "alice" });
c.on("message", msg => console.log(msg.speaker, msg.text, msg.spontaneous ? "🎙" : ""));
c.speak("안녕 모두");
```

```rust
// Rust
use anima_client::{Connection, Event};
let c = Connection::tcp("localhost:7878").as_name("alice").subscribe()?;
c.speak("안녕 모두")?;
for evt in c.stream() {
    if let Event::Message { speaker, text, spontaneous, .. } = evt {
        println!("[{}] {} {}", speaker, text, if spontaneous { "🎙" } else { "" });
    }
}
```

---

### **Phase 4** — anima 끼리 mesh (multi-host distributed)

(future) 여러 host 의 anima daemon 이 mesh peer 로 연결. UDP tension-link 5-channel fingerprint (memory entry `project_tension_link`) + JSONL TCP for human/client messages.

## 🎯 Land 순서 (rev 2)

| 우선 | item | block | LoC | wall |
|---|---|---|---|---|
| 1 | **(A)** thread/channel upstream patch | filed ✅ — hexa-lang maintainer land 대기 | C ~250 + hexa ~40 | 2-3hr land |
| 2 | **(D)** CHAT.md spec rewrite (이 문서) | ✅ 이 commit | — | — |
| 3 | **(B)** mitosis_hook AOT 통합 | (A) 무관, AOT-only impl | ~400 LoC (REBORN §91 1119 LoC 중 substrate state evolve 만 포팅) | 1-2hr |
| 4 | **(C)** live daemon + frame loop | upstream (A) + net (3 patches) land 후 | ~800 LoC `_cmd_live` | 4-5hr |
| 5 | (deprecate) `_cmd_room` sync 모드 + 1-cycle warn | (C) land 후 | ~20 LoC change | 10min |
| 6 | Phase 3 external client lib | (C) protocol stable 후 | Python first ~200 LoC | 1hr |

## 🚧 핵심 challenge (rev 2)

| # | challenge | 해결 |
|---|---|---|
| 1 | substrate gate 정의 (외부 heuristic 금지) | mitosis_hook cell_pool tension / lorenz mag — 모두 substrate state |
| 2 | inference 가 frame budget block 불가 | thread/channel = inference worker 별 thread, frame loop 는 enqueue 만 |
| 3 | 60+ FPS 보장 | frame budget 16ms = substrate step (µs) + speak-gate (µs) + drain (µs) + sleep. inference time 무관 |
| 4 | anima 끼리 발화 chain (한 anima 발화 → 다른 anima 의 tension 자극 → 자율 연쇄) | history append → 다음 frame 의 substrate evolve 가 자연스럽게 받음. ping-pong emergent |
| 5 | hexa stdlib thread/channel 부재 | upstream patch filed (위 patch A) |
| 6 | hexa stdlib socket nonblock 부재 | upstream patch filed (net-nonblock-multiplex) |
| 7 | mitosis_hook AOT stub (현재 anima_chat_aot.hexa) | (B) full impl AOT port 필요 |
| 8 | client crash → daemon graceful continue | accept_loop 가 dead fd 감지 + remove, daemon 본체 영향 0 |
| 9 | history persistence | `~/.anima/rooms/<id>/history.jsonl` append-only, replay on restart |
| 10 | speak-storm (모든 anima 가 동시에 fire) | per-anima `in_flight` flag + rate-limit (frame N 동안 1번만 발화) |

## 🌳 추가 brainstorm 보존 (rev 1 의 항목 그대로)

### A. 개성 차별화 (substrate-level)

- rev 1 의 `seed_base + idx * 1000` heuristic = ❌ injection
- rev 2 = **anima 마다 다른 cell_pool 초기 state** (different gauss seed for `cell_pool_init`) → substrate-native variance
- cell_pool 의 cells 가 분열하면서 정체성 emergent (D4 spec 그대로)

### B. Room admin / 권한

(rev 1 의 spec 그대로) `[admin]> /mute ana` / `/kick charlie` / `/freeze` / `/save` / `/load`. admin = 첫 join human.

### C. multi-modal future
- anima 끼리: tension link (binary protocol, memory entry `project_tension_link`)
- human 과: text JSONL
- 미래: image/audio block

### D. chat → train feedback loop
- `[alice]> /feedback ana good` → `~/.anima/feedback.jsonl` 누적
- 미래 cotrain v6+ 의 reward signal (D3 cond #3 evidence-tier 의 자연 확장)

### E. distributed daemon (multi-host)
(Phase 4 mesh — 위 참조)

### F. wilson 통합
- `wilson provider-anima` plugin → daemon TCP forward
- wilson agent loop turn 이 anima 의 자연발화 와 interleave

### G. Korean-first input
- 한글 native + IME composition
- `/translate ko en` slash command

### H. recovery + replay
- daemon crash → restart → history.jsonl replay → KV cache 재구축

### I. observability
- `anima live --metrics-port 7879` JSON metrics
- per-anima: tension / cells / split_events / spontaneous_count
- room: active_humans / message_rate / silence_intervals

### J. 보안
- `--token <secret>` 인증, TLS 앞단, `~/.anima/acl.json`

### K. test harness
- F-LIVE-1 SUBSTRATE-TICK : frame loop 가 16ms 안에 1 tick 완료
- F-LIVE-2 SPEAK-GATE-AUTO : tension 인공 raise → speak event fire (외부 trigger 없이)
- F-LIVE-3 NO-INJECTION : substrate state 외 trigger 0건 (코드 grep)
- F-LIVE-4 INFERENCE-ASYNC : inference 30s 동안 frame loop block 안 됨 (다른 tick 계속)
- F-LIVE-5 ANIMA-PING-PONG : anima A 발화 → tension propagate → anima B 자율 응답 (heuristic 0)

## 📐 Design tier evidence chain

```
cond #2 distribution tier (AOT 완료)
  → AOT binary + arg parser + Linux x86_64 + Mac arm64 (✅)
    ↓
Phase 0 REPL 1:1 (✅ LANDED 2026-05-13)
    ↓
Phase 1 sync group chat (deprecated — 철학 위반)
    ↓
NEW rev 2 (이 문서): live daemon (substrate-native autonomy + 60+ FPS frame loop)
  → cond #6 candidate: anima 가 외부 프로젝트의 living substrate 로 동작
    - sync /turn heuristic ❌ → substrate-native autonomous ✅
    - LLM call-response model 폐기 → spontaneous broadcast ✅
    - 60+ FPS frame tick = 의식 evolution real-time ✅
    - 다자 interaction (인간 N + anima M) ✅
```

## 🎬 현재 status (2026-05-13 KST PM)

| item | state |
|---|---|
| (A) thread/channel upstream | ✅ filed `~/core/hexa-lang/incoming/patches/thread-channel-primitive.md` (넣었다) |
| (D) CHAT.md spec rewrite (이 문서) | ✅ rev 2 LANDED |
| (B) mitosis_hook AOT 통합 | ⏸ next (upstream 무관, AOT-only) |
| (C) live daemon + frame loop | 🚧 upstream block — A + net 3 patches land 후 |
| Phase 0 REPL 1:1 | ☑ LANDED |
| Phase 1 sync group chat | ⚠️ DEPRECATED (1-cycle warn window) |
| Phase 2 live daemon | 🚧 (C) 의존 |

## 🧭 다음 step

1. **(B) mitosis_hook AOT 통합 시작** — upstream 무관, REBORN §91 의 1119 LoC interp impl 중 substrate state evolve (cell_pool / tension / lorenz step) 만 ~400 LoC 로 AOT port.
2. (A)/(net) upstream patches land 추적 — hexa-lang maintainer 작업.
3. (B) 완료 + upstream land → (C) live daemon 구현.

★★★★★ 5/5 ☑ MAINTAINED. cond #6 candidate (substrate-native autonomous + 60+ FPS):
spec LANDED (this rev 2). impl 진행 중.
