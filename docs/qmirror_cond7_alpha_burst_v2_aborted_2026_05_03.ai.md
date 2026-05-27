# qmirror cond.7 IBM Heron α-burst v2 — ABORT (no API key)

**Date**: 2026-05-03
**Status**: `ABORT_NO_API_KEY` (no IBM API contact, $0 spent)
**Verdict file**: `state/nexus_qmirror_ibm_heron_alpha_burst_v2_2026_05_03/verdict.json`
**Marker**: `state/markers/qmirror_cond7_alpha_burst_v2_aborted_no_api_key.marker`
**Patched runner (READY)**: `state/nexus_qmirror_ibm_heron_alpha_burst_v2_2026_05_03/_runner/run_chsh_v3_patched.py`

## Why ABORT

Per task spec mandate: *"If `secret check ibmcloud.api_key` fails → ABORT + report user must re-set"*.

`secret list` confirms `ibmcloud.api_key` is **absent** from the secret store. The prior subagent (commit `a86f6b25f`) correctly revoked the v1/v2 key after the burst per raw#15 protocol. Re-submission requires the user to mint a new IBM Cloud API key.

Verified:
- `ibm_quantum.crn` → **PRESENT**
- `ibmcloud.api_key` → **ABSENT** (revoked post-v2, expected behavior)

## What's ready for re-submission

Runner v3 (`run_chsh_v3_patched.py`) is staged with:

1. **Bug patch** — single-line fix in `make_bell_chsh()`:
   - Old (buggy): `qc.ry(-2 * theta_a, 0); qc.ry(-2 * theta_b, 1)`
   - New (canonical): `qc.ry(-theta_a, 0); qc.ry(-theta_b, 1)`

   The doubled angle in v1/v2 is what produced the spurious near-zero S values (S=0.111 / 0.041). Aer simulator with the corrected runner confirms S=2.842 (within ANU reference 2.838).

2. **Backend pinning** — `ibm_boston` (Heron r3) explicitly preferred. Different from cond.3 `ibm_fez` and from v1/v2 `ibm_pittsburgh`, providing the 2nd IBM datapoint required for cond.7 triangulation.

3. **Cost cap reduced** — `COST_CAP_USD = 4.0` (down from $8.00). Per-burst heuristic ~$3.20 leaves headroom.

4. **Cross-vendor matrix** updated to include ANU reference (2.838) alongside IonQ Aria/Forte, Rigetti, IBM_fez_cond3.

## User action required

```
# 1. Mint new key at https://cloud.ibm.com/iam/apikeys
# 2. Store via secret CLI
secret set ibmcloud.api_key '<NEW_KEY>'
# 3. Re-trigger this burst (subagent will re-run with patched runner)
```

## Cross-vendor matrix (current state, v1/v2 INVALID)

| Vendor | Backend | S | Source | Status |
|---|---|---|---|---|
| IBM (super) | ibm_fez (Heron r2) | 2.357 | cond.3 | VALID |
| IBM (super) | ibm_pittsburgh v1/v2 | 0.111 / 0.041 | α-burst v1/v2 | **INVALID** (runner bug) |
| IBM (super) | ibm_boston | TBD | α-burst v3 (pending key) | PENDING |
| Rigetti (super) | Cepheus 108Q | 2.273 | qmirror cond.7 | VALID |
| IonQ (trap) | Aria-1 | 2.808 | qmirror | VALID |
| IonQ (trap) | Forte-1 | 2.920 | qmirror | VALID |
| ANU (photon) | QRNG ref | 2.838 | external reference | VALID |
| Aer (sim) | corrected runner | 2.842 | post-burst validation | VALID |

**qmirror cond.7 spirit verdict**: PASS (Rigetti↔IBM_fez |ΔS|=0.0836, prior verdict unchanged).

## Spec fragmentation note (SSOT consolidation TODO)

Two distinct CHSH circuit conventions co-exist in this codebase:

- **cond.3 runner** (ibm_fez, prior cycle): canonical `Ry(-theta)` → S=2.357 ✓
- **α-burst v1/v2 runners**: drifted to `Ry(-2*theta)` → S~0 ✗

Root cause: independent re-derivation of the basis-rotation step without cross-checking the cond.3 reference implementation. Recommend a future SSOT consolidation cycle to:

1. Promote a single `make_bell_chsh()` to a shared module (e.g. `nexus/qmirror/chsh_circuits.py`).
2. Pin Aer-validation as a pre-flight gate in any runner that touches paid hardware.
3. Add a unit test asserting `S_aer ∈ [2.7, 2.85]` before any `SamplerV2.run` is invoked on a real backend.

## Cost summary

- This attempt spent: **$0.00** (no IBM API contact)
- Cumulative cycle spend: **$6.40 / $8.00** (v1 $3.20 + v2 $3.20, both INVALID hardware data due to runner bug)
- Remaining headroom for v3: **$1.60** under original cap, or fresh **$4.00** under new task-spec cap

## Token revocation status

- `ibmcloud.api_key`: **already absent from secret store** (revoked post-v2 by prior subagent per raw#15).
- IBM Cloud console manual revoke: **assumed complete** (prior subagent's responsibility, no new key in flight).
- This attempt: no new key created → no new revoke action required.
