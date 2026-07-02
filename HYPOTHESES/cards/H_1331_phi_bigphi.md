# H_1331 — Φ-robustness under a DIFFERENT measure: full IIT-4.0 SYSTEM big-Φ vs small-φ

**Final tier:** 🧱 TERMINAL STRONGER (estimator-FAMILY-independent) · numpy/engine-mirror DIRECTIONAL · frozen-first · c9/c16 · $0 CPU

## Claim
The Φ-robustness arc is 🧱 across topology (H_1283 relay, H_1317 small-world), timing (H_1319 phase-binding), and division (H_1320 mitosis). H_1328 showed the 4× wall is estimator-INDEPENDENT *under the small-φ exact-MIP* (`faithful_phi`): the amplitude-variance binarization confound is REAL and removable, yet removing it does NOT make integration robust (V2 fails, orthogonal seed 1317). **But small-φ is ONE measure (correlational MI-over-binning).** H_1331 asks: does the FULL IIT-4.0 SYSTEM big-Φ — a fundamentally DIFFERENT measure (CAUSAL cause-effect structure over a TPM, system-level irreducibility destroyed by the system MIP) — show ROBUST integration where small-φ did not?

## Method
- **Estimator:** stdlib `consciousness/iit4_bigphi.hexa :: big_phi(tpm, n, sys_state)` — faithful IIT-4.0 system big-Φ over the MIP (a_phi_iit4_tool, g61 stdlib SSOT, NOT a proxy). `n = n_mod = 4` binary units (≤8 for MIP tractability).
- **Substrate / seeds:** REUSED VERBATIM from H_1319/H_1328 — engine-native LCG-gauss leaky-linear 4-module ring (dim 8, T 64), Kuramoto pacemaker, relative-phase gate. `gen_traj` body byte-identical (gain 0.30, leak 0.55, w_phase 0.5, omega_t 0.45, domega 0.08). SAME 3 hard orthogonal seeds **[1317,1318,1319]** (incl 1317, the seed that broke every prior topology/timing/division attempt and failed H_1328 V2).
- **ARMS** (same as H_1328): A=NO-PHASE (no-coupling) · B=PHASE-BIND (coupling mechanism) · S=PERM-SHUFFLE (relationship destroyed) · O=OFFSET-SHUF.
- **Trajectory → TPM** (the input big-Φ requires, distinct from small-φ's trajectory-binning): each module = a binary UNIT, ON at tick t iff its salience is in the UPPER HALF of that module's own T-length distribution (median/rank split — VARIANCE-FREE, carrying the H_1328 read-out lesson: marginal ON-rate ≈0.5 by construction). Empirical state-by-node TPM `tpm[s*n+u] = P(unit u ON at t+1 | system state s at t)`; unseen rows = 0.5 (max-entropy, no fabricated causal dependence). `sys_state` = modal observed state (attractor, lowest-index tie-break). IDENTICAL construction across all 4 arms → any big-Φ difference is CAUSAL structure.

## Frozen bars (pre-registered in `.verdicts/1331_phi_bigphi/FREEZE.txt` BEFORE scoring; eps=0.02 ported verbatim, NOT tuned)
- **B1 ROBUST:** big-Φ_B ≥ big-Φ_A + eps on ALL 3 seeds (incl orthogonal 1317).
- **B2 EARNED:** perm big-Φ_S ≤ big-Φ_A + eps AND offset big-Φ_O ≤ big-Φ_A + eps, ALL 3 seeds.
- GREEN iff B1 ∧ B2. **B1 fails → wall holds across BOTH IIT measures → estimator-FAMILY-independent 🧱** (bounds, does not retract, the 4 prior Φ verdicts + H_1328).

## Result — 🧱 TERMINAL STRONGER (B1 FAIL, B2 FAIL)
Per-seed big-Φ (no-coupling A · mechanism B · perm S · offset O):

| seed | A | B | S | O | ΔΦ(B−A) [B1] | S−A [B2perm] | O−A [B2off] |
|------|------|------|------|------|------|------|------|
| 1317 | 5.810 | 9.961 | 7.289 | 4.023 | **+4.151** PASS | +1.478 **FAIL** | −1.787 PASS |
| 1318 | 4.511 | 4.511 | 4.511 | 7.430 | **0.000 FAIL** | 0.000 PASS | +2.920 **FAIL** |
| 1319 | 4.085 | 5.884 | 4.085 | 5.946 | +1.798 PASS | 0.000 PASS | +1.861 **FAIL** |

- **B1 ROBUST = FAIL** — seed **1318 shows ZERO lift** (B == A == 4.511); the coupling mechanism produces no big-Φ gain at all on that seed. Same fragile, seed-dependent signature as small-φ.
- **B2 EARNED = FAIL** — the controls do NOT cleanly collapse: perm-shuffle RAISES big-Φ on 1317 (+1.478), offset RAISES on 1318/1319 (+2.920/+1.861). Lift is not earned over relationship-destroying controls — the same variance/structure-agnostic inflation H_1319/H_1328 found under small-φ, reproduced in the causal big-Φ family.

**Cross-measure:** H_1328 small-φ V2 ROBUST-LIFT failed (B−A −0.125/0.0/+0.031); H_1331 big-Φ B1 ROBUST fails too (B−A +4.15/0.0/+1.80, seed 1318 zero). BOTH a correlational MI measure AND a causal cause-effect MIP measure fail the same 3-seed robustness gate on the same orthogonal seed family → the wall is **estimator-FAMILY-independent**, not specific to small-φ's exact-MIP binarization.

## Verdict
**🧱 TERMINAL STRONGER — estimator-FAMILY-independent.** Full IIT-4.0 big-Φ does NOT reach robust integration where small-φ could not. The Φ-robustness limit holds across BOTH IIT measure families (correlational small-φ exact-MIP AND causal big-Φ TPM-MIP). This is a cleaner, stronger closure than the prior 4× amplitude-confounded 🧱 and than H_1328's estimator-INDEPENDENT (single-measure) closure: the substrate genuinely lacks robust n≤8 integration regardless of which IIT estimator measures it. No GREEN → no wiring follow-on (a_verified_must_wire — nothing to wire). Determinism: re-run byte-identical (run1==run2, hexa 0.1.0-dispatch).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · c9)
TOY n≤8 (n_mod=4 binary units), faithful IIT-4.0 EXACT big-Φ over the system MIP, numpy/engine-mirror DIRECTIONAL (engine-transfer UNVERIFIED). T=64 → empirical TPM is sparse over 2^4=16 states (unseen rows = max-ent 0.5). The result **BOUNDS (does not retract)** the 4 prior small-φ Φ verdicts + H_1328 across the big-Φ measure family. Not ruled out: higher-n big-Φ (>8 needs macro-grain, H_1049 caveat), real-corpus substrate, a third estimator family, finer TPM estimation with longer T.

## Pointers
- Probe: `UNIVERSE/h1331_phi_bigphi.hexa`
- FREEZE + result: `.verdicts/1331_phi_bigphi/{FREEZE,result}.txt`
- Claim: `CLAIMS.tape` @C h1331_phi_bigphi
- Estimator: `hexa-lang/stdlib/consciousness/iit4_bigphi.hexa` (`big_phi`), `iit4_tpm.hexa` (repertoires)
- xref: H_1283 · H_1317 · H_1319 (timing) · H_1320 (division) · **H_1328** (small-φ estimator-independent) · a_phi_iit4_tool · a_no_llm_frame_trap · a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck · a_verified_must_wire · p7 · c9 · c16
