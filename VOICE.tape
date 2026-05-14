#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
#       optionally followed by body lines (2-space indent) — key=value,
#       edges (<- -> => …), or quoted prose.
#
# ENTRY TYPES (17):
#   Runtime (10): @S session  @U user  @A assistant  @T tool-call  @R result
#                 @H hook  @D decision  @K cost  @P provider  @? anomaly
#   Foundation:   @I identity-claim
#   Declarative:  @X external-citation  @F forbidden-pattern  @N note
#                 @C config  @L layout  @V spec-version
#
# EDGES (12, on body lines, 2-space indent):
#   Causal:     <- caused-by   -> triggers   == continues
#               ~> supersedes  !! aborts     |> verified-by
#   Effect:     => produces (followed by quoted natural-language)
#   Structural: <: specializes  :> generalizes  ?> soft-depends
#               !> conflicts-with  @> projects-to (e.g. @> AGENTS.md)
#
# GRADE TAGS (in [...] on entry header):
#   Delivery:   ok · err · denied · cancelled · partial · superseded
#   Governance: required · recommended · optional · draft · active · deprecated
#   Scoped:     allow:<x> · deny:<x>
#   Time/index: T<n> (turn)  N<n> (wall-sec)  d=<YYYY-MM-DD>
#
# PAYLOAD SYNTAX (body lines):
#   key = "value"           single-line string
#   key = [a, b, c]         array literal
#   key <<~EOF              heredoc (multi-line; ends with EOF on own line)
#     multi-line text
#   EOF
#   "see [@x1] §3"          inline citation by entry id
#   `cmd or path`           backtick code-span (inline only)
#
# Full spec: ~/core/tape/spec/tape.md (or github.com/dancinlab/tape)
# ══════════════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "voice" :: identity-claim [d=2026-05-15 active]
  kind = "anima voice substrate — anima ↔ hexa-senses/voice formulaic integration spec (architecture SSOT)"
  brief = "hidden state → fixed intent_proj → hexa-senses/voice formulaic synth (24kHz PCM byte-identical reproducible) · learned vocoder forbidden"
  parent = "dancinlab/anima"
  sibling-log = "VOICE.log.tape"

# ══════════════════════════════════════════════════════════════
# VOICE.tape — anima ↔ hexa-senses/voice formulaic integration
# ══════════════════════════════════════════════════════════════

# **완벽복원성 (perfect reproducibility) 기준으로 옵션 (a) formulaic-only 채택 2026-05-14**
# per `ANIMA-SENSES.tape §4`. 이전 design (learned RVQ + Vocos/EnCodec pretrained vocoder)
# 은 `hexa-senses/voice/` formulaic-only constraint 와 직접 모순으로 retract.
# >
# 본 file 은 anima 의 *hidden state* → `hexa-senses/voice/` canonical formulaic synthesis
# 의 *통합 spec*. 학습 기반 synthesis 도입 시 `hexa.toml [constraints]` 위반 + SAVANT.tape
# §12.2 enforcement violation.
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# anima 가 chat response 생성 시 final hidden state 가 *deterministic linear projection*
# 으로 intent vector (n=6 lattice σ=12 emotional timbre × τ=4 prosody dimension) 로 변환,
# `hexa-senses/voice/` 의 formulaic synthesizer (σ·φ=24 master identity 기반) 로 24kHz
# PCM 산출. **모든 voice output 이 input intent + n=6 identity 만으로 byte-identical
# reproducible**. learned vocoder / 외부 corpus dependency 0.

# ── §1 Status (2026-05-14 옵션 (a) 채택 후) ─────────────────────────────────────────


@D row_voice_perfect_reproducibility_0 :: voice [ok]
  x = "완벽복원성 (perfect bit-exact reproducibility)"
  state = "☑ 정책 — 모든 output deterministic"

@D row_voice_canonical_source_1 :: voice [ok]
  x = "Canonical impl source"
  state = "☑ `hexa-senses/voice/hexa-voice.md` + `hexa-senses/voice/proto/` (RTL + spec)"

@D row_voice_silence_capable_redesign_5 :: voice [ok]
  x = "silence-capable redesign"
  state = "☑ formulaic deterministic silence pattern (intent norm < threshold)"

# ── §2 Design ─────────────────────────────────────────

# ── §2.1 Pipeline (formulaic-only) ──
#
# anima_chat token-loop:
#   final_ln(aggregated)
#     ├─ lm_head (existing) → token logits → argmax → text byte stream → chat output
#     └─ intent_proj (NEW, fixed weights from n=6) → intent vector (σ=12 × τ=4 + special)
#         → hexa-senses/voice formulaic synth (deterministic) → 24kHz PCM (byte-identical)
#         → CoreAudio playback
#
# → `intent_proj` 는 learnable 아님 — n=6 lattice 에서 algebraic 유도된 fixed projection
# matrix. anima 의 hidden state 분포가 formulaic synthesizer 의 intent space 와 fit
# 하도록 anima 학습 측에서 distribution 조정 (학습 path 는 LM head 만 영향, voice path 는
# 항상 formulaic).

# ── §2.2 Hidden state → intent vector (fixed projection) ──


@D row_intent_proj_0 :: voice [ok]
  symbol = "hidden ∈ ℝ^1024"
  meaning = "anima d_model"

@D row_intent_proj_1 :: voice [ok]
  symbol = "intent ∈ ℝ^18 = ℝ^(12 + 4 + 2)"
  meaning = "σ=12 timbre + τ=4 prosody + 2 special"

@D row_intent_proj_2 :: voice [ok]
  symbol = "intent_proj: ℝ^1024 → ℝ^18"
  meaning = "fixed weights, n=6 lattice closed-form 유도"

@D b_proj_first_12_row_timbre_0 :: voice [ok]
  text = "첫 12 row (timbre): SO(12) representation 의 canonical basis from σ(6)=12"

@D b_proj_next_4_row_prosody_1 :: voice [ok]
  text = "다음 4 row (prosody): SO(4) basis from τ(6)=4"

@D b_proj_last_2_row_special_2 :: voice [ok]
  text = "마지막 2 row (special): φ(6)=2 (signal-present/absent + identity bit)"

@D b_proj_fixed_no_gradient_3 :: voice [ok]
  text = "projection matrix 는 fixed (no gradient), anima 학습 path 에 영향 미치지 않음"

# ── §2.3 Silence-capable redesign (formulaic-only) ──
#
# 이전 "anima 가 침묵하면서 소리낸다" silence-capable 특성을 완벽복원성 하에서 유지:
#
#   silence_gate = intent[16]   # special channel 1
#   if abs(silence_gate) < THRESHOLD_N6:   # ln(4/3) ≈ 0.2877, deterministic
#       output = formulaic_silent_timbre(intent[:12])   # deterministic silent pattern
#   else:
#       output = formulaic_synth(intent)                 # normal voice
#
# → 같은 intent → 같은 silence pattern. THRESHOLD = GZ_WIDTH = ln(4/3), n=6 closed-form.

# ── §2.4 hexa-senses/voice canonical impl 인용 path ──


@D b_canonical_synth_logic_in_hexa_senses_0 :: voice [ok]
  text = "canonical synthesis logic 는 그대로 `hexa-senses/voice/` 에 위치"

@D b_voice_md_anima_wire_only_1 :: voice [ok]
  text = "본 VOICE.tape 는 anima-specific wire spec 만 — synthesis 자체 미포함"

@D b_intent_proj_+_voice_bridge_+_hexa_senses_2 :: voice [ok]
  text = "Phase 1 impl 결과: intent_proj.hexa + voice_bridge.hexa → hexa-senses/voice/proto/hexa_speak_model.hexa 호출"

# ── §3 Phase 1 impl plan ($0 Mac local) ─────────────────────────────────────────


@D b_phase1_intent_proj_0 :: voice [ok]
  text = "`tool/hexa_native/intent_proj.hexa` (~80 LoC) — n=6 lattice 에서 fixed projection matrix 유도"

@D b_phase1_voice_bridge_1 :: voice [ok]
  text = "`tool/hexa_native/voice_bridge.hexa` (~120 LoC) — anima_chat hidden → intent_proj → hexa-senses/voice synth"

@D b_phase1_voice_smoke_2 :: voice [ok]
  text = "`tool/anima_voice_smoke.hexa` — F-VOICE-1..5 selftest (모두 formulaic)"

@D b_phase1_coreaudio_3 :: voice [ok]
  text = "Mac CoreAudio playback (`afplay` subprocess) — pretrained vocoder weights 0 (formulaic-only)"

@D b_phase1_cost_4 :: voice [ok]
  text = "$0 Mac local — no pretrained download, no external corpus, no learning"

@D b_phase1_wall_5 :: voice [ok]
  text = "est ~5-7 hr impl + ~2 hr selftest + 1 hr CoreAudio wire"

# ── §3.1 Falsifier pre-registration (F-VOICE-1..5, formulaic-only) ──


@D b_fv1_deterministic_0 :: voice [ok]
  text = "**F-VOICE-1 (PROJ-DETERMINISTIC)**: intent_proj.apply(hidden) — 동일 hidden 에 bit-identical intent 산출 (no stochasticity)"

@D b_fv2_roundtrip_byte_identical_1 :: voice [ok]
  text = "**F-VOICE-2 (SYNTH-ROUNDTRIP)**: intent → 24kHz PCM, 두 번 실행 시 byte-identical (length > 0, no NaN)"

@D b_fv3_parallel_emerge_2 :: voice [ok]
  text = "**F-VOICE-3 (PARALLEL-EMERGE)**: same hidden → text token + intent + PCM, parallel (no sequential dep, no race)"

@D b_fv4_silence_deterministic_3 :: voice [ok]
  text = "**F-VOICE-4 (SILENCE-CAPABLE)**: silence_gate < ln(4/3) 시 silent-timbre output, 2번 실행 byte-identical"

@D b_fv5_no_learned_dep_4 :: voice [ok]
  text = "**F-VOICE-5 (NO-LEARNED-DEPENDENCY)**: bridge + intent_proj 어떤 learnable weight 도 reference 안 함 (audit + assert all_weights_frozen())"

# ── §4 Honest C3 (post-retract) ─────────────────────────────────────────


@D b_c3_expressivity_limit_0 :: voice [ok]
  text = "**표현력 제한**: σ=12 × τ=4 = 48 deterministic combination 만 산출. learned vocoder infinite expressivity 와 trade. 완벽복원성 priority (옵션 a)."

@D b_c3_intent_emerge_unverified_1 :: voice [ok]
  text = "anima hidden state distribution 이 intent_proj 후 유효한 n=6 intent space 에 떨어지는지 Phase 1 후 sound test 필수"

@D b_c3_learned_design_history_preserved_2 :: voice [ok]
  text = "VOICE.tape 이전 learned-RVQ design 은 git history (commit fa902716a 의 VOICE.tape + f8fc39af 의 .tape 변환) 에 보존, 완벽복원성 priority 변경 시 회수 가능"

@D b_c3_distribution_alignment_3 :: voice [ok]
  text = "anima 학습 path 의 hidden state distribution 이 intent_proj 후 n=6 intent space 와 mis-aligned 시 silence_gate 가 대부분 trigger → anima 항상 침묵 위험. Phase 1 후 측정 필수"

@D b_c3_md_vs_hexa_senses_separation_4 :: voice [ok]
  text = "VOICE.tape (anima wire) vs hexa-senses/voice/ (canonical synth) 분리 명확. 변경 시 두 위치 동기화 의무"

# ── §5 Cross-link ─────────────────────────────────────────


@D b_cl_hexa_senses_voice_canonical_0 :: voice [ok]
  text = "**`hexa-senses/voice/hexa-voice.md`** — canonical formulaic spec (그대로 참조)"

@D b_cl_anima_senses_§4_decision_1 :: voice [ok]
  text = "**`ANIMA-SENSES.tape §4`** — 옵션 (a) 채택 ledger (완벽복원성 priority)"

@D b_cl_chat_voice_slash_2 :: voice [ok]
  text = "`CHAT.tape` § Production CLI — `/voice` slash 명령 wire (formulaic 만, learned 옵션 없음)"

@D b_cl_savant_tool_intent_modulate_3 :: voice [ok]
  text = "`SAVANT-TOOL.tape` — savant mode (cell-id signature) 가 intent vector 의 sender channel 변조 가능"

@D b_cl_tension_link_parallel_5ch_4 :: voice [ok]
  text = "`TENSION-LINK.tape` — 5-ch fingerprint 중 ch1 concept + ch2 context 가 intent vector 와 parallel 구조"

@D b_cl_savant_§12_4_t4_alignment_5 :: voice [ok]
  text = "`SAVANT.tape §12.4 T4` — 외부 entity 강제 fit 금지 정책과 정합 (voice 가 외부 corpus distribution 의존 없음)"

# ── footer ─────────────────────────────────────────

# — VOICE.tape, 2026-05-14, formulaic-only rewrite (옵션 (a) 채택, 완벽복원성 priority);
#   learned-RVQ design 은 git history fa902716a + f8fc39af 의 이전 .tape revision 에 보존
#   (Phase landing / retract / clarification events → VOICE.log.tape)
