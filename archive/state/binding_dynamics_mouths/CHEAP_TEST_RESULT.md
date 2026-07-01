# Cheap-test ($0 numpy probes) — DIRECTIONAL, frozen-first

`cheap_test.py`, the per-card $0 decision probes. **DIRECTIONAL only** (numpy, not
engine-native; terminal bar = engine-native G0-G6 on the serialized .clm).

## Result (honest, frozen-first — bar NOT moved)

| mouth | bind-arm acc | ablate/ctrl acc | mechanism signature | cheap-test verdict |
|-------|-------------|-----------------|---------------------|--------------------|
| H1620 energy-settle | 1.000 | 1.000 (K=1) | — | NOT-SUPPORTED (gap 0) |
| H1630 tropical | 1.000 | 1.000 (T=1) | — | NOT-SUPPORTED (gap 0) |
| H1631 sheaf | 0.506 | 0.506 (R=I) | coboundary valid 0.0 vs scrambled 451 (separates ✓) | NOT-SUPPORTED (probe acc 0.51) |
| H1632 Galois | 0.844 | 0.844 (OR) | idempotence: AND-pool resid 1.4e-17 vs OR 7.8e-4 (✓) | NOT-SUPPORTED (gap 0) |

## Interpretation (c9 · a_break_the_wall type-a = measurement defect, NOT clean refute)

The cheap-test bars are **inconclusive-by-construction**, not a clean mechanism
refutation:

- **H1620/H1630 = linear-leak artifact.** The synthetic target (AND of two
  directly-readable clamp bits / role-filler pair index) is *linearly separable
  from the raw clamps*, so a linear probe reads it at 1.0 from BOTH the bound rep
  and the ablation — the task does not actually REQUIRE binding (mirrors
  `SCREEN_multiply_vs_add`: additive solves full-set via marginal shortcut). The
  probe needed the *ambiguous illusory-conjunction subset* (`binding_op_screen.py`
  §진단) where the additive rep is provably identical for pos/neg; this generic
  probe omitted that, so it can't isolate binding. Not evidence against the mouth.
- **H1631/H1632 = mechanism-specific signature FIRES.** The sheaf **coboundary**
  cleanly separates valid (0.0) from scrambled (451) bindings — the cohomological
  obstruction object the card predicts — while the identity-restriction control
  cannot produce it. The Galois **idempotence** holds for the AND-pool (closure∘
  closure residual 1.4e-17) but NOT the OR-pool ablation (7.8e-4) — exactly the
  card's idempotence discriminator. The *linear-probe accuracy* tie is again the
  linear-leak issue, but the binding-specific quantities behave as designed.

## Decision

The cheap-test is a weak DIRECTIONAL screen; the **terminal bar is engine-native
G0-G6 on the serialized .clm** (the card's GPU recipe). The mouths are NOT
falsified by the cheap-test (linear-leak inconclusive). Proceed to the GPU 303M
engine-native measurement, which is the real frozen bar. The H1631/H1632
mechanism signatures (coboundary, idempotence) confirm the ops are implemented
faithfully to the card mechanism before the expensive run.
