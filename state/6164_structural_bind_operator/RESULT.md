# H_6164 G1 STRUCTURAL BIND-OPERATOR — cheap-gate RESULT (2026-07-02)

**TIER: 🧱 DIRECTIONAL-FLOOR** (torch=DIRECTIONAL, aiden $0). Tests the framebreak thesis
([[substrate-framebreak-g1-combination-operator]]: G1 wall = combination operator) in the controlled
solvable toy: swap the trunk pair-composition from additive-concat to explicit multiplicative binders.

## Design (same factored toy; oracle=1.0 all seeds = task solvable)
Arms (trunk composition h of part-reps ra,rb → readout): **add**(concat→MLP, baseline) ·
**hadamard**(ra*rb) · **tensorproduct**(vec(ra⊗rb)→linear) · **bilinear**(low-rank R=32).
5 seeds. FROZEN bar: best-binder held-out − add held-out ≥ +0.15 on ≥2/3 seeds, no regress → SUPPORT.

## Result — FLOOR, but the session's only consistent positive signal
best-binder vs additive held-out delta per seed: **+0.050 / +0.054 / +0.071 / +0.109 / +0.004**.
n(Δ≥+0.15)=**0/5** → FLOOR. HOWEVER no_regress=True and 4/5 seeds show a positive lift — structural
binders (best arm = tensorproduct/bilinear) consistently beat additive by a small margin that never
reaches the lever threshold. This is the only axis this session with a consistent directional edge
(objective/regularization/data all gave flat/regress).

## Reading
The combination-operator (framebreak) IS where the (weak) compositional action lives — trunk-level
multiplicative binding gives a small real edge over additive — but at cheap scale the effect is far
below a lever (≤+0.11, never +0.15). Confirms H_1840 (γ bypass-denied bilinear FALSIFIED) from a
cleaner angle and closes the STRUCTURAL axis. The consistent-but-sub-threshold lift is the honest
residual: it weakly re-motivates a GPU-scale γ/bind test, but the cheap evidence does not authorize it.

## Session convergence (4 cheap axes, one controlled solvable toy)
objective (H_6162) · regularization (H_6161) · data-coverage (H_1824) · **structural-bind (H_6164)** —
ALL 🧱 FLOOR. G1 recombination wall is axis-invariant at cheap scale (DPI meta-law). structural-bind is
the least-dead (consistent +0.05–0.11) but still sub-lever.

## Provenance
aiden pool CPU, torch, OMP=4, $0. toy_bind_operator.py, run.log, result.json.
