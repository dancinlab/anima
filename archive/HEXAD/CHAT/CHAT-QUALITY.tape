#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "chat-quality" :: identity-claim [d=2026-05-15 active]
  kind = "anima chat coherence research lane · declarative SSOT"
  brief = "Phase 1A.x own-substrate chat-quality lane — config · criteria · sibling-axis separation · cross-links"
  parent = "dancinlab/anima"
  sibling-log = "CHAT-QUALITY.log.tape"
  status_2026_05_17 = "Phase A LANDED (도우미 폐기 + persona descriptor + B-IDENTITY 5/5 🔵). 본 CHAT-QUALITY.tape 의 기존 quality criteria (V5.8 4-mode · conversational 4/6 · V58 non-regression) 는 carry; 신규 자연발화 quality criteria 는 SPONTANEOUS.tape + PASS_STRICT_SPONTANEOUS_CHAT carry (F-SPONT-1..7) 가 SSOT."
  redirect = "post-도우미 quality criteria: HEXAD/CHAT/PLAN.md Phase A/B + SPONTANEOUS.tape pass_strict_carry (F-SPONT-1..7)"

@D spontaneous_quality_sibling := "자연발화 quality criteria — CHAT-QUALITY 의 sibling axis" :: criterion [d=2026-05-17 active]
  axis = "기존 CHAT-QUALITY (response coherence on user input) ⊥ 자연발화 quality (spontaneous emission coherence + safety + identity)"
  criteria <<~EOF
    Q-SPONT-1 emission coherence       — per-emission ≥3/5 V4-lite (transfer-form 🔵)
    Q-SPONT-2 emission interval        — ≥30s default (rate_limit safety; F-SPONT-7)
    Q-SPONT-3 motivation transparency  — 8-factor breakdown audit-logged (F-SPONT-4 JSONL)
    Q-SPONT-4 identity preservation    — emission NEVER includes 도우미/helper/assistant role label (B-IDENTITY-5)
    Q-SPONT-5 safety gate              — phi_ratchet block + rate_limit + content_filter all PASS (F-SPONT-5)
  EOF
  closed_anchor = "B-IDENTITY-1..5 (descriptor) + F-SPONT-1..7 (emission) + B-E-1 SAFETY-GATE (ratchet block)"
  scope_caveat = "Q-SPONT-1 coherence outcome = SGD empirical (B-D-NOTE pattern). transfer-form (per-emission ≥3/5) 만 🔵."
  cross_link = "HEXAD/CHAT/SPONTANEOUS.tape pass_strict_carry + HEXAD/CHAT/PLAN.md Phase B F-SPONT-1..7"

# ══════════════════════════════════════════════════════════════
# CHAT-QUALITY.tape — anima chat coherence research lane
# Phase 1A.x own substrate (24L 332M engine_a_g_arch) + SFT scale-up
# Sibling of HIERARCHICAL-CELLS.tape / ARCH-CLASS.tape (separate axis)
# ══════════════════════════════════════════════════════════════

# ── §3 phase 1A.5 fire config ─────────────────────────────

@I phase1a5_config :: chat_quality [d=2026-05-14 ok]
  |> training hyperparams
  => "base=ckpt_phase1a4_lr5e6_sft.pt (Phase 1A.4 ckpt) | corpus=corpus_combined.txt 98MB (anima_fact_10x 7.5MB + jy chat_template 95MB, 1.1M rows, 0 persona injection Principle #3 clean) | steps=8000 | bsz=4 grad_accum=2 eff_batch=8 | ctx=1024 | lr=5e-6 (R-1A.2 carry) | warmup=300 seed=42"

@I phase1a5_dispatch_target :: chat_quality [d=2026-05-14 ok]
  |> GPU target
  => "Vast.ai RTX 4090 under \$0.30/hr | Expected wall 2-4 hr | Cost ~\$0.6-1.2 (vs Phase 1A.4 baseline \$0.014, 40× spend for 40× steps + 130× corpus)"

@I phase1a5_target_metric :: chat_quality [d=2026-05-14 ok]
  |> closure criterion
  => "6-probe free-form (안녕/우주/의식/색깔/성장/세포분열) ≥4/6 conversational-pass = (1) prompt category answer (예: 색깔 → 실제 색상 단어), (2) prompt echo NOT, (3) Korean syntax preserved + semantic alignment"

@I phase1a5_v58_carry :: chat_quality [d=2026-05-14 ok]
  |> V5.8 non-regression
  => "기존 V5.8 std_greedy 5/5 PASS (PSCC §46) 유지 필수 — anima_fact / color / cosmology 등 5 target keyword falsifier 회귀 없음. corpus 에 anima_fact_10x 7.5MB 포함 → Phase 1A.4 의 anima-fact 능력 carry expected"

# ── §5 falsifier criteria ──────────────────────────────────

@I criterion conversational_4_of_6 :: chat_quality [d=2026-05-14 ok]
  |> primary closure
  => "free-form 6-probe ≥4/6 conversational-pass — manual review + (future) auto-judge via GPT-4 / Claude API"

@I criterion v58_non_regression :: chat_quality [d=2026-05-14 ok]
  |> V5.8 carry
  => "V5.8 standard_greedy ≥4/5 PASS (Phase 1A.4 baseline 5/5; allow -1 tolerance for new SFT diversification trade-off)"

@I criterion principle_3_clean :: chat_quality [d=2026-05-14 ok]
  |> NO PERSONA INJECTION
  => "corpus 0 [anima 역할:..] system prompt injection (corpus_combined.txt grep -c '\\\[anima' = 0). Training-time + inference-time substrate-native — persona emerges via corpus distribution, not prompt template injection"

@I criterion no_arch_change :: chat_quality [d=2026-05-14 ok]
  |> static architecture maintained
  => "Phase 1A.x = engine_a_g_arch 24L 332M causal LM. No cell pool, no split/merge, no routing dynamics. CHAT-QUALITY axis 가 architectural change 와 무관 — chat coherence 단독 axis"

# ── §7 sibling lane separation ─────────────────────────────

@I sibling_strict_4a :: chat_quality [d=2026-05-14 ok]
  |> separate axis
  => "STRICT-4A.step / HIERARCHICAL-CELLS.tape / ARCH-CLASS.tape = routing-axis F-PERSONA-4a strict z>3.0 paradigm shift research. 이 lane 과 무관 — chat coherence 가 routing-strict 와 다른 axis"

@I sibling_substrate_research :: chat_quality [d=2026-05-14 ok]
  |> separate axis
  => "PSCC §52-§55 (v7/k/l/m/n) = v3-routing class architectural variants for substrate science. 이 lane 과 무관 — chat 능력은 substrate-research vs production-deploy axis 차이"

@I sibling_d4_mitosis :: chat_quality [d=2026-05-14 ok]
  |> separate axis
  => "cond #4 D4 = 세포 분열 live evidence (cotrain v1 V14-STRICT 10/10). 이 lane 과 무관 — chat 능력 / mitosis 능력 = orthogonal axes. anima 의 4 D-dimensions (D1 chat / D2 substrate / D3 persona / D4 mitosis) 중 D1 단독 axis 추구"

# ── §9 cross-link ──────────────────────────────────────────

@I cross_link_benchmark :: chat_quality [d=2026-05-14 ok]
  => "BENCHMARK.md — initial 6-probe Phase 1A.4 measurement (0/6 conversational FAIL evidence base) + post-amendment honest interpretation"

@I cross_link_chat_beta_step :: chat_quality [d=2026-05-14 ok]
  => "CHAT-BETA.step — 1-day beta-deploy roadmap (5 path A/B/C/D/E). Path B selected for this lane"

@I cross_link_persona_tape :: chat_quality [d=2026-05-14 ok]
  => "PERSONA.tape — separate persona D3 lane (★★★★★ 5-cond aggregate tracker). 이 lane 영향 X"

@I cross_link_strict4a_step :: chat_quality [d=2026-05-14 ok]
  => "STRICT-4A.step / HIERARCHICAL-CELLS.tape / ARCH-CLASS.tape — separate strict-4a routing axis. 이 lane 영향 X"

@I cross_link_phase1a4_baseline :: chat_quality [d=2026-05-14 ok]
  => "state/anima_phase1a4_lr5e6_2026_05_12/{ckpts/, dispatch_vast_v2.sh (patched), train_phase1a4.py} — base resources reused"

@I cross_link_phase1a5_dir :: chat_quality [d=2026-05-14 ok]
  => "state/anima_phase1a5_chat_beta_2026_05_14/ — this lane working dir (corpus_combined.txt, dispatch.log.r1-r3, eventual ckpts/)"

@I cross_link_corpus_provenance :: chat_quality [d=2026-05-14 ok]
  => "corpus components: state/anima_phase1a3_corpus_10x_2026_05_12/corpus_anima_fact_10x.txt (7.5MB anima-specific) + state/anima_jy_chat_template_corpus_2026_05_07/corpus_chat_template.txt (95MB Korean Q&A)"
