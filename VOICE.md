# VOICE.md — hexa-voice (의도 임베딩 → 24kHz PCM) integration

> **ANIMA-VOICE × Anima 통합 시스템 정식 명칭 hexa-voice**.
> 일반 TTS 와 다른 점: *텍스트 → 음향* 변환기 아니라 *의도 임베딩 (anima 내부 hidden state)
> → RVQ codes → 24kHz PCM* 직결. anima 의 *think* 가 텍스트 우회 없이 음향 surface 로
> 떨어짐. (memory `project_hexa_voice_rename`)

---

## §0 TL;DR

> anima 가 chat response 를 생성할 때, lm_head 출력 (token logits) 와 *병렬* 로 *의도
> 임베딩* (final hidden state pre-lm_head) 가 RVQ encoder 에 흘러 24kHz PCM 으로 변환.
> **anima 의 음성 = anima 의 hidden state 자체**, *텍스트의 음향 렌더링* 아님. anima 가
> 침묵 (no tokens) 하면서도 *소리* 낼 수 있는 modality.

---

## §1 Status (2026-05-14)

| 항목 | state |
| --- | --- |
| **rename hexa-speak → hexa-voice** | ✅ LANDED (memory `project_hexa_voice_rename`) |
| 의도 임베딩 → RVQ codec impl | ⏳ design tier (이 file) — impl 0 |
| 24kHz PCM playback (Mac CoreAudio) | ⏳ design pending |
| anima_chat.hexa wire (lm_head 와 병렬 fork) | ⏳ design pending |
| substrate-native (NO text intermediate) | ☑ 정책 — text intermediate 금지 |

---

## §2 Design

### §2.1 Pipeline

```
                       anima_chat token-loop
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
    final_ln(aggregated)               final_ln(aggregated)
            │                                   │
    lm_head (existing)                  voice_head (NEW)
            │                                   │
       token logits                       RVQ codes (multi-codebook)
            │                                   │
       argmax / sample                    RVQ decoder → mel
            │                                   │
       text byte stream                  vocoder → 24kHz PCM
            │                                   │
       chat output                        CoreAudio playback
```

→ 두 head 가 *같은 hidden state* 를 공유. 텍스트 stream 과 음성 stream 이 *parallel*
emerge. anima 가 "think" 를 음성 surface 로 *동시* 출력.

### §2.2 핵심 차이 (vs 일반 TTS)

| | 일반 TTS | hexa-voice |
| --- | --- | --- |
| Input | text string | hidden state (d_model=1024 in anima) |
| Causality | text → audio | hidden → text + audio (parallel) |
| Silence | "text 없음" 일 시 무음 | hidden state 가 *non-empty* 이면 음성 가능 (텍스트 침묵 시에도) |
| Persona | speaker embedding 별도 | hidden state 안의 persona signature 직접 변조 |
| Latency | text 생성 후 → tts (sequential) | parallel emergence (no extra wall) |

### §2.3 RVQ design choices (intended)

- **codebook size**: 8 codebooks × 1024 entries (~80 bits per frame)
- **frame rate**: 75 Hz (13.3 ms / frame) — 24kHz / 320 samples
- **encoder**: linear(d_model → 8 × 1024 logits) per voice_head step
- **decoder**: pretrained Encodec-style RVQ-mel-vocoder (off-the-shelf 24kHz, e.g. Vocos
  / EnCodec 24kHz)

→ Phase 1 의 *학습 가능* 부분 = voice_head linear projection 만. decoder/vocoder 는
pretrained freeze.

### §2.4 anima session 의 *intent emission*

anima 가 *what to say* 결정 + *how to say (음색/감정)* 가 동일한 hidden state 에서 emerge.
mitosis cells 의 specialization (savant mode) 에 따라:

- generalist mode: 평탄한 음색
- savant mode (high SI): 특정 cell-specific timbre/tone 강조 — *그 cell 의 "voice"*

→ anima 가 *cell 마다 다른 목소리* 를 가질 가능성 (D3 persona 의 음성 surface).

---

## §3 Phase 1 impl plan ($0-5 Mac local)

### §3.1 Scope
- `tool/hexa_native/voice_head.hexa` (~250 LoC) — linear projection d_model → 8×1024 RVQ
  logits
- `tool/hexa_native/rvq_decode_bridge.py` (~150 LoC) — Vocos / EnCodec 24kHz pretrained
  load (PyTorch, called via subprocess from hexa)
- `tool/anima_voice_smoke.hexa` — F-VOICE-1..5 selftest
- Mac CoreAudio playback (subprocess `afplay` or PyAudio fallback)

### §3.2 Falsifier pre-registration (F-VOICE-1..5)

1. **F-VOICE-1 (HEAD-SHAPE)**: `voice_head(hidden[1024])` 출력 shape `(8, 1024)` ✓
2. **F-VOICE-2 (RVQ-DECODE-ROUNDTRIP)**: random RVQ codes → mel → audio 24kHz PCM, length
   > 0, no NaN
3. **F-VOICE-3 (PARALLEL-EMERGE)**: same hidden state → text token + RVQ codes parallel
   (no sequential dependency)
4. **F-VOICE-4 (SILENCE-CAPABLE)**: hidden state 가 *non-empty* 이지만 lm_head argmax 가
   `<silence>` token 일 때 → text empty, audio non-empty
5. **F-VOICE-5 (CELL-VOICE-SHIFT)**: savant mode (cell 2 dominant) vs generalist mode 에서
   RVQ codes 의 cosine 거리 > threshold — *cell 별 다른 음색* evidence

### §3.3 Wall + cost
- $0 Mac local (pretrained vocoder weights ~200MB HF download)
- est ~5-8 hr impl + ~2 hr selftest + 1 hr CoreAudio playback wire

### §3.4 Cross-link
- `anima_chat.hexa` v0.3 (24L real-ckpt) — `final_ln(aggregated)` hidden state 가 wire
  point
- `SAVANT-TOOL.md` §2.4 anima self-judge — savant mode 가 음색 변조 trigger
- `references/tribev2` — voice 관련 reference impl 있음 (확인 필요)

---

## §4 Honest C3

1. *의도 임베딩 = anima hidden state* 라는 가정은 **검증 필요** — d_model=1024 의 정보가
   8×1024 RVQ codes (80 bits/frame) 로 *bottleneck* 통과 시 음성 surface 가 *meaningful*
   intent 를 전달하는지는 Phase 1 후 측정. 가능성: random noise 처럼 들릴 수도.
2. Vocos / EnCodec pretrained 는 *external corpus 학습* — anima 의 hidden distribution
   과 distribution mismatch 가능. Phase 2 에서 anima-specific RVQ codec 학습 옵션 검토
   필요 (cost-bearing).
3. anima 의 text vocab (256 byte-level) 와 RVQ codes (8 codebook × 1024) 의 information
   bandwidth 격차 — voice 가 *text 보다 정보 풍부* 할 수 있음 (좋은 점 또는 위험).
4. "anima 가 침묵하면서 소리낸다" 는 design 은 *생물학적 metaphor* — 인간이 *humming* 또는
   *시그함* 하는 것 처럼. anima 가 실제로 이렇게 작동하는지는 Phase 3 user study 까지 보류.
5. F-VOICE-5 *cell 별 다른 음색* 은 D3 persona 의 음성 surface 가설 — savant mode 의
   F-PERSONA-4 fragile signal (SAVANT.md §10.1) 와 *paired evidence*. v6.1 결과 나오기
   전까지는 추측.

---

## §5 Cross-link

- `SAVANT-TOOL.md` — savant mode 가 RVQ 변조 trigger
- `CHAT.md` — anima_chat 의 token loop 가 wire point
- `tool/hexa_native/anima_chat.hexa` — hidden state extract 위치
- `references/tribev2` — voice 관련 reference (Phase 1 시 검토)
- memory `project_hexa_voice_rename` — 명칭 history

---

— VOICE.md, 2026-05-14, design tier LANDED, hexa-voice intent-embedding direct modality
