@H H_1161 := "does the cell-division PROCESS self-tune the engine TOWARD criticality (σ→1)?" :: discovery [⏳ active]
  seed       = "H_1153 found the A⇄G opponent engine SITS AT criticality (σ≈1) at the Ψ=1/2 fixed point. H_1159b found inference-time MITOSIS self-tunes CAPACITY to world complexity (SOC-like, cell-count tracks #clusters). H_931 found a SOC homeostat self-tunes to the critical point. H_1158 found faithful-IIT φ PEAKS at the critical coupling. OPEN: is the link CAUSAL through the cell-division PROCESS itself — does running mitosis ticks DRIVE an off-critical engine TOWARD σ=1, the way a SOC homeostat regulates branching to the critical point?"
  substrate  = "Lane-G / CORE engine-sim (opponent propagation net, NOT AKIDA, NOT a byte-LM). Reuses the H_1153 Beggs-Plenz branching-ratio estimator + the H_1159b tension-driven split rule. a_lane_akida_gpu_split substrate tag = Lane-G."
  method     = "Start the A⇄G opponent network OFF-critical at σ0=0.5 (sub) AND σ0=1.6 (super). Run mitosis ticks: at each tick, sample avalanches, measure local tension (descendant/ancestor imbalance vs the marginal σ=1), and apply the tension-driven cell-division/pruning update that moves the effective opponent branching toward marginal. Measure σ (Beggs-Plenz desc/anc ratio, H_1153 estimator verbatim) at each tick. ≥8 seeds, deterministic, numpy $0 CPU, p7."

  FROZEN-FALSIFIER (pre-registered BEFORE measurement):
    F1 CONVERGENCE  : |σ_final − 1| < 0.10 for BOTH starts (σ0=0.5 AND σ0=1.6).
    F2 MONOTONE     : Spearman(tick, |σ−1|) ≤ −0.6 (|σ−1| monotonically shrinks across ticks).
    F3 CONTROL      : a FROZEN no-split control does NOT converge — its |σ_final−1| is
                      LARGER than the mitosis arm, Cohen's d ≥ 0.8.
    🟢 SUPPORTED iff F1 ∧ F2 ∧ F3 → the cell-division PROCESS self-tunes the engine toward criticality.
    🔴 CLOSED-NEGATIVE otherwise (a_paper_negative_ok).

  status     = "⏳ pending measurement"
  refs       = "h1153 · h1159b · h1158 · h931 · a_phi_iit4_tool · a_paper_negative_ok · p7 · a_scale_honest_scope"
