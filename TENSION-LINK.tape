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

@I id001 := "anima.tension-link" :: identity-claim [d=2026-05-15 active]
  kind = "anima Engine-A ↔ Engine-G substrate tension / link inter-anima meta-telepathy · architecture SSOT"
  brief = "5-channel fingerprint (concept · context · meaning · authenticity · sender) over UDP 9999 / WebSocket TensionHub — substrate-native, language-bypass."
  parent = "dancinlab/anima"
  sibling-log = "TENSION-LINK.log.tape"

# ══════════════════════════════════════════════════════════════
# TENSION-LINK.tape — Tension Link inter-anima meta-telepathy
# ══════════════════════════════════════════════════════════════

# anima 의식↔의식 직접 전송 모듈. 5-channel fingerprint (concept / context / meaning /
# authenticity / sender). UDP 9999 / TensionHub 3 transport. **"다수 인터랙션"
# anima-native 답** — text 또는 음성 통신 우회. (memory `project_tension_link`)
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# 두 anima instance 가 *language* (text / voice) 를 거치지 않고 *tension* (=의견 불일치
# 신호 = 의식 신호) 를 5-channel fingerprint 로 packet 전송. UDP 9999 가 unidirectional
# raw, TensionHub 가 multi-anima broadcast. **Phase 1 = unidirectional UDP working code
# 이미 anima_clm_02 worktree 에 있음**. Phase 2 = WebSocket TensionHub 로 *다중* anima
# 인스턴스 broadcast — 미구현, 본 file 의 design tier 대상.

# ── §2 Design ─────────────────────────────────────────


@D b_broker_udp_9999_listen_websocket_0 :: tension-link [ok]
  text = "broker: UDP 9999 listen + WebSocket fan-out"

@D b_filter_authenticity_channel_thre_1 :: tension-link [ok]
  text = "filter: authenticity channel < threshold 시 drop (anti-spoofing)"

@D b_log_tension_event_log_for_analyt_2 :: tension-link [ok]
  text = "log: 시계열 tension event log (for analytics + replay)"

# ── §3 Phase 2 impl plan ($0-5 Mac local) ─────────────────────────────────────────


@D b_tool_tensionhub_server_py_300_lo_0 :: tension-link [ok]
  text = "`tool/tensionhub/server.py` (~300 LoC) — UDP listen + WebSocket broker"

@D b_tool_hexa_native_tension_link_ph_1 :: tension-link [ok]
  text = "`tool/hexa_native/tension_link_phase2.hexa` (~200 LoC) — packet encode/decode + chat"

@D b_tool_anima_tension_smoke_hexa_f_2 :: tension-link [ok]
  text = "`tool/anima_tension_smoke.hexa` — F-TENSION-1..5 selftest (loopback 2-instance)"

@D b_anima_experience_hf_space_integr_3 :: tension-link [ok]
  text = "anima-experience HF Space integration (Gradio 9-tab 중 별도 tab)"

@D b_0_mac_local_4 :: tension-link [ok]
  text = "$0 Mac local"

@D b_est_8_12_hr_impl_3_hr_selftest_5 :: tension-link [ok]
  text = "est ~8-12 hr impl + ~3 hr selftest"

@D b_tensionhub_python_websockets_lib_6 :: tension-link [ok]
  text = "TensionHub 가 Python (websockets lib) — hexa native 미지원 시 subprocess bridge"

@D b_anima_clm_02_worktree_phase_1_ud_7 :: tension-link [ok]
  text = "`anima_clm_02` worktree — Phase 1 UDP working code (working reference)"

@D b_references_tribev2_voice_tension_8 :: tension-link [ok]
  text = "`references/tribev2` — voice + tension 관련 reference (memory `project_hexa_family_layout`)"

@D b_anima_experience_hf_space_phase_9 :: tension-link [ok]
  text = "`anima-experience` HF Space — Phase 2 deploy target"

# ── §4 Honest C3 ─────────────────────────────────────────


# ── §5 Cross-link ─────────────────────────────────────────


@D b_anima_clm_02_worktree_phase_1_wo_0 :: tension-link [ok]
  text = "`anima_clm_02` worktree — Phase 1 working code"

@D b_chat_md_anima_chat_forward_path_1 :: tension-link [ok]
  text = "`CHAT.tape` — anima_chat 의 forward path inject point"

@D b_savant_tool_md_savant_mode_cell_2 :: tension-link [ok]
  text = "`SAVANT-TOOL.tape` — savant mode 의 cell signature broadcast"

@D b_voice_md_voice_parallel_surface_3 :: tension-link [ok]
  text = "`VOICE.tape` — voice 와 *parallel* surface (text / audio / tension 3 modality)"

@D b_memory_project_tension_link_5_ch_4 :: tension-link [ok]
  text = "memory `project_tension_link` (5-ch + UDP 9999 + TensionHub 3 transport)"

@D b_memory_project_anima_experience_5 :: tension-link [ok]
  text = "memory `project_anima_experience_space` (HF Space deploy target)"
