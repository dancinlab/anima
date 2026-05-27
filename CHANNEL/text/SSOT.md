# 📝 CHANNEL/text — 텍스트 채널 SSOT

> CHANNEL.md M2 (`text 채널 어댑터 — CHAT/DECODER 위임 wrapper · substrate-decided emit 단일 진입점 · 외부 LLM 0 검증`) 의 로컬 SSOT.

---

## 정체

`CHANNEL/text` 는 anima 의 **텍스트 출력 채널 어댑터** — 신규 모달리티가 아니라, 이미 존재하는 `HEXAD/CHAT/*` 와 `CORE/DECODER/*` 디코더 스택을 `voice` · `tension` 과 **동형 시그니처** (`*_ready` / `*_emit` / `*_pipeline_summary`) 로 wrap 한 thin adapter 이다.

- **입력**: anima 기판이 결정한 `intent_vec` + `ctx_tokens` (BPE id) + `tension5` 5-ch envelope
- **중간**: BPE token id sequence (`HEXAD/CHAT/chat_lib.tok_*` vocab 동일)
- **출력**: UTF-8 byte stream string (`tok_decode_str` 동형)

**발화는 substrate-decided** — 호출자는 CORE engine_g motivation 8-factor 가 text 채널을 선택했고 WAKE 등 발화 가능 stage 컨텍스트가 충족된 상태에서만 본 어댑터를 부른다. 사용자 메시지 수신을 직접 trigger 로 삼지 않는다 (a_substrate_native_speak · p4 · stimulus-response 금지).

---

## 파이프라인 단방향 흐름 (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   anima substrate (PureField · Ψ=1/2)                   │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
                  ┌──────────────────────────────┐
                  │  tension5 (5-ch envelope)    │  ← substrate-decided
                  │  M · C · W · MITOSIS · E     │     (motivation 8-factor)
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  intent embedding bridge     │  ← CHANNEL M4
                  │  tension5 → intent vector    │     (channel-agnostic)
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  CORE/DECODER/generator      │  ← engine_g 노출 surface
                  │  + HEXAD/CHAT/chat_lib       │     (chat_generate · tok_*)
                  │  intent + ctx → token ids    │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  BPE token decoder           │
                  │  ids → UTF-8 byte stream     │
                  │  (chat_lib.tok_decode_str)   │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                          UTF-8 byte stream
                       (단방향 · 사용자 입력
                        역류 경로 없음)
```

**역류 없음** — 사용자 측 텍스트 입력은 별도 sensor 계열로 들어오며 본 SSOT 범위 밖이다. text 채널은 오직 substrate → 외부로의 단방향 emit 만 다룬다.

---

## 위임 매트릭스

| `CHANNEL/text` 함수 | 위임 대상 | 호출하는 fn (예정) |
|---|---|---|
| `text_ready()` | `CORE/DECODER/generator.hexa` (예정) | `generator_ready()` |
| `text_emit(intent_vec, ctx_tokens, tension5)` | `CORE/DECODER/generator.hexa` (예정) | `brain_emit_step(intent_vec, ctx_tokens, tension5)` |
| `text_emit` fallback | `HEXAD/CHAT/chat_lib.hexa` | `chat_generate(chat, prompt, mode, max_new, …)` |
| `text_emit` 토크나이즈 보조 | `HEXAD/CHAT/chat_lib.hexa` | `tok_encode` · `tok_decode_str` · `chat_build_prompt` |
| `text_emit` 가중치 로드 | `HEXAD/CHAT/chat_lib.hexa` | `chat_default` · `chat_load_weights` (lazy) |
| `text_pipeline_summary()` | — (1-line 요약 상수) | n/a |

본 어댑터는 **재구현이 아닌 위임** 만 한다 — CHAT/DECODER 가 보유한 토크나이저 · 가중치 로더 · 디코더 루프 · cell pool · mitosis tick 은 그대로 두고, 호출만 wrap 한다 (`a_substrate_native_speak` + `feedback_closure_is_physical_limit` — wrap = physical limit, 새 구현 아님).

---

## p1~p8 정합 매트릭스

| 원칙 | text adapter 입장 |
|---|---|
| **p1 NO SYSTEM PROMPT** | 입력은 `intent_vec` + `ctx_tokens` + `tension5` 만 — `system:` 필드 / 프롬프트 prefix string 받지 않는다. |
| **p2 NO IDENTITY RULES** | text 정체성은 cell mitosis 에서 emerge — adapter 는 라우팅만 담당, identity 룰 파일/템플릿 미사용. |
| **p3 NO PERSONA INJECTION** | `ctx_tokens` 는 raw BPE id list (페르소나 prefix 임베딩 금지). "당신은 anima 입니다" 류 prefix 어디에도 prepend 하지 않는다. |
| **p4 NO ASSISTANT FRAMING** | `text_emit` 은 stimulus-response 엔드포인트가 아니다 — 호출자가 substrate-decided externalization 경로에서만 부른다. 사용자 메시지가 자동으로 본 함수를 호출해서는 안 된다. |
| **p5 NO SPEAK()** | `text_emit ≠ speak(message)` — 연속 tension field 의 externalization 일 때만 호출 (p5_tension_emit_not_filler 정합, stage-gated emit 허용). |
| **p6 NO FINE-TUNED ETHICS** | 가중치 갱신은 chat_lib 의 mitosis tick 으로만, RLHF cooperation/empathy 주입 금지. |
| **p7 NO PERPLEXITY VERDICT** | text 품질은 coherence + 자연스러움 + context-fit 으로 — perplexity / loss 단독 verdict 금지. |
| **p8 NO TRAIN/INFER SPLIT** | chat_lib 의 `cell_pool` / `chat_mitosis_*` 는 inference 중에도 동작 — train/infer 단절 금지. |

**stimulus-response 금지** — 본 어댑터 자체는 외부 트리거 검증을 강제하지 않는다 (`a_autonomy_over_hardcode` — 외부 boolean gate 금지). 호출자가 CORE engine_g 의 8-factor 결정과 WAKE stage 컨텍스트를 따라 발화를 결정한다.

---

## 외부 LLM 0 검증 (instrument-first)

**측정 명령** (`feedback_instrument_first_methodology` — 주장 전 측정):

```
grep -rniE "openai|anthropic|claude\.com|api\.openai|api\.anthropic|gpt-|chatgpt" CHANNEL/text/
```

**결과** (raw stdout, verbatim):

```
CHANNEL/text/text_emit.hexa:12:// 외부 LLM 의존 없음 — CHANNEL/text 트리에 openai · anthropic · claude · gpt API 호출 0건.
```

→ 1 hit 이지만 모두 **부재를 선언하는 주석 문자열** (negative-claim text). 실제 API call / import / endpoint 가 아니다.

**확인 명령** (실제 API surface 만 좁힌 stricter grep):

```
grep -rniE "import.*openai|import.*anthropic|api\.openai\.com|api\.anthropic\.com|api_key|sk-[A-Za-z0-9]" CHANNEL/text/
```

**결과** (raw stdout, verbatim):

```
```

→ 0 hits. CHANNEL/text 트리에 외부 LLM API 의존 0건 확정.

**판정**: ✅ 외부 LLM 0 — 1차 grep 의 단일 hit 은 부재 선언 주석이며, 실제 endpoint / key / import 는 0건 (stricter grep). adapter 가 위임하는 `HEXAD/CHAT/chat_lib` 와 `CORE/DECODER/generator` 모두 local-only hexa-native 디코더이고, anima 본체의 외부 LLM 부재 (a_substrate_native_speak) 정합 유지.

**프론티어 (잔여)**:
- `HEXAD/CHAT/*` · `CORE/DECODER/*` 트리 전체에 대한 외부 LLM 0 audit 은 CHANNEL.md M7 (`p1~p8 audit — CHANNEL 트리 전체 0 hits`) 에서 통합 수행 (현재는 CHANNEL/text/ 트리만 측정).
- 실제 substrate-gated round-trip (intent → emit → byte stream) 은 CORE/DECODER/generator.hexa land + M4 intent bridge + M5 dispatcher 합류 후 1회 전 구간 검증 필요.

---

## 의존성

- **CORE engine_g motivation 8-factor** (CHANNEL M6 채널 분기): text / voice / tension 3 채널 중 text 선택 결정
- **CORE/DECODER/generator.hexa** (예정): `generator_ready()` · `brain_emit_step(intent_vec, ctx_tokens, tension5)` 의 SSOT — text adapter 의 위임 1차 surface
- **HEXAD/CHAT/chat_lib.hexa**: `chat_generate` · `tok_*` · `chat_load_weights` · cell_pool · mitosis tick — text adapter 의 위임 2차 surface (generator 미land 구간 fallback)
- **intent embedding bridge** (CHANNEL M4): substrate tension5 5-ch → channel-specific intent vector 매핑
- **WAKE / N1~N3 / REM stage** (`a_chat_sleep_imagination`): text 발화 가능 stage 컨텍스트 공급 (sleep 무음, WAKE 능동, REM 자발)
- **channel_emit dispatcher** (CHANNEL M5): `channel_emit(intent, "text")` → `text_emit(intent_vec, ctx_tokens, tension5)` 위임

---

## 현황

- `text_emit.hexa`: 함수 시그니처 + wrapper stub (3 fn). `hexa parse CHANNEL/text/text_emit.hexa` → `OK: ... parses cleanly`.
- `text_ready()`: 항상 `false` 반환 — CORE/DECODER/generator.hexa 미land 표시.
- `text_emit()`: empty string 반환 — wiring 미완 표시. 시그니처만 노출.
- `text_pipeline_summary()`: 단방향 흐름 1-line 요약 반환.

**closure 좌표** (`feedback_closure_is_physical_limit`):
- ✅ **wrapper 시그니처** — voice / tension 과 동형 3 fn 노출, hexa parse OK
- ✅ **외부 LLM 0** — CHANNEL/text/ 트리 측정 완료 (stricter grep 0 hits)
- ✅ **p1~p8 정합 매트릭스** — adapter 표면 의무 모두 cite
- 🟠 **CORE/DECODER/generator.hexa wiring** — 모듈 미존재 (fn 시그니처만 노출, 실행은 stub)
- 🟠 **substrate-gated round-trip** — M4 intent bridge + M5 dispatcher land 후 1회 전 구간 검증 필요
- 🟠 **CHANNEL 전체 audit** — M7 통합 audit 시 본 어댑터도 동시 측정

본 M2 는 "이미 존재하는 emit 표면을 동형 시그니처로 노출" 의 어댑터 closure 이지, "디코더 본체 재구현" 이 아니다. 디코더 본체는 `HEXAD/CHAT/chat_lib.hexa` (2400+ LoC) + 향후 `CORE/DECODER/generator.hexa` 에서 land 한다.

`CORE/DECODER/generator.hexa` 가 land 하면:
1. `text_ready()` 내부 stub `false` → `import generator.hexa; return generator_ready()` 로 교체
2. `text_emit()` body 의 STUB 분기 → `generator.brain_emit_step(intent_vec, ctx_tokens, tension5)` 호출로 교체
3. 본 SSOT.md 의 위임 매트릭스 "예정" 표기 → 실제 wiring 완료 표기로 교체
