#!/usr/bin/env python3
# h1297_engine_export.py — export the R3 SHARP-TARGET supervised pairs (byte-exact
# with UNIVERSE/h1297_r2_sharp_target.py) for the ENGINE-NATIVE probe
# CORE/h1297_mitosis_train_engine_probe.hexa (a_engine_native_learning +
# a_verified_must_wire).
#
# The R3 mirror builds (feature, next_byte) pairs over a fixed Korean+English UTF-8
# byte corpus with CTX=4 + a 3-D feature phi(ctx) = [last/255, 2nd-last/255,
# cont_depth/3], even-index->train, odd-index->test. The corpus + features are
# SEED-INDEPENDENT (the mirror's seed only perturbs arm A init + the shuffle RNG;
# the targeted/ablate partition geometry is deterministic). So a single export of
# the deterministic train/test pairs feeds every seed of the engine probe.
#
# The SHUFFLE arm (split a RANDOM eligible cell) is a CONTROL — its only requirement
# is that the split target is decorrelated from per-cell error. The mirror picks it
# with numpy's Mersenne-Twister; the engine probe picks it with an engine-native LCG
# (seeded per seed). The specific RNG is immaterial to the control's validity (both
# are error-AGNOSTIC random picks); making it engine-native keeps the ENGINE the sole
# decider (a_engine_native_learning) rather than importing numpy's RNG state. So NO
# draw stream is exported — the shuffle RNG runs inside the .hexa probe.
#
# arm A (gradient) is the INCUMBENT control, re-used VERBATIM from the mirror
# (numpy backprop, unchanged) — the ENGINE realizes only arm B mitosis. We export
# arm A's per-seed CE so the engine probe scores c1 against the SAME incumbent.
#
# $0 CPU, no GPU, no secrets. The corpus is declared in the mirror (provenance).

import numpy as np
import os
import sys

# import the FROZEN mirror so corpus + feature fn are byte-identical (single SSOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h1297_r2_sharp_target as M  # noqa: E402

OUT = "/tmp"


def main():
    Xtr, Ytr, Xte, Yte = M.make_pairs()
    with open(f"{OUT}/h1297_train.feats", "w") as f:
        for row in Xtr:
            f.write(" ".join(f"{v:.10f}" for v in row) + "\n")
    with open(f"{OUT}/h1297_train.next", "w") as f:
        f.write("\n".join(str(int(y)) for y in Ytr) + "\n")
    with open(f"{OUT}/h1297_test.feats", "w") as f:
        for row in Xte:
            f.write(" ".join(f"{v:.10f}" for v in row) + "\n")
    with open(f"{OUT}/h1297_test.next", "w") as f:
        f.write("\n".join(str(int(y)) for y in Yte) + "\n")

    with open(f"{OUT}/h1297_armA.ce", "w") as f:
        for seed in M.SEEDS:
            a_ce, a_acc, a_params = M.arm_gradient(Xtr, Ytr, Xte, Yte, seed)
            f.write(f"{seed} {a_ce:.10f} {a_acc:.10f} {a_params}\n")

    print(f"exported: train_pairs={Xtr.shape[0]} test_pairs={Xte.shape[0]} "
          f"V={M.V} CTX={M.CTX} seeds={M.SEEDS}")
    print(f"  {OUT}/h1297_train.feats .next  {OUT}/h1297_test.feats .next")
    print(f"  {OUT}/h1297_armA.ce")


if __name__ == "__main__":
    main()
