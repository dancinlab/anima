#!/usr/bin/env python3
"""compare.py — generic key=value byte/numeric parity comparator for the
core/ 2-production .hexa <-> .py mirror parity gate.

Usage: compare.py <hexa.txt> <py.txt> [tol_dp]
Parses lines of form `key=value` from both files (section headers `--- ... ---`
ignored, used only to keep ordering). Compares: numeric values to <tol_dp>
decimal places of relative agreement (default 12); non-numeric (strings/bools)
must be byte-identical. Prints first divergence + PASS/FAIL.
"""
import sys


def parse(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("---") or line == "":
                rows.append(("__section__", line))
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                rows.append((k.strip(), v.strip()))
    return rows


def isnum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def main():
    hexa, py = parse(sys.argv[1]), parse(sys.argv[2])
    tol_dp = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    # filter to key=value rows only, in order
    h = [(k, v) for k, v in hexa if k != "__section__"]
    p = [(k, v) for k, v in py if k != "__section__"]
    if len(h) != len(p):
        print("FAIL row-count: hexa=%d py=%d" % (len(h), len(p)))
        sys.exit(1)
    worst = 0.0
    worst_key = ""
    n = 0
    for (hk, hv), (pk, pv) in zip(h, p):
        if hk != pk:
            print("FAIL key-order: hexa=%s py=%s" % (hk, pk))
            sys.exit(1)
        if isnum(hv) and isnum(pv):
            a, b = float(hv), float(pv)
            denom = max(abs(a), abs(b), 1e-300)
            rel = abs(a - b) / denom
            if rel > worst:
                worst, worst_key = rel, hk
            thresh = 10.0 ** (-tol_dp)
            if rel > thresh:
                print("FAIL numeric %s: hexa=%s py=%s rel=%.3e > 1e-%d"
                      % (hk, hv, pv, rel, tol_dp))
                sys.exit(1)
        else:
            if hv != pv:
                print("FAIL string %s: hexa=%r py=%r" % (hk, hv, pv))
                sys.exit(1)
        n += 1
    print("PASS %d fields, worst rel=%.3e (%s), tol=1e-%d"
          % (n, worst, worst_key, tol_dp))


if __name__ == "__main__":
    main()
