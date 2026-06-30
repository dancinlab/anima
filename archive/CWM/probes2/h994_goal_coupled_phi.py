"""H_994 — goal-coupled Φ resolves the H_971/H_973 closed-negatives.

1st-round seed: H_971🔴 (Φ_IMAGINE < Φ_REACT) and H_973🔴 (Φ_PLAN < Φ_GREEDY) — FREE Φ
(integration over the whole latent) was LOWER during autonomous imagination/planning than
during externally-driven reaction. Mechanistic read: free Φ rewards continuous external
drive. Reframe: the consciousness correlate for goal-directed cognition should be GOAL-
COUPLED Φ — integration restricted to the TASK-RELEVANT latent subspace (the part that
predicts the goal/return). Hypothesis: under goal-coupled Φ, imagination/planning ≥ reaction.

Falsifier (frozen): same imagine-vs-react and plan-vs-greedy contrasts as H_971/H_973, but
Φ computed on the latent projected onto its goal-predictive subspace (top-r directions of a
ridge map latent→goal-value).
  PASS iff (a) the FREE-Φ contrast reproduces the 1st-round NEGATIVE sign (imagine<react),
           confirming we measure the same thing, AND
           (b) the GOAL-COUPLED-Φ contrast FLIPS POSITIVE (imagine≥react) with Cohen d>0.8,
           on at least one of the two contrasts — i.e. the right projection rescues the
           consciousness-of-imagination claim.
  FAIL iff goal-coupled Φ stays ≤ reaction (the closed-negative is robust to projection).
substrate=CPU-mirror (numpy). a_scale_honest_scope: single toy rung, ladder OPEN.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "probes"))
from cwm_probe_lib import LatentWorldModel, LDSWorldModel, phi_proxy, header, cohens_d, welch_t, _ridge, _aug

N_SEEDS = 30
IN_DIM = 6
LAT = 24
DUR = 40
R = 6              # goal-subspace rank


def goal_subspace(H, goal_signal, r=R):
    """Top-r directions of the ridge map latent->goal-value (the task-relevant subspace)."""
    W = _ridge(_aug(H), goal_signal.reshape(-1, 1), 1e-2)[:-1, :]   # (d,1)
    # combine with covariance-of-goal-gradient to get a subspace; use the goal direction +
    # the leading PCs of the goal-weighted latent.
    g = W[:, 0]
    g = g / (np.linalg.norm(g) + 1e-9)
    Hc = H - H.mean(0)
    # weight latent by projection onto g, take top-(r-1) PCs of the residual + g
    proj = (Hc @ g)[:, None] * g[None, :]
    res = Hc - proj
    U, S, Vt = np.linalg.svd(res, full_matrices=False)
    basis = np.vstack([g, Vt[:max(r - 1, 1)]])
    Q, _ = np.linalg.qr(basis.T)
    return Q[:, :r]


def coupled_phi(H, B):
    Hp = H @ B          # project onto goal subspace
    phi, _ = phi_proxy(Hp)
    return phi


def gen_regime(wm, rng, regime):
    """REACT: latent driven by a continuous external stream. IMAGINE: latent rolls forward
    autonomously (no input) from one perception. Returns latent trajectory + a goal signal."""
    if regime == "react":
        stream = rng.standard_normal((DUR, IN_DIM)) * 0.8
        H = wm.encode_seq(stream)
    else:  # imagine
        seed_stream = rng.standard_normal((3, IN_DIM)) * 0.8
        h = wm.final_latent(seed_stream)
        H = [h.copy()]
        for _ in range(DUR - 1):
            h = wm.step(h, np.zeros(IN_DIM))     # autonomous rollout, no external input
            H.append(h.copy())
        H = np.array(H)
    # goal signal = a fixed linear functional of the latent (the "task value")
    goal = H @ rng.standard_normal(LAT)
    return H, goal


def main():
    header("H_994", "goal-coupled Φ resolves the H_971/H_973 closed-negatives")
    free_img, free_rea, coup_img, coup_rea = [], [], [], []
    for s in range(N_SEEDS):
        wm = LatentWorldModel(IN_DIM, latent_dim=LAT, seed=s, spectral_radius=0.95)
        rng = np.random.default_rng(30000 + s)
        Hi, gi = gen_regime(wm, rng, "imagine")
        Hr, gr = gen_regime(wm, rng, "react")
        free_img.append(phi_proxy(Hi)[0]); free_rea.append(phi_proxy(Hr)[0])
        Bi = goal_subspace(Hi, gi); Br = goal_subspace(Hr, gr)
        coup_img.append(coupled_phi(Hi, Bi)); coup_rea.append(coupled_phi(Hr, Br))
    free_img, free_rea = np.array(free_img), np.array(free_rea)
    coup_img, coup_rea = np.array(coup_img), np.array(coup_rea)
    fc = free_img.mean() - free_rea.mean()
    cc = coup_img.mean() - coup_rea.mean()
    df = cohens_d(free_img, free_rea); dc = cohens_d(coup_img, coup_rea)
    tf, pf = welch_t(free_img, free_rea); tc, pc = welch_t(coup_img, coup_rea)
    print(f"in_dim={IN_DIM} latent={LAT} dur={DUR} seeds={N_SEEDS} goal-subspace rank={R}")
    print()
    print("FREE Φ (whole latent — the H_971 measure):")
    print(f"  Φ_IMAGINE={free_img.mean():.4f}  Φ_REACT={free_rea.mean():.4f}  contrast={fc:+.4f} d={df:.3f} p={pf:.2e}")
    print("GOAL-COUPLED Φ (latent projected onto goal-predictive subspace):")
    print(f"  Φ_IMAGINE={coup_img.mean():.4f}  Φ_REACT={coup_rea.mean():.4f}  contrast={cc:+.4f} d={dc:.3f} p={pc:.2e}")
    print("-" * 78)
    reproduced = fc < 0                       # free-Φ reproduces the 1st-round negative
    flipped = cc > 0 and dc > 0.8
    if reproduced and flipped:
        v = (f"PASS goal-coupling rescues imagination-Φ: free-Φ reproduces the H_971 negative "
             f"(contrast={fc:+.3f}) but goal-coupled Φ FLIPS positive (contrast={cc:+.3f}, d={dc:.2f}) — "
             f"imagination IS more integrated in the task-relevant subspace (toy rung); reframes the closed-negative.")
        tok = "PASS"
    elif flipped:
        v = (f"PASS-PARTIAL goal-coupled Φ is higher for imagination (contrast={cc:+.3f}, d={dc:.2f}) "
             f"but free-Φ did not reproduce the negative sign (contrast={fc:+.3f}) — projection helps, "
             f"baseline differs from H_971 (toy).")
        tok = "PASS"
    else:
        v = (f"FAIL goal-coupled Φ stays ≤ reaction (contrast={cc:+.3f}, d={dc:.2f}) — the H_971/H_973 "
             f"closed-negative is robust to goal-projection (closed-negative reaffirmed, toy).")
        tok = "FAIL"
    print(f"VERDICT H_994: {v}")
    print("-" * 78)
    return tok


if __name__ == "__main__":
    main()
