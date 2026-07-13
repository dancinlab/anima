"""Thalamic content-relay substrate — byte-faithful Python port of the H_9260 probe.

Reference (`reference-match`): `state/1283_r6_content_relay_clean/
h9260_content_relay_clean_probe.hexa` (engine LCG `_lcg_*` == `core/engine_cli.hexa`).

FROZEN, may not move (FREEZE.txt of H_9260, inherited verbatim):
    n_mod=4  dim=8  T=64  GAIN=0.30  LEAK=0.55  W_NBR=0.5  W_IN=0.5  W_RELAY=0.5  NBINS=8
    traj[i, t] = ||s_i(t)||^2         seeds [3..11]        bar = dPhi >= +0.02

The RNG draw order (states -> inputs -> channels -> relay) is fixed and arm-independent, so
arm A depends only on draws 1-2 and is byte-identical across every arm.
"""

from __future__ import annotations

import numpy as np

N_MOD = 4
N_EDGE = 4
DIM = 8
T_TICKS = 64
GAIN = 0.30
LEAK = 0.55
W_NBR = 0.5
W_IN = 0.5
W_RELAY = 0.5
NBINS = 8

# arm codes (identical to the hexa probe's `mode`)
A_DIRECT, B_MULTI, X_SHARED, N_SELF, R_CHORD = 0, 1, 2, 3, 4
BPERM, APERM, CPERM, DENSE, DENSE_SHUF = 5, 6, 7, 8, 9

ARM_NAME = {
    A_DIRECT: "A", B_MULTI: "B", X_SHARED: "X", N_SELF: "N", R_CHORD: "R",
    BPERM: "Bperm", APERM: "Aperm", CPERM: "Cperm", DENSE: "dense", DENSE_SHUF: "denseShuf",
}

_MASK = 2147483647


def lcg_next(state: int) -> int:
    return (state * 1103515245 + 12345) & _MASK


class Lcg:
    """The engine's deterministic LCG-gauss stream (Box-Muller, cos branch)."""

    __slots__ = ("st",)

    def __init__(self, st: int):
        self.st = st if st != 0 else 12345

    def gauss(self) -> float:
        s1 = lcg_next(self.st)
        s2 = lcg_next(s1)
        u1 = s1 / 2147483648.0
        u2 = s2 / 2147483648.0
        if u1 < 0.0000001:
            u1 = 0.0000001
        self.st = s2
        return np.sqrt(-2.0 * np.log(u1)) * np.cos(6.283185307179586 * u2)

    def gauss_arr(self, k: int) -> np.ndarray:
        return np.fromiter((self.gauss() for _ in range(k)), dtype=np.float64, count=k)


def seed_state(seed: int) -> int:
    """H_9260's per-seed root state (the r=0 realization)."""
    st = (seed * 2654435761) & _MASK
    return st if st != 0 else 12345


def gen_traj(seed: int, mode: int, t_ticks: int = T_TICKS) -> np.ndarray:
    """Per-module salience trajectory traj[i, t] = ||s_i(t)||^2, shape (N_MOD, t_ticks)."""
    rng = Lcg(seed_state(seed))

    states = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.5
    inputs = rng.gauss_arr(N_MOD * t_ticks * DIM).reshape(N_MOD, t_ticks, DIM) * 0.8
    chans = rng.gauss_arr(N_EDGE * DIM).reshape(N_EDGE, DIM) * 0.5
    relay = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.5

    # ring edges (0,1)(1,2)(2,3)(3,0) · Cperm = cyclic relabel · R = chords
    elo, ehi = [0, 1, 2, 3], [1, 2, 3, 0]
    if mode == CPERM:
        elo, ehi = [3, 0, 1, 2], [0, 1, 2, 3]
    if mode == R_CHORD:
        elo, ehi = [0, 1, 0, 1], [2, 3, 2, 3]

    channel_arm = mode in (B_MULTI, X_SHARED, R_CHORD, CPERM)
    incident = [[e for e in range(N_EDGE) if elo[e] == i or ehi[e] == i] for i in range(N_MOD)]

    traj = np.zeros((N_MOD, t_ticks), dtype=np.float64)

    for tt in range(t_ticks):
        # ── cortex stage — uses PRE-update channel/relay values ──
        new_states = np.empty_like(states)
        for i in range(N_MOD):
            left = states[(i + N_MOD - 1) % N_MOD]
            right = states[(i + 1) % N_MOD]
            nbr = (left + right) / 2.0
            v = LEAK * states[i] + GAIN * (W_NBR * nbr + W_IN * inputs[i, tt])
            if mode != A_DIRECT:
                if channel_arm:
                    rin = chans[incident[i]].mean(axis=0) if incident[i] else np.zeros(DIM)
                elif mode == N_SELF:
                    rin = chans[i]
                elif mode in (DENSE, DENSE_SHUF):
                    rin = relay[i]
                else:  # Bperm/Aperm are post-hoc shifts of B/A, never generated here
                    raise ValueError(f"gen_traj: mode {mode} is not a generative arm")
                v = v + GAIN * (W_RELAY * rin)
            new_states[i] = v

        # ── thalamus stage — integrates PRE-update module states (one-tick delay) ──
        if channel_arm:
            cmean = chans.mean(axis=0)
            new_ch = np.empty_like(chans)
            for e in range(N_EDGE):
                pair = 0.5 * (states[elo[e]] + states[ehi[e]])
                # B/R/Cperm: DISJOINT — channel e sees only its own pair.
                # X: same total capacity (4x8) and same gain, but half the drive is the
                #    mean over ALL channels → disjointness destroyed, spanning+capacity kept.
                drive = 0.5 * pair + 0.5 * cmean if mode == X_SHARED else pair
                new_ch[e] = LEAK * chans[e] + GAIN * (W_NBR * drive)
            chans = new_ch
        elif mode == N_SELF:
            # each channel integrates ONE module (no spanning); same count/leak/gain
            chans = LEAK * chans + GAIN * (W_NBR * states)
        elif mode in (DENSE, DENSE_SHUF):
            new_rl = np.empty_like(relay)
            for i in range(N_MOD):
                src = (i + N_MOD - 1) % N_MOD if mode == DENSE_SHUF else i
                others = np.stack([relay[j] for j in range(N_MOD) if j != src]).mean(axis=0)
                new_rl[i] = LEAK * relay[i] + GAIN * (W_NBR * states[i] + W_RELAY * others)
            relay = new_rl

        states = new_states
        traj[:, tt] = np.sum(states * states, axis=1)

    return traj


def rank_uniform(traj: np.ndarray) -> np.ndarray:
    """H_1328 variance-clean read-out: per-row rank over t, ties broken by index.

    Mirrors the reference's O(T^2) count ("strictly less, plus equal-and-earlier"), which is
    exactly `argsort(kind='stable')` inverted — every row becomes the multiset {0..T-1}.
    """
    order = np.argsort(traj, axis=1, kind="stable")
    out = np.empty_like(traj)
    rows = np.arange(traj.shape[0])[:, None]
    out[rows, order] = np.arange(traj.shape[1], dtype=np.float64)[None, :]
    return out


def shift_modules(traj: np.ndarray) -> np.ndarray:
    """Per-module circular time-shift (i*17 mod T) — marginals byte-identical."""
    t = traj.shape[1]
    return np.stack([np.roll(traj[i], -((i * 17) % t)) for i in range(traj.shape[0])])
