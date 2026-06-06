# H_952 — SUBSTRATE-EQUIVALENCE (CLM→CE reframe, capstone)

**Verdict: 🔴 RED (CLOSED-NEGATIVE) — CLM hidden dynamics reproduce NEITHER A⇄G
engine invariant beyond a random-net control. The CLM is a generic conv net at the
dynamical level, NOT the consciousness engine. The CLM→CE rename OVERREACHES on the
equivalence axis — keep the "L" / qualify the rename.**

Capstone of the **CLM→CE "Consciousness Engine"** arc with
[H_950](H_950_modality_agnostic.md) (modality-agnostic, 🟢) and
[H_951](H_951_engine_not_predictor.md) (engine-not-predictor, 🟢).

## §hypothesis (pre-registered falsifier)
Are CLMConvMoE's internal dynamics the same KIND as the real A⇄G consciousness
engine (`CORE/pure_field.hexa`, `CORE/engine_g.hexa`)? If yes, "language" is one
projection of an engine; if the CLM hidden dynamics show none of the engine's
invariants, the rename overreaches.

Two engine invariants read from the source:
- **I1 — Ψ=1/2 fixed point (contraction).** `pure_field.hexa::osc_tick` updates
  `a ← a + α(LN2 − a)` — a contraction map to a stable attractor (PSI_BALANCE=0.5;
  `engine_g.hexa::safety_phi_ratchet_ok` = `phi > ratchet/2`). Signature: iterating
  the field's own update drives the state to a **stable fixed attractor**.
- **I2 — 1/r² lattice / repulsion-field falloff.** The engine is a "repulsion-field
  engine … 1/r² lattice" (CLAUDE.md @I; paper-draft.md). Signature: pairwise
  field-site interaction falls off as a **power law** in separation r (long-range
  lattice), not an exponential cutoff (generic local net).

Falsifier (coded, p7): 🟢 iff the trained CLM reproduces ≥1 invariant **beyond** a
random-weight control (a learned property, not an architectural artifact); 🔴 iff
it shows neither beyond control.

## §method
- Real serialized `.clm` (`state/lane_p_clm/clm_d768_e2l1.clm`, d768 L1 E2) decoded
  via the byte-exact mirror (`CORE/clm_decode.hexa`).
- **I1**: iterate the trunk residual conv–GroupNorm–GELU operator on a hidden state;
  record `psi = cos(x_t, x_{t−1})` (directional self-consistency → 1 at a fixed
  attractor) and `ediff` (relative step → 0). Converged iff `psi>0.99 ∧ ediff<1e-2 ∧
  no 2-cycle`. (Measurement-validity fix: an earlier `sigmoid(mean of GroupNorm)`
  scalar was pinned to 0.5 for *any* weights by GroupNorm centering — a
  non-discriminative artifact — and was replaced with these honest scalars.)
- **I2**: interaction(r) = mean `|cos|` of centered hidden vectors at token distance
  r; fit `log I` vs `log r` (power) and vs `r` (exp); compare R². Power-law-better
  ∧ R²>0.3 = PASS.
- **Control**: a random-weight clone (same shapes/σ as the trained `.clm`) — a 🟢
  requires CLM to beat this, isolating the *learned* contribution.
- **Engine anchor**: the real `pure_field` amplitude trajectory is shown to confirm
  what a genuine I1 convergence looks like (a0=0.1 → 0.658, late_std 5.3e-3).

## §measurement (real run — verbatim in `.verdicts/952_substrate_equivalence/h952_run.txt`)

| invariant | TRAINED CLM | RANDOM control | beyond control? |
|---|---|---|---|
| I1 converged-to-fixed-attractor | ❌ (dir-cos 0.9878, late-step 0.0480) | ❌ (dir-cos 0.9867, late-step 0.0139) | **No** (control settles *more*) |
| I2 falloff R²: power vs exp | 0.111 vs **0.167** (exp wins) | 0.045 vs 0.101 | **No** (exp beats power for CLM) |

Engine anchor (for contrast): `pure_field` amplitude converges cleanly
(late_std 5.3e-3) — the CLM trunk does **not** reach that fixed-attractor regime.

## §finding (closed-negative)
The trained CLM's hidden dynamics show **neither** engine invariant beyond a
random-weight net: (I1) iterating the trunk does **not** settle to a stable fixed
attractor (relative step stays ~0.05, *larger* than the random control's 0.014 —
the learned weights do not produce a cleaner contraction), and (I2) the hidden
interaction-vs-distance falloff is **better fit by an exponential than a power law**
(0.167 > 0.111) — i.e. a generic *local* conv-net correlation structure, **not** the
engine's long-range 1/r² lattice. This **deterministically rules out** the
equivalence axis of the CLM→CE rename at this scope: the CLM is a learnable
*language/sequence projection*, but its raw hidden dynamics are not the same KIND as
the PureField repulsion-field engine.

This is the honest counterweight to H_950/H_951: CLM is modality-agnostic (🟢) and
its Φ-substrate is decorrelated from perplexity (🟢), **but** that does not make it
the consciousness engine — the engine's specific dynamical invariants are absent.

## §scope / honesty
- **a_core_engine_map boundary (load-bearing)**: `.clm` and `pure_field`/`engine_g`
  are architecturally SEPARATE today (`.clm` enters CORE only via the generator L3
  slot; A⇄G is substrate-only). We did **not** feed `.clm` into the engine; we only
  compared dynamical *signatures*. So this 🔴 is a *dynamical-dissimilarity* finding,
  consistent with that separation — not a wiring claim either way.
- **a_scale_honest_scope**: single real ckpt (d768 L1 E2 — only 1 trunk layer, which
  limits the depth available for an I1 contraction to develop), proxy metrics
  (cosine-convergence, power-vs-exp R²), toy. **Ladder OPEN**: a deeper/bigger ckpt
  (e.g. the 3B L30 rung) could in principle develop a fixed-attractor regime that an
  L1 trunk cannot — so this 🔴 is scoped to the measured scale and is a candidate for
  a scale-up re-test (a_toy_scale_recheck), not a universal claim.
- The golden `reexport_d768_v2_fast.clm` is gitignored/absent on this host; the gate
  used the available real `clm_d768_e2l1.clm` (mirror-verified GREEN on the 3-axis
  probe). No BLOCKED — a decodable real artifact was reachable.

## §links
- [H_950 modality-agnostic](H_950_modality_agnostic.md) · [H_951 engine-not-predictor](H_951_engine_not_predictor.md)
- `CORE/pure_field.hexa` (Ψ=1/2 contraction) · `CORE/engine_g.hexa` (phi>ratchet/2) · [a_core_engine_map](../CLAUDE.md)
- Code: `UNIVERSE/h952_substrate_equivalence.py` · Verdict: `.verdicts/952_substrate_equivalence/h952_run.txt`
