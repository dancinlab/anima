#!/usr/bin/env python3
"""h940_robustness_replication.py — stability check on H_940's borderline 🔴.

WHY THIS EXISTS
===============
The primary H_940 run (h940_real_anu_reconfirm.py) returned a PRE-REGISTERED 🔴
F-H940-SOURCE-DEPENDENT: with a REAL ANU big buffer the DET-vs-QB phi_mean test was
KS p=0.012 (<0.05) and |Cohen d|=0.674 (>=0.2), tripping the falsifier — whereas the
H_936 os.urandom big buffer had given parity (p≈0.14). BUT this rests on a SINGLE
ANU draw + a SINGLE seed_base, and #123-A states ANU == chacha20 statistically (so a
genuine source-dependence is not expected). p=0.012 is also borderline (between 0.05
and 0.01), and the absolute phi_mean shift is tiny (DET 0.141427 vs QB 0.141714).

This companion does NOT change the primary verdict (the pre-registered falsifier
stands, CODE-decided). It MEASURES whether that 🔴 is STABLE across independent draws
+ seed bases, so the .md can scope the finding honestly: a stable 🔴 is a real
source-dependence; an unstable one (flips to parity on a fresh draw) means the single
rung was a sampling fluke and the source-dependence claim is NOT robust at this scale.

METHOD (g5 CODE-measured, p7 — no LLM judge)
============================================
R independent replicates. Each replicate:
  - pulls a FRESH REAL ANU big buffer (new request_id, new sha256)
  - runs DET and QB arms at a DISTINCT seed_base (so DET and QB both move together)
  - records DET-vs-QB phi_mean Cohen d + KS p, and #distinguishing tension observables
Report the distribution: how many of R replicates trip the pre-registered falsifier
(p<0.05 AND |d|>=0.2 on phi_mean, OR >=1 distinguishing tension observable).
If the fraction tripping is high -> 🔴 is ROBUST. If low/mixed -> 🔴 is a FRAGILE
single-rung artifact (honest scope: source-dependence UNCONFIRMED at this scale).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_SEED_DIR = os.path.join(_REPO, "mirror", "qmirror", "seed")
sys.path.insert(0, _SEED_DIR)
sys.path.insert(0, _HERE)

# reuse the H_936 machinery VERBATIM (same self/尺 as H_940)
_h936_path = os.path.join(_HERE, "h936_unbiased_buffer_retest.py")
_spec = importlib.util.spec_from_file_location("h936_module", _h936_path)
h936 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h936)

run_arm = h936.run_arm
cohen_d = h936.cohen_d
ks = h936.ks
col = h936.col
chan = h936.chan
prove_unbiased = h936.prove_unbiased
PureField = h936.PureField
brain_emit_decision = h936.brain_emit_decision
FIELD_DIM = h936.FIELD_DIM
IM_THRESHOLD = h936.IM_THRESHOLD
ANU_PULLER = os.path.join(_SEED_DIR, "anu_pull.py")


def pull_fresh(n_bytes, out_path, prov_path):
    """Fresh REAL ANU pull; returns (ok, info). No fallback (defends the test)."""
    r = subprocess.run(
        [sys.executable, ANU_PULLER, "--bytes", str(n_bytes),
         "--out", out_path, "--provenance", prov_path],
        capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        return False, {"blocker": f"exit {r.returncode}: {r.stderr.strip()[:300]}"}
    raw = open(out_path, "rb").read()
    j = json.loads(r.stdout.strip().splitlines()[-1])
    return True, {"tier": j.get("tier"), "request_id": j.get("request_id"),
                  "sha256": hashlib.sha256(raw).hexdigest(), "n_bytes": len(raw)}


def tension_distinguishing(armA, armB):
    keys = ["phi_mean", "phi_var"] + [f"ch{c}_mean" for c in range(FIELD_DIM)]
    out = []
    for k in keys:
        if k in ("phi_mean", "phi_var"):
            d = cohen_d(col(armA, k), col(armB, k)); s = ks(col(armA, k), col(armB, k))
        else:
            c = int(k[2:].split("_")[0])
            d = cohen_d(chan(armA, c), chan(armB, c)); s = ks(chan(armA, c), chan(armB, c))
        if s["p"] is not None and s["p"] < 0.05 and abs(d) >= 0.20:
            out.append(k)
    return out


def main():
    T = int(os.environ.get("H940R_T", "2400"))
    N_SEEDS = int(os.environ.get("H940R_SEEDS", "24"))
    R = int(os.environ.get("H940R_REPS", "4"))
    ENT_SCALE = 0.04
    NEG = 0.20
    ts = datetime.now(timezone.utc).isoformat()

    out_dir = os.path.join(_REPO, ".verdicts", "940_real_anu_reconfirm")
    os.makedirs(out_dir, exist_ok=True)
    state_dir = os.path.join(_REPO, "state", "h940_real_anu")
    os.makedirs(state_dir, exist_ok=True)

    # shared emit gate (== H_940 / H_936)
    cal = PureField()
    scs = []
    for _ in range(T):
        cal.step(perturb=0.0)
        _, sc = brain_emit_decision(cal, gate=IM_THRESHOLD)
        scs.append(sc)
    shared_gate = sum(scs) / len(scs)

    draws_per_seed = T
    worst_span = draws_per_seed * (N_SEEDS * (N_SEEDS + 1) // 2 + N_SEEDS)
    big_bytes = max(131072, int(worst_span * 1.10) + 4096)

    reps = []
    for r in range(R):
        seed_base = 1000 + r * 100  # distinct base => DET and QB both shift together
        big_path = os.path.join(state_dir, f"anu_big_rep{r}.bin")
        prov_path = os.path.join(state_dir, "provenance_robust.jsonl")
        ok, info = pull_fresh(big_bytes, big_path, prov_path)
        if not ok:
            reps.append({"rep": r, "ok": False, **info})
            continue
        bstat = prove_unbiased(big_path)
        armDET = run_arm("DET", "deterministic", N_SEEDS, T, shared_gate, ENT_SCALE, seed_base)
        armQB = run_arm("QB", "quantum", N_SEEDS, T, shared_gate, ENT_SCALE, seed_base,
                        big_buf_path=big_path, big_buf_bytes=big_bytes)
        cd = cohen_d(col(armDET, "phi_mean"), col(armQB, "phi_mean"))
        k = ks(col(armDET, "phi_mean"), col(armQB, "phi_mean"))
        dist = tension_distinguishing(armDET, armQB)
        phi_trips = (k["p"] is not None and k["p"] < 0.05 and abs(cd) >= NEG)
        trips = phi_trips or len(dist) > 0
        reps.append({
            "rep": r, "ok": True, "seed_base": seed_base,
            "request_id": info["request_id"], "tier": info["tier"],
            "sha256": info["sha256"][:16], "buf_unbiased": bstat["unbiased"],
            "phi_cohen_d": cd, "phi_ks_p": k["p"],
            "n_tension_distinguishing": len(dist), "tension_distinguishing": dist,
            "phi_falsifier_trips": phi_trips, "replicate_trips_falsifier": trips,
        })
        # prune the per-rep big bin to keep state small (raw is reproducible from rid)
        try:
            os.remove(big_path)
        except OSError:
            pass

    ok_reps = [x for x in reps if x.get("ok")]
    n_trip = sum(1 for x in ok_reps if x["replicate_trips_falsifier"])
    n_ok = len(ok_reps)
    frac = (n_trip / n_ok) if n_ok else None
    # ROBUST 🔴 if the falsifier trips in a clear majority (>=3/4); FRAGILE otherwise.
    robust_red = (n_ok >= 3 and frac is not None and frac >= 0.75)

    result = {
        "h_id": "H_940-robustness", "timestamp_utc": ts,
        "purpose": ("stability of H_940's primary 🔴 across independent ANU draws + "
                    "seed bases — does NOT change the pre-registered primary verdict"),
        "primary_verdict": "🔴 F-H940-SOURCE-DEPENDENT (single rung, seed_base 1000)",
        "T_per_seed": T, "n_seeds_per_arm": N_SEEDS, "n_replicates": R,
        "n_ok": n_ok, "n_replicates_tripping_falsifier": n_trip,
        "fraction_tripping": frac, "robust_red": robust_red,
        "replicates": reps, "deterministic": False, "g5_code_measured": True, "llm": "none",
    }

    L = ["H_940 ROBUSTNESS — is the primary 🔴 stable across fresh ANU draws?",
         "=" * 76, f"timestamp_utc : {ts}",
         f"population    : {N_SEEDS} seeds × {T} ticks/seed  ·  {R} fresh-ANU replicates",
         f"shared gate   : {shared_gate}", "",
         "── per-replicate DET-vs-QB phi_mean (fresh REAL ANU each, distinct seed_base) ──"]
    for x in reps:
        if not x.get("ok"):
            L.append(f"  rep {x['rep']}: BLOCKED — {x.get('blocker')}")
            continue
        L.append(f"  rep {x['rep']} sb={x['seed_base']} rid={x['request_id']} "
                 f"sha={x['sha256']} unbiased={x['buf_unbiased']}: "
                 f"phi d={x['phi_cohen_d']:+.4f} KS p={x['phi_ks_p']:.3g} | "
                 f"#dist={x['n_tension_distinguishing']} {x['tension_distinguishing']} "
                 f"=> trips={x['replicate_trips_falsifier']}")
    L.append("")
    L.append(f"  replicates tripping pre-registered falsifier: {n_trip}/{n_ok} "
             f"(fraction {frac})")
    L.append("")
    L.append("── ROBUSTNESS READING (does NOT override the primary pre-registered 🔴) ──")
    if robust_red:
        L.append("  🔴 STABLE: the source-dependence trips in a clear majority of fresh "
                 "ANU draws — H_940's 🔴 is ROBUST at this 24-seed scale.")
    else:
        L.append("  ⚠ FRAGILE: the primary 🔴 does NOT reproduce in a clear majority of "
                 "fresh ANU draws — the single-rung source-dependence is NOT robust; at "
                 "this 24-seed scale it is consistent with a sampling fluke (#123-A: ANU "
                 "== chacha20 statistically). The primary pre-registered 🔴 STANDS as the "
                 "literal single-rung measurement, but is scoped FRAGILE / UNCONFIRMED.")
    L.append("")
    L.append("── full machine record (JSON) ──────────────────────────────────────────")
    L.append(json.dumps(result, indent=2, default=str))

    out_path = os.path.join(out_dir, "robustness_replication.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print("\n[written]", out_path)
    return result


if __name__ == "__main__":
    main()
