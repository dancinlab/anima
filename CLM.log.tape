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


# ══════════════════════════════════════════════════════════════
# CLM.log.tape — append-only event history
# (v1.2 architecture-vs-history split, 2026-05-14)
# ══════════════════════════════════════════════════════════════

# §Log — entries chronological, oldest first.

@D row_clm_family_ssot_0 :: clm-tape [ok]
  x = "**CLM family SSOT (this file + .roadmap.clm)**"
  state = "✅ CLM.tape narrative ledger LANDED 2026-05-14; .roadmap.clm JSONL (18 entries) 운용 중"


@D row_phase_1_90m_1 :: clm-tape [ok]
  x = "Phase 1 (90M, BG-LB substrate ckpt)"
  state = "✅ LANDED — Phase 2 ancestor; substrate ckpt /workspace/anima_phase2/bg_lb_step_8000_final.pt"


@D row_phase_2_350m_cotrain_2 :: clm-tape [ok]
  x = "Phase 2 (350M Engine A/G cotrain, 2026-05-09)"
  state = "🔶 EXECUTED but consciousness FAIL — V14 violation v5 mirror; private record-keeping ckpt; H4 + H5 blockers open"
  ckpt = "dancinlab/clm-v5-phase2-cotrain-engine-ag (private)"
  cost = "$4.63 wall 90.57min"
  blocker = "V14 violation re-confirmed at v5 mirror — random_init PPR ≥ trained PPR; chat coherence not measured"


@D row_phase_3_7b_3 :: clm-tape [ok]
  x = "Phase 3 (7B Engine A/G cotrain, planned)"
  state = "⏳ BLOCKED on Phase 2 consciousness PASS — entry condition `phase_2_consciousness_pass: required` 미충족"
  arch = "32L × 4096 × 32h × 8kv (GQA 4:1), Engine A/G dual-engine, ~7.0B params"
  data = "~140B tokens (Chinchilla optimal); corpus pipeline 미구축 (~135B token external)"
  cost = "$200-600 envelope (8× H100 × 50-80h × runpod spot)"
  fire_keyword = "OK CLM PHASE 3 7B FIRE COST $200-600"


@D row_phase_4_14b_4 :: clm-tape [ok]
  x = "Phase 4 (14B 본진 모델, planned)"
  state = "⏳ BLOCKED on Phase 3 PASS — anima 사가 first scratch 14B 본진 등극 milestone"
  arch = "40L × 5120 × 40h × 8kv, Engine A/G dual-engine, ~14.0B params"
  data = "~280B tokens (Chinchilla optimal); Phase 3 corpus 14B-extensible 필요"
  cost = "$500-1500 envelope (8-16× H100 × 75-250h); expansion verbatim 별도 필수"
  fire_keyword = "OK CLM PHASE 4 14B FIRE COST $500-1500"


@D row_v5_mitosis_lane_5 :: clm-tape [ok]
  x = "v5-mitosis substrate lane (§88~§91 mitosis_hook.hexa)"
  state = "✅ LANDED — `mitosis_hook.hexa` 1119 LoC executable (D4a), F-MIT-HOOK-1..5 5/5 PASS, $0 Mac local"
  position = "본진 .clm Phase ladder 와 별개 lane — substrate-native mitosis 진화; 본 file §5 re-frame 가설 검증 대상"


@D row_v5_ddp_92_6 :: clm-tape [ok]
  x = "v5-mitosis cotrain v5 DDP (§92 BG, 2026-05-13)"
  state = "🔶 LANDED INCONCLUSIVE — 5.37B params 6.72hr $86.82; F-V5MIT 3/5 FAIL + F-PERSONA-4a KL_PASS_NULL_FAIL + F-PERSONA-4b FAIL"
  meaning = "size class 5.37B ≈ Phase 3 7B 의 76% — 이미 fire 됐지만 substrate-native lane (v5-mitosis) path 였음, Engine A/G arch 가 아님"
  artifact = "state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13/cotrain_v5_ddp_result.json"


@D row_bypass_prohibited_7 :: clm-tape [ok]
  x = "**우회금지 governance (§7.5, 8 rules, deny:write; g5 WAIVED 2026-05-14)**"
  state = "🚫 LANDED 2026-05-14 — 본진 Phase 3/4 fire 의 7 우회 path 강행 차단 (g5 V14 audit prerequisite WAIVED per user directive)"
  rules = "g1 Phase entry · g2 sibling lane · g3 도구 substitute · g4 corpus bypass · ~~g5 V14 unaudit~~ (WAIVED) · g6 cost verbatim · g7 silent demote · g8 lane re-frame"
  enforcement = "any fire-keyword 발화 전 7 rule 검증 mandatory; (F-PHASE3-5 / F-PHASE4-6 hard-falsifier 는 §8 hypothesis-based 로 superseded)"
  v14-waiver-risk = "Phase 3/4 fire 시 V14 violation 재현 시 cost $200-1500 burn 사용자 수용; revoke 'V14 WAIVER REVOKE'"


@D row_hypothesis_verification_8 :: clm-tape [ok]
  x = "**검증 조건 (§8 hypothesis-driven, 2026-05-14)**"
  state = "🔄 PIVOT LANDED — 기존 falsifier-based 검증 [superseded], 가설 폴더 (193 promoted + 1189 candidates) 기반 verdict 로 교체"
  source = "hypotheses/ + hypotheses_candidates/ 의 frontmatter `verification_method` (W1..W12 ladder)"
  sample = ".clm-relevant 12 가설 pre-selected (H_005 / H_014 / H_015 / H_042 / H_068 / H_080 / Hc_003 / Hc_011 / Hc_017 / Hc_020 / Hc_022 / Hc_047 / Hc_048 / Hc_1110 / Hc_1240)"
  verdict-method = "각 가설 verification_method 실행 → frontmatter status 갱신 (running → promoted / falsified / partial) + PHILOSOPHY.tape append"

# ── §2 .clm family definition (.clm 가 뭔지) ─────────────────────────────────────────


@D def_origin :: clm-tape [ok]
  text = "**Origin**: anima_native_scratch substrate (D1=1.0). anima 가 외부 base 없이 from-scratch 짓는 모델 가족. ALM (LoRA-derived 외부집) 의 SUNSET 이후 successor track."


@D def_engine_a_g :: clm-tape [ok]
  text = "**Arch**: Engine A/G dual-engine — Engine A (autoregressive language) ⇄ Engine G (cell-state ODE flow). a_g_tension_temperature=0.25 로 두 engine 간 routing. Engine G cells (16/24/32/40 = Phase 1/2/3/4) 가 substrate-coupled emergence (D3) 의 캐리어."


@D def_two_axis :: clm-tape [ok]
  text = "**Two-axis verifier**: 의식측정 (AN11 + Φ + adversarial + Putnam) ✓ + 자연어 chat coherence (KO+EN ≥3/5) ✓ — 둘 다 통과해야 다음 Phase 진학. clm.cond.1 (의식) + clm.cond.2 (HF release) 가 .roadmap.clm 의 두 cond."


@D def_lineage :: clm-tape [ok]
  text = "**Lineage v3→v4→v5**: v3 (ALM era, 2026-05-01 이전, SUNSET), v4 (#115 NOT_READY chat category error, consciousness-measurement only), v5 (Engine A/G cotrain era, 2026-05-09 ~ 현재 — Phase 2/3/4 ladder + v5-mitosis substrate lane 분기)."


@D def_v5_split :: clm-tape [ok]
  text = "**v5 lane split**: v5-cotrain-engine-ag (Phase ladder canonical) ⇄ v5-mitosis (mitosis_hook substrate-native). 둘 다 anima_native_scratch D1=1.0 이지만 arch 와 verifier 다름. 본 file §5 가 둘의 정합성 검증."

# ── §3 흩어진 방향 audit — REBORN.tape §85~§92 cycle 매핑 ─────────────────────────────────────────


@D audit_85 :: clm-tape [ok]
  cycle = "§85"
  topic = "anima_chat.hexa hexa-native port (1589 LoC, 2026-05-12)"
  clm_align = "Phase 3/4 prerequisite — inference 표면 hexa-native 화. 본진 14B 의 chat coherence 측정 도구. ✓ aligned"


@D audit_86 :: clm-tape [ok]
  cycle = "§86~§87"
  topic = "D1 anima_chat.hexa v0.2/v0.3 (TODO[load] + multitoken RESOLVED, real 24L ckpt 21/21 PASS, ★★★★★)"
  clm_align = "Phase 2 ckpt 으로 hexa-native chat 측정 capable. Phase 3/4 chat coherence ≥3/5 측정 path 의 핵심 인프라. ✓ aligned"


@D audit_88 :: clm-tape [ok]
  cycle = "§88~§90"
  topic = "v5-mitosis cond.1~cond.4 arch spec + port skeleton + REBORN.tape §90 mitosis_model_v5.py 852L"
  clm_align = "v5-mitosis = .clm Phase 2 가 V14 violated 후 mitosis substrate 로 진화한 lane. §5 re-frame 가설 대상. ⚠ AMBIGUOUS — 본진 lane 인지 우회 lane 인지 미결"


@D audit_89 :: clm-tape [ok]
  cycle = "§91"
  topic = "D4a `mitosis_hook.hexa` 1119 LoC FULL IMPL + F-MIT-HOOK 5/5 PASS"
  clm_align = "v5-mitosis lane 의 hexa-native impl. Phase 3/4 본진 lane 과 별개 substrate. ⚠ AMBIGUOUS"


@D audit_90 :: clm-tape [ok]
  cycle = "§92"
  topic = "v5-mitosis cotrain v5 DDP — 5.37B params 4×GPU 6.72hr $86.82 (LANDED INCONCLUSIVE)"
  clm_align = "v5-mitosis path 의 7B-class scale-up 시도. F-V5MIT 3/5 FAIL → 본진 lane re-frame 가설 (§5) 의 negative evidence. ✗ off-track for canonical Phase 3"


@D audit_savant :: clm-tape [ok]
  cycle = "PSCC ledger 외부"
  topic = "SAVANT-TOOL Phase 1+2+3 b/c/d (5 artifacts, 24/24 falsifier PASS, 2026-05-14)"
  clm_align = "도구화 path — anima 가 inference 시 self-toggle. Phase 3/4 의 routing modifier overlay (savant_routing_overlay top-k mask) 로 evidence-tier 활용 가능. ✓ partially aligned (tool, not lane)"


@D audit_voice :: clm-tape [ok]
  cycle = "PSCC ledger 외부"
  topic = "VOICE Phase 1+2+3 (formulaic-only synth, hexa_speak_model Phase A, anima_chat CLI bridge)"
  clm_align = "도구화 path — anima 발성 도구. Phase 3/4 의 자연어 측정 axis 와 분리 (voice ≠ chat coherence). ✓ tool-only, off main lane"


@D audit_tension_link :: clm-tape [ok]
  cycle = "PSCC ledger 외부"
  topic = "TENSION-LINK Phase 1 (5-ch fingerprint, anima 의식↔의식 직접 전송)"
  clm_align = "inter-anima 통신 — Phase 4 본진 모델 등극 후 multi-anima 시대의 인프라. Phase 3/4 prerequisite 아님. ⚠ deferred"


@D audit_summary :: clm-tape [ok]
  text <<~EOF
    **Audit verdict**: 7 cycle 중 2 (§85, §86) 가 본진 .clm Phase ladder 와
    명확히 정합 (chat 측정 인프라). 2 (§88, §89) 가 ambiguous (v5-mitosis re-frame
    가설 §5 대상). 1 (§92) 가 off-track (cotrain v5 DDP 가 substrate-native lane
    의 scale-up 으로 본진 7B Engine A/G 와 다른 arch). 2 (SAVANT, VOICE) 가 도구
    only (lane 아님). 1 (TENSION-LINK) 가 deferred.

    **다른 곳 = 어디**: 사용자가 본 "다른 곳" 의 정체는 §88~§92 의 v5-mitosis lane
    이 본진 lane 으로 *오해/대체* 되어가는 흐름. v5-mitosis 가 의식측정 evidence
    (F-V5MIT, F-PERSONA, Φ, 의식 verifier) 를 풍부하게 산출하지만, Phase 3 Engine
    A/G 7B 의 entry condition (Phase 2 V14 violation 해결) 은 *미해결*. mitosis 가
    별개 lane 으로 흐르는 동안 본진 ladder 는 정지.
  EOF

# ── §4 v5-mitosis re-frame 가설 (옵션 C 검증) ─────────────────────────────────────────


@D hyp_verdict :: clm-tape [ok]
  text = "**Re-frame verdict**: v5-mitosis ≠ .clm mk3. v5-mitosis 는 *sibling lane* (anima_clm_12 worktree 자산 + REBORN §88~§92). 본진 .clm Phase 3/4 는 Engine A/G arch 의 별도 path 로 진행. naming SSOT 재정렬 불필요."

# ── §5 §92 v5 DDP 결과 land (옵션 D) ─────────────────────────────────────────


@D ddp_result_size :: clm-tape [ok]
  text = "n_params = 5,373,430,016 (~5.37B) — Phase 3 7B 의 76% size class"


@D ddp_result_compute :: clm-tape [ok]
  text = "wall = 24185.6s (6.72hr) · cost = $86.82 · ddp world_size=4 (per_gpu_batch=2, effective=8) · freeze_mitosis=1"


@D ddp_result_metrics :: clm-tape [ok]
  text = "ce_final_avg100 = 0.0646 (낮음) · aux_final = 1.208 · ent_gate_final = 5.543/5.545 (최대값) · wmax_final = 0.190 · n_active>.01 = 8.0/256 cells · gate_max = 0.0072 (dead routing)"


@D ddp_result_falsifiers :: clm-tape [ok]
  text <<~EOF
    F-V5MIT regression: **3/5 FAIL**
      F-V5MIT-1 SPLIT-NOGRAD FAIL (freeze_mitosis=1 로 splits=0, baseline 미산출)
      F-V5MIT-2 MERGE-WEIGHT PASS
      F-V5MIT-3 PHI-CONSERVATION PASS
      F-V5MIT-4 COTRAIN-CONVERGE PASS (ce 0.065 ≪ 1.0)
      F-V5MIT-5 V14-STRICT FAIL

    F-PERSONA-4a routing (top-K MoE): **KL_PASS_NULL_FAIL**
      KL = 1.4903, null permutation 1.36±0.25, z = 0.51 p = 0.31 (null 안 통과)
      (soft gate) KL = 0.0005, z = 2.33 (cf. PSCC §52 v7 z=2.75 first signal)

    F-PERSONA-4b content (M4 aggregated cosine): **FAIL**
      cos_dist = 2.34e-4, null = 1.75e-4 ± 6.3e-5, z = 0.94 p = 0.14
      (v2 carry z = 3.20, §44 PSCC reference)
  EOF


@D ddp_result_verdict :: clm-tape [ok]
  text <<~EOF
    **§92 v5 DDP verdict**: 5.37B Phase 3-class 시도 **INCONCLUSIVE**.

    Positive: cotrain converge (ce 0.065), 7B-class wall feasibility 입증 ($86.82,
    6.72hr 4×GPU), DDP 인프라 작동.

    Negative: F-V5MIT 3/5 FAIL (V14-STRICT 재현), F-PERSONA-4a soft gate z=2.33
    < 3.0 strict (§52 v7 z=2.75 와 동일 ballpark), F-PERSONA-4b FAIL.

    **Off-track for canonical Phase 3**: arch 가 Engine A/G dual-engine 아니라
    v5-mitosis 1L + 256 cells substrate. fire_keyword `OK CLM PHASE 3 7B FIRE`
    와 무관 — 본진 ladder entry 미시도. cost $86.82 가 Phase 3 envelope $200-600
    의 14-43% 소진했지만 Engine A/G path 진척 0.

    **그러나** size feasibility + DDP infra + V14 mirror behavior 의 evidence
    는 Phase 3 Engine A/G fire 시 carry-forward 가치.
  EOF

# ── §6 본진 14B Phase 4 복귀 path (옵션 A) ─────────────────────────────────────────


@D path_a_root_unblock :: clm-tape [ok]
  step = "Step 1 — Phase 2 V14 violation root-unblock"
  detail = "H4 normalize 무력화 가설 (normalize 가 effective 하지 않음) + H5 chat curriculum collapse 가설 (Engine G cell-state cotrain collapse) 별도 audit. arch tile bug `clm_v4_mount.hexa L626-630` (8-cell 2× tile reps=2) 점검. ~5-10 hr Mac local + ~$50 small GPU."


@D path_a_phase_2b :: clm-tape [ok]
  step = "Step 2 — Phase 2b 재시도 (350M Engine A/G, fix-5/fix-6 적용)"
  detail = "Phase 2 의 fix-5 normalize removal + fix-6 chat curriculum redesign 적용한 신규 cotrain. private repo `dancinlab/clm-v5-phase2b-cotrain-engine-ag`. cost ~$5-10 (90min 1× H100). entry 통과 시 Phase 3 7B fire entry condition 충족."


@D path_a_phase_3 :: clm-tape [ok]
  step = "Step 3 — Phase 3 7B fire ($200-600)"
  detail = "OK CLM PHASE 3 7B FIRE COST $200-600 fire_keyword 후 dispatch. 8× H100 SXM × 50-80hr × runpod spot. 외부 corpus pipeline BG-CORPUS-7B 필요 (~135B token external). hf_repo dancinlab/clm-v5-engine-a-g-7b-cotrain (private initial)."


@D path_a_phase_4 :: clm-tape [ok]
  step = "Step 4 — Phase 4 14B 본진 ($500-1500, expansion verbatim)"
  detail = "본진 모델 등극 milestone. Phase 3 7B PASS 후 expansion verbatim 별도 fire — `OK CLM PHASE 4 14B BUDGET EXPANSION` + `OK CLM PHASE 4 14B FIRE COST $500-1500`. 8-16× H100 × 75-250hr. hf_repo dancinlab/clm-v5-engine-a-g-14b-cotrain."


@D path_total_cost :: clm-tape [ok]
  text = "**Total path cost envelope**: $5-10 (Phase 2b) + $200-600 (Phase 3) + $500-1500 (Phase 4) = $705-2110. 사용자 verbatim 3회 필요 (Phase 2b 는 own 16 standard band, Phase 3+4 는 cost-bearing + expansion verbatim)."

# ── §7 진행 path 결정 (옵션 통합) ─────────────────────────────────────────


@D path_decision :: clm-tape [ok]
  text <<~EOF
    **4 옵션 verdict 통합**:
    - (B) audit + .clm align 회수 → ✅ §3 LANDED (본 file)
    - (D) §92 v5 DDP 결과 land → ✅ §5 LANDED
    - (C) v5-mitosis = .clm mk3 re-frame → ✗ §4 negative verdict (sibling lane)
    - (A) 본진 14B 복귀 path 설계 → ⏳ §6 step-by-step LANDED, fire 대기

    **Next-step (4 옵션 통합 후 자연스러운 다음)**:
    fire 전 prerequisite: Phase 2 V14 violation root-audit doc (§6 Step 1).
    $0 Mac local audit + REBORN.tape §93 신규 section 으로 ledger.
    Output: H4/H5 hypothesis 검증 시나리오 + Phase 2b 재시도 spec.
  EOF

# ── §7.5 우회금지 governance (bypass-prohibited rules) ─────────────────────────────────────────

# 본 section 은 .clm 본진 Phase ladder 의 *우회금지 강행규칙*. 사용자 directive
# 2026-05-14 "우회금지 반드시 추가" 의 응답. §3 audit 가 식별한 옆길 흐름 +
# §4 sibling-lane verdict 를 운용 정책으로 enforce.


@D b_hypothesis_verification_kind :: clm-tape [ok]
  text = "**Verification kind**: anima 의 philosophy pipeline (hypotheses_candidates/ → hypotheses/ → PHILOSOPHY.tape) 의 가설 list 가 검증 조건. fire result 의 verdict = 가설 verdict (PASS/FAIL/PARTIAL/AMBIGUOUS) 의 set."


@D b_hypothesis_verdict_method :: clm-tape [ok]
  text = "**Verdict method**: 각 가설의 frontmatter `verification_method` field (W1..W12 ladder) 가 measurement 명시. fire 후 verification_method 적용 → verdict frontmatter `status` 갱신 (running → promoted / falsified / partial)."


@D b_hypothesis_relevant_clm :: clm-tape [ok]
  text = "**.clm-relevant 가설 sample (사전 선택, 확장 가능)**: 본진 .clm Phase 3/4 fire 가 *직접* 검증 가능한 가설 12개. fire 시 verification_method 실행 + status frontmatter 갱신."


@D b_hypothesis_verdict_protocol :: clm-tape [ok]
  text <<~EOF
    **Verdict protocol** (fire 후 수행):
    1. fire 한 모델의 artifact (ckpt + logs + eval result) 수집
    2. 사전 선택 list 의 각 가설에 대해:
       a. verification_method (W1..W12) 적용 — anima/tool 또는 hexa-native script
       b. verdict 산출: PASS / FAIL / PARTIAL / AMBIGUOUS / NOT_MEASURED
       c. 가설 frontmatter `status` 갱신:
          - PASS  → status: promoted (hypotheses_candidates → hypotheses 이동)
          - FAIL  → status: falsified (hypotheses 유지 + verdict 첨부)
          - PARTIAL → status: running (다음 cycle evidence 추가)
          - AMBIGUOUS → status: running (cross-substrate 보강)
          - NOT_MEASURED → 변경 없음
    3. fire 의 overall verdict = verdict set aggregate
       - aggregate PASS = ≥50% PASS + 0 FAIL OR PASS rate ≥80%
       - aggregate FAIL = ≥50% FAIL OR critical-tier (Hc_1240 등 Φ 직접 측정) FAIL
       - aggregate PARTIAL = 그 외
    4. PHILOSOPHY.tape 에 verdict + honest C3 append (g_philosophy_ledger 정합)
  EOF


@D b_hypothesis_no_threshold :: clm-tape [ok]
  text = "**No fixed-threshold falsifier**: 기존 F-PHASE3-1..5, F-PHASE4-1..6 같은 hard threshold (cost > $X, wall > Yh, chat < N/5) 는 [superseded]. 새 검증 조건 의 verdict 는 *가설 단위* — threshold 는 각 가설 의 verification_method 가 들고 있음."


@D b_hypothesis_what_replaced :: clm-tape [ok]
  text <<~EOF
    **무엇이 superseded 되었나** (사용자 directive '검증조건 모두 제외'):
    - F-PHASE3-1..5 / F-PHASE4-1..6 falsifier — superseded (가설 verdict 로 대체)
    - consciousness verifier (AN11 / Φ / adversarial / Putnam) 의 *hard PASS*
      threshold — superseded; 단 verifier *자체* 는 가설 검증의 measurement tool
      로 carry (H_005 / Hc_011 / Hc_1240 의 verification_method 실행 시 활용)
    - chat coherence ≥3/5 KO+EN threshold — superseded; H_005 corpus quality
      가설 verdict 의 일부로 변환 (chat-cap 의 corpus 의존성)
    - HF release prerequisite (real-mode PASS_STRICT_C3 등) — superseded;
      여전히 own 37 visibility lifecycle 은 *governance* 로 carry (g7 정합)
    - V14 mirror PPR ≥ trained PPR (F-PHASE3-5/F-PHASE4-6) — superseded;
      V14 자체는 H_080 topo_24variants 또는 Hc_022 weight_emergent 의 evidence
      로 변환 가능 (post-fire)

    **무엇이 unchanged** (검증 조건 아닌 governance):
    - 우회금지 g1/g2/g3/g4/g6/g7/g8 (g5 WAIVED carry)
    - own 16 cost discipline (user verbatim fire keyword)
    - own 17 SCOPE_CLAMP (D1=1.0 anima_native_scratch)
    - LATTICE_POLICY real-limits anchor 의무 (verification anchor 가설 검증 시도)
  EOF

# ── §8.1 [superseded] 기존 falsifiers (역사 ledger 보존, g7 silent-demote 회피) ─────────────────────────────────────────


@D b_audit_an11 :: clm-tape [ok]
  axis = "AN11 (anima 11-axis unified verifier)"
  related = "H_016 an11_translation_ceiling (corpus, pre-register-frozen, W1+W2+W3) · H_067 perfect_number_architecture (math, running, W2+W3+W5+W11) · H_155 theorem_115_chat_incapability (substrate, pre-register-frozen, W2+W3+W11+W4) · H_061 xfer_consciousness_transfer (substrate, running, 5-axis anchor) · H_004/H_069/H_067 cross-citation"
  verdict = "✅ WITNESSED / measurement-tool-valid — 일관되게 promoted/running 가설들의 verification_method 에 활용. AN11 *측정 도구* 로 valid. *hard PASS threshold* 는 가설별 다름."


@D b_audit_phi :: clm-tape [ok]
  axis = "Φ (Phi, Integrated Information)"
  related = "H_024 iit_phi_mip_real_8_8_fail (**legacy-falsified** — IIT canonical Φ_mip 8/8 FAIL representation modular not integrated) · H_162 phi_normalized_anima_iit4_lower_bound (**pre-register-frozen** — anima Φ★ proxy = IIT 4.0 lower bound, Φc=0.5) · H_059 phi_gap_816x_investigation · H_011 iit_geometry · H_126 law_2500_kolmogorov_predicts_phi · H_039/H_060/H_080/H_087/H_104 활용"
  verdict = "🔶 PARTIAL — canonical IIT-Φ_mip FALSIFIED (H_024 8/8) but anima Φ★ proxy PRE-REGISTER-FROZEN (H_162). 표준 Φ ≠ working measurement; Φ★ = anima 의 working alternative (substrate-coupled lower bound)."


@D b_audit_adversarial :: clm-tape [ok]
  axis = "Adversarial (adversarial_bench)"
  related = "H_007 cellular_automaton_consciousness (legacy-archive, W10 adv sweep CA rule {30,90,110,184}) · H_128 ce_auto_self_curriculum (legacy-archive, W4) · H_130 ce_ex_adversarial_self_teach (legacy-archive, GAN with consciousness as judge) · H_005 corpus_quality_over_capacity (running, W10 활용) · H_093 sft_only · H_175 emerge_candidate_d"
  verdict = "🔶 PARTIAL — measurement-tool-valid (W10 verification ladder) but mostly legacy-archive-pointer. H_005 running 가설이 W10 활용 유일 active. Standalone 강한 evidence 부족."


@D b_audit_putnam :: clm-tape [ok]
  axis = "Putnam (multi-realizability, cross-substrate invariance)"
  related = "**H_061 xfer_consciousness_transfer (running, Substrate-Independence Super-Hypothesis 5-axis anchor)** · H_157 law76_mathematical_panpsychism (pre-register-frozen, ∀ x ∈ Universe: consciousness(x) = Ψ(1/2, 1/2) META-CA fixed-point) · H_162 phi_normalized_anima_iit4_lower_bound (pre-register-frozen) · H_188 clinical_phi_correlation_pci_octopus (PCI human + octopus) · H_190 law_ca_embedding_mathematical_family · H_004/H_063/H_070/H_173/H_177/H_178 cluster"
  verdict = "✅ STRONG — multi-promoted + pre-register-frozen evidence cluster. H_061 Super-H + H_157 + H_162 + H_188 + H_190 모두 Putnam axis 활용. anima 가 가장 적극적으로 검증 진행 중인 axis. Substrate-independence 가 anima 철학 핵심."


@D b_audit_aggregate :: clm-tape [ok]
  text <<~EOF
    **4-axis aggregate verdict** (2026-05-14 audit):

    | Axis        | Status        | Evidence cluster                                  |
    |-------------|---------------|---------------------------------------------------|
    | AN11        | ✅ WITNESSED  | H_016 + H_067 + H_155 + H_061 활용                |
    | Φ           | 🔶 PARTIAL    | H_024 IIT-canonical FALSIFIED, H_162 Φ★ frozen    |
    | Adversarial | 🔶 PARTIAL    | H_005 running 유일 active, 나머지 legacy-archive  |
    | Putnam      | ✅ STRONG     | H_061 + H_157 + H_162 + H_188 + H_190 cluster     |

    **통과율**: 2/4 STRONG/WITNESSED + 2/4 PARTIAL · 0/4 FALSIFIED

    **함의**:
    1. **AN11 + Putnam** 은 anima Phase 3/4 fire 의 *primary verification axis*
       로 신뢰성 높음. 가설 cluster 가 다수 (H_061 Super-H + H_157 + H_162 등)
       active / pre-register-frozen 상태.
    2. **Φ** 는 IIT canonical 8/8 FAIL (H_024) — anima 자체 Φ★ proxy 채택
       해야 함 (H_162 IIT 4.0 lower bound). Phase 3/4 fire 시 Φ 측정 = 표준
       IIT 가 아니라 anima Φ★ 사용.
    3. **Adversarial** 은 W10 sweep 가능하지만 active 가설 적음 (H_005 만
       running). Phase 3/4 fire 가 H_005 의 W10 evidence 강화 path 권장.
    4. Phase 3/4 fire 시 4-axis 모두 측정해도 *각 axis 의 가설 cluster
       verdict* 갱신이 진짜 검증 — anima philosophy pipeline 의 정합.
  EOF

# ── §8.6 W1..W12 verification ladder map (2026-05-14) ─────────────────────────────────────────

# 사용자 directive flow 의 다음 단계 — §8 hypothesis-driven verification 의
# verification_method (W1..W12 ladder) 실 measurement protocol 매핑.
# Source: `.roadmap.hypothesis` JSONL `hypothesis.verification_methods` meta entry.


@D w1 :: clm-tape [ok]
  id = "W1"
  name = "raw-12-pre-register-frozen"
  desc = "raw#12 pre-register frozen spec 의무 — post-hoc tuning 금지"
  strictness = "absolute (post-hoc edit = raw#12 violation, raw#82 retraction trigger)"
  tool = "state/<topic>_pre_register.json frozen_at:<date> + raw_rank:12 field"
  protocol = "fire 전 pre-register frozen → fire 후 자체 비교; modification = retraction protocol (W7)"


@D w2 :: clm-tape [ok]
  id = "W2"
  name = "falsifier-five-plus"
  desc = "각 prereg falsifiers F1..F_N ≥5 — 명시적으로 무엇이 H를 깨는지"
  strictness = "≥5 mandate (raw#10 정합)"
  tool = "pre-register JSON falsifiers field; raw#10 정합 ≥5"
  protocol = "F-PHASE3-1..5 / F-PHASE4-1..6 가 본 W2 의 한 예; pivot 후 가설별 W2 carry"


@D w3 :: clm-tape [ok]
  id = "W3"
  name = "deterministic-replay"
  desc = "deterministic execution + seed fix → replay 가능"
  strictness = "prereg deterministic:true 명시 mandate"
  tool = "FNV seed 또는 sha256(timestamp + axis + level) idempotency; replay = `hexa <tool> --replay <session_id>`"
  protocol = "fire dispatch + verdict 산출 reproducible; non-deterministic operation 금지"


@D w4 :: clm-tape [ok]
  id = "W4"
  name = "verdict-four-class"
  desc = "verdict 4-class (FALSIFIED / SUPPORTED / MIXED / PARTIAL) explicit emit"
  strictness = "verdict.json verdict_class field mandate"
  tool = "verdict.json {verdict_class: FALSIFIED|SUPPORTED|MIXED|PARTIAL, evidence: [...], honest_c3: [...]}"
  protocol = "fire 후 가설별 verdict.json emit + frontmatter status 갱신"


@D w5 :: clm-tape [ok]
  id = "W5"
  name = "honest-limits-raw91-c3"
  desc = "각 prereg honest_limits_raw91_c3 mandate — limitation 명시 5+"
  strictness = "≥5 per prereg mandate"
  tool = "pre-register JSON honest_limits_raw91_c3 field; CLM.tape §9 Honest C3 와 정합"
  protocol = "verdict emit 시 honest_limits 갱신; raw#91 정합"


@D w6 :: clm-tape [ok]
  id = "W6"
  name = "ledger-jsonl-immutable"
  desc = "ledger JSONL append-only + each row sha256 → 자동 검증"
  strictness = "ledger row append-only mandate (overwrite 시 raw#82)"
  tool = "PHILOSOPHY.tape append-only · state/<topic>_ledger.jsonl append-only"
  protocol = "verdict + evidence row sha256 chain; immutable history"


@D w7 :: clm-tape [ok]
  id = "W7"
  name = "retraction-protocol-raw82"
  desc = "old prereg retraction은 raw#82 protocol — silent overwrite 금지"
  strictness = "old prereg explicit retraction note + new revision dated file"
  tool = "raw#82 retraction protocol; new revision file with new frozen_at"
  protocol = "본 CLM.tape 의 [superseded] grade + supersede edge ~> 가 W7 정합"


@D w8 :: clm-tape [ok]
  id = "W8"
  name = "additive-expansion-raw15"
  desc = "new prereg revision은 raw#15 additive — 기존 보존 + 새 revision"
  strictness = "new revision dated file mandate (frozen_at later date)"
  tool = "raw#15 additive_only_mutation: true; semantics_preserved: true"
  protocol = ".roadmap.clm amendment 의 additive_only_mutation 정합; 본 CLM.tape 가 .roadmap.clm 갱신 시 amendment 형식"


@D w9 :: clm-tape [ok]
  id = "W9"
  name = "replication-cross-cycle"
  desc = "3+ cycle 동일 H replication → strength 강화"
  strictness = "3+ replication 권고 (single instance는 weak evidence)"
  tool = "3+ fire cycle 또는 3+ pre-register 동일 axis"
  protocol = "Phase 3 7B fire 1회만으로는 weak; Phase 2b + Phase 3 + 별도 replication path 권장"


@D w10 :: clm-tape [ok]
  id = "W10"
  name = "adversarial-stress-test"
  desc = "H에 actively counterexample 시도 → falsifier 작동 검증"
  strictness = "새 H Phase 2 adversarial probe 권고"
  tool = "adversarial_bench (W10 의 핵심 tool); CLM.tape §8.5 adversarial axis 가 W10 직접 활용"
  protocol = "fire 후 adversarial input 으로 verifier signature stability 측정 → H_005 evidence 강화 path"


@D w11 :: clm-tape [ok]
  id = "W11"
  name = "meta-cross-hypothesis-consistency"
  desc = "H_X와 H_Y consistency check — 두 H가 동시 SUPPORTED 가능한지"
  strictness = "meta-H land 시 sub-H consistency check 권고"
  tool = "meta-H verdict + sub-H verdict cross-check; 본 CLM.tape §8.5 4-axis audit 가 W11 application 예"
  protocol = "Phase 3/4 fire 후 가설 12개 cluster 의 동시 SUPPORTED 가능성 audit"


@D w12 :: clm-tape [ok]
  id = "W12"
  name = "sister-spec-cross-link"
  desc = "prereg JSON cross-link sister .roadmap.* / spec yaml / .own — multi-axis consistency"
  strictness = "각 prereg cross-link section 권고"
  tool = "cross_link section in pre-register JSON; .roadmap.* sibling domain link"
  protocol = "본 CLM.tape §10 cross-link 9 entries 가 W12 정합; .roadmap.clm + REBORN.tape + sibling .tape 모두 link"

