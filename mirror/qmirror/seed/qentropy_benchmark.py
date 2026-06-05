#!/usr/bin/env python3
"""qentropy_benchmark.py — per-path QUANTUM-vs-DETERMINISTIC A/B benchmark harness.

H_924 M6. One-command, Mac-runnable ($0, no device, no torch) A/B runner over every
SW-reachable anima entropy seed/sample path. For each path it runs N trials in BOTH
entropy modes and records a ledger row.

────────────────────────────────────────────────────────────────────────────────
WHAT THIS IS — and what it deliberately is NOT
────────────────────────────────────────────────────────────────────────────────
This is a STATISTICAL-PARITY SANITY check + a PROVENANCE DIFFERENTIATOR surface.
It is *not* a superiority test. The honest non-claim (#123-A, NIST SP 800-22 7/7)
is that ANU vacuum-fluctuation entropy is statistically EQUAL to a chacha20/numpy
PRNG (JSD 0.000433, 23x under threshold). So we EXPECT the two modes to come out
statistically indistinguishable at the application level — and that expectation IS
the test: if the application-level distributions diverged wildly, *that* would be a
red flag (a coupling bug), not a win.

The difference that actually matters — and the reason both modes exist — is
PROVENANCE / auditability:

    quantum       -> tier=anu_committed, sha256 of the real ANU vacuum-fluctuation
                     buffer (a physical, auditable origin you can pin to a draw).
    deterministic -> tier=numpy_prng(seed=187), reproducible, no physical origin.

So the ledger surfaces, per path: (a) each mode's metric mean/std over N trials,
(b) a simple two-sample closeness check (|Δmean| / pooled_std) confirming parity,
and (c) each mode's provenance (mode / tier / sha256). The headline is NOT a delta
in the metric — it is the provenance column.

────────────────────────────────────────────────────────────────────────────────
WHY A SUBPROCESS PER ARM
────────────────────────────────────────────────────────────────────────────────
qentropy.py reads ANIMA_ENTROPY_MODE *at import time* (module-global `_MODE`). Once
imported in this process, flipping os.environ would NOT change its behavior. So each
(path, mode) arm runs in a FRESH `python3 -c ...` subprocess with ANIMA_ENTROPY_MODE
set in its environment. That guarantees the mode is honestly fresh per arm and that
this harness's own import of qentropy can never contaminate an arm.

────────────────────────────────────────────────────────────────────────────────
PATHS
────────────────────────────────────────────────────────────────────────────────
SW-runnable now (benchmarked here):
  * plasticity_sw_approx  — SW learning. Metric = weight_l1 (a scalar summarizing
                            the learned weight matrix) per trial, over N trials.
  * decoder_qsample       — DECODER sampling. Metric = Shannon entropy (bits) of the
                            sampled-token histogram per trial, over N trials; we also
                            aggregate the pooled token histogram per mode.

device/torch-pending (recorded as rows so the surface is complete + extensible):
  * akida_r2_noise        — AKIDA spontaneous R2 noise (pi5-akida AKD1000). Same A/B
                            by flipping ANIMA_ENTROPY_MODE on the pi5 host.
  * akida_edge_learn      — AKIDA on-chip edge-learn input (pi5-akida). Same A/B.
  * torch_lane_p          — torch Lane-P CLM seed (GPU host). Same A/B; needs torch.

See BENCHMARK.md for how to flip those on once the device/torch host is available.

────────────────────────────────────────────────────────────────────────────────
USAGE
────────────────────────────────────────────────────────────────────────────────
    python3 qentropy_benchmark.py                 # default N=64, JSON ledger to stdout
    python3 qentropy_benchmark.py --n 128         # more trials per arm
    python3 qentropy_benchmark.py --out ledger.json
    python3 qentropy_benchmark.py --json | jq .   # pipe-friendly

The per-arm env (ANIMA_ENTROPY_MODE) is set by the harness internally; you do NOT
set it yourself when running the full A/B. (You CAN set it for a single manual run
of a path module — see BENCHMARK.md.)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
# repo root = mirror/qmirror/seed -> up 3
_REPO = os.path.abspath(os.path.join(_HERE, os.pardir, os.pardir, os.pardir))

MODES = ("quantum", "deterministic")


# ────────────────────────────────────────────────────────────────────────────
# Arm runners. Each runs ONE mode in a fresh subprocess (so ANIMA_ENTROPY_MODE is
# honestly applied at qentropy import time) and returns a list of per-trial scalar
# metrics + the provenance dict of (the last) draw + optional path-specific extras.
# ────────────────────────────────────────────────────────────────────────────

def _run_arm(mode: str, snippet: str) -> dict:
    """Run `snippet` in a fresh python3 -c subprocess with ANIMA_ENTROPY_MODE=mode.

    The snippet MUST print exactly one line of JSON to stdout as its LAST stdout line:
        {"metrics": [float, ...], "provenance": {...}, "extra": {...}}
    `extra` is optional path-specific aggregate data (e.g. a pooled histogram).
    qentropy's committed-buffer resolution works offline, so no network is used.
    """
    env = dict(os.environ)
    env["ANIMA_ENTROPY_MODE"] = mode
    # Make sure the arm can import qentropy + the path modules regardless of cwd.
    preamble = (
        "import sys, os, json\n"
        f"sys.path.insert(0, {_HERE!r})\n"            # qentropy
        f"sys.path.insert(0, {os.path.join(_REPO, 'PLASTICITY')!r})\n"
        f"sys.path.insert(0, {os.path.join(_REPO, 'CORE', 'DECODER')!r})\n"
        "import numpy as np\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", preamble + snippet],
        capture_output=True, text=True, env=env, cwd=_REPO, timeout=300,
    )
    if proc.returncode != 0:
        return {"error": (proc.stderr.strip()[-800:] or "nonzero exit"),
                "metrics": [], "provenance": {}, "extra": {}}
    # The arm may emit a benign stderr WARN (e.g. fallback). Parse the LAST stdout line.
    lines = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()]
    if not lines:
        return {"error": "no stdout", "metrics": [], "provenance": {}, "extra": {}}
    out = json.loads(lines[-1])
    out.setdefault("extra", {})
    return out


def arm_plasticity(mode: str, n: int) -> dict:
    """SW learning path: run sw_approx_fit N times, collect weight_l1 per trial.

    Each trial draws a fresh weight-init from qentropy (the SW learning lever), so
    across N trials the weight_l1 spread reflects the entropy policy's variation.
    The input spike pattern is held FIXED across trials (a fixed deterministic numpy
    seed inside the arm) so the ONLY varying factor is the qentropy-sourced init —
    isolating the entropy path under test."""
    snippet = f"""
import plasticity_sw_approx as P
metrics = []
prov = {{}}
fixed = np.random.default_rng(20260606).integers(0, 2, size=(8, P.IN_DIM), dtype=np.uint8)
for _ in range({n}):
    r = P.sw_approx_fit(fixed)
    metrics.append(float(r["weight_l1"]))
    prov = r["entropy_provenance"]
print(json.dumps({{"metrics": metrics, "provenance": prov, "extra": {{}}}}))
"""
    return _run_arm(mode, snippet)


def arm_decoder(mode: str, n: int) -> dict:
    """DECODER sampling path: for each of N trials draw a block of tokens from a
    FIXED logits vector and record the Shannon entropy (bits) of that trial's token
    histogram. Also aggregate a pooled token histogram across all draws per mode. The
    forward logits are identical in both modes (only the draw differs)."""
    snippet = f"""
import decoder_qsample as D
logits = np.array([2.0, 1.0, 0.5, 3.0, 0.2, 1.5], dtype=np.float64)
block = 16
metrics = []
pooled = {{}}
prov = {{}}
for _ in range({n}):
    res = D.sample_n(logits, n=block, temperature=1.0)
    draws = res["draws"]
    vals, cnts = np.unique(draws, return_counts=True)
    p = cnts / cnts.sum()
    ent = float(-(p * np.log2(p)).sum())   # Shannon entropy (bits) of this trial
    metrics.append(ent)
    for v, c in zip(vals.tolist(), cnts.tolist()):
        pooled[str(int(v))] = pooled.get(str(int(v)), 0) + int(c)
    prov = res["provenance"]
print(json.dumps({{"metrics": metrics, "provenance": prov,
                   "extra": {{"pooled_histogram": pooled,
                              "argmax_forward": int(np.argmax(logits))}}}}))
"""
    return _run_arm(mode, snippet)


# ────────────────────────────────────────────────────────────────────────────
# Stats helpers (stdlib only — the harness top-level needs nothing exotic)
# ────────────────────────────────────────────────────────────────────────────

def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def _std(xs):
    if not xs or len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _two_sample(a: list, b: list) -> dict:
    """A small, honest two-sample closeness check between the two modes' metric
    samples. We report |Δmean| / pooled_std (a standardized mean separation): values
    near 0 = statistically indistinguishable (PARITY, the EXPECTED outcome); large
    values would flag a coupling anomaly. Also report the raw delta/pooled. This is
    deliberately a *parity* statistic, NOT a superiority/win metric."""
    ma, mb = _mean(a), _mean(b)
    if ma is None or mb is None:
        return None
    sa, sb = _std(a), _std(b)
    pooled = math.sqrt((sa ** 2 + sb ** 2) / 2.0)
    if pooled == 0.0:
        sep = 0.0 if ma == mb else float("inf")
    else:
        sep = abs(ma - mb) / pooled
    return {
        "delta_mean": ma - mb,
        "abs_delta_mean": abs(ma - mb),
        "pooled_std": pooled,
        "standardized_separation": sep,            # ~0 = parity; >~1 = investigate
        "parity_check": ("PARITY (statistically indistinguishable)"
                         if sep < 1.0 else "DIVERGENT (investigate coupling)"),
    }


def _prov_view(p: dict) -> dict:
    """The provenance columns that actually matter for the audit trail."""
    return {"mode": p.get("mode"), "tier": p.get("tier"), "sha256": p.get("sha256")}


# ────────────────────────────────────────────────────────────────────────────
# Ledger assembly
# ────────────────────────────────────────────────────────────────────────────

# device/torch-pending rows: the SAME A/B applies by flipping ANIMA_ENTROPY_MODE on
# the device/GPU host. Recorded so the benchmark surface is complete + obviously
# extensible (see BENCHMARK.md "Extending to device/torch paths").
PENDING_PATHS = [
    {
        "path": "akida_r2_noise",
        "status": "device-pending",
        "substrate": "pi5-akida (AKD1000)",
        "module": "SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py",
        "metric": "R2 spontaneous-noise symbol histogram / spike rate",
        "how_to_run": ("on pi5-akida: ANIMA_ENTROPY_MODE={quantum,deterministic} "
                       "python3 spontaneous_emission.py  (qentropy_uniform 0..3)"),
    },
    {
        "path": "akida_edge_learn",
        "status": "device-pending",
        "substrate": "pi5-akida (AKD1000)",
        "module": "SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py",
        "metric": "on-chip learned winner-unit distribution",
        "how_to_run": ("on pi5-akida: ANIMA_ENTROPY_MODE={quantum,deterministic} "
                       "python3 edge_learn_probe.py  (qentropy_bits learn-input)"),
    },
    {
        "path": "torch_lane_p",
        "status": "torch-pending",
        "substrate": "GPU host (Lane-P)",
        "module": "CLM/train/_qseed.py (resolve_seed) + _qseed_check.py",
        "metric": "torch.manual_seed -> torch.rand sample distribution",
        "how_to_run": ("on a torch host: ANIMA_ENTROPY_MODE={quantum,deterministic} "
                       "python3 CLM/train/_qseed_check.py"),
    },
]


def build_ledger(n: int) -> dict:
    runnable = [
        ("plasticity_sw_approx", arm_plasticity,
         "weight_l1", "L1 norm of SW-learned weight matrix (scalar per trial)"),
        ("decoder_qsample", arm_decoder,
         "token_hist_entropy_bits",
         "Shannon entropy (bits) of sampled-token histogram per trial"),
    ]
    rows = []
    for path, runner, metric_name, metric_desc in runnable:
        per_mode = {}
        arm_extra = {}
        raw_metrics = {}
        for mode in MODES:
            res = runner(mode, n)
            metrics = res.get("metrics", [])
            raw_metrics[mode] = metrics
            per_mode[mode] = {
                "n": len(metrics),
                "metric_mean": _mean(metrics),
                "metric_std": _std(metrics),
                "provenance": _prov_view(res.get("provenance", {})),
                "error": res.get("error"),
            }
            if res.get("extra"):
                arm_extra[mode] = res["extra"]
        comparison = _two_sample(raw_metrics["quantum"], raw_metrics["deterministic"])
        qp = per_mode["quantum"]["provenance"]
        dp = per_mode["deterministic"]["provenance"]
        row = {
            "path": path,
            "status": "benchmarked",
            "substrate": "SW (Mac, $0, no device/torch)",
            "metric_name": metric_name,
            "metric_desc": metric_desc,
            "n_per_mode": n,
            "modes": per_mode,
            "comparison": comparison,
            "provenance_differs": (qp.get("tier") != dp.get("tier")),
        }
        if arm_extra:
            row["extra"] = arm_extra
        rows.append(row)
    return {
        "benchmark": "qentropy_quantum_vs_deterministic_AB",
        "milestone": "H_924 M6",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "host": "mac (SW-only, $0, no device, no torch)",
        "n_trials_per_arm": n,
        "modes": list(MODES),
        "framing": ("Statistical-parity SANITY + PROVENANCE differentiator, NOT a "
                    "superiority test. #123-A: ANU quantum == chacha20 PRNG statistically "
                    "(JSD 23x under NIST 7/7). Expectation: per-path metric distributions "
                    "are statistically indistinguishable across modes (parity holds at the "
                    "application level); the difference that matters is the provenance "
                    "column (quantum->anu_committed sha256 vs deterministic->numpy_prng seed)."),
        "rows": rows,
        "device_pending_rows": PENDING_PATHS,
        "honest_non_claim": ("This benchmark does NOT and cannot show quantum entropy is "
                             "'better'. The two modes are by design statistically equal. "
                             "The auditable PROVENANCE (physical ANU origin + sha256) is the "
                             "only real differentiator and is surfaced per path/mode."),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="qentropy quantum-vs-deterministic A/B benchmark")
    ap.add_argument("--n", type=int, default=64, help="trials per (path, mode) arm (>=64)")
    ap.add_argument("--out", type=str, default="", help="write ledger JSON to this path")
    ap.add_argument("--json", action="store_true", help="print ledger JSON to stdout (default)")
    args = ap.parse_args()
    n = max(args.n, 1)
    ledger = build_ledger(n)
    text = json.dumps(ledger, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            f.write(text + "\n")
        sys.stderr.write(f"[qentropy_benchmark] ledger written: {args.out}\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
