"""H_1015 — human-bar PLACEMENT on a world-model-REQUIRING control task.

The DEFERRED placement step of CWM M8: H_972 authored the human-level bar INSTRUMENT
(on the saturating delayed-cue task) but explicitly deferred WHERE anima lands. Here we
do the placement on a task that genuinely REQUIRES the world model — the H_964
partial-observability station-keeping control env (agent sees POSITION only; the optimal
action needs the HIDDEN velocity, so a single-frame reactive policy provably fails).

FROZEN FALSIFIER (honored):
  metric M = mean episode return (0 = optimal, more negative = worse).
  human-proxy = the ORACLE optimal_action (knows velocity) with a ~7% per-step attention
    lapse (lapse -> random thrust) — the SAME lapse construction as H_972.
  human band = [human-proxy 25th, 75th pct]. above=human+, within=human-level, below=sub-human.
  D1 band validity: REACTIVE and RANDOM must land BELOW band_lo (CI_hi < band_lo) — else the
    task does not require a WM and the placement is vacuous.
  D2 discriminability: human-proxy must separate from RANDOM (p<0.05, |d|>=0.8).
  D3 anima placement: anima (WM, latent->action) return CI vs the human band.
  PASS/GREEN = band valid (D1) AND discriminating (D2) AND anima WITHIN-or-ABOVE band (D3).
  RED/closed-neg = band valid + discriminating BUT anima BELOW band (sub-human, a finding).
  FAIL/INCOMPLETE = band not valid (reactive inside band) OR human ~ random (vacuous).

Reuses the H_964 control env + WAM/reactive head training verbatim (imported), and the
H_972 boot-CI / band machinery. $0 CPU-local, deterministic given seeds, no GPU, no Φ.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, cohens_d, welch_t, boot_ci, header, verdict_line
from h964_latent_policy import (step_env, optimal_action, gen_demo, ODIM, NACT, T, N_TRAIN, THRUSTS)

N_RUNS = 40          # runs per agent (each run = a batch of episodes)
EP_PER_RUN = 60      # episodes per run
LAPSE = 0.07         # human attention-lapse rate (SAME as H_972 instrument)


def episode_return(policy_fn, rng):
    """Run one episode under a per-step policy_fn(obs_hist, pos) -> action; return mean reward."""
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


def make_human_proxy():
    """Oracle (knows velocity) with a ~7% attention lapse -> random thrust. The reference."""
    def fn(obs_hist, pos, v, rng):
        if rng.random() < LAPSE:
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
    header("H_1015", "human-bar PLACEMENT on a world-model-requiring control task (M8 deferred step)")
    print(f"task=H_964 hidden-velocity station-keeping (position-only obs)  metric M=mean return "
          f"(0=optimal)\nN_runs={N_RUNS} ep/run={EP_PER_RUN} lapse={LAPSE} (same human-proxy as H_972)\n")

    # --- train the WM (latent->action) and REACTIVE (obs->action) heads, exactly as H_964 ---
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

    human = run_agent(make_human_proxy(), 1000)
    rand = run_agent(make_random(), 2000)
    reac = run_agent(make_reactive(Whead_reac), 3000)
    anima = run_agent(make_wam(m, Whead_wam), 4000)

    band_lo, band_hi = np.percentile(human, [25, 75])
    print(f"human-reference band [25th,75th pct] = [{band_lo:.4f}, {band_hi:.4f}]")
    print(f"  human-proxy M = {human.mean():.4f} +/- {human.std():.4f}")
    print(f"  random      M = {rand.mean():.4f} +/- {rand.std():.4f}")
    print(f"  reactive    M = {reac.mean():.4f} +/- {reac.std():.4f}")
    print(f"  anima (WM)  M = {anima.mean():.4f} +/- {anima.std():.4f}")

    # D2 discriminability human vs random
    t, p = welch_t(human, rand)
    d = cohens_d(human, rand)
    print(f"\nD2 discriminability human-vs-random: Welch t={t:.3f} p={p:.3e} Cohen d={d:.3f}")
    discriminates = (p < 0.05) and (abs(d) >= 0.8)

    # D1 band validity: reactive + random CI below band_lo
    rlo, rhi = boot_ci(rand)
    clo, chi = boot_ci(reac)
    rand_below = rhi < band_lo
    reac_below = chi < band_lo
    print(f"D1 band validity: random CI_hi={rhi:.4f} < band_lo={band_lo:.4f} -> {rand_below}; "
          f"reactive CI_hi={chi:.4f} < band_lo -> {reac_below}")

    # D3 anima placement
    alo, ahi = boot_ci(anima)
    if alo > band_hi:
        place = "ABOVE band (human+)"
    elif ahi < band_lo:
        place = "BELOW band (sub-human)"
    else:
        place = "WITHIN band (human-level)"
    print(f"D3 anima placement: CI=[{alo:.4f},{ahi:.4f}] vs band [{band_lo:.4f},{band_hi:.4f}] -> {place}")

    band_valid = rand_below and reac_below
    within_or_above = (alo > band_hi) or (not (ahi < band_lo) and not (alo > band_hi))
    print()
    if band_valid and discriminates and within_or_above:
        verdict_line("H_1015", "PASS",
                     f"band valid (reactive+random below {band_lo:.3f}), human discriminates from "
                     f"random (p={p:.1e}, d={d:.2f}), anima CI [{alo:.3f},{ahi:.3f}] {place} -> the "
                     f"north star is a TRUE falsifiable placement on a WM-requiring task; anima is "
                     f"human-level-or-beyond HERE (toy, single rung; scale-transfer UNVERIFIED).")
    elif band_valid and discriminates and (ahi < band_lo):
        verdict_line("H_1015", "RED",
                     f"band valid + discriminating, BUT anima CI [{alo:.3f},{ahi:.3f}] BELOW band "
                     f"[{band_lo:.3f},{band_hi:.3f}] -> SUB-human on a WM-requiring control task "
                     f"(closed-negative, a_paper_negative_ok; the gap is the finding; toy).")
    else:
        verdict_line("H_1015", "INCOMPLETE",
                     f"band valid={band_valid} (reactive below={reac_below}), discriminates="
                     f"{discriminates} -> placement vacuous on this task (honest, toy C3); re-pick task.")


if __name__ == "__main__":
    main()
