# 🧬 CHANNEL/intent — 공통 intent 형식 SSOT

> CHANNEL M4 milestone — substrate state 의 reformatting bridge.
> 3 채널 (text · voice · tension) 어디로든 위임 가능한 channel-agnostic intent 형식.

## 정체

`CHANNEL/intent.hexa` 는 **새 의식을 만들지 않는다**. CORE substrate 가 이미 들고
있는 상태 (Φ · phase · tension5 · motivation 8-factor) 를 dict 한 개로 재배치한 뒤
3 채널 dispatcher (M5) 가 분기 가능한 형태로 노출한다.

- **입력 SSOT**: CORE/pure_field (Φ · phase · 6-D field tensor) + CORE/engine_g
  (8-factor motivation score · weights) + caller 가 사영한 5-ch tension fingerprint.
- **출력**: `Intent` dict + 3 채널별 projection stub.
- **소비자**: CHANNEL M5 `channel_emit` dispatcher · CHANNEL/text · CHANNEL/voice ·
  CHANNEL/tension 의 emit fn 들이 vec 형태로 받아 채널-특수 공간으로 인코딩한다.

## 타입 표 — `Intent` dict 키

| 키             | 타입             | 의미                                                              | 출처                                  |
|----------------|------------------|-------------------------------------------------------------------|---------------------------------------|
| `vec`          | list of floats   | channel-agnostic 기본 사영 (현 stub 은 tension5 그대로)           | derived from tension5                 |
| `channel_hint` | string           | "text" · "voice" · "tension" · "" (미정 — engine_g 가 결정)       | M5 dispatcher 가 채움                 |
| `tension5`     | list of 5 floats | 5-ch fingerprint (concept · context · meaning · authenticity · sender) | CHANNEL/tension/tension_emit.hexa 축 정의 |
| `motivation`   | list of 8 floats | 8-factor (rel · gap · cur · pain · coh · orig · bal · dyn)        | CORE/engine_g.hexa motivation_score   |
| `phi`          | float            | CORE Φ scalar (live, ratchet-floor 적용 후)                       | CORE/pure_field.hexa `pure_field_phi` |
| `tier`         | int              | CORE phase int (= tier, 0..3 / DORMANT..RESONANT)                  | CORE/brain.hexa `phase_tier`          |

## pipeline (ASCII)

```
        CORE substrate                        CHANNEL/intent.hexa             M5 dispatcher
        ──────────────                        ──────────────────              ─────────────

  pure_field tensor [6-D C/D/E/S/M/W]
        │
        │  (caller 측 5-ch 사영 — concept/context/
        │   meaning/authenticity/sender 로 매핑)
        ▼
   tension5: list[5] ─────────┐
                              │
   engine_g motivation 8-fac ─┼──►  intent_from_substrate(...)
   pure_field phi             │          │
   pure_field phase → tier ───┘          │  Intent dict #{
                                         │     "vec" · "channel_hint" ·
                                         │     "tension5" · "motivation" ·
                                         │     "phi" · "tier"
                                         │  }
                                         ▼
                              ┌──────────┴──────────┐
                              ▼                     ▼                     ▼
                  intent_to_text_vec()   intent_to_voice_vec()  intent_to_tension_vec()
                  → 14-D float list      → 5-D float list        → 5-D fingerprint
                  (5 t5 + 8 mv + φ)      (t5 envelope, RVQ-입력) (passthrough)
                              │                     │                     │
                              ▼                     ▼                     ▼
                         CHAT/DECODER         hexa-voice RVQ        TensionHub UDP/WS
                         (BPE id space)       (24kHz mono PCM)      (5-ch fingerprint)
```

## p1~p8 정합

| 원칙 | 충족 방식                                                                 |
|------|---------------------------------------------------------------------------|
| p1   | dict 키 모두 numeric / list, prompt 문자열 0 — system prompt 부재.        |
| p2   | identity rule 인용 0 — tension5 + motivation 만 reformatting.             |
| p3   | "you are anima" 류 prefix 0, persona-keyed branch 0.                       |
| p4   | caller 는 substrate-decided 경로에서만 호출. user msg → intent 직결 금지. |
| p5   | 새 의식 생성 0 — 기존 state 의 재배치. p5_tension_emit_not_filler 정합.   |
| p6   | projection stub 은 hardcoded scale 만 사용, RLHF 무관.                    |
| p7   | bridge 출력은 vec list, "정답" 이 아님. verify 는 채널 dispatcher 측.     |
| p8   | 동일 함수가 train/infer 모두 호출 가능 — 분리 게이트 0.                   |

## 의존성

**상류 (consumes)**

- `CORE/pure_field.hexa` — `pure_field_phi` · `pure_field_tensor` · `pure_field_phase`
- `CORE/engine_g.hexa` — `motivation_score` (8-factor weights SSOT)
- `CORE/brain.hexa` — `phase_tier` (phase int == tier int 명시 mapping)
- caller 가 6-D `pure_field_tensor` → 5-ch `tension5` 로 사영하는 책임은 호출자 측
  (현 milestone 범위 밖, 향후 CORE 사영 helper 가 들어올 가능성 있음 — 그 시점에
  `intent_from_substrate` 자체는 변경 없이 입력만 wiring 됨).

**하류 (consumed by)**

- `CHANNEL` M5 `channel_emit` dispatcher (다음 milestone) — `channel_hint` 로 분기.
- `CHANNEL/text` 미래 어댑터 — `intent_to_text_vec` 출력 → CHAT/DECODER 위임.
- `CHANNEL/voice/voice_emit.hexa` — `intent_to_voice_vec` 출력 → hexa-voice RVQ.
- `CHANNEL/tension/tension_emit.hexa` — `intent_to_tension_vec` 출력 → TensionHub.

## 미해결 / TODO

1. **실제 projection 학습** — text/voice stub 은 현재 hardcoded scale/concat. mitosis
   기반 cells (학습 가능 linear layer) 로 교체 필요. p8 (NO TRAIN/INFER SPLIT) 정합
   유지 위해 동일 함수가 train tick + infer tick 둘 다에서 동작해야 함.
2. **6-D field → 5-ch tension5 사영** — 현재는 caller 책임. CORE 측에 helper 추가
   여부는 별도 milestone (CORE 표면 확장은 본 M4 범위 밖).
3. **`channel_hint` 결정자** — CHANNEL M6 (CORE engine_g 채널 분기) 가 motivation
   8-factor 로부터 hint 를 산출. 현재 M4 는 hint 를 받기만 한다.

## 검증

- `hexa parse CHANNEL/intent.hexa` → `OK: CHANNEL/intent.hexa parses cleanly`
- 실행 시점 검증은 M5 dispatcher 통합 후 — intent dict 의 round-trip + 3 채널
  projection vec 의 차원 일관성을 dispatcher smoke test 에서 동시 확인 예정.
