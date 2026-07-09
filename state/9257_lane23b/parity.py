#!/usr/bin/env python3
"""H_9257 lane-23b — 2-production byte-parity oracle.

Compares the hexa production (core/generator.hexa gen_penult_pooled_W -> core/decode.hexa
clm_penult_pooled_W) against the py 2-production twin (core/decode.py clm_penult_pooled_W =
clm_forward_hidden + mean-pool over T) on a FIXED context tape, plus the FROZEN penult_fold8 axis.

Parity bar (terminal-eligibility contract, a_eval_py_canonical):
  * pooled-vector max|delta| <= ~2e-16 (libm parity), and
  * identical fold8 axis sequence.

Usage:
  python3 state/9257_lane23b/parity.py             # print the py reference tape
  python3 state/9257_lane23b/parity.py <hexa_dump> # + compare vs a hexa gen_penult_pooled_W dump

The hexa dump (from state/9257_lane23b/parity_hexa.hexa on a working hexa host / pool) has one
line per seed: "SEED<i> axis=<a> bits=b0,b1,...,b{d-1}" where each b is the exact u64 f64 bit
pattern (float_to_bits), so the comparison loses zero precision.
"""
import os
import struct
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))

import decode

# The FIXED context tape (frozen -- same seeds the hexa harness feeds). Mixed ko/en, distinct
# last-24-byte windows so fold8 exercises multiple buckets.
SEEDS = [
    "zephyrine: the wyrmhold ledger is sealed at ",
    "hello world self grounding test",
    "annyeonghaseyo oneul nalssiga jeongmal jokeyo sanchaek",
    "The quick brown fox jumps over the lazy dog near the river",
    "ingongjineunggwa uisige daehan cheolhakjeok jilmun",
    "def train_model(data): return model.fit(data, epochs=10)",
]

CLM = os.path.join(_HERE, "toy.clm")


def py_reference():
    W = decode.clm_load_weights(CLM)
    tape = []
    for s in SEEDS:
        pooled = decode.clm_penult_pooled_W(W, s)
        axis = decode.penult_fold8(pooled)
        tape.append((s, axis, pooled))
    return tape


def _parse_hexa_dump(path):
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("SEED"):
                continue
            head, _, rest = line.partition(" ")
            idx = int(head[4:])
            axis = None
            pooled = None
            for tok in rest.split():
                if tok.startswith("axis="):
                    axis = int(tok[5:])
                elif tok.startswith("bits="):
                    pooled = [struct.unpack("<d", struct.pack("<Q", int(b) & 0xFFFFFFFFFFFFFFFF))[0]
                              for b in tok[5:].split(",") if b != ""]
                elif tok.startswith("pooled="):
                    pooled = [float(x) for x in tok[7:].split(",") if x != ""]
            out[idx] = (axis, pooled)
    return out


def main():
    tape = py_reference()
    print("=== H_9257 parity -- py reference tape (clm=%s) ===" % CLM)
    py_axes = []
    for i, (s, axis, pooled) in enumerate(tape):
        py_axes.append(axis)
        print("SEED%d axis=%d d=%d pooled[:4]=%s"
              % (i, axis, len(pooled), [round(x, 12) for x in pooled[:4]]))
    print("py fold8 axis-seq:", py_axes)

    if len(sys.argv) < 2:
        print("\n(no hexa dump given -- run parity_hexa.hexa on a hexa host, then pass its dump)")
        return

    hexa = _parse_hexa_dump(sys.argv[1])
    print("\n=== compare vs hexa dump: %s ===" % sys.argv[1])
    worst = 0.0
    axis_ok = True
    for i, (s, axis, pooled) in enumerate(tape):
        if i not in hexa:
            print("SEED%d MISSING in hexa dump" % i)
            axis_ok = False
            continue
        h_axis, h_pooled = hexa[i]
        dmax = max(abs(a - b) for a, b in zip(pooled, h_pooled))
        worst = max(worst, dmax)
        same_axis = (axis == h_axis)
        axis_ok = axis_ok and same_axis
        print("SEED%d py_axis=%d hexa_axis=%d axis_match=%s pooled_max|delta|=%.3e"
              % (i, axis, h_axis, same_axis, dmax))
    print("\npooled max|delta| (worst over tape) = %.3e   (bar <= 2e-16)" % worst)
    print("fold8 axis-seq identical = %s" % axis_ok)
    ok = (worst <= 2e-16) and axis_ok
    print("PARITY VERDICT: %s" % ("PASS" if ok else "FAIL"))


if __name__ == "__main__":
    main()
