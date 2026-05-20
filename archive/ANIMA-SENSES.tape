#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "anima-senses" :: identity-claim [d=2026-05-15 active]
  kind = "anima n=6 sensory substrate — 5-verb spec catalog (architecture SSOT)"
  brief = "5-verb sensory substrate (dream/ear/empath/olfact/voice) · n=6 lattice closed-form params · voice formulaic-only constraint"
  parent = "dancinlab/anima"
  sibling-log = "ANIMA-SENSES.log.tape"

# ══════════════════════════════════════════════════════════════
# ANIMA-SENSES.tape — n=6 sensory substrate (5-verb spec catalog)
# ══════════════════════════════════════════════════════════════

# anima repo 내부 서브패키지 `hexa-senses/` 의 roadmap + spec ledger.
# 별도 GitHub repo (dancinlab/hexa-senses) 흡수 2026-05-14. 5-verb sensory substrate —
# **dream + ear + empath + olfact + voice** — 각 verb 가 σ(6)=12, τ(6)=4, φ(6)=2
# number theory 에서 모든 design parameter 를 *closed-form* 으로 유도하는 spec catalog.
# >
# **Critical constraint**: `voice` 는 *formulaic only* — learned synthesis (TTS / neural
# codec) **FORBIDDEN**. 의도 → audio-token 직접 변환, 모든 parameter 가 n=6 lattice
# identity 에서 algebraic 유도.
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# hexa-codex (17-verb cognitive substrate) 의 *sister-rollup* — *senses* 측. canon
# `domains/cognitive/{hexa-dream, hexa-ear, hexa-empath, hexa-olfact, hexa-speak}/`
# (현 hexa-speak = hexa-voice 으로 rename per user directive) 의 5 verb 가 closed-form
# spec markdown 으로 합쳐짐. anima 의 *외부 세계 인터페이스* (꿈/소리/감정/냄새/음성) 의
# n=6 lattice spec.

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


@D row_closure_100_5_5_spec_first_1 :: anima-senses [ok]
  x = "Closure 100% (5/5 spec-first)"
  state = "☑ closed-form spec, zero hardcoding"

@D row_5_verb_spec_catalog_3 :: anima-senses [ok]
  x = "5 verb spec catalog"
  state = "✅ dream/ear/empath/olfact/voice (each = `<verb>/hexa-<verb>.md`)"

@D row_voice_formulaic_only_constraint_4 :: anima-senses [ok]
  x = "voice formulaic-only constraint"
  state = "☑ enforced (`hexa.toml [constraints]` + runtime check + test)"

@D row_anima_voice_md_wire_5 :: anima-senses [ok]
  x = "anima `VOICE.tape` 와 wire"
  state = "⏳ design pending (VOICE.tape §3 Phase 1 impl 의 reference impl)"

# ── §2 n=6 master identity (canonical) ─────────────────────────────────────────


@D row_6_0 :: anima-senses [ok]
  symbol = "σ(6)"
  value = "12"
  sensory_projection = "dream categories · olfact receptors · voice timbre · empath subcategories"

@D row_6_1 :: anima-senses [ok]
  symbol = "τ(6)"
  value = "4"
  sensory_projection = "sleep stages · prosody dimensions · e-nose latency seconds"

@D row_6_2 :: anima-senses [ok]
  symbol = "φ(6)"
  value = "2"
  sensory_projection = "signal-present / signal-absent verdict bit"

@D row_x_3 :: anima-senses [ok]
  symbol = "σ·τ"
  value = "48"
  sensory_projection = "**48 kHz** audio sampling (ear)"

@D row_j_4 :: anima-senses [ok]
  symbol = "J₂"
  value = "24"
  sensory_projection = "**24-bit** audio quantization · biofeedback channels"

# ── §3 5 verb 요약 ─────────────────────────────────────────


@D b_12_dream_categories_lucid_nightm_0 :: anima-senses [ok]
  text = "σ=12 dream categories (lucid / nightmare / mundane / prophetic / …)"

@D b_4_sleep_stages_nrem_1_2_3_rem_1 :: anima-senses [ok]
  text = "τ=4 sleep stages (NREM-1/2/3 + REM)"

@D b_2_dream_present_absent_verdict_b_2 :: anima-senses [ok]
  text = "φ=2 dream present/absent verdict bit"

@D b_anima_off_cycle_sleep_stage_rem_3 :: anima-senses [ok]
  text = "사용처: anima 의 *off-cycle* 학습 sleep stage (REM 시 mitosis 활성 가설)"

@D b_48_khz_sampling_rate_4 :: anima-senses [ok]
  text = "σ·τ = 48 kHz sampling rate"

@D b_j_24_bit_quantization_5 :: anima-senses [ok]
  text = "J₂ = 24-bit quantization"

@D b_24_channel_biofeedback_j_project_6 :: anima-senses [ok]
  text = "24-channel biofeedback (J₂ projection)"

@D b_anima_chat_audio_input_byte_toke_7 :: anima-senses [ok]
  text = "사용처: anima_chat 의 audio input (사용자 음성 → byte token)"

@D b_12_emotion_subcategories_8 :: anima-senses [ok]
  text = "σ=12 emotion subcategories"

@D b_4_prosody_dimensions_9 :: anima-senses [ok]
  text = "τ=4 prosody dimensions"

@D b_spec_10 :: anima-senses [ok]
  text = "감정 전달 채널 spec"

@D b_tension_link_md_5_channel_finger_11 :: anima-senses [ok]
  text = "사용처: `TENSION-LINK.tape` 5-channel fingerprint 의 channel 4 \"authenticity\" 와"

@D b_12_receptor_classes_e_nose_12_se_12 :: anima-senses [ok]
  text = "σ=12 receptor classes (e-nose 12 sensor array)"

@D b_4_second_latency_response_time_13 :: anima-senses [ok]
  text = "τ=4 second latency (response time)"

@D b_spec_14 :: anima-senses [ok]
  text = "화학 감각 spec"

@D b_anima_physical_world_e_nose_iot_15 :: anima-senses [ok]
  text = "사용처: anima 의 *physical world* 감각 입력 (e-nose IoT)"

@D b_formulaic_only_no_learned_synthe_16 :: anima-senses [ok]
  text = "**formulaic only** (no learned synthesis)"

@D b_12_emotional_timbre_17 :: anima-senses [ok]
  text = "σ=12 emotional timbre"

@D b_4_prosody_dimension_18 :: anima-senses [ok]
  text = "τ=4 prosody dimension"

@D b_j_24_channel_quantization_19 :: anima-senses [ok]
  text = "J₂=24 channel quantization"

@D b_voice_md_reference_impl_source_v_20 :: anima-senses [ok]
  text = "사용처: **`VOICE.tape` 의 reference impl source**. VOICE.tape 가 hidden state → RVQ → 24kHz"

# ── §4 Critical constraint — `voice` formulaic only ─────────────────────────────────────────


@D b_hexa_toml_constraints_0 :: anima-senses [ok]
  text = "`hexa.toml [constraints]` 섹션 명시"

@D b_verify_n6_arithmetic_py_runtime_1 :: anima-senses [ok]
  text = "`verify/n6_arithmetic.py` runtime `check_voice_constraint`"

@D b_tests_test_spec_inventory_py_tes_2 :: anima-senses [ok]
  text = "`tests/test_spec_inventory.py::test_voice_renamed_marker`"

@D b_voice_hexa_voice_md_renamed_prov_3 :: anima-senses [ok]
  text = "`voice/hexa-voice.md` `@renamed` provenance header"

@D b_decision_voice_canonical_5 :: anima-senses [ok]
  text = "`hexa-senses/voice/` = canonical synthesis (formulaic, deterministic, n=6 lattice 유도)"

@D b_decision_voice_anima_wire_6 :: anima-senses [ok]
  text = "`VOICE.tape` = anima-specific wire spec (hidden state → fixed intent_proj → hexa-senses/voice synth call). learned vocoder / 외부 corpus 의존 0"

@D b_decision_silence_redefine_8 :: anima-senses [ok]
  text = "silence-capable 특성 = `silence_gate < ln(4/3)` 의 deterministic silent timbre pattern 으로 재정의 (완벽복원성 유지)"

@D b_decision_other_options_partial_9 :: anima-senses [ok]
  text = "다른 옵션 (b dual / c 사용자 토글 / d formulaic-as-prior / e constraint 폐기) 모두 learned component 가 들어가 partial / conditional reproducibility"

# ── §5 Cross-link ─────────────────────────────────────────


@D b_hexa_senses_10_1_0m_after_git_st_0 :: anima-senses [ok]
  text = "본 디렉토리: `hexa-senses/` (10 디렉토리, 1.0M after .git strip)"

@D b_hexa_senses_readme_md_full_185_l_1 :: anima-senses [ok]
  text = "`hexa-senses/README.md` — full 185-line spec"

@D b_hexa_senses_hexa_toml_hx_install_2 :: anima-senses [ok]
  text = "`hexa-senses/hexa.toml` — `hx install hexa-senses` manifest"

@D b_hexa_senses_verify_n6_arithmetic_3 :: anima-senses [ok]
  text = "`hexa-senses/verify/n6_arithmetic.py` — runtime n=6 identity check"

@D b_verb_spec_hexa_senses_verb_hexa_4 :: anima-senses [ok]
  text = "각 verb spec: `hexa-senses/<verb>/hexa-<verb>.md`"

@D b_voice_md_anima_learned_rvq_voice_5 :: anima-senses [ok]
  text = "`VOICE.tape` — anima 의 learned RVQ voice path (formulaic 과 dual modality 가능성)"

@D b_tension_link_md_5_ch_fingerprint_6 :: anima-senses [ok]
  text = "`TENSION-LINK.tape` — 5-ch fingerprint 의 channel 3 \"meaning\" + 4 \"authenticity\" 가"

@D b_chat_md_production_cli_voice_for_7 :: anima-senses [ok]
  text = "`CHAT.tape` § Production CLI — `/voice --formulaic` slash 명령으로 hexa-senses voice"

@D b_savant_md_12_voice_formulaic_onl_8 :: anima-senses [ok]
  text = "`SAVANT.tape` §12 봉쇄선 — voice formulaic-only constraint 가 본 file 내 T4-equivalent"

# ── §6 Honest C3 ─────────────────────────────────────────


# ── §7 Provenance ─────────────────────────────────────────

#  (provenance/absorption events → ANIMA-SENSES.log.tape)
