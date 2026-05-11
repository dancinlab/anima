<!-- [Hc_958 qmirror-2-5-conds-cluster — moved to hypotheses_candidates/Hc_958_qmirror_2_5_conds_cluster.md on 2026-05-11] -->

# qmirror 2.0 cond.11 — Stabilizer-measurement primitive — LANDED

**Date:** 2026-05-04
**Falsifier:** F-QM-2-STAB-11
**Verdict:** **PASS**
**Verdict path:** `anima/state/qmirror_2_cond11_stabilizer_2026_05_04/verdict.json`
**Cost:** $0.00 (Aer state-vector local; no QPU shots)
**Wall:** ~3 s observed for 1792 noiseless 4-qubit shots
**Spec ref:** `anima/docs/qmirror_2_axes_spec_2026_05_03.md` §2 (axis 3, cond.11)

---

## Headline numbers

| Metric                  | Observed | Threshold | Pass? |
|-------------------------|---------:|----------:|:-----:|
| syndrome_plus_ratio     | 1.0      | >= 0.99   | YES   |
| syndrome_zz_plus_ratio  | 1.0      | >= 0.99   | YES   |
| syndrome_xx_plus_ratio  | 1.0      | >= 0.99   | YES   |
| post_fidelity           | 1.0      | >= 0.99   | YES   |
| <ZZ>                    | +1.0     | analytic +1 | YES |
| <XX>                    | +1.0     | analytic +1 | YES |
| <YY>                    | -1.0     | analytic -1 | YES |

PASS gate: `syndrome_plus_ratio >= 0.99 AND post_fidelity >= 0.99` -> **CLEARED**

---

## What landed

1. **`/Users/ghost/core/qmirror/modules/stabilizer.hexa`** (~210 LoC)
   - `fn stabilizer_run(n_trials, seed) -> StabilizerVerdict`
   - `_selftest()` runs the full F-QM-2-STAB-11 check
   - `__QMIRROR_STABILIZER__ <PASS|FAIL>` sentinel
   - Bridge resolver pattern identical to `chsh.hexa` / `ghz_mermin.hexa`
     (`NEXUS_QMIRROR_BRIDGE_PATH` env override -> HOME-relative fallback)
   - **Two notable wrapper hardening fixes** (vs the ghz_mermin.hexa template
     they were copied from):
     * `index_of("{")` (FIRST open-brace) instead of `last_index_of("{")`
       so JSON extraction lands on the OUTERMOST object, not a nested
       sub-object like `post_basis_E:{...}`. The latter was silently
       corrupting parses on responses with any nested map.
     * Direct field assignment from the parsed map instead of `to_str()` /
       `to_float()` (those builtins are not present in the active hexa
       runtime). Type annotations on `let` bindings preserve schema intent.

2. **`/Users/ghost/core/qmirror/modules/_python_bridge/stabilizer_runner.py`** (~330 LoC)
   - Implements the ancilla-mediated Z⊗Z + X⊗X stabilizer protocol on
     qiskit `AerSimulator(method="statevector")` with full numpy-native
     fallback (16-amplitude statevector, mid-circuit equivalent via
     pre-measurement basis rotations).
   - Default tier: `qiskit_aer` if `qiskit-aer` importable; else
     `numpy_native` (mathematically identical for noiseless SV).
   - Stratified shot allocation: `n_trials` shots for syndrome stats +
     `max(256, n_trials/4)` shots for each of 3 post-tomography bases
     (ZZ, XX, YY) -> Bell-witness `F = (1+<ZZ>+<XX>-<YY>)/4`.
   - 0 .py files added under `anima/` repo root (raw#9 compliance).

3. **`/Users/ghost/core/anima/state/qmirror_2_cond11_stabilizer_2026_05_04/`**
   - `verdict.json` — canonical falsifier verdict + 4 caveats array
   - `syndrome_stats.json` — Z⊗Z, X⊗X, joint counts + ratios
   - `post_fid.json` — Bell-witness fidelity + per-basis Pauli expectations
   - `_full_run.json` — raw bridge response (debugging)
   - `run.log` — runtime log (config, results, hexa-wrapper sentinel)

4. **`/Users/ghost/core/anima/state/markers/qmirror_2_cond11_stabilizer_landed.marker`**
   - Headline numbers + reverify recipe.

---

## Protocol (4-qubit ancilla-mediated stabilizer measurement)

```
Qubits:  q0,q1 = data    q2 = ancilla a0 (ZZ)    q3 = ancilla a1 (XX)
Classical bits: c[0]=s_zz, c[1]=s_xx, c[2]=q0_readout, c[3]=q1_readout

(1) Bell prep         H(q0) ; CNOT(q0, q1)
(2) Z⊗Z syndrome      H(q2) ; CNOT(q0, q2) ; CNOT(q1, q2) ; H(q2) ; measure q2 -> c[0]
(3) X⊗X syndrome      H(q3) ; CNOT(q3, q0) ; CNOT(q3, q1) ; H(q3) ; measure q3 -> c[1]
(4) Post-tomography   per-trial choose basis in {ZZ, XX, YY}:
                      apply rotation (H for X, S^dag+H for Y) on q0,q1
                      then measure q0,q1 -> c[2],c[3]
(5) Aggregate         F(|Phi+>) = (1 + <ZZ> + <XX> - <YY>) / 4
                      conditioned on (s_zz, s_xx) = (0, 0)  i.e. (+1, +1)
```

Analytic: `|Phi+>` is +1 eigenstate of both Z⊗Z and X⊗X (commuting
stabilizers); noiseless Aer reproduces F=1.0, syndrome_plus_ratio=1.0
exactly. Real hardware would show finite-fidelity decay.

---

## raw#10 caveats (4)

1. **Aer noiseless ceiling.** Reproduces analytic 1.0/1.0 exactly because
   `|Phi+>` is a perfect simultaneous eigenstate of Z⊗Z and X⊗X, and the
   ancilla-CNOT gadgets implement an exact projective non-destructive
   measurement on the +1 eigenspace. Real hardware (IBM/IonQ/Rigetti)
   would exhibit two-qubit-gate infidelity, ancilla T1/T2 decay, and SPAM
   error; expected hardware regime is `synd_plus_ratio in [0.85, 0.97]`
   and `post_fid in [0.80, 0.95]` without QEC.

2. **Bell-witness vs full process tomography.** Post-fidelity is
   reconstructed via the 3-Pauli witness `F = (1+<ZZ>+<XX>-<YY>)/4`
   conditioned on syndrome `(+1,+1)`. This is a tight lower bound for
   pure `|Phi+>` but does NOT replace cond.9 process tomography for the
   full Choi-matrix verification. Cross-cond.9 cross-check is a soft dep
   not exercised here.

3. **Sequential (not simultaneous) two-stabilizer measurement.** The two
   commuting stabilizers Z⊗Z and X⊗X are measured sequentially via two
   separate ancillas. On the |Phi+> eigenstate the order is irrelevant.
   On non-stabilizer states the residual `(+1,-1)` etc. outcomes would
   project onto error syndrome subspaces; cond.12 (surface-code distance-3
   toy) builds on this primitive with simultaneous d=3 syndrome readout.

4. **$0 default substrate is Aer-only; no QPU shots submitted.**
   Cross-tech reproduction (cond.7-style multi-vendor anchor) is OUT OF
   SCOPE for cond.11 by design (qmirror_2_axes_spec §2 axis 3 explicitly
   labels the Aer-noiseless protocol as the falsifier baseline). cond.11
   PASS validates the gadget construction + measurement pipeline; QPU
   validation is a separate cond.12 sister cycle.

---

## raw rule compliance

- **raw#9** (.py only via `_python_bridge/`): bridge lives at
  `qmirror/modules/_python_bridge/stabilizer_runner.py`; 0 .py files added
  under `anima/` repo root.
- **raw#10** (4 caveats per land doc): see above.
- **raw#15** (no personal paths in artifact bodies): bridge resolved via
  `NEXUS_QMIRROR_BRIDGE_PATH` env or `$HOME`-relative fallback; verdict.json
  / syndrome_stats.json / post_fid.json contain no `/Users/<name>` strings.

---

## Mirror

- qmirror standalone (`/Users/ghost/core/qmirror/`): code lives here
  (`modules/stabilizer.hexa` + `modules/_python_bridge/stabilizer_runner.py`).
- nexus legacy (`/Users/ghost/core/nexus/modules/qmirror/`): **REMOVED** per
  `state/markers/nexus_qmirror_legacy_removed_landed.marker`; no mirror.
- anima (`/Users/ghost/core/anima/`): verdict + handoff + marker land here.

---

## Reverify

```
hexa run /Users/ghost/core/qmirror/modules/stabilizer.hexa
# expect:  __QMIRROR_STABILIZER__ PASS

jq '.syndrome_plus_ratio >= 0.99 and .post_fidelity >= 0.99' \
   /Users/ghost/core/anima/state/qmirror_2_cond11_stabilizer_2026_05_04/verdict.json
# expect:  true
```

---

## Status

**qmirror 2.0 cond progression:**
| cond | falsifier        | status |
|------|------------------|--------|
| 9    | F-QM-2-TOMO-9    | LANDED 2026-05-03 |
| 10   | F-QM-2-GHZ-10    | LANDED 2026-05-03 |
| 11   | F-QM-2-STAB-11   | **LANDED 2026-05-04 (this cycle)** |
| 12   | F-QM-2-SURF-12   | NEXT — surface-code d=3 toy, depends on cond.11 |
| 13   | F-QM-2-CSCS-13   | DEFERRED — chained sequential CHSH |

cond.11 PASS unblocks cond.12 (surface-code distance-3 toy uses the
stabilizer measurement primitive landed here for its plaquette/vertex
syndrome rounds).
