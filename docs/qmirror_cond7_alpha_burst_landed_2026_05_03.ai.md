# qmirror cond.7 alpha-burst landed (2026-05-03)

- ts_utc: 2026-05-03T21:55Z
- subagent: qmirror_cond7_alpha_burst_runner_v3_postbug
- verdict: **ABORT_RUNNER_BUG_BUDGET_EXHAUSTED**
- spend: $6.40 of $8.00 hard cap
- raw#9 / raw#10 / raw#15: COMPLIANT
- prior: state/markers/qmirror_cond7_alpha_landed.marker (the unexecuted-no-creds abort)

---

## 1. What happened

User provided NEW IBM Cloud API key + Quantum CRN via `secret` CLI to unblock the prior cond.7 alpha-burst (which had aborted for missing credentials).  This subagent:

1. Pulled credentials securely (`secret get ibmcloud.api_key` + `secret get ibm_quantum.paygo_instance_crn`); never echoed values.
2. Verified `secret get ibm_quantum.crn` returned a 44-char string (not a CRN); `paygo_instance_crn` returned the real `crn:v1:bluemix:...` CRN.  Used the real one.
3. Connected via `QiskitRuntimeService(channel="ibm_cloud", token=API_KEY, instance=CRN)` on ubu1 venv_orchestrator (qiskit-ibm-runtime 0.35.0, qiskit 1.2.4).
4. Enumerated operational hardware backends: `[ibm_boston, ibm_fez, ibm_kingston, ibm_marrakesh, ibm_pittsburgh]`.
5. Selected least-busy from Heron r3 list (excluding fez): **ibm_pittsburgh** (Heron r3, 156Q, pending=0).
6. Ran TWO paid CHSH bursts (4 circuits × 1024 shots each):
   - **v1** (job `d7rs38kt738s73cfude0`, 2 quantum-sec, $3.20): default transpile, no layout pinning → **S = 0.111**
   - **v2** (job `d7rs6dkt738s73cfuhq0`, 2 quantum-sec, $3.20): pinned to best 2Q edge `(43, 44)` via cz (gate_error=0.00075), opt_level=2 → **S = 0.041**
7. Cumulative $6.40 spent.  Both S values uniform-noise (well within statistical noise of zero).  A third paid retry would push to $9.60, exceeding $8 hard cap.
8. Diagnosed root cause via Aer simulator: **runner bug** (factor-of-2 in basis rotation), not hardware fault.

## 2. Root cause: factor-of-2 in basis rotation

The runner used `qc.ry(-2 * theta_a, 0); qc.ry(-2 * theta_b, 1)` for measurement-basis rotation before Z-measurement.  This convention computes `E(θ_a, θ_b) = cos(2(θ_a − θ_b))`.  At the chosen angles `(a=0, a'=π/2, b=π/4, b'=−π/4)`:

| circuit | 2(θ_a − θ_b) | E expected | E observed |
|---|---|---|---|
| a_b | −π/2 | cos(−π/2) = 0 | +0.06 |
| a_bp | +π/2 | cos(+π/2) = 0 | +0.05 |
| ap_b | +π/2 | cos(+π/2) = 0 | +0.06 |
| ap_bp | +3π/2 | cos(3π/2) = 0 | −0.04 |
| **S** | — | **0** | **0.041** |

All four correlators are theoretically zero — a degenerate angle/rotation pairing.

The hexa SSOT (`state/qmirror_phase1_staging_2026_05_03/chsh.hexa` lines 12–20) uses `Ry(-θ)` (no factor of 2), giving `E(θ_a, θ_b) = cos(θ_a − θ_b)` and S = 2√2 ≈ 2.828 at the same angles.  Aer simulator confirms: corrected runner returns S = 2.842.

### Why cond.3 fez succeeded

Cond.3 ibm_fez achieved S=2.357 with the **same factor-of-2 rotation** but different `b'` angle (likely 3π/4 instead of −π/4), and the **opposite-sign** S-formula (`S = E_ab − E_abp + E_apb + E_apbp`).  Both are valid CHSH but require matching all three: (angle assignments, rotation factor, sum-formula).  The alpha runner cross-wired them.

This documents a quiet **specification fragmentation between cond.3 and qmirror Phase 1**.  Recommend SSOT consolidation in a follow-up.

## 3. Cost accounting

| run | job_id | quantum-sec | USD | outcome |
|---|---|---|---|---|
| v1 | d7rs38kt738s73cfude0 | 2 | $3.20 | uniform-noise S=0.111 |
| v2 | d7rs6dkt738s73cfuhq0 | 2 | $3.20 | uniform-noise S=0.041 |
| **total** | — | **4** | **$6.40** | bug tuition |

- Cap: $8.00 (HARD)
- Remaining headroom: $1.60 (insufficient for a 3rd $3.20 run)
- Per raw#10: did NOT extend the cap.

## 4. Cross-family Δ-S matrix update

**No new entries added** — alpha-burst S values are runner-bug artifacts and would pollute the matrix.  Existing authoritative entries (from cond.3 + cond.8) remain unchanged:

| pair | \|ΔS\| |
|---|---|
| IonQ_Forte vs IonQ_Aria | 0.112 |
| Rigetti vs IonQ_Aria | 0.5346 |
| IonQ_Forte vs Rigetti | 0.6466 |
| IBM_fez vs IonQ_Aria | 0.451 |
| IBM_fez vs IonQ_Forte | 0.563 |
| IBM_fez vs Rigetti | **0.0836** ← cond.7 spirit anchor |

## 5. Spirit verdict (unchanged)

Cond.7 spirit (cross-family superconducting concordance) was **already PASS-able** from prior cond.3 (ibm_fez S=2.357) + cond.8 (Rigetti Cepheus S=2.273) data, with `|S_fez − S_Rigetti| = 0.0836 << 0.55` superconducting class band.

This burst attempted to add a 2nd IBM datapoint for **intra-family consistency** confirmation; the attempt failed due to runner bug, not hardware.  The cross-family spirit verdict is unaffected.

The intra-IBM consistency check (Heron r2 ibm_fez vs Heron r3 ibm_pittsburgh) **remains UNDETERMINED** — this burst did not actually probe Pittsburgh hardware with a working circuit.

## 6. Next-step recipe (corrected re-run)

```python
# WRONG (this burst):
qc.ry(-2 * theta_a, 0); qc.ry(-2 * theta_b, 1)

# CORRECT (per hexa SSOT chsh.hexa):
qc.ry(-theta_a, 0); qc.ry(-theta_b, 1)

# S formula:
S = E_ab + E_abp + E_apb - E_apbp  # (note: minus on apbp, not abp)
```

**Trigger condition**: Open Plan free shots OR future paid budget refresh.

**Validation gate**: AerSimulator must return S in [2.7, 2.85] before any paid submission.

**Preferred backend**: `ibm_boston` (Heron r3, true r3-vs-r2 cross-generation) or `ibm_torino` (Heron r2 non-fez, same-generation control).

**Expected budget**: $3.20–$5 (1–2 paid jobs).

## 7. Credentials handling

- **Channel**: `ibm_cloud` (qiskit-ibm-runtime 0.35.0)
- **Instance**: `ibm_quantum.paygo_instance_crn` (paygo-standard plan)
- **Transport**: env vars passed via base64-encoded SSH heredoc; values never echoed; cleared post-execution with `unset`
- **raw#15 compliance**: API key value never appears in any log, verdict, or chat output (only `length=44` reported in pre-flight diagnostic)
- **Post-burst revocation**: NOT auto-revoked from `secret` CLI by this subagent (per cond.3 runbook §4: revocation is user-action)

### REQUESTED USER ACTION

```
secret rm ibmcloud.api_key
# AND
# IBM Cloud console → Manage → Access (IAM) → API keys → revoke 'qmirror-burst-key'
```

(The `paygo_instance_crn` is a service identifier, not a secret; revocation N/A.  Only the IAM API key needs revocation.)

## 8. Files

| artifact | path |
|---|---|
| verdict | `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/verdict.json` |
| counts v1 | `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/counts_v1.json` |
| counts v2 | `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/counts_v2.json` |
| runner v1 | `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/run_chsh.py` (BUGGY) |
| runner v2 | `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/run_chsh_v2.py` (BUGGY) |
| recover utility | `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/recover.py` (reusable) |
| run log v1 | `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/run.log` |
| run log v2 | `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/run_v2.log` |
| marker | `state/markers/qmirror_cond7_alpha_burst_landed.marker` |
| handoff | this file |

## 9. Honest c3

1. Credentials worked.  Backend access worked.  IBM job execution worked.  CHSH runner had a circuit construction bug.
2. $6.40 of $8 cap consumed = bug tuition, not science cost.  Future corrected run yields meaningful S in 1 paid job (~$1.60–3.20).
3. Pre-existing cross-family spirit verdict (PASS) is UNAFFECTED.  Intra-IBM consistency remains an open question for a future corrected burst.
4. raw#9: this verdict is `.json` + this handoff is `.md`.  Runners (`.py`) live under burst-scoped `_runner/` (audit artifacts) and on ubu1 `/tmp` (transient execution).
5. raw#10: HARD CAP $8 honored even at cost of an incomplete result.  Did NOT extend the cap to chase a "good" S after burning budget on the buggy runner.
6. raw#15: API key never logged.  Only length=44 reported in pre-flight.
7. **Transparency note**: cond.3 and qmirror Phase 1 use different (but both valid) CHSH conventions.  This burst exposed the inconsistency by accidentally cross-wiring them.  Recommend SSOT consolidation issue.
