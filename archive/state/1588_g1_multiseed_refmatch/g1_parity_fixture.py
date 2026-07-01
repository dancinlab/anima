#!/usr/bin/env python3
"""g1_parity_fixture.py — py side of the multi-seed G1 byte-parity oracle (lockstep with
g1_parity_fixture.hexa). Runs core/g_gates.py g_eval_g1_seeded on the SAME tiny .clm fixture +
base_seed + gen, printing the per-seed counts in the identical key:value form the .hexa harness
emits, so a plain diff proves .hexa == .py."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import g_gates as G

def main():
    ck = os.environ["FX_CK"]; seed = int(os.environ["FX_SEED"]); gen = int(os.environ["FX_GEN"])
    known = G._g6_dict_load()
    mouth = G._Mouth(ck)
    r = G.g_eval_g1(mouth, gen, known, base_seed=seed)
    print("base_seed:%s" % r["base_seed"])
    print("max_single:%s" % r["max_single"])
    print("best_k:%s" % r["best_k"])
    print("best_distinct:%s" % r["best_distinct"])
    print("pass:%s" % ("true" if r["pass"] else "false"))

if __name__ == "__main__": main()
