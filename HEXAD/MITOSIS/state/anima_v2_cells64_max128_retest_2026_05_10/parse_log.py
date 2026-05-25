"""parse_log.py — extract per-run checkpoint data from streaming runner log.

Parses the v5mitosis_d384_v14_mirror.py stdout (run_300_max128.log) and emits a
JSON snapshot of all completed runs (TRAINED + RANDOM_s* fully traversed). Can be
called repeatedly during training; writes to partial_result.json.

: deliverable; raw#9 local script.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TURN_RE = re.compile(r"^\s*\[(\w+)\]\s+turn\s+(\d+)\s+n_cells=(\d+)\s+phi=([\d\.\-]+)\s+phi/c=([\d\.\-]+)\s+\(([\d\.]+)s\)\s*$")
SECTION_RE = re.compile(r"^---\s+seed\s+(\d+)\s+---\s*$")


def parse(log_path: Path, n_turns_target: int = 300) -> Dict:
    runs: Dict[str, List[Tuple[int, int, float, float, float]]] = {}
    last_label: Optional[str] = None
    with log_path.open() as f:
        for line in f:
            m = TURN_RE.match(line)
            if m:
                label = m.group(1)
                turn = int(m.group(2))
                ncells = int(m.group(3))
                phi = float(m.group(4))
                phi_pc = float(m.group(5))
                elapsed = float(m.group(6))
                runs.setdefault(label, []).append((turn, ncells, phi, phi_pc, elapsed))
                last_label = label
                continue
            sm = SECTION_RE.match(line)
            if sm:
                # next run starts; don't reset, just track
                pass

    # A run is "complete" if its highest logged turn is at or beyond n_turns_target - 1
    # (the script logs every log_every and at last turn n_turns-1).
    completed = {}
    in_progress = {}
    for label, traj in runs.items():
        max_turn = max(e[0] for e in traj)
        last = traj[-1]
        cap_first = next((e[0] for e in traj if e[1] >= 128), None)
        max_n = max(e[1] for e in traj)
        # Use last logged entry as the "best estimate of final state"
        info = {
            "label": label,
            "max_turn_logged": max_turn,
            "last": {"turn": last[0], "n_cells": last[1], "phi": last[2], "phi_per_cell": last[3], "elapsed_s": last[4]},
            "max_n_cells_observed": max_n,
            "first_turn_at_cap_128": cap_first,
            "trajectory_logged": [list(e) for e in traj],
            "complete": max_turn >= (n_turns_target - 1),
        }
        if info["complete"]:
            completed[label] = info
        else:
            in_progress[label] = info
    return {"completed": completed, "in_progress": in_progress, "n_turns_target": n_turns_target}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default="run_300_max128.log")
    ap.add_argument("--out", default="partial_result.json")
    ap.add_argument("--n-turns", type=int, default=300)
    args = ap.parse_args()
    base = Path(__file__).resolve().parent
    log = base / args.log
    out = base / args.out
    res = parse(log, n_turns_target=args.n_turns)
    out.write_text(json.dumps(res, indent=2))
    print(f"completed: {list(res['completed'].keys())}")
    print(f"in_progress: {list(res['in_progress'].keys())}")
    for lbl, info in res["completed"].items():
        last = info["last"]
        print(f"  {lbl}: turn {last['turn']} n={last['n_cells']} phi={last['phi']:.2f} phi/c={last['phi_per_cell']:.3f}  cap@turn={info['first_turn_at_cap_128']}")


if __name__ == "__main__":
    main()
