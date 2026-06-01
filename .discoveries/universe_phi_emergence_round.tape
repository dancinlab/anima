@V := "tape" :: spec [active]
  version = "1.0"

# UNIVERSE domain — phi↔emergence hypothesis-generation round (2026-06-02)
#
# seed: H_912 lineage — cheap variance-phi_proxy ⊥ real emergence (FALSIFIED,
#   r=-0.277, perm p=0.962, "proxy pathology", X⊥Φ signature) vs H_288 faithful
#   big-Φ ∥ LZ-complexity (SUPPORTED, r=0.831). The gap between a Φ-PROXY and a
#   faithful causal big-Φ is the generator. Brainstorm-to-depletion (8 rounds,
#   depletion at round 8) → 14 surviving falsifiable candidates Hc_1286..Hc_1299.
# honesty: candidate-UNVERIFIED. Each carries a PRE-REGISTERED falsifier + a real
#   $0 mac-local measurement path (hexa, HEXAD/IIT4/lib reuse). NO hexa verify run,
#   NO tier claimed (generation only). 4 ideas DROPPED for circularity/dup.
# flow: discovery -> hypotheses_candidates/Hc_*.md -> (future) /cycle verify.

@N uni_proxy_faithful_ladder := "proxy↔faithful big-Φ agreement is a function of N" :: discovery [d=2026-06-02 active]
  id     = "Hc_1286"
  seed   = "H_912 single-scale proxy⊥emergence + H_288 faithful∥LZ — agreement vs N never laddered"
  method = "r(phi_proxy, big_Φ) across N=3..8, ECA panel, exact n≤8"
  falsifier = "r(N) non-monotone OR flat-noise (|Δr|<0.1 all rungs) → FALSIFIED"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL (monotone ladder) | 🔴 CLOSED-NEGATIVE"

@N uni_proxy_residual_selfsim := "phi_proxy↔faithful residual predicted by self-similarity" :: discovery [d=2026-06-02 active]
  id     = "Hc_1287"
  seed   = "H_288 L3 rule90 self-similar LZ over-prediction witness → generalize to residual law"
  method = "residual = LZ_norm − Φ_norm vs box-counting fractal-dim / LZ-self-affinity"
  falsifier = "r(self_sim, residual) < 0.5 → FALSIFIED (over-prediction not self-sim-predicted)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE"

@N uni_proxy_variance_artifact := "phi_proxy measures raw state-variance, not integration (partial-corr diagnosis)" :: discovery [d=2026-06-02 active]
  id     = "Hc_1288"
  seed   = "H_912 root-cause — WHY proxy⊥emergence; variance-confound hypothesis"
  method = "partial correlation r(phi_proxy, emergence | state_variance); big_Φ as control"
  falsifier = "|r(proxy,emergence|variance)| ≥ 0.3 → FALSIFIED (proxy has signal beyond variance)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE"

@N uni_causal_emergence_ei := "Hoel causal emergence — EI_macro > EI_micro, EI-gain ∥ big-Φ" :: discovery [d=2026-06-02 active]
  id     = "Hc_1289"
  seed   = "emergence operationalized via Hoel effective-information (orthogonal to Bedau H_219)"
  method = "coarse-grain ECA TPM, do-intervention EI macro vs micro; EI_gain vs big_Φ"
  falsifier = "EI_macro ≤ EI_micro all rules/grains → FALSIFIED (no causal-emergence in ECA)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)"

@N uni_predictive_information_phi := "faithful big-Φ ∥ predictive information (excess entropy)" :: discovery [d=2026-06-02 active]
  id     = "Hc_1290"
  seed   = "info-measure arc 4th face — Shannon⊥(H_287) LZ∥(H_288) TE∥(H_290) → excess entropy E=I(past;future)"
  method = "block-entropy → excess entropy vs big_Φ, 10-rule panel; distinct-from-Shannon gate"
  falsifier = "r(excess_entropy, big_Φ) < 0.5 → FALSIFIED (predictive info in Shannon class)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE"

@N uni_statistical_complexity_phi := "big-Φ tracks statistical complexity Cμ (ε-machine) ≥ LZ; resolves rule90 over-prediction" :: discovery [d=2026-06-02 active]
  id     = "Hc_1291"
  seed   = "complexity 3rd face — Crutchfield Cμ (causal-state memory) vs LZ (H_288 rule90 residual)"
  method = "ε-machine (CSSR-lite) Cμ vs big_Φ + LZ on same panel; rule90 Cμ check; coin-anchor"
  falsifier = "r(Cμ,Φ) < r(LZ,Φ)−0.1 → FALSIFIED (Cμ tracks worse than LZ)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE"

@N uni_dissipation_rate_phi := "big-Φ ∥ entropy-production rate (dissipation) — consciousness↔thermodynamics quantitative" :: discovery [d=2026-06-02 active]
  id     = "Hc_1292"
  seed   = "H_008/Hc_409 thermo qualitative — dissipation RATE ↔ faithful Φ correlation unmeasured"
  method = "forward/backward TPM asymmetry → entropy-production rate vs big_Φ; reversible anchor"
  falsifier = "r(dissipation_rate, big_Φ) < 0.5 → FALSIFIED (dissipation ⊥ Φ)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)"

@N uni_phi_inverse_u_gradient := "big-Φ inverse-U over energy-gradient (drive) — thermodynamic edge-of-chaos" :: discovery [d=2026-06-02 active]
  id     = "Hc_1293"
  seed   = "H_204/H_285 inverse-U over λ/closure (internal) — DRIVE-axis inverse-U unmeasured"
  method = "bias-field drive g sweep → forward-TPM; Φ(g) curve, interior-peak unimodality"
  falsifier = "Φ(g) monotone OR flat OR peak at endpoint → FALSIFIED (no drive-axis inverse-U)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE"

@N uni_soc_branching_phi_peak := "SOC substrate big-Φ peaks at branching ratio σ=1 (self-tuned criticality)" :: discovery [d=2026-06-02 active]
  id     = "Hc_1294"
  seed   = "H_251/H_285 externally-tuned criticality — SOC (no-knob, branching σ) unmeasured; critical-brain"
  method = "branching-process substrate σ-sweep {0.7..1.3}; Φ(σ) peak at σ≈1, dead-anchor"
  falsifier = "argmax Φ(σ) outside σ=1±0.15 → FALSIFIED (SOC criticality ≠ Φ peak)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE"

@N uni_criticality_not_sufficient := "criticality is necessary not sufficient for Φ — power-law-avalanche but Φ=0 witness (X⊥Φ)" :: discovery [d=2026-06-02 active]
  id     = "Hc_1295"
  seed   = "H_288 rule90 (LZ but Φ=0) generalized to criticality axis; X⊥Φ signature"
  method = "branching substrate with power-law avalanche (KS-validated) + big_Φ; hunt Φ=0 witness"
  falsifier = "all critical substrates Φ>0 → H1(criticality⇒Φ) SUPPORTED, witness absent"
  verdict_tier_target = "🔴 CLOSED-NEGATIVE (witness found, publishable) | 🟢 SUPPORTED"

@N uni_combination_threshold := "combination problem — micro→macro Φ smooth-accumulation(panpsychist) vs threshold-jump(emergentist)" :: discovery [d=2026-06-02 active]
  id     = "Hc_1296"
  seed   = "H_204 panpsychism existence + H_609 collective-agents — single-substrate micro→macro combination unmeasured"
  method = "N (or coupling-density) sweep; big-Φ(N) continuity vs discontinuous threshold jump"
  falsifier = "continuous monotone accumulation → emergentist FALSIFIED; threshold jump → panpsychist FALSIFIED"
  verdict_tier_target = "🟢 SUPPORTED (either pattern resolves split) | 🔴 NEITHER (null)"

@N uni_link_substrate_independence := "Φ→emergence MAPPING substrate-independent? matched-Φ → matched-emergence across families" :: discovery [d=2026-06-02 active]
  id     = "Hc_1297"
  seed   = "H_011/H_022 Φ-value multi-realizability + H_670 ordering — the LINK's substrate-transfer unmeasured"
  method = "matched-Φ controlled pairs across ECA vs random Boolean net; |Δemergence| matched vs unmatched"
  falsifier = "matched-Φ |Δemergence| not < unmatched-Φ |Δemergence| → FALSIFIED (link substrate-dependent)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL | 🔴 CLOSED-NEGATIVE"

@N uni_correlation_scale_ladder := "Φ↔emergence correlation r itself is a function of N — H_288 single n=4 → ≥3-rung ladder" :: discovery [d=2026-06-02 active]
  id     = "Hc_1298"
  seed   = "H_288 r=0.831 single n=4 point; a_scale_honest_scope demands ≥3-rung ladder; H_002 C2 scale-variant lesson"
  method = "r_N = r(big_Φ, LZ_norm) at N=4..8 (exact); scale-stable vs scale-variant"
  falsifier = "any rung r_N<0.5 OR |r_8−r_4| ≥ 0.2 → FALSIFIED (H_288 scale-variant, re-scope)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL (scale-stable) | 🔴 CLOSED-NEGATIVE (scale-variant)"

@N uni_phi_density_fine_tuning := "high-Φ substrates rare in rule-space? 256-rule full Φ-density census — fine-tuning cosmology analogue" :: discovery [d=2026-06-02 active]
  id     = "Hc_1299"
  seed   = "H_654/H_668 class-level profile + H_002 fine-tuning — full 256-rule Φ-density census never run"
  method = "256-rule exhaustive big-Φ census (n=4 exact); high-Φ fraction; Wolfram-class consistency"
  falsifier = "high-Φ fraction ≥ 0.5 → FALSIFIED (integration common, not fine-tuned)"
  verdict_tier_target = "🟢 SUPPORTED-NUMERICAL (rare/fine-tuned) | 🔴 CLOSED-NEGATIVE (common)"

@N uni_dropped_for_circularity_dup := "ideas DROPPED — circular, unfalsifiable, or duplicate of existing H" :: audit [d=2026-06-02 active]
  drop_downward_causation = "downward-causation macro-intervention — DUP of H_219/H_227/Hc_607 (Bedau forward-pass)"
  drop_landauer_irrev     = "Landauer/irreversibility ↔ Φ — DUP of H_036/H_008/H_037 (already filed)"
  drop_observer_cut       = "observer-relative Φ / boundary-cut frame-dependence — DUP of H_295/H_296/H_286 (exclusion/MIP-pathology)"
  drop_rg_flow_phi        = "RG-flow of Φ — redundant: faithful coarse-grain version IS Hc_1289 (causal-emergence); H_050 covers RG"
  note = "4 distinct ideas dropped (no padding). Circularity guard also rejected any emergence-axis defined identically to Φ (tautology)."
