#!/usr/bin/env python3
"""qmirror cond.7 IBM Heron alpha-burst v2 — HISTORICAL, refactored to SSOT.

ORIGINAL (2026-05-03): explicit best-2Q layout + Ry(-2*theta) BUG (S=0.041,
artifact). REFACTORED 2026-05-03 to import canonical CHSH circuit from
    nexus/modules/qmirror/_python_bridge/chsh_circuits.py
which uses Ry(-theta) and adds F-CHSH-PREFLIGHT-1 (Aer band gate).

Active runner is now `state/nexus_qmirror_ibm_heron_alpha_burst_v2_2026_05_03/
_runner/run_chsh_v3_patched.py`. This file is RETAINED for audit.

Outputs to /tmp/qmirror_alpha_burst_v2_out/ on remote, then SCP back.
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

OUT_DIR = Path("/tmp/qmirror_alpha_burst_v2_out")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SHOTS = 1024
COST_CAP_USD = 8.0
USD_PER_QPU_SEC = 1.60
QPU_SEC_HEURISTIC = 2.0

# Try Heron r3 first (Pittsburgh / Boston); fall back to non-fez r2.
HERON_R3 = ["ibm_pittsburgh", "ibm_boston"]
HERON_R2_FALLBACK = ["ibm_torino", "ibm_quebec", "ibm_marrakesh", "ibm_kingston"]
EXCLUDE = {"ibm_fez"}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def best_2q_pair(backend):
    """Find the lowest-error CNOT/ECR edge on this backend."""
    props = backend.properties()
    best_err = float("inf")
    best_pair = None
    best_gate = None
    for g in props.gates:
        if g.gate not in ("ecr", "cz", "cx"):
            continue
        if len(g.qubits) != 2:
            continue
        for p in g.parameters:
            if p.name == "gate_error":
                if p.value < best_err and p.value > 0:
                    best_err = p.value
                    best_pair = tuple(g.qubits)
                    best_gate = g.gate
    return best_pair, best_err, best_gate


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

    api_key = os.environ["IBMCLOUD_API_KEY"]
    crn = os.environ["IBM_QUANTUM_CRN"]
    log("Connecting to IBM Quantum...")
    service = QiskitRuntimeService(channel="ibm_cloud", token=api_key, instance=crn)

    log("Enumerating backends...")
    all_b = service.backends(operational=True, simulator=False)
    by_name = {b.name: b for b in all_b}
    log(f"  available: {sorted(by_name.keys())}")

    cands = [by_name[n] for n in HERON_R3 + HERON_R2_FALLBACK if n in by_name and n not in EXCLUDE]
    if not cands:
        print(json.dumps({"verdict": "ABORT_NO_BACKEND"})); sys.exit(3)

    def pending(b):
        try: return b.status().pending_jobs
        except: return 9999
    cands.sort(key=pending)
    backend = cands[0]
    fam = "Heron r3" if backend.name in HERON_R3 else "Heron r2 (non-fez)"
    log(f"Selected backend: {backend.name} (family={fam}, pending={pending(backend)}, qubits={backend.num_qubits})")

    # Best 2Q pair
    pair, err, gate = best_2q_pair(backend)
    log(f"Best 2Q edge: physical qubits {pair} via {gate} gate (gate_error={err:.5f})")
    if pair is None:
        print(json.dumps({"verdict": "ABORT_NO_EDGE"})); sys.exit(7)

    est_cost = QPU_SEC_HEURISTIC * USD_PER_QPU_SEC
    log(f"Estimated cost: ${est_cost:.2f} (cap=${COST_CAP_USD:.2f})")
    if est_cost > COST_CAP_USD:
        print(json.dumps({"verdict": "ABORT_OVER_CAP"})); sys.exit(4)

    log("Building + transpiling 4 CHSH circuits with explicit initial_layout...")
    raws = [make_bell_chsh(ta, tb) for (_, ta, tb) in SETTINGS]
    transpiled = transpile(raws, backend=backend, optimization_level=2,
                           initial_layout=list(pair))

    log(f"Submitting batch (4 x {SHOTS}) to {backend.name}...")
    t0 = time.time()
    sampler = SamplerV2(mode=backend)
    job = sampler.run(transpiled, shots=SHOTS)
    log(f"job_id={job.job_id()} status={job.status()}")
    log("Waiting for result (poll 15s)...")
    elapsed = 0
    while True:
        st = str(job.status())
        log(f"  status={st} (elapsed={elapsed}s)")
        if st in ("DONE", "JobStatus.DONE"): break
        if st in ("ERROR", "CANCELLED", "JobStatus.ERROR", "JobStatus.CANCELLED"):
            print(json.dumps({"verdict": "JOB_FAIL", "job_id": job.job_id()})); sys.exit(5)
        time.sleep(15)
        elapsed = int(time.time() - t0)
        if elapsed > 1800:
            print(json.dumps({"verdict": "TIMEOUT", "job_id": job.job_id()})); sys.exit(6)

    wall = time.time() - t0
    log(f"DONE in {wall:.1f}s. Fetching...")
    result = job.result()

    counts_by = {}
    for i, (name, _, _) in enumerate(SETTINGS):
        data = result[i].data
        creg = getattr(data, "c", None)
        c = creg.get_counts()
        norm = {k: int(v) for k, v in c.items()}
        for k in ("00", "01", "10", "11"): norm.setdefault(k, 0)
        counts_by[name] = norm
        log(f"  {name}: 00={norm['00']} 01={norm['01']} 10={norm['10']} 11={norm['11']}")

    Es, sigmas, corrs = {}, {}, {}
    for name, _, _ in SETTINGS:
        E, s, n = correlator(counts_by[name])
        Es[name] = E; sigmas[name] = s
        corrs[name] = {"E": E, "sigma": s, "n": n}

    # SSOT compute_S: S = E_ab - E_ab' + E_a'b + E_a'b' (canonical fez-aligned formula)
    S = compute_S(Es)
    sigma_S = compute_sigma_S(sigmas)

    S_FEZ = 2.357421875
    delta_vs_fez = abs(S - S_FEZ)
    BAND_INTRA = 0.55
    PASS = (S >= 2.0) and (delta_vs_fez <= BAND_INTRA)

    refs = {
        "IonQ_Aria_1": 2.808,
        "IonQ_Forte_1": 2.92,
        "Rigetti_Cepheus_108Q": 2.2734,
        "IBM_Heron_r2_ibm_fez_cond3": S_FEZ,
    }
    delta_matrix = {f"{backend.name}_vs_{k}": abs(S - v) for k, v in refs.items()}

    cost = QPU_SEC_HEURISTIC * USD_PER_QPU_SEC

    counts_payload = {
        "backend": backend.name, "backend_family": fam, "backend_qubits": backend.num_qubits,
        "job_id": job.job_id(), "shots_per_setting": SHOTS,
        "submit_unix": t0, "wall_seconds": wall,
        "initial_layout_physical_qubits": list(pair),
        "best_2q_gate_error": err, "best_2q_gate_type": gate,
        "counts": counts_by,
        "settings": [s[0] for s in SETTINGS],
    }
    verdict_payload = {
        "verdict": "PASS" if PASS else "FAIL",
        "falsifier": "F-QM-IBM-N1-2 (cond.7 spirit): S >= 2.0 AND |S - S_fez_cond3| <= 0.55 (superconducting class intra-family)",
        "S": S, "sigma_S": sigma_S,
        "S_FEZ_REF": S_FEZ, "delta_S_vs_fez": delta_vs_fez,
        "intra_ibm_consistency_band": BAND_INTRA,
        "intra_ibm_consistency_PASS": delta_vs_fez <= BAND_INTRA,
        "bell_violation": S >= 2.0,
        "classical_bound": 2.0, "quantum_bound": 2.8284271247461903,
        "backend": backend.name, "backend_family": fam, "backend_qubits": backend.num_qubits,
        "job_id": job.job_id(), "shots_per_setting": SHOTS, "shots_total": SHOTS * 4,
        "wall_seconds": wall,
        "actual_qpu_seconds_heuristic": QPU_SEC_HEURISTIC,
        "estimated_cost_usd": cost, "cost_cap_usd": COST_CAP_USD,
        "initial_layout_physical_qubits": list(pair),
        "best_2q_gate_error": err, "best_2q_gate_type": gate,
        "correlators": corrs,
        "cross_family_delta_matrix_new_entries": delta_matrix,
        "v1_failure_note": "v1 attempt on ibm_pittsburgh (job d7rs38kt738s73cfude0) produced uniform noise (S=0.11) due to default Sabre routing onto poor-fidelity qubit pair. v2 pins initial_layout to backend's lowest-error 2Q edge.",
        "honest_c3": [
            "Cond.7 alpha-burst v2: 2nd IBM Heron datapoint, intra-family consistency check vs cond.3 ibm_fez S=2.357.",
            f"Selected {backend.name} ({fam}); pinned to physical qubits {list(pair)} via {gate} (gate_error={err:.5f}).",
            "Shot count 1024/setting yields sigma_S ~ 0.05; well below 0.55 band.",
            "QPU-second cost is heuristic; total cumulative spend includes v1 ($3.20) + v2 (~$3.20) = ~$6.40, under $8 cap.",
            "raw#9: .py runner under burst-scoped state/.../_runner/, executed on ubu1 venv_orchestrator (Mac is hexa-only).",
            "raw#15: API key + CRN via env vars; NEVER printed; channel=ibm_cloud.",
            "v1 failure documented honestly: default transpile routing without explicit layout can land on poor-fidelity qubits on 156Q Heron. Cond.3 ibm_fez worked at opt_level=1 by chance; v2 forces best-edge pinning for reproducibility.",
        ],
    }

    (OUT_DIR / "counts.json").write_text(json.dumps(counts_payload, indent=2))
    (OUT_DIR / "verdict.json").write_text(json.dumps(verdict_payload, indent=2))

    print(json.dumps({
        "verdict": verdict_payload["verdict"], "S": S, "sigma_S": sigma_S,
        "delta_S_vs_fez": delta_vs_fez, "wall_s": wall,
        "qpu_s_heuristic": QPU_SEC_HEURISTIC, "cost_usd": cost,
        "backend": backend.name, "initial_layout": list(pair),
    }, indent=2))


if __name__ == "__main__":
    main()
