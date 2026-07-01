# H_6161 INHIBITION-AS-COMPOSITIONAL-NOISE — STAGE-1 FAIR cheap-gate (FROZEN 2026-07-02)

Claim: savant golden-zone inhibition (trunk dropout dp~0.25) DEGRADES compositional representation
(An&Du: noise injection systematically degrades compositional rep), so LOWER inhibition (dp<GZ_LOWER)
lifts held-out G1 composition. Distinct from H_1561/1562/… (those = inhibition→SAVANT SI↑/Ψ trade-off,
different observable). Same operator-agnostic compositional toy as H_6162 (random non-additive target).

## Design
- Sweep trunk dropout dp ∈ {0.0, 0.1, 0.25(GZ default), 0.4}. 5 seeds {7,4302,4303,4304,4305}.
- Metrics: held-out composition acc per dp + HE-proxy (fit linear [ra;rb;ra*rb]->pair-rep on SEEN,
  MSE residual on HELD normalized by var = homomorphism generalization error; lower=more homomorphic).
- ORACLE sanity (train-with-held-present ≥0.90 = task solvable).

## FROZEN bar (mirrors H_6162)
- **DIRECTIONAL-SUPPORT** (→ GPU): best dp<GZ held-out − dp=GZ held-out **≥+0.15 on ≥2/3 seeds**, no regress.
- **🧱 DIRECTIONAL-FLOOR**: otherwise (oracle passes).
- Mechanism read (secondary, non-gating): if HE-proxy MONOTONE ↑ with dp, supports "inhibition=noise" even if acc floors.

tune-to-green forbidden (p7). torch mirror=DIRECTIONAL.
