# H_6162 HE-AS-OBJECTIVE — STAGE-1 FAIR cheap-gate v2 (FROZEN 2026-07-02)

v1 (run_v1.log/result_v1.json) returned INCONCLUSIVE by its own rule: the sanity clause
`off_learns` required the BASELINE to beat held-out chance+0.05 — but a baseline flooring at
chance on held-out IS the G1 wall under test (self-contradictory gate). a_break_the_wall type-a:
fix the measurement, keep the bar.

## v2 changes (bar UNCHANGED)
- **Sanity gate fixed** → ORACLE control: train an identical net with the held-out combos PRESENT in
  the training set; require oracle held-out acc ≥0.90 for ALL seeds. This proves the task is
  compositionally solvable (the baseline floor = composition gap, not noise/undertrain).
- +2 seeds (4304, 4305 → 5 total) for power against v1's high variance.
- Everything else identical: operator-agnostic random target T[fa,fb], target-blind learned g,
  L_HE=MSE(h, g(r_a,r_b)) both trainable, λ∈{0,0.3,1,3}, held-out=unseen factor pairings.

## FROZEN decision bar (unchanged from v1)
- **DIRECTIONAL-SUPPORT** (→ GPU authorized): best-λ ON − OFF held-out **≥+0.15 on ≥2/3 seeds** AND no seed regresses.
- **🧱 DIRECTIONAL-FLOOR**: otherwise (given oracle sanity passes).
- **INCONCLUSIVE**: oracle can't solve (≥0.90) OR train acc <0.90.

tune-to-green forbidden (p7). torch mirror = DIRECTIONAL. PASS → engine-native GPU 자격; FLOOR → objective-axis 소진 재확인.
