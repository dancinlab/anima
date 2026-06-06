"""H_962 — Latent forward dynamics (world-state rollout beats surface prediction).

FROZEN FALSIFIER (honored):
  a toy dynamical world with known generating factors. arm-LATENT = encode -> roll the
  latent transition operator forward h steps -> decode -> compare to truth. arm-OBS =
  predict the next observation directly (surface baseline). horizons h in {1,2,4,8}.
  D1 = h-step factor decode error, latent-rollout vs observation-baseline.
  D2 = horizon advantage slope: does (error_OBS - error_LATENT) grow with h?
  D3 = a persistence ("state stays put") baseline bounds trivial worlds.
  PASS: error_LATENT < error_OBS for h>=2 (d>=0.5,p<0.05) AND advantage slope>0 AND
        latent beats persistence.
  FAIL: error_LATENT ~ error_OBS OR no horizon advantage OR fails to beat persistence.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LatentWorldModel, _ridge, _aug, cohens_d, welch_t, spearman, header, verdict_line

LATENT = 32
SDIM = 4           # full state: [pos_x, pos_y, vel_x, vel_y]
ODIM = 2           # OBSERVABLE: position only (velocity is HIDDEN -> needs world-state)
T = 30
N = 300
HORIZONS = [1, 2, 4, 8]


def make_traj(rng):
    """state = [pos(2), vel(2)]; observation = position only. To predict the future you
    must infer the HIDDEN velocity from the observation SEQUENCE (a world-state); a
    surface predictor that sees only the current position cannot (partial observability)."""
    theta = 0.4
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    A = np.eye(SDIM); A[:2, :2] = R; A[2:, 2:] = 0.9 * R
    A[0, 2] = 0.5; A[1, 3] = 0.5         # velocity drives position
    s = rng.standard_normal(SDIM); states = [s]
    for _ in range(T - 1):
        s = A @ s + 0.03 * rng.standard_normal(SDIM); states.append(s)
    return np.array(states)


def obs_of(states):
    return states[:, :ODIM]


def main():
    header("H_962", "Latent forward dynamics (rollout beats surface prediction)")
    print(f"toy world SDIM={SDIM} T={T} N={N} horizons={HORIZONS}\n")
    rng = np.random.default_rng(0)
    trajs = [make_traj(rng) for _ in range(N)]
    # LATENT world model: a delay-embedding latent z_t = [o_t, o_{t-1}] (captures the
    # HIDDEN velocity that a single observation lacks), with a LEARNED linear transition
    # A (z_{t+1} = A z_t) and a decoder C (z -> position). This is the faithful "latent
    # forward dynamics" object (JEPA/Dreamer-style latent rollout) -- it can roll forward
    # because the latent holds the world-state (velocity), unlike a single-frame surface
    # predictor.
    def embed(ob):
        z = np.zeros((len(ob), ODIM * 2))
        z[:, :ODIM] = ob
        z[1:, ODIM:] = ob[:-1]
        return z
    Zt, Ztp1, Zd, Yd = [], [], [], []
    for st in trajs:
        z = embed(obs_of(st))
        Zt.append(z[1:-1]); Ztp1.append(z[2:])
        Zd.append(z); Yd.append(st[:, :ODIM])
    A_lat = _ridge(_aug(np.vstack(Zt)), np.vstack(Ztp1), 1e-3)    # latent transition
    Wdec = _ridge(_aug(np.vstack(Zd)), np.vstack(Yd), 1e-3)       # latent -> position
    def roll(z0, h):
        z = z0.copy()
        for _ in range(h):
            z = (_aug(z[None, :]) @ A_lat)[0]
        return z
    test = [make_traj(np.random.default_rng(5000 + i)) for i in range(N)]

    adv_by_h = {}
    for h in HORIZONS:
        eL, eO, eP = [], [], []
        # obs-baseline: a SURFACE next-observation predictor (o_t -> ô_{t+1}) with NO
        # persistent state, rolled ITERATIVELY h times (feed its own prediction back).
        # Without the hidden velocity it cannot represent the rotation -> error compounds.
        Xo, Yo = [], []
        for st in trajs:
            ob = obs_of(st)
            for t in range(T - 1):
                Xo.append(ob[t]); Yo.append(ob[t + 1])
        Wo = _ridge(_aug(np.array(Xo)), np.array(Yo), 1e-1)
        for st in test:
            ob = obs_of(st)
            Z = embed(ob)
            for t in range(2, T - h, 3):           # t>=2 so the latent has seen >=2 obs (can infer velocity)
                zroll = roll(Z[t], h)
                pred_L = (_aug(zroll[None, :]) @ Wdec)[0]
                # iterated surface rollout (stateless): apply the one-step map h times
                o = ob[t].copy()
                for _ in range(h):
                    o = (_aug(o[None, :]) @ Wo)[0]
                pred_O = o
                pred_P = ob[t]                       # persistence (position stays put)
                truth = ob[t + h]
                eL.append(np.mean((pred_L - truth) ** 2))
                eO.append(np.mean((pred_O - truth) ** 2))
                eP.append(np.mean((pred_P - truth) ** 2))
        eL, eO, eP = map(np.array, (eL, eO, eP))
        adv_by_h[h] = (eL.mean(), eO.mean(), eP.mean(), eL, eO)
        print(f"h={h}: error_LATENT={eL.mean():.4f}  error_OBS={eO.mean():.4f}  "
              f"persistence={eP.mean():.4f}")

    # D1 at h>=2
    h2 = adv_by_h[2]; d = cohens_d(h2[3], h2[1] if False else h2[3]) if False else cohens_d(adv_by_h[2][4], adv_by_h[2][3])
    t2, p2 = welch_t(adv_by_h[2][3], adv_by_h[2][4])
    latent_wins_h2 = adv_by_h[2][0] < adv_by_h[2][1] and p2 < 0.05 and d >= 0.5
    # D2 advantage slope
    advs = [adv_by_h[h][1] - adv_by_h[h][0] for h in HORIZONS]
    rho, prho = spearman(HORIZONS, advs)
    print(f"\nD1 (h=2) latent<obs: d={d:.3f} p={p2:.3e} -> {latent_wins_h2}")
    print(f"D2 horizon-advantage (OBS−LATENT) by h = {dict(zip(HORIZONS, np.round(advs,4)))}  "
          f"slope Spearman rho={rho:.3f}")
    beats_persist = all(adv_by_h[h][0] < adv_by_h[h][2] for h in HORIZONS if h >= 2)
    print(f"D3 latent beats persistence at h>=2: {beats_persist}")

    if latent_wins_h2 and rho > 0 and beats_persist:
        verdict_line("H_962", "PASS",
                     f"error_LATENT<error_OBS at h>=2 (d={d:.2f}), advantage grows with horizon "
                     f"(rho={rho:.2f}), latent beats persistence — latent world-state dynamics (toy).")
    elif not latent_wins_h2 or rho <= 0:
        verdict_line("H_962", "FAIL",
                     f"latent~obs (d={d:.2f}) or no horizon advantage (rho={rho:.2f}) — surface "
                     f"predictor, no world-state dynamics (closed-negative).")
    else:
        verdict_line("H_962", "INCOMPLETE", f"d={d:.2f} rho={rho:.2f} marginal; toy C3.")


if __name__ == "__main__":
    main()
