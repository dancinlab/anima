#!/usr/bin/env python3
"""kuramoto_local_sim.py — Mac local Kuramoto N-oscillator sim.

Pure numpy reference for the neuromorphic adapters (Loihi 2 / Akida) in
this directory.  Mirrors `social/kuramoto_coupling.hexa::simulate_network`
dynamics:

    dθ_i/dt = ω_i + (K/N) · Σ_{j≠i} sin(θ_j − θ_i)

with:
    OMEGA_MEAN = 1.0
    OMEGA_STD  = 1.5  → K_c ≈ 2.4
    N = 8, T = 1000 steps, dt = 0.01 (default)

Falsifiers (anima-physics HW target #3):
    F-HW-KU-1  phase init uniform random in [0, 2π)
    F-HW-KU-2  K below critical → r_tail < 0.3
    F-HW-KU-3  K above critical → r_tail > 0.7
    F-HW-KU-4  r̄ monotone over K sweep (3-seed avg)
    F-HW-KU-5  long-time stability — std(r[last 100]) < 0.1 at K=2.0
"""

from __future__ import annotations

import numpy as np

# ----- physical constants (mirror kuramoto_coupling.hexa) -----
OMEGA_MEAN = 1.0
OMEGA_STD = 1.5
TWO_PI = 2.0 * np.pi

# ----- default sim params -----
N_DEFAULT = 8
T_DEFAULT = 1000
DT_DEFAULT = 0.01


def make_omegas(n: int, seed: int) -> np.ndarray:
    """Gaussian-distributed intrinsic frequencies (deterministic per seed)."""
    rng = np.random.default_rng(seed)
    return OMEGA_MEAN + OMEGA_STD * rng.standard_normal(n)


def make_initial_phases(n: int, seed: int) -> np.ndarray:
    """Uniform phase init in [0, 2π) (deterministic per seed)."""
    rng = np.random.default_rng(seed + 987654321)
    return rng.uniform(0.0, TWO_PI, size=n)


def order_parameter(phases: np.ndarray) -> tuple[float, float]:
    """Returns (r, psi) for a phase array."""
    z = np.exp(1j * phases).mean()
    return float(np.abs(z)), float(np.angle(z))


def kuramoto_step(phases: np.ndarray, omegas: np.ndarray,
                  k: float, dt: float) -> np.ndarray:
    """One explicit-Euler step of the all-to-all Kuramoto equation."""
    n = phases.shape[0]
    # Pairwise sin(θ_j − θ_i): outer-diff
    diff = phases[None, :] - phases[:, None]   # shape (N, N)
    coupling = np.sin(diff).sum(axis=1)        # Σ_j sin(θ_j − θ_i)
    dtheta = omegas + (k / n) * coupling
    next_phases = (phases + dt * dtheta) % TWO_PI
    return next_phases


def simulate(n: int, k: float, steps: int, dt: float,
             seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Returns (r_history, phase_final) for a single (k, seed) run."""
    phases = make_initial_phases(n, seed)
    omegas = make_omegas(n, seed)
    r_hist = np.zeros(steps, dtype=np.float64)
    for t in range(steps):
        phases = kuramoto_step(phases, omegas, k, dt)
        r_hist[t], _ = order_parameter(phases)
    return r_hist, phases


def r_tail(r_hist: np.ndarray, tail_frac: float = 0.1) -> float:
    """Mean r over the last `tail_frac` of the history."""
    tail_n = max(1, int(r_hist.shape[0] * tail_frac))
    return float(r_hist[-tail_n:].mean())


# ═══════════════════════════════════════════════════════════════════════
# Falsifier suite F-HW-KU-1..5
# ═══════════════════════════════════════════════════════════════════════

def f_ku_1_phase_init() -> tuple[bool, str]:
    """Phase init uniform random in [0, 2π); check mean ≈ π within ±30%
    on a single seed, N=64 (statistically informative; the substrate
    really uses N=8 but the *init distribution* is the test target)."""
    phases = make_initial_phases(64, seed=42)
    in_range = bool(np.all(phases >= 0.0) and np.all(phases < TWO_PI))
    mu = float(phases.mean())
    sigma = float(phases.std())
    # Uniform[0, 2π) → mean=π≈3.14, std=2π/√12≈1.81
    mu_ok = abs(mu - np.pi) < 0.30 * np.pi  # within 30%
    sigma_ok = abs(sigma - TWO_PI / np.sqrt(12.0)) < 0.30 * (TWO_PI / np.sqrt(12.0))
    ok = in_range and mu_ok and sigma_ok
    return ok, (f"[F-HW-KU-1] phase init: in[0,2π)={in_range} "
                f"mean={mu:.3f} (target≈π={np.pi:.3f}) "
                f"std={sigma:.3f} (target≈1.814)")


def f_ku_2_below_critical(n: int, steps: int, dt: float) -> tuple[bool, str, float]:
    """K=0.1 (below K_c≈2.4) → r_tail < 0.3."""
    r_hist, _ = simulate(n, k=0.1, steps=steps, dt=dt, seed=42)
    r = r_tail(r_hist)
    ok = r < 0.3
    return ok, (f"[F-HW-KU-2] K=0.1 N={n} steps={steps}: "
                f"r_tail={r:.3f} (threshold < 0.3)"), r


def f_ku_3_above_critical(n: int, steps: int, dt: float) -> tuple[bool, str, float]:
    """K above critical → r_tail > 0.7.

    With OMEGA_STD=1.5 the critical coupling is K_c ≈ 2.4, so K=2.0
    sits *near* (just below) K_c and finite-N stochastic effects keep
    r ≲ 0.7.  We use K=5.0 here to be genuinely "above critical" per
    the falsifier wording.  The summary still reports r(K=2.0) for
    DESIGN.md §5 traceability."""
    r_hist, _ = simulate(n, k=5.0, steps=steps, dt=dt, seed=42)
    r = r_tail(r_hist)
    ok = r > 0.7
    return ok, (f"[F-HW-KU-3] K=5.0 N={n} steps={steps}: "
                f"r_tail={r:.3f} (threshold > 0.7, K_c≈2.4)"), r


def f_ku_4_monotone(n: int, steps: int, dt: float) -> tuple[bool, str]:
    """3-seed-averaged r̄ monotone non-decreasing across K∈{0.1, 1.0, 5.0}."""
    seeds = [11, 42, 97]
    ks = [0.1, 1.0, 5.0]
    means = []
    for k in ks:
        rs = [r_tail(simulate(n, k=k, steps=steps, dt=dt, seed=s)[0]) for s in seeds]
        means.append(float(np.mean(rs)))
    ok = (means[2] >= means[1]) and (means[1] >= means[0])
    return ok, (f"[F-HW-KU-4] r̄(K=0.1)={means[0]:.3f} ≤ "
                f"r̄(K=1.0)={means[1]:.3f} ≤ "
                f"r̄(K=5.0)={means[2]:.3f} monotone={ok}")


def f_ku_5_long_time_stable(n: int, steps: int, dt: float) -> tuple[bool, str]:
    """std(r[last 100 steps]) < 0.1 at K=2.0 (locked regime is stable)."""
    r_hist, _ = simulate(n, k=2.0, steps=steps, dt=dt, seed=42)
    tail = r_hist[-100:] if r_hist.shape[0] >= 100 else r_hist
    s = float(tail.std())
    ok = s < 0.1
    return ok, (f"[F-HW-KU-5] K=2.0 last-100 std(r)={s:.4f} "
                f"(threshold < 0.1)")


def main() -> int:
    n = N_DEFAULT
    steps = T_DEFAULT
    dt = DT_DEFAULT

    print("[kuramoto_neuromorphic/local_sim] HW target #3 — Mac local numpy "
          "oscillator sim")
    print(f"  N={n}, T={steps}, dt={dt}, OMEGA_MEAN={OMEGA_MEAN}, "
          f"OMEGA_STD={OMEGA_STD}  (K_c ≈ 2.4)")
    print(f"  numpy={np.__version__}")
    print("")

    results = []

    ok1, msg1 = f_ku_1_phase_init()
    print(msg1)
    print("  → " + ("PASS" if ok1 else "FAIL"))
    results.append(("F-HW-KU-1", ok1))

    ok2, msg2, _ = f_ku_2_below_critical(n, steps, dt)
    print(msg2)
    print("  → " + ("PASS" if ok2 else "FAIL"))
    results.append(("F-HW-KU-2", ok2))

    ok3, msg3, _r_at_k5 = f_ku_3_above_critical(n, steps, dt)
    print(msg3)
    print("  → " + ("PASS" if ok3 else "FAIL"))
    results.append(("F-HW-KU-3", ok3))

    ok4, msg4 = f_ku_4_monotone(n, steps, dt)
    print(msg4)
    print("  → " + ("PASS" if ok4 else "FAIL"))
    results.append(("F-HW-KU-4", ok4))

    ok5, msg5 = f_ku_5_long_time_stable(n, steps, dt)
    print(msg5)
    print("  → " + ("PASS" if ok5 else "FAIL"))
    results.append(("F-HW-KU-5", ok5))

    print("")
    pass_n = sum(1 for _, ok in results if ok)
    total = len(results)
    # Standalone reference: r(K=2.0) for DESIGN.md §5 / task spec traceability
    _r_hist_k2, _ = simulate(n, k=2.0, steps=steps, dt=dt, seed=42)
    r_at_k2 = r_tail(_r_hist_k2)
    print(f"r(K=2.0) = {r_at_k2:.4f}  (near-critical, K_c≈2.4 — reference only)")
    print(f"F-HW-KU-1..5 PASS count: {pass_n}/{total}")
    if pass_n == total:
        print("[kuramoto_neuromorphic/local_sim] 5/5 PASS — HW target #3 "
              "Phase 1a local sim DONE")
        return 0
    else:
        failed = [name for name, ok in results if not ok]
        print(f"[kuramoto_neuromorphic/local_sim] FAILED: {failed}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
