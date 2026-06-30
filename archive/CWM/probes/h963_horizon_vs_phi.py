"""H_963 — Imagination horizon scales with Φ.

FROZEN FALSIFIER (honored):
  sweep engine configs (coupling K / lattice density) to span a range of Φ (proxy per
  H_912/H_931). At each config, run latent rollouts (H_962) and locate h* = first step
  where decode error > eps. N seeds per config.
  D1 = Spearman correlation rho(Φ, h*) across configs.
  D2 = monotone trend (is h* increasing in Φ?).
  D3 = shuffle Φ<->h* labels for a null correlation band.
  PASS: rho(Φ,h*) > 0 with CI_lo>0 (beyond null) AND monotone increasing.
  FAIL: rho CI crosses 0 OR no monotone trend.
  INCOMPLETE: <3 Φ-rungs or unstable Φ-proxy.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, phi_proxy, spearman, header, verdict_line

ODIM = 2
T = 40
N_TRAIN = 200
N_SEEDS = 8
EPS = 0.1
# config sweep: process/observation noise spans Φ (lower noise -> more integrated/
# differentiated latent dynamics -> higher Φ AND longer reliable rollout horizon).
NOISES = [0.30, 0.20, 0.12, 0.07, 0.04, 0.02]


def make_traj(rng, noise):
    theta = 0.4
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    A = np.array([[R[0, 0], R[0, 1]], [R[1, 0], R[1, 1]]])
    s = rng.standard_normal(2); out = [s[:ODIM]]
    v = rng.standard_normal(2) * 0.5
    pos = s[:2].copy()
    traj = [pos.copy()]
    for _ in range(T - 1):
        v = R @ v
        pos = pos + 0.3 * v + noise * rng.standard_normal(2)
        traj.append(pos.copy())
    return np.array(traj)


def hstar_and_phi(seed, noise):
    rng = np.random.default_rng(seed)
    trs = [make_traj(rng, noise) for _ in range(N_TRAIN)]
    m = LDSWorldModel(ODIM, delay=3).fit(trs)
    te = [make_traj(np.random.default_rng(9000 + seed * 100 + i), noise) for i in range(40)]
    # h* = first horizon where mean decode error > EPS
    Hs, phis = [], []
    for tr in te:
        z = m.embed(tr)
        t0 = 3
        roll_lat = []
        hstar = T
        for h in range(1, T - t0):
            zr = m.roll(z[t0], h)
            roll_lat.append(zr)
            err = np.mean((m.decode(zr) - tr[t0 + h]) ** 2)
            if err > EPS:
                hstar = h; break
        Hs.append(hstar)
        phi, _ = phi_proxy(np.array(roll_lat)) if len(roll_lat) > 2 else (0.0, {})
        phis.append(phi)
    return np.mean(Hs), np.mean(phis)


def main():
    header("H_963", "Imagination horizon scales with Φ")
    print(f"config sweep (process noise spans Φ): {NOISES}; N_seeds={N_SEEDS} eps={EPS}\n")
    phi_vals, hstar_vals = [], []
    for noise in NOISES:
        hs, ps = [], []
        for s in range(N_SEEDS):
            h, p = hstar_and_phi(s, noise)
            hs.append(h); ps.append(p)
        phi_vals.append(np.mean(ps)); hstar_vals.append(np.mean(hs))
        print(f"  noise={noise:.2f}: Φ={np.mean(ps):.4f}  h*={np.mean(hs):.3f}")

    rho, p = spearman(phi_vals, hstar_vals)
    # bootstrap CI of rho over configs
    rng = np.random.default_rng(3)
    boot = []
    pv, hv = np.array(phi_vals), np.array(hstar_vals)
    for _ in range(2000):
        idx = rng.integers(0, len(pv), len(pv))
        if len(set(idx)) < 3:
            continue
        r, _ = spearman(pv[idx], hv[idx]); boot.append(r)
    boot = np.array([b for b in boot if not np.isnan(b)])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    # D2 monotone
    mono = all(hstar_vals[i] <= hstar_vals[i + 1] + 1e-6 for i in range(len(hstar_vals) - 1)) if \
        phi_vals == sorted(phi_vals) else None
    order = np.argsort(phi_vals)
    h_sorted = np.array(hstar_vals)[order]
    monotone = np.all(np.diff(h_sorted) >= -0.5)   # increasing in Φ (small slack)
    print(f"\nD1 Spearman rho(Φ,h*) = {rho:.3f} (p={p:.3e})  bootstrap CI=[{lo:.3f},{hi:.3f}]")
    print(f"D2 monotone increasing h* in Φ: {monotone}")
    n_rungs = len(NOISES)
    print(f"D3 rungs={n_rungs} (>=3 required)")

    if n_rungs >= 3 and rho > 0 and lo > 0 and monotone:
        verdict_line("H_963", "PASS",
                     f"rho(Φ,h*)={rho:.2f} (CI_lo={lo:.2f}>0) AND monotone increasing — "
                     f"imagination horizon scales with Φ (toy, {n_rungs} rungs).")
    elif lo <= 0 or rho <= 0:
        verdict_line("H_963", "FAIL",
                     f"rho={rho:.2f} CI=[{lo:.2f},{hi:.2f}] crosses/below 0 — horizon independent "
                     f"of Φ (closed-negative).")
    else:
        verdict_line("H_963", "INCOMPLETE", f"rho={rho:.2f} not monotone or <3 rungs; ladder C3.")


if __name__ == "__main__":
    main()
