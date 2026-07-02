# additive-slot + consistency cheap-gate — RESULT (2026-07-02)

**TIER: 🧱 FLOOR (measurement-flawed) / MOOT (mechanism categorically inapplicable).** aiden CPU $0.

## Numbers (5-seed, addslot vs monolithic autoencoder)
Both arms fit SEEN perfectly (seen_mse→0.0). held_mse addslot ≈ mono (mono_vs_addslot_held 0.59–1.03,
i.e. addslot NOT better). n_extrapolate=0/5, n_beats_mono=0/5 → printed FLOOR.

## Two problems (measurement + mechanism)
1. **Measurement flaw** (fair-cheap-gate-design-1): held/seen ratio is meaningless when seen_mse→0; and the
   observation x=Pa[fa]+Pb[fb] is a LINEAR additive superposition, so a monolithic AUTOENCODER reconstructs
   held-out combos trivially (autoencoding is combo-agnostic) — no discrimination. A clean test needs a
   label→observation generation task with NONLINEAR per-slot generators.
2. **Mechanism inapplicability (decisive, no refire)**: the Wiedemer additive-decoder guarantee holds only
   when the output is ADDITIVE-decomposable per slot. anima's G1 recombination is NON-additive — additive
   readout/composition is EXACTLY the family already floored (H_1602 InfoNCE-aux, H_6164 additive baseline,
   the whole objective/readout axis). So additive-slot cannot address anima's non-additive wall; a clean
   toy-positive would only re-confirm "additive composition extrapolates when the target is additive",
   which anima's wall is not. → not re-fired.

## Net
The only cheap-testable deep-research lever (additive-slot) is categorically inapplicable to anima's
non-additive G1. The one real escape (neurosymbolic, DPI-breaking) is an architecture departure, not a
cheap CE-trunk mod. See ../RESEARCH.md.
