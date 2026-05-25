# qmirror 2.0 cond.9 - process tomography (F-QM-2-TOMO-9) - LANDED

**date_utc:** 2026-05-04
**verdict:** PASS (7/7 gates)
**cost_usd:** 0.00 ($0 Aer-local)
**wall_seconds_total:** 8.68
**source:** RETRY of bg ac9c99dd (quota); cycle land via subagent BG

---

## Verdict

| field | value |
|---|---|
| cond | qmirror.cond9_tomography |
| falsifier_id | F-QM-2-TOMO-9 |
| verdict | PASS |
| n_pass / n_total | 7 / 7 |
| fidelity_min | 0.99918 (CNOT) |
| fidelity_mean | 1.00023 |
| fidelity_threshold | 0.99 |
| method | linear-inversion process tomography |
| engine | qiskit_aer 0.17.2 (noiseless) |
| n_shots | 8000 |
| seed | 2026 |

cond.9 MET. Verifier:

```
jq '.fidelity_min >= 0.99 and .ok == 1' \
  /Users/ghost/core/anima/state/qmirror_2_cond9_tomography_2026_05_03/verdict.json
```

## Per-gate fidelity matrix

| gate | n_qubits | n_circuits | process_fidelity | avg_gate_fidelity | wall_s | PASS |
|------|---------:|-----------:|-----------------:|------------------:|-------:|:---:|
| H    | 1 |  12 | 1.00197 | 1.00131 | 0.81 | YES |
| X    | 1 |  12 | 1.00009 | 1.00006 | 0.45 | YES |
| Y    | 1 |  12 | 0.99991 | 0.99994 | 0.45 | YES |
| Z    | 1 |  12 | 1.00053 | 1.00035 | 0.44 | YES |
| S    | 1 |  12 | 0.99991 | 0.99994 | 0.44 | YES |
| T    | 1 |  12 | 1.00001 | 1.00001 | 0.45 | YES |
| CNOT | 2 | 144 | 0.99918 | 0.99934 | 5.28 | YES |

(process_fidelity values slightly above 1.0 are statistical floor effects from
 finite-sample Pauli expectation estimates; they remain inside the
 trust region for F-QM-2-TOMO-9.)

## Method

Linear-inversion quantum process tomography on a noiseless AerSimulator.

For each n-qubit target gate U:

1. **Prep sweep (4^n):** prepare each qubit in
   { |0>, |1>, |+>, |+i> } via Clifford prep circuits.
2. **Apply U** (gate under test).
3. **Measurement basis sweep (3^n):** apply pre-measurement rotation
   { I, H, S†H } for { Z, X, Y } readout, then computational-basis
   measurement, n_shots samples per setting.
4. **Reconstruct rho_out** for each prep state via the standard
   Pauli-expansion estimator
   `rho = (1/2^n) Σ_p Tr(P rho) P`
   where `Tr(P rho)` is the basis-aligned outcome correlation.
5. **Assemble Choi matrix** by writing each computational dyad |i><j| as
   a linear combination of the four prep densities (per-qubit
   decomposition, tensored across qubits) and substituting the
   corresponding rho_out:
   `Choi(U) = Σ_{ij} |i><j| ⊗ U(|i><j|)U†`
6. **Compare to ideal** Choi(U) via
   `qiskit.quantum_info.process_fidelity` and `average_gate_fidelity`.

PASS criterion: `process_fidelity >= 0.99` for **every** gate.

## Deliverables

| path | sha256 |
|---|---|
| /Users/ghost/core/qmirror/modules/process_tomography.hexa                              | 4c2fbfc96d5b4ee0… |
| /Users/ghost/core/nexus/modules/qmirror/process_tomography.hexa                        | 4c2fbfc96d5b4ee0… (mirror) |
| /Users/ghost/core/qmirror/modules/_python_bridge/process_tomography_runner.py          | b25b1702d627e262… |
| /Users/ghost/core/nexus/modules/qmirror/_python_bridge/process_tomography_runner.py    | b25b1702d627e262… (mirror) |
| /Users/ghost/core/anima/state/qmirror_2_cond9_tomography_2026_05_03/verdict.json       | 1de6219bb131e104… |
| /Users/ghost/core/anima/state/qmirror_2_cond9_tomography_2026_05_03/per_gate_fidelity.json | fb8bfc556e3a8ad1… |
| /Users/ghost/core/anima/state/qmirror_2_cond9_tomography_2026_05_03/choi_matrices.npz  | 35ebca333194eb91… |
| /Users/ghost/core/anima/state/qmirror_2_cond9_tomography_2026_05_03/run.log            | 7480f202889924b1… |
| /Users/ghost/core/anima/state/markers/qmirror_2_cond9_tomography_landed.marker         | (this cycle's marker) |
| /Users/ghost/core/anima/docs/qmirror_2_cond9_tomography_landed_2026_05_03.ai.md        | (this doc) |

`process_tomography.hexa` is ~330 LoC hexa-strict (raw#15 no emoji);
`process_tomography_runner.py` is ~360 LoC qiskit + qiskit-aer wrapper.
Both files mirror byte-for-byte between `qmirror/modules/` (standalone)
and `nexus/modules/qmirror/` (anima-internal nexus).

## raw#10 caveats (4)

1. **Linear inversion only.** No MLE or projected-CP correction. Shot noise
   produces small negative Choi eigenvalues on every gate (the
   "channel not CP" warnings are suppressed in the runner; the largest
   negative eigenvalue across the 7-gate sweep is ≈ -0.066 on CNOT, well
   inside the noise floor). Banaszek-style MLE and Smolin-Gambetta
   projected-CP are roadmap items for Phase 3.

2. **Qubit ceiling n ≤ 4.** Pauli-product POVM cap; 4^n prep states ×
   3^n measurement bases scales quickly. The 7-gate sweep tops at CNOT
   (n=2): 4^2 × 3^2 = 144 circuits per gate. Compressed-sensing
   (Flammia-Gross 2012) is Phase 4 territory and requires an SDP solver.

3. **Choi data flat-list transport.** raw#9 forbids native complex types
   in hexa, so the bridge ships Choi as `choi_re` + `choi_im` lists.
   The runner persists them as a single NPZ blob
   (`choi_matrices.npz`, 14 arrays = 7 gates × {re, im}). The hexa
   wrapper does **not** load the matrix back into hexa structs - it
   only consumes the fidelity scalars from the bridge response.

4. **Aer noiseless ≠ QPU calibration.** F-QM-2-TOMO-9 PASS validates
   the **reconstruction pipeline** end-to-end (state prep, measurement
   rotation, Pauli expansion, Choi assembly, fidelity vs ideal). It
   does **not** claim that any real QPU achieves these fidelities.
   QPU process tomography is a separate cond (qmirror.cond12_surface
   for the surface-d3 path, or `.roadmap.ionq` for vendor-side QPT).

## Constraints honoured

- **raw#9** (.py only via `_python_bridge/`): one new file
  `process_tomography_runner.py` added under `_python_bridge/`. No
  other .py files added. Hexa wrapper transports JSON over
  stdin/stdout, identical pattern to `aer_runner.py`.
- **raw#10** (4-caveat ceiling): exactly 4 caveats above.
- **raw#15** (no emoji in source): both new files are ASCII only.
- **F-CHSH-PREFLIGHT-1 pattern**: Aer-local first; verdict JSON +
  reproducible bridge invocation embedded; SHA256 provenance for
  every artifact.
- **$0 cost cap**: Aer noiseless local; total wall 8.68 s on Mac.

## Reproduce

```
echo '{"mode":"sweep","gates":["H","X","Y","Z","S","T","CNOT"],"n_shots":8000,"seed":2026}' \
  | /Users/ghost/etc/anima-quantum/.venv/bin/python3 \
    /Users/ghost/core/qmirror/modules/_python_bridge/process_tomography_runner.py
```

Or via hexa selftest (1-qubit H, ~1 s):

```
hexa run /Users/ghost/core/qmirror/modules/process_tomography.hexa
# expects: __QMIRROR_PROCESS_TOMOGRAPHY__ PASS
```

## Provenance

- python   = 3.14 (`/Users/ghost/etc/anima-quantum/.venv/bin/python3`)
- qiskit   = 2.4.1
- qiskit_aer = 0.17.2
- numpy    = (venv-bundled)

`qiskit_experiments` was **not** required (the task brief permitted it,
but qiskit's native `quantum_info` API was sufficient: `Operator`,
`Choi`, `process_fidelity`, `average_gate_fidelity`).

## Sentinel

`__QMIRROR_PROCESS_TOMOGRAPHY_COND9__ PASS`
`F-QM-2-TOMO-9 = PASS  (cond.9 MET)`
