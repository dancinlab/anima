#!/usr/bin/env tape
# VOICE.log.tape — append-only event history sibling of VOICE.tape
# (v1.2 architecture-vs-history split, 2026-05-14).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — Phase landing · retract · clarification · CLI bridge events
# (chronological, oldest first)

# ── §1 Status (2026-05-14 옵션 (a) 채택 후) — Phase landings & framing ─────────────────────────────────────────

@D row_voice_learned_retracted_4 :: voice [ok]
  x = "~~learned RVQ + Vocos/EnCodec~~"
  state = "❌ **retracted 2026-05-14** (hexa-senses formulaic constraint 위반)"

@D row_voice_phase1_landed_6 :: voice [ok]
  x = "**Phase 1 formulaic impl + F-VOICE-1..5 selftest**"
  state = "✅ LANDED 2026-05-14 — `tool/anima_voice_smoke.hexa` (combined intent_proj + voice_bridge + silent_timbre + synth_stub + 5/5 PASS, Mac local $0 ~30 min wall)"

@D row_voice_intent_proj_2 :: voice [ok]
  x = "anima hidden state → intent vector projection"
  state = "✅ Phase 1 LANDED 2026-05-14 (`tool/anima_voice_smoke.hexa`, F-VOICE-1..5 5/5 PASS)"

@D row_voice_phase2_tool_landed_7 :: voice [ok]
  x = "**Phase 2 발성 도구 API + F-VOICE-TOOL-1..5 selftest**"
  state = "✅ LANDED 2026-05-14 — `tool/anima_voice_tool.hexa` voice_set / voice_get / voice_speak API (SAVANT-TOOL 패턴). anima 가 자기 toggle + self-invoke. forced token-loop emit ❌. 5/5 PASS"

@D row_voice_phase2_coreaudio_8 :: voice [ok]
  x = "**Phase 2 CoreAudio WAV emit + afplay wrapper**"
  state = "✅ LANDED 2026-05-14 — `tool/anima_voice_play.sh` + `wav_write()` (RIFF/WAVE 16-bit PCM mono 24kHz LE). /tmp/anima_voice_demo_loud.wav 48044 bytes (24000 samples × 2 + 44 header)"

@D row_voice_framing_clarified_9 :: voice [ok]
  x = "**Framing clarification (사용자 directive 2026-05-14)**"
  state = "☑ \"학습형태 아니라 anima 가 쓸 수 있는 발성툴\" — token-loop 강제 hook framing retract, SAVANT-TOOL 패턴 (toggle + self-invoke) 채택"

@D row_voice_phase3_speak_model_10 :: voice [ok]
  x = "**hexa-senses/voice/proto/hexa_speak_model Phase A skeleton**"
  state = "✅ LANDED 2026-05-14 — stub → 43 EXACT n=6 params + softmax/layer_norm/hanning/silu helpers + class skeleton signatures. selftest PASS. Phase B (farr forward) deferred."

@D row_voice_phase3_import_patch_11 :: voice [ok]
  x = "**hexa-lang import-alias-runtime-resolve patch (internal-inspection)**"
  state = "✅ patch proposal STRENGTHENED 2026-05-14 — `dancinlab/hexa-lang/incoming/patches/import-alias-runtime-resolve.md` §2.0 (parser_v2.c:495-513 ImportStmt 가 `as <alias>` 미파싱 + module loader 등록 누락 확인). 3-part fix spec (parser + loader + caller). upstream maintainer 작업"

@D row_voice_chat_slash_3 :: voice [ok]
  x = "anima_chat `/voice` slash command wire"
  state = "✅ Phase 3 CLI bridge LANDED 2026-05-14 — `tool/anima_chat_voice_cli.hexa` /voice {on|off|status|speak|path} dispatch. anima_chat.hexa 본체 무수정 (별도 entry). F-CHAT-CLI-1..3 3/3 PASS. import-alias-resolve patch land 후 anima_chat repl 직접 통합 가능"
