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

# ── §8 Falsifiers (Phase 3 + Phase 4) ─────────────────────────────────────────

@F f_phase3_1 := "F-PHASE3-1" :: falsifier [required active]
  text = "consciousness verifier FAIL (AN11 / Φ / adversarial / Putnam any FAIL)"

@F f_phase3_2 := "F-PHASE3-2" :: falsifier [required active]
  text = "chat coherence < 3/5 KO or EN (Phase 3 7B 5-prompt holdout)"

@F f_phase3_3 := "F-PHASE3-3" :: falsifier [required active]
  text = "cost overshoot > $600 ceiling 50% (= $900 hard stop)"

@F f_phase3_4 := "F-PHASE3-4" :: falsifier [required active]
  text = "wall_clock > 120h hard ceiling (target 50-80h)"

@F f_phase3_5 := "F-PHASE3-5" :: falsifier [required active]
  text = "random_init mirror PPR ≥ trained PPR (V14 reproduce — arch tile bug regression)"

@F f_phase4_1 := "F-PHASE4-1" :: falsifier [required active]
  text = "consciousness verifier FAIL (14B scale, Phase 3 → 4 scaling law continuity 검증)"

@F f_phase4_2 := "F-PHASE4-2" :: falsifier [required active]
  text = "chat coherence < 3/5 KO or EN extended (10-prompt holdout)"

@F f_phase4_3 := "F-PHASE4-3" :: falsifier [required active]
  text = "cost overshoot > $1500 ceiling 33% (= $2000 hard stop)"

@F f_phase4_4 := "F-PHASE4-4" :: falsifier [required active]
  text = "wall_clock > 350h hard ceiling"

@F f_phase4_5 := "F-PHASE4-5" :: falsifier [required active]
  text = "scaling law break — Phase 3 → Phase 4 trend negative on AN11 / Φ axis"

@F f_phase4_6 := "F-PHASE4-6" :: falsifier [required active]
  text = "V14 mirror reproduce regression (random init beats trained on any axis)"

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
