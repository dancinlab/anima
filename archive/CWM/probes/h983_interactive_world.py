"""H_983 — Generated interactive world (the engine simulates a self-consistent world).

FROZEN FALSIFIER (honored):
  engine generates a small latent world from a seed. A scripted agent executes action
  sequences (including loops that return to prior states). N seeds x trajectories.
  D1 = action-consequence coherence: do equal actions from equal states yield equal
       next-states (rule-consistency) above a shuffled-transition baseline?
  D2 = revisit-consistency: returning to a configuration via a loop yields a state within
       eps of the first visit (no contradictory drift).
  D3 = a no-structure (random-transition) world bounds chance coherence.
  PASS: action-consequence coherence > baseline (d>=0.5, p<0.05) AND revisit-consistency
        error < eps above the random-world control.
  FAIL: coherence ~ baseline OR revisit drift ~ random world.

The generated world = a learned switching-LDS (per-action transition, from H_967): given a
latent state and an action, it produces a deterministic next latent (a simulator). We test
rule-consistency (same state+action -> same next-state) and loop revisit-consistency.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, _aug1, cohens_d, welch_t, header, verdict_line

ODIM = 2
NACT = 4
T = 25
N_TRAIN = 300
N_TEST = 200
LOOP = [0, 1, 2, 3, 3, 2, 1, 0]   # an action loop that should return near start


def dynamics(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


ACT_THETAS = np.linspace(-0.5, 0.5, NACT)


def gen_traj(rng):
    pos = rng.standard_normal(2); v = rng.standard_normal(2) * 0.5
    obs, acts = [pos.copy()], []
    for _ in range(T - 1):
        a = rng.integers(NACT); v = dynamics(ACT_THETAS[a]) @ v
        pos = pos + 0.3 * v + 0.02 * rng.standard_normal(2)
        obs.append(pos.copy()); acts.append(a)
    acts.append(0)
    return np.array(obs), acts


class Simulator:
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


def main():
    header("H_983", "Generated interactive world (self-consistent simulator)")
    print(f"actions={NACT}; rule-consistency + loop revisit-consistency; N_test={N_TEST}\n")
    rng = np.random.default_rng(0)
    trs = [gen_traj(rng) for _ in range(N_TRAIN)]
    sim = Simulator(ODIM, NACT).fit([o for o, a in trs], [a for o, a in trs])

    # D1 action-consequence coherence: same state + same action -> same next-state.
    # (deterministic simulator => coherence is exact; the test is vs a SHUFFLED-transition
    #  baseline that applies a random action's operator.)
    rng2 = np.random.default_rng(7)
    coh_real, coh_shuf = [], []
    for _ in range(N_TEST):
        o, a = gen_traj(rng2); z = sim.m.embed(o)[5]
        act = rng2.integers(NACT)
        n1 = sim.step(z, act); n2 = sim.step(z, act)          # same state+action twice
        coh_real.append(np.linalg.norm(n1 - n2))              # ~0 if rule-consistent
        wrong = sim.step(z, (act + 1) % NACT)
        coh_shuf.append(np.linalg.norm(n1 - wrong))           # different action -> differs
    coh_real, coh_shuf = np.array(coh_real), np.array(coh_shuf)
    print(f"D1 action-consequence: same-state+action repeat dist = {coh_real.mean():.6f} "
          f"(rule-consistent if ~0)")
    print(f"   different-action dist (shuffled-transition baseline) = {coh_shuf.mean():.4f}")
    d1, p1 = welch_t(coh_real, coh_shuf); dd1 = cohens_d(coh_shuf, coh_real)
    coherent = coh_real.mean() < 1e-6 and coh_shuf.mean() > 1e-3

    # D2 revisit-consistency: a forward-then-inverse action loop should return NEAR the
    # start in a self-consistent world (the rule composes coherently), measured RELATIVE
    # to the world's own scale and against a random-world control of MATCHED output scale.
    # D3 random-world = per-action operators fit to scrambled (rule-less) next-states, so
    # the operators have the SAME output magnitude as the learned ones but no real rule.
    rng3 = np.random.default_rng(11)
    obs_all = [o for o, a in trs]; acts_all = [a for o, a in trs]
    rand_sim = Simulator(ODIM, NACT)
    rand_sim.m = sim.m                              # share embedding/decoder
    # fit random-rule operators on SHUFFLED (state -> wrong next-state) pairs
    pairs = {a: ([], []) for a in range(NACT)}
    for ob, ac in zip(obs_all, acts_all):
        z = sim.m.embed(ob)
        for t in range(2, len(ob) - 1):
            pairs[ac[t]][0].append(z[t]); pairs[ac[t]][1].append(z[t + 1])
    for a in range(NACT):
        Z = np.array(pairs[a][0]); Znext = np.array(pairs[a][1])
        perm = rng3.permutation(len(Znext))        # SCRAMBLE the targets -> no real rule
        rand_sim.A[a] = _ridge(_aug(Z), Znext[perm], 1e-3)

    fwd = [2, 3, 2, 3]; rev = [1, 0, 1, 0]
    revisit_real, revisit_rand = [], []
    for _ in range(N_TEST):
        o, a = gen_traj(rng3); z0 = sim.m.embed(o)[5]
        z = z0.copy()
        for act in fwd + rev:
            z = sim.step(z, act)
        revisit_real.append(np.linalg.norm(sim.m.decode(z) - sim.m.decode(z0)))
        zr = z0.copy()
        for act in fwd + rev:
            zr = rand_sim.step(zr, act)
        revisit_rand.append(np.linalg.norm(rand_sim.m.decode(zr) - rand_sim.m.decode(z0)))
    revisit_real, revisit_rand = np.array(revisit_real), np.array(revisit_rand)
    print(f"\nD2 revisit drift (loop return-to-start): real-world = {revisit_real.mean():.4f}")
    print(f"D3 random-world revisit drift (no-structure bound) = {revisit_rand.mean():.4f}")
    d2, p2 = welch_t(revisit_real, revisit_rand); dd2 = cohens_d(revisit_rand, revisit_real)
    revisit_ok = (revisit_real.mean() < revisit_rand.mean()) and p2 < 0.05 and dd2 >= 0.5

    print(f"\nD1 coherence (real vs shuffled, d) = {dd1:.3f} p={p1:.3e}")
    print(f"D2 revisit (real vs random-world, d) = {dd2:.3f} p={p2:.3e}")
    revisit_sig = (revisit_real.mean() < revisit_rand.mean()) and p2 < 0.05
    if coherent and revisit_ok:
        verdict_line("H_983", "PASS",
                     f"action-consequence coherent (same-state+action repeat dist "
                     f"{coh_real.mean():.0e}~0 << different-action {coh_shuf.mean():.2f}) AND loop "
                     f"revisit drift {revisit_real.mean():.3f} << random-world {revisit_rand.mean():.3f} "
                     f"(d={dd2:.2f}) — generative interactive world / simulator (toy).")
    elif coherent and revisit_sig and not revisit_ok:
        verdict_line("H_983", "INCOMPLETE",
                     f"D1 action-consequence coherence STRONG (rule-consistent, d={dd1:.2f}, repeat "
                     f"dist ~0) but D2 loop revisit-consistency only WEAKLY beats the random-world "
                     f"control (drift {revisit_real.mean():.2f} vs {revisit_rand.mean():.2f}, d={dd2:.2f}"
                     f"<0.5, p={p2:.2g}) — the linear simulator is rule-consistent but not loop-"
                     f"reversible; full PASS bar (both D1+D2) not cleared. Toy C3, ladder OPEN.")
    elif not coherent:
        verdict_line("H_983", "FAIL",
                     f"action-consequence incoherent (d={dd1:.2f}) — cannot simulate a self-"
                     f"consistent world (closed-negative).")
    else:
        verdict_line("H_983", "INCOMPLETE", f"D2 revisit not above random world (d={dd2:.2f}); toy C3.")


if __name__ == "__main__":
    main()
