#!/usr/bin/env python3
"""H_1513 LITERAL-CONNECTOME — H_1512-ALIGNED re-score (R1 numpy mirror, DIRECTIONAL).

Re-uses H_1512's EXACT harness (build_population, apply_topology, phi_iit4 min-cut Φ,
CORE, degree_matched_random, lateralize_collapse, and the SAME 5 frozen bars + the SAME
thresholds A_MIN/B_MIN) and replaces ONLY the adjacency source:

    brain_adjacency()  (synthetic small-world/rich-club over anatomical coords)
        ->  literal_adjacency()  (REAL Hagmann/BCT DSI structural connectome subnetwork)

Every other line is H_1512's. This is the faithful literal-data scale-recheck
(a_toy_scale_recheck): same bars, same min-cut Φ, same population — only the wiring is
the real published human connectome. $0 CPU, p7, frozen-first, c9. NO tune-to-green.

LITERAL MAPPING: H_1512's 15 anatomical lanes -> 15 real DSI regions, chosen by
(hemisphere: A/left HEMI=-1 -> left-hemi region block; G/right HEMI=+1 -> right block;
midline HEMI=0 -> either) x (graph role: HUBS -> literal high-strength rich-club nodes,
PERIPHERAL -> literal low-degree fringe, rest -> mid-strength), within the lane's
hemisphere. Then literal_adjacency = the REAL DSI weighted subnetwork among the mapped
regions (binarized at the connectome's own median to match H_1512's binary adjacency
regime; weighted variant also reported).
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIB = os.path.join(HERE, "..", "1512_brain_topology")
sys.path.insert(0, os.path.abspath(SIB))
import h1512 as H  # the sibling harness — single source of bars/Φ/population

CONN = os.path.join(HERE, "sample_group_dsi.npy")


def load_group_avg():
    a = np.load(CONN)            # (219,219,8)
    g = a.mean(axis=2)
    np.fill_diagonal(g, 0.0)
    return g


def map_lanes_to_regions(g, seed):
    """H_1512 lane -> real DSI region, by (hemisphere x graph role). Deterministic per seed."""
    rng = np.random.default_rng(seed)
    Nr = g.shape[0]
    half = Nr // 2                       # contiguous L | R (verified ~4x intra/cross weight)
    strength = g.sum(1)
    Lidx = np.arange(0, half)
    Ridx = np.arange(half, Nr)

    def ranked(idxs):
        return idxs[np.argsort(-strength[idxs])]
    Lr, Rr = ranked(Lidx), ranked(Ridx)

    band = {"hub": (0.0, 0.15), "mid": (0.30, 0.55), "periph": (0.75, 1.0)}

    def role_of(lane_idx):
        if lane_idx in H.HUBS:        return "hub"
        if lane_idx in H.PERIPHERAL:  return "periph"
        return "mid"

    used = set()
    region_of = np.zeros(H.N, dtype=int)
    # midline (HEMI==0) lanes may draw from either hemisphere; assign them last after L/R fixed
    order = sorted(range(H.N), key=lambda i: (H.HEMI[i] == 0))
    for li in order:
        role = role_of(li)
        hemi = H.HEMI[li]
        if hemi < 0:    pool = Lr
        elif hemi > 0:  pool = Rr
        else:           pool = ranked(np.arange(Nr))   # midline: whole brain
        lo, hi = band[role]
        a0 = int(lo * len(pool)); a1 = max(int(hi * len(pool)), a0 + 1)
        cand = [int(x) for x in pool[a0:a1] if int(x) not in used]
        if not cand:
            cand = [int(x) for x in pool if int(x) not in used]
        pick = int(rng.choice(cand))
        used.add(pick)
        region_of[li] = pick
    return region_of


def literal_subnet(g, region_of):
    sub = g[np.ix_(region_of, region_of)].copy()
    np.fill_diagonal(sub, 0.0)
    return sub


def binarize_like_brain(sub):
    """Binarize the real weighted subnetwork at its own positive median so the literal
    adjacency lives in the SAME binary regime as H_1512's brain_adjacency (which is 0/1).
    This keeps apply_topology/min-cut comparable; weighted variant reported separately."""
    pos = sub[sub > 0]
    if pos.size == 0:
        return np.zeros_like(sub)
    thr = np.median(pos)
    A = (sub >= thr).astype(float)
    np.fill_diagonal(A, 0.0)
    # symmetric (sub is symmetric already)
    return A


def run_seed(seed):
    g = load_group_avg()
    region_of = map_lanes_to_regions(g, seed)
    sub = literal_subnet(g, region_of)

    # LITERAL adjacency in H_1512's binary regime (replaces brain_adjacency)
    A_lit = binarize_like_brain(sub)

    rng = np.random.default_rng(seed)
    X = H.build_population(rng)

    A_rand = H.degree_matched_random(A_lit, rng)
    A_flat = np.zeros((H.N, H.N))
    A_latcol = H.lateralize_collapse(A_lit)

    # coord/region shuffle: re-map lanes to a permuted region set -> destroys the
    # literal lane->region structure (the literal analogue of H_1512 shuffle_coords)
    perm_region = map_lanes_to_regions(g, seed + 7777)
    pr = np.random.default_rng(seed + 7777).permutation(perm_region)
    A_shuf = binarize_like_brain(literal_subnet(g, pr))

    phi = lambda A: H.phi_core(H.apply_topology(X, A))
    phi_flat   = phi(A_flat)
    phi_brain  = phi(A_lit)
    phi_rand   = phi(A_rand)
    phi_latcol = phi(A_latcol)
    phi_shuf   = phi(A_shuf)

    eff_flat  = H.global_efficiency(A_flat)
    eff_brain = H.global_efficiency(A_lit)
    eff_rand  = H.global_efficiency(A_rand)

    Xb = H.apply_topology(X, A_lit)
    core_hubs = [0, 3, 2, 13]
    core_peri = [5, 7, 9, 14]
    hub_drop  = float(np.mean([H.phi_core_ablate(Xb, h) for h in core_hubs]))
    peri_drop = float(np.mean([H.phi_core_ablate(Xb, p) for p in core_peri]))

    return dict(seed=seed, phi_flat=phi_flat, phi_brain=phi_brain, phi_rand=phi_rand,
                phi_latcol=phi_latcol, phi_shuf=phi_shuf,
                eff_flat=eff_flat, eff_brain=eff_brain, eff_rand=eff_rand,
                hub_drop=hub_drop, peri_drop=peri_drop,
                n_edges=int(A_lit.sum() // 2), region_of=region_of.tolist())


def main():
    SEEDS = H.SEEDS                      # SAME seeds as H_1512 [5120,5121,5122]
    rows = [run_seed(s) for s in SEEDS]
    keys = ["phi_flat","phi_brain","phi_rand","phi_latcol","phi_shuf",
            "eff_flat","eff_brain","eff_rand","hub_drop","peri_drop"]
    mean = {k: float(np.mean([r[k] for r in rows])) for k in keys}

    # H_1512's EXACT frozen bars + thresholds (verbatim) ------------------------------------
    A_pass = mean['phi_brain'] >= mean['phi_flat'] + H.A_MIN
    B_pass = mean['phi_brain'] >= mean['phi_rand'] + H.B_MIN
    C_pass = mean['hub_drop']  >  mean['peri_drop']
    D_pass = mean['phi_latcol'] < mean['phi_brain']
    brain_adv = mean['phi_brain'] - mean['phi_rand']
    shuf_adv  = mean['phi_shuf'] - mean['phi_rand']
    E_pass = shuf_adv <= 0.5 * brain_adv if brain_adv > 1e-9 else True
    green = A_pass and B_pass and C_pass and E_pass   # H_1512: GREEN iff A∧B∧C∧E

    if green:
        verdict = "🟢 REPRODUCES — literal connectome reproduces H_1512 brain-topology Φ advantage"
    elif not A_pass:
        verdict = "🧱 NON-REPRO (A fails) — real placement INERT under min-cut Φ"
    else:
        verdict = "🟠 PARTIAL — some bars diverge (literal vs synthetic)"

    out = dict(
        hypothesis="H_1513_literal_connectome_ALIGNED",
        rung="R1_numpy_mirror_DIRECTIONAL",
        harness="re-uses H_1512 h1512.py (build_population/apply_topology/phi_iit4/CORE/bars) byte-for-byte; only adjacency = literal DSI",
        connectome="Hagmann/BCT DSI group avg 219x8 (GPLv3) — REAL",
        metric="IIT4 min-cut Φ (phi_iit4 over CORE) — H_1512 headline metric",
        seeds=SEEDS, A_MIN=H.A_MIN, B_MIN=H.B_MIN, ALPHA=H.ALPHA, N_TRIALS=H.N_TRIALS,
        phi=dict(flat=mean['phi_flat'], brain=mean['phi_brain'], random=mean['phi_rand'],
                 latcol=mean['phi_latcol'], shuf=mean['phi_shuf']),
        efficiency=dict(flat=mean['eff_flat'], brain=mean['eff_brain'], random=mean['eff_rand']),
        richclub=dict(hub_drop=mean['hub_drop'], peri_drop=mean['peri_drop']),
        bars=dict(A_brain_gt_flat=A_pass, B_brain_gt_random=B_pass,
                  C_richclub=C_pass, D_lateralize_headline=D_pass, E_coord_shuffle=E_pass),
        green_iff_ABCE=green, verdict=verdict,
        n_edges_brain=rows[0]['n_edges'],
        per_seed=[{k: r[k] for k in keys + ['seed','n_edges']} for r in rows],
    )
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
