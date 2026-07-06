#!/usr/bin/env python3
"""H_1404 affect×ethics lane-composed Φ — rung-3 LIVE re-measure via prod signals.

Upgrades the H_1404 STAGE-1 (fixture-equivalent) to a live measurement: the affect 4 units come
from the prod affect_substrate_features read off a real prod ImmuneMemory store, ethics 4 units
from the prod ethics_units, arbiter-coupled via the prod lane_compose_step — fed to the SHARED
prod readout lane_composed_phi (ci_phi_iit4). H_1407/1408 pattern. READOUT=ci_phi_iit4; Φ VERDICT
tier=stdlib faithful_phi (a_phi_iit4_tool). Negative live ordering is a RESULT (p7).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "core"))
import engine_cli as E
import numpy as np

STEPS = 40
SEEDS = [1404, 1405, 1406]

def run_seed(seed):
    rng = np.random.default_rng(seed)
    class _Cfg:
        mitosis = True; topo_couple = False; engine = "conv"
    cfg = _Cfg()
    subjs = ["ana","ben","cyd","dan","eli","fia","gus","hye"]
    cities = ["seoul","tokyo","paris","lima","cairo","oslo","accra","quito"]
    facts = {s: cities[rng.integers(0, len(cities))] for s in subjs}
    # prod ImmuneMemoryGrow store (affect reads .protos/.last_used/.split_thr off this)
    mem = E.immune_grow_new(E.immune_embed_key("%s lives in" % subjs[0]), facts[subjs[0]], 8, 16, True)
    for s in subjs[1:]:
        mem = E.immune_grow_bind(mem, E.immune_embed_key("%s lives in" % s), facts[s], cfg)
    exposure = {s: 0.0 for s in subjs}
    arb = 0.0
    xc = []; xd = []
    for t in range(STEPS):
        s = subjs[rng.integers(0, len(subjs))]
        exposure[s] += 1.0
        qa = facts[s] if rng.random() < 0.6 else cities[rng.integers(0, len(cities))]
        # prod affect features off the LIVE immune store
        af = E.affect_substrate_features(mem, E.immune_embed_key("%s lives in" % s), qa)
        row = E.lane_compose_step(af, exposure[s], arb)   # prod affect+ethics arbiter step
        xc.append([float(v) for v in row[0]])
        xd.append([float(v) for v in row[1]])
        arb = row[2]
    return E.lane_composed_phi(xc, xd)

def main():
    lifts = []
    for s in SEEDS:
        r = run_seed(s)
        lifts.append(r[2])
        print("  seed %d: phi_composed=%.4f phi_disconnected=%.4f lift=%.4f" % (s, r[0], r[1], r[2]))
    med = float(np.median(lifts))
    npos = sum(1 for l in lifts if l > 0.0)
    print("\nH_1404 LIVE re-measure: median lift=%.4f · %d/%d seeds lift>0" % (med, npos, len(SEEDS)))
    print("VERDICT: %s" % ("🟢 INTEGRATION-RAISES-Φ reproduces on prod signals (readout ci_phi_iit4; Φ tier=stdlib faithful_phi)"
                            if npos >= 2 and med > 0.0
                            else "🔴 live ordering does NOT reproduce — a RESULT (a_toy_scale_recheck · p7 no tune-to-green)"))

if __name__ == "__main__":
    main()
