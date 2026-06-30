"""H_972 — Human-level-or-beyond bar: operationalize a FALSIFIABLE human-reference bar.

FROZEN FALSIFIER (honored):
  fix a task with a measurable outcome M. Obtain a human-reference distribution (a
  documented human-proxy). human-level band = [ref 25th, 75th pct]; human+ = above band.
  D1 = metric discriminability: does M separate human-reference from random/degenerate?
  D2 = anima placement vs the band (below/within/above), with CI.
  D3 = random + degenerate agents must score below the band (band validity).
  PASS = the metric discriminates human-ref from random (D1 significant) AND anima can be
         CI-placed against the band (regardless of WHERE anima lands).
  Note: PASS = "a falsifiable bar exists and works", NOT "anima is human-level".

This H authors the INSTRUMENT. Task = the delayed-cue WM task (H_970). The human-proxy =
a documented near-optimal policy (a human who remembers the cue: ~0.95 success with
human-like lapse noise). random = 1/K. degenerate = always-same-action.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import (LatentWorldModel, welch_t, cohens_d, boot_ci, header, verdict_line)
sys.path.insert(0, os.path.dirname(__file__))
from h970_wm_vs_lm import make_episode, onehot, K, L, LATENT

N_RUNS = 40         # runs per agent (each run = a batch of episodes)
EP_PER_RUN = 100


def human_proxy_run(rng, lapse=0.07):
    """A documented human-proxy: remembers the cue, acts correctly, with a human lapse
    rate (attention slips). This is the reference distribution (NOT anima)."""
    succ = 0
    for _ in range(EP_PER_RUN):
        _, c = make_episode(rng)
        if rng.random() < lapse:
            ans = rng.integers(K)        # attention lapse -> random
        else:
            ans = c                      # remembers
        succ += (ans == c)
    return succ / EP_PER_RUN


def random_run(rng):
    succ = 0
    for _ in range(EP_PER_RUN):
        _, c = make_episode(rng)
        succ += (rng.integers(K) == c)
    return succ / EP_PER_RUN


def degenerate_run(rng):
    succ = 0
    for _ in range(EP_PER_RUN):
        _, c = make_episode(rng)
        succ += (0 == c)                 # always action 0
    return succ / EP_PER_RUN


def anima_run(rng, wm):
    succ = 0
    for _ in range(EP_PER_RUN):
        seq, c = make_episode(rng)
        h = wm.final_latent(seq)
        ans = int(wm.predict_readout(h[None, :]).argmax())
        succ += (ans == c)
    return succ / EP_PER_RUN


def main():
    header("H_972", "Human-level-or-beyond bar — operationalize a falsifiable instrument")
    print(f"task=delayed-cue WM (H_970)  metric M=success rate  N_runs={N_RUNS} ep/run={EP_PER_RUN}\n")
    # train anima (WM) once
    trng = np.random.default_rng(7)
    wm = LatentWorldModel(K + 2, latent_dim=LATENT, seed=7, retentive=True, spectral_radius=1.0)
    train = [make_episode(trng) for _ in range(800)]
    H = np.array([wm.final_latent(s) for s, _ in train])
    Y = np.array([onehot(c, K) for _, c in train])
    wm.fit_readout(H, Y)

    human = np.array([human_proxy_run(np.random.default_rng(1000 + i)) for i in range(N_RUNS)])
    rand = np.array([random_run(np.random.default_rng(2000 + i)) for i in range(N_RUNS)])
    degen = np.array([degenerate_run(np.random.default_rng(3000 + i)) for i in range(N_RUNS)])
    anima = np.array([anima_run(np.random.default_rng(4000 + i), wm) for i in range(N_RUNS)])

    band_lo, band_hi = np.percentile(human, [25, 75])
    print(f"human-reference band [25th,75th pct] = [{band_lo:.4f}, {band_hi:.4f}]")
    print(f"  human-proxy M = {human.mean():.4f} ± {human.std():.4f}")
    print(f"  random      M = {rand.mean():.4f} ± {rand.std():.4f}")
    print(f"  degenerate  M = {degen.mean():.4f} ± {degen.std():.4f}")
    print(f"  anima (WM)  M = {anima.mean():.4f} ± {anima.std():.4f}")

    # D1 discriminability: human vs random
    t, p = welch_t(human, rand)
    d = cohens_d(human, rand)
    print(f"\nD1 discriminability human-vs-random: Welch t={t:.3f} p={p:.3e} Cohen d={d:.3f}")
    discriminates = (p < 0.05) and (d >= 0.8)

    # D3 band validity: random + degenerate below band_lo
    rlo, rhi = boot_ci(rand)
    dlo, dhi = boot_ci(degen)
    rand_below = rhi < band_lo
    degen_below = dhi < band_lo
    print(f"D3 band validity: random CI_hi={rhi:.4f} < band_lo={band_lo:.4f} -> {rand_below}; "
          f"degenerate CI_hi={dhi:.4f} < band_lo -> {degen_below}")

    # D2 anima placement
    alo, ahi = boot_ci(anima)
    if alo > band_hi:
        place = "ABOVE band (human+)"
    elif ahi < band_lo:
        place = "BELOW band"
    else:
        place = "WITHIN band (human-level)"
    print(f"D2 anima placement: CI=[{alo:.4f},{ahi:.4f}] vs band -> {place}")

    if discriminates and rand_below and degen_below:
        verdict_line("H_972", "PASS",
                     f"metric discriminates human-ref from random (p={p:.1e}, d={d:.2f}), "
                     f"band valid (random+degenerate below), anima CI-placed {place} — a "
                     f"falsifiable human-level bar EXISTS + works (instrument authored, toy).")
    else:
        verdict_line("H_972", "FAIL",
                     f"metric does not cleanly discriminate human from random / band invalid "
                     f"-> north star not yet measurable here (honest, toy C3).")


if __name__ == "__main__":
    main()
