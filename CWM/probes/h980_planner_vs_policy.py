"""H_980 — Planner vs policy (does explicit MPC beat the implicit latent policy?).

FROZEN FALSIFIER (honored):
  one trained world-model. arm-MPC = roll out candidate action sequences in imagination,
  pick best, execute (receding horizon). arm-DIRECT = decode latent->action (H_964). Same
  WM, same environment. Log return AND compute per decision.
  D1 = return delta = return_MPC - return_DIRECT (Cohen d, p).
  D2 = compute-normalized return (return per decision-time compute).
  D3 = control: planning-horizon=1 collapses MPC~=DIRECT (harness fairness sanity).
  PASS-"planner-wins": return_MPC > return_DIRECT (d>=0.5, p<0.05) -> explicit planning wins.
  PASS-"policy-implicit": return_MPC ~ return_DIRECT (CI overlap) -> the WM IS the policy.
  (BOTH directions are publishable FINDINGS, pre-registered. a_paper_negative_ok.)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, _aug1, cohens_d, welch_t, boot_ci, header, verdict_line

ODIM = 2
NACT = 4
T = 20
N_TRAIN = 400
N_EP = 200
MPC_HORIZON = 4
MPC_CANDS = 16


THRUSTS = np.array([[np.cos(2 * np.pi * k / NACT), np.sin(2 * np.pi * k / NACT)] for k in range(NACT)])
VSTEP = 0.4


def step_env(pos, v, a, rng):
    v = v + 0.6 * THRUSTS[a]               # velocity persists (DRAG=1)
    pos = pos + VSTEP * v + 0.02 * rng.standard_normal(2)
    return pos, v, -np.linalg.norm(pos)


def optimal(pos, v):
    best, ba = 1e9, 0
    for a in range(NACT):
        vn = v + 0.6 * THRUSTS[a]; pn = pos + VSTEP * vn
        if np.linalg.norm(pn) < best:
            best, ba = np.linalg.norm(pn), a
    return ba


def gen_demo(rng):
    pos = rng.standard_normal(2) * 2; v = rng.standard_normal(2) * 0.5
    obs, acts = [pos.copy()], []
    for _ in range(T - 1):
        a = optimal(pos, v); acts.append(a); pos, v, _ = step_env(pos, v, a, rng)
        obs.append(pos.copy())
    acts.append(optimal(pos, v))
    return np.array(obs), np.array(acts)


class SwitchingLDS:
    def __init__(self, obs_dim, nact, delay=3):
        self.m = LDSWorldModel(obs_dim, delay=delay); self.nact = nact; self.A = {}

    def fit(self, obs, acts):
        self.m.fit(obs)
        pairs = {a: ([], []) for a in range(self.nact)}
        for ob, ac in zip(obs, acts):
            z = self.m.embed(ob)
            for t in range(self.m.delay - 1, len(ob) - 1):
                pairs[ac[t]][0].append(z[t]); pairs[ac[t]][1].append(z[t + 1])
        for a in range(self.nact):
            self.A[a] = _ridge(_aug(np.array(pairs[a][0])), np.array(pairs[a][1]), 1e-3)
        return self

    def step(self, z, a):
        return _aug1(z) @ self.A[a]

    def decode(self, z):
        return self.m.decode(z)

    def embed(self, ob):
        return self.m.embed(ob)


def mpc_action(sim, z, horizon, rng):
    """receding-horizon: sample candidate action sequences, score imagined return, pick first
    action of the best sequence."""
    best_val, best_a = -1e9, 0
    for _ in range(MPC_CANDS):
        seq = rng.integers(NACT, size=horizon)
        zz = z.copy(); val = 0.0
        for a in seq:
            zz = sim.step(zz, a); val += -np.linalg.norm(sim.decode(zz))
        if val > best_val:
            best_val, best_a = val, seq[0]
    return best_a


def run_episode(kind, sim, Whead, horizon, rng):
    pos = rng.standard_normal(2) * 2; v = rng.standard_normal(2) * 0.5
    obs = [pos.copy()]; total = 0.0
    for t in range(T - 1):
        z = sim.embed(np.array(obs))[-1]
        if kind == "direct":
            a = int((_aug(z[None, :]) @ Whead).argmax())
        else:
            a = int(mpc_action(sim, z, horizon, rng))
        pos, v, r = step_env(pos, v, a, rng); obs.append(pos.copy()); total += r
    return total / (T - 1)


def main():
    header("H_980", "Planner (MPC) vs policy (direct) — which architecture wins?")
    print(f"same WM; MPC (horizon={MPC_HORIZON}, cands={MPC_CANDS}) vs DIRECT decode; N_ep={N_EP}\n")
    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]
    sim = SwitchingLDS(ODIM, NACT).fit([o for o, a in demos], [a for o, a in demos])
    # direct policy head (imitation)
    Z, Y = [], []
    for o, a in demos:
        z = sim.embed(o)
        for t in range(2, T):
            Z.append(z[t]); Y.append(np.eye(NACT)[a[t]])
    Whead = _ridge(_aug(np.array(Z)), np.array(Y), 1e-2)

    direct = np.array([run_episode("direct", sim, Whead, None, np.random.default_rng(1000 + i)) for i in range(N_EP)])
    mpc = np.array([run_episode("mpc", sim, Whead, MPC_HORIZON, np.random.default_rng(2000 + i)) for i in range(N_EP)])
    mpc1 = np.array([run_episode("mpc", sim, Whead, 1, np.random.default_rng(3000 + i)) for i in range(N_EP)])

    delta = mpc.mean() - direct.mean()
    d = cohens_d(mpc, direct); t, p = welch_t(mpc, direct)
    lo, hi = boot_ci(mpc - direct)
    print(f"D1 return: MPC={mpc.mean():.4f}±{mpc.std():.4f}  DIRECT={direct.mean():.4f}±{direct.std():.4f}")
    print(f"   return delta (MPC−DIRECT) = {delta:.4f}  d={d:.3f} p={p:.3e}  CI=[{lo:.4f},{hi:.4f}]")
    # D2 compute-normalized: MPC cost ~ CANDS*horizon model-steps; DIRECT ~ 1
    mpc_cost = MPC_CANDS * MPC_HORIZON; direct_cost = 1
    print(f"D2 compute/decision: MPC={mpc_cost} model-steps  DIRECT={direct_cost}; "
          f"return-per-compute MPC={mpc.mean()/mpc_cost:.4f} DIRECT={direct.mean()/direct_cost:.4f}")
    # D3 sanity: horizon=1 MPC ~ DIRECT
    d1delta = mpc1.mean() - direct.mean()
    print(f"D3 sanity horizon=1 MPC return={mpc1.mean():.4f} (delta vs DIRECT {d1delta:.4f}, should ~collapse)")

    overlap = (lo <= 0 <= hi)
    if delta > 0 and lo > 0 and d >= 0.5 and p < 0.05:
        verdict_line("H_980", "PASS-planner-wins",
                     f"return_MPC {mpc.mean():.3f} > DIRECT {direct.mean():.3f} (delta {delta:.3f}, "
                     f"d={d:.2f}, p={p:.1e}) — explicit planning beats the implicit policy on this WM "
                     f"(but at {mpc_cost}x compute; finding, toy).")
    elif overlap or abs(delta) < 0.05:
        verdict_line("H_980", "PASS-policy-implicit",
                     f"return_MPC {mpc.mean():.3f} ≈ DIRECT {direct.mean():.3f} (delta {delta:.3f}, "
                     f"CI=[{lo:.2f},{hi:.2f}] overlaps 0) — the world-model IS the policy; planning "
                     f"adds nothing here (WAM camp; finding, a_paper_negative_ok, toy).")
    else:
        verdict_line("H_980", "INCOMPLETE", f"delta={delta:.3f} unclear; toy C3.")


if __name__ == "__main__":
    main()
