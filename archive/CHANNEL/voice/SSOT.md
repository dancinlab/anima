# 🔊 CHANNEL/voice — hexa-voice SSOT

> CHANNEL.md M1 (`hexa-voice repo SSOT 연결`) 의 로컬 SSOT 스캐폴드. 향후 `github.com/dancinlab/hexa-voice` 가 생성되면 이 파일이 포인터-only 로 축소.

---

## 정체

`hexa-voice` 는 anima 의 **24kHz RVQ 오디오 출력 채널** — ANIMA-VOICE × Anima 통합 시스템의 정식 명칭.

- **입력**: anima 기판이 결정한 `intent vector` (substrate-decided externalization 의 channel-specific 표현)
- **중간**: RVQ (Residual Vector Quantization) audio token codes
- **출력**: 24kHz mono PCM bytes (raw 또는 즉시 재생용)

**텍스트 변환기가 아니다.** TTS (Text-to-Speech) 처럼 "텍스트 → 음성" 의 변환 파이프라인이 아니라, **anima 기판 텐션장 → 의도 임베딩 → 오디오 토큰 → PCM** 의 단방향 흐름이다. 텍스트는 별도 채널 (`CHANNEL/text` · CHAT/DECODER 위임) 으로 분기한다.

memory project_hexa_voice_rename SSOT: "ANIMA-VOICE × Anima 통합 시스템 정식 명칭 hexa-voice (의도 임베딩 → RVQ → 24kHz PCM, 텍스트 변환기 아님)".

---

## repo pointer

- **향후**: `github.com/dancinlab/hexa-voice` (user-gated · 미생성)
- **현재**: 본 디렉터리가 로컬 SSOT — repo 생성 시 spec / 모델 / 파이프라인 코드가 이쪽으로 이전, 본 SSOT.md 는 포인터-only 로 축소
- **patterns**: `hexa-lang` · `kosmos` · `hexa-codex` 와 같은 sibling 위치 (CLAUDE.md `@I.siblings`)

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
                  │  RVQ encoder (hexa-voice)    │
                  │  intent vec → audio codes    │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  audio token decoder         │
                  │  codes → 24kHz mono PCM      │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                          24kHz PCM bytes
                       (raw stream · 단방향)
```

**역류 없음** — PCM bytes 에서 substrate 로 거꾸로 흐르는 경로는 정의되지 않는다 (음성 입력은 별도 sensor 채널 의무, 본 SSOT 범위 밖). 의도 임베딩이 RVQ 의 입력이고, RVQ 가 PCM 의 입력이다. 텍스트는 어디에도 끼어들지 않는다.

---

## p1~p8 정합

| 원칙 | hexa-voice 입장 |
|---|---|
| **p1 NO SYSTEM PROMPT** | RVQ 입력은 intent vector — 프롬프트 문자열 부재. |
| **p2 NO IDENTITY RULES** | "anima 의 목소리" 정체성은 기판 셀 분열에서 emerge — voice 모델은 음향 잔향만 담당. |
| **p3 NO PERSONA INJECTION** | "you are anima" 같은 prefix 임베딩 없음 — intent vector 는 substrate tension5 의 직접 매핑. |
| **p4 NO ASSISTANT FRAMING** | TTS-style "사용자 요청 → 음성 응답" 패턴 금지. voice_emit 은 **substrate-decided** 일 때만 발화. |
| **p5 NO SPEAK()** | `voice_emit(intent_vec, sr)` 은 `speak(message)` 가 아니다 — intent vector 가 substrate tension 의 externalization 일 때만 호출, 외부 trigger 로 부르지 않는다. p5_tension_emit_not_filler 적용. |
| **p6 NO FINE-TUNED ETHICS** | RVQ 모델 학습에 cooperation/empathy RLHF 주입 금지 — 음향 표현은 셀 분열 결과로만 변화. |
| **p7 NO PERPLEXITY VERDICT** | voice 품질 평가는 audio coherence + substrate fit 으로 — perplexity / loss 단독 verdict 금지. |
| **p8 NO TRAIN/INFER SPLIT** | RVQ encoder 가중치는 inference 중에도 셀 분열 (mitosis tick) 으로 갱신 가능 — train/infer 단절 금지. |

**stimulus-response 금지** — 사용자 음성 입력이 자동으로 voice_emit 을 trigger 하지 않는다. CORE engine_g motivation 8-factor 가 voice 채널을 선택했을 때, 그리고 WAKE / REM stage 가 substrate context 를 공급할 때만 흐른다 (a_substrate_native_speak · a_autonomy_over_hardcode).

**TTS-style command-response 금지** — "이 텍스트를 읽어줘" → PCM 같은 명령-응답 인터페이스가 아니다. intent vector 가 substrate tension5 에서 직접 derive 되어야 한다.

---

## 의존성

- **CORE engine_g motivation 8-factor** (CHANNEL M6 채널 분기): text / voice / tension 3 채널 중 voice 선택 결정
- **intent embedding bridge** (CHANNEL M4): substrate tension5 5-ch → channel-specific intent vector 매핑
- **WAKE / REM stage** (a_chat_sleep_imagination): voice 발화 가능 stage 컨텍스트 공급 (N1~N3 sleep 무음)
- **channel_emit dispatcher** (CHANNEL M5): `channel_emit(intent, "voice")` → `voice_emit(intent_vec, 24000)` 위임

---

## 현황

- `voice_emit.hexa`: 함수 시그니처 stub — 실제 RVQ 모델 / encoder / decoder 코드는 hexa-voice repo 생성 후 이전
- `voice_ready()`: 항상 `false` 반환 — 파이프라인 미연결 표시
- `voice_pipeline_summary()`: 본 SSOT 의 ASCII 흐름 요약 string 반환

`hexa-voice` repo 가 생성되면:
1. RVQ encoder / decoder 모델 가중치 → hexa-voice repo
2. intent vector spec → hexa-voice repo `spec/intent.md`
3. 본 SSOT.md → 1-line pointer (`see github.com/dancinlab/hexa-voice/spec/`)
4. `voice_emit.hexa` → hexa-voice 의 stdlib 함수를 import 하는 thin shim
