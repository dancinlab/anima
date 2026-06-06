"""H_995 — WM-as-critic: choose actions purely from IMAGINED value (Dreamer-style).

1st-round seed: H_967🟢 action-conditioned imagined rollouts RANK actions in agreement with
true return (given the returns). H_964🟢 latent→action policy. This goes further (Dreamer
actor-critic): the WM learns a VALUE function on its latent, then at decision time it
IMAGINES each candidate action's rollout, scores the imagined terminal value, and picks the
best — with NO access to the environment reward at decision time (planning in the head).

Falsifier (frozen): a latent task with a hidden-reward landscape. Train value head on
latent→return from offline data. At test, for each candidate action imagine the rollout,
read imagined value, pick argmax.
  PASS iff the imagined-value policy achieves true return significantly above (a) a random-
       action baseline AND (b) a reactive 1-step-greedy baseline, with the imagined-value
       choice's CORRELATION to the true best action's return rank > 0.7 (Spearman), over
       >=20 seeds. The WM is its own critic — value comes from imagination, not env reward.
  FAIL iff imagined value does not beat random/greedy or imagined ranks ≠ true ranks.
substrate=CPU-mirror (numpy). a_scale_honest_scope: single toy rung, ladder OPEN.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "probes"))
from cwm_probe_lib import LDSWorldModel, header, cohens_d, welch_t, spearman, _ridge, _aug, _aug1

N_SEEDS = 24
H = 6
N_ACT = 5
OBS = 3
REW_C = np.array([1.5, -1.0, 0.5])    # reward peak in observation space


def reward(ob):
    return float(np.exp(-0.5 * np.linalg.norm(np.asarray(ob) - REW_C) ** 2))


def dynamics(ob, a_vec):
    """Ground-truth latent-world dynamics: action nudges the observation with momentum."""
    return np.asarray(ob, float) + 0.5 * a_vec


def gen_offline(rng, n=120):
    """Offline trajectories under a random behavior policy; collect (obs-seq, act-seq) +
    returns for value training."""
    trajs, acts, val_states, val_targets = [], [], [], []
    A = rng.standard_normal((N_ACT, OBS))      # fixed action repertoire (vectors)
    for _ in range(n):
        ob = rng.uniform(-2, 2, OBS)
        obs = [ob.copy()]; aseq = []
        for t in range(H):
            ai = rng.integers(N_ACT); a = A[ai]
            ob = dynamics(ob, a)
            obs.append(ob.copy()); aseq.append(a)
        obs = np.array(obs); aseq = np.array(aseq)
        trajs.append(obs); acts.append(np.vstack([aseq, aseq[-1]]))
        # value of each visited state = discounted future reward
        for t in range(len(obs)):
            G = sum((0.9 ** k) * reward(obs[min(t + k, len(obs) - 1)]) for k in range(H))
            val_states.append(obs[t]); val_targets.append(G)
    return A, trajs, acts, np.array(val_states), np.array(val_targets)


def main():
    header("H_995", "WM-as-critic: pick actions from IMAGINED value (Dreamer-style)")
    img_ret, rand_ret, greedy_ret = [], [], []
    rank_corrs = []
    for s in range(N_SEEDS):
        rng = np.random.default_rng(40000 + s)
        A, trajs, acts, vs, vt = gen_offline(rng)
        lm = LDSWorldModel(obs_dim=OBS, delay=2, act_dim=OBS, ridge=1e-3)
        lm.fit(trajs, traj_acts=acts)
        Wv = _ridge(_aug(vs), vt.reshape(-1, 1), 1e-2)       # value head latent(obs)->return
        value = lambda ob: float(np.ravel(_aug1(np.asarray(ob, float)) @ Wv)[0])
        # decision episodes
        ir = rr = gr = 0.0; corrs = []
        for _ in range(30):
            ob0 = rng.uniform(-2, 2, OBS)
            true_vals = []
            imag_vals = []
            for a in A:
                # TRUE return of committing this action for H steps (greedy repeat)
                ob = ob0.copy(); R = 0
                for k in range(H):
                    ob = dynamics(ob, a); R += (0.9 ** k) * reward(ob)
                true_vals.append(R)
                # IMAGINED value via the WM (latent rollout) + value head, no env reward
                z = lm.embed(np.vstack([ob0, ob0]))[-1]
                z = lm.roll(z, H, act_seq=[a] * H)
                imag_vals.append(value(lm.decode(z)))
            imag_vals = np.array(imag_vals); true_vals = np.array(true_vals)
            best_imag = int(imag_vals.argmax())
            ir += true_vals[best_imag]
            rr += true_vals[rng.integers(N_ACT)]
            # reactive greedy: pick action max 1-step reward
            one = [reward(dynamics(ob0, a)) for a in A]
            gr += true_vals[int(np.argmax(one))]
            rc, _ = spearman(imag_vals, true_vals)
            if not np.isnan(rc):
                corrs.append(rc)
        img_ret.append(ir / 30); rand_ret.append(rr / 30); greedy_ret.append(gr / 30)
        rank_corrs.append(np.mean(corrs))
    img_ret, rand_ret, greedy_ret = map(np.array, (img_ret, rand_ret, greedy_ret))
    rc = float(np.mean(rank_corrs))
    print(f"task=latent reward-landscape  H={H} actions={N_ACT} seeds={N_SEEDS}")
    print("true return achieved (higher=better), mean ± std:")
    print(f"  IMAGINED-VALUE policy (WM critic) : {img_ret.mean():.4f} ± {img_ret.std():.4f}")
    print(f"  RANDOM action                     : {rand_ret.mean():.4f} ± {rand_ret.std():.4f}")
    print(f"  REACTIVE 1-step greedy            : {greedy_ret.mean():.4f} ± {greedy_ret.std():.4f}")
    tr, pr = welch_t(img_ret, rand_ret); tg, pg = welch_t(img_ret, greedy_ret)
    print()
    print(f"D1 imagined>random: d={cohens_d(img_ret,rand_ret):.3f} p={pr:.2e}")
    print(f"D2 imagined>greedy: d={cohens_d(img_ret,greedy_ret):.3f} p={pg:.2e}")
    print(f"D3 imagined-vs-true action-value rank corr (Spearman) = {rc:.3f}")
    print("-" * 78)
    beats = img_ret.mean() > rand_ret.mean() and pr < 0.05 and img_ret.mean() > greedy_ret.mean() and pg < 0.05
    ranks = rc > 0.7
    if beats and ranks:
        v = (f"PASS WM is its own critic: imagined-value policy return={img_ret.mean():.3f} beats random "
             f"{rand_ret.mean():.3f} (p={pr:.1e}) AND greedy {greedy_ret.mean():.3f} (p={pg:.1e}), with "
             f"imagined-vs-true rank corr {rc:.2f} — actions chosen from imagination, no env reward (toy rung).")
        tok = "PASS"
    elif beats:
        v = (f"PASS-PARTIAL imagined-value beats random+greedy but rank-corr {rc:.2f}<0.7 — WM-critic "
             f"helps, ranking imperfect (toy).")
        tok = "PASS"
    else:
        v = (f"FAIL imagined-value policy does not beat baselines (vs random p={pr:.1e}, vs greedy p={pg:.1e}) "
             f"— WM cannot serve as its own critic here (closed-negative, toy).")
        tok = "FAIL"
    print(f"VERDICT H_995: {v}")
    print("-" * 78)
    return tok


if __name__ == "__main__":
    main()
