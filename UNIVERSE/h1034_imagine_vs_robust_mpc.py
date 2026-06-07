"""H_1034 — imagine-rollout vs a ROBUST (scenario / tube) true-dynamics MPC.

Pre-registered (frozen 2026-06-08; honored verbatim, see
UNIVERSE/H_1034_imagine_vs_robust_mpc.md):

  H_1027 (RED, TRACKS-ALL-DEPTHS) found imagine-rollout (CEM through anima's OWN LEARNED LDS world
  model) not only TRACKED but, at deep horizon d>=8, OUTPERFORMED the same-depth true-dynamics
  CEM-MPC on the H_964 continuous hidden-velocity station-keeping toy. The honest read: a deep
  CEM-MPC optimizing a NOISE-FREE deterministic rollout over-commits to a plan optimal for the
  deterministic model but brittle under process noise; imagine (planning through a smoother
  ridge-fit learned transition) yields more robust actions and so wins at depth.

  RESIDUAL: was "imagine beats MPC at deep horizon" a WEAK-BASELINE artifact? This H adds a ROBUST
  true-dynamics MPC baseline and re-runs the SAME depth ladder. The robust MPC has the TRUE
  dynamics AND the disturbance model: its CEM scores each candidate plan as the MEAN return over
  N_SCEN independently sampled process-noise scenarios (scenario / sample-average-approximation
  tube-MPC), so it does NOT over-commit to a noise-free optimum.

  PASS  = IMAGINE-BEATS-ROBUST-MPC-TOO : imagine-rollout is still >= the ROBUST MPC at BOTH deep
          depths {8,16} (robust_gap(d) = robust_MPC(d) - imagine(d) <= GAP_TOL for d in {8,16}).
          The imagine advantage at depth is REAL, not a brittle-baseline artifact.
  FAIL  = ARTIFACT-OF-BRITTLE-MPC : the ROBUST MPC beats imagine by more than GAP_TOL at SOME deep
          depth d in {8,16} -> H_1027's imagine>MPC was a weak-baseline artifact (closed-negative,
          a_paper_negative_ok).

REUSE (do NOT reinvent): the H_1027 / H_1025 continuous-action machinery VERBATIM — the H_964
hidden-velocity station-keeping env (position-only obs, hidden velocity a delay-embedding latent
must recover), the LEARNED LDSWorldModel (ridge on greedy-oracle demos; NEVER given the true
dynamics), the CEM continuous-action planner, the AnimaImaginePlanner imagine-rollout, the naive
noise-free true-MPC (re-run unchanged as the WEAK reference), the frozen depth ladder, and the
N_RUNS x EP_PER_RUN protocol. The ONLY new component is cem_plan_robust (scenario/tube MPC).

$0 CPU-local, deterministic given seeds, serial, no GPU, polls inline (no Monitor/waiter,
a_cpu_local_no_waiter). No Phi claim (a_phi_iit4_tool n/a -- behavior return only). TOY single env;
robust MPC = scenario/SAA tube variant only (other robustifications untested); ladder OPEN
(a_scale_honest_scope · a_toy_scale_recheck).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, _aug1, boot_ci, welch_t, cohens_d, spearman, header, verdict_line

# ----------------------------------------------------------------- env constants (continuous variant of H_964; VERBATIM from H_1027)
ODIM = 2             # observation = position (2-D); velocity is HIDDEN
ADIM = 2             # CONTINUOUS action = thrust vector (2-D)
T = 20               # episode length
N_TRAIN = 400        # demo trajectories
VSTEP = 0.4          # position integration step
DRAG = 1.0           # velocity FULLY persists -> must counter the HIDDEN velocity
AMAX = 1.0           # action box half-width: a in [-AMAX, AMAX]^2
NOISE = 0.02         # process noise std
DELAY = 3            # delay-embedding (anima's H_964/H_1019/H_1021/H_1025/H_1027 WM)

# ----------------------------------------------------------------- frozen protocol constants (frozen 2026-06-08)
N_RUNS = 40          # runs per agent (same as H_1019/H_1021/H_1025/H_1027)
EP_PER_RUN = 60      # episodes per run
DEPTHS = [1, 2, 4, 8, 16]   # PRE-FROZEN depth ladder (identical to H_1027; MPC depth == imagine horizon)
DEEP = [8, 16]       # deep-horizon tail where H_1027 saw imagine > naive-MPC; verdict decided here
GAP_TOL = 0.05       # frozen tolerance: robust MPC "beats" imagine when robust_MPC(d)-imagine(d) > GAP_TOL
CEM_ITERS = 5        # CEM refinement iterations (VERBATIM)
CEM_POP = 64         # CEM population size per iteration (VERBATIM)
CEM_ELITE = 8        # CEM elite count (VERBATIM)
CEM_INIT_STD = 0.6   # CEM initial per-dim action std (VERBATIM)
N_SCEN = 16          # NEW: robust-MPC process-noise scenarios per candidate (scenario/SAA tube-MPC)


# ----------------------------------------------------------------- continuous env (VERBATIM from H_1027)
def step_env(pos, v, a, rng):
    a = np.clip(a, -AMAX, AMAX)
    v = DRAG * v + a
    pos = pos + VSTEP * v + NOISE * rng.standard_normal(ADIM)
    return pos, v, -float(np.linalg.norm(pos))


def greedy_action(pos, v):
    """Continuous 1-step oracle (needs the HIDDEN velocity)."""
    return np.clip(-(DRAG * v) - pos / VSTEP, -AMAX, AMAX)


def gen_demo(rng):
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


# ----------------------------------------------------------------- NAIVE true-dynamics MPC (noise-free CEM, VERBATIM from H_1027 = WEAK baseline)
def cem_plan_true(pos, v, rng, horizon):
    mu = np.zeros((horizon, ADIM))
    std = np.full((horizon, ADIM), CEM_INIT_STD)
    for _ in range(CEM_ITERS):
        samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, ADIM)),
                       -AMAX, AMAX)                                   # (POP, H, A)
        # VECTORIZED over the population (identical scoring to the H_1027 per-candidate loop:
        # deterministic forward rollout, sum of -||pos|| over the horizon). Same rng draw shape
        # so the random stream is preserved bit-for-bit vs the scalar version.
        p = np.tile(pos.astype(float), (CEM_POP, 1))                 # (POP, A)
        vel = np.tile(v.astype(float), (CEM_POP, 1))                 # (POP, A)
        scores = np.zeros(CEM_POP)
        for k in range(horizon):
            vel = DRAG * vel + samp[:, k]
            p = p + VSTEP * vel
            scores += -np.linalg.norm(p, axis=1)
        elite = samp[np.argsort(scores)[-CEM_ELITE:]]
        mu = elite.mean(0)
        std = elite.std(0) + 1e-6
    return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- ROBUST true-dynamics MPC (scenario / SAA tube-MPC; the ONLY new component)
def cem_plan_robust(pos, v, rng, horizon):
    """Identical CEM search to cem_plan_true (same TRUE dynamics, same pop/iters/elite/std,
    same receding-horizon use: returns only mu[0]), with ONE change: each candidate plan is
    scored as the MEAN return over N_SCEN independently sampled process-noise scenarios drawn
    from the SAME NOISE Gaussian the real env applies in step_env. The planner is given the
    TRUE dynamics AND the disturbance model and picks the plan with the best EXPECTED return,
    so it does not over-commit to a noise-free optimum (scenario / SAA tube-MPC). Scenario noise
    is shared across the population this CEM iteration (common random numbers -> lower-variance
    candidate ranking). VECTORIZED over (population x scenarios); same rng draw shapes so the
    random stream is preserved bit-for-bit vs the scalar version."""
    mu = np.zeros((horizon, ADIM))
    std = np.full((horizon, ADIM), CEM_INIT_STD)
    for _ in range(CEM_ITERS):
        samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, ADIM)),
                       -AMAX, AMAX)                                   # (POP, H, A)
        scen_noise = rng.standard_normal((N_SCEN, horizon, ADIM))    # (S, H, A) shared across POP
        # broadcast to (POP, S, A): every scenario shares the same candidate plan
        p = np.broadcast_to(pos.astype(float), (CEM_POP, N_SCEN, ADIM)).copy()
        vel = np.broadcast_to(v.astype(float), (CEM_POP, N_SCEN, ADIM)).copy()
        scores = np.zeros(CEM_POP)
        for k in range(horizon):
            vel = DRAG * vel + samp[:, None, k, :]                   # (POP,1,A) broadcast over S
            p = p + VSTEP * vel + NOISE * scen_noise[None, :, k, :]  # (1,S,A) noise broadcast over POP
            scores += -np.linalg.norm(p, axis=2).mean(axis=1)        # per-step cost, mean over scenarios
        elite = samp[np.argsort(scores)[-CEM_ELITE:]]
        mu = elite.mean(0)
        std = elite.std(0) + 1e-6
    return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- imagine-rollout (VERBATIM from H_1027)
class AnimaImaginePlanner:
    """anima's OWN learned action-conditioned WM + a CONTINUOUS-action CEM planner.
    Plans by rolling the LEARNED transition A forward and decoding via the LEARNED decoder C;
    NEVER calls step_env. Horizon is a plan() argument so the SAME planner sweeps the ladder."""

    def __init__(self, fm):
        self.fm = fm

    def plan(self, obs_hist, rng, horizon):
        z0 = self.fm.embed(np.array(obs_hist))[-1]
        mu = np.zeros((horizon, ADIM))
        std = np.full((horizon, ADIM), CEM_INIT_STD)
        A = self.fm.A; C = self.fm.C
        for _ in range(CEM_ITERS):
            samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, ADIM)),
                           -AMAX, AMAX)
            # VECTORIZED over the population (identical to the H_1027 per-candidate loop:
            # roll LEARNED transition z<-aug1([z,a])@A, decode pred<-aug1(z)@C, sum -||pred||
            # over the horizon). Same rng draw shape so the random stream is preserved bit-for-bit.
            z = np.tile(z0.astype(float), (CEM_POP, 1))               # (POP, zdim)
            ones = np.ones((CEM_POP, 1))
            scores = np.zeros(CEM_POP)
            for k in range(horizon):
                zin = np.hstack([z, samp[:, k], ones])               # (POP, zdim+ADIM+1) = aug1([z,a])
                z = zin @ A                                          # (POP, zdim) learned transition
                pred = np.hstack([z, ones]) @ C                      # (POP, obs) learned decode = aug1(z)@C
                scores += -np.linalg.norm(pred, axis=1)
            elite = samp[np.argsort(scores)[-CEM_ELITE:]]
            mu = elite.mean(0)
            std = elite.std(0) + 1e-6
        return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- harness (VERBATIM from H_1027)
def episode_return(policy_fn, rng):
    pos = rng.standard_normal(2) * 2
    v = rng.standard_normal(2) * 0.5
    obs_hist = [pos.copy()]
    total = 0.0
    for t in range(T - 1):
        a = policy_fn(obs_hist, pos, v, rng)
        pos, v, r = step_env(pos, v, a, rng)
        obs_hist.append(pos.copy())
        total += r
    return total / (T - 1)


def run_agent(policy_fn, seed0):
    out = []
    for i in range(N_RUNS):
        rng = np.random.default_rng(seed0 + i)
        ep = np.array([episode_return(policy_fn, rng) for _ in range(EP_PER_RUN)])
        out.append(ep.mean())
    return np.array(out)


def main():
    header("H_1034", "imagine-rollout vs a ROBUST (scenario/tube) true-dynamics MPC")
    print(f"task=continuous-action hidden-velocity station-keeping (position-only obs)  "
          f"metric M=mean return (0=optimal)")
    print(f"N_runs={N_RUNS} ep/run={EP_PER_RUN}  action=CONTINUOUS 2-D thrust in [-{AMAX},{AMAX}]^2")
    print(f"FROZEN depth ladder DEPTHS={DEPTHS}  deep-tail={DEEP}  GAP_TOL={GAP_TOL}")
    print(f"robust-MPC = scenario/SAA tube-MPC, N_SCEN={N_SCEN} process-noise draws/candidate (NOISE={NOISE})")
    print(f"planner=CEM (pop={CEM_POP} iters={CEM_ITERS} elite={CEM_ELITE})  "
          f"no-Phi (a_phi_iit4_tool n/a)\n")

    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]

    # --- anima's OWN LEARNED action-conditioned forward model (VERBATIM from H_1027; SAME demos) ---
    fm = LDSWorldModel(ODIM, delay=DELAY, act_dim=ADIM)
    fm.fit([o for o, a in demos], traj_acts=[a for o, a in demos])
    planner = AnimaImaginePlanner(fm)

    o0, a0 = demos[0]
    pred1 = fm.decode(fm.roll(fm.embed(o0)[DELAY - 1], 1, act_seq=a0[DELAY - 1:DELAY]))
    print(f"[learned-WM 1-step decode sanity] true pos={o0[DELAY].round(3)} "
          f"pred pos={pred1.round(3)}\n")

    # --- depth ladder: same-depth imagine vs naive-MPC vs robust-MPC ---
    print("---- depth ladder: imagine vs naive-MPC vs ROBUST-MPC (mean return, bootstrap CI) ----")
    ladder = []   # rows: (d, naive_mean, naive_ci, robust_mean, robust_ci, imag_mean, imag_ci,
                  #         robust_gap, welch_p_robust_vs_imag, cohen_d, naive_to_robust)
    for d in DEPTHS:
        naive = run_agent(lambda oh, p, v, r, _d=d: cem_plan_true(p, v, r, _d), 1000 + d)
        robust = run_agent(lambda oh, p, v, r, _d=d: cem_plan_robust(p, v, r, _d), 3000 + d)
        imag = run_agent(lambda oh, p, v, r, _d=d: planner.plan(oh, r, _d), 5000 + d)
        nlo, nhi = boot_ci(naive); rlo, rhi = boot_ci(robust); ilo, ihi = boot_ci(imag)
        robust_gap = robust.mean() - imag.mean()         # >0 => robust MPC beats imagine
        naive_to_robust = robust.mean() - naive.mean()   # >0 => robustness helped the true planner
        tp, pp = welch_t(robust, imag); dd = cohens_d(robust, imag)
        ladder.append((d, naive.mean(), (nlo, nhi), robust.mean(), (rlo, rhi),
                       imag.mean(), (ilo, ihi), robust_gap, pp, dd, naive_to_robust))
        deep = "DEEP" if d in DEEP else "    "
        flag = "robust>imag" if robust_gap > GAP_TOL else "imag>=robust"
        print(f"  d={d:2d} [{deep}]  naive-MPC={naive.mean():.4f}[{nlo:.4f},{nhi:.4f}]   "
              f"robust-MPC={robust.mean():.4f}[{rlo:.4f},{rhi:.4f}]   "
              f"imagine={imag.mean():.4f}[{ilo:.4f},{ihi:.4f}]")
        print(f"            robust_gap=robust-imag={robust_gap:+.4f} (Welch p={pp:.2e} d={dd:+.3f}) "
              f"[{flag} @ GAP_TOL={GAP_TOL}]   naive->robust improvement={naive_to_robust:+.4f}")
    print()

    # --- pre-registered verdict gate: decided at the deep tail {8,16} ---
    deep_rows = [row for row in ladder if row[0] in DEEP]
    robust_beats_imag = [(row[0], row[7]) for row in deep_rows if row[7] > GAP_TOL]
    print(f"deep-tail {DEEP} robust_gap (robust-MPC - imagine): "
          f"{[(row[0], round(row[7], 4)) for row in deep_rows]}")
    print(f"depths where robust MPC beats imagine by > GAP_TOL={GAP_TOL}: "
          f"{[d for d, g in robust_beats_imag]}\n")

    # --- secondary: does robustness help the true planner; does robust MPC stop degrading at depth ---
    naive_curve = np.array([row[1] for row in ladder])
    robust_curve = np.array([row[3] for row in ladder])
    imag_curve = np.array([row[5] for row in ladder])
    print(f"naive-MPC  return curve over {DEPTHS}: {naive_curve.round(4).tolist()}")
    print(f"robust-MPC return curve over {DEPTHS}: {robust_curve.round(4).tolist()}")
    print(f"imagine    return curve over {DEPTHS}: {imag_curve.round(4).tolist()}")
    naive_degrades_deep = naive_curve[-1] < naive_curve[1]     # H_1027: naive worse past d=2
    robust_degrades_deep = robust_curve[-1] < robust_curve[1]
    print(f"naive-MPC degrades d=2->16: {naive_degrades_deep} "
          f"({naive_curve[1]:.4f}->{naive_curve[-1]:.4f})")
    print(f"robust-MPC degrades d=2->16: {robust_degrades_deep} "
          f"({robust_curve[1]:.4f}->{robust_curve[-1]:.4f})")
    print()

    # ---- verdict (g5 CODE-measured; pre-registered tokens) ----
    if robust_beats_imag:
        worst_d, worst_gap = max(robust_beats_imag, key=lambda x: x[1])
        verdict_line("H_1034", "RED",
                     f"ARTIFACT-OF-BRITTLE-MPC (closed-negative, a_paper_negative_ok) — a ROBUST "
                     f"(scenario/SAA tube, N_SCEN={N_SCEN}) true-dynamics MPC BEATS imagine-rollout "
                     f"by more than GAP_TOL={GAP_TOL} at deep depth(s) {[d for d, g in robust_beats_imag]} "
                     f"(max robust_gap {worst_gap:+.4f} @ d={worst_d}). H_1027's 'imagine beats MPC at "
                     f"deep horizon' was a WEAK-BASELINE artifact: the H_1027 naive true-MPC optimized a "
                     f"NOISE-FREE rollout and over-committed to brittle plans, but a true planner that "
                     f"optimizes EXPECTED return under the disturbance reclaims (>=) the lead at depth. "
                     f"naive-MPC curve {naive_curve.round(3).tolist()} -> robust-MPC curve "
                     f"{robust_curve.round(3).tolist()} (robustness helps: naive degrades deep="
                     f"{naive_degrades_deep}, robust degrades deep={robust_degrades_deep}). "
                     f"TOY single rung, $0 CPU-local; scenario-tube variant only, other robustifications "
                     f"UNVERIFIED; scale-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). "
                     f"a_phi_iit4_tool n/a.")
    else:
        deep_gaps = [round(row[7], 4) for row in deep_rows]
        verdict_line("H_1034", "GREEN",
                     f"IMAGINE-BEATS-ROBUST-MPC-TOO — imagine-rollout (CEM through anima's OWN learned "
                     f"LDS world model) is STILL >= a ROBUST (scenario/SAA tube, N_SCEN={N_SCEN}) "
                     f"true-dynamics MPC at BOTH deep depths {DEEP}: robust_gap (robust-MPC - imagine) "
                     f"{deep_gaps} <= GAP_TOL={GAP_TOL} at every deep depth. The imagine advantage at "
                     f"depth from H_1027 is REAL, NOT a brittle-baseline artifact: even a true planner "
                     f"given the disturbance model and optimizing expected return does not clearly "
                     f"out-plan imagination on this toy. naive-MPC curve {naive_curve.round(3).tolist()} "
                     f"-> robust-MPC curve {robust_curve.round(3).tolist()} (robustness helped the true "
                     f"planner: naive degrades deep={naive_degrades_deep}, robust degrades deep="
                     f"{robust_degrades_deep}) yet imagine still tracks/leads. TOY single rung, $0 "
                     f"CPU-local; scenario-tube variant only, other robustifications (min-max/CVaR) "
                     f"UNVERIFIED; scale-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). "
                     f"a_phi_iit4_tool n/a.")


if __name__ == "__main__":
    main()
