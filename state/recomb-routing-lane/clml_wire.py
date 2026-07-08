#!/usr/bin/env python3
"""H_9235 fork-A — wire a trained CLML lane (clml_lane.npz) into a base .clm → lane.clm.
Copies base.clm then appends the CLML trailer via core/serialize.append_clml_trailer (a lane .clm =
base + trailer; absent trailer = byte-identical). Usage: PYTHONPATH=core:cli python3 clml_wire.py <base.clm> <lane.npz> <out.clm>"""
import sys, shutil
sys.path[:0] = ["core", "cli"]
import numpy as np
import serialize as S


def main():
    base, lane_npz, out = sys.argv[1], sys.argv[2], sys.argv[3]
    z = np.load(lane_npz)
    lane = {"lane_type": 1, "r": int(z["r"]), "tau": float(z["tau"]),
            "W1": z["W1"], "b1": z["b1"], "W2": z["W2"], "w_g": z["w_g"], "b_g": float(z["b_g"])}
    shutil.copy(base, out)
    n = S.append_clml_trailer(out, lane)
    print("wired CLML lane (%d bytes) → %s" % (n, out))


if __name__ == "__main__":
    main()
