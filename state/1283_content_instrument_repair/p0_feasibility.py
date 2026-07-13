"""P0' — FEASIBILITY GATE (run BEFORE the 9-seed campaign; design: Fable 5, §2).

Question it settles: is the FROZEN +0.02 bar commensurable with this axis's Phi dynamic range
at all? The bar was inherited from the TIMING axis (H_1448). If the CONTENT axis's population
Phi is two orders of magnitude below it, then every content verdict ever cemented — R6's green
AND the axis's wall — was reading instrument noise, and no amount of averaging can rescue it.

Method: run each arm at T_LONG = 65536 (vs the frozen T=64). At ~1024 samples per joint cell the
plugin bias is ~6e-4 bits, so Phi(T_LONG) ~ the POPULATION Phi — the effect size the campaign
would be chasing. Nothing here is tuned: same substrate, same hypers, same mandated estimator,
same rank-uniform read-out. Only the tick count grows.

    P0'-a   Phi_pop(B)                >= 0.02
    P0'-b   Phi_pop(B) - Phi_pop(A)    >= 0.02
    P0'-c   Phi_pop(B) - Phi_pop(N)    >= 0.02
    P0'-d   Phi_pop(B) - Phi_pop(X)    >= 0.02      <- the axis claim's own population effect

Any leg FAIL => the campaign is NOT fired; tier = PENDING BAR-ABOVE-SIGNAL (not a wall — the axis
is still-unmeasured, and the honest statement is that the bar sits above the signal).

ADJUNCT LENS (reported, never a gate): the same pipeline on traj_sgn[i, t] = s_i(t)[0], the signed
component. This does not produce a verdict; it only separates "substrate ceiling" from
"the ||s||^2 salience map threw the sign channel away" (the decision table's demotion rule).
"""

from __future__ import annotations

import json
import sys

import numpy as np

from faithful_phi import build_mi_matrix, faithful_phi_from_mi
from substrate import (
    A_DIRECT, B_MULTI, CPERM, DIM, GAIN, LEAK, NBINS, N_EDGE, N_MOD, N_SELF, R_CHORD,
    W_IN, W_NBR, W_RELAY, X_SHARED, Lcg, rank_uniform, seed_state,
)

T_LONG = 65536
BAR = 0.02
SEED = 3  # linear-gaussian stationary system: one seed suffices for the population value

ARMS = [("A", A_DIRECT), ("B", B_MULTI), ("X", X_SHARED), ("N", N_SELF),
        ("R", R_CHORD), ("Cperm", CPERM)]


def gen_traj_long(seed: int, mode: int, t_ticks: int, signed: bool):
    """Same recurrence as substrate.gen_traj, but streams inputs tick-by-tick so T=65536 fits.

    The RNG draw order differs from the T=64 probe (inputs are drawn per tick rather than as one
    up-front block), so these long runs are NOT byte-comparable to the frozen T=64 arms — they are
    a population-scale estimate of the SAME stationary process, which is all P0' claims.
    """
    rng = Lcg(seed_state(seed))
    states = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.5
    chans = rng.gauss_arr(N_EDGE * DIM).reshape(N_EDGE, DIM) * 0.5

    elo, ehi = [0, 1, 2, 3], [1, 2, 3, 0]
    if mode == CPERM:
        elo, ehi = [3, 0, 1, 2], [0, 1, 2, 3]
    if mode == R_CHORD:
        elo, ehi = [0, 1, 0, 1], [2, 3, 2, 3]
    channel_arm = mode in (B_MULTI, X_SHARED, R_CHORD, CPERM)
    incident = [[e for e in range(N_EDGE) if elo[e] == i or ehi[e] == i] for i in range(N_MOD)]

    traj = np.zeros((N_MOD, t_ticks), dtype=np.float64)
    for tt in range(t_ticks):
        inp = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.8
        new_states = np.empty_like(states)
        for i in range(N_MOD):
            nbr = (states[(i + N_MOD - 1) % N_MOD] + states[(i + 1) % N_MOD]) / 2.0
            v = LEAK * states[i] + GAIN * (W_NBR * nbr + W_IN * inp[i])
            if mode != A_DIRECT:
                rin = chans[incident[i]].mean(axis=0) if channel_arm else chans[i]
                v = v + GAIN * (W_RELAY * rin)
            new_states[i] = v

        if channel_arm:
            cmean = chans.mean(axis=0)
            new_ch = np.empty_like(chans)
            for e in range(N_EDGE):
                pair = 0.5 * (states[elo[e]] + states[ehi[e]])
                drive = 0.5 * pair + 0.5 * cmean if mode == X_SHARED else pair
                new_ch[e] = LEAK * chans[e] + GAIN * (W_NBR * drive)
            chans = new_ch
        elif mode == N_SELF:
            chans = LEAK * chans + GAIN * (W_NBR * states)

        states = new_states
        traj[:, tt] = states[:, 0] if signed else np.sum(states * states, axis=1)
    return traj


def phi_pop(seed: int, mode: int, signed: bool):
    traj = rank_uniform(gen_traj_long(seed, mode, T_LONG, signed))
    flat = traj.reshape(-1)
    mi = build_mi_matrix(flat, N_MOD, T_LONG, NBINS)
    return faithful_phi_from_mi(mi, N_MOD), mi


def mi_shape(mi: np.ndarray) -> dict:
    adj = [(0, 1), (1, 2), (2, 3), (3, 0)]
    diag = [(0, 2), (1, 3)]
    c_adj = float(np.mean([mi[i, j] for i, j in adj]))
    c_diag = float(np.mean([mi[i, j] for i, j in diag]))
    return {"c_adj": c_adj, "c_diag": c_diag, "aniso": c_adj - c_diag}


def main() -> int:
    out = {"T_LONG": T_LONG, "seed": SEED, "bar": BAR, "energy": {}, "signed": {}}
    for lens, signed in (("energy", False), ("signed", True)):
        print(f"── lens = {lens}  (traj = {'s_i(t)[0]' if signed else '||s_i(t)||^2'}) "
              f"· T={T_LONG} · faithful IIT4 exact MIP-EI")
        for name, mode in ARMS:
            phi, mi = phi_pop(SEED, mode, signed)
            sh = mi_shape(mi)
            out[lens][name] = {"phi_pop": phi, **sh}
            print(f"   {name:6s} Phi_pop={phi:.6f}   c_adj={sh['c_adj']:.6f} "
                  f"c_diag={sh['c_diag']:.6f} aniso={sh['aniso']:+.6f}")
        print()

    e = out["energy"]
    legs = {
        "P0'-a  Phi_pop(B)      >= 0.02": e["B"]["phi_pop"],
        "P0'-b  Phi_pop(B) - A  >= 0.02": e["B"]["phi_pop"] - e["A"]["phi_pop"],
        "P0'-c  Phi_pop(B) - N  >= 0.02": e["B"]["phi_pop"] - e["N"]["phi_pop"],
        "P0'-d  Phi_pop(B) - X  >= 0.02": e["B"]["phi_pop"] - e["X"]["phi_pop"],
    }
    all_pass = True
    print("P0' gate (pre-registered, 4-leg conjunctive · FROZEN bar +0.02):")
    for label, val in legs.items():
        ok = val >= BAR
        all_pass &= ok
        print(f"   {label}   measured {val:+.6f}   {'PASS' if ok else 'FAIL'}")
    out["legs"] = {k: v for k, v in legs.items()}
    out["p0_pass"] = bool(all_pass)

    s = out["signed"]
    out["signed_lens"] = {
        "B": s["B"]["phi_pop"],
        "B_minus_A": s["B"]["phi_pop"] - s["A"]["phi_pop"],
    }
    print()
    print("ADJUNCT signed lens (NOT a gate — decides 🧱 vs ⏳ READOUT-LIMITED):")
    print(f"   Phi_pop_sgn(B)          = {out['signed_lens']['B']:+.6f}")
    print(f"   Phi_pop_sgn(B) - sgn(A) = {out['signed_lens']['B_minus_A']:+.6f}")
    print()
    if all_pass:
        print("VERDICT: P0' PASS — signal is commensurable with the bar. FIRE the 9-seed campaign.")
    else:
        print("VERDICT: ⏳ BAR-ABOVE-SIGNAL — campaign NOT fired. The frozen +0.02 bar sits above "
              "this axis's Phi dynamic range under the ||s||^2 read-out; every content-axis tier "
              "ever cemented on it (R6's 🟢 AND the 🧱) was reading instrument noise.")

    json.dump(out, open("p0_feasibility.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
