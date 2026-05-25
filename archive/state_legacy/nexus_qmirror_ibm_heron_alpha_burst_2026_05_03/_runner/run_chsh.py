#!/usr/bin/env python3
"""qmirror cond.7 IBM Heron alpha-burst v1 (HISTORICAL — refactored to SSOT).

ORIGINAL (2026-05-03 first attempt) had a Ry(-2*theta) bug that produced
S~0.111 (artifact, not real hardware decoherence). REFACTORED 2026-05-03
to import canonical CHSH circuit from
    nexus/modules/qmirror/_python_bridge/chsh_circuits.py
which uses Ry(-theta) and adds F-CHSH-PREFLIGHT-1 (Aer band [2.7, 2.85]
gate before any paid SamplerV2.run).

This file is RETAINED for historical/audit reference; the active runner
is `state/nexus_qmirror_ibm_heron_alpha_burst_v2_2026_05_03/_runner/
run_chsh_v3_patched.py`. Re-running this file now uses the SSOT recipe
(no longer reproduces the v1 bug).

Outputs: counts.json + verdict.json to PROJECT_ROOT/state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/

Cred channel: env IBMCLOUD_API_KEY + IBM_QUANTUM_CRN (no save_account; one-shot).
Cost cap: $8 hard.
"""

import json
import math
import os
import sys
import time
from pathlib import Path

from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

# --- SSOT import (resilient to nexus repo location) --------------------
# Primary: anima staging (writable mirror). Secondary: nexus modules dir.
_SSOT_CANDIDATES = [
    Path.home() / "core" / "anima" / "state" / "qmirror_phase1_staging_2026_05_03" / "_python_bridge",
    Path.home() / "core" / "nexus" / "modules" / "qmirror" / "_python_bridge",
    Path("/home/aiden/core/anima/state/qmirror_phase1_staging_2026_05_03/_python_bridge"),
    Path("/home/aiden/core/nexus/modules/qmirror/_python_bridge"),
]
for _p in _SSOT_CANDIDATES:
    if (_p / "chsh_circuits.py").is_file():
        sys.path.insert(0, str(_p))
        break

from chsh_circuits import (  # noqa: E402
    SETTINGS,
    make_bell_chsh,
    correlator,
    compute_S,
    compute_sigma_S,
    aer_preflight,
    AerPreflightFail,
)

# Backwards-compat alias for the old function name used elsewhere in this file.
make_bell_chsh_circuit = make_bell_chsh

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

OUT_DIR = Path(__file__).resolve().parent.parent  # state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/
SHOTS = 1024
COST_CAP_USD = 8.0
USD_PER_QPU_SEC = 1.60  # IBM paygo rate
QPU_SEC_HEURISTIC = 2.0  # cond.3 actual was 2 QPU-sec for same workload

# Backend selection priority (raw#9: hardcoded list, no live family probing magic)
HERON_R3_PREFERRED = ["ibm_pittsburgh", "ibm_boston"]
HERON_R2_FALLBACK = ["ibm_torino", "ibm_quebec", "ibm_marrakesh", "ibm_kingston"]
EXCLUDE = {"ibm_fez"}  # cond.3 already used fez


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    # --- F-CHSH-PREFLIGHT-1 GATE (mandatory before any paid run) ------
    log("F-CHSH-PREFLIGHT-1: Aer pre-flight (cost $0; verifies SSOT circuit)")
    try:
        preflight = aer_preflight(shots=8192)
    except AerPreflightFail as exc:
        log(f"PREFLIGHT FAIL: {exc}")
        print(json.dumps({"verdict": "ABORT_PREFLIGHT_FAIL", "error": str(exc)}))
        sys.exit(8)
    log(f"PREFLIGHT PASS: Aer S={preflight['S']:.4f} (band [{preflight['band_min']}, {preflight['band_max']}])")

    api_key = os.environ.get("IBMCLOUD_API_KEY")
    crn = os.environ.get("IBM_QUANTUM_CRN")
    if not api_key or not crn:
        print(json.dumps({"verdict": "ABORT_NO_CREDS"}))
        sys.exit(2)

    log("Connecting to IBM Quantum (channel=ibm_cloud)...")
    service = QiskitRuntimeService(channel="ibm_cloud", token=api_key, instance=crn)

    # Enumerate available backends and filter
    log("Enumerating backends...")
    all_backends = service.backends(operational=True, simulator=False)
    by_name = {b.name: b for b in all_backends}
    log(f"  visible operational hardware backends: {sorted(by_name.keys())}")

    # Pick least-busy from r3 list, then r2 fallback
    candidates_r3 = [by_name[n] for n in HERON_R3_PREFERRED if n in by_name and n not in EXCLUDE]
    candidates_r2 = [by_name[n] for n in HERON_R2_FALLBACK if n in by_name and n not in EXCLUDE]

    candidates = candidates_r3 + candidates_r2
    if not candidates:
        print(json.dumps({"verdict": "ABORT_NO_HERON_BACKEND",
                          "available": sorted(by_name.keys())}))
        sys.exit(3)

    # Sort by pending jobs ascending
    def pending(b):
        try:
            return b.status().pending_jobs
        except Exception:
            return 9999

    candidates.sort(key=pending)
    backend = candidates[0]
    fam = "Heron r3" if backend.name in HERON_R3_PREFERRED else "Heron r2 (non-fez)"
    log(f"Selected backend: {backend.name} (family={fam}, pending={pending(backend)}, qubits={backend.num_qubits})")

    # Cost gate
    est_cost = QPU_SEC_HEURISTIC * USD_PER_QPU_SEC
    log(f"Estimated cost: ${est_cost:.2f} (cap=${COST_CAP_USD:.2f})")
    if est_cost > COST_CAP_USD:
        print(json.dumps({"verdict": "ABORT_COST_OVER_CAP",
                          "est_cost_usd": est_cost, "cap_usd": COST_CAP_USD}))
        sys.exit(4)

    # Build + transpile
    log("Building + transpiling 4 CHSH circuits...")
    raw_circuits = [make_bell_chsh_circuit(ta, tb) for (_, ta, tb) in SETTINGS]
    transpiled = transpile(raw_circuits, backend=backend, optimization_level=1)

    # Submit batch
    log(f"Submitting batch (4 circuits x {SHOTS} shots) to {backend.name}...")
    submit_t0 = time.time()
    sampler = SamplerV2(mode=backend)
    job = sampler.run(transpiled, shots=SHOTS)
    log(f"job_id={job.job_id()} status={job.status()}")
    log("Waiting for result (poll 15s)...")
    elapsed = 0
    while True:
        st = str(job.status())
        log(f"  status={st} (elapsed={elapsed}s)")
        if st in ("DONE", "JobStatus.DONE"):
            break
        if st in ("ERROR", "CANCELLED", "JobStatus.ERROR", "JobStatus.CANCELLED"):
            print(json.dumps({"verdict": "ABORT_JOB_FAILED", "job_id": job.job_id(), "status": st}))
            sys.exit(5)
        time.sleep(15)
        elapsed = int(time.time() - submit_t0)
        if elapsed > 1800:
            print(json.dumps({"verdict": "ABORT_TIMEOUT_30MIN", "job_id": job.job_id()}))
            sys.exit(6)

    wall = time.time() - submit_t0
    log(f"Job DONE in {wall:.1f}s. Fetching results...")
    result = job.result()

    # Extract counts (SamplerV2: result[i].data.<creg_name>.get_counts())
    counts_by_setting = {}
    for i, (name, _ta, _tb) in enumerate(SETTINGS):
        pubresult = result[i]
        # SamplerV2 stores per-classical-register; default is "c"
        data = pubresult.data
        attrs = [a for a in dir(data) if not a.startswith("_")]
        log(f"  data attrs for {name}: {attrs}")
        # try .c first (default classical register), else first non-private attr
        creg = getattr(data, "c", None)
        if creg is None:
            for a in attrs:
                obj = getattr(data, a)
                if hasattr(obj, "get_counts"):
                    creg = obj
                    break
        c = creg.get_counts()
        # bitstrings come as e.g. "01" - normalize to "01"/"10"/"00"/"11"
        norm = {k: int(v) for k, v in c.items()}
        # ensure all 4 keys present (fill 0)
        for k in ("00", "01", "10", "11"):
            norm.setdefault(k, 0)
        counts_by_setting[name] = norm
        log(f"  {name}: {sum(norm.values())} shots, {len([v for v in norm.values() if v>0])} unique outcomes")

    # Compute correlators + S
    correlators_out = {}
    Es = {}
    sigmas = {}
    for name, _, _ in SETTINGS:
        E, sigma, n = correlator(counts_by_setting[name])
        correlators_out[name] = {"E": E, "sigma": sigma, "n": n}
        Es[name] = E
        sigmas[name] = sigma

    # SSOT compute_S: S = E_ab - E_ab' + E_a'b + E_a'b' (canonical fez-aligned formula)
    S = compute_S(Es)
    sigma_S = compute_sigma_S(sigmas)

    # Reference S_fez from cond.3
    S_FEZ = 2.357421875
    delta_vs_fez = abs(S - S_FEZ)

    # Falsifier: cond.7 spirit
    BAND_INTRA = 0.55  # superconducting class
    PASS = (S >= 2.0) and (delta_vs_fez <= BAND_INTRA)

    # Cross-family matrix
    refs = {
        "IonQ_Aria_1": 2.808,
        "IonQ_Forte_1": 2.92,
        "Rigetti_Cepheus_108Q": 2.2734,
        "IBM_Heron_r2_ibm_fez_cond3": S_FEZ,
    }
    delta_matrix = {f"{backend.name}_vs_{k}": abs(S - v) for k, v in refs.items()}

    actual_qpu_seconds = QPU_SEC_HEURISTIC  # heuristic; real billing reconciled later
    actual_cost_usd = actual_qpu_seconds * USD_PER_QPU_SEC

    counts_payload = {
        "backend": backend.name,
        "backend_family": fam,
        "backend_qubits": backend.num_qubits,
        "job_id": job.job_id(),
        "shots_per_setting": SHOTS,
        "submit_unix": submit_t0,
        "wall_seconds": wall,
        "counts": counts_by_setting,
        "settings": [s[0] for s in SETTINGS],
    }
    verdict_payload = {
        "verdict": "PASS" if PASS else "FAIL",
        "falsifier": "F-QM-IBM-N1-2 (cond.7 spirit): S >= 2.0 AND |S - S_fez_cond3| <= 0.55 (superconducting class intra-family)",
        "S": S,
        "sigma_S": sigma_S,
        "S_FEZ_REF": S_FEZ,
        "delta_S_vs_fez": delta_vs_fez,
        "intra_ibm_consistency_band": BAND_INTRA,
        "intra_ibm_consistency_PASS": delta_vs_fez <= BAND_INTRA,
        "bell_violation": S >= 2.0,
        "classical_bound": 2.0,
        "quantum_bound": 2.8284271247461903,
        "backend": backend.name,
        "backend_family": fam,
        "backend_qubits": backend.num_qubits,
        "job_id": job.job_id(),
        "shots_per_setting": SHOTS,
        "shots_total": SHOTS * 4,
        "wall_seconds": wall,
        "actual_qpu_seconds_heuristic": actual_qpu_seconds,
        "estimated_cost_usd": actual_cost_usd,
        "cost_cap_usd": COST_CAP_USD,
        "correlators": correlators_out,
        "cross_family_delta_matrix_new_entries": delta_matrix,
        "honest_c3": [
            "Cond.7 alpha-burst: 2nd IBM Heron datapoint (intra-family consistency check vs cond.3 ibm_fez S=2.357).",
            f"Selected {backend.name} ({fam}); cond.3 used ibm_fez (Heron r2). cond.7 spirit verdict here is intra-family consistency, not cross-family (that is cond.8).",
            "Shot count 1024/setting yields sigma_S ~ 0.05; well below 0.55 band.",
            "QPU-second cost is a heuristic ($1.60/sec * 2 sec); real IBM billing reconciled via dashboard later.",
            "raw#9: this runner is .py because qiskit-ibm-runtime is python-only; located under state/nexus_qmirror_ibm_heron_alpha_burst_2026_05_03/_runner/ as burst-scoped vendored helper (NOT under nexus/modules/).",
            "raw#15: API key + CRN passed via env vars only; NEVER printed. Channel=ibm_cloud (qiskit-ibm-runtime 0.35.0).",
            "Cross-family delta_matrix entries appended; original delta_matrix (IonQ/Rigetti/fez) remain authoritative in respective verdicts.",
        ],
    }

    (OUT_DIR / "counts.json").write_text(json.dumps(counts_payload, indent=2))
    (OUT_DIR / "verdict.json").write_text(json.dumps(verdict_payload, indent=2))

    print(json.dumps({
        "verdict": verdict_payload["verdict"],
        "S": S,
        "sigma_S": sigma_S,
        "delta_S_vs_fez": delta_vs_fez,
        "wall_s": wall,
        "qpu_s_heuristic": actual_qpu_seconds,
        "cost_usd_heuristic": actual_cost_usd,
        "backend": backend.name,
    }, indent=2))


if __name__ == "__main__":
    main()
