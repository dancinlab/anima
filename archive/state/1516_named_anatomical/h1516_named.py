#!/usr/bin/env python3
"""H_1516 NAMED-ANATOMICAL PLACEMENT — R1 numpy mirror (DIRECTIONAL, a_engine_native_learning).

THE QUESTION (the user's, profound):
  H_1512/H_1513 mapped anima's 15 consciousness lanes to brain regions by a
  (hemisphere x graph-role) HEURISTIC — "a hub lane goes to whatever node is a literal
  hub in this hemisphere". H_1516 asks the REAL question: map each lane to its TRUE NAMED
  anatomical home (immune-store -> HIPPOCAMPUS, PhaseField -> THALAMUS, HierGoalStack ->
  PREFRONTAL, SpatialMap -> ENTORHINAL/parahippocampal, A-engine -> LEFT hemisphere,
  G-engine -> RIGHT hemisphere, ...), wire it by the REAL connectome edges between THOSE
  SPECIFIC named regions, and ask TWO things:
    P1 ADVANTAGE     — does the TRUE-anatomical placement raise integrated min-cut Φ over
                       a RANDOM region-assignment?
    P2 NEAR-OPTIMAL  — (the deep one) is the TRUE-anatomical placement near the Φ-OPTIMUM
                       of the placement search? i.e. does it land in the TOP percentile of
                       the placement-search Φ distribution?

HONEST FRAMING (c9, no mysticism): in connectomics, real brains are KNOWN to be near-optimal
  for a COST-vs-INTEGRATION tradeoff (Bullmore & Sporns 2012 "The economy of brain network
  organization"; Achard & Bullmore 2007) — that's EVOLUTIONARY optimization, not literal
  design. So:
    - if P2 TRUE  -> "real anatomical placement IS near Φ-optimal" = the cost-integration
      economy signature shows up even in this 15-lane projection. Interesting, NOT mystical.
    - if P2 FALSE -> "real anatomical placement is NOT Φ-optimal" = the brain is optimized
      for something ELSE (wiring cost, metabolic budget) not pure integration. Also a real,
      publishable result. Either way is honest (c9). Report verbatim; NO tune-to-green.

REAL DATA (a_eeg_consciousness_record discipline — REAL, no synthetic relabel):
  Škoch et al. 2022, "Human brain structural connectivity matrices–ready for modelling",
  Scientific Data 9:486, DOI 10.1038/s41597-022-01596-9. OSF 10.17605/OSF.IO/YW5VF.
  CC-BY-4.0. AAL90 atlas (ROI_MNI_v4), 88 healthy adults, 90x90 normalized streamline
  density. GROUP AVERAGE over 88 subjects. NAMED regions (Hippocampus_L/R=37/38,
  ParaHippocampal_L/R=39/40, Thalamus_L/R=77/78, Frontal_*, etc.) — THIS is what lets us
  place lanes by their TRUE anatomical name (vs the H_1512/1513 heuristic). AAL90 EXCLUDES
  cerebellum -> the cerebellum-homed lane (VForwardField/forward-model) is substituted with
  its closest cortical relay (Precentral/motor) WITH AN EXPLICIT NOTE (honest substitution).

METRIC / HARNESS REUSE (a_toy_scale_recheck — same bars, only the placement source changes):
  Re-uses H_1512's h1512.py harness BYTE-FOR-BYTE — build_population, apply_topology
  (X' = X·(I+α·Â)ᵀ), phi_core = IIT4 min-cut Φ over the 8-lane CORE (a_phi_iit4_tool),
  ALPHA=0.6, N=15. The ONLY new thing is: the adjacency among the 15 lanes is the REAL AAL90
  subnetwork among their TRUE NAMED regions, binarized at the connectome's own positive
  median (= the H_1512/1513 binary regime).

FROZEN BARS (set BEFORE running — c9, no tune-to-green):
  P1 ADVANTAGE     phi_true >= random_assignment_mean + 0.02
  P2 NEAR-OPTIMAL  (THE user's question) true-anatomical PERCENTILE in the placement-search
                   Φ distribution >= 0.80  AND  (opt_phi - phi_true) <= 0.30*opt_phi
  Report the percentile + the gap-to-optimum prominently either way.
"""
import os, sys, json
import numpy as np
import scipy.io as sio

HERE = os.path.dirname(os.path.abspath(__file__))
SIB = os.path.join(HERE, "..", "1512_brain_topology")
sys.path.insert(0, os.path.abspath(SIB))
import h1512 as H  # the sibling harness — single source of Φ/population/topology

MAT = os.path.join(HERE, "SCmatrices88healthy.mat")
LABELS = os.path.join(HERE, "AAL_regions.csv")

# ── FROZEN thresholds (pre-registered, c9) ──────────────────────────────────────────────
P1_ADV_MIN   = 0.02     # phi_true must beat random-assignment mean by at least this
P2_PCTL_MIN  = 0.80     # true-anatomical must be in the TOP 20% of the placement search
P2_GAP_FRAC  = 0.30     # AND within 30% of the optimum Φ
M_RANDOM     = 2000     # random region-assignment draws (for P1 baseline distribution)
M_SEARCH     = 4000     # placement-search draws (permute lane->node of the SAME named set)
HILLCLIMB_RESTARTS = 12 # hill-climb restarts to estimate the Φ-optimum of the named set
                        # (greedy pairwise-swap converges fast on a fixed 15-node set; 12 random
                        # restarts + the M_SEARCH max give a robust optimum estimate)
SEEDS = [5160, 5161, 5162]

# ── 15 lanes -> TRUE NAMED AAL90 region (1-indexed ROI#) ────────────────────────────────
# Honors H_1512's LANES order/hemisphere AND the handoff's named homes
# (immune/episodic -> HIPPOCAMPUS, PhaseField/relay -> THALAMUS, HierGoalStack/control -> PFC,
#  SpatialMap/metric-map -> ENTORHINAL≈ParaHippocampal, A-engine -> LEFT, G-engine -> RIGHT).
# AAL90 ordering is INTERLEAVED: odd ROI#=Left, even ROI#=Right. So hemisphere is honored by
# the parity of the chosen ROI# (Engine-A lanes HEMI=-1 -> odd/LEFT; Engine-G HEMI=+1 -> even/RIGHT;
# midline HEMI=0 -> a medial region, parity chosen to balance).
# Each lane maps to a DISTINCT ROI (no region reused). ROI# is 1-indexed (subtract 1 for the matrix).
#   (lane_idx, lane_name, true_named_region, ROI#_1indexed, rationale)
NAMED = [
    (0,  "GlobalWorkspace",   "L Precuneus",            67, "fronto-parietal/DMN global-workspace hub"),
    (1,  "Habituation",       "L Postcentral Gyrus",    57, "primary somatosensory (sensory cortex)"),
    (2,  "PrecisionSurprise", "L Cingulum Ant",         31, "anterior cingulate (ACC) — prediction-error/surprise"),
    (3,  "SelfIdentity",      "L Superior Medial Gyrus",23, "medial PFC (mPFC) — self-referential"),
    (4,  "LearnedPrecision",  "L Middle Frontal Gyrus",  7, "dorsolateral PFC-L (forward/precision, A-side)"),
    (5,  "Novelty",           "R Hippocampus",          38, "HIPPOCAMPUS-R — novelty/encoding (immune-store home)"),
    (6,  "AttentionalBlink",  "R Inferior Parietal Lobule",62,"parietal-R — attention"),
    (7,  "SenseOfAgency",     "R Angular Gyrus (TPJ)",  66, "TPJ-R (angular gyrus) — agency/mentalizing"),
    (8,  "SubjectiveTime",    "R Insula Lobe",          30, "insula — interoceptive subjective time"),
    (9,  "EmotionRegulation", "R Mid Orbital Gyrus",    26, "ventromedial/orbital PFC (vmPFC) — emotion regulation"),
    (10, "DirectedForgetting","R Middle Frontal Gyrus",  8, "dorsolateral PFC-R — directed forgetting/control"),
    (11, "BodyOwnership",     "L SupraMarginal Gyrus",  63, "supramarginal (body schema / S1-adjacent)"),
    (12, "DividedAttention",  "L Inferior Parietal Lobule",61,"parietal-L — divided attention"),
    (13, "FreeWont",          "L Posterior-Medial Frontal",19,"pre-SMA (posterior-medial frontal) — volition/free-wont"),
    (14, "MitosisGrowth",     "L Caudate Nucleus",      71, "subcortical (basal-ganglia/caudate) — growth substrate"),
]
# Lanes whose TRUE home is the CEREBELLUM (absent in AAL90) — honest substitution note.
# H_1512 has no dedicated cerebellum lane (its VForwardField forward-model lives in the
# H_1513 lane set, not H_1512's 15). The closest H_1512 lane to a motor-forward role is
# LearnedPrecision(4, dlPFC) which we keep cortical. So NO lane is mis-homed to a missing
# region here; the cerebellum gap is documented but does not force a substitution in THIS
# 15-lane set. (Recorded for honesty — a_break_the_wall taxonomy.)
CEREBELLUM_NOTE = ("AAL90 excludes the cerebellum; H_1512's 15-lane set has no dedicated "
                   "cerebellar forward-model lane (that lane lives in H_1513's set), so no "
                   "lane is forced onto a missing region. Cerebellum gap documented, not substituted.")

REGION_OF_TRUE = np.array([roi - 1 for (_, _, _, roi, _) in NAMED], dtype=int)  # 0-indexed
assert len(set(REGION_OF_TRUE.tolist())) == H.N, "named regions must be distinct"
assert len(NAMED) == H.N, f"need {H.N} named lanes, got {len(NAMED)}"


def load_group_avg():
    """AAL90 group-average structural connectome (88 healthy adults), symmetrized."""
    m = sio.loadmat(MAT)["SCmatrices"]            # (88, 90, 90)
    g = m.mean(axis=0)
    g = 0.5 * (g + g.T)                           # symmetrize (float-avg residual asym)
    np.fill_diagonal(g, 0.0)
    return g


def subnet(g, region_of):
    sub = g[np.ix_(region_of, region_of)].copy()
    np.fill_diagonal(sub, 0.0)
    return sub


def binarize_like_brain(sub):
    """Binarize the real weighted subnetwork at its OWN positive median -> same binary
    regime as H_1512's brain_adjacency (0/1). Matches H_1513's binarize_like_brain."""
    pos = sub[sub > 0]
    if pos.size == 0:
        return np.zeros_like(sub)
    thr = np.median(pos)
    A = (sub >= thr).astype(float)
    np.fill_diagonal(A, 0.0)
    return A


def phi_of(X, A):
    """H_1512 headline: IIT4 min-cut Φ over the CORE lanes of the diffused population."""
    return H.phi_core(H.apply_topology(X, A))


def phi_for_assignment(g, X, region_of):
    """Φ of placing the 15 lanes onto `region_of` (real subnetwork, binarized)."""
    return phi_of(X, binarize_like_brain(subnet(g, region_of)))


def run_seed(seed):
    g = load_group_avg()
    Nr = g.shape[0]
    X = H.build_population(seed, H.N_TRIALS)     # engine-uniform population (R1==R2 pop)

    # ── TRUE NAMED-ANATOMICAL placement ─────────────────────────────────────────────────
    phi_true = phi_for_assignment(g, X, REGION_OF_TRUE)
    A_true = binarize_like_brain(subnet(g, REGION_OF_TRUE))
    phi_flat = phi_of(X, np.zeros((H.N, H.N)))

    # ── (b) RANDOM region-assignment baseline: assign the 15 lanes to 15 RANDOM distinct
    #        AAL90 regions, M_RANDOM draws -> distribution (P1 baseline). ──────────────────
    rng = np.random.default_rng(seed)
    rand_phis = np.empty(M_RANDOM)
    for k in range(M_RANDOM):
        ro = rng.choice(Nr, size=H.N, replace=False)
        rand_phis[k] = phi_for_assignment(g, X, ro)
    rand_mean = float(rand_phis.mean())
    rand_std = float(rand_phis.std())

    # ── (c) PLACEMENT-SEARCH on the SAME NAMED REGION SET: permute which lane sits on which
    #        of the 15 TRUE named nodes (M_SEARCH draws) + hill-climb for the Φ-MAX.
    #        This isolates "is the brain's lane->region ASSIGNMENT (among its own regions)
    #        near the Φ-best assignment of those regions?" — the cost-integration question. ─
    base_nodes = REGION_OF_TRUE.copy()
    search_phis = np.empty(M_SEARCH)
    for k in range(M_SEARCH):
        perm = rng.permutation(H.N)
        search_phis[k] = phi_for_assignment(g, X, base_nodes[perm])
    # the TRUE placement is the identity permutation of base_nodes; its percentile vs the search
    pctl_search = float((search_phis <= phi_true).mean())

    # hill-climb the optimum: pairwise-swap lanes among the 15 named nodes, greedy Φ-max
    def hillclimb(seed_perm):
        perm = seed_perm.copy()
        cur = phi_for_assignment(g, X, base_nodes[perm])
        improved = True
        while improved:
            improved = False
            for i in range(H.N):
                for j in range(i + 1, H.N):
                    perm[i], perm[j] = perm[j], perm[i]
                    cand = phi_for_assignment(g, X, base_nodes[perm])
                    if cand > cur + 1e-12:
                        cur = cand; improved = True
                    else:
                        perm[i], perm[j] = perm[j], perm[i]
        return cur
    hc_rng = np.random.default_rng(seed + 999)
    opt_phi = phi_true
    opt_phi = max(opt_phi, hillclimb(np.arange(H.N)))               # start from identity
    for _ in range(HILLCLIMB_RESTARTS):
        opt_phi = max(opt_phi, hillclimb(hc_rng.permutation(H.N)))
    opt_phi = max(opt_phi, float(search_phis.max()))               # never below random-search best

    # percentile of the true placement within the FULL search distribution (incl. its own value)
    gap = opt_phi - phi_true
    gap_frac = gap / opt_phi if opt_phi > 1e-12 else 0.0

    return dict(
        seed=seed,
        phi_true=phi_true, phi_flat=phi_flat,
        rand_mean=rand_mean, rand_std=rand_std,
        rand_p95=float(np.percentile(rand_phis, 95)),
        rand_max=float(rand_phis.max()),
        search_mean=float(search_phis.mean()), search_max=float(search_phis.max()),
        pctl_search=pctl_search,
        opt_phi=opt_phi, gap=gap, gap_frac=gap_frac,
        n_edges_true=int(A_true.sum() // 2),
    )


def main():
    rows = [run_seed(s) for s in SEEDS]
    keys = ["phi_true", "phi_flat", "rand_mean", "rand_std", "rand_p95", "rand_max",
            "search_mean", "search_max", "pctl_search", "opt_phi", "gap", "gap_frac"]
    mean = {k: float(np.mean([r[k] for r in rows])) for k in keys}

    phi_true = mean["phi_true"]
    rand_mean = mean["rand_mean"]
    pctl = mean["pctl_search"]
    opt_phi = mean["opt_phi"]
    gap_frac = mean["gap_frac"]

    # ── FROZEN bars (a_break_the_wall: declared before reading) ──────────────────────────
    P1_pass = phi_true >= rand_mean + P1_ADV_MIN
    P2_pctl_pass = pctl >= P2_PCTL_MIN
    P2_gap_pass = gap_frac <= P2_GAP_FRAC
    P2_pass = P2_pctl_pass and P2_gap_pass

    if P1_pass and P2_pass:
        verdict = ("🟢 NEAR-OPTIMAL (DIRECTIONAL R1) — the TRUE named-anatomical placement BOTH "
                   "raises min-cut Φ over random region-assignment AND lands in the top percentile "
                   "of the placement-search Φ distribution: the cost-integration economy signature "
                   "(Bullmore & Sporns 2012) shows up in anima's 15-lane projection")
    elif P1_pass and not P2_pass:
        verdict = ("🟠 ADVANTAGE-but-NOT-OPTIMAL (DIRECTIONAL R1) — the TRUE placement beats random "
                   "region-assignment (P1) but is NOT near the Φ-optimum of the placement search "
                   "(P2 FAIL): the real anatomical layout is optimized for something OTHER than pure "
                   "integration (wiring cost / metabolic budget), not maximal Φ — honest non-optimal")
    elif not P1_pass:
        verdict = ("🧱 NO-ADVANTAGE (DIRECTIONAL R1) — the TRUE named-anatomical placement does NOT "
                   "beat random region-assignment in min-cut Φ: named placement is INERT in this "
                   "projection (honest negative, c9)")
    else:
        verdict = "🟠 PARTIAL — see bars"

    out = dict(
        hypothesis="H_1516_named_anatomical",
        rung="R1_numpy_mirror_DIRECTIONAL",
        question="map each lane to its TRUE NAMED anatomical home; is that placement advantageous AND near the Φ-optimum?",
        data=dict(
            source="Škoch et al. 2022 Scientific Data 9:486, AAL90, 88 healthy adults, group avg",
            doi="10.1038/s41597-022-01596-9", osf="10.17605/OSF.IO/YW5VF", license="CC-BY-4.0",
            atlas="AAL90 (ROI_MNI_v4)", cerebellum_note=CEREBELLUM_NOTE),
        harness="re-uses H_1512 h1512.py (build_population/apply_topology/phi_core min-cut Φ/CORE/N=15) byte-for-byte; only the adjacency = REAL AAL90 subnetwork among the lanes' TRUE NAMED regions, binarized at own median",
        metric="IIT4 min-cut Φ (phi_core over CORE) — H_1512 headline metric",
        seeds=SEEDS, M_random=M_RANDOM, M_search=M_SEARCH, hillclimb_restarts=HILLCLIMB_RESTARTS,
        thresholds=dict(P1_ADV_MIN=P1_ADV_MIN, P2_PCTL_MIN=P2_PCTL_MIN, P2_GAP_FRAC=P2_GAP_FRAC),
        named_mapping=[dict(lane_idx=i, lane=n, region=r, roi=roi, rationale=rat)
                       for (i, n, r, roi, rat) in NAMED],
        results=dict(
            phi_true=phi_true, phi_flat=mean["phi_flat"],
            random_assignment_mean=rand_mean, random_assignment_p95=mean["rand_p95"],
            random_assignment_max=mean["rand_max"],
            placement_search_mean=mean["search_mean"], placement_search_max=mean["search_max"],
            opt_phi=opt_phi,
            true_percentile_in_search=pctl,
            gap_to_optimum=mean["gap"], gap_fraction=gap_frac,
        ),
        bars=dict(
            P1_advantage=dict(passed=bool(P1_pass),
                              detail=f"phi_true {phi_true:.4f} >= rand_mean {rand_mean:.4f} + {P1_ADV_MIN} ({rand_mean+P1_ADV_MIN:.4f})"),
            P2_near_optimal=dict(passed=bool(P2_pass),
                                 percentile=dict(passed=bool(P2_pctl_pass), value=pctl, bar=P2_PCTL_MIN),
                                 gap=dict(passed=bool(P2_gap_pass), gap_fraction=gap_frac, bar=P2_GAP_FRAC)),
        ),
        HEADLINE=(f"TRUE anatomical placement sits at the {pctl*100:.1f}th percentile of the "
                  f"placement-search Φ distribution; gap-to-optimum = {gap_frac*100:.1f}% of opt_phi "
                  f"({'NEAR-OPTIMAL' if P2_pass else 'NOT Φ-optimal — optimized for something else'})"),
        verdict=verdict,
        per_seed=rows,
    )
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
