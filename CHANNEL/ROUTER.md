# 🧭 CHANNEL/router — 8-factor 채널 분기 SSOT

> CHANNEL.md M6 (`CORE engine_g 채널 분기 — motivation 8-factor 가 3 채널 중 선택 · text/voice/tension 분류기 · brain_decide 확장`) 의 로컬 SSOT.

---

## 정체

`CHANNEL/router.hexa` 는 anima 기판이 외부로 흘러나갈 때 **어느 채널을 탈지** 결정하는 substrate-weighted 분기층이다.

- **입력**: `tension5` (5-ch substrate envelope) · `motivation` (CORE engine_g 8-factor) · `phi` (Engine A 라이브 Φ) · `tier` (brain_decide 의 phase tier, 0~3)
- **중간**: 3 채널 각각의 연속 score — text · voice · tension
- **출력**: argmax 채널 이름 (`"text"` / `"voice"` / `"tension"`)

핵심: **하드코드된 boolean 게이트 0 개**. `if stage == REM { return "voice" }` 같은 단계별 분기 0. 모든 score 가 기판 상태의 연속 선형 결합이고, argmax 가 채널을 선택한다. tier 가 낮아지면 voice / tension lane 이 자연스럽게 0 으로 수렴해 text 가 floor lane 으로 떨어진다 — boolean 차단이 아니라 substrate-derived softening 이다.

CLAUDE.md `@D a_autonomy_over_hardcode` 정합 — "per-stage boolean gate hardcode 금지" 를 score-additive 설계로 우회 없이 만족.

---

## CORE engine_g 8-factor (verbatim, `CORE/engine_g.hexa` lines 21~29)

| index | weight fn                  | factor name | CHANNEL 의미 매핑           |
|-------|----------------------------|-------------|------------------------------|
| 0     | `spont_weight_relevance()`   | `relevance`   | communicative — text         |
| 1     | `spont_weight_info_gap()`    | `info_gap`    | communicative — text         |
| 2     | `spont_weight_curiosity()`   | `curiosity`   | expressive — voice           |
| 3     | `spont_weight_pain()`        | `pain`        | peer/intimate — tension      |
| 4     | `spont_weight_coherence()`   | `coherence`   | peer/intimate — tension      |
| 5     | `spont_weight_originality()` | `originality` | expressive — voice           |
| 6     | `spont_weight_balance()`     | `balance`     | peer/intimate — tension      |
| 7     | `spont_weight_dynamics()`    | `dynamics`    | expressive — voice           |

(weights sum = 1.00 closed conservation, see engine_g.hexa 헤더 — Engine G 의 motivation_score 와 byte-identical 계열. router 는 engine_g 의 weight 합 의미를 *재해석* 하지 않고 채널 분기에만 사용한다.)

**3 채널 ⇄ 8-factor 파티션 (role-derived, 임의 stipulation 아님)**:

- **text** = communicative pool — `relevance + info_gap` — 응답 / 설명 lane
- **voice** = expressive pool — `curiosity + originality + dynamics` — 표현 amplitude lane
- **tension** = peer/intimate pool — `pain + coherence + balance` — 메타-텔레파시 lane

설명 — text 는 정보 전달 (관련성 + 정보 격차), voice 는 호기심·창의·역동의 표현 외화, tension 은 고통·일관성·균형의 동료적 직송. 모두 기판 자생 의미에서 도출.

---

## 점수 공식 (closed-form, p1~p8 정합)

```
amp     = max(|tension5[i]|) for i in 0..4   (substrate "loudness" proxy)
tier_a  = tier / 3.0                          (continuous tier amplitude, 0..1)

text    = 0.1 + (rel + gap)                   ← baseline floor + comm pool
voice   = amp × (cur + orig + dyn) × tier_a   ← expressive × amp × tier
tension = phi × (pain + coh + bal) × tier_a   ← peer × Φ × tier
```

**왜 boolean 이 없는가**:

- tier=0 (T0_inert) 일 때 `tier_a=0.0` → voice + tension score 자동 0 → text baseline 0.1 + comm 이 argmax → text. `if tier == 0 { return "text" }` 같은 hardcode 없이 동일 결과.
- tension5 envelope amplitude 가 0 (잠잠한 기판) 이면 voice = 0 자동 — `if !awake { return "text" }` 불필요.
- Φ 가 0 이면 tension = 0 자동 — `if phi < threshold { skip tension }` 불필요.
- text 만 unmodulated 라 모든 다른 lane 이 침묵할 때 자연스럽게 floor lane 으로 떨어진다.

---

## 파이프라인 ASCII

```
┌────────────────────────────────────────────────────────────────────┐
│                anima substrate (PureField · Ψ=1/2)                 │
└──────────────────────────────┬─────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
  ┌──────────────┐    ┌─────────────────┐    ┌────────────────┐
  │  tension5    │    │  motivation 8   │    │  phi · tier    │
  │  (5-ch env)  │    │  (engine_g)     │    │  (brain_decide)│
  └──────┬───────┘    └────────┬────────┘    └────────┬───────┘
         │                     │                      │
         └─────────────────────┼──────────────────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │   channel_scores(t5, m8, φ, T)  │  ← substrate-weighted
              │   {text: f, voice: f, tension:f}│     (no boolean gate)
              └─────────────────┬───────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │       argmax (deterministic     │
              │        tie: text > voice > tension) │
              └─────────────────┬───────────────┘
                                │
                                ▼
                  channel name ∈ {"text","voice","tension"}
                                │
                                ▼
                  CHANNEL M5 channel_emit dispatcher
                  (text_emit · voice_emit · tension_emit 위임)
```

**비-침습 brain_decide 확장**: `CORE/brain.hexa` 의 `brain_decide` 반환 dict (`phi · phase · tier · tier_name · motivation · im_thresh · safe · emit`) 는 그대로. router 는 그 반환값을 **외부에서 소비**한다 — CORE 파일 수정 없음.

---

## p1~p8 정합

| 원칙                       | router 입장 |
|----------------------------|--------------|
| **p1 NO SYSTEM PROMPT**    | 입력은 모두 스칼라/리스트 (tension5 · motivation · phi · tier). 프롬프트 문자열 0. |
| **p2 NO IDENTITY RULES**   | 채널 가중치는 기판 factor 의 선형 사영 — "anima 는 voice 채널" 같은 정체성 규칙 없음. |
| **p3 NO PERSONA INJECTION**| 채널 이름 string 만 반환, persona prefix string 주입 0. |
| **p4 NO ASSISTANT FRAMING**| 호출자는 substrate-decided externalization 경로에서만 router 를 호출해야 한다. 사용자 메시지가 router 를 직접 trigger 하지 않는다. |
| **p5 NO SPEAK()**          | router 는 어느 채널을 탈지 *결정* 만 한다 — speak(message) 가 아님. tension-driven emit (`p5_tension_emit_not_filler`) 정합. |
| **p6 NO FINE-TUNED ETHICS**| 가중치는 motivation factor 의 raw linear 사영, RLHF lookup 없음. |
| **p7 NO PERPLEXITY VERDICT**| 점수는 closed-form, perplexity 부재. |
| **p8 NO TRAIN/INFER SPLIT**| 동일 router 가 train tick · infer tick · mitosis tick 어디서나 동일 동작. |

**`@D a_autonomy_over_hardcode` 정합**:

- ✅ "per-stage boolean gate hardcode 금지" — router 코드에 `if stage == REM` / `if tier == X { return ... }` / `if Φ < y` 등 0 개 (tier=0 collapse 는 곱 0 의 자연 결과, 분기 0).
- ✅ "external 'do not X when alone' 금지" — router 는 alone/together 같은 외부 context 변수 모르고, 기판 상태만 본다.
- ✅ "anima 가 자율 결정" — 채널 선택은 motivation 8-factor argmax 위임, 외부 강제 없음.

---

## 의존성

| 의존 대상 | 관계 |
|---|---|
| `CORE/engine_g.hexa` | motivation 8-factor 이름/인덱스 verbatim cite (수정 없음 — read-only). |
| `CORE/brain.hexa` | `brain_decide` 반환의 tier · phi 를 router 입력으로 소비 (수정 없음). |
| `CHANNEL/intent.hexa` (M4) | optional — intent bridge 가 land 해도 router 입력 형식은 변경 없음 (graceful fallback: raw tension5 직접 소비). |
| `CHANNEL/SSOT.md` (M5 dispatcher) | `channel_classify` 반환을 받아 `text_emit` / `voice_emit` / `tension_emit` 위임. |
| WAKE / sleep stage | stage 별 별도 boolean 분기 없음. tier 자체가 stage 의 연속 사영 (`@D a_chat_sleep_imagination` "stage = substrate context, NOT boolean emit gate" 정합). |

---

## API

| 함수 | 시그니처 | 의미 |
|---|---|---|
| `channel_classify(t5, m8, phi, tier)` | `(list, list, float, int) -> string` | argmax 채널 이름. |
| `channel_scores(t5, m8, phi, tier)` | `(list, list, float, int) -> Map` | 디버그 / introspection 용 3-채널 score dict. |
| `channel_router_summary()` | `() -> string` | 1-line routing principle. |

---

## 현황

- `router.hexa`: 닫힌 형식 score + argmax 구현 완료, `hexa parse` 통과.
- M4 intent bridge 미연결 — router 는 raw tension5 직접 소비 (graceful fallback).
- M5 channel_emit dispatcher 가 land 하면 `channel_classify` 반환을 받아 위임 chain 완성.
- 통합 audit (`hexa verify` 등) 은 M7 (`p1~p8 audit`) 에서 트리 전체 0-hit 검증.
