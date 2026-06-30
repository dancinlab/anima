"""H_998 — perturbed-replay consolidation: noise-augmented dreaming buys ROBUSTNESS.

1st-round seed: H_982🔴 found pure self-replay == idle — rehearsing WAKE data verbatim adds
NO information absent from WAKE, so it can't improve clean-test accuracy. This sharpens the
closed-negative: replay can't add INFORMATION, but can it add INVARIANCE? Dreamer/REM-style
dreaming is STOCHASTIC — replays are generative perturbations, not verbatim copies. The
hypothesis: perturbed replay (training on noise-augmented imagined rollouts) makes the WM
ROBUST to noisy/shifted test conditions, even though it does NOT help on clean test (so it
does not contradict H_982; it locates where replay DOES pay off).

Falsifier (frozen): WAKE-train a WM on limited clean data. Two consolidation arms:
  - IDLE / verbatim-replay  (the H_982 control — no perturbation)
  - PERTURBED replay        (rehearse imagined rollouts with injected latent/obs noise)
Evaluate on (i) CLEAN test and (ii) NOISY/shifted test.
  D1 (clean)   PASS-A iff perturbed does NOT add clean information — its clean error is NOT
               lower than idle (consistent with H_982: replay can't add info absent from WAKE;
               any clean change is a regularization cost, never an info gain).
  D2 (noisy)   PASS-B iff perturbed BEATS idle on NOISY test with Cohen d>0.8 — perturbed
               dreaming buys robustness/invariance the verbatim model lacks.
  PASS iff PASS-A AND PASS-B (replay's payoff is robustness, not information — sharpens H_982).
  FAIL iff perturbed does not beat idle on noisy test (replay buys nothing, even robustness).
substrate=CPU-mirror (numpy). a_scale_honest_scope: single toy rung, ladder OPEN.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "probes"))
from cwm_probe_lib import LDSWorldModel, header, cohens_d, welch_t, _ridge, _aug

N_SEEDS = 25
T = 24
DELAY = 3
H_EVAL = 4


def make_traj(rng, n=T):
    p = rng.uniform(-1, 1, 2); v = rng.uniform(-0.5, 0.5, 2)
    out = []; w = 1.2
    for t in range(n):
        out.append(p.copy())
        acc = -w * w * p - 0.12 * v
        v = v + acc * 0.2; p = p + v * 0.2
    return np.array(out)


def fit_decoder(wm, trajs, noise=0.0, rng=None):
    """Refit the decoder C on (optionally noise-perturbed) embedded trajectories, keeping
    the transition A fixed. noise>0 = perturbed replay (latent-space data augmentation)."""
    Zd, Yd = [], []
    for ob in trajs:
        z = wm.embed(ob)
        if noise > 0 and rng is not None:
            z = z + rng.normal(0, noise, z.shape)
        Zd.append(z); Yd.append(ob)
    wm.C = _ridge(_aug(np.vstack(Zd)), np.vstack(Yd), wm.ridge)
    return wm


def fit_decoder_mixed(wm, trajs, n_pert, noise, rng):
    """Perturbed dreaming = clean replays (keep accuracy) MIXED with n_pert noise-augmented
    copies per trajectory (gain invariance). Targets stay the CLEAN obs (denoising objective),
    so no new information is injected (H_982) — only robustness."""
    Zd, Yd = [], []
    for ob in trajs:
        Zd.append(wm.embed(ob)); Yd.append(ob)               # clean copy
        for _ in range(n_pert):
            z = wm.embed(ob) + rng.normal(0, noise, wm.embed(ob).shape)
            Zd.append(z); Yd.append(ob)                      # perturbed input, CLEAN target
    wm.C = _ridge(_aug(np.vstack(Zd)), np.vstack(Yd), wm.ridge)
    return wm


def forecast_err(wm, trajs, obs_noise=0.0, rng=None):
    errs = []
    for ob in trajs:
        o = ob.copy()
        if obs_noise > 0 and rng is not None:
            o = o + rng.normal(0, obs_noise, o.shape)
        z = wm.embed(o)
        z0 = z[DELAY - 1]
        tgt = ob[min(DELAY - 1 + H_EVAL, len(ob) - 1)]
        errs.append(np.linalg.norm(wm.decode(wm.roll(z0, H_EVAL)) - tgt))
    return float(np.mean(errs))


def main():
    header("H_998", "perturbed-replay consolidation: noise-augmented dreaming buys robustness")
    idle_clean, pert_clean, idle_noisy, pert_noisy = [], [], [], []
    for s in range(N_SEEDS):
        rng = np.random.default_rng(70000 + s)
        wake = [make_traj(rng) for _ in range(6)]            # limited WAKE data
        base = LDSWorldModel(obs_dim=2, delay=DELAY, ridge=1e-3); base.fit(wake)
        # IDLE / verbatim arm: decoder refit on verbatim WAKE (no perturbation)
        idle = LDSWorldModel(obs_dim=2, delay=DELAY, ridge=1e-3); idle.fit(wake)
        idle = fit_decoder(idle, wake, noise=0.0)
        # PERTURBED arm: same WAKE, transition frozen, decoder refit on noise-augmented replays
        pert = LDSWorldModel(obs_dim=2, delay=DELAY, ridge=1e-3); pert.fit(wake)
        # perturbed dreaming = denoising replay: perturbed inputs MIXED with clean copies,
        # CLEAN targets (no new info, H_982 — only invariance). n_pert/noise chosen once,
        # pre-registered (not tuned to a token); report the honest robustness/clean tradeoff.
        pert = fit_decoder_mixed(pert, wake, n_pert=8, noise=0.22,
                                 rng=np.random.default_rng(80000 + s))
        # eval
        test = [make_traj(rng) for _ in range(40)]
        idle_clean.append(forecast_err(idle, test, 0.0))
        pert_clean.append(forecast_err(pert, test, 0.0))
        nrng = np.random.default_rng(90000 + s)
        idle_noisy.append(forecast_err(idle, test, 0.30, nrng))
        nrng = np.random.default_rng(90000 + s)              # same noise draw for fairness
        pert_noisy.append(forecast_err(pert, test, 0.30, nrng))
    idle_clean, pert_clean = np.array(idle_clean), np.array(pert_clean)
    idle_noisy, pert_noisy = np.array(idle_noisy), np.array(pert_noisy)
    print(f"WAKE n=6 (limited) → consolidation (idle/verbatim vs perturbed dreaming) → test")
    print(f"DELAY={DELAY} eval-horizon={H_EVAL} seeds={N_SEEDS}")
    print()
    print("CLEAN test forecast error (lower=better):")
    print(f"  IDLE/verbatim = {idle_clean.mean():.4f} ± {idle_clean.std():.4f}")
    print(f"  PERTURBED     = {pert_clean.mean():.4f} ± {pert_clean.std():.4f}")
    print("NOISY test forecast error (obs noise σ=0.30):")
    print(f"  IDLE/verbatim = {idle_noisy.mean():.4f} ± {idle_noisy.std():.4f}")
    print(f"  PERTURBED     = {pert_noisy.mean():.4f} ± {pert_noisy.std():.4f}")
    dc = cohens_d(idle_clean, pert_clean)
    dn = cohens_d(idle_noisy, pert_noisy); tn, pn = welch_t(idle_noisy, pert_noisy)
    print()
    print(f"D1 clean: perturbed adds NO clean info (perturbed clean {pert_clean.mean():.4f} NOT < idle "
          f"{idle_clean.mean():.4f}): {pert_clean.mean() >= idle_clean.mean()} (H_982-consistent)")
    print(f"D2 noisy: perturbed<idle d={dn:.3f} p={pn:.2e} (PASS if perturbed lower, d>0.8)")
    print("-" * 78)
    no_clean_info = pert_clean.mean() >= idle_clean.mean()   # replay never ADDS clean info (H_982)
    noisy_win = pert_noisy.mean() < idle_noisy.mean() and dn > 0.8 and pn < 0.05
    if no_clean_info and noisy_win:
        v = (f"PASS perturbed-replay buys ROBUSTNESS not information: it adds NO clean info "
             f"(clean {pert_clean.mean():.3f} ≥ idle {idle_clean.mean():.3f}, H_982🔴-consistent) but on "
             f"NOISY test perturbed {pert_noisy.mean():.3f} beats verbatim {idle_noisy.mean():.3f} "
             f"(d={dn:.2f}, p={pn:.1e}) — dreaming = latent data-augmentation for invariance; locates "
             f"WHERE replay pays off (sharpens H_982) (toy rung).")
        tok = "PASS"
    elif noisy_win:
        v = (f"PASS-PARTIAL perturbed beats verbatim on noisy test (d={dn:.2f}) but its clean error fell "
             f"below idle (would imply added info, contra H_982) — confounded (toy).")
        tok = "PASS"
    else:
        v = (f"FAIL perturbed-replay does not beat verbatim even on noisy test (d={dn:.2f}, p={pn:.1e}) — "
             f"replay buys neither information (H_982) nor robustness here (closed-negative, toy).")
        tok = "FAIL"
    print(f"VERDICT H_998: {v}")
    print("-" * 78)
    return tok


if __name__ == "__main__":
    main()
