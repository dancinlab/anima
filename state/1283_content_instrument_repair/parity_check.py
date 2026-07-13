"""PARITY GATE — the py port must reproduce the hexa engine run, or nothing downstream is valid.

Recomputes every Phi the hexa H_9260 probe printed (10 arms x 9 seeds, raw and rank-uniform
read-outs) with the py port, and reports max|delta| against the hexa anchor. This is the
`reference-match` receipt that licenses a py-channel verdict under `a_phi_iit4_tool`: the
estimator is the mandated faithful IIT-4 exact MIP-EI, not a proxy or a re-derivation.

usage:  python3 parity_check.py <hexa_anchor_stdout.txt>
"""

from __future__ import annotations

import re
import sys

import numpy as np

from faithful_phi import faithful_phi
from substrate import (
    APERM, A_DIRECT, BPERM, B_MULTI, CPERM, DENSE_SHUF, DIM, NBINS, N_MOD, N_SELF,
    R_CHORD, T_TICKS, X_SHARED, gen_traj, rank_uniform, shift_modules,
)

SEEDS = [3, 4, 5, 6, 7, 8, 9, 10, 11]


def phi_of(seed: int, mode: int, clean: bool) -> float:
    if mode == BPERM:
        traj = shift_modules(gen_traj(seed, B_MULTI))
    elif mode == APERM:
        traj = shift_modules(gen_traj(seed, A_DIRECT))
    else:
        traj = gen_traj(seed, mode)
    if clean:
        traj = rank_uniform(traj)
    return faithful_phi(traj.reshape(-1), N_MOD, T_TICKS, NBINS)


def parse_anchor(path: str) -> dict:
    """Pull every printed Phi out of the hexa probe's stdout."""
    txt = open(path).read()
    out: dict[tuple[int, str, bool], float] = {}
    seed = None
    for line in txt.splitlines():
        m = re.match(r"seed (\d+) \| OLD A=([\d.eE+-]+) dsh=([\d.eE+-]+)", line)
        if m:
            seed = int(m.group(1))
            out[(seed, "A", False)] = float(m.group(2))
            out[(seed, "denseShuf", False)] = float(m.group(3))
            continue
        m = re.match(r"\s+\| NEW A=([\d.eE+-]+) dsh=([\d.eE+-]+)", line)
        if m and seed is not None:
            out[(seed, "A", True)] = float(m.group(1))
            out[(seed, "denseShuf", True)] = float(m.group(2))
            continue
        if seed is not None and line.strip().startswith("| B="):
            for k, v in re.findall(r"(\w+)=([\d.eE+-]+)", line):
                out[(seed, k, True)] = float(v)
    return out


def main() -> int:
    anchor = parse_anchor(sys.argv[1])
    modes = {
        "A": A_DIRECT, "B": B_MULTI, "X": X_SHARED, "N": N_SELF, "R": R_CHORD,
        "Bperm": BPERM, "Aperm": APERM, "Cperm": CPERM, "denseShuf": DENSE_SHUF,
    }

    worst = 0.0
    worst_at = None
    n_cmp = 0
    for seed in SEEDS:
        for name, mode in modes.items():
            for clean in (False, True):
                key = (seed, name, clean)
                if key not in anchor:
                    continue
                got = phi_of(seed, mode, clean)
                d = abs(got - anchor[key])
                n_cmp += 1
                if d > worst:
                    worst, worst_at = d, (seed, name, "RU" if clean else "raw", anchor[key], got)
                print(f"seed {seed:2d} {name:9s} {'RU ' if clean else 'raw'} "
                      f"hexa={anchor[key]:.15f} py={got:.15f} |d|={d:.3e}")

    print()
    print(f"compared {n_cmp} Phi values (hexa engine anchor vs py port)")
    print(f"max|delta| = {worst:.6e}  at {worst_at}")
    ok = worst < 1e-12
    print(f"PARITY: {'PASS — py port is the hexa estimator' if ok else 'FAIL — DO NOT PROCEED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
