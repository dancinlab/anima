# H_9026 — G1 trained-bind on REAL 303M manifold, held-out recombination (H_9025 Rung1)

- **tier:** 🧱 DIRECTIONAL-FLOOR
- **slug:** `g1_trained_bind_real_manifold`
- **parents:** [[H_9025]] (Rung0 harness) · [[H_1822]] (substrate-framebreak: no constructive combiner op) · [[H_1840]] (cheap-gate FAIR FALSIFIED) · [[H_6164]] (structural-bind cheap-gate FLOOR)
- **wired:** `DIRECTIONAL-mirror` (numpy trunk mirror + torch-free ridge head; live `core/engine_cli.hexa` VAdaptField 미배선)

## claim (the one genuinely-untried cell)

H_1840 (random-synthetic target + untrained algebraic op) and H_6164 (synthetic factored toy)
both floored, but neither trained a bind op on the **REAL 303M concept manifold** and tested
**held-out recombination generalization**. H_9026 does exactly that: extract clm303.clm trunk
penultimate mean-pool vectors (β embedding), train W_bind (circular-conv ⊛) to predict the
manifold's OWN composed-phrase representation, and test compose on UNSEEN concept pairs vs a
trained additive baseline (shuffle-controlled EARNED + ablation + oracle).

## verdict (2026-07-02, summer pool $0, DIRECTIONAL)

**🧱 FLOOR.** oracle valid (task solvable, train-fit≈0.99). PRIMARY held-out recombination:
`bind_pure − add` Δ/seed = [0.12, 0.12, 0.08, 0.07, 0.09], `bind_open − add` = [0.08, 0.09,
0.055, 0.055, 0.045]; **n(Δ≥+0.15)=0/5 both, no_regress=True** (bind soft-beats add on all 10
deltas but every seed sub-threshold — identical pattern to H_6164). Trained multiplicative bind
does NOT beat trained additive on held-out recombination even on the real trained manifold.

**CONFIRMS prior LOW** (H_1840 FAIR-gate + DPI meta-law). G1 combination-operator axis now
measured on the real manifold, not just synthetic toys. Weak-but-consistent multiplicative
signal preserved (H_6164 convergence) = signal location, not a lever. DIRECTIONAL (numpy/torch
mirror, not engine-native terminal).

## follow-on

- Rung2 (engine-native VAdaptField op-slot wire-in) prior now even LOWER → ING, GPU/engine-native
  cost-gated, NOT authorized to fire this session.

## artifacts
- `state/9025_g1_substrate_combiner_decoderfree/rung1_trainer.py`
- `state/9025_g1_substrate_combiner_decoderfree/rung1_run.log`
- `state/9025_g1_substrate_combiner_decoderfree/RESULT.md`
