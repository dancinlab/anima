#!/usr/bin/env python3
"""anima-side falsifier orchestrator (F-M3b + F-M4 only).

Emits anima sister follow-up witness pointing to nexus 2026-05-07 master.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time

ANIMA_FALSIFIERS = ["F-M3b", "F-M4"]
HARNESS = {
    "F-M3b": [sys.executable, os.path.join(os.path.dirname(__file__), "phi_substrate_invariance.py")],
    "F-M4":  [sys.executable, os.path.join(os.path.dirname(__file__), "trace_equivalence.py")],
}


def run_one(fid: str, hardware: bool) -> dict:
    cmd = list(HARNESS[fid])
    if not hardware:
        cmd.append("--cpu-only")
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    wall = time.time() - t0
    last = None
    try:
        last = json.loads(proc.stdout.splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        try:
            last = json.loads(proc.stdout)
        except json.JSONDecodeError:
            pass
    return {
        "falsifier_id": fid, "command": " ".join(cmd),
        "returncode": proc.returncode, "wall_seconds": wall,
        "evidence": last, "stderr_tail": proc.stderr[-1000:] if proc.stderr else "",
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--hardware", action="store_true")
    p.add_argument("--only", choices=ANIMA_FALSIFIERS, default=None)
    p.add_argument("--out", default="design/kick/2026-05-07_anima-side-followup_omega_cycle.json")
    p.add_argument("--nexus-witness", default=os.path.expanduser("~/core/nexus/design/kick/2026-05-07_anima-nexus-akida-physical-math-limit-saturation_omega_cycle.json"))
    args = p.parse_args(argv[1:])

    ids = [args.only] if args.only else ANIMA_FALSIFIERS
    results = [run_one(fid, args.hardware) for fid in ids]

    follow = {
        "topic": "anima-side-akida-followup-2026-05-07",
        "sister_of_nexus_witness": args.nexus_witness,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": results,
        "evidence_summary": {
            r["falsifier_id"]: {
                "verdict": r["evidence"].get("verdict") if r["evidence"] else "NO-EVIDENCE",
                "raw_log_path": r["evidence"].get("raw_log_path") if r["evidence"] else None,
                "measured_ts": r["evidence"].get("measured_ts") if r["evidence"] else None,
            } for r in results
        },
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(follow, f, indent=2)
    print(json.dumps({"anima_followup_witness": args.out, "verdicts": follow["evidence_summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
