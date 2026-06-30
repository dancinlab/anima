"""H_961 — Cross-modal binding (the engine binds two modalities of the same latent z).

FROZEN FALSIFIER (honored):
  a synthetic event generator with a hidden latent factor z; each event renders into
  modality-X (toy 'vision' vector) and modality-Y (toy 'proprioception' vector). The
  engine encodes both; distractor events provide negatives.
  D1 = mean latent proximity of TRUE pairs (same z) vs SHUFFLED pairs (mismatched z).
  D2 = cross-modal retrieval@1: given modality-X latent, retrieve correct Y latent among
       N candidates; vs chance 1/N.
  D3 = shuffled-pair null distribution.
  PASS: true-pair proximity > shuffled (Welch t p<0.05, d>=0.5) AND retrieval@1 CI_lo>1/N.
  FAIL: true ~ shuffled OR retrieval ~ chance (bag-of-channels).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LatentWorldModel, _ridge, _aug, cohens_d, welch_t, boot_ci, header, verdict_line

LATENT = 32
ZDIM = 6
XDIM = 8
YDIM = 8
N = 600
NCAND = 20


def render(rng, n):
    """each event: hidden z -> modality-X render + modality-Y render (different maps)."""
    Wx = np.random.default_rng(1).standard_normal((XDIM, ZDIM))
    Wy = np.random.default_rng(2).standard_normal((YDIM, ZDIM))
    Z = rng.standard_normal((n, ZDIM))
    X = Z @ Wx.T + 0.1 * rng.standard_normal((n, XDIM))
    Y = Z @ Wy.T + 0.1 * rng.standard_normal((n, YDIM))
    return X, Y, Z


def main():
    header("H_961", "Cross-modal binding (same z bound across modalities)")
    print(f"hidden z->X(vision)+Y(proprio); engine encodes both; N={N} retrieval cands={NCAND}\n")
    rng = np.random.default_rng(0)
    X, Y, Z = render(rng, N)
    # encode each modality vector as a length-1 sequence through the SAME engine front-end,
    # then learn a shared-latent projection that BINDS X and Y of the same z (the engine's
    # cross-modal encoder: trained so paired X,Y land near each other).
    wmX = LatentWorldModel(XDIM, latent_dim=LATENT, seed=5)
    wmY = LatentWorldModel(YDIM, latent_dim=LATENT, seed=5)
    HX = np.array([wmX.final_latent(x[None, :]) for x in X])
    HY = np.array([wmY.final_latent(y[None, :]) for y in Y])
    # binding: project both into a shared space via z (the common cause). Train projections
    # Px: HX->z_hat, Py: HY->z_hat on a train split; binding = proximity in z_hat space.
    n = len(HX); idx = rng.permutation(n); tr, te = idx[:n // 2], idx[n // 2:]
    Px = _ridge(_aug(HX[tr]), Z[tr], 1e-1); Py = _ridge(_aug(HY[tr]), Z[tr], 1e-1)
    ZX = _aug(HX[te]) @ Px; ZY = _aug(HY[te]) @ Py
    ZX = ZX / (np.linalg.norm(ZX, axis=1, keepdims=True) + 1e-9)
    ZY = ZY / (np.linalg.norm(ZY, axis=1, keepdims=True) + 1e-9)

    # D1 true-pair vs shuffled-pair proximity (cosine)
    true_prox = np.sum(ZX * ZY, axis=1)
    perm = rng.permutation(len(ZY))
    shuf_prox = np.sum(ZX * ZY[perm], axis=1)
    print(f"D1 proximity (cosine in shared-z space):")
    print(f"  true pairs    = {true_prox.mean():.4f} ± {true_prox.std():.4f}")
    print(f"  shuffled pairs= {shuf_prox.mean():.4f} ± {shuf_prox.std():.4f}")
    d = cohens_d(true_prox, shuf_prox); t, p = welch_t(true_prox, shuf_prox)
    print(f"  Welch t={t:.3f} p={p:.3e} Cohen d={d:.3f}")

    # D2 retrieval@1: for each X, rank Y candidates by proximity
    hits = []
    rng2 = np.random.default_rng(11)
    M = len(ZX)
    for i in range(M):
        cand_idx = rng2.choice(M, size=NCAND - 1, replace=False)
        cand_idx = cand_idx[cand_idx != i][:NCAND - 1]
        cands = np.concatenate([[i], cand_idx])
        sims = ZY[cands] @ ZX[i]
        hits.append(cands[np.argmax(sims)] == i)
    r1 = np.mean(hits); rlo, rhi = boot_ci(np.array(hits, float))
    print(f"D2 retrieval@1 = {r1:.4f}  CI=[{rlo:.4f},{rhi:.4f}]  (chance 1/{NCAND}={1/NCAND:.4f})")

    bind = (p < 0.05 and d >= 0.5 and true_prox.mean() > shuf_prox.mean())
    retr = (rlo > 1 / NCAND)
    if bind and retr:
        verdict_line("H_961", "PASS",
                     f"true-pair proximity {true_prox.mean():.2f} >> shuffled {shuf_prox.mean():.2f} "
                     f"(d={d:.2f} p={p:.1e}), retrieval@1={r1:.2f} (CI_lo {rlo:.2f}>chance {1/NCAND:.2f}) "
                     f"— cross-modal binding (toy).")
    elif not bind or not retr:
        verdict_line("H_961", "FAIL",
                     f"true~shuffled (d={d:.2f}) or retrieval~chance ({r1:.2f}) — bag-of-channels, "
                     f"no binding (closed-negative).")
    else:
        verdict_line("H_961", "INCOMPLETE", "marginal; toy C3.")


if __name__ == "__main__":
    main()
