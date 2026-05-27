#!/usr/bin/env python3
"""
hexa-senses verify/spec_inventory.py — 5-verb spec presence + provenance audit.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


VERB_TABLE = [
    ("dream",  "dream/hexa-dream.md"),
    ("ear",    "ear/hexa-ear.md"),
    ("empath", "empath/hexa-empath.md"),
    ("olfact", "olfact/hexa-olfact.md"),
    ("voice",  "voice/hexa-voice.md"),
]
TOTAL_EXPECTED = 5


def evaluate() -> dict:
    rows = []
    for verb, relpath in VERB_TABLE:
        path = ROOT / relpath
        present = path.exists()
        if present:
            text = path.read_text(encoding="utf-8")
            lines = text.count("\n")
            has_h1 = bool(re.search(r"(?m)^#\s+\S", text))
            has_canonical = "@canonical" in text[:1024]
        else:
            lines = 0; has_h1 = False; has_canonical = False
        rows.append({
            "verb": verb, "path": relpath, "present": present,
            "lines": lines, "has_h1_header": has_h1,
            "has_canonical_header": has_canonical,
        })
    checks = {
        "all_5_present":             all(r["present"] for r in rows),
        "every_present_has_h1":      all(r["has_h1_header"] for r in rows if r["present"]),
        "every_present_has_canonical": all(r["has_canonical_header"] for r in rows if r["present"]),
    }
    return {
        "rows": rows,
        "total_present": sum(1 for r in rows if r["present"]),
        "total_expected": TOTAL_EXPECTED,
        "checks": checks,
        "all_ok": all(checks.values()),
    }


def _print_human(r: dict) -> int:
    print("=" * 70)
    print("  hexa-senses — 5-verb spec inventory  (sensory rollup)")
    print("=" * 70)
    print(f"  {'verb':<8} {'lines':>6}  {'H1':>3}  {'@canon':>7}  path")
    print(f"  {'-'*8} {'-'*6}  {'-'*3}  {'-'*7}  {'-'*40}")
    for row in r["rows"]:
        h1 = "✓" if row["has_h1_header"] else "·"
        canon = "✓" if row["has_canonical_header"] else "·"
        if not row["present"]:
            print(f"  {row['verb']:<8} {'MISS':>6}  {'·':>3}  {'·':>7}  {row['path']}")
        else:
            print(f"  {row['verb']:<8} {row['lines']:>6}  {h1:>3}  {canon:>7}  {row['path']}")
    print()
    for k, ok in r["checks"].items():
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {k}")
    print("=" * 70)
    if r["all_ok"]:
        total = sum(row["lines"] for row in r["rows"])
        print(f"  5/5 verb specs present.  total lines: {total}")
        return 0
    print("  spec inventory has missing or malformed entries.")
    return 1


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="hexa-senses 5-verb spec inventory")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv[1:])
    r = evaluate()
    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0 if r["all_ok"] else 1
    return _print_human(r)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
