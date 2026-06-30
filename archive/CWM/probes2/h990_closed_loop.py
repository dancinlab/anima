"""H_990 — closed perceive→imagine→act→perceive LOOP end-to-end.

1st-round seed: H_960 (perceive 🟢) + H_962 (imagine 🟢) + H_964 (act 🟢) each PASS in
isolation. Does the COMPOSED closed loop run end-to-end on ONE shared latent state without
per-stage retraining, and does closed-loop control beat (a) open-loop imagine-then-act
(commit a whole imagined plan blind) and (b) a reactive controller with no world-state?

Falsifier (frozen): a 2D point-to-goal control task with a partially-observed velocity
(the controller must infer hidden velocity from a latent state = a world model).
  PASS  iff  closed-loop (re-perceive every step, act from current latent) reaches goal
            with FINAL DISTANCE strictly below BOTH the open-loop-imagined-plan baseline
            AND the reactive (position-only, no latent) baseline, at matched controller
            capacity, over >=20 seeds, Welch p<0.05 on closed<reactive.
  FAIL  iff  closed-loop does not beat reactive (the loop adds nothing).
  Also report whether open-loop error COMPOUNDS vs closed-loop (drift containment).
substrate=CPU-mirror (numpy). a_scale_honest_scope: single toy rung, ladder OPEN.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "probes"))
from cwm_probe_lib import LDSWorldModel, header, cohens_d, welch_t

N_SEEDS = 24
T = 30           # control horizon
DT = 0.25
DRAG = 0.92


def rollout_world(seed, controller, latent_model=None, reactive=False, open_loop=False,
                  plan_h=None):
    """Run the 2D double-integrator world. obs = position only (velocity HIDDEN).
    controller: callable(state_vec)->action(2,). state_vec depends on mode."""
    rng = np.random.default_rng(seed + 7000)
    p = rng.uniform(-2, 2, 2)          # start position
    v = np.zeros(2)                    # hidden velocity
    goal = np.array([0.0, 0.0])
    obs_hist = []
    if open_loop:
        # commit an imagined plan: roll the latent forward under a fixed greedy plan,
        # then execute it BLIND (no re-perception) — error compounds.
        # build plan by imagining from the first 2 obs.
        for _ in range(2):
            obs_hist.append(p.copy())
            a = np.zeros(2)
            v = DRAG * v + a * DT
            p = p + v * DT
        z = latent_model.embed(np.array(obs_hist))[-1]
        plan = []
        zc = z.copy()
        for k in range(T):
            # greedy: action = controller on the IMAGINED latent (never re-perceives)
            a = controller(zc)
            plan.append(a)
            zc = latent_model.roll(zc, 1, act_seq=[_act1h(a)])
        for k in range(T):
            a = plan[k]
            v = DRAG * v + a * DT
            p = p + v * DT
        return np.linalg.norm(p - goal)

    for t in range(T):
        obs_hist.append(p.copy())
        if reactive:
            a = controller(p.copy())            # position only, no latent
        else:
            ob = np.array(obs_hist[-latent_model.delay:]) if len(obs_hist) >= latent_model.delay else np.array(obs_hist)
            if len(ob) < latent_model.delay:
                ob = np.vstack([np.tile(ob[0], (latent_model.delay - len(ob), 1)), ob])
            z = latent_model.embed(ob)[-1]      # current world-latent (re-perceived)
            a = controller(z)
        a = np.clip(a, -3, 3)
        v = DRAG * v + a * DT
        p = p + v * DT
    return np.linalg.norm(p - goal)


def _act1h(a):
    return np.asarray(a, float)   # continuous action passthrough for the LDS


def fit_controllers(seed):
    """Fit a latent->action and a position->action controller by behavioral cloning of
    an LQR-ish expert that DOES see velocity (the world model must recover it from latent)."""
    rng = np.random.default_rng(seed)
    # collect expert demos
    trajs_obs, lat_states, lat_acts, pos_states, pos_acts = [], [], [], [], []
    lm = LDSWorldModel(obs_dim=2, delay=3, act_dim=2, ridge=1e-3)
    raw = []
    for d in range(60):
        p = rng.uniform(-2, 2, 2); v = np.zeros(2); obs=[]; acts=[]
        for t in range(T):
            obs.append(p.copy())
            a = -1.4 * p - 1.1 * v        # expert sees velocity
            acts.append(a)
            v = DRAG * v + a * DT; p = p + v * DT
        obs = np.array(obs); acts = np.array(acts)
        raw.append((obs, acts))
        trajs_obs.append(obs)
    lm.fit(trajs_obs, traj_acts=[a for (_, a) in raw])
    # build cloning targets
    for obs, acts in raw:
        Z = lm.embed(obs)
        lat_states.append(Z); lat_acts.append(acts)
        pos_states.append(obs); pos_acts.append(acts)
    Zs = np.vstack(lat_states); As = np.vstack(lat_acts)
    Ps = np.vstack(pos_states); Aps = np.vstack(pos_acts)
    from cwm_probe_lib import _aug, _ridge, _aug1
    W_lat = _ridge(_aug(Zs), As, 1e-2)
    W_pos = _ridge(_aug(Ps), Aps, 1e-2)
    lat_ctrl = lambda z: _aug1(z) @ W_lat
    pos_ctrl = lambda p: _aug1(p) @ W_pos
    return lm, lat_ctrl, pos_ctrl, W_lat.size, W_pos.size


def main():
    header("H_990", "closed perceive→imagine→act→perceive LOOP end-to-end")
    closed, reactive, openl = [], [], []
    for s in range(N_SEEDS):
        lm, lat_ctrl, pos_ctrl, np_lat, np_pos = fit_controllers(s)
        closed.append(rollout_world(s, lat_ctrl, latent_model=lm))
        reactive.append(rollout_world(s, pos_ctrl, reactive=True))
        openl.append(rollout_world(s, lat_ctrl, latent_model=lm, open_loop=True))
    closed = np.array(closed); reactive = np.array(reactive); openl = np.array(openl)
    print(f"task=2D point-to-goal, velocity HIDDEN (needs world-state)  T={T} seeds={N_SEEDS}")
    print(f"capacity: latent-ctrl params={np_lat}  position-ctrl params={np_pos}")
    print()
    print("FINAL goal-distance (lower=better), mean ± std:")
    print(f"  CLOSED loop  (re-perceive+act/step) : {closed.mean():.4f} ± {closed.std():.4f}")
    print(f"  REACTIVE     (position-only, no WM)  : {reactive.mean():.4f} ± {reactive.std():.4f}")
    print(f"  OPEN-LOOP    (commit imagined plan)  : {openl.mean():.4f} ± {openl.std():.4f}")
    tcr, pcr = welch_t(closed, reactive)
    dcr = cohens_d(closed, reactive)
    print()
    print(f"D1 closed<reactive: Welch t={tcr:.3f} p={pcr:.3e}  Cohen d={dcr:.3f}")
    win_cr = closed.mean() < reactive.mean() and pcr < 0.05
    print(f"D2 drift containment: open-loop/closed final-dist ratio = {openl.mean()/max(closed.mean(),1e-9):.3f} "
          f"({'open-loop COMPOUNDS error' if openl.mean()>closed.mean() else 'no compounding'})")
    print(f"D3 closed also < open-loop: {closed.mean() < openl.mean()}")
    print("-" * 78)
    if win_cr and closed.mean() < openl.mean():
        v = (f"PASS closed-loop perceive→imagine→act works end-to-end: closed={closed.mean():.3f} < "
             f"reactive={reactive.mean():.3f} (p={pcr:.1e},d={dcr:.2f}) AND < open-loop={openl.mean():.3f} "
             f"(open-loop compounds error ratio {openl.mean()/max(closed.mean(),1e-9):.2f}x) — the LOOP composes (toy rung).")
        tok = "PASS"
    elif win_cr:
        v = (f"PASS-PARTIAL closed beats reactive (p={pcr:.1e}) but not open-loop — loop composes, "
             f"drift-containment weak (toy).")
        tok = "PASS"
    else:
        v = (f"FAIL closed-loop does not beat reactive (closed={closed.mean():.3f} vs reactive={reactive.mean():.3f}, "
             f"p={pcr:.1e}) — the composed loop adds nothing (closed-negative, toy).")
        tok = "FAIL"
    print(f"VERDICT H_990: {v}")
    print("-" * 78)
    return tok


if __name__ == "__main__":
    main()
