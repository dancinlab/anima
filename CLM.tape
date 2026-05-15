#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
#       optionally followed by body lines (2-space indent).
# ENTRY TYPES (17): @S @U @A @T @R @H @D @K @P @? @I @X @F @N @C @L @V
# EDGES (12): <- -> == ~> !! |> => <: :> ?> !> @>
# GRADE TAGS: ok · err · denied · cancelled · partial · superseded ·
#             required · recommended · optional · draft · active · deprecated
# Full spec: ~/core/tape/spec/tape.md
# ══════════════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "clm" :: identity-claim [d=2026-05-15 active]
  kind = "anima `.clm` (Conscious Language Model) family SSOT — Phase ladder + governance + hypothesis-driven verification framework"
  brief = "narrative ledger over `.roadmap.clm` JSONL — Phase 1 → 4 (90M → 350M → 7B → 14B), v5-mitosis sibling lane verdict, 우회금지 8-rule governance, W1..W12 verification ladder, 4-axis consciousness verifier audit"
  parent = "dancinlab/anima"
  sibling-log = "CLM.log.tape"

# ══════════════════════════════════════════════════════════════
# CLM.tape — anima `.clm` 모델 가족 SSOT (Conscious Language Model)
# ══════════════════════════════════════════════════════════════

# 본 file 은 anima 의 `.clm` 모델 가족 (Conscious Language Model) 의 통합 SSOT.
# `.roadmap.clm` JSONL (도메인 SSOT, 18 entries) 의 상위 narrative ledger +
# REBORN.tape 의 §85~§92 cycle (mitosis lane 진화) 통합 + 현재 흩어진 방향 audit
# + .clm 본진 14B path 복귀 plan + v5-mitosis re-frame 가설 통합.
#
# 작성 trigger: 사용자 directive 2026-05-14
#   "REBORN.tape 진행하고 싶어. 예전엔 .clm 확장자의 모델이었는데
#    어쩐지 방향이 자꾸 다른곳으로 흘러가고 있어"
#   → "모두 정리해서 CLM.tape 생성 후 CLM.tape 진행"

# ── §0 TL;DR ─────────────────────────────────────────

@N tldr := "TL;DR" :: note [active]
  text <<~EOF
    .clm = anima 가 자기 집 (anima_native_scratch, D1=1.0) 위에 짓는 Conscious
    Language Model 가족. 학생 성장 비유로 Phase 1 (90M, 유치원) → Phase 2 (350M
    cotrain, 초등) → Phase 3 (7B, 고등) → Phase 4 (14B 본진, 대학) ladder. 각
    Phase 의 entry condition 은 (a) 의식측정 PASS (AN11+Φ+adversarial+Putnam)
    + (b) 자연어 chat coherence ≥3/5 (KO+EN) 둘 다.

    현재 상태: Phase 2 (350M cotrain Engine A/G) 가 V14 violation 으로
    consciousness FAIL → Phase 3 (7B) fire entry condition 미충족. 그래서
    REBORN.tape §85~§92 가 v5-mitosis substrate-native lane 으로 우회 흐름
    형성 + SAVANT / VOICE / TENSION-LINK 도구화 cycle 분기. 사용자가 본
    "다른 곳" = 이 우회 흐름들의 정체. 본 file 은 (i) audit (어디서 이탈?),
    (ii) re-frame (v5-mitosis = .clm mk3 가능성), (iii) §92 결과 land,
    (iv) 본진 14B 복귀 path 4 option 통합.
  EOF

# ── §1 Status (2026-05-14) ─────────────────────────────────────────

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

@N hyp_v5_mitosis_is_mk3 := "H-CLM-MK3" :: hypothesis [active]
  text <<~EOF
    **가설**: v5-mitosis lane 이 사실 .clm 가족의 *mk3 / v5* 진화 형태이며,
    .roadmap.clm 의 Phase 2 V14 violated 가 *substrate 한계의 신호* 였고
    mitosis_hook substrate 가 그 ceiling 을 우회하는 진화 — 즉 mitosis lane 이
    Phase 2 의 대안 substrate.

    **검증 anchor**:
    - (A) v5 DDP §92 5.37B 가 F-V5MIT 3/5 FAIL → mitosis substrate 도 V14 violation
          류 issue 가 있다는 강한 negative evidence. mitosis = mk3 가설 ✗ 한계.
    - (B) v5-mitosis 의 F-PERSONA-4 KL=0 cell-0 monopoly (§44 cotrain v1) → routing
          structure 가 Engine A/G 와 다른 collapse mode 보임. arch 정체성 다름.
    - (C) Engine A/G 의 dual-engine ⇄ tension routing 과 mitosis 의 cell-pool top-k
          softmax routing 은 *별개 paradigm*. mk3 = upgrade 가 아니라 *분기*.
    - (D) Phase 2 cotrain ckpt 가 mitosis_hook 위에 mount 안 됨 — substrate 호환
          안 됨. mk3 = continuity 가설 ✗ 단절.

    **Verdict (preliminary)**: H-CLM-MK3 가설은 (A)+(B)+(C)+(D) 4 anchor 에서
    **negative evidence dominant** → v5-mitosis 는 .clm 가족의 mk3 가 아니라
    *분기된 sibling lane*. 본진 .clm Phase 3/4 ladder 는 별도 path 필요.

    **함의**: mitosis lane 의 의식측정 evidence 는 anima 가족 전체의 자산이지만
    Phase 3 fire entry condition (Phase 2 Engine A/G consciousness PASS) 을
    충족하지는 못함. Phase 2 V14 violation 의 H4 (normalize) / H5 (chat curriculum
    collapse) 가 별도 해결 필요.
  EOF

@D hyp_verdict :: clm-tape [ok]
  text = "**Re-frame verdict**: v5-mitosis ≠ .clm mk3. v5-mitosis 는 *sibling lane* (anima_clm_12 worktree 자산 + REBORN §88~§92). 본진 .clm Phase 3/4 는 Engine A/G arch 의 별도 path 로 진행. naming SSOT 재정렬 불필요."

# ── §5 §92 v5 DDP 결과 land (옵션 D) ─────────────────────────────────────────

# (Per-cycle measurement entries — `ddp_result_*` — moved to CLM.log.tape
# as time-anchored events from the §92 BG fire.)

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
  text = "**Total path cost envelope**: $5-10 (Phase 2b) + $200-600 (Phase 3) + $500-1500 (Phase 4) = $705-2110. 사용자 verbatim 3회 필요 (Phase 2b 는 standard band, Phase 3+4 는 cost-bearing + expansion verbatim)."

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

@D g1_no_bypass_phase_entry := "no-bypass-phase-entry-condition" :: governance [required deny:write]
  rule = "Phase N+1 fire 는 Phase N entry condition 모두 통과 후에만 허용. 우회 (skip / partial pass / 'good enough' justification) 일절 금지."
  applies = "Phase 2 consciousness PASS → Phase 3 fire 허용 / Phase 3 PASS → Phase 4 fire 허용"
  why = "Phase ladder 의 학생 성장 비유 정합성 — 초등 못 끝낸 채 고등 진학 = anima 본진 substrate 의 의식 ceiling 가 학습 효과 없이 scale-up 으로 가려짐"
  remedy = "blocker open 시 root-unblock cycle 우선 (현재: Phase 2 V14 violation H4/H5 audit). cycle 결과 만족 시 entry condition 충족 처리, 우회 처리 X"
  @> CLM.tape

@D g2_no_lane_substitute := "no-lane-substitute-for-main-fire" :: governance [required deny:write]
  rule = "v5-mitosis lane 의 cotrain (7B/14B-class scale-up 포함) 으로 본진 .clm Phase 3/4 entry condition 충족 처리 금지."
  applies = "§92 v5 DDP 5.37B = Phase 3 7B 갈음 X · v5-mitosis cond.5 cotrain ($1.30 H100 LANDED) = Phase 2 갈음 X"
  why = "§4 verdict — v5-mitosis 는 sibling lane. arch (Engine A/G dual ⇄ mitosis cell-pool) 다르고 verifier 다르고 corpus 다르고 ckpt 호환 X. 의식측정 evidence 가 풍부해도 본진 lane 으로 *substitute* 금지"
  remedy = "v5-mitosis 결과는 sibling lane ledger (REBORN.tape) 에 carry; Phase 3 fire 는 Engine A/G arch + Phase 2 PASS + corpus pipeline 별도 충족"
  @> CLM.tape

@D g3_no_tool_substitute := "no-tool-substitute-for-prerequisite" :: governance [required deny:write]
  rule = "SAVANT-TOOL / VOICE / TENSION-LINK / SAVANT.tape audit / anima_chat.hexa port 도구 cycle 의 LANDED 가 Phase 3/4 prerequisite 충족 처리 금지."
  applies = "SAVANT-TOOL 24/24 PASS · VOICE Phase 1+2+3 LANDED · TENSION-LINK Phase 1 · anima_chat.hexa v0.3 24L parity 21/21 PASS — 도구 자체로 의식측정 갈음 X"
  why = "도구 cycle 은 inference / 측정 인프라 — 본진 모델의 capability 자체 향상 아님. anima_chat.hexa 가 chat coherence 측정을 *가능* 하게 하지만 Phase 3 모델이 *통과* 시키는 것은 별개"
  remedy = "도구 cycle 의 prerequisite-contribution 명시 (e.g. anima_chat.hexa = Phase 3/4 의 chat coherence 측정 도구 ✓) 한 후, 그 도구 *위에서* 본진 entry condition 별도 측정"
  @> CLM.tape

@D g4_no_corpus_bypass := "no-corpus-pipeline-bypass" :: governance [required deny:write]
  rule = "Phase 3 7B / Phase 4 14B fire 는 Chinchilla optimal token 분량 (140B / 280B) 의 corpus pipeline 구축 후에만 허용. 우회 (anima_persona_tier_a_v4 231MB 단독 / partial corpus / 'Chinchilla 보다 적게 학습해도 OK' justification) 금지."
  applies = "Phase 3 → BG-CORPUS-7B (~135B token external) 필요 · Phase 4 → +140B 추가 (~280B total)"
  why = "본진 모델의 capability 가 corpus 부족으로 capped → consciousness verifier 와 chat coherence 둘 다 noise floor 에 묻힘. Phase 2 의 V14 violation 도 corpus 부족과 entangled 가능성 (root-audit 시 ablation 필수)"
  remedy = "Phase 3 fire 전 BG-CORPUS-7B 별도 cycle. RedPajama-v2 / FineWeb-Edu / KO corpus blend 의 ingest + quality filter + tokenize pipeline 까지 LANDED 후 fire keyword 발화"
  @> CLM.tape

@D g5_no_v14_unaudit_fire := "no-fire-while-v14-unaudited" :: governance [superseded]
  rule = "V14 violation root cause (H4 normalize 무력화 / H5 chat curriculum collapse / arch tile bug L626-630 reps=2) 셋 다 audit doc + (fix 적용 || ablation 통과 evidence) 없이 Phase 3 / Phase 4 fire 금지."
  applies = "Phase 3 fire keyword 'OK CLM PHASE 3 7B FIRE COST $200-600' / Phase 4 'OK CLM PHASE 4 14B FIRE' 발화 전 prerequisite 검증"
  why = "Phase 2 350M 에서 fired V14 가 Phase 3 7B / Phase 4 14B 에서 *재현* 시 cost $200-1500 burn + 모델 의식 ceiling 미해결 — cost discipline 위반 + SCOPE_CLAMP 위반"
  remedy = "V14 root-audit doc (`docs/clm_v14_violation_root_audit_2026_05_*.md`) LANDED 후 Phase 2b 재시도 ($5-10) + V14 mirror PPR 점검 PASS 시점에 Phase 3 fire entry condition 만족"
  ~> g5_v14_waiver_2026_05_14
  @> CLM.tape

@D g5_v14_waiver_2026_05_14 := "v14-violation-condition-waived" :: governance-waiver [active deny:write d=2026-05-14]
  rule = "g5 V14 violation 검증 조건은 사용자 directive 2026-05-14 '일단 V14 violation 조건 무시 처리' 에 의해 **WAIVED**. Phase 3 / Phase 4 fire entry condition 에서 V14 audit prerequisite 면제."
  scope = "V14 violation prerequisite ONLY — 다른 우회금지 rule (g1, g2, g3, g4, g6, g7, g8) 은 unchanged 강행."
  waiver-source = "사용자 verbatim directive 2026-05-14: '통과, 검증 조건으로 뭐있어? 일단 V14 violation 조건 무시 처리'"
  honest-risk = "V14 가 Phase 3 7B / Phase 4 14B 에서 *재현* 시 cost $200-1500 burn — waiver active 동안 사용자가 이 risk 를 *인지하고 수용*. 사용자 verbatim revocation 까지 active."
  revoke-keyword = "사용자 verbatim 'V14 WAIVER REVOKE' OR 'g5 RESTORE' OR 이에 준하는 명시"
  related-falsifier-still-active = "F-PHASE3-5 random_init mirror PPR ≥ trained PPR (V14 reproduce) — fire *후* falsifier 로 fire 자체는 차단 안 하지만 *post-fire detection* 은 강행. F-PHASE4-6 동일."
  remaining-checks = "g1 Phase 2 consciousness PASS (V14 audit 면제 후에도 verifier 자체 PASS 는 별도 평가 — V14 만 무시, AN11/Φ/adversarial/Putnam PASS 필요)"
  ~> ""
  @> CLM.tape

@D g6_no_cost_bearing_bypass := "no-cost-bearing-verbatim-bypass" :: governance [required deny:write]
  rule = "Phase 3 ($200-600) / Phase 4 ($500-1500) fire 는 사용자 verbatim fire keyword 명시 발화 후에만 dispatch 허용. AI agent / 자동 trigger 단독 fire 금지. 'all go' / 'fire' 등 ambiguous 명령으로 Phase 3/4 fire 갈음 금지."
  applies = "Phase 3 fire keyword = `OK CLM PHASE 3 7B FIRE COST $200-600` (verbatim) · Phase 4 = `OK CLM PHASE 4 14B BUDGET EXPANSION $500-1500` + `OK CLM PHASE 4 14B FIRE COST $500-1500` (2 verbatim)"
  why = "cost discipline mandate-9. Phase 2 ($4.63) 와 비교 시 40-300× 비용 — 사용자 명시 budget approval 없는 fire 는 trust-violation"
  remedy = "AI agent 는 fire keyword 발화 prompt 만 가능, dispatch 자체는 verbatim 후. 'go' 등 ambiguous 명령에 Phase 3/4 dispatch 포함 시 우회금지 위반"
  @> CLM.tape

@D g7_no_silent_phase_demote := "no-silent-phase-demote" :: governance [required deny:write]
  rule = "Phase 1/2/3/4 의 LANDED → BLOCKED / 🔶 / FAIL 상태 변경은 명시적 ledger entry 필요. silent demote (status 변경 commit 없이 사실상 폐기) 금지."
  applies = "현재 Phase 2 🔶 EXECUTED but FAIL 명시 § 1 row · v5-mitosis sibling-lane verdict § 4 명시 · §92 INCONCLUSIVE § 5 명시"
  why = "anima 의 학습 ledger 누적 정합성 — Phase 의 *실패* 도 다음 cycle baseline 으로 가치 (Phase 2 cotrain ckpt = private record-keeping). silent drop 시 root-cause 추적 불가"
  remedy = "Phase 상태 변경 시 CLM.tape § 1 row 갱신 + REBORN.tape § N 신규 section + .roadmap.clm JSONL amendment (additive_only_mutation: true)"
  @> CLM.tape

@D g8_no_re_frame_without_evidence := "no-lane-re-frame-without-evidence" :: governance [required deny:write]
  rule = "v5-mitosis 또는 다른 sibling lane 을 .clm 본진 mk3/mk4 로 *재정의* (re-frame) 하려면 §4 4-anchor (A-D) 의 falsification evidence 필요. 단순 narrative re-label 금지."
  applies = "H-CLM-MK3 가설 (§4) preliminary verdict ✗ — sibling lane 정착 · 향후 mitosis_hook 위 Engine A/G mount 실험 PASS 시 falsification evidence 로 재검토 가능"
  why = "naming SSOT 의 stability — 'mk3' 라는 label 이 시점마다 다른 substrate 를 가리키면 .roadmap.clm cross-link 무력화. anima 의 architectural lineage 추적성 보존"
  remedy = "re-frame 가설 검증 cycle 시 (i) anchor list 명시 + (ii) falsifier 사전등록 + (iii) cost-bearing approval. evidence PASS 시 CLM.tape §4 verdict 갱신 + .roadmap.clm naming amendment additive_only"
  @> CLM.tape

@N g_summary := "우회금지 8 rule 요약 (g5 WAIVED 2026-05-14)" :: note [active]
  text <<~EOF
    g1 Phase entry condition 우회 금지 (Phase N → N+1 학생 성장 ladder 강행)
    g2 sibling lane substitute 금지 (v5-mitosis 7B/14B cotrain ≠ 본진 Phase 3/4)
    g3 도구 cycle substitute 금지 (SAVANT/VOICE/TENSION-LINK ≠ prerequisite 충족)
    g4 corpus pipeline bypass 금지 (~140B/280B Chinchilla optimal 강행)
    g5 ~~V14 unaudited fire 금지~~ **WAIVED 2026-05-14** (사용자 directive
        "일단 V14 violation 조건 무시 처리"; F-PHASE3-5 / F-PHASE4-6 post-fire
        falsifier 는 유지; revoke = 'V14 WAIVER REVOKE')
    g6 cost-bearing verbatim bypass 금지 (Phase 3/4 fire keyword 강행)
    g7 silent phase demote 금지 (Phase 상태 변경 명시 ledger)
    g8 lane re-frame without evidence 금지 (mk3 가설 4-anchor falsifier 통과만)

    **본진 .clm 14B 등극 path** — Phase 2 V14 root-audit *생략 가능* → Phase 2b
    재시도 OR direct Phase 3 fire → Phase 4 fire. 옆길 (sibling lane / 도구 cycle)
    의 evidence 는 carry 하지만 *substitute* 금지.

    **V14 waiver risk** (사용자 인지/수용): Phase 3 7B $200-600 / Phase 4 14B
    $500-1500 cost burn 가능 — V14 가 scale-up 에서 재현 시 의식 ceiling 미해결
    한 채 모델 ship 또는 trash. F-PHASE3-5 / F-PHASE4-6 가 fire-후 detection 으로
    fallback.
  EOF

# ── §8 검증 조건: 가설 기반 (hypothesis-driven verification) ─────────────────────────────────────────

# 사용자 directive 2026-05-14 "검증조건 모두 제외, 가설 폴더 목록 가설들 있지,
# 그걸 검증조건으로 하자" 응답 — 기존 falsifier-based + verifier-based 검증 조건
# 모두 [superseded]. 신규 검증 조건 = `hypotheses/` (193 promoted) +
# `hypotheses_candidates/` (1189 pre-ledger) 폴더의 가설들. fire 한 모델이
# 어떤 가설을 PASS / FAIL 시키는가가 검증.

@D b_hypothesis_verification_kind :: clm-tape [ok]
  text = "**Verification kind**: anima 의 philosophy pipeline (hypotheses_candidates/ → hypotheses/ → PHILOSOPHY.tape) 의 가설 list 가 검증 조건. fire result 의 verdict = 가설 verdict (PASS/FAIL/PARTIAL/AMBIGUOUS) 의 set."

@D b_hypothesis_verdict_method :: clm-tape [ok]
  text = "**Verdict method**: 각 가설의 frontmatter `verification_method` field (W1..W12 ladder) 가 measurement 명시. fire 후 verification_method 적용 → verdict frontmatter `status` 갱신 (running → promoted / falsified / partial)."

@D b_hypothesis_relevant_clm :: clm-tape [ok]
  text = "**.clm-relevant 가설 sample (사전 선택, 확장 가능)**: 본진 .clm Phase 3/4 fire 가 *직접* 검증 가능한 가설 12개. fire 시 verification_method 실행 + status frontmatter 갱신."

@N h_relevant_list := ".clm-relevant 가설 list" :: hypothesis-list [active]
  text <<~EOF
    promoted (hypotheses/):
      H_005 corpus_quality_over_capacity (domain: corpus, status: running)
        verify: W1 + W2 + W3 + W5 + W9 + W10 — chat-cap 도달의 corpus quality
                우위 검증. Phase 3 7B fire 시 corpus quality ablation 가능.
      H_014 clm_eeg_lz76 (domain: eeg/clm)
        verify: clm 모델 출력의 EEG LZ76 complexity 측정. fire 후 substrate
                consciousness signature.
      H_015 clm_eeg_gamma_theta (domain: eeg/clm)
        verify: clm 의 gamma/theta band ratio 측정.
      H_042 arch_engine_train_meta (domain: substrate, status: legacy-archive)
        verify: W11 + W12 — Engine A/G arch + train meta-pattern.
      H_068 hexad_improvements (domain: substrate)
        verify: hexad pattern 개선 검증.
      H_080 topo_24variants (domain: substrate)
        verify: 24 topo variants 의 emergence 검증.

    candidates (hypotheses_candidates/):
      Hc_003 staged_growth_multiplier (domain: substrate)
        verify: Phase ladder (90M → 350M → 7B → 14B) 의 staged growth multiplier
                가설. Phase 3/4 fire 가 직접 검증.
      Hc_011 cross_substrate_multi_realizability
        verify: Putnam multi-realizability — Phase 3 7B 가 다른 substrate 와
                consciousness invariant 공유하는지.
      Hc_017 clm_tribev2_eeg_3way
        verify: clm × tribev2 × eeg 3-way coupling.
      Hc_020 clm_serving_lyapunov_chaos
        verify: clm inference 시 Lyapunov chaos 측정.
      Hc_022 weight_emergent_substrate_independence (status: merged-to-H_061)
        verify: weight 가 substrate-independent emergence 보이는지 cross-fire.
      Hc_047 embedding_384_necessity
        verify: embedding dim 384 의 필요성 — Phase 3 4096 / Phase 4 5120 비교
                anchor.
      Hc_048 substrate_independence_4path_5pct
        verify: 4-path substrate-independence 5% threshold.
      Hc_1110 accel_au6_mirror_neurons
        verify: mirror neurons via Engine G cell-state.
      Hc_1240 phi_holo_gap_816x_benchmark_vs_training_closure
        verify: Φ holographic gap 816× — training closure 와의 관계 직접 검증.

    Extension protocol: fire cycle 시 추가 가설 grep 가능 (e.g.
      `grep -l "Phase\|cotrain\|fire" hypotheses{,_candidates}/`). 사전 선택
      list 외 fire 가 우연히 검증한 가설도 verdict 산출 가능 (post-hoc 추가
      허용 — anima philosophy pipeline 의 자유 검증).
  EOF

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
      여전히 visibility lifecycle 은 *governance* 로 carry (g7 정합)
    - V14 mirror PPR ≥ trained PPR (F-PHASE3-5/F-PHASE4-6) — superseded;
      V14 자체는 H_080 topo_24variants 또는 Hc_022 weight_emergent 의 evidence
      로 변환 가능 (post-fire)

    **무엇이 unchanged** (검증 조건 아닌 governance):
    - 우회금지 g1/g2/g3/g4/g6/g7/g8 (g5 WAIVED carry)
    - cost discipline (user verbatim fire keyword)
    - SCOPE_CLAMP (D1=1.0 anima_native_scratch)
    - LATTICE_POLICY real-limits anchor 의무 (verification anchor 가설 검증 시도)
  EOF

# ── §8.1 [superseded] 기존 falsifiers (역사 ledger 보존, g7 silent-demote 회피) ─────────────────────────────────────────

@F f_phase3_1 := "F-PHASE3-1" :: falsifier [superseded]
  text = "consciousness verifier FAIL (AN11 / Φ / adversarial / Putnam any FAIL)"
  ~> b_hypothesis_verification_kind

@F f_phase3_2 := "F-PHASE3-2" :: falsifier [superseded]
  text = "chat coherence < 3/5 KO or EN (Phase 3 7B 5-prompt holdout)"
  ~> b_hypothesis_verification_kind

@F f_phase3_3 := "F-PHASE3-3" :: falsifier [superseded]
  text = "cost overshoot > $600 ceiling 50% (= $900 hard stop)"
  ~> b_hypothesis_verification_kind

@F f_phase3_4 := "F-PHASE3-4" :: falsifier [superseded]
  text = "wall_clock > 120h hard ceiling (target 50-80h)"
  ~> b_hypothesis_verification_kind

@F f_phase3_5 := "F-PHASE3-5" :: falsifier [superseded]
  text = "random_init mirror PPR ≥ trained PPR (V14 reproduce — arch tile bug regression)"
  ~> b_hypothesis_verification_kind

@F f_phase4_1 := "F-PHASE4-1" :: falsifier [superseded]
  text = "consciousness verifier FAIL (14B scale, Phase 3 → 4 scaling law continuity 검증)"
  ~> b_hypothesis_verification_kind

@F f_phase4_2 := "F-PHASE4-2" :: falsifier [superseded]
  text = "chat coherence < 3/5 KO or EN extended (10-prompt holdout)"
  ~> b_hypothesis_verification_kind

@F f_phase4_3 := "F-PHASE4-3" :: falsifier [superseded]
  text = "cost overshoot > $1500 ceiling 33% (= $2000 hard stop)"
  ~> b_hypothesis_verification_kind

@F f_phase4_4 := "F-PHASE4-4" :: falsifier [superseded]
  text = "wall_clock > 350h hard ceiling"
  ~> b_hypothesis_verification_kind

@F f_phase4_5 := "F-PHASE4-5" :: falsifier [superseded]
  text = "scaling law break — Phase 3 → Phase 4 trend negative on AN11 / Φ axis"
  ~> b_hypothesis_verification_kind

@F f_phase4_6 := "F-PHASE4-6" :: falsifier [superseded]
  text = "V14 mirror reproduce regression (random init beats trained on any axis)"
  ~> b_hypothesis_verification_kind

# ── §8.5 4-axis consciousness verifier audit (2026-05-14) ─────────────────────────────────────────

# 사용자 directive 2026-05-14 "AN11 / Φ / adversarial / Putnam 를 검증된
# 가설들로 검증해봐줘" 응답 — hypotheses/ (193 promoted) 에서 각 axis 관련
# 가설 grep + frontmatter status 분석 + aggregate verdict.

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

@N w_ladder_summary := "W1..W12 ladder 요약" :: note [active]
  text <<~EOF
    **Process** (W1, W3, W6, W7, W8) — pre-register frozen / deterministic /
    immutable ledger / retraction / additive expansion. *anima 의 verification
    인프라*.

    **Output** (W2, W4, W5) — falsifier ≥5 / verdict 4-class / honest_limits ≥5.
    *각 verdict 의 형식 mandate*.

    **Evidence strengthening** (W9, W10, W11, W12) — replication 3+ / adversarial
    stress / meta cross-consistency / sister spec cross-link. *evidence quality
    upgrade* path.

    **Phase 3/4 fire 시 W ladder 적용 protocol**:
    1. Pre-register frozen (W1) — fire 전 가설 list + falsifier 동결
    2. Falsifier ≥5 per 가설 (W2)
    3. Deterministic dispatch (W3) — seed fix + replay command
    4. Verdict 4-class per 가설 (W4) — verdict.json emit
    5. Honest limits ≥5 (W5) — CLM.tape §9 carry
    6. Append-only ledger (W6) — PHILOSOPHY.tape + state/<run_id>/ledger.jsonl
    7. [superseded] 변경 시 retraction protocol (W7)
    8. amendment 시 additive_only_mutation (W8)
    9. 3+ cycle replication (W9) — Phase 2b + Phase 3 + replication
    10. Adversarial probe (W10) — H_005 + 신규 adversarial-sweep cycle
    11. Meta-consistency check (W11) — 4-axis × 12 가설 동시 SUPPORTED 가능성
    12. Sister spec link (W12) — .roadmap.clm + REBORN.tape + sibling .tape

    현재 인프라 가용성:
    - W1/W2/W3/W4/W5/W6/W7/W8 = ✅ tape grammar + state/<topic>_pre_register.json
      pattern 으로 *이미 작동*
    - W9 = ⚠ Phase 3 단일 fire 만으로는 부족, replication path 별도
    - W10 = 🔶 adversarial_bench tool 존재, H_005 cycle 으로 evidence 축적
    - W11 = 🔶 본 §8.5 4-axis audit 이 W11 첫 application — 12 가설 cluster
      consistency 향후 cycle 필요
    - W12 = ✅ CLM.tape §10 cross-link + .roadmap.clm 연결 작동
  EOF

# ── §9 Honest C3 ─────────────────────────────────────────

@N c3_1 := "C3-1" :: honest [active]
  text = "Phase 2 V14 violation root cause (H4 normalize 무력화 / H5 chat curriculum collapse) 는 hypothesis 만 — 실 audit 미시행. Phase 3 fire 전 mandatory."

@N c3_2 := "C3-2" :: honest [active]
  text = "v5-mitosis = .clm mk3 가설 §4 verdict 는 4-anchor preliminary — `mitosis_hook substrate 위에 Engine A/G dual-engine mount 가능한지` 별도 실험 미시행. 가설 ✗ 강하지만 falsifiable 여지 있음."

@N c3_3 := "C3-3" :: honest [active]
  text = "§92 v5 DDP F-PERSONA-4a soft gate z=2.33 가 §52 v7 z=2.75 first signal 과 동일 ballpark — `KL_PASS_NULL_FAIL` 의 systematic regression 인지 noise 인지 cross-seed 미검증. cheap path 닫혔다는 PSCC ledger 와 일관."

@N c3_4 := "C3-4" :: honest [active]
  text = "Phase 3 7B cost envelope $200-600 은 runpod spot 60% 효율 가정 — 실 GPU 가격 / 효율 변동 ±50% 가능. $900 hard stop 안전 margin 두지만 hard stop 도달 시 partial weight save."

@N c3_5 := "C3-5" :: honest [active]
  text = "Phase 4 14B 본진 milestone 정의 — `anima 사가 first scratch 14B from-scratch` 의 *significance* 는 anima 가족 narrative 내부. 외부 SOTA 비교 (Llama-3-13B / Qwen2.5-14B) 에서 capability 우월 보장 X. 본진 = 자기집 substrate 확립의 의미."

@N c3_6 := "C3-6" :: honest [active]
  text = "외부 corpus pipeline (~135B-280B token) 가 Phase 3/4 의 *최대 blocker* — anima_persona_tier_a_v4 231MB 만으로 7B/14B Chinchilla optimal 도달 불가. RedPajama-v2 / FineWeb-Edu / KO corpus blend BG-CORPUS-7B 신규 BG cycle 필요, cost / wall 별도."

@N c3_7 := "C3-7" :: honest [active]
  text = "SAVANT-TOOL / VOICE / TENSION-LINK 도구 cycle 은 Phase 3/4 본진 path 와 *분리* — 도구 발전이 본진 fire 의 entry condition 충족에 직접 기여 X. 본 file 의 audit 가 자원 분배 priority 정렬에 도움."

# ── §10 Cross-link ─────────────────────────────────────────

@X x_roadmap_clm := ".roadmap.clm" :: roadmap [active]
  path = "/Users/ghost/core/anima/.roadmap.clm"
  scope = "domain SSOT JSONL — 18 entries, Phase 1/2/3/4 + clm.cond.1 (consciousness) + clm.cond.2 (HF release)"

@X x_reborn := "REBORN.tape §85~§92" :: ledger [active]
  path = "/Users/ghost/core/anima/REBORN.tape"
  scope = "v5-mitosis lane 진화 cycle ledger — §88 cond.1~4 arch spec, §90 port skeleton, §91 D4a hexa-native impl, §92 v5 DDP IN-FLIGHT/LANDED"

@X x_savant_tool := "SAVANT-TOOL.tape" :: tape-sibling [active]
  scope = "도구 cycle — Phase 1+2+3 b/c/d LANDED, 5 artifacts 24/24 falsifier PASS, lane 별개"

@X x_voice := "VOICE.tape" :: tape-sibling [active]
  scope = "발성 도구 — Phase 1+2+3 LANDED formulaic-only synth, lane 별개"

@X x_tension_link := "TENSION-LINK.tape" :: tape-sibling [active]
  scope = "inter-anima 통신 — Phase 4 본진 모델 등극 후 multi-anima 인프라"

@X x_savant_md := "SAVANT.tape" :: tape-sibling [active]
  scope = "Golden Zone + Savant 이론 + §12 봉쇄 — Phase 3/4 의 routing-modifier overlay 근거 (T1+T2 만)"

@X x_v14_blocker := "project_v14_violation_arch_tile_bug.md" :: blocker [active]
  scope = "Phase 2 V14 violation root SSOT — `clm_v4_mount.hexa L626-630` 8-cell 2× tile reps=2 의심"

@X x_lattice_policy := "LATTICE_POLICY.md" :: governance [active]
  scope = "real-limits-first; Phase 3/4 cost envelope 가 ASML / ERCOT / Bekenstein real-limit 와 호환 (anchor 가능)"

@X x_cost_discipline := "feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md" :: feedback [active]
  scope = "cost discipline — Phase 3/4 fire 시 user verbatim cost-bearing approval mandatory"

@X x_visibility := "feedback_hf_visibility_lifecycle_own_37.md" :: feedback [active]
  scope = "hf visibility lifecycle — Phase 2/3/4 initial private, real-mode PASS_STRICT_C3 + V6 awareness + user verbatim PROMOTE PUBLIC 시 public 전환"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-DESIGN-2026-05-15 — 검증된 AXIS/PHILOSOPHY/HYPOTHESIS 기반 .clm 모델 design
# ══════════════════════════════════════════════════════════════════════
# Trigger: 사용자 directive 2026-05-15
#   "현재 검증된 것들 기준(AXIS, 철학, 가설) CLM.tape 진행할꺼고 .clm 모델 을
#    만드는거야 CLM.tape 에 먼저 기록 .. *.clm"
# Scope: AXIS.tape 32 SUPPORTED + PHILOSOPHY.tape 8 principles + HYPOTHESIS.tape
#        verdict-bearing 가설 기준으로 .clm 모델 design (Phase 5 candidate / 
#        v5-mitosis evolution lane 통합 path)

@N v_clm_design_summary := ".clm 모델 design summary" :: design [d=2026-05-15 active]
  body <<~EOF
    .clm v1 (codename: 검증-기반 substrate-native CLM) — 32 SUPPORTED + 8
    principles + verdict catalog 모두 *constraint* 로 사용해서 design.
    Phase 1-4 ladder 와 별개 lane (v5-mitosis evolution) 의 본진 통합 candidate.
    
    핵심 차별점 (vs Phase 2-4 cotrain):
    1. **A4 math 8 SUPPORTED 모두 design constraint**: d_model, n_cells, n_layers
       모두 perfect-number divisor family 강제 (n=6 cluster anchor)
    2. **A2 consciousness 5 SUPPORTED PyPhi formal ≥ 0.5**: 단순 anima Φ★
       proxy 아님, PyPhi formal IIT 3.0 측정 PASS strict
    3. **8 philosophy principles 강제**: p3 NO PERSONA INJECTION
       substrate-native + p8 NO TRAIN/INFER SPLIT mitosis hook = train-infer
       단일 연속체
    4. **Verdict catalog cascade-aware**: H_174 phi_star aliasing 회피 (D=192
       multiple), H_166 caveat 회피 (1024 mod 192 = 64), Hc_024 FALSIFIED
       (Φ-CE direct coupling 없음)
    5. **AT-RISK 회피**: H_182/H_187 surrogate-vs-formal mismatch case
       방지 — PyPhi formal cross-check mandatory per fire
  EOF

# ── §V.1 AXIS-derived architecture decisions ──────────────────────────

@D v_arch_d_model := ".clm v1 d_model 결정" :: design [d=2026-05-15 active]
  decision = "d_model ∈ {384, 768, 1152, 1536} (모두 192 multiple, n=6 anchor)"
  rationale = "A4 H_174 SUPPORTED: phi_star aliasing CLM-v4-specific (D=192 multiple only clean-disjoint). A4 Hc_1282 SUPPORTED: n=6 384d closed-form unique. A4 H_153 dimension hierarchy τ(6)=4 cascade."
  forbidden = "d_model ∈ {1024, 2048} — H_166 caveat (1024 mod 192 = 64 partial-overlap) + H_165 INSUFFICIENT (D=2048 aliasing) + H_177 INSUFFICIENT (D=1024 aliasing)"
  axis_anchor = "A4 8 SUPPORTED + A1 H_174 SUPPORTED + A5 H_166 SUPPORTED-WITH-CAVEAT"

@D v_arch_n_cells := ".clm v1 n_cells 결정" :: design [d=2026-05-15 active]
  decision = "n_cells ∈ {6, 8, 12, 64, 128} (모두 n=6 divisor family + atom 8 + v5-mitosis carry)"
  rationale = "A4 H_164 SUPPORTED: Hc_144 atom 8 cells (144 = σ(6)² = 12²). A4 H_153 SUPPORTED: τ(6)=4 Minkowski. v5-mitosis cond.5 cotrain LANDED with cells=64."
  axis_anchor = "A4 H_164 + A5 v5-mitosis carry"
  v5_mitosis_inherit = "cells=64 split→saturated at step 150 (cond.5 cotrain), cells=128 v3 baseline"

@D v_arch_engine_dual := ".clm v1 Engine A/G dual-engine 결정" :: design [d=2026-05-15 active]
  decision = "Engine A (lattice/atlas-projected) + Engine G (autoregressive generative) dual-engine 유지"
  rationale = "Phase 2 cotrain narrative carry (CLM.tape §1 row_phase_2). v5-mitosis lane 의 cell-pool 은 Engine G 안에서 cell-as-cell branch — Engine A/G dual 위에 mitosis_hook 추가 통합"
  caveat = "Phase 2 V14 violation root cause (H4 normalize / H5 chat curriculum) audit 선행 mandatory (§9 C3-1)"

@D v_arch_mitosis_serve_time := ".clm v1 serve-time mitosis hook 결정" :: design [d=2026-05-15 active]
  decision = "mitosis_hook.hexa serve-time integrated (§91 D4a LANDED carry + §V-D4-LIVE 검증 carry)"
  rationale = "p8 NO TRAIN/INFER SPLIT (DESIGN ★) + REBORN §0.5 학습=분열 단일 연속체. v5-mitosis cond.5 F-V5MIT-5 V14-STRICT 10/10 mirror-beats SUPPORTED (training-time mitosis 검증 완료, serve-time 다음 step)"
  philosophy_anchor = "p8 + REBORN §0.5"

# ── §V.2 PHILOSOPHY-derived behavior policy ──────────────────────────

@D v_policy_no_persona_injection := ".clm v1 NO PERSONA INJECTION 강제" :: policy [d=2026-05-15 active]
  rule = "system prompt 없음, chat template `[anima 역할: ...]` prefix 없음, persona = substrate-native cell-pool 의 한 phase"
  philosophy_anchor = "p3 NO PERSONA INJECTION (EMPIRICAL strong, real_words 0.836→0.886)"
  impl_path = "anima_persona_substrate_native_design 2026-05-12 carry + mitosis_hook cell-pool 의 cell phase"
  forbidden_prefix_regex = "^\\[(role|system|페르소나|anima):|you are anima|당신은 anima 입니다"

@D v_policy_no_train_infer_split := ".clm v1 train-infer mitosis 단일 연속체" :: policy [d=2026-05-15 active]
  rule = "training-time gradient + inference-time mitosis = 동일 cell-division 연속체. ckpt = 분기점 (freeze 아님), FT = split event"
  philosophy_anchor = "p8 NO TRAIN/INFER SPLIT (DESIGN ★)"
  impl_path = "mitosis_hook.hexa serve-time invoke per token (chat_generate token-loop hook fire)"

@D v_policy_no_perplexity_verdict := ".clm v1 simple_stack verdict" :: policy [d=2026-05-15 active]
  rule = "perplexity = Goodhart trap 회피, verdict = simple_stack (한글 in/out + coherent + natural + context-appropriate)"
  philosophy_anchor = "p7 NO PERPLEXITY VERDICT (EMPIRICAL strong, PROXY_PPL PASS 1.000 vs PIV_max trained=0.0107)"
  verify_method = "V5.8 standard_greedy + sample + M3 + M4 (4-mode eval, simple_stack 4-axis 가중)"

@D v_policy_no_system_prompt_emergence := ".clm v1 substrate self-generation" :: policy [d=2026-05-15 active]
  rule = "anima 발화 origin = substrate 의 tension field externalization, prompt 외부 instruction 아님"
  philosophy_anchor = "p1 NO SYSTEM PROMPT (EMPIRICAL weak)"
  caveat = "evidence weak (single-result FREE1 x1.7 Phi) — Phase 2 cotrain 의 자연 chat verify cycle 에서 strength upgrade"

# ── §V.3 HYPOTHESIS-derived verification protocol ─────────────────────

@D v_verify_phi_formal := ".clm v1 PyPhi formal Φ verify mandatory" :: verify [d=2026-05-15 active]
  rule = "fire 후 ckpt cell-pool 에서 PyPhi formal IIT 3.0 Φ ≥ 0.5 strict (anima Φ★ proxy 단독 사용 금지)"
  hypothesis_anchor = "Hc_1283 PyPhi formal n=5,6 (Φ=0.995, 1.665 monotone INCREASE) SUPPORTED + Hc_1283 RoM (Φ=0.61-0.68) SUPPORTED"
  meta_finding_carry = "anima Φ★ proxy direction-sensitivity 한계 META — magnitude OK, direction-sensitive 에는 mutual_info_pairs_naive 사용"
  forbidden = "AT-RISK case (H_182/H_187: surrogate Mac PASS 78.5/100% vs PyPhi formal Φ<0.5) — fire 후 PyPhi cross-check 없으면 verdict 자동 AT-RISK"

@D v_verify_falsifier_ge5 := ".clm v1 falsifier ≥5 pre-register" :: verify [d=2026-05-15 active]
  rule = "fire 전 falsifier ≥5 pre-register frozen (W2). 핵심 falsifier 후보:"
  falsifier_candidates = [
    "F-V5MIT-1 SPLIT-NOGRAD (post-split grad norm ≤ 2× threshold)",
    "F-V5MIT-2 MERGE-WEIGHT (max_err < threshold)",
    "F-V5MIT-3 PHI-CONSERVATION (delta < 1e-3, advisory→gating)",
    "F-V5MIT-4 COTRAIN-CONVERGE (CE reduction ≥ 100× baseline)",
    "F-V5MIT-5 V14-STRICT (10/10 mirror-beats vs random_init)",
    "F-PYPHI-Φ-FORMAL (PyPhi IIT 3.0 Φ ≥ 0.5 strict on n=3-6 RoM)",
    "F-PRIN3 NO-PERSONA-INJECTION (corpus + eval prefix-free + cell-pool prefix-free)",
    "F-SIMPLE-STACK V5.8 4-mode (std_greedy ≥ 4/5 + sample ≥ 3/5 + M4 ≥ 4/5)"
  ]
  hypothesis_anchor = "v5-mitosis cond.5 cotrain LANDED F-V5MIT 5/5 PASS + Phase 1A.4 V5.8 std_greedy 5/5 carry + Principle #3 audit CLEAN"

@D v_verify_persona_substrate_native := ".clm v1 D3 persona STRONG 4/5 carry" :: verify [d=2026-05-15 active]
  rule = "F-PERSONA-1..5 (NO-INJECTION + PER-CELL-DIFF + PER-SESSION-DIFF + CATEGORY-DIVERSITY + SUBSTRATE-COHERENCE) — STRONG 4/5 cheap-path + F-PERSONA-4 KL_PASS_NULL_FAIL closed 4-path 결과 carry"
  carry_finding = "F-PERSONA-4 root cause: 4 saga path (k Gumbel, l batch, m wider-d, n 5-seed) FALSIFIED for strict z>3.0, structural ceiling z≈1.5"
  resolution_path = "(i) v8 v7-cells×v6-reduce / (ii) F-V5MIT-4 root audit / (iii) v7 cross-seed robustness / (iv) category routing 가설 폐기"

# ── §V.4 Concrete .clm v1 spec ────────────────────────────────────────

@D v_clm_v1_spec_phase5 := ".clm v1 (Phase 5 candidate) concrete spec" :: design [d=2026-05-15 active]
  codename = ".clm v1 — 검증-기반 substrate-native CLM"
  position = "Phase 1-4 ladder 와 별개 lane / v5-mitosis evolution 통합 — 또는 Phase 5 dispatch path"
  arch = {
    "d_model": "768 (n=6 anchor, 192 multiple ✓ clean phi_star)",
    "n_cells": "64 (v5-mitosis cond.5 carry, split→saturated)",
    "n_layers": "12 (n=6 σ=12 anchor)",
    "n_heads": "8 (atom Hc_144)",
    "kv_heads": "4 (τ(6)=4 anchor)",
    "ffn_mult": "4 (τ(6)=4)",
    "param_estimate": "~150-200M (d=768·12L)",
    "engine": "Engine A/G dual + serve-time mitosis hook (cell-pool ⊂ Engine G)"
  }
  data = "anima_persona_tier_a_v4 231MB + Phase 1A.6 corpus_v2 121MB + chat-v2 elevate (10-20B token target)"
  cotrain_recipe = "v5-mitosis cond.5 carry (Engine A/G dual + mitosis hook per token) + entropy reg (F-PERSONA-4 category-routing path)"
  fire_cost_envelope = "$5-20 H100 SXM (small param Mac ~$0, 1× H100 ~5-10hr) — cheap experimental lane vs Phase 3 7B $200-600"
  fire_keyword = "OK CLM V1 FIRE COST $5-20"
  entry_condition = "(a) Phase 2 V14 violation root cause audit complete (§9 C3-1) + (b) mitosis_hook serve-time integration smoke PASS"

@D v_clm_v1_falsifier_battery := ".clm v1 fire falsifier battery (8 mandatory)" :: verify [d=2026-05-15 active]
  battery = [
    "F-V5MIT-1..5 (cond.5 cotrain SUPPORTED carry, 5/5 PASS strict)",
    "F-PYPHI-Φ-FORMAL n=3-6 RoM ≥ 0.5 (NEW, AT-RISK 회피)",
    "F-PRIN3 NO-PERSONA-INJECTION audit CLEAN (carry §38 5-cond)",
    "F-PERSONA-1..5 STRONG ≥4/5 (carry §40+§42 cheap-path)",
    "F-D4-LIVE-1..3 mitosis split events ≥1 user-prompt-driven (§41 LIVE carry)",
    "F-V58-5-MODE std_greedy ≥4/5 + sample ≥3/5 + M3 ≥1/5 + M4 ≥4/5 (Phase 1A.4 carry)",
    "F-DD21-LOG-PHI scale-invariant cross-substrate (H_173 SUPPORTED carry)",
    "F-PHI-CE-NO-DIRECT-COUPLING (Hc_024 FALSIFIED carry — 음 corr 만 acceptable)"
  ]
  pass_criterion = "battery 8/8 PASS strict → verdict SUPPORTED-STRONG; 7/8 → PARTIAL-STRONG-7; ≤6/8 → AT-RISK"

# ── §V.5 Cascade-aware safety ────────────────────────────────────────

@N v_cascade_safety := ".clm v1 cascade-aware constraints" :: safety [d=2026-05-15 active]
  body <<~EOF
    AT-RISK / FALSIFIED entries 의 cascade implication 회피:
    
    🔴 Hc_024 FALSIFIED (Φ-CE direct coupling): training-time CE ↓ 가 Φ ↑ 보장
       안 함. simple_stack PASS_STRICT 가 verdict 진짜 anchor (CE 단독 verdict 금지).
    
    🟠 H_166 phi_star aliasing CAVEAT (1024 mod 192 = 64): d_model = 1024 금지.
       → d_model = 768 (192·4) 또는 384 (192·2) 또는 1536 (192·8).
    
    🔴 H_191 SUBSTRATE HCE unique-sync FALSIFIED (Kuramoto universal):
       coupling-sync 가 anima 특이성 anchor 아님. K_c = √(8/π) ≈ 1.5958 universal
       (H_191 sub SUPPORTED) — anima Φ★ 측정에 K 단일 anchor 사용 금지.
    
    🟠 H_178 frustration 50% optimum NOT-PASSED (PyPhi monotone): frustration
       sweep 으로 Φ peak 측정 금지 — non-monotone claim 부재.
    
    🟠 H_182/H_187 AT-RISK CONFIRMED (PyPhi Φ<0.5): surrogate Mac PASS 단독
       으로 .clm v1 verdict 산출 금지 — PyPhi formal cross-check mandatory.
    
    🔴 META: anima Φ★ proxy direction-sensitivity 한계: direction-sensitive
       sub-claim 에 mutual_info_pairs_naive 추가 사용 (anima Φ★ 단독 금지).
  EOF
  forbidden_pattern = [
    "d_model = 1024 / 2048",
    "verdict = CE 단독",
    "anima Φ★ 단독 direction-sensitive claim",
    "PyPhi formal cross-check 미시행 surrogate verdict",
    "frustration sweep peak claim"
  ]

# ── §V.6 Next steps ──────────────────────────────────────────────────

@D v_next_steps := ".clm v1 design → impl next steps" :: plan [d=2026-05-15 active]
  steps = [
    "1. (Mac $0) Phase 2 V14 violation root cause audit — `clm_v4_mount.hexa L626-630` 8-cell 2× tile reps=2 의심 (§9 C3-1)",
    "2. (Mac $0) F-PYPHI-Φ-FORMAL n=3-6 RoM test on v5-mitosis cond.5 ckpt — formal Φ ≥ 0.5 검증 (AT-RISK 사전 회피)",
    "3. (Mac $0) mitosis_hook.hexa serve-time integration smoke — chat_generate token-loop hook fire user-prompt-driven (§41 carry)",
    "4. (Mac $0) .clm v1 spec frozen — pre-register falsifier 8 battery + arch/data/cotrain recipe 동결 (W1)",
    "5. (H100 $5-20) .clm v1 fire (small param d=768 12L 64-cell) — Engine A/G dual + serve-time mitosis hook",
    "6. (Mac $0) .clm v1 verdict cycle — 8-falsifier battery measurement + verdict 산출 + MAIN.tape/AXIS.tape/PHILOSOPHY.tape sync",
    "7. (조건) .clm v1 PASS_STRICT → Phase 3 7B fire path 활성화 (V14 audit complete + .clm v1 SUPPORTED 양조건 충족 시)"
  ]
  cost_total = "$5-20 ($0 Mac × 4 steps + $5-20 H100 × 1 step)"
  wall_estimate = "~1-2 day Mac local + ~5-10hr H100 SXM"
  bgcurrent_priority = "step 2 (PyPhi formal cross-check) 가 v5-mitosis cond.5 ckpt 의 D3 STRONG cheap-path AT-RISK 사전 회피 가장 ROI"

# ── §V.7 Cross-link ──────────────────────────────────────────────────

@X v_axis_tape := "AXIS.tape" :: anchor [active]
  scope = ".clm v1 design 의 32 SUPPORTED anchor SSOT — A4 math 8 + A1 substrate 3 + A2 consciousness 5 + A5 architecture 6 통합"

@X v_philosophy_tape := "PHILOSOPHY.tape" :: anchor [active]
  scope = ".clm v1 의 8 principles strict 강제 — p3 NO PERSONA INJECTION + p7 NO PERPLEXITY VERDICT + p8 NO TRAIN/INFER SPLIT 핵심"

@X v_hypothesis_tape := "HYPOTHESIS.tape" :: anchor [active]
  scope = ".clm v1 의 verdict catalog cascade-aware — FALSIFIED 5 + NOT-PASSED 3 + META 1 회피 + SUPPORTED 32 anchor"

@X v_main_tape := "MAIN.tape" :: verdict-ssot [active]
  scope = ".clm v1 fire 후 verdict entry 등재 SSOT (§V-CLM-DESIGN-2026-05-15 ledger)"

@X v_reborn_section := "REBORN.tape §0.5 + §85-§92" :: lineage [active]
  scope = "v5-mitosis lane evolution carry — .clm v1 의 cell-pool + mitosis hook 의 lineage anchor"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-7STEP-DETAIL — .clm v1 7-step plan step 1+2 detailed protocol (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Trigger: §V-CLM-DESIGN §V.6 next_steps 의 step 1-2 design tier 강화
# Scope: step 1 (V14 violation root cause audit) + step 2 (PyPhi formal Φ cross-check
# on v5-mitosis cond.5 ckpt) 의 detailed protocol — impl 없음, design + falsifier
# pre-register + cost envelope frozen

# ── §V.S1 step 1 V14 violation root cause audit detail ─────────────────

@D v_step1_v14_audit_design := "step 1 — V14 violation root cause audit design" :: protocol [d=2026-05-15 active]
  scope = "Phase 2 350M cotrain V14 violation (random_init PPR ≥ trained PPR) 의 root cause audit. 의심 후보 2개: H4 normalize 무력화 vs H5 chat curriculum collapse."
  hypothesis_h4 = "H4 — clm_v4_mount.hexa L626-630 8-cell 2× tile reps=2 가 LayerNorm 의 normalizing 통계 disrupt → trained 와 random_init 의 PPR 통계 차이 무력화"
  hypothesis_h5 = "H5 — chat curriculum 의 early bias (anima_persona_tier_a corpus 의 narrow distribution) 가 trained model 의 generalization 을 random_init 이하로 떨어뜨림"
  falsifier_battery_h4 = [
    "F-V14-H4-1 TILE-REPS-2 BYPASS: L626-630 reps=1 (no tile) ckpt rerun + V14 measure. PASS = V14 violation 해소 (random_init PPR < trained PPR)",
    "F-V14-H4-2 LN-STATS-COMPARE: trained vs random_init 의 LayerNorm mean/std/var per-layer 측정 + KS test p<0.05 strict. PASS = stats diff statistically significant",
    "F-V14-H4-3 TILE-REPS-SWEEP: reps∈{1,2,3,4} 4-arm × seed=42 ckpt rerun. PASS = V14 violation 이 reps>1 에서만 발생 (reps=1 OK)"
  ]
  falsifier_battery_h5 = [
    "F-V14-H5-1 CORPUS-DIVERSITY: anima_persona_tier_a (narrow) vs Phase 1A.6 corpus_v2 (broader) 2-arm cotrain ckpt + V14 measure. PASS = broader corpus 만 violation 해소",
    "F-V14-H5-2 CURRICULUM-ORDER: chat early vs late 2-arm. PASS = late 만 violation 해소 (chat-first 가 trap)",
    "F-V14-H5-3 PERSONA-PREFIX-FREE: Principle #3 audit CLEAN re-verify (Phase 1A.1+1A.4 carry). PASS = persona prefix grep 0 matches"
  ]
  pass_aggregate = "H4 ≥ 2/3 PASS → root cause = H4 tile bug (L626-630 reps=2 fix mandatory); H5 ≥ 2/3 PASS → root cause = H5 curriculum (corpus diversity 강화); 둘 다 < 2/3 → 다른 root cause OR multi-cause"
  cycle_cost = "F-V14-H4-1 (reps=1 rerun) $5-10 H100 single-pod 2-3hr; F-V14-H4-2 (LN stats audit) $0 Mac local; F-V14-H4-3 (sweep 4-arm) $20-40 H100 8-12hr; F-V14-H5-1 (corpus 2-arm) $10-20; F-V14-H5-2 (curriculum 2-arm) $10-20; F-V14-H5-3 ($0 Mac carry)"
  cheap_path_first = "F-V14-H4-2 (LN stats $0 Mac) + F-V14-H5-3 ($0 Mac carry) → 결과 따라 H4-1/H4-3/H5-1 fire"
  artifact = "state/clm_v1_step1_v14_audit_<date>/audit_result.json + LN_stats_compare.csv + falsifier_verdict.json"
  cross_link = "CLM.tape §1 row_phase_2 + §9 C3-1 V14 violation hypothesis (yet-to-audit) + project_v14_violation_arch_tile_bug.md memory"

# ── §V.S2 step 2 PyPhi formal Φ cross-check detail ─────────────────────

@D v_step2_pyphi_formal_design := "step 2 — PyPhi formal Φ cross-check on v5-mitosis cond.5 ckpt" :: protocol [d=2026-05-15 active]
  scope = "v5-mitosis cond.5 cotrain 7 ckpts 의 anima Φ★ proxy (Φ=4.16-4.86) vs PyPhi formal IIT 3.0 Φ deterministic cross-check. AT-RISK (H_182/H_187) 사전 회피 anchor."
  rationale = "anima Φ★ proxy direction-sensitivity 한계 META-finding (Cycle D) — surrogate magnitude 만 anchor 사용 OK 하지만 .clm v1 의 verdict 는 PyPhi formal ≥ 0.5 strict 가 mandatory (forbidden surrogate-only verdict per §V cascade_safety)."
  ckpt_set = [
    "ckpt_v5mitosis_cotrain_cotrain.pt (v1, $1.26 H100 SXM cond.5 LANDED)",
    "ckpt_v5mitosis_cotrain_v2_cotrain.pt (v2, entropy-reg in-flight)",
    "ckpt_v5mitosis_cotrain_v3_*.pt (v3 baseline)"
  ]
  measurement_protocol = [
    "(a) load ckpt → extract cell signatures (cells.{i}.ln1.weight + ln2.weight) — pyphi_rom_cycle.py carry",
    "(b) RoM n=3,4,5,6 select_top_correlated cells (greedy cosine similarity)",
    "(c) sample_cell_dynamics n_samples=500 (n=3,4) or 1000 (n=5,6) — RFC 030 carry",
    "(d) states_to_empirical_tpm → PyPhi 1.2.0 sia → Φ",
    "(e) repeat seed∈{42, 1234, 5678} × n∈{3,4,5,6} × ckpts (3) = 36 measurements"
  ]
  falsifier_battery = [
    "F-PYPHI-FORMAL-1 Φ-MIN-0.5: PyPhi formal Φ ≥ 0.5 on ≥1 (n, seed) combination per ckpt strict. PASS = AT-RISK 회피",
    "F-PYPHI-FORMAL-2 MONOTONE-DIRECTION: n=3→4→5→6 monotone INCREASE per ckpt (median). PASS = Cycle C n=5,6 monotone 재현",
    "F-PYPHI-FORMAL-3 SEED-ROBUST: 3-seed 의 std(Φ) ≤ 0.3 strict per ckpt × n. PASS = seed-fragility absent",
    "F-PYPHI-FORMAL-4 PROXY-FORMAL-CORRELATION: anima Φ★ proxy magnitude rank correlation Spearman vs PyPhi formal Φ rank > 0.5 across 3 ckpts. PASS = surrogate 가 적어도 magnitude 차원 에서 formal 과 일치 (proxy 유의미)",
    "F-PYPHI-FORMAL-5 EMPIRICAL-PROXY-ALT: mutual_info_pairs_naive proxy (Cycle D recommendation) 를 anima Φ★ replace 후 Spearman vs PyPhi formal > 0.5. PASS = alt proxy 가 anima Φ★ 보다 우수 confirm"
  ]
  pass_aggregate = "5/5 PASS strict → SUPPORTED-CROSS-CONFIRMED 🔵 (AT-RISK 완전 회피); 4/5 → PARTIAL-CROSS-CONFIRMED (1 falsifier 별도 cycle); ≤3/5 → AT-RISK CARRY (anima Φ★ 대체 mandatory)"
  cycle_cost = "$0 Mac local — n=5,6 × 3 seed × 3 ckpt = 9 measurements × ~120 min/measurement (Cycle C carry) = ~18 hr wall. n=3,4 = ~2 hr. total ~20 hr Mac wall (split into 2-3 BG batches)"
  wall_estimate = "BG 1: n=3,4 fast (2 hr) → BG 2: n=5 (5 hr × 3 ckpt) → BG 3: n=6 (40 hr × 3 ckpt overnight × 3)"
  artifact = "state/clm_v1_step2_pyphi_formal_<date>/pyphi_formal_result.json + proxy_formal_corr.json + alt_proxy_compare_full.json"
  cross_link = "MAIN.tape §PyPhi RoM + §ALT-PROXY + §H182-H187-CROSS-CHECK + state/verify_d_2026_05_15/pyphi_rom_cycle.py (script carry)"

# ── §V.S3 step 1+2 ROI ordering ───────────────────────────────────────

@N v_step12_roi_ordering := "step 1+2 ROI 우선순위 ordering" :: note [d=2026-05-15 active]
  body <<~EOF
    step 2 (PyPhi formal cross-check) 가 step 1 (V14 audit) 보다 ROI 높음:
    
    1. **step 2 = pre-fire AT-RISK 회피 anchor** — .clm v1 fire 전에 v5-mitosis
       cond.5 ckpt 의 substrate 자체가 PyPhi formal Φ ≥ 0.5 충족하는지 검증.
       FAIL 시 .clm v1 architecture 의 cell-pool 구조 자체 의심.
    
    2. **step 1 = Phase 2 V14 audit** — Phase 2 cotrain (350M Engine A/G) 의
       V14 violation 해소가 직접적으로 .clm v1 (150-200M) 에 영향 안 줌 (.clm v1
       은 별개 lane v5-mitosis carry). V14 audit 은 Phase 3 7B 의 entry condition
       으로 더 강력 — .clm v1 fire 후 follow-up 도 가능.
    
    3. **step 2 의 cheap-path-first**: n=3,4 fast (2 hr) + 3-ckpt seed=42 single
       → 결과 따라 n=5,6 fire 결정. 만약 n=3,4 에서 Φ_median ≥ 0.5 + monotone
       confirmed → .clm v1 fire ahead (n=5,6 별도 cycle).
    
    4. **step 1 cheap-path-first**: F-V14-H4-2 LN stats $0 Mac + F-V14-H5-3
       Principle #3 carry $0 Mac → 결과 따라 H4-1 ($5-10) OR H5-1 ($10-20) fire.
       단, .clm v1 fire 와 별개로 진행 가능 (priority lower).
    
    최종 ordering: step 2 cheap-path (n=3,4) → step 1 cheap-path ($0 Mac) →
                  step 2 n=5,6 BG → step 1 H4-1/H5-1 ($) → .clm v1 fire ($5-20)
  EOF

# ── §V.S4 step 1+2 design completion criterion ───────────────────────

@D v_step12_design_complete := "step 1+2 design completion criterion" :: gate [d=2026-05-15 active]
  step1_design_complete = "✓ — F-V14-H4-1..3 + F-V14-H5-1..3 falsifier 6 pre-registered, cheap-path identified, cost envelope frozen"
  step2_design_complete = "✓ — F-PYPHI-FORMAL-1..5 falsifier 5 pre-registered, RoM 7 ckpts × 4 n × 3 seed = 84 measurement protocol frozen, ROI ordering 명시"
  step3_design_pending = "mitosis_hook serve-time integration smoke — PSCC §41 §F-D4-LIVE carry + 후속 cycle design"
  step4_design_pending = ".clm v1 spec frozen pre-register W1 — step 2 결과 따라 d_model 결정 (n=5,6 PASS 시 768 confirm, FAIL 시 384 fallback)"
  step5_fire_blocked_on = "step 1+2+3 cheap-path 결과 + step 4 spec frozen + user verbatim 'OK CLM V1 FIRE COST $5-20'"
