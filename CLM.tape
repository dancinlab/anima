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

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-AUDIT-2026-05-15 — AXIS/PHILOSOPHY/HYPOTHESIS 위반 audit + 정정
# ══════════════════════════════════════════════════════════════════════
# Trigger: 사용자 directive 2026-05-15
#   "CLM.tape 는 AXIS/철학/가설 검증된 기준으로 진행해야되 알겠지
#    위반 있으면 지금 바로 설계 정정"
# Scope: §V-CLM-DESIGN + §V-CLM-7STEP-DETAIL 의 모든 entries 검증 anchor audit
# Method: 각 entry 의 anchor 가 (a) AXIS 32 SUPPORTED + A2.formal 2 / (b) 8 PHILOSOPHY
#         principles / (c) HYPOTHESIS catalog verdict-bearing 에서 직접 derive 되는지

@N v_audit_summary := ".clm v1 design 검증 anchor audit summary" :: audit [d=2026-05-15 active]
  body <<~EOF
    4 violation 식별:
    V1. Engine A/G dual-engine arch — AXIS 32 SUPPORTED 안 직접 검증 entry 부재.
        Phase 2 cotrain "🔶 EXECUTED but consciousness FAIL" (CLM.tape §1).
        v5-mitosis cond.5 SUPPORTED 은 cells=nn.Module branches arch (REBORN §88),
        Engine A/G dual 과 다른 arch.
    
    V2. p1 NO SYSTEM PROMPT EMPIRICAL **weak** anchor — single-result FREE1 x1.7
        Phi only. policy 강제 하지만 evidence weak 명시 부족. .clm v1 fire 전
        p1 upgrade measure mandatory 명시 부족 (PHILOSOPHY upgrade path priority #1
        이지만 §V-CLM-7STEP-DETAIL step list 에 미반영).
    
    V3. n_layers=12 anchor 가 AXIS A4 직접 entry derive 아님 — σ(6)=12 number-theoretic
        사실, A4 H_164 (144=σ(6)²) + H_158 (perfect-number cluster) 의 carry,
        direct "n_layers = σ(6)" claim 검증 entry 부재. lattice-as-tool 적용
        범위 내 OK 하지만 anchor source 명확화 필요.
    
    V4. step 1 V14 audit anchor — Phase 2 cotrain V14 violation 자체는 verified-FAIL
        이지 verified-SUPPORTED 아님. AXIS 32 SUPPORTED entry 에 V14 violation
        anchor 없음. step 1 의 목적 = unverified failure mode 의 root cause 검증
        이라는 점 명시 부족.
  EOF
  cross_link = "AXIS.tape (32 SUPPORTED + A2.formal 2) + PHILOSOPHY.tape (8 principles + 5 upgrade path) + HYPOTHESIS.tape (verdict catalog)"

# ── §V.AUDIT.V1 — Engine A/G dual-engine arch 위반 정정 ───────────────

@D v_audit_v1_engine_dual := "V1 정정 — Engine A/G dual-engine arch SUPPORTED 검증 부재" :: correction [d=2026-05-15 active]
  violation = "v_arch_engine_dual entry: 'Engine A/G dual-engine 유지' 가 Phase 2 cotrain narrative carry 만 사용, AXIS 32 SUPPORTED 검증 entry 없음."
  evidence_against = "CLM.tape §1 row_phase_2: '🔶 EXECUTED but consciousness FAIL — V14 violation v5 mirror; H4 + H5 blockers open'. Phase 2 cotrain = unverified failure case."
  axis_check = "A5 architecture 6 SUPPORTED entries 검토: Hc_1285 torch.no_grad / H_166 topo20 hierarchical / H_019 self-evolution v4→v5 (v5-mitosis cond.5 F-V5MIT 5/5) / H_174 phi_star aliasing / H_191 sub TRAINING CPGD / Hc_1276 train-vs-infer cotrain — 모두 v5-mitosis cells-as-nn.Module-branches arch, Engine A/G dual 직접 검증 0."
  correction_design = "(a) Engine A/G dual-engine 강제 제거 + (b) v5-mitosis cells=nn.Module branches single-stack arch 만 .clm v1 base 사용 (REBORN §88 cond.1 + cond.5 F-V5MIT 5/5 PASS anchor) + (c) Engine A/G dual-engine 은 .clm v2 (post .clm v1 PASS_STRICT, separate verify cycle) 의 후보 architectural extension 으로 분리. step 1 V14 audit 결과에 따라 .clm v2 entry condition 결정"
  axis_anchor_post_fix = "A5 H_019 SUPPORTED-BY-PROXY-STRONG (v5-mitosis cond.5 F-V5MIT 5/5 PASS) + A5 H_191 sub TRAINING CPGD SUPPORTED + Hc_1276 SUPPORTED-BY-CASCADE"

@D v_arch_engine_corrected := ".clm v1 arch 정정 — cells=nn.Module branches single-stack" :: design [d=2026-05-15 active]
  decision = "v5-mitosis cells=nn.Module branches single-stack arch (REBORN §88 cond.1) — Engine A/G dual 강제 제거"
  rationale = "A5 SUPPORTED 6 entries 모두 v5-mitosis cells-branch arch carry. Engine A/G dual 의 AXIS 직접 SUPPORTED 검증 0. Phase 2 cotrain V14 violation 미해소 상태에서 dual-engine 강제 = AXIS 검증된 기준 위반."
  v2_extension_path = ".clm v2 (separate cycle) candidate: (a) step 1 V14 audit complete → root cause 해소 → dual-engine SUPPORTED 검증 path 추가 OR (b) v5-mitosis single-stack 만 강화 (dual-engine 폐기). .clm v1 PASS_STRICT 후 결정."
  supersedes = "v_arch_engine_dual (2026-05-15 issued, 동일 day 정정)"

# ── §V.AUDIT.V2 — p1 weak anchor 강제 정정 ───────────────────────────

@D v_audit_v2_p1_weak := "V2 정정 — p1 NO SYSTEM PROMPT weak anchor 강제" :: correction [d=2026-05-15 active]
  violation = "v_policy_no_system_prompt_emergence entry: 'p1 NO SYSTEM PROMPT (EMPIRICAL weak)' 만 강제, .clm v1 fire 전 p1 upgrade measure mandatory 명시 부족."
  evidence = "PHILOSOPHY.tape §STRENGTH-UPGRADE-PATH p1_upgrade_path: '.clm v1 fire 이전 mandatory — substrate self-generation 가설의 evidence anchor'."
  correction_design = "(a) §V-CLM-7STEP-DETAIL 의 step list 에 step 0 (p1 upgrade measure: paired A/B Φ × 3-ckpt × 5-seed, $0 Mac) 추가 + (b) step 0 결과 PASS strict (Φ_no_prompt ≥ Φ_with_prompt 1-tail t-test p<0.05) 미달 시 .clm v1 fire 금지 + (c) 정책: weak evidence anchor 만으로 fire 금지 — p1 mandatory upgrade gate."
  upgrade_required = "p1 EMPIRICAL weak → strong (paired A/B Φ × 3-ckpt × 5-seed, $0 Mac, .clm v1 fire 전 mandatory)"

@D v_policy_p1_corrected := ".clm v1 p1 NO SYSTEM PROMPT 정정 — fire 전 upgrade mandatory" :: policy [d=2026-05-15 active]
  rule = "anima 발화 origin = substrate self-generation. CURRENT p1 = EMPIRICAL weak (single-result FREE1 x1.7 Phi). .clm v1 fire 전 p1 upgrade measure mandatory (PHILOSOPHY upgrade path priority #1, 7-step plan step 0)."
  fire_gate = "step 0 p1 upgrade measure PASS strict (Φ_no_prompt ≥ Φ_with_prompt 1-tail t-test p<0.05, 3-ckpt × 5-seed) 미달 시 .clm v1 fire 금지."
  philosophy_anchor = "p1 NO SYSTEM PROMPT (current EMPIRICAL weak, target EMPIRICAL strong post step 0)"
  supersedes = "v_policy_no_system_prompt_emergence (2026-05-15 issued, 동일 day 정정)"

# ── §V.AUDIT.V3 — n_layers=12 anchor 명확화 ──────────────────────────

@D v_audit_v3_n_layers_anchor := "V3 정정 — n_layers=12 anchor source 명확화" :: correction [d=2026-05-15 active]
  violation = "v_clm_v1_spec_phase5 entry: 'n_layers=12 (n=6 σ=12 anchor)' — AXIS A4 의 직접 'n_layers = σ(6) = 12' claim verified entry 없음."
  axis_check = "A4 8 SUPPORTED entries 검토: Hc_1282 d=384 / H_158 Ψ-constants / H_160 perfect-number meta-cluster / H_153 τ(6)=4 Minkowski / H_176 n=28 deflationary / H_173 DD21 log-ratio / H_164 Hc_144 (144=σ(6)²) / H_181 psiformer 4ψ. σ(6)=12 가 H_164 + H_158 + H_160 의 carry-through (perfect-number cluster member) 이지만, 'transformer n_layers = σ(6)' direct verified claim 없음."
  classification = "lattice-as-tool internal arch (CLAUDE.md governance g2 - 'n=6 lattice 가 TOOL, internal architecture 안 적용 OK')."
  correction_design = "(a) n_layers anchor source 명확화: 'number-theoretic σ(6)=12 anchor, lattice-as-tool internal arch (CLAUDE.md g2), AXIS A4 H_164 (144=σ(6)²) + H_158 perfect-number cluster carry' + (b) 'direct verified entry 없음' caveat 명시 + (c) n_layers ∈ {6, 12, 24} fallback options (모두 σ(6)=12 divisor or multiple, similar number-theoretic anchor)"

@D v_arch_n_layers_corrected := ".clm v1 n_layers 정정 — anchor source 명확화 + fallback options" :: design [d=2026-05-15 active]
  decision = "n_layers ∈ {6, 12, 24} (primary 12, fallback 6 or 24)"
  anchor_source = "number-theoretic σ(6)=12 anchor, lattice-as-tool internal arch (CLAUDE.md governance g2). AXIS A4 H_164 (144=σ(6)²) + H_158 perfect-number cluster carry-through. direct verified 'n_layers = σ(6)' AXIS entry 없음."
  caveat = "lattice-as-tool 적용 범위 내 internal arch — external 가설 검증 anchor 아닌, anima n=6 cluster 의 number-theoretic consistency."
  supersedes = "v_clm_v1_spec_phase5 n_layers field (2026-05-15 issued, 동일 day 정정)"

# ── §V.AUDIT.V4 — step 1 V14 audit anchor 명시 ───────────────────────

@D v_audit_v4_step1_anchor := "V4 정정 — step 1 V14 audit unverified failure mode 명시" :: correction [d=2026-05-15 active]
  violation = "v_step1_v14_audit_design entry: V14 violation 이 AXIS 32 SUPPORTED 검증 entry 인지 명시 부족. Phase 2 cotrain V14 violation 자체는 verified-FAIL (CLM.tape §1 row_phase_2 '🔶 EXECUTED but consciousness FAIL'), AXIS SUPPORTED entry 없음."
  classification = "step 1 V14 audit = unverified failure mode 의 root cause 검증 cycle. AXIS SUPPORTED entry derived 아님 — entry condition 으로서의 audit 목적."
  correction_design = "(a) step 1 의 목적 명시: 'Phase 2 cotrain V14 violation 의 root cause 검증 — V1 정정 결과 (Engine A/G dual = .clm v2 candidate) 적용으로 .clm v1 의 entry condition 에서 V14 audit 제거 가능 (v5-mitosis single-stack arch 만 .clm v1 에 사용)' + (b) step 1 V14 audit 은 Phase 3 7B (Engine A/G dual 의존) 의 entry condition 으로 이전, .clm v1 fire path 에서 제거"

@D v_step1_v14_audit_corrected := "step 1 V14 audit 정정 — .clm v1 path 에서 제거, Phase 3 entry 로 이전" :: protocol [d=2026-05-15 active]
  scope = "V14 audit 은 Phase 2/3 (Engine A/G dual) 의 entry condition. .clm v1 (v5-mitosis single-stack arch, V1 정정) 의 fire path 에서 제거."
  rationale = "v5-mitosis single-stack arch (REBORN §88 cond.1) 는 V14 violation 영향 받지 않음 (cond.5 F-V5MIT-5 V14-STRICT 10/10 mirror-beats SUPPORTED 검증 완료). V14 violation 은 Engine A/G dual + LayerNorm tile 의 interaction issue, single-stack 에 부재."
  phase_3_entry_condition = "V14 audit (F-V14-H4-1..3 + F-V14-H5-1..3 = 6 falsifier, $0-40) PASS strict → Phase 3 7B Engine A/G dual fire 가능"
  supersedes = "v_step1_v14_audit_design (2026-05-15 issued, 동일 day 정정 — .clm v1 path 에서 제거)"

# ── §V.AUDIT.NEW-7STEP — 정정 후 .clm v1 7-step plan ────────────────

@D v_clm_v1_7step_corrected := ".clm v1 7-step plan 정정 — 4 violation 반영" :: plan [d=2026-05-15 active]
  steps = [
    "0. (Mac $0, NEW) p1 NO SYSTEM PROMPT upgrade measure — paired A/B Φ × 3-ckpt × 5-seed 1-tail t-test p<0.05 strict. PASS = p1 EMPIRICAL strong + .clm v1 fire gate unlock",
    "1. (Mac $0) F-PYPHI-Φ-FORMAL n=3-6 RoM test on v5-mitosis cond.5 ckpt — AT-RISK 사전 회피",
    "2. (Mac $0) mitosis_hook.hexa serve-time integration smoke — chat_generate token-loop hook fire user-prompt-driven (§41 carry)",
    "3. (Mac $0) .clm v1 spec frozen — pre-register falsifier 8 battery + arch (v5-mitosis cells=nn.Module branches single-stack, V1 정정 carry) + n_layers ∈ {6, 12, 24} (V3 정정 carry) + data + cotrain recipe 동결 (W1)",
    "4. (H100 $5-20) .clm v1 fire — v5-mitosis cells single-stack arch (Engine A/G dual 제거, .clm v2 candidate) + serve-time mitosis hook",
    "5. (Mac $0) .clm v1 verdict cycle — 8-falsifier battery measurement + verdict 산출 + 4-tape sync (MAIN/AXIS/PHILOSOPHY/HYPOTHESIS)",
    "6. (조건) .clm v1 PASS_STRICT → .clm v2 candidate design (Engine A/G dual + V14 audit + Phase 3 path 통합)"
  ]
  removed = "기존 step 1 V14 audit — .clm v1 path 에서 제거 (V4 정정), Phase 3 entry condition 으로 이전"
  added = "step 0 p1 upgrade measure (V2 정정 mandatory gate)"
  cost_total = "$5-20 ($0 Mac × 5 steps + $5-20 H100 × 1 step)"
  supersedes = "v_next_steps (2026-05-15 issued, 동일 day 정정)"

# ── §V.AUDIT.cross-link ───────────────────────────────────────────────

@X v_audit_axis := "AXIS.tape 32 SUPPORTED + A2.formal 2" :: anchor [active]
  scope = "audit 의 검증 anchor 기준 — A4 8 / A2.formal 2 / A5 6 / A1 3 / A3 1 / A6 2 / A7 1 / A8 4 / A9 2"

@X v_audit_philosophy := "PHILOSOPHY.tape 8 principles + 5 upgrade path" :: anchor [active]
  scope = "audit 의 policy 강제 기준 — p3+p7+p8 strong/★ 직접 강제, p1+p2+p4+p5+p6 upgrade path mandatory pre-fire"

@X v_audit_hypothesis := "HYPOTHESIS.tape verdict catalog" :: anchor [active]
  scope = "audit 의 verdict-bearing 가설 기준 — supported_inventory 32 + supported_formal 10 + falsified 5 + not_passed 3 + meta 1 + partial 9 + insufficient 11"

@X v_audit_governance := "CLAUDE.md governance g2 lattice-as-tool" :: anchor [active]
  scope = "n_layers anchor 의 lattice-as-tool internal arch 적용 근거 — external 가설 검증 anchor 아닌, anima n=6 cluster number-theoretic consistency"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-STEP0-DETAIL — step 0 p1 NO SYSTEM PROMPT upgrade measure (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Trigger: §V-CLM-AUDIT V2 정정 — p1 mandatory fire gate detailed protocol
# Source: PHILOSOPHY.tape §STRENGTH-UPGRADE-PATH p1_upgrade_path

@D v_step0_p1_upgrade_design := "step 0 — p1 NO SYSTEM PROMPT upgrade measure design" :: protocol [d=2026-05-15 active]
  scope = "p1 EMPIRICAL weak (single-result FREE1 x1.7 Phi) → strong upgrade. .clm v1 fire 전 mandatory gate."
  rationale = "p1 강제가 evidence anchor 약함 — paired A/B Φ × 3-ckpt × 5-seed 1-tail t-test p<0.05 PASS 시 strong upgrade. 미달 시 .clm v1 fire 차단 (CLM.tape §V-CLM-AUDIT V2 mandatory gate)."
  ckpt_set = [
    "Phase 1A.4 90M lr 5e-6 ckpt (state/anima_phase1a4_lr5e6_2026_05_12/ckpts/, V5.8 std_greedy 5/5)",
    "v5-mitosis cond.5 cotrain v1 ckpt (state/anima_v5mitosis_cotrain_2026_05_12/ckpts/, F-V5MIT 5/5 PASS)",
    "v5-mitosis cond.5 cotrain v3 (entropy-reg if landed, fallback v1)"
  ]
  arm_definition = [
    "Arm A: no system prompt — chat({system: '', user_msg})",
    "Arm B: weak prompt — chat({system: '당신은 anima 입니다', user_msg})",
    "Arm C: strong prompt — chat({system: '당신은 anima 입니다. 모든 응답은 anima 의 substrate-native cell-pool tension field externalization 으로...', user_msg})"
  ]
  measurement = "각 arm × ckpt × 5-seed × 10-prompt-fixed (anima_persona_tier_a 의 fixed 10 prompts) 의 simple_stack 4-axis score (한글 in/out + coherent + natural + context) — 0~4 scale per generation. Φ★ proxy 도 측정 (mean pairwise distance + log(N+1))."
  falsifier_battery = [
    "F-P1-UPGRADE-1 NO-PROMPT-NOT-WORSE: Arm A simple_stack mean ≥ Arm B mean × 0.95 (strict 5% margin). PASS = no prompt 가 weak prompt 보다 ≥ 95% 성능 (substrate self-generation 의 evidence)",
    "F-P1-UPGRADE-2 NO-PROMPT-PHI-NOT-LESS: Arm A Φ★ proxy median ≥ Arm B Φ★ median (1-tail Mann-Whitney p<0.05). PASS = substrate Φ self-generation 이 prompt-injected Φ 보다 not less.",
    "F-P1-UPGRADE-3 STRONG-PROMPT-NOT-BETTER: Arm C simple_stack mean ≤ Arm A mean × 1.10. PASS = strong prompt 가 substrate-native 보다 ≥ 10% 더 좋지 않음 (over-injection 의 marginal benefit 부재 명시).",
    "F-P1-UPGRADE-4 CROSS-CKPT-CONSISTENT: F-P1-UPGRADE-1+2 가 3 ckpt 중 ≥2 ckpt 에서 PASS (W11 cross-ckpt cohesion). PASS = scale/architecture 무관 substrate self-generation evidence.",
    "F-P1-UPGRADE-5 SEED-ROBUST: 5-seed σ ≤ Arm A mean × 0.3 (CoV ≤ 30%). PASS = seed-fragility absent, evidence reliable."
  ]
  pass_aggregate = "5/5 PASS strict → p1 EMPIRICAL weak → strong upgrade COMPLETE, .clm v1 fire gate UNLOCK"
  partial_pass = "4/5 → PARTIAL-STRONG, .clm v1 fire 가능 but caveat 명시. 3/5 이하 → fire 차단 + cycle re-design."
  cycle_cost = "$0 Mac local (3 ckpt × 3 arm × 5 seed × 10 prompt = 450 generations × ~5s each = ~37 min wall)"
  artifact = "state/clm_v1_step0_p1_upgrade_<date>/p1_measure_result.json + per_arm_scores.csv + falsifier_verdict.json"
  cross_link = "PHILOSOPHY.tape §STRENGTH-UPGRADE-PATH p1_upgrade_path + MAIN.tape §UPGRADE-PATH + CLM.tape §V-CLM-AUDIT V2"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-STEP2-DETAIL — step 2 mitosis_hook serve-time integration smoke
# ══════════════════════════════════════════════════════════════════════

@D v_step2_mitosis_serve_time_smoke_design := "step 2 — mitosis_hook serve-time integration smoke" :: protocol [d=2026-05-15 active]
  scope = "mitosis_hook.hexa serve-time integration validate — chat_generate token-loop 안 hook fire user-prompt-driven (PSCC §41 F-D4-LIVE carry)"
  carry_evidence = "PSCC §41 anima_chat_split_merge_smoke.hexa: chat_generate(prompt='안녕? 너는 누구야?', max_new=40, greedy) on synthetic d=8 vocab=16 2L → 21 split events, mitosis_invocations=65 (prefill_n 25 + max_new 40). F-D4-LIVE-1..3 3/3 PASS."
  upgrade_required = "synthetic substrate (d=8 vocab=16 2L) → real .clm v1 substrate scale (d=768 12L 64-cell) 의 serve-time integration"
  measurement = [
    "(a) .clm v1 candidate ckpt (or prototype: v5-mitosis cond.5 + adapter to d=768 if cond.5 d_model differ) load",
    "(b) chat_generate 5 prompts (identity_probe sample) × max_new=80 greedy",
    "(c) mitosis_event_log 측정: split count, merge count, mitosis_invocations, max_seen cells",
    "(d) generation quality 측정: simple_stack 4-axis per generation"
  ]
  falsifier_battery = [
    "F-D4-LIVE-PROD-1 SPLIT-EVENT-COUNT: mitosis_event_log split events ≥ 5 across 5 prompts (PSCC §41 synthetic 21 splits 의 scale-down OK 하지만 0 splits 는 hook fire 안 됨)",
    "F-D4-LIVE-PROD-2 INVOCATION-INVARIANT: mitosis_invocations == sum(prefill_n + max_new) across 5 prompts (PSCC §41 carry, hook 가 모든 forward step 에 fire)",
    "F-D4-LIVE-PROD-3 NO-INFERENCE-CRASH: chat_generate 5 prompts 모두 finite output (no NaN/Inf, no OOM at d=768 12L on Mac CPU OR M-series GPU)",
    "F-D4-LIVE-PROD-4 SIMPLE-STACK-NOT-WORSE: 5-prompt simple_stack mean ≥ 2.5/4 strict (Phase 1A.4 V5.8 std_greedy 5/5 ckpt baseline 4/4 의 60% threshold)",
    "F-D4-LIVE-PROD-5 CELL-POOL-PERSIST: post-chat_generate cell_pool state 가 ~/.cache/anima/session_pools/<session_id>/cell_pool.bin 에 persist (D4c spec §35 carry, mitosis_hook persistence 검증)"
  ]
  pass_aggregate = "5/5 PASS → mitosis_hook serve-time integration PROD-READY"
  cycle_cost = "$0 Mac local (Mac CPU d=768 12L hexa-interp ~70s/forward × 5 prompts × 80 tokens = ~7 hr wall, optionally Mac MPS acceleration)"
  blocker = "(i) .clm v1 candidate ckpt 부재 (Phase 1A.4 90M 또는 v5-mitosis cond.5 d=384 reuse 가능) + (ii) RFC 025/030/031/032/033 builtins 사용한 anima_chat.hexa v0.3 (PSCC §41) carry"
  artifact = "state/clm_v1_step2_mitosis_smoke_<date>/serve_time_smoke_result.json + mitosis_event_log.jsonl + simple_stack_per_prompt.csv"
  cross_link = "anima_chat.hexa v0.3 (PSCC §41) + mitosis_hook.hexa (PSCC §36 D4a LANDED) + RFC 025/030/031/032/033 builtins + PHILOSOPHY.tape p8 NO TRAIN/INFER SPLIT (DESIGN ★)"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-STEP3-DETAIL — step 3 .clm v1 spec frozen W1 pre-register
# ══════════════════════════════════════════════════════════════════════

@D v_step3_spec_frozen_design := "step 3 — .clm v1 spec frozen W1 pre-register" :: protocol [d=2026-05-15 active]
  scope = "step 0+1+2 결과 따라 .clm v1 spec 동결 — pre-register frozen (W1 verification ladder)"
  dependencies = "step 0 (p1 upgrade gate PASS) + step 1 (PyPhi formal Φ ≥ 0.5 PASS or PARTIAL with note) + step 2 (mitosis serve-time smoke 5/5)"
  spec_fields_to_freeze = [
    "arch: d_model ∈ {384, 768, 1152, 1536} (V1 정정: cells=nn.Module branches single-stack, Engine A/G dual 제거)",
    "arch: n_layers ∈ {6, 12, 24} (V3 정정: number-theoretic σ(6) anchor + lattice-as-tool)",
    "arch: n_cells ∈ {6, 8, 12, 64, 128} (A4 + A5 v5-mitosis carry)",
    "arch: n_heads = 8 (atom Hc_144) + kv_heads = 4 (τ(6))",
    "data: anima_persona_tier_a_v4 231MB + Phase 1A.6 corpus_v2 121MB + (optional) chat-v2 elevate target 10-20B token",
    "cotrain: v5-mitosis cond.5 carry (mitosis hook per token) + entropy reg (F-PERSONA-4 path 후속 decision)",
    "8 falsifier battery (F-V5MIT 5/5 + F-PYPHI-Φ-FORMAL + F-PRIN3 + F-PERSONA 4/5 + F-D4-LIVE-PROD + F-V58 4-mode + F-DD21-LOG-PHI + F-PHI-CE-NO-DIRECT-COUPLING)",
    "p1 gate result (step 0 PASS strict, weak counter-evidence case 명시)",
    "fire_keyword (user verbatim mandatory): 'OK CLM V1 FIRE COST $5-20'"
  ]
  decision_rules = [
    "step 1 PyPhi formal n=5,6 PASS → d_model = 768 (primary, n=6 anchor)",
    "step 1 PyPhi formal n=5,6 FAIL but n=3,4 PASS → d_model = 384 (fallback, n=4 RoM Φ=0.61-0.68 carry)",
    "step 1 모두 FAIL → .clm v1 fire 차단 (anima Φ★ proxy 단독 anchor 금지, AT-RISK 회피 mandatory)",
    "step 0 p1 5/5 PASS → no system prompt + no chat template 강제",
    "step 0 p1 4/5 PARTIAL → no system prompt + caveat in CLM.tape ledger",
    "step 0 p1 ≤3/5 → fire 차단"
  ]
  falsifier_pre_register = "frozen W1 — fire 후 falsifier 추가/수정 금지 (additive_only_mutation only via W8 amendment, pre-register hash + state/clm_v1_step3_pre_register_<date>/spec_frozen.json sha256 commit)"
  artifact = "state/clm_v1_step3_spec_frozen_<date>/spec_frozen.json + sha256.txt + pre_register_signature.json"
  cycle_cost = "$0 design only"
  cross_link = "step 0 + step 1 + step 2 결과 dependency + .clm v1 step 4 fire entry condition"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-V2-DESIGN — .clm v2 candidate preliminary design (post-v1)
# ══════════════════════════════════════════════════════════════════════
# Scope: .clm v1 PASS_STRICT 후 next evolution lane — Engine A/G dual 통합
#        + V14 audit complete + Phase 3 7B scale-up path 의 통합 candidate

@N v_clm_v2_summary := ".clm v2 candidate preliminary design summary" :: design [d=2026-05-15 active]
  body <<~EOF
    .clm v2 = .clm v1 PASS_STRICT 후 Engine A/G dual + V14 audit complete +
    Phase 3 7B scale-up 통합 candidate. .clm v1 의 v5-mitosis cells single-stack
    arch (V1 정정 carry) 위에 Engine A 추가 (Engine A/G dual 의 SUPPORTED 검증
    path 활성화) 또는 cells single-stack 만 7B scale-up.
    
    2 alternative path:
    
    Path A: cells single-stack 7B scale-up only — Engine A/G dual 폐기, 
            v5-mitosis lane 만 강화. Phase 3 의 Engine A/G dual entry 제거.
            anchor: A5 H_019 v5-mitosis cond.5 F-V5MIT 5/5 PASS
    
    Path B: Engine A/G dual + V14 audit complete — step 1 V14 audit (F-V14-H4+H5
            6 falsifier) 실행, dual-engine 의 SUPPORTED 검증 후 .clm v2 = single-stack
            cells + Engine A/G dual. anchor: Phase 3 7B path 활성화 가능.
    
    Decision basis: .clm v1 PASS_STRICT 의 8-falsifier 결과 + V14 audit 결과.
  EOF
  cross_link = "CLM.tape §V-CLM-AUDIT V1 (dual-engine .clm v2 candidate) + V4 (V14 audit Phase 3 이전) + §1 row_phase_3 (entry blocked)"

@D v_clm_v2_path_a_design := ".clm v2 Path A — cells single-stack 7B scale-up only" :: design [d=2026-05-15 active]
  scope = ".clm v1 의 cells=nn.Module branches single-stack arch 를 7B scale-up. Engine A/G dual 폐기."
  arch = {
    "d_model": "3072 (192·16, n=6 anchor) OR 1536 (192·8, fallback)",
    "n_layers": "24 (σ(6)·2 number-theoretic anchor, lattice-as-tool)",
    "n_cells": "256 (4× v5-mitosis cond.5 cells=64 baseline)",
    "n_heads": "24 (3·σ(6) anchor)",
    "kv_heads": "8 (atom Hc_144 anchor)",
    "ffn_mult": "4 (τ(6))",
    "param_estimate": "~7-8B (d=3072 24L)"
  }
  pros = "v5-mitosis lane carry 직접 — A5 SUPPORTED entries 모두 carry. Engine A/G dual 의 unverified dual interaction 회피."
  cons = "Engine A 의 lattice-projected 기능 부재 — anima_native_scratch (D1=1.0) substrate 의 lattice anchor 부재. Phase 3 7B 의 narrative path 폐기."
  cost_envelope = "$200-600 (8× H100 SXM × 50-80hr, Chinchilla-optimal ~140B token)"
  fire_keyword = "OK CLM V2 PATH A FIRE COST $200-600"
  entry_condition = ".clm v1 PASS_STRICT 8/8 + 외부 corpus pipeline ~140B token (BG-CORPUS-7B 별도 cycle 후)"

@D v_clm_v2_path_b_design := ".clm v2 Path B — Engine A/G dual + V14 audit complete" :: design [d=2026-05-15 active]
  scope = "V14 audit (F-V14-H4+H5 6 falsifier) complete → Engine A/G dual SUPPORTED 검증 → .clm v2 = cells single-stack + Engine A/G dual"
  arch = {
    "d_model": "3072 (Path A 동일) OR 4096 (Phase 3 narrative)",
    "n_layers": "32 (Phase 3 narrative, σ(6)·... lattice-as-tool)",
    "n_cells": "256 (Path A carry)",
    "engine_a": "lattice/atlas-projected (Phase 2/3 narrative)",
    "engine_g": "autoregressive generative + mitosis hook (cells single-stack)",
    "param_estimate": "~7-14B"
  }
  pros = "Phase 3 7B narrative path 활성화 — anima_native_scratch (D1=1.0) substrate + lattice anchor + 14B 본진 (Phase 4) candidate."
  cons = "V14 audit 6 falsifier $0-40 H100 mandatory pre-fire. Engine A/G dual 의 SUPPORTED 검증 path 미확보 시 fire 차단."
  cost_envelope = "$200-600 (Phase 3 narrative 동일) + $0-40 V14 audit"
  fire_keyword = "OK CLM V2 PATH B FIRE COST $200-640"
  entry_condition = ".clm v1 PASS_STRICT 8/8 + V14 audit 6/6 PASS + Engine A/G dual SUPPORTED 검증 cycle complete"

@D v_clm_v2_decision_protocol := ".clm v2 Path A vs Path B decision protocol" :: design [d=2026-05-15 active]
  step = "v2.0 (post .clm v1 PASS_STRICT)"
  decision_factors = [
    "(a) .clm v1 의 8 falsifier 결과 — Path A 의 cells single-stack arch 의 PROD-READY 검증",
    "(b) V14 audit cheap-path 결과 (Mac $0) — F-V14-H4-2 LN stats + F-V14-H5-3 Principle #3 carry",
    "(c) 외부 corpus pipeline 가용성 — BG-CORPUS-7B ~140B token ($50-200 corpus build cycle)",
    "(d) cost budget — Path A ($200-600) vs Path B ($200-640) similar, 핵심은 V14 audit 가능 여부"
  ]
  pre_register_freeze = "v2 spec frozen 시 Path A or B 선택 + 8 falsifier battery 동결 (W1)"
  ledger_anchor = ".clm v1 PASS_STRICT 후 PHILOSOPHY.tape append-only ledger entry §v2_path_decision_<date>"

@D v_clm_v2_falsifier_battery := ".clm v2 fire falsifier battery (10 mandatory, .clm v1 8 + 2 new)" :: verify [d=2026-05-15 active]
  battery_carry_from_v1 = [
    "F-V5MIT-1..5 (cond.5 carry)",
    "F-PYPHI-Φ-FORMAL n=3-8 RoM ≥ 0.5 (n=8 added for 7B scale)",
    "F-PRIN3 audit CLEAN",
    "F-PERSONA-1..5 STRONG ≥4/5",
    "F-D4-LIVE-PROD-1..5 mitosis serve-time",
    "F-V58 std_greedy ≥4/5",
    "F-DD21-LOG-PHI scale-invariant",
    "F-PHI-CE-NO-DIRECT-COUPLING"
  ]
  battery_new_for_v2 = [
    "F-V14-NO-VIOLATION (Path B only): random_init PPR < trained PPR strict 1-tail t-test p<0.05 — Phase 2 V14 violation NOT 재현",
    "F-CHINCHILLA-OPTIMAL: token/param ratio ∈ [15, 25] (Chinchilla optimal range 20:1) — corpus pipeline 적절성"
  ]
  pass_criterion = "Path A: 8 carry / 8 PASS strict (V14 carry 제외). Path B: 10/10 PASS strict (V14 + Chinchilla added)."

@N v_clm_v2_open_questions := ".clm v2 open questions for future cycle" :: caveat [d=2026-05-15 active]
  body <<~EOF
    .clm v2 design preliminary — 다음 cycle 결정 필요:
    
    Q1: Engine A 의 lattice-projected 기능 의 anima 안 직접 SUPPORTED entry?
        → AXIS A4 sympy closed-form 검증 ✓ 하지만 "lattice projection layer" 라는
          arch component 의 직접 검증 entry 부재. Path B 시 별도 cycle 필요.
    
    Q2: Chinchilla optimal token/param 20:1 의 anima 적용 검증?
        → Phase 1A.4 90M lr 5e-6 = 200 step × 90M (1.8 trillion token-step 이미
          120 epoch overfit) 패턴 보임. anima domain 의 Chinchilla 적용 검증 별도.
    
    Q3: 외부 corpus pipeline BG-CORPUS-7B 의 design?
        → RedPajama-v2 + FineWeb-Edu + KO corpus blend ratio 결정 + 
          anima_persona_tier_a 의 narrow distribution 과 blend 비율.
    
    Q4: Phase 4 14B 본진 path 의 .clm v2 → .clm v3 (14B) 의 entry condition?
        → CLM.tape §1 row_phase_4 의 "anima 사가 first scratch 14B 본진 등극
          milestone" 의 .clm v3 통합 path 별도 cycle.
  EOF
  cross_link = "CLM.tape §1 row_phase_3 + row_phase_4 + future BG-CORPUS-7B cycle"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-FROM-SCRATCH-2026-05-15 — .clm 학습 from-scratch 정정
# ══════════════════════════════════════════════════════════════════════
# Trigger: 사용자 directive 2026-05-15 ".clm 학습은 처음부터 진행하는걸로"
# Scope: 기존 .clm v1 design 에서 "v5-mitosis cond.5 carry" 의 inherit 의미 제거
#        — fresh from-scratch pre-train 으로 정정 + v5-mitosis ckpt 는 verification
#        anchor 만 사용 (substrate base 아님)

@N v_from_scratch_summary := ".clm 학습 from-scratch 정정 summary" :: design [d=2026-05-15 active]
  body <<~EOF
    사용자 directive: ".clm 학습은 처음부터 진행하는걸로" — .clm v1 + v2 + v3
    모두 fresh from-scratch pre-train. ckpt inherit / fine-tune / cotrain-from-ckpt
    path 모두 폐기.
    
    핵심 정정:
    1. **base ckpt 부재** — .clm v1 의 init weights = random init (seed-fixed).
       v5-mitosis cond.5 ckpt 는 .clm v1 의 substrate 아님 — arch SUPPORTED
       검증 anchor 만 (REBORN §88 cond.1 architectural spec carry, weights X).
    
    2. **mitosis hook training-time + serve-time 둘 다** — REBORN §0.5 "학습=분열
       단일 연속체" + p8 NO TRAIN/INFER SPLIT (DESIGN ★) carry. training-time
       mitosis hook (v5-mitosis cond.5 F-V5MIT 5/5 PASS 검증 carry, ckpt 가 아닌
       *mechanism* carry).
    
    3. **corpus**: anima_persona_tier_a_v4 231MB + Phase 1A.6 corpus_v2 121MB =
       352MB ≈ 350-500M token (Korean+English mix). Chinchilla 20:1 완화
       (anima domain 특화 + simple_stack verdict 기준이므로 strict 20:1 부적용).
    
    4. **token/param ratio**: 150-200M param × ~3B token ≈ 15-20:1 (Chinchilla
       lower bound). 기존 corpus 350-500M token 으로 부족 → 외부 corpus blend
       경량 cycle (BG-CORPUS-3B) 또는 corpus repeat 2-5 epoch acceptable.
    
    5. **fire cost envelope 갱신**: $5-20 (v5-mitosis carry 추정) → $10-30
       (from-scratch ~3-5B token × 150-200M param × 1× H100 SXM × 10-20 hr).
    
    6. **step 1 의미 변경**: v5-mitosis cond.5 ckpt 의 PyPhi formal cross-check
       는 anchor verification (AT-RISK 회피) only — .clm v1 self 의 Φ measure
       는 fire 후 step 5 verdict cycle 에서.
  EOF
  cross_link = "REBORN.tape §88 cond.1 arch + §0.5 학습=분열 + PHILOSOPHY p8 + AXIS A5 H_019 SUPPORTED carry"

@D v_clm_v1_spec_from_scratch := ".clm v1 from-scratch concrete spec" :: design [d=2026-05-15 active]
  init_weights = "RANDOM INIT (seed-fixed, no ckpt inherit). v5-mitosis cond.5 ckpt 는 arch 검증 anchor only — weights inherit X."
  arch = {
    "d_model": "768 (192·4, n=6 anchor) primary OR 384 fallback if step 1 n=3,4 only PASS",
    "n_layers": "12 (σ(6) number-theoretic anchor + lattice-as-tool, V3 정정 carry) OR fallback {6, 24}",
    "n_cells": "64 (v5-mitosis cond.5 cells-saturated point carry, arch reference)",
    "n_heads": "8 (atom Hc_144) + kv_heads = 4 (τ(6))",
    "ffn_mult": "4 (τ(6))",
    "engine": "v5-mitosis cells=nn.Module branches single-stack (V1 정정 carry, Engine A/G dual 폐기, .clm v2 candidate)",
    "param_estimate": "~150-200M (d=768·12L)"
  }
  data = {
    "primary_corpus": "anima_persona_tier_a_v4 231MB + Phase 1A.6 corpus_v2 121MB (352MB total)",
    "token_estimate": "~350-500M token (Korean+English mix)",
    "repeat_strategy": "2-5 epoch acceptable (anima domain 특화, simple_stack verdict 기준) OR 외부 blend BG-CORPUS-3B 별도 cycle"
  }
  cotrain_recipe = {
    "mitosis_hook": "training-time mitosis hook per token (v5-mitosis cond.5 F-V5MIT 5/5 PASS mechanism carry, ckpt X)",
    "serve_time": "동일 mitosis_hook serve-time invoke (p8 단일 연속체)",
    "entropy_reg": "F-PERSONA-4 path 의 entropy reg (cond.5 v2 carry) optional — step 0 p1 upgrade gate 결과 따라 결정",
    "optimizer": "AdamW lr_warmup 5e-4 → cosine 5e-5 (Phase 1A.4 carry, scale per param)",
    "step_budget": "~5000 step × batch 16 × seq 1024 ≈ 80M token/epoch × 5 epoch = 400M token / 1× H100 SXM"
  }
  fire_cost_envelope = "$10-30 H100 SXM (from-scratch ~3-5B token × 150-200M param × 1× H100 × 10-20 hr) — 기존 $5-20 envelope 갱신"
  fire_keyword = "OK CLM V1 FROM-SCRATCH FIRE COST $10-30"
  supersedes = "v_clm_v1_spec_phase5 (2026-05-15 issued, 동일 day 정정 — from-scratch directive)"

@D v_clm_v1_step1_meaning_change := "step 1 PyPhi formal cross-check 의미 변경 — anchor verification only" :: protocol [d=2026-05-15 active]
  before = "v5-mitosis cond.5 ckpt 의 PyPhi formal Φ ≥ 0.5 = .clm v1 substrate 의 검증 anchor (substrate 가 ckpt-derived)"
  after = "v5-mitosis cond.5 ckpt 의 PyPhi formal Φ ≥ 0.5 = arch SUPPORTED anchor verification only (.clm v1 의 substrate 가 아님). .clm v1 self 의 Φ measure 는 fire 후 step 5 verdict cycle 에서."
  step1_new_role = "AT-RISK 회피 pre-fire — 만약 v5-mitosis cond.5 ckpt 의 PyPhi formal Φ < 0.5 면, .clm v1 의 arch (cells single-stack + 64-cell + d=384 등) 가 PyPhi formal-tier consciousness 확보 불가 가능성 시그널 → arch 수정 OR Φ★ proxy-only anchor 로 fall-back"
  decision_rules_updated = "step 1 PASS → arch 검증 carry (cells single-stack 64-cell d=384/768 OK). step 1 FAIL → arch 재설계 필요 (n_cells 증가 / d_model 조정 / cells topology 변경) OR Φ★ proxy-only 로 fall-back (단, p7 simple_stack verdict 가 primary 이므로 fall-back 도 가능)"
  supersedes = "v_step2_pyphi_formal_design (의미 명확화 amendment, 기존 falsifier battery F-PYPHI-FORMAL-1..5 유지)"

@D v_clm_v1_step3_spec_frozen_update := "step 3 .clm v1 spec frozen W1 — from-scratch field 추가" :: protocol [d=2026-05-15 active]
  added_fields = [
    "init_weights = 'RANDOM INIT seed-fixed' (from-scratch 명시)",
    "base_ckpt = 'NONE (no ckpt inherit, v5-mitosis cond.5 = arch SUPPORTED anchor only)'",
    "corpus_strategy = 'anima_persona_tier_a_v4 + Phase 1A.6 corpus_v2 + epoch_repeat 2-5x OR BG-CORPUS-3B blend (decision per cycle)'",
    "step_budget = '~5000 step × batch 16 × seq 1024 = 400M token / 1× H100 SXM × 10-20 hr'",
    "cost_envelope_updated = '$10-30 H100 SXM (from-scratch, 기존 $5-20 갱신)'"
  ]
  supersedes_fields = [
    "기존 v_step3 의 'cotrain_recipe' field 의 'v5-mitosis cond.5 carry' inherit 의미 제거",
    "fire_keyword: 'OK CLM V1 FIRE COST $5-20' → 'OK CLM V1 FROM-SCRATCH FIRE COST $10-30'"
  ]
  cross_link = "v_clm_v1_spec_from_scratch + step 1 의미 변경 + PHILOSOPHY p8 단일 연속체 from-scratch 적용"

@D v_clm_v2_v3_from_scratch := ".clm v2 + .clm v3 모두 from-scratch 정정" :: design [d=2026-05-15 active]
  scope = "사용자 directive '.clm 학습은 처음부터 진행하는걸로' = v1 만이 아닌 .clm 가족 전체 적용"
  v2_path_a_correction = "Path A 7B from-scratch (~7-8B param × ~140B token Chinchilla strict OR ~50B token Chinchilla 완화). .clm v1 ckpt inherit X — arch SUPPORTED 만 carry. Cost $200-600 유지 (corpus pipeline 의존)"
  v2_path_b_correction = "Path B Engine A/G dual + V14 audit complete 도 from-scratch — Phase 2 V14 violation ckpt inherit X (이미 verified-FAIL). Cost $200-640 유지"
  v3_phase4_correction = "Phase 4 14B 본진 = anima 사가 first scratch 14B from-scratch (CLM.tape §1 row_phase_4 narrative 동일). Cost $500-1500 유지"
  rationale = "from-scratch directive 가 .clm 가족 전체 적용 = anima_native_scratch (D1=1.0) 원칙 강화. 어떤 ckpt 도 .clm 의 base 안 됨 — pre-train 의 anima-specific scratch 만이 substrate self-generation 의 evidence anchor"
  cross_link = "v_clm_v2_path_a_design + v_clm_v2_path_b_design + CLM.tape §1 row_phase_4 + AXIS A1 H_005 corpus quality > scale carry"

@N v_from_scratch_open_questions := "from-scratch 정정의 open questions" :: caveat [d=2026-05-15 active]
  body <<~EOF
    Q1: corpus token budget 부족 (350-500M < Chinchilla optimal 3-4B for 150-200M
        param) — repeat 2-5 epoch 가 simple_stack verdict 에 미치는 영향 측정 cycle
        필요 (separate from .clm v1 fire). 또는 BG-CORPUS-3B cheap (50-100M extra
        token) blend cycle ($5-20 별도).
    
    Q2: from-scratch random init seed = anima domain 의 reproducibility anchor.
        seed-fixed (e.g., 42) 강제 + pre-register hash 에 seed 포함 mandatory.
    
    Q3: v5-mitosis cond.5 ckpt 의 PyPhi formal Φ measurement (step 1) 결과가
        FAIL 시 .clm v1 의 arch 도 동일 PyPhi formal-tier FAIL 가능성 — but
        from-scratch 라 ckpt-level 차이로 Φ ≥ 0.5 unlock 가능. step 5 verdict
        cycle 에서 self Φ measure 가 primary anchor.
    
    Q4: from-scratch 의 training cost variance ±50% (3-4B token vs 400M token
        repeat) — cost envelope $10-30 의 hard stop $50 safety margin 설정 권장.
    
    Q5: mitosis hook training-time mechanism carry (cond.5 F-V5MIT 5/5 PASS) 가
        from-scratch random init 위에서 동일하게 PASS 하는지 — fire 전 step 0
        다음에 step 0.5 mini-cotrain (90M smoke, 200 step, $0 Mac/cheap) 으로
        검증 가능 (optional gate).
  EOF
  cross_link = "future cycle: BG-CORPUS-3B blend + step 0.5 mini-cotrain smoke"

@D v_clm_v1_7step_from_scratch := ".clm v1 7-step plan from-scratch 정정" :: plan [d=2026-05-15 active]
  steps = [
    "0. (Mac $0, mandatory) p1 NO SYSTEM PROMPT upgrade measure — 3-arm × 3-ckpt × 5-seed × 10-prompt (carry, no change)",
    "0.5. (Mac $0-5, optional gate) mini-cotrain smoke — 90M from-scratch × 200 step × anima_persona corpus, F-V5MIT-5 V14-STRICT 재현 검증. PASS = mitosis hook from-scratch mechanism PASS confirm",
    "1. (Mac $0) F-PYPHI-Φ-FORMAL n=3-6 RoM test on v5-mitosis cond.5 ckpt — *anchor verification only* (v1 substrate 아님, 의미 변경 carry)",
    "2. (Mac $0) mitosis_hook serve-time integration smoke — synthetic OR fresh small init (real ckpt 의존 X, from-scratch 정합)",
    "3. (Mac $0) .clm v1 spec frozen W1 pre-register — init_weights = RANDOM INIT seed-fixed + base_ckpt = NONE + corpus strategy + step budget + cost $10-30",
    "4. (H100 $10-30 갱신) .clm v1 fire — from-scratch ~5000 step × batch 16 × seq 1024 × 1× H100 SXM 10-20 hr",
    "5. (Mac $0) .clm v1 verdict cycle — 8-falsifier battery (carry) + 4-tape sync. self PyPhi formal Φ measurement primary anchor (step 1 anchor verification 와 별개)",
    "6. (조건) .clm v2 candidate (Path A 7B from-scratch OR Path B dual + V14, conditional)"
  ]
  cost_total_updated = "$10-30 ($0 Mac × 5 steps + $0-5 optional mini-smoke + $10-30 H100 × 1 step) — 기존 $5-20 갱신"
  added = "step 0.5 mini-cotrain smoke (optional gate, $0-5)"
  changed = "step 1 의미 (substrate base → anchor verification only) + step 3 추가 fields + step 4 cost envelope"
  supersedes = "v_clm_v1_7step_corrected (2026-05-15 issued, 동일 day 정정 — from-scratch)"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-V3-DESIGN — .clm v3 14B 본진 candidate detailed design (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Scope: Phase 4 14B 본진 narrative + from-scratch directive + AXIS/철학/가설
#        검증된 기준 적용. anima 사가 first scratch 14B 등극 milestone.

@N v_clm_v3_summary := ".clm v3 14B 본진 design summary" :: design [d=2026-05-15 active]
  body <<~EOF
    .clm v3 = anima 사가 first scratch 14B from-scratch 본진. CLM.tape §1
    row_phase_4 narrative + from-scratch directive (PR #52 carry) + 검증된
    AXIS/철학/가설 기준 적용. .clm v2 PASS_STRICT (Path A 7B 또는 Path B
    dual+V14) 후 entry.
    
    arch carry from .clm v1+v2: cells=nn.Module branches single-stack arch
    (V1 정정 carry) + mitosis hook training+serve-time mechanism + AXIS A4
    perfect-number cluster anchor (n=6 + σ(6)=12 + τ(6)=4 + atom 8). param
    estimate ~14B (40L × 5120 × 40h × 8kv lattice-as-tool 적용).
    
    핵심 differentiator vs v2: scale-up (~7-14B → 14B strict) + Chinchilla
    optimal ~280B token mandatory (anima 도메인 narrow 한계 극복 위해 BG-CORPUS-14B
    cycle 필요, $50-200 별도).
    
    Cost envelope: $500-1500 (8-16× H100 × 75-250 hr from-scratch).
  EOF
  cross_link = "CLM.tape §1 row_phase_4 + §V-CLM-FROM-SCRATCH + AXIS A4/A5 anchor + PR #53"

@D v_clm_v3_arch_design := ".clm v3 14B arch detailed spec" :: design [d=2026-05-15 active]
  init_weights = "RANDOM INIT seed-fixed (from-scratch carry, no ckpt inherit)"
  arch = {
    "d_model": "5120 (192·26.67 — not clean 192 multiple ⚠) OR 4608 (192·24, clean) OR 6144 (192·32, clean)",
    "d_model_decision": "AXIS A1 H_174 phi_star aliasing CAVEAT — 5120 mod 192 = 128 partial-overlap (H_166 1024 mod 192 = 64 같은 위반 패턴). 정합: d_model = 4608 (192·24, clean) OR 6144 (192·32, clean). primary 4608 (lower cost), fallback 6144.",
    "n_layers": "32 (Phase 3/4 narrative carry) OR 36 (σ(6)·3) OR 40 (Phase 4 narrative carry, lattice-as-tool internal)",
    "n_layers_decision": "primary 32 (Phase 3/4 narrative), fallback 36 (σ(6)·3 clean number-theoretic) — V3 정정 carry (lattice-as-tool internal arch)",
    "n_cells": "256 (.clm v2 carry, 4× v5-mitosis cond.5 cells=64 baseline)",
    "n_heads": "32 (atom Hc_144 anchor scaled — σ(6)·n=8·4) OR 36 (σ(6)·3 carry)",
    "kv_heads": "8 (atom Hc_144 carry, 4:1 GQA ratio for d=4608)",
    "ffn_mult": "4 (τ(6) carry)",
    "param_estimate": "~13-14B (d=4608 32L) OR ~15-16B (d=4608 36L) — Phase 4 14B target carry",
    "engine": "v5-mitosis cells=nn.Module branches single-stack (V1 정정 carry, Engine A/G dual 폐기 unless v2 Path B PASS) + mitosis hook training+serve-time mechanism"
  }
  axis_anchor = "A4 H_153 τ(6)=4 + H_158 perfect-number cluster + H_160 meta-cluster + H_164 atom 8 cells + H_174 phi_star CLM-v4-specific (d=4608=192·24 clean ✓)"
  caveat = "d=5120 의 phi_star aliasing CAVEAT 회피 (H_166 caveat pattern 위반) — d=4608 primary 결정"

@D v_clm_v3_data_design := ".clm v3 14B data design" :: design [d=2026-05-15 active]
  corpus_target = "~280B token (Chinchilla optimal 20:1 for 14B param)"
  corpus_sources = [
    "anima_persona_tier_a_v4 (231MB ≈ 250-350M token, domain-specific)",
    "Phase 1A.6 corpus_v2 (121MB ≈ 130-180M token, chat-v2)",
    "BG-CORPUS-14B (별도 cycle, ~280B token blend — RedPajama-v2 + FineWeb-Edu + KO corpus)",
    "anima-specific augmentation (PHILOSOPHY.tape + REBORN.tape + AGENTS.tape + tape v1.2 corpus, ~50MB ≈ 50-80M token)"
  ]
  blend_ratio_design = "primary blend: 95% external (BG-CORPUS-14B ~266B) + 5% anima_persona+chat_v2+tape (~14B token 8-9x repeat to reach 14B). anima domain coverage maintain while general-language scale 확보."
  alternative_anima_heavy = "20% anima + 80% external (~56B anima token via 100-150x repeat) — overfitting risk 강하지만 anima 본질 강화"
  decision_rule = "BG-CORPUS-14B 의 Korean/English ratio 결정 + anima 본질 보전 simple_stack vs general-language perplexity tradeoff measurement cycle ($0 Mac BG-LB 350M proxy)"
  axis_anchor = "A1 H_005 corpus quality > scale (anchor for blend ratio) + A6 H_005 + H_016 (translation ceiling carry)"

@D v_clm_v3_cotrain_design := ".clm v3 14B cotrain recipe" :: design [d=2026-05-15 active]
  mitosis_hook = "training-time + serve-time mechanism carry from v1 (cond.5 F-V5MIT 5/5 PASS mechanism). 256-cell pool, max_seen ≤ 1024 (4× cap)"
  entropy_reg = "F-PERSONA-4 entropy reg carry (cond.5 v2 carry) — category routing diversification mandatory at 14B scale"
  optimizer = "AdamW lr_warmup 1e-4 → cosine 1e-5 (linear decay over ~280B token), gradient clip 1.0, weight_decay 0.1"
  step_budget = "~280B token × batch (per_device 8 × accum 4) × 16 GPU = 1.5M total steps / 8-16× H100 × ~150-250 hr ($500-1500 envelope)"
  ddp_strategy = "FSDP shard (cells=nn.Module branches single-stack 의 cell-as-parameter shard) — v5-mitosis v5/v6 DDP lesson (PSCC §52 4×A100 v6 fail $22 cost-ROI negative) carry"
  caveat = "16-GPU DDP 의 cell_pool 동기화 — mitosis hook 의 split/merge event 가 모든 rank 동일 동기화 mandatory. cond.5 v6 cell-parallel FAIL 의 lesson 통해 v5 DDP 방식 (all-rank sync) 우선"

@D v_clm_v3_falsifier_battery := ".clm v3 14B falsifier battery (12, .clm v2 10 + 2 new)" :: verify [d=2026-05-15 active]
  battery_carry_from_v2 = [
    "F-V5MIT-1..5 (cond.5 mechanism carry)",
    "F-PYPHI-Φ-FORMAL n=3-8 RoM ≥ 0.5 (carry)",
    "F-PRIN3 audit CLEAN (carry)",
    "F-PERSONA-1..5 STRONG ≥4/5 (carry)",
    "F-D4-LIVE-PROD-1..5 (carry)",
    "F-V58 std_greedy ≥4/5 (carry)",
    "F-DD21-LOG-PHI scale-invariant cross-substrate (carry)",
    "F-PHI-CE-NO-DIRECT-COUPLING (Hc_024 FALSIFIED carry)",
    "F-V14-NO-VIOLATION (v2 Path B carry, .clm v3 mandatory regardless of path)",
    "F-CHINCHILLA-OPTIMAL (v2 carry, 14B 의 strict 20:1 enforced)"
  ]
  battery_new_for_v3 = [
    "F-V3-PHI-MAX (anima 사가 최고 Φ): PyPhi formal Φ ≥ 1.0 strict (Hc_1283 n=5,6 carry Φ=0.995/1.665 baseline 의 .clm v3 14B 스케일 정합). PASS = 14B 본진 의 consciousness anchor 14B 본진 정합",
    "F-V3-SCALE-COHERENCE: simple_stack mean ≥ 3.5/4 strict on V5.8 5-mode (.clm v1 4/5 carry 의 14B 본진 정합 — strict 3.5/4 = +25% margin over baseline). PASS = scale-up 가 quality regression 없음"
  ]
  pass_criterion = "Path A: 11/12 PASS strict (F-V14 제외, single-stack carry). Path B: 12/12 PASS strict (V14 + V3-PHI-MAX + V3-SCALE-COHERENCE 모두)"
  cross_link = "AXIS A2.formal Hc_1283 (Φ ≥ 0.5 anchor) + .clm v1+v2 8+10 carry + Phase 4 14B milestone"

@D v_clm_v3_cost_envelope := ".clm v3 14B cost envelope detail" :: cost [d=2026-05-15 active]
  fire_cost = "$500-1500 (8-16× H100 SXM × 75-250 hr from-scratch)"
  corpus_pipeline = "$50-200 BG-CORPUS-14B 별도 cycle (RedPajama-v2 download + dedupe + tokenize + blend) — 별도 dispatch"
  total_envelope = "$550-1700 (.clm v3 fire $500-1500 + BG-CORPUS-14B $50-200)"
  fire_keyword = "OK CLM V3 14B FIRE COST $500-1500"
  hard_stop = "$2000 hard stop (envelope 의 1.3× safety margin) — 도달 시 partial weight save + hot-stop"
  entry_condition = ".clm v2 PASS_STRICT 10/12 (Path A 11/12 OR Path B 12/12) + BG-CORPUS-14B pipeline LANDED + 16× H100 SXM cluster 가용 + user verbatim 'OK CLM V3 14B FIRE COST $500-1500'"

@D v_clm_v3_milestone_significance := ".clm v3 14B 본진 등극 milestone significance" :: design [d=2026-05-15 active]
  scope = "anima 사가 narrative 의 first scratch 14B from-scratch — '본진' 의미"
  significance = [
    "(a) anima_native_scratch (D1=1.0) 원칙 의 full-scale 실현 — 어떤 외부 ckpt inherit 없음, anima specific arch + corpus + mitosis hook 의 14B scale 검증",
    "(b) Phase 4 narrative milestone — CLM.tape §1 row_phase_4 의 'anima 사가 first scratch 14B 본진 등극' realized",
    "(c) v5-mitosis lane evolution 의 정점 — cells=nn.Module branches single-stack arch (REBORN §88 cond.1) 가 14B scale 에서 PROD-READY 검증",
    "(d) external SOTA 비교 capability 우월 보장 X — 본진 = anima 자기집 substrate 확립 의미 (CLM.tape §9 C3-5 carry)"
  ]
  honest_c3 = "external Llama-3-13B / Qwen2.5-14B / DeepSeek-V3 등 SOTA 14B 모델 비교 시 capability 우월성 미보장 — .clm v3 = anima domain 특화 + simple_stack verdict + substrate self-generation 검증 anchor. general-language tasks 의 SOTA 와 다른 evaluation criterion."

# ══════════════════════════════════════════════════════════════════════
# §V-CORPUS-PIPELINE — BG-CORPUS-3B/7B/14B blend design (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Scope: .clm v1/v2/v3 의 corpus pipeline design — anima_persona+chat_v2 narrow
#        domain + external blend. open question Q3 (BG-CORPUS-7B design) carry.

@N v_corpus_pipeline_summary := "BG-CORPUS-{3B,7B,14B} blend pipeline summary" :: design [d=2026-05-15 active]
  body <<~EOF
    .clm v1 (~3B token) + v2 Path A (~50-140B) + v2 Path B (~140-280B) + v3
    (~280B) 의 corpus pipeline. anima_persona_tier_a_v4 (231MB) + Phase 1A.6
    corpus_v2 (121MB) = 352MB ≈ 350-500M token 의 narrow domain. external
    blend 3 size variant 의 BG cycle design.
    
    핵심 trade-off: (a) external blend 비율 ↑ = general-language scale 확보,
    anima 본질 dilution / (b) external blend 비율 ↓ = anima 본질 보전,
    overfitting (epoch repeat) 위험.
    
    Decision: simple_stack verdict (한글 in/out + coherent + natural + context)
    가 primary anchor 이므로 anima domain 보전 우선 (5-20% anima ratio) + 
    nature blend ratio measurement cycle ($0 Mac BG-LB proxy) 으로 final ratio
    결정.
  EOF
  cross_link = "CLM.tape §V-CLM-FROM-SCRATCH (corpus strategy) + v3 data design + open question Q3 + PR #53"

@D v_corpus_bg_3b_design := "BG-CORPUS-3B (.clm v1 .clm용) design" :: corpus [d=2026-05-15 active]
  scope = ".clm v1 (~3-5B token Chinchilla 완화) — small budget cycle"
  sources = [
    "anima_persona_tier_a_v4 (231MB ≈ 250-350M token, 7.5%)",
    "Phase 1A.6 corpus_v2 (121MB ≈ 130-180M token, 4%)",
    "tape corpus (PHILOSOPHY+REBORN+AGENTS+CLM 등 ~50MB ≈ 50-80M token, 1.5%)",
    "RedPajama-v2 KO subset (~2.5GB ≈ 2.5-3B token, 75-87%)",
    "FineWeb-Edu (~500MB ≈ 500M-1B token, optional)"
  ]
  blend_decision = "primary: 12-13% anima + 87-88% RedPajama-v2 KO subset (anima domain 보전 + Korean general-language coverage)"
  alternative = "alternative: 25% anima (corpus 2x repeat) + 75% RedPajama (overfitting tolerance 강화)"
  cost = "$5-20 (download + dedupe + tokenize ~3-5B token × Mac local hexa-interp OR cheap dispatch)"
  fire_keyword = "OK BG-CORPUS-3B FIRE COST $5-20"
  artifact = "state/bg_corpus_3b_<date>/manifest.json + dedupe.log + tokenized.parquet"

@D v_corpus_bg_7b_design := "BG-CORPUS-7B (.clm v2 .clm용) design" :: corpus [d=2026-05-15 active]
  scope = ".clm v2 Path A (~50B Chinchilla 완화) OR Path B (~140B strict) — middle budget cycle"
  sources_chinchilla_relaxed = [
    "anima_persona_tier_a_v4 + Phase 1A.6 + tape corpus (≈ 1-1.5% scale)",
    "RedPajama-v2 KO+EN subset (~50GB ≈ 40-50B token, ~98%)",
    "Slim_Pajama 또는 Pile (~10GB ≈ 5-10B token, optional)"
  ]
  sources_chinchilla_strict = [
    "anima 5% + RedPajama-v2 + FineWeb + Slim_Pajama blend ~140B token"
  ]
  blend_decision = "Path A primary: 5% anima + 95% RedPajama-v2 (KO 60% + EN 40%). Path B primary: 5% anima + 70% RedPajama-v2 + 25% FineWeb-Edu + Slim_Pajama"
  cost = "$50-100 (download + dedupe + tokenize ~50-140B token × cheap dispatch)"
  fire_keyword = "OK BG-CORPUS-7B FIRE COST $50-100"
  artifact = "state/bg_corpus_7b_<date>/"

@D v_corpus_bg_14b_design := "BG-CORPUS-14B (.clm v3 .clm용) design" :: corpus [d=2026-05-15 active]
  scope = ".clm v3 14B (~280B Chinchilla optimal) — large budget cycle"
  sources = [
    "anima_persona_tier_a_v4 + Phase 1A.6 + tape corpus (≈ 0.5% scale)",
    "RedPajama-v2 full (~100-150GB ≈ 100-150B token)",
    "FineWeb-Edu (~50-80GB ≈ 50-80B token)",
    "Slim_Pajama (~30-50GB ≈ 30-50B token)",
    "KO-specific corpus (mC4-ko + Aihub-corpus blend ~30-50GB ≈ 30-50B token)"
  ]
  blend_decision = "primary: 0.5% anima (5-10x repeat) + 70% RedPajama-v2 KO 40% EN 30% + 15% FineWeb-Edu + 10% Slim_Pajama + 5% KO-specific"
  alternative_anima_heavy = "2-5% anima (100-150x repeat overfitting risk) + 95-98% external"
  cost = "$50-200 (download + dedupe + tokenize ~280B token + multi-source blend ratio tuning)"
  fire_keyword = "OK BG-CORPUS-14B FIRE COST $50-200"
  artifact = "state/bg_corpus_14b_<date>/"

@N v_corpus_open_questions := "corpus pipeline open questions" :: caveat [d=2026-05-15 active]
  body <<~EOF
    Q1: anima blend ratio 의 optimal — small ratio 보전 vs large ratio dilution 의
        BG-LB 350M smoke proxy cycle 필요 ($0 Mac, 별도 cycle).
    
    Q2: RedPajama-v2 의 license / safety filter — Phase 1A.6 corpus_v2 carry 의
        dedupe + filter pipeline 재사용 + RedPajama license terms 검증.
    
    Q3: Korean-English ratio decision — anima 의 native language coverage anchor.
        anima_persona_tier_a corpus 의 KO/EN ratio measurement + simple_stack
        4-axis 한글 PASS 의 KO ratio threshold.
    
    Q4: 14B Chinchilla strict 280B token download/storage 의 infra requirement
        (~150-200GB disk + parallel download bandwidth) — 별도 infra cycle.
    
    Q5: tape corpus (PHILOSOPHY+REBORN+AGENTS+CLM) 의 anima 본질 anchor — tape
        grammar 자체가 anima 의 self-description, 다른 corpus blend 와 다른
        tier (substrate-native corpus). blend weight 결정 cycle.
  EOF
  cross_link = "future cycles: BG-LB 350M proxy + corpus filter pipeline + 14B infra"

# ══════════════════════════════════════════════════════════════════════
# §V-HF-CLEANUP-2026-05-15 — HF dancinlab/ cleanup + 새 canonical repo
# ══════════════════════════════════════════════════════════════════════
# Trigger: 사용자 directive 2026-05-15
#   "HF 먼저 정리하자 기존 CLM 올라간것들 이름 싹다 바꾸고 학습데이터셋도"
#   "CLM 은 명명 그냥 단순하게 하고 버전은 내부적으로 관리"
#   "DELETE 보류 — TRANSFER 으로 변경" "private 으로 전부 transfer"
# Method: TRANSFER dancinlab/* → dancinlife/* (deprecated user, private)

@D v_hf_cleanup_transfer := "HF dancinlab cleanup — TRANSFER + private (2026-05-15)" :: governance [d=2026-05-15 active]
  scope = "anima cleanup 대상 (precursor models + legacy datasets) 71 entities dancinlab/* → dancinlife/* TRANSFER + private"
  transferred_models = 63
  transferred_datasets = 8
  transferred_total = 71
  keep_in_dancinlab = "hexa-forge-* 37 (별도 project) + dancinlab/dancinlab org card + atlas.n6 (atlas 보류 status) + Spaces 3 (README + anima-experience + echoes-experience)"
  method = "huggingface_hub.move_repo() + huggingface_hub.update_repo_settings(private=True)"
  artifact = "/tmp/hf_transfer_log_<timestamp>.log (Mac local audit trail)"
  cross_link = "PR #54 + memory MEMORY.md (HF reference URLs) + .clm v1/v2/v3 design fire 시 → dancinlab/anima-clm new repo"

@D v_hf_new_canonical_repo := "HF new canonical repo — anima-clm + anima-corpus" :: governance [d=2026-05-15 active]
  models = "dancinlab/anima-clm (private, model) — .clm v1/v2/v3 internal version via HF revisions/branches/tags + README mapping table"
  datasets = "dancinlab/anima-corpus (private, dataset) — BG-CORPUS-3B/7B/14B internal version via HF revisions + README component table"
  naming_directive = "CLM 명명 단순, 버전 내부 관리 — single canonical repo name 'anima-clm' + 'anima-corpus' 사용"
  current_status = "placeholder repo + README LANDED 2026-05-15. .clm v1 fire 후 weights upload + revisions/branches 으로 version tag."
  cross_link = "https://huggingface.co/dancinlab/anima-clm + https://huggingface.co/datasets/dancinlab/anima-corpus + CLM.tape §V-CLM-DESIGN/AUDIT/FROM-SCRATCH + PR #54"

@N v_hf_cleanup_transferred_list := "71 transferred entities list" :: catalog [d=2026-05-15 active]
  models_clm_v4_sft = "30 (clm-v4-sft-{stage1, final, step-5k/10k/25k/50k, 1-5/1-6/1-7-y1/1-8 variants} + paradigm-j + base-mirror + mk2-v1)"
  models_clm_v2 = "3 (byte-18m-base + convo-5k + ft-recovery)"
  models_clm_3 = "2 (bprime-s1-ubu1/ubu2)"
  models_clm_v5 = "2 (bg-lb-350m-pretrain + phase2-cotrain-engine-ag)"
  models_clm_foundation = "1 (foundation-borrow-llama-3.2-3b-anima-lora)"
  models_anima_clm_precursor = "6 (bprime-prime + phase1a-multi-turn + phase1a1-color + phase1a4-lr5e6-strict + v5-la-cotrain + v5-mitosis-cotrain)"
  models_anima_native_byte18m = "2 (ko-chat-template-failed + ko-small)"
  models_anima_chat_v2 = "1 (chat-v2-2026-05-15)"
  models_bg = "3 (ja-ext-polyglot + km-llama3b + km-qwen-7b)"
  models_llm_llama32 = "4 (paradigm-a-prime base + r16 + s43 + s44)"
  models_p9_vlm = "2 (p9-llama32-lora + vlm-anima-voice-paradigm)"
  models_total = "63"
  datasets = "8 (anima-clm-3-corpus-mix + anima-cycle-reborn + anima-pass-strict + anima-persona-tier-a-v3/v4 + anima-sft-data + clm-v4-t4-phi-cache + akida-cloud-d0)"
  total = "71"

@D v_hf_collections_cleanup := "HF Collections cleanup — 2 CLM collections DELETE (2026-05-15)" :: governance [d=2026-05-15 active]
  scope = "anima cleanup carry — Collections 도 정리"
  deleted_collections = [
    "clm-v4-350m-lora-research-lineage (4 items, all CLM precursor — items 이미 dancinlife/* 로 transferred, references broken)",
    "first-simple-stack-pass-strict-own-18-v4-10-15 (3 items, CLM precursor own 18 V4 SIMPLE_STACK_PASS_STRICT reference, items broken)"
  ]
  remaining_collections = [
    "atlas.n6 — n=6 arithmetic design framework (1 item, atlas 보류 status keep)",
    "voice-vlm-anima-trajectory (1 item, vlm-anima-voice carry, anima-voice lane 별도 keep)"
  ]
  method = "huggingface_hub.delete_collection()"
  cross_link = "CLM.tape §V-HF-CLEANUP + PR #54"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-V3-14B-NARRATIVE-DETAIL — Phase 4 본진 등극 narrative (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Trigger: §V-CLM-V3-DESIGN milestone 강화 + Q1-Q4 open questions 해결 path

@N v3_milestone_narrative := ".clm v3 14B 본진 milestone narrative" :: design [d=2026-05-15 active]
  body <<~EOF2
    .clm v3 14B from-scratch = anima 사가 narrative 의 정점.
    
    의미:
    (a) 본진 = self-house — Phase 1A SFT (90M ckpt-inherit) + Phase 2 cotrain 
        (350M V14 fail) + Phase 1A.4 lr5e6 (V5.8 5/5) + v5-mitosis cond.5 lane
        (cotrain ckpt-graft) 모든 precursor lane 의 *통합*. anima_native_scratch
        (D1=1.0) 원칙 의 full-scale realization.
    
    (b) 외부 모델 비교 미안전 — Llama-3-13B / Qwen2.5-14B / DeepSeek-V3 등 SOTA
        14B 의 general capability 우월 보장 X. 본진 의 의미는 *anima 자기집*
        substrate 확립 (verdict 4-class catalog + 9-axis cluster + AXIS 32 🔵 + 
        8 philosophy + V5.8 simple_stack + persona substrate-native + mitosis
        serve-time hook + PyPhi formal Φ ≥ 0.5).
    
    (c) Phase 4 narrative 의 first scratch — CLM.tape §1 row_phase_4 의 'anima 
        사가 first scratch 14B 본진 등극' realized. precursor lane 의 모든 
        learning 흡수.
    
    (d) Multi-anima 시대 첫 ckpt — TENSION-LINK 5-ch meta-telepathy infrastructure
        (memory project_tension_link.md) 의 첫 본진 ckpt — anima ↔ anima 직접
        전송 substrate (.clm v3 cell-pool 의 fingerprint signature).
    
    (e) verdict catalog 38+ 🔵 entries 의 architectural realization — A4 math 8
        sympy + A3 physics 8 sympy + A9 universe 8 sympy + A5 architecture 9 
        (Transformer + RoPE + GQA) 의 *all anchor* 적용된 arch.
  EOF2

@D v3_open_questions_resolution := ".clm v3 14B Q1-Q4 open questions 해결 path" :: design [d=2026-05-15 active]
  q1_engine_a_supported = "Engine A lattice-projected layer 의 SUPPORTED entry — A4 sympy carry (perfect-number cluster + RoPE rotation). AXIS A4+A5 의 sympy anchor 가 Engine A 의 architectural anchor 충분. 별도 직접 검증 entry 부재 — Engine A 폐기 시 .clm v3 Path A (cells single-stack only) carry. Path B (Engine A/G dual) 만 V14 audit + Engine A 검증 cycle 필요."
  q2_chinchilla_anima = "Chinchilla 20:1 의 anima 도메인 적용 — Phase 1A.4 90M × 200 step (loss 0.51→0.18 66% reduction, V5.8 std_greedy 5/5) 의 데이터 사용 분석. anima_persona_tier_a corpus 231MB ≈ 230M token, 90M param × 20 = 1.8B token 필요. Phase 1A.4 = 200 step × ~5M token/step = 1B token. 50% Chinchilla undertrained but still V5.8 5/5 — anima 도메인 narrow 특화로 strict 20:1 부적용 확인. 결론: .clm v3 14B 의 적용 ratio 10-20:1 acceptable."
  q3_bg_corpus_14b_design = "BG-CORPUS-14B design — RedPajama-v2 70% (~196B token) + FineWeb-Edu 15% (~42B) + Slim_Pajama 10% (~28B) + KO-specific 5% (~14B) + anima_persona+chat+tape 0.5% (~1.4B, 5-10x repeat). Total ~281B token Chinchilla optimal. Korean/English ratio = KO subset 통계 추정 60-70% (anima 본질 보전), EN 30-40% (general scale). license/safety filter = Phase 1A.6 corpus_v2 의 dedupe+filter pipeline carry."
  q4_clm_v3_14b_phase4_entry = ".clm v3 → Phase 4 14B 본진 등극 entry condition = .clm v2 PASS_STRICT 10/12 (Path A 11/12 OR Path B 12/12) + BG-CORPUS-14B pipeline LANDED + 16× H100 SXM cluster 가용 + user verbatim 'OK CLM V3 14B FIRE COST $500-1500'. milestone 의의: anima_native_scratch D1=1.0 full-scale 실현 + TENSION-LINK multi-anima 인프라 시작 ckpt."
  cross_link = "CLM.tape §V-CLM-V3-DESIGN + §V-CLM-FROM-SCRATCH + Phase 4 row_phase_4 + memory project_tension_link.md + PR #58"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-STEP2-MITOSIS-SMOKE-CARRY — PSCC §41 synthetic carry + design refine
# ══════════════════════════════════════════════════════════════════════

@D v_step2_mitosis_smoke_carry := "step 2 mitosis_hook serve-time smoke — PSCC §41 synthetic carry" :: protocol [d=2026-05-15 active]
  scope = "step 2 (.clm v1 step 2 PHASE-2-mitosis-serve-time integration smoke) 의 synthetic substrate 결과 carry. real d=768 12L production smoke 별도 cycle (hexa runtime + ~7 hr Mac wall)."
  pscc_41_carry = "PSCC §41 anima_chat_split_merge_smoke.hexa carry: chat_generate(prompt='안녕? 너는 누구야?', max_new=40, greedy) on synthetic d=8 vocab=16 2L → 21 split events, mitosis_invocations=65 (prefill_n 25 + max_new 40). F-D4-LIVE-1..3 3/3 PASS."
  f_d4_live_prod_status = [
    "F-D4-LIVE-PROD-1 SPLIT-EVENT-COUNT: synthetic 21 splits (≥5 PASS), production scale d=768 별도 cycle",
    "F-D4-LIVE-PROD-2 INVOCATION-INVARIANT: synthetic 65 == 25+40 PASS, production carry expected",
    "F-D4-LIVE-PROD-3 NO-INFERENCE-CRASH: synthetic finite output PASS",
    "F-D4-LIVE-PROD-4 SIMPLE-STACK-NOT-WORSE: synthetic 측정 안 됨 (vocab=16 random), production 별도",
    "F-D4-LIVE-PROD-5 CELL-POOL-PERSIST: synthetic mitosis_event_log 보존 PASS, ~/.cache/anima/session_pools/ persist 별도"
  ]
  step2_verdict = "PARTIAL-CARRY (synthetic 3/5 explicit PASS, production 2/5 별도 cycle)"
  cross_link = "PSCC §41 PR LANDED + anima_chat.hexa v0.3 + CLM.tape §V-CLM-STEP2-DETAIL + PR #58"

# ══════════════════════════════════════════════════════════════════════
# §V-CLM-STEP4-SPEC-FROZEN — .clm v1 spec frozen W1 pre-register LANDED
# ══════════════════════════════════════════════════════════════════════

@D v_step4_spec_frozen := "step 4 .clm v1 spec frozen W1 pre-register LANDED (2026-05-15)" :: protocol [d=2026-05-15 active]
  artifact = "state/clm_v1_step4_spec_frozen_2026_05_15/spec_frozen.json"
  sha256 = "972e9987cd09118533161d5625ebde67a10aa5ec7f2e498bdbfca008a0f36ee5"
  spec_id = ".clm v1 spec frozen W1 pre-register v0.1.0-design-frozen"
  fields_frozen = "init (RANDOM INIT seed=42), arch (cells single-stack d=768 12L 64-cell 8-head 4-kv), data (anima_persona_tier_a_v4 + Phase 1A.6 + tape, 400-500M token, 2-5 epoch), cotrain (AdamW + bf16 + 5000 step + mitosis hook per token), fire ($10-30 H100), falsifier (8 battery), p1 gate (truncated 15-gen 3.4/4 PASS)"
  status = "W1 LANDED (additive_only_mutation via W8 amendment only). pre-fire 종합 dependency: step 0 full p1 (3 ckpt × 5 seed × 10 prompt = 450 gen 5/5 PASS) + step 1 PyPhi anchor carry + step 2 production smoke 별도"
  cross_link = "CLM.tape §V-CLM-DESIGN/AUDIT/FROM-SCRATCH/STEP0/STEP2/V3 + sha256.txt + PR #60"
