#!/usr/bin/env python3
# lidar_ingest_ref.py — REAL public point-cloud → 128D tension fingerprint → 5-ch tension.
#
#   ROLE (a_core_engine_map · g61 engine ⊥ adapter)
#     This is the WORKING reference implementation of the path that
#     anima-tools/lidar_sense.hexa DESIGNS (the .hexa keeps the contract; the
#     device-capture path there stays stubbed/gated). Mirrors the way
#     conscious_decoder.py mirrors the hexa decode path, and the way
#     BRAIN/eeg/eeg_to_tpm.hexa is an ADAPTER (sensor → substrate state), NOT a
#     runtime engine. LiDAR here = a MEASUREMENT-ANCHOR (GOAL.md §97): an input
#     coupling, GOAL-orthogonal plumbing — NOT a command channel (one Boolean
#     flip `DRIVES_STATE ∧ ¬PHYSICS_SOURCED` from a §7-forbidden command path,
#     so it is deliberately read-only here: it produces a tension fingerprint,
#     it does not steer anima).
#
#   PIPELINE (real, deterministic)
#     point cloud (XYZ [+RGB], N×3) — a SET of points
#       → extract_3d_features: centroid, bounding-volume extents, range/depth
#         histogram (radial dist from centroid), surface-normal variance (PCA on
#         local k-NN), voxel-occupancy histogram
#       → encode_fingerprint: concat + pad/truncate to a fixed 128D vector
#       → fingerprint_to_tension: reduce the 128D to the 5-ch tension
#         [alpha, theta, gamma, 1-delta, beta] (mirrors the eeg_to_tpm adapter
#         SHAPE: sensor → a small fixed substrate vector), deterministic.
#
#   PERMUTATION INVARIANCE
#     A point cloud is a SET. Every feature here is a function of the multiset of
#     point coordinates (sums, histograms, eigenvalues of a covariance) → order
#     does NOT matter. Scrambling the GEOMETRY (perturbing coordinates) DOES
#     change the fingerprint. Both are measured in the validation harness.
#
#   SCOPE / HONESTY (a_toy_scale_recheck · a_scale_honest_scope)
#     CPU · $0 · public point-cloud DATA (Redwood indoor RGBD scan fragments via
#     Open3D, MIT) — NOT a live device scan. Toy-scale validation of the
#     fingerprint contract; transfer to a live iPhone/Record3D capture is
#     UNVERIFIED and gated (same posture as the EEG real-device capture).
# ============================================================================
import hashlib
import json
import os
import sys

import numpy as np

FP_DIM = 128
VOXEL_BINS = 4          # 4x4x4 = 64 occupancy bins
RANGE_BINS = 32         # radial depth histogram
KNN_K = 12              # neighbours for local surface-normal PCA
DET_SEED = 0            # fingerprint path itself is seed-free; seed only labels frames


# ---------------------------------------------------------------------------
# feature extraction — every quantity is a function of the multiset of points
# ---------------------------------------------------------------------------
def extract_3d_features(xyz: np.ndarray) -> dict:
    xyz = np.asarray(xyz, dtype=np.float64)
    n = xyz.shape[0]
    centroid = xyz.mean(axis=0)
    c = xyz - centroid

    # bounding-volume extents (order-invariant: min/max over the set)
    mn = xyz.min(axis=0)
    mx = xyz.max(axis=0)
    extents = mx - mn

    # radial depth histogram (distance from centroid) — order-invariant
    r = np.linalg.norm(c, axis=1)
    rmax = r.max() if r.max() > 0 else 1.0
    range_hist, _ = np.histogram(r, bins=RANGE_BINS, range=(0.0, rmax))
    range_hist = range_hist.astype(np.float64) / max(n, 1)

    # voxel-occupancy histogram over the normalized bounding box — order-invariant
    span = np.where(extents > 1e-9, extents, 1.0)
    norm = (xyz - mn) / span                       # [0,1]^3
    idx = np.clip((norm * VOXEL_BINS).astype(int), 0, VOXEL_BINS - 1)
    flat = idx[:, 0] * VOXEL_BINS * VOXEL_BINS + idx[:, 1] * VOXEL_BINS + idx[:, 2]
    occ = np.bincount(flat, minlength=VOXEL_BINS ** 3).astype(np.float64) / max(n, 1)

    # global covariance eigenvalues (shape anisotropy) — order-invariant
    cov = (c.T @ c) / max(n, 1)
    evals = np.sort(np.linalg.eigvalsh(cov))[::-1]   # descending
    evals = np.maximum(evals, 0.0)
    ev_sum = evals.sum() if evals.sum() > 0 else 1.0
    ev_norm = evals / ev_sum                          # planarity/linearity signature

    # surface-normal variance via local k-NN PCA (deterministic), order-invariant.
    # Subsample deterministically for cost (stride), but the per-normal computation
    # uses the WHOLE set for neighbour search → permutation-invariant.
    surf_var = _surface_normal_variance(xyz)

    return {
        "n": n,
        "centroid": centroid,
        "extents": extents,
        "range_hist": range_hist,
        "voxel_occ": occ,
        "ev_norm": ev_norm,
        "surf_var": float(surf_var),
        "rmax": float(rmax),
    }


def _set_order(xyz: np.ndarray) -> np.ndarray:
    """A canonical ordering of the points that is a function of the point SET
    only (lexicographic by coordinate), NOT of the input array order. This makes
    any value-stride subsample built on it permutation-invariant."""
    return np.lexsort((xyz[:, 2], xyz[:, 1], xyz[:, 0]))


def _surface_normal_variance(xyz: np.ndarray) -> float:
    """Mean variance of local surface-normal direction (cos to global mean normal).
    Deterministic AND permutation-invariant: every selection below is taken on a
    canonical SET-ordering (lexsort by coordinate), so the result depends only on
    the multiset of points, not on the input array order."""
    n = xyz.shape[0]
    order = _set_order(xyz)
    xyz_s = xyz[order]                      # canonical, order-independent
    # value-stride subsample of query points for cost (full canonical set for NN)
    stride = max(1, n // 1500)
    q_idx = np.arange(0, n, stride)
    # brute-force k-NN on a canonical anchor subsample to bound cost
    a_stride = max(1, n // 4000)
    anchors = xyz_s[np.arange(0, n, a_stride)]
    normals = []
    for qi in q_idx:
        p = xyz_s[qi]
        d = anchors - p
        dist2 = np.einsum("ij,ij->i", d, d)
        k = min(KNN_K, anchors.shape[0])
        nn = np.argpartition(dist2, k - 1)[:k]
        nb = anchors[nn]
        cc = nb - nb.mean(axis=0)
        cov = (cc.T @ cc) / k
        w, v = np.linalg.eigh(cov)
        normals.append(v[:, 0])     # smallest-eigenvalue direction = surface normal
    normals = np.array(normals)
    # orient consistently (sign-free) by squaring the cos to the mean direction
    m = normals.mean(axis=0)
    mn = m / (np.linalg.norm(m) + 1e-12)
    cosv = normals @ mn
    return float(np.var(cosv * cosv))


# ---------------------------------------------------------------------------
# encode → fixed 128D fingerprint
# ---------------------------------------------------------------------------
def encode_fingerprint(feat: dict, dim: int = FP_DIM) -> np.ndarray:
    parts = [
        feat["extents"] / (np.linalg.norm(feat["extents"]) + 1e-12),  # 3 (shape only)
        feat["range_hist"],                                            # 32
        feat["voxel_occ"],                                             # 64
        feat["ev_norm"],                                               # 3
        np.array([feat["surf_var"]]),                                  # 1
        # log-density features (scale-aware but order-invariant)
        np.array([np.log1p(feat["n"]) / 20.0]),                        # 1
    ]
    vec = np.concatenate([np.asarray(p, dtype=np.float64).ravel() for p in parts])
    if vec.shape[0] < dim:
        vec = np.concatenate([vec, np.zeros(dim - vec.shape[0])])
    else:
        vec = vec[:dim]
    return vec


def fingerprint_to_tension(fp: np.ndarray) -> np.ndarray:
    """Reduce 128D → 5-ch tension [alpha, theta, gamma, 1-delta, beta] in [0,1].
    Mirrors the eeg_to_tpm adapter SHAPE (sensor → small fixed substrate vector).
    Deterministic; bounded by a logistic squash so the tension-link stays in range."""
    seg = np.array_split(fp, 5)
    raw = np.array([s.mean() for s in seg])
    # logistic squash to (0,1) — bounded, finite
    t = 1.0 / (1.0 + np.exp(-4.0 * (raw - raw.mean())))
    return t


def ingest(xyz: np.ndarray):
    feat = extract_3d_features(xyz)
    fp = encode_fingerprint(feat)
    tension = fingerprint_to_tension(fp)
    return fp, tension, feat


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------
def load_xyz(path: str) -> np.ndarray:
    import open3d as o3d
    pc = o3d.io.read_point_cloud(path)
    return np.asarray(pc.points, dtype=np.float64)


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# validation harness
# ---------------------------------------------------------------------------
def run_validation(manifest_path: str):
    import open3d as o3d  # noqa
    with open(manifest_path) as f:
        manifest = json.load(f)

    frames = []          # (name, path, sha, license, xyz)
    for m in manifest:
        xyz = load_xyz(m["path"])
        frames.append((m["name"], m["path"], m["sha256"], xyz))

    results = {"dataset": manifest, "frames": [], "checks": {}}

    # encode every frame; record fingerprint + tension
    encs = []
    for name, path, sha, xyz in frames:
        fp, tension, feat = ingest(xyz)
        encs.append((name, fp, tension, feat))
        results["frames"].append({
            "name": name,
            "n_points": int(feat["n"]),
            "fp_l2": float(np.linalg.norm(fp)),
            "fp_finite": bool(np.all(np.isfinite(fp))),
            "tension": [float(x) for x in tension],
            "surf_var": float(feat["surf_var"]),
        })

    # ---- F-STABLE: finite/bounded, tension in range ----
    all_finite = all(np.all(np.isfinite(e[1])) for e in encs)
    tension_in_range = all(np.all((e[2] >= 0.0) & (e[2] <= 1.0)) for e in encs)
    results["checks"]["STABLE"] = {
        "all_fingerprints_finite": bool(all_finite),
        "tension_5ch_in_[0,1]": bool(tension_in_range),
        "verdict": "HOLDS" if (all_finite and tension_in_range) else "REFUTED",
    }

    # ---- F-DISCRIMINATIVE: cross-scene distance > within-scene (re-encode) noise ----
    # within-scene "noise": re-encode same frame → distance should be ~0 (deterministic).
    within = []
    for name, path, sha, xyz in frames:
        fp1, _, _ = ingest(xyz)
        fp2, _, _ = ingest(xyz)
        within.append(float(np.linalg.norm(fp1 - fp2)))
    # cross-scene pairwise distances
    cross = []
    for i in range(len(encs)):
        for j in range(i + 1, len(encs)):
            cross.append(float(np.linalg.norm(encs[i][1] - encs[j][1])))
    max_within = max(within) if within else 0.0
    min_cross = min(cross) if cross else 0.0
    mean_cross = float(np.mean(cross)) if cross else 0.0
    discriminative = (min_cross > max_within) and (max_within == 0.0 or min_cross > 10 * max_within)
    results["checks"]["DISCRIMINATIVE"] = {
        "max_within_scene_dist_reencode": max_within,
        "min_cross_scene_dist": min_cross,
        "mean_cross_scene_dist": mean_cross,
        "n_pairs": len(cross),
        "determinism_within_scene_zero": bool(max_within == 0.0),
        "verdict": "HOLDS" if discriminative else "REFUTED",
    }

    # ---- F-PERM-INVARIANT: shuffle ORDER must NOT change fp; scramble GEOMETRY must ----
    perm_deltas = []
    geom_deltas = []
    rng = np.random.default_rng(12345)
    for seed in range(3):  # 3 seeds
        rng_s = np.random.default_rng(1000 + seed)
        name, path, sha, xyz = frames[seed % len(frames)]
        fp_ref, _, _ = ingest(xyz)
        # (a) shuffle point ORDER (same set) → must be invariant
        perm = rng_s.permutation(xyz.shape[0])
        fp_perm, _, _ = ingest(xyz[perm])
        perm_deltas.append(float(np.linalg.norm(fp_ref - fp_perm)))
        # (b) scramble GEOMETRY (add structured jitter to coords) → must change
        jitter = rng_s.normal(0.0, 0.05 * (xyz.std() + 1e-9), size=xyz.shape)
        fp_geom, _, _ = ingest(xyz + jitter)
        geom_deltas.append(float(np.linalg.norm(fp_ref - fp_geom)))
    max_perm_delta = max(perm_deltas)
    min_geom_delta = min(geom_deltas)
    perm_invariant = (max_perm_delta < 1e-9)
    geom_sensitive = (min_geom_delta > 1e-6)
    results["checks"]["PERM_INVARIANT"] = {
        "max_order_shuffle_delta (want 0)": max_perm_delta,
        "min_geometry_scramble_delta (want >0)": min_geom_delta,
        "order_shuffle_deltas": perm_deltas,
        "geometry_scramble_deltas": geom_deltas,
        "permutation_invariant": bool(perm_invariant),
        "geometry_sensitive": bool(geom_sensitive),
        "verdict": "HOLDS" if (perm_invariant and geom_sensitive) else "REFUTED",
    }

    return results


if __name__ == "__main__":
    mp = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lidar_data/fetch_manifest.json"
    res = run_validation(mp)
    print(json.dumps(res, indent=2))
