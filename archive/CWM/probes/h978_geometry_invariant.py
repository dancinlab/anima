"""H_978 — Ψ-lattice geometry invariant across modalities.

FROZEN FALSIFIER (honored):
  read latents from the SAME engine layer for (A) language stream and (B) >=1 non-language
  toy stream (H_960 generator). Compute geometry descriptors on each.
  D1 = pairwise-distance distribution SHAPE match (KS distance A-vs-B vs A-vs-A bootstrap band).
  D2 = repulsion-spacing statistic (min-distance / nearest-neighbour distribution) match.
  D3 = leading spectral structure (top-k eigenvalue ratios of latent covariance) match in band.
  PASS: D1,D2,D3 all within the A-vs-A self-similarity band (KS not significantly worse than
        the within-language bootstrap).
  FAIL: any of D1/D2/D3 outside the band (non-language geometry qualitatively different).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from scipy import stats
from cwm_probe_lib import LatentWorldModel, header, verdict_line

LATENT = 32
IN_DIM = 8
N = 400


def lang_stream(rng, n):
    X = []
    for _ in range(n):
        topic = rng.integers(8)
        seq = np.zeros((10, IN_DIM))
        for t in range(10):
            seq[t, (topic + rng.integers(2)) % IN_DIM] = 1.0
            seq[t] += 0.1 * rng.standard_normal(IN_DIM)
        X.append(seq)
    return X


def sensor_stream(rng, n):
    X = []
    for _ in range(n):
        f = 0.1 + 0.08 * rng.integers(8)
        t = np.arange(10)
        X.append(np.stack([np.sin(f * t + k) + 0.1 * rng.standard_normal(10) for k in range(IN_DIM)], 1))
    return X


def pdist_sample(H, rng, m=4000):
    n = len(H)
    i = rng.integers(0, n, m); j = rng.integers(0, n, m)
    keep = i != j
    return np.linalg.norm(H[i[keep]] - H[j[keep]], axis=1)


def nn_dist(H):
    from scipy.spatial import cKDTree
    tree = cKDTree(H)
    d, _ = tree.query(H, k=2)
    return d[:, 1]


def spectral_ratios(H, k=5):
    C = np.cov(H.T); ev = np.sort(np.clip(np.linalg.eigvalsh(C), 0, None))[::-1]
    return ev[:k] / (ev[0] + 1e-12)


def main():
    header("H_978", "Ψ-lattice geometry invariant across modalities")
    print(f"latents from SAME engine layer; A=language, B=sensor; geometry descriptors\n")
    rng = np.random.default_rng(0)
    cfg = dict(in_dim=IN_DIM, latent_dim=LATENT, seed=42, spectral_radius=0.9)
    wm = LatentWorldModel(**cfg)            # SAME engine for both streams
    HA = np.array([wm.final_latent(s) for s in lang_stream(rng, N)])
    HB = np.array([wm.final_latent(s) for s in sensor_stream(rng, N)])
    HA2 = np.array([wm.final_latent(s) for s in lang_stream(rng, N)])  # 2nd lang draw -> A-vs-A band

    rng2 = np.random.default_rng(3)
    # D1 pairwise-distance shape: KS(A,B) vs A-vs-A bootstrap band
    dA = pdist_sample(HA, rng2); dA2 = pdist_sample(HA2, rng2); dB = pdist_sample(HB, rng2)
    ks_AB = stats.ks_2samp(dA, dB).statistic
    band = [stats.ks_2samp(pdist_sample(HA[rng2.permutation(len(HA))[:N//2]], rng2),
                           pdist_sample(HA2[rng2.permutation(len(HA2))[:N//2]], rng2)).statistic
            for _ in range(40)]
    band_hi = np.percentile(band, 95)
    print(f"D1 pairwise-distance KS(A,B)={ks_AB:.4f}  A-vs-A band 95pct={band_hi:.4f}  "
          f"-> within band: {ks_AB <= band_hi}")

    # D2 nearest-neighbour spacing (repulsion 1/r^2 signature) KS, A-vs-A bootstrap band
    nnA, nnB = nn_dist(HA), nn_dist(HB)
    ks_nn_AB = stats.ks_2samp(nnA, nnB).statistic
    nn_band = []
    for _ in range(40):
        p = rng2.permutation(len(HA))
        h1, h2 = HA[p[:len(HA)//2]], HA2[p[:len(HA2)//2]]
        nn_band.append(stats.ks_2samp(nn_dist(h1), nn_dist(h2)).statistic)
    band_nn_hi = np.percentile(nn_band, 95)
    print(f"D2 NN-spacing KS(A,B)={ks_nn_AB:.4f}  A-vs-A band 95pct={band_nn_hi:.4f} "
          f"-> within band: {ks_nn_AB <= band_nn_hi}")

    # D3 spectral structure: top-5 eigenvalue ratios, L2 distance vs A-vs-A bootstrap band
    sA, sB = spectral_ratios(HA), spectral_ratios(HB)
    spec_AB = np.linalg.norm(sA - sB)
    spec_band = []
    for _ in range(40):
        p = rng2.permutation(len(HA))
        s1 = spectral_ratios(HA[p[:len(HA)//2]]); s2 = spectral_ratios(HA2[p[:len(HA2)//2]])
        spec_band.append(np.linalg.norm(s1 - s2))
    band_spec_hi = np.percentile(spec_band, 95)
    print(f"D3 spectral-ratio L2(A,B)={spec_AB:.4f}  A-vs-A band 95pct={band_spec_hi:.4f} "
          f"-> within band: {spec_AB <= band_spec_hi}")

    d1_ok = ks_AB <= band_hi
    d2_ok = ks_nn_AB <= band_nn_hi
    d3_ok = spec_AB <= band_spec_hi
    if d1_ok and d2_ok and d3_ok:
        verdict_line("H_978", "PASS",
                     f"all 3 geometry descriptors within the A-vs-A self-similarity band "
                     f"(KS_pdist {ks_AB:.3f}, KS_nn {ks_nn_AB:.3f}, spec {spec_AB:.3f}) — "
                     f"lattice geometry invariant across modalities (toy).")
    else:
        fails = [n for n, ok in [("D1-pdist", d1_ok), ("D2-NN", d2_ok), ("D3-spectral", d3_ok)] if not ok]
        verdict_line("H_978", "FAIL",
                     f"geometry differs outside band on {fails} — lattice is modality-specific "
                     f"(closed-negative).")


if __name__ == "__main__":
    main()
