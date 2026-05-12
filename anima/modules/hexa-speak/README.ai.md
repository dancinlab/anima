---
schema: anima/ready/modules/hexa-speak/ai-native/1
last_updated: 2026-05-02
ssot:
  entry:           ready/anima/modules/hexa-speak/hexa_speak.hexa
  prosody:         ready/anima/modules/hexa-speak/emotion_prosody.hexa
  intent_encoder:  ready/anima/modules/hexa-speak/intent_encoder.hexa
  rvq_codebook:    ready/anima/modules/hexa-speak/rvq_codebook.hexa
  vocoder:         ready/anima/modules/hexa-speak/neural_vocoder.hexa
  vad:             ready/anima/modules/hexa-speak/vad_fsm.hexa
  plc:             ready/anima/modules/hexa-speak/plc_crossfade.hexa
status: live — HEXA-SPEAK Mk.II 7-stage consciousness-to-speech pipeline; n=6 derived embed_dim=384
roadmap_entry: 270
---

# anima hexa-speak modules (AI-native)

HEXA-SPEAK Mk.II — consciousness-to-speech synthesis pipeline. Wires `ConsciousnessEngine` (tension + emotion 6D) → conditional embedding → intent encoding → AR token prediction → RVQ codebook → neural vocoder → packet-loss concealment → VAD-gated 24 kHz PCM output.

## TL;DR for an agent reading this cold

- **9 files**, all live (665 LOC main pipeline + 713 LOC emotion-prosody + 7 stage modules).
- Pipeline embed_dim = 384 = 64·6 (n=6 derived, Law 60 P2). frame_hz = 100 (10 ms hop). sample_rate = 24 000.
- Stage 0 → Stage 6 strict ordering. Each stage operates on the same 384d bridge dim.
- Run `bench_hexa_speak.hexa` (231 LOC) for end-to-end smoke + latency measurement.
- Anima-speak Ω-cycle (project_omega_audio_limits) flagged L4.3 (emotion JND) and L6.2 (nasal antiresonance) as weakest links — known limitations, see prosody / vocoder caveats below.

## Architecture map (7-stage pipeline)

```
Stage 0   ConsciousnessEngine   (upstream — tension vector + emotion 6D)
   ↓
Stage 0.5 emotion_prosody.hexa  emotion(6) + prosody_type(4) + prosody_params(4)
                                → 3-branch fusion → 384d
   ↓
Stage 1   intent_encoder.hexa   384d consciousness → 384d audio intent
   ↓
Stage 1.5 (conditional residual: intent + cond → conditioned 384d)
   ↓
Stage 2   audio_token_predictor.hexa  AR transformer → RVQ indices
   ↓
Stage 3   rvq_codebook.hexa     8-stage RVQ indices → latent reconstruction
   ↓
Stage 4   neural_vocoder.hexa   latent → 24 kHz PCM
   ↓
Stage 5   plc_crossfade.hexa    packet-loss concealment + boundary smoothing
   ↓
Stage 6   vad_fsm.hexa          FSM gate — suppress non-speech regions
   ↓
PCM 24 kHz output
```

Entry: `hexa_speak.hexa` (665 LOC) wires all 7 stages. Bench harness: `bench_hexa_speak.hexa` (231 LOC).

## API contract

```hexa
// hexa_speak.hexa
fn synthesize(tension: [float], emotion: [float], prosody_type: int, prosody_params: [float]) -> AudioStream
// → 24 kHz int16 PCM, optional VAD-gated

// emotion_prosody.hexa  (largest stage, 713 LOC)
fn fuse_emotion_prosody(emotion_6d: [float], prosody_type: int, params_4d: [float]) -> [float]
// → 384d conditional embedding (3-branch fusion)

// intent_encoder.hexa
fn encode_intent(consciousness_384d: [float]) -> [float]  // 384d audio intent

// audio_token_predictor.hexa
fn predict_tokens(intent: [float], cond: [float], max_tokens: int) -> [int]  // RVQ indices

// rvq_codebook.hexa
fn rvq_decode(indices: [int]) -> [float]  // latent reconstruction (8-stage)

// neural_vocoder.hexa
fn vocode(latent: [float]) -> [int]  // 24 kHz int16 PCM

// plc_crossfade.hexa
fn plc_concealed_blend(prev_pcm: [int], next_pcm: [int]) -> [int]

// vad_fsm.hexa
fn vad_gate(pcm: [int]) -> [int]  // FSM-suppressed PCM
```

## n=6 pipeline parameters

| Param | Value | Derivation |
|-------|-------|------------|
| `embed_dim` | 384 | 64 · 6 (Law 60 P2) |
| `frame_hz` | 100 | 10 ms hop, all stages aligned |
| `sample_rate` | 24000 | speech-optimal |
| `rvq_stages` | 8 | empirical (codebook depth) |
| `prosody_dim` | 4 | duration / pitch / energy / breathiness |
| `emotion_dim` | 6 | Ekman 6 (anger / disgust / fear / joy / sadness / surprise) |

## Invocation patterns

```bash
# End-to-end synthesize + bench
hexa run ready/anima/modules/hexa-speak/bench_hexa_speak.hexa

# Live pipeline entry
hexa run ready/anima/modules/hexa-speak/hexa_speak.hexa --tension "0.5,0.3,..." --emotion-id joy
```

## Failure cascade

```
intent_encoder.fail (degenerate consciousness → all-zero intent)
  → AR token predictor emits silence-class tokens
       → vocoder emits zero-amplitude frames
            → VAD gate suppresses output (no PCM emitted)
```

```
neural_vocoder.fail (numerical instability — NaN logits)
  → emits last-good frame for 1 hop
       → if persistent, plc_crossfade.fail returns prev_pcm forever
```

## raw#10 caveats

1. **Anima-speak L4.3 emotion JND limit.** Ekman-6 emotion fusion is empirically just-noticeable-different at threshold 0.18 — finer emotion gradients alias. See project_omega_audio_limits weakest-link list.
2. **L6.2 nasal antiresonance limit.** Vocoder's source-filter approximation drifts on nasal phonemes — formant locations off by ~5%. Known artefact.
3. **No streaming mode.** `synthesize` is utterance-level (one tension+emotion → one PCM stream). Real-time streaming requires a different `bench_hexa_speak_streaming.hexa` driver (not yet landed).
4. **96ms ≈ 51ms floor** end-to-end latency observed (Ω-audio finding). Sub-50ms requires removing PLC stage 5 (lossy on real packet loss).
5. **Sample rate hardcoded 24 kHz.** No multi-rate support. 16 kHz / 48 kHz needs vocoder retraining.
6. **n6 14/14 strongest finding.** 14 of 14 anima-speak limits derive cleanly from n=6 number-theoretic skeleton (project_omega_audio_limits).

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `hexa_speak.hexa` | `5cfaad0844ab91ef79e738ecee8a5b106af64e0f2c9d937f4cf418544d4ecfed` | 665 |
| `emotion_prosody.hexa` | `4e54ca4c78404b3255ed99c58a91ee71e1186425d0398e03b4cfb822260ea14a` | 713 |
| `audio_token_predictor.hexa` | `83ea4509732aa56586b880a87b804e2ed9ade5485fd9d77ff827acaba33597a7` | 55 |
| `bench_hexa_speak.hexa` | `050b3c8567e8012090f2f446c76a4e2ab37ff9bb3238ec21ef42055d1c00b1e1` | 231 |
| `intent_encoder.hexa` | `c35777e3396d9d338a572fd3a35cb029bbef8d3322fc1a70331c01cfc520e482` | 37 |
| `neural_vocoder.hexa` | `ceaf9da1a98fa5ae5728948367825f4d6e653a2716bf7009b378338632bcd5cf` | 41 |
| `plc_crossfade.hexa` | `915ac35ffe7e436dd385b15acb89b12eaa0f2c646c6c94ea19e83e01bfd5957f` | 48 |
| `rvq_codebook.hexa` | `5c991786d812709679c8cdd69cd79d6669388bac847dcc79ad40ef0a38288c3e` | 51 |
| `vad_fsm.hexa` | `2653a517320627647ad8bf1ae9bd471f255b8d4b6d1315d792235d250789c033` | 92 |

shas pinned 2026-05-02.
