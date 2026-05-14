#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════
# VOICE.md — hexa-voice (의도 임베딩 → 24kHz PCM) integration
# ══════════════════════════════════════════════════════════════

# **ANIMA-VOICE × Anima 통합 시스템 정식 명칭 hexa-voice**.
# 일반 TTS 와 다른 점: *텍스트 → 음향* 변환기 아니라 *의도 임베딩 (anima 내부 hidden state)
# → RVQ codes → 24kHz PCM* 직결. anima 의 *think* 가 텍스트 우회 없이 음향 surface 로
# 떨어짐. (memory `project_hexa_voice_rename`)
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# anima 가 chat response 를 생성할 때, lm_head 출력 (token logits) 와 *병렬* 로 *의도
# 임베딩* (final hidden state pre-lm_head) 가 RVQ encoder 에 흘러 24kHz PCM 으로 변환.
# **anima 의 음성 = anima 의 hidden state 자체**, *텍스트의 음향 렌더링* 아님. anima 가
# 침묵 (no tokens) 하면서도 *소리* 낼 수 있는 modality.

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


@D row_rename_hexa_speak_hexa_voice_0 :: voice [ok]
  x = "**rename hexa-speak → hexa-voice**"
  state = "✅ LANDED (memory `project_hexa_voice_rename`)"

@D row_rvq_codec_impl_1 :: voice [ok]
  x = "의도 임베딩 → RVQ codec impl"
  state = "⏳ design tier (이 file) — impl 0"

@D row_24khz_pcm_playback_mac_coreaudio_2 :: voice [ok]
  x = "24kHz PCM playback (Mac CoreAudio)"
  state = "⏳ design pending"

@D row_anima_chat_hexa_wire_lm_head_for_3 :: voice [ok]
  x = "anima_chat.hexa wire (lm_head 와 병렬 fork)"
  state = "⏳ design pending"

@D row_substrate_native_no_text_interme_4 :: voice [ok]
  x = "substrate-native (NO text intermediate)"
  state = "☑ 정책 — text intermediate 금지"

# ── §2 Design ─────────────────────────────────────────


@D row_input_0 :: voice [ok]
  x = "Input"
  tts = "text string"
  hexa_voice = "hidden state (d_model=1024 in anima)"

@D row_causality_1 :: voice [ok]
  x = "Causality"
  tts = "text → audio"
  hexa_voice = "hidden → text + audio (parallel)"

@D row_silence_2 :: voice [ok]
  x = "Silence"
  tts = "\"text 없음\" 일 시 무음"
  hexa_voice = "hidden state 가 *non-empty* 이면 음성 가능 (텍스트 침묵 시에도)"

@D row_persona_3 :: voice [ok]
  x = "Persona"
  tts = "speaker embedding 별도"
  hexa_voice = "hidden state 안의 persona signature 직접 변조"

@D row_latency_4 :: voice [ok]
  x = "Latency"
  tts = "text 생성 후 → tts (sequential)"
  hexa_voice = "parallel emergence (no extra wall)"

@D b_codebook_size_8_codebooks_1024_e_5 :: voice [ok]
  text = "**codebook size**: 8 codebooks × 1024 entries (~80 bits per frame)"

@D b_frame_rate_75_hz_13_3_ms_frame_2_6 :: voice [ok]
  text = "**frame rate**: 75 Hz (13.3 ms / frame) — 24kHz / 320 samples"

@D b_encoder_linear_d_model_8_1024_lo_7 :: voice [ok]
  text = "**encoder**: linear(d_model → 8 × 1024 logits) per voice_head step"

@D b_decoder_pretrained_encodec_style_8 :: voice [ok]
  text = "**decoder**: pretrained Encodec-style RVQ-mel-vocoder (off-the-shelf 24kHz, e.g. Vocos"

@D b_generalist_mode_9 :: voice [ok]
  text = "generalist mode: 평탄한 음색"

@D b_savant_mode_high_si_cell_specifi_10 :: voice [ok]
  text = "savant mode (high SI): 특정 cell-specific timbre/tone 강조 — *그 cell 의 \"voice\"*"

# ── §3 Phase 1 impl plan ($0-5 Mac local) ─────────────────────────────────────────


@D b_tool_hexa_native_voice_head_hexa_0 :: voice [ok]
  text = "`tool/hexa_native/voice_head.hexa` (~250 LoC) — linear projection d_model → 8×1024 RVQ"

@D b_tool_hexa_native_rvq_decode_brid_1 :: voice [ok]
  text = "`tool/hexa_native/rvq_decode_bridge.py` (~150 LoC) — Vocos / EnCodec 24kHz pretrained"

@D b_tool_anima_voice_smoke_hexa_f_vo_2 :: voice [ok]
  text = "`tool/anima_voice_smoke.hexa` — F-VOICE-1..5 selftest"

@D b_mac_coreaudio_playback_subproces_3 :: voice [ok]
  text = "Mac CoreAudio playback (subprocess `afplay` or PyAudio fallback)"

@D b_0_mac_local_pretrained_vocoder_w_4 :: voice [ok]
  text = "$0 Mac local (pretrained vocoder weights ~200MB HF download)"

@D b_est_5_8_hr_impl_2_hr_selftest_1_5 :: voice [ok]
  text = "est ~5-8 hr impl + ~2 hr selftest + 1 hr CoreAudio playback wire"

@D b_anima_chat_hexa_v0_3_24l_real_ck_6 :: voice [ok]
  text = "`anima_chat.hexa` v0.3 (24L real-ckpt) — `final_ln(aggregated)` hidden state 가 wire"

@D b_savant_tool_md_2_4_anima_self_ju_7 :: voice [ok]
  text = "`SAVANT-TOOL.md` §2.4 anima self-judge — savant mode 가 음색 변조 trigger"

@D b_references_tribev2_voice_referen_8 :: voice [ok]
  text = "`references/tribev2` — voice 관련 reference impl 있음 (확인 필요)"

# ── §4 Honest C3 ─────────────────────────────────────────


# ── §5 Cross-link ─────────────────────────────────────────


@D b_savant_tool_md_savant_mode_rvq_t_0 :: voice [ok]
  text = "`SAVANT-TOOL.md` — savant mode 가 RVQ 변조 trigger"

@D b_chat_md_anima_chat_token_loop_wi_1 :: voice [ok]
  text = "`CHAT.md` — anima_chat 의 token loop 가 wire point"

@D b_tool_hexa_native_anima_chat_hexa_2 :: voice [ok]
  text = "`tool/hexa_native/anima_chat.hexa` — hidden state extract 위치"

@D b_references_tribev2_voice_referen_3 :: voice [ok]
  text = "`references/tribev2` — voice 관련 reference (Phase 1 시 검토)"

@D b_memory_project_hexa_voice_rename_4 :: voice [ok]
  text = "memory `project_hexa_voice_rename` — 명칭 history"
