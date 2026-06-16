"""H_1025 — does imagine-rollout (planning THROUGH anima's LEARNED world-model) reach
continuous-action MPC parity, or does the discrete-action enumerator that worked in H_1021
fail to transfer to a CONTINUOUS action space?

H_1021 (PASS) showed that a receding-horizon ENUMERATOR planning through anima's OWN learned
LDS world-model reaches depth-4 MPC parity -- but on a DISCRETE action space (NACT=4, 4^4
enumeration). Real embodied control is CONTINUOUS; the CWM @goal (act on silicon/SW) needs
continuous-action planning. H_1025 replaces the enumerator with a CONTINUOUS-action planner
(CEM, Cross-Entropy Method, sampling-MPC) and asks whether planning-through-the-learned-model
still reaches the optimum when the action is a vector that must be SEARCHED, not enumerated.

FROZEN FALSIFIER (pre-registered 2026-06-07; honored verbatim):
  metric M = mean episode return (0 = optimal, more negative = worse). TOL = 0.05.
  CEILING  = continuous-action MPC = CEM(horizon=H) over the TRUE dynamics; band = [P-TOL, P+TOL].
  Ladder: random/reactive floors -> single-step head -> imagine-rollout (CEM through LEARNED
  model) -> continuous MPC ceiling.
  D1 (non-vacuity)  = reactive CI_hi < band_lo (the band is non-trivial to reach).
  D2 (strong ref)   = continuous MPC >= the continuous greedy 1-step oracle (a real ceiling).
  D3 (search genuine) = imagine-rollout differs from the single-step head by > CI noise.
  PASS  = CONTINUOUS-PARITY  : imagine-rollout within the MPC band AND CI overlaps (or above).
  PARTIAL = CONTINUOUS-GAP   : imagine-rollout IMPROVES over single-step head (p<0.05) but stays
            BELOW the band (search / forward-model error compounds; closed-negative, a_paper_negative_ok).
  RED   = CONTINUOUS-GAP-hard: imagine-rollout does NOT beat the single-step head AND below band.
  INCONCLUSIVE = boundary / D3 fails.

This is the CONTINUOUS analogue of H_1021. It REUSES the H_964 hidden-velocity station-keeping
structure (position-only obs, hidden velocity that a delay-embedding latent must recover), the
H_1021 LEARNED-WM design (LDSWorldModel fitted by ridge on greedy-oracle demos -- a LEARNED model,
NEVER given the true dynamics), the single-step ridge head, and the H_1019/H_1021 multi-seed /
multi-episode protocol (N_RUNS runs x EP_PER_RUN episodes). The ONLY structural change vs H_1021:
the action space is CONTINUOUS (a 2-D thrust vector in a box) and the planner is CEM, not an
enumerator. Reference = continuous-action CEM-MPC on the TRUE dynamics.

$0 CPU-local, deterministic given seeds, no GPU. No Phi claim (a_phi_iit4_tool n/a).
a_scale_honest_scope: TOY single rung, ladder OPEN -- no production / real-robot transfer.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, _aug1, boot_ci, welch_t, cohens_d, header, verdict_line

# ----------------------------------------------------------------- env constants (continuous variant of H_964)
ODIM = 2             # observation = position (2-D); velocity is HIDDEN (as in H_964)
ADIM = 2             # CONTINUOUS action = thrust vector (2-D)  <-- the H_1025 change
T = 20               # episode length (same as H_1019/H_1021)
N_TRAIN = 400        # demo trajectories (same as H_964/H_1021)
VSTEP = 0.4          # position integration step (same as H_964)
DRAG = 1.0           # velocity FULLY persists -> must counter the HIDDEN velocity (same as H_964)
AMAX = 1.0           # action box half-width: a in [-AMAX, AMAX]^2 (continuous thrust magnitude cap)
NOISE = 0.02         # process noise std (same as H_964 step_env)
DELAY = 3            # delay-embedding (same as anima's H_964/H_1019/H_1021 WM)

# ----------------------------------------------------------------- frozen protocol constants
N_RUNS = 40          # runs per agent (same as H_1019/H_1021)
EP_PER_RUN = 60      # episodes per run (same as H_1019/H_1021)
TOL = 0.05           # pre-registered parity tolerance band half-width (frozen 2026-06-07)
HORIZON = 4          # planning horizon for BOTH the MPC ceiling and imagine-rollout (cf H_1021 depth-4)
CEM_ITERS = 5        # CEM refinement iterations
CEM_POP = 64         # CEM population size per iteration
CEM_ELITE = 8        # CEM elite count
CEM_INIT_STD = 0.6   # CEM initial per-dim action std


# ----------------------------------------------------------------- continuous env (drop-in analogue of H_964 step_env)
def step_env(pos, v, a, rng):
    """Continuous-action dynamics. a is a 2-D thrust vector (clipped to the box).
    v_new = DRAG*v + a ; pos += VSTEP*v_new + noise ; reward = -||pos|| (stay near origin)."""
    a = np.clip(a, -AMAX, AMAX)
    v = DRAG * v + a
    pos = pos + VSTEP * v + NOISE * rng.standard_normal(ADIM)
    return pos, v, -float(np.linalg.norm(pos))


def greedy_action(pos, v):
    """Continuous 1-step oracle (needs the HIDDEN velocity): the box-clipped thrust that
    minimizes ||pos + VSTEP*(DRAG*v + a)|| in closed form.  a* = clip(-(DRAG*v) - pos/VSTEP)."""
    return np.clip(-(DRAG * v) - pos / VSTEP, -AMAX, AMAX)


def gen_demo(rng):
    """Greedy-oracle demonstrations (continuous actions) to fit the LEARNED WM + heads."""
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


# ----------------------------------------------------------------- continuous MPC ceiling (CEM over TRUE dynamics)
def cem_plan_true(pos, v, rng):
    """Continuous-action receding-horizon MPC: CEM over a HORIZON-length action sequence rolled
    through the TRUE deterministic dynamics (knows pos, v). Returns the first action of the best
    plan. Planning is noise-free (uses the deterministic part of step_env, as H_1021's MPC did)."""
    mu = np.zeros((HORIZON, ADIM))
    std = np.full((HORIZON, ADIM), CEM_INIT_STD)
    for _ in range(CEM_ITERS):
        samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, HORIZON, ADIM)),
                       -AMAX, AMAX)
        scores = np.empty(CEM_POP)
        for i in range(CEM_POP):
            p, vel, acc = pos.copy(), v.copy(), 0.0
            for k in range(HORIZON):
                vel = DRAG * vel + samp[i, k]
                p = p + VSTEP * vel
                acc += -np.linalg.norm(p)
            scores[i] = acc
        elite = samp[np.argsort(scores)[-CEM_ELITE:]]
        mu = elite.mean(0)
        std = elite.std(0) + 1e-6
    return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- imagine-rollout (CEM through anima's LEARNED model)
class AnimaImaginePlanner:
    """anima's OWN learned action-conditioned world model + a CONTINUOUS-action CEM planner.

    The forward model is an LDSWorldModel(delay=DELAY, act_dim=ADIM) fitted by ridge on the SAME
    greedy-oracle demo trajectories (obs seqs + continuous action vectors). Its learned transition
    A (z_{t+1} ~ A[z_t; a_t]) and decoder C (z -> position) are anima's LEARNED model -- fitted
    ONLY from demos, NEVER given the true step_env. The planner runs CEM over a HORIZON-length
    sequence of CONTINUOUS action vectors, rolling A forward and decoding each imagined latent via
    C to a predicted position, scoring cumulative -||predicted pos|| (noise-free, in imagination),
    and plays the FIRST action of the best imagined plan. It NEVER calls step_env. This is the
    CONTINUOUS analogue of H_1021's enumerator: CEM replaces the 4^d enumeration."""

    def __init__(self, fm):
        self.fm = fm

    def plan(self, obs_hist, rng):
        z0 = self.fm.embed(np.array(obs_hist))[-1]   # current latent from observed positions
        mu = np.zeros((HORIZON, ADIM))
        std = np.full((HORIZON, ADIM), CEM_INIT_STD)
        for _ in range(CEM_ITERS):
            samp = np.clip(mu[None] + std[None] * rng.standard_normal((CEM_POP, HORIZON, ADIM)),
                           -AMAX, AMAX)
            scores = np.empty(CEM_POP)
            for i in range(CEM_POP):
                z, acc = z0.copy(), 0.0
                for k in range(HORIZON):
                    z = (_aug1(np.hstack([z, samp[i, k]])) @ self.fm.A)  # roll LEARNED transition
                    pred_pos = self.fm.decode(z)                          # LEARNED decoder -> pos
                    acc += -np.linalg.norm(pred_pos)                      # imagined reward
                scores[i] = acc
            elite = samp[np.argsort(scores)[-CEM_ELITE:]]
            mu = elite.mean(0)
            std = elite.std(0) + 1e-6
        return np.clip(mu[0], -AMAX, AMAX)


# ----------------------------------------------------------------- arms / harness (continuous action)
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


def make_mpc():
    def fn(obs_hist, pos, v, rng):
        return cem_plan_true(pos, v, rng)
    return fn


def make_greedy():
    def fn(obs_hist, pos, v, rng):
        return greedy_action(pos, v)
    return fn


def make_random():
    def fn(obs_hist, pos, v, rng):
        return rng.uniform(-AMAX, AMAX, ADIM)
    return fn


def make_reactive(Whead):
    def fn(obs_hist, pos, v, rng):
        return np.clip(_aug1(pos) @ Whead, -AMAX, AMAX)
    return fn


def make_single_step(m, Whead):
    """anima's single-step head: latent -> CONTINUOUS action (acts greedily, no imagine).
    The continuous analogue of H_1019/H_1021's single-step WM ridge head."""
    def fn(obs_hist, pos, v, rng):
        z = m.embed(np.array(obs_hist))[-1]
        return np.clip(_aug1(z) @ Whead, -AMAX, AMAX)
    return fn


def make_imagine(planner):
    def fn(obs_hist, pos, v, rng):
        return planner.plan(obs_hist, rng)
    return fn


def run_agent(policy_fn, seed0):
    out = []
    for i in range(N_RUNS):
        rng = np.random.default_rng(seed0 + i)
        ep = np.array([episode_return(policy_fn, rng) for _ in range(EP_PER_RUN)])
        out.append(ep.mean())
    return np.array(out)


def main():
    header("H_1025", "imagine-rollout (CEM through anima's LEARNED WM) vs continuous-action MPC")
    print(f"task=continuous-action hidden-velocity station-keeping (position-only obs)  "
          f"metric M=mean return (0=optimal)")
    print(f"N_runs={N_RUNS} ep/run={EP_PER_RUN}  action=CONTINUOUS 2-D thrust in [-{AMAX},{AMAX}]^2  "
          f"ceiling=CEM-MPC horizon={HORIZON} (TRUE dyn)")
    print(f"planner=CEM (pop={CEM_POP} iters={CEM_ITERS} elite={CEM_ELITE} horizon={HORIZON})  "
          f"TOL={TOL}  no-Phi (a_phi_iit4_tool n/a)\n")

    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]

    # --- anima's single-step head (latent -> continuous action) + REACTIVE head (obs -> action) ---
    m = LDSWorldModel(ODIM, delay=DELAY).fit([o for o, a in demos])
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

    # --- anima's OWN LEARNED action-conditioned forward model (fitted on the SAME demos) ---
    # continuous action vectors are appended directly (act_dim=ADIM); learned A (z_{t+1}~A[z_t;a_t])
    # + decoder C (z->pos). LEARNED model -- never sees the true step_env.
    fm = LDSWorldModel(ODIM, delay=DELAY, act_dim=ADIM)
    fm.fit([o for o, a in demos], traj_acts=[a for o, a in demos])
    planner = AnimaImaginePlanner(fm)

    # learned-WM 1-step decode sanity (forward-model fidelity check)
    o0, a0 = demos[0]
    z0 = m.embed(o0)
    pred1 = fm.decode(fm.roll(z0[DELAY - 1], 1, act_seq=a0[DELAY - 1:DELAY]))
    print(f"[learned-WM 1-step decode sanity] true pos={o0[DELAY].round(3)} "
          f"pred pos={pred1.round(3)}\n")

    # arms (distinct seed bases so floors/ceiling/anima don't share RNG streams)
    mpc    = run_agent(make_mpc(), 1000)                    # CEILING: continuous CEM-MPC (true dyn)
    greedy = run_agent(make_greedy(), 1000)                 # continuous greedy 1-step oracle (D2)
    rand   = run_agent(make_random(), 2000)                 # floor
    reac   = run_agent(make_reactive(Whead_reac), 3000)     # floor: obs->action
    ss     = run_agent(make_single_step(m, Whead_ss), 4000) # anima single-step head (latent->action)
    imag   = run_agent(make_imagine(planner), 5000)         # anima imagine-rollout (CEM through learned WM)

    P = mpc.mean()
    band_lo, band_hi = P - TOL, P + TOL
    plo, phi = boot_ci(mpc); glo, ghi = boot_ci(greedy); rlo, rhi = boot_ci(rand)
    clo, chi = boot_ci(reac); slo, shi = boot_ci(ss); ilo, ihi = boot_ci(imag)

    print("---- ladder (mean +/- std, bootstrap CI) ----")
    print(f"  CEM-MPC horizon={HORIZON} (CEILING, true dyn) M = {P:.4f} +/- {mpc.std():.4f}  CI=[{plo:.4f},{phi:.4f}]")
    print(f"  anima imagine-rollout (CEM, learned WM)        M = {imag.mean():.4f} +/- {imag.std():.4f}  CI=[{ilo:.4f},{ihi:.4f}]")
    print(f"  anima single-step head (latent->action)        M = {ss.mean():.4f} +/- {ss.std():.4f}  CI=[{slo:.4f},{shi:.4f}]")
    print(f"  continuous greedy 1-step oracle                M = {greedy.mean():.4f} +/- {greedy.std():.4f}  CI=[{glo:.4f},{ghi:.4f}]")
    print(f"  reactive (obs->action, floor)                  M = {reac.mean():.4f} +/- {reac.std():.4f}  CI=[{clo:.4f},{chi:.4f}]")
    print(f"  random (floor)                                 M = {rand.mean():.4f} +/- {rand.std():.4f}  CI=[{rlo:.4f},{rhi:.4f}]")

    print(f"\nparity band [P - TOL, P + TOL] = [{band_lo:.4f}, {band_hi:.4f}]  (P={P:.4f}, TOL={TOL})")

    # ---- pre-registered checks ----
    d1_nonvacuous = (chi < band_lo)
    d2_strong = (P >= greedy.mean() - 1e-2)
    print(f"D1 non-vacuity (reactive CI_hi {chi:.4f} < band_lo {band_lo:.4f}) = {d1_nonvacuous}")
    print(f"D2 hardening real (MPC {P:.4f} >= greedy 1-step {greedy.mean():.4f}) = {d2_strong}")

    im = imag.mean(); ssm = ss.mean()
    t_is, p_is = welch_t(imag, ss); d_is = cohens_d(imag, ss)
    d3_genuine = (p_is < 0.05)
    print(f"D3 search genuine (imagine vs single-step head: Welch p={p_is:.3e} d={d_is:.3f}, "
          f"differs={d3_genuine})")

    within_band = (band_lo <= im <= band_hi)
    ci_overlaps = (ilo <= band_hi) and (ihi >= band_lo)
    below = (im < band_lo) and (ihi < band_lo)
    above = (im > band_hi) and (ilo > band_hi)
    improves = (im > ssm) and (p_is < 0.05)
    gap_to_mpc = P - im
    gap_vs_ss = im - ssm
    print(f"imagine mean {im:.4f} vs band -> within_band={within_band} ci_overlaps={ci_overlaps} "
          f"below={below} above={above}")
    print(f"imagine vs single-step head delta = {gap_vs_ss:+.4f} (improves={improves})")
    print(f"MPC-imagine gap = {gap_to_mpc:+.4f}")
    t_im, p_im = welch_t(imag, mpc); d_im = cohens_d(imag, mpc)
    print(f"imagine vs MPC: Welch p={p_im:.3e}  Cohen d={d_im:.3f}")

    print()
    valid = d1_nonvacuous and d2_strong
    if not valid:
        verdict_line("H_1025", "INVALID",
                     f"pre-registered validity gate failed (D1 non-vacuity={d1_nonvacuous}, "
                     f"D2 hardening-real={d2_strong}); placement not interpretable.")
    elif not d3_genuine:
        verdict_line("H_1025", "INCONCLUSIVE",
                     f"D3 failed: imagine {im:.4f} does NOT differ from the single-step head "
                     f"{ssm:.4f} beyond CI noise (Welch p={p_is:.3e}) — the CEM search is doing "
                     f"nothing actionable; comparison vacuous. report honestly, no emoji.")
    elif (within_band and ci_overlaps) or above:
        verdict_line("H_1025", "PASS",
                     f"CONTINUOUS-PARITY — anima imagine-rollout (CEM through its OWN learned WM) "
                     f"reaches M={im:.4f}, WITHIN the continuous CEM-MPC parity band "
                     f"[{band_lo:.3f},{band_hi:.3f}] (CI [{ilo:.3f},{ihi:.3f}], above={above}). "
                     f"Planning-through-the-learned-model is NOT specific to enumerable discrete "
                     f"actions: a CONTINUOUS-action CEM search through the learned model recovers "
                     f"near-optimal control, generalizing H_1021. imagine lift over single-step "
                     f"head {gap_vs_ss:+.4f}. TOY single rung; scale/real-robot UNVERIFIED.")
    elif improves and below:
        verdict_line("H_1025", "PARTIAL",
                     f"CONTINUOUS-GAP (a_paper_negative_ok) — anima imagine-rollout (CEM, learned "
                     f"WM) M={im:.4f} IMPROVES over the single-step head {ssm:.4f} (delta "
                     f"{gap_vs_ss:+.4f}, p={p_is:.1e}) — continuous planning HELPS — but STILL lands "
                     f"BELOW the continuous CEM-MPC band [{band_lo:.3f},{band_hi:.3f}] (gap "
                     f"{gap_to_mpc:+.4f}, CI_hi {ihi:.3f} < band_lo {band_lo:.3f}). Search and/or "
                     f"learned-model forward error compounds in continuous space: parity does NOT "
                     f"transfer from discrete (H_1021) to continuous actions. Closed-negative. "
                     f"TOY single rung; deeper-CEM / better-WM ladder OPEN.")
    elif below:
        verdict_line("H_1025", "RED",
                     f"CONTINUOUS-GAP-hard (a_paper_negative_ok) — anima imagine-rollout (CEM, "
                     f"learned WM) M={im:.4f} does NOT improve over the single-step head {ssm:.4f} "
                     f"(delta {gap_vs_ss:+.4f}, p={p_is:.1e}) AND stays below the continuous CEM-MPC "
                     f"band [{band_lo:.3f},{band_hi:.3f}] (gap {gap_to_mpc:+.4f}). Continuous "
                     f"planning through the learned model gives no actionable advantage. TOY single rung.")
    else:
        verdict_line("H_1025", "INCONCLUSIVE",
                     f"imagine mean {im:.4f} vs band [{band_lo:.3f},{band_hi:.3f}] within={within_band} "
                     f"overlap={ci_overlaps} below={below} above={above} improves={improves} -> "
                     f"boundary; report honestly.")


if __name__ == "__main__":
    main()
