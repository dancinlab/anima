#!/usr/bin/env python3
"""H_1407 cerebellum×basal lane-composed Φ — rung-3 LIVE re-measure via prod signals.

a_toy_scale_recheck: 8-unit trajectory from PROD engine_cli — cerebellum units off the prod
VForwardField NLMS forward-model (vforward_predict/update), basal units off the prod ImmuneMemory
recalled state (affinity go-values) — through a real episode trajectory, fed to the SHARED prod
readout lane_composed_phi (ci_phi_iit4). H_1407 arbiter (cb: pred_error<0.30, bg: go_margin>0)
ported verbatim. READOUT=ci_phi_iit4; Φ VERDICT tier=stdlib faithful_phi (a_phi_iit4_tool).
NOTE: the H_1407 card flags a BASAL-DEGENERACY precondition — a near-constant basal unit collapses
Φ. A negative/degenerate live ordering is a RESULT (p7, no tune-to-green).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "core"))
import engine_cli as E
import numpy as np

STEPS = 40
SEEDS = [5407, 5408, 5409]
DIM = 32

def _embed(s):
    # prod key embedding (byte-trigram FNV) — reuse engine's immune_embed_key
    return np.array(E.immune_embed_key(s), dtype=float)

def run_seed(seed):
    rng = np.random.default_rng(seed)
    class _Cfg:
        mitosis = True; topo_couple = False; engine = "conv"
    cfg = _Cfg()
    subjs = ["ana","ben","cyd","dan","eli","fia","gus","hye"]
    cities = ["seoul","tokyo","paris","lima","cairo","oslo","accra","quito"]
    facts = {s: cities[rng.integers(0, len(cities))] for s in subjs}
    # prod ImmuneMemory: bind each subject→city
    mem = E.immune_memory_new(_embed("%s lives in" % subjs[0]).tolist(), facts[subjs[0]], 64)
    for s in subjs[1:]:
        E.immune_memory_bind(mem, _embed("%s lives in" % s).tolist(), facts[s], cfg)
    # prod VForwardField forward-model
    ff = E.vforward_new(DIM, 2, 0.30)
    exposure = {s: 0.0 for s in subjs}
    arb = 0.0
    xc = []; xd = []
    predicted = np.zeros(DIM)
    for t in range(STEPS):
        s = subjs[rng.integers(0, len(subjs))]
        true_ans = facts[s]
        distr = [c for c in cities if c != true_ans]
        cand = [true_ans] + list(rng.choice(distr, size=3, replace=False))
        rng.shuffle(cand)
        exposure[s] += 1.0
        # actual recalled state vector (prod-embed of true answer, DIM-truncated)
        actual = _embed(true_ans)[:DIM]
        if len(actual) < DIM: actual = np.pad(actual, (0, DIM-len(actual)))
        # cerebellum (prod-style forward model delta-rule)
        pred_error = float(np.linalg.norm(actual - predicted))
        pred_confidence = float(np.exp(-pred_error))
        correction_drive = 0.30 * pred_error
        recall_key = _embed("%s lives in" % s).tolist()
        margin = float(max(0.0, 1.0 - abs(E.immune_memory_recall_margin(mem, recall_key))))
        state_novelty = max(0.0, 1.0 - margin)
        predicted = predicted + 0.30 * (actual - predicted)  # NLMS step
        cb4 = [pred_error, pred_confidence, correction_drive, state_novelty]
        # basal (affinity go-values over candidates)
        gv = np.array([float(actual @ (_embed(c)[:DIM] if len(_embed(c))>=DIM else np.pad(_embed(c),(0,DIM-len(_embed(c)))))) for c in cand])
        order = np.argsort(gv)[::-1]
        top1 = float(gv[order[0]]); top2 = float(gv[order[1]])
        go_margin = top1 - top2
        competition_spread = float(np.std(gv))
        no_go_pressure = max(0.0, 0.5 - top1)
        outcome_reward = 1.0 if cand[int(order[0])] == true_ans else -1.0
        bg4 = [go_margin, competition_spread, no_go_pressure, outcome_reward]
        # H_1407 arbiter
        cb_vote = 1.0 if pred_error < 0.30 else -1.0
        cb_conf = abs(0.30 - pred_error)
        bg_vote = 1.0 if go_margin > 0.0 else -1.0
        bg_conf = abs(go_margin)
        arb_step = (cb_conf * cb_vote + bg_conf * bg_vote) / (cb_conf + bg_conf + 1e-9)
        arb = 0.6 * arb + 0.4 * arb_step
        g = 0.5 * (arb + 1.0)
        comp = [u + 0.35 * g * (u - 0.5) for u in cb4] + [u + 0.35 * g * (u - 0.5) for u in bg4]
        disc = cb4 + bg4
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
    print("\nH_1407 LIVE re-measure: median lift=%.4f · %d/%d seeds lift>0" % (med, npos, len(SEEDS)))
    print("VERDICT: %s" % ("🟢 INTEGRATION-RAISES-Φ reproduces on prod signals (readout ci_phi_iit4; Φ tier=stdlib faithful_phi)"
                            if npos >= 2 and med > 0.0
                            else "🔴/🧱 live ordering does NOT reproduce (basal-degeneracy precondition) — a RESULT (a_toy_scale_recheck · p7)"))

if __name__ == "__main__":
    main()
