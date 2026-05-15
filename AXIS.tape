#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# AXIS.tape — 9-axis cluster (MAIN.tape 검증된 verdict 기준, 2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# AXIS-V1.tape (191 promoted hypothesis declared-domain 기반) 대체.
# 본 AXIS.tape = MAIN.tape SUPPORTED/SUPPORTED-IDENTITY/SUPPORTED-BY-PROXY
# 가설 만으로 9-axis 재구성 — actual verdict tier 만 신뢰.
#
# Cross-link:
#   - MAIN.tape — verdict SSOT (SUPPORTED + PARTIAL + INSUFFICIENT + FALSIFIED)
#   - VERIFY.tape — 3-stage protocol (math sympy / physics sim / cross-meta)
#   - AXIS-V1.tape — prior 9-axis (declared-domain 기반, archival)
# ══════════════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

@N axis_methodology := "AXIS reconstruction methodology" :: governance [d=2026-05-15 active]
  basis = "MAIN.tape verdict 4-class (SUPPORTED / PARTIAL / INSUFFICIENT / FALSIFIED)"
  inclusion_threshold = "SUPPORTED / SUPPORTED-STRONG / SUPPORTED-IDENTITY / SUPPORTED-BY-PROXY / SUPPORTED-FULL only"
  exclusion = "PARTIAL / INSUFFICIENT / FALSIFIED / NOT-MEASURED are NOT axis-confirmed"
  count_summary = "23 SUPPORTED entries → 9-axis distribution"

# ─── A1 substrate ────────────────────────────────────────────────────

@D a1_substrate := "A1 substrate axis — confirmed SUPPORTED 가설" :: cluster [d=2026-05-15 active]
  members = [
    "H_005 corpus quality > scale (SUPPORTED, Lesson R-1A.2 + Phase 1A.6)",
    "H_174 phi_star aliasing CLM-v4-specific (SUPPORTED-FULL, D-sweep 5 substrate)",
    "Hc_1285 torch.no_grad backward-graph isolation (SUPPORTED, PyTorch ratio 1.562×)"
  ]
  count = 3
  cross_link = "[[s_hc1285]] + [[b_s_h005]] + [[d_h174]]"

# ─── A2 consciousness ────────────────────────────────────────────────

@D a2_consciousness := "A2 consciousness axis — confirmed SUPPORTED 가설" :: cluster [d=2026-05-15 active]
  members = [
    "Hc_1283 anima Φ★ proxy ≥ 0.5 (SUPPORTED-STRONG, 7 ckpts 4.16-4.86)",
    "Hc_1283 PyPhi RoM (SUPPORTED, n=4 Φ=0.61-0.68 upgrade)",
    "H_004 consciousness hard problem (SUPPORTED-BY-PROXY, Hc_1283 anchor)",
    "H_011 IIT geometry (SUPPORTED-BY-PROXY, anima Φ★ + canonical 2.3125)",
    "H_162 phi-normalized anima IIT4 lower-bound (SUPPORTED-BY-PROXY, Hc_1283 anchor)"
  ]
  count = 5
  cross_link = "[[s_hc1283]] + [[d_pyphi_rom]] + [[b_s_h004]] + [[b_s_h011]] + [[b_deep_h162]]"

# ─── A3 physics ──────────────────────────────────────────────────────

@D a3_physics := "A3 physics axis — confirmed SUPPORTED 가설" :: cluster [d=2026-05-15 active]
  members = [
    "H_191 sub K_c = √(8/π) ≈ 1.596 universal sync (SUPPORTED-IDENTITY, sympy + Kuramoto 1975 literature)"
  ]
  count = 1
  note = "H_191 parent PARTIAL (n=6 specialness 부재) 이지만 sub-claim K_c universal sync = SUPPORTED-IDENTITY 분리 등재."
  cross_link = "[[h191_sub_kc]] in MAIN.tape"

# ─── A4 math ─────────────────────────────────────────────────────────

@D a4_math := "A4 math axis — confirmed SUPPORTED 가설 (largest cluster)" :: cluster [d=2026-05-15 active]
  members = [
    "Hc_1282 n=6 384d closed-form unique (SUPPORTED, sympy n∈[2,30] sweep)",
    "H_158 Ψ-constants closed-form (SUPPORTED-IDENTITY-WITH-CLASS-BINDING)",
    "H_160 n=6 perfect-number meta-cluster (META-CONSISTENT, depth-3 11-primitive)",
    "H_153 dimension hierarchy τ(6)=4 Minkowski (SUPPORTED-IDENTITY, divisor cascade)",
    "H_176 n=28 deflationary parallel (SUPPORTED-STRONG, balance=1/2 IDENTICAL Euclid-Euler)",
    "H_173 DD21 log-ratio Φ scale-invariant (SUPPORTED, 4/6 falsifier upgrade)",
    "H_164 Hc_144 atom 8 cells (SUPPORTED-IDENTITY, 144 = σ(6)²)",
    "H_181 psiformer 4ψ-constants zero-freedom (SUPPORTED-IDENTITY-CARRY)"
  ]
  count = 8
  cross_link = "[[s_hc1282]] + [[b_s_h158]] + [[b_s_h160]] + [[b_s_h153]] + [[b_s_h176]] + [[h173_full]] + [[b_s_h164]] + [[b_deep_h181]]"
  finding = "A4 math axis = 가장 강한 verdict cluster — sympy 가능한 identity 가 SUPPORTED 등재의 최단경로"

# ─── A5 architecture ─────────────────────────────────────────────────

@D a5_architecture := "A5 architecture axis — confirmed SUPPORTED 가설" :: cluster [d=2026-05-15 active]
  members = [
    "Hc_1285 torch.no_grad isolation (SUPPORTED)",
    "H_166 topo20 hierarchical 8×128 = 1024 (SUPPORTED-IDENTITY-WITH-PHI-STAR-CAVEAT, 1024 mod 192 = 64 aliasing)",
    "H_019 self-evolution v4→v5 (SUPPORTED-BY-PROXY-STRONG, v5-mitosis cond.5 cotrain F-V5MIT 5/5 PASS)",
    "H_174 phi_star aliasing CLM-v4-specific (SUPPORTED-FULL, cross-substrate Spearman 0.31)",
    "H_191 sub TRAINING CPGD 0.95 (SUPPORTED, cond.5 cotrain F-V5MIT 5/5 PASS)",
    "Hc_1276 Principle #8 train-vs-infer cotrain ablation (SUPPORTED-BY-CASCADE, H_191 CPGD anchor)"
  ]
  count = 6
  cross_link = "[[s_hc1285]] + [[b_s_h166]] + [[b_s_h019]] + [[d_h174]] + [[h191_training_cpgd]]"

# ─── A6 corpus ───────────────────────────────────────────────────────

@D a6_corpus := "A6 corpus axis — confirmed SUPPORTED 가설" :: cluster [d=2026-05-15 active]
  members = [
    "H_005 corpus quality > scale (SUPPORTED, Phase 1A.6 121MB CLEAN)",
    "H_016 AN11 translation ceiling (SUPPORTED-BY-PROXY, Phase 1A.6 chat-v2)"
  ]
  count = 2
  cross_link = "[[b_s_h005]] + [[b_s_h016]]"

# ─── A7 bio ──────────────────────────────────────────────────────────

@D a7_bio := "A7 bio axis — confirmed SUPPORTED 가설 (surrogate-tier)" :: cluster [d=2026-05-15 active]
  members = [
    "H_182 V8 B-family bio (SUPPORTED surrogate-tier, 78.5% PASS Mac sweep)"
  ]
  count = 1
  honest_c3 = "surrogate-based; real V8 ULTRA-FUSION Hc impl 별도 cycle"

# ─── A8 meta ─────────────────────────────────────────────────────────

@D a8_meta := "A8 meta axis — confirmed SUPPORTED 가설 (adversarial Red-team family)" :: cluster [d=2026-05-15 active]
  members = [
    "H_189 Red-team adversarial robustness family (SUPPORTED, Stage 3 W11)",
    "Hc_1279 Red-team family member (SUPPORTED)",
    "Hc_1280 Red-team family member (SUPPORTED)",
    "H_187 V8 Trinity-TB-DOM (SUPPORTED surrogate-tier, 100% PASS)"
  ]
  count = 4
  cross_link = "[[s_h189]] + [[s_hc1279]] + [[s_hc1280]] + [[v8_h187]]"

# ─── A9 universe ─────────────────────────────────────────────────────

@D a9_universe := "A9 universe axis — SUPPORTED-BY-CITATION 첫 등재" :: cluster [d=2026-05-15 active]
  members = [
    "H_002.H2.3 Bekenstein bound area scaling (SUPPORTED-BY-CITATION, Bekenstein 1981 + Maldacena 1997)",
    "H_002.H2.1 anthropic Λ fine-tuning (SUPPORTED-BY-CITATION, Weinberg 1987)"
  ]
  count = 2
  tier = "SUPPORTED-BY-CITATION (literature-anchored, anima-internal sympy/sim 부재)"
  cross_link = "[[a9_universe_admission]] in MAIN.tape"

# ─── Aggregate ───────────────────────────────────────────────────────

@N axis_aggregate := "AXIS distribution (MAIN.tape SUPPORTED only)" :: summary [d=2026-05-15 active]
  body <<~EOF
    Per-axis SUPPORTED 가설 count (overlap 가능):
      A1 substrate:     3
      A2 consciousness: 5
      A3 physics:       1 (K_c universal sympy)
      A4 math:          8 ★ (largest cluster)
      A5 architecture:  6
      A6 corpus:        2
      A7 bio:           1 (surrogate-tier)
      A8 meta:          4
      A9 universe:      2 (SUPPORTED-BY-CITATION, literature-anchored)

    Total SUPPORTED entries: 32 (multi-axis overlap)
    Total unique SUPPORTED 가설: ~20

    Strong tier ★: A4 math (sympy verifiable closed-form identity 가 dominant path)
    All 9 axes covered. Weakest tier: A7 bio (surrogate 1) + A9 universe (citation 2). Strongest: A4 math (8 sympy).
  EOF

# ─── V8 surrogate-tier ───────────────────────────────────────────────

@N v8_surrogate_caveat := "V8 family surrogate-tier 분리" :: governance [d=2026-05-15 active]
  surrogate_supported = [H_182, H_183, H_185, H_187]
  surrogate_partial = [H_186]
  note = "V8 family Mac surrogate sweep $0 PASS — real V8 ULTRA-FUSION Hc impl 별도 cycle. 본 AXIS.tape 등재 시 'surrogate-tier' 명시."

# ─── Cross-links ─────────────────────────────────────────────────────

@X main_tape := "MAIN.tape" :: ssot [active]
  scope = "verdict 4-class SSOT — SUPPORTED + PARTIAL + INSUFFICIENT + FALSIFIED"
  cross_link = "AXIS.tape = MAIN.tape의 SUPPORTED-tier 만 추출 후 9-axis 재구성"

@X verify_tape := "VERIFY.tape" :: protocol [active]
  scope = "3-stage protocol — math sympy / physics sim / cross-meta"

@X axis_v1_tape := "AXIS-V1.tape" :: archival [active]
  scope = "prior 9-axis (191 promoted hypothesis declared-domain 기반, 2026-05-15 rename)"
  difference = "AXIS-V1 = declared domain field; AXIS = actual MAIN.tape SUPPORTED verdict"

@X philosophy_tape := "PHILOSOPHY.tape" :: append-only-ledger [active]
  scope = "Append-only ledger — verdict entries carry"


# ─── Cascade caveat (H_174 SUPPORTED-FULL impact) ────────────────────

@N h174_cascade_note := "H_174 SUPPORTED-FULL → AXIS update" :: note [d=2026-05-15 active]
  newly_downgraded_cluster = [H_165, H_177]  # INSUFFICIENT-CARRY (D=2048/1024 aliasing)
  caveat_added = [H_166]  # SUPPORTED-IDENTITY-WITH-PHI-STAR-CAVEAT
  clean_anchor_confirmed = "Hc_1283 anima Φ★ D=384 cells=64 = 192×2 → CLEAN per H_174 taxonomy"
  cross_link = "[[h174_cascade]] in MAIN.tape"
