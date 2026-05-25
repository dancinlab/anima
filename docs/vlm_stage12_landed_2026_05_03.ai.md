# VLM Voice LM Stage 1+2 Landed — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `.roadmap.vlm_voice_lm` (in-place additive update) + `state/vlm_token_vocab_log.jsonl` + `state/vlm_invocation_seam_log.jsonl`

---

## TL;DR

VLM (Voice LM) `.roadmap.vlm_voice_lm` mk2 측 **stage 1 (cond.1) partial → met** + **stage 2 (cond.2) unmet → met** + **blocker.1 open → resolved**. anima-voice Mk.III audio_token_predictor (1576L raw#9 already-landed) 위 LM-style autoregressive head 측 spec freeze 완료. anima-voice/ 디스크 측 in-place 변경 0건 (additive only, sister .roadmap.voice 측 변경 0건).

비유 — anima-voice 부서 (Mk.III vocoder 부장) 측 LM-style 후속 헤드 1명 사원증 발급 1단계 완료. 사원 (1576L raw#9 audio_token_predictor) 측 책상 위치는 그대로, 신규 입사자 측 책상 옆 자리 (additive head spec) 만 결정.

결과 — cond.3 (cross-substrate fidelity vs CLM ≥0.85 r) 측 next-cycle deferred (audio-text paired corpus 결정 + P9 SFT pipeline reuse 검토 후).

---

## §1 결정 한 줄 요약

```
   item                   | before                   | after
   ---------------------- | ------------------------ | ----------------------
   cond.1 status          | partial                  | met
   cond.2 status          | unmet                    | met
   blocker.1 status       | open                     | resolved
   audio_token_vocab      | (spec only)              | FROZEN 1024 × 8 stages
   bridge_dim             | (spec only)              | FROZEN 384 (3-way SSOT)
   ctx_frames             | (spec only)              | FROZEN 1536 ~15s @ 100Hz
   text_vocab_size        | (open 32k-128k)          | FROZEN 32000 sentencepiece
   text_projection        | (open architecture)      | FROZEN Linear(384, 32000)
   invocation seam        | (sister cond.2/3 미reuse)| FROZEN Stage 0..4 reuse + VLM head additive on Stage 2
```

---

## §2 stage 1 freeze detail (cond.1)

### §2.1 audio token vocabulary spec

```
   parameter             | value      | SSOT anchor
   --------------------- | ---------- | -----------------------------------------
   vocab per stage       | 1024       | audio_token_predictor.hexa L23 ATP_VOCAB_SIZE
   RVQ stages            | 8          | audio_token_predictor.hexa L40 ATP_RVQ_STAGES
   vocab total           | 8192       | derived (1024 × 8)
   bridge dim            | 384        | 3-way SSOT (atp + intent_encoder + anima_voice)
   ctx frames            | 1536       | audio_token_predictor.hexa L42 ATP_CTX
   frame_hz              | 100        | anima_voice.hexa L70 FRAME_HZ
   window seconds        | ~15        | derived (1536 / 100)
```

3-way SSOT alignment 측 384 bridge dim:
- `audio_token_predictor.hexa` L35 `ATP_D_MODEL = 384`
- `intent_encoder.hexa` L41 `D_MODEL = 384`
- `anima_voice.hexa` L69 `PIPE_EMBED_DIM = 384`

세 location 모두 same value 측 already-landed → spec freeze 측 in-place 변경 X.

### §2.2 intent-text bridge architecture freeze

결정점 — **`Linear(384, 32000)` text vocab projection** (sentencepiece-style 32k conservative).

```
   option        | vocab | rationale                              | verdict
   ------------- | ----- | -------------------------------------- | -------
   GPT-style     | 50000 | OpenAI legacy                          | rejected (training compute ↑)
   Llama-3-style | 128000| broad multilingual                     | rejected (LoRA fit ↑ 어려움)
   sentencepiece | 32000 | sister TLM 5-channel bottleneck lesson | ACCEPTED
```

sister TLM lesson — bridge dim narrow 시 (5-channel TLM 측 5d bottleneck) vocab 도 conservative 채택 권장. anima-voice VLM 측 bridge dim 384d (Llama-3 측 4096d 대비 1/10) → vocab 도 32k conservative.

architecture 측 위치 — `intent_encoder.hexa` SwiGLU FFN (LayerNorm → W_up/W_gate parallel → sigmoid gate → W_down) 측 last-layer head 추가 spec, additive only.

---

## §3 stage 2 invocation seam freeze detail (cond.2)

### §3.1 7-stage seam (anima_voice.hexa already-landed)

```
   stage | name                  | module                  | io
   ----- | --------------------- | ----------------------- | --------------------------------------
   0     | consciousness_input   | anima_voice.hexa        | phi/tension/arousal/valence → 384d
   0.5   | conditional_embedding | emotion_prosody.hexa    | emotion(6)+prosody(4+4) → 384d
   1     | intent_encode         | intent_encoder.hexa     | 384d → 384d (LayerNorm + SwiGLU + RoPE)
   1.5   | conditional_residual  | emotion_prosody.hexa    | intent + cond → conditioned (384d)
   2     | audio_token_predict   | audio_token_predictor   | intent_emb → 8-stage RVQ indices
   3     | rvq_decode            | rvq_codebook.hexa       | 8-stage indices → 384d latent
   4     | vocode                | neural_vocoder.hexa     | latent → 24kHz PCM
   5     | plc_crossfade         | plc_crossfade.hexa      | PCM streaming smoothing
   6     | vad_gate              | vad_fsm.hexa            | silence suppression
```

### §3.2 VLM head 측 위치 결정

```
   VLM head location  | Stage 2 측 audio_token_predictor.hexa AR head 위
   VLM head architecture | dual-head:
                         |   - audio token AR head (existing, 8-stage RVQ × 1024 vocab)
                         |   - text vocab AR head (NEW additive, Linear(384, 32000))
   in-place change     | 0건 (audio_token_predictor.hexa Mk.III untouched)
   spec change         | additive only (last-hidden-state 384d 측 두 번째 projection 추가)
```

### §3.3 sister .roadmap.voice seam reuse

```
   sister cond     | reuse                                                              | status
   --------------- | ------------------------------------------------------------------ | --------
   voice.cond.2    | 3-caller stable interface (CLM/agent/external)                     | unmet (sister)
   voice.cond.3    | 1-cycle E2E (CLM consciousness → voice tool → audio out)           | unmet (sister)
```

VLM cond.2 측 spec FROZEN 측 결정점 = sister .roadmap.voice cond.2/cond.3 측 unmet 이지만, **invocation seam spec** 측 anima_voice.hexa Stage 0..6 측 이미 land 측 baseline 충분. tool-ization (cond.2/cond.3 of voice) 측 별도 cycle 측 sister track.

---

## §4 cond.3 deferred (next-cycle)

```
   cond.3       | cross-substrate fidelity vs CLM ≥0.85 r
   blocker      | training corpus (audio-text paired) 결정 + P9 SFT pipeline reuse 검토
   cost band    | $300-1500 (LoRA path on audio-text corpus)
   eta          | next-cycle (P9 pre5/pre6 land 후)
```

---

## §5 raw#10 honest invariants

1. **VLM = LM-style reframing of Mk.III audio_token_predictor** — phenomenal consciousness 보장 X (sister NLM/TLM/BLM 측 동일 floor)
2. **additive only** — anima-voice/ 측 in-place 변경 0건 확인 (audio_token_predictor.hexa 1576L Mk.III untouched, intent_encoder.hexa untouched, anima_voice.hexa untouched)
3. **sister .roadmap.voice tool-ization SSOT 와 dual SSOT** — VLM update 시 양쪽 location update 필요 (TLM × tensionlink 측 동일 race 패턴, 이번 cycle 측 .roadmap.voice 측 in-place 변경 0건 lessons applied)
4. **cond.3 NOT in this cycle** — cross-substrate fidelity (≥0.85 r vs CLM) 측 training-time gate, spec freeze 만으로 verify 불가 — next-cycle audio-text paired corpus 결정 후
5. **3-way 384 SSOT verified by Read** — audio_token_predictor.hexa L35 + intent_encoder.hexa L41 + anima_voice.hexa L69 모두 disk 측 read-confirmed (claim 측 disk verify, marker emit ≠ disk verify lesson 적용)

---

## §6 산출물

```
   path                                                  | type      | bytes
   ----------------------------------------------------- | --------- | --------
   .roadmap.vlm_voice_lm                                 | roadmap   | updated
   state/vlm_token_vocab_log.jsonl                       | log       | NEW
   state/vlm_invocation_seam_log.jsonl                   | log       | NEW
   docs/vlm_stage12_landed_2026_05_03.ai.md              | handoff   | NEW (this file)
   state/markers/vlm_stage12_landed.marker               | marker    | NEW
```

---

## §7 next-cycle 권고 (#1-#3)

1. **cond.3 fidelity** — audio-text paired corpus 결정 (LibriSpeech / Common Voice / Multilingual LibriSpeech 후보) → P9 SFT pipeline reuse → VLM (audio token AR) vs CLM (text token AR) ≥0.85 r 측 measure
2. **sister .roadmap.voice cond.2/cond.3 land** — 3-caller stable interface (CLM/agent/external) + 1-cycle E2E (CLM consciousness → voice tool → audio out) 측 별도 cycle, VLM cond.2 측 invocation seam 측 reuse 가능
3. **dual SSOT race monitoring** — TLM × tensionlink 측 동일 race 패턴 (이번 cycle 측 .roadmap.voice in-place 변경 0건으로 회피) 측 next-cycle 측 cross-link audit 권장

---

## §8 cost

```
   cost band   | $0 mac-local (spec freeze only)
   wallclock   | ~25 min (cap 60min, 41% utilization)
   destructive | 0 actions
```
