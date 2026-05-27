#!/usr/bin/env python3
"""
hexa-senses verify/cli.py — unified verifier dispatcher.

    python3 verify/cli.py             # all checks
    python3 verify/cli.py n6
    python3 verify/cli.py inventory
    python3 verify/cli.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

VERIFY_DIR = Path(__file__).resolve().parent
ROOT = VERIFY_DIR.parent

CHECKS = [
    ("n6",        "n6_arithmetic.py",  "n=6 lattice arithmetic + voice constraint"),
    ("inventory", "spec_inventory.py", "5-verb spec presence + headers"),
]
SCRIPT_FOR = {n: s for n, s, _ in CHECKS}
LABEL_FOR  = {n: l for n, _, l in CHECKS}


def _use_color() -> bool:
    return not os.environ.get("NO_COLOR") and sys.stdout.isatty()

def _c(code, t): return f"\033[{code}m{t}\033[0m" if _use_color() else t
def _green(t):  return _c("32", t)
def _red(t):    return _c("31", t)
def _bold(t):   return _c("1",  t)


def _run_one(name: str) -> dict:
    script = VERIFY_DIR / SCRIPT_FOR[name]
    if not script.exists():
        return {"name": name, "label": LABEL_FOR[name], "exit_code": 2,
                "duration_s": 0.0, "stdout": "", "stderr": f"missing: {script}",
                "ok": False}
    t0 = time.monotonic()
    rc = subprocess.run([sys.executable, str(script)],
                        capture_output=True, text=True, cwd=str(ROOT))
    dt = time.monotonic() - t0
    return {"name": name, "label": LABEL_FOR[name],
            "exit_code": rc.returncode, "duration_s": round(dt, 3),
            "stdout": rc.stdout, "stderr": rc.stderr,
            "ok": rc.returncode == 0}


def _print_human(results, quiet):
    if not quiet: print()
    for r in results:
        if not quiet:
            print("=" * 72)
            print(f"  ▶ {_bold(r['name'])}  —  {r['label']}")
            print("=" * 72)
            if r["stdout"]: print(r["stdout"].rstrip("\n"))
        verdict = _green("PASS") if r["ok"] else _red("FAIL")
        if not quiet: print()
        print(f"  [{verdict}] {r['name']:11s}  ({r['duration_s']:5.2f}s)  {r['label']}")
    print("=" * 72)
    n = len(results)
    n_ok = sum(1 for r in results if r["ok"])
    line = f"  {n_ok}/{n} checks PASS"
    print(_bold(_green(line)) if n_ok == n else _bold(_red(line)))


def main(argv):
    p = argparse.ArgumentParser(prog="verify/cli.py")
    p.add_argument("target", nargs="?", default="all")
    p.add_argument("--json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--list", action="store_true")
    a = p.parse_args(argv[1:])
    if a.list:
        for n, s, l in CHECKS:
            ex = (VERIFY_DIR / s).exists()
            mark = "ok " if ex else "MISS"
            print(f"  [{mark}] {n:11s} → verify/{s:24s}  {l}")
        return 0
    if a.target == "all":
        names = [n for n, _, _ in CHECKS]
    elif a.target in SCRIPT_FOR:
        names = [a.target]
    else:
        print(f"unknown check: {a.target!r}", file=sys.stderr); return 2
    results = [_run_one(n) for n in names]
    if a.json:
        n_ok = sum(1 for r in results if r["ok"])
        print(json.dumps({"tool": "hexa-senses verify/cli.py", "ok": n_ok == len(results),
                          "checks_total": len(results), "checks_pass": n_ok,
                          "results": results}, indent=2, ensure_ascii=False))
    else:
        _print_human(results, a.quiet)
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
