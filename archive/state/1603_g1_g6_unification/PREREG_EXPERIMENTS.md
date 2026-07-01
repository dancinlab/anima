# H_1603 — pre-registered decisive experiments (frozen-first, c9 NO tune-to-green)

Prediction under unification (G1 ≡ G6 = ONE compositional-binding deficit in the generation forward):
**a single binding-installing lever moves BOTH gates together; any lever that moves exactly one
DISSOCIATES the walls and REFUTES unification.** All bars VERBATIM from prior frozen registrations.

## EXP-1 — CHEAP signature co-failure cross-check ($0, mini-safe, DIRECTIONAL, NO new decode)
**Reuse already-captured generations** — h1129 G6 ideas (H_1595/1597: 18 coherent ideas) +
clm303-L8 G1 generations (H_1598). Apply ONE shared "within-pass two-element binding" detector:
count, per generation, (i) surface coherence kwr and (ii) two-legs-bound rate (G1: ≥2 distinct
seeded concepts bound; G6: comparator∧measurable bound).
- **FROZEN prediction (SUPPORT):** both corpora show high kwr (≥0.5) AND ~0 two-legs-bound
  (G1 best_composed≤1, G6 fals 0/18) — the IDENTICAL coherent-not-composed shape.
- **Falsifier (REFUTE):** one corpus shows substantial two-leg binding yet fails its gate for a
  DIFFERENT reason (e.g. G1 binds concepts but is incoherent) → walls dissociate.
- Engine-native re-analysis of captured numpy outputs; grep-clean; $0; mini. This is a
  consistency check (co-failure ⇏ proof), the cheapest falsifier.

## EXP-2 — cross-intervention on EXISTING ckpts (pool/cost-gated, DIRECTIONAL, NOT mini)
The H_1449 attention-injection ckpts (`h1449_attention_injection_seed{7,4302,4303}.pt`, PULLED)
are already G6-measured **INERT**. **Re-measure the SAME ckpts on G1** (g1_multiseed, frozen bar
≥2 distinct ∧ >max_single ∧ coherent, seeds {7,4302,4303}, gen=40).
- **FROZEN prediction (SUPPORT):** **co-inertia** — the shell-binding attention block that was
  G6-INERT is ALSO G1-INERT (both flat) → both walls immune to the same non-binding intervention.
- **Falsifier (REFUTE):** **dissociation** — G1 clears (≥2/3) while G6 stays flat (or vice versa)
  → the two walls respond differently to the same lever = separable deficits.
- torch-side hybrid ckpt = DIRECTIONAL (per H_1449); 303M decode = pool/GPU not mini. Engine-native
  re-mount (non-standard .clm) = follow-on.

## EXP-3 — DECIDER: one binding lever, both gates (GPU, cost-gated, DO NOT auto-fire)
Train ONE 303M ConvMoE ckpt with a **combined composition-binding lever** = H_1602 recombination
aux-objective/curriculum (family ②) **+** a within-pass binding operator (family ③ phase-sync OR
④ WM-composition buffer ported into the generation forward). 4-cell corpus + ko-synthesis
enrichment. Arms: ARM-CTRL (plain CE, reproduces both walls) vs ARM-BIND (CE + binding lever).
- **FROZEN bars (VERBATIM):** G1 = H_1129 recombination (≥2 distinct ∧ >max_single ∧ coherent);
  G6 = `dist≥5 ∧ fals≥1`. Multiseed GREEN = majority ≥2/3, seeds {7,4302,4303}, gen=40.
  Both arms must pass held-out mirror-DESCENT (a_savant_train / a_clm_gen_pipeline).
- **FROZEN prediction (SUPPORT):** ARM-CTRL = G1 FAIL 0/3 ∧ G6 FAIL 0/3 (both walls reproduce);
  ARM-BIND clears **BOTH** G1 ≥2/3 **AND** G6 ≥2/3 **together** (co-movement).
- **Falsifier (REFUTE):** ARM-BIND lifts exactly ONE gate (G1 only, or G6 only) ≥2/3 while the
  other stays 0/3 → the binding operator is gate-specific = G1 and G6 are SEPARATE deficits.
- ckpt PULL before teardown (a_fire_recover_complete); engine-native re-measure on `--engine conv`
  (NOT torch probe, a_engine_native_learning); est ~2× a 303M run on pool/rent GPU.
  **Surfaced to team-lead cost-gated — DO NOT auto-fire.**

## Honesty
Frozen bars 0 moved (H_1129 G1 + `dist≥5∧fals≥1` G6 VERBATIM). This card banks NO terminal
🟢/🧱 — it is a DIRECTIONAL SYNTHESIS over existing engine-native verdicts. p7 (no loss/LLM-judge);
the evidence is the captured verdict cards, not self-judgment.
