#!/usr/bin/env python3
"""qmirror cond.8 option β collector + CHSH analyzer.

Polls all 8 task ARNs from submissions.json, waits for COMPLETED,
extracts measurement counts, computes E_xy correlators per vendor,
and yields S = E_a_b - E_a_bprime + E_aprime_b + E_aprime_bprime.

Bell rule: outcomes (0,0)/(1,1) → +1, (0,1)/(1,0) → -1.
"""
import os
import json
import time
import math
import sys

os.environ["AWS_PROFILE"] = "braket"

OUT_DIR = "/Users/ghost/core/anima/state/qmirror_chsh_xvendor_2026_05_03"
SUB_PATH = os.path.join(OUT_DIR, "submissions.json")
RES_PATH = os.path.join(OUT_DIR, "results.json")
VERDICT_PATH = os.path.join(OUT_DIR, "verdict.json")

POLL_INTERVAL = 30
MAX_WAIT_SEC = 60 * 60 * 4  # 4 hour cap

CHSH_QUANTUM_BOUND = 2 * math.sqrt(2)
CHSH_CLASSICAL_BOUND = 2.0


def fetch_task(task_arn, region):
    from braket.aws import AwsQuantumTask
    import boto3
    sess = boto3.Session(profile_name="braket", region_name=region)
    return AwsQuantumTask(task_arn, aws_session=None) if False else AwsQuantumTask(task_arn)


def region_from_arn(arn):
    # arn:aws:braket:<region>:...
    return arn.split(":")[3]


def status_of(arn):
    from braket.aws import AwsQuantumTask
    t = AwsQuantumTask(arn)
    return t.state(), t


def parse_counts(result):
    """Return dict {bitstring: count} for 2-qubit measurement counts."""
    out = {}
    try:
        mc = result.measurement_counts
        for k, v in mc.items():
            if isinstance(k, str):
                key = k
            else:
                key = "".join(str(int(b)) for b in k)
            out[key] = out.get(key, 0) + int(v)
        return out
    except Exception:
        pass
    # fallback: iterate measurements
    for meas in result.measurements:
        seq = "".join(str(int(b)) for b in meas)
        out[seq] = out.get(seq, 0) + 1
    return out


def compute_E_and_sigma(counts):
    """Bell correlator E = (N_++ + N_-- - N_+- - N_-+) / N_total.

    Bit convention: bitstring "ij" where i=q[0]=Alice, j=q[1]=Bob.
    Map 0 -> +1, 1 -> -1.  Outcome value = Alice * Bob.
    """
    n_plus = 0
    n_minus = 0
    for k, v in counts.items():
        # Take last 2 chars to be safe; should already be length 2.
        bits = k.replace(" ", "")[-2:]
        a = 1 if bits[0] == "0" else -1
        b = 1 if bits[1] == "0" else -1
        if a * b > 0:
            n_plus += v
        else:
            n_minus += v
    n = n_plus + n_minus
    if n == 0:
        return 0.0, 0.0, 0
    E = (n_plus - n_minus) / n
    # Variance of E: <X^2> = 1, so var(E) = (1 - E^2)/n. sigma = sqrt of that.
    var = max(0.0, (1.0 - E * E)) / n
    sig = math.sqrt(var)
    return E, sig, n


def compute_S(corrs):
    """corrs: dict name -> (E, sigma, n).  Returns S, sigma_S."""
    e_ab = corrs["circuit_a_b"][0]
    e_ab_p = corrs["circuit_a_bprime"][0]
    e_ap_b = corrs["circuit_aprime_b"][0]
    e_ap_bp = corrs["circuit_aprime_bprime"][0]
    S = e_ab - e_ab_p + e_ap_b + e_ap_bp
    # sigma_S = sqrt(sum sigma_i^2)
    s2 = sum(corrs[n][1] ** 2 for n in corrs)
    sigma_S = math.sqrt(s2)
    return S, sigma_S


def wait_and_collect(records):
    """records: list of {task_arn, name, alice, bob, vendor, shots}.
    Returns dict name -> {status, counts, E, sigma, n}."""
    from braket.aws import AwsQuantumTask
    pending = {r["task_arn"]: r for r in records}
    done = {}
    start = time.time()
    while pending and (time.time() - start) < MAX_WAIT_SEC:
        completed_now = []
        for arn, r in list(pending.items()):
            try:
                t = AwsQuantumTask(arn)
                st = t.state()
            except Exception as e:
                print(f"  [poll-err] {arn}: {e}", flush=True)
                continue
            if st in ("COMPLETED",):
                try:
                    res = t.result()
                    counts = parse_counts(res)
                    E, sig, n = compute_E_and_sigma(counts)
                    done[r["name"]] = {
                        "task_arn": arn,
                        "vendor": r["vendor"],
                        "alice": r["alice"],
                        "bob": r["bob"],
                        "status": st,
                        "counts": counts,
                        "E": E,
                        "sigma": sig,
                        "n": n,
                        "shots_requested": r["shots"],
                    }
                    completed_now.append(arn)
                    print(f"  [done] {r['vendor']}/{r['name']} E={E:+.4f} n={n}", flush=True)
                except Exception as e:
                    print(f"  [result-err] {r['name']}: {e}", flush=True)
            elif st in ("FAILED", "CANCELLED"):
                done[r["name"]] = {
                    "task_arn": arn,
                    "vendor": r["vendor"],
                    "alice": r["alice"],
                    "bob": r["bob"],
                    "status": st,
                    "counts": {},
                    "E": 0.0,
                    "sigma": 0.0,
                    "n": 0,
                    "shots_requested": r["shots"],
                }
                completed_now.append(arn)
                print(f"  [{st}] {r['vendor']}/{r['name']}", flush=True)
            else:
                # still queued/running
                pass
        for a in completed_now:
            del pending[a]
        if pending:
            elapsed = int(time.time() - start)
            print(f"  [wait] elapsed={elapsed}s pending={len(pending)} (sleep {POLL_INTERVAL}s)", flush=True)
            time.sleep(POLL_INTERVAL)
    if pending:
        for arn, r in pending.items():
            done[r["name"]] = {
                "task_arn": arn,
                "vendor": r["vendor"],
                "alice": r["alice"],
                "bob": r["bob"],
                "status": "TIMEOUT",
                "counts": {},
                "E": 0.0,
                "sigma": 0.0,
                "n": 0,
                "shots_requested": r["shots"],
            }
    return done


def actual_cost_for_vendor(vendor_records, results, task_fee, shot_fee):
    """Sum task fee per completed task + shot fee per shot actually returned."""
    n_tasks = 0
    n_shots = 0
    for r in vendor_records:
        info = results.get(r["name"])
        if info and info["status"] == "COMPLETED":
            n_tasks += 1
            n_shots += info["n"]  # actual shots returned
    return n_tasks * task_fee + n_shots * shot_fee, n_tasks, n_shots


def main():
    with open(SUB_PATH) as f:
        sub = json.load(f)
    ionq_recs = sub["ionq_forte_1"]
    rig_recs = sub["rigetti_cepheus_108q"]
    all_recs = ionq_recs + rig_recs
    print(f"Polling {len(all_recs)} tasks ...", flush=True)
    results = wait_and_collect(all_recs)
    with open(RES_PATH, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Wrote {RES_PATH}", flush=True)

    # Compute per-vendor S
    def vendor_corrs(records):
        c = {}
        for r in records:
            info = results.get(r["name"])
            if not info or info["status"] != "COMPLETED":
                c[r["name"]] = (0.0, 0.0, 0)
            else:
                c[r["name"]] = (info["E"], info["sigma"], info["n"])
        return c

    ionq_c = vendor_corrs(ionq_recs)
    rig_c = vendor_corrs(rig_recs)
    S_ionq, sig_S_ionq = compute_S(ionq_c)
    S_rig, sig_S_rig = compute_S(rig_c)

    # Costs
    ionq_cost, ionq_nt, ionq_ns = actual_cost_for_vendor(
        ionq_recs, results, 0.30, 0.08)
    rig_cost, rig_nt, rig_ns = actual_cost_for_vendor(
        rig_recs, results, 0.30, 0.000425)

    delta_S = abs(S_ionq - S_rig)
    # Vendor-bias verdict: both in [2.6, 2.85] within combined sigma band
    band_lo, band_hi = 2.6, 2.85
    bias_eliminated = (
        band_lo <= S_ionq <= band_hi
        and band_lo <= S_rig <= band_hi
        and delta_S <= 2.0 * math.sqrt(sig_S_ionq ** 2 + sig_S_rig ** 2)
    )

    verdict = {
        "option_selected": "beta",
        "vendors": ["ionq_forte_1", "rigetti_cepheus_108q"],
        "ionq_forte_1": {
            "S": S_ionq,
            "sigma_S": sig_S_ionq,
            "correlators": {n: {"E": v[0], "sigma": v[1], "n": v[2]} for n, v in ionq_c.items()},
            "shots_per_setting_requested": 100,
            "tasks_completed": ionq_nt,
            "shots_returned_total": ionq_ns,
            "cost_actual_usd": ionq_cost,
        },
        "rigetti_cepheus_108q": {
            "S": S_rig,
            "sigma_S": sig_S_rig,
            "correlators": {n: {"E": v[0], "sigma": v[1], "n": v[2]} for n, v in rig_c.items()},
            "shots_per_setting_requested": 1024,
            "tasks_completed": rig_nt,
            "shots_returned_total": rig_ns,
            "cost_actual_usd": rig_cost,
        },
        "cross_vendor": {
            "delta_S": delta_S,
            "joint_sigma": math.sqrt(sig_S_ionq ** 2 + sig_S_rig ** 2),
            "bias_band": [band_lo, band_hi],
            "vendor_bias_verdict": "eliminated" if bias_eliminated else "observed",
        },
        "reference_nexus_chsh_bell_2026_05_02": {
            "ionq_S": 2.808,
            "ionq_sigma_S": 0.09,
        },
        "quantum_bound": CHSH_QUANTUM_BOUND,
        "classical_bound": CHSH_CLASSICAL_BOUND,
        "total_cost_actual_usd": ionq_cost + rig_cost,
        "honest_c3": [
            "Shot-count asymmetry: IonQ 100/setting vs Rigetti 1024/setting => sigma bands not directly comparable; per-setting CI is ~3x wider on IonQ.",
            "Trapped-ion (IonQ) and superconducting (Rigetti) implement Bell pair via fundamentally different gate-physics (laser-driven vs microwave-pulse); equal S is operational anchor only — CHSH cannot disentangle vendor-specific decoherence channels.",
            "Single-trial design: each S has only intra-circuit shot-noise; no run-to-run repeat means systematic drift (calibration window) is not estimable.",
        ],
    }
    with open(VERDICT_PATH, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"Wrote {VERDICT_PATH}", flush=True)
    print(json.dumps({
        "S_ionq": S_ionq,
        "sigma_S_ionq": sig_S_ionq,
        "S_rig": S_rig,
        "sigma_S_rig": sig_S_rig,
        "delta_S": delta_S,
        "verdict": verdict["cross_vendor"]["vendor_bias_verdict"],
        "cost_total": ionq_cost + rig_cost,
    }, indent=2))


if __name__ == "__main__":
    main()
