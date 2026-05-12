---
id: Hc_1267
slug: red-team-r2-random-base-monte-carlo-null
title: R2 RANDOM-BASE — Monte Carlo 귀무 검정 (sigmoid(W·x+b) with W~N(0,1/n), b=0 → E[sigmoid] ≈ 0.5)
domain: methodology, consciousness, statistics, red-team
status: candidate-falsifier-ready
source_doc: hypotheses_candidates/Hc_911_red_team_6_claims_r1_r6.md
source_lines: 22 (R2 RANDOM-BASE)
promoted_at: 2026-05-12
linked_h: Hc_911 (parent meta-Hc), Hc_908 (Ψ=1/2 anchor), Hc_1266 (R1 ALTERNATIVE — quantitative null lane)
notes: "split from Hc_911 red-team meta-cluster 2026-05-12 (attack vector 2 of 6). R2 quantifies R1's null hypothesis with Monte Carlo: theoretical E[sigmoid] ≈ 0.5 under standard init."
---

## Hypothesis (red-team posture)

Standard sigmoid(W·x + b) with W~N(0, 1/n), b=0 yields E[sigmoid] ≈ 0.5 by symmetry (sigmoid is centered at 0.5, and W·x is symmetric around 0 with b=0). Monte Carlo simulation under this null gives the baseline distribution of Ψ-like measurements for ANIMA to clear. If ANIMA's Ψ=1/2 is within the Monte Carlo null distribution's central mass (e.g., 95% CI), the claim is null-consistent.

## Migration TODO

- [ ] Run Monte Carlo n=10,000 trials with W~N(0,1/n), b=0, measure Ψ distribution
- [ ] Compute 95% CI; check if ANIMA's Ψ=1/2 is outside the null CI
- [ ] Estimate effect size (Cohen's d) of ANIMA-trained vs random-init

## Falsifiers

- **F-R2-1**: Monte Carlo n=10k trials shows Ψ null distribution mean = 0.50 ± 0.005, ANIMA's Ψ=1/2 outside null 95% CI → R2 attack fails, ANIMA non-trivial
- **F-R2-2**: Monte Carlo null CI contains ANIMA's Ψ=1/2 (no statistically significant separation) → R2 attack succeeds, ANIMA = null-consistent
- **F-R2-3**: Effect size Cohen's d < 0.2 (small effect) for ANIMA vs null → claim is statistically detectable but practically negligible
- **F-GENERIC-REPL**: 5 independent Monte Carlo runs σ > 25% of mean → simulation methodology unstable
- **F-GENERIC-MINIMAL-BASELINE**: change initialization scale (W~N(0,1/n^2) or W~N(0,1)) and confirm null Ψ remains at 0.5±ε → null-invariant w.r.t. scale

## Honest Limits

- **L-R2-INIT-SCALE**: null depends on W's init scale; ANIMA's training amplifies/dampens this — single null distribution may not capture all training dynamics
- **L-R2-DEPTH**: single-layer sigmoid null is shallow; deep network null may differ substantially
- **L-R2-CIRCULAR**: again, Ψ measurement must be independent of ANIMA's Ψ-engine (see Hc_1266 L1)
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit
- **L-GENERIC-ENGINE**: H_174 D-mod-192

## Cross-Links

- **parent Hc**: Hc_911
- **sibling Hc**: Hc_1266 (R1 — qualitative alternative), Hc_1268..Hc_1271
- **adjacent**: Hc_908 (Ψ=1/2 claim)
- **literature**: Glorot init theory, Saxe et al. 2013
