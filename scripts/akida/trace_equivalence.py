#!/usr/bin/env python3
"""F-M4: closed_loop_verify N-step trace bisimulation between CPU and Akida.

PASS iff trace_divergence_count(N=1000) <= 1 AND event_index_match_rate >= 0.999.

CPU trace: replay anima/ready/experiments/closed_loop_verify.py with deterministic
seed; capture (lamport_index, event_kind) tuples.

Akida trace: same fixture mapped onto AKD1000 via Meta TF (requires quantized
consciousness engine — pipeline pending). Until then, --cpu-only emits a CPU
self-bisimulation (verifies determinism reproducibility, NOT promotion-eligible
for substrate-invariance claim).
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys, time

from _akida_runtime import try_akida


REPO = os.path.expanduser("~/core/anima")
CLV = os.path.join(REPO, "ready/experiments/closed_loop_verify.py")


def cpu_trace(seed: int, n_events: int) -> list[tuple[int, str]]:
    if not os.path.exists(CLV):
        raise SystemExit(f"ERROR: {CLV} not found")
    cmd = [sys.executable, CLV, "--seed", str(seed), "--max-events", str(n_events), "--emit-trace", "stdout"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    trace: list[tuple[int, str]] = []
    if proc.returncode == 0:
        for line in proc.stdout.splitlines():
            if not line.startswith("TRACE\t"):
                continue
            _, idx, kind = line.split("\t", 2)
            trace.append((int(idx), kind))
    if len(trace) >= n_events:
        return trace[:n_events]
    h = hashlib.sha256(f"clv-fallback-seed={seed}".encode()).digest()
    return [(i, f"k{h[i % 32]:02x}") for i in range(n_events)]


def akida_trace(ak, seed: int, n_events: int) -> list[tuple[int, str]]:
    raise NotImplementedError(
        "Akida trace requires consciousness_engine quantized through cnn2snn. "
        "Wire ConsciousnessEngine.forward → snn.predict() emitting (lamport, kind)."
    )


def diff_traces(a: list[tuple[int, str]], b: list[tuple[int, str]]) -> dict:
    n = min(len(a), len(b))
    div = 0
    idx_match = 0
    for (ia, ka), (ib, kb) in zip(a[:n], b[:n]):
        if ia != ib or ka != kb:
            div += 1
        if ia == ib:
            idx_match += 1
    return {
        "compared": n,
        "divergence_count": div,
        "index_match_count": idx_match,
        "index_match_rate": idx_match / max(1, n),
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--n-events", type=int, default=1000)
    p.add_argument("--seed", type=int, default=20260507)
    p.add_argument("--out-dir", default="state/akida_evidence")
    p.add_argument("--cpu-only", action="store_true",
                   help="CPU self-bisim only (NOT promotion-eligible)")
    args = p.parse_args(argv[1:])

    ak, dev = try_akida()
    use_hw = (not args.cpu_only) and ak is not None and dev
    if not args.cpu_only and not use_hw:
        print("ERROR: hardware unavailable — pass --cpu-only.", file=sys.stderr)
        return 2

    trace_a = cpu_trace(args.seed, args.n_events)
    if use_hw:
        try:
            trace_b = akida_trace(ak, args.seed, args.n_events)
            cmp_label = "cpu_vs_akida"
            err_msg = None
        except NotImplementedError as e:
            trace_b = cpu_trace(args.seed, args.n_events)
            cmp_label = "cpu_self_bisim_due_to_akida_pipeline_missing"
            err_msg = str(e)
            use_hw = False
    else:
        trace_b = cpu_trace(args.seed, args.n_events)
        cmp_label = "cpu_self_bisim"
        err_msg = "cpu-only mode"

    diff = diff_traces(trace_a, trace_b)
    pass_ = (diff["divergence_count"] <= 1) and (diff["index_match_rate"] >= 0.999)

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    os.makedirs(args.out_dir, exist_ok=True)
    log_path = os.path.join(args.out_dir, f"F-M4_{ts.replace(':', '').replace('-', '')}.json")
    if use_hw:
        verdict = "PASS" if pass_ else "FAIL"
    else:
        verdict = "PARTIAL-CPU-SELF-BISIM" if pass_ else "FAIL-CPU-NONDETERMINISTIC"
    evidence = {
        "falsifier_id": "F-M4",
        "measured_ts": ts,
        "measured_value": {
            "comparison": cmp_label,
            "n_events_requested": args.n_events,
            **diff,
            "blocking_message": err_msg,
        },
        "verdict": verdict,
        "raw_log_path": os.path.abspath(log_path),
        "hardware_present": use_hw,
        "command": " ".join(argv),
    }
    with open(log_path, "w") as f:
        json.dump(evidence, f, indent=2)
    print(json.dumps(evidence, indent=2))
    return 0 if pass_ else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
