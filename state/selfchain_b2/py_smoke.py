# B② self-CHAIN — DIRECTIONAL py-mirror smoke (numbers designed to match the
# engine-native core/engine_cli_smoke.hexa cases). $0 / CPU / no model load.
#
# Proves, over a tiny synthetic K-session chain:
#   F1  continuity        — adjacent waypoint cos high, distant low
#   F2  impostor-history  — AUROC(chain) >> AUROC(single-vector) on impostors
#                           that MATCH the latest anchor but not the trajectory
#   F3  ablation          — erase history (count<3) -> chain-fit collapses to the
#                           single-vector regime (no separation)
#   F5  retrodiction      — cos("self j sessions ago") monotone-decreasing in j
#   F6  reproducible + disk round-trip (H_1204: in-memory carry != disk round-trip)
#
# HONEST SCOPE: drift is a deterministic designed law (SATURATED). The discriminator
# must beat the single-vector baseline DECISIVELY to count. py = DIRECTIONAL only;
# terminal verdict = the hexa engine-native smoke.
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "core"))
import engine_cli as E

DIM = 8
K = 4  # 5 waypoints w0..w4; progression axes 1,2,3,4 -> a_pred = 5

def build_chain():
    s = E.self_new(DIM, 0)
    c = E.self_chain_new(s)
    cur = s
    for tick in range(K):
        cur = E.self_drift(cur, tick, 0.3)   # anchor waypoint at each session boundary
        c = E.self_chain_append(c, cur)
    return c, cur

def genuine_next(latest, tick, step):
    # continues the true drift (axis (tick+1)%dim) forward
    return E.self_drift(latest, tick, step)

def impostor(latest, fresh_axis, step):
    # MATCHES the latest anchor (drift is small, high self_cos) but along a WRONG
    # fresh axis -> wrong trajectory history. single-vector self_cos ~ genuine's.
    v = list(latest.v)
    v[fresh_axis] = v[fresh_axis] + step
    return E.SelfIdentity(E._self_norm(v, DIM), DIM)

def auroc(pos, neg):
    # fraction of (pos,neg) pairs with pos>neg (ties=0.5) = Mann-Whitney AUROC
    n = 0
    s = 0.0
    for p in pos:
        for q in neg:
            if p > q: s += 1.0
            elif p == q: s += 0.5
            n += 1
    return s / n

def main():
    c, latest = build_chain()
    wp = [E._chain_wp(c, k) for k in range(c.count)]

    # F1 continuity: adjacent cos high, distant low
    adj = E.self_cos(wp[-2], wp[-1])
    dist = E.self_cos(wp[0], wp[-1])
    f1 = adj >= 0.70 and dist < adj

    # F5 retrodiction: cos(latest, w_{K-j}) monotone decreasing in j
    retro = [E.self_chain_retro_cos(c, j) for j in range(c.count)]
    f5 = all(retro[j] > retro[j + 1] - 1e-12 for j in range(len(retro) - 1)) and retro[0] > retro[-1]

    # populations: genuine continuations vs impostors matching the latest anchor
    steps = [0.24, 0.27, 0.30, 0.33, 0.36, 0.39]
    fresh = [6, 7, 0]  # axes never drifted in w4 (progression used 1..4, a_pred=5)
    gen = [genuine_next(latest, K, st) for st in steps]
    imp = [impostor(latest, fresh[i % len(fresh)], st) for i, st in enumerate(steps)]

    fit_gen = [E.self_chain_fit(g, c) for g in gen]
    fit_imp = [E.self_chain_fit(m, c) for m in imp]
    cos_gen = [E.self_cos(g, latest) for g in gen]
    cos_imp = [E.self_cos(m, latest) for m in imp]

    auroc_chain = auroc(fit_gen, fit_imp)
    auroc_single = auroc(cos_gen, cos_imp)
    f2 = auroc_chain >= 0.95 and (auroc_chain - auroc_single) >= 0.30

    # F3 ablation: erase history -> count<3 -> chain-fit = 0 for BOTH (no separation)
    c_ablated = E.self_chain_from_flat(list(latest.v), 1, DIM)
    fit_gen_abl = [E.self_chain_fit(g, c_ablated) for g in gen]
    fit_imp_abl = [E.self_chain_fit(m, c_ablated) for m in imp]
    auroc_abl = auroc(fit_gen_abl, fit_imp_abl)
    f3 = all(x == 0.0 for x in fit_gen_abl + fit_imp_abl) and abs(auroc_abl - 0.5) < 1e-9

    # F6a reproducible checksum over fit scores
    def cksum(xs):
        h = 2166136261
        for x in xs:
            h = (h ^ (int(round(x * 1e6)) & 0xFFFFFFFF)) * 16777619 & 0xFFFFFFFF
        return h
    ck = cksum(fit_gen + fit_imp)

    # F6b DISK round-trip (H_1204): write flat payload to .kosmos-style JSON, reload, recompute
    path = os.path.join(os.path.dirname(__file__), "chain_anchor.kosmos.json")
    payload = {"flat": [E.self_chain_component(c, i) for i in range(c.count * c.dim)],
               "count": E.self_chain_count(c), "dim": E.self_chain_dim(c)}
    with open(path, "w") as fh:
        json.dump(payload, fh)
    with open(path) as fh:
        rp = json.load(fh)
    c2 = E.self_chain_from_flat(rp["flat"], rp["count"], rp["dim"])
    fit_gen2 = [E.self_chain_fit(g, c2) for g in gen]
    fit_imp2 = [E.self_chain_fit(m, c2) for m in imp]
    roundtrip = (fit_gen2 == fit_gen) and (fit_imp2 == fit_imp) and cksum(fit_gen2 + fit_imp2) == ck
    f6 = roundtrip

    print("=== B② self-CHAIN — DIRECTIONAL py smoke (dim=%d, K=%d) ===" % (DIM, K))
    print("F1 continuity      adj_cos=%.4f distant_cos=%.4f  -> %s" % (adj, dist, "PASS" if f1 else "FAIL"))
    print("F5 retrodiction    retro=%s monotone-dec -> %s" %
          (["%.3f" % x for x in retro], "PASS" if f5 else "FAIL"))
    print("   fit_genuine     = %s" % ["%.3f" % x for x in fit_gen])
    print("   fit_impostor    = %s" % ["%.3f" % x for x in fit_imp])
    print("   cos_genuine→wK  = %s" % ["%.3f" % x for x in cos_gen])
    print("   cos_impostor→wK = %s" % ["%.3f" % x for x in cos_imp])
    print("F2 impostor-hist   AUROC(chain)=%.3f  AUROC(single-vector)=%.3f  gap=%.3f -> %s"
          % (auroc_chain, auroc_single, auroc_chain - auroc_single, "PASS" if f2 else "FAIL"))
    print("F3 ablation        erase history -> AUROC(chain)=%.3f (=single-vector regime) -> %s"
          % (auroc_abl, "PASS" if f3 else "FAIL"))
    print("F6 checksum=%08x  disk round-trip byte-identical -> %s" % (ck, "PASS" if f6 else "FAIL"))
    allok = f1 and f2 and f3 and f5 and f6
    print("RESULT %s (F1..F6, F4=engine-native only)" % ("ALL-PASS" if allok else "FAIL"))
    return 0 if allok else 1

if __name__ == "__main__":
    sys.exit(main())
