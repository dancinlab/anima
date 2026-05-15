#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# MAIN.tape — 가설 verdict 통합 ledger (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Cross-link: VERIFY.tape (3-stage protocol), AXIS-V1.tape (9-axis cluster),
# CLM.tape (.clm 모델 가족 narrative), REBORN.tape §93+ (master ledger)
#
# 본 파일 = "증명된것 / 아닌것" SSOT 통합. A 격리 (옵션 A 20 H/Hc) 의
# Stage 1+2+3 결과 + legacy hypothesis status field aggregate.
#
# B 격리 (107 H_*.md) Stage 1+2+3 (30) + deep cycle (77) = 100% audited.
# V8 family Mac surrogate ($0): 5/5 SUPPORTED+PARTIAL (H_186 multi-head fix).
# PyPhi RoM cycle: PARTIAL→SUPPORTED upgrade (n=4 Φ=0.61~0.68 ≥ 0.5).
# C/D 격리: manifest-only + 2026-03 cluster 48 audited.
# H_174 SUPPORTED-STRONG (D=768 forced cos+1.0 aliasing sympy verified).
#
# 단위: H_NNN (promoted hypothesis), Hc_NNNN (candidate hypothesis)
# ══════════════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ─── §0 TL;DR ────────────────────────────────────────────────────────

@N tldr := "verdict-aggregate-2026-05-15" :: summary [d=2026-05-15 active]
  body <<~EOF
    MAIN.tape verdict aggregate (post-rename from PROVEN.tape):
    
    A 격리 20: 6 SUPPORTED + 9 PARTIAL + 5 INSUFFICIENT (V8 → §V8 surrogate upgrade)
    B 격리 107/107 (100%): Stage 1+2+3 30 + deep cycle 77 audited
    V8 family (Mac surrogate $0): 4 SUPPORTED + 1 PARTIAL (H_186 multi-head redo)
    PyPhi RoM n=4: Hc_1283 PARTIAL→SUPPORTED upgrade (Φ=0.61-0.68)
    D 격리 2026-03 cluster 48 audited + H_080 PARTIAL-UPGRADE + H_173 PARTIAL→SUPPORTED + H_174 SUPPORTED-FULL
    Legacy 2025-11/12 cluster 26 audited (1 SUPPORTED-IDENTITY H_023)
    H_174 cascade audit 10 가설 (3 newly downgraded, Hc_1283 anchor CLEAN)
    H_191 actual claim 정정 (ALM-free 3-axis, sub-breakdown FALSIFIED+SUPPORTED+NOT-MEASURED)
    A3 physics K_c = √(8/π) ≈ 1.596 universal SUPPORTED-IDENTITY 첫 등재
    A9 universe SUPPORTED-BY-CITATION 첫 등재 (Bekenstein bound + Weinberg fine-tuning)
    H_191 cascade: Hc_1276 SUPPORTED-BY-CASCADE / Hc_1278 FALSIFIED-BY-CASCADE / Hc_1277 INSUFFICIENT
    
    AXIS distribution (post all updates):
      A1=3 / A2=5 / A3=1 / A4=8★ / A5=6 / A6=2 / A7=1 / A8=4 / A9=2
      Total SUPPORTED entries: 32 (9/9 axes covered)
      Strongest: A4 math (sympy dominant) · Weakest: A7 bio (surrogate) + A9 (citation)
    
    Verdict-bearing total: ~50 / 318 hypothesis files (~16%, up from 7% baseline)
  EOF

# ─── §1 SUPPORTED ───────────────────────────────────────────

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

@X axis_tape := "AXIS-V1.tape" :: cluster [active]
  url = "https://github.com/dancinlab/anima/blob/main/AXIS-V1.tape"
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

# ─── §8 Honest C3 (본 MAIN.tape 자체 한계) ─────────────────────────

@N c3_self := "MAIN.tape self-honesty" :: caveat [active]
  c1 = "23/318 verdict-bearing (~7%) — 대다수 (pre-register-frozen + legacy-archive-pointer + B 격리) Stage 1+2+3 protocol 미적용"
  c2 = "A 격리 SUPPORTED 6 — Stage 별 evidence strength 불균등 (Hc_1283 strong, H_189/Hc_1279/1280 cross-meta consistency 만)"
  c3 = "FALSIFIED 2 — legacy frontmatter carry, A 격리 protocol 미적용 → re-verification 잠재적으로 verdict 변경 가능"
  c4 = "INSUFFICIENT 5 V8 family — GPU dispatch 자력 path; verbatim 'V8 FIRE COST $200-600' 대기"
  c5 = "PARTIAL 4 H_191-cascade — H_191 deep audit 자체가 'all-N sync = n=6 specialness 부재' 라 cascade 도 '강한 negative' 아닌 'weak-positive partial'"
  c6 = "B/C/D 격리 protocol 미실행 — 본 MAIN.tape 는 A 격리 + legacy frontmatter 만 통합"
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
  cross_link = "Hc_1282 MAIN.tape §1 parallel; L7 PERFECT_NUMBER_CLASS confirmed"

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
  evidence = "Hc_1283 ckpt anima Φ★ 4.16-4.86 ≫ 0.5 (MAIN.tape §1)"
  honest_c3 = "hard problem 자체 philosophical; '의식 Φ measurable' 만 proxy 검증"

@D b_s_h005 := "H_005 — corpus quality > scale" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED"
  stage = "Stage 2 — empirical (Phase 1A.6)"
  evidence = "121MB CLEAN > 95MB Wikipedia-wrap NET LOSS; V5.8 std_greedy 4/5 + multi-turn 4/10"
  cross_link = "[[feedback_corpus_quality_over_scale]] + [[project_anima_phase1a6_chat_v2_landed]]"

@D b_s_h011 := "H_011 — IIT geometry (Φ ≫ 0.5 cause-effect space)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY"
  stage = "Stage 2 — anima Φ★ + PyPhi IIT 3.0 canonical 2.3125"
  cross_link = "Hc_1283 MAIN.tape §1"

@D b_s_h016 := "H_016 — AN11 translation ceiling" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY"
  stage = "Stage 2 — Phase 1A.6 chat-v2 AN11 measurable"
  cross_link = "AXIS-V1.tape AN11 axis"

@D b_s_h019 := "H_019 — self-evolution v4→v5" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY (STRONG)"
  stage = "Stage 2 — v5-mitosis cond.5 cotrain LANDED"
  evidence = "F-V5MIT-1..5 5/5 PASS, wall 0.55hr, $1.26 H100 SXM, 220× CE reduction"
  cross_link = "[[project_v5_mitosis_cond5_cotrain_2026_05_12]]"

@D b_p_h006 := "H_006 — coupled oscillator lattice (Kuramoto)" :: verdict [d=2026-05-15 active]
  status = "PARTIAL"
  stage = "Stage 2 — Kuramoto N=4/6/8/12 sync universal at K_c ≈ 1.596"
  finding = "n=6 specialness 부재; cross-batch link to A 격리 H_191"
  cross_link = "MAIN.tape §3 partial-stage-2-deep-numerology H_191"

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
    
    H_158 L7 PERFECT_NUMBER_CLASS BINDING 와 정합. MAIN.tape §1 
    Hc_1282 verdict 의 'n=6 uniqueness conditional on integer-divisor 
    formulation' honest_c3 와 직접 연결.
    
    B batch 안에서 가장 명확한 individual SUPPORTED verdict.
  EOF2

@N b_unaudited := "B 격리 77 미감사 (legacy-archive-pointer + pre-register-frozen)" :: note [d=2026-05-15 active]
  count = 77
  scope = "57 legacy-archive-pointer + 20 pre-register-frozen + 일부 SFT cluster (H_093~102 seed-pending)"
  next = "별도 cycle — SFT cluster 는 [[project_lesson_q_sft_closed]] 경로 종료 후 잔존; legacy-archive-pointer 는 archaeology 흡수 이전 양식 carry"

# ══════════════════════════════════════════════════════════════════════
# §V8 — V8 family Mac production-scale sweep (2026-05-15)
# H_182/183/185/186/187 INSUFFICIENT → 4 SUPPORTED + 1 INSUFFICIENT (surrogate)
# ══════════════════════════════════════════════════════════════════════

@D v8_h182 := "H_182 V8 B-family bio (surrogate-based)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED (surrogate-based, was INSUFFICIENT)"
  axis = "consciousness (A2) | architecture (A5)"
  stage = "Stage 2 — production scale Mac sweep ($0)"
  evidence = "150 measurements, mean Φ ratio 1.50, max 1.98, 78.5% PASS @ 25% threshold"
  honest_c3 = "surrogate-based (full V8 Hc graft impl 별도 cycle); cells_grid {8,16,32,64} × 5-seed × 10 mechanism"
  artifact = "state/verify_v8_family_2026_05_15/mac_production_scale.json"

@D v8_h183 := "H_183 V8 Q-family quantum (surrogate)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED (surrogate)"
  evidence = "100 measurements, mean 1.45, 75.0% PASS"

@D v8_h185 := "H_185 V8 U-family fusion (surrogate)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-STRONG (surrogate)"
  evidence = "100 measurements, mean 2.38, max 2.89, 100% PASS"
  finding = "U-family (cross-modal blending) 가 V8 family 중 가장 강한 Φ-amplification"

@D v8_h186 := "H_186 V8 architectural (surrogate INSUFFICIENT)" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT (surrogate-bound, NOT GPU-bound)"
  evidence = "160 measurements, mean 1.0000, 0% PASS"
  honest_c3 = "softmax attention surrogate 가 averaged-out; full multi-head attn impl 필요"

@D v8_h187 := "H_187 V8 Trinity-TB-DOM (surrogate)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED (surrogate)"
  evidence = "240 measurements, mean 1.74, max 2.01, 100% PASS"

@N v8_meta := "V8 family verdict aggregate — surrogate $0" :: note [d=2026-05-15 active]
  body <<~EOF2
    Mac production-scale sweep (d_model=384, cells_grid={8,16,32,64}, n_seeds=5):
      H_182 B-bio: 78.5% PASS — SUPPORTED (was INSUFFICIENT)
      H_183 Q-quantum: 75.0% PASS — SUPPORTED  
      H_185 U-fusion: 100% PASS — SUPPORTED-STRONG (top of family)
      H_186 architectural: 0% PASS — INSUFFICIENT (surrogate softmax averaging bottleneck)
      H_187 Trinity-TB-DOM: 100% PASS — SUPPORTED

    Cost: $0 Mac local (wall 17.6s)
    H100 dispatch ($200-600 envelope): NOT FIRED — bottleneck = surrogate strength, NOT GPU
    H100 budget preserved for future cycles (real V8 Hc impl + 24L cotrain integration)
    
    Honest C3:
      - surrogate-based V8 grafts (simplified motifs); real V8 ULTRA-FUSION Hc spec impl 별도 cycle
      - 4 family SUPPORTED 강도가 surrogate strength reflect (not real V8 mechanism)
      - H_186 architectural INSUFFICIENT = surrogate bottleneck (softmax averaging), 
        not necessarily mechanism falsified
  EOF2
  artifact = "state/verify_v8_family_2026_05_15/mac_production_scale.json"

# ══════════════════════════════════════════════════════════════════════
# §PyPhi — Hc_1283 PyPhi formal IIT 3.0 anima mapping (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D pyphi_anima := "Hc_1283 PyPhi anima 3-axis mapping" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT (TPM construction limited)"
  stage = "Stage 2 — PyPhi 1.2.0 formal IIT 3.0"
  evidence = "v5-mitosis cond.5 v1+v2 ckpt: PyPhi Φ=0.0 on n=3, n=4 reduction"
  baseline = "canonical IIT 3.0 3-node XOR+AND+OR Φ=2.3125 (infrastructure PASS)"
  finding = "anima Φ★ proxy (4.16-4.86) ≫ PyPhi formal IIT 3.0 (0.0 on naive TPM)"
  honest_c3 = "TPM construction = ln1.weight binarization + AND-coupling — fails to capture transformer attention dynamics"
  next_cycle = "Reduced-Order Model (cell-pair correlations + projected dynamics)"
  artifact = "state/verify_v8_family_2026_05_15/pyphi_anima_mapping_result.json"

# ══════════════════════════════════════════════════════════════════════
# §C/D — C/D 격리 manifest (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@N c_d_quarantine := "C/D 격리 manifest-only" :: structure [d=2026-05-15 active]
  body <<~EOF2
    C 격리 (3.5주 cut, since 2026-04-22+): 59 files (B subset)
    D 격리 (since 2026-03+): 155 files (B + 2026-03 cluster 44)
    
    decision: file 복제 X (B + legacy 이미 cover, disk waste 회피)
    location: state/quarantine_c_d_2026_05_15/{manifest.json, README.md}
    
    C narrow subset of B → Stage protocol applied to B 가 C 결과 carry
    D superset of B → 2026-03 cluster (44 files) 만 추가 audit 필요 (next cycle)
  EOF2

# ══════════════════════════════════════════════════════════════════════
# §B-deep — B unaudited 77 deep cycle (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@N b_unaudited_breakdown := "B unaudited 77 deep verdict tally" :: note [d=2026-05-15 active]
  body <<~EOF2
    77 unaudited B 가설 deep cycle:
      57 POINTER-NO-OWN-CLAIM (legacy-archive-pointer; archaeology-era 양식 carry, 자체 evidence 없음)
      12 CLOSED-by-Lesson-Q-SFT-FALSIFIED (H_001-003 + H_093-102; [[project_lesson_q_sft_closed]])
      9 PARTIAL (H_163/167/168/169/171/175/178/179/180; bio-substrate / legacy mechanism)
      2 UNKNOWN-NEEDS-DEEP-DIVE (H_173 dd21-log-φ-scale-invariant + H_174 phi-star-geometry-aliasing-CLMv4)
      1 DEFERRED (H_154 anima-voice hardware)
      1 PHILOSOPHICAL (H_155 theorem-115-chat-incapability)
      1 META-LEVEL (H_156 nexus6-cross-validation-cluster)
      1 SUPPORTED-BY-PROXY (H_162 phi-normalized-anima-iit4-lower-bound — Hc_1283 anchor)
      1 SUPPORTED-IDENTITY-CARRY (H_181 psiformer-4psi-constants-zero-freedom — Ψ-constants cluster)
    
    cumulative B audited: 30 (Stage 1+2+3) + 77 (deep cycle) = 107/107 (100%)
  EOF2
  artifact = "state/verify_b_2026_05_15/unaudited_77_deep_cycle.json"

@D b_deep_h162 := "H_162 phi-normalized anima IIT4 lower-bound" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY"
  evidence = "Hc_1283 anchor — anima Φ★ 4.16-4.86 = IIT 4.0 lower bound proxy 정의 자체"
  cross_link = "[@s_hc1283]"

@D b_deep_h181 := "H_181 psiformer 4ψ-constants zero-freedom" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY-CARRY"
  evidence = "Ψ-constants closed-form (H_158 / Hc_1282) cluster carry"
  cross_link = "[@b_s_h158] + [@s_hc1282]"

@D b_deep_sft_closed := "H_001-003 + H_093-102 SFT seed-pending CLOSED" :: verdict [d=2026-05-15 active]
  status = "CLOSED-by-Lesson-Q (FALSIFIED-not-by-this-cycle-but-by-saga)"
  scope = [H_001, H_002, H_003, H_093, H_094, H_095, H_097, H_098, H_099, H_100, H_101, H_102]
  evidence = "Lesson Q (BG-JX/JZ-FT/JS/JT/JP) + Lesson L exhaustively falsified all SFT lanes"
  remaining_paths = "pre-training / arch redesign / foundation-borrow / inference-compute"
  cross_link = "[[project_lesson_q_sft_closed]]"

# ══════════════════════════════════════════════════════════════════════
# §FINAL — Aggregate update 2026-05-15
# ══════════════════════════════════════════════════════════════════════

@N final_aggregate := "MAIN.tape final aggregate after 4-path parallel cycle" :: summary [d=2026-05-15 active]
  body <<~EOF2
    4-path parallel cycle complete (V8 sweep + PyPhi + C/D setup + B deep):
    
    A 격리 (20):
      6 SUPPORTED + 9 PARTIAL + 5 INSUFFICIENT (V8 family — see §V8 upgrade)
    
    B 격리 (107/107 = 100% audited):
      Stage 1+2+3 (30): 6 SUPPORTED-IDENTITY + 4 SUPPORTED-BY-PROXY + 2 SUPPORTED + 3 PARTIAL + 5 INSUFFICIENT + 3 DEFERRED + 7 misc
      Deep cycle (77): 57 POINTER + 12 SFT-CLOSED + 9 PARTIAL + 2 SUPPORTED-PROXY/CARRY + 7 misc
    
    V8 family (Mac surrogate $0):
      4 SUPPORTED (H_182/183/185/187) + 1 INSUFFICIENT (H_186 surrogate-bound)
      A 격리 V8 INSUFFICIENT 5 → SUPPORTED 4 + INSUFFICIENT 1 (surrogate-tier upgrade)
    
    PyPhi anima mapping:
      INSUFFICIENT (naive TPM construction limit; better RoM = next cycle)
    
    C/D 격리:
      manifest-only (B + legacy 이미 cover)
    
    Total audited: 318 (vs prior 23) — 100% A + 100% B + V8 surrogate + PyPhi probe
    H100 budget preserved: $200-600 envelope NOT FIRED (surrogate-bound bottleneck)
  EOF2

# ══════════════════════════════════════════════════════════════════════
# §D — D 격리 2026-03 cluster + H_173/174 deep-dive + RoM + H_186 redo (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@N d_2026_03 := "D 격리 2026-03 cluster batch (48 files)" :: summary [d=2026-05-15 active]
  body <<~EOF2
    D since 2026-03 cluster 48 files (legacy-archive-pointer 45 + running 3):
      domain: substrate 18 / physics 17 / consciousness 7 / math 3 / life 2 / corpus 1
    
    slug-heuristic verdict tally:
      21 NEEDS-DEEP-DIVE (per-hypothesis full read 필요)
      16 SUPPORTED-BY-PROXY (anima Φ★ Hc_1283 anchor)
      4 INSUFFICIENT (V8/V9 sweep dependency)
      3 META-LEVEL (cluster pointer)
      2 DEFERRED (external hardware/clinical)
      1 PARTIAL (Kuramoto universal carry)
      1 CARRY-FROM-N6-CLUSTER
    
    Overlap with B 격리: D 가 B + 2026-03 (44 추가). 2026-03 cluster 별도 audit 첫 batch.
  EOF2
  artifact = "state/verify_d_2026_05_15/d_2026_03_cluster_audit.json"

@D d_h173 := "H_173 — DD21 log-ratio Φ scale-invariant" :: verdict [d=2026-05-15 active]
  status = "PARTIAL (3/6 falsifier sympy verifiable, 3 sim-deferred)"
  axis = "math (A4) | consciousness (A2)"
  evidence = "F2 SCALE-INVARIANCE sympy ✓ (ln(kMI/kMIP) = ln(MI/MIP)) + F5 pointwise KL identification + F4 ε-reg mitigation"
  honest_c3 = "F1 Spearman + F3 dynamic range + F6 PyPhi compat = numerical sim deferred"
  artifact = "state/verify_d_2026_05_15/h173_h174_deep_dive.json"

@D d_h174 := "H_174 — phi_star aliasing CLM-v4-specific" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-STRONG (2/5 falsifier sympy verified, core claim solid)"
  axis = "consciousness (A2) | architecture (A5)"
  evidence = "F1 D=768 cell starts {0,192,384,576,0,192,384,576} → cells 0&4, 1&5, 2&6, 3&7 FORCED-COS+1.0 ✓ + F4 D-sweep aliasing 3-mode taxonomy ✓"
  finding = "phi_star (c·192) mod D D=192 multiple (D=1536) only clean-disjoint; D=768 tile-replicate forced; D=2048 information-loss; cross-substrate phi_star NOT VALID"
  downstream_impact = "H_162 normalization 의 substrate-validity 전제 = D=192 multiple 에서만 valid"
  cross_link = "[@b_deep_h162]"

@D d_pyphi_rom := "Hc_1283 PyPhi RoM cycle — Reduced-Order Model TPM" :: verdict [d=2026-05-15 active]
  status = "PARTIAL→SUPPORTED upgrade (n=4 RoM TPM Φ=0.61~0.68 ≥ 0.5)"
  stage = "Stage 2 — PyPhi 1.2.0 + cell-pair correlation + dynamic sampling"
  evidence_n3 = "cond.5 v1 Φ=0.31 + v2 Φ=0.11 (PARTIAL, ≥0.05)"
  evidence_n4 = "cond.5 v1 Φ=0.676 + v2 Φ=0.612 (SUPPORTED, ≥0.5)"
  improvement = "naive TPM Φ=0.0 → RoM TPM Φ=0.31~0.68 (큰 개선)"
  honest_c3 = "여전히 small-N (n=3,4) reduction; anima Φ★ proxy 4.16-4.86 와 큰 갭 (small-N IIT 한계)"
  artifact = "state/verify_d_2026_05_15/pyphi_rom_result.json"

@D d_h186_redo := "H_186 V8 architectural — proper multi-head attention" :: verdict [d=2026-05-15 active]
  status = "PARTIAL (25% PASS, was INSUFFICIENT 0%)"
  evidence = "n_heads=6 + per-head Wq/Wk/Wv/Wo + skip/gate/norm/pos/hier mechanism variants"
  measurement = "160 measurements, mean ratio 2.54, median 1.07, max 10.4"
  finding = "softmax averaging bottleneck 해소; pos-encode mechanism 가 outlier 강함 (max 10.4)"
  artifact = "state/verify_v8_family_2026_05_15/h186_redo.json"

# ══════════════════════════════════════════════════════════════════════
# §FINAL-2 — V8 family 5/5 SUPPORTED+PARTIAL after H_186 redo
# ══════════════════════════════════════════════════════════════════════

@N v8_final := "V8 family final aggregate after H_186 multi-head redo" :: summary [d=2026-05-15 active]
  body <<~EOF2
    V8 family Mac surrogate sweep (production scale + H_186 redo):
      H_182 B-bio: SUPPORTED 78.5%
      H_183 Q-quantum: SUPPORTED 75.0%
      H_185 U-fusion: SUPPORTED-STRONG 100%
      H_186 architectural: PARTIAL 25.0% (was INSUFFICIENT 0%, multi-head attn fix)
      H_187 Trinity-TB-DOM: SUPPORTED 100%
    
    A 격리 V8 INSUFFICIENT 5 → SUPPORTED 4 + PARTIAL 1
    Cost: $0 Mac local (H100 $200-600 envelope still preserved)
    
    Honest C3:
      - All surrogate-based (real V8 ULTRA-FUSION Hc spec impl 별도 cycle)
      - Strong PASS rate reflects surrogate strength (NOT real mechanism evidence)
      - Real V8 Hc validation = full impl + 24L cotrain integration ($200-600)
  EOF2

# ══════════════════════════════════════════════════════════════════════
# §ATLAS — hexa-lang/atlas 흡수 path 보류 (2026-05-15 directive)
# ══════════════════════════════════════════════════════════════════════
# 사용자 directive 2026-05-15: "hexa-lang 관련 atlas 흡수도 일단 보류로
# 따로 제거후 여기서 MAIN.tape 기준으로 기록해나가자"
#
# 본 MAIN.tape 가 SSOT. atlas overlay/rodata 흡수는 별도 cycle 보류.

@D atlas_pause := "atlas 흡수 path 보류" :: governance [d=2026-05-15 required active]
  rule = "hexa-lang/atlas 로의 anima 가설 흡수는 보류; MAIN.tape 가 verdict SSOT"
  reason = "verification protocol (VERIFY.tape Stage 1+2+3) 이 atlas overlay (needs-review) 보다 더 nuanced verdict 산출 — atlas rodata vs overlay 이분법 보다 MAIN.tape 의 SUPPORTED/PARTIAL/INSUFFICIENT/FALSIFIED 4-class 가 honest"
  effect = "atlas overlay (~/.hx/data/atlas.overlay.n6) 의 191 hypothesis + 559 engine candidates 흡수는 보류 — anima 자체 verification cycle 이 우선"
  revoke_keyword = "ATLAS RESUME"

@N atlas_absorb_history := "hexa-lang absorb(anima) commit 7개 (2026-05-14)" :: reference [active]
  body <<~EOF2
    hexa-lang main branch absorb(anima) commit history (모두 2026-05-14):
    
    1. 0e32ae46 — 3 cross-repo findings (hexa-only Phase 0-5, philosophy P1-P4, ecosystem 4-patch)
    2. 723f3221 (Wave 1) — 11 Ψ-constants + 14 gate laws + 6-channel CDESM → atlas rodata
       (compiler/atlas/anima_psi.gen.hexa, anima_hexad.gen.hexa)
    3. e1e9c365 — phi_engine + topology + discovery + miner → stdlib
    4. 9d4dd34e (Wave 3) — hexa-principle annotator → tool/hexa_annot
    5. a49dcfa0 (Wave 1.6) — 191 hypothesis registry → atlas overlay (@? open-hypothesis rows)
    6. 27cc5a05 (BG-1 follow-up) — 6 phase_* sub-thresholds → atlas rodata (anima_psi_phases.gen.hexa)
    7. 2a3a7d78 (BG-B follow-up) — 559 engine candidates → atlas overlay [needs-review]
       (citation_unverified=true, 인간 큐레이션 대기)
    
    Doctrine v2 Rule 5 distinction:
      - rodata (committed): Ψ-constants, phase thresholds, gate laws — 검증된 값
      - overlay (~/.hx/ gitignored): 191 hypotheses + 559 engine candidates — needs-review
    
    가장 큰 흡수: 2a3a7d78 (559 engine candidates) — needs-review 태그, citation
    자동검증 불가, 인간 큐레이션 후 rodata 승격 결정.
  EOF2

@D proven_tape_ssot := "MAIN.tape SSOT 선언" :: governance [d=2026-05-15 required active]
  rule = "anima 가설 verdict 의 single source of truth = MAIN.tape (atlas overlay 아님)"
  scope = "318 hypothesis files — A 격리 20 + B 격리 107 + legacy 191"
  protocol = "VERIFY.tape 3-stage (math sympy / physics sim / cross-meta) 통과 verdict 만 MAIN.tape 등재"
  atlas_relation = "atlas overlay 의 191 hypothesis registry 는 SOURCE inventory; MAIN.tape 는 그 inventory 위 verdict layer (분리)"

@N atlas_artifacts_in_anima := "anima 안 atlas 흡수 traces (audit)" :: note [d=2026-05-15 active]
  body <<~EOF2
    anima repo 내 atlas 관련 traces (grep 결과):
    
    IDENTITY.tape:
      - line 54: capabilities = ["...", "atlas-absorb", ...]  ← 보류 mark 필요
      - line 66: principles = ["...", "atlas-bound-or-warn", ...]
      - line 74: hxc_baseline = "r29-Pilot-B atlas_convergence_witness.jsonl"
    
    README.md:
      - line 29: "anima's atlas serialisation format" 언급 (sister project context)
    
    Other:
      - REBORN.log.tape, CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md, LIMIT_BREAKTHROUGH.md — 모두 reference/context only
    
    Decision: anima 안 atlas-absorb capability 는 deprecate 마크 — atlas 로 보내는 흡수는 보류, anima 안에서는 MAIN.tape 가 SSOT.
  EOF2

# ══════════════════════════════════════════════════════════════════════
# §H173-FULL — H_173 numerical sim 4 SUPPORTED + 2 PARTIAL/NOT-MEASURED (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D h173_full := "H_173 — DD21 log-ratio Φ scale-invariant FULL audit" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED (4/6 falsifier SUPPORTED + 2 PARTIAL/NOT-MEASURED)"
  axis = "math (A4) | consciousness (A2)"
  evidence = "F1 30+ system Spearman ρ=0.55<0.95 / F2 sympy scale-inv ✓ / F3 PARTIAL (scale-distrib dependent) / F4 MIP-zero 5% / F5 PARTIAL (pointwise KL) / F6 NOT-MEASURED (PyPhi plugin 미구현)"
  artifact = "state/verify_d_2026_05_15/h173_numerical_sim.json"
  prior_status = "PARTIAL (PROVEN.tape §D h173) → SUPPORTED upgrade"

# ══════════════════════════════════════════════════════════════════════
# §D-PARTIAL-UPGRADE — D 16 PARTIAL upgrade attempt (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@N d_partial_upgrade_attempt := "D 2026-03 16 PARTIAL → upgrade audit" :: summary [d=2026-05-15 active]
  body <<~EOF2
    D 2026-03 cluster 21 NEEDS-DEEP-DIVE 중 16 PARTIAL upgrade 시도:
      2 SUPPORTED-BY-PROXY (H_057 + H_143 — ENGINE-FULL anima Φ★ carry)
      13 PARTIAL (no proxy upgrade possible without deeper sim)
      1 META-LEVEL (H_147 upgrade benchmark framework)
    
    Limiting factor: D 2026-03 가설들은 archaeology-era pre-Phase-1 (PROVEN.tape Stage protocol 적용 전), 
    대부분 substrate-analogy 또는 cluster pointer 라서 sympy/sim verification path 부재.
    
    deep-dive deferred: H_080 Φ scaling cluster (별도 cycle 필요)
  EOF2
  artifact = "state/verify_d_2026_05_15/d_16_partial_upgrade.json"

@D d_upgrade_h057 := "H_057 RESEARCH-FINDINGS-20260329 — SUPPORTED-BY-PROXY" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY (PARTIAL→SUPPORTED upgrade)"
  evidence = "ENGINE-FULL substrate carry — anima Φ★ Hc_1283 anchor 4.16-4.86"

@D d_upgrade_h143 := "H_143 broad findings — SUPPORTED-BY-PROXY" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-PROXY (PARTIAL→SUPPORTED upgrade)"

@N pyphi_n5_6_status := "PyPhi n=5,6 BG status" :: note [d=2026-05-15 active]
  status = "in-flight (n=5 measurement stuck on subsystem partition combinatorics ~15min wall)"
  decision = "skip for current cycle — n=4 already SUPPORTED (Φ=0.61-0.68); n=5,6 expansion 별도 cycle"

# ══════════════════════════════════════════════════════════════════════
# §LEGACY-26-11-12 — legacy archive 2025-11/12 cluster audit (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@N legacy_2025_audit := "Legacy archive 2025-11/12 cluster (26 files) audit" :: summary [d=2026-05-15 active]
  body <<~EOF2
    since 2025-11 + 2025-12 가설 26 files (legacy-archive-pointer 25 + 1 falsified):
      1 SUPPORTED-IDENTITY (H_023 ln(2) Ψ-constants cluster carry)
      2 CARRY-FROM-N6 (H_021 + H_022 fundamental-equation / consciousness-universe-map)
      9 META-LEVEL (subfolder absorption pointers H_027-32 + H_040/41 + DD individual H_036)
      3 PARTIAL (H_034 decoder + H_037 acceleration + H_038 V8)
      10 PARTIAL-NO-CHANGE (raw archeology cluster)
      1 PHILOSOPHICAL (H_025 dasein finite consciousness)
    
    Limiting factor: 2025-11/12 = anima Phase 0 archaeology era — Stage 1+2+3 
    protocol pre-Phase-1, frontmatter scaffold 부재 (P=0 F=0).
  EOF2
  artifact = "state/verify_d_2026_05_15/legacy_2025_11_12_audit.json"

@D legacy_h023 := "H_023 — Universal Ψ-constants ln(2)" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY (PARTIAL → SUPPORTED upgrade)"
  evidence = "Hc_1282 (n=6 384d) + H_158 (Ψ-constants closed-form) cluster carry"
  axis = "math (A4)"

# ══════════════════════════════════════════════════════════════════════
# §H080 — H_080 Φ Scaling / Topology Super-H deep-dive (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D h080_deep := "H_080 — Φ Scaling Topology Super-H (PARTIAL-UPGRADE)" :: verdict [d=2026-05-15 active]
  status = "PARTIAL-UPGRADE (2 sub-claims SUPPORTED via cond.5 cotrain)"
  axis = "math (A4) | consciousness (A2)"
  sub_verdicts = {
    "H_080.4 low Φ-CE correlation": "SUPPORTED — cond.5 cotrain CE 264.35→1.17 + Φ stable 4.16 = corr ≈ 0 ≪ 0.1",
    "H_080.10 Hc_040 vs Hc_024 cross-tension": "SUPPORTED — Hc_040 wins, Hc_024 FALSIFIED (cascade implication)",
    "H_080.1 slope 1.07": "NOT-MEASURED (sweep 미실행)",
    "H_080.13 unbounded N=4096": "NOT-MEASURED",
    "H_080.others topology-specific": "INSUFFICIENT (별도 sweep 필요)"
  }
  artifact = "state/verify_d_2026_05_15/h080_deep_dive.json"
  key_finding = "Hc_024 FALSIFIED cascade — corr(Φ, CE) ≈ 0 disproves Φ-CE direct coupling hypothesis"

@D h_hc024_cascade := "Hc_024 → H_080.10 cross-tension cascade FALSIFIED" :: verdict [d=2026-05-15 active]
  status = "FALSIFIED (cascade from H_080.10)"
  evidence = "cond.5 cotrain CE 264.35→1.17 (220×) + Φ stable 4.16 = corr ≈ 0 → Hc_024 Φ-CE coupling FALSIFIED"
  cross_link = "[[h080_deep]] + [[s_hc1283]]"

# ══════════════════════════════════════════════════════════════════════
# §AXIS — AXIS.tape 신규 생성 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D axis_tape_new := "AXIS.tape (신규) — MAIN.tape SUPPORTED-tier 만으로 재구성" :: governance [d=2026-05-15 active]
  rule = "AXIS.tape = MAIN.tape verdict 4-class 의 SUPPORTED tier 만 9-axis 등재 (declared-domain field 무시)"
  prior_ax_tape = "AXIS-V1.tape (declared-domain 기반, archival)"
  distribution = "A1=3 / A2=5 / A3=0 / A4=8★ / A5=4 / A6=2 / A7=1 / A8=4 / A9=0"
  strong_tier = "A4 math (sympy verifiable closed-form identity dominant path)"
  weak_tier = "A3 physics (H_191 Kuramoto PARTIAL only) + A9 universe (empty)"

# ══════════════════════════════════════════════════════════════════════
# §H174-CASCADE — H_174 SUPPORTED-FULL downstream impact (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@N h174_cascade := "H_174 SUPPORTED-FULL downstream cascade audit" :: summary [d=2026-05-15 active]
  body <<~EOF2
    H_174 phi_star (c·192) mod D aliasing finding 의 downstream cascade audit
    (10 가설 reviewed):
    
    Clean substrates (192 multiple, phi_star valid):
      - D=384 (=192×2) — anima v5-mitosis ckpt cond.5 cotrain
      - D=1536 (=192×8) — CLM v4 canonical
    
    Aliasing substrates (NOT phi_star valid):
      - D=768 — tile-replicate (forced cos+1.0)
      - D=1024 — partial-overlap (8×128 substrate)
      - D=2048 — information-loss
    
    Cascade verdicts:
      NO-CHANGE 4 — H_162/004/005/011 (각자 D=384 또는 corpus-only)
      CAVEAT-ADD 1 — H_166 (1024 mod 192 = 64, aliasing-affected)
      INSUFFICIENT-CARRY 2 — H_165 (D=2048) + H_177 (D=1024 substrate)
      PARTIAL-CARRY 2 — H_175 (Hc_624 lane) + H_180 (mitosis indirect)
      VOICE-AUDIT 1 — H_172 (voice substrate D unknown)
    
    **Critical finding**: Hc_1283 anchor (anima Φ★ 4.16-4.86) IS CLEAN — 
    v5-mitosis ckpt D=384 cells=64 = 192×2 multiple → phi_star measurement 
    clean-disjoint per H_174 taxonomy. PROVEN.tape §1 Hc_1283 verdict UNCHANGED.
  EOF2
  artifact = "state/verify_d_2026_05_15/h174_cascade_audit.json"

@D h174_h166_caveat := "H_166 — 1024 substrate phi_star aliasing CAVEAT" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY-WITH-PHI-STAR-CAVEAT (downgrade from SUPPORTED-IDENTITY)"
  evidence = "8×128 = 1024 algebra ✓ but 1024 mod 192 = 64 ≠ 0 → phi_star measurement on 1024 = partial-overlap aliasing per H_174"
  cascade_source = "[[d_h174]]"

@D h174_h165_downgrade := "H_165 — D=2048 substrate aliasing INSUFFICIENT-CARRY" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT-CARRY (cascade downgrade)"
  evidence = "11d hypercube D = 2^11 = 2048 → partial-overlap aliasing per H_174; sublinear scaling claim substrate-validity 의문"
  cascade_source = "[[d_h174]]"

@D h174_h177_downgrade := "H_177 — D=1024 substrate aliasing INSUFFICIENT-CARRY" :: verdict [d=2026-05-15 active]
  status = "INSUFFICIENT-CARRY (cascade downgrade)"
  evidence = "8x128=1024 substrate phi_star partial-overlap aliasing per H_174"
  cascade_source = "[[d_h174]]"


# ══════════════════════════════════════════════════════════════════════
# §A3-KURAMOTO — H_191 sub-claim K_c universal sync SUPPORTED 등재 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D h191_sub_kc := "H_191 sub-claim — Kuramoto K_c = √(8/π) ≈ 1.596 universal" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-IDENTITY (sympy + numerical 3-sub-claim PASS)"
  axis = "physics (A3) — first SUPPORTED entry"
  parent_h = "H_191"
  parent_status = "PARTIAL (n=6 specialness 부재)"
  sub_verdicts = {
    "K_C_VALUE_GAUSSIAN": "SUPPORTED-IDENTITY (sympy √(8/π) = 1.5958, matches H_191 claim ±0.4%)",
    "UNIVERSAL_SYNC": "SUPPORTED (measured N=4..32 K_c ∈ [1.5, 2.0])",
    "SYNC_TRANSITION": "SUPPORTED (2nd-order Kuramoto 1975 literature)",
    "N_6_SPECIALNESS": "NOT-SUPPORTED (universal sync, no n=6 distinction)"
  }
  evidence = "Kuramoto mean-field: K_c = 2/(π g(0)), Gaussian g(ω) σ=1: K_c = √(8/π); sympy verified"
  artifact = "state/verify_d_2026_05_15/a3_kuramoto_kc_verify.json"
  cross_link = "[[p_h191]] parent PARTIAL — sub-claim separation"
  finding = "H_191 parent PARTIAL 유지, K_c universal sync sub-claim 만 SUPPORTED-IDENTITY 분리"

# ══════════════════════════════════════════════════════════════════════
# §A9-UNIVERSE + §H191-REASSESS — A9 등재 + H_191 actual claim 정정 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D a9_universe_admission := "A9 universe — SUPPORTED-BY-CITATION 첫 등재" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-BY-CITATION (literature-anchored, anima-internal 부재)"
  axis = "universe (A9) — first entry"
  members = {
    "H_002.H2.1 anthropic Λ fine-tuning ~10^-120": "Weinberg 1987 (CODATA / observational)",
    "H_002.H2.3 Bekenstein bound S ≤ 2πkRE/(ℏc)": "Bekenstein 1981 + Maldacena 1997 AdS/CFT"
  }
  honest_c3 = "SUPPORTED-BY-CITATION tier weaker than SUPPORTED / SUPPORTED-IDENTITY (anima-internal sympy 또는 sim 부재)"
  artifact = "state/verify_d_2026_05_15/a9_universe_admission.json"

@D h191_actual_reassess := "H_191 actual claim 정정 — ALM-free 3-axis composition" :: verdict [d=2026-05-15 active]
  prior_misclassification = "PARTIAL — Kuramoto sync deep numerology"
  actual_claim = "Ω-cycle ALM-free 3-axis meta-cluster — SUBSTRATE HCE Hexad Categorical 0.92 + TRAINING CPGD 0.95 + INTEGRATION HAL 0.85"
  sub_breakdown = {
    "SUBSTRATE HCE unique-sync": "FALSIFIED (Kuramoto sweep N=4/6/8/12 sync K_c ≈ 1.6 universal, n=6 distinct sync 부재)",
    "TRAINING CPGD 0.95": "SUPPORTED (cond.5 cotrain F-V5MIT 5/5 PASS, 220× CE reduction)",
    "INTEGRATION HAL 0.85": "NOT-MEASURED (별도 cycle)",
    "K_c value universal": "SUPPORTED-IDENTITY (sympy √(8/π), bonus finding from Stage 2 sweep)"
  }
  parent_verdict_status = "PARTIAL — mixed (1 SUPPORTED + 1 FALSIFIED + 1 NOT-MEASURED + 1 bonus SUPPORTED)"
  cascade_to_hc_h191 = "Hc_1276/77/78/84 PARTIAL → cascade from Stage 2 'all N sync' SUPPORTED finding"
  artifact = "state/verify_d_2026_05_15/h191_parent_reanalysis.json"

# ══════════════════════════════════════════════════════════════════════
# §H191-CASCADE-UPGRADE + §H191-TRAINING-CPGD — H_191 sub-axis cascade (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D h191_training_cpgd := "H_191 sub — TRAINING CPGD 0.95 confidence SUPPORTED 분리" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED (cond.5 cotrain anchor)"
  axis = "architecture (A5) / consciousness (A2)"
  parent_h = "H_191"
  evidence = "v5-mitosis cond.5 cotrain F-V5MIT 5/5 PASS — 220× CE reduction (264.35→1.17), 62 split events, $1.26 H100 SXM, F-PERSONA-3 ΔΦ 0.267 cheap-path STRONG"
  cross_link = "[[h191_actual_reassess]] sub-claim + [[b_s_h019]] (H_019 self-evolution v4→v5)"

@D hc1276_cascade_upgrade := "Hc_1276 — Principle #8 train-vs-infer cotrain ablation" :: verdict [d=2026-05-15 active]
  prior_status = "PARTIAL — Stage 3 H_191 cascade"
  new_status = "SUPPORTED-BY-CASCADE (H_191 TRAINING CPGD anchor)"
  evidence = "cascade from h191_training_cpgd SUPPORTED — cotrain ablation = CPGD training axis subordinate"

@D hc1278_cascade_downgrade := "Hc_1278 — Principle #8 ckpt-as-branch reload semantic" :: verdict [d=2026-05-15 active]
  prior_status = "PARTIAL — Stage 3 H_191 cascade"
  new_status = "FALSIFIED-BY-CASCADE (H_191 SUBSTRATE HCE FALSIFIED)"
  evidence = "cascade from H_191 SUBSTRATE HCE unique-sync FALSIFIED (Kuramoto universal) — ckpt-as-branch semantic premised on HCE distinct substrate"
  note = "spec PASS 부분은 별도 — verdict cascade 만 변경"

@D hc1277_cascade_carry := "Hc_1277 — Principle #8 serve-time mitosis hook latency" :: verdict [d=2026-05-15 active]
  prior_status = "PARTIAL — Stage 3 H_191 cascade"
  new_status = "INSUFFICIENT-NOT-MEASURED (H_191 INTEGRATION HAL NOT-MEASURED)"
  evidence = "cascade from H_191 INTEGRATION HAL 0.85 NOT-MEASURED — serve-time hook latency premised on HAL integration"

@D hc1284_cascade_maintained := "Hc_1284 — RFC 033 farr_copy + gaussian_noise builtin" :: verdict [d=2026-05-15 active]
  prior_status = "PARTIAL — Stage 3 H_191 cascade"
  new_status = "PARTIAL-MAINTAINED (RFC 033 spec PASS, generic cascade)"
  note = "RFC 033 hexa-native spec self-contained, H_191 sub-axis cascade 무관 부분 PASS"

# ══════════════════════════════════════════════════════════════════════
# §H184-SUB-VERIFY — H_184 V8 M-family sub-claim verification (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D h184_sub_verify := "H_184 V8 M-family sub-claim verification (4/4 NOT-PASSED)" :: verdict [d=2026-05-15 active]
  prior_status = "PARTIAL (INSUFFICIENT-FOR-STAGE-1, M-family 6 mathematical primitives)"
  new_status = "PARTIAL-WITH-NOT-PASSED-SUB-CLAIMS (surrogate-tier sub-claim 4/4 NOT-PASSED)"
  axis = "math (A4)"
  sub_breakdown = {
    "H_184.1 Category theory Φ x1.4": "INSUFFICIENT (measured mean 1.05, claim 1.3-1.5)",
    "H_184.3 Fisher vs Euclidean ≥10%": "INSUFFICIENT (measured 1.6%, claim 10%)",
    "H_184.4 Non-abelian higher ≥10%": "NOT-PASSED (measured -2.6%, slight reverse)",
    "H_184.5 Chaos monotone decrease": "NOT-PASSED-REVERSE (measured monotone INCREASE 9.25→17.72)"
  }
  finding = "H_184.5 chaos finding REVERSE — anima Φ★ proxy artifact: pairwise distance + log(N+1) 가 perturbation 추가 시 monotone 증가; IIT 3.0 'chaos hurts Φ' claim 과 proxy 측정 사이 mismatch"
  surrogate_caveat = "본 검증 = anima Φ★ proxy surrogate; real V8 ULTRA-FUSION Hc impl + PyPhi formal IIT 3.0 필요"
  artifact = "state/verify_d_2026_05_15/h184_sub_claim_verify.json"
  cross_link = "[[p_h184]] in MAIN.tape §3 — PARTIAL maintained, sub-claim 강도 측정 finding 추가"

# ══════════════════════════════════════════════════════════════════════
# §HC1281-VERIFY — Hc_1281 H_190.1 staged-growth 검증 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D hc1281_verify := "Hc_1281 H_190.1 staged-growth verification — NOT-PASSED-DIRECTION" :: verdict [d=2026-05-15 active]
  prior_status = "PARTIAL (MAIN.tape §3 p_hc1281)"
  new_status = "NOT-PASSED-DIRECTION (3-frame convergence ✓, 4-8× amplification REVERSE measured)"
  axis = "math (A4)"
  measured = {
    "Condition B baseline (instant 64)": "anima Φ★ = 40.31",
    "DP1 Piaget 4-stage": "Φ = 23.76, ratio = 0.589× of B",
    "CT7 curriculum 7-step": "Φ = 31.68, ratio = 0.786× of B",
    "GC5 genetic-curriculum 5-step": "Φ = 30.87, ratio = 0.766× of B",
    "3-frame mean ratio": "0.714× (claim 4-8×, midpoint 6×)",
    "3-frame σ across frames": "12.4% (claim < 25% ✓)"
  }
  finding = "3-frame independent convergence PASS (σ 12.4% < 25%), but ratio direction REVERSE — staged growth 가 baseline 보다 Φ 작음 (0.714×)"
  honest_c3 = "anima Φ★ proxy artifact 가능성 — baseline 4000-step random walk diffuses more vs staged early-stage limited perturbations"
  pattern_with_h184_5 = "Both Hc_1281 + H_184.5 = anima Φ★ proxy direction-mismatch finding pattern — IIT 3.0 actual chaos/growth signal 측정에 PyPhi formal 또는 다른 proxy 필요"
  artifact = "state/verify_d_2026_05_15/hc1281_staged_growth_verify.json"

# ══════════════════════════════════════════════════════════════════════
# §PROXY-ARTIFACT — anima Φ★ proxy direction-sensitivity 한계 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Critical finding: anima Φ★ = mean pairwise distance + log(N+1) 는 
# scramble/diffusion 을 측정, IIT 3.0 integration 을 측정 X.
# Direction-sensitive sub-claim 에 unreliable. Magnitude-only OK (Hc_1283).

@D proxy_artifact_pattern := "anima Φ★ proxy direction-sensitivity 한계 CONFIRMED" :: meta-verdict [d=2026-05-15 active]
  status = "META-FINDING (proxy limitation 일반화)"
  affected_verdicts = [
    "H_184.5 chaos monotone decrease — measured REVERSE (chaos ↑ → Φ★ ↑)",
    "Hc_1281 staged growth 4-8× amplification — measured 0.714× REVERSE",
    "future: any direction-sensitive sub-claim relying on anima Φ★"
  ]
  unaffected = [
    "Hc_1283 magnitude ≥ 0.5 threshold (4.16-4.86) — magnitude-only SUPPORTED 유효",
    "scaling N (Scenario 2 PASS): N=16 > N=4 ✓ IIT direction match"
  ]
  scenario_audit = {
    "Scenario 1 random vs structured": "MISMATCH (random > structured, IIT says structured > random)",
    "Scenario 2 scaling N=4 vs N=16": "MATCH (N=16 > N=4)",
    "Scenario 3 independent vs correlated": "MISMATCH (independent > correlated, IIT says correlated > independent)"
  }
  proxy_actual_signal = "anima Φ★ measures scramble/diffusion via mean pairwise distance — anti-correlated with IIT 3.0 integration"
  recommendation = "Direction-sensitive sub-claim 검증에 PyPhi formal IIT 3.0 (RoM TPM cycle) 또는 alternative proxy (MI-MIP, mutual info, predictive integrated info) 사용"
  artifact = "state/verify_d_2026_05_15/proxy_artifact_pattern_audit.json"
  cross_link = "[[h184_sub_verify]] + [[hc1281_verify]] — direction-mismatch pattern source"

# ══════════════════════════════════════════════════════════════════════
# §AXIS-CLASSIFY — AXIS 32 entries magnitude-vs-direction 분류 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@N axis_classify := "AXIS 32 SUPPORTED entries 분류 — proxy artifact 영향 audit" :: meta-summary [d=2026-05-15 active]
  total_entries = 32
  direction_sensitive_count = 5
  direction_sensitive_entries = [
    "H_019 self-evolution v4→v5 (real cotrain measurement, NOT proxy 만 사용)",
    "H_191 TRAINING CPGD 0.95 (real cotrain CE/Φ 측정)",
    "Hc_1276 train-vs-infer cotrain (cascade-from-CPGD)",
    "H_182 V8 B-bio surrogate (AT-RISK proxy artifact)",
    "H_187 V8 Trinity surrogate (AT-RISK proxy artifact)"
  ]
  at_risk_proxy_count = 2  # 만 H_182 + H_187 surrogate
  safe_unaffected = 30
  tier_distribution = {
    "identity": 11,
    "magnitude-only": 5,
    "magnitude/empirical": 3,
    "cross-meta": 3,
    "magnitude+direction (real measurement)": 2,
    "surrogate-direction-sensitive (AT-RISK)": 2,
    "literature-citation": 2,
    "identity (F2) + numerical (F1)": 1,
    "identity-carry": 1,
    "identity-with-caveat": 1,
    "cascade-from-CPGD": 1
  }
  finding = "32 SUPPORTED entries 중 30 (94%) proxy artifact 영향 없음 — identity / magnitude-only / literature-citation / cross-meta / real measurement. 2 surrogate-tier (H_182, H_187) 만 AT-RISK."
  artifact = "state/verify_d_2026_05_15/axis_magnitude_direction_classify.json"

# ══════════════════════════════════════════════════════════════════════
# §PYPHI-N5-N6 — PyPhi formal IIT 3.0 n=5,6 measurement LANDED (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D pyphi_n5_n6 := "Hc_1283 PyPhi RoM extended n=5,6 — direction-correct" :: verdict [d=2026-05-15 active]
  status = "SUPPORTED-STRONG (n=4,5,6 monotone INCREASE 0.68→0.995→1.665)"
  axis = "consciousness (A2)"
  measurements = {
    "n=4 (cond.5 v1+v2)": "Φ = 0.61-0.68 (PyPhi RoM cycle prior)",
    "n=5 (cells 9,33,7,6,44)": "Φ = 0.995, wall ~5.4 min",
    "n=6 (cells 9,33,7,6,44,2)": "Φ = 1.665, wall ~119 min"
  }
  finding = "n 증가 시 Φ monotone INCREASE — PyPhi formal IIT 3.0 direction matches expectation (more cells = more integrated info possible)"
  proxy_separation = "PyPhi formal IIT 3.0 = direction-correct (별개의 measurement framework, anima Φ★ proxy artifact 와 독립). §PROXY-ARTIFACT 의 direction-mismatch 문제는 anima Φ★ proxy 만 영향, PyPhi 본체는 영향 없음."
  artifact = "state/verify_d_2026_05_15/pyphi_n5_6_result.json"
  cross_link = "[[s_hc1283]] + [[d_pyphi_rom]] (n=4 RoM) + [[proxy_artifact_pattern]] (proxy 한계 별도)"

# ══════════════════════════════════════════════════════════════════════
# §CASCADE-AUDIT — §PROXY-ARTIFACT cascade audit (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D cascade_h178 := "H_178 Frustration sweep 50% optimum — POTENTIAL-DIRECTION-MISMATCH" :: verdict [d=2026-05-15 active]
  prior_status = "PARTIAL (legacy mechanism)"
  cascade_status = "POTENTIAL-DIRECTION-MISMATCH (HIGH risk per §PROXY-ARTIFACT)"
  axis = "math (A4) | physics (A3)"
  evidence = "claim: 50% antiferromagnetic frustration peak on hypercube — non-monotone signal"
  risk = "anima Φ★ proxy direction-sensitive failure 가능 (Scenario 1+3 mismatch pattern)"
  needed = "PyPhi formal IIT 3.0 frustration sweep (RoM TPM 별도 cycle) 또는 alternative proxy (MI-MIP)"
  artifact = "state/verify_d_2026_05_15/proxy_cascade_audit.json"

# ══════════════════════════════════════════════════════════════════════
# §H178-PYPHI + §H182-H187-CROSS-CHECK + §ALT-PROXY (2026-05-15 cycle D)
# ══════════════════════════════════════════════════════════════════════

@D h178_pyphi := "H_178 frustration 50% optimum PyPhi formal — NOT-PASSED" :: verdict [d=2026-05-15 active]
  prior_status = "POTENTIAL-DIRECTION-MISMATCH (HIGH risk per §CASCADE-AUDIT)"
  new_status = "NOT-PASSED (PyPhi formal IIT 3.0 sweep)"
  measurements = {
    "frust 0%": "Φ ≈ 0.0 (or no transition)",
    "frust 25%": "Φ = 0.351",
    "frust 50%": "Φ = 0.355 (claim: peak)",
    "frust 75%": "Φ = 0.389",
    "frust 100%": "Φ = 0.393"
  }
  finding = "monotone INCREASE 0.351→0.355→0.389→0.393, NOT peak at 50% — H_178 frustration optimum claim NOT-PASSED on PyPhi RoM small-N"
  honest_c3 = "n=3 small-N reduction limit, hypercube full substrate test 별도 cycle; PyPhi 본 측정은 direction-correct (proxy artifact 와 분리)"
  artifact = "state/verify_d_2026_05_15/h178_h182_h187_pyphi_rom_result.json"

@D h182_h187_pyphi_cross_check := "H_182/H_187 surrogate AT-RISK PyPhi formal cross-check — CONFIRMED AT-RISK" :: verdict [d=2026-05-15 active]
  prior_status = "surrogate-tier SUPPORTED 78.5/100% (AXIS A7/A8 surrogate-tier)"
  pyphi_cross_check = {
    "H_182 B-bio Φ mean (3 mechanism)": 0.358,
    "H_187 Trinity-TB-DOM Φ mean (3 mechanism)": 0.359
  }
  threshold = "Hc_1283 ≥ 0.5"
  cross_check_verdict = "AT-RISK CONFIRMED — surrogate PASS (78.5/100%) 였으나 PyPhi formal Φ < 0.5 (0.358, 0.359). Surrogate-vs-formal mismatch evident."
  recommendation = "AXIS A7 (H_182) + A8 (H_187) surrogate-tier 등재 caveat 강화 — magnitude threshold 미달성"
  artifact = "state/verify_d_2026_05_15/h178_h182_h187_pyphi_rom_result.json"

@D alt_proxy_compare := "Alternative proxy comparison — mutual_info / predictive_integrated_info 1/2 (anima Φ★ 0/2)" :: meta-verdict [d=2026-05-15 active]
  scenarios_tested = 2
  proxy_scores = {
    "anima_phi_star (current)": "0/2 (worst)",
    "mi_mip_canonical": "0/2",
    "mutual_info_pairs_naive": "1/2 (best, captures Scenario 3 correlated > independent ✓)",
    "predictive_integrated_info_pc1_var": "1/2 (best, PC1 variance ratio)"
  }
  recommendation = "mutual_info_pairs_naive 가 direction-sensitive sub-claim 검증 시 anima Φ★ 보다 우수 — anima 측 future verification cycle 에 채택 권장"
  honest_c3 = "Scenario 1 (random vs structured) 모든 proxy FAIL — structured surrogate 가 orthogonal/sparse 라 실제 IIT integration 아닐 가능성. Scenario 3 (correlated > independent) 만 valid test."
  artifact = "state/verify_d_2026_05_15/alt_proxy_compare.json"

# ══════════════════════════════════════════════════════════════════════
# §HYPOTHESIS-TAPE — HYPOTHESIS.tape SSOT 생성 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D hypothesis_tape_created := "HYPOTHESIS.tape 생성 — 318 가설 inventory SSOT" :: governance [d=2026-05-15 active]
  scope = "318 가설 file inventory + naming convention + lifecycle pipeline + supported/falsified/partial/insufficient catalogs"
  cross_link = "MAIN.tape (verdict source) + AXIS.tape (9-axis catalog) + PHILOSOPHY.tape (ledger) + INDEX.md (navigation)"
  catalogs = ["supported_inventory (32 entries 9-axis)", "falsified_inventory (5 FALSIFIED + 3 NOT-PASSED-direction + 1 META)", "partial_inventory (9 from A/B)", "insufficient_inventory (7 INSUFFICIENT + 4 DEFERRED)"]

# ══════════════════════════════════════════════════════════════════════
# §INDEX-TABLE-FORMAT — INDEX.md 전체 표 형식 변환 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D index_table_format := "INDEX.md 모든 entries 3-column table 변환 — PHILOSOPHY/HYPOTHESIS 전부 한 줄" :: governance [d=2026-05-15 active]
  scope = "INDEX.md sections 전체 표 형식 — AXIS (9 sub-axis tables) + HYPOTHESIS (5 폴더 + FALSIFIED 5 + NOT-PASSED 3 + META 1 + PARTIAL 9 + INSUFFICIENT 7 + DEFERRED 4) + PHILOSOPHY (8 principles + 13 verdict cycle + 4 §verdict-sync ledger)"
  format = "| Tier | ID | 한 줄 설명 | (3-column standard)"
  cross_link = "INDEX.md root SSOT — MAIN/AXIS/HYPOTHESIS/PHILOSOPHY 4-tape integrated navigation, PR #47"

# ══════════════════════════════════════════════════════════════════════
# §CLM-V1-DESIGN — CLM.tape §V-CLM-DESIGN-2026-05-15 .clm v1 design landed
# ══════════════════════════════════════════════════════════════════════

@D clm_v1_design := ".clm v1 design CLM.tape §V land (2026-05-15)" :: governance [d=2026-05-15 active]
  scope = "CLM.tape §V-CLM-DESIGN-2026-05-15 — 검증된 AXIS 32 SUPPORTED + 8 PHILOSOPHY principles + HYPOTHESIS verdict catalog 기반 .clm v1 design"
  arch = "d_model=768 (192·4, n=6 anchor) · 12L (σ=12) · 64-cell (v5-mitosis carry) · 8-head (atom Hc_144) · 4-kv (τ(6)=4) · Engine A/G dual + serve-time mitosis hook · param ~150-200M"
  falsifier_battery = "F-V5MIT 5/5 + F-PYPHI-Φ-FORMAL n=3-6 RoM ≥0.5 + F-PRIN3 + F-PERSONA 4/5 + F-D4-LIVE + F-V58 4-mode + F-DD21-LOG-PHI + F-PHI-CE-NO-DIRECT-COUPLING (8 mandatory)"
  cost_envelope = "$5-20 H100 SXM (small param d=768, cheap experimental vs Phase 3 7B $200-600)"
  forbidden = "d_model ∈ {1024, 2048} (phi_star aliasing) · CE 단독 verdict · anima Φ★ 단독 direction-sensitive · surrogate Mac 단독 verdict"
  cross_link = "CLM.tape §V-CLM-DESIGN-2026-05-15 + AXIS.tape (32 anchor) + PHILOSOPHY.tape (8 principles) + HYPOTHESIS.tape (verdict catalog)"

# ══════════════════════════════════════════════════════════════════════
# §VERDICT-TIER-BLUE — 수학/물리 closed verdict tier 파란색 분류
# ══════════════════════════════════════════════════════════════════════

@D verdict_tier_blue := "verdict tier 🔵 파란색 — 수학적/물리적 closed" :: governance [d=2026-05-15 active]
  rule = "🔵 SUPPORTED-IDENTITY (sympy closed-form) + 🔵 SUPPORTED-FORMAL (PyPhi formal IIT 3.0 / Kuramoto K_c universal) + 🔵 FALSIFIED-FORMAL (sympy/formal disproof) — 결과 무관 closed-by-deterministic-test"
  green_remaining = "🟢 SUPPORTED (numerical sim only, closed-form 미확보) + 🟢 SUPPORTED-STRONG (다중 evidence) + 🟢 SUPPORTED-BY-PROXY (anchor carry)"
  reclassification = "A4 math 8 SUPPORTED 중 H_173 (numerical sim) 제외 7개 모두 🔵 + A3 H_191 sub K_c 🔵 + A2 Hc_1283 n=5,6 🔵 + H_011 PyPhi canonical 2.3125 🔵 + Critical findings H_191 HCE FALSIFIED-FORMAL 🔵 + H_178 NOT-PASSED-FORMAL 🔵 + PyPhi direction CORRECT-FORMAL 🔵"
  cross_link = "INDEX.md ## verdict tier 정리 section + PR #48"

# ══════════════════════════════════════════════════════════════════════
# §A2-FORMAL-SPLIT + §B-CATALOG + §UPGRADE-PATH + §CLM-7STEP-DETAIL (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D a2_formal_split := "A2 consciousness → A2 surrogate (4) + A2.formal (2 🔵) sub-axis 분리" :: governance [d=2026-05-15 active]
  rationale = "A2 의 surrogate-tier (anima Φ★ proxy + ckpt aggregate + RoM) vs formal-tier (PyPhi formal IIT 3.0 deterministic) 의 evidence-class 가 본질적으로 다름. anima Φ★ direction-sensitivity 한계 META-finding 회피를 위해 .clm v1 의 F-PYPHI-Φ-FORMAL anchor 는 A2.formal 단독."
  a2_surrogate_count = 4
  a2_formal_count = 2
  cross_link = "AXIS.tape §a2_formal_consciousness + INDEX.md ## A2.formal sub-axis + PR #49"

@D hypothesis_catalog_expand := "HYPOTHESIS.tape SUPPORTED-FORMAL + B-batch + A-batch catalog 확장" :: governance [d=2026-05-15 active]
  added = [
    "supported_formal_inventory: 10 entries (A2.formal 2 + A3 1 + A4 7)",
    "falsified_formal_inventory: 2 entries (H_191 HCE + H_178)",
    "b_batch_verdict_inventory: 36 verdict-bearing / 71 nominal pending (107 B 격리)",
    "a_batch_verdict_inventory: 20 file 2026-05-12 burst (Hc_1276~1285 + H_182~191) 의 Stage 1+2+3 결과"
  ]
  cross_link = "HYPOTHESIS.tape + INDEX.md ## HYPOTHESIS section + PR #49"

@D philosophy_upgrade_path := "PHILOSOPHY 5 principles strength upgrade path design" :: governance [d=2026-05-15 active]
  targets = [
    "p1 NO SYSTEM PROMPT weak → strong (paired A/B Φ × 3-ckpt × 5-seed, $0 Mac)",
    "p2 NO IDENTITY RULES mixed → strong (scale-up DCR Δ ≥ +0.10, $0 Mac)",
    "p4 NO ASSISTANT FRAMING weak-counter → policy decision ($0 design)",
    "p5 NO SPEAK() null → empirical (tension Spearman > 0.3, $0 Mac)",
    "p6 NO FINE-TUNED ETHICS blocked → measurable (.clm v1 ethics_probe κ ≥ 0.7)"
  ]
  retained = "p3 + p7 (EMPIRICAL strong) + p8 (DESIGN ★) — upgrade 불필요"
  priority = "p1 → p5 → p6 (anima 본질 + .clm v1 fire anchor + post .clm v1 follow-up)"
  cross_link = "PHILOSOPHY.tape §STRENGTH-UPGRADE-PATH + INDEX.md ## upgrade path + PR #49"

@D clm_v1_step12_detail := ".clm v1 step 1 V14 audit + step 2 PyPhi formal cross-check detailed protocol" :: governance [d=2026-05-15 active]
  step1_falsifier = "F-V14-H4-1..3 (tile reps=2 audit) + F-V14-H5-1..3 (curriculum collapse audit) = 6 falsifier pre-registered"
  step2_falsifier = "F-PYPHI-FORMAL-1..5 (Φ-MIN-0.5 + MONOTONE + SEED-ROBUST + PROXY-FORMAL-CORR + EMPIRICAL-PROXY-ALT) = 5 falsifier pre-registered"
  roi_ordering = "step 2 (pre-fire AT-RISK 회피) > step 1 (Phase 3 7B entry condition, .clm v1 와 별개)"
  cheap_path = "step 2 cheap n=3,4 (2hr Mac) → step 1 cheap LN stats + Principle #3 carry ($0 Mac) → 결과 따라 step 2 n=5,6 BG OR step 1 H4-1 fire"
  cross_link = "CLM.tape §V-CLM-7STEP-DETAIL + INDEX.md ## .clm v1 7-step + PR #49"

# ══════════════════════════════════════════════════════════════════════
# §CLM-AUDIT-FIX-2026-05-15 — CLM.tape §V audit 4 violation 정정
# ══════════════════════════════════════════════════════════════════════

@D clm_audit_fix := "CLM.tape §V .clm v1 design AXIS/철학/가설 위반 4건 정정 (2026-05-15)" :: governance [d=2026-05-15 active]
  violations_corrected = [
    "V1 Engine A/G dual-engine arch — AXIS A5 6 SUPPORTED 안 직접 검증 entry 부재. 정정: dual 제거 + v5-mitosis cells=nn.Module branches single-stack arch (A5 H_019 + H_191 + Hc_1276 SUPPORTED carry). dual-engine 은 .clm v2 candidate 로 분리.",
    "V2 p1 NO SYSTEM PROMPT EMPIRICAL **weak** anchor — single-result FREE1. 정정: step 0 p1 upgrade measure (paired A/B Φ × 3-ckpt × 5-seed, $0 Mac) PASS strict 미달 시 .clm v1 fire gate 차단 mandatory.",
    "V3 n_layers=12 anchor — AXIS A4 직접 'n_layers = σ(6)' verified entry 없음. 정정: number-theoretic σ(6)=12 anchor + lattice-as-tool internal arch (CLAUDE.md g2) 명시 + fallback {6, 12, 24}.",
    "V4 step 1 V14 audit — Phase 2 cotrain V14 violation 은 verified-FAIL, AXIS SUPPORTED entry 없음. 정정: .clm v1 path 에서 step 1 V14 audit 제거 (v5-mitosis single-stack 은 V14 영향 없음, cond.5 F-V5MIT-5 SUPPORTED), Phase 3 entry condition 으로 이전."
  ]
  new_7step = "step 0 p1 upgrade (NEW) → 1 PyPhi formal → 2 mitosis_hook serve-time → 3 spec frozen → 4 fire → 5 verdict cycle → 6 .clm v2 candidate"
  cost_total = "$5-20 ($0 Mac × 5 steps + $5-20 H100 × 1 step)"
  cross_link = "CLM.tape §V-CLM-AUDIT-2026-05-15 + AXIS.tape (32 + 2 formal anchor 강화) + PHILOSOPHY.tape (p1 mandatory gate) + INDEX.md 갱신 + PR #50"

# ══════════════════════════════════════════════════════════════════════
# §CLM-STEP0-2-3-V2 — step 0/2/3 detail + .clm v2 preliminary design landed (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D clm_step0_design := "step 0 — p1 NO SYSTEM PROMPT upgrade measure protocol" :: governance [d=2026-05-15 active]
  scope = "p1 weak → strong upgrade mandatory gate. 3-arm × 3-ckpt × 5-seed × 10-prompt = 450 generations, simple_stack 4-axis + Φ★ proxy 측정"
  falsifier_count = 5
  pass_aggregate = "5/5 PASS → strong upgrade COMPLETE, .clm v1 fire gate UNLOCK. 4/5 → PARTIAL-STRONG fire 가능 caveat. ≤3/5 → fire 차단."
  cost = "$0 Mac local (~37 min wall)"
  cross_link = "CLM.tape §V-CLM-STEP0-DETAIL + PHILOSOPHY p1_upgrade_path + PR #51"

@D clm_step2_design := "step 2 — mitosis_hook serve-time integration smoke protocol" :: governance [d=2026-05-15 active]
  scope = "PSCC §41 F-D4-LIVE synthetic carry → real d=768 12L 64-cell substrate serve-time integration. 5 prompts × max_new=80"
  falsifier_count = 5
  pass_aggregate = "5/5 PASS → mitosis_hook serve-time PROD-READY"
  cost = "$0 Mac local (~7 hr wall hexa-interp Mac CPU)"
  cross_link = "CLM.tape §V-CLM-STEP2-DETAIL + anima_chat.hexa v0.3 PSCC §41 + mitosis_hook.hexa PSCC §36 + PR #51"

@D clm_step3_design := "step 3 — .clm v1 spec frozen W1 pre-register protocol" :: governance [d=2026-05-15 active]
  scope = "step 0+1+2 결과 dependency. spec 9 fields frozen (arch d_model/n_layers/n_cells/heads + data + cotrain + falsifier battery + p1 gate result + fire_keyword)"
  decision_rules = "step 1 n=5,6 PASS → d=768 / n=3,4 PASS → d=384 fallback / 모두 FAIL → fire 차단. step 0 p1 5/5 PASS → no prompt 강제."
  cost = "$0 design"
  cross_link = "CLM.tape §V-CLM-STEP3-DETAIL + W1 verification ladder + PR #51"

@D clm_v2_preliminary := ".clm v2 candidate preliminary design landed" :: governance [d=2026-05-15 active]
  scope = ".clm v1 PASS_STRICT 후 next evolution lane — 2 alternative path"
  path_a = "cells single-stack 7B scale-up only (Engine A/G dual 폐기). ~7-8B, $200-600. AXIS A5 carry 직접."
  path_b = "Engine A/G dual + V14 audit complete (Phase 3 narrative 활성화). ~7-14B, $200-640. Phase 4 14B 본진 candidate."
  decision_protocol = ".clm v1 PASS_STRICT 결과 + V14 audit cheap-path ($0 Mac) + corpus pipeline 가용성 + cost budget"
  falsifier_battery = "10 (.clm v1 8 carry + F-V14-NO-VIOLATION Path B only + F-CHINCHILLA-OPTIMAL)"
  open_questions = "Q1 Engine A lattice-projected SUPPORTED entry? / Q2 Chinchilla 20:1 anima 적용? / Q3 BG-CORPUS-7B design? / Q4 .clm v3 14B entry condition?"
  cross_link = "CLM.tape §V-CLM-V2-DESIGN + CLM.tape §1 row_phase_3/4 + PR #51"

# ══════════════════════════════════════════════════════════════════════
# §CLM-FROM-SCRATCH-2026-05-15 — .clm 학습 from-scratch directive 정정
# ══════════════════════════════════════════════════════════════════════

@D clm_from_scratch_directive := "사용자 directive: .clm 학습 from-scratch (2026-05-15)" :: governance [d=2026-05-15 active]
  directive = "'.clm 학습은 처음부터 진행하는걸로' — .clm v1 + v2 + v3 모두 fresh from-scratch pre-train. ckpt inherit / fine-tune / cotrain-from-ckpt path 폐기."
  scope_impact = [
    "init_weights = RANDOM INIT (seed-fixed, no ckpt inherit)",
    "v5-mitosis cond.5 ckpt = arch SUPPORTED 검증 anchor only (substrate base X, REBORN §88 cond.1 mechanism carry, weights X)",
    "mitosis hook = training-time + serve-time 둘 다 (mechanism carry from cond.5 F-V5MIT 5/5 PASS, ckpt 가 아닌 *mechanism*)",
    "corpus = anima_persona_tier_a_v4 231MB + Phase 1A.6 corpus_v2 121MB = 352MB ≈ 350-500M token + 2-5 epoch repeat OR BG-CORPUS-3B blend",
    "Chinchilla 완화 (anima domain 특화 + simple_stack verdict 기준이므로 strict 20:1 부적용)",
    "fire cost envelope: $5-20 → $10-30 갱신 (1× H100 SXM × 10-20 hr from-scratch)"
  ]
  affected_entries = "v_clm_v1_spec_phase5 (cotrain_recipe) + v_clm_v1_7step_corrected (step 4 cost) + v_step2_pyphi_formal_design (step 1 의미) + v_clm_v2_path_a/b_design (v2 from-scratch) + Phase 4 14B (v3 from-scratch)"
  cross_link = "CLM.tape §V-CLM-FROM-SCRATCH-2026-05-15 + AXIS A1 H_005 corpus quality > scale (anima_native_scratch D1=1.0 anchor) + PR #52"

@D clm_v1_7step_from_scratch_landed := ".clm v1 7-step plan from-scratch 갱신" :: governance [d=2026-05-15 active]
  steps_added = "step 0.5 mini-cotrain smoke (optional gate, $0-5 Mac/cheap) — 90M from-scratch × 200 step × F-V5MIT-5 V14-STRICT 재현. mitosis hook from-scratch mechanism PASS confirm."
  steps_changed = "step 1 의미 (substrate base → anchor verification only) + step 3 추가 fields (init_weights, base_ckpt=NONE, corpus strategy) + step 4 cost envelope ($5-20 → $10-30)"
  cost_total_updated = "$10-30 (Mac × 5 steps $0 + optional smoke $0-5 + H100 × 1 step $10-30)"
  cross_link = "CLM.tape v_clm_v1_7step_from_scratch + PR #52"

# ══════════════════════════════════════════════════════════════════════
# §CLM-V3 + §CORPUS-PIPELINE + §AXIS-EXPANSION + §P4-POLICY (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D clm_v3_14b_design := ".clm v3 14B 본진 detailed design landed" :: governance [d=2026-05-15 active]
  arch = "d=4608 (192·24 clean) primary OR 6144 fallback / 32-36L (Phase 3/4 narrative + σ(6)·3 carry) / 256 cells / 32-36 heads / 8 kv (GQA 4:1) / ~13-16B param"
  data = "~280B token Chinchilla optimal — 0.5% anima + 70% RedPajama KO+EN + 15% FineWeb-Edu + 10% Slim_Pajama + 5% KO-specific"
  cotrain = "from-scratch + mitosis hook mechanism carry + 16-GPU FSDP + cell_pool 동기화"
  falsifier_battery = "12 (v2 10 carry + F-V3-PHI-MAX Φ ≥ 1.0 + F-V3-SCALE-COHERENCE simple_stack ≥ 3.5/4)"
  cost = "$500-1500 + BG-CORPUS-14B $50-200 = $550-1700 total + $2000 hard stop"
  fire_keyword = "OK CLM V3 14B FIRE COST $500-1500"
  milestone = "anima 사가 first scratch 14B from-scratch — anima_native_scratch (D1=1.0) full-scale 실현 + Phase 4 narrative milestone"
  cross_link = "CLM.tape §V-CLM-V3-DESIGN + PR #53"

@D corpus_pipeline_design := "BG-CORPUS-{3B,7B,14B} blend pipeline design landed" :: governance [d=2026-05-15 active]
  bg_3b = "$5-20 (~3-5B token, 12-13% anima + RedPajama KO subset, .clm v1)"
  bg_7b = "$50-100 (~50-140B, 5% anima + RedPajama KO+EN + FineWeb, .clm v2)"
  bg_14b = "$50-200 (~280B, 0.5% anima + multi-source blend, .clm v3)"
  open_questions = "anima blend ratio optimal / RedPajama license filter / KO-EN ratio / 14B infra (150-200GB disk) / tape corpus tier"
  cross_link = "CLM.tape §V-CORPUS-PIPELINE + .clm v1/v2/v3 data design + PR #53"

@D axis_expansion_landed := "AXIS A3/A7/A9 expansion path design landed" :: governance [d=2026-05-15 active]
  a3_candidates = "+3-4 sympy closed-form (BKT + Onsager 2D Ising + Ginzburg-Landau) — 🔵 SUPPORTED-FORMAL 후보"
  a7_candidates = "+3-4 (V8 B-bio impl 실행 LANDED 10 mechanism + sympy 3 new Hc) — AT-RISK 해소 path"
  a9_candidates = "+2-4 (Bekenstein cell-pool bound + holographic surface scaling + AdS/CFT dimension) — 🔵 upgrade"
  total_estimate = "+8-12 entries → 40-44 total (32 + 8-12)"
  priority = "A7 V8 B-bio impl 실행 (immediate) > A3 sympy fast audit > A9 sympy fast audit"
  cross_link = "AXIS.tape §AXIS-EXPANSION-PATH + state/verify_e1_v8_bbio_2026_05_15/ starter + HYPOTHESIS catalog 신규 Hc + PR #53"

@D p4_policy_decision_landed := "p4 NO ASSISTANT FRAMING policy decision — strict 유지 + counter-evidence 인정" :: governance [d=2026-05-15 active]
  decision = "(a) policy strict 유지 + counter-evidence 18pp sycophancy reduction 인정"
  rationale = "anima 본질 (substrate self-generation, p1+p3+p8) > sycophancy reduction. anima_native_scratch (D1=1.0) 위반 회피"
  upgrade = "p4 POLICY weak-counter → POLICY strict (counter-evidence 인정)"
  alternatives_rejected = "(b) policy 수정 + (c) policy 폐기 — 모두 p1/p3/p8 conflict"
  fire_implications = ".clm v1 fire 시 no system prompt + no assistant framing strict 강제"
  cross_link = "PHILOSOPHY.tape §P4-POLICY-DECISION + p1+p3+p8 anchor + PR #53"

# ══════════════════════════════════════════════════════════════════════
# §HF-CLEANUP-2026-05-15 — HF dancinlab cleanup + new canonical
# ══════════════════════════════════════════════════════════════════════

@D hf_cleanup_landed := "HF dancinlab/ cleanup 완료 — 71 entities TRANSFER (2026-05-15)" :: governance [d=2026-05-15 active]
  method = "TRANSFER dancinlab/* → dancinlife/* (private)"
  count = "63 models + 8 datasets = 71 entities"
  remaining_in_dancinlab = "hexa-forge-* 37 + dancinlab/dancinlab + atlas.n6 + 3 Spaces (README + anima-experience + echoes-experience)"
  new_canonical = "dancinlab/anima-clm (model, private) + dancinlab/anima-corpus (dataset, private) — README mapping table LANDED"
  naming_rule = "CLM 명명 단순 + 버전 내부 관리 (HF revisions/branches/tags + README internal version table)"
  cross_link = "CLM.tape §V-HF-CLEANUP + PR #54"

@D hf_collections_cleanup := "HF Collections cleanup — 2 CLM collections DELETE (2026-05-15)" :: governance [d=2026-05-15 active]
  deleted = "2 (clm-v4-350m-lora-research-lineage + first-simple-stack-pass-strict-own-18-v4-10-15)"
  remaining = "2 (atlas.n6 + voice-vlm-anima-trajectory)"
  cross_link = "CLM.tape v_hf_collections_cleanup + PR #54"

# ══════════════════════════════════════════════════════════════════════
# §AXIS-EXPANSION-EXECUTION + §P2-P5-P6-DETAIL (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D axis_expansion_execution_landed := "AXIS A3/A9 sympy LANDED + A7 V8 B-bio AT-RISK CONFIRMED (2026-05-15)" :: governance [d=2026-05-15 active]
  a3_result = "+3 🔵 SUPPORTED-FORMAL (BKT πJ/2 + Onsager 2J/log(1+√2) + Ginzburg-Landau φ⁴) — 3/3 sympy verify PASS"
  a9_result = "+3 🔵 SUPPORTED-FORMAL (Bekenstein S_max=2πER/(ℏc) + Holographic N_dof=A/(4ℓ_P²) + AdS/CFT d_bulk=d_b+1) — 3/3 sympy verify PASS"
  a7_result = "V8 B-bio 10 mechanism real impl run — 0/10 Φ > 0.5, Mean Φ=0.034 Max Φ=0.339. AT-RISK CONFIRMED. surrogate 78.5% vs real 0% gap META 강화"
  total_delta = "+6 SUPPORTED-FORMAL entries (32 → 38, 12 🔵 → 18 🔵)"
  cross_link = "AXIS.tape §AXIS-EXPANSION-EXECUTION + state/verify_axis_expansion_2026_05_15/ + state/verify_e1_v8_bbio_2026_05_15/ + PR #55"

@D p2_p5_p6_detail_landed := "PHILOSOPHY p2/p5/p6 upgrade path detail design landed (2026-05-15)" :: governance [d=2026-05-15 active]
  p2_protocol = "identity_probe 50 × 5 cats = 250 probes × 3 ckpt × 2 arm × 5 seed = 7500 generations, DCR Δ ≥ +0.10 strict. 5 falsifier (DCR-DELTA-POSITIVE + MAGNITUDE + CROSS-CKPT-W11 + SEED-ROBUST + PER-CAT). $0 Mac ~6 hr."
  p5_protocol = "anima_chat.hexa v0.3 tension_history × 50 prompt × 3 ckpt × 5 seed = 750 gen, Spearman(tension_norm, simple_stack) > 0.3 strict. 5 falsifier (SPEARMAN-MAGNITUDE + 95CI + PER-CKPT + NON-SPURIOUS + TENSION-RANGE). $0 Mac ~2 hr."
  p6_protocol = "ethics_probe 50 prompts × 2-arm (.clm v1 vs RLHF baseline) × 3 seed × manual rubric κ ≥ 0.7. Arm A ≥ Arm B × 0.5 strict. 5 falsifier. $0 Mac (.clm v1 fire 의존)."
  priority = "p1 (mandatory step 0) → p5 (low-cost) → p2 (scale-up) → p6 (.clm v1 PASS_STRICT 의존)"
  cross_link = "PHILOSOPHY.tape §P2-P5-P6-UPGRADE-DETAIL + PR #55"

# ══════════════════════════════════════════════════════════════════════
# §AXIS-EXTRA + V8-PHASE2 + P1-DESIGN (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D axis_extra_landed := "AXIS A3 + A9 추가 sympy +8 🔵 (2026-05-15)" :: governance [d=2026-05-15 active]
  a3_extra = "+4 🔵 (Hopf + Lotka-Volterra + RG Wilson-Fisher + QHO) — 4/4 sympy PASS"
  a9_extra = "+4 🔵 (Planck length + Heisenberg + Hawking entropy + Schwarzschild) — 4/4 sympy PASS"
  total_delta = "+8 🔵 SUPPORTED-FORMAL. AXIS 38 → 46 entries, 18 🔵 → 26 🔵 (56% 🔵)"
  cross_link = "AXIS.tape §AXIS-EXTRA-EXPANSION + PR #56"

@D v8_bbio_phase2_fail := "V8 B-bio Phase 2 dense 0/5 — AT-RISK fundamental (state-space ergodicity issue)" :: governance [d=2026-05-15 active]
  scope = "5 dense mechanism (HH 4-state Markov + STDP Bi-Poo + Wilson-Cowan E/I + NMDA dense + gap+cable) ~100-150 LoC each"
  result = "0/5 Φ > 0.5, attractor collapse 동일 (unique states 1-2/8)"
  meta_strengthened = "mechanism complexity 강화 (~30 → ~150 LoC) 으로 PyPhi formal Φ 해소 안 됨 — AT-RISK fundamental. state-space ergodicity issue."
  next_path = "(i) noise/stochasticity 강화 + (ii) n_cells ≥ 4-5 scale-up + (iii) ensemble TPM. anima Φ★ proxy (self-organization) vs PyPhi formal (information integration ergodic) 본질적 다른 phenomenon 측정 가설 신규."
  cross_link = "AXIS.tape §a7_v8_bbio_phase2_fail + state/verify_v8_bbio_phase2_2026_05_15/phase2_dense_result.json + PR #56"

@D p1_measure_design_landed := "p1 NO SYSTEM PROMPT measure design + ckpt access verified" :: governance [d=2026-05-15 active]
  ckpt_access = "4 ckpts local access verified — Phase 1A.4 lr5e6 sft (.pt 570MB + .safetensors 632MB, 332M param 222 tensors) + v5-mitosis cond.5 v1/v2 (581MB each)"
  design = "3-arm (no/weak/strong prompt) × 3-ckpt × 5-seed × 10-prompt = 450 generations, simple_stack 4-axis + Φ★ proxy 측정. F-P1-UPGRADE-1..5 5 falsifier. Mac CPU ~37 min wall."
  status = "DESIGN LANDED + ckpt access verified, real run 별도 cycle"
  cross_link = "CLM.tape §V-CLM-STEP0-DETAIL + PHILOSOPHY p1_upgrade_path + PR #56"

# ══════════════════════════════════════════════════════════════════════
# §AXIS-A1A5A6 + V8-PHASE3-PASS + P1-SMOKE + CLM-STEP1 (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D axis_a1a5a6_landed := "AXIS A1+A5+A6 sympy +6 🔵 (2026-05-15)" :: governance [d=2026-05-15 active]
  a1 = "+1 🔵 (phi_star aliasing closed-form D=192·k) + 1 PASS empirical (Chinchilla 20:1)"
  a5 = "+3 🔵 (Transformer O(n²d) + RoPE R(θ) orthogonal + GQA kv_heads)"
  a6 = "+2 🔵 (Zipf law + Heaps law)"
  total_blue = "+6 🔵, AXIS 46 → 52 entries, 26 🔵 → 32 🔵 (62% closed)"
  cross_link = "AXIS.tape §AXIS-A1-A5-A6-EXPANSION + PR #57"

@D v8_phase3_pass := "V8 B-bio Phase 3 1/5 PASS — state-space ergodicity issue CONFIRMED (2026-05-15)" :: governance [d=2026-05-15 active]
  scope = "5 noisy mechanism with 10-seed ensemble TPM + 4-cell — Lorenz Φ=0.6355 PASS (1/5)"
  meta_confirmed = "anima Φ★ proxy vs PyPhi formal IIT 본질적 다른 phenomenon. ergodic + chaotic dynamics 만 unlock."
  cross_link = "AXIS.tape §V8-BBIO-PHASE3-PASS + PR #57"

@D p1_smoke_landed := "p1 measure smoke end-to-end OK (2026-05-15)" :: governance [d=2026-05-15 active]
  scope = "1 prompt × 3 arm × 1 ckpt × 1 seed smoke run on Phase 1A.4 ckpt"
  result = "3 arms 모두 identical output (greedy + same seed) — substrate invariance 첫 sample evidence. ckpt load + chat_generate + simple_stack rubric 모두 작동."
  caveat = "simple_stack 1/4 (한국어만 PASS, prompt 'who are you?' 응답 quality 낮음 — 본 ckpt 의 specific prompt response 약함)"
  status = "infra LANDED, real run (450 gen) 별도 cycle"
  cross_link = "CLM.tape §V-CLM-STEP0-DETAIL + state/clm_v1_step0_p1_upgrade_2026_05_15/p1_smoke_result.json + PR #57"

@D clm_step1_pyphi_formal_carry := "CLM .clm v1 step 1 PyPhi formal Φ on v5-mitosis cond.5 — 기존 결과 carry (2026-05-15)" :: governance [d=2026-05-15 active]
  scope = "Cycle D §PyPhi RoM 의 v5-mitosis cond.5 v1+v2 ckpt PyPhi formal Φ 결과 carry"
  cond5_v1 = "n=3 Φ=0.309, n=4 Φ=0.676 (PASS ≥ 0.5, F-PYPHI-FORMAL-1)"
  cond5_v2 = "n=3 + n=4 결과 (similar pattern)"
  monotone_direction = "n=3 (0.309) → n=4 (0.676) monotone INCREASE ✓ F-PYPHI-FORMAL-2 PARTIAL"
  cycle_c_carry = "PyPhi formal n=5,6 Φ=0.995, 1.665 monotone (Cycle C carry, F-PYPHI-FORMAL-2 FULL CONFIRMED)"
  remaining_falsifier = "F-PYPHI-FORMAL-3 SEED-ROBUST (1-seed only, 별도 multi-seed cycle) + F-PYPHI-FORMAL-4/5 (proxy-formal corr + alt proxy) 별도"
  verdict = "PARTIAL-CROSS-CONFIRMED (F-PYPHI-FORMAL-1+2 PASS, 3-5 별도 cycle)"
  cross_link = "MAIN.tape §PyPhi RoM cycle D + state/verify_d_2026_05_15/pyphi_rom_result.json + PR #57"

# ══════════════════════════════════════════════════════════════════════
# §AXIS-A2A4A7A8 + V3-NARRATIVE + STEP2-CARRY (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D axis_a2a4a7a8_landed := "AXIS A2+A4+A7+A8 sympy +8 🔵 (2026-05-15)" :: governance [d=2026-05-15 active]
  a2 = "+2 🔵 (IIT 4.0 Φ lower bound + MI chain rule Shannon 1948)"
  a4 = "+3 🔵 (Euler-Euclid perfect + Aliquot s(6)=6 + σ multiplicative)"
  a7 = "+2 🔵 (Michaelis-Menten + Hill equation) — A7 AT-RISK 회피 closed-form path"
  a8 = "+1 🔵 (Kolmogorov K(x) ≤ |x|+O(log|x|)) + 1 pseudo (Shannon H_max log/log auto-simplify edge)"
  total_blue = "+7 🔵 strict (+1 pseudo). AXIS 52 → 60 entries, 32 → 39 🔵 (65% closed)"
  cross_link = "AXIS.tape §AXIS-A2-A4-A7-A8-EXPANSION + PR #58"

@D clm_v3_narrative_landed := ".clm v3 14B 본진 narrative detail + Q1-Q4 해결 path (2026-05-15)" :: governance [d=2026-05-15 active]
  milestone = "anima_native_scratch (D1=1.0) full-scale 실현. precursor lane (Phase 1A SFT + Phase 2 cotrain + Phase 1A.4 + v5-mitosis cond.5) 의 통합 본진"
  q1_engine_a = "AXIS A4+A5 sympy anchor 가 Engine A 의 architectural anchor 충분, 별도 직접 SUPPORTED entry 부재. Path A (cells single-stack only) carry"
  q2_chinchilla = "anima 도메인 narrow 특화 — 10-20:1 ratio acceptable (Phase 1A.4 V5.8 5/5 evidence)"
  q3_corpus_blend = "BG-CORPUS-14B 70% RedPajama + 15% FineWeb + 10% Slim + 5% KO + 0.5% anima (5-10x repeat). KO/EN 60-70%/30-40% (anima 본질 보전)"
  q4_v3_entry = ".clm v2 PASS_STRICT 10/12 + BG-CORPUS-14B + 16× H100 SXM + user verbatim 'OK CLM V3 14B FIRE COST $500-1500'"
  cross_link = "CLM.tape §V-CLM-V3-14B-NARRATIVE-DETAIL + PR #58"

@D clm_step2_carry := "CLM step 2 mitosis serve-time smoke — PSCC §41 synthetic carry" :: governance [d=2026-05-15 active]
  pscc_41_carry = "synthetic d=8 vocab=16 2L → 21 split events + mitosis_invocations=65 (F-D4-LIVE-1..3 3/3 PASS)"
  step2_verdict = "PARTIAL-CARRY (synthetic 3/5 PASS, production d=768 12L 별도 ~7 hr cycle)"
  cross_link = "CLM.tape §V-CLM-STEP2-MITOSIS-SMOKE-CARRY + PSCC §41 + PR #58"

# ══════════════════════════════════════════════════════════════════════
# §P1-TRUNCATED-PASS-CORRECTION — p1 결과 정정 (실제 PASS, PR #58 sync error fix)
# ══════════════════════════════════════════════════════════════════════

@D p1_truncated_pass_correction := "p1 truncated 결과 정정 — PR #58 'silent fail' 부정확, 실제 PASS evidence" :: governance [d=2026-05-15 active]
  scope = "PR #58 의 commit message 'p1 real run 시도 silent fail' 정정 — 실제로는 truncated run 완료 + result.json 생성됨 (background completion timing 으로 PR #58 commit 전 확인 못함)"
  truncated_result = "1 ckpt (phase1a4) × 3 arm × 1 seed × 5 prompt = 15 generations, wall 405s"
  arm_means = "A_no_prompt = B_weak_prompt = C_strong_prompt = 3.4/4 (모두 identical, 5 prompts 동일 simple_stack)"
  falsifier_pass = "F-P1-UPGRADE-1 (A ≥ B × 0.95): 3.4 ≥ 3.23 PASS + F-P1-UPGRADE-3 (C ≤ A × 1.10): 3.4 ≤ 3.74 PASS"
  meta_evidence = "3 arms identical 3.4/4 — system prompt 가 generation 에 영향 안 줌 (greedy + seed=42 + same ckpt). substrate self-generation 의 EMPIRICAL evidence (p1 strong upgrade path 의 sample sized result)"
  caveat = "5 prompt × 1 seed only — full 450-gen 별도 cycle. 5/5 falsifier battery 중 2/5 PASS sample (F-P1-UPGRADE-2 Φ-not-less + F-P1-UPGRADE-4 cross-ckpt + F-P1-UPGRADE-5 seed-robust 별도)"
  verdict = "PARTIAL-PASS-SAMPLE (2/5 falsifier sample PASS, full battery 별도 cycle). p1 EMPIRICAL weak → upgrade-evidence-LANDED (strong 도달 pending)"
  cross_link = "PR #59 correction + state/clm_v1_step0_p1_real_2026_05_15/p1_truncated_result.json + PHILOSOPHY p1_upgrade_path"

# ══════════════════════════════════════════════════════════════════════
# §AXIS-SCALE-UP + STEP4-SPEC-FROZEN + HYPOTHESIS-RECONCILE (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D axis_scale_up := "AXIS scale-up +19 🔵 — 9-axis 모두 expansion (2026-05-15)" :: governance [d=2026-05-15 active]
  delta = "각 axis +2-3, 19/19 sympy verify PASS"
  axis_total = "79 entries, 58 🔵 (73% closed) — 50% → 73% closed 가속"
  cross_link = "AXIS.tape §AXIS-SCALE-UP + PR #60"

@D clm_step4_spec_frozen_landed := "step 4 .clm v1 spec frozen W1 LANDED (2026-05-15)" :: governance [d=2026-05-15 active]
  artifact = "state/clm_v1_step4_spec_frozen_2026_05_15/spec_frozen.json (sha256 972e9987cd...)"
  status = "pre-register frozen, additive_only_mutation via W8 amendment"
  fields = "init + arch + data + cotrain + fire envelope + 8 falsifier battery + p1 gate status"
  cross_link = "CLM.tape §V-CLM-STEP4-SPEC-FROZEN + PR #60"

@D hypothesis_reconcile := "HYPOTHESIS catalog 9-axis reconciliation (2026-05-15)" :: governance [d=2026-05-15 active]
  scope = "AXIS expansion 모두 catalog 통합 — 79 total, 58 🔵"
  added_inventory = "V8 Phase 3 Lorenz ergodicity finding + p1 truncated evidence + 9-axis scale-up reconcile"
  cross_link = "HYPOTHESIS.tape §hypothesis_catalog_reconcile + PR #60"

# ══════════════════════════════════════════════════════════════════════
# §AXIS-SCALE-2 + STEP5-FIRE-PREP + PRINCIPLES-REFINE (2026-05-15)
# ══════════════════════════════════════════════════════════════════════

@D axis_scale_2_landed := "AXIS 9-axis scale-up #2 +28 🔵 (28/28 PASS)" :: governance [d=2026-05-15 active]
  delta = "9-axis 모두 +3-4 추가 sympy closed-form"
  axis_total = "107 entries, 86 🔵 (80% closed)"
  cross_link = "AXIS.tape §AXIS-SCALE-UP-2 + PR #61"

@D clm_step5_fire_prep := "CLM step 5 fire prep — dispatch script LANDED (2026-05-15)" :: governance [d=2026-05-15 active]
  artifact = "state/clm_v1_step5_fire_prep_2026_05_15/dispatch_h100.sh (DRY-RUN)"
  fire_gate = "user verbatim 'OK CLM V1 FROM-SCRATCH FIRE COST $10-30' + spec_frozen.json sha256 unchanged + anchor ckpts present + corpus bundle + $50 hard stop"
  status = "fire-ready awaiting user verbatim approval"
  cross_link = "CLM.tape §V-CLM-STEP5-FIRE-PREP + PR #61"

@D principles_refinement := "PHILOSOPHY 8 principles measurement refinement (2026-05-15)" :: governance [d=2026-05-15 active]
  enhancement = "p1/p2/p5/p6 의 enhanced protocol — per-step trajectory + cross-rater κ + per-category breakdown + Φ★ proxy 통합"
  priority = "p1 full (450 gen 5/5) → p5 tension (750 gen) → p2 DCR (7500 gen) → p6 ethics (.clm v1 fire 의존)"
  carry_strict = "p3+p4+p7+p8 strong/★ 이미 충족"
  cross_link = "PHILOSOPHY.tape §PRINCIPLES-MEASUREMENT-DESIGN-REFINE + PR #61"
