#!/usr/bin/env python3
"""qmirror cond.8 option β cross-vendor CHSH submission.

Submits identical Bell-state circuits with 4 measurement bases to:
  - IonQ Forte 1 (us-east-1)  : 4 × 100 shots
  - Rigetti Cepheus-1-108Q (us-west-1) : 4 × 1024 shots

Reuses circuit JSONs from state/nexus_chsh_bell_2026_05_02/.
DRY_RUN by default (env QMIRROR_DRY_RUN=1). LIVE = QMIRROR_DRY_RUN=0.

Output: writes submissions.json with task ARNs + per-vendor metadata.
"""
import os
import json
import time
import sys
import math

os.environ["AWS_PROFILE"] = "braket"

REF_DIR = "/Users/ghost/core/anima/state/nexus_chsh_bell_2026_05_02"
OUT_DIR = "/Users/ghost/core/anima/state/qmirror_chsh_xvendor_2026_05_03"

IONQ_ARN = "arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1"
RIGETTI_ARN = "arn:aws:braket:us-west-1::device/qpu/rigetti/Cepheus-1-108Q"

IONQ_SHOTS = 100
RIGETTI_SHOTS = 1024

# Pricing (per AWS Braket public list price 2025/2026)
IONQ_TASK_FEE = 0.30
IONQ_SHOT_FEE = 0.08
RIGETTI_TASK_FEE = 0.30
RIGETTI_SHOT_FEE = 0.000425

# Bell + 4 measurement bases (a, a' on Alice; b, b' on Bob).
# Reuse identical openqasm3 circuits from nexus_chsh_bell_2026_05_02 reference.
SETTINGS = [
    ("circuit_a_b",         "a",  "b"),
    ("circuit_a_bprime",    "a",  "b'"),
    ("circuit_aprime_b",    "a'", "b"),
    ("circuit_aprime_bprime","a'", "b'"),
]

DRY_RUN = os.environ.get("QMIRROR_DRY_RUN", "1") != "0"


def build_circuit_from_openqasm(qasm_str):
    """Build a braket.circuits.Circuit from the QASM3 in the reference json.

    The reference circuits are minimal: H, CNOT, RY, measure.  We reproduce
    them programmatically to use the SDK's Circuit class which is portable
    across vendors.
    """
    from braket.circuits import Circuit
    c = Circuit()
    # Parse key lines: h q[0]; cnot q[0],q[1]; ry(angle) q[i];
    # ignore measure lines — Braket auto-measures all qubits.
    for line in qasm_str.splitlines():
        s = line.strip().rstrip(";").lower()
        if s.startswith("h "):
            qb = int(s.split("q[")[1].split("]")[0])
            c.h(qb)
        elif s.startswith("cnot "):
            parts = s.replace("cnot", "").strip()
            ctrl = int(parts.split("q[")[1].split("]")[0])
            tgt = int(parts.split("q[")[2].split("]")[0])
            c.cnot(ctrl, tgt)
        elif s.startswith("ry("):
            angle = float(s.split("ry(")[1].split(")")[0])
            qb = int(s.split("q[")[1].split("]")[0])
            c.ry(qb, angle)
        # measure lines ignored
    return c


def load_circuits():
    out = []
    for name, alice, bob in SETTINGS:
        p = os.path.join(REF_DIR, name + ".json")
        with open(p) as f:
            j = json.load(f)
        circuit = build_circuit_from_openqasm(j["openqasm3"])
        out.append({
            "name": name,
            "alice": alice,
            "bob": bob,
            "circuit": circuit,
            "qasm": j["openqasm3"],
        })
    return out


def cost_estimate():
    ionq_cost = IONQ_TASK_FEE * 4 + IONQ_SHOT_FEE * IONQ_SHOTS * 4
    rig_cost = RIGETTI_TASK_FEE * 4 + RIGETTI_SHOT_FEE * RIGETTI_SHOTS * 4
    return ionq_cost, rig_cost, ionq_cost + rig_cost


def submit_vendor(vendor_label, device_arn, shots, circuits):
    from braket.aws import AwsDevice
    device = AwsDevice(device_arn)
    rec = []
    for c in circuits:
        if DRY_RUN:
            rec.append({
                "name": c["name"],
                "alice": c["alice"],
                "bob": c["bob"],
                "task_arn": "DRY_RUN",
                "shots": shots,
                "device_arn": device_arn,
                "vendor": vendor_label,
                "submitted_at": time.time(),
            })
            continue
        task = device.run(c["circuit"], shots=shots)
        rec.append({
            "name": c["name"],
            "alice": c["alice"],
            "bob": c["bob"],
            "task_arn": task.id,
            "shots": shots,
            "device_arn": device_arn,
            "vendor": vendor_label,
            "submitted_at": time.time(),
        })
        print(f"  [{vendor_label}] {c['name']}: {task.id}", flush=True)
    return rec


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    circuits = load_circuits()
    ionq_cost, rig_cost, total = cost_estimate()
    print(f"DRY_RUN={DRY_RUN}", flush=True)
    print(f"Cost estimate: IonQ ${ionq_cost:.2f}, Rigetti ${rig_cost:.2f}, total ${total:.2f}", flush=True)
    if total > 80.0:
        print("HARD CAP $80 EXCEEDED — abort", flush=True)
        sys.exit(2)
    print("Submitting IonQ Forte 1 ...", flush=True)
    ionq_rec = submit_vendor("ionq_forte_1", IONQ_ARN, IONQ_SHOTS, circuits)
    print("Submitting Rigetti Cepheus-1-108Q ...", flush=True)
    rig_rec = submit_vendor("rigetti_cepheus_108q", RIGETTI_ARN, RIGETTI_SHOTS, circuits)
    payload = {
        "dry_run": DRY_RUN,
        "cost_estimate_usd": {
            "ionq": ionq_cost,
            "rigetti": rig_cost,
            "total": total,
        },
        "ionq_forte_1": ionq_rec,
        "rigetti_cepheus_108q": rig_rec,
        "circuits_source": REF_DIR,
        "settings": [(n, a, b) for n, a, b in SETTINGS],
        "timestamp": time.time(),
    }
    out_path = os.path.join(OUT_DIR, "submissions.json")
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"Wrote {out_path}", flush=True)


if __name__ == "__main__":
    main()
