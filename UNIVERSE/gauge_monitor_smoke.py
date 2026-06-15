#!/usr/bin/env python3
"""Smoke for gauge_monitor.render (c2 verify-before-done).

Writes a SAMPLE gauges.jsonl (a few rows mirroring the trainer's row schema, incl
mitosis_cells), renders the SIX-gauge dashboard with gauge_monitor.render, asserts
every gauge column + the DASHBOARD-NOT-A-GATE header is present, and prints the
render verbatim. Pure stdlib, $0, no torch/network.
"""
import io
import json
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import gauge_monitor as GM  # noqa: E402


def main():
    tmp = tempfile.mkdtemp(prefix="gauge_monitor_smoke_")
    gp = os.path.join(tmp, "gauges.jsonl")
    # sample rows matching CLM/train/train_lane_p_3b.py gauge_tick schema.
    sample = [
        {"step": 0,   "ce": 5.4231, "g1_composed_distinct": 0, "g2_novelty_rate": 0.0,
         "g6_count": 1, "g6_jaccard": None, "phi_proxy": 0.012345, "mitosis_cells": 3},
        {"step": 400, "ce": 2.8810, "g1_composed_distinct": 2, "g2_novelty_rate": 0.41,
         "g6_count": 3, "g6_jaccard": 0.62, "phi_proxy": 0.034521, "mitosis_cells": 11},
        {"step": 800, "ce": 1.9044, "g1_composed_distinct": 4, "g2_novelty_rate": 0.58,
         "g6_count": 5, "g6_jaccard": 0.71, "phi_proxy": 0.041002, "mitosis_cells": 18},
    ]
    with open(gp, "w") as f:
        for r in sample:
            f.write(json.dumps(r) + "\n")

    rows = GM._read_rows(gp)
    assert len(rows) == 3, f"expected 3 rows, got {len(rows)}"

    buf = io.StringIO()
    GM.render(rows, stream=buf)
    out = buf.getvalue()

    # all SIX gauge column labels must render.
    for _k, lbl, _w in GM.GAUGES:
        assert lbl in out, f"missing gauge column {lbl!r} in render"
    # the DASHBOARD-NOT-A-GATE governance header must be present.
    assert "NOT A GATE" in out
    assert "phi_proxy" in out and "IIT4" in out
    assert "mitosis_cells = substrate lane, NOT a generation gate" in out
    # the data must render (last-row values).
    assert "1.9044" in out and "18" in out

    print(out)
    print("SMOKE PASS — gauge_monitor.render emits the SIX-gauge dashboard "
          "(ce · g1_composed_distinct · g2_novelty_rate · g6_count · phi_proxy · "
          "mitosis_cells) from a sample gauges.jsonl, with the DASHBOARD-NOT-A-GATE "
          "header (a_train_inline_gauge · phi_proxy≠IIT4 · mitosis=substrate).")


if __name__ == "__main__":
    main()
