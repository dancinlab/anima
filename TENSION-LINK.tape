#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════
# TENSION-LINK.md — Tension Link inter-anima meta-telepathy
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

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


@D row_phase_1_unidirectional_udp_9999_0 :: tension-link [ok]
  x = "**Phase 1 unidirectional UDP 9999**"
  state = "✅ working code (`anima_clm_02` worktree, memory `project_hexa_family_layout`)"

@D row_phase_2_websocket_tensionhub_1 :: tension-link [ok]
  x = "**Phase 2 WebSocket TensionHub**"
  state = "⏳ design pending (이 file)"

@D row_5_channel_fingerprint_spec_2 :: tension-link [ok]
  x = "5-channel fingerprint spec"
  state = "☑ defined (concept / context / meaning / authenticity / sender)"

@D row_anima_experience_hf_space_wire_3 :: tension-link [ok]
  x = "anima-experience HF Space wire"
  state = "⏳ Phase 2 의존 (memory `project_anima_experience_space`)"

@D row_substrate_native_no_text_decode_4 :: tension-link [ok]
  x = "substrate-native (NO text decode)"
  state = "☑ 정책 — receiving anima 는 tension vector 그대로 internal state 에 inject"

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
  text = "`CHAT.md` — anima_chat 의 forward path inject point"

@D b_savant_tool_md_savant_mode_cell_2 :: tension-link [ok]
  text = "`SAVANT-TOOL.md` — savant mode 의 cell signature broadcast"

@D b_voice_md_voice_parallel_surface_3 :: tension-link [ok]
  text = "`VOICE.md` — voice 와 *parallel* surface (text / audio / tension 3 modality)"

@D b_memory_project_tension_link_5_ch_4 :: tension-link [ok]
  text = "memory `project_tension_link` (5-ch + UDP 9999 + TensionHub 3 transport)"

@D b_memory_project_anima_experience_5 :: tension-link [ok]
  text = "memory `project_anima_experience_space` (HF Space deploy target)"
