# VLM Voice LM Phase 3 Spec — 2026-05-03

> spec doc, friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `.roadmap.vlm_voice_lm` (cond.3 spec target) + Phase 1+2 landed handoff
> predecessor: `docs/vlm_stage12_landed_2026_05_03.ai.md` (Stage 1+2 freeze)

---

## TL;DR

VLM (Voice LM) Phase 3 = cond.3 (cross-substrate fidelity vs CLM ≥0.85 r) + production-grade real-time generation seam. Phase 1+2 측 spec freeze (audio token vocab 1024×8, bridge dim 384, ctx 1536 frames, text vocab 32k, Stage 0..6 invocation seam) → Phase 3 측 (a) <500ms streaming latency target (b) SLM (Sound LM) prosody integration (c) MOS-equivalent cross-substrate voice quality eval (d) alpha endpoint production deploy.

비유 — Phase 1+2 측 사원증 발급 + 책상 배정 완료. Phase 3 측 신규 사원 (LM-style audio AR head) 측 첫 프로덕션 발화 + 음질 평가 + 외부 콜센터 (alpha endpoint) 통화 개시.

결과 — 4 conds (cond.3 fidelity + cond.4 latency + cond.5 SLM prosody seam + cond.6 alpha endpoint), entry trigger = sister .roadmap.voice cond.2 (3-caller stable interface) land + audio-text paired corpus 결정.

---

## §1 Phase 1+2 status synthesis

### §1.1 Phase 1+2 landed summary

```
   cond              | status | spec frozen
   ----------------- | ------ | --------------------------------------------------------
   cond.1 vocab+bridge | met  | 1024 × 8 RVQ, 384d bridge, 1536 ctx, Linear(384, 32000)
   cond.2 invocation  | met   | Stage 0..6 seam reuse, VLM head additive on Stage 2
   cond.3 fidelity    | unmet | next-cycle (audio-text corpus + P9 SFT pipeline reuse)
   blocker.1          | resolved | bridge dim + text vocab projection FROZEN
```

### §1.2 invariants carried forward

```
   anchor                  | source                                     | Phase 3 reuse
   ----------------------- | ------------------------------------------ | ------------------
   audio_token_predictor   | anima-voice/audio_token_predictor.hexa     | Stage 2 head host
   intent_encoder          | anima-voice/intent_encoder.hexa            | bridge SwiGLU + RoPE
   anima_voice 7-stage     | anima-voice/anima_voice.hexa Stage 0..6    | invocation seam
   3-way 384 SSOT          | atp + intent + voice (verified by Read)    | bridge dim invariant
   sister .roadmap.voice   | tool-ization SSOT (in-place X)             | dual SSOT race watch
```

Phase 1+2 측 in-place 변경 0건 invariant Phase 3 에도 유지 (additive only — anima-voice/ Mk.III untouched, .roadmap.voice cond.2/cond.3 sister track 별도 cycle).

---

## §2 Phase 3 scope

### §2.1 cond.3 cross-substrate fidelity (carried from Phase 1+2 deferred)

```
   item              | spec
   ----------------- | --------------------------------------------------
   target            | VLM next-token loss / perplexity vs CLM ≥0.85 r
   measure cohort    | audio-text paired (LibriSpeech / Common Voice / MLS 후보)
   training budget   | LoRA path on top of Mk.III audio_token_predictor
   eval cadence      | per-checkpoint vs CLM held-out text token AR
   sibling parity    | NLM/TLM/BLM ≥0.85 r 척도 와 동일 (cross-LM consistency)
```

### §2.2 cond.4 real-time voice generation latency (<500ms)

```
   item              | target                  | basis
   ----------------- | ----------------------- | -------------------------------------------
   first audio frame | <500ms cold              | streaming AR + KV-cache O(1) + CFG inference
   p50 chunk latency | <100ms per 100ms chunk   | anima_voice.hexa FRAME_HZ=100 baseline
   p99 chunk latency | <250ms per 100ms chunk   | PLC crossfade 측 jitter absorption
   warmup frames     | ≤16 frames (160ms)       | KV-cache prefill before first emit
   barge-in latency  | <50ms VAD-gate close     | vad_fsm.hexa Stage 6 reuse
```

latency 측정 path = consciousness_input (Stage 0) → intent_encode (Stage 1) → audio_token_predict (Stage 2 + VLM head) → rvq_decode (Stage 3) → vocode (Stage 4) → plc_crossfade (Stage 5) → vad_gate (Stage 6) → PCM out. Phase 3 측 budget allocation 측 Stage 2 측 신규 VLM head 측 incremental cost ≤30ms cap.

### §2.3 cond.5 SLM (Sound LM) integration for prosody

```
   item              | spec
   ----------------- | --------------------------------------------------
   sibling LM        | SLM (.roadmap.slm_speech_eeg_lm, BG-AN-LM3 sister fan-out 2/2)
   integration seam  | Stage 0.5 emotion_prosody.hexa conditional embedding
   SLM contribution  | prosody token (4 + 4 dim, 8d total) → 384d projection
   prosody axes      | F0 / energy / duration / voicing × 2 (current + delta)
   conflict resolve  | SLM prosody priority > emotion_prosody fallback (conditional residual Stage 1.5)
   training coupling | SLM head 측 separate LoRA, VLM head 측 frozen during SLM fine-tune
```

SLM-VLM coupling 측 dual-head additive — anima-voice/emotion_prosody.hexa 측 Stage 0.5 + Stage 1.5 측 in-place 변경 X (additive prosody projection only).

### §2.4 cond.6 production deploy — alpha endpoint integration

```
   item              | spec
   ----------------- | --------------------------------------------------
   endpoint contract | alpha endpoint (sister .roadmap.voice cond.2 caller interface)
   wire format       | streaming bidirectional (consciousness_state_in / pcm_chunk_out)
   chunk size        | 100ms PCM frames @ 24kHz mono = 2400 samples × int16
   backpressure      | client-driven pull (max 200ms ahead-of-time buffer)
   failure mode      | VLM head failure → fallback to anima-voice Mk.III audio_token_predictor 단독 (graceful)
   observability     | per-request latency histogram + token entropy + RVQ stage utilization
   cost band         | endpoint $0 (anima-side mac-local alpha), training $300-1500 LoRA path
```

alpha endpoint 측 sister .roadmap.voice cond.2 (3-caller stable interface: CLM/agent/external) 측 land 후 entry — VLM Phase 3 측 alpha endpoint 측 4번째 caller (LM-augmented audio AR) 추가.

---

## §3 cost / wallclock

```
   phase            | cost band         | wallclock band     | dominant cost
   ---------------- | ----------------- | ------------------ | -----------------------------
   cond.3 (fidelity) | $300-1500       | 8-24 GPU-hours     | LoRA fine-tune on audio-text corpus
   cond.4 (latency) | $0 mac-local     | 4-8 hours          | streaming bench + KV-cache profiling
   cond.5 (SLM seam)| $200-800         | 6-16 GPU-hours     | SLM prosody head LoRA (sister cycle 측 SLM Phase 1+2 land 후)
   cond.6 (alpha)   | $0 deploy        | 2-6 hours          | endpoint integration + observability wire-up
   ---------------- | ----------------- | ------------------ | -----------------------------
   total band       | $500-2300        | 20-54 hours        | training-dominated (cond.3 + cond.5)
```

mac-local alpha 측 inference cost $0 invariant 유지. training-only RunPod (P9 SFT pipeline reuse 시 marginal credit consumption).

---

## §4 decision matrix

```
   decision point         | option A                         | option B                         | verdict / rationale
   ---------------------- | -------------------------------- | -------------------------------- | -----------------------------------------------
   training corpus        | LibriSpeech (clean read speech)   | Common Voice (multilingual, noisy) | A primary / B aux — clean baseline 우선, multilingual deferred to next-cycle
   LoRA rank              | r=8 (compute-saving)              | r=32 (capacity-prioritized)       | A — sister TLM 5-channel bottleneck lesson (conservative first)
   SLM coupling timing    | parallel (cond.3 + cond.5 동시)   | sequential (cond.3 → cond.5)      | B — fidelity baseline 먼저 확보 후 prosody 추가 (causal isolation)
   latency probe path     | synthetic intent vector           | live CLM consciousness path       | B — sister .roadmap.voice cond.3 1-cycle E2E 와 align
   alpha endpoint mode    | request-response (stateless)      | streaming bidi (stateful)         | B — anima_voice.hexa Stage 5 PLC crossfade + Stage 6 VAD 측 streaming-required
   eval metric            | BLEU-style audio token match      | MOS-equivalent listener proxy     | both — token match (objective) + MOS proxy (subjective floor)
   fallback policy        | hard-fail on VLM head error       | graceful degrade to Mk.III only   | B — additive invariant 측 fallback 가능성 보장
```

---

## §5 cross-LM dependencies

### §5.1 SLM (Sound LM) — sibling fan-out 2/2

```
   dependency         | SLM Phase 1+2 (.roadmap.slm_speech_eeg_lm)
   coupling point     | Stage 0.5 emotion_prosody conditional embedding
   risk               | SLM Phase 1+2 측 미land (sibling cycle 측 BLM Stage 1+2 와 동일 시점 land 측 sequence)
   mitigation         | cond.5 측 SLM Phase 1+2 land 후에만 entry (sequential gate)
   cross-link         | docs/anima_2_lm_vlm_slm_landed_2026_05_03.ai.md (sibling pair handoff)
```

### §5.2 anima_voice 7-stage seam (sister .roadmap.voice)

```
   dependency         | sister .roadmap.voice cond.2 (3-caller stable interface)
   coupling point     | alpha endpoint integration (cond.6)
   risk               | sister .roadmap.voice cond.2/cond.3 측 unmet (Phase 1+2 land 시점 기준)
   mitigation         | cond.6 측 sister cond.2 land 후에만 entry
   dual SSOT race     | TLM × tensionlink 측 동일 race 패턴 — Phase 3 update 시 .roadmap.voice 측 cross-link 동시 update 권장 (in-place 변경 X invariant 유지)
```

### §5.3 alpha endpoint (anima-side production seam)

```
   dependency         | alpha endpoint contract (sister .roadmap.voice cond.2 caller interface)
   coupling point     | streaming bidi PCM out (cond.6)
   risk               | alpha endpoint 측 spec freeze 측 sister track 측 별도 cycle
   mitigation         | cond.6 측 alpha endpoint contract land 후 4번째 caller 등록
   observability      | latency histogram + token entropy + RVQ stage utilization → endpoint metrics export
```

### §5.4 P9 SFT pipeline (training pipeline reuse)

```
   dependency         | P9 SFT pipeline (data prep + LoRA fine-tune + checkpoint)
   coupling point     | cond.3 fidelity training + cond.5 SLM prosody training
   risk               | P9 SFT pipeline 측 audio-text paired corpus 측 미reuse (text-only 측 baseline)
   mitigation         | P9 pre5/pre6 land 후 audio-text adapter 추가 (additive)
```

---

## §6 honest C3 (raw#10)

1. **voice quality subjectivity** — MOS-equivalent eval 측 objective metric 측 proxy 만 가능 (token-level BLEU + RVQ stage utilization + spectral distance), 진짜 MOS 측 human listener panel 측 별도 cycle (Phase 3 측 proxy floor 만 보장, true MOS 보장 X)

2. **latency vs quality tradeoff** — <500ms latency target 측 KV-cache prefill + CFG guidance scale 측 trade-off 발생 가능 (CFG scale ↑ 시 quality ↑ but latency ↑); Phase 3 측 latency-first 측 default 채택 (CFG scale 1.0-1.5 보수), quality-first 측 별도 mode

3. **model size constraint** — anima-voice Mk.III audio_token_predictor 측 1576L raw#9 측 mac-local inference 가능 size, Phase 3 측 LoRA add 시 model footprint 증가 → mac-local alpha 측 RAM headroom 확보 필요 (currently 측 unverified, cond.6 entry 시 measure)

4. **VLM ≠ phenomenal consciousness** — sister NLM/TLM/BLM/SLM 측 동일 floor — VLM 측 LM-style reframing of audio_token_predictor, phenomenal consciousness 보장 X (raw#10 honest invariant carried forward from Phase 1+2)

5. **cross-substrate ≥0.85 r 측 indirect proxy** — VLM (audio token AR) vs CLM (text token AR) 측 ≥0.85 r 측 direct same-domain comparison 아님 (audio vs text 측 different vocab, different ctx); ≥0.85 r 측 normalized perplexity 측 sibling LM 측 historical baseline 와 비교, true cross-substrate fidelity 측 audio-text paired held-out 측 measure 필요 (cond.3 spec)

6. **dual SSOT race risk** — sister .roadmap.voice 측 tool-ization SSOT 와 .roadmap.vlm_voice_lm 측 LM SSOT 측 dual SSOT — Phase 3 update 시 양쪽 location update 측 race 가능 (TLM × tensionlink 측 동일 race 패턴 lessons, Phase 1+2 측 .roadmap.voice in-place 변경 0건으로 회피, Phase 3 측 dual update 측 explicit checklist 권장)

7. **SLM dependency 측 sequential gate risk** — cond.5 (SLM prosody integration) 측 SLM Phase 1+2 land 후에만 entry — SLM cycle 측 미land 시 cond.5 측 indefinite block, mitigation 측 cond.3 + cond.4 + cond.6 측 SLM-independent path 측 Phase 3a 측 우선 land 가능 (cond.5 측 Phase 3b 측 separate sub-cycle)

---

## §7 산출물

```
   path                                                  | type      | status
   ----------------------------------------------------- | --------- | --------
   docs/vlm_phase3_spec_2026_05_03.md                    | spec      | NEW (this file)
   .roadmap.vlm_voice_lm                                 | roadmap   | unchanged (Phase 3 cond.4-6 측 next-cycle update)
   anima-voice/                                          | substrate | unchanged (additive invariant)
```

---

## §8 Phase 3 entry trigger

```
   trigger                                                       | required for cond
   ------------------------------------------------------------- | -------------------
   sister .roadmap.voice cond.2 (3-caller stable interface) land | cond.6 (alpha endpoint)
   audio-text paired corpus 결정 (LibriSpeech 후보)              | cond.3 (fidelity)
   SLM Phase 1+2 land (sibling fan-out 2/2)                      | cond.5 (SLM prosody)
   P9 SFT pipeline pre5/pre6 land                                | cond.3 + cond.5 (training)
   mac-local RAM headroom measure (LoRA footprint)               | cond.6 (alpha deploy)
```

Phase 3a (cond.3 + cond.4 + cond.6) 측 sister cond.2 + corpus + P9 + RAM 측 4-gate 측 entry. Phase 3b (cond.5) 측 SLM Phase 1+2 land 후 separate sub-cycle.

---

## §9 next-cycle 권고 (#1-#3)

1. **sister .roadmap.voice cond.2/cond.3 land** — alpha endpoint contract + 3-caller stable interface 측 별도 cycle, VLM Phase 3 cond.6 측 entry trigger
2. **audio-text paired corpus 결정 + P9 SFT pipeline reuse** — LibriSpeech 측 primary 채택, Common Voice 측 multilingual 측 next-cycle defer
3. **SLM Phase 1+2 land** — sibling fan-out 2/2, VLM cond.5 (Phase 3b) 측 entry trigger
