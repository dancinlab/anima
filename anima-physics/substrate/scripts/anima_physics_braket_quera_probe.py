#!/usr/bin/env python3
# anima-physics/scripts/anima_physics_braket_quera_probe.py
#
# raw#37 transient helper for anima-physics/analog/cloud_facade_poc.hexa.
# Builds a 4-atom Rydberg AHS program for QuEra Aquila (us-east-1).
# DRY_RUN default (env ANIMA_BRAKET_DRY_RUN=1) verifies SDK + auth path,
# returns api_call_count=0.  LIVE mode (ANIMA_BRAKET_DRY_RUN=0) submits the
# AHS task with `shots` and reports api_call_count >= 1.
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

DEVICE_ARN = "arn:aws:braket:us-east-1::device/qpu/quera/Aquila"
BACKEND_PREFIX = "aws_braket_quera_"
AWS_PROFILE = os.environ.get("AWS_PROFILE_OVERRIDE", "braket")
N_ATOMS = 4
SHOTS = 100
SPACING_M = 5.5e-6  # 5.5 µm — Aquila default lattice constant
RABI_HZ = 1.58e7    # ~2.5 MHz Rabi (in rad/s)
DETUNING_HZ = 2e7   # ~3 MHz detuning
TOTAL_TIME_S = 3.5e-6  # 3.5 µs total

# Force AWS profile resolution before any boto3/braket import that
# might consult env.  raw#10 honest — no hardcoded keys.
os.environ["AWS_PROFILE"] = AWS_PROFILE


def _emit(d, exit_code=0):
    """Single-line JSON to stdout, deterministic key ordering."""
    sys.stdout.write(json.dumps(d, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.flush()
    sys.exit(exit_code)


def _sha256_program_signature(program_kind, n_atoms, spacing_m, rabi, detuning, t_total, seed):
    sig = (
        f"quera_aquila|{program_kind}|n={n_atoms}|d={spacing_m:.3e}|"
        f"omega={rabi:.3e}|delta={detuning:.3e}|T={t_total:.3e}|seed={seed}"
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


def _build_ahs_program(program_kind, seed):
    """Construct AnalogHamiltonianSimulation for `mis` or `uncoupled`.

    `mis`        : full driving field — Rydberg blockade induces
                   anti-ferromagnetic ground state on a 1D chain.
    `uncoupled`  : Rabi=0 entire schedule — atoms remain in ground state,
                   trivial product distribution.
    """
    from braket.ahs.atom_arrangement import AtomArrangement
    from braket.ahs.analog_hamiltonian_simulation import AnalogHamiltonianSimulation
    from braket.ahs.driving_field import DrivingField
    from braket.timings.time_series import TimeSeries

    arr = AtomArrangement()
    for i in range(N_ATOMS):
        arr.add((i * SPACING_M, 0.0))

    times = [0.0, 0.5e-6, TOTAL_TIME_S - 0.5e-6, TOTAL_TIME_S]

    if program_kind == "mis":
        amp_pts = [0.0, RABI_HZ, RABI_HZ, 0.0]
        det_pts = [-DETUNING_HZ, -DETUNING_HZ, DETUNING_HZ, DETUNING_HZ]
    elif program_kind == "uncoupled":
        amp_pts = [0.0, 0.0, 0.0, 0.0]
        det_pts = [0.0, 0.0, 0.0, 0.0]
    else:
        raise ValueError(f"unknown program kind: {program_kind}")

    amplitude = TimeSeries()
    for t, v in zip(times, amp_pts):
        amplitude.put(t, v)
    detuning = TimeSeries()
    for t, v in zip(times, det_pts):
        detuning.put(t, v)
    phase = TimeSeries()
    phase.put(0.0, 0.0)
    phase.put(TOTAL_TIME_S, 0.0)

    df = DrivingField(amplitude=amplitude, detuning=detuning, phase=phase)
    return AnalogHamiltonianSimulation(register=arr, hamiltonian=df)


def _expected_dry_entropy_nat(program_kind):
    """Theoretical reference entropy for DRY_RUN bookkeeping only.

    Real Rydberg dynamics need real HW.  These DRY_RUN numbers are NOT
    measurements — they are the schedule-class signature so the .hexa
    can sanity-check program-distinguishability without a cloud call.
    """
    if program_kind == "mis":
        # 4-atom anti-ferromagnetic blockade pattern: mix of 1010 + 0101
        # plus thermal smear → H ~ ln(2) ≈ 0.693 nat (placeholder, not measured)
        return 0.6931
    if program_kind == "uncoupled":
        return 0.0
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


def _live_run(ahs_program, program_kind, seed):
    """LIVE: submit AHS task and tally pattern entropy from shot counts.

    Returns (entropy_nat, actual_backend, api_call_count, error_str).
    api_call_count >= 1 marks the genuine cloud spend.
    """
    api_calls = 0
    try:
        from braket.aws import AwsDevice
        device = AwsDevice(DEVICE_ARN)
        api_calls += 1  # device metadata fetch
        actual = (device.name or "Aquila").replace(" ", "_")
        task = device.run(ahs_program, shots=SHOTS)
        api_calls += 1  # task submission
        result = task.result()
        api_calls += 1  # result retrieval
        # Count post-sequence atom states; key by ground-state bitstring.
        counts = {}
        for meas in result.measurements:
            # post_sequence: 1 = ground (g), 0 = Rydberg (r); per-atom array
            seq = "".join(str(int(b)) for b in meas.post_sequence)
            counts[seq] = counts.get(seq, 0) + 1
        h = _shannon_entropy_from_counts(counts)
        return h, actual, api_calls, ""
    except Exception as exc:
        tb = traceback.format_exc(limit=2)
        return 0.0, "", api_calls, f"{type(exc).__name__}: {exc} | {tb.splitlines()[-1] if tb else ''}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--program", choices=["mis", "uncoupled"], default="mis")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    program_kind = args.program
    seed = args.seed
    dry_run = os.environ.get("ANIMA_BRAKET_DRY_RUN", "1") != "0"

    sha = _sha256_program_signature(
        program_kind, N_ATOMS, SPACING_M, RABI_HZ, DETUNING_HZ, TOTAL_TIME_S, seed
    )

    base = {
        "program": program_kind,
        "n_atoms": N_ATOMS,
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
        })
        _emit(out, 0)

    # Verify SDK + AHS program build.  This is local-only (no API call).
    try:
        ahs_program = _build_ahs_program(program_kind, seed)
        # Force IR materialization to confirm program validity.
        _ir = ahs_program.to_ir()
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
            "error": "AHS build failed: " + sdk_err,
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
        })
        _emit(out, 0)

    # LIVE branch — explicit ANIMA_BRAKET_DRY_RUN=0 only.
    h, actual, api_calls, live_err = _live_run(ahs_program, program_kind, seed)
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
    })
    _emit(out, 0 if not degraded else 0)


if __name__ == "__main__":
    main()
