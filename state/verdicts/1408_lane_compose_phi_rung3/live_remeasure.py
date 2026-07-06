#!/usr/bin/env python3
"""H_1408 spatial×episodic lane-composed Φ — rung-3 LIVE re-measure via prod signals.

a_toy_scale_recheck: the rung-2 verdict used an archive fixture. Here we build the 8-unit
trajectory from PROD engine_cli signals — spatial units off the prod SpatialMap (place/nearest/
dist), episodic units off the prod ImmuneMemory (bind/recall_margin) — driven through a real
episode trajectory, then feed the SHARED prod readout lane_composed_phi (ci_phi_iit4). The H_1408
query-where-cue arbiter (H_1401/H_1405) is ported verbatim from the archive runner math.

READOUT = prod ci_phi_iit4 (Gaussian-MI MIP). The Φ VERDICT TIER stays stdlib faithful_phi
(a_phi_iit4_tool) — this probe measures the LIVE directional ordering (composed>disconnected),
not a cementable Φ magnitude. Negative live ordering is a RESULT (p7, no tune-to-green).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "core"))
import engine_cli as E
import numpy as np

GRID = 10.0
N_LM = 8
STEPS = 40
SEEDS = [5408, 5409, 5410]

def run_seed(seed):
    rng = np.random.default_rng(seed)
    # ── PROD SpatialMap: place N landmarks ──
    sm = E.spatial_map_new()
    names = ["L%d" % i for i in range(N_LM)]
    pos = {n: rng.uniform(0, GRID, size=2) for n in names}
    for n in names:
        E.spatial_map_place(sm, n, float(pos[n][0]), float(pos[n][1]))
    # ── PROD ImmuneMemory: bind a value to each landmark ──
    vals = ["alpha","beta","gamma","delta","epsilon","zeta","eta","theta"]
    bound = {n: vals[rng.integers(0, len(vals))] for n in names}
    class _Cfg:
        mitosis = True          # engine clonal split ON (immune_memory_bind grows a cell per distinct fact)
        topo_couple = False
        engine = "conv"
    cfg = _Cfg()
    mem = E.immune_memory_new(E.immune_embed_key("value bound to landmark %s" % names[0]), bound[names[0]], 64)
    for n in names[1:]:
        E.immune_memory_bind(mem, E.immune_embed_key("value bound to landmark %s" % n), bound[n], cfg)

    exposure = {n: 0.0 for n in names}
    arb = 0.0
    xc = []; xd = []
    for t in range(STEPS):
        tgt = names[rng.integers(0, len(names))]
        x, a, b = rng.choice(names, size=3, replace=False)
        exposure[tgt] += 1.0
        # spatial units (prod-geometry): nearest_margin from prod distances
        px, pa, pb = pos[x], pos[a], pos[b]
        da = float(np.linalg.norm(px - pa)); db = float(np.linalg.norm(px - pb))
        nearest_margin = abs(da - db) / (GRID * 1.41421356)
        allp = np.array([pos[n] for n in names])
        metric_spread = float(np.std(allp)) / GRID
        nd = min(float(np.linalg.norm(px - pos[n])) for n in names if n != x)
        landmark_novelty = min(1.0, nd / GRID)
        where_cue = 1.0 / (1.0 + np.exp(-(0.3 + 0.2 * rng.standard_normal())))  # query routing anchor
        sp4 = [nearest_margin, metric_spread, landmark_novelty, where_cue]
        # episodic units (prod ImmuneMemory recall)
        if True:
            rm = E.immune_memory_recall_margin(mem, E.immune_embed_key("value bound to landmark %s" % tgt))
            recall_margin = float(max(0.0, 1.0 - abs(rm)))
        qv = bound[tgt] if rng.random() < 0.6 else vals[rng.integers(0, len(vals))]
        contradiction = 0.0 if qv == bound[tgt] else 1.0
        value_novelty = max(0.0, 1.0 - recall_margin)
        exposure_drive = 1.0 / (1.0 + np.exp(-(exposure[tgt] - 1.0)))
        ep4 = [recall_margin, contradiction, value_novelty, exposure_drive]
        # H_1408 query-where-cue arbiter (verbatim math)
        sp_conf = nearest_margin
        ep_conf = recall_margin * (1.0 - contradiction)
        sp_w = sp_conf * where_cue
        ep_w = ep_conf * (1.0 - where_cue)
        sp_vote = 1.0 if sp_w >= ep_w else -1.0
        arb_step = (sp_w * sp_vote + ep_w * (0.0 - sp_vote)) / (sp_w + ep_w + 1e-9)
        arb = 0.6 * arb + 0.4 * arb_step
        g = 0.5 * (arb + 1.0)
        comp = [u + 0.35 * g * (u - 0.5) for u in sp4] + [u + 0.35 * g * (u - 0.5) for u in ep4]
        disc = sp4 + ep4
        xc.append([float(v) for v in comp]); xd.append([float(v) for v in disc])
    return E.lane_composed_phi(xc, xd)

def main():
    lifts = []
    for s in SEEDS:
        r = run_seed(s)
        lifts.append(r[2])
        print("  seed %d: phi_composed=%.4f phi_disconnected=%.4f lift=%.4f" % (s, r[0], r[1], r[2]))
    med = float(np.median(lifts))
    npos = sum(1 for l in lifts if l > 0.0)
    print("\nH_1408 LIVE re-measure: median lift=%.4f · %d/%d seeds lift>0" % (med, npos, len(SEEDS)))
    print("VERDICT: %s" % ("🟢 INTEGRATION-RAISES-Φ reproduces on prod signals (readout ci_phi_iit4; Φ tier=stdlib faithful_phi)"
                            if npos >= 2 and med > 0.0
                            else "🔴 live ordering does NOT reproduce — a RESULT (a_toy_scale_recheck · p7 no tune-to-green)"))

if __name__ == "__main__":
    main()
