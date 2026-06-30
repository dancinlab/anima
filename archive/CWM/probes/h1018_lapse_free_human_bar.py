"""H_1018 — lapse-free human bar (close the H_1015 ~7% attention-lapse caveat).

H_1015 placed anima's WM policy ABOVE the lapsing human band, but honestly flagged the
caveat: the human-proxy carried a ~7% per-step attention lapse while anima's deterministic
WM does not lapse, so "above-human" really meant "above-human-BECAUSE-no-lapse". Here we
re-run the SAME H_964 control placement with a LAPSE-FREE oracle (lapse=0.00) as the human
reference, to separate genuine WM parity from the lapse artifact. We also reproduce the
lapsing proxy (lapse=0.07) so the lapse contribution is explicit.

FROZEN FALSIFIER (honored, identical env/policies/seeds to H_1015 except the human lapse):
  metric M = mean episode return (0 = optimal, more negative = worse).
  no-lapse oracle O = ORACLE optimal_action (knows velocity), lapse=0.00 — the human reference.
  lapsing proxy = same oracle with lapse=0.07 (reproduces H_1015).
  TOL = 0.05 (return units). parity band = [O - TOL, O + TOL].
  PASS (genuine parity) = anima mean within [O-TOL, O+TOL] AND anima CI overlaps the band.
  RED (closed-neg)      = anima mean < O - TOL AND anima CI_hi < O - TOL (sub-oracle; lapse artifact).
  GREEN-PLUS            = anima mean > O + TOL AND anima CI_lo > O + TOL (above the pure oracle).
  lapse contribution    = O_mean - lapsing_mean (the return the ~7% lapse costs the human).

Reuses the H_964 control env + WAM/reactive head training verbatim (imported), and the
H_972/H_1015 boot-CI machinery. $0 CPU-local, deterministic given seeds, no GPU, no Phi.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, cohens_d, welch_t, boot_ci, header, verdict_line
from h964_latent_policy import (step_env, optimal_action, gen_demo, ODIM, NACT, T, N_TRAIN, THRUSTS)

N_RUNS = 40          # runs per agent (each run = a batch of episodes)  -- same as H_1015
EP_PER_RUN = 60      # episodes per run                                  -- same as H_1015
LAPSE = 0.07         # lapsing-proxy attention-lapse rate (H_1015 reproduction)
NO_LAPSE = 0.00      # the pure oracle (this hypothesis's human reference)
TOL = 0.05           # pre-registered parity tolerance band half-width (frozen 2026-06-07)


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


def make_oracle(lapse):
    """Oracle (knows velocity); with prob `lapse` plays a random thrust instead of optimal."""
    def fn(obs_hist, pos, v, rng):
        if lapse > 0.0 and rng.random() < lapse:
            return rng.integers(NACT)
        return optimal_action(pos, v)
    return fn


def make_random():
    def fn(obs_hist, pos, v, rng):
        return rng.integers(NACT)
    return fn


def make_reactive(Whead):
    def fn(obs_hist, pos, v, rng):
        feat = _aug(pos[None, :])
        return int((feat @ Whead).argmax())
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
    header("H_1018", "lapse-free human bar (close the H_1015 ~7% attention-lapse caveat)")
    print(f"task=H_964 hidden-velocity station-keeping (position-only obs)  metric M=mean return "
          f"(0=optimal)\nN_runs={N_RUNS} ep/run={EP_PER_RUN}  human-ref=NO-LAPSE oracle (lapse={NO_LAPSE})"
          f"  +reproduce lapsing proxy (lapse={LAPSE})  TOL={TOL}\n")

    # --- train WM (latent->action) + REACTIVE (obs->action) heads, exactly as H_964/H_1015 ---
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

    # same seeds as H_1015
    oracle = run_agent(make_oracle(NO_LAPSE), 1000)   # NO-LAPSE oracle = the human reference here
    lapsing = run_agent(make_oracle(LAPSE), 1000)     # lapsing proxy = H_1015 reproduction
    rand = run_agent(make_random(), 2000)
    reac = run_agent(make_reactive(Whead_reac), 3000)
    anima = run_agent(make_wam(m, Whead_wam), 4000)

    O = oracle.mean()
    band_lo, band_hi = O - TOL, O + TOL
    olo, ohi = boot_ci(oracle)
    llo, lhi = boot_ci(lapsing)
    rlo, rhi = boot_ci(rand)
    clo, chi = boot_ci(reac)
    alo, ahi = boot_ci(anima)

    print("---- decomposition (mean +/- std, bootstrap CI) ----")
    print(f"  no-lapse ORACLE (human ref) M = {O:.4f} +/- {oracle.std():.4f}  CI=[{olo:.4f},{ohi:.4f}]")
    print(f"  lapsing proxy (H_1015 repr) M = {lapsing.mean():.4f} +/- {lapsing.std():.4f}  CI=[{llo:.4f},{lhi:.4f}]")
    print(f"  anima (WM latent->action)   M = {anima.mean():.4f} +/- {anima.std():.4f}  CI=[{alo:.4f},{ahi:.4f}]")
    print(f"  reactive (single-frame)     M = {reac.mean():.4f} +/- {reac.std():.4f}  CI=[{clo:.4f},{chi:.4f}]")
    print(f"  random                      M = {rand.mean():.4f} +/- {rand.std():.4f}  CI=[{rlo:.4f},{rhi:.4f}]")

    lapse_cost = O - lapsing.mean()
    print(f"\nlapse contribution = no-lapse-oracle - lapsing-proxy = {O:.4f} - {lapsing.mean():.4f} "
          f"= {lapse_cost:.4f} (return the ~{int(LAPSE*100)}% lapse costs the human)")

    print(f"\nparity band [O - TOL, O + TOL] = [{band_lo:.4f}, {band_hi:.4f}]  (O={O:.4f}, TOL={TOL})")
    am = anima.mean()
    within_band = (band_lo <= am <= band_hi)
    ci_overlaps = (alo <= band_hi) and (ahi >= band_lo)
    below = (am < band_lo) and (ahi < band_lo)
    above = (am > band_hi) and (alo > band_hi)
    gap = O - am
    print(f"anima mean {am:.4f} vs band -> within_band={within_band} ci_overlaps={ci_overlaps} "
          f"below={below} above={above}")
    print(f"oracle-anima gap = {gap:+.4f}")

    print()
    if within_band and ci_overlaps:
        verdict_line("H_1018", "PASS",
                     f"GENUINE PARITY — anima mean {am:.4f} within parity band [{band_lo:.3f},{band_hi:.3f}] "
                     f"around the NO-LAPSE oracle O={O:.4f} (anima CI [{alo:.3f},{ahi:.3f}] overlaps band); the WM "
                     f"has recovered the hidden velocity to oracle quality -> clean 'human-level (not beyond)'. "
                     f"The H_1015 'above-human' is explained as exactly the lapse cost {lapse_cost:.4f} the "
                     f"real no-lapse oracle does not pay. TOY single rung; scale-transfer UNVERIFIED.")
    elif below:
        verdict_line("H_1018", "RED",
                     f"CLOSED-NEGATIVE (a_paper_negative_ok) — anima mean {am:.4f} BELOW the no-lapse oracle "
                     f"O={O:.4f} (gap {gap:+.4f}; anima CI_hi {ahi:.3f} < band_lo {band_lo:.3f}); the H_1015 "
                     f"'above-human' was ENTIRELY the ~{int(LAPSE*100)}% lapse artifact (lapse cost {lapse_cost:.4f}); "
                     f"anima is human-competitive only vs a LAPSING human, NOT vs a pure oracle. TOY single rung.")
    elif above:
        verdict_line("H_1018", "GREEN-PLUS",
                     f"ABOVE-ORACLE — anima mean {am:.4f} EXCEEDS even the no-lapse oracle O={O:.4f} "
                     f"(anima CI_lo {alo:.3f} > band_hi {band_hi:.3f}); the imitation-trained WM head out-returns "
                     f"the hand-coded optimal_action in this toy env (env/oracle-suboptimality finding, scoped "
                     f"tightly — NOT a general human-superiority claim). TOY single rung; scale-transfer UNVERIFIED.")
    else:
        verdict_line("H_1018", "INCONCLUSIVE",
                     f"anima mean {am:.4f} vs band [{band_lo:.3f},{band_hi:.3f}] within={within_band} "
                     f"overlap={ci_overlaps} below={below} above={above} -> boundary case; report honestly.")


if __name__ == "__main__":
    main()
