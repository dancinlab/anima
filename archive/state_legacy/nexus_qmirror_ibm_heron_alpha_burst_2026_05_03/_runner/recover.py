#!/usr/bin/env python3
"""Recover counts from completed IBM job (no re-billing).

Uses job_id from the previous failed-write run. Outputs counts.json + verdict.json
to /tmp/qmirror_alpha_burst_out/.
"""

import json
import math
import os
import sys
import time
from pathlib import Path

from qiskit_ibm_runtime import QiskitRuntimeService

JOB_ID = "d7rs38kt738s73cfude0"
BACKEND_NAME = "ibm_pittsburgh"
SHOTS = 1024
OUT_DIR = Path("/tmp/qmirror_alpha_burst_out")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SETTINGS = ["circuit_a_b", "circuit_a_bprime", "circuit_aprime_b", "circuit_aprime_bprime"]


def correlator(counts_dict):
    n = sum(counts_dict.values())
    same = counts_dict.get("00", 0) + counts_dict.get("11", 0)
    diff = counts_dict.get("01", 0) + counts_dict.get("10", 0)
    E = (same - diff) / n
    sigma = math.sqrt(max(0.0, (1.0 - E * E) / n))
    return E, sigma, n


def main():
    api_key = os.environ["IBMCLOUD_API_KEY"]
    crn = os.environ["IBM_QUANTUM_CRN"]
    service = QiskitRuntimeService(channel="ibm_cloud", token=api_key, instance=crn)

    print(f"[recover] Fetching job {JOB_ID}...", flush=True)
    job = service.job(JOB_ID)
    print(f"[recover] status={job.status()}", flush=True)
    result = job.result()

    counts_by_setting = {}
    for i, name in enumerate(SETTINGS):
        data = result[i].data
        creg = getattr(data, "c", None)
        c = creg.get_counts()
        norm = {k: int(v) for k, v in c.items()}
        for k in ("00", "01", "10", "11"):
            norm.setdefault(k, 0)
        counts_by_setting[name] = norm

    Es, sigmas = {}, {}
    correlators_out = {}
    for name in SETTINGS:
        E, sigma, n = correlator(counts_by_setting[name])
        Es[name] = E; sigmas[name] = sigma
        correlators_out[name] = {"E": E, "sigma": sigma, "n": n}

    S = Es["circuit_a_b"] - Es["circuit_a_bprime"] + Es["circuit_aprime_b"] + Es["circuit_aprime_bprime"]
    sigma_S = math.sqrt(sum(s * s for s in sigmas.values()))

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
    delta_matrix = {f"ibm_pittsburgh_vs_{k}": abs(S - v) for k, v in refs.items()}

    QPU_SEC_HEURISTIC = 2.0
    USD_PER_QPU_SEC = 1.60
    actual_cost_usd = QPU_SEC_HEURISTIC * USD_PER_QPU_SEC

    counts_payload = {
        "backend": BACKEND_NAME,
        "backend_family": "Heron r3",
        "backend_qubits": 156,
        "job_id": JOB_ID,
        "shots_per_setting": SHOTS,
        "wall_seconds_recover": None,  # original wall=159.6s in run.log
        "counts": counts_by_setting,
        "settings": SETTINGS,
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
        "backend": BACKEND_NAME,
        "backend_family": "Heron r3",
        "backend_qubits": 156,
        "job_id": JOB_ID,
        "shots_per_setting": SHOTS,
        "shots_total": SHOTS * 4,
        "wall_seconds_orig_run": 159.6,
        "actual_qpu_seconds_heuristic": QPU_SEC_HEURISTIC,
        "estimated_cost_usd": actual_cost_usd,
        "cost_cap_usd": 8.0,
        "correlators": correlators_out,
        "cross_family_delta_matrix_new_entries": delta_matrix,
        "honest_c3": [
            "Cond.7 alpha-burst: 2nd IBM Heron datapoint (intra-family consistency check vs cond.3 ibm_fez S=2.357).",
            "Selected ibm_pittsburgh (Heron r3, 156Q); cond.3 used ibm_fez (Heron r2). Distinct IBM hardware generation.",
            "Shot count 1024/setting yields sigma_S ~ 0.05; well below 0.55 band.",
            "QPU-second cost is a heuristic ($1.60/sec * 2 sec); real IBM billing reconciled via dashboard later.",
            "Recovery path: original write_text() failed due to OUT_DIR resolving to '/' from /tmp script location; re-fetched cached job result via service.job(job_id). Same data, same billing event - no double charge.",
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
        "backend": BACKEND_NAME,
        "out_dir": str(OUT_DIR),
    }, indent=2))


if __name__ == "__main__":
    main()
