#!/usr/bin/env python3
"""F-M3b: Putnam multiple-realization fixed-point.

Compute anima Phi-vector on (a) CPU baseline, (b) AKD1000-quantized model.
PASS iff max relative error across an N-input panel <= 5%.

The CPU arm uses the in-process Python intrinsic proxy below. It has no
external runtime or subprocess dependency.

Akida side requires a quantized Phi calculator deployed via Meta TF (cnn2snn);
this script raises NotImplementedError until that pipeline lands, but the CPU
side runs and emits a partial evidence file so progress is auditable.
"""
from __future__ import annotations
import argparse, json, os, statistics, sys, time

from _akida_runtime import try_akida

def synth_panel(n: int, seed: int = 0):
    import numpy as np
    rng = np.random.default_rng(seed)
    return [rng.normal(size=(8, 16)).astype("float32") for _ in range(n)]


def phi_cpu(state) -> float:
    return _phi_intrinsic(state)


def _phi_intrinsic(state) -> float:
    import numpy as np
    arr = state.flatten()
    if arr.size < 2:
        return 0.0
    cov = float(np.var(arr))
    return min(1.0, cov / (1.0 + cov))


def phi_akida(ak, state) -> float:
    raise NotImplementedError(
        "Akida Phi requires Meta TF cnn2snn-quantized Phi calculator + AKD1000 deploy. "
        "Wire the Python intrinsic proxy through cnn2snn.convert() and load the resulting .fbz."
    )


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--panel-size", type=int, default=100)
    p.add_argument("--threshold", type=float, default=0.05)
    p.add_argument("--out-dir", default="state/akida_evidence")
    p.add_argument("--cpu-only", action="store_true",
                   help="emit partial evidence with Akida side stubbed (NOT promotion-eligible)")
    args = p.parse_args(argv[1:])

    panel = synth_panel(args.panel_size)
    phi_c = [phi_cpu(s) for s in panel]

    ak, dev = try_akida()
    use_hw = (not args.cpu_only) and ak is not None and dev
    if not args.cpu_only and not use_hw:
        print("ERROR: hardware unavailable — pass --cpu-only for partial evidence.", file=sys.stderr)
        return 2

    if use_hw:
        try:
            phi_a = [phi_akida(ak, s) for s in panel]
        except NotImplementedError as e:
            phi_a = None
            err_msg = str(e)
        else:
            err_msg = None
    else:
        phi_a = None
        err_msg = "cpu-only mode"

    rel_errs: list[float] = []
    if phi_a is not None:
        for c, a in zip(phi_c, phi_a):
            denom = max(1e-12, abs(c))
            rel_errs.append(abs(c - a) / denom)
        max_err = max(rel_errs) if rel_errs else float("inf")
        pass_ = max_err <= args.threshold
        verdict = "PASS" if pass_ else "FAIL"
    else:
        max_err = None
        pass_ = False
        verdict = "PARTIAL-CPU-ONLY" if not use_hw else "BLOCKED-AKIDA-PIPELINE-MISSING"

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    os.makedirs(args.out_dir, exist_ok=True)
    log_path = os.path.join(args.out_dir, f"F-M3b_{ts.replace(':', '').replace('-', '')}.json")
    evidence = {
        "falsifier_id": "F-M3b",
        "measured_ts": ts,
        "measured_value": {
            "panel_size": args.panel_size,
            "phi_cpu_mean": statistics.fmean(phi_c) if phi_c else None,
            "phi_cpu_min": min(phi_c) if phi_c else None,
            "phi_cpu_max": max(phi_c) if phi_c else None,
            "phi_akida_run": phi_a is not None,
            "max_rel_err": max_err,
            "threshold": args.threshold,
            "blocking_message": err_msg,
        },
        "verdict": verdict,
        "raw_log_path": os.path.abspath(log_path),
        "hardware_present": use_hw and phi_a is not None,
        "command": " ".join(argv),
    }
    with open(log_path, "w") as f:
        json.dump(evidence, f, indent=2)
    print(json.dumps(evidence, indent=2))
    return 0 if pass_ else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
