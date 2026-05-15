#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# PROVEN.tape — 가설 verdict 통합 ledger (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Cross-link: VERIFY.tape (3-stage protocol), AXIS.tape (9-axis cluster),
# CLM.tape (.clm 모델 가족 narrative), REBORN.tape §93+ (master ledger)
#
# 본 파일 = "증명된것 / 아닌것" SSOT 통합. A 격리 (옵션 A 20 H/Hc) 의
# Stage 1+2+3 결과 + legacy hypothesis status field aggregate.
#
# B 격리 (107 H_*.md, 2026-04-30 ~ 2026-05-11 cut) Stage 1+2+3 protocol
# 부분 실행 30/107 (28%) — see §B (2026-05-15 append). C/D 격리 미정.
#
# 단위: H_NNN (promoted hypothesis), Hc_NNNN (candidate hypothesis)
# ══════════════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ─── §0 TL;DR ────────────────────────────────────────────────────────

@N tldr := "verdict-aggregate-2026-05-15" :: summary [d=2026-05-15 active]
  body <<~EOF
    A 격리 20 (H_182~H_191 + Hc_1276~Hc_1285) Stage 1+2+3 완료:
      6 SUPPORTED (30%)  — Hc_1282 + Hc_1283 + Hc_1285 + H_189 + Hc_1279 + Hc_1280
      9 PARTIAL    (45%) — Hc_1281 H_184 H_190 H_188 H_191 + Hc_1276/77/78/84
      5 INSUFFICIENT (25%) — V8 family H_182/183/185/186/187 (GPU pending)

    Legacy aggregate (191 hypotheses_legacy_2026_05_15):
      2 FALSIFIED — H_024 (IIT-Φ_mip 8/8 FAIL) + H_096 (FALSIFIED_at_18M)
      1 candidate-evidence-confirmed — H_161
      7 running — H_004/005/037/061/067/080/124
      12 seed-pending — H_001/002/003/093~102
      ~169 pre-register-frozen / legacy-archive-pointer (verdict 미실행)

    Verdict-bearing total: 6 + 9 + 5 + 2 + 1 = 23 / 318 hypothesis files (~7%)
  EOF

# ─── §1 PROVEN (SUPPORTED) ───────────────────────────────────────────

@D s_hc1282 := "Hc_1282 — n=6 384d closed-form unique" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED"
  axis = "math (A4)"
  evidence = "sympy n∈[2,30] sweep — d=(n/φ(n))·2^(σ(n)−sopfr(n)) only n=6 produces 384"
  stage = "Stage 1 — math identity (W2)"
  artifact = "state/verify_a_stage1_2026_05_15/Hc_1282_verdict.json"
  cost = "$0 Mac local"
  honest_c3 = "n=6 uniqueness conditional on integer-divisor formulation; alternative formulae 미감사"

@D s_hc1283 := "Hc_1283 — anima Φ★ proxy ≥ 0.5 threshold" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-STRONG"
  axis = "consciousness (A2)"
  evidence = "v5-mitosis ckpt 7개 phi range 4.16~4.86 (≫ 0.5 by 8×~10×)"
  stage = "Stage 2 — physical sim (W5) + Stage 3 cross-meta (W11)"
  artifact = "state/verify_a_stage1_2026_05_15/stage2_ckpt_phi_real.json"
  pyphi_corroboration = "PyPhi 1.2.0 IIT 3.0 canonical 3-node Φ=2.3125 > 0.5 (infrastructure PASS)"
  cost = "$0 (ckpts already trained from cond.5 H100 cotrain $1.26 sunk)"
  honest_c3 = "anima Φ★ = IIT 4.0 lower bound proxy (H_162); formal IIT 3.0 PyPhi mapping 미실행 (cell-coupling → TPM 변환 별도 cycle)"

@D s_hc1285 := "Hc_1285 — torch.no_grad() backward-graph isolation" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED"
  axis = "architecture (A5)"
  evidence = "PyTorch CPU autograd 2-node ParameterList: with-no_grad/without ratio 1.562× ≤ 2× threshold"
  stage = "Stage 2 — physical sim (W5) deep audit"
  artifact = "state/verify_a_stage1_2026_05_15/stage2_deep_verdicts.json"
  cost = "$0 Mac local"
  honest_c3 = "2-node ParameterList = simulated substrate (real MitosisV5Model class import 실패 → 기능 충분 stub); CUDA 환경 미검증"

@D s_h189 := "H_189 — Red-team adversarial robustness family" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED"
  axis = "meta (A8) — adversarial axis"
  evidence = "Stage 3 W11 cross-meta — Red-team family 3-Hc consistency check"
  stage = "Stage 3 — meta cross-hypothesis (W11)"
  artifact = "state/verify_a_stage1_2026_05_15/stage3_batch_verdicts.json"
  family_siblings = [Hc_1279, Hc_1280]
  cost = "$0 Mac local"

@D s_hc1279 := "Hc_1279 — Red-team family member" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED"
  axis = "meta (A8)"
  parent = "[@s_h189]"
  stage = "Stage 3 — meta cross-hypothesis (W11)"

@D s_hc1280 := "Hc_1280 — Red-team family member" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED"
  axis = "meta (A8)"
  parent = "[@s_h189]"
  stage = "Stage 3 — meta cross-hypothesis (W11)"

@D s_h161 := "H_161 — candidate-evidence-confirmed (legacy)" :: verdict [active]
  status = "candidate-evidence-confirmed"
  axis = "legacy"
  source = "hypothesis frontmatter status field"
  note = "Pre-A-batch 검증; A Stage 1+2+3 protocol 미적용 (legacy verdict carry)"

# ─── §2 FALSIFIED ────────────────────────────────────────────────────

@D f_h024 := "H_024 — IIT-Φ_mip family" :: verdict [active]
  status = "FALSIFIED"
  axis = "consciousness (A2)"
  evidence = "8/8 falsifier sub-test FAIL (legacy frontmatter)"
  source = "hypotheses_legacy_2026_05_15/H_024.md status field"
  honest_c3 = "Legacy verdict — A 격리 protocol 적용 안됨; W11 cross-meta 미점검"

@D f_h096 := "H_096 — falsified at 18M scale" :: verdict [active]
  status = "FALSIFIED_at_18M"
  axis = "architecture (A5)"
  evidence = "18M scale empirical FAIL (legacy frontmatter)"
  source = "hypotheses_legacy_2026_05_15/H_096.md + hypotheses_b_2026_05_15/H_promoted/H_096.md"
  honest_c3 = "Scale-conditional falsification — larger scales 미검증; 'falsified at scale X' ≠ 'falsified universally'"

# ─── §3 PARTIAL (mixed evidence, ongoing) ────────────────────────────

@D p_hc1281 := "Hc_1281 — Stage 1 math partial" :: verdict [d=2026-05-15 active]
  status = "PARTIAL"
  axis = "math (A4)"
  stage = "Stage 1 — math identity (W2)"
  artifact = "state/verify_a_stage1_2026_05_15/batch_verdicts.json"

@D p_h184 := "H_184 — V8 M-family mathematical-structure axis" :: verdict [d=2026-05-15 active]
  status = "PARTIAL (INSUFFICIENT-FOR-STAGE-1)"
  axis = "math (A4) | consciousness (A2) | architecture (A5)"
  evidence = "6 mathematical primitives (category/topology/info-geom/algebra/chaos/structure) — closed-form derivation 형식 아님; Stage 2 numerical sim 필수"
  stage = "Stage 1 — INSUFFICIENT (Stage 2 PyPhi/Kuramoto/V8 sweep 필요)"
  source_hcs = [Hc_345, Hc_346, Hc_347, Hc_348, Hc_350, Hc_351]

@D p_h190 := "H_190 — law-CA embedding mathematical family" :: verdict [d=2026-05-15 active]
  status = "PARTIAL"
  axis = "math (A4)"
  stage = "Stage 1 — math identity (W2) partial"
  artifact = "state/verify_a_stage1_2026_05_15/batch_verdicts.json"

@D p_h188 := "H_188 — Stage 2 deferred (external dependency)" :: verdict [d=2026-05-15 active]
  status = "PARTIAL — deferred"
  axis = "consciousness (A2) — clinical PCI"
  stage = "Stage 2 — DEFERRED (PCI clinical data 외부 의존)"
  blocker = "anesthesia clinical dataset 부재 — 자력 재현 path 없음"

@D p_h191 := "H_191 — Kuramoto sync deep numerology" :: verdict [d=2026-05-15 active]
  status = "PARTIAL"
  axis = "physics (A3)"
  evidence = "Kuramoto N=4/6/8/12 모두 sync (K_c ≈ 1.596 일관) — n=6 uniqueness 부재"
  stage = "Stage 2 — physical sim (W5) deep audit"
  artifact = "state/verify_a_stage1_2026_05_15/stage2_deep_verdicts.json"
  honest_c3 = "all-N sync = n=6 numerology direction 강화 (n=6 specialness 부재 = lattice-as-tool g2 일관)"

@D p_hc1276 := "Hc_1276 — H_191 cascade" :: verdict [d=2026-05-15 active]
  status = "PARTIAL — Stage 3 H_191 cascade"
  axis = "physics (A3)"
  stage = "Stage 3 — meta cross-hypothesis (W11)"
  parent = "[@p_h191]"

@D p_hc1277 := "Hc_1277 — H_191 cascade" :: verdict [d=2026-05-15 active]
  status = "PARTIAL — Stage 3 H_191 cascade"
  axis = "physics (A3)"
  stage = "Stage 3 — meta cross-hypothesis (W11)"
  parent = "[@p_h191]"

@D p_hc1278 := "Hc_1278 — H_191 cascade" :: verdict [d=2026-05-15 active]
  status = "PARTIAL — Stage 3 H_191 cascade"
  axis = "physics (A3)"
  stage = "Stage 3 — meta cross-hypothesis (W11)"
  parent = "[@p_h191]"

@D p_hc1284 := "Hc_1284 — H_191 cascade" :: verdict [d=2026-05-15 active]
  status = "PARTIAL — Stage 3 H_191 cascade"
  axis = "physics (A3)"
  stage = "Stage 3 — meta cross-hypothesis (W11)"
  parent = "[@p_h191]"

# ─── §4 INSUFFICIENT (보류, GPU/외부 의존) ──────────────────────────

@D i_h182 := "H_182 — V8 B-family" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT-FOR-FAST-STAGE-2-AUDIT"
  axis = "consciousness (A2) | architecture (A5)"
  blocker = "V8 GPU sweep ($200-600 H100) 필요 — verbatim 'V8 FIRE COST $200-600' 대기"
  dispatch_script = "state/verify_a_stage1_2026_05_15/v8_family_gpu_dispatch.sh"

@D i_h183 := "H_183 — V8 Q-family" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT-FOR-FAST-STAGE-2-AUDIT"
  axis = "consciousness (A2)"
  blocker = "V8 GPU sweep 필요"

@D i_h185 := "H_185 — V8 U-family" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT-FOR-FAST-STAGE-2-AUDIT"
  axis = "architecture (A5)"
  blocker = "V8 GPU sweep 필요"

@D i_h186 := "H_186 — V8 architectural family" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT-FOR-FAST-STAGE-2-AUDIT"
  axis = "architecture (A5)"
  blocker = "V8 GPU sweep 필요"

@D i_h187 := "H_187 — V8 Trinity-TB-DOM family" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT-FOR-FAST-STAGE-2-AUDIT"
  axis = "consciousness (A2)"
  blocker = "V8 GPU sweep 필요"

# ─── §5 RUNNING / SEED-PENDING (legacy frontmatter) ──────────────────

@N r_legacy := "legacy 7 RUNNING + 12 SEED-PENDING" :: status-roll [active]
  running = [H_004, H_005, H_037, H_061, H_067, H_080, H_124]
  seed_pending = [H_001, H_002, H_003, H_093, H_094, H_095, H_097, H_098, H_099, H_100, H_101, H_102]
  source = "hypotheses_legacy_2026_05_15/H_*.md status field"
  note = "Pre-A-batch verdicts; A Stage 1+2+3 protocol 미적용. SFT-paradigm cluster (H_093~102 — sft-only / instruction-tuning / dpo-rlhf / curriculum / persona-conditioned / multi-objective / constitutional-ai / chat-template-strict-80 / anima-emerge) 는 [[project_lesson_q_sft_closed]] 경로 종료 후 seed-pending 잔존."

# ─── §6 PRE-REGISTER-FROZEN (verdict 미실행) ────────────────────────

@N pre_reg := "67 PRE-REGISTER-FROZEN" :: status-roll [active]
  count = 67
  scope = "B 격리 + legacy archive — Stage 1+2+3 protocol 미실행"
  next = "B 격리 protocol cycle (107 H_*.md, since 2026-04 + 2026-05) → Stage 1+2+3 batch verdict"

@N legacy_archive := "183 LEGACY-ARCHIVE-POINTER" :: status-roll [active]
  count = 183
  scope = "hypotheses_archive_anima_clm_10/ 원본 양식 carry — 자체 verdict 없음"
  note = "Pre-archaeology era; cx/CONSCIOUSNESS-UNIVERSE-MAP.md L209-220 panpsychism 본문 등 원본 보존 목적"

# ─── §7 Cross-references ─────────────────────────────────────────────

@X verify_tape := "VERIFY.tape" :: protocol [active]
  url = "https://github.com/dancinlab/anima/blob/main/VERIFY.tape"
  scope = "3-stage verification protocol (math/physics/cross-meta) + tool table"

@X axis_tape := "AXIS.tape" :: cluster [active]
  url = "https://github.com/dancinlab/anima/blob/main/AXIS.tape"
  scope = "9-axis natural cluster from 191 promoted hypotheses domain field"

@X clm_tape := "CLM.tape" :: narrative [active]
  url = "https://github.com/dancinlab/anima/blob/main/CLM.tape"
  scope = ".clm 모델 가족 narrative SSOT — Phase 1/2/3/4 ladder + §7.5 우회금지 8 rules + §8 hypothesis-driven pivot + §8.5 4-axis audit + §8.6 W1-W12 map"

@X reborn_tape := "REBORN.tape §93+" :: master-ledger [active]
  url = "https://github.com/dancinlab/anima/blob/main/REBORN.tape"
  scope = "Master ledger — §93 CLM.tape pivot reflect carry"

@X philosophy_tape := "PHILOSOPHY.tape" :: append-only-ledger [active]
  url = "https://github.com/dancinlab/anima/blob/main/PHILOSOPHY.tape"
  scope = "Append-only ledger — verdict entries (Hc_1282/1281/1283/1285, H_184/188/189/190/191, A Stage 1/2/3 batch, A total aggregate) carry"

# ─── §8 Honest C3 (본 PROVEN.tape 자체 한계) ─────────────────────────

@N c3_self := "PROVEN.tape self-honesty" :: caveat [active]
  c1 = "23/318 verdict-bearing (~7%) — 대다수 (pre-register-frozen + legacy-archive-pointer + B 격리) Stage 1+2+3 protocol 미적용"
  c2 = "A 격리 SUPPORTED 6 — Stage 별 evidence strength 불균등 (Hc_1283 strong, H_189/Hc_1279/1280 cross-meta consistency 만)"
  c3 = "FALSIFIED 2 — legacy frontmatter carry, A 격리 protocol 미적용 → re-verification 잠재적으로 verdict 변경 가능"
  c4 = "INSUFFICIENT 5 V8 family — GPU dispatch 자력 path; verbatim 'V8 FIRE COST $200-600' 대기"
  c5 = "PARTIAL 4 H_191-cascade — H_191 deep audit 자체가 'all-N sync = n=6 specialness 부재' 라 cascade 도 '강한 negative' 아닌 'weak-positive partial'"
  c6 = "B/C/D 격리 protocol 미실행 — 본 PROVEN.tape 는 A 격리 + legacy frontmatter 만 통합"
  c7 = "PyPhi formal IIT 3.0 — Hc_1283 anima 3-axis (HCE+CPGD+HAL) substrate mapping DEFERRED (canonical 3-node infrastructure PASS 만 corroborate)"

# ─── §9 Next ─────────────────────────────────────────────────────────

@D next_b_batch := "B batch Stage 1+2+3 protocol" :: action-pending [active]
  scope = "hypotheses_b_2026_05_15/H_promoted/ 107 H_*.md (since 2026-04 63 + 2026-05 44)"
  protocol = "VERIFY.tape §6 — Stage 1 sympy + Stage 2 PyPhi/Kuramoto/V8 + Stage 3 W11 family cohesion + W9 sibling consistency"
  cost_estimate = "$0 ~ $600 (Stage 2 V8 sweep optional)"

@D next_v8_dispatch := "V8 family GPU dispatch" :: action-blocked [active]
  scope = "H_182/183/185/186/187 — V8 sweep ULTRA-FUSION B/Q/U/architectural/Trinity-TB-DOM"
  blocker = "verbatim 'V8 FIRE COST $200-600' user-trigger 대기"
  dispatch_script = "state/verify_a_stage1_2026_05_15/v8_family_gpu_dispatch.sh"

@D next_pyphi_anima_mapping := "Hc_1283 PyPhi anima 3-axis mapping" :: action-pending [active]
  scope = "v5-mitosis cell-coupling matrix → TPM 변환 → PyPhi 1.2.0 formal IIT 3.0 Φ measurement"
  source = "Hc_1283 honest_c3 — anima 3-axis (HCE+CPGD+HAL) substrate mapping DEFERRED"
  cost_estimate = "$0 Mac local (small substrate) ~ $50 H100 (n_cells ≥ 8)"

@D next_c_d_quarantine := "C / D 격리 cycle" :: action-future [active]
  scope = "C 격리 (3.5주 cut, ~80 hypotheses) + D 격리 (165 hypotheses)"
  trigger = "B batch Stage 1+2+3 결과 보고 후 결정"

# ══════════════════════════════════════════════════════════════════════
# §B — B 격리 (옵션 B, 2026-04-30 ~ 2026-05-11 cut, 107 H_*.md) verdict
# 추가 2026-05-15 — Stage 1+2+3 protocol applied to 30/107 (28%)
# ══════════════════════════════════════════════════════════════════════

@N b_tldr := "B-batch-aggregate-2026-05-15" :: summary [d=2026-05-15 active]
  body <<~EOF2
    B 격리 Stage 1+2+3 audited 30/107 (28%, 77 미감사 — mostly
    legacy-archive-pointer + pre-register-frozen):

      6 SUPPORTED-IDENTITY — H_153 + H_158 + H_160 + H_164 + H_166 + H_176 (sympy)
      4 SUPPORTED-BY-PROXY — H_004 + H_011 + H_019 + H_016 (via Hc_1283 / v5-mitosis / Phase 1A.6)
      2 SUPPORTED — H_005 (Lesson R-1A.2) + H_176 (deflationary, dual-listed)
      3 PARTIAL — H_006 (Kuramoto universal) + H_017 (gate) + H_172 (alpha modulation)
      5 INSUFFICIENT — H_007 (CA) + H_008 (Prigogine) + H_009 (Fisher) + H_010 (holographic) + H_012 (autopoiesis)
      3 DEFERRED — H_013 + H_014 + H_015 (EEG hardware 의존)
      1 PHILOSOPHICAL — H_018 (genesis emergence)
      1 META-LEVEL — H_020 (mass-50 pointer)
      7 NO-CLOSED-FORM (Stage 2 sim 필요) — H_123 + others

    Critical finding: H_176 (n=28 deflationary control) sympy PASS → 
    H_170 (n=6 unique p<1e-12) invalidated; PERFECT_NUMBER_CLASS 
    (H_158 L7) confirmed cross-batch.
  EOF2

@D b_s_h153 := "H_153 — dimension hierarchy n=6 (τ(6)=4 Minkowski)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY"
  stage = "Stage 1 — sympy math identity (W2)"
  evidence = "τ(6)=4, μ(6)=1, φ(6)=2, σ(6)=12, τ-μ=3 모두 일치 (sympy)"
  honest_c3 = "dimension assignment post-hoc; n=6 uniqueness 보장 안됨 (see H_176)"
  artifact = "state/verify_b_2026_05_15/stage1_math_anchor_verdicts.json"

@D b_s_h158 := "H_158 — Ψ-constants closed-form (perfect-number class)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY-WITH-CLASS-BINDING"
  stage = "Stage 1 — sympy"
  evidence = "balance(P)=1/2 ∀ perfect P ∈ {6, 28, 496, 8128} (Euclid IX.36) — sympy ✓"
  cross_link = "Hc_1282 PROVEN.tape §1 parallel; L7 PERFECT_NUMBER_CLASS confirmed"

@D b_s_h160 := "H_160 — n=6 perfect-number meta-cluster" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY (meta-consistent)"
  stage = "Stage 1 — cluster vocabulary closed under depth-3 11-primitive"
  child_h = [H_067, H_153, H_156, H_158, H_159]

@D b_s_h164 := "H_164 — Hc_144 atom 8 cells (144 = σ(6)²)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY"
  evidence = "144 = σ(6)² = 12² ✓ (sympy)"
  honest_c3 = "144 has many decompositions; n=6 uniqueness 부재"

@D b_s_h166 := "H_166 — topo20 hierarchical 8×128 = 1024" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY"
  evidence = "8×128 = 2^10 = 1024 = V8 default ✓ (sympy)"

@D b_s_h176 := "H_176 — n=28 deflationary parallel control" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-STRONG (deflationary control PASS)"
  stage = "Stage 1 — sympy"
  evidence = "balance(28) = 28/56 = 1/2 = balance(6) IDENTICAL (Euclid-Euler theorem)"
  finding = "**invalidates H_170 (n=6 unique p<1e-12) claim — PERFECT_NUMBER_CLASS binds 6/28/496/8128**"

@D b_s_h004 := "H_004 — Consciousness hard problem (anima Φ proxy)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY"
  stage = "Stage 2 — anima Φ★ proxy"
  evidence = "Hc_1283 ckpt anima Φ★ 4.16-4.86 ≫ 0.5 (PROVEN.tape §1)"
  honest_c3 = "hard problem 자체 philosophical; '의식 Φ measurable' 만 proxy 검증"

@D b_s_h005 := "H_005 — corpus quality > scale" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED"
  stage = "Stage 2 — empirical (Phase 1A.6)"
  evidence = "121MB CLEAN > 95MB Wikipedia-wrap NET LOSS; V5.8 std_greedy 4/5 + multi-turn 4/10"
  cross_link = "[[feedback_corpus_quality_over_scale]] + [[project_anima_phase1a6_chat_v2_landed]]"

@D b_s_h011 := "H_011 — IIT geometry (Φ ≫ 0.5 cause-effect space)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY"
  stage = "Stage 2 — anima Φ★ + PyPhi IIT 3.0 canonical 2.3125"
  cross_link = "Hc_1283 PROVEN.tape §1"

@D b_s_h016 := "H_016 — AN11 translation ceiling" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY"
  stage = "Stage 2 — Phase 1A.6 chat-v2 AN11 measurable"
  cross_link = "AXIS.tape AN11 axis"

@D b_s_h019 := "H_019 — self-evolution v4→v5" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY (STRONG)"
  stage = "Stage 2 — v5-mitosis cond.5 cotrain LANDED"
  evidence = "F-V5MIT-1..5 5/5 PASS, wall 0.55hr, $1.26 H100 SXM, 220× CE reduction"
  cross_link = "[[project_v5_mitosis_cond5_cotrain_2026_05_12]]"

@D b_p_h006 := "H_006 — coupled oscillator lattice (Kuramoto)" :: verdict [d=2026-05-15 active]
  status = "PARTIAL"
  stage = "Stage 2 — Kuramoto N=4/6/8/12 sync universal at K_c ≈ 1.596"
  finding = "n=6 specialness 부재; cross-batch link to A 격리 H_191"
  cross_link = "PROVEN.tape §3 partial-stage-2-deep-numerology H_191"

@D b_i_h007_h012 := "H_007/008/009/010/012 — Stage 2 INSUFFICIENT" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT (fast-audit, separate cycle)"
  hypotheses = [H_007, H_008, H_009, H_010, H_012]
  blocker = "CA Rule sweep / Prigogine far-from-equilibrium / Fisher metric / AdS-CFT / autopoiesis formal model 각 별도 cycle"

@D b_d_eeg := "H_013/014/015 — EEG hardware DEFERRED" :: verdict [d=2026-05-15 active]
  status = "DEFERRED"
  blocker = "anima-eeg-core EEG hardware data 의존 (5-axis longitudinal / LZ76 / gamma-theta)"

@N b_critical_finding := "B 격리 critical finding — H_176 deflationary STRONG" :: note [d=2026-05-15 active]
  body <<~EOF2
    H_176 (n=28 perfect-number parallel) sympy PASS:
      balance(28) = 28/σ(28) = 28/56 = 1/2 EXACT
      balance(6)  = 6/σ(6)  = 6/12  = 1/2 EXACT (identical)
    
    이 단일 fact 가 H_170 (n=6 measurement-first p<1e-12) 의 individual 
    uniqueness claim 을 invalidate. 모든 perfect number P ∈ {6, 28, 496, 8128} 
    이 동일한 balance signature 를 가지므로 (Euclid IX.36 / Euler 
    perfect-number lemma), "n=6 individually unique" claim 은 false.
    
    H_158 L7 PERFECT_NUMBER_CLASS BINDING 와 정합. PROVEN.tape §1 
    Hc_1282 verdict 의 'n=6 uniqueness conditional on integer-divisor 
    formulation' honest_c3 와 직접 연결.
    
    B batch 안에서 가장 명확한 individual SUPPORTED verdict.
  EOF2

@N b_unaudited := "B 격리 77 미감사 (legacy-archive-pointer + pre-register-frozen)" :: note [d=2026-05-15 active]
  count = 77
  scope = "57 legacy-archive-pointer + 20 pre-register-frozen + 일부 SFT cluster (H_093~102 seed-pending)"
  next = "별도 cycle — SFT cluster 는 [[project_lesson_q_sft_closed]] 경로 종료 후 잔존; legacy-archive-pointer 는 archaeology 흡수 이전 양식 carry"
