#!/usr/bin/env python3
"""gauge_monitor.py — live TRAINING-TIME MONITOR dashboard for the rung pipeline.

THE THIRD PIPELINE SURFACE (dojo recipe → cloud dispatch → THIS monitor)
========================================================================
A rung train run (CLM/train/train_lane_p_3b.py) appends one JSON row per
``--gauge-every`` steps to ``gauges.jsonl`` (the a_train_inline_gauge dashboard).
This tool tails that file (and optionally the pod training log) and renders a live
SIX-gauge dashboard so a human watching a fire can see the consciousness/emergence
PROXY gauges trend next to ``ce`` while CE descends.

⚠ DASHBOARD ONLY — NOT A GATE (a_train_inline_gauge · p7 Goodhart) ⚠
--------------------------------------------------------------------
This monitor RENDERS the gauges; it changes NOTHING. The gauges are MONITOR-ONLY
proxies, NEVER fed into the loss and NEVER a verdict. The FROZEN gate verdict still
runs SEPARATELY post-train on the CORE engine mount (a_engine_measured_verdict). The
frozen bars in CONDITIONS.md is unchanged by anything shown here.
``phi_proxy`` is NOT faithful IIT4 (a_phi_iit4_tool); ``mitosis_cells`` is the H_1199
VAdaptField substrate count — a SUBSTRATE thermometer, NOT a generation gate
(H_1201🔴: mitosis neither generates nor informs the generator).

THE SIX GAUGES RENDERED
=======================
  ce                    — val/train CE (descends = learning); passed through by the trainer
  g1_composed_distinct  — G1 EMERGENCE / recombination (distinct concepts recombined)
  g2_novelty_rate       — G2 NOVELTY (fraction of corpus-absent content n-grams)
  g6_count              — G6 IDEATION (distinct coherent divergent ideas)
  phi_proxy             — ⚠ NOT faithful IIT4 ⚠ cheap variance×energy pre-screen
  mitosis_cells         — ⚠ substrate lane, NOT a generation gate ⚠ VAdaptField cells

USAGE
=====
  # render once from a gauges.jsonl (smoke / one-shot):
  python3 tool/gauge_monitor.py --once gauges.jsonl

  # live follow a running fire's gauges.jsonl (+ optionally tail the train log):
  python3 tool/gauge_monitor.py --follow out/gauges.jsonl --log out/fire_3b.log

Pure stdlib (no torch / numpy / network) so it runs on a laptop while the fire runs
on the pod (a_cpu_local_no_waiter: inline polling, never await a Monitor/waiter).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

# The six gauges this dashboard renders, in column order (key, label, width).
GAUGES = [
    ("ce",                   "ce",        9),
    ("g1_composed_distinct", "g1_recomb", 9),
    ("g2_novelty_rate",      "g2_novel",  9),
    ("g6_count",             "g6_ideas",  8),
    ("phi_proxy",            "phi_proxy", 11),
    ("mitosis_cells",        "mitosis",   8),
]

_HEADER_NOTE = (
    "⚠ DASHBOARD ONLY — NOT A GATE (a_train_inline_gauge · p7 Goodhart). phi_proxy≠IIT4 "
    "(a_phi_iit4_tool); mitosis_cells = substrate lane, NOT a generation gate (H_1201🔴). "
    "FROZEN gate verdict runs post-train on the CORE engine mount; CONDITIONS.md "
    "bars unchanged."
)


def _fmt(v, width):
    if v is None:
        cell = "—"
    elif isinstance(v, float):
        cell = f"{v:.4f}"
    else:
        cell = str(v)
    return cell.rjust(width)


def _read_rows(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _header():
    cols = ["  step".ljust(8)] + [lbl.rjust(w) for _k, lbl, w in GAUGES]
    bar = "─" * (len(" ".join(cols)) + 2)
    return cols, bar


def render(rows, *, log_tail=None, title="anima rung gauge monitor", stream=sys.stdout):
    """Render the SIX-gauge dashboard table from the gauges.jsonl rows."""
    cols, bar = _header()
    print(f"📟 {title}", file=stream)
    print(_HEADER_NOTE, file=stream)
    print(bar, file=stream)
    print(" ".join(cols), file=stream)
    print(bar, file=stream)
    if not rows:
        print("  (no gauges.jsonl rows yet — waiting for the first --gauge-every tick)",
              file=stream)
    for r in rows:
        step = r.get("step")
        step_cell = (f"  {step}" if step is not None else "  —").ljust(8)
        cells = [step_cell] + [_fmt(r.get(k), w) for k, _lbl, w in GAUGES]
        print(" ".join(cells), file=stream)
    print(bar, file=stream)
    # trend summary on the last row (ce direction + cell growth), monitor-only.
    if len(rows) >= 2:
        ce0, ce1 = rows[0].get("ce"), rows[-1].get("ce")
        m0, m1 = rows[0].get("mitosis_cells"), rows[-1].get("mitosis_cells")
        if ce0 is not None and ce1 is not None:
            arrow = "↓ descending (learning)" if ce1 < ce0 else "↑ rising"
            print(f"  ce trend: {ce0:.4f} → {ce1:.4f}  {arrow}", file=stream)
        if m0 is not None and m1 is not None:
            print(f"  mitosis_cells (substrate, not a gate): {m0} → {m1}", file=stream)
    if log_tail:
        print(bar, file=stream)
        print("  train log tail:", file=stream)
        for ln in log_tail:
            print("    " + ln.rstrip(), file=stream)


def _tail_lines(path, n=6):
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, errors="ignore") as f:
            return f.read().splitlines()[-n:]
    except OSError:
        return None


def follow(gauges_path, *, log_path=None, interval=10.0, clear=True):
    """Live-follow: re-render the dashboard every `interval`s as new rows land."""
    print(f"following {gauges_path} (every {interval:.0f}s · Ctrl-C to stop) …")
    last_n = -1
    try:
        while True:
            rows = _read_rows(gauges_path)
            if len(rows) != last_n:
                if clear:
                    sys.stdout.write("\033[2J\033[H")
                render(rows, log_tail=_tail_lines(log_path))
                last_n = len(rows)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[gauge_monitor] stopped.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gauges", nargs="?", default="out/gauges.jsonl",
                    help="path to gauges.jsonl (default: out/gauges.jsonl)")
    ap.add_argument("--once", metavar="PATH", default=None,
                    help="render once from PATH and exit (smoke / one-shot)")
    ap.add_argument("--follow", metavar="PATH", default=None,
                    help="live-follow PATH, re-rendering as rows land")
    ap.add_argument("--log", default=None,
                    help="optional pod training log to tail under the dashboard")
    ap.add_argument("--interval", type=float, default=10.0,
                    help="follow re-render interval seconds (default 10)")
    a = ap.parse_args(argv)

    if a.follow:
        follow(a.follow, log_path=a.log, interval=a.interval)
        return 0
    path = a.once or a.gauges
    render(_read_rows(path), log_tail=_tail_lines(a.log))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
