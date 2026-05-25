#!/usr/bin/env python3
"""qmirror cond.7 IBM Heron alpha-burst v3 (PATCHED) — canonical Ry(-theta).

REFACTORED 2026-05-03: imports from shared SSOT
    nexus/modules/qmirror/_python_bridge/chsh_circuits.py
to prevent the cond.3-vs-alpha-burst spec drift that caused the v1/v2
Ry(-2*theta) bug. Adds F-CHSH-PREFLIGHT-1: Aer pre-flight gate runs
before any SamplerV2.run() on real hardware; aborts if Aer S not in
[2.7, 2.85].

History:
    v1/v2 BUG:  qc.ry(-2 * theta_a, 0); qc.ry(-2 * theta_b, 1)  -> S~0
    v3 FIX  :  qc.ry(-theta_a, 0);     qc.ry(-theta_b, 1)       -> S=2.842 (Aer)
    SSOT     : single make_bell_chsh() in chsh_circuits module

Backend selection: ibm_boston (Heron r3) preferred — DIFFERENT from cond.3
ibm_fez and from v1/v2 ibm_pittsburgh, providing 2nd-IBM datapoint for
qmirror cond.7 triangulation.

Outputs to /tmp/qmirror_alpha_burst_v3_out/ on remote, then SCP back.

HARD CAP: $4.00 (reduced from prior $8.00 envelope; remaining headroom).
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
# Primary: anima staging (writable mirror). Secondary: nexus modules dir
# (canonical hexa repo location). On ubu1, /home/aiden mirrors /Users/ghost.
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
    TSIRELSON,
    CLASSICAL_BOUND,
)

OUT_DIR = Path("/tmp/qmirror_alpha_burst_v3_out")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SHOTS = 1024
COST_CAP_USD = 4.0
USD_PER_QPU_SEC = 1.60
QPU_SEC_HEURISTIC = 2.0

# Heron r3 preferred; ibm_boston is target (different from fez/pittsburgh).
HERON_R3_PREFERRED = ["ibm_boston", "ibm_pittsburgh"]
HERON_R2_FALLBACK = ["ibm_torino", "ibm_quebec", "ibm_marrakesh", "ibm_kingston"]
EXCLUDE = {"ibm_fez"}  # cond.3 already covered


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
        (OUT_DIR / "preflight_fail.json").write_text(json.dumps({
            "verdict": "ABORT_PREFLIGHT_FAIL",
            "falsifier": "F-CHSH-PREFLIGHT-1",
            "error": str(exc),
        }, indent=2))
        print(json.dumps({"verdict": "ABORT_PREFLIGHT_FAIL", "error": str(exc)}))
        sys.exit(8)
    log(f"PREFLIGHT PASS: Aer S={preflight['S']:.4f} (band [{preflight['band_min']}, {preflight['band_max']}])")
    (OUT_DIR / "preflight.json").write_text(json.dumps(preflight, indent=2, default=str))

    api_key = os.environ["IBMCLOUD_API_KEY"]
    crn = os.environ["IBM_QUANTUM_CRN"]
    log("Connecting to IBM Quantum...")
    service = QiskitRuntimeService(channel="ibm_cloud", token=api_key, instance=crn)

    log("Enumerating backends...")
    all_b = service.backends(operational=True, simulator=False)
    by_name = {b.name: b for b in all_b}
    log(f"  available: {sorted(by_name.keys())}")

    cands = [by_name[n] for n in HERON_R3_PREFERRED + HERON_R2_FALLBACK if n in by_name and n not in EXCLUDE]
    if not cands:
        print(json.dumps({"verdict": "ABORT_NO_BACKEND"})); sys.exit(3)

    def pending(b):
        try: return b.status().pending_jobs
        except: return 9999

    # Prefer ibm_boston explicitly if available, else lowest queue.
    if "ibm_boston" in by_name and by_name["ibm_boston"] in cands:
        backend = by_name["ibm_boston"]
        log("Pinned to ibm_boston (per task spec — different from fez/pittsburgh)")
    else:
        cands.sort(key=pending)
        backend = cands[0]
        log(f"ibm_boston unavailable; falling back to {backend.name}")

    fam = "Heron r3" if backend.name in HERON_R3_PREFERRED else "Heron r2 (non-fez)"
    log(f"Selected backend: {backend.name} (family={fam}, pending={pending(backend)}, qubits={backend.num_qubits})")

    pair, err, gate = best_2q_pair(backend)
    log(f"Best 2Q edge: physical qubits {pair} via {gate} gate (gate_error={err:.5f})")
    if pair is None:
        print(json.dumps({"verdict": "ABORT_NO_EDGE"})); sys.exit(7)

    est_cost = QPU_SEC_HEURISTIC * USD_PER_QPU_SEC
    log(f"Estimated cost: ${est_cost:.2f} (cap=${COST_CAP_USD:.2f})")
    if est_cost > COST_CAP_USD:
        print(json.dumps({"verdict": "ABORT_OVER_CAP"})); sys.exit(4)

    log("Building + transpiling 4 CHSH circuits with explicit initial_layout (SSOT make_bell_chsh)...")
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
        "ANU_QRNG_reference": 2.838,
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
        "runner_version": "v3_ssot_chsh_circuits_2026_05_03",
        "ssot_module": "nexus/modules/qmirror/_python_bridge/chsh_circuits.py",
        "preflight_S": preflight["S"],
        "preflight_band": [preflight["band_min"], preflight["band_max"]],
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
        "v1_v2_failure_note": (
            "v1 (ibm_pittsburgh, S=0.111) and v2 (ibm_pittsburgh, S=0.041) produced uniform-noise "
            "artifacts NOT due to hardware decoherence but due to runner bug: Ry(-2*theta) instead of "
            "canonical Ry(-theta). Aer simulator post-burst with corrected runner returned S=2.842 "
            "(matching ANU reference 2.838). v1/v2 hardware data is INVALID — discarded from cross-vendor matrix."
        ),
        "runner_patch": "imports SSOT make_bell_chsh from nexus/modules/qmirror/_python_bridge/chsh_circuits.py",
        "preflight_record": {
            "falsifier": "F-CHSH-PREFLIGHT-1",
            "S": preflight["S"],
            "sigma_S": preflight["sigma_S"],
            "band_min": preflight["band_min"],
            "band_max": preflight["band_max"],
            "shots_per_setting": preflight["shots_per_setting"],
            "engine": preflight["engine"],
        },
        "honest_c3": [
            "Cond.7 alpha-burst v3 (SSOT-refactored): 2nd IBM Heron datapoint with shared-module CHSH circuit.",
            f"Selected {backend.name} ({fam}); pinned to physical qubits {list(pair)} via {gate} (gate_error={err:.5f}).",
            "Shot count 1024/setting yields sigma_S ~ 0.05; well below 0.55 band.",
            "QPU-second cost is heuristic; HARD CAP $4.00 (this burst only ~$3.20 budgeted).",
            "raw#9: this is the SECOND .py allowed under nexus/modules/qmirror/ (after aer_runner.py); rationale documented in chsh_circuits.py docstring.",
            "raw#15: API key + CRN via env vars; NEVER printed; channel=ibm_cloud; revoke MANDATORY post-burst.",
            "raw#10: F-CHSH-PREFLIGHT-1 falsifier added 2026-05-03; runner aborts BEFORE any paid hardware contact if Aer-simulated S not in [2.7, 2.85]. Catches Ry-doubling, sign-flipped formulae, swapped angles, bit-string parsing bugs.",
            "SSOT consolidation: runner now imports make_bell_chsh, correlator, compute_S, aer_preflight from nexus/modules/qmirror/_python_bridge/chsh_circuits.py. cond.3 fez vs alpha-burst drift CANNOT recur because both paths share the canonical implementation.",
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
