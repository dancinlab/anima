"""H_1019 — north-star HARDENING: anima vs a TRUE multi-step-optimal human reference.

H_1015 placed anima above a hand-coded `optimal_action`, and H_1018 (lapse-free) confirmed
anima beats even the no-lapse oracle. But that oracle is only 1-step-GREEDY (picks the thrust
whose SINGLE next-step position is nearest origin). On a DRAG=1.0 env where velocity fully
persists, the greedy choice is MYOPIC, not the multi-step optimum -> so H_1018's "above-oracle"
is an env/oracle-suboptimality finding. H_1019 HARDENS the human reference to a depth-H
receding-horizon planner (exhaustive NACT^H action-sequence search over the known deterministic
dynamics, knows velocity, plays the first action of the best plan) and re-places anima. Does
anima still clear the bar, or was the H_1018 GREEN-PLUS entirely the myopic-oracle gap?

FROZEN FALSIFIER (honored, identical env/arms/seeds to H_1015/H_1018 except the human reference):
  metric M = mean episode return (0 = optimal, more negative = worse).
  MPC = depth-4 receding-horizon planner (4^4=256 rollouts/step, noise-free planning), the human ref.
  TOL = 0.05 (return units, same as H_1018). band = [MPC - TOL, MPC + TOL].
  D1 (non-vacuity)  = reactive CI_hi < band_lo (single-frame reactive cannot reach the hardened band).
  D2 (strong ref)   = MPC mean >= greedy no-lapse oracle mean (-0.8906) up to noise (hardening is real).
  PASS (parity)     = anima mean within band AND anima CI overlaps band.
  GREEN-PLUS        = anima mean > band_hi AND anima CI_lo > band_hi (above the hardened optimum).
  RED (closed-neg)  = anima mean < band_lo AND anima CI_hi < band_lo (below the TRUE optimum).
  INCONCLUSIVE      = boundary case.

Reuses the H_964 control env + anima/reactive head training VERBATIM (imported) and the
H_1018 boot-CI run-harness. $0 CPU-local, deterministic given seeds, no GPU, no Phi.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, boot_ci, welch_t, cohens_d, header, verdict_line
from h964_latent_policy import (step_env, optimal_action, gen_demo, ODIM, NACT, T, N_TRAIN,
                                THRUSTS, DRAG, VSTEP)

N_RUNS = 40          # runs per agent (same as H_1015/H_1018)
EP_PER_RUN = 60      # episodes per run (same as H_1015/H_1018)
TOL = 0.05           # pre-registered parity tolerance band half-width (frozen 2026-06-07)
MPC_DEPTH = 4        # receding-horizon planning depth (NACT^DEPTH = 4^4 = 256 rollouts/step)
GREEDY_NOLAPSE_REF = -0.8906   # H_1018 no-lapse greedy-oracle mean (for the D2 hardening check)


def mpc_action(pos, v, depth):
    """Hardened human reference: exhaustive depth-`depth` receding-horizon planner.

    Knows the true (pos, v) and the DETERMINISTIC part of step_env (noise excluded in
    planning). Searches every length-`depth` action sequence, scores by cumulative -||pos||,
    returns the FIRST action of the best plan (standard MPC). Recursive enumeration over the
    NACT actions -> NACT^depth leaves; cheap at NACT=4, depth=4 (256/step).
    """
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
    def fn(obs_hist, pos, v, rng):
        z = m.embed(np.array(obs_hist))[-1]
        return int((_aug(z[None, :]) @ Whead).argmax())
    return fn


def run_agent(policy_fn, seed0):
    out = []
    for i in range(N_RUNS):
        rng = np.random.default_rng(seed0 + i)
        ep = np.array([episode_return(policy_fn, rng) for _ in range(EP_PER_RUN)])
        out.append(ep.mean())
    return np.array(out)


def main():
    header("H_1019", "north-star HARDENING (anima vs a TRUE depth-4 MPC human reference)")
    print(f"task=H_964 hidden-velocity station-keeping (position-only obs)  metric M=mean return "
          f"(0=optimal)\nN_runs={N_RUNS} ep/run={EP_PER_RUN}  human-ref=depth-{MPC_DEPTH} receding-"
          f"horizon MPC ({NACT}^{MPC_DEPTH}={NACT**MPC_DEPTH} rollouts/step)  TOL={TOL}\n")

    # --- train anima WM (latent->action) + REACTIVE heads, EXACTLY as H_964/H_1015/H_1018 ---
    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]
    m = LDSWorldModel(ODIM, delay=3).fit([o for o, a in demos])
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

    # same seeds as H_1015/H_1018
    mpc = run_agent(make_mpc(MPC_DEPTH), 1000)    # HARDENED human reference (depth-4 MPC)
    greedy = run_agent(make_greedy(), 1000)       # greedy no-lapse oracle (H_1018 reproduction)
    rand = run_agent(make_random(), 2000)
    reac = run_agent(make_reactive(Whead_reac), 3000)
    anima = run_agent(make_wam(m, Whead_wam), 4000)

    P = mpc.mean()
    band_lo, band_hi = P - TOL, P + TOL
    plo, phi = boot_ci(mpc)
    glo, ghi = boot_ci(greedy)
    rlo, rhi = boot_ci(rand)
    clo, chi = boot_ci(reac)
    alo, ahi = boot_ci(anima)

    print("---- decomposition (mean +/- std, bootstrap CI) ----")
    print(f"  depth-{MPC_DEPTH} MPC (human ref)    M = {P:.4f} +/- {mpc.std():.4f}  CI=[{plo:.4f},{phi:.4f}]")
    print(f"  greedy oracle (depth-1)     M = {greedy.mean():.4f} +/- {greedy.std():.4f}  CI=[{glo:.4f},{ghi:.4f}]")
    print(f"  anima (WM latent->action)   M = {anima.mean():.4f} +/- {anima.std():.4f}  CI=[{alo:.4f},{ahi:.4f}]")
    print(f"  reactive (single-frame)     M = {reac.mean():.4f} +/- {reac.std():.4f}  CI=[{clo:.4f},{chi:.4f}]")
    print(f"  random                      M = {rand.mean():.4f} +/- {rand.std():.4f}  CI=[{rlo:.4f},{rhi:.4f}]")

    hardening = P - greedy.mean()
    print(f"\nhardening delta = MPC - greedy = {P:.4f} - {greedy.mean():.4f} = {hardening:+.4f} "
          f"(return the multi-step plan buys over greedy)")

    # ---- pre-registered checks ----
    d1_nonvacuous = (chi < band_lo)                         # reactive CI_hi below band
    d2_strong = (P >= GREEDY_NOLAPSE_REF - 1e-2)            # MPC at least as good as greedy ref
    print(f"\nparity band [P - TOL, P + TOL] = [{band_lo:.4f}, {band_hi:.4f}]  (P={P:.4f}, TOL={TOL})")
    am = anima.mean()
    within_band = (band_lo <= am <= band_hi)
    ci_overlaps = (alo <= band_hi) and (ahi >= band_lo)
    below = (am < band_lo) and (ahi < band_lo)
    above = (am > band_hi) and (alo > band_hi)
    gap = P - am
    print(f"D1 non-vacuity (reactive CI_hi {chi:.4f} < band_lo {band_lo:.4f}) = {d1_nonvacuous}")
    print(f"D2 hardening real (MPC {P:.4f} >= greedy-ref {GREEDY_NOLAPSE_REF}) = {d2_strong}")
    print(f"anima mean {am:.4f} vs band -> within_band={within_band} ci_overlaps={ci_overlaps} "
          f"below={below} above={above}")
    print(f"MPC-anima gap = {gap:+.4f}")
    t_am, p_am = welch_t(anima, mpc)
    d_am = cohens_d(anima, mpc)
    print(f"anima vs MPC: Welch p={p_am:.3e}  Cohen d={d_am:.3f}")

    print()
    valid = d1_nonvacuous and d2_strong
    if not valid:
        verdict_line("H_1019", "INVALID",
                     f"pre-registered validity gate failed (D1 non-vacuity={d1_nonvacuous}, "
                     f"D2 hardening-real={d2_strong}); placement not interpretable.")
    elif within_band and ci_overlaps:
        verdict_line("H_1019", "PASS",
                     f"GENUINE PARITY with the TRUE optimum — anima mean {am:.4f} within parity band "
                     f"[{band_lo:.3f},{band_hi:.3f}] around the depth-{MPC_DEPTH} MPC P={P:.4f} (anima CI "
                     f"[{alo:.3f},{ahi:.3f}] overlaps band). The north-star placement SURVIVES oracle-"
                     f"hardening: anima is human-level vs a multi-step-optimal reference, NOT just vs a "
                     f"myopic greedy oracle. hardening delta {hardening:+.4f}. TOY single rung; "
                     f"scale-transfer UNVERIFIED.")
    elif above:
        verdict_line("H_1019", "GREEN-PLUS",
                     f"ABOVE THE TRUE OPTIMUM — anima mean {am:.4f} EXCEEDS even the depth-{MPC_DEPTH} MPC "
                     f"P={P:.4f} (anima CI_lo {alo:.3f} > band_hi {band_hi:.3f}). The H_1018 above-oracle "
                     f"is NOT merely the myopic gap; anima clears a hardened multi-step reference (scoped "
                     f"tightly to this discrete-action toy env — NOT a general human-superiority claim). "
                     f"hardening delta {hardening:+.4f}. TOY single rung; scale-transfer UNVERIFIED.")
    elif below:
        verdict_line("H_1019", "RED",
                     f"CLOSED-NEGATIVE (a_paper_negative_ok) — anima mean {am:.4f} BELOW the TRUE "
                     f"depth-{MPC_DEPTH} MPC optimum P={P:.4f} (gap {gap:+.4f}; anima CI_hi {ahi:.3f} < "
                     f"band_lo {band_lo:.3f}); the H_1018 GREEN-PLUS was the MYOPIC-ORACLE gap "
                     f"(hardening delta {hardening:+.4f}). Honest scope: anima is human-competitive only "
                     f"vs a GREEDY reference, NOT vs a true multi-step optimum. north-star placement "
                     f"BOUNDED to weak references. TOY single rung.")
    else:
        verdict_line("H_1019", "INCONCLUSIVE",
                     f"anima mean {am:.4f} vs band [{band_lo:.3f},{band_hi:.3f}] within={within_band} "
                     f"overlap={ci_overlaps} below={below} above={above} -> boundary; report honestly.")


if __name__ == "__main__":
    main()
