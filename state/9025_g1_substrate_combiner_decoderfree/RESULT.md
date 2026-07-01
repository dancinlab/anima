# H_9026 (H_9025 Rung1) — TRAINED substrate-bind on REAL 303M manifold, held-out recombination

**verdict: 🧱 DIRECTIONAL-FLOOR** (2026-07-02, summer pool $0, numpy/torch mirror = DIRECTIONAL, prior LOW CONFIRMED)

## what was tested (the ONE genuinely-untried cell, distinct from H_1840 / H_6164 / H_9025 Rung0)

- **(i) REAL 303M manifold** — concept part-vecs a_i and composed-pair targets T_ij = `clm303.clm`
  trunk penultimate (final-groupnorm `yn`) mean-pool L2-unit, byte-faithful numpy mirror of
  `core/clm_decode.py::_fwd_logits` (the SAME β embedding H_1822 β used). NOT random-synthetic (H_1840)
  and NOT a synthetic factored toy (H_6164).
- **(ii) ACTUALLY-TRAINED W_bind** — recombination-reward objective = predict the manifold's OWN
  composed-phrase representation T_ij ("c_i c_j") from parts. Closed-form ridge head (deterministic).
  arms: `add` = Linear(concat(a,b)); `bind_open` = Linear(concat(hrr(a,b),a,b)) (multiplicative+additive
  superset); `bind_pure` = Linear(hrr(a,b)) (circular-conv multiplicative only).
- **(iii) HELD-OUT RECOMBINATION** — 34 concepts × 500 sampled ordered pairs, 60/40 train/held-out
  split. Concepts each seen individually in train; the tested PAIR unseen → generalization not retrieval.
- **(iv) shuffle-controlled EARNED + additive baseline + ablation + oracle** — earned iff
  cos(pred(a_i,b_j),T_ij)>COMPOSE ∧ cos(pred(a_i,b_shuffled),T_ij)≤COMPOSE. ablation op→additive.
  oracle = best-arm train-fit≥0.60 (task solvable).

## frozen bars (pre-registered, no tune-to-green)

- oracle/learnability: best-arm train-fit ≥ 0.60 every seed.
- EARNED: shuffle-controlled (right partner composes ∧ wrong fails).
- **PRIMARY G1 direction: n(Δ≥+0.15) ≥ 3/5 seeds ∧ no_regress**, Δ = earned(bind) − earned(add).
- ablation: bind-op→additive must go inert.

## result (verbatim, `rung1_run.log`)

- oracle: best-arm train-fit ≥0.60 all 5 seeds = **True** (train_cos ≈0.99) → task solvable, valid recomb gate.
- `bind_open − add` Δ/seed = **[0.08, 0.09, 0.055, 0.055, 0.045]** · n(Δ≥+0.15)=**0/5** · no_regress=**True**
- `bind_pure − add` Δ/seed = **[0.12, 0.12, 0.08, 0.07, 0.09]** · n(Δ≥+0.15)=**0/5** · no_regress=**True**
- earned rates: add 0.00–0.02 · bind_open 0.065–0.10 · bind_pure 0.085–0.13 (all near-floor).
- **PRIMARY G1 = 🧱 FLOOR** — trained multiplicative bind does NOT beat trained additive on held-out
  recombination.

## honest reading (c9)

- **CONFIRMS prior LOW** (H_1840 FAIR-gate FALSIFIED + DPI meta-law). The one cell H_1840/H_6164 hadn't
  covered — REAL trained manifold + held-out — **also floors**. G1 combination-operator axis is now
  measured on the real manifold, not just synthetic toys.
- **weak-but-consistent signal preserved (matches H_6164):** bind soft-beats additive on ALL 10 deltas
  (no_regress=True) but every seed sub-threshold. The multiplicative direction is the real (but sub-lever)
  signal location, not a lever.
- **caveat (measurement):** real penultimate manifold is anisotropic (cone): pr≈0.92, ps≈0.70 for every
  arm, so absolute COMPOSE=0.30 is trivially passed. Discriminative power comes from the shuffle Δ, which
  is frozen-primary and 0/5. A future rung could use a whitened/isotropic metric, but the Δ (which cancels
  shared anisotropy) already floors → unlikely to flip.
- **scope: DIRECTIONAL** — numpy trunk mirror + torch-free ridge head; not live `core/engine_cli.hexa`
  VAdaptField wire-in. per gate 1 this is NOT a terminal engine-native verdict.

## ladder status

- Rung0 (H_9025): numpy decoder-free harness ✓ DIRECTIONAL
- **Rung1 (this): trained W_bind on REAL manifold + held-out recombination ✓ 🧱 DIRECTIONAL-FLOOR**
- Rung2 (engine-native VAdaptField op-slot wire-in): prior now even LOWER (real-manifold trained bind
  floored). NOT authorized to fire — registered as ING follow-on, GPU/engine-native cost-gated.

## artifacts
- `rung1_trainer.py` (extractor + trained heads + frozen gates + oracle self-test)
- `rung1_run.log` (verbatim summer pool output)
- host: summer (RTX5070 pool box, CPU numpy path) · pid 236624 · wall 82s · $0
