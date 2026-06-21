#!/usr/bin/env python3
"""
H_1531 horizon DIAGNOSTIC (NOT the verdict — a_break_the_wall taxonomy check).

The frozen-bar run (H_1531_R1.json) floored ALL arms near chance at K_interf=120 /
collinear_frac=0.6 on 24 targets: every target cell is clobbered ~3x, overwhelming
even the cascade's resistance. Before accepting WALL we must classify the wall
(a_break_the_wall): is this (a) a measurement artifact — a horizon calibrated to
overwhelm any store — or (d) a true ceiling where the cascade NEVER separates from
flat at ANY interference horizon?

This diagnostic SWEEPS the interference horizon (and collinear fraction) and reports
cascade-minus-flat at each, WITHOUT moving the frozen bar. It does not produce the
verdict; it tells us whether to re-fixture (frozen-first) or accept the wall.
"""
import numpy as np
import importlib.util, os

spec = importlib.util.spec_from_file_location(
    "h1531", os.path.join(os.path.dirname(__file__), "h1531_cascade_meta.py"))
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)

SEEDS = [11, 22, 33]
N_TARGETS = 24
N_CONFIRM = 3
MAX_CELLS = N_TARGETS * 3
ST = 0.4  # the grid-tuned best-fixed split_thresh from R1


def mean_ret(arm, K, cfrac, csig):
    vals = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        vals.append(h.run_trial(arm, rng, ST, N_TARGETS, N_CONFIRM, K, cfrac, csig, MAX_CELLS))
    return float(np.mean(vals))


print(f"{'K':>5} {'cfrac':>6} {'csig':>5} | {'FLAT':>6} {'CASC':>6} {'ABL':>6} {'SHUF':>6} | {'C-F':>7}")
print("-" * 64)
for csig in (0.18, 0.30):
    for cfrac in (0.6, 0.3, 0.15):
        for K in (24, 48, 72, 120):
            f = mean_ret('FLAT', K, cfrac, csig)
            c = mean_ret('CASCADE', K, cfrac, csig)
            a = mean_ret('ABL', K, cfrac, csig)
            s = mean_ret('SHUFFLE', K, cfrac, csig)
            print(f"{K:>5} {cfrac:>6} {csig:>5} | {f:>6.3f} {c:>6.3f} {a:>6.3f} {s:>6.3f} | {c-f:>+7.3f}")
    print()
