"""H_964 — World-model-as-policy (latent -> action beats reactive obs -> action).

FROZEN FALSIFIER (honored):
  a toy control environment with a return signal. arm-WAM = engine latent -> action head;
  arm-REACTIVE = observation -> action (no latent dynamics); arm-RANDOM = random action.
  N episodes x seeds.
  D1 = episode return, WAM vs REACTIVE vs RANDOM.
  D2 = latent-information lift = return_WAM - return_REACTIVE.
  D3 = random-action return bounds chance.
  PASS: return_WAM > return_REACTIVE > return_RANDOM (d>=0.5, p<0.05, latent lift>0).
  FAIL: return_WAM ~ return_REACTIVE (no lift) OR ~ random.

Environment: partial-observability control -- the agent sees POSITION only; the optimal
action depends on the HIDDEN velocity. A latent (delay-embedding) recovers velocity and
acts well; a reactive single-frame policy cannot.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, cohens_d, welch_t, header, verdict_line

ODIM = 2
NACT = 4
T = 20
N_TRAIN = 400
N_EPISODES = 300


# actions = thrust in one of NACT directions; thrust modifies velocity. The reward is to
# stay near origin, so the optimal thrust must COUNTER the current (hidden) velocity --
# a single position frame cannot tell you the velocity, but a latent (history) can.
THRUSTS = np.array([[np.cos(2 * np.pi * k / NACT), np.sin(2 * np.pi * k / NACT)] for k in range(NACT)])
VSTEP = 0.4
DRAG = 1.0       # velocity FULLY persists -> to stay near origin you must counter the
                 # (hidden) velocity, which a single position frame cannot reveal.


def step_env(pos, v, a, rng):
    v = DRAG * v + 0.6 * THRUSTS[a]
    pos = pos + VSTEP * v + 0.02 * rng.standard_normal(2)
    reward = -np.linalg.norm(pos)        # reward = stay near origin
    return pos, v, reward


def optimal_action(pos, v):
    """oracle: pick the thrust whose 1-step result is nearest origin (needs velocity)."""
    best, ba = 1e9, 0
    for a in range(NACT):
        vn = DRAG * v + 0.6 * THRUSTS[a]
        pn = pos + VSTEP * vn
        if np.linalg.norm(pn) < best:
            best = np.linalg.norm(pn); ba = a
    return ba


def gen_demo(rng):
    """expert demonstrations (oracle policy) to train the action heads via imitation."""
    pos = rng.standard_normal(2) * 2; v = rng.standard_normal(2) * 0.5
    obs, acts = [pos.copy()], []
    for _ in range(T - 1):
        a = optimal_action(pos, v); acts.append(a)
        pos, v, _ = step_env(pos, v, a, rng)
        obs.append(pos.copy())
    acts.append(optimal_action(pos, v))
    return np.array(obs), np.array(acts)


def run_policy(kind, m, Whead, rng):
    pos = rng.standard_normal(2) * 2; v = rng.standard_normal(2) * 0.5
    obs_hist = [pos.copy()]
    total = 0.0
    for t in range(T - 1):
        if kind == "random":
            a = rng.integers(NACT)
        elif kind == "reactive":
            feat = _aug(pos[None, :]); a = int((feat @ Whead).argmax())
        else:  # wam: latent (delay-embed) -> action
            z = m.embed(np.array(obs_hist))[-1]
            a = int((_aug(z[None, :]) @ Whead).argmax())
        pos, v, r = step_env(pos, v, a, rng)
        obs_hist.append(pos.copy()); total += r
    return total / (T - 1)


def main():
    header("H_964", "World-model-as-policy (latent->action beats reactive)")
    print(f"partial-obs control (hidden velocity); WAM vs REACTIVE vs RANDOM; N_ep={N_EPISODES}\n")
    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]
    m = LDSWorldModel(ODIM, delay=3).fit([o for o, a in demos])
    # WAM head: latent -> action (imitation of oracle)
    Zw, Yw = [], []
    for o, a in demos:
        z = m.embed(o)
        for t in range(2, T):
            Zw.append(z[t]); Yw.append(np.eye(NACT)[a[t]])
    Whead_wam = _ridge(_aug(np.array(Zw)), np.array(Yw), 1e-2)
    # REACTIVE head: single observation -> action
    Xr, Yr = [], []
    for o, a in demos:
        for t in range(T):
            Xr.append(o[t]); Yr.append(np.eye(NACT)[a[t]])
    Whead_reac = _ridge(_aug(np.array(Xr)), np.array(Yr), 1e-2)

    wam = np.array([run_policy("wam", m, Whead_wam, np.random.default_rng(1000 + i)) for i in range(N_EPISODES)])
    reac = np.array([run_policy("reactive", m, Whead_reac, np.random.default_rng(2000 + i)) for i in range(N_EPISODES)])
    rand = np.array([run_policy("random", m, None, np.random.default_rng(3000 + i)) for i in range(N_EPISODES)])

    print(f"D1 episode return (higher=better, 0=optimal):")
    print(f"  WAM (latent->action) = {wam.mean():.4f} ± {wam.std():.4f}")
    print(f"  REACTIVE (obs->action)= {reac.mean():.4f} ± {reac.std():.4f}")
    print(f"  RANDOM               = {rand.mean():.4f} ± {rand.std():.4f}")
    lift = wam.mean() - reac.mean()
    d = cohens_d(wam, reac); t, p = welch_t(wam, reac)
    print(f"D2 latent-information lift = {lift:.4f}  d={d:.3f} p={p:.3e}")
    dr = cohens_d(reac, rand); tr, pr = welch_t(reac, rand)
    print(f"D3 REACTIVE vs RANDOM: d={dr:.3f} p={pr:.3e}")

    lift_ok = (lift > 0) and p < 0.05 and d >= 0.5
    order_ok = (wam.mean() > reac.mean() > rand.mean())
    if lift_ok and order_ok:
        verdict_line("H_964", "PASS",
                     f"return_WAM {wam.mean():.3f} > REACTIVE {reac.mean():.3f} > RANDOM {rand.mean():.3f}; "
                     f"latent lift {lift:.3f} (d={d:.2f}, p={p:.1e}>0) — world-model-as-policy (toy).")
    elif not lift_ok:
        verdict_line("H_964", "FAIL",
                     f"WAM~REACTIVE (lift {lift:.3f}, d={d:.2f}) — latent carries no actionable "
                     f"advantage; engine is an emitter not a policy (closed-negative).")
    else:
        verdict_line("H_964", "INCOMPLETE", f"lift={lift:.3f} d={d:.2f} marginal; toy C3.")


if __name__ == "__main__":
    main()
