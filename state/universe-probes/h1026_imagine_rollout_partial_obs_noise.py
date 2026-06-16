"""H_1026 — under PARTIAL OBSERVATION *plus* OBSERVATION NOISE, does planning THROUGH
anima's LEARNED world-model still reach the noise-aware MPC optimum, or does learned-model
forward-error compound and BREAK the H_1021 / H_1025 parity (and at what noise level)?

LINEAGE / REUSE (do NOT reinvent):
  H_1021 (PASS, discrete-action) and H_1025 (PASS, CONTINUOUS-action) both showed that planning
  through anima's OWN learned LDS world-model reaches depth-4 MPC parity on a hidden-velocity
  station-keeping env whose observations were CLEAN (only velocity was hidden -> partial obs, but
  position read exactly). Real perception is NOISY *and* partially observed. H_1026 REUSES the
  H_1025 continuous-action machinery verbatim -- the H_964 hidden-velocity env, the LEARNED
  LDSWorldModel (ridge on greedy-oracle demos, NEVER given the true dynamics), the CEM continuous
  planner, the single-step ridge head, and the H_1019/H_1021/H_1025 multi-seed protocol -- and adds
  the ONE pre-registered change: a frozen OBSERVATION-NOISE sweep. At each noise level the agent
  sees pos + obs_noise*N(0,I) (position is now BOTH partially observed -- velocity hidden -- AND
  noisy); it must infer the hidden state from the NOISY history before planning.

REFERENCE (noise-aware): a KALMAN-belief MPC on the TRUE dynamics + the TRUE noise model. A Kalman
  filter (correct linear-Gaussian state-space: state=[pos;vel], known A_dyn/B/Q/R) produces the MMSE
  belief from the noisy observation history; the SAME CEM-MPC as H_1025 then plans on the true
  dynamics from that filtered belief. This is the optimal-given-the-noise-model reference -- it KNOWS
  the noise model; anima's learned WM does NOT. Band = [Kalman-MPC - TOL, +TOL], recomputed PER noise
  level (the optimum itself degrades with noise, so parity is measured against the noise-aware ceiling
  at each level, not the noiseless one).

FROZEN FALSIFIER (pre-registered 2026-06-07 in H_1026_*.md; honored verbatim):
  metric M = mean episode return (0 = optimal, more negative = worse). TOL = 0.05 (frozen, == H_1025).
  Pre-frozen observation-noise grid OBS_NOISE_GRID (below). Multi-seed (N_RUNS x EP_PER_RUN, == H_1025).
  At each noise sigma: ceiling = Kalman-belief CEM-MPC (true dyn + true noise model); band=[P-TOL,P+TOL];
  ladder = random/reactive floors -> single-step head -> imagine-rollout (CEM through LEARNED WM) -> band.
  PASS  = NOISE-ROBUST-PARITY : imagine-rollout stays WITHIN the noise-aware band up to a STATED noise
          level sigma*, AND degrades MONOTONICALLY (not a cliff) beyond it.
  FAIL  = NOISE-BREAKS-PARITY : parity lost even at LOW noise / degrades CATASTROPHICALLY (a cliff)
          (closed-negative, a_paper_negative_ok) -- bounds H_1021/H_1025 to (near-)noiseless control.

  Operationalization of the frozen words (decided BEFORE running, fixed here):
   * "within the band up to a stated noise level" = sigma* := the LARGEST grid sigma at which
     imagine-rollout's mean is within [P-TOL,P+TOL] for that sigma AND every smaller grid sigma is
     also within-band (a contiguous parity plateau from sigma=0).
   * "low noise" = the two smallest NON-ZERO grid sigmas. parity must HOLD at sigma=0 (sanity, == H_1025
     regime at OBS_NOISE=0) and at least at the smallest non-zero sigma, else NOISE-BREAKS-PARITY.
   * "monotone (not a cliff)" = beyond sigma*, the imagine return curve is non-increasing within CI
     tolerance (each step's drop <= MONO_TOL OR overlapping CIs) AND no single one-grid-step drop
     exceeds CLIFF_FRAC of the total noiseless->max-noise span (a cliff = one step eats > CLIFF_FRAC).
   * a contiguous parity plateau covering at least sigma=0 and the smallest non-zero sigma, with the
     subsequent degradation monotone (not a cliff), = NOISE-ROBUST-PARITY (PASS).

$0 CPU-local, deterministic given seeds, serial, polled inline (a_cpu_local_no_waiter -- NO Monitor).
No GPU. No Phi claim (a_phi_iit4_tool n/a -- this is a control/robustness probe, not a Phi probe).
a_scale_honest_scope: TOY single env; learned model NOT given the true noise model; scale-transfer +
real-sensor noise UNVERIFIED.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, _aug1, boot_ci, welch_t, cohens_d, header, verdict_line

# ----------------------------------------------------------------- env constants (== H_1025 continuous H_964)
ODIM = 2             # observation = position (2-D); velocity is HIDDEN (partial obs, as in H_964/H_1025)
ADIM = 2             # CONTINUOUS action = thrust vector (2-D)
T = 20               # episode length (== H_1019/H_1021/H_1025)
N_TRAIN = 400        # demo trajectories (== H_964/H_1021/H_1025)
VSTEP = 0.4          # position integration step (== H_964)
DRAG = 1.0           # velocity FULLY persists -> must counter the HIDDEN velocity (== H_964)
AMAX = 1.0           # action box half-width: a in [-AMAX, AMAX]^2
PROC_NOISE = 0.02    # PROCESS noise std on position (== H_964 step_env NOISE; held fixed, not swept)
DELAY = 3            # delay-embedding (== anima's H_964/H_1019/H_1021/H_1025 WM)

# ----------------------------------------------------------------- frozen protocol constants
N_RUNS = 40          # runs per agent per noise level (== H_1019/H_1021/H_1025)
EP_PER_RUN = 60      # episodes per run (== H_1019/H_1021/H_1025)
TOL = 0.05           # pre-registered parity band half-width (frozen 2026-06-07; == H_1025)
HORIZON = 4          # planning horizon for BOTH ceiling and imagine (== H_1021/H_1025 depth-4)
CEM_ITERS = 5        # CEM refinement iterations (== H_1025)
CEM_POP = 64         # CEM population size (== H_1025)
CEM_ELITE = 8        # CEM elite count (== H_1025)
CEM_INIT_STD = 0.6   # CEM initial per-dim action std (== H_1025)

# ----------------------------------------------------------------- PRE-FROZEN observation-noise grid (the H_1026 change)
# OBSERVATION noise std added to the position read (the agent NEVER sees the clean pos or the hidden vel).
# Frozen 2026-06-07. 0.0 = the H_1025 regime (clean obs) -> must reproduce parity (sanity).
OBS_NOISE_GRID = [0.0, 0.05, 0.10, 0.20, 0.40, 0.80]
MONO_TOL = 0.02      # frozen: a step-to-step imagine return may RISE by at most this (else non-monotone)
CLIFF_FRAC = 0.60    # frozen: one grid-step drop > this fraction of the total span = a "cliff" (catastrophic)


# ----------------------------------------------------------------- TRUE dynamics (clean state; == H_1025 step_env)
def step_env(pos, v, a, rng):
    """TRUE continuous-action dynamics on the CLEAN state. v_new = DRAG*v + a (clipped);
    pos += VSTEP*v_new + PROCESS noise; reward = -||clean pos||. Observation NOISE is added
    separately by the agent's perceive step, NEVER here -- the world evolves on the clean state."""
    a = np.clip(a, -AMAX, AMAX)
    v = DRAG * v + a
    pos = pos + VSTEP * v + PROC_NOISE * rng.standard_normal(ADIM)
    return pos, v, -float(np.linalg.norm(pos))


def greedy_action(pos, v):
    """Continuous 1-step oracle on the CLEAN state (needs the hidden velocity)."""
    return np.clip(-(DRAG * v) - pos / VSTEP, -AMAX, AMAX)


def gen_demo(rng):
    """Greedy-oracle demos (CLEAN obs, as H_1025) to fit the LEARNED WM + heads. The learned model
    is trained on CLEAN demos and is NEVER given the noise model -- it must generalize to noisy obs."""
    pos = rng.standard_normal(2) * 2
    v = rng.standard_normal(2) * 0.5
    obs, acts = [pos.copy()], []
    for _ in range(T - 1):
        a = greedy_action(pos, v)
        acts.append(a.copy())
        pos, v, _ = step_env(pos, v, a, rng)
        obs.append(pos.copy())
    acts.append(greedy_action(pos, v).copy())
    return np.array(obs), np.array(acts)


# ----------------------------------------------------------------- noise-aware reference: KALMAN belief + CEM-MPC
# True linear-Gaussian state-space for the filter (the reference KNOWS this; anima does not):
#   state s = [px, py, vx, vy].  s_{t+1} = F s_t + G a_t + w,  w ~ N(0, Q)
#   obs    o = H s_t + r,        r ~ N(0, R = obs_sigma^2 I)
# From step_env: v_{t+1}=DRAG v_t + a_t ; pos_{t+1}=pos_t + VSTEP v_{t+1} = pos_t + VSTEP DRAG v_t + VSTEP a_t.
F_DYN = np.array([
    [1, 0, VSTEP * DRAG, 0],
    [0, 1, 0, VSTEP * DRAG],
    [0, 0, DRAG, 0],
    [0, 0, 0, DRAG],
], float)
G_DYN = np.array([
    [VSTEP, 0],
    [0, VSTEP],
    [1, 0],
    [0, 1],
], float)
H_OBS = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], float)           # observe position only (partial)
Q_PROC = np.diag([PROC_NOISE ** 2, PROC_NOISE ** 2, 1e-9, 1e-9])  # process noise on pos (vel noiseless)


class KalmanFilter:
    """Standard linear-Gaussian Kalman filter -> MMSE belief mean from the NOISY position history."""

    def __init__(self, obs_sigma):
        self.R = np.eye(2) * (obs_sigma ** 2 + 1e-9)
        self.reset()

    def reset(self):
        # diffuse prior (we know neither initial pos nor the hidden vel)
        self.mu = np.zeros(4)
        self.P = np.diag([4.0, 4.0, 1.0, 1.0])  # matches gen_demo init scale (pos~N(0,2), vel~N(0,0.5))

    def predict(self, a):
        self.mu = F_DYN @ self.mu + G_DYN @ a
        self.P = F_DYN @ self.P @ F_DYN.T + Q_PROC

    def update(self, o):
        S = H_OBS @ self.P @ H_OBS.T + self.R
        K = self.P @ H_OBS.T @ np.linalg.inv(S)
        self.mu = self.mu + K @ (o - H_OBS @ self.mu)
        self.P = (np.eye(4) - K @ H_OBS) @ self.P
        return self.mu.copy()


def cem_plan_true(pos_est, v_est, rng):
    """CEM receding-horizon MPC over HORIZON actions rolled through the TRUE deterministic dynamics,
    starting from the (estimated) state. Noise-free in planning (== H_1021/H_1025 MPC). Returns a[0]."""
    mu = np.zeros((HORIZON, ADIM))
    std = np.full((HORIZON, ADIM), CEM_INIT_STD)
    for _ in range(CEM_ITERS):
        samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, HORIZON, ADIM)), -AMAX, AMAX)
        scores = np.empty(CEM_POP)
        for i in range(CEM_POP):
            p, vel, acc = pos_est.copy(), v_est.copy(), 0.0
            for k in range(HORIZON):
                vel = DRAG * vel + samp[i, k]
                p = p + VSTEP * vel
                acc += -np.linalg.norm(p)
            scores[i] = acc
        elite = samp[np.argsort(scores)[-CEM_ELITE:]]
        mu = elite.mean(0)
        std = elite.std(0) + 1e-6
    return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- anima imagine-rollout (CEM through LEARNED WM)
class AnimaImaginePlanner:
    """anima's OWN learned action-conditioned WM + CONTINUOUS-action CEM planner (== H_1025). The WM
    is an LDSWorldModel fitted by ridge on CLEAN greedy demos -- NEVER given the noise model. Under
    noise it embeds the NOISY position history (the delay-embedding does whatever implicit filtering
    it learned) and CEM-plans through the learned A/C. It NEVER calls step_env or the Kalman filter."""

    def __init__(self, fm):
        self.fm = fm

    def plan(self, noisy_obs_hist, rng):
        z0 = self.fm.embed(np.array(noisy_obs_hist))[-1]  # latent from the NOISY observed positions
        mu = np.zeros((HORIZON, ADIM))
        std = np.full((HORIZON, ADIM), CEM_INIT_STD)
        for _ in range(CEM_ITERS):
            samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, HORIZON, ADIM)), -AMAX, AMAX)
            scores = np.empty(CEM_POP)
            for i in range(CEM_POP):
                z, acc = z0.copy(), 0.0
                for k in range(HORIZON):
                    z = (_aug1(np.hstack([z, samp[i, k]])) @ self.fm.A)
                    acc += -np.linalg.norm(self.fm.decode(z))
                scores[i] = acc
            elite = samp[np.argsort(scores)[-CEM_ELITE:]]
            mu = elite.mean(0)
            std = elite.std(0) + 1e-6
        return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- harness (noisy-obs episode)
def episode_return(policy_fn, obs_sigma, rng):
    """Roll one episode. The world evolves on the CLEAN state; the policy sees ONLY the NOISY position
    history (velocity always hidden). Reward is on the clean pos. policy_fn(noisy_hist, o_noisy, rng)."""
    pos = rng.standard_normal(2) * 2
    v = rng.standard_normal(2) * 0.5
    o_noisy = pos + obs_sigma * rng.standard_normal(ADIM)
    noisy_hist = [o_noisy.copy()]
    total = 0.0
    for t in range(T - 1):
        a = policy_fn(noisy_hist, o_noisy, rng)
        pos, v, r = step_env(pos, v, a, rng)
        o_noisy = pos + obs_sigma * rng.standard_normal(ADIM)
        noisy_hist.append(o_noisy.copy())
        total += r
    return total / (T - 1)


# ----- arm factories (all consume the noisy obs history; none sees clean pos or hidden vel) -----
def make_kalman_mpc(obs_sigma):
    """noise-aware reference: a fresh Kalman filter per episode tracks the belief from the noisy
    history; CEM-MPC plans on true dyn from the belief mean. KNOWS true dyn + true noise model."""
    def fn(noisy_hist, o_noisy, rng, _kf=[None], _last_a=[None]):
        if len(noisy_hist) == 1:                 # episode start -> new filter
            _kf[0] = KalmanFilter(obs_sigma)
            _kf[0].update(o_noisy)
        else:
            _kf[0].predict(_last_a[0])
            _kf[0].update(o_noisy)
        b = _kf[0].mu
        a = cem_plan_true(b[:2].copy(), b[2:].copy(), rng)
        _last_a[0] = a
        return a
    return fn


def make_random():
    def fn(noisy_hist, o_noisy, rng):
        return rng.uniform(-AMAX, AMAX, ADIM)
    return fn


def make_reactive(Whead):
    """floor: maps the latest NOISY obs straight to an action (no state inference)."""
    def fn(noisy_hist, o_noisy, rng):
        return np.clip(_aug1(o_noisy) @ Whead, -AMAX, AMAX)
    return fn


def make_single_step(m, Whead):
    """anima single-step head: latent (from noisy history) -> action, greedily, no imagine."""
    def fn(noisy_hist, o_noisy, rng):
        z = m.embed(np.array(noisy_hist))[-1]
        return np.clip(_aug1(z) @ Whead, -AMAX, AMAX)
    return fn


def make_imagine(planner):
    def fn(noisy_hist, o_noisy, rng):
        return planner.plan(noisy_hist, rng)
    return fn


def run_agent(policy_factory, obs_sigma, seed0):
    """policy_factory() must return a FRESH policy_fn (so per-episode filter state does not leak)."""
    out = []
    for i in range(N_RUNS):
        rng = np.random.default_rng(seed0 + i)
        pf = policy_factory()
        out.append(np.array([episode_return(pf, obs_sigma, rng) for _ in range(EP_PER_RUN)]).mean())
    return np.array(out)


def main():
    header("H_1026", "imagine-rollout under PARTIAL OBS + OBSERVATION NOISE vs noise-aware Kalman-MPC")
    print(f"task=continuous-action hidden-velocity station-keeping, NOISY position obs  "
          f"metric M=mean return (0=optimal)")
    print(f"N_runs={N_RUNS} ep/run={EP_PER_RUN}  action=CONTINUOUS 2-D thrust in [-{AMAX},{AMAX}]^2  "
          f"horizon={HORIZON}")
    print(f"reference=KALMAN-belief CEM-MPC (true dyn + true noise model)  planner=CEM "
          f"(pop={CEM_POP} iters={CEM_ITERS})")
    print(f"PRE-FROZEN obs-noise grid = {OBS_NOISE_GRID}  (process noise fixed at {PROC_NOISE})")
    print(f"TOL={TOL}  MONO_TOL={MONO_TOL}  CLIFF_FRAC={CLIFF_FRAC}  no-Phi (a_phi_iit4_tool n/a)\n")

    # --- fit anima's LEARNED model + heads ONCE on CLEAN demos (never given the noise model) ---
    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]

    m = LDSWorldModel(ODIM, delay=DELAY).fit([o for o, a in demos])  # latent encoder for the heads
    Zw, Yw = [], []
    for o, a in demos:
        z = m.embed(o)
        for t in range(DELAY - 1, T):
            Zw.append(z[t]); Yw.append(a[t])
    Whead_ss = _ridge(_aug(np.array(Zw)), np.array(Yw), 1e-2)
    Xr, Yr = [], []
    for o, a in demos:
        for t in range(T):
            Xr.append(o[t]); Yr.append(a[t])
    Whead_reac = _ridge(_aug(np.array(Xr)), np.array(Yr), 1e-2)

    fm = LDSWorldModel(ODIM, delay=DELAY, act_dim=ADIM)
    fm.fit([o for o, a in demos], traj_acts=[a for o, a in demos])
    planner = AnimaImaginePlanner(fm)

    o0, a0 = demos[0]
    z0 = m.embed(o0)
    pred1 = fm.decode(fm.roll(z0[DELAY - 1], 1, act_seq=a0[DELAY - 1:DELAY]))
    print(f"[learned-WM 1-step decode sanity, CLEAN demo] true pos={o0[DELAY].round(3)} "
          f"pred pos={pred1.round(3)}\n")

    # --- sweep the frozen noise grid; build the degradation curve ---
    rows = []   # one dict per noise level
    print("==== noise sweep (mean +/- std, bootstrap CI) ====")
    for sig in OBS_NOISE_GRID:
        kf  = run_agent(lambda: make_kalman_mpc(sig), sig, 1000)     # noise-aware reference
        rnd = run_agent(lambda: make_random(),        sig, 2000)     # floor
        rea = run_agent(lambda: make_reactive(Whead_reac), sig, 3000)  # floor
        ss  = run_agent(lambda: make_single_step(m, Whead_ss), sig, 4000)  # anima single-step head
        im  = run_agent(lambda: make_imagine(planner), sig, 5000)    # anima imagine-rollout

        P = kf.mean(); blo, bhi = P - TOL, P + TOL
        plo, phi = boot_ci(kf); ilo, ihi = boot_ci(im); slo, shi = boot_ci(ss)
        clo, chi = boot_ci(rea); rlo, rhi = boot_ci(rnd)
        within = (blo <= im.mean() <= bhi)
        ci_ov = (ilo <= bhi) and (ihi >= blo)
        t_is, p_is = welch_t(im, ss); d_is = cohens_d(im, ss)
        rows.append(dict(sig=sig, P=P, blo=blo, bhi=bhi, plo=plo, phi=phi,
                         im=im.mean(), ilo=ilo, ihi=ihi, ss=ss.mean(), slo=slo, shi=shi,
                         rea=rea.mean(), chi=chi, rnd=rnd.mean(), rhi=rhi,
                         within=within, ci_ov=ci_ov, p_is=p_is, d_is=d_is,
                         lift=im.mean() - ss.mean(), gap=P - im.mean()))
        print(f"  sigma={sig:<5} Kalman-MPC P={P:+.4f} band=[{blo:+.4f},{bhi:+.4f}] | "
              f"imagine={im.mean():+.4f} CI=[{ilo:+.4f},{ihi:+.4f}] within={within} ci_ov={ci_ov} | "
              f"single={ss.mean():+.4f} | reac={rea.mean():+.4f} | rand={rnd.mean():+.4f} | "
              f"lift={im.mean()-ss.mean():+.4f}(p={p_is:.1e}) gap={P-im.mean():+.4f}")

    # ----- degradation-curve analysis (the falsifier operationalization, frozen above) -----
    print("\n==== degradation curve : imagine return vs obs-noise ====")
    print(f"  {'sigma':>6} {'imagine':>9} {'Kalman-MPC':>11} {'band':>22} {'within':>7} {'lift':>9}")
    for r in rows:
        print(f"  {r['sig']:>6} {r['im']:>+9.4f} {r['P']:>+11.4f} "
              f"[{r['blo']:+.4f},{r['bhi']:+.4f}] {str(r['within']):>7} {r['lift']:>+9.4f}")

    # contiguous parity plateau from sigma=0
    plateau = []
    for r in rows:
        if r['within']:
            plateau.append(r['sig'])
        else:
            break
    sigma_star = plateau[-1] if plateau else None
    nz = [r['sig'] for r in rows if r['sig'] > 0]
    low1 = nz[0] if nz else None
    parity_at_zero = rows[0]['within']
    parity_at_low1 = next((r['within'] for r in rows if r['sig'] == low1), False)

    # monotone-vs-cliff on the imagine curve beyond sigma*
    ims = [r['im'] for r in rows]
    span = max(ims) - min(ims) + 1e-12
    steps = []
    for k in range(1, len(rows)):
        drop = rows[k - 1]['im'] - rows[k]['im']            # positive = got worse (more negative return)
        rise = -drop
        ci_overlap = (rows[k]['ihi'] >= rows[k - 1]['ilo']) and (rows[k]['ilo'] <= rows[k - 1]['ihi'])
        is_cliff = (drop / span) > CLIFF_FRAC
        non_monotone = (rise > MONO_TOL) and (not ci_overlap)
        steps.append(dict(a=rows[k - 1]['sig'], b=rows[k]['sig'], drop=drop,
                          frac=drop / span, ci_overlap=ci_overlap, cliff=is_cliff, nonmono=non_monotone))
    any_cliff = any(s['cliff'] for s in steps)
    any_nonmono = any(s['nonmono'] for s in steps)
    monotone_no_cliff = (not any_cliff) and (not any_nonmono)

    print("\n  step-to-step (drop = worsening of imagine return; frac of total span):")
    for s in steps:
        flags = []
        if s['cliff']: flags.append("CLIFF")
        if s['nonmono']: flags.append("NON-MONO")
        print(f"    sigma {s['a']:<5}-> {s['b']:<5}  drop={s['drop']:+.4f} "
              f"frac={s['frac']:+.3f} ci_overlap={s['ci_overlap']} {' '.join(flags)}")

    print(f"\n  contiguous within-band parity plateau from sigma=0 : {plateau}")
    print(f"  sigma* (largest contiguous within-band noise level) : {sigma_star}")
    print(f"  parity at sigma=0 = {parity_at_zero}   parity at smallest non-zero sigma "
          f"({low1}) = {parity_at_low1}")
    print(f"  curve monotone (no non-mono jump) = {not any_nonmono}   no cliff (no >"
          f"{CLIFF_FRAC} span single drop) = {not any_cliff}")

    # ----- pre-registered verdict -----
    # PASS (NOISE-ROBUST-PARITY): parity holds at sigma=0 AND at the smallest non-zero sigma (plateau
    # covers >=2 levels incl. one noisy level), AND the degradation beyond sigma* is monotone (no cliff).
    robust_plateau = parity_at_zero and parity_at_low1 and (sigma_star is not None) and (sigma_star >= low1)
    print()
    if robust_plateau and monotone_no_cliff:
        verdict_line("H_1026", "PASS",
                     f"NOISE-ROBUST-PARITY (\U0001F7E2) -- planning through anima's OWN learned WM stays WITHIN "
                     f"the noise-aware Kalman-belief CEM-MPC parity band up to obs-noise sigma*={sigma_star} "
                     f"(contiguous within-band plateau {plateau}, incl. the noisy level sigma={low1}), then "
                     f"degrades MONOTONICALLY (no cliff: max single-step drop "
                     f"{max(s['frac'] for s in steps):.2f} of span <= {CLIFF_FRAC}; no non-monotone jump). "
                     f"The learned WM -- trained ONLY on clean demos, never given the noise model -- recovers "
                     f"enough hidden state from NOISY partial history to match the noise-aware optimum at low "
                     f"noise; forward-model error compounds gracefully, not catastrophically. H_1021/H_1025 "
                     f"parity is NOISE-ROBUST, not noiseless-only. TOY single rung; real-sensor noise / scale "
                     f"UNVERIFIED (a_scale_honest_scope).")
    else:
        # FAIL (NOISE-BREAKS-PARITY): parity lost even at low noise OR catastrophic (cliff / non-monotone).
        reason = []
        if not parity_at_zero:
            reason.append(f"parity FAILS even at sigma=0 (imagine {rows[0]['im']:+.4f} outside band "
                          f"[{rows[0]['blo']:+.4f},{rows[0]['bhi']:+.4f}])")
        elif not parity_at_low1:
            reason.append(f"parity LOST at the smallest non-zero noise sigma={low1} "
                          f"(imagine outside band) -- breaks at LOW noise")
        if any_cliff:
            cs = next(s for s in steps if s['cliff'])
            reason.append(f"CATASTROPHIC cliff: imagine return drops {cs['drop']:+.4f} "
                          f"({cs['frac']:.2f} of total span > {CLIFF_FRAC}) over one grid step "
                          f"sigma {cs['a']}->{cs['b']}")
        if any_nonmono:
            ns = next(s for s in steps if s['nonmono'])
            reason.append(f"NON-MONOTONE degradation (return rises {-ns['drop']:+.4f} with CI-disjoint "
                          f"at sigma {ns['a']}->{ns['b']})")
        if not reason:
            reason.append(f"parity plateau {plateau} does not cover a noisy level (sigma*={sigma_star}, "
                          f"smallest non-zero sigma={low1})")
        verdict_line("H_1026", "FAIL",
                     f"NOISE-BREAKS-PARITY (\U0001F534, closed-negative a_paper_negative_ok) -- " +
                     "; ".join(reason) + f". Observation noise + partial observation breaks the "
                     f"H_1021/H_1025 imagine-rollout = MPC parity: forward-model error through the learned "
                     f"WM compounds where the noise-aware Kalman-MPC (which KNOWS the noise model) does not. "
                     f"Bounds H_1021/H_1025 to (near-)noiseless control; the CWM perceive step needs an "
                     f"explicit noise/belief model, not a clean-demo learned WM. TOY single rung "
                     f"(a_scale_honest_scope).")


if __name__ == "__main__":
    main()
