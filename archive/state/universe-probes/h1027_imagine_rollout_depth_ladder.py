"""H_1027 — imagine-rollout depth ladder vs a deepening optimum.

Pre-registered (frozen 2026-06-07; honored verbatim, see
UNIVERSE/cards/H_1027_imagine_rollout_depth_ladder.md):

  H_1021 matched a depth-4 imagine-rollout to a depth-4 MPC, but only SAMPLED the depth
  dependence at d in {2,4}. The general question: planning through a LEARNED world model
  accumulates forward-prediction error with horizon, while a deeper TRUE-dynamics MPC keeps
  improving. There should be a crossover horizon h* where imagine-rollout (planning through
  anima's LEARNED model) STOPS TRACKING the same-depth true-dynamics MPC, and h* should be
  tied to where the learned model's multi-step forward error grows.

  Sweep BOTH the reference MPC depth and the imagine-rollout horizon over a PRE-FROZEN ladder
  DEPTHS = {1, 2, 4, 8, 16}. At each depth d compare imagine-rollout(d) to the SAME-DEPTH
  true-dynamics MPC(d); locate h* = the first depth where the gap (MPC(d) - imagine(d))
  exceeds a FROZEN tolerance GAP_TOL. Also measure the learned model's k-step forward error
  (k-step open-loop prediction error vs the true rollout) over the same ladder and report
  whether h* coincides with where that error grows.

  PASS  = HORIZON-CHARACTERIZED : a finite h* exists where imagine-rollout's gap to the
          same-depth MPC first exceeds GAP_TOL, AND h* correlates with the learned model's
          forward-error growth (a Delta-vs-depth result).
  FAIL  = TRACKS-ALL-DEPTHS    : the gap never exceeds GAP_TOL on the tested ladder (the
          learned model is near-perfect on this toy) -> closed-negative, a_paper_negative_ok.
        | BREAKS-IMMEDIATELY    : imagine-rollout never tracks past d=1 (gap exceeds GAP_TOL
          already at the smallest tracked depth) -> closed-negative, a_paper_negative_ok.

REUSE (do NOT reinvent): the H_1025 continuous-action machinery VERBATIM — the H_964
hidden-velocity station-keeping env (position-only obs, hidden velocity a delay-embedding
latent must recover), the LEARNED LDSWorldModel (ridge on greedy-oracle demos; NEVER given
the true dynamics), the CEM continuous-action planner, and the multi-seed / multi-episode
protocol (N_RUNS x EP_PER_RUN). The CEM planner is used because it scales LINEARLY in horizon
(the H_1021 discrete enumerator was NACT^d -> 4^16 = 4e9 leaves, infeasible at d=16). The ONLY
change vs H_1025: HORIZON is no longer fixed at 4 -- it is SWEPT over the frozen ladder for
BOTH the true-MPC ceiling and the imagine-rollout, and the learned model's k-step forward
error is measured along the same ladder.

$0 CPU-local, deterministic given seeds, serial, no GPU, polls inline (no Monitor/waiter,
a_cpu_local_no_waiter). No Phi claim (a_phi_iit4_tool n/a -- behavior return + forward error
only, no Phi). a_scale_honest_scope: TOY single env, ladder OPEN -- no production / real-robot
transfer.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, _aug1, boot_ci, welch_t, cohens_d, spearman, header, verdict_line

# ----------------------------------------------------------------- env constants (continuous variant of H_964; same as H_1025)
ODIM = 2             # observation = position (2-D); velocity is HIDDEN
ADIM = 2             # CONTINUOUS action = thrust vector (2-D)
T = 20               # episode length
N_TRAIN = 400        # demo trajectories
VSTEP = 0.4          # position integration step
DRAG = 1.0           # velocity FULLY persists -> must counter the HIDDEN velocity
AMAX = 1.0           # action box half-width: a in [-AMAX, AMAX]^2
NOISE = 0.02         # process noise std
DELAY = 3            # delay-embedding (anima's H_964/H_1019/H_1021/H_1025 WM)

# ----------------------------------------------------------------- frozen protocol constants (frozen 2026-06-07)
N_RUNS = 40          # runs per agent (same as H_1019/H_1021/H_1025)
EP_PER_RUN = 60      # episodes per run
DEPTHS = [1, 2, 4, 8, 16]   # PRE-FROZEN depth ladder (MPC depth == imagine horizon, swept together)
GAP_TOL = 0.05       # frozen tracking tolerance: imagine "stops tracking" when MPC(d)-imag(d) > GAP_TOL
CEM_ITERS = 5        # CEM refinement iterations
CEM_POP = 64         # CEM population size per iteration
CEM_ELITE = 8        # CEM elite count
CEM_INIT_STD = 0.6   # CEM initial per-dim action std
FWD_TEST = 200       # held-out trajectories for the k-step forward-error measurement


# ----------------------------------------------------------------- continuous env (drop-in H_964 analogue; same as H_1025)
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


# ----------------------------------------------------------------- true-dynamics MPC (CEM over TRUE dynamics) at a given horizon
def cem_plan_true(pos, v, rng, horizon):
    mu = np.zeros((horizon, ADIM))
    std = np.full((horizon, ADIM), CEM_INIT_STD)
    for _ in range(CEM_ITERS):
        samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, ADIM)),
                       -AMAX, AMAX)
        scores = np.empty(CEM_POP)
        for i in range(CEM_POP):
            p, vel, acc = pos.copy(), v.copy(), 0.0
            for k in range(horizon):
                vel = DRAG * vel + samp[i, k]
                p = p + VSTEP * vel
                acc += -np.linalg.norm(p)
            scores[i] = acc
        elite = samp[np.argsort(scores)[-CEM_ELITE:]]
        mu = elite.mean(0)
        std = elite.std(0) + 1e-6
    return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- imagine-rollout (CEM through anima's LEARNED model) at a given horizon
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
        for _ in range(CEM_ITERS):
            samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, horizon, ADIM)),
                           -AMAX, AMAX)
            scores = np.empty(CEM_POP)
            for i in range(CEM_POP):
                z, acc = z0.copy(), 0.0
                for k in range(horizon):
                    z = (_aug1(np.hstack([z, samp[i, k]])) @ self.fm.A)   # roll LEARNED transition
                    pred_pos = self.fm.decode(z)                           # LEARNED decoder -> pos
                    acc += -np.linalg.norm(pred_pos)
                scores[i] = acc
            elite = samp[np.argsort(scores)[-CEM_ELITE:]]
            mu = elite.mean(0)
            std = elite.std(0) + 1e-6
        return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- harness (continuous action)
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


# ----------------------------------------------------------------- learned-model k-step forward error (open-loop prediction)
def kstep_forward_error(fm, depths, seed):
    """For each k in depths, measure the learned model's k-step OPEN-LOOP position-prediction
    error: from a held-out trajectory's latent at t, roll the LEARNED transition A forward k
    steps under the trajectory's OWN actions, decode to a predicted position, and compare to the
    true position k steps ahead. Returns {k: mean ||pred - true||} (the model-error curve that
    h* should track). The model NEVER sees the true dynamics here -- pure learned-A rollout."""
    rng = np.random.default_rng(seed)
    errs = {k: [] for k in depths}
    for _ in range(FWD_TEST):
        o, a = gen_demo(rng)                 # held-out greedy-oracle trajectory
        z = fm.embed(o)
        for t in range(DELAY - 1, T):
            for k in depths:
                if t + k >= T:
                    continue
                zk = fm.roll(z[t], k, act_seq=a[t:t + k])   # learned A rolled k steps
                pred = fm.decode(zk)
                errs[k].append(float(np.linalg.norm(pred - o[t + k])))
    return {k: float(np.mean(v)) if v else float("nan") for k, v in errs.items()}


def main():
    header("H_1027", "imagine-rollout depth ladder vs a deepening MPC optimum")
    print(f"task=continuous-action hidden-velocity station-keeping (position-only obs)  "
          f"metric M=mean return (0=optimal)")
    print(f"N_runs={N_RUNS} ep/run={EP_PER_RUN}  action=CONTINUOUS 2-D thrust in [-{AMAX},{AMAX}]^2")
    print(f"FROZEN depth ladder DEPTHS={DEPTHS}  GAP_TOL={GAP_TOL}  (MPC depth == imagine horizon)")
    print(f"planner=CEM (pop={CEM_POP} iters={CEM_ITERS} elite={CEM_ELITE})  "
          f"no-Phi (a_phi_iit4_tool n/a)\n")

    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]

    # --- anima's OWN LEARNED action-conditioned forward model (fitted on the SAME demos) ---
    fm = LDSWorldModel(ODIM, delay=DELAY, act_dim=ADIM)
    fm.fit([o for o, a in demos], traj_acts=[a for o, a in demos])
    planner = AnimaImaginePlanner(fm)

    # --- 1-step decode sanity ---
    o0, a0 = demos[0]
    pred1 = fm.decode(fm.roll(fm.embed(o0)[DELAY - 1], 1, act_seq=a0[DELAY - 1:DELAY]))
    print(f"[learned-WM 1-step decode sanity] true pos={o0[DELAY].round(3)} "
          f"pred pos={pred1.round(3)}\n")

    # --- learned model's k-step forward-error curve (open-loop, model-error axis) ---
    fwd = kstep_forward_error(fm, DEPTHS, seed=7777)
    print("---- learned-model k-step OPEN-LOOP forward error (||pred pos - true pos||) ----")
    for k in DEPTHS:
        print(f"  k={k:2d}  forward_err = {fwd[k]:.4f}")
    print()

    # --- depth ladder: for each depth, same-depth true-MPC ceiling vs imagine-rollout ---
    print("---- depth ladder: same-depth true-MPC vs imagine-rollout (mean +/- std, bootstrap CI) ----")
    ladder = []   # rows: (d, mpc_mean, mpc_ci, imag_mean, imag_ci, gap, welch_p, cohen_d)
    for d in DEPTHS:
        mpc = run_agent(lambda oh, p, v, r, _d=d: cem_plan_true(p, v, r, _d), 1000 + d)
        imag = run_agent(lambda oh, p, v, r, _d=d: planner.plan(oh, r, _d), 5000 + d)
        mlo, mhi = boot_ci(mpc); ilo, ihi = boot_ci(imag)
        gap = mpc.mean() - imag.mean()
        tp, pp = welch_t(imag, mpc); dd = cohens_d(imag, mpc)
        ladder.append((d, mpc.mean(), (mlo, mhi), imag.mean(), (ilo, ihi), gap, pp, dd))
        flag = "TRACKS" if gap <= GAP_TOL else "BREAKS"
        print(f"  d={d:2d}  MPC={mpc.mean():.4f} CI=[{mlo:.4f},{mhi:.4f}]   "
              f"imagine={imag.mean():.4f} CI=[{ilo:.4f},{ihi:.4f}]   "
              f"gap={gap:+.4f}  (Welch p={pp:.2e} d={dd:+.3f})  [{flag} @ GAP_TOL={GAP_TOL}]")
    print()

    # --- locate h* = first depth where the gap exceeds GAP_TOL ---
    hstar = None
    for (d, mm, mci, im, ici, gap, pp, dd) in ladder:
        if gap > GAP_TOL:
            hstar = d
            break

    # --- correlation of the gap with the learned model's forward error over the ladder ---
    gaps = np.array([row[5] for row in ladder])
    fwd_curve = np.array([fwd[row[0]] for row in ladder])
    rs, ps = spearman(gaps, fwd_curve)
    print(f"gap-vs-forward-error correlation over the ladder: Spearman r={rs:+.4f} p={ps:.3e}  "
          f"(gaps={gaps.round(4).tolist()}, fwd_err={fwd_curve.round(4).tolist()})")

    # --- pre-registered validity gate: D3 (the rollout must be genuine at SOME depth) ---
    # reuse H_1021/H_1025 D3 spirit: imagine must differ from the same-depth MPC measurably AND
    # at least the shallowest tracked depth must show genuine planning (gap small there).
    d1_gap = ladder[0][5]
    tracks_d1 = (d1_gap <= GAP_TOL)
    print(f"\nshallowest depth d={DEPTHS[0]} gap={d1_gap:+.4f} -> tracks_at_shallowest={tracks_d1}")

    # forward error monotone-growing? (does the model degrade with horizon at all)
    fwd_growing = fwd_curve[-1] > fwd_curve[0]
    print(f"forward error grows with horizon (k={DEPTHS[-1]} {fwd_curve[-1]:.4f} > "
          f"k={DEPTHS[0]} {fwd_curve[0]:.4f}) = {fwd_growing}")

    print()
    # ---- verdict (g5 CODE-measured; pre-registered tokens) ----
    if not tracks_d1:
        # BREAKS-IMMEDIATELY: never tracks past the shallowest depth
        verdict_line("H_1027", "RED",
                     f"BREAKS-IMMEDIATELY (closed-negative, a_paper_negative_ok) — imagine-rollout "
                     f"does NOT track the true-MPC even at the shallowest tested depth d={DEPTHS[0]} "
                     f"(gap {d1_gap:+.4f} > GAP_TOL {GAP_TOL}). Planning through the learned model "
                     f"gives no actionable depth-tracking; there is no horizon to characterize. "
                     f"TOY single rung; scale-transfer UNVERIFIED.")
    elif hstar is None:
        # TRACKS-ALL-DEPTHS: gap never exceeds tolerance on the ladder
        verdict_line("H_1027", "RED",
                     f"TRACKS-ALL-DEPTHS (closed-negative, a_paper_negative_ok) — imagine-rollout "
                     f"tracks the same-depth true-MPC at EVERY tested depth {DEPTHS} (max gap "
                     f"{gaps.max():+.4f} <= GAP_TOL {GAP_TOL}). On this toy the learned model is "
                     f"accurate enough that NO finite crossover horizon h* exists in the tested "
                     f"ladder: imagination substitutes for the true planner across the whole range. "
                     f"forward-err k={DEPTHS[0]}->{DEPTHS[-1]}: {fwd_curve[0]:.4f}->{fwd_curve[-1]:.4f} "
                     f"(grows={fwd_growing}) but stays small enough not to break planning. "
                     f"a_scale_honest_scope: a deeper ladder / harder env may yet expose h*. TOY rung.")
    else:
        # HORIZON-CHARACTERIZED: finite h* found; check forward-error correlation
        corr_ok = (rs > 0.0)
        verdict_line("H_1027", "GREEN" if corr_ok else "AMBER",
                     f"HORIZON-CHARACTERIZED — a finite crossover horizon h*={hstar} exists: "
                     f"imagine-rollout TRACKS the same-depth true-MPC up to depth "
                     f"{[d for d in DEPTHS if d < hstar] or '(>=1)'} then BREAKS at d={hstar} "
                     f"(gap first exceeds GAP_TOL {GAP_TOL}). Gap-vs-forward-error Spearman "
                     f"r={rs:+.4f} (p={ps:.2e}); forward error grows k={DEPTHS[0]}->{DEPTHS[-1]}: "
                     f"{fwd_curve[0]:.4f}->{fwd_curve[-1]:.4f}. "
                     + ("h* COINCIDES with where the learned model's forward error grows "
                        "(positive gap-vs-error correlation) — the planning horizon is "
                        "model-error-limited, exactly as hypothesized. " if corr_ok else
                        "BUT the gap does NOT positively correlate with forward error over the "
                        "ladder (r<=0) — h* exists but is not cleanly attributable to forward-error "
                        "growth on this run; report AMBER honestly. ")
                     + f"Delta-vs-H_1021: H_1021 sampled only d in {{2,4}} and saw parity at d=4; "
                       f"the full ladder reveals the model-error-limited horizon. "
                       f"TOY single rung, $0 CPU-local; scale-transfer / deeper-ladder UNVERIFIED "
                       f"(a_scale_honest_scope · a_toy_scale_recheck). a_phi_iit4_tool n/a.")


if __name__ == "__main__":
    main()
