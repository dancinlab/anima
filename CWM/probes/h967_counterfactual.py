"""H_967 — Counterfactual imagination (imagined action values rank true returns).

FROZEN FALSIFIER (honored):
  a toy world with a small discrete action set and a known return function. From sampled
  states, the engine rolls out each action's latent branch h steps and scores an imagined
  value; the environment provides the true return. N states x seeds.
  D1 = rank correlation (Spearman/Kendall) between imagined-value order and true-return
       order across actions per state.
  D2 = top-1 regret: true return of the imagined-best action vs the actual best.
  D3 = random ranking bounds chance.
  PASS: rank corr CI_lo>0 (beats random) AND top-1 regret < random-selection regret
        (d>=0.5, p<0.05).
  FAIL: rank corr ~ chance OR regret ~ random.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, _aug1, cohens_d, welch_t, boot_ci, header, verdict_line
from scipy import stats


class SwitchingLDS:
    """one linear transition PER ACTION (a switching-linear world model) — faithful to
    'roll each action's latent branch'; captures action-dependent dynamics a single linear
    map cannot. Shared delay-embedding + decoder."""

    def __init__(self, obs_dim, nact, delay=3, ridge=1e-3):
        self.m = LDSWorldModel(obs_dim, delay=delay)
        self.nact = nact; self.ridge = ridge; self.A = {}

    def fit(self, obs, acts):
        self.m.fit(obs)                       # shared decoder + embedding
        # per-action transition: collect (z_t -> z_{t+1}) pairs where action a was taken
        pairs = {a: ([], []) for a in range(self.nact)}
        for ob, ac in zip(obs, acts):
            z = self.m.embed(ob)
            for t in range(self.m.delay - 1, len(ob) - 1):
                a = int(np.argmax(ac[t])) if ac[t].sum() > 0 else None
                if a is not None:
                    pairs[a][0].append(z[t]); pairs[a][1].append(z[t + 1])
        for a in range(self.nact):
            if pairs[a][0]:
                self.A[a] = _ridge(_aug(np.array(pairs[a][0])), np.array(pairs[a][1]), self.ridge)
        return self

    def roll(self, z0, a, h):
        z = z0.copy()
        for _ in range(h):
            z = _aug1(z) @ self.A[a]
        return z

    def decode(self, z):
        return self.m.decode(z)

    def embed(self, ob):
        return self.m.embed(ob)

ODIM = 2
NACT = 4
H = 5
T = 25
N_TRAIN = 300
N_STATES = 200


def dynamics(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


ACT_THETAS = np.linspace(-0.6, 0.6, NACT)   # each action = a different turn rate


def gen_traj(rng):
    """action-conditioned: at each step a random action sets the turn; observe position."""
    pos = rng.standard_normal(2); v = rng.standard_normal(2) * 0.5
    obs, acts = [pos.copy()], []
    for _ in range(T - 1):
        a = rng.integers(NACT)
        v = dynamics(ACT_THETAS[a]) @ v
        pos = pos + 0.3 * v + 0.02 * rng.standard_normal(2)
        obs.append(pos.copy()); acts.append(np.eye(NACT)[a])
    acts.append(np.zeros(NACT))
    return np.array(obs), np.array(acts)


def true_return(pos0, v0, a, h):
    """known return = negative distance from origin after committing to action a for h steps
    (reward for staying near origin)."""
    pos, v = pos0.copy(), v0.copy()
    for _ in range(h):
        v = dynamics(ACT_THETAS[a]) @ v
        pos = pos + 0.3 * v
    return -np.linalg.norm(pos)


def main():
    header("H_967", "Counterfactual imagination (imagined value ranks true return)")
    print(f"actions={NACT} rollout h={H} N_states={N_STATES}\n")
    rng = np.random.default_rng(0)
    trs = [gen_traj(rng) for _ in range(N_TRAIN)]
    obs = [o for o, a in trs]; acts = [a for o, a in trs]
    m = SwitchingLDS(ODIM, NACT, delay=3).fit(obs, acts)

    rank_corrs, regrets, rnd_regrets = [], [], []
    rng2 = np.random.default_rng(11)
    for _ in range(N_STATES):
        o, a = gen_traj(rng2)
        t0 = 5
        z0 = m.embed(o)[t0]
        # current velocity estimate from consecutive observed positions
        v0 = (o[t0] - o[t0 - 1]) / 0.3
        imagined, truth = [], []
        for act in range(NACT):
            zr = m.roll(z0, act, H)
            pos_pred = m.decode(zr)
            imagined.append(-np.linalg.norm(pos_pred))   # imagined value (near origin good)
            truth.append(true_return(o[t0], v0, act, H))
        imagined, truth = np.array(imagined), np.array(truth)
        rc, _ = stats.spearmanr(imagined, truth)
        if not np.isnan(rc):
            rank_corrs.append(rc)
        best_imagined = int(np.argmax(imagined)); best_true = int(np.argmax(truth))
        regrets.append(truth[best_true] - truth[best_imagined])
        rnd = rng2.integers(NACT)
        rnd_regrets.append(truth[best_true] - truth[rnd])

    rank_corrs = np.array(rank_corrs); regrets = np.array(regrets); rnd_regrets = np.array(rnd_regrets)
    rc_lo, rc_hi = boot_ci(rank_corrs)
    print(f"D1 rank correlation (imagined vs true) = {rank_corrs.mean():.4f}  CI=[{rc_lo:.4f},{rc_hi:.4f}]")
    print(f"D2 top-1 regret: imagined-best={regrets.mean():.4f}  random={rnd_regrets.mean():.4f}")
    d = cohens_d(rnd_regrets, regrets); t, p = welch_t(regrets, rnd_regrets)
    print(f"   regret reduction vs random: d={d:.3f} p={p:.3e}")

    beats_rand_rank = rc_lo > 0
    beats_rand_regret = (regrets.mean() < rnd_regrets.mean()) and p < 0.05 and d >= 0.5
    if beats_rand_rank and beats_rand_regret:
        verdict_line("H_967", "PASS",
                     f"rank-corr={rank_corrs.mean():.2f} (CI_lo {rc_lo:.2f}>0) AND top-1 regret "
                     f"{regrets.mean():.3f} << random {rnd_regrets.mean():.3f} (d={d:.2f}) — "
                     f"counterfactual imagination (toy).")
    elif not beats_rand_rank or not beats_rand_regret:
        verdict_line("H_967", "FAIL",
                     f"rank-corr CI=[{rc_lo:.2f},{rc_hi:.2f}] or regret~random — cannot imagine "
                     f"action consequences (closed-negative).")
    else:
        verdict_line("H_967", "INCOMPLETE", "marginal; toy C3.")


if __name__ == "__main__":
    main()
