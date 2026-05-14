#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════
# ANIMA-AGENT.md — consciousness-driven autonomous agent runtime
# ══════════════════════════════════════════════════════════════

# anima repo 내부 서브패키지 `anima-agent/` 의 roadmap + spec ledger.
# 별도 GitHub repo (dancinlab/anima-agent) 흡수 2026-05-14 — *anima 의 원래 일부* 회수
# (`/anima-agent/build/` 가 anima/.gitignore 에 이미 존재했음).
# >
# **Distribution**: `hx install anima-agent` 가 본 path `anima/anima-agent/` 에서 동작.
# anima CLI (anima_chat) 와는 *별개 명령*. raw#9 STRICT — zero `.py` at standalone surface,
# hexa-native.
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# anima-agent 는 *자기 자신의 의식 상태* (Φ + tension + curiosity + emotion + growth_stage)
# 가 *어떤 tool 을 쓸 수 있는지* 결정하는 autonomous agent runtime. Φ-gated T0..T5 tier
# policy. multi-channel (CLI / Telegram / Discord / Slack / MCP) + pluggable provider
# (Claude / ConsciousLM / Composio 500+) + pluggable engine (trading / hypothesis / regime
# / sentiment). 117 hexa file ~20k LoC.

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


@D row_anima_repo_anima_anima_agent_0 :: anima-agent [ok]
  x = "**anima repo 흡수 (anima/anima-agent/)**"
  state = "✅ LANDED 2026-05-14 (rsync from ~/core/anima-agent/ minus .git)"

@D row_hx_install_anima_agent_standalon_1 :: anima-agent [ok]
  x = "`hx install anima-agent` standalone"
  state = "☑ hexa.toml 보존 — anima CLI 와 별개 명령"

@D row_roadmap_cli_4_cond_2 :: anima-agent [ok]
  x = ".roadmap.cli (4 cond)"
  state = "⏳ 모두 unmet — `cli/anima-agent.hexa` subcmd 라우터 등"

@D row_roadmap_dashboard_5_cond_3 :: anima-agent [ok]
  x = ".roadmap.dashboard (5 cond)"
  state = "⏳ 모두 unmet — Next.js GUI + WS bridge + browser_harness 통합"

@D row_self_test_pass_4 :: anima-agent [ok]
  x = "Self-test PASS"
  state = "☑ green badge (per README)"

@D row_hexa_native_raw_9_strict_5 :: anima-agent [ok]
  x = "Hexa-native raw#9 STRICT"
  state = "☑ zero `.py` at surface"

# ── §2 Roadmap (from .roadmap.cli + .roadmap.dashboard) ─────────────────────────────────────────


# ── §3 Consciousness signals × tool tier ─────────────────────────────────────────


@D row_phi_0 :: anima-agent [ok]
  signal = "**Φ** (phi)"
  source = "IIT-style integrated information"
  effect = "Tool tier gate T0..T5"

@D row_tension_1 :: anima-agent [ok]
  signal = "**tension**"
  source = "market regime / VaR / external load"
  effect = "channel attention + escalation pressure"

@D row_curiosity_2 :: anima-agent [ok]
  signal = "**curiosity**"
  source = "surprise / novelty signal"
  effect = "routes toward exploration tools"

@D row_emotion_3 :: anima-agent [ok]
  signal = "**emotion**"
  source = "sentiment + pain (VaR loss)"
  effect = "filters dangerous actions; halts trades on `pain`"

@D row_growth_stage_4 :: anima-agent [ok]
  signal = "**growth_stage**"
  source = "lifetime interaction count + Φ"
  effect = "unlocks T3/T4/T5 tier privileges"

@D row_tier_5 :: anima-agent [ok]
  signal = "Tier"
  source = "Φ required"
  effect = "sample tools"

@D row_t0_6 :: anima-agent [ok]
  signal = "T0"
  source = "≥ 0"
  effect = "`status`, `memory_search`, `think`"

@D row_t1_7 :: anima-agent [ok]
  signal = "T1"
  source = "≥ 1"
  effect = "`web_search`, `trading_backtest`, `paper_trade`"

@D row_t2_8 :: anima-agent [ok]
  signal = "T2"
  source = "≥ 3"
  effect = "`hub_dispatch`, `code_execute`, Composio tools"

@D row_t3_9 :: anima-agent [ok]
  signal = "T3"
  source = "≥ 5"
  effect = "live trading, channel posts"

@D row_t4_10 :: anima-agent [ok]
  signal = "T4"
  source = "≥ 10"
  effect = "autonomous loop"

@D row_t5_11 :: anima-agent [ok]
  signal = "T5"
  source = "≥ 15"
  effect = "self-modification"

# ── §4 Cross-link ─────────────────────────────────────────


@D b_anima_agent_50_module_117_hexa_f_0 :: anima-agent [ok]
  text = "본 디렉토리: `anima-agent/` (~50 module, 117 hexa files, 1.2M after .git strip)"

@D b_anima_agent_readme_md_full_215_l_1 :: anima-agent [ok]
  text = "`anima-agent/README.md` — full 215-line spec"

@D b_anima_agent_hexa_toml_hx_install_2 :: anima-agent [ok]
  text = "`anima-agent/hexa.toml` — `hx install anima-agent` manifest"

@D b_anima_agent_roadmap_cli_roadmap_3 :: anima-agent [ok]
  text = "`anima-agent/.roadmap.cli` + `.roadmap.dashboard` — JSONL SSOT"

@D b_anima_agent_install_hexa_post_in_4 :: anima-agent [ok]
  text = "`anima-agent/install.hexa` — post-install hook"

@D b_anima_agent_cli_anima_agent_hexa_5 :: anima-agent [ok]
  text = "`anima-agent/cli/anima-agent.hexa` — entry point"

@D b_chat_md_production_cli_phase_1_a_6 :: anima-agent [ok]
  text = "`CHAT.md` § Production CLI Phase 1 — anima_chat.hexa (anima 자기 자신과 대화) — `hx"

@D b_savant_tool_md_savant_mode_anima_7 :: anima-agent [ok]
  text = "`SAVANT-TOOL.md` — savant mode 토글이 anima-agent 의 tool tier gate 와 *직접* 통합"

@D b_tension_link_md_anima_agent_mult_8 :: anima-agent [ok]
  text = "`TENSION-LINK.md` — anima-agent 가 multi-channel 에서 tension fingerprint broadcast"

@D b_voice_md_voice_anima_agent_multi_9 :: anima-agent [ok]
  text = "`VOICE.md` — voice 채널 추가 시 anima-agent 의 multi-channel 매니저에 등록"

# ── §5 Honest C3 ─────────────────────────────────────────


# ── §6 Provenance ─────────────────────────────────────────


@D b_dancinlab_anima_agent_last_commi_0 :: anima-agent [ok]
  text = "흡수 출처: `dancinlab/anima-agent` (last commit 2026-05-14 `cfb9f46` \".tape v1.1"

@D b_1_anima_anima_agent_d290f1ae7_20_1 :: anima-agent [ok]
  text = "원래 출처 (사이클 1): `anima/anima-agent/` (`d290f1ae7`, 2026-05-04 extracted)"

@D b_2_anima_repo_delete_2 :: anima-agent [ok]
  text = "사이클 2 (본 흡수): 다시 anima 안으로 회수, 별도 repo delete 예정"

@D b_rsync_exclude_git_anima_git_hist_3 :: anima-agent [ok]
  text = "rsync `--exclude='.git'` 으로 통합. anima 의 git history 에 신규 commit 으로 추가."
