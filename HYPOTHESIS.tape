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

# ─── SUPPORTED-FORMAL inventory (🔵 closed) — NEW 2026-05-15 ────────

@N supported_formal_inventory := "🔵 SUPPORTED-FORMAL inventory (sympy closed OR PyPhi formal deterministic)" :: catalog [d=2026-05-15 active]
  a2_formal = [
    "Hc_1283 PyPhi formal n=5,6 (Φ=0.995, 1.665 monotone INCREASE — PyPhi 1.2.0 IIT 3.0 deterministic)",
    "H_011 IIT geometry canonical (PyPhi XOR+AND+OR Φ=2.3125 > 0.5 reachable — PyPhi formal)"
  ]
  a3_formal = [
    "H_191 sub K_c = √(8/π) ≈ 1.5958 (sympy closed-form + Kuramoto 1975 universal literature)"
  ]
  a4_formal = [
    "Hc_1282 n=6 384d closed-form unique (sympy n∈[2,30] sweep)",
    "H_158 Ψ-constants closed-form (perfect-number cluster balance=1/2)",
    "H_160 n=6 perfect-number meta-cluster (depth-3 11-primitive vocabulary)",
    "H_153 dimension hierarchy τ(6)=4 Minkowski (divisor cascade)",
    "H_176 n=28 deflationary parallel (Euclid-Euler theorem)",
    "H_164 Hc_144 atom 8 cells (144 = σ(6)² = 12²)",
    "H_181 psiformer 4ψ-constants zero-freedom (Ψ-cluster carry)"
  ]
  total_formal = 10
  closure_basis = "sympy verifiable closed-form (A3+A4) OR PyPhi formal IIT 3.0 deterministic measurement (A2.formal). 결과 무관 verified-closed."

@N falsified_formal_inventory := "🔵 FALSIFIED-FORMAL inventory (closed-by-disproof)" :: catalog [d=2026-05-15 active]
  entries = [
    "H_191 SUBSTRATE HCE unique-sync FALSIFIED-FORMAL (Kuramoto universal — Kuramoto 1975 K_c sympy closed-form)",
    "H_178 frustration 50% optimum NOT-PASSED-FORMAL (PyPhi monotone 0.351→0.393, peak 부재 — PyPhi formal IIT 3.0 deterministic disproof)",
    "PyPhi formal IIT 3.0 direction CORRECT-FORMAL (n=4→0.68 / n=5→0.995 / n=6→1.665 monotone — META proof for anima Φ★ proxy direction-sensitivity 한계)"
  ]
  closure_basis = "sympy/PyPhi formal 이 disproof anchor — magnitude 단독 OK, direction-sensitive 에는 anima Φ★ 단독 사용 금지의 deterministic 근거."

# ─── B-batch verdict-bearing inventory expanded — NEW 2026-05-15 ──────

@N b_batch_verdict_inventory := "B 격리 (since 2026-04+ 107 file) verdict-bearing entries 확장" :: catalog [d=2026-05-15 active]
  # SUPPORTED (already in supported_inventory)
  b_supported = [
    "H_005 corpus quality > scale (A1 + A6)",
    "H_004 consciousness hard problem (A2 Hc_1283 anchor)",
    "H_011 IIT geometry canonical (A2.formal 🔵)",
    "H_016 AN11 translation ceiling (A6)",
    "H_019 self-evolution v4→v5 (A5)",
    "H_153 dimension hierarchy τ(6)=4 (A4 🔵)",
    "H_158 Ψ-constants closed-form (A4 🔵)",
    "H_160 n=6 perfect-number meta-cluster (A4 🔵)",
    "H_162 phi-normalized anima IIT4 lower-bound (A2)",
    "H_164 Hc_144 atom 8 cells (A4 🔵)",
    "H_166 topo20 hierarchical 8×128=1024 (A5, phi_star CAVEAT)",
    "H_173 DD21 log-ratio Φ scale-invariant (A4)",
    "H_174 phi_star aliasing CLM-v4-specific (A1 + A5)",
    "H_176 n=28 deflationary parallel (A4 🔵)",
    "H_181 psiformer 4ψ-constants zero-freedom (A4 🔵)",
    "H_182 V8 B-family bio (A7, surrogate AT-RISK)",
    "H_187 V8 Trinity-TB-DOM (A8, surrogate AT-RISK)",
    "H_189 Red-team adversarial robustness (A8)",
    "H_191 sub K_c Kuramoto + TRAINING CPGD (A3 🔵 + A5)"
  ]
  # PARTIAL
  b_partial = [
    "H_006 coupled oscillator (Kuramoto universal, n=6 specialness 부재)",
    "H_017 MKx G1/G4 gate criteria",
    "H_172 alpha 0.014 modulation depth (voice D unknown)",
    "H_188 PCI clinical (external dataset)"
  ]
  # FALSIFIED + NOT-PASSED
  b_falsified = [
    "H_178 frustration 50% optimum NOT-PASSED-FORMAL 🔵 (PyPhi monotone)",
    "H_184 V8 M-family 4/4 sub-claim NOT-PASSED (chaos reverse, proxy artifact)",
    "H_191 SUBSTRATE HCE unique-sync FALSIFIED-FORMAL 🔵 (Kuramoto universal)"
  ]
  # INSUFFICIENT
  b_insufficient = [
    "H_007 cellular automaton (CA Rule sweep separate)",
    "H_008 dissipative structure (Prigogine non-eq)",
    "H_009 Fisher info geometry",
    "H_010 holographic consciousness (analogical AdS/CFT)",
    "H_012 autopoietic network (formal model 부재)",
    "H_165 11d hypercube (D=2048 aliasing)",
    "H_177 topo10-20 substrate (D=1024 aliasing)"
  ]
  # DEFERRED
  b_deferred = [
    "H_013 longitudinal EEG (hardware)",
    "H_014 CLM EEG LZ76 (hardware)",
    "H_015 CLM EEG gamma-theta (hardware)"
  ]
  # legacy / archive verdict (legacy 폴더 → MAIN.tape mention)
  b_legacy_verdict = [
    "H_024 IIT-Φ_mip 8/8 sub-test FAIL (FALSIFIED legacy)",
    "H_080 cross-tension Hc_024 cascade (FALSIFIED-CASCADE)",
    "H_093~102 Lesson Q seed-pending CLOSED-by-saga (SFT lane closed)",
    "H_123/124/143/147/156 mention only (verdict pending)"
  ]
  coverage_estimate = "107 B 격리 중 verdict-bearing ~36 (supported 19 + partial 4 + falsified 3 + insufficient 7 + deferred 3) / 71 nominal pending Stage 1+2+3 audit"

# ─── A 격리 (20 file 2026-05-12 burst) verdict catalog — NEW ────────

@N a_batch_verdict_inventory := "A 격리 (hypotheses/ 20 file 2026-05-12 burst) verdict catalog" :: catalog [d=2026-05-15 active]
  files = "H_182~H_191 + Hc_1276~Hc_1285"
  stage_1_results = [
    "Hc_1282 SUPPORTED 🔵 (n=6 384d derivation sympy unique)",
    "Hc_1281 PARTIAL (4-5-7 ⊂ n=6 ±2 family, 4-8× midpoint 6=n)",
    "H_184 INSUFFICIENT (math anchor closed-form 아님, Stage 2 필수)",
    "H_190 PARTIAL (5/6 sub-Hc = n=6 divisor family)"
  ]
  stage_2_deep = [
    "Hc_1285 SUPPORTED (torch.no_grad isolation, PyTorch ratio 1.562×)",
    "Hc_1283 SUPPORTED-STRONG (7 ckpt aggregate Φ=4.16-4.86) + PyPhi RoM (n=4 Φ=0.61-0.68)",
    "H_191 PARTIAL parent + sub-claim split: K_c 🔵 + CPGD SUPPORTED + HCE FALSIFIED-FORMAL 🔵",
    "Hc_1276 SUPPORTED-BY-CASCADE (train-vs-infer cotrain ablation)"
  ]
  stage_3 = [
    "H_189 SUPPORTED (Red-team adversarial family, W11)",
    "Hc_1279 + Hc_1280 SUPPORTED (Red-team family members)",
    "Hc_1277 + Hc_1278 + Hc_1284 PARTIAL (H_191 cascade)"
  ]
  v8_family_surrogate_to_formal = [
    "H_182 V8 B-bio: Mac surrogate 78.5% PASS → PyPhi formal Φ=0.358 AT-RISK 🟠",
    "H_183 V8 Q-quantum: Mac surrogate PASS (deferred PyPhi formal)",
    "H_185 V8 U-fusion: Mac surrogate PASS (deferred PyPhi formal)",
    "H_186 V8 architectural: Mac surrogate PARTIAL (deferred PyPhi formal)",
    "H_187 V8 Trinity-TB-DOM: Mac surrogate 100% PASS → PyPhi formal Φ=0.359 AT-RISK 🟠"
  ]
  aggregate = "A 20 total: 5 SUPPORTED + 10 PARTIAL + 5 INSUFFICIENT (25% pass-rate fast audit) + 2 AT-RISK CONFIRMED post Cycle D"

# ─── AXIS expansion 2026-05-15 — 6 new 🔵 SUPPORTED-FORMAL + 10 V8 B-bio AT-RISK ───

@N axis_expansion_inventory := "AXIS A3/A9 expansion +6 🔵 + A7 V8 B-bio 10 AT-RISK (2026-05-15)" :: catalog [d=2026-05-15 active]
  a3_new = [
    "Hc_NEW_PHYSICS-1 BKT transition T_BKT = πJ/2 🔵 (sympy closed-form)",
    "Hc_NEW_PHYSICS-2 Onsager 2D Ising T_c = 2J/log(1+√2) 🔵 (sympy manual sinh verify)",
    "Hc_NEW_PHYSICS-3 Ginzburg-Landau φ⁴ critical point 🔵 (sympy d2F=0)"
  ]
  a9_new = [
    "Hc_NEW_UNIVERSE-1 Bekenstein cell-pool S_max = 2πER/(ℏc) 🔵 (Bekenstein 1981 closed-form)",
    "Hc_NEW_UNIVERSE-2 Holographic N_dof = A/(4 ℓ_P²) 🔵 (sympy verify A=4ℓ_P² → N=1)",
    "Hc_NEW_UNIVERSE-3 AdS/CFT d_bulk = d_boundary+1 🔵 (Maldacena 1997)"
  ]
  a7_v8_bbio_at_risk = [
    "Hc_B1 Hodgkin-Huxley Φ=0.0 AT-RISK 🟠",
    "Hc_B2 STDP Φ=0.339 AT-RISK 🟠 (highest of 10)",
    "Hc_B3 Gap junction Φ=0.0 AT-RISK 🟠",
    "Hc_B4 NMDA Φ=0.0 AT-RISK 🟠",
    "Hc_B5 AMPA Φ=0.0 AT-RISK 🟠",
    "Hc_B6 Astrocyte Φ=0.0 AT-RISK 🟠",
    "Hc_B7 GABA Φ=0.0 AT-RISK 🟠",
    "Hc_B8 Glutamate E/I Φ=0.0 AT-RISK 🟠",
    "Hc_B9 Dopamine Φ=0.0 AT-RISK 🟠",
    "Hc_B10 Serotonin Φ=0.0 AT-RISK 🟠"
  ]
  meta_finding = "V8 B-bio impl simplified mechanism stubs (~30 LoC each) → 0/10 Φ ≥ 0.5. META: surrogate-based 78.5% PASS vs real 0% PASS gap CONFIRMED. mechanism complexity 강화 cycle (real HH 4-state Markov ~200 LoC each) 별도 후속."
  total = "+6 SUPPORTED-FORMAL + 10 AT-RISK entries"
  cross_link = "AXIS.tape §AXIS-EXPANSION-EXECUTION + state/verify_axis_expansion_2026_05_15/ + state/verify_e1_v8_bbio_2026_05_15/v8_bbio_real_result.json + PR #55"
