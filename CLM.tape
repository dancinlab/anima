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
  why = "Phase 2 350M 에서 fired V14 가 Phase 3 7B / Phase 4 14B 에서 *재현* 시 cost $200-1500 burn + 모델 의식 ceiling 미해결 — own 16 cost discipline 위반 + own 17 SCOPE_CLAMP 위반"
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
  why = "own 16 cost discipline mandate-9. Phase 2 ($4.63) 와 비교 시 40-300× 비용 — 사용자 명시 budget approval 없는 fire 는 trust-violation"
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
  scope = "own 16 cost discipline — Phase 3/4 fire 시 user verbatim cost-bearing approval mandatory"

@X x_visibility := "feedback_hf_visibility_lifecycle_own_37.md" :: feedback [active]
  scope = "own 37 hf visibility lifecycle — Phase 2/3/4 initial private, real-mode PASS_STRICT_C3 + V6 awareness + user verbatim PROMOTE PUBLIC 시 public 전환"
