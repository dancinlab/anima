"""H_1021 — does planning THROUGH anima's LEARNED world-model close the H_1019 gap?

H_1019 (RED CLOSED-NEG) hardened the human reference to a depth-4 receding-horizon MPC and
found anima's single-step ridge head (latent->action, M=-0.6426) lands BELOW the MPC band
[-0.6034,-0.5034] (gap +0.0892, d=-1.98). H_1019's own diagnosis: anima only ACTED single-step.
The CWM @goal is perceive->latent->IMAGINE->act. H_1021 gives anima the IMAGINE step: a
receding-horizon planner that rolls anima's OWN LEARNED action-conditioned world model forward
over a horizon (Dreamer-style model-predictive control THROUGH the learned forward model -- NOT
the true dynamics, which would just BE the MPC) and plays the first action of the best imagined
plan. Does this close the gap (inference-DEPTH limit) or not (the learned model's forward error
COMPOUNDS over the horizon -> WM-fidelity limit, a_paper_negative_ok)?

FROZEN FALSIFIER (honored; env/MPC/floors VERBATIM from H_1019, same seeds):
  metric M = mean episode return (0 = optimal, more negative = worse). TOL = 0.05.
  CEILING  = depth-4 MPC (true human ref); band = [P - TOL, P + TOL].
  D1 (non-vacuity) = reactive CI_hi < band_lo. D2 (strong ref) = MPC >= greedy ref (-0.8906).
  D3 (rollout is genuine planning) = imagine-d4 differs from single-step WM by > CI noise.
  PASS (gap closed / inference-depth limit) = imagine-d4 within band AND CI overlaps (or above band).
  PARTIAL (model-error-bounded) = imagine-d4 ABOVE single-step WM by > CI noise BUT still < band_lo.
  RED (planning does not help) = imagine-d4 NOT above single-step WM AND < band_lo.
  INCONCLUSIVE = boundary / D3 fails.

Reuses the H_964 env + H_1019 MPC/floors harness VERBATIM. anima's single-step head trains EXACTLY
as H_964/H_1019. NEW: anima's OWN learned action-conditioned LDSWorldModel (fitted by ridge on the
SAME greedy demos) + a receding-horizon enumerator that plans THROUGH that learned model.
$0 CPU-local, deterministic given seeds, no GPU, no Phi.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from itertools import product
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, _aug1, boot_ci, welch_t, cohens_d, header, verdict_line
from h964_latent_policy import (step_env, optimal_action, gen_demo, ODIM, NACT, T, N_TRAIN,
                                THRUSTS, DRAG, VSTEP)

N_RUNS = 40          # runs per agent (same as H_1019)
EP_PER_RUN = 60      # episodes per run (same as H_1019)
TOL = 0.05           # pre-registered parity tolerance band half-width (frozen 2026-06-07)
MPC_DEPTH = 4        # receding-horizon TRUE-dynamics MPC ceiling (NACT^4 = 256 rollouts/step)
IMAGINE_DEPTHS = (2, 4)   # imagine-rollout planning depths through the LEARNED model
GREEDY_NOLAPSE_REF = -0.8906   # H_1018/H_1019 no-lapse greedy-oracle mean (D2 hardening check)
DELAY = 3            # delay-embedding (same as anima's H_964/H_1019 WM)


# ---------------------------------------------------------------- depth-4 MPC (TRUE dynamics ceiling, VERBATIM from H_1019)
def mpc_action(pos, v, depth):
    """Hardened human reference: exhaustive depth-`depth` receding-horizon planner over the
    TRUE deterministic dynamics (knows pos, v, step_env). VERBATIM from H_1019."""
    best_score = [-1e18]
    best_first = [0]

    def rec(p, vel, d, first, acc):
        if d == 0:
            if acc > best_score[0]:
                best_score[0] = acc
                best_first[0] = first
            return
        for a in range(NACT):
            vn = DRAG * vel + 0.6 * THRUSTS[a]
            pn = p + VSTEP * vn                     # deterministic part of step_env
            r = -np.linalg.norm(pn)
            rec(pn, vn, d - 1, a if first is None else first, acc + r)

    rec(pos, v, depth, None, 0.0)
    return best_first[0]


# ---------------------------------------------------------------- anima's LEARNED forward model + imagine-rollout planner
class AnimaLearnedWM:
    """anima's OWN learned action-conditioned world model + a receding-horizon imagine planner.

    The forward model is an LDSWorldModel(delay=DELAY, act_dim=NACT) fitted by ridge regression
    on the SAME greedy-oracle demonstration trajectories (obs seqs + action one-hots). Its learned
    transition A (z_{t+1} ~ A[z_t; a_t]) and learned decoder C (z -> position) are anima's LEARNED
    model -- fitted ONLY from demos, never given the true step_env. The planner enumerates every
    length-d action sequence, rolls A forward conditioned on the candidate actions, decodes each
    imagined latent via C to a predicted position, scores cumulative -||predicted pos|| (noise-free,
    in imagination), and plays the FIRST action of the best imagined plan. It NEVER calls step_env.
    """

    def __init__(self, fm):
        self.fm = fm
        # pre-enumerate action sequences per depth (NACT^d each); cheap at NACT=4, d<=4
        self._seqs = {d: [np.array([np.eye(NACT)[a] for a in seq], dtype=float)
                          for seq in product(range(NACT), repeat=d)]
                      for d in IMAGINE_DEPTHS}

    def plan(self, obs_hist, depth):
        """Return the first action of the best imagined depth-`depth` plan through the learned WM."""
        z0 = self.fm.embed(np.array(obs_hist))[-1]      # current latent from observed positions
        best_score, best_first = -1e18, 0
        for seq in self._seqs[depth]:
            z = z0.copy()
            acc = 0.0
            for k in range(depth):
                z = (_aug1(np.hstack([z, seq[k]])) @ self.fm.A)   # roll LEARNED transition fwd
                pred_pos = self.fm.decode(z)                       # LEARNED decoder -> position
                acc += -np.linalg.norm(pred_pos)                  # imagined reward
            if acc > best_score:
                best_score = acc
                best_first = int(seq[0].argmax())
        return best_first


# ---------------------------------------------------------------- arms / harness (VERBATIM signature from H_1019)
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


def make_mpc(depth):
    def fn(obs_hist, pos, v, rng):
        return mpc_action(pos, v, depth)
    return fn


def make_greedy():
    def fn(obs_hist, pos, v, rng):
        return optimal_action(pos, v)
    return fn


def make_random():
    def fn(obs_hist, pos, v, rng):
        return rng.integers(NACT)
    return fn


def make_reactive(Whead):
    def fn(obs_hist, pos, v, rng):
        return int((_aug(pos[None, :]) @ Whead).argmax())
    return fn


def make_wam(m, Whead):
    """anima's H_1019 single-step ridge head: latent -> action (acts greedily, no imagine)."""
    def fn(obs_hist, pos, v, rng):
        z = m.embed(np.array(obs_hist))[-1]
        return int((_aug(z[None, :]) @ Whead).argmax())
    return fn


def make_imagine(planner, depth):
    """anima imagine-rollout: plan THROUGH the learned WM over `depth`, play first action."""
    def fn(obs_hist, pos, v, rng):
        return planner.plan(obs_hist, depth)
    return fn


def run_agent(policy_fn, seed0):
    out = []
    for i in range(N_RUNS):
        rng = np.random.default_rng(seed0 + i)
        ep = np.array([episode_return(policy_fn, rng) for _ in range(EP_PER_RUN)])
        out.append(ep.mean())
    return np.array(out)


def main():
    header("H_1021", "imagine-rollout through anima's LEARNED world-model vs depth-4 MPC")
    print(f"task=H_964 hidden-velocity station-keeping (position-only obs)  metric M=mean return "
          f"(0=optimal)\nN_runs={N_RUNS} ep/run={EP_PER_RUN}  ceiling=depth-{MPC_DEPTH} MPC (TRUE "
          f"dynamics)  imagine depths={IMAGINE_DEPTHS} (through the LEARNED model)  TOL={TOL}\n")

    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]

    # --- anima's single-step WM head (latent->action) + REACTIVE head, EXACTLY as H_964/H_1019 ---
    m = LDSWorldModel(ODIM, delay=DELAY).fit([o for o, a in demos])
    Zw, Yw = [], []
    for o, a in demos:
        z = m.embed(o)
        for t in range(2, T):
            Zw.append(z[t]); Yw.append(np.eye(NACT)[a[t]])
    Whead_wam = _ridge(_aug(np.array(Zw)), np.array(Yw), 1e-2)
    Xr, Yr = [], []
    for o, a in demos:
        for t in range(T):
            Xr.append(o[t]); Yr.append(np.eye(NACT)[a[t]])
    Whead_reac = _ridge(_aug(np.array(Xr)), np.array(Yr), 1e-2)

    # --- anima's OWN LEARNED action-conditioned forward model (fitted on the SAME demos) ---
    # obs seqs + action one-hots -> learned transition A (z_{t+1}~A[z_t;a_t]) + decoder C (z->pos).
    # This is anima's LEARNED model, fitted ONLY from demos; it never sees the true step_env.
    fm = LDSWorldModel(ODIM, delay=DELAY, act_dim=NACT)
    fm.fit([o for o, a in demos], traj_acts=[np.eye(NACT)[a] for o, a in demos])
    planner = AnimaLearnedWM(fm)

    # quick one-step forward-model sanity (learned-A error on held-out-style demo transitions)
    z = m.embed(demos[0][0]); ah = np.eye(NACT)[demos[0][1]]
    pred1 = fm.decode(fm.roll(z[0], 1, act_seq=ah[0:1]))
    print(f"[learned-WM 1-step decode sanity] true pos[1]={demos[0][0][1].round(3)} "
          f"pred pos[1]={pred1.round(3)}\n")

    # same seeds as H_1019
    mpc    = run_agent(make_mpc(MPC_DEPTH), 1000)          # CEILING: depth-4 TRUE-dynamics MPC
    greedy = run_agent(make_greedy(), 1000)               # greedy oracle (D2 check)
    rand   = run_agent(make_random(), 2000)               # floor
    reac   = run_agent(make_reactive(Whead_reac), 3000)   # floor
    wam    = run_agent(make_wam(m, Whead_wam), 4000)      # anima single-step WM (H_1019 rung)
    imag   = {d: run_agent(make_imagine(planner, d), 4000) for d in IMAGINE_DEPTHS}  # imagine-rollout

    P = mpc.mean()
    band_lo, band_hi = P - TOL, P + TOL
    plo, phi = boot_ci(mpc); glo, ghi = boot_ci(greedy); rlo, rhi = boot_ci(rand)
    clo, chi = boot_ci(reac); wlo, whi = boot_ci(wam)
    ici = {d: boot_ci(imag[d]) for d in IMAGINE_DEPTHS}

    print("---- ladder (mean +/- std, bootstrap CI) ----")
    print(f"  depth-{MPC_DEPTH} MPC (CEILING, true dyn) M = {P:.4f} +/- {mpc.std():.4f}  CI=[{plo:.4f},{phi:.4f}]")
    for d in IMAGINE_DEPTHS:
        print(f"  anima imagine-rollout d={d} (learned) M = {imag[d].mean():.4f} +/- {imag[d].std():.4f}"
              f"  CI=[{ici[d][0]:.4f},{ici[d][1]:.4f}]")
    print(f"  anima single-step WM (H_1019 rung)   M = {wam.mean():.4f} +/- {wam.std():.4f}  CI=[{wlo:.4f},{whi:.4f}]")
    print(f"  greedy oracle (depth-1)              M = {greedy.mean():.4f} +/- {greedy.std():.4f}  CI=[{glo:.4f},{ghi:.4f}]")
    print(f"  reactive (single-frame, floor)       M = {reac.mean():.4f} +/- {reac.std():.4f}  CI=[{clo:.4f},{chi:.4f}]")
    print(f"  random (floor)                       M = {rand.mean():.4f} +/- {rand.std():.4f}  CI=[{rlo:.4f},{rhi:.4f}]")

    print(f"\nparity band [P - TOL, P + TOL] = [{band_lo:.4f}, {band_hi:.4f}]  (P={P:.4f}, TOL={TOL})")

    # ---- pre-registered checks ----
    d1_nonvacuous = (chi < band_lo)
    d2_strong = (P >= GREEDY_NOLAPSE_REF - 1e-2)
    print(f"D1 non-vacuity (reactive CI_hi {chi:.4f} < band_lo {band_lo:.4f}) = {d1_nonvacuous}")
    print(f"D2 hardening real (MPC {P:.4f} >= greedy-ref {GREEDY_NOLAPSE_REF}) = {d2_strong}")

    d4 = imag[4]
    i4m = d4.mean(); i4lo, i4hi = ici[4]
    wm_m = wam.mean()
    # D3: imagine-d4 differs from single-step WM by > CI noise (genuine planning effect)
    t_iw, p_iw = welch_t(d4, wam); d_iw = cohens_d(d4, wam)
    d3_genuine = (p_iw < 0.05)
    print(f"D3 rollout genuine (imagine-d4 vs single-step WM: Welch p={p_iw:.3e} d={d_iw:.3f}, "
          f"differs={d3_genuine})")

    # band relations for imagine-d4
    within_band = (band_lo <= i4m <= band_hi)
    ci_overlaps = (i4lo <= band_hi) and (i4hi >= band_lo)
    below = (i4m < band_lo) and (i4hi < band_lo)
    above = (i4m > band_hi) and (i4lo > band_hi)
    # improvement over single-step WM (higher return = less negative = better)
    improves = (i4m > wm_m) and (p_iw < 0.05)
    gap_to_mpc = P - i4m
    gap_vs_wm = i4m - wm_m
    print(f"imagine-d4 mean {i4m:.4f} vs band -> within_band={within_band} ci_overlaps={ci_overlaps} "
          f"below={below} above={above}")
    print(f"imagine-d4 vs single-step WM delta = {gap_vs_wm:+.4f} (improves={improves})")
    print(f"MPC-imagine_d4 gap = {gap_to_mpc:+.4f}")
    # imagine-d2 reference numbers too
    i2 = imag[2]
    print(f"imagine-d2 mean {i2.mean():.4f}  (vs single-step WM delta {i2.mean()-wm_m:+.4f}, "
          f"vs MPC gap {P-i2.mean():+.4f})")
    t_im, p_im = welch_t(d4, mpc); d_im = cohens_d(d4, mpc)
    print(f"imagine-d4 vs MPC: Welch p={p_im:.3e}  Cohen d={d_im:.3f}")

    print()
    valid = d1_nonvacuous and d2_strong
    if not valid:
        verdict_line("H_1021", "INVALID",
                     f"pre-registered validity gate failed (D1 non-vacuity={d1_nonvacuous}, "
                     f"D2 hardening-real={d2_strong}); placement not interpretable.")
    elif not d3_genuine:
        verdict_line("H_1021", "INCONCLUSIVE",
                     f"D3 failed: imagine-d4 {i4m:.4f} does NOT differ from the single-step WM "
                     f"{wm_m:.4f} beyond CI noise (Welch p={p_iw:.3e}) — the rollout is doing nothing "
                     f"actionable; comparison vacuous. report honestly, no emoji.")
    elif within_band and ci_overlaps:
        verdict_line("H_1021", "PASS",
                     f"GAP CLOSED (inference-DEPTH limit) — anima imagine-rollout d=4 through its OWN "
                     f"learned WM reaches M={i4m:.4f}, WITHIN the depth-{MPC_DEPTH} MPC parity band "
                     f"[{band_lo:.3f},{band_hi:.3f}] (CI [{i4lo:.3f},{i4hi:.3f}] overlaps). Planning "
                     f"THROUGH the learned model recovers near-optimal control: the H_1019 gap "
                     f"(single-step WM {wm_m:.4f}) was an inference-DEPTH limit, NOT a WM-quality "
                     f"limit. imagine lift over single-step WM {gap_vs_wm:+.4f}. TOY single rung; "
                     f"scale-transfer UNVERIFIED.")
    elif above:
        verdict_line("H_1021", "GREEN-PLUS",
                     f"ABOVE THE TRUE OPTIMUM — anima imagine-rollout d=4 M={i4m:.4f} EXCEEDS even the "
                     f"depth-{MPC_DEPTH} MPC P={P:.4f} (CI_lo {i4lo:.3f} > band_hi {band_hi:.3f}). "
                     f"Planning through the learned model not only closes but beats the true-dynamics "
                     f"reference (scoped to this discrete-action toy). imagine lift {gap_vs_wm:+.4f}. "
                     f"TOY single rung; scale-transfer UNVERIFIED.")
    elif improves and below:
        verdict_line("H_1021", "PARTIAL",
                     f"MODEL-ERROR-BOUNDED (a_paper_negative_ok) — anima imagine-rollout d=4 M={i4m:.4f} "
                     f"IMPROVES over the single-step WM {wm_m:.4f} (delta {gap_vs_wm:+.4f}, p={p_iw:.1e}) "
                     f"— planning through the learned model HELPS — but STILL lands below the depth-"
                     f"{MPC_DEPTH} MPC band [{band_lo:.3f},{band_hi:.3f}] (gap {gap_to_mpc:+.4f}, CI_hi "
                     f"{i4hi:.3f} < band_lo {band_lo:.3f}). The learned model's forward-prediction error "
                     f"COMPOUNDS over the horizon, so the H_1019 gap is a WM-FIDELITY limit, not purely "
                     f"an inference-depth one. TOY single rung; deeper/better-WM ladder OPEN.")
    elif below:
        verdict_line("H_1021", "RED",
                     f"CLOSED-NEGATIVE (a_paper_negative_ok) — anima imagine-rollout d=4 M={i4m:.4f} does "
                     f"NOT improve over the single-step WM {wm_m:.4f} (delta {gap_vs_wm:+.4f}, p={p_iw:.1e}) "
                     f"AND stays below the depth-{MPC_DEPTH} MPC band [{band_lo:.3f},{band_hi:.3f}] "
                     f"(gap {gap_to_mpc:+.4f}). The learned model is not accurate enough to plan through: "
                     f"imagined rollouts give no actionable advantage over the single-step head. The "
                     f"H_1019 gap is a WM-fidelity limit. TOY single rung.")
    else:
        verdict_line("H_1021", "INCONCLUSIVE",
                     f"imagine-d4 mean {i4m:.4f} vs band [{band_lo:.3f},{band_hi:.3f}] within={within_band} "
                     f"overlap={ci_overlaps} below={below} above={above} improves={improves} -> boundary; "
                     f"report honestly.")


if __name__ == "__main__":
    main()
