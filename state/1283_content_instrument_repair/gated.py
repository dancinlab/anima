"""The GATED substrate — one change to the linear one: relay feedback becomes CONDITIONAL.

H_9294 closed the content axis on the LINEAR substrate: match the coupling strength and
disjointness contributes exactly 0. But in a jointly-gaussian system every pairwise dependence
collapses to one correlation, so the MI matrix is a sufficient statistic and structure has no
room to contribute independently — the closure may be a property of linearity, not of Φ.

The one axis of H_1283 that ever broke cleanly (H_1448 🟢 WIRED) was TIMING: Kuramoto phase
synchrony with phase-GATED salience — a multiplicative, nonlinear mechanism. So the real axis may
be "linear vs gated coupling", and this module builds the minimal honest test of that.

    coincidence_e(t) = ẑ_a(t−1) · ẑ_b(t−1)          ẑ = lens scalar standardised on arm A ALONE
    gate_e(t)        = sigmoid(β · coincidence_e(t))
    rin_i(t)         = Σ_{e ∋ i} gate_e(t) · c_e(t)   (was: Σ_{e ∋ i} c_e(t))

Everything else is frozen: n=4, dim=8, LEAK/GAIN/W_*, the channel integration, T, the estimator,
Φ*, the seeds. Channel dimension and capacity do not move — only the coupling OPERATOR does,
from additive to conditional. The t−1 delay is deliberate: feeding ẑ_a·ẑ_b back into a and b at
the SAME tick would manufacture a genuine a–b dependence out of arithmetic, which is an artifact,
not integration. V-ZERO is the standing guard for exactly that.

β IS NOT A KNOB: it is pinned on arm A alone, before any contrast is looked at, so that the gate's
operating point sits at the centre of its dynamic range (E[coincidence] ≈ 0 ⇒ σ(0) = 0.5). A larger
β saturates it into a hard AND (gradient dies); a smaller one flattens it to gate ≡ 0.5, which is
just a half-gain LINEAR relay. Neither is the mechanism under test.
"""

from __future__ import annotations

import numpy as np

from substrate import (
    A_DIRECT, B_MULTI, CPERM, DIM, GAIN, LEAK, N_EDGE, N_MOD, N_SELF, R_CHORD,
    W_IN, W_NBR, W_RELAY, X_SHARED, Lcg, seed_state,
)

P_PLUS, P_MINUS = 10, 11          # positive-control arms (co-active / anti-active endpoints)
GATE_C = 1.0                      # β = GATE_C / std_A(coincidence) — frozen before any contrast

# P−'s shared-latent amplitude, grid-matched so |ρ_adj(P−)| = |ρ_adj(P+)| within 0.6% on the
# LINEAR substrate (see `gen`). Chosen on ρ ALONE — Φ was never consulted — and it makes the
# control arm stronger, i.e. it tunes against the liveness claim. V-LINEAR verifies the match by
# checking that the two arms are then indistinguishable to the estimator, exactly as gaussian
# MI's evenness in ρ demands.
PCTL_AMP_MINUS = 1.30


def _edges(mode: int) -> tuple[list[int], list[int]]:
    if mode == CPERM:
        return [3, 0, 1, 2], [0, 1, 2, 3]
    if mode == R_CHORD:
        return [0, 1, 0, 1], [2, 3, 2, 3]
    return [0, 1, 2, 3], [1, 2, 3, 0]


def gen(seed: int, mode: int, t_ticks: int, *, gated: bool, beta: float = 0.0,
        mu: np.ndarray | None = None, sd: np.ndarray | None = None,
        w_relay: float = W_RELAY, pctl_amp: float | None = None) -> np.ndarray:
    """Signed-lens trajectory. `gated=False` reproduces the linear substrate exactly.

    P_PLUS / P_MINUS drive the two endpoints of every channel from a SHARED input component with
    the same magnitude and opposite sign — identical coupling strength, opposite co-activation.
    Gaussian MI is an EVEN function of ρ, so on the linear substrate these two arms are provably
    indistinguishable (V-LINEAR checks that). The gate reacts to the SIGN of the coincidence, so
    they can only separate once the gate is live — which is what makes them a liveness control.
    """
    rng = Lcg(seed_state(seed))
    states = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.5
    chans = rng.gauss_arr(N_EDGE * DIM).reshape(N_EDGE, DIM) * 0.5

    pctl = mode in (P_PLUS, P_MINUS)
    base_mode = B_MULTI if pctl else mode
    elo, ehi = _edges(base_mode)
    channel_arm = base_mode in (B_MULTI, X_SHARED, R_CHORD, CPERM)
    inc = [[e for e in range(N_EDGE) if elo[e] == i or ehi[e] == i] for i in range(N_MOD)]

    traj = np.zeros((N_MOD, t_ticks), dtype=np.float64)
    zprev = np.zeros(N_MOD, dtype=np.float64)

    for tt in range(t_ticks):
        inp = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.8
        if pctl:
            # ONE shared latent driving every module, with a per-module sign pattern.
            #   P+ : all +1            → every ring pair is co-active   (ρ_adj > 0)
            #   P− : alternating ±1    → every ring pair is anti-active (ρ_adj < 0)
            # The alternating pattern needs an EVEN ring (n=4) so adjacent modules always carry
            # opposite signs.
            #
            # `pctl_amp` exists because the substrate is NOT neutral to the sign: the ring's own
            # W_NBR term pulls neighbours together, so an anti-aligned latent FIGHTS it and lands
            # a weaker |ρ| than the aligned one at equal amplitude. A raw sign flip would therefore
            # change coupling STRENGTH as well as sign, and the whole point of P± is that only the
            # sign moves (gaussian MI is even in ρ, so a pure sign flip is provably invisible to
            # the estimator and visible only to the gate). So P−'s amplitude is raised until
            # |ρ_adj| matches P+'s — chosen on ρ ALONE, never on Φ, and it strengthens the control
            # arm, i.e. it tunes AGAINST the liveness claim. V-LINEAR is the check that this
            # matching actually worked.
            shared = rng.gauss_arr(DIM) * 0.8
            amp = 0.7 if mode == P_PLUS else (PCTL_AMP_MINUS if pctl_amp is None else pctl_amp)
            for i in range(N_MOD):
                sgn = 1.0 if (mode == P_PLUS or i % 2 == 0) else -1.0
                inp[i] = inp[i] + amp * sgn * shared

        # gate per channel from the PREVIOUS tick's standardised lens scalars (delay 1)
        if gated and channel_arm:
            coin = np.array([zprev[elo[e]] * zprev[ehi[e]] for e in range(N_EDGE)])
            gate = 1.0 / (1.0 + np.exp(-beta * coin))
        else:
            gate = np.ones(N_EDGE, dtype=np.float64)

        new = np.empty_like(states)
        for i in range(N_MOD):
            nbr = (states[(i + N_MOD - 1) % N_MOD] + states[(i + 1) % N_MOD]) / 2.0
            v = LEAK * states[i] + GAIN * (W_NBR * nbr + W_IN * inp[i])
            if base_mode != A_DIRECT:
                if channel_arm:
                    rin = np.mean([gate[e] * chans[e] for e in inc[i]], axis=0)
                else:                       # N_SELF: one channel per module, no spanning
                    rin = chans[i]
                v = v + GAIN * (w_relay * rin)
            new[i] = v

        if channel_arm:
            cmean = chans.mean(axis=0)
            nc = np.empty_like(chans)
            for e in range(N_EDGE):
                pair = 0.5 * (states[elo[e]] + states[ehi[e]])
                drive = 0.5 * pair + 0.5 * cmean if base_mode == X_SHARED else pair
                nc[e] = LEAK * chans[e] + GAIN * (W_NBR * drive)
            chans = nc
        elif base_mode == N_SELF:
            chans = LEAK * chans + GAIN * (W_NBR * states)

        states = new
        traj[:, tt] = states[:, 0]
        if mu is not None and sd is not None:
            zprev = (traj[:, tt] - mu) / sd

    return traj


def calibrate_beta(seeds: list[int], t_ticks: int) -> tuple[float, np.ndarray, np.ndarray]:
    """Pin β on arm A ALONE — never on a contrast. Returns (β, μ_A, σ_A).

    β = GATE_C / std(coincidence) puts the gate's operating point at the centre of its dynamic
    range: E[coincidence] ≈ 0 (centred product) ⇒ sigmoid(0) = 0.5, and a ±1σ swing moves it to
    [0.27, 0.73] — responsive, neither saturated nor inert.
    """
    trajs = [gen(s, A_DIRECT, t_ticks, gated=False) for s in seeds]
    allt = np.concatenate(trajs, axis=1)
    mu, sd = allt.mean(axis=1), allt.std(axis=1)
    elo, ehi = _edges(B_MULTI)
    coins = []
    for tr in trajs:
        z = (tr - mu[:, None]) / sd[:, None]
        for e in range(N_EDGE):
            coins.append(z[elo[e], :-1] * z[ehi[e], :-1])
    std_coin = float(np.concatenate(coins).std())
    return GATE_C / std_coin, mu, sd
