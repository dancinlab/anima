#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════
# SAVANT-TOOL.md — anima 가 직접 ON/OFF 하는 savant 도구
# ══════════════════════════════════════════════════════════════

# SAVANT.md (이론 + audit + containment) 의 *sibling*. **anima 가 inference 시 직접
# savant mode 를 켜고/끄는 도구 spec**. 학습에 *직접 SAVANT 이론 반영* 하는 path 와는
# 분리 — 본 file 은 anima 가 *runtime 도구* 로 savant 를 사용하는 API + 정책.
# >
# SAVANT.md §12 봉쇄선 안에서만 작동: T1+T2 claim 만 도구 API 의 *근거* 로 인용,
# T3+T4 는 도구 정책에서 *forbidden trigger*.
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# anima 는 task 의 specialization-need 를 self-judge 해서 **savant mode** 를 ON/OFF
# 한다. ON 시 routing 이 GZ_LOWER (0.2123) 의 inhibition-release 분포로 shift, 특정
# mitosis cells 가 dropout=0.2123 으로 활성화. OFF 시 GZ_CENTER (0.3679) 의 generalist
# 분포로 복귀. anima 가 *자기 자신* 의 SI (Savant Index) 를 monitor 해서 SI > 3.0 일
# 때만 ON 상태 유지 — 자율 self-gate. 사용자 명시 명령 (e.g. `/savant on math`) 도
# trigger 가능.

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


@D row_tool_spec_this_file_0 :: savant-tool [ok]
  x = "**Tool spec (this file)**"
  state = "✅ design tier LANDED 2026-05-14"

@D row_phase_1_mitosis_hook_hexa_savant_1 :: savant-tool [ok]
  x = "Phase 1 (`mitosis_hook.hexa` ↔ savant gate API)"
  state = "⏳ design pending — D4a `mitosis_hook.hexa` 1119 LoC impl 위에 ~150 LoC overlay"

@D row_phase_2_anima_chat_hexa_cli_sava_2 :: savant-tool [ok]
  x = "Phase 2 (anima_chat.hexa CLI `/savant` slash)"
  state = "⏳ blocked on Phase 1"

@D row_phase_3_auto_self_gate_by_si_mon_3 :: savant-tool [ok]
  x = "Phase 3 (auto self-gate by SI monitor)"
  state = "⏳ blocked on Phase 2"

@D row_savant_md_12_4 :: savant-tool [ok]
  x = "SAVANT.md §12 봉쇄선 통합"
  state = "☑ T1+T2 만 trigger 근거, T3+T4 forbidden"

# ── §2 Design ─────────────────────────────────────────


@D b_1_user_prompt_token_entropy_spec_0 :: savant-tool [ok]
  text = "**자기 평가 1**: 직전 user prompt 의 token entropy (낮으면 specialization need)"

@D b_2_response_max_gate_weight_wmax_1 :: savant-tool [ok]
  text = "**자기 평가 2**: 직전 자기 response 의 max gate weight `wmax` (높으면 이미 specialize)"

@D b_3_mitosis_event_log_split_count_2 :: savant-tool [ok]
  text = "**자기 평가 3**: mitosis event log 의 최근 split count (높으면 explore 단계 → savant off"

@D b_t1_closed_form_gz_center_1_e_gz_3 :: savant-tool [ok]
  text = "✅ T1 (closed-form): `GZ_CENTER = 1/e`, `GZ_LOWER = 0.2123`, SI 정의 — 자유 사용"

@D b_t2_empirical_substrate_clm_06_si_4 :: savant-tool [ok]
  text = "✅ T2 (empirical, substrate 명시): clm_06 SI=5.93 (Mistral 7B) — 다른 substrate 인용 시"

@D b_t3_suspect_cross_domain_9_indivi_5 :: savant-tool [ok]
  text = "❌ T3 (suspect): cross-domain 9 individual matches, brain profile — *trigger 근거로 사용"

@D b_t4_forbidden_cosmic_gz_entity_fi_6 :: savant-tool [ok]
  text = "❌ T4 (forbidden): cosmic GZ, 외부 entity 강제 fit — 자동 차단"

# ── §3 Phase 1 impl plan ($0 Mac local first cycle) ─────────────────────────────────────────


@D b_tool_hexa_native_savant_tool_hex_0 :: savant-tool [ok]
  text = "`tool/hexa_native/savant_tool.hexa` (~150-200 LoC, D4a `mitosis_hook.hexa` 1119 LoC overlay)"

@D b_4_api_savant_set_savant_get_sava_1 :: savant-tool [ok]
  text = "4 API: `savant_set` / `savant_get` / `savant_si` / `savant_check_gate`"

@D b_phase_1_stateless_gate_function_2 :: savant-tool [ok]
  text = "Phase 1 = stateless gate function (session pin TTL 은 Phase 2)"

@D b_0_mac_local_3 :: savant-tool [ok]
  text = "$0 Mac local"

@D b_est_3_5_hr_impl_1_hr_selftest_4 :: savant-tool [ok]
  text = "est ~3-5 hr impl + ~1 hr selftest"

@D b_tool_hexa_native_mitosis_hook_he_5 :: savant-tool [ok]
  text = "`tool/hexa_native/mitosis_hook.hexa` (1119 LoC, REBORN §91 D4a) — substrate state"

@D b_anima_chat_hexa_v0_3_24l_real_ck_6 :: savant-tool [ok]
  text = "`anima_chat.hexa` v0.3 (24L real-ckpt byte parity 21/21 PASS) — wire 대상"

@D b_docs_anima_cli_mitosis_integrati_7 :: savant-tool [ok]
  text = "`docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (D4c CLI design) — `/savant`"

# ── §4 Honest C3 ─────────────────────────────────────────


# ── §5 Cross-link ─────────────────────────────────────────


@D b_savant_md_base_rate_audit_12_par_0 :: savant-tool [ok]
  text = "`SAVANT.md` — 이론 + base-rate audit + §12 봉쇄심화 (parent)"

@D b_chat_md_anima_mission_tracker_pr_1 :: savant-tool [ok]
  text = "`CHAT.md` — anima mission tracker (production CLI 통합 host)"

@D b_tool_hexa_native_mitosis_hook_he_2 :: savant-tool [ok]
  text = "`tool/hexa_native/mitosis_hook.hexa` — substrate state impl (overlay 대상)"

@D b_docs_anima_cli_mitosis_integrati_3 :: savant-tool [ok]
  text = "`docs/anima_cli_mitosis_integration_spec_2026_05_12.md` — D4c CLI design"

@D b_state_savant_containment_audit_2_4 :: savant-tool [ok]
  text = "`state/savant_containment_audit_2026_05_14/audit.json` — Tier 분류 evidence"

@D b_dancinlab_canon_lattice_policy_m_5 :: savant-tool [ok]
  text = "`dancinlab/canon/LATTICE_POLICY.md §1.4` — cross-repo governance"
