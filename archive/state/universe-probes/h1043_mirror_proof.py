#!/usr/bin/env python3
"""H_1043 mirror proof — RE-PROVE the python faithful_phi_prescreen MIRROR ≡ the
stdlib exact MIP-EI engine (iit4_faithful_phi) at n=4 and n=5 on fixed binary
state matrices (a_phi_iit4_tool — the python φ is a labelled PRE-SCREEN only; this
proves it tracks the terminal engine bit-for-bit at the verdict's working n).

Writes the fixed n=4,5 binary states to a file (format consumed by
run_faithful_phi_1043.hexa) AND prints the python mirror φ for each, so the
companion hexa run over the SAME file can be diffed line-for-line.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h1043_minimal_arch_adapter import faithful_phi_prescreen, write_state_file

# fixed, reproducible binary n×dim state matrices (dim = 12 steps).
DIM = 12

def fixed_states():
    rng = np.random.default_rng(20260609)
    out = {}
    for n in (4, 5):
        # build correlated binary rows so φ is non-trivial (some shared structure,
        # one independent row) — exercises a real MIP, not a degenerate all-zeros.
        base = (rng.random(DIM) > 0.5).astype(float)
        rows = []
        for i in range(n):
            if i == 0:
                rows.append(base.copy())
            elif i < n - 1:
                # partially coupled to row 0 (flip ~25%)
                r = base.copy()
                flip = rng.random(DIM) < 0.25
                r[flip] = 1.0 - r[flip]
                rows.append(r)
            else:
                # one fully-independent row (the natural MIP cut)
                rows.append((rng.random(DIM) > 0.5).astype(float))
        out[n] = [list(r) for r in rows]
    return out


def main():
    path = os.environ.get("H1043_MIRROR_STATE", "/tmp/h1043_mirror_states.txt")
    if os.path.exists(path):
        os.remove(path)
    states = fixed_states()
    print("=== H_1043 mirror proof — python faithful_phi_prescreen (MIRROR) ===")
    print(f"state file -> {path}  (feed to run_faithful_phi_1043 via H1043_STATE)")
    for n in (4, 5):
        st = states[n]
        phi = faithful_phi_prescreen(st, n, 2)
        write_state_file(path, f"mirror_n{n}", st)
        print(f"  [mirror_n{n}]  n={n} dim={DIM}  python_mirror_phi_EI={phi:.6f}")
    print("now run: H1043_STATE=%s hexa run UNIVERSE/run_faithful_phi_1043.hexa" % path)
    print("PASS = stdlib terminal φ_EI == python mirror φ_EI (per n) to 6 dp.")


if __name__ == "__main__":
    main()
