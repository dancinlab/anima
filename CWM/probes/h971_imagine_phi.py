"""H_971 — Imagined rollout is a higher-Φ state than reactive perceive→act.

FROZEN FALSIFIER (honored):
  arm-IMAGINE = internal rollout (input withheld, internally driven, REM rehearsal);
  arm-REACT = reactive perceive→act on external input. Φ (proxy H_912/H_931) sampled
  in both; matched substrate config; N seeds; matched duration.
  D1 = Φ contrast = Φ_IMAGINE − Φ_REACT (Welch t, Cohen d).
  D2 = regime separability: does Φ alone classify imagine vs react above chance?
  D3 = shuffled-regime-label null bounds the contrast.
  PASS: Φ_IMAGINE > Φ_REACT, CI_lo>0, d>=0.5, p<0.05, beyond shuffled null.
  FAIL: Φ_IMAGINE <= Φ_REACT. INCOMPLETE: proxy unstable / n small.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import (LatentWorldModel, phi_proxy, cohens_d, welch_t, boot_ci,
                           header, verdict_line)

IN_DIM = 6
LATENT = 24
N_SEEDS = 30
ROLL = 40       # matched duration


def fit_engine(rng, seed):
    """Train the engine's latent transition operator on a toy dynamical stream so the
    imagined rollout is a self-driven trajectory (not noise)."""
    wm = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed, retentive=False,
                          spectral_radius=0.95)
    # toy smooth input stream (sinusoidal mixture) to train the transition operator
    T = 400
    t = np.arange(T)
    stream = np.stack([np.sin(0.2 * t + k) + 0.3 * rng.standard_normal(T)
                       for k in range(IN_DIM)], axis=1)
    H = wm.encode_seq(stream)
    wm.fit_transition(H[:-1], H[1:])
    return wm, stream


def run_seed(seed):
    rng = np.random.default_rng(seed)
    wm, stream = fit_engine(rng, seed)
    # REACT: encode an external input stream (reactive perceive)
    react_stream = np.stack([np.sin(0.2 * np.arange(ROLL) + k) +
                             0.3 * rng.standard_normal(ROLL) for k in range(IN_DIM)], axis=1)
    H_react = wm.encode_seq(react_stream)
    phi_react, _ = phi_proxy(H_react)
    # IMAGINE: internal rollout from the same start latent, NO external input
    h0 = H_react[0]
    H_img = wm.roll_latent(h0, ROLL)
    phi_img, _ = phi_proxy(H_img)
    return phi_img, phi_react


def main():
    header("H_971", "Imagined rollout is a higher-Φ state (REM/dream framing)")
    print(f"Φ proxy = integration×differentiation×entropy (H_912/H_931 family, NOT IIT4)")
    print(f"in_dim={IN_DIM} latent={LATENT} N_SEEDS={N_SEEDS} duration={ROLL}\n")
    img, react = [], []
    for s in range(N_SEEDS):
        a, b = run_seed(s)
        img.append(a); react.append(b)
    img, react = np.array(img), np.array(react)
    contrast = img.mean() - react.mean()
    d = cohens_d(img, react)
    t, p = welch_t(img, react)
    diff = img - react
    lo, hi = boot_ci(diff)
    # shuffled-regime null
    rng = np.random.default_rng(999)
    pooled = np.concatenate([img, react])
    null = []
    for _ in range(2000):
        perm = rng.permutation(pooled)
        null.append(perm[:len(img)].mean() - perm[len(img):].mean())
    null = np.array(null)
    null_hi = np.percentile(null, 97.5)

    print("D1 Φ contrast:")
    print(f"  Φ_IMAGINE = {img.mean():.4f} ± {img.std():.4f}")
    print(f"  Φ_REACT   = {react.mean():.4f} ± {react.std():.4f}")
    print(f"  contrast (IMG−REACT) = {contrast:.4f}  Cohen d = {d:.3f}  Welch t={t:.3f} p={p:.3e}")
    print(f"  paired-diff bootstrap 95% CI = [{lo:.4f}, {hi:.4f}]")
    print(f"D3 shuffled-regime null 97.5pct = {null_hi:.4f}  (contrast must exceed)")
    # D2 separability: Φ-threshold classification accuracy
    thr = pooled.mean()
    acc = (np.mean(img > thr) + np.mean(react <= thr)) / 2
    print(f"D2 regime separability (Φ-threshold classifier) acc = {acc:.3f} (chance 0.5)")

    if contrast > 0 and lo > 0 and d >= 0.5 and p < 0.05 and contrast > null_hi:
        verdict_line("H_971", "PASS",
                     f"Φ_IMAGINE>Φ_REACT contrast={contrast:.3f} d={d:.2f} p={p:.1e} "
                     f"CI_lo={lo:.3f}>0 beyond null — imagination is a higher-Φ state (toy).")
    elif contrast <= 0 or hi < 0:
        verdict_line("H_971", "FAIL",
                     f"Φ_IMAGINE<=Φ_REACT (contrast={contrast:.3f}) — imagination not more "
                     f"conscious by Φ here (closed-negative, toy).")
    else:
        verdict_line("H_971", "INCOMPLETE",
                     f"contrast={contrast:.3f} d={d:.2f} did not clear the frozen bar; toy-only C3.")


if __name__ == "__main__":
    main()
