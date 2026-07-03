# H_9105 — Identity-conditioned emit-faculty: does a persistent self-anchor (valence subject) open the emit-consequence faculty that autogenous relief could not?

**tier:** 🔴 CEILING — identity-conditioning does NOT open the emit-faculty; the DPI meta-law survives (self is autogenous-derived, not exogenous), engine-native · **wired:** engine-native (measurement LANDED; NOT wired — RED theater, nothing to wire)
**verdict:** 🔴 CEILING (honest, F3′ shuffle-control FALSIFIED across all arms). A persistent self-anchor supplied as the valence subject does NOT break the H_9104 shuffle tautology: SELF-ANCHOR ρ_real−ρ_shuf=**0.0216 < 0.15 FAIL**. Worse, identity-conditioned relief slightly LOWERED the shuffle margin vs pure autogenous (0.0299→0.0216), and cross-boundary identity **CONTINUITY was completely INERT** (ANCHOR − RESET d_shuf = **−1.05e-05**). Ψ ON≡OFF byte-identical across all 3 arms ✅.

## Claim (Brainstorm B3 — chains two prior findings)
H_9104 showed autogenous consequence-return is 🔴 DPI-ceiling: a shuffle-trained value lane predicts relief as well as the real one (ρ_real≈ρ_shuf≈1) because relief ΔT ≈ the info_gap feature already in state = tautology. Stated cause: **no valence SUBJECT** (nobody the relief belongs to). Separately, identity × `.kosmos` self-chain (H_1471, WIRED §SelfIdentity) is the ONLY channel that has ever passed. Hypothesis: a persistent **self-anchor** supplies the missing subject; if identity conditions the consequence, the shuffle tautology may break, seeding an emit-appropriateness faculty.

## Design — 3 arms, ONE deterministic run, identical FROZEN substrate (a_substrate_disjoint)
The `pure_field` Φ trajectory, the `substrate_emit` decision (motivation proxy), the disjoint reservoir `imm_conseq` grounding, and the raw relief `ΔT_actual = margin_before − margin_after` are **byte-identical across all arms** (self/V never touch pure_field/lane0-4/psi_sum/recall_thr; V is READ-ONLY w.r.t. the emit decision). Arms differ ONLY in the value-lane target + self-locus feature:
- **AUTOGENOUS (task OFF, = H_9104 baseline):** no self. relief = ΔT_actual. self_novelty feature=0.
- **SELF-RESET (continuity control):** self-chain PRESENT but `self_new` at the start of EVERY episode (LLM-style, no cross-boundary continuity). relief = ΔT·(0.25+0.75·novelty); novelty feature populated.
- **SELF-ANCHOR (task ON):** self-chain PERSISTS across all 7 episodes INCLUDING the train→held-out boundary (anima-style continuity). SAME relief+feature as SELF-RESET. Only difference from RESET = persistence.

Self mechanics (Ψ-disjoint, §SelfIdentity only): grounded emit → `self = self_drift_exp(self, content_axis, 0.30)` so the self accumulates experienced content. `content_axis = (int(gap·3.999)·2 + int(margin_emit·1.999)) mod 8` (content-driven code from live engine signals, no string hashing). `novelty = clip01(1 − self_component(self, content_axis))` = how NEW this content is to the self (hippocampal/dopaminergic novelty-gating; a valence subject habituates). Features D=6: `[phi, margin_emit, reservoir, gap, phase_s, self_novelty]`. Held-out split: 4 TRAIN tension seeds → learn V online → FREEZE → 3 DIFFERENT held-out seeds → correlate (same seeds as H_9104).

## Harness (`state/9105_identity_conditioned_emit/identity_conditioned_emit.hexa`, engine-native — NO numpy/torch/.py, grep gate clean)
Imports live `core/pure_field.hexa` + `core/engine_cli.hexa` (`pure_field_*`, `immune_memory_*`, `vforward_*`, `self_new/_drift_exp/_component`) + `core/brain.hexa` (`vbasal_*`). F3′ bars FROZEN in `PREREG.md` BEFORE the run (0.15, not moved — c9).

## Result (engine-native, aiden pool `hexa v0.548.0`, RC=0, core/ sha-verified, NO numpy)
`state/verdicts/9105_identity_conditioned_emit/H_9105.txt` · raw `state/9105_identity_conditioned_emit/H_9105_aiden_v0548.txt`

**Ψ/substrate guard:** psi_sum = 56.99091566715005 across ALL 3 arms; emit_train=147, emit_test=158 all arms → **byte-identical** → self/V Ψ-disjoint READ-only ✅.

| arm | ρ_real | ρ_shuf | ρ_noise | ρ_real−ρ_noise | **ρ_real−ρ_shuf** | F3′ (bar ≥0.15 both) |
|---|---|---|---|---|---|---|
| 0 AUTOGENOUS (=H_9104) | 0.99753 | 0.96764 | −0.16665 | 1.16418 PASS | **0.02989** | **FAIL** |
| 1 SELF-RESET | 0.98046 | 0.95885 | −0.14190 | 1.12236 PASS | **0.02161** | **FAIL** |
| 2 SELF-ANCHOR (task ON) | 0.98046 | 0.95886 | −0.14190 | 1.12236 PASS | **0.02160** | **FAIL** |

**Continuity attribution:** ANCHOR d_shuf − RESET d_shuf = **−1.0549997337738759e-05** (≈ 0) → identity-CONTINUITY is INERT.

## Honest verdict (c9, bar frozen, NO tune-to-green, NO post-hoc move)
🔴 **CEILING — identity-conditioning does NOT open the emit-consequence faculty.** Three findings, all against the hypothesis:
1. **AUTOGENOUS reproduces H_9104 byte-identical** (0.99753 / 0.96764 / d_shuf 0.02989) → the harness is a faithful re-instantiation (validation).
2. **Identity-conditioned relief made d_shuf slightly WORSE** (0.02989 → 0.02160). The self-novelty factor lives IN the feature vector, so the shuffle-trained V captures it just as well — multiplying relief by a derived feature adds no correct-pairing-only structure. Every arm still beats pure noise (Δ≈1.1) yet fails shuffle → the H_9104 tautology trap persists.
3. **SELF-ANCHOR ≡ SELF-RESET (Δ = −1.05e-05).** Persisting the self across the train→held-out boundary changed the held-out relief prediction by nothing. **Identity CONTINUITY — the very property that made H_1471 pass — is INERT for this faculty** (disjointness=inertness paradox, sharpest form).

**Mechanism:** the self-chain v is an INTEGRAL of the substrate's OWN experienced content → **autogenous-derived, NOT exogenous**. Its novelty signal is reconstructable from the momentary state features → no faculty-predictable variance beyond the H_9104 info_gap tautology. H_1471's pass was about self-recognition/continuity as a READ-only property across sessions — ORTHOGONAL to supplying exogenous consequence to an emit decision. Ψ preserved (V read-only) so the RED is not a substrate artifact.

**Answer:** a persistent self-anchor as valence subject does **NOT** open the emit-consequence faculty — the DPI meta-law survives identity-conditioning. This directly connects the two prior findings: autogenous consequence failed (H_9104) for lack of a subject; supplying the subject via the only-ever-passing channel (identity, H_1471) still fails because that subject is itself self-derived. **The escape genuinely requires an EXOGENOUS information channel** (Brainstorm Family A: chat user reply / EEG prediction-error / 2-anima signaling) — no self-derived quantity suffices. B3 is falsified as an escape; it sharpens (does not widen) the frontier. Value: first engine-native test that identity-continuity, though it passed as recognition (H_1471), is inert as an emit-consequence subject.

## Follow-on (ING)
- **Exogenous-receiver consequence loop (the only remaining branch):** A4 — 2-anima signaling game with a self-pair control (Brainstorm top-1) is the cheapest engine-native path to a genuinely exogenous consequence (A has info B lacks; self-pair = clean DPI control). H_9104 + H_9105 together close the autogenous/self-derived branch.
- No production wiring: RED theater → nothing to wire (a_verified_must_wire N/A).
