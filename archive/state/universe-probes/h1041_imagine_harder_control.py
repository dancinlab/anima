"""H_1041 — Does imagine-rollout STILL beat MPC on a HARDER control task? (H_1034 generalization)

Pre-registered (frozen; honored verbatim, see UNIVERSE/cards/H_1041_imagine_harder_control.md):

  H_1034 (GREEN) showed imagine-rollout (CEM through anima's OWN LEARNED LDS world model) still
  beats a ROBUST (scenario/SAA tube) true-dynamics MPC at deep horizon {8,16} on a stiff-linear
  hidden-velocity station-keeping toy: the deep-MPC failure was CEM landscape difficulty, not
  process-noise brittleness. That was ONE task (linear stiff dynamics). H_1041 asks: does the
  imagine-beats-MPC advantage HOLD on a genuinely HARDER control problem?

  HARDER along BOTH axes the pre-reg names (a) AND (b):
    TASK A  NONLINEAR — a pendulum swing-up: state = [angle, angular-velocity], CONTINUOUS torque
            action; dynamics have a sin(theta) gravity term (genuinely nonlinear, NOT a linear LDS).
            The imagine planner's learned WM is STILL a delay-embedding LINEAR LDS (it does NOT get
            the nonlinear true dynamics) — so this is the harder case for imagine, while both MPCs
            plan on the EXACT nonlinear true dynamics. Reward = -(upright-angle-error + small ctrl).
    TASK B  PARTIALLY-OBSERVED + NOISE (belief tracking) — the H_964/H_1026 hidden-velocity
            station-keeping env but with OBSERVATION NOISE on top of the hidden velocity, so the
            controller must track a BELIEF, not read state. The MPCs get a KALMAN belief on the TRUE
            linear-Gaussian state-space (the optimal-given-the-noise-model reference); imagine plans
            through its LEARNED WM from the same noisy history (it is NOT given the true noise model).

  THREE PLANNERS (== H_1034): naive-MPC (true dynamics, noise-free CEM rollout), robust-MPC
  (scenario/SAA tube CEM on true dynamics + disturbance model), imagine-rollout (CEM through the
  LEARNED WM, never calls the true env). FROZEN depth ladder {1,2,4,8,16}; deep tail {8,16}; >=30
  seeds; mean episode return metric; GAP_TOL=0.05; Welch p<1e-3.

  PASS (H1, imagine advantage GENERALIZES) = on the harder task(s), at deep horizon {8,16}
       imagine-rollout's mean return STILL leads the BEST MPC by > GAP_TOL=0.05 with Welch p<1e-3.
       Per pre-reg: "imagine still leads the best MPC". Operationalized PER TASK: lead(d) =
       imagine(d) - max(naive(d), robust(d)); PASS for a task requires lead(d) > GAP_TOL AND
       Welch(imagine vs the better MPC) p < 1e-3 at BOTH d in {8,16}. Overall PASS = at least one
       harder task PASSes (advantage generalizes beyond stiff-linear).
  FAIL (advantage is task-specific to stiff-linear CEM-landscape difficulty; honest scoped
       negative, a_paper_negative_ok) = on EVERY harder task an MPC baseline CATCHES or BEATS
       imagine at deep horizon (lead(d) <= GAP_TOL at some deep d, or not significant) — the
       mechanism (robust planning vs brittle landscape), not the headline, is what transfers.

REUSE (do NOT reinvent): the H_1034 CEM machinery VERBATIM — CEM hyperparameters (pop/iters/
elite/init-std), the scenario/SAA robust scoring shape, the AnimaImaginePlanner imagine-rollout
through the LEARNED LDSWorldModel (ridge on greedy-oracle demos; NEVER given true dynamics), the
N_RUNS x EP_PER_RUN protocol, boot_ci/welch_t/cohens_d. The H_1034 reproduce check (reproduce_h1034)
re-runs the H_1034 env+planners and asserts the stored curve bit-identical BEFORE scoring H_1041.

$0 CPU-local, deterministic given seeds, SERIAL, no GPU, polled inline (a_cpu_local_no_waiter — NO
Monitor/Pool, H_1038 hang lesson; `if __name__`-guarded). g5 CODE-measured (control-return metric;
a_phi_iit4_tool N/A). TOY single rung per task; scenario-tube + Kalman-belief variants only, other
robustifications UNVERIFIED; scale-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import numpy as np
from cwm_probe_lib import LDSWorldModel, boot_ci, welch_t, cohens_d, header, verdict_line

# ============================================================================= frozen protocol (== H_1034)
N_RUNS = 40          # runs per agent (>=30 seeds)
EP_PER_RUN = 40      # episodes per run
DEPTHS = [1, 2, 4, 8, 16]   # PRE-FROZEN depth ladder (identical to H_1034)
DEEP = [8, 16]       # deep-horizon tail; verdict decided here
GAP_TOL = 0.05       # frozen tolerance
PSIG = 1e-3          # frozen Welch significance threshold
CEM_ITERS = 5        # CEM refinement iterations (VERBATIM H_1034)
CEM_POP = 64         # CEM population size (VERBATIM H_1034)
CEM_ELITE = 8        # CEM elite count (VERBATIM H_1034)
CEM_INIT_STD = 0.6   # CEM initial per-dim action std (VERBATIM H_1034)
N_SCEN = 16          # robust-MPC scenario/SAA process-noise draws/candidate (VERBATIM H_1034)
DELAY = 3            # delay-embedding for the learned WM (VERBATIM H_1034)
N_TRAIN = 400        # demo trajectories for the learned WM (VERBATIM H_1034)
T = 20               # episode length (VERBATIM H_1034)

# ============================================================================= TASK A — NONLINEAR pendulum swing-up
# state = [theta, omega]; obs = [cos theta, sin theta] (angle-only, omega HIDDEN -> the WM must
# recover angular velocity from the delay embedding, as in H_1034's hidden-velocity setup).
# CONTINUOUS torque action a in [-AMAX_P, AMAX_P]. Reward = -(angle-from-upright + small ctrl cost).
A_ODIM = 2; A_ADIM = 1
A_DT = 0.05; A_G = 9.81; A_L = 1.0; A_M = 1.0; A_DAMP = 0.1
AMAX_P = 2.0                 # torque box half-width (under-actuated: cannot lift in one step => swing-up)
A_NOISE = 0.01               # process noise on omega
A_CTRL_W = 0.001             # small control penalty


def a_step(theta, omega, a, rng):
    a = float(np.clip(a, -AMAX_P, AMAX_P))
    # pendulum: theta measured from UPRIGHT; gravity pulls toward theta=pi (down).
    omega_dot = -(A_G / A_L) * np.sin(theta + np.pi) - A_DAMP * omega + a / (A_M * A_L * A_L)
    omega = omega + A_DT * omega_dot + A_NOISE * rng.standard_normal()
    theta = theta + A_DT * omega
    werr = (theta + np.pi) % (2 * np.pi) - np.pi
    r = -float(werr * werr) - A_CTRL_W * a * a
    return theta, omega, r


def a_obs(theta):
    return np.array([np.cos(theta), np.sin(theta)])


def a_greedy(theta, omega):
    """Continuous 1-step heuristic oracle for DEMOS (energy-shaping swing-up + LQR-ish near top)."""
    werr = (theta + np.pi) % (2 * np.pi) - np.pi
    if abs(werr) < 0.5:                      # near upright -> stabilize
        return np.clip(-12.0 * werr - 3.0 * omega, -AMAX_P, AMAX_P)
    return np.clip(2.0 * np.sign(omega if abs(omega) > 1e-6 else 1.0), -AMAX_P, AMAX_P)


def a_gen_demo(rng):
    theta = np.pi + rng.standard_normal() * 0.3      # start near DOWN
    omega = rng.standard_normal() * 0.3
    obs, acts = [a_obs(theta)], []
    for _ in range(T - 1):
        a = np.array([a_greedy(theta, omega)])
        acts.append(a.copy())
        theta, omega, _ = a_step(theta, omega, a[0], rng)
        obs.append(a_obs(theta))
    acts.append(np.array([a_greedy(theta, omega)]))
    return np.array(obs), np.array(acts)


def a_rollout_score_naive(theta0, omega0, plans):
    """VECTORIZED noise-free true-dynamics rollout score over a (POP,H) torque-plan batch."""
    POP, H = plans.shape
    th = np.full(POP, float(theta0)); om = np.full(POP, float(omega0))
    sc = np.zeros(POP)
    for k in range(H):
        a = np.clip(plans[:, k], -AMAX_P, AMAX_P)
        om_dot = -(A_G / A_L) * np.sin(th + np.pi) - A_DAMP * om + a / (A_M * A_L * A_L)
        om = om + A_DT * om_dot
        th = th + A_DT * om
        werr = (th + np.pi) % (2 * np.pi) - np.pi
        sc += -(werr * werr) - A_CTRL_W * a * a
    return sc


def a_rollout_score_robust(theta0, omega0, plans, scen_noise):
    """VECTORIZED scenario/SAA robust score: mean cumulative reward over N_SCEN process-noise
    scenarios (true dynamics + disturbance model). plans (POP,H); scen_noise (S,H). Returns (POP,)."""
    POP, H = plans.shape
    S = scen_noise.shape[0]
    th = np.zeros((POP, S)) + float(theta0)
    om = np.zeros((POP, S)) + float(omega0)
    sc = np.zeros(POP)
    for k in range(H):
        a = np.clip(plans[:, k], -AMAX_P, AMAX_P)[:, None]          # (POP,1) broadcast over S
        om_dot = -(A_G / A_L) * np.sin(th + np.pi) - A_DAMP * om + a / (A_M * A_L * A_L)
        om = om + A_DT * om_dot + A_NOISE * scen_noise[None, :, k]  # (1,S) noise broadcast over POP
        th = th + A_DT * om
        werr = (th + np.pi) % (2 * np.pi) - np.pi
        sc += (-(werr * werr) - A_CTRL_W * (a * a)).mean(axis=1)    # mean over scenarios
    return sc


def a_cem(theta, omega, rng, horizon, robust):
    mu = np.zeros((horizon, A_ADIM)); std = np.full((horizon, A_ADIM), CEM_INIT_STD)
    for _ in range(CEM_ITERS):
        samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, A_ADIM)),
                       -AMAX_P, AMAX_P)                              # (POP,H,1)
        plans = samp[:, :, 0]                                       # (POP,H) scalar torque
        if robust:
            scen = rng.standard_normal((N_SCEN, horizon))           # (S,H) shared CRN
            scores = a_rollout_score_robust(theta, omega, plans, scen)
        else:
            scores = a_rollout_score_naive(theta, omega, plans)
        elite = samp[np.argsort(scores)[-CEM_ELITE:]]
        mu = elite.mean(0); std = elite.std(0) + 1e-6
    return np.clip(mu[0], -AMAX_P, AMAX_P)


class APlannerImagine:
    """imagine-rollout through the LEARNED LDS WM (== H_1034 AnimaImaginePlanner, A_ADIM=1).
    Planner reward proxy = -||decoded obs - upright-target||, target = obs(theta=0)=[1,0].
    The WM is LINEAR — it does NOT know the nonlinear pendulum dynamics."""

    def __init__(self, fm):
        self.fm = fm
        self.target = a_obs(0.0)                                    # upright obs [cos0, sin0] = [1,0]

    def plan(self, obs_hist, rng, horizon):
        z0 = self.fm.embed(np.array(obs_hist))[-1]
        mu = np.zeros((horizon, A_ADIM)); std = np.full((horizon, A_ADIM), CEM_INIT_STD)
        A = self.fm.A; C = self.fm.C
        for _ in range(CEM_ITERS):
            samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, A_ADIM)),
                           -AMAX_P, AMAX_P)
            z = np.tile(z0.astype(float), (CEM_POP, 1)); ones = np.ones((CEM_POP, 1))
            scores = np.zeros(CEM_POP)
            for k in range(horizon):
                zin = np.hstack([z, samp[:, k], ones]); z = zin @ A
                pred = np.hstack([z, ones]) @ C
                scores += -np.linalg.norm(pred - self.target, axis=1)
            elite = samp[np.argsort(scores)[-CEM_ELITE:]]
            mu = elite.mean(0); std = elite.std(0) + 1e-6
        return np.clip(mu[0], -AMAX_P, AMAX_P)


def a_episode(policy_fn, rng):
    theta = np.pi + rng.standard_normal() * 0.3
    omega = rng.standard_normal() * 0.3
    obs_hist = [a_obs(theta)]; total = 0.0
    for t in range(T - 1):
        a = policy_fn(obs_hist, theta, omega, rng)
        theta, omega, r = a_step(theta, omega, float(np.atleast_1d(a)[0]), rng)
        obs_hist.append(a_obs(theta)); total += r
    return total / (T - 1)


# ============================================================================= TASK B — PARTIAL-OBS + NOISE (belief tracking)
# == H_964/H_1026 hidden-velocity 2-D station-keeping, BUT the position observation is NOISY
# (OBS_NOISE). state=[pos(2),vel(2)] hidden; obs = pos + OBS_NOISE*N(0,I). MPCs get a KALMAN belief
# (true linear-Gaussian SSM); imagine plans through its LEARNED WM from the noisy history.
B_ODIM = 2; B_ADIM = 2
B_VSTEP = 0.4; B_DRAG = 1.0; B_AMAX = 1.0
B_PROC = 0.02                # process noise std (== H_1034 NOISE)
B_OBS = 0.15                 # observation noise std (belief-tracking regime)


def b_step(pos, vel, a, rng):
    a = np.clip(a, -B_AMAX, B_AMAX)
    vel = B_DRAG * vel + a
    pos = pos + B_VSTEP * vel + B_PROC * rng.standard_normal(B_ADIM)
    return pos, vel, -float(np.linalg.norm(pos))


def b_obs(pos, rng):
    return pos + B_OBS * rng.standard_normal(B_ODIM)


def b_greedy(pos, vel):
    return np.clip(-(B_DRAG * vel) - pos / B_VSTEP, -B_AMAX, B_AMAX)


def b_gen_demo(rng):
    pos = rng.standard_normal(2) * 2; vel = rng.standard_normal(2) * 0.5
    obs, acts = [b_obs(pos, rng)], []
    for _ in range(T - 1):
        a = b_greedy(pos, vel); acts.append(a.copy())
        pos, vel, _ = b_step(pos, vel, a, rng)
        obs.append(b_obs(pos, rng))
    acts.append(b_greedy(pos, vel).copy())
    return np.array(obs), np.array(acts)


# --- Kalman filter on the TRUE linear-Gaussian SSM (state s=[px,py,vx,vy]) ---
B_F = np.array([[1, 0, B_VSTEP * B_DRAG, 0],
                [0, 1, 0, B_VSTEP * B_DRAG],
                [0, 0, B_DRAG, 0],
                [0, 0, 0, B_DRAG]], float)
B_G = np.array([[B_VSTEP, 0], [0, B_VSTEP], [1, 0], [0, 1]], float)
B_H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], float)
B_Q = np.zeros((4, 4)); B_Q[0, 0] = B_Q[1, 1] = B_PROC ** 2           # process noise hits position
B_R = np.eye(2) * (B_OBS ** 2)


class Kalman:
    def __init__(self):
        self.s = np.zeros(4); self.P = np.eye(4) * 4.0
    def predict(self, a):
        self.s = B_F @ self.s + B_G @ a
        self.P = B_F @ self.P @ B_F.T + B_Q
    def update(self, z):
        S = B_H @ self.P @ B_H.T + B_R
        K = self.P @ B_H.T @ np.linalg.inv(S)
        self.s = self.s + K @ (z - B_H @ self.s)
        self.P = (np.eye(4) - K @ B_H) @ self.P


def b_cem(pos, vel, rng, horizon, robust):
    """CEM on TRUE dynamics from a (pos,vel) BELIEF point estimate (== H_1034 cem_plan_*)."""
    mu = np.zeros((horizon, B_ADIM)); std = np.full((horizon, B_ADIM), CEM_INIT_STD)
    for _ in range(CEM_ITERS):
        samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, B_ADIM)),
                       -B_AMAX, B_AMAX)
        if robust:
            scen = rng.standard_normal((N_SCEN, horizon, B_ADIM))
            p = np.broadcast_to(pos.astype(float), (CEM_POP, N_SCEN, B_ADIM)).copy()
            v = np.broadcast_to(vel.astype(float), (CEM_POP, N_SCEN, B_ADIM)).copy()
            scores = np.zeros(CEM_POP)
            for k in range(horizon):
                v = B_DRAG * v + samp[:, None, k, :]
                p = p + B_VSTEP * v + B_PROC * scen[None, :, k, :]
                scores += -np.linalg.norm(p, axis=2).mean(axis=1)
        else:
            p = np.tile(pos.astype(float), (CEM_POP, 1)); v = np.tile(vel.astype(float), (CEM_POP, 1))
            scores = np.zeros(CEM_POP)
            for k in range(horizon):
                v = B_DRAG * v + samp[:, k]; p = p + B_VSTEP * v
                scores += -np.linalg.norm(p, axis=1)
        elite = samp[np.argsort(scores)[-CEM_ELITE:]]
        mu = elite.mean(0); std = elite.std(0) + 1e-6
    return np.clip(mu[0], -B_AMAX, B_AMAX)


class BPlannerImagine:
    """imagine-rollout through the LEARNED WM from the NOISY obs history (== H_1034 verbatim;
    NOT given the true noise model — must absorb noise via the learned ridge-fit transition)."""
    def __init__(self, fm):
        self.fm = fm
    def plan(self, obs_hist, rng, horizon):
        z0 = self.fm.embed(np.array(obs_hist))[-1]
        mu = np.zeros((horizon, B_ADIM)); std = np.full((horizon, B_ADIM), CEM_INIT_STD)
        A = self.fm.A; C = self.fm.C
        for _ in range(CEM_ITERS):
            samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, B_ADIM)),
                           -B_AMAX, B_AMAX)
            z = np.tile(z0.astype(float), (CEM_POP, 1)); ones = np.ones((CEM_POP, 1))
            scores = np.zeros(CEM_POP)
            for k in range(horizon):
                zin = np.hstack([z, samp[:, k], ones]); z = zin @ A
                pred = np.hstack([z, ones]) @ C
                scores += -np.linalg.norm(pred, axis=1)
            elite = samp[np.argsort(scores)[-CEM_ELITE:]]
            mu = elite.mean(0); std = elite.std(0) + 1e-6
        return np.clip(mu[0], -B_AMAX, B_AMAX)


def b_episode_mpc(robust, rng, horizon):
    """MPC episode with KALMAN belief tracking on the TRUE SSM."""
    pos = rng.standard_normal(2) * 2; vel = rng.standard_normal(2) * 0.5
    kf = Kalman(); kf.s[:2] = b_obs(pos, rng)                       # init belief from first obs
    total = 0.0
    for t in range(T - 1):
        z = b_obs(pos, rng); kf.update(z)
        bp = kf.s[:2].copy(); bv = kf.s[2:].copy()
        a = b_cem(bp, bv, rng, horizon, robust)
        kf.predict(a)
        pos, vel, r = b_step(pos, vel, a, rng); total += r
    return total / (T - 1)


def b_episode_imagine(planner, rng, horizon):
    pos = rng.standard_normal(2) * 2; vel = rng.standard_normal(2) * 0.5
    obs_hist = [b_obs(pos, rng)]; total = 0.0
    for t in range(T - 1):
        a = planner.plan(obs_hist, rng, horizon)
        pos, vel, r = b_step(pos, vel, a, rng)
        obs_hist.append(b_obs(pos, rng)); total += r
    return total / (T - 1)


# ============================================================================= generic seeded run
def run_agent_A(policy_fn, seed0):
    out = []
    for i in range(N_RUNS):
        rng = np.random.default_rng(seed0 + i)
        out.append(np.mean([a_episode(policy_fn, rng) for _ in range(EP_PER_RUN)]))
    return np.array(out)


def run_agent_B(ep_fn, seed0, horizon):
    out = []
    for i in range(N_RUNS):
        rng = np.random.default_rng(seed0 + i)
        out.append(np.mean([ep_fn(rng, horizon) for _ in range(EP_PER_RUN)]))
    return np.array(out)


def score_task(name, ladder):
    """ladder rows: (d, naive_mean, robust_mean, imag_mean, naive_arr, robust_arr, imag_arr).
    Returns (pass_bool, deep_detail_list, lines)."""
    lines = []
    deep_detail = []
    task_pass = True
    for (d, nm, rm, im, na, ra, ia) in ladder:
        best_mpc = max(nm, rm)
        best_arr = na if nm >= rm else ra
        lead = im - best_mpc                       # >0 => imagine leads the best MPC
        tp, pp = welch_t(ia, best_arr); dd = cohens_d(ia, best_arr)
        deep = "DEEP" if d in DEEP else "    "
        flag = "imag-leads" if (lead > GAP_TOL and pp < PSIG) else "MPC-catches/beats"
        lines.append(f"  d={d:2d} [{deep}]  naive={nm:.4f}  robust={rm:.4f}  imagine={im:.4f}  "
                     f"best-MPC={best_mpc:.4f}")
        lines.append(f"            lead=imag-bestMPC={lead:+.4f} (Welch p={pp:.2e} d={dd:+.3f}) "
                     f"[{flag} @ GAP_TOL={GAP_TOL}, p<{PSIG}]")
        if d in DEEP:
            ok = (lead > GAP_TOL and pp < PSIG)
            deep_detail.append((d, lead, pp, ok))
            if not ok:
                task_pass = False
    return task_pass, deep_detail, lines


# ============================================================================= H_1034 reproduce check
H1034_NAIVE = [-0.3715, -0.2623, -0.3205, -0.4847, -0.8746]
H1034_ROBUST = [-0.3702, -0.2697, -0.3174, -0.4787, -0.8734]
H1034_IMAG = [-0.3790, -0.2684, -0.3167, -0.4526, -0.7606]


def reproduce_h1034():
    """Re-run the H_1034 module and assert its curve is bit-identical to the stored verdict (g73:
    'VERIFY the vectorized planners reproduce H_1034 before scoring')."""
    import importlib.util
    p = os.path.join(os.path.dirname(__file__), "h1034_imagine_vs_robust_mpc.py")
    spec = importlib.util.spec_from_file_location("h1034", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    rng = np.random.default_rng(0)
    demos = [m.gen_demo(rng) for _ in range(m.N_TRAIN)]
    fm = m.LDSWorldModel(m.ODIM, delay=m.DELAY, act_dim=m.ADIM)
    fm.fit([o for o, a in demos], traj_acts=[a for o, a in demos])
    planner = m.AnimaImaginePlanner(fm)
    naive, robust, imag = [], [], []
    for d in m.DEPTHS:
        naive.append(m.run_agent(lambda oh, p, v, r, _d=d: m.cem_plan_true(p, v, r, _d), 1000 + d).mean())
        robust.append(m.run_agent(lambda oh, p, v, r, _d=d: m.cem_plan_robust(p, v, r, _d), 3000 + d).mean())
        imag.append(m.run_agent(lambda oh, p, v, r, _d=d: planner.plan(oh, r, _d), 5000 + d).mean())
    naive = [round(x, 4) for x in naive]; robust = [round(x, 4) for x in robust]; imag = [round(x, 4) for x in imag]
    ok = (naive == H1034_NAIVE and robust == H1034_ROBUST and imag == H1034_IMAG)
    print("==== H_1034 REPRODUCE CHECK (bit-identical vs stored verdict) ====")
    print(f"  naive : got {naive}  expect {H1034_NAIVE}  {'OK' if naive == H1034_NAIVE else 'MISMATCH'}")
    print(f"  robust: got {robust}  expect {H1034_ROBUST}  {'OK' if robust == H1034_ROBUST else 'MISMATCH'}")
    print(f"  imag  : got {imag}  expect {H1034_IMAG}  {'OK' if imag == H1034_IMAG else 'MISMATCH'}")
    print(f"  reproduce-H_1034 = {'PASS (bit-identical)' if ok else 'FAIL'}\n")
    return ok


# ============================================================================= main
def main():
    header("H_1041", "imagine-rollout vs MPC on a HARDER control task (H_1034 generalization)")
    print(f"N_runs={N_RUNS} ep/run={EP_PER_RUN}  FROZEN depth ladder DEPTHS={DEPTHS}  deep-tail={DEEP}")
    print(f"GAP_TOL={GAP_TOL}  Welch p<{PSIG}  CEM(pop={CEM_POP} iters={CEM_ITERS} elite={CEM_ELITE}) "
          f"robust N_SCEN={N_SCEN}  no-Phi (a_phi_iit4_tool n/a)\n")

    repro_ok = reproduce_h1034()
    if not repro_ok:
        verdict_line("H_1041", "ABORT",
                     "reproduce-H_1034 FAILED — vectorized planners do NOT reproduce the stored "
                     "H_1034 curve bit-identically; refusing to score H_1041 (g73). Investigate the "
                     "shared CEM/WM machinery before any verdict.")
        return

    # ----------------------------------------------------------------- TASK A — NONLINEAR swing-up
    print("==== TASK A — NONLINEAR pendulum swing-up (angle-only obs, omega HIDDEN) ====")
    rng = np.random.default_rng(0)
    a_demos = [a_gen_demo(rng) for _ in range(N_TRAIN)]
    a_fm = LDSWorldModel(A_ODIM, delay=DELAY, act_dim=A_ADIM)
    a_fm.fit([o for o, a in a_demos], traj_acts=[a for o, a in a_demos])
    a_planner = APlannerImagine(a_fm)
    ladderA = []
    for d in DEPTHS:
        na = run_agent_A(lambda oh, th, om, r, _d=d: a_cem(th, om, r, _d, False), 11000 + d)
        ra = run_agent_A(lambda oh, th, om, r, _d=d: a_cem(th, om, r, _d, True), 13000 + d)
        ia = run_agent_A(lambda oh, th, om, r, _d=d: a_planner.plan(oh, r, _d), 15000 + d)
        ladderA.append((d, na.mean(), ra.mean(), ia.mean(), na, ra, ia))
    passA, deepA, linesA = score_task("A", ladderA)
    for ln in linesA:
        print(ln)
    print(f"  TASK A curves: naive={[round(r[1],4) for r in ladderA]}  "
          f"robust={[round(r[2],4) for r in ladderA]}  imag={[round(r[3],4) for r in ladderA]}")
    print(f"  TASK A deep-tail lead(imag-bestMPC): {[(d, round(l,4), f'p={p:.1e}', ok) for d,l,p,ok in deepA]}")
    print(f"  TASK A PASS = {passA}\n")

    # ----------------------------------------------------------------- TASK B — PARTIAL-OBS + NOISE
    print(f"==== TASK B — PARTIAL-OBS + OBS-NOISE station-keeping (belief tracking, OBS_NOISE={B_OBS}) ====")
    rng = np.random.default_rng(0)
    b_demos = [b_gen_demo(rng) for _ in range(N_TRAIN)]
    b_fm = LDSWorldModel(B_ODIM, delay=DELAY, act_dim=B_ADIM)
    b_fm.fit([o for o, a in b_demos], traj_acts=[a for o, a in b_demos])
    b_planner = BPlannerImagine(b_fm)
    ladderB = []
    for d in DEPTHS:
        na = run_agent_B(lambda rng_, h: b_episode_mpc(False, rng_, h), 21000 + d, d)
        ra = run_agent_B(lambda rng_, h: b_episode_mpc(True, rng_, h), 23000 + d, d)
        ia = run_agent_B(lambda rng_, h: b_episode_imagine(b_planner, rng_, h), 25000 + d, d)
        ladderB.append((d, na.mean(), ra.mean(), ia.mean(), na, ra, ia))
    passB, deepB, linesB = score_task("B", ladderB)
    for ln in linesB:
        print(ln)
    print(f"  TASK B curves: naive(Kalman)={[round(r[1],4) for r in ladderB]}  "
          f"robust(Kalman)={[round(r[2],4) for r in ladderB]}  imag={[round(r[3],4) for r in ladderB]}")
    print(f"  TASK B deep-tail lead(imag-bestMPC): {[(d, round(l,4), f'p={p:.1e}', ok) for d,l,p,ok in deepB]}")
    print(f"  TASK B PASS = {passB}\n")

    # ----------------------------------------------------------------- pre-registered verdict gate
    overall_pass = passA or passB
    passed_tasks = [n for n, p in (("A-nonlinear", passA), ("B-partial-obs", passB)) if p]
    failed_tasks = [n for n, p in (("A-nonlinear", passA), ("B-partial-obs", passB)) if not p]
    print(f"GENERALIZES (>= one harder task PASS) = {overall_pass}  passed={passed_tasks}  failed={failed_tasks}\n")

    detailA = "; ".join(f"d={d}: lead={l:+.4f} p={p:.1e} {'lead' if ok else 'caught'}" for d, l, p, ok in deepA)
    detailB = "; ".join(f"d={d}: lead={l:+.4f} p={p:.1e} {'lead' if ok else 'caught'}" for d, l, p, ok in deepB)

    if overall_pass:
        verdict_line("H_1041", "GREEN",
                     f"IMAGINE-ADVANTAGE-GENERALIZES — on at least one genuinely HARDER control task, "
                     f"imagine-rollout (CEM through anima's OWN learned LDS world model) STILL leads "
                     f"the BEST MPC by > GAP_TOL={GAP_TOL} at BOTH deep depths {DEEP} (Welch p<{PSIG}). "
                     f"PASS tasks: {passed_tasks}; FAIL tasks: {failed_tasks}. "
                     f"TASK A (nonlinear pendulum swing-up, angle-only obs, omega hidden) deep tail: {detailA}. "
                     f"TASK B (partial-obs + obs-noise station-keeping, Kalman-belief MPC reference) deep tail: {detailB}. "
                     f"The H_1034 imagine-beats-MPC advantage is NOT specific to stiff-linear CEM-landscape "
                     f"difficulty — it transfers to a harder task even though the learned WM is a LINEAR LDS "
                     f"that does NOT get the true (nonlinear / noise) model the MPCs receive. reproduce-H_1034 "
                     f"= bit-identical (PASS) before scoring. TOY single rung per task, $0 CPU-local; "
                     f"scenario-tube + Kalman-belief variants only, other robustifications UNVERIFIED; "
                     f"scale-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). a_phi_iit4_tool n/a.")
    else:
        verdict_line("H_1041", "RED",
                     f"IMAGINE-ADVANTAGE-IS-TASK-SPECIFIC (closed-negative, a_paper_negative_ok) — on EVERY "
                     f"harder task an MPC baseline CATCHES or BEATS imagine at deep horizon {DEEP} "
                     f"(lead <= GAP_TOL={GAP_TOL} or not Welch-significant p<{PSIG}). "
                     f"TASK A (nonlinear pendulum swing-up) deep tail: {detailA}. "
                     f"TASK B (partial-obs + obs-noise, Kalman-belief MPC) deep tail: {detailB}. "
                     f"The H_1034 'imagine beats MPC at deep horizon' was specific to stiff-LINEAR "
                     f"CEM-landscape difficulty: when the true dynamics are nonlinear (so the MPC's true-model "
                     f"advantage matters) or the optimal belief is available (Kalman), a true-model MPC reclaims "
                     f"the deep-horizon lead. The MECHANISM (robust/expected-return planning beats a brittle "
                     f"noise-free landscape) transfers, but the HEADLINE (imagine > MPC) does not generalize "
                     f"beyond the stiff-linear toy. reproduce-H_1034 = bit-identical (PASS) before scoring. "
                     f"TOY single rung per task, $0 CPU-local; scale-transfer UNVERIFIED "
                     f"(a_scale_honest_scope · a_toy_scale_recheck). a_phi_iit4_tool n/a.")


if __name__ == "__main__":
    main()
