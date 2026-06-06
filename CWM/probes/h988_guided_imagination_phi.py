"""H_988 — RE-FORMULATION re-test of H_971 🔴 (imagination does NOT raise Φ).

ORIGINAL 🔴 (H_971): arm-IMAGINE = AUTONOMOUS unconditional latent rollout (input withheld,
self-driven); arm-REACT = reactive perceive on external input. Φ_IMAGINE 0.068 < Φ_REACT
0.095 (d=-3.4) → "imagination is a LOWER-Φ state". Interpretation: an autonomous rollout
SETTLES toward the transition operator's dominant mode (a low-dimensional attractor) → less
bound, lower Φ than continuously externally-driven activity.

WHY THE ORIGINAL MAY BE A FORMULATION ARTIFACT:
  H_971's "imagination" was AUTONOMOUS DRIFT — a free-running rollout with NO goal, NO
  external constraint. Decaying toward an attractor is exactly what an undriven linear-ish
  operator does, so low Φ there says more about free-running drift than about imagination
  as a cognitive act. Human imagination is largely GOAL-DIRECTED: a target/constraint
  steers the rollout, injecting structured variation that keeps the trajectory off the
  attractor. The fair test is GUIDED imagination (rollout pulled toward a goal latent at
  each step) vs reactive — does goal-directed imagination raise Φ? We ALSO swap to an
  alternative Φ-proxy axis-weighting to check the original was not proxy-artifactual.

FROZEN FALSIFIER (this re-formulation — frozen 2026-06-06):
  Same engine/training as H_971. THREE regimes, matched duration:
    arm-GUIDED  = imagined rollout with a goal latent pulling the trajectory each step
                  (goal-directed imagination) — the re-formulated IMAGINE arm.
    arm-DRIFT   = the H_971 autonomous unconditional rollout (the original IMAGINE arm).
    arm-REACT   = reactive perceive on external input (the H_971 baseline).
  D1 = Φ contrast GUIDED − REACT (Welch t, Cohen d, bootstrap CI) — the flip test.
  D2 = GUIDED vs DRIFT: does guidance raise Φ over free drift (isolating the goal effect)?
  D3 = alternative Φ-proxy (differentiation-weighted variant) — the GUIDED>REACT sign must
       survive a proxy change (guards against proxy-artifact), AND a shuffled-regime null.
  PASS = "🟢 FLIPS": Φ_GUIDED > Φ_REACT (CI_lo>0, d>=0.5, p<0.05, beyond null) AND the sign
         survives the alt-proxy — goal-directed imagination IS a higher-Φ state; H_971's null
         was specific to the autonomous-drift formulation.
  FAIL = "🔴 ROBUST": even guided imagination <= reactive — imagination-raises-Φ is false
         across formulations (closed-negative robust).

g5 CODE-measured (no LLM self-judge, p7). substrate=CPU-mirror (numpy). Φ is a PROXY
(H_912/H_931 family, NOT IIT4). Toy single-rung, ladder OPEN (a_scale_honest_scope).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import (LatentWorldModel, phi_proxy, cohens_d, welch_t, boot_ci,
                           header, verdict_line)

IN_DIM = 6
LATENT = 24
N_SEEDS = 30
ROLL = 40
GOAL_PULL = 0.25     # strength of the goal constraint steering the guided rollout


def fit_engine(rng, seed):
    wm = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed, retentive=False,
                          spectral_radius=0.95)
    T = 400; t = np.arange(T)
    stream = np.stack([np.sin(0.2 * t + k) + 0.3 * rng.standard_normal(T)
                       for k in range(IN_DIM)], axis=1)
    H = wm.encode_seq(stream)
    wm.fit_transition(H[:-1], H[1:])
    return wm, H


def guided_rollout(wm, h0, goal, steps, pull):
    """Goal-directed imagined rollout: apply the learned transition, then PULL toward a goal
    latent each step (the cognitive 'aim' that keeps imagination structured / off-attractor)."""
    out = []
    h = h0.copy()
    for _ in range(steps):
        h = wm.roll_latent(h, 1)[0]
        h = h + pull * (goal - h)        # steer toward the goal latent
        out.append(h.copy())
    return np.array(out)


def phi_alt(H):
    """Alternative Φ-proxy: same integration×entropy structure but differentiation enters
    LINEARLY (not divided by d) and is given DOUBLE weight — a different axis-weighting so a
    real Φ-elevation effect survives a proxy change (guards against proxy-artifact)."""
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    _, base = phi_proxy(H)
    integ, diff, ent = base["integration"], base["differentiation"], base["entropy"]
    return integ * (diff ** 0.5) * (0.5 + 0.5 * ent) * (1.0 + diff)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    wm, Htrain = fit_engine(rng, seed)
    react_stream = np.stack([np.sin(0.2 * np.arange(ROLL) + k) +
                             0.3 * rng.standard_normal(ROLL) for k in range(IN_DIM)], axis=1)
    H_react = wm.encode_seq(react_stream)
    h0 = H_react[0]
    # goal latent = a real reachable engine state (a later training latent), not noise
    goal = Htrain[rng.integers(len(Htrain) // 2, len(Htrain))]
    H_guided = guided_rollout(wm, h0, goal, ROLL, GOAL_PULL)
    H_drift = wm.roll_latent(h0, ROLL)
    return (phi_proxy(H_guided)[0], phi_proxy(H_react)[0], phi_proxy(H_drift)[0],
            phi_alt(H_guided), phi_alt(H_react))


def main():
    header("H_988", "GUIDED (goal-directed) imagination raises Φ — re-test of H_971 🔴")
    print("re-formulation: H_971 used AUTONOMOUS drift; here imagination is GOAL-DIRECTED")
    print("Φ proxy = integration×differentiation×entropy (H_912/H_931 family, NOT IIT4)")
    print(f"in_dim={IN_DIM} latent={LATENT} N_SEEDS={N_SEEDS} duration={ROLL} goal_pull={GOAL_PULL}\n")
    g, r, dft, ga, ra = [], [], [], [], []
    for s in range(N_SEEDS):
        a, b, c, d, e = run_seed(s)
        g.append(a); r.append(b); dft.append(c); ga.append(d); ra.append(e)
    g, r, dft, ga, ra = map(np.array, (g, r, dft, ga, ra))

    contrast = g.mean() - r.mean()
    d = cohens_d(g, r); t, p = welch_t(g, r)
    lo, hi = boot_ci(g - r)
    rng = np.random.default_rng(999)
    pooled = np.concatenate([g, r])
    null = np.array([(perm := rng.permutation(pooled))[:len(g)].mean() - perm[len(g):].mean()
                     for _ in range(2000)])
    null_hi = float(np.percentile(null, 97.5))
    print("D1 Φ contrast (GUIDED vs REACT):")
    print(f"  Φ_GUIDED = {g.mean():.4f} ± {g.std():.4f}")
    print(f"  Φ_REACT  = {r.mean():.4f} ± {r.std():.4f}")
    print(f"  contrast (GUIDED−REACT) = {contrast:.4f}  Cohen d = {d:.3f}  Welch t={t:.3f} p={p:.3e}")
    print(f"  paired-diff bootstrap 95% CI = [{lo:.4f}, {hi:.4f}]  shuffled-null 97.5pct = {null_hi:.4f}")

    contrast_drift = g.mean() - dft.mean()
    dd = cohens_d(g, dft); td, pd = welch_t(g, dft)
    print(f"D2 GUIDED vs DRIFT (isolate the goal effect): Φ_DRIFT={dft.mean():.4f} "
          f"contrast(GUIDED−DRIFT)={contrast_drift:.4f} d={dd:.3f} p={pd:.3e}")

    contrast_alt = ga.mean() - ra.mean()
    da = cohens_d(ga, ra); ta, pa = welch_t(ga, ra)
    alt_sign_survives = (np.sign(contrast_alt) == np.sign(contrast)) and contrast > 0 and pa < 0.05
    print(f"D3 alt-Φ-proxy (differentiation-weighted): Φalt_GUIDED={ga.mean():.4f} "
          f"Φalt_REACT={ra.mean():.4f} contrast={contrast_alt:.4f} d={da:.3f} p={pa:.3e} "
          f"-> GUIDED>REACT sign survives proxy change: {alt_sign_survives}")

    flips = (contrast > 0 and lo > 0 and d >= 0.5 and p < 0.05 and contrast > null_hi
             and alt_sign_survives)
    if flips:
        verdict_line("H_988", "PASS",
                     f"🟢 FLIPS — goal-directed imagination Φ_GUIDED {g.mean():.3f} > Φ_REACT "
                     f"{r.mean():.3f} (contrast {contrast:.3f}, d={d:.2f}, p={p:.1e}, CI_lo {lo:.3f}>0, "
                     f"beyond null, alt-proxy agrees) — H_971's null was specific to AUTONOMOUS DRIFT; "
                     f"guided imagination IS higher-Φ (toy, ladder OPEN). xref H_971.")
    else:
        why = []
        if contrast <= 0: why.append(f"Φ_GUIDED {g.mean():.3f} <= Φ_REACT {r.mean():.3f}")
        elif lo <= 0 or p >= 0.05 or contrast <= null_hi: why.append("contrast not significant beyond null")
        if not alt_sign_survives: why.append("sign did NOT survive alt-proxy")
        verdict_line("H_988", "FAIL",
                     f"🔴 ROBUST — even goal-directed imagination does not raise Φ over reactive "
                     f"[{'; '.join(why)}] — imagination-raises-Φ is false across formulations; the "
                     f"H_971 closed-negative is FORMULATION-ROBUST (toy). xref H_971.")


if __name__ == "__main__":
    main()
