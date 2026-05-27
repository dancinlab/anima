#!/usr/bin/env python3
"""qmirror cond.8 option β CHSH analyzer (stdlib-only).

Reads raw_results/*.json (downloaded from S3 via aws CLI), computes
per-vendor CHSH S statistic, and writes verdict.json.

Bell rule: outcomes (0,0)/(1,1) -> +1 (correlated); (0,1)/(1,0) -> -1.
"""
import json
import math
import os
import sys

ROOT = "/Users/ghost/core/anima/state/qmirror_chsh_xvendor_2026_05_03"
RAW = os.path.join(ROOT, "raw_results")
SUB = os.path.join(ROOT, "submissions.json")
VERDICT = os.path.join(ROOT, "verdict.json")

CHSH_QB = 2.0 * math.sqrt(2.0)   # 2.828427
CHSH_CB = 2.0

# ANU / nexus_chsh_bell_2026_05_02 reference (IonQ Aria-1, S=2.808)
NEXUS_CHSH_REF_S = 2.808
NEXUS_CHSH_REF_SIGMA = 0.09

# Falsifier F-QM-CROSSVENDOR-1: any vendor pair with |dS| <= 0.30 -> PASS
FALSIFIER_THRESHOLD = 0.30


def measurements_to_E(measurements):
    """Bell correlator from list of [bit_alice, bit_bob] measurements."""
    n_pos = 0
    n_neg = 0
    for m in measurements:
        a = 1 if m[0] == 0 else -1
        b = 1 if m[1] == 0 else -1
        if a * b > 0:
            n_pos += 1
        else:
            n_neg += 1
    n = n_pos + n_neg
    if n == 0:
        return 0.0, 0.0, 0
    E = (n_pos - n_neg) / n
    var = max(0.0, 1.0 - E * E) / n
    sig = math.sqrt(var)
    return E, sig, n


def counts_to_E(counts):
    """Bell correlator from {bitstring -> count}.

    bitstring 'ij' where i=q[0]=Alice, j=q[1]=Bob.
    """
    n_pos = 0
    n_neg = 0
    for k, v in counts.items():
        bits = k.replace(" ", "")[-2:]
        a = 1 if bits[0] == "0" else -1
        b = 1 if bits[1] == "0" else -1
        if a * b > 0:
            n_pos += int(v)
        else:
            n_neg += int(v)
    n = n_pos + n_neg
    if n == 0:
        return 0.0, 0.0, 0
    E = (n_pos - n_neg) / n
    var = max(0.0, 1.0 - E * E) / n
    sig = math.sqrt(var)
    return E, sig, n


def load_result(path):
    """Return (E, sigma, n, status_str) for a single S3 results.json file."""
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            r = json.load(f)
    except Exception as e:
        return ("ERR_PARSE", str(e))
    # IonQ usually has measurementProbabilities; Rigetti has measurements list.
    if "measurements" in r and r["measurements"]:
        E, s, n = measurements_to_E(r["measurements"])
        return (E, s, n, "COMPLETED")
    if "measurementProbabilities" in r and r["measurementProbabilities"]:
        # Probabilities -> approximate counts using shots
        shots = r.get("taskMetadata", {}).get("shots", 0) or 0
        if shots <= 0:
            shots = 100
        counts = {k: int(round(p * shots)) for k, p in r["measurementProbabilities"].items()}
        E, s, n = counts_to_E(counts)
        return (E, s, n, "COMPLETED")
    if "measurementCounts" in r:
        E, s, n = counts_to_E(r["measurementCounts"])
        return (E, s, n, "COMPLETED")
    return (0.0, 0.0, 0, "NO_DATA")


def compute_S(corrs):
    """corrs: dict name -> (E, sigma, n).  Returns (S, sigma_S)."""
    e_ab = corrs["circuit_a_b"][0]
    e_abp = corrs["circuit_a_bprime"][0]
    e_apb = corrs["circuit_aprime_b"][0]
    e_apbp = corrs["circuit_aprime_bprime"][0]
    S = e_ab - e_abp + e_apb + e_apbp
    s2 = sum(c[1] ** 2 for c in corrs.values())
    return S, math.sqrt(s2)


def main():
    with open(SUB) as f:
        sub = json.load(f)

    settings = ["circuit_a_b", "circuit_a_bprime",
                "circuit_aprime_b", "circuit_aprime_bprime"]

    # --- Rigetti ---
    rig_corrs = {}
    rig_complete = 0
    rig_shots_total = 0
    for name in settings:
        path = os.path.join(RAW, f"rigetti_{name}.json")
        r = load_result(path)
        if r and len(r) == 4 and r[3] == "COMPLETED":
            rig_corrs[name] = (r[0], r[1], r[2])
            rig_complete += 1
            rig_shots_total += r[2]
        else:
            rig_corrs[name] = (0.0, 0.0, 0)

    # --- IonQ ---
    ionq_corrs = {}
    ionq_complete = 0
    ionq_shots_total = 0
    ionq_status_per_setting = {}
    for name in settings:
        path = os.path.join(RAW, f"ionq_{name}.json")
        r = load_result(path)
        if r and len(r) == 4 and r[3] == "COMPLETED":
            ionq_corrs[name] = (r[0], r[1], r[2])
            ionq_complete += 1
            ionq_shots_total += r[2]
            ionq_status_per_setting[name] = "COMPLETED"
        else:
            ionq_corrs[name] = (0.0, 0.0, 0)
            ionq_status_per_setting[name] = "QUEUED_OR_PENDING"

    S_rig, sig_rig = compute_S(rig_corrs)
    S_ionq, sig_ionq = compute_S(ionq_corrs)

    ionq_available = (ionq_complete == 4)
    rig_available = (rig_complete == 4)

    # --- Cross-vendor matrix ---
    nexus_S = NEXUS_CHSH_REF_S
    nexus_sig = NEXUS_CHSH_REF_SIGMA

    pairs = {}
    if rig_available:
        pairs["rigetti_vs_nexus_ionq_aria1"] = {
            "delta_S": abs(S_rig - nexus_S),
            "joint_sigma": math.sqrt(sig_rig ** 2 + nexus_sig ** 2),
            "pass_falsifier_F-QM-CROSSVENDOR-1": abs(S_rig - nexus_S) <= FALSIFIER_THRESHOLD,
        }
    if ionq_available:
        pairs["ionq_forte_vs_nexus_ionq_aria1"] = {
            "delta_S": abs(S_ionq - nexus_S),
            "joint_sigma": math.sqrt(sig_ionq ** 2 + nexus_sig ** 2),
            "pass_falsifier_F-QM-CROSSVENDOR-1": abs(S_ionq - nexus_S) <= FALSIFIER_THRESHOLD,
        }
    if rig_available and ionq_available:
        pairs["ionq_forte_vs_rigetti_cepheus"] = {
            "delta_S": abs(S_ionq - S_rig),
            "joint_sigma": math.sqrt(sig_ionq ** 2 + sig_rig ** 2),
            "pass_falsifier_F-QM-CROSSVENDOR-1": abs(S_ionq - S_rig) <= FALSIFIER_THRESHOLD,
        }

    any_pair_pass = any(p["pass_falsifier_F-QM-CROSSVENDOR-1"] for p in pairs.values()) if pairs else False
    overall = "PASS" if any_pair_pass else ("PARTIAL_PENDING" if not ionq_available else "FAIL")

    # Cost: only shots already submitted bill (no new shots).
    # Per submissions.json estimates: ionq=33.20 (4 task * (0.30 + 100*0.08)) + rigetti=2.94 (4 task * (0.30 + 1024*0.000425))
    # Actual cost is incurred at submission, regardless of completion.
    rig_cost = 4 * (0.30 + 1024 * 0.000425) if True else 0.0
    ionq_cost = 4 * (0.30 + 100 * 0.08) if True else 0.0

    verdict = {
        "option_selected": "beta",
        "falsifier": "F-QM-CROSSVENDOR-1 (|delta_S| <= 0.30 between any 2 vendors -> cond.8 PASS)",
        "verdict": overall,
        "vendors_tested": ["rigetti_cepheus_108q", "ionq_forte_1"],
        "reference": {
            "name": "nexus_chsh_bell_2026_05_02",
            "vendor": "ionq_aria_1_via_nexus_baseline",
            "S": nexus_S,
            "sigma_S": nexus_sig,
            "note": "ANU=2.838 cited in task prompt; nexus_chsh_bell verdict.json shows S=2.808 (ionq_aria1, 250 shots/setting). Using nexus value as the on-disk source of truth.",
        },
        "rigetti_cepheus_108q": {
            "S": S_rig,
            "sigma_S": sig_rig,
            "complete": rig_available,
            "tasks_completed": rig_complete,
            "shots_returned_total": rig_shots_total,
            "shots_per_setting_requested": 1024,
            "correlators": {n: {"E": v[0], "sigma": v[1], "n": v[2]} for n, v in rig_corrs.items()},
            "cost_actual_usd": rig_cost,
            "region": "us-west-1",
        },
        "ionq_forte_1": {
            "S": S_ionq if ionq_available else None,
            "sigma_S": sig_ionq if ionq_available else None,
            "complete": ionq_available,
            "tasks_completed": ionq_complete,
            "shots_returned_total": ionq_shots_total,
            "shots_per_setting_requested": 100,
            "correlators": {n: {"E": v[0], "sigma": v[1], "n": v[2]} for n, v in ionq_corrs.items()},
            "status_per_setting": ionq_status_per_setting,
            "cost_billed_at_submission_usd": ionq_cost,
            "region": "us-east-1",
            "note": "IonQ Forte-1 batches process during business hours; queue depth was 8 at submission; expect long latency.",
        },
        "cross_vendor_pairs": pairs,
        "any_pair_pass": any_pair_pass,
        "quantum_bound": CHSH_QB,
        "classical_bound": CHSH_CB,
        "total_cost_actual_usd": rig_cost + ionq_cost,
        "honest_c3": [
            "N=1 single shot batch per (vendor, setting); no run-to-run repeats; vendor calibration drift not estimable.",
            "No IRB / no ground-truth oracle: equal S between vendors is operational concordance only -- does not falsify hidden vendor-correlated systematics.",
            "Shot-count asymmetry: Rigetti 1024/setting vs IonQ 100/setting => sigma bands differ by ~3.2x; sigma_S(Rigetti)~0.025, sigma_S(IonQ)~0.085 best-case.",
            "Trapped-ion (IonQ) vs superconducting (Rigetti) implement Bell pair via fundamentally different gate-physics; the F-QM-CROSSVENDOR-1 threshold of 0.30 is loose enough to absorb decoherence asymmetry but cannot disentangle vendor-specific noise channels.",
            "Reference S=2.808 from nexus_chsh_bell_2026_05_02 is itself IonQ Aria-1 (not vendor-orthogonal); ANU value 2.838 in task prompt does not match on-disk verdict; using on-disk SSOT.",
        ],
    }
    with open(VERDICT, "w") as f:
        json.dump(verdict, f, indent=2)
    print(json.dumps({
        "verdict": overall,
        "S_rigetti": S_rig if rig_available else None,
        "S_ionq": S_ionq if ionq_available else None,
        "S_nexus_ref": nexus_S,
        "any_pair_pass": any_pair_pass,
        "ionq_complete": ionq_complete,
        "rig_complete": rig_complete,
    }, indent=2))


if __name__ == "__main__":
    main()
