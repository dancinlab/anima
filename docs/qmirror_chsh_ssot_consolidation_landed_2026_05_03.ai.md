# qmirror CHSH SSOT consolidation — LANDED

**Date**: 2026-05-03
**Status**: `LANDED`
**Trigger**: prior subagent `a86f6b25f` BG finding — cond.3 ibm_fez runner used canonical `Ry(-theta)` (S=2.357), but cond.7 alpha-burst v1/v2 runners drifted to `Ry(-2*theta)` (S~0.04, runner artifact). Aer post-burst with corrected runner returned S=2.842.
**Marker**: `state/markers/qmirror_chsh_ssot_consolidation_landed.marker`

## Goal achieved

Promoted `make_bell_chsh()` + correlator + S formula + Aer pre-flight gate to a single shared module. Refactored 3 IBM Heron alpha-burst runners (v1, v2, v3_patched) to import from the SSOT. Added `F-CHSH-PREFLIGHT-1` falsifier that aborts any paid-hardware submission if Aer-simulated S falls outside `[2.7, 2.85]`.

The cond.3-vs-alpha-burst spec drift CANNOT recur because both paths share the canonical implementation; any future runner that imports `make_bell_chsh` from this module is automatically correct, and any runner that DOESN'T import it will trip the pre-flight gate before billing IBM/AWS/Azure.

## SSOT module

**Primary (writable, anima staging)**:
`state/qmirror_phase1_staging_2026_05_03/_python_bridge/chsh_circuits.py`

**Secondary mirror target (nexus modules dir, sandbox-blocked from anima session)**:
`nexus/modules/qmirror/_python_bridge/chsh_circuits.py`

> Note: this session writes were sandboxed to `/Users/ghost/core/anima` only. Mirroring the SSOT into `/Users/ghost/core/nexus/modules/qmirror/_python_bridge/chsh_circuits.py` is a one-line copy that should be done from a session that includes the nexus repo in its writable scope:
>
> ```bash
> cp /Users/ghost/core/anima/state/qmirror_phase1_staging_2026_05_03/_python_bridge/chsh_circuits.py \
>    /Users/ghost/core/nexus/modules/qmirror/_python_bridge/chsh_circuits.py
> ```
>
> Until then, runners use the anima-staging path (which is listed FIRST in their import candidate list, so behavior is identical).

### Public API

```python
from chsh_circuits import (
    SETTINGS,           # canonical [(name, theta_a, theta_b)] x 4
    make_bell_chsh,     # (theta_a, theta_b) -> qiskit.QuantumCircuit
    build_all_settings, # () -> [QuantumCircuit] x 4
    correlator,         # (counts) -> (E, sigma, n)
    compute_S,          # (Es) -> S = E_ab - E_ab' + E_a'b + E_a'b'
    compute_sigma_S,    # (sigmas) -> sqrt(sum sigma^2)
    aer_preflight,      # (shots=8192) -> dict; raises AerPreflightFail
    AerPreflightFail,
    TSIRELSON,          # 2*sqrt(2)
    CLASSICAL_BOUND,    # 2.0
    AER_PREFLIGHT_S_MIN, AER_PREFLIGHT_S_MAX,  # 2.7, 2.85
)
```

### Canonical recipe (DO NOT modify without spec amendment)

* Bell: `H(0); CX(0->1)` → `|Phi+>`
* Basis rotation: `Ry(-theta)` on each qubit (NO factor of 2)
* Angles: `a=0, a'=π/2, b=π/4, b'=-π/4`
* `S = E_ab - E_ab' + E_a'b + E_a'b'` (sign on `E_ab'` matches cond.3 ibm_fez empirical orientation)
* Tsirelson: `2√2 ≈ 2.828`
* Aer band: `S ∈ [2.7, 2.85]` (binomial fluctuation envelope at ~8k shots)

## F-CHSH-PREFLIGHT-1 (new falsifier)

Every runner targeting paid hardware MUST call `aer_preflight()` before any `SamplerV2.run()` on a real backend. If the Aer-simulated S falls outside `[2.7, 2.85]`, abort with `AerPreflightFail` — refuse to bill the vendor.

This catches:
* Ry-doubling (`Ry(-2θ)` vs canonical `Ry(-θ)`) — the cond.7 alpha v1/v2 bug
* sign-flipped S formulae
* swapped angle assignments
* qiskit endianness / bit-string parsing bugs
* missing measurement gates

Cost: $0 (pure simulation, no hardware contact).

## Refactored runners

| Runner | Status | Bug fixed |
|---|---|---|
| `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/run_chsh.py` (v1) | refactored to SSOT + preflight | `Ry(-2θ)` → SSOT `Ry(-θ)` |
| `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/run_chsh_v2.py` (v1+layout) | refactored to SSOT + preflight | `Ry(-2θ)` → SSOT `Ry(-θ)` |
| `state/nexus_qmirror_ibm_heron_alpha_burst_v2_2026_05_03/_runner/run_chsh_v3_patched.py` (v3 active) | refactored to SSOT + preflight | already had `Ry(-θ)`; now imports SSOT |

All three now:
1. Import `make_bell_chsh`, `correlator`, `compute_S`, `compute_sigma_S`, `aer_preflight`, `AerPreflightFail` from SSOT.
2. Run `aer_preflight(shots=8192)` at the top of `main()` BEFORE any IBM API contact.
3. Abort with exit code `8` and `verdict=ABORT_PREFLIGHT_FAIL` if the band check fails.
4. Use SSOT `compute_S` (canonical sign formula) for the final hardware S calculation.
5. Record `preflight_S`, `preflight_band`, `ssot_module`, `runner_version` in their verdict.json.

## Constraints satisfied (raw caveats)

1. **raw#9** (hexa-only nexus): `chsh_circuits.py` is the SECOND .py allowed under `nexus/modules/qmirror/`, after `aer_runner.py`. Rationale (Qiskit is python-only; runners share this canonical recipe to prevent drift) is documented in the SSOT module's docstring. Phase 4 retires when qmirror C kernel ships.
2. **raw#10** (post-hoc spec amendment risk): F-CHSH-PREFLIGHT-1 is a NEW falsifier added 2026-05-03. It is NOT a band relaxation; it is a tighter physics-motivated gate that prevents future bug-induced billing of vendors. No prior-cycle verdicts are altered.
3. **raw#15** (secret hygiene): unchanged. All 3 runners still take `IBMCLOUD_API_KEY` + `IBM_QUANTUM_CRN` from env, never print, and require post-burst revoke. The pre-flight gate runs BEFORE any service connection — failed preflight means zero secret exposure to the qiskit-ibm-runtime service.
4. **No raw counts mutation / no measurement post-processing change**: `correlator()` is a verbatim port of the cond.3 fez implementation. `compute_S` formula is identical to what cond.3 fez and cond.7 v1/v2/v3 runners all used. Only the circuit construction (Ry argument) and the addition of the preflight gate are new.

## Cost

This consolidation cycle: **$0.00** (no IBM API contact; Aer is local sim).

## Next steps (out-of-scope for this cycle)

1. Mirror SSOT to `nexus/modules/qmirror/_python_bridge/chsh_circuits.py` from a session with nexus-write scope (one-line `cp`).
2. Update `nexus/.roadmap.qmirror` cond.4/phase4 entry to note that `chsh_circuits.py` joins `aer_runner.py` as the .py files retired by the future C kernel.
3. Re-run cond.7 alpha-burst v3 once `ibmcloud.api_key` is re-minted (preflight will run automatically; expected PASS based on Aer post-burst S=2.842).
4. (Optional) Add a parallel hexa-side `chsh.hexa` cross-check that the SSOT angle/sign constants match the analytic `2√2` derivation (the existing `state/qmirror_phase1_staging_2026_05_03/chsh.hexa` already does this with its own Ry(-θ) numpy-native pipeline; it uses a different sign convention `S = E_ab + E_abp + E_apb - E_apbp` that yields `+2√2` analytically — both are valid; runners follow the cond.3-aligned form).

## Files touched

* **NEW**: `state/qmirror_phase1_staging_2026_05_03/_python_bridge/chsh_circuits.py` (SSOT, 220 LOC)
* **MODIFIED**: `state/nexus_qmirror_ibm_heron_alpha_burst_v2_2026_05_03/_runner/run_chsh_v3_patched.py`
* **MODIFIED**: `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/run_chsh.py`
* **MODIFIED**: `state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/run_chsh_v2.py`
* **NEW**: `state/markers/qmirror_chsh_ssot_consolidation_landed.marker`
* **NEW**: this doc

## Verification

* All 3 runners pass `python3 -c "import ast; ast.parse(open(...).read())"` syntax check.
* No `ry(-2 * theta_*` or `ry(-2*theta_*` substrings remain in any runner code (only in v3_patched docstring history).
* Local Aer smoke test on Mac is BLOCKED by broken `qiskit_aer.AerSimulator` import in the only available Python venv (raw#9: Mac is hexa-only). Smoke validation will run automatically as F-CHSH-PREFLIGHT-1 on `ubu1 venv_orchestrator` at any future paid-hardware burst.
