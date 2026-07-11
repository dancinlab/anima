#!/usr/bin/env python3
"""
ARM-BLIND substrate liveness scan (V1 gate).  Looks ONLY at the c1_none (no
removal) pool: does the substrate end in a regime with a real health SPREAD
(some organelles damaged, some not)?  If everything is at the floor (v0 run) the
metric has no dynamic range and no arm - not even the latent-truth oracle - can
move it => the cell is INVALID, not THEATER.

Selection rule (declared BEFORE looking at any experimental arm, and mentioning
none of them):  final-window mean latent health of the NO-REMOVAL pool in
[0.35, 0.75]  AND  its std >= 0.10.
"""
import numpy as np
import run as R


def c1_health(p, seeds=(0, 1, 2)):
    ms, ss, effs = [], [], []
    for s in seeds:
        tape = R.make_tape(s, p)
        N, T = p["N0"], p["T"]
        h = tape["h0"].copy()
        cap = np.ones(N)
        alive = np.ones(N, dtype=bool)
        d_all = np.exp(p["SIGMA_DEMAND"] * tape["z"])
        eff = np.zeros(T)
        for t in range(T):
            w = cap * d_all[t] * alive
            load = p["D_TOTAL"] * w / max(w.sum(), 1e-12)
            eff[t] = (load * h).sum() / max(load.sum(), 1e-12)
            ros = load / np.maximum(cap * h, 1e-9)
            h = h * (1.0 - p["K_WEAR"] * np.clip(ros - p["ROS0"], 0.0, None))
            h = np.where(tape["hit"][t] < p["P_HIT"], h * tape["mag"][t], h)
            h = np.clip(h, p["H_FLOOR"], 1.0)
        ms.append(h.mean()); ss.append(h.std()); effs.append(eff[-p["FINAL_WIN"]:].mean())
    return float(np.mean(ms)), float(np.mean(ss)), float(np.mean(effs))


print(f"{'P_HIT':>7} {'K_WEAR':>7} {'ROS0':>5} | {'meanH':>6} {'stdH':>6} {'eff':>6}  live?")
cands = []
for ph in [0.004, 0.002, 0.001, 0.0005]:
    for kw in [0.002, 0.0005]:
        for r0 in [1.0, 1.5, 2.0]:
            p = dict(R.P); p["P_HIT"] = ph; p["K_WEAR"] = kw; p["ROS0"] = r0
            mh, sh, ef = c1_health(p)
            live = (0.35 <= mh <= 0.75) and (sh >= 0.10)
            if live:
                cands.append((ph, kw, r0, mh, sh, ef))
            print(f"{ph:>7} {kw:>7} {r0:>5} | {mh:>6.3f} {sh:>6.3f} {ef:>6.3f}  {'LIVE' if live else '.'}")
print("\nLIVE candidates:", cands)
