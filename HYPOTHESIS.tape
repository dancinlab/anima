#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# HYPOTHESIS.tape — 가설 inventory SSOT (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Cross-link:
#   MAIN.tape — verdict 4-class SSOT (SUPPORTED/PARTIAL/INSUFFICIENT/FALSIFIED)
#   AXIS.tape — MAIN.tape SUPPORTED-tier 9-axis 재구성
#   PHILOSOPHY.tape — 철학 진행 append-only ledger
#   INDEX.md — root navigation SSOT
# ══════════════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

@N hypothesis_inventory := "가설 318 file inventory" :: structure [d=2026-05-15 active]
  total = 318
  folders = {
    "hypotheses/ (A 격리)": "20 file — 옵션 A 2026-05-12 burst (H_182~H_191 + Hc_1276~Hc_1285)",
    "hypotheses_b_2026_05_15/H_promoted/ (B 격리)": "107 file — since 2026-04+ (옵션 B 2주+ cut)",
    "hypotheses_legacy_2026_05_15/ (legacy)": "191 file — pre-Phase-1 archaeology + recent",
    "hypotheses_archive_anima_clm_10/": "원본 양식 archaeology (panpsychism 등 96 file)",
    "state/quarantine_c_d_2026_05_15/": "C/D 격리 manifest-only (B 의 narrow subset / superset)"
  }

@N hypothesis_naming := "naming convention" :: structure [active]
  H_NNN = "promoted hypothesis (Stage 1+2+3 protocol 적용 대상)"
  Hc_NNNN = "candidate hypothesis (raw, pre-promotion)"
  example_promoted = "H_182, H_191, H_158, H_174, Hc_1283"
  example_candidate = "Hc_1276, Hc_1281, Hc_1283 (Hc 가 H_NNN 로 합쳐지기 전 candidate)"

@N hypothesis_lifecycle := "3-stage pipeline (don't skip)" :: workflow [active]
  stage_1 = "hypotheses_candidates/ — raw candidate ideas"
  stage_2 = "hypotheses/ — promoted, Stage 1+2+3 verify protocol 적용 대상"
  stage_3 = "MAIN.tape verdict 등재 → PHILOSOPHY.tape append-only ledger"

# ─── verdict-tier inventory (MAIN.tape SUPPORTED only) ──────────────

@N supported_inventory := "MAIN.tape SUPPORTED-tier 가설 inventory (32 entries)" :: catalog [d=2026-05-15 active]
  # A1 substrate
  a1_substrate = [
    "H_005 corpus quality > scale (Phase 1A.6 121MB CLEAN, V5.8 std_greedy 4/5)",
    "H_174 phi_star aliasing CLM-v4-specific (D=192 multiple only clean)",
    "Hc_1285 torch.no_grad backward-graph isolation (PyTorch ratio 1.562×)"
  ]
  # A2 consciousness
  a2_consciousness = [
    "Hc_1283 anima Φ★ proxy ≥ 0.5 (v5-mitosis 7 ckpt 4.16-4.86)",
    "Hc_1283 PyPhi RoM n=4 (cell-pair correlation TPM Φ=0.61-0.68)",
    "Hc_1283 PyPhi formal n=5,6 (Φ=0.995, 1.665 monotone INCREASE)",
    "H_004 consciousness hard problem (Hc_1283 anchor)",
    "H_011 IIT geometry (Φ ≫ 0.5 reachable + PyPhi canonical 2.3125)",
    "H_162 phi-normalized anima IIT4 lower-bound (Hc_1283 anchor, D=384 multiple ✓ clean)"
  ]
  # A3 physics
  a3_physics = [
    "H_191 sub K_c = √(8/π) ≈ 1.5958 Kuramoto mean-field (sympy + literature)"
  ]
  # A4 math (largest cluster)
  a4_math = [
    "Hc_1282 n=6 384d closed-form unique (sympy n∈[2,30] sweep)",
    "H_158 Ψ-constants closed-form (perfect-number cluster balance=1/2)",
    "H_160 n=6 perfect-number meta-cluster (depth-3 11-primitive vocabulary)",
    "H_153 dimension hierarchy τ(6)=4 Minkowski (divisor cascade)",
    "H_176 n=28 deflationary parallel (Euclid-Euler theorem, n=6 NOT unique)",
    "H_173 DD21 log-ratio Φ scale-invariant (4/6 falsifier SUPPORTED)",
    "H_164 Hc_144 atom 8 cells (144 = σ(6)² = 12²)",
    "H_181 psiformer 4ψ-constants zero-freedom (Ψ-cluster carry)"
  ]
  # A5 architecture
  a5_architecture = [
    "Hc_1285 torch.no_grad isolation (autograd)",
    "H_166 topo20 hierarchical 8×128 = 1024 (algebra ✓, phi_star aliasing caveat)",
    "H_019 self-evolution v4→v5 (v5-mitosis cond.5 cotrain F-V5MIT 5/5 PASS)",
    "H_174 phi_star aliasing CLM-v4-specific (cross-substrate Spearman 0.31)",
    "H_191 sub TRAINING CPGD 0.95 (cond.5 cotrain 220× CE reduction)",
    "Hc_1276 train-vs-infer cotrain ablation (cascade-from-CPGD)"
  ]
  # A6 corpus
  a6_corpus = [
    "H_005 corpus quality > scale (Phase 1A.6)",
    "H_016 AN11 translation ceiling (chat-v2 measurable)"
  ]
  # A7 bio
  a7_bio = [
    "H_182 V8 B-family bio (surrogate 78.5%, PyPhi formal Φ=0.358<0.5 AT-RISK)"
  ]
  # A8 meta
  a8_meta = [
    "H_189 Red-team adversarial robustness family (Stage 3 W11)",
    "Hc_1279 Red-team family member",
    "Hc_1280 Red-team family member",
    "H_187 V8 Trinity-TB-DOM (surrogate 100%, PyPhi formal Φ=0.359<0.5 AT-RISK)"
  ]
  # A9 universe
  a9_universe = [
    "H_002.H2.3 Bekenstein bound area scaling (literature Bekenstein 1981 + Maldacena 1997)",
    "H_002.H2.1 anthropic Λ fine-tuning ~10^-120 (literature Weinberg 1987)"
  ]

# ─── FALSIFIED / NOT-PASSED inventory ────────────────────────────────

@N falsified_inventory := "FALSIFIED + NOT-PASSED entries" :: catalog [d=2026-05-15 active]
  falsified = [
    "H_024 IIT-Φ_mip 8/8 sub-test FAIL (legacy)",
    "H_096 FALSIFIED_at_18M (scale-conditional)",
    "Hc_024 Φ-CE direct coupling FALSIFIED (cond.5 cotrain corr ≈ 0)",
    "Hc_1278 ckpt-as-branch on HCE substrate FALSIFIED-BY-CASCADE",
    "H_191 SUBSTRATE HCE unique-sync FALSIFIED (Kuramoto universal)"
  ]
  not_passed_direction = [
    "H_184.5 chaos monotone decrease — REVERSE (proxy artifact)",
    "Hc_1281 staged-growth 4-8× — REVERSE (0.714× measured, proxy artifact)",
    "H_178 frustration 50% optimum — NOT-PASSED (PyPhi monotone 0.351→0.393)"
  ]
  meta_finding = [
    "anima Φ★ proxy direction-sensitivity 한계 — 2/3 scenarios MISMATCH IIT 3.0"
  ]

# ─── PARTIAL inventory (mixed evidence) ──────────────────────────────

@N partial_inventory := "PARTIAL entries (mixed evidence)" :: catalog [active]
  a_batch_partial = [
    "Hc_1281 Stage 1 math partial",
    "H_184 V8 M-family math-structure axis (PARTIAL INSUFFICIENT-FOR-STAGE-1)",
    "H_190 law-CA embedding mathematical family",
    "H_188 PCI clinical deferred (external data)",
    "H_191 Kuramoto deep numerology (sub-claims separated)",
    "Hc_1276/77/78/84 H_191 cascade (resolved per cycle)"
  ]
  b_batch_partial = [
    "H_006 coupled oscillator (Kuramoto universal, n=6 specialness 부재)",
    "H_017 MKx G1/G4 gate criteria",
    "H_172 alpha 0.014 modulation depth (voice D unknown)"
  ]

# ─── INSUFFICIENT + DEFERRED ─────────────────────────────────────────

@N insufficient_inventory := "INSUFFICIENT + DEFERRED entries" :: catalog [active]
  insufficient = [
    "H_007 cellular automaton (CA Rule sweep separate)",
    "H_008 dissipative structure (Prigogine non-eq thermo)",
    "H_009 Fisher info geometry (별도 cycle)",
    "H_010 holographic consciousness (analogical AdS/CFT)",
    "H_012 autopoietic network (self-production formal model 부재)",
    "H_165 11d hypercube (D=2048 phi_star aliasing)",
    "H_177 topo10-20 substrate (D=1024 aliasing)"
  ]
  deferred = [
    "H_013 longitudinal EEG (hardware)",
    "H_014 CLM EEG LZ76 (anima-eeg-core hardware)",
    "H_015 CLM EEG gamma-theta (hardware)",
    "H_188 PCI clinical (external dataset)"
  ]

# ─── Cross-references ────────────────────────────────────────────────

@X main_tape := "MAIN.tape" :: ssot [active]
  cross_link = "verdict 4-class SSOT — 본 HYPOTHESIS.tape 의 verdict source"

@X axis_tape := "AXIS.tape" :: cluster [active]
  cross_link = "MAIN.tape SUPPORTED-tier 9-axis 재구성 — 본 HYPOTHESIS.tape supported_inventory 와 동일 32 entries"

@X philosophy_tape := "PHILOSOPHY.tape" :: append-only-ledger [active]
  cross_link = "verdict cycle ledger entries — append-only"

@X verify_tape := "VERIFY.tape" :: protocol [active]
  cross_link = "3-stage verification protocol"

@X index_md := "INDEX.md" :: navigation [active]
  cross_link = "root SSOT navigation — 4 tape (MAIN/AXIS/HYPOTHESIS/PHILOSOPHY) integrated"
