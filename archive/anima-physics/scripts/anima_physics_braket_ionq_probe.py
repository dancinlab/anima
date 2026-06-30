#!/usr/bin/env python3
# anima-physics/scripts/anima_physics_braket_ionq_probe.py
#
# raw#37 transient helper for anima-physics/trapped_ion/cloud_facade_poc.hexa.
# Builds a 4-qubit GHZ gate-based circuit for IonQ Forte 1 (us-east-1).
# DRY_RUN default (env ANIMA_BRAKET_DRY_RUN=1) verifies SDK + auth path,
# returns api_call_count=0.  LIVE mode (ANIMA_BRAKET_DRY_RUN=0) submits the
# task with `shots` and reports api_call_count >= 1.
#
# Output: single-line JSON on stdout (caller parses via awk).
# Required keys (all branches):
#   credentials_present, dry_run, degraded, entropy_pattern_nat,
#   sha256_program, backend_name, actual_backend, error,
#   api_call_count, device_arn
#
# raw#9 hexa-only strict — this .py is transient (raw#37) under
# anima-physics/scripts/ scope.  No top-level library import side-effects
# in the .hexa.  Variables + log keys English; comments may use 한글.

import argparse
import hashlib
import json
import math
import os
import sys
import traceback

DEVICE_ARN = "arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1"
BACKEND_PREFIX = "aws_braket_ionq_"
AWS_PROFILE = os.environ.get("AWS_PROFILE_OVERRIDE", "braket")
N_QUBITS = 4
SHOTS = 100

# Force AWS profile resolution before any boto3/braket import.
# raw#10 honest — no hardcoded keys.
os.environ["AWS_PROFILE"] = AWS_PROFILE


def _emit(d, exit_code=0):
    """Single-line JSON to stdout, deterministic key ordering."""
    sys.stdout.write(json.dumps(d, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.flush()
    sys.exit(exit_code)


def _sha256_program_signature(program_kind, n_qubits, shots, seed):
    sig = (
        f"ionq_forte_1|{program_kind}|n={n_qubits}|shots={shots}|seed={seed}"
    )
    return hashlib.sha256(sig.encode("utf-8")).hexdigest()


def _check_credentials():
    """raw#10 honest — return (present, error_message)."""
    home_creds = os.path.expanduser("~/.aws/credentials")
    has_env = bool(
        os.environ.get("AWS_ACCESS_KEY_ID")
        and os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    has_file = os.path.isfile(home_creds)
    if not (has_env or has_file):
        return False, "no AWS credentials in env or ~/.aws/credentials"
    return True, ""


def _build_circuit(program_kind, seed):
    """Construct gate circuit for `ghz` or `unentangled` programs.

    `ghz`         : H(0) + CNOT(0,1) + CNOT(1,2) + CNOT(2,3)
                    → produces |0000> + |1111> superposition (Bell-like).
    `unentangled` : H(0) only — separable product state, low bipartite
                    entropy.
    """
    from braket.circuits import Circuit

    c = Circuit()
    c.h(0)
    if program_kind == "ghz":
        c.cnot(0, 1)
        c.cnot(1, 2)
        c.cnot(2, 3)
    elif program_kind == "unentangled":
        # H only on qubit 0, all others remain |0>.
        # IonQ Forte 1 does NOT support `i` (identity) gate outside verbatim
        # boxes. We use rx(0.0) on qubits 1..3 — a zero-angle rotation that
        # is functionally identical to identity but uses a native-supported
        # gate set member (rx is in IonQ's supportedOperations).
        c.rx(1, 0.0)
        c.rx(2, 0.0)
        c.rx(3, 0.0)
    else:
        raise ValueError(f"unknown program kind: {program_kind}")

    return c


def _expected_dry_entropy_nat(program_kind):
    """Theoretical reference entropy for DRY_RUN bookkeeping only.

    Real IonQ dynamics need real HW.  These DRY_RUN numbers are NOT
    measurements — they are the schedule-class signature so the .hexa
    can sanity-check program-distinguishability without a cloud call.
    """
    if program_kind == "ghz":
        # ideal 4-qubit GHZ: equal superposition of 0000 + 1111
        # → 2 outcomes equally likely → H = ln(2) ≈ 0.6931 nat
        return 0.6931
    if program_kind == "unentangled":
        # H on qubit 0 only, others |0>: 2 outcomes (0000, 1000)
        # → H = ln(2) ≈ 0.6931 nat ALSO at qubit-0 level
        # but bipartite entropy across {0,1,2,3} cut is 0 since
        # state is product. We report distribution Shannon H here for
        # consistency with measurement scheme.
        return 0.6931
    return 0.0


def _shannon_entropy_from_counts(counts):
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    h = 0.0
    for c in counts.values():
        if c <= 0:
            continue
        p = c / total
        h -= p * math.log(p)
    return h


def _live_run(circuit, program_kind, seed):
    """LIVE: submit gate-based task and tally pattern entropy from shot counts.

    Returns (entropy_nat, actual_backend, api_call_count, error_str, task_arn).
    api_call_count >= 1 marks the genuine cloud spend.
    """
    api_calls = 0
    task_arn = ""
    try:
        from braket.aws import AwsDevice
        device = AwsDevice(DEVICE_ARN)
        api_calls += 1  # device metadata fetch
        actual = (device.name or "Forte-1").replace(" ", "_")
        task = device.run(circuit, shots=SHOTS)
        api_calls += 1  # task submission
        try:
            task_arn = task.id
        except Exception:
            task_arn = ""
        result = task.result()
        api_calls += 1  # result retrieval
        # Count gate-based measurements; key by full bitstring.
        counts = {}
        # Try measurement_counts first (gate-based standard).
        try:
            mc = result.measurement_counts
            for bitstr, n in mc.items():
                key = "".join(str(b) for b in bitstr) if not isinstance(bitstr, str) else bitstr
                counts[key] = counts.get(key, 0) + int(n)
        except Exception:
            # fallback: iterate measurements
            for meas in result.measurements:
                seq = "".join(str(int(b)) for b in meas)
                counts[seq] = counts.get(seq, 0) + 1
        h = _shannon_entropy_from_counts(counts)
        return h, actual, api_calls, "", task_arn
    except Exception as exc:
        tb = traceback.format_exc(limit=2)
        return 0.0, "", api_calls, f"{type(exc).__name__}: {exc} | {tb.splitlines()[-1] if tb else ''}", task_arn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--program", choices=["ghz", "unentangled"], default="ghz")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    program_kind = args.program
    seed = args.seed
    dry_run = os.environ.get("ANIMA_BRAKET_DRY_RUN", "1") != "0"

    sha = _sha256_program_signature(program_kind, N_QUBITS, SHOTS, seed)

    base = {
        "program": program_kind,
        "n_qubits": N_QUBITS,
        "seed": seed,
        "device_arn": DEVICE_ARN,
        "sha256_program": sha,
    }

    creds_present, cred_err = _check_credentials()
    if not creds_present:
        out = dict(base)
        out.update({
            "credentials_present": False,
            "dry_run": True,
            "degraded": True,
            "shots": 0,
            "api_call_count": 0,
            "entropy_pattern_nat": 0.0,
            "backend_name": BACKEND_PREFIX + "DEGRADED_NO_AWS_CREDENTIALS",
            "actual_backend": "",
            "error": cred_err,
            "task_arn": "",
        })
        _emit(out, 0)

    # Verify SDK + circuit build.  This is local-only (no API call).
    try:
        circuit = _build_circuit(program_kind, seed)
        # Force serialization to confirm circuit validity.
        _ir = circuit.to_ir()
        sdk_ok = True
        sdk_err = ""
    except Exception as exc:
        sdk_ok = False
        sdk_err = f"{type(exc).__name__}: {exc}"

    if not sdk_ok:
        out = dict(base)
        out.update({
            "credentials_present": True,
            "dry_run": dry_run,
            "degraded": True,
            "shots": 0,
            "api_call_count": 0,
            "entropy_pattern_nat": 0.0,
            "backend_name": BACKEND_PREFIX + "DEGRADED_SDK_BUILD",
            "actual_backend": "",
            "error": "circuit build failed: " + sdk_err,
            "task_arn": "",
        })
        _emit(out, 0)

    # Verify boto3 session + region (still no API call).
    try:
        import boto3
        session = boto3.Session(profile_name=AWS_PROFILE)
        region = session.region_name or "us-east-1"
        auth_ok = True
        auth_err = ""
    except Exception as exc:
        auth_ok = False
        auth_err = f"{type(exc).__name__}: {exc}"
        region = ""

    if not auth_ok:
        out = dict(base)
        out.update({
            "credentials_present": True,
            "dry_run": dry_run,
            "degraded": True,
            "shots": 0,
            "api_call_count": 0,
            "entropy_pattern_nat": 0.0,
            "backend_name": BACKEND_PREFIX + "DEGRADED_AUTH_PATH",
            "actual_backend": "",
            "error": "boto3 session failed: " + auth_err,
            "task_arn": "",
        })
        _emit(out, 0)

    if dry_run:
        out = dict(base)
        out.update({
            "credentials_present": True,
            "dry_run": True,
            "degraded": False,
            "shots": 0,
            "api_call_count": 0,
            "entropy_pattern_nat": _expected_dry_entropy_nat(program_kind),
            "backend_name": BACKEND_PREFIX + "DRY_RUN",
            "actual_backend": "DRY_RUN",
            "region": region,
            "error": "",
            "task_arn": "",
        })
        _emit(out, 0)

    # LIVE branch — explicit ANIMA_BRAKET_DRY_RUN=0 only.
    h, actual, api_calls, live_err, task_arn = _live_run(circuit, program_kind, seed)
    degraded = bool(live_err)
    backend_name = BACKEND_PREFIX + (actual if actual else "DEGRADED_LIVE")
    out = dict(base)
    out.update({
        "credentials_present": True,
        "dry_run": False,
        "degraded": degraded,
        "shots": SHOTS,
        "api_call_count": api_calls,
        "entropy_pattern_nat": h,
        "backend_name": backend_name,
        "actual_backend": actual,
        "region": region,
        "error": live_err,
        "task_arn": task_arn,
    })
    _emit(out, 0 if not degraded else 0)


if __name__ == "__main__":
    main()
