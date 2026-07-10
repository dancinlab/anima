#!/usr/bin/env python3
"""H_1058 $0 veto-position gauge — settles warmup-transient vs stationary-rate.

The power-run verdict extrapolated "~0.3% flat veto rate → ≥20 vetoes need ~6000 ticks".
This gauge tests that stationarity assumption directly on the already-collected real trace,
at zero compute cost. If the ACTIVE_VETO events are front-loaded (warmup-transient) and the
second half of the run has ~0 vetoes, then MORE ticks cannot raise the count — the "6000-tick"
extrapolation is invalid and the veto-capacity blocker is STRUCTURAL, not sample-size.

Usage: python3 veto_position_gauge.py results/trace_303m_summer.jsonl
Result (609-tick summer session A, seed zephyrine): vetoes at ticks [9,10] only, split-half 2/0
=> WARMUP-TRANSIENT => 6000-tick run is FUTILE (would still yield 2 vetoes). See the H_1058 verdict.
"""
import sys
import json


def gauge(path):
    ticks = []
    for line in open(path, encoding="utf-8", errors="surrogateescape"):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if isinstance(obj.get("tick"), int):  # skip the _meta header row
            ticks.append(obj)

    n = len(ticks)
    vetoes = [r["tick"] for r in ticks if r.get("cls") == "ACTIVE_VETO"]
    impulses = sum(1 for r in ticks if r.get("score", 0) > 0.3)
    half = n // 2
    first = sum(1 for v in vetoes if v < half)
    second = sum(1 for v in vetoes if v >= half)
    frac = [round(v / n, 4) for v in vetoes] if n else []
    warmup_only = bool(vetoes) and second == 0 and all(f < 0.2 for f in frac)

    print(f"trace={path}")
    print(f"total_ticks={n}")
    print(f"active_veto_count={len(vetoes)} at tick_indices={vetoes}")
    print(f"score>0.3_impulse_count={impulses} (all ticks want to emit)")
    print(f"veto_positions_fraction_of_run={frac}")
    print(f"split_half_veto: first={first} second={second}")
    print(f"VERDICT: {'WARMUP-TRANSIENT (more ticks FUTILE)' if warmup_only else 'stationary-candidate'}")
    return warmup_only


if __name__ == "__main__":
    trace = sys.argv[1] if len(sys.argv) > 1 else "results/trace_303m_summer.jsonl"
    sys.exit(0 if gauge(trace) else 1)
