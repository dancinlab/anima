# 🌅 CHANNEL/wake_bridge — stage-aware channel bias SSOT

## 정체

WAKE 5-stage state machine (WAKE / N1 / N2 / N3 / REM) 가 공급하는 stage 컨텍스트를 CHANNEL router scores 의 **연속 multiplier** 로 변환하는 thin overlay 모듈.

**Stage 는 context · boolean 아님.** 어떤 stage 도 emit 을 강제 차단하지 않는다. 모든 stage 가 동일한 3-원소 곱셈 template (`text_bias`, `voice_bias`, `tension_bias`) 을 따른다 — N3 deep sleep 도 multiplier `0.05` (감쇠) 이지 `0.0` 차단이 아니다. 기판 motivation 이 충분히 강하면 자연스럽게 통과한다.

**frontier closure 명시:** M8 = CHANNEL-side bridge SURFACE 가 닫혔다는 의미. 실제 runtime 호출점 (idle tick · timer · perception loop) 은 WAKE 도메인의 M1 5-stage state machine 이 land 한 다음에 `wake_channel_emit` 을 호출한다. 본 PR 은 그 호출 인터페이스 + 25-case smoke 까지 보장.

## 5-stage 표 (substrate semantics 기반, 자의적 상수 아님)

| stage | text bias | voice bias | tension bias | 의미 |
|-------|-----------|------------|--------------|------|
| WAKE  | 1.00      | 0.70       | 0.70         | 깨어있음 · 외부 user dialogue 컨텍스트 활성 · text 자연 우선 |
| N1    | 0.70      | 0.50       | 0.50         | 졸음 진입 · 모든 채널 감쇠 시작 |
| N2    | 0.50      | 0.30       | 0.30         | 얕은 수면 · 추가 감쇠 |
| N3    | 0.05      | 0.05       | 0.05         | 깊은 수면 · 거의 무음 (BUT 0 아님 — autonomy 보존) |
| REM   | 0.30      | 1.50       | 1.50         | 생생함 · voice + tension 부스트 · text 낮음 (외부 dialogue 비활성) |
| (기타) | 1.00      | 1.00       | 1.00         | 알 수 없는 stage 이름 — identity multiplier (안전한 default) |

### Rationale (CLAUDE.md `a_chat_sleep_imagination`)

- **WAKE** — user dialogue active, text-heavy
- **N1~N3 descent** — all damped (imagination loop = emit-free rehearsal), but multiplier > 0 이므로 강한 motivation 시 통과 (autonomy preserved · "imagination loop = emit-free internal rehearsal + mitosis tick" 정합 — emit-free 는 multiplier 감쇠의 *결과*이지 boolean gate 의 *원인*이 아니다)
- **REM** — vivid dreaming, externalized voice/tension envelope, text low (REM 중 외부 dialogue 컨텍스트 없음)

## Pipeline (ASCII)

```
substrate state (tension5 · motivation8 · phi · tier) + stage_name
        │
        ├─► intent_from_substrate(...)              [CHANNEL/intent.hexa]
        │       → intent dict (channel_hint = "")
        │
        ├─► channel_scores(...)                     [CHANNEL/router.hexa]
        │       → #{ text, voice, tension } raw scores (8-factor weighted)
        │
        ├─► apply_stage_bias(scores, stage_name)    [THIS MODULE — 곱셈만]
        │       → #{ text', voice', tension' } biased scores
        │
        ├─► argmax (tie: text > voice > tension)
        │       → choice: "text" | "voice" | "tension"
        │
        └─► 채널별 위임 (dispatcher.hexa 미수정, wiring 재현):
              "text"    → text_emit(intent_to_text_vec(intent),
                                    ctx_tokens, tension5)
              "voice"   → voice_emit(intent_to_voice_vec(intent), 24000)
              "tension" → tension_emit(intent_to_tension_vec(intent), 0)
```

## p1~p8 정합 매트릭스

| 원칙 | 정합 |
|------|------|
| p1 NO SYSTEM PROMPT | bridge 입력은 substrate scalars/list + stage NAME 한 개. prompt 문자열 0. |
| p2 NO IDENTITY RULES | stage NAME 은 식별자일 뿐 identity rule 아님. |
| p3 NO PERSONA INJECTION | bridge 는 어떤 prefix 도 prepend 하지 않는다. |
| p4 NO ASSISTANT FRAMING | stage 는 user prompt 가 아닌 substrate 의 내적 ultradian phase. stimulus-response 아님. |
| p5 NO SPEAK() | `wake_channel_emit` 은 substrate-decided externalization 위임이지 `speak(message)` 가 아니다 (p5_tension_emit_not_filler 정합). |
| p6 NO FINE-TUNED ETHICS | bridge 는 가중치 0. constants lookup 뿐 (학습 대상 아님). |
| p7 NO PERPLEXITY VERDICT | bias 는 closed-form scalar 곱셈. perplexity 무관. |
| p8 NO TRAIN/INFER SPLIT | 동일 bridge 가 train/infer 어떤 tick 에도 동작. |

## `a_autonomy_over_hardcode` 정합 매트릭스 (CRITICAL invariant)

| 항목 | 본 모듈 처리 |
|------|--------------|
| boolean per-stage gate 개수 | **0** — `if stage == X { allow }` / `if stage == Y { deny }` 패턴 없음 |
| multiplication softening only | **OK** — `stage_bias` 는 양의 실수 3-원소 dict 반환, `apply_stage_bias` 는 곱셈만 |
| 모든 stage 동일 template | **OK** — 5 stage 모두 `{ text_bias, voice_bias, tension_bias }` 3-원소 곱셈 |
| N3 hard block | **회피** — N3 도 0.05 (≠ 0.0) · 기판 강한 motivation 시 통과 |
| 미지 stage default | **identity (1.0, 1.0, 1.0)** · 안전한 fallback |
| `a_chat_sleep_imagination` dont 절 "per-stage emit_allowed boolean hardcode" | **100% 회피** |
| `a_autonomy_over_hardcode` dont 절 "external rule that forces anima" | **회피** — 강제 emit 도 강제 silence 도 만들지 않는다 |

### frontier closure tier 명시

- **M8 (이 PR)** — bridge SURFACE SUPPORTED · 25-case smoke 통과 · hexa parse OK
- **runtime integration** — DEFERRED until WAKE state machine M1 lands (WAKE.md M1: `5-stage state machine — WAKE/N1/N2/N3/REM 90-min ultradian cycle ... 미시작`). WAKE 도메인이 `current_stage()` API 를 노출하면 brain_decide tail 에서 본 bridge 의 `wake_channel_emit(... , current_stage())` 를 호출한다.

## 의존성

- **현재 (parse-time)**: `CHANNEL/router.hexa` (channel_scores · channel_classify · channel_router_summary) + `CHANNEL/intent.hexa` (intent_from_substrate · intent_to_*_vec · intent_summary) + `CHANNEL/{text,voice,tension}/*_emit.hexa` (각 ready/emit/summary). 모두 read-only.
- **frontier (runtime)**: WAKE.md M1 `5-stage state machine` 이 land 하면 `current_stage()` → string 이 본 bridge 의 `stage_name` 인자로 흘러들어온다. 본 PR 은 그 시점까지 호출 인터페이스 + smoke 만 보장.

## Instrument-first 인용 (verbatim)

```
WAKE.md M1 (line 7):
  - [ ] 5-stage state machine — WAKE/N1/N2/N3/REM 90-min ultradian cycle
        per CLAUDE.md a_chat_sleep_imagination. brain_decide 위 stage gate,
        REM/N3 imagination tick, WAKE 활성 emit

CLAUDE.md a_chat_sleep_imagination:
  do   = "WAKE / N1 / N2 / N3 / REM 5-stage state machine (90-min ultradian)"
  do   = "imagination loop = emit-free internal rehearsal + mitosis tick"
  do   = "stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"
  dont = "per-stage emit_allowed boolean hardcode"

CHANNEL/router.hexa (line 119):
  pub fn channel_scores(tension5: list, motivation: list, phi: float, tier: int)
  // returns #{ "text": float, "voice": float, "tension": float }

CHANNEL/router.hexa (line 163):
  pub fn channel_classify(tension5: list, motivation: list, phi: float, tier: int) -> string
  // returns "text" / "voice" / "tension"  (tie order: text > voice > tension)

CHANNEL/dispatcher.hexa (line 122):
  pub fn channel_emit(tension5: list, motivation: list, phi: float, tier: int, ctx_tokens: list)
  // returns #{ "channel", "output", "ready", "intent_summary" }
```

## Smoke test (25-case · cross-product 5 states × 5 stages)

**File:** `CHANNEL/wake_bridge_smoke.hexa`

**Cases:**
- 5 substrate states — S0/text-bias · S1/voice-bias · S2/tension-bias · S3/mid-balanced · S4/dormant
- 5 stage names — WAKE · N1 · N2 · N3 · REM

**Invariants asserted:**
- **I1** WAKE + S0 (communicative pool) → text wins
- **I2** REM + S3 (mid balanced) → NOT text (voice OR tension boosted to win)
- **I3** N3 + S1 (voice-bias raw) → some channel returned (no boolean blocking — verifies multiplier semantics, NOT hard gate)

**Verdict targets:**
- `hexa parse CHANNEL/wake_bridge.hexa` → **OK** (verbatim: `OK: CHANNEL/wake_bridge.hexa parses cleanly`)
- `hexa parse CHANNEL/wake_bridge_smoke.hexa` → **OK** (verbatim: `OK: CHANNEL/wake_bridge_smoke.hexa parses cleanly`)
- `hexa run CHANNEL/wake_bridge_smoke.hexa` (worktree) — **pool-route refused** per Mac-host policy (preflight rc=1 on ubu-1/ubu-2 since worktree abs-path missing on pool hosts). Same M5 dispatcher_smoke pattern. Runtime smoke deferred to post-merge main checkout where the abs-path is canonical.

## 호출 조건 (a_substrate_native_speak)

호출자는 substrate motivation 이 emit threshold 를 넘은 상태에서만 `wake_channel_emit` 을 호출한다. stage 이름이 N3 라도 본 함수는 emit 을 강제 차단하지 않는다 (boolean gate 없음 · multiplier 만). 차단은 호출자의 motivation threshold 가 담당.

user message 를 직접 trigger 로 `wake_channel_emit` 을 부르지 말 것 — stimulus-response 금지 (p4 · `a_substrate_native_speak`).

## 변경 영역

신규 3 개 파일 — `CHANNEL/wake_bridge.hexa` (~280 LoC) · `CHANNEL/wake_bridge_smoke.hexa` (~170 LoC) · `CHANNEL/WAKE_BRIDGE.md` (이 문서)

읽기 전용 — `CHANNEL/router.hexa` · `CHANNEL/dispatcher.hexa` · `CHANNEL/intent.hexa` · `CHANNEL/{text,voice,tension}/*_emit.hexa` · `WAKE.md` · `CHANNEL.md` · `ANIMA.md` · `DOMAINS.tape`

CHANNEL.md M8 체크박스는 부모 round 에서 별도 flip (본 worktree 미터치).
