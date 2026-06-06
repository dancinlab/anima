"""H_986 — RE-FORMULATION re-test of H_978 🔴 (lattice geometry is modality-specific).

ORIGINAL 🔴 (H_978): raw latent-distribution geometry descriptors (pairwise-distance KS,
NN-spacing KS, top-k spectral-ratio L2) of a language manifold vs a sensor manifold fall
FAR outside the within-language self-similarity band → "lattice geometry is modality-
SPECIFIC" (closed-negative).

WHY THE ORIGINAL MAY BE A FORMULATION ARTIFACT:
  H_978 compared the RAW latent clouds in a SHARED, FIXED coordinate frame. Two manifolds
  can carry the SAME intrinsic geometric structure yet sit in different sub-spaces / at
  different scales of that frame — raw-coordinate descriptors (absolute pairwise distances,
  absolute spectral magnitudes) would then differ even when the *shape* is invariant. The
  fair question for "is the geometry invariant" is whether there exists an alignment (a
  rigid Procrustes rotation, or a representation-similarity index like linear CKA that is
  ITSELF invariant to rotation+isotropic-scaling) under which the two manifolds match.

FROZEN FALSIFIER (this re-formulation — frozen 2026-06-06):
  Same SAME-engine language (A) and sensor (B) latents as H_978, but measured under a
  FAIRER alignment:
  D1 = linear CKA(A,B) — a rotation/scale-invariant representational-similarity index —
       compared to the A-vs-A self-similarity band AND to a label-shuffled / cross-paired
       null (the floor for "unrelated manifolds").
  D2 = orthogonal-Procrustes residual: best rigid rotation R aligning B's structure to A
       (on a paired support built from a SHARED latent factor), normalized residual vs the
       A-vs-A Procrustes band.
  D3 = control — a TRULY unrelated manifold (independent random engine on B) must NOT pass,
       so the test can FAIL (guards against a vacuous "everything aligns" instrument).
  PASS = "🟢 FLIPS": under fair alignment the cross-modal geometry IS within the A-vs-A
         band AND clears the unrelated-null (CKA in band & Procrustes residual in band &
         control rejected) — the original 🔴 was a raw-coordinate formulation artifact.
  FAIL = "🔴 ROBUST": even under the fairest alignment the cross-modal geometry stays
         outside the band — modality-specificity is robust across formulations.

g5 CODE-measured (no LLM self-judge, p7). substrate=CPU-mirror (numpy). Toy single-rung,
ladder OPEN (a_scale_honest_scope). Read-only probe; does NOT modify engine/pure_field.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from scipy import stats
from cwm_probe_lib import LatentWorldModel, cka, header, verdict_line

LATENT = 32
IN_DIM = 8
N = 400
N_FACTORS = 8   # shared latent factor (topic / frequency band) = the paired support


def lang_stream(rng, n):
    """Same generator family as H_978; factor index returned so A/B share a latent cause."""
    X, fac = [], []
    for _ in range(n):
        topic = rng.integers(N_FACTORS)
        seq = np.zeros((10, IN_DIM))
        for t in range(10):
            seq[t, (topic + rng.integers(2)) % IN_DIM] = 1.0
            seq[t] += 0.1 * rng.standard_normal(IN_DIM)
        X.append(seq); fac.append(topic)
    return X, np.array(fac)


def sensor_stream(rng, n, factors):
    """Same generator family as H_978; the frequency band is DRIVEN by the same factor as
    language so A and B encode a COMMON latent cause (fair paired support for Procrustes)."""
    X = []
    for k_, f in enumerate(factors):
        freq = 0.1 + 0.08 * f
        t = np.arange(10)
        X.append(np.stack([np.sin(freq * t + k) + 0.1 * rng.standard_normal(10)
                           for k in range(IN_DIM)], 1))
    return X


def factor_centroids(H, fac, n_fac):
    """Per-shared-factor centroid of the latent manifold — the paired support for
    orthogonal Procrustes (factor f in A corresponds to factor f in B)."""
    return np.array([H[fac == f].mean(0) for f in range(n_fac)])


def procrustes_resid(P, Q):
    """Normalized residual of the best ORTHOGONAL (rigid rotation) map P->Q after centering
    + isotropic scale (the geometry-only alignment). 0 = identical shape, 1 = no alignment."""
    P = P - P.mean(0); Q = Q - Q.mean(0)
    nP = np.linalg.norm(P); nQ = np.linalg.norm(Q)
    if nP < 1e-9 or nQ < 1e-9:
        return 1.0
    P = P / nP; Q = Q / nQ
    U, s, Vt = np.linalg.svd(Q.T @ P)
    R = U @ Vt
    return float(np.linalg.norm(P @ R.T - Q) ** 2)  # in [0, ~2]; 0 = perfect shape match


def main():
    header("H_986", "geometry invariance under FAIR alignment (CKA/Procrustes) — re-test of H_978 🔴")
    print("re-formulation: H_978 compared RAW coords; here we allow rotation/scale alignment")
    print("A=language, B=sensor (SAME engine, SHARED latent factor); CKA + orthogonal-Procrustes\n")
    rng = np.random.default_rng(0)
    cfg = dict(in_dim=IN_DIM, latent_dim=LATENT, seed=42, spectral_radius=0.9)
    wm = LatentWorldModel(**cfg)                       # SAME engine for both modalities

    LA, facA = lang_stream(rng, N)
    HA = np.array([wm.final_latent(s) for s in LA])
    HB = np.array([wm.final_latent(s) for s in sensor_stream(rng, N, facA)])
    LA2, facA2 = lang_stream(rng, N)                   # 2nd language draw -> A-vs-A band
    HA2 = np.array([wm.final_latent(s) for s in LA2])

    # ---- D1: linear CKA (rotation/scale-invariant) cross-modal vs A-vs-A band vs null ----
    # paired support: match by shared factor so rows correspond (fair representational sim)
    CA = factor_centroids(HA, facA, N_FACTORS)
    CB = factor_centroids(HB, facA, N_FACTORS)
    CA2 = factor_centroids(HA2, facA2, N_FACTORS)
    cka_AB = cka(CA, CB)
    # A-vs-A band: split-half CKA within language (the self-similarity ceiling/floor)
    rng2 = np.random.default_rng(3)
    band = []
    for _ in range(200):
        idx = rng2.permutation(N)
        h1 = factor_centroids(HA[idx[:N // 2]], facA[idx[:N // 2]], N_FACTORS)
        h2 = factor_centroids(HA2[idx[N // 2:]], facA2[idx[N // 2:]], N_FACTORS)
        band.append(cka(h1, h2))
    band = np.array(band)
    band_lo = float(np.percentile(band, 5))           # within-language self-sim 5th pct
    # null: shuffle the factor correspondence (destroy the shared cause) -> unrelated floor
    null = []
    for _ in range(200):
        perm = rng2.permutation(N_FACTORS)
        null.append(cka(CA, CB[perm]))
    null = np.array(null)
    null_hi = float(np.percentile(null, 95))          # unrelated-manifold ceiling
    d1_ok = (cka_AB >= band_lo) and (cka_AB > null_hi)
    print("D1 linear CKA (rotation/scale-invariant):")
    print(f"  CKA(A,B)={cka_AB:.4f}  A-vs-A band 5pct={band_lo:.4f}  shuffled-null 95pct={null_hi:.4f}"
          f"  -> in band & > null: {d1_ok}")

    # ---- D2: orthogonal-Procrustes residual vs A-vs-A Procrustes band ----
    pr_AB = procrustes_resid(CA, CB)
    pr_band = []
    for _ in range(200):
        idx = rng2.permutation(N)
        h1 = factor_centroids(HA[idx[:N // 2]], facA[idx[:N // 2]], N_FACTORS)
        h2 = factor_centroids(HA2[idx[N // 2:]], facA2[idx[N // 2:]], N_FACTORS)
        pr_band.append(procrustes_resid(h1, h2))
    pr_band = np.array(pr_band)
    pr_band_hi = float(np.percentile(pr_band, 95))
    d2_ok = pr_AB <= pr_band_hi
    print(f"D2 orthogonal-Procrustes residual(A,B)={pr_AB:.4f}  A-vs-A band 95pct={pr_band_hi:.4f}"
          f"  -> within band: {d2_ok}")

    # ---- D3: control — a truly UNRELATED engine on B must be REJECTED (instrument has teeth) ----
    wm_other = LatentWorldModel(in_dim=IN_DIM, latent_dim=LATENT, seed=777, spectral_radius=0.9)
    HB_unrel = np.array([wm_other.final_latent(s) for s in sensor_stream(rng, N, facA)])
    CB_unrel = factor_centroids(HB_unrel, facA, N_FACTORS)
    cka_unrel = cka(CA, CB_unrel)
    pr_unrel = procrustes_resid(CA, CB_unrel)
    control_rejected = not ((cka_unrel >= band_lo) and (cka_unrel > null_hi) and (pr_unrel <= pr_band_hi))
    print(f"D3 control (UNRELATED engine on B): CKA={cka_unrel:.4f} Procrustes={pr_unrel:.4f}"
          f"  -> correctly rejected: {control_rejected}")

    flips = d1_ok and d2_ok and control_rejected
    if flips:
        verdict_line("H_986", "PASS",
                     f"🟢 FLIPS — under fair alignment cross-modal geometry IS within the A-vs-A band "
                     f"(CKA {cka_AB:.3f}>=band {band_lo:.3f} & >null {null_hi:.3f}; Procrustes "
                     f"{pr_AB:.3f}<=band {pr_band_hi:.3f}) with the unrelated control rejected — "
                     f"H_978 🔴 was a RAW-COORDINATE formulation artifact; the lattice IS modality-"
                     f"invariant up to rotation/scale (toy, ladder OPEN). xref H_978.")
    else:
        why = []
        if not d1_ok: why.append(f"CKA {cka_AB:.3f} below band {band_lo:.3f} or under null {null_hi:.3f}")
        if not d2_ok: why.append(f"Procrustes {pr_AB:.3f} > band {pr_band_hi:.3f}")
        if not control_rejected: why.append("control NOT rejected (instrument vacuous)")
        verdict_line("H_986", "FAIL",
                     f"🔴 ROBUST — even under the fairest alignment (CKA + orthogonal Procrustes) "
                     f"modality-specificity holds [{'; '.join(why)}] — H_978 closed-negative is "
                     f"FORMULATION-ROBUST (toy). xref H_978.")


if __name__ == "__main__":
    main()
