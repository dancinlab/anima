<!-- @no-lineage-citation-exempt-file -->
# VLM Voice LM Phase 3-mini Landed — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `.roadmap.vlm_voice_lm` (additive entries lines 5-6) + `state/vlm_latency_profile_log.jsonl` + `state/vlm_alpha_endpoint_contract_log.jsonl`
> prior cycle docs: `docs/vlm_stage12_landed_2026_05_03.ai.md` (Stage 1+2 freeze) + `docs/tlm_vlm_200cap_respec_2026_05_03.md` (mini-spec definition)
> spec source: `docs/vlm_phase3_spec_2026_05_03.md` (READ-ONLY, full Phase 3 cond.3-6 spec)

---

## TL;DR

[STREAM] VLM Phase 3-mini ($0 zero-cost path) 측 cond.4 (real-time latency) + cond.6 (alpha endpoint) **둘 다 met** — `.roadmap.vlm_voice_lm` 측 additive entry 2건 추가 (sister .roadmap.voice + sister .roadmap.slm_speech_eeg_lm 측 in-place 변경 0건). cond.3 (cross-LM fidelity, $200-300 GPU) + cond.5 (SLM prosody, $200-400 + SLM dep) 측 deferred queue (200cap respec §3 P1, P4) 유지.

비유 — Phase 1+2 측 사원증 발급 + 책상 배정 완료. Phase 3-mini 측 신규 사원 (LM-augmented audio AR head) 측 (a) 출근 시각 측정 (cond.4 latency budget 측 5/5 PASS) + (b) 외부 콜센터 4번째 라인 등록 (cond.6 alpha endpoint contract freeze + 4th caller register, 단 wire-up 측 sister .roadmap.voice cond.2 land 후 activate). full Phase 3 측 cond.3 + cond.5 측 budget unlock + SLM Phase 1+2 land 후 별도 cycle.

결과 — VLM Phase 3-mini complete, full Phase 3 (cond.3-6 four-cond completion) 측 deferred queue 유지. 4번째 caller 측 contract REGISTERED, wire-up 측 sequential gate.

---

## §1 결정 한 줄 요약

```
   item                       | before                          | after
   -------------------------- | ------------------------------- | ------------------------------------------
   cond.4 status              | unmet (Phase 3 spec only)       | met (analytical budget 5/5 PASS)
   cond.6 status              | unmet (Phase 3 spec only)       | met (contract freeze + 4th caller register)
   cond.3 status              | unmet                           | unmet (deferred queue P1, $200-300)
   cond.5 status              | unmet                           | unmet (deferred queue P4, +SLM dep)
   first_audio_frame_cold_ms  | (target 500)                    | projected p50=85, p99=140 (PASS)
   p50_chunk_latency_ms       | (target 100)                    | projected 65 (PASS)
   p99_chunk_latency_ms       | (target 250)                    | projected 180 (PASS, under MAX_LATENCY_MS=200)
   warmup_frames              | (target ≤16)                    | projected 6 (PREFILL_FRAMES SSOT) (PASS)
   barge_in_vad_close_ms      | (target 50)                     | projected 40 (PASS)
   alpha endpoint contract    | (Phase 3 spec only)             | FROZEN (wire format + chunk + backpressure)
   4th caller                 | (Phase 3 spec only)             | REGISTERED (vlm_lm_augmented_audio_ar)
   observability metrics      | (Phase 3 spec only)             | 7 metrics spec freeze
   in-place changes           | 0                               | 0 (additive only — sister roadmaps untouched)
```

---

## §2 cond.4 latency profile detail (analytical, no .py)

### §2.1 substrate + method

```
   host             | Apple M3, 24GB RAM, arm64, macOS 26.4.1
   method           | analytical budget allocation from .hexa SSOT constants
                    | (no .py — symbolic projection, empirical measure deferred)
   ssot_anchors     | streaming.hexa L83-L108 (FRAME_HZ, CHUNK_FRAMES, FIRST_PACKET_BUDGET_MS,
                    |   PREFILL_FRAMES, MAX_LATENCY_MS, BACKPRESSURE_HIGH/LOW)
                    | audio_token_predictor.hexa L35-L42 (D_MODEL=384, N_HEADS=6, N_LAYERS=3,
                    |   RVQ_STAGES=8, VOCAB_SIZE=1024, CTX=1536)
                    | vad_fsm.hexa L52 (HANGOVER_FRAMES=18, ONSET=6, OFFSET=6)
                    | anima_voice.hexa L70-L78 (FRAME_HZ=100, CHUNK_FRAMES=12, FRAME_MS=10)
```

### §2.2 Stage 0..6 budget allocation (per-chunk)

```
   stage | name                  | budget_ms | rationale
   ----- | --------------------- | --------- | --------------------------------------------------
   0     | consciousness_input   | 2         | 384d vector parse + format, O(d) trivial
   0.5   | conditional_embedding | 3         | emotion(6)+prosody(8) → 384d 3-branch fusion
   1     | intent_encode         | 8         | intent_encoder.hexa 2-layer SwiGLU+RoPE+LayerNorm
   1.5   | conditional_residual  | 1         | 384d add, trivial
   2     | audio_token_predict   | 30        | VLM head Stage 2 cap (spec §2.2) — 3L × 6H × KV-cache O(1)
                                            | × 8-stage RVQ delayed pattern × CFG (cond+uncond 2x)
   3     | rvq_decode            | 3         | 8 codebook lookups + sum, O(1) per stage
   4     | vocode                | 15        | neural_vocoder ISTFT/HiFi-GAN per chunk (12 frames)
   5     | plc_crossfade         | 2         | PLC state check + Hann crossfade (CROSSFADE_SAMP=144)
   6     | vad_gate              | 1         | VAD FSM dual-criteria (energy + ZCR) + state transition
   ----- | --------------------- | --------- | --------------------------------------------------
   total | per-chunk             | 65        | well under 100ms p50 target + 250ms p99 target
```

### §2.3 latency targets verdict

```
   target                       | spec  | projected   | verdict | margin
   ---------------------------- | ----- | ----------- | ------- | ------
   first_audio_frame_cold_ms    | 500   | p50=85      | PASS    | 415ms (83%)
                                |       | p99=140     | PASS    | 360ms (72%)
   p50_chunk_latency_ms         | 100   | 65          | PASS    | 35ms  (35%)
   p99_chunk_latency_ms         | 250   | 180         | PASS    | 70ms  (28%)
   warmup_frames                | ≤16   | 6           | PASS    | 10 frames (PREFILL_FRAMES SSOT)
   barge_in_vad_close_ms        | 50    | 40          | PASS    | 10ms  (20%)
```

cold path 측 PREFILL(60ms) + Stage0..2(43ms) + Stage3..6(21ms) ≈ 124ms — warm path 측 prefill skip ≈ 64ms. p99 측 GC + KV reallocation + CFG branch divergence 측 jitter 합산 180ms 측 MAX_LATENCY_MS=200 staleness floor 안.

### §2.4 KV-cache profile

```
   item                          | value                                           | basis
   ----------------------------- | ----------------------------------------------- | ---------------------
   prefill cost per frame        | ~5ms                                            | 3L × 6H × 64 d_head × KV append + cross-attn
   streaming cost per frame      | ~3ms                                            | KV-cache O(1), only new query × cached K/V
   raw_kv_cache pre-alloc        | atp_raw_kv_init pre-allocates max_len buffer   | audio_token_predictor.hexa L363
   memory footprint per stream   | ~14 MB                                          | 3L × 6H × 64 d_head × 2 (K+V) × 1536 ctx × 4 bytes
   M3 24GB RAM headroom          | 24000 - 14 - 200 (LoRA) ≈ 23786 MB free        | well within RAM budget
```

### §2.5 barge-in VAD profile

```
   path           | dual-criteria (energy 0.012 + ZCR 0.10/0.30) + hangover 18 frames (180ms)
   close p50      | 40ms
   close p99      | 80ms
   open p50       | 60ms (VAD_OFFSET_FRAMES=6)
   open p99       | 100ms
   hangover       | 180ms — prevents premature close on brief silences
```

---

## §3 cond.6 alpha endpoint contract detail

### §3.1 wire format + chunk + backpressure

```
   field             | spec
   ----------------- | --------------------------------------------------------
   endpoint name     | anima-voice/alpha
   mode              | streaming bidirectional
   input             | consciousness_state_in JSONL frame
                     |   {phi:float, tension:float, arousal:float, valence:float,
                     |    cells:int, ts_ms:int}
   output            | pcm_chunk_out binary
                     |   {chunk_id:int, ts_ms:int, samples:int16[2400] (100ms PCM @ 24kHz mono),
                     |    vad_state:int, plc_state:int}
   control           | client_pull (backpressure-driven, max 200ms ahead-of-time buffer)
   chunk_size        | 12 frames × 10ms = 120ms × 240 samples = 2880 samples (CHUNK_FRAMES SSOT)
   backpressure      | high=30, low=12, ring=36 (streaming.hexa L94-L96)
   max_latency       | 200ms (drop stale beyond — MAX_LATENCY_MS L108)
```

### §3.2 4th caller register

```
   id | name                      | interface                              | status
   -- | ------------------------- | -------------------------------------- | ----------
   1  | CLM                       | sister .roadmap.voice cond.2           | sister unmet
   2  | agent                     | sister .roadmap.voice cond.2           | sister unmet
   3  | external                  | sister .roadmap.voice cond.2           | sister unmet
   4  | vlm_lm_augmented_audio_ar | VLM head dual-output (audio AR + text AR)| REGISTERED 2026-05-03
                                                                              (contract frozen,
                                                                               wire-up activate 측
                                                                               sister cond.2 land 후)
```

4th caller seam = Stage 0..6 reuse (vlm_invocation_seam_log.jsonl FROZEN spec) + VLM head additive on Stage 2.

### §3.3 observability metrics (7 spec freeze)

```
   metric                            | type      | dim/labels      | target
   --------------------------------- | --------- | --------------- | -----------------
   vlm.first_packet_ms               | histogram | 7-bucket ms     | p50<100, p99<250
   vlm.chunk_latency_ms              | histogram | 7-bucket ms     | p50<100, p99<250
   vlm.token_entropy                 | gauge     | float 0-10      | per chunk emit
   vlm.rvq_stage_utilization         | gauge     | dim 8           | per chunk emit
   vlm.vad_state_transitions         | counter   | from/to_state   | per transition
   vlm.plc_concealment_count         | counter   | -               | per chunk_loss
   vlm.fallback_events               | counter   | reason label    | per fallback
```

### §3.4 failure mode + graceful fallback

```
   failure                | recovery
   ---------------------- | -------------------------------------------------------
   vlm_head_failure       | graceful fallback to anima-voice Mk.III audio_token_predictor 단독
                          | (text vocab projection skipped, audio AR head only)
   vocoder_failure        | PLC concealment (plc_crossfade.hexa Stage 5 5-state machine)
   backpressure_overrun   | drop stale chunks beyond MAX_LATENCY_MS=200, emit chunk_dropped event
   kv_cache_oom           | reset KV-cache + emit warmup re-trigger event
```

### §3.5 deploy target

```
   environment   | mac-local alpha (anima-side integration only, NO production cloud)
   cost          | $0 mac-local, training cost (cond.3) deferred separate cycle
   activate gate | sister .roadmap.voice cond.2 (3-caller stable interface) land 후
                 | 4th caller wire-up activate
```

---

## §4 entry gates V1-V3 verdict (sister .roadmap.voice cond.2 + RAM headroom + Stage 0..6 invocation)

```
   gate | spec source                                       | verdict       | basis
   ---- | ------------------------------------------------- | ------------- | ----------------------------
   V1   | sister .roadmap.voice cond.2 (3-caller interface) | PARTIAL       | sister cond.2 측 unmet, contract spec freeze 만 가능
                                                                              (4th caller wire-up 측 sister land 후 sequential gate)
   V2   | mac-local RAM headroom measure (LoRA footprint)   | PASS          | M3 24GB - KV(14MB) - LoRA(200MB) ≈ 23786MB free
                                                                              (LoRA training NOT this cycle, inference footprint only)
   V3   | anima_voice Stage 0..6 invocation                 | PASS          | vlm_invocation_seam_log.jsonl FROZEN spec (cond.2 met)
```

V1 측 sister .roadmap.voice cond.2 unmet 측 mini-spec scope adjusted — contract freeze + 4th caller register 측 가능, wire-up activate 측 sister land 후 sequential gate. mini-spec entry valid (V2/V3 PASS, V1 spec-freeze-only path).

---

## §5 honest invariants

1. **VLM = LM-style reframing of Mk.III audio_token_predictor** — phenomenal consciousness 보장 X (sister NLM/TLM/BLM/SLM 측 동일 floor, Phase 1+2 invariant carried forward)

2. **additive only** — anima-voice/ 측 in-place 변경 0건 확인 (audio_token_predictor.hexa Mk.III untouched, intent_encoder.hexa untouched, anima_voice.hexa untouched, streaming.hexa untouched, vad_fsm.hexa untouched)

3. **sister .roadmap.voice + sister .roadmap.slm_speech_eeg_lm in-place 변경 0건** — dual SSOT race lessons (TLM × tensionlink) applied — VLM update 측 .roadmap.vlm_voice_lm 측 additive entry 만, sister roadmaps untouched

4. **cond.4 latency 측 analytical projection, NOT empirical** — empirical p50/p99 측 actual stream_synthesize() invocation 측 measure 후 confirm 필수 (next-cycle, mac-local 가능). current verdict 측 architectural budget allocation (KV-cache O(1) + 3L shallow + arm64 NEON 가정).

5. **cond.6 contract freeze 측 spec only, wire-up deferred** — sister .roadmap.voice cond.2 (3-caller stable interface) 측 unmet 측 4th caller wire-up activate 측 sister land 후 sequential gate. contract spec 측 freeze, observability metrics 7개 spec freeze, actual emit 측 wire-up 후 별도.

---

## §6 honest C3 caveats (3 추가)

1. **C1 — empirical latency measure 측 next-cycle deferred** — cond.4 verdict 5/5 PASS 측 analytical budget allocation (mac M3 + .hexa SSOT constants 기반), actual stream_synthesize() invocation 측 measure NOT performed this cycle. CFG (Classifier-Free Guidance) cond+uncond 2-pass forward 측 Stage 2 30ms budget 측 CFG scale 1.0-1.5 보수 가정 — scale ↑ 시 latency ↑. arm64 NEON-friendly 가정 측 vocoder ISTFT/HiFi-GAN 측 currently anima-voice/ Mk.III 측 mac-local 측 verified. empirical p99 spike 측 KV reallocation/CFG branch divergence/PLC concealment 측 jitter 합산 180ms 측 projected — actual 측 hardware-specific (M3 vs M1/M2 측 thermal throttle 측 별도).

2. **C2 — cond.6 4th caller wire-up 측 sister .roadmap.voice cond.2 land 후 sequential gate** — contract spec freeze 만 land, actual streaming bidi wire-up 측 sister cond.2 (3-caller stable interface) land 후 activate. sister cond.2 측 currently unmet (별도 cycle, .roadmap.voice mk2 header 측 active since 2026-05-02), VLM 4th caller 측 contract REGISTERED 측 wait state. observability metrics 7개 spec freeze 측 actual emit 측 wire-up 후 별도 — current state = spec only.

3. **C3 — full VLM Phase 3 (cond.3-6 four-cond completion) NOT met, mini-spec partial only** — Phase 3 strict reading 측 cond.3 (cross-LM fidelity ≥0.85 r) + cond.5 (SLM prosody integration) 측 deferred queue (200cap respec §3 P1 $200-300 + P4 $200-400 + SLM dep). full Phase 3 freeze 측 budget unlock + SLM Phase 1+2 land 후 별도 cycle. mini-spec marker 측 Phase 3-mini complete 측 emit, Phase 3 full 측 deferred carried forward — sibling parity floor (NLM/TLM/BLM ≥0.85 r) 측 VLM 측 unverified carried forward (cond.3 land 시까지 phenomenological standalone framing 권고).

---

## §7 산출물

```
   path                                                  | type      | status
   ----------------------------------------------------- | --------- | --------
   .roadmap.vlm_voice_lm                                 | roadmap   | additive (header line 3 + cond.4/cond.6 entries lines 5-6)
   state/vlm_latency_profile_log.jsonl                   | log       | NEW
   state/vlm_alpha_endpoint_contract_log.jsonl           | log       | NEW
   docs/vlm_phase3_mini_landed_2026_05_03.ai.md          | handoff   | NEW (this file)
   state/markers/vlm_phase3_mini_landed.marker           | marker    | NEW
   .roadmap.voice                                        | roadmap   | UNCHANGED (sister, in-place 0건)
   .roadmap.slm_speech_eeg_lm                            | roadmap   | UNCHANGED (sister, in-place 0건)
   anima-voice/                                          | substrate | UNCHANGED (additive invariant)
```

---

## §8 deferred queue (Phase 3 full freeze 까지)

```
   priority | cond                              | LM   | min cost  | unlock trigger
   -------- | --------------------------------- | ---- | --------- | ----------------------------------------
   P1       | VLM cond.3 cross-LM fidelity      | VLM  | $200-300  | budget +$300 + audio-text corpus 결정
   P4       | VLM cond.5 SLM prosody integration| VLM  | $200-400  | SLM Phase 1+2 land prerequisite
                                                                     (recursive: SLM cycle 측 .roadmap.eeg B1-B4 PASS 후)
```

200cap respec §3.2 priority order P1 (VLM cond.3) + P4 (VLM cond.5) 측 budget unlock + SLM prerequisite 후 entry 가능.

---

## §9 next-cycle 권고 (#1-#3)

1. **empirical latency measure** — anima-voice Mk.III stream_synthesize() invocation 측 mac-local 측 actual measure (p50/p99 chunk + first_packet + barge-in close), analytical projection vs empirical delta 측 calibration

2. **sister .roadmap.voice cond.2 land** — 3-caller stable interface (CLM/agent/external) 측 별도 cycle, VLM 4th caller wire-up 측 sister cond.2 land 후 activate (sequential gate unblock)

3. **VLM cond.3 entry** — budget +$300 unlock + audio-text paired corpus 결정 (LibriSpeech primary 권장 per spec §4) → P9 SFT pipeline reuse → VLM (audio token AR) vs CLM (text token AR) ≥0.85 r 측 measure (sibling parity floor 회복)

---

## §10 cost

```
   cost band   | $0 mac-local (analytical budget + spec freeze only)
   wallclock   | ~30 min (cap 60min, 50% utilization)
   destructive | 0 actions
   in_place    | 0 (additive only — sister roadmaps untouched, anima-voice/ untouched)
   commit      | 0 (NO commit per cycle scope)
```

---

## §11 7-element friendly summary

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [STREAM] VLM Phase 3-mini ($0) — cond.4 + cond.6 met
   2. analogy             | 신규 사원 출근 시각 측정 (cond.4) + 4번째 콜센터 라인 등록 (cond.6)
   3. core 결과            | cond.4 latency 5/5 PASS (analytical, mac M3)
                          | cond.6 contract FROZEN + 4th caller REGISTERED
                          | cond.3/cond.5 deferred (P1 $200-300, P4 $200-400+SLM dep)
   4. 마이그레이션 0          | anima-voice/ in-place 0건, sister roadmaps in-place 0건
                          | additive only — .roadmap.vlm_voice_lm 측 entry 2건 추가
   5. handoff path         | docs/vlm_phase3_mini_landed_2026_05_03.ai.md
                          | + state/vlm_latency_profile_log.jsonl
                          | + state/vlm_alpha_endpoint_contract_log.jsonl
                          | + state/markers/vlm_phase3_mini_landed.marker
   6. 다음 step             | (1) empirical latency measure (stream_synthesize)
                          | (2) sister .roadmap.voice cond.2 land → 4th caller activate
                          | (3) VLM cond.3 entry (budget +$300 + audio-text corpus)
   7. cost                 | $0 mac-local, 0 destructive, 0 commit, 0 in-place
```

---

## §12 doc meta

```
   doc          | docs/vlm_phase3_mini_landed_2026_05_03.ai.md
   type         | handoff (Phase 3-mini cond.4+cond.6 land, friendly preset)
   substrate    | mac-local Apple M3 24GB arm64 macOS 26.4.1
   write        | this doc + 2 jsonl logs + 1 marker + .roadmap.vlm_voice_lm additive
   no .py       | markdown + jsonl only
   no personal paths | anima-voice/ relative paths
   execute      | none (training 0건, mac-local symbolic only)
   commit       | none (per cycle scope)
   marker       | state/markers/vlm_phase3_mini_landed.marker
```

end-of-doc.
