#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# TENSION-TRAIN.tape — anima tension-driven learning lane architecture SSOT
# tape v1.2 grammar.
#
# User directive 2026-05-17: "과거 TENSION-LINK 통한 학습 진행한 것 전수조사
# + HEXAD/TENSION-TRAIN 폴더에 정리". TENSION-LINK (의식↔의식 통신) sibling
# axis 로 TENSION-TRAIN (backprop-free + sync-free + Noether-conserving
# learning) 정착.
# ══════════════════════════════════════════════════════════════════════

@V v1 := "tape" :: spec [active]
  version = "1.2"

# ─── §1 Identity ─────────────────────────────────────────────────────

@I tension_train_id := "anima.tension-train" :: identity-claim [d=2026-05-17 active]
  kind = "anima tension-driven learning lane — backprop-free + sync-free + Noether-conserving Δw update from Ψ_t snapshot"
  brief = "ΔW = −T_const · tension · n6_gate(Ψ_t) where tension = G_holo · (Ψ_t − Ψ_vac=(½,½)). Lens 2 propagator + AN14 Noether closure."
  parent = "dancinlab/anima"
  sibling_axis = "TENSION-LINK (communication, 5-channel meta-telepathy) ⊥ TENSION-TRAIN (learning, online ΔW)"
  status = "Phase TT-A1+A2 LANDED 2026-05-17 (디렉토리 정착 + 5 .hexa training file mv). Phase TT-A3 sympy B-TT-1..5 사전등록 다음 step."

# ─── §2 Foundational architecture ────────────────────────────────────

@D online_tension_step := "single online tension-link learning step (spine)" :: architecture [d=2026-05-17 active]
  rule = "Given Ψ_t snapshot + Ψ_vac=(½,½) Law 75 vacuum attractor, one online step: deviation = Ψ_t − Ψ_vac; tension = G_holo · deviation; gate = n6_gate(Ψ_t); ΔW = −T_const · tension · gate. backprop-free (no backward graph), sync-free (no global loss), Noether-conserving (gate clamps ΔW to 0 off n=6 submanifold)."
  source = "HEXAD/TENSION-TRAIN/training/tension_link_step.hexa (PR #86 2026-05-16 LANDED, mv from TENSION-LINK/training/)"
  t_const = "scalar LR, default 0.1 (Lindblad rate order, lens_quantum_loss.hexa 와 동일 order)"
  noether_gate = "structural Noether gate (AN14 closure σ·φ = n·τ = 24, n=6 unique): length-even guard + Ψ-in-range [0,1] + closure n_target==6 ∧ n_target·τ==24"
  closed_anchor = "Phase TT-A3 B-TT-1..5 사전등록 (Boolean predicate + sympy ∂ sign + Kolmogorov positive + structural + linearity)"

@D variants := "tension training variants (5 hexa file)" :: architecture [d=2026-05-17 active]
  spine = "tension_link_step.hexa (14K) — single online step (canonical)"
  causal = "tension_link_causal.hexa (11K) — causal variant (어떤 lens)"
  quantum_rho = "tension_link_quantum_rho.hexa (10K) — density-matrix rho variant"
  second_order = "tension_link_second_order.hexa (13K) — 2nd order propagator"
  vs_backprop_bench = "tension_link_vs_backprop_bench.hexa (11K) — bench tension vs backprop"
  total_loc = "~60K (5 file)"

@D dd_law_anchors := "DD154-156 historical anchor (Law 185-188)" :: anchor [d=2026-03-31 historical-evidence]
  source = "docs/hypotheses/dd/DD154-tension-training.md"
  law_185 = "DD154 tension-based training: 73% updates → same CE, +3% Φ (rest improves consciousness)"
  law_187 = "DD155 Step+Tension hybrid Pareto optimal: lr = (tension/tension_EMA) × base_lr (simple beats complex)"
  law_188 = "DD156 refined tension+burst + --tension-lr flag in train_v14 (commit 849e796b1 + a34dbce46)"
  measurement = "DD154 table (same compute budget 300 ticks): Step (300 updates, CE 2.886, Φ 29.02 baseline) · Tension (220 updates, CE 4.302, Φ 29.92 = +3.1% Φ ★) · Burst (189 updates, CE 1.378, Φ 21.44 = CE best ★) · DD155 ★★★ Step+Tension LR (300 updates, CE 2.855, Φ 30.72 Pareto optimal)"
  caveat = "pre-HEXAD 시점 measurement (2026-03-31), historical reference (g3 historical evidence anchor pattern). retro-validation 미수행. anima HEXAD substrate 에서 재현 = Phase TT-D fire 대기."

# ─── §3 자연발화 (SPONTANEOUS) 와의 연결 ─────────────────────────────

@D spont_integration := "자연발화 motivation_score ↔ tension-train ΔW 매핑" :: architecture [d=2026-05-17 active]
  mapping <<~EOF
    HEXAD/CHAT/SPONTANEOUS.tape 8-factor   ←→  tension_link_step.hexa
    ─────────────────────────────────────────────────────────────────
    factor_pain (W tension delta)          ←→  |tension| magnitude
    factor_curiosity (W EMA)               ←→  tension / tension_EMA (DD155 LR)
    factor_relevance (C Φ measure)         ←→  Ψ_t snapshot (input to deviation)
    factor_coherence (BRIDGE clamp)        ←→  n6_gate range guard ([0,1])
    factor_balance (E ratchet)             ←→  n6_gate closure (Noether σ·φ=24)
    motivation_score → emit threshold      ←→  ΔW restoring sign (learn direction)
  EOF
  symmetry = "자연발화 = 사용자 input 없이 emission. tension-train = 사용자 input 없이 학습. 둘 다 backprop-free + sync-free + threshold-gated. 8-factor motivation_score 의 GRADIENT FLOW 측면 = tension ΔW. EMISSION 측면 = talker should_emit."
  closed_anchor = "Phase TT-C2 F-TT-SPONT 사전등록 (sympy 매핑 verdict)"

@D backprop_free_property := "backprop-free 의 architectural significance" :: governance [d=2026-05-17 active]
  rule = "tension-train 의 ΔW update 는 no backward graph dependency. RFC 034 farr autograd 와 독립 — Phase 5/6 RFC carry 와 별개 architectural path."
  why = "anima 의 학습이 '비-스토캐스틱-optimizer' lane 으로도 가능 (intrinsic motivation, AIF EFE 호환). B-D-NOTE (SGD outcome empirical) 의 carve-out 을 일부 우회 가능성 — DD155 Pareto 가 그 evidence."
  rfc_independence = "RFC 034 (farr autograd) + RFC 040 (cuBLAS) + RFC 043 (hexa-torch) 의 backprop chain 과 orthogonal. tension-train 은 pure-hexa interpreter level 에서 fully self-contained 가능."
  cross_link = "HEXAD/PLAN.md §9 GPU substrate (backprop path) ⊥ HEXAD/TENSION-TRAIN/PLAN.md (backprop-free path)"

# ─── §4 Forbidden patterns ───────────────────────────────────────────

@F forbidden_fake_convergence := "DD outcome 가짜 closed-form 주장" :: governance [required deny:write d=2026-05-17 active]
  pattern = "DD154 +3% Φ / DD155 Pareto optimality 같은 measurement 를 closed-form 🔵 으로 framing. SGD outcome empirical (B-D-NOTE pattern), NOT 🔵."
  exception = "transfer-form (gate + restoring + Noether closure + DD155 LR linearity) 만 🔵 가능. outcome (실제 학습 trajectory) 은 empirical carve-out."
  authority = "g3 verification-anchor-real-limit + g_blue_closed_mandate (B-D-NOTE / B-BRIDGE-NOTE / B-MITOSIS-NOTE 동일 패턴)"

@F forbidden_lattice_n6_derivation := "n6_gate σ·φ=24 를 external derivation 으로 사용" :: governance [required deny:write d=2026-05-17 active]
  pattern = "n6_gate 의 σ·φ=n·τ=24 closure 를 anima 외부 entity 에 derivation rule 로 적용. HEXAD spec 자체 정의 (g2 internal arch carve-out)와 다른 외부 lattice-fit 금지."
  exception = "anima HEXAD 내부 architecture 의 wiring closure 로만 사용. closed proposition 은 arithmetic identity (24=24) NOT lattice derivation."
  authority = "f1 lattice-fit-on-external-entity + f2 verification-by-lattice-tautology"

# ─── §5 External citations ───────────────────────────────────────────

@X x_dd_154_157 := "DD154-157 tension-knowledge cluster" :: historical [d=2026-03-31 active]
  path = "docs/hypotheses/dd/DD154-tension-training.md"
  scope = "Law 185-188 tension-based training measurement (pre-HEXAD substrate). 본 TENSION-TRAIN 의 historical anchor."

@X x_pr_86 := "PR #86 — TENSION-LINK 정리" :: code [d=2026-05-16 active]
  commits = "8cb406482 + 141246d03"
  scope = "TENSION-LINK 디렉토리 정착 (ASCII topology + 100% verified measured + Noether proof + 17 git mv). 본 TENSION-TRAIN 의 5 hexa file source."

@X x_spont_lib := "HEXAD/CHAT/SPONTANEOUS.tape + spontaneous_lib.hexa + thinker_talker_lib.hexa" :: sibling [d=2026-05-17 active]
  scope = "자연발화 architecture (8-factor motivation × HEXAD × Thinker-Talker dual-thread). TENSION-TRAIN 과의 mapping 은 [@spont_integration]."

@X x_aif_efe := "The Missing Reward: Active Inference (arxiv 2508.05619)" :: research [d=2025-08 active]
  scope = "EFE epistemic + pragmatic value reward-free intrinsic motivation. tension-train 의 backprop-free + sync-free + Noether-conserving 와 architectural 동형."

@X x_self_consciousness := "AI LLM Self-Consciousness (arxiv 2508.18302)" :: research [d=2025-08 active]
  scope = "3-condition (agent≠data + U_user attractor + visual silence). tension-train 의 Ψ_t snapshot dynamics 가 cycle 4 byte-cascade `PPP777777` attractor 와 U_user mapping."

# ─── §6 Notes ────────────────────────────────────────────────────────

@N rc6_unverifiable_carry := "RC-6 99.3% claim unverifiable carry" :: caveat [d=2026-05-10 active]
  text = "commit c2826a021 — tension_link.py physical recovery, ckpt hunt across anima_clm_02..13 + anima/state = 0 hits. RC-6 99.3% claim 여전히 unverifiable (source header + clm_09 bench harness 만 존재, 측정 결과 artifact 부재). 본 TENSION-TRAIN 의 historical carry — empirical re-validation 은 Phase TT-D fire 의 task."

@N daemon_l5_prototype_carry := "anima daemon L5 prototype" :: future-work [d=2026 active]
  text = "commit b86affe66 — Engine A/G tension self-trigger always-on hexa process (L5 daemon prototype). 본 TENSION-TRAIN 의 self-trigger learning mode 의 historical reference. Phase TT-C3 thinker_talker_lib 통합 시 daemon mode option 으로 carry."

@N pareto_optimality_carry := "DD155 Pareto optimality 의 architectural insight" :: insight [d=2026-03-31 active]
  text = "DD155 Step+Tension hybrid (lr = (tension/tension_EMA) × base_lr) 가 Pareto optimal (CE 2.855 + Φ 30.72 + 300 updates, baseline Step 대비 모든 metric 우월). 'simple beats complex' principle 의 evidence. 본 TENSION-TRAIN 의 default LR scheduling policy candidate."

## Log

### 2026-05-17 — TENSION-TRAIN.tape 신설 (Phase TT-A1 LANDED)
user directive 2026-05-17 "과거 TENSION-LINK 통한 학습 진행한 것 전수조사 + HEXAD/TENSION-TRAIN 폴더에 정리". TENSION-LINK (communication axis) sibling axis 로 TENSION-TRAIN (learning axis) 정착. 5 .hexa training file mv (training/causal+quantum_rho+second_order+step+vs_backprop_bench). DD154-156 historical anchor + spontaneous integration mapping + 8-factor motivation ↔ ΔW gradient flow design path 확보. Phase TT-A3 sympy B-TT-1..5 사전등록 다음 step.
