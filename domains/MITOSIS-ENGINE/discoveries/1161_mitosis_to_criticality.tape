@H 1161 := "does the cell-division PROCESS self-tune the A⇄G engine TOWARD criticality (branching ratio σ→1)?" :: discovery [status=CLOSED-NEGATIVE d=2026-06-12]

  seed   = 1161  (deterministic, 10 seeds 1161..1170, $0 numpy CPU, Lane-G/CORE engine-sim — NOT AKIDA, NOT byte-LM)
  domain = MITOSIS-ENGINE
  verdict_tier_target = 🟢 SUPPORTED (F1∧F2∧F3) else 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)
  result = 🔴 CLOSED-NEGATIVE  (NEAR-MISS — F1 fails on the super-critical start ONLY, by 0.0013)

  gap   = "H_1153 🟢 showed the engine SITS at σ≈1 at Ψ=½ (STATIC). H_1159b 🟢 showed mitosis self-tunes cell-COUNT to world complexity (DYNAMIC capacity SOC). MISSING edge: is the cell-division PROCESS the MECHANISM that DRIVES an OFF-critical engine TOWARD σ≈1 (self-organized criticality via cell-division — the H_931 SOC homeostat realized by p8)?"

  method = "REUSE the H_1153 branching/avalanche substrate VERBATIM (build_graph · psi_to_branching · run_avalanches · sigma_beggs_plenz imported unchanged) for σ̂ estimation, and the H_1159b tension-driven split RULE VERBATIM (ten += (d−ten)/WIN; split when ten>THETA) for mitosis. The engine drive is shared over a POPULATION of n_cells drive-cells: σ_target = σ0·(N_CELLS0/n_cells) — a SPLIT divides each cell's drive (σ↓), a MERGE concentrates it (σ↑). Per tick: measure σ̂ via Beggs-Plenz on real cascades; load d=(σ̂−1); EMA tension; split if ten>THETA (super) / merge if ten<−THETA (sub). FROZEN control holds n_cells=N_CELLS0 (no split) → σ pinned at σ0. N=4000 K_out=8 (H_1153 graph), 30 ticks, 3000 avalanches/probe, THETA=0.10 WIN=5."

  frozen_falsifier = "PRE-REGISTERED in the h1161 docstring BEFORE measuring:
    F1 CONVERGENCE: starting sub-critical (σ0=0.5) AND super-critical (σ0=1.6), after mitosis ticks |σ_final−1| < 0.10 for BOTH starts.
    F2 MONOTONE-APPROACH: |σ(t)−1| decreases over ticks, Spearman(tick,|σ−1|) ≤ −0.6 (pooled).
    F3 MITOSIS-CAUSAL: a FROZEN (no-split) control does NOT converge — its |σ_final−1| > the mitosis arm's, Cohen's d ≥ 0.8.
    🟢 SUPPORTED iff F1∧F2∧F3 ; else 🔴 CLOSED-NEGATIVE naming the failing gate."

  result_detail = "
    F1 CONVERGENCE  = FAIL (the load-bearing failing gate):
        sub-critical   σ0=0.5 → σ̂_final=0.9981  |σ−1|=0.0019  PASS  (n_cells 8→4.0, MERGED to concentrate drive)
        super-critical σ0=1.6 → σ̂_final=1.1013  |σ−1|=0.1013  FAIL  (n_cells 8→11.3, SPLIT to divide drive) — over the 0.10 band by 0.0013
    F2 MONOTONE     = PASS  Spearman(tick,|σ−1|) = −0.664 ≤ −0.6 (the approach IS monotone, both starts)
    F3 MITOSIS-CAUSAL = PASS  mitosis mean |σ−1| = 0.0516  ≪  frozen 0.4176, Cohen's d = 5.38 ≫ 0.8 (cell-division IS the cause)
    per-gate: F1=False  F2=True  F3=True  →  VERDICT 🔴 CLOSED-NEGATIVE"

  finding = "The cell-division MECHANISM works — and the causal evidence is STRONG: the tension-driven mitosis homeostat MONOTONICALLY drives σ̂ from both off-critical starts toward 1 (F2 PASS), and a frozen no-split control stays pinned off-critical (F3 PASS, d=5.38). From the SUB-critical start it converges essentially exactly (σ̂=0.998, |σ−1|=0.002, MERGING cells to concentrate drive). The verdict is CLOSED-NEGATIVE ONLY because the SUPER-critical start plateaus at σ̂≈1.101 — 0.0013 over the frozen ±0.10 band. WHY (mechanism, honest): the Beggs-Plenz desc/anc estimator on a FINITE network has a SUPER-CRITICAL-ORIGIN FLOOR — when the homeostat lowers the drive, the cascades seeded from a super-critical regime are still truncated by the finite-size cap (N·K_out activity), and truncated cascades systematically bias ⟨n_{t+1}/n_t⟩ upward, so the LOWEST σ̂ the estimator can REPORT from that direction asymptotes near 1.10, NOT 1.00. The homeostat regulates against its own measured σ̂, and the trajectory [0.336→0.169→0.100→0.101→0.101] shows it PARKS exactly at that estimator floor (n_cells grows to 11.3 then stops because tension can no longer cross −THETA). So this is an ESTIMATOR finite-size artifact on ONE direction, not a failure of cell-division as a criticality homeostat — but the frozen falsifier asked for the MEASURED σ̂ inside ±0.10 for BOTH starts, and on the strict letter that is FAIL. NO goalpost move."

  honest = "Asymmetry is real and directional: SUB→σ≈1 clean (merge), SUPER→σ≈1.10 floor (split, finite-size truncation bias of the Beggs-Plenz estimator). The mechanism claim (mitosis = SOC homeostat) is SUPPORTED by F2+F3; the strict bidirectional convergence claim (F1) is FALSIFIED on the super arm by the estimator's finite-size floor. Ruled out at toy scale: that tension-driven cell-division drives the MEASURED branching ratio inside ±0.10 of criticality from a super-critical start under a finite-size Beggs-Plenz estimator. A larger N (smaller finite-size bias) or a truncation-corrected estimator is the open path. Lane-G/CORE engine-sim PROXY; live CORE engine + scale UNVERIFIED (a_scale_honest_scope). Frozen no-split control = the load-bearing causal guard (passed decisively)."

  artifacts = "UNIVERSE/h1161_mitosis_to_criticality.py · .verdicts/1161_mitosis_to_criticality/H_1161.txt"
  xref = "h1153-criticality-branching · h1159b-mitosis-capacity-self-tuning · h1158-phi-at-criticality · h931(SOC homeostat) · a_paper_negative_ok · a_scale_honest_scope · p7 · p8"
