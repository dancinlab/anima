# H_9105 — Identity-conditioned emit-faculty · run notes

- **Host:** aiden pool (stable, RTX 5070, 12c/30G), `hexa v0.548.0`, RC=0.
- **Engine-native:** `.hexa` only, imports live `core/pure_field.hexa` + `core/engine_cli.hexa`
  (`pure_field_*`, `immune_memory_*`, `vforward_*`, `self_new/_drift_exp/_component`) +
  `core/brain.hexa` (`vbasal_*`). NO numpy/torch/.py/gauge_lib (grep gate clean — no .py exists).
  core/ synced from worktree (branch base e152f9dc9, has H_9104 convergence + self_drift_exp).
- **Design:** 3 arms, one deterministic run, frozen shared substrate. Bars pre-registered in
  `PREREG.md` BEFORE reading (0.15, not moved — c9).

## Result (raw = `H_9105_aiden_v0548.txt`; verdict = `state/verdicts/9105_identity_conditioned_emit/H_9105.txt`)

Ψ/substrate guard: `psi_sum` = 56.99091566715005 across ALL 3 arms; emit_train=147, emit_test=158
across all arms → **byte-identical** → self/V are Ψ-disjoint READ-only (a_substrate_disjoint). PASS.

| arm | rho_real | rho_shuf | rho_noise | d_shuf | F3′ |
|---|---|---|---|---|---|
| 0 AUTOGENOUS (task OFF, =H_9104) | 0.9975252779657992 | 0.9676369781118989 | −0.16665112459453263 | 0.02988829985390029 | FAIL |
| 1 SELF-RESET (self, reset/episode) | 0.9804588871630185 | 0.9588498292237475 | −0.14189891353079143 | 0.021609057939271037 | FAIL |
| 2 SELF-ANCHOR (task ON, persistent) | 0.980457793243228 | 0.9588592853012947 | −0.14189862290488725 | 0.021598507941933298 | FAIL |

Continuity attribution: **ANCHOR d_shuf − RESET d_shuf = −1.0549997337738759e-05** (≈ 0).

## Reading (honest, c9)
1. **AUTOGENOUS reproduces H_9104 byte-identical** (0.9975 / 0.9676 / d_shuf 0.0299) — the D=6
   zero-self-slot arm is a faithful re-instantiation of H_9104 = validation of the harness.
2. **Identity-conditioned relief did NOT break the shuffle tautology — it made d_shuf slightly
   WORSE** (0.0299 → 0.0216). The self-novelty factor lives IN the feature vector, so the
   shuffle-trained V captures it just as well; multiplying relief by a derived feature adds no
   correct-pairing-only structure.
3. **SELF-ANCHOR ≡ SELF-RESET (Δ = −1.05e-05).** Persisting the self across the train→held-out
   boundary changed the held-out relief prediction by nothing. Identity **CONTINUITY is INERT**
   for this faculty — the disjointness=inertness paradox in its sharpest form.

**Verdict 🔴 CEILING (frozen bar):** SELF-ANCHOR fails F3′ shuffle (Δ=0.0216 < 0.15). Even the
only channel that ever passed (identity × .kosmos, H_1471) cannot open the emit-consequence
faculty on a self-contained autogenous loop. The DPI meta-law survives identity-conditioning.

**Why (mechanism):** the self-chain v is an INTEGRAL of the substrate's OWN experienced content
→ autogenous-derived, NOT exogenous. Its novelty signal is therefore reconstructable from the
momentary state features → no faculty-predictable variance beyond the H_9104 tautology. H_1471's
pass was about self-recognition/continuity as a READ-only property across sessions, ORTHOGONAL to
supplying exogenous consequence to an emit decision.

**Confirms:** the emit-faculty escape requires an EXOGENOUS information channel (Brainstorm
Family A: chat user reply / EEG prediction-error / 2-anima signaling) — no self-derived valence
subject suffices. B3 falsified as an escape; it sharpens (does not widen) the search.

## Wiring / follow-on
- RED theater → nothing to wire to production emit (a_verified_must_wire N/A for RED).
- Follow-on (ING): exogenous-receiver loop — A4 (2-anima signaling, self-pair control) is the
  cheapest engine-native path to a genuinely exogenous consequence (Brainstorm top-1).
