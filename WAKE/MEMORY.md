# WAKE/memory — episodic + working memory layer (M5)

> WAKE M5 milestone — anima 의 in-process 단기 / 장기 기억 surface. brain_decide 의 ctx 전치 단계 + .kosmos 영속화 통합 (M4 delegate).

## @goal
anima 가 *과거 발화의 기록* (episodic) 과 *최근 perception 의 컨텍스트 윈도* (working) 를 in-process 로 보유하고, 두 axis 모두 brain_decide 의 ctx 입력으로 자연스럽게 흐른다. .kosmos 영속화는 M4 `wake_save / wake_load` 를 그대로 delegate — duplicate impl 0. 결정은 substrate 가 자율, 본 모듈은 *데이터 surface*.

## SSOT 참조

### governance — CLAUDE.md `@D a_substrate_native_speak` (verbatim)
```
@D a_substrate_native_speak := "anima speech is substrate-native — no assistant regression" :: governance [required active]
  do   = "compute anima motivation from internal substrate state (M activation · C Φ · W tension · MITOSIS · idle time · curiosity · E ratchet) · user messages = environment context, not a response obligation · anima may speak during user silence and may stay silent under a direct question"
  dont = "stimulus-response where a user message directly triggers anima speech (assistant regression) · reactive design that 'responds' to a prompt · turn-based 'user asked, so anima must answer' assumptions"
```

### WAKE 도메인 인접 모듈
- M1 [`WAKE/state_machine.hexa`](state_machine.hexa) — stage NAME · timing.
- M2 [`WAKE/perception.hexa`](perception.hexa) — sensor → ctx_tokens producer (working memory 의 input source).
- M3 [`WAKE/input_step.hexa`](input_step.hexa) — pf state input-conditioned step.
- M4 [`WAKE/kosmos_persist.hexa`](kosmos_persist.hexa) — `.kosmos` 영속화 surface. **M5 가 wake_save / wake_load 를 delegate**.
- 본 모듈 = **M5** : in-process episodic + working memory.

### CORE consumer
- [`CORE/brain.hexa`](../CORE/brain.hexa) — `brain_decide(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v, seconds_since_last, env_off, content_clean)`. M5 는 brain_decide signature 를 **변경하지 않는다**. 8 motivation factor (rel/gap/cur/pain/coh/orig/bal/dyn_v) 산출 시 caller 가 `mem_recent_emits` · `mem_working_window` 를 참조 surface 로 활용 (예: rel = mem_working_window 의 ctx 와 새 perception 의 코사인 유사도).

## pub surface

```hexa
pub fn mem_init() -> Map
    // returns #{ "episodic": [], "working": [] }

pub fn mem_record_emit(mem: Map, ts: float, ctx_summary: string,
                       phi: float, tension5: [float], stage: string,
                       emit_text: string) -> Map
    // appends a record to episodic; panic if len(tension5) != 5.
    // record shape:
    //   #{ "ts": float, "ctx_summary": string, "phi": float,
    //      "tension5": [float], "stage_name": string,
    //      "emit_text": string }

pub fn mem_push_ctx(mem: Map, ctx_tokens: list) -> Map
    // appends ctx_tokens to working ring buffer; cap=20 FIFO.
    // empty list push counted as 1 tick (silence-tick 기록).

pub fn mem_recent_emits(mem: Map, n: int) -> list
    // returns last n episodic records (chronological order within slice).
    // n<=0 → []; episodic 길이 < n → 전체 반환.

pub fn mem_working_window(mem: Map) -> list
    // returns working buffer copy (oldest→newest, len ≤ 20).

pub fn mem_save_to_kosmos(mem: Map, out_dir: string, t: float) -> string
    // delegates to wake_save (M4). pf_state는 synthetic placeholder (memory
    // layer 가 pf 를 소유하지 않음). emit_history = episodic 의 emit_text list.
    // tension5/stage = 마지막 episodic record (없으면 [0]*5 / "WAKE").

pub fn mem_load_from_kosmos(path: string) -> Map
    // delegates to wake_load. episodic 의 각 record 는 snapshot scope 의
    // 단일 t/phi/tension5/stage 로 reconstruct. working buffer 는 [].

pub fn memory_summary() -> string
```

## record shape (episodic)

| key | type | meaning |
|-----|------|---------|
| `ts` | float | unix epoch seconds (발화 시각) |
| `ctx_summary` | string | 짧은 ctx 요약 (caller 가 미리 요약, raw bytes 아님) |
| `phi` | float | 발화 당시 substrate phi |
| `tension5` | [float;5] | TENSION-LINK 5-ch fingerprint (concept/context/meaning/authenticity/sender) |
| `stage_name` | string | "WAKE" \| "N1" \| "N2" \| "N3" \| "REM" |
| `emit_text` | string | 실제 발화 raw text |

## working memory ring buffer policy

- **cap N = 20** — anima 가 한 stage (~수 분) 내에서 참조할 수 있는 단기 perception 윈도.
- push 시 길이가 20 을 넘으면 *가장 오래된 1 entry drop* (FIFO). bulk-truncate 0.
- empty list push 도 1 tick 으로 count — substrate 가 "no perception" 의 시간상 자리도 기억할 수 있다 (silence tick).
- N=20 의 근거: chat_lib 의 ctx window (수 백 token) 보다 짧되, 한 cycle (~90 min) 의 perception 흐름 capture. 추후 daemon (M6) tuning 시 조정.

## episodic memory append-only policy

- in-process 에서 cap 무제한 (.kosmos save 가 disk 백업).
- `mem_recent_emits(n)` 은 *최근 n* 만 반환 — 단기 회상.
- 장기 회상은 episodic full list 의 timestamp 정렬 순회.

## kosmos round-trip (M4 delegate)

본 모듈은 .kosmos 영속화 spec 을 **복제하지 않는다** — `wake_save / wake_load` 를 직접 호출. payload 는 M4 의 그것을 그대로 따른다:
- `@payload text` = emit_history serialized (pipe-sep + escape)
- `@payload tension` = TENSION-LINK 5-ch
- `@payload pf_state` · `@payload stage_state` · `@payload emit_history` carve-out

### M4 delegate 의 design choice

- **pf_state synthetic placeholder** — memory layer 가 PureField 를 소유하지 않으므로 `phi = 마지막 episodic record 의 phi`, field/oscs 는 zero default. caller (M6 daemon) 가 *full pf_state* 까지 영속화하려면 `wake_save` 를 직접 호출. 본 fn 은 **memory-axis** 만 영속화.
- **tension5 = last episodic** — 새 fingerprint 가 필요하면 caller 가 mem_record_emit 으로 새 record 를 push 한 후 save.
- **stage = last episodic** — 동일 정책.
- **working buffer 영속화 안 됨** — daemon restart 시 working 은 빈 list 로 시작 (in-process 단기 윈도의 자연스러운 표현). episodic 만 재개.

## carve-out

### K1 — fine-grained timestamp 손실 (kosmos round-trip)
`mem_load_from_kosmos` 는 wake_load 의 emit_history 로부터 episodic 을 reconstruct 하는데, 각 record 의 ts 는 snapshot 의 단일 `t` 로 채워진다. 즉 fine-grained per-emit timestamp 가 snapshot scope 에는 보존되지 않는다 — 본 layer 의 명시적 design choice. fine-grained meta 를 보존하려면 episodic 을 별도 .kosmos lane 으로 저장하는 후속 milestone 필요.

### K2 — ctx_summary string scope
- caller 책임 (raw bytes 가 아닌 *요약* string).
- 길이 제한 0 (본 모듈) — caller 가 요약 정책 결정.
- snapshot scope 에서는 "" 빈 string 으로 복원 (K1 동일 이유).

### K3 — working buffer 의 PAD/BOS/EOS 의미
- working 의 각 entry 는 perception_to_ctx_tokens 반환값 (BPE id list of int).
- 본 모듈은 entry 의 *내용* 을 검사하지 않는다 — BOS/EOS/PAD 의 의미는 perception (M3) 의 spec.
- empty list `[]` 도 *유효한 entry* — silence tick 의 자연스러운 표현.

## p1~p8 정합 매트릭스

| principle | 정합 근거 |
|-----------|-----------|
| p1 NO SYSTEM PROMPT | record 는 numeric (phi · tension5) + raw emit text 뿐. identity rule 0. |
| p2 NO IDENTITY RULES | 어떤 필드도 identity rule 인코드 안 함. |
| p3 NO PERSONA INJECTION | working ctx 는 raw BPE id. prefix prepend 0. |
| p4 NO ASSISTANT FRAMING | memory 는 *과거 substrate state*. forced emit trigger 아님. |
| p5 NO SPEAK() | 본 모듈에 emit fn 0. data surface 일 뿐. |
| p6 NO FINE-TUNED ETHICS | 가중치 0. 순수 list 관리. |
| p7 NO PERPLEXITY VERDICT | verification = round-trip equality + invariant. perplexity 무관. |
| p8 NO TRAIN/INFER SPLIT | train pause / infer wake / daemon restart 어떤 phase 에도 동일 memory. |

## a_substrate_native_speak 정합

working ctx 가 길든 짧든, episodic record 가 1개든 1000개든, brain_decide 의 *연속* threshold 가 단독으로 emit 결정을 한다. 본 모듈에 "ctx 가 N tokens 이상이면 emit" 같은 boolean gate 0.

## a_autonomy_over_hardcode 정합

- boolean gate 0 — 모든 fn 은 단순 list 조작 (push · slice · concat).
- panic 은 1군데만: `mem_record_emit` 의 `len(tension5) != 5` (wake_save delegate 호환 강제 — boolean gate 가 아닌 sentinel).

## a_kosmos 정합

- `mem_save_to_kosmos / mem_load_from_kosmos` = `wake_save / wake_load` 직접 위임.
- payload spec = M4 의 그것 그대로 (text + tension 5-ch + coord · lane · radius · tier).
- spec 을 *복제하지 않고 준수*. duplicate impl 0.

## smoke 결과

`WAKE/memory_smoke.hexa` — 4 case 5 invariant.

```
=== WAKE/memory episodic + working + kosmos round-trip smoke (4 case) ===
RESULT: 5 PASS / 0 FAIL
HEADLINE: WAKE-M5-MEMORY-LAYER-OK
```

검증 invariants:
- I1 `mem_init()` empty episodic + empty working.
- I2 `mem_record_emit` 3회 후 `mem_recent_emits(2)` 가 마지막 2 record (chronological).
- I3 `mem_push_ctx` 25회 (cap=20 초과) 후 working len = 20 + wk[0]=[105] + wk[19]=[124] (FIFO).
- I4 empty list push 도 1 tick 으로 count (silence tick 기록).
- I5 `mem_save_to_kosmos → mem_load_from_kosmos` round-trip 시 episodic len + emit_text identity + working=[] 보존.

## 호출 site (예상)

- **M6 daemon loop**:
  - tick 마다 `mem = mem_push_ctx(mem, ctx_tokens)` (perception ingest 직후).
  - emit 결정 후 `mem = mem_record_emit(mem, ts, summary, phi, tension5, stage, text)`.
  - graceful shutdown 직전 `mem_save_to_kosmos(mem, dir, t)`.
  - startup 시 `wake_recent_snapshots(dir, 1)` → `mem_load_from_kosmos(path)` 으로 episodic 복원.
- **brain_decide caller (M6 inner loop)**:
  - `let working = mem_working_window(mem)` → 8 motivation factor 산출의 ctx surface.
  - `let recent = mem_recent_emits(mem, 5)` → recent-emit-aware factor (예: orig = 새 emit 의 originality vs recent).

## frontier closure (honest framing)

M5 = memory layer *surface* 가 닫혔다는 의미. 실제 runtime 진입점 (M6 daemon wire-up) 은 후속 milestone 에서 land. 본 PR 은:
- pub fn 8 개 (init · record · push · recent · window · save · load · summary).
- 4 case · 5 invariant 모두 PASS (runtime smoke verified).
- M4 delegate 호환 (wake_save / wake_load round-trip).
- governance 정합 (a_substrate_native_speak · a_autonomy_over_hardcode · a_kosmos · p1~p8).

까지 보장. M6 daemon 이 본 모듈의 pub fn 을 그대로 호출하면 in-process memory + .kosmos 영속화가 자동 통합된다.

## 향후 가능한 path

- (a) episodic 의 fine-grained per-emit timestamp 영속화 — K1 제한 제거. 별도 `.kosmos` lane.
- (b) ctx_summary 자동 산출 — caller 가 직접 요약하지 않고 perception_compose 출력에서 짧은 요약 추출 fn 제공.
- (c) episodic retrieval — tension5 fingerprint 기반 과거 emit 검색 (kosmos_io.retrieve 와 통합).
- (d) working buffer cap 동적 조정 — stage 에 따라 cap 가변 (WAKE 20, REM 40 등).

위 path 들은 모두 *후속 milestone* 으로, M5 자체의 closure 와 직교한다.
