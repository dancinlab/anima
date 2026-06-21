#!/usr/bin/env python3
"""H_1517 COST-vs-Φ PARETO FRONT — R1 numpy/scipy mirror (DIRECTIONAL, a_engine_native_learning).

THE QUESTION (the deep version of the user's "is the brain mysteriously optimal?"):
  Two prior MERGED lanes found the TRUE anatomical placement is Φ-SUBOPTIMAL for UNCONSTRAINED
  integration: H_1515 (#2493 engine-native — node-permutation search finds ~2.5× higher-Φ
  placements) and H_1516 (#2494 REAL AAL90 connectome — true named-anatomical placement at only
  ~37th percentile, ~65% below the Φ-optimum). The honest interpretation (Bullmore & Sporns 2012
  "The economy of brain network organization"; Achard & Bullmore 2007): the brain optimizes
  COST-CONSTRAINED integration, not pure Φ — it pays for short/cheap wiring.

  H_1517 makes that LOAD-BEARING — compute BOTH axes per placement:
    integration Φ  = IIT4 min-cut Φ (phi_core over the CORE lanes — EXACTLY H_1512/1515/1516), AND
    wiring COST    = Σ over PRESENT edges of euclidean distance ||centroid_i − centroid_j||₂ (MNI mm)
                     between the AAL region centroids of the two lanes an edge connects.
  Then: does the TRUE anatomical placement lie ON (or near ε of) the Φ-vs-cost PARETO FRONT?
    YES → the brain IS near-optimal for the COST-CONSTRAINED objective (deep YES to the user).
    NO  → even cost-constrained, the placement is dominated (another honest result, c9).

REAL DATA (REAL, openly-licensed, citable — NO synthetic relabel):
  (1) CONNECTOME — Škoch et al. 2022, "Human brain structural connectivity matrices–ready for
      modelling," Scientific Data 9:486, DOI 10.1038/s41597-022-01596-9, OSF 10.17605/OSF.IO/YW5VF,
      CC-BY-4.0. AAL90 atlas, 88 healthy adults, 90×90 normalized streamline density, GROUP AVERAGE.
      (SCmatrices88healthy.mat, gitignored 4.3 MB; re-fetch https://osf.io/download/6823g/, $0.)
  (2) CENTROIDS — AAL atlas (Tzourio-Mazoyer et al. 2002, NeuroImage 15(1):273-289), ROI_MNI_V4.nii
      (MNI 2mm, 91×109×91, sform affine). Each AAL90 region's MNI centroid = mean MNI coordinate of
      all voxels labeled with that ROI. Computed reproducibly from the atlas NIfTI (see
      make_centroids below) → state/1517_cost_pareto/AAL90_centroids_MNI.csv (committed).
      Cross-checked: Precentral_L=(-38.9,-7.0,49.6), Hippocampus_L=(-25.3,-22.0,-11.4),
      Thalamus_L=(-11.2,-18.8,6.6) — all anatomically correct, left=−x / right=+x.

HARNESS REUSE (a_toy_scale_recheck — same Φ bars/metric, only the cost axis is new):
  Re-uses H_1512's h1512.py BYTE-FOR-BYTE (build_population engine-uniform, apply_topology
  X'=X·(I+α·Â)ᵀ, phi_core = IIT4 min-cut Φ over the CORE, ALPHA=0.6, N=15) and H_1516's
  lane→AAL-region NAMED mapping. The placement-search permutes lane→node over the SAME 15 named
  AAL nodes (so BOTH cost & Φ are measured on the identical region set — isolates the ASSIGNMENT).

FROZEN BARS — see state/verdicts/1517_cost_pareto/H_1517_FREEZE.txt (pre-registered, c9, NEVER moved).
"""
import os, sys, json
import numpy as np
import scipy.io as sio

HERE = os.path.dirname(os.path.abspath(__file__))
SIB = os.path.join(HERE, "..", "1512_brain_topology")
sys.path.insert(0, os.path.abspath(SIB))
import h1512 as H  # the sibling harness — single source of Φ / population / topology

MAT      = os.path.join(HERE, "SCmatrices88healthy.mat")
NIFTI    = os.path.join(HERE, "ROI_MNI_V4.nii")
LABELS   = os.path.join(HERE, "AAL_regions.csv")
CENTROID = os.path.join(HERE, "AAL90_centroids_MNI.csv")

# ── FROZEN thresholds (pre-registered, c9 — verbatim from H_1517_FREEZE.txt) ──────────────
P1a_DOM_FRAC_MAX = 0.05      # ≤5% of candidates strictly dominate the true placement
P1b_DIST_MAX     = 0.05      # normalized distance-to-front ≤ 0.05
P2_COST_PCTL_MAX = 1.0/3.0   # true cost in the BOTTOM tercile of the candidate cost distribution
M_RANDOM           = 3000
HILLCLIMB_RESTARTS = 12
SEEDS = [5170, 5171, 5172]

# ── 15 lanes → TRUE NAMED AAL90 region (1-indexed ROI#) — IDENTICAL to H_1516's NAMED map ──
NAMED = [
    (0,  "GlobalWorkspace",   "L Precuneus",            67),
    (1,  "Habituation",       "L Postcentral Gyrus",    57),
    (2,  "PrecisionSurprise", "L Cingulum Ant",         31),
    (3,  "SelfIdentity",      "L Superior Medial Gyrus",23),
    (4,  "LearnedPrecision",  "L Middle Frontal Gyrus",  7),
    (5,  "Novelty",           "R Hippocampus",          38),
    (6,  "AttentionalBlink",  "R Inferior Parietal Lobule",62),
    (7,  "SenseOfAgency",     "R Angular Gyrus (TPJ)",  66),
    (8,  "SubjectiveTime",    "R Insula Lobe",          30),
    (9,  "EmotionRegulation", "R Mid Orbital Gyrus",    26),
    (10, "DirectedForgetting","R Middle Frontal Gyrus",  8),
    (11, "BodyOwnership",     "L SupraMarginal Gyrus",  63),
    (12, "DividedAttention",  "L Inferior Parietal Lobule",61),
    (13, "FreeWont",          "L Posterior-Medial Frontal",19),
    (14, "MitosisGrowth",     "L Caudate Nucleus",      71),
]
REGION_OF_TRUE = np.array([roi - 1 for (_, _, _, roi) in NAMED], dtype=int)  # 0-indexed
assert len(set(REGION_OF_TRUE.tolist())) == H.N, "named regions must be distinct"
assert len(NAMED) == H.N, f"need {H.N} named lanes, got {len(NAMED)}"


def make_centroids_if_missing():
    """Compute AAL90 MNI centroids from ROI_MNI_V4.nii (reproducible) if the CSV is absent."""
    if os.path.exists(CENTROID):
        return
    import struct
    b = open(NIFTI, "rb").read()
    e = ">" if struct.unpack_from(">i", b, 0)[0] == 348 else "<"
    A = np.array([struct.unpack_from(e + "4f", b, 280),
                  struct.unpack_from(e + "4f", b, 296),
                  struct.unpack_from(e + "4f", b, 312), [0, 0, 0, 1]], dtype=float)
    vol = np.frombuffer(b, dtype=e + "i2", offset=352, count=91*109*91).reshape((91,109,91), order="F")
    u = np.unique(vol); u = u[u != 0]; aal90 = u[:90]
    names = [ln.split(";")[1] for ln in open(LABELS).read().splitlines()[1:]]
    with open(CENTROID, "w") as f:
        f.write("roi;name;aal_code;x_mni;y_mni;z_mni\n")
        for i, code in enumerate(aal90):
            ijk = np.argwhere(vol == code).mean(axis=0)
            mni = A @ np.array([ijk[0], ijk[1], ijk[2], 1.0])
            f.write(f"{i+1};{names[i]};{int(code)};{mni[0]:.3f};{mni[1]:.3f};{mni[2]:.3f}\n")


def load_centroids():
    """AAL90 region MNI centroids (90×3), index 0..89 = ROI#1..90."""
    make_centroids_if_missing()
    rows = open(CENTROID).read().splitlines()[1:]
    C = np.zeros((90, 3))
    for ln in rows:
        p = ln.split(";")
        C[int(p[0]) - 1] = [float(p[3]), float(p[4]), float(p[5])]
    return C


def load_group_avg():
    """AAL90 group-average structural connectome (88 healthy adults), symmetrized."""
    m = sio.loadmat(MAT)["SCmatrices"]            # (88, 90, 90)
    g = m.mean(axis=0)
    g = 0.5 * (g + g.T)
    np.fill_diagonal(g, 0.0)
    return g


def subnet(g, region_of):
    sub = g[np.ix_(region_of, region_of)].copy()
    np.fill_diagonal(sub, 0.0)
    return sub


def binarize_like_brain(sub):
    """Binarize the real weighted subnetwork at its OWN positive median → H_1512/1516 binary regime."""
    pos = sub[sub > 0]
    if pos.size == 0:
        return np.zeros_like(sub)
    thr = np.median(pos)
    A = (sub >= thr).astype(float)
    np.fill_diagonal(A, 0.0)
    return A


def phi_for_assignment(g, X, region_of):
    """Φ of placing the 15 lanes onto `region_of` (real subnetwork, binarized) — H_1512 min-cut Φ."""
    A = binarize_like_brain(subnet(g, region_of))
    return H.phi_core(H.apply_topology(X, A))


def cost_for_assignment(g, region_of, C):
    """Wiring COST of a placement = Σ over PRESENT edges of euclidean centroid distance (MNI mm).
    SAME binarized adjacency the Φ metric sees (the edges that carry integration also cost wire)."""
    A = binarize_like_brain(subnet(g, region_of))
    coords = C[region_of]                              # (15,3) MNI centroids of the placed regions
    total = 0.0
    n = A.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] > 0:
                total += float(np.linalg.norm(coords[i] - coords[j]))
    return total


def pareto_front_mask(costs, phis):
    """Non-dominated mask: point p is on the front iff NO other point has BOTH cost ≤ AND Φ ≥
    with strict improvement on ≥1 axis. O(n²) — fine for ~3000 points."""
    n = len(costs)
    on = np.ones(n, dtype=bool)
    for i in range(n):
        ci, pi = costs[i], phis[i]
        # dominated if some j has cost_j ≤ ci AND phi_j ≥ pi AND strictly better on ≥1
        dom = (costs <= ci) & (phis >= pi) & ((costs < ci) | (phis > pi))
        if np.any(dom):
            on[i] = False
    return on


def run_seed(seed, g, C):
    # NOTE (measurement-fix, frozen-first — see H_1517_FREEZE.txt): candidates draw 15 DISTINCT
    # regions from ALL 90 AAL nodes (the H_1516 random-baseline space). Permuting over the SAME
    # 15 named nodes is cost-degenerate (constant wiring cost) — that collapses the cost axis. The
    # all-90 search makes BOTH cost AND Φ vary, so the Pareto front is non-trivial. BARS UNCHANGED.
    Nr = g.shape[0]                                    # 90 AAL regions
    X = H.build_population(seed, H.N_TRIALS)            # engine-uniform population (R1==R2 pop)
    base_nodes = REGION_OF_TRUE.copy()                 # the TRUE 15 named regions (0-indexed)

    # ── candidate set: TRUE placement + M_RANDOM all-90 placements (15 distinct of 90) ──
    rng = np.random.default_rng(seed)
    costs = np.empty(M_RANDOM + 1)
    phis  = np.empty(M_RANDOM + 1)

    # index 0 = the TRUE anatomical placement
    costs[0] = cost_for_assignment(g, base_nodes, C)
    phis[0]  = phi_for_assignment(g, X, base_nodes)
    for k in range(1, M_RANDOM + 1):
        ro = rng.choice(Nr, size=H.N, replace=False)   # 15 distinct AAL regions out of 90
        costs[k] = cost_for_assignment(g, ro, C)
        phis[k]  = phi_for_assignment(g, X, ro)

    # ── Φ-optimum anchor: hill-climb over single-region REPLACEMENT across all 90 nodes (the
    #    H_1515/1516 unconstrained Φ-max — it occupies its OWN 15 regions with its OWN cost). ──
    def hillclimb(seed_nodes):
        nodes = list(seed_nodes)
        cur = phi_for_assignment(g, X, np.array(nodes))
        improved = True
        while improved:
            improved = False
            present = set(nodes)
            for i in range(H.N):
                old = nodes[i]
                for cand_region in range(Nr):
                    if cand_region in present:
                        continue
                    nodes[i] = cand_region
                    v = phi_for_assignment(g, X, np.array(nodes))
                    if v > cur + 1e-12:
                        cur = v; improved = True
                        present.discard(old); present.add(cand_region); old = cand_region
                    else:
                        nodes[i] = old
        return np.array(nodes), cur
    hc_rng = np.random.default_rng(seed + 999)
    best_nodes, opt_phi = hillclimb(base_nodes.copy())
    for _ in range(HILLCLIMB_RESTARTS):
        seed_nodes = hc_rng.choice(Nr, size=H.N, replace=False)
        nn, v = hillclimb(seed_nodes)
        if v > opt_phi:
            best_nodes, opt_phi = nn, v
    opt_cost = cost_for_assignment(g, best_nodes, C)
    # add the Φ-optimum into the candidate cloud (a real placement with its own cost & Φ)
    costs = np.append(costs, opt_cost); phis = np.append(phis, opt_phi)

    # ── the TRUE point's standing ────────────────────────────────────────────────────────
    ti = 0
    ct, pt = costs[ti], phis[ti]

    # P1a: strict-domination fraction (cost ≤ ct AND Φ ≥ pt AND strictly better on ≥1), excluding self
    dom = (costs <= ct) & (phis >= pt) & ((costs < ct) | (phis > pt))
    dom[ti] = False
    dom_frac = float(dom.sum()) / float(len(costs) - 1)

    # Pareto front of the full cloud
    front = pareto_front_mask(costs, phis)
    true_on_front = bool(front[ti])

    # P1b: normalized distance-to-front. Front points that dominate-or-tie the true on its axes
    # (cheaper-or-equal cost AND higher-or-equal Φ) are the ones the true would have to move to.
    cost_range = float(costs.max() - costs.min()) or 1.0
    phi_range  = float(phis.max() - phis.min()) or 1.0
    if true_on_front:
        dist_front = 0.0
    else:
        fidx = np.where(front)[0]
        # candidate front points the true point is dominated-toward: cheaper-or-equal AND higher-or-equal Φ
        cands = [f for f in fidx if costs[f] <= ct + 1e-12 and phis[f] >= pt - 1e-12]
        pool = cands if cands else list(fidx)   # fallback: nearest front point overall
        d = [np.sqrt(((ct - costs[f]) / cost_range) ** 2 + ((phis[f] - pt) / phi_range) ** 2) for f in pool]
        dist_front = float(min(d))

    # P2: true-cost percentile (fraction of candidates with cost ≤ ct) — bottom tercile?
    cost_pctl = float((costs <= ct).mean())

    # P3 (report): within the cheap band (cost ≤ ct), the true placement's Φ percentile
    cheap = costs <= ct + 1e-12
    cheap_phi_pctl = float((phis[cheap] <= pt).mean()) if cheap.sum() > 1 else 1.0

    # extra reporting
    phi_pctl_all = float((phis <= pt).mean())                  # H_1516-style Φ percentile (sanity)
    n_front = int(front.sum())

    return dict(
        seed=seed,
        cost_true=ct, phi_true=pt,
        cost_min=float(costs.min()), cost_max=float(costs.max()),
        cost_mean=float(costs.mean()),
        phi_min=float(phis.min()), phi_max=float(phis.max()), phi_mean=float(phis.mean()),
        opt_phi=float(opt_phi), opt_cost=float(opt_cost),
        dom_frac=dom_frac, true_on_front=true_on_front, dist_front=dist_front,
        cost_pctl=cost_pctl, cheap_phi_pctl=cheap_phi_pctl, phi_pctl_all=phi_pctl_all,
        n_front=n_front, n_candidates=int(len(costs)),
    )


def main():
    g = load_group_avg()
    C = load_centroids()
    rows = [run_seed(s, g, C) for s in SEEDS]
    keys = ["cost_true", "phi_true", "cost_min", "cost_max", "cost_mean", "phi_min", "phi_max",
            "phi_mean", "opt_phi", "opt_cost", "dom_frac", "dist_front", "cost_pctl",
            "cheap_phi_pctl", "phi_pctl_all", "n_front"]
    mean = {k: float(np.mean([r[k] for r in rows])) for k in keys}
    true_on_front_all = all(r["true_on_front"] for r in rows)

    dom_frac   = mean["dom_frac"]
    dist_front = mean["dist_front"]
    cost_pctl  = mean["cost_pctl"]

    # ── FROZEN bars (declared before reading — H_1517_FREEZE.txt) ──────────────────────────
    P1a_pass = dom_frac <= P1a_DOM_FRAC_MAX
    P1b_pass = dist_front <= P1b_DIST_MAX
    P1_pass  = P1a_pass and P1b_pass
    P2_pass  = cost_pctl <= P2_COST_PCTL_MAX

    if P1_pass and P2_pass:
        verdict = ("🟢 PARETO-EFFICIENT (DIRECTIONAL R1) — the TRUE anatomical placement lies ON/near "
                   "the Φ-vs-cost PARETO FRONT AND is in the cheap-wiring tercile: the brain is "
                   "NEAR-OPTIMAL for COST-CONSTRAINED integration. Once the wiring-cost axis is added "
                   "(Bullmore & Sporns 2012 economy), the user's 'mysteriously optimal' intuition is "
                   "RIGHT — the placement only looked suboptimal because pure-Φ ignored the cost it pays")
    elif P2_pass and not P1_pass:
        verdict = ("🟠 CHEAP-but-DOMINATED (DIRECTIONAL R1) — the TRUE placement is in the cheap-wiring "
                   "tercile (P2) but a cheaper-or-equal-cost placement achieves strictly higher Φ "
                   f"({dom_frac*100:.1f}% of candidates dominate it): dominated even cost-constrained — "
                   "honest non-optimal (the brain pays for cheap wire but does NOT sit on the front here)")
    elif P1_pass and not P2_pass:
        verdict = ("🟠 EFFICIENT-but-NOT-CHEAP (DIRECTIONAL R1) — the TRUE placement is on/near the front "
                   "but NOT in the cheap tercile: Pareto-efficient yet not the cheapest regime")
    else:
        verdict = ("🧱 DOMINATED (DIRECTIONAL R1) — the TRUE anatomical placement is NEITHER on the "
                   "Φ-vs-cost Pareto front NOR in the cheap tercile: dominated even cost-constrained "
                   "(honest negative, c9 — the cost axis does NOT rescue the placement here)")

    out = dict(
        hypothesis="H_1517_cost_pareto",
        rung="R1_numpy_scipy_mirror_DIRECTIONAL",
        question=("does the TRUE anatomical placement lie ON/near the Φ-vs-cost PARETO FRONT — "
                  "i.e. is the brain near-optimal for COST-CONSTRAINED integration?"),
        data=dict(
            connectome=dict(source="Škoch et al. 2022 Scientific Data 9:486, AAL90, 88 healthy adults, group avg",
                            doi="10.1038/s41597-022-01596-9", osf="10.17605/OSF.IO/YW5VF", license="CC-BY-4.0"),
            centroids=dict(source="AAL atlas ROI_MNI_V4.nii (Tzourio-Mazoyer et al. 2002, NeuroImage 15(1):273-289)",
                           method="per-ROI mean MNI coordinate of all labeled voxels (MNI 2mm, sform affine)",
                           file="AAL90_centroids_MNI.csv (committed, reproducible from atlas NIfTI)"),
            atlas="AAL90 (ROI_MNI_v4)"),
        harness=("re-uses H_1512 h1512.py (build_population/apply_topology/phi_core IIT4 min-cut Φ/CORE/"
                 "N=15) byte-for-byte + H_1516 NAMED lane→region map; COST axis = Σ present-edge euclidean "
                 "centroid distance (MNI mm) over the SAME binarized adjacency the Φ metric sees"),
        metric=dict(phi="IIT4 min-cut Φ (phi_core over CORE)", cost="Σ present-edge euclidean centroid distance (MNI mm)"),
        seeds=SEEDS, M_random=M_RANDOM, hillclimb_restarts=HILLCLIMB_RESTARTS,
        thresholds=dict(P1a_DOM_FRAC_MAX=P1a_DOM_FRAC_MAX, P1b_DIST_MAX=P1b_DIST_MAX, P2_COST_PCTL_MAX=P2_COST_PCTL_MAX),
        named_mapping=[dict(lane_idx=i, lane=n, region=r, roi=roi) for (i, n, r, roi) in NAMED],
        results=dict(
            cost_true=mean["cost_true"], phi_true=mean["phi_true"],
            cost_range=[mean["cost_min"], mean["cost_max"]], cost_mean=mean["cost_mean"],
            phi_range=[mean["phi_min"], mean["phi_max"]], phi_mean=mean["phi_mean"],
            opt_phi=mean["opt_phi"], opt_cost=mean["opt_cost"],
            true_on_front=true_on_front_all,
            domination_fraction=dom_frac,
            distance_to_front=dist_front,
            cost_percentile=cost_pctl,
            cheap_band_phi_percentile=mean["cheap_phi_pctl"],
            phi_percentile_all=mean["phi_pctl_all"],
            n_front_points=mean["n_front"], n_candidates=rows[0]["n_candidates"],
        ),
        bars=dict(
            P1_pareto_efficient=dict(passed=bool(P1_pass),
                P1a_domination=dict(passed=bool(P1a_pass), dom_frac=dom_frac, bar=P1a_DOM_FRAC_MAX),
                P1b_distance=dict(passed=bool(P1b_pass), dist_front=dist_front, bar=P1b_DIST_MAX)),
            P2_cost_cheap=dict(passed=bool(P2_pass), cost_percentile=cost_pctl, bar=P2_COST_PCTL_MAX),
            P3_cheap_band_phi=dict(non_gating=True, cheap_band_phi_percentile=mean["cheap_phi_pctl"]),
        ),
        HEADLINE=(f"TRUE anatomical placement: cost={mean['cost_true']:.1f}mm (cost-percentile "
                  f"{cost_pctl*100:.1f}% — {'CHEAP/bottom-tercile' if P2_pass else 'NOT cheap'}), "
                  f"Φ={mean['phi_true']:.4f}; dominated by {dom_frac*100:.2f}% of candidates, "
                  f"distance-to-front={dist_front:.4f} → "
                  f"{'ON/NEAR the Φ-vs-cost Pareto front = brain NEAR-OPTIMAL for cost-constrained integration' if P1_pass else 'OFF the front (dominated even cost-constrained)'}"),
        verdict=verdict,
        per_seed=rows,
    )
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
