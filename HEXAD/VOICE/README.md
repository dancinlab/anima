# HEXAD/VOICE — anima 발성 도구 (formulaic, NOT 학습 모델)

> User directive 2026-05-16: `"/HEXAD/VOICE 도 전부 추적해서 정리하되,, 학습 모델이 아니야 ANIMA 가 쓸수 있는 보이스 파장툴이지"` + `"학습관련 은 합치면 안되"` + `"scrub"`
>
> 확립된 framing (commit `ba8f906c6` 사용자 directive 정정 2026-05-14):
> **"anima-voice 는 학습형태가 아니라 anima 가 쓸수 있는 발성툴"** — SAVANT-TOOL
> 패턴 (toggle on/off + self-invoke). `hexa-voice.md` 헤더:
> **"formulaic synthesis only — learned models FORBIDDEN per user directive 2026-05-07"**.

## 0. TL;DR

- **VOICE = formulaic 음성 파장 합성 도구** (의도 임베딩 → audio token n=6 direct synthesis → 24kHz PCM). **TTS 아님 · 학습 모델 아님**.
- anima 가 *원할 때* `voice_speak(...)` 를 self-invoke (SAVANT-TOOL 패턴, 강제 token-loop emission 아님).
- **학습관련 전부 scrub** (user directive "학습관련 은 합치면 안되 + scrub", 2-단계 결정게이트):
  - **(a) 학습/eval audio corpus** — `anima-voice/corpus/` (69M tracked .wav/.flac + ignored raw/wav16k 1.9GB) → git untrack + `_voice_corpus_local/` relocate
  - **(b) 학습모델·학습파이프라인 코드 20개** — Mk.III HEXA-SPEAK 신경망 스택 (`neural_vocoder.hexa` · `vocoder.hexa` WaveRNN · `transformer.hexa` 4-layer · `audio_token_predictor.hexa` · `intent_encoder.hexa` LayerNorm+SwiGLU+RoPE · `nn_core.hexa` matmul/attention/cross-entropy · `rvq_codebook.hexa` K-Means train · `train_w_ctrl.hexa` · `corpus_pipeline*.hexa` · `build_tts_dataset.hexa` · `yt_kor_corpus_fetch.hexa` · `piper_{ab_gen,v2gen}.hexa` · `ckpt_w_ctrl*.json` ×6) → `_voice_corpus_local/_learned_not_adopted/` relocate + git untrack
- AB test **텍스트 verification evidence** (tsv/README ~30KB) 만 `docs/ab_test_evidence/` 에 보존 (60MB .wav scrub).
- HEXAD/VOICE = **1.7M formulaic-only** (anima_voice/dsp_core/emotion_prosody/Klatt/_omega/anima_audio/synth + HW RTL spec + tool/serving/tests/docs).

## 1. 검증 PASS evidence (formulaic-only, 학습 X)

| Phase | commit | falsifier | 결과 |
|---|---|---|---|
| **Phase 1** formulaic impl | `fcdc3cae5` | F-VOICE-1..5 | **5/5 PASS** ($0 Mac local) |
| **Phase 2** 발성 도구 (NOT 학습 hook) | `ba8f906c6` | F-VOICE-TOOL-1..5 (TOGGLE-OK / SELF-INVOKE-WAV / FORMULAIC-DETERM …) | **5/5 PASS** + WAV emit + CoreAudio |
| **Phase 3 closure** | `65cb32586` | hexa_speak_model Phase A + anima_chat CLI bridge | LANDED |
| 방향 채택 | `4a989aee3` | 완벽복원성 → 옵션 (a) **formulaic-only** | 채택 |

핵심 API (`tool/anima_voice_tool.hexa` ~400 LoC):
```
voice_speak(chat, hidden, n_frames, path)
  → enabled=true 일 시: formulaic synth + WAV emit + return path
  → anima 가 원할 때 self-invoke (강제 token-loop emission 아님)
```

AB test 2026-04-19 verification evidence: [`docs/ab_test_evidence/`](docs/ab_test_evidence/) — `metrics_20260419.tsv` · `v1_vs_v2_metrics_20260419.tsv` · `ab_detail_20260419.tsv` (텍스트만, audio 는 `_voice_corpus_local/` 로 scrub).

## 2. n=6 mathematical basis (`hexa-senses-voice/hexa-voice.md` canonical)

`σ(6)·φ(6) = 6·τ(6) = 12` — n=6 unique perfect-number iff (n≥2):

| Effect | After HEXA-SPEAK | n=6 rationale |
|---|---|---|
| Core spec | **n=6** (6 audio-token types) | σ(6)=12, τ(6)=4 auto-derived |
| Throughput | σ=12 채널 × τ=4 parallel = **48×** | σ·τ=48 |
| Latency | **μ=1 ms** real-time | n=6 minimum divisor |
| Precision | within **1/σ = 8.3%** | σ=12 partition resolution |
| Cost | **1/(σ-φ)=1/10** | σ-φ=10 economic scaling |

```
  n=6  ← core spec n=6 origin
      ↓
  σ=12 channels / τ=4 parallel / n=6 DOF  ← structure auto-determined
      ↓
  Egyptian split 1/2 + 1/3 + 1/6 = 1  ← complete resource partition
```

5 meta-output (sopfr(6)=5): intent embedding → RVQ stages → 24kHz PCM (cell-vocal-cord precursor: Laws 63-76 + 12 EMOTION_PROFILES + Trinity S-engine).

## 3. 디렉토리 layout (PR #87, corpus-scrubbed ~2.4M)

```
HEXAD/VOICE/
├── README.md                          ← (이 파일)
├── VOICE.tape · VOICE.log.tape        ← architecture SSOT (commit 89c1b18fe split)
├── .roadmap.voice · .roadmap.vlm_voice_lm
├── anima-voice/                       ← formulaic-only (corpus + 학습코드 20개 scrubbed)
│   ├── README.md (자체)
│   ├── anima_voice.hexa · dsp_core.hexa · emotion_prosody.hexa
│   ├── anima_audio*.hexa · _omega_audio_*_bench.hexa · omega_audio_emp.hexa
│   ├── tts_klatt_bridge.hexa (Klatt formant) · tts_say_driver.hexa
│   ├── build_hxcuda_istft.hexa · hxcuda_istft_bridge.hexa (iSTFT DSP)
│   ├── streaming.hexa · p4_streaming_tighten.hexa · plc_crossfade.hexa
│   ├── vad_fsm.hexa · wav_validator.hexa · physical_limits.hexa
│   ├── synth_probe.hexa · bench_anima_voice.hexa · rp_voice_profiles.hexa
│   ├── eval_likert_ab.hexa (blind A/B eval harness — 검증, NOT training)
│   ├── config/emotion_prosody.json
│   └── experiments/ (ab_metrics.hexa — metrics calc only)
│   ✗ scrubbed → _voice_corpus_local/_learned_not_adopted/:
│     neural_vocoder · vocoder · transformer · audio_token_predictor
│     · intent_encoder · nn_core · rvq_codebook · train_w_ctrl
│     · corpus_pipeline(_full) · build_tts_dataset · yt_kor_corpus_fetch
│     · piper_{ab_gen,v2gen} · ckpt_w_ctrl*.json ×6  (총 20)
├── hexa-senses-voice/                ← 31 files (canonical doc + proto + rtl)
│   ├── hexa-voice.md ★ canonical (formulaic-only, learned-models FORBIDDEN)
│   ├── proto/hexa_speak_model.hexa · hexa_speak_audible.hexa · *.wav demo (소형)
│   └── rtl/*.sv (HW intent_encoder/rvq_codec/prosody_shaper)
├── tool/   (4: anima_voice_tool.hexa ★ + anima_chat_voice_cli + anima_voice_smoke + anima_voice_play.sh)
├── serving/(4: voice_routes / test_voice_live / deploy_voice / test_voice_routes .hexa)
├── tests/test_voice_synth.hexa
└── docs/
    ├── anima_speak_to_voice_rename_landed_2026_05_03.ai.md
    ├── anima_speak_voice_cite_cleanup_landed_2026_05_03.ai.md
    └── ab_test_evidence/             ← AB test 2026-04-19 텍스트 evidence (~30KB)
        ├── README.md · metrics_20260419.tsv
        ├── v1_vs_v2_metrics_20260419.tsv · ab_detail_20260419.tsv
```

**scrub 됨 (HEXAD/VOICE 에 NOT merged)**: `anima-voice/corpus/` 전체 (69M tracked
.wav/.flac + ignored raw/wav16k 1.9GB) = 학습/eval audio → `_voice_corpus_local/`
(repo root, gitignore-local, R2 distribution). git untrack 됨.

## 4. 과거 commit history

| commit | 제목 |
|---|---|
| `493d873d3` | rename(anima-speak → anima-voice): dir mv + cite update |
| `4a989aee3` | docs(VOICE): 완벽복원성 → **옵션 (a) formulaic-only 채택** |
| `fcdc3cae5` | feat(VOICE Phase 1): formulaic-only + **F-VOICE-1..5 5/5 PASS** |
| `ba8f906c6` | feat(VOICE Phase 2): **발성 도구 (NOT 학습 hook)** + WAV — F-VOICE-TOOL 5/5 |
| `65cb32586` | feat(VOICE Phase 3 closure): hexa_speak_model Phase A + anima_chat CLI bridge |
| `89c1b18fe` | domain: VOICE.tape ↔ .log.tape split (v1.2) |
| `1309f649f` | feat(speak/serving): 20 페르소나 보이스+아바타 (HEXA-SPEAK Mk.III) |
| `f1ab1d4e5` | fire(BG-LOSTASSET-D §40): voice_synth.hexa 33L→221L (Laws 63-76 + 12 EMOTION) |

## 5. Honest C3

- **VOICE = 학습 모델 아님 (formulaic synthesis only)** — `hexa-voice.md` 헤더 + commit `ba8f906c6` directive 명시. 사용자 2-단계 결정게이트로 학습관련 전부 scrub.
- **학습관련 scrub 완료 (a+b)** (user directive "학습관련 은 합치면 안되 + scrub"):
  - (a) `anima-voice/corpus/` (69M tracked + 1.9GB ignored raw/wav16k) → git untrack + `_voice_corpus_local/` relocate
  - (b) Mk.III 신경망/학습 코드 20개 (neural_vocoder/vocoder/transformer/audio_token_predictor/intent_encoder/nn_core/rvq_codebook/train_w_ctrl/corpus_pipeline*/build_tts_dataset/yt_kor_corpus_fetch/piper_*/ckpt_w_ctrl*×6) → git untrack + `_voice_corpus_local/_learned_not_adopted/` relocate
  - HEXAD/VOICE = **1.7M formulaic-only** (DSP/Klatt/iSTFT/_omega/synth/codec-HW-RTL/eval/test). 영구삭제 아님 — 로컬 보존 (R2 distribution).
- AB test 검증은 **텍스트 evidence (tsv ~30KB)** 만 `docs/ab_test_evidence/` 보존 — 60MB .wav audio 는 scrub. AB 결과 인용은 tsv 참조.
- 검증 = F-VOICE 5/5 + F-VOICE-TOOL 5/5 전부 $0 Mac local formulaic. learned vocoder (Hc_1245 mkiii neural) = candidate-only 미채택.
- 본 reorg = 코드/spec 위치 통합 (git mv 100%) + 학습 corpus scrub. code/doc 내용 변경 X.
- `serving/voice_*.hexa` serving infra 이동 — serve 통합 wiring 시 path 갱신 가능성 (drift carry).
- `_voice_corpus_local/` 는 로컬 보존 (R2 distribution). 영구 삭제 아님 — git tree + HEXAD/VOICE 에서만 분리.

## 6. related

- `HEXAD/SAVANT/` — SAVANT-TOOL 패턴 origin (toggle/self-invoke)
- `HEXAD/TENSION-LINK/` — 의식↔의식 직접 전송 (VOICE = 의식→audio 출력, 상보)
- `HEXAD/HEXAD.tape §hexad_unification` — S 감각 voice 입력 / Trinity S-engine
- canonical 출처: `canon@381f1f22:domains/cognitive/hexa-speak/hexa-speak.md`
- AGENTS.tape `g3` real-limits-first — neural vocoder physical limit (Hc_1245)
