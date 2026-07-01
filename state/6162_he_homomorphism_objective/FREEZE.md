# H_6162 HE-AS-OBJECTIVE — STAGE-1 FAIR cheap-gate (pre-registration · FROZEN)

**Date frozen:** 2026-07-02 (before any run). tune-to-green 금지 (p7). torch mirror = DIRECTIONAL (a_engine_native_learning); pass → engine-native GPU 자격, fail → 🧱 DIRECTIONAL floor.

## Claim under test
Adding a homomorphism-error auxiliary loss `L_HE` to the trunk objective — forcing the pair
representation to be predictable from its parts via a *learned, target-agnostic* composition
operator — improves **held-out compositional generalization** vs plain CE. (Barin-Pacela 2603.28744:
oracle dictionary solves at all scales ⇒ objective is the lever; An&Du: homomorphism structure
predicts OOD composition.)

## Fairness design (learned from H_1840 RIGGED-gate failure)
- **Target is operator-agnostic**: y = T[fa,fb], T a RANDOM non-additive F×F→C table (C=9, chance≈.111).
  No arm's operator is told/matched to T (H_1840's rig was target=circ_conv matching the HRR arm).
- **HE operator g is LEARNED and target-blind**: g = bilinear+MLP over (r(a),r(b)); never sees y.
  L_HE only asks the pair-rep to be homomorphically reconstructable from part-reps — a generic
  compositional-structure prior, not the answer.
- Both arms share identical capacity, data, init, optimizer, seeds. Only λ (L_HE weight) differs.
- Held-out = unseen (fa,fb) factor combinations (~22%): pure recombination (present factors, absent pairing).
- Surface abstraction: E=4 distinct entity tokens per factor → abstract factor from token AND compose.

## Arms
- **OFF**: λ=0 (plain CE).   **ON**: λ∈{0.3, 1.0, 3.0} (sweep; best-λ vs OFF for the bar).
- Seeds: {7, 4302, 4303} (match H_1840).

## FROZEN decision bar
- **DIRECTIONAL-SUPPORT** (→ engine-native GPU authorized): best-λ ON held-out − OFF held-out
  **≥ +0.15 abs on ≥2/3 seeds** AND ON ≥ OFF on 3/3 (no seed regresses).
- **🧱 DIRECTIONAL-FLOOR** (→ NOT-SUPPORTED, objective-axis exhausted reconfirmed): otherwise.
- Sanity (else INCONCLUSIVE): both arms train acc ≥0.90 on SEEN AND OFF held-out > chance+0.05.

## Artifacts
`toy_he_objective_gate.py` · `result.json` · `run.log` · `RESULT.md` (verdict verbatim → card+jsonl lockstep).
