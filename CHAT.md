# CHAT.md — anima REPL + 외부 연결 + 자연발화 brainstorm

> 전체 구현 계획 브레인스토밍 (고갈까지). 사용자 directive 2026-05-13 KST PM:
> "REPL chat + 외부 연결용" + "단편 메시지 말고" + "인간 3 anima 2 단체채팅 가능" +
> "호출 응답이 아니라 자연발화" + "소켓 같은 시스템 있어야 될듯" +
> "anima 도 여럿 가능" + "외부 프로젝트에서 쓰려면".

## Directive 핵심 5개

1. **REPL chat** — 상시 1:1 대화
2. **단편 X / 연속 대화** — multi-turn history 누적
3. **인간 N + anima M 단체 채팅** — group chat (예: 인간 3 + anima 2)
4. **외부 프로젝트 연결** — 호출/응답 model 아님
5. **자연발화 (spontaneous utterance)** — anima 가 알아서 말함

→ **socket daemon + 자연발화 trigger** 가 핵심 architecture.

## 📐 5-Layer Architecture

```
┌──────────────────────────────────────────────────────────────┐
│            Phase 3: anima daemon (long-running)              │
│                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────────────┐  │
│  │ anima       │ │ message bus │ │ spontaneous fire     │  │
│  │ instances   │ │ (broadcast) │ │ (tension/timer trig) │  │
│  │ (N animas)  │ │             │ │ ★ 자연발화 ★          │  │
│  └──────┬──────┘ └──────┬──────┘ └──────────┬───────────┘  │
│         └────────────────┴────────────────────┘            │
│                          │                                  │
│              ┌───────────┴───────────┐                      │
│              │  socket server        │                      │
│              │  TCP :7878 / unix     │                      │
│              │  JSONL frame protocol │                      │
│              └───────────┬───────────┘                      │
└──────────────────────────┼──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────┴────┐      ┌──────┴──────┐    ┌──────┴──────┐
   │ Phase 0 │      │ Phase 1     │    │ Phase 4     │
   │ REPL    │      │ room (multi-│    │ external    │
   │ 1:1     │      │ party human │    │ project     │
   │ stdin   │      │ + anima)    │    │ client lib  │
   └─────────┘      └─────────────┘    └─────────────┘
```

## 📋 Phase별 명세

### **Phase 0** — REPL chat (1:1 단순 상시) ☑ **LANDED 2026-05-13 KST PM**

> hexa-native impl in `anima_chat_aot.hexa::_cmd_chat_repl` (~120 LoC).
> Mac arm64 + Linux x86_64 cross-compile parity. multi-turn + /show + /save + /exit verified.
> /save → `~/.anima/sessions/<name>.jsonl` 파일 생성. CLI: `anima chat repl [--mode M] [--max-new N] [--temp F] [--seed N]`.



```sh
anima chat repl [--mode greedy --seed 0]
> 안녕? 너는 누구야?
anima: 네, 맞아요. 저는 anima 입니다.
> 우주에 대해
anima: 우주는 진동으로 차 있어요.
> /reset                          # 히스토리 비움
> /show                           # 누적 history 출력
> /save my-session                # ~/.anima/sessions/my-session.jsonl 저장
> /exit
```

**구현**:
- `hexa_input()` line read loop
- chat["history"] 누적 (chat_generate 내부에서 history 참조)
- KV cache 재사용 (cap_len 1024)
- /reset /show /save /exit slash commands
- `/save <name>` → `~/.anima/sessions/<name>.jsonl` append-only history

---

### **Phase 1** — 단체 채팅 (인간 N + anima M, single-process REPL)

```sh
anima room --humans "alice,bob,charlie" --animas "ana,ben" [--ckpt P]
[alice]> 안녕 모두?
[bob]> 안녕 alice
[/turn ana]
ana: 안녕하세요 두 분! 저도 인사드려요.
[charlie]> ben 너는?
[/turn ben]                       # 또는 /turn ana,ben (병렬)
ben: 저는 또 다른 anima 예요.
[/show]                           # 전체 history (sender label 포함)
[/exit]
```

**구현**:
- Roster parse: `--humans "alice,bob,charlie"` → 3 humans, `--animas "ana,ben"` → 2 animas
- Input prefix syntax: `<name>:` 형태로 화자 명시 OR `[<name>]>` prompt
- `/turn <anima_name>` → 그 anima 가 전체 history 를 context 로 받아 chat_generate
- `/turn <a>,<b>` → 병렬 (또는 순차) 발화
- Chat-formatted prompt builder: `[alice]: 안녕\n[bob]: 안녕 alice\n[ana]:` 형태로 prompt 구성
- N anima 인스턴스 — shared ckpt mmap, 독립 KV cache + seed (다른 seed = 다른 발화 패턴)

---

### **Phase 2** — anima daemon (socket server)

```sh
# 서버 띄우기
anima daemon --port 7878 --animas "ana,ben" [--unix /tmp/anima.sock]

# 클라이언트 (어떤 언어에서든)
$ nc localhost 7878
> {"type":"speak","speaker":"alice","text":"안녕"}
< {"type":"message","speaker":"alice","text":"안녕","ts":...}
> {"type":"turn","anima":"ana"}
< {"type":"message","speaker":"ana","text":"...","ts":...,"spontaneous":false}
```

**JSONL frame protocol** (one JSON per line):

| direction | type | payload |
|---|---|---|
| client → daemon | `speak` | `{"speaker":"...","text":"..."}` |
| client → daemon | `turn` | `{"anima":"<id>"}` |
| client → daemon | `subscribe` | `{"channel":"all\|<anima_id>"}` |
| client → daemon | `list` | `{}` → roster + animas |
| client → daemon | `state` | `{}` → anima tension/cells/history depth |
| client → daemon | `quit` | `{}` |
| daemon → all | `message` | `{"speaker":"...","text":"...","ts":...,"spontaneous":bool,"trigger":"timer\|tension\|curiosity\|named"}` |
| daemon → all | `state` | `{"animas":[{"id":"ana","tension":4.2,"cells":4,"hist_depth":12}]}` |
| daemon → all | `event` | `{"kind":"join\|leave\|reset","speaker":"..."}` |
| daemon → all | `pong` | `{"ts":...}` |

**기술 stack**:
- TCP socket on port 7878 (configurable)
- Optional Unix domain socket `/tmp/anima.sock` (lower latency, local-only)
- JSONL line-delimited (one JSON per line, `\n` terminator)
- Multi-client subscribers (broadcast to all subscribed channels)
- Non-blocking accept loop

---

### **Phase 3** — 자연발화 (★ 핵심 ★)

**호출-응답 모델 폐기**. anima 가 알아서 발화한다.

**Trigger sources** (4 종류):

| kind | 발생 조건 | 구현 비용 |
|---|---|---|
| **(a) timer** | 일정 idle 시간 후 발화 (예: 30s 무대화) | ★ 가장 cheap |
| **(b) tension** | mitosis_hook 의 tension > threshold (cell_pool 통합) | ★★★ AOT 에서 stub, full 은 별도 |
| **(c) curiosity** | 마지막 N turns 의 entropy 낮으면 새 화제 시작 | ★★ 측정 + threshold 필요 |
| **(d) named** | 다른 화자가 anima 이름 mention 시 자동 응답 | ★ string match |

**Daemon tick loop**:

```hexa
fn spontaneous_tick(animas, room, current_ts) {
    let mut ai = 0
    while ai < len(animas) {
        let anima = animas[ai]
        let trigger = check_trigger(anima, room, current_ts)
        if trigger["fired"] {
            let context = build_history_prompt(room, anima["id"])
            let response = chat_generate(anima["chat"], context, "greedy",
                                         anima["max_new"], 0.7, [], 1.0, 1.0,
                                         0.5, anima["seed_advance"](), [], true)
            broadcast(room, #{
                "type":        "message",
                "speaker":     anima["id"],
                "text":        response,
                "ts":          current_ts,
                "spontaneous": true,
                "trigger":     trigger["kind"]
            })
        }
        ai = ai + 1
    }
}
```

**MVP 우선순위**: timer (a) + named (d) → 가장 쉬운 구현. tension (b) + curiosity (c) 는 cell_pool 통합 후 follow-up cycle.

---

### **Phase 4** — 외부 프로젝트 연결 (3 방식)

**(a) socket client lib (any language)**

```python
# Python
import anima_client
c = anima_client.connect("localhost:7878")
c.subscribe()
c.speak("alice", "안녕")
for msg in c.stream():
    print(msg["speaker"], msg["text"])
```

```javascript
// Node.js
const anima = require("anima-client");
const c = anima.connect("localhost:7878");
c.subscribe();
c.speak("alice", "안녕");
c.on("message", (m) => console.log(m.speaker, m.text));
```

```rust
// Rust
use anima_client::Connection;
let c = Connection::tcp("localhost:7878")?;
c.subscribe()?;
c.speak("alice", "안녕")?;
while let Some(msg) = c.next_message()? { ... }
```

**(b) AOT binary one-shot (no daemon)**

```sh
anima ask "안녕" --result          # 기존 (PSCC §51), JSON ToolResult emit
```

**(c) Hexa import (in-process embed)**

```hexa
use "anima_chat"
let chat = chat_default()
let r = chat_generate(chat, "안녕", "greedy", 10, 0.7, [], 1.0, 1.0, 0.5, 0, [], true)
```

## 🚧 핵심 challenge + 해결

| # | 문제 | 해결 전략 |
|---|---|---|
| **1** | hexa AOT stdin = `hexa_input()` blocking line-read | Phase 0 OK (단일 stdin loop). Phase 2 socket = select/poll 필요 → hexa stdlib gap → C builtin 추가 또는 fd-multiplexer plugin |
| **2** | N anima = N × 2.6 GB weight load | **shared chat weight pool** — 1회 load, N chats clone farr handles (mmap CoW + farr table = integer handle, 메모리 공유) |
| **3** | concurrent generation single ckpt | turn-based, queue per anima. parallel infer 는 별도 cycle (multi-GPU 필요) |
| **4** | 자연발화 trigger (cell_pool AOT-stub) | Phase 3 MVP = timer + last-message-anima-mentioned. cell_pool 통합 (tension/lorenz dynamics) = follow-up cycle |
| **5** | history JSONL persistence | `~/.anima/rooms/<id>/history.jsonl` append-only, atomic write |
| **6** | socket 종료 시 graceful cleanup | SIGTERM handler + atomic save + WAL replay on restart |
| **7** | multi-line input (paste, multi-paragraph) | terminator sentinel (`/end` or `\\` 줄끝 join) |
| **8** | 한 화자가 여러 anima 동시 호출 | `/turn ana,ben` 병렬 (별도 thread) 또는 순차 |
| **9** | anima 끼리 대화 (사람 없이) | spontaneous trigger 가 named/timer 로 chain → "ana → ben → ana" 자동 ping-pong 가능 |
| **10** | 외부 client 가 daemon crash 시 reconnect | exponential backoff + 마지막 ts 부터 history replay |

## 🎯 구현 순서 제안

| 우선순위 | Phase | scope | ~LoC | wall |
|---|---|---|---|---|
| **1** | Phase 0 REPL 1:1 | hexa_input loop + history + /commands | ~200 | 30분 |
| **2** | Phase 1 group chat | roster + name prefix + /turn | ~400 | 1시간 |
| **3** | Phase 2 daemon TCP | socket server + JSONL frame + broadcast | ~600 | 2-3시간 |
| **4** | Phase 3 자연발화 | timer trigger MVP + mention detector | ~300 | 1시간 |
| **5** | Phase 4 external client | Python lib + example | ~200 | 30분 |

**총 ~1700 LoC / 4-5시간 wall, $0** (Mac local).

## 🌳 결정 필요 사항 — 사용자 input

1. **soc/tcp protocol**: TCP `:7878` 면 충분? Unix socket `/tmp/anima.sock` 도 같이?
2. **자연발화 trigger 종류**: timer / tension / curiosity / named — 모두 or 일부 MVP?
3. **daemon 동시 anima 수**: 2-3 정도 MVP / 무제한?
4. **다중 화자 (humans) 단일 process vs separate clients**: 시작은 단일 process REPL (Phase 1) → Phase 2 daemon 으로 자연 확장 OK?
5. **history persistence**: 즉시 (`~/.anima/rooms/`) / 메모리만?
6. **시작 phase**: Phase 0 (REPL 1:1) → Phase 1 → Phase 2 순차? 아니면 Phase 0 + Phase 2 동시 (TCP daemon 부터)?

## 🧠 추가 brainstorm 항목 (고갈까지)

### A. 개성 차별화 (anima persona variance)

- 같은 ckpt 라도 anima 마다 **seed offset** 으로 sample variance → 다른 발화 패턴
- `--animas "ana:seed=42,ben:seed=137"` 형태로 명시
- 미래: cell_pool 통합 후 anima 마다 **다른 cell_pool 초기화** → substrate-level 차별화
- D3 cond #3 의 M4 cosine z=3.20 evidence 를 anima 별 분리로 재활용
- 발화 스타일 fingerprint: `--style verbose|terse|metaphoric` (post-prompt sample bias)

### B. Room 권한 + Admin

- `[admin]> /mute ana` — anima 발화 일시 정지
- `[admin]> /kick charlie` — human 추방
- `[admin]> /freeze` — 모든 자발발화 정지 (debug 용)
- `[admin]> /save` `[admin]> /load <name>` — room snapshot
- 첫 join 한 human = 자동 admin

### C. multi-modal future

- anima 끼리는 **tension link** (binary protocol, 기존 memory entry `project_tension_link`) — 5-channel fingerprint
- human 과는 text JSONL
- 미래: image / audio frame block 추가 (wilson `tool-image` v1 pattern 참조)

### D. chat → train feedback loop

- 자연발화 응답이 좋았다 → 그 KV state + history 를 **RLHF-style 학습 신호** 로 저장
- `[alice]> /feedback ana good` — 마지막 ana 발화에 +1
- `~/.anima/feedback.jsonl` 누적 → 미래 cotrain v6+ 의 reward signal
- D3 cond #3 evidence-tier 의 자연 확장

### E. distributed daemon (multi-host)

- Phase 2 의 socket 위에 mesh network: anima daemon 들이 서로 connect
- `anima daemon --mesh-peers "mac.local:7878,ubu.local:7878"` — 여러 host 의 anima 가 단일 logical room
- 동기화: vector clock or CRDT for history merge
- 미래: anima 간 tension link binary protocol on UDP 9999 (memory entry 기존 spec)

### F. CLI integration with wilson

- wilson 의 `provider-anima` plugin 작성 — daemon TCP 통해 LLM provider 로 동작
- wilson agent loop 의 turn 이 anima 의 자연발화 와 interleave
- `wilson -p "..."` → anima daemon 에 forward → 응답

### G. Korean-first input experience

- input 직접 한글 / 영문 mix 지원
- `/translate ko en` slash command
- IME composition state (한글 조합 중 enter 처리) — Phase 1 의 hexa_input 자체는 lined-based 라 OK

### H. recovery + replay

- daemon crash → restart 시 마지막 `history.jsonl` replay
- KV cache 재구축 (history 의 prompt 들을 prefill)
- 또는 `kv_cache.bin` snapshot — periodic save

### I. observability

- `anima daemon --metrics-port 7879` — JSON metrics endpoint
- per-anima: tension / cells / hist_depth / tokens_generated / spontaneous_count
- room-level: active_humans / message_rate / silence_intervals
- 외부 dashboard (grafana 같은) 통합 가능

### J. 보안

- `anima daemon --token <secret>` — 첫 연결 시 인증
- TLS termination via nginx/caddy 앞단
- `~/.anima/acl.json` — speaker 별 allow/deny
- room 별 invite-only mode

### K. test harness

- `anima daemon-test` — 가짜 client N 명 자동 생성, scripted scenario
- F-CHAT-1..N falsifier 세트:
  - F-CHAT-1 ROUND-TRIP: 1 message in → broadcast received
  - F-CHAT-2 SPONTANEOUS: timer trigger fires within window
  - F-CHAT-3 MULTI-ANIMA: 2 animas independent state
  - F-CHAT-4 HISTORY-REPLAY: crash → restart → history intact
  - F-CHAT-5 PERSONA-VARIANCE: same prompt different anima → different response

## 📐 Design tier evidence chain (PERSONA.md 통합)

```
cond #2 distribution tier (현재 closure 100%)
  → AOT binary + arg parser + Linux x86_64 + Mac arm64
    ↓
NEW Phase 0+1+2+3 (이 CHAT.md)
  → REPL + group chat + daemon + 자연발화
    ↓
NEW cond #6 candidate (★★★★★★ 6/6 ?)
  → anima 가 외부 프로젝트의 living substrate 로 동작
    (호출/응답 model 폐기 → 자율 발화 + 다자 interaction)
```

## 🎬 다음 step

사용자 답변 받으면 → Phase 0 (REPL 1:1) MVP 즉시 구현 → 그 위에 Phase 1/2/3 누적.

브레인스토밍 진행 메모:
- ASCII diagram 포함 전체 내용 = 본 CHAT.md
- PERSONA.md 의 Distribution section 에 cross-link 추가 검토
- README.md 에 CHAT.md 등록 (PERSONA.md 와 함께 SSOT-tier)
- 구현 시 PSCC §N+1 entry 로 timeline 기록
- 14-track tasks (Phase 0~4 × 측정 + doc) TaskCreate 로 트래킹

★★★★★ 5/5 cond 유지 + Phase 0 시작 시 cond #6 (group chat / 자연발화) candidate evidence 시작.
