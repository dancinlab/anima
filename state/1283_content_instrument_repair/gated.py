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
# MODE-SWAP positive control (P±) — mode powers, and why they must be calibrated NUMERICALLY.
#
# The construction swaps the steady-state POWER of the ring's uniform mode φ₀ and alternating mode
# φ₂, which leaves Var and cov_diag identically unchanged while flipping cov_adj's sign at equal
# magnitude. But the realised power in each mode is  p_k = (noise floor)_k + (driven)_k , and the
# NOISE FLOOR IS NOT SWAPPABLE: every module's private input injects equal power into all modes,
# and the substrate's own gain (1 − λ_k²)⁻¹ then amplifies φ₀'s share more than φ₂'s. A closed-form
# amplitude therefore lands the DRIVEN power correctly and the TOTAL power wrong — which is exactly
# what the first mode-swap attempt measured (adjacent ρ nearly matched, diagonal ρ off by 0.08).
#
# So the driven amplitudes are solved NUMERICALLY against the measured floor: run arm A (no control
# drive), read its realised mode powers, and pick a_k so that floor_k + driven_k hits the target.
# Calibration reads arm A ONLY — never a contrast — and V-LINEAR then MEASURES whether the
# construction actually delivered an elementwise |ρ|-identical pair. It is never assumed.
_LAM = {0: LEAK + 2.0 * GAIN * W_NBR, 2: LEAK - 2.0 * GAIN * W_NBR, 1: LEAK, 3: LEAK}
_P_HI, _P_LO, _P_Q = 2.40, 0.60, 0.45          # target TOTAL mode powers (P, Q, q) — frozen


def _mode_basis() -> np.ndarray:
    """The 4-ring's Fourier modes: uniform φ₀, quadrature φ₁/φ₃, alternating φ₂."""
    r2 = np.sqrt(2.0)
    return np.array([
        [0.5, 0.5, 0.5, 0.5],                       # φ₀ uniform      (λ₀ = LEAK + 2·GAIN·W_NBR)
        [1 / r2, 0.0, -1 / r2, 0.0],                # φ₁ quadrature   (λ₁ = LEAK)
        [0.5, -0.5, 0.5, -0.5],                     # φ₂ alternating  (λ₂ = LEAK − 2·GAIN·W_NBR)
        [0.0, 1 / r2, 0.0, -1 / r2],                # φ₃ quadrature   (λ₃ = LEAK)
    ])


_MODE_AMP: dict[float, float] = {}


def _calibrate_mode_amps(seeds: list[int], t_ticks: int = 8192) -> None:
    """Solve the driven amplitudes against the MEASURED noise floor (arm A only)."""
    if _MODE_AMP:
        return
    # Calibrate on the arm the control actually RUNS on (B, linear) — not on A. The relay channels
    # integrate pair means, which is a mode-0-heavy operation, so they give φ₀ extra gain on top of
    # the bare ring's. Calibrating against the bare ring leaves that unabsorbed and the swap comes
    # out lopsided (measured: adjacent ρ +0.49 / −0.44, diagonal 0.56 / 0.54 — V-LINEAR FAIL).
    # This still reads ONE arm, never a contrast.
    phi = _mode_basis()
    floor = np.zeros(4)
    for s in seeds:
        tr = gen(s, B_MULTI, t_ticks, gated=False)
        floor += np.array([np.var(phi[k] @ tr) for k in range(4)])
    floor /= len(seeds)
    # power is quadratic in the injected amplitude, so one probe run fixes the constant
    probe = 1.0
    gains = np.zeros(4)
    for k in (0, 2, 1, 3):
        acc = 0.0
        for s in seeds:
            tr = gen(s, B_MULTI, t_ticks, gated=False, probe_mode=k, probe_amp=probe)
            acc += np.var(phi[k] @ tr)
        gains[k] = (acc / len(seeds) - floor[k]) / probe ** 2
    for target in (_P_HI, _P_LO, _P_Q):
        for k in range(4):
            need = max(target - floor[k], 0.0)
            _MODE_AMP[(target, k)] = float(np.sqrt(need / gains[k])) if gains[k] > 0 else 0.0


def _edges(mode: int) -> tuple[list[int], list[int]]:
    if mode == CPERM:
        return [3, 0, 1, 2], [0, 1, 2, 3]
    if mode == R_CHORD:
        return [0, 1, 0, 1], [2, 3, 2, 3]
    return [0, 1, 2, 3], [1, 2, 3, 0]


def gen(seed: int, mode: int, t_ticks: int, *, gated: bool, beta: float = 0.0,
        mu: np.ndarray | None = None, sd: np.ndarray | None = None,
        w_relay: float = W_RELAY, gate_shuffle: bool = False,
        gate_override: np.ndarray | None = None, record_gate: bool = False,
        probe_mode: int | None = None, probe_amp: float = 0.0):
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
    gate_log = np.zeros((N_EDGE, t_ticks), dtype=np.float64) if record_gate else None

    for tt in range(t_ticks):
        inp = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.8
        if probe_mode is not None:
            # calibration probe: inject a known amplitude into ONE mode, so `_calibrate_mode_amps`
            # can read off that mode's realised gain. Arm A only; never used in a contrast.
            inp = inp + probe_amp * _mode_basis()[probe_mode][:, None] * rng.gauss_arr(DIM)[None, :]
        if pctl:
            # MODE-SWAP. A per-module SIGN pattern cannot work here (it was tried, and V-LINEAR
            # killed it): the 4-ring is circulant, so it diagonalises in the module Fourier basis
            # and the recurrence amplifies the uniform mode more than the alternating one
            # (λ₀ = LEAK + 2·GAIN·W_NBR  vs  λ₂ = LEAK − 2·GAIN·W_NBR). Driving φ₀ in one arm and
            # φ₂ in the other therefore moves coupling STRENGTH, not just its sign.
            #
            # The fix is a POWER SWAP: drive BOTH modes in BOTH arms and exchange their powers.
            #     P+ : (p₀, p₂) = (P, Q)      P− : (p₀, p₂) = (Q, P)      with P > Q, same q
            # Steady-state covariance depends only on mode powers:
            #     Var = (p₀+p₂)/4 + q/2      cov_adj = (p₀−p₂)/4      cov_diag = (p₀+p₂)/4 − q/2
            # The swap preserves p₀+p₂, so Var and cov_diag are IDENTICALLY unchanged while cov_adj
            # keeps its magnitude and flips sign — an elementwise |ρ|-identical MI matrix by
            # construction, which the sign-pattern family could not deliver.
            #
            # The gate reads coincidence on RING EDGES, whose sign follows cov_adj, so it opens in
            # P+ and closes in P−; the estimator (MI is even in ρ) cannot tell them apart. That
            # asymmetry is the whole point — and V-LINEAR is the standing measurement of it.
            phi = _mode_basis()
            t0, t2 = (_P_HI, _P_LO) if mode == P_PLUS else (_P_LO, _P_HI)
            for k, tgt in ((0, t0), (2, t2), (1, _P_Q), (3, _P_Q)):
                inp = inp + _MODE_AMP[(tgt, k)] * phi[k][:, None] * rng.gauss_arr(DIM)[None, :]

        # gate per channel from the PREVIOUS tick's standardised lens scalars (delay 1)
        if gated and channel_arm:
            coin = np.array([zprev[elo[e]] * zprev[ehi[e]] for e in range(N_EDGE)])
            gate = 1.0 / (1.0 + np.exp(-beta * coin))
            if gate_shuffle:
                # L-SHIFT control — the liveness proof that survives P±'s troubles.
                #
                # Take the gate this arm WOULD have applied and delay it by a large circular shift:
                # gate_e(t) → gate_e((t + τ) mod T), τ drawn once per (seed, edge) from the middle
                # half of the record. The gate's marginal AND its autocorrelation are preserved
                # exactly — it is the same time series — but its ALIGNMENT with c_e(t) is destroyed.
                # A gate that is merely a fluctuating GAIN is unaffected by this. A gate that is
                # genuinely CONDITIONAL on the coincidence it is meant to detect is.
                #
                # Why not the obvious β=0 ablation: β=0 collapses the gate to the constant 0.5 — a
                # half-gain LINEAR relay — so it removes the conditionality AND the gain fluctuation
                # at once, and a positive result would only prove "a fluctuating multiplicative gain
                # does something". That cannot carry the liveness claim.
                gate = gate_override[:, tt]
        else:
            gate = np.ones(N_EDGE, dtype=np.float64)
        if gate_log is not None:
            gate_log[:, tt] = gate

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

    return (traj, gate_log) if record_gate else traj


def l_shift_pair(seed: int, mode: int, t_ticks: int, beta: float, mu: np.ndarray,
                 sd: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(gated trajectory, L-SHIFT surrogate trajectory) — the liveness contrast, two passes.

    Pass 1 records the gate this arm actually applied. Pass 2 re-runs the SAME substrate driving it
    with that gate circularly shifted by a large per-edge lag τ. The gate's marginal and its whole
    autocorrelation structure are preserved — it is literally the same series — while its alignment
    with c_e(t) is destroyed. A gate that is only a fluctuating gain is untouched by this; a gate
    that is genuinely conditional on the coincidence it detects is not.
    """
    traj, gate_log = gen(seed, mode, t_ticks, gated=True, beta=beta, mu=mu, sd=sd, record_gate=True)
    rng = np.random.Generator(np.random.Philox(key=0x51F7_0000 + seed))
    taus = rng.integers(t_ticks // 4, 3 * t_ticks // 4, size=N_EDGE)
    shifted = np.stack([np.roll(gate_log[e], int(taus[e])) for e in range(N_EDGE)])
    sur = gen(seed, mode, t_ticks, gated=True, beta=beta, mu=mu, sd=sd, gate_shuffle=True,
              gate_override=shifted)
    return traj, sur


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
