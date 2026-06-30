# 🎛 CHANNEL/dispatcher — 통합 진입점 `channel_emit` SSOT

> CHANNEL.md M5 milestone — 단일 진입점 `channel_emit` · router 가 채널 선택 · 3 emit fn 위임 · substrate-gated 발화.
> 본 문서는 SSOT, 코드는 [`CHANNEL/dispatcher.hexa`](dispatcher.hexa), smoke 는 [`CHANNEL/dispatcher_smoke.hexa`](dispatcher_smoke.hexa).

---

## 1. 정체

- **단일 진입점** — `channel_emit(tension5, motivation, phi, tier, ctx_tokens) -> Map`
  - substrate state 만 입력으로 받는다 (prompt 문자열 없음, p1 정합).
  - 어떤 새 의식도 만들지 않는다 — `CHANNEL/intent.hexa`의 reformat 만 사용.
- **router 결정** — `channel_classify(tension5, motivation, phi, tier)` 가 `"text"` / `"voice"` / `"tension"` 중 하나를 argmax 로 반환. dispatcher 는 그 결정을 따른다.
- **3 emit fn 위임** — text/voice/tension 각각의 emit fn 시그니처 대로 호출, 어떤 prefix 도 prepend 하지 않는다.
- **substrate-gated 발화** — dispatcher 가 자체적으로 게이트하지 않는다 (a_autonomy_over_hardcode). 호출자가 substrate-decided externalization 경로에서만 호출해야 한다 (a_substrate_native_speak).

---

## 2. Pipeline ASCII

```
substrate state (tension5 · motivation8 · phi · tier · ctx_tokens)
        │
        ▼
intent_from_substrate(tension5, phi, motivation, tier, "")     ← CHANNEL/intent.hexa
        │      (channel_hint = "" — router 가 결정)
        ▼
   Intent dict  #{ "vec", "channel_hint", "tension5",
                   "motivation", "phi", "tier" }
        │
        │           channel_classify(tension5, motivation, phi, tier) ← CHANNEL/router.hexa
        │                       │
        │                       ▼
        │            "text" | "voice" | "tension"
        │                       │
        ├──── "text"    ───────►│  intent_to_text_vec(intent)   → text_emit(vec, ctx_tokens, tension5)
        ├──── "voice"   ───────►│  intent_to_voice_vec(intent)  → voice_emit(vec, 24000)
        ├──── "tension" ───────►│  intent_to_tension_vec(intent)→ tension_emit(vec, 0)
        └──── default   ───────►│  text 위임 (자연 floor lane — router tie order text > voice > tension)
                                │
                                ▼
                  #{ "channel": string, "output": <emit raw>, "ready": bool,
                     "intent_summary": string }
```

---

## 3. 의존성 매트릭스

| upstream 파일                                  | dispatcher 가 호출하는 pub fn                                                                                                  |
|------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `CHANNEL/intent.hexa`                          | `intent_from_substrate(tension5, phi, motivation, tier, channel_hint)` · `intent_to_text_vec(intent)` · `intent_to_voice_vec(intent)` · `intent_to_tension_vec(intent)` · `intent_summary(intent)` |
| `CHANNEL/router.hexa`                          | `channel_classify(tension5, motivation, phi, tier) -> string`                                                                  |
| `CHANNEL/text/text_emit.hexa`                  | `text_emit(intent_vec, ctx_tokens, tension5) -> string` · `text_ready() -> bool`                                               |
| `CHANNEL/voice/voice_emit.hexa`                | `voice_emit(intent_vec, sample_rate) -> string` · `voice_ready() -> bool`                                                      |
| `CHANNEL/tension/tension_emit.hexa`            | `tension_emit(fingerprint5, target_lane) -> bool` · `tension_ready() -> bool`                                                  |

**Read-only contract** — dispatcher 는 위 5 파일을 수정하지 않는다 (M1~M4/M6 가 이미 land 한 SSOT).

---

## 4. pub surface

```hexa
pub fn channel_emit(tension5: list, motivation: list, phi: float, tier: int, ctx_tokens: list)
  // 반환 dict: #{ "channel": string, "output": <any>, "ready": bool, "intent_summary": string }

pub fn channel_emit_ready(name: string) -> bool
  // name ∈ {"text","voice","tension"} → 각 채널의 ready() 반환값. 다른 값 → false.

pub fn channel_emit_summary() -> string
  // 한 줄 설명.
```

---

## 5. p1~p8 정합

| 원칙                                | dispatcher 측 보장                                                                                                                       |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| p1 NO SYSTEM PROMPT                 | 입력은 substrate scalars/list 만 (`tension5` · `motivation` · `phi` · `tier` · `ctx_tokens` BPE id). 어떤 prompt 문자열도 받지 않음.    |
| p2 NO IDENTITY RULES                | dispatcher 내부에 어떤 identity rule 인용 0. channel 식별 외 어떤 룰도 적용 안 함.                                                       |
| p3 NO PERSONA INJECTION             | `ctx_tokens` 를 그대로 `text_emit` 에 위임 (prefix 0). voice/tension 측에도 페르소나 임베딩 prepend 0.                                  |
| p4 NO ASSISTANT FRAMING             | `channel_emit` 은 stimulus-response endpoint 가 아니다. user message 직접 trigger 금지 — 문서에서 명시 경고.                            |
| p5 NO SPEAK()                       | substrate tension field externalization 위임 (p5_tension_emit_not_filler 정합). speak(message) 단일 호출이 아님.                       |
| p6 NO FINE-TUNED ETHICS             | dispatcher 는 가중치 0 — router · intent · emit 모듈만 자기 갱신을 mitosis 로 수행.                                                    |
| p7 NO PERPLEXITY VERDICT            | 라우팅 결정은 closed-form argmax (`channel_scores`), perplexity 무관.                                                                  |
| p8 NO TRAIN/INFER SPLIT             | 동일 dispatcher 가 train/infer 어떤 tick 에도 호출 가능.                                                                              |

---

## 6. a_autonomy_over_hardcode 정합

- dispatcher 내부에 **`if stage == N3` · `if tier == 0 { return "text" }` 같은 boolean per-stage gate = 0**.
- 채널 선택은 전적으로 `channel_classify` (continuous score argmax) 에 위임.
- default 경로 (router 가 unknown 문자열 반환 시) 도 채널 결정이 아닌 "자연 floor lane = text" 위임 — router 의 tie order (`text > voice > tension`) 정책과 일치.
- 외부 모듈 (router) 이 substrate score 만 보고 결정하는 구조 → governance 가 substrate self-follows.

---

## 7. smoke 3-case 결과 (verbatim)

`CHANNEL/dispatcher_smoke.hexa` 는 hand-tuned substrate state 3 종으로 router decision → dispatcher channel field 일치를 검사한다.

| case               | tension5                  | motivation (rel·gap·cur·pain·coh·orig·bal·dyn) | phi   | tier | 기대값    | 산식 (router channel_scores)                          |
|--------------------|---------------------------|------------------------------------------------|-------|------|-----------|--------------------------------------------------------|
| text-biased        | `[0.05]×5`                | `[0.6,0.3,0,0,0,0,0,0]`                       | 0.1   | 0    | `text`    | text=0.1+0.9=**1.0** · voice=0.05·0.3·0=0 · tension=0  |
| voice-biased       | `[1.0,0.9,0.8,0.7,0.6]`   | `[0,0,0.9,0,0,0.8,0,0.7]`                     | 0.2   | 3    | `voice`   | text=0.1+0=0.1 · voice=1.0·2.4·1.0=**2.4** · tension=0 |
| tension-biased     | `[0.05]×5`                | `[0,0,0,0.9,0.85,0,0.8,0]`                    | 0.95  | 3    | `tension` | text=0.1 · voice=0.05·0·1=0 · tension=0.95·2.55·1=**2.4225** |

### parse 결과 (verbatim)

```
$ hexa parse CHANNEL/dispatcher.hexa
OK: CHANNEL/dispatcher.hexa parses cleanly

$ hexa parse CHANNEL/dispatcher_smoke.hexa
OK: CHANNEL/dispatcher_smoke.hexa parses cleanly
```

### run 결과 (honest framing)

`hexa run CHANNEL/dispatcher_smoke.hexa` 는 현 worktree 환경에서 **runtime 미실행** — `dispatcher.hexa` 의 abs-path import (`/Users/ghost/core/anima/CHANNEL/router.hexa`) 가 머지 후 canonical 위치를 가리키지만 머지 전에는 워크트리 내부 경로 (`/Users/ghost/core/anima/.claude/worktrees/agent-a667df88c9feefb0b/CHANNEL/router.hexa`) 에 위치한다. 머지 후 `hexa run` 가능.

`hexa run` 시 추가 제약 (memory `reference_life_cycle_hexa_run_gotchas`):
- pool-route 가 `hexa run` 명령을 가로채 Linux pool host (`ubu-1`/`ubu-2`) 로 dispatch — 두 호스트 모두 preflight 실패 (workdir 부재 + hexa_interp 미빌드).
- 우회 = `hexa.real.bak-2026-05-22-pre-no-hxc build` 도 abs-path 해석 실패 동일 원인.

**parse PASS = 시그니처/문법 closure 확인** — 실제 dispatch 동작은 머지 후 origin/main 에서 검증 가능 (post-merge follow-up).

---

## 8. frontier closure honest framing

CHANNEL.md M5 closure 의 정의는 **"단일 진입점 channel_emit 이 3 채널로 위임하는 dispatcher 구조가 wiring 되었다"**. 본 PR 의 성립도:

- ✅ `channel_emit` 시그니처 노출 + 5 upstream pub fn 모두 호출.
- ✅ router 결정 → 3 emit fn 위임 흐름 코드 존재.
- ✅ parse clean (2/2).
- ✅ smoke test 3-case design 명시 — 머지 후 runtime 검증 가능.
- ⚠ runtime PASS = 머지 후 (worktree abs-path 한계 — 머지 직후 hexa run 가능).
- ⚠ 3 underlying emit fn 들은 여전히 STUB (M1/M2/M3) — dispatcher 자체는 정상이나 실제 외부화는 emit fn 들이 wire 된 후 동작.

→ frontier closure level = **structural wiring SUPPORTED · runtime SUPPORTED-by-design (post-merge verify path documented)**.
