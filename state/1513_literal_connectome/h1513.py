#!/usr/bin/env python3
"""H_1513 LITERAL-CONNECTOME — literal-data scale-recheck (a_toy_scale_recheck) of
H_1512 BRAIN-TOPOLOGY.

Replaces the STATISTICALLY-FAITHFUL synthetic small-world/rich-club topology with a
REAL, published human structural connectome (Hagmann/BCT DSI group average, 219
regions × 8 subjects, GPLv3 — see PROVENANCE.md) and re-scores the SAME frozen bars.

R1 = numpy mirror (DIRECTIONAL — a_engine_native_learning). $0 CPU, p7, frozen-first,
c9. If the literal connectome REPRODUCES H_1512's advantage → synthetic was faithful,
scale-transfer confirmed. If NOT → honest 🟠/🔴 (synthetic over-fit). NO tune-to-green.

PHI MECHANISM (mirrors live core/engine_cli.hexa ci_phi_multiinfo, the Gaussian
multi-information Φ = ½(Σ_i ln Σ_ii − ln det Σ) ≥ 0 op H_1512 feeds topology into):
a lane×lane coupling C (derived from the connectome subnetwork among the mapped
regions) shapes a multivariate-Gaussian lane population X; Φ(X) measures how
integrated the lanes are. Real wiring that is small-world + rich-club + hemispherically
organized should integrate MORE than a flat (uniform) or degree-matched random graph.
"""
import numpy as np
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = [4513, 4514, 4515]
NSAMP = 4000          # Gaussian samples per lane population
COUPLE = 0.55         # base coupling gain applied to normalized connectome weights

# ---------------------------------------------------------------------------
# anima lane -> brain-region scheme (re-use H_1512's anatomical mapping).
# Each lane maps to an anatomical region; the LITERAL realization picks that
# region's index in the real connectome by graph ROLE (hub lanes -> literal hubs,
# peripheral lanes -> literal low-degree nodes) AND by hemisphere (A:left / G:right).
# This is the faithful "real wiring" realization of the named-region scheme: only the
# ADJACENCY SOURCE changes (synthetic -> literal); the lane set + roles + hemispheres
# are identical to H_1512.
# role: 'hub' (rich-club core) | 'mid' | 'periph';  hemi: 'L'(A-engine) | 'R'(G-engine)
LANES = [
    ("ConsciousnessIndex", "precuneus/hub",     "hub",    "L"),  # global workspace hub
    ("PhaseField",         "thalamus",          "hub",    "R"),  # relay hub
    ("ImmuneMemory",       "hippocampus",       "mid",    "L"),  # episodic store
    ("HierGoalStack",      "dlPFC",             "mid",    "L"),  # PFC control
    ("VForwardField",      "cerebellum",        "mid",    "R"),  # forward model
    ("VBasalGate",         "basal-ganglia",     "mid",    "R"),  # gating (subcortical)
    ("AffectField",        "amygdala/insula",   "periph", "R"),  # affect
    ("SpatialMap",         "entorhinal/parietal","periph","L"),  # metric map
    ("HomeostaticDrive",   "hypothalamus",      "periph", "R"),  # drive
    ("OtherMindModel",     "TPJ",               "periph", "L"),  # theory-of-mind
]
NL = len(LANES)


# ---------------------------------------------------------------------------
def load_connectome():
    a = np.load(os.path.join(HERE, "sample_group_dsi.npy"))  # (219,219,8)
    g = a.mean(axis=2)                                        # group average
    np.fill_diagonal(g, 0.0)
    return g


def map_lanes_to_regions(g, rng):
    """Pick a real region index for each lane by (hemisphere, graph-role).
    REAL wiring decides which region is a hub: role 'hub' draws from the literal
    high-strength rich-club, 'periph' from the low-degree fringe, within the lane's
    hemisphere half. Deterministic-given-seed tie-breaks only."""
    N = g.shape[0]
    h = N // 2                       # contiguous L | R split (verified ~4x intra/cross)
    strength = g.sum(1)
    Lidx = np.arange(0, h)
    Ridx = np.arange(h, N)
    # rank within each hemisphere by strength (descending)
    def ranked(idxs):
        return idxs[np.argsort(-strength[idxs])]
    Lr, Rr = ranked(Lidx), ranked(Ridx)
    # role -> quantile band within the hemisphere's strength ranking
    band = {"hub": (0.0, 0.12), "mid": (0.30, 0.55), "periph": (0.78, 1.0)}
    used = set()
    region_of = []
    for (_, _, role, hemi) in LANES:
        ranks = Lr if hemi == "L" else Rr
        lo, hi = band[role]
        a0, a1 = int(lo * len(ranks)), max(int(hi * len(ranks)), int(lo * len(ranks)) + 1)
        cand = [int(x) for x in ranks[a0:a1] if int(x) not in used]
        if not cand:
            cand = [int(x) for x in ranks if int(x) not in used]
        pick = int(rng.choice(cand))
        used.add(pick)
        region_of.append(pick)
    return np.array(region_of), h


def lane_coupling_from_adjacency(adj, region_of):
    """Extract the lane×lane subnetwork: C[i,j] = connectome weight between the
    regions mapped to lane i and lane j, normalized to its own max."""
    sub = adj[np.ix_(region_of, region_of)].copy()
    np.fill_diagonal(sub, 0.0)
    m = sub.max()
    if m > 0:
        sub = sub / m
    return sub


def phi_multiinfo(cov):
    """Gaussian multi-information Φ = ½(Σ_i ln Σ_ii − ln det Σ), the exact mirror of
    core/engine_cli.hexa ci_phi_multiinfo."""
    d = np.clip(np.diag(cov), 1e-9, None)
    sign, logdet = np.linalg.slogdet(cov)
    if sign <= 0:
        # numerical floor: regularize
        cov = cov + 1e-6 * np.eye(cov.shape[0])
        sign, logdet = np.linalg.slogdet(cov)
    phi = 0.5 * (np.sum(np.log(d)) - logdet)
    return max(phi, 0.0)


def population_from_coupling(C, rng, n=NSAMP, gain=COUPLE):
    """Build a lane population X whose covariance reflects coupling C: each lane =
    own innovation + sum_j gain*C[i,j]*innovation_j (a one-step linear mix on the
    literal graph), then Φ of its sample covariance."""
    nl = C.shape[0]
    z = rng.standard_normal((n, nl))          # independent innovations
    mix = np.eye(nl) + gain * C               # one-step structural propagation
    x = z @ mix.T
    cov = np.cov(x, rowvar=False)
    return phi_multiinfo(cov), cov


def global_efficiency(adj):
    """Weighted global efficiency on the lane subnetwork (distance = 1/weight)."""
    nl = adj.shape[0]
    D = np.full((nl, nl), np.inf)
    np.fill_diagonal(D, 0.0)
    W = adj.copy()
    dist = np.where(W > 0, 1.0 / np.maximum(W, 1e-9), np.inf)
    np.fill_diagonal(dist, 0.0)
    # Floyd-Warshall (small nl)
    D = dist.copy()
    for k in range(nl):
        D = np.minimum(D, D[:, [k]] + D[[k], :])
    inv = np.where(np.isfinite(D) & (D > 0), 1.0 / D, 0.0)
    return inv.sum() / (nl * (nl - 1))


def degree_matched_random(C, rng):
    """Random graph preserving each lane's total coupling strength (config-model
    style on the lane subnetwork): shuffle the off-diagonal weights then symmetrize,
    rescaling rows toward original strength."""
    nl = C.shape[0]
    iu = np.triu_indices(nl, 1)
    w = C[iu].copy()
    rng.shuffle(w)
    R = np.zeros_like(C)
    R[iu] = w
    R = R + R.T
    # rescale to match per-node strength as closely as a single pass allows
    s0 = C.sum(1); s1 = R.sum(1)
    scale = np.where(s1 > 0, s0 / np.maximum(s1, 1e-9), 1.0)
    R = R * np.sqrt(np.outer(scale, scale))
    np.fill_diagonal(R, 0.0)
    return R


def ablate_richclub(C, region_strength, region_of, k=2):
    """Remove the k strongest (rich-club hub) lanes' edges -> coupling drop test."""
    lane_strength = region_strength[region_of]
    hubs = np.argsort(-lane_strength)[:k]
    Ca = C.copy()
    for hbi in hubs:
        Ca[hbi, :] = 0.0
        Ca[:, hbi] = 0.0
    return Ca, hubs.tolist()


def lateralization_phi(C, region_of, h, rng):
    """A/G lateralization: A-engine lanes = left-hemi regions, G = right. Within-hemi
    coupling is the literal intra-hemispheric (strong) block; a 'flattened' version
    that ERASES the hemisphere distinction (mix L/R uniformly) should integrate worse
    if lateralization is load-bearing."""
    is_left = np.array([region_of[i] < h for i in range(C.shape[0])])
    # keep only within-hemisphere literal coupling (the real lateralized structure)
    latC = C.copy()
    for i in range(C.shape[0]):
        for j in range(C.shape[0]):
            if is_left[i] != is_left[j]:
                latC[i, j] = latC[i, j] * 0.20   # real cross-hemi ~0.24x intra (measured)
    # de-lateralized control: replace with hemisphere-blind uniform of same total
    blind = np.full_like(C, latC[latC > 0].mean() if (latC > 0).any() else 0.0)
    np.fill_diagonal(blind, 0.0)
    phi_lat, _ = population_from_coupling(latC, rng)
    phi_blind, _ = population_from_coupling(blind, np.random.default_rng(rng.integers(1 << 30)))
    return phi_lat, phi_blind, is_left.tolist()


def run_seed(seed):
    rng = np.random.default_rng(seed)
    adj = load_connectome()
    region_of, h = map_lanes_to_regions(adj, rng)
    region_strength = adj.sum(1)

    C_brain = lane_coupling_from_adjacency(adj, region_of)

    # FLAT: uniform coupling of the same average magnitude (no topology)
    mean_off = C_brain[np.triu_indices(NL, 1)].mean()
    C_flat = np.full((NL, NL), mean_off); np.fill_diagonal(C_flat, 0.0)

    # RANDOM: degree-matched random rewiring
    C_rand = degree_matched_random(C_brain, np.random.default_rng(seed + 100))

    phi_brain, _ = population_from_coupling(C_brain, np.random.default_rng(seed + 1))
    phi_flat, _  = population_from_coupling(C_flat,  np.random.default_rng(seed + 2))
    phi_rand, _  = population_from_coupling(C_rand,  np.random.default_rng(seed + 3))

    eff_brain = global_efficiency(C_brain)
    eff_flat  = global_efficiency(C_flat)
    eff_rand  = global_efficiency(C_rand)

    # (C) rich-club hub ablation
    C_abl, hubs = ablate_richclub(C_brain, region_strength, region_of, k=2)
    phi_abl, _ = population_from_coupling(C_abl, np.random.default_rng(seed + 4))

    # (D) A/G lateralization
    phi_lat, phi_blind, is_left = lateralization_phi(C_brain, region_of, h,
                                                     np.random.default_rng(seed + 5))

    # (E) coord/region shuffle: permute the lane->region assignment -> destroys the
    # literal wiring's lane structure -> Φ should decorrelate toward random.
    perm = np.random.default_rng(seed + 6).permutation(adj.shape[0])[:NL]
    C_shuf = lane_coupling_from_adjacency(adj, perm)
    phi_shuf, _ = population_from_coupling(C_shuf, np.random.default_rng(seed + 7))

    return dict(seed=seed, region_of=region_of.tolist(), hubs=hubs,
                phi_brain=phi_brain, phi_flat=phi_flat, phi_rand=phi_rand,
                eff_brain=eff_brain, eff_flat=eff_flat, eff_rand=eff_rand,
                phi_abl=phi_abl, phi_lat=phi_lat, phi_blind=phi_blind,
                phi_shuf=phi_shuf)


def main():
    results = [run_seed(s) for s in SEEDS]
    def mean(k): return float(np.mean([r[k] for r in results]))

    pb, pf, pr = mean("phi_brain"), mean("phi_flat"), mean("phi_rand")
    eb, ef, er = mean("eff_brain"), mean("eff_flat"), mean("eff_rand")
    pa = mean("phi_abl"); plat, pbl = mean("phi_lat"), mean("phi_blind")
    psh = mean("phi_shuf")

    # FROZEN bars (a_break_the_wall: declared before reading; mirror H_1512 A-E)
    # (A) LITERAL-BRAIN Φ AND efficiency >= FLAT
    A = (pb >= pf + 0.02) and (eb >= ef)
    # (B) LITERAL-BRAIN Φ >= degree-matched RANDOM (topology, not just strength)
    B = (pb >= pr + 0.02)
    # (C) rich-club hub ablation drops Φ by a clear margin (hubs load-bearing)
    C = (pa <= pb - 0.05)
    # (D) A/G lateralization load-bearing: lateralized Φ >= hemisphere-blind Φ
    D = (plat >= pbl + 0.02)
    # (E) coord/region shuffle decorrelates: shuffled Φ <= brain Φ (no advantage kept)
    E = (psh <= pb - 0.02)

    npass = sum([A, B, C, D, E])
    if npass == 5:
        verdict = "GREEN"
    elif npass >= 3:
        verdict = "AMBER"
    else:
        verdict = "RED"

    out = dict(
        hypothesis="H_1513_literal_connectome",
        rung="R1_numpy_mirror_DIRECTIONAL",
        connectome="Hagmann/BCT DSI group avg 219x8 (GPLv3) — REAL",
        seeds=SEEDS, nsamp=NSAMP, couple=COUPLE,
        phi=dict(brain=pb, flat=pf, random=pr, ablated=pa,
                 lateralized=plat, hemi_blind=pbl, shuffled=psh),
        efficiency=dict(brain=eb, flat=ef, random=er),
        bars=dict(
            A_brain_ge_flat=A, B_brain_ge_random=B, C_richclub_ablation=C,
            D_lateralization=D, E_coord_shuffle=E),
        npass=npass, verdict=verdict,
        per_seed=results,
    )
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
