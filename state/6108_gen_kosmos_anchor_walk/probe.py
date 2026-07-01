# H_6108 — 생성 = .kosmos 앵커 walk  (numpy DIRECTIONAL screen, transfer-UNVERIFIED)
# Mechanism: output = path through anchor space; recombination = the NEW interpolation
#            anchor that a geodesic between two DISTANT anchors passes through.
#
# Task (2-concept INDEPENDENT recombination, the G1 shape):
#   d-dim feature space. Each stored concept activates an INDEPENDENT random feature-subset.
#   The composed/recombined target of concepts (i,j) = the UNION of their feature sets
#   (a novel concept never stored). We hold out the composition and ask each operator to
#   reconstruct it from only the two single-concept anchors.
#
# Operators compared:
#   ADDITIVE readout (baseline floor)  : a_i + a_j            (superposition)
#   H_6108 geodesic anchor-walk        : (1-t)*a_i + t*a_j at t=0.5  (convex interpolation
#                                        = the "new interpolation anchor" on the geodesic)
# Decode: threshold > 0.5  -> feature ON.  composed_distinct scores a pair as HIT iff
#   decoded set == true UNION  AND  decoded set != a_i's set  AND != a_j's set (genuinely new).
#
# FROZEN BAR (set BEFORE run, p7, no post-hoc move):
#   GREEN-DIRECTIONAL iff  mean composed_distinct(geodesic) >= mean composed_distinct(additive) + 0.15
#   else FALSIFIED / floor.  (numpy => DIRECTIONAL by construction, never terminal.)
import numpy as np

def run(seed):
    rng = np.random.default_rng(seed)
    d = 128            # anchor / feature dim
    K = 40             # stored concepts
    active = 6         # features active per concept (independent random subsets)
    anchors = np.zeros((K, d))
    for i in range(K):
        idx = rng.choice(d, size=active, replace=False)
        anchors[i, idx] = 1.0
    # all distinct held-out pairs whose union is genuinely new (differs from both)
    pairs = []
    for i in range(K):
        for j in range(i+1, K):
            si, sj = set(np.nonzero(anchors[i])[0]), set(np.nonzero(anchors[j])[0])
            union = si | sj
            if union != si and union != sj:   # composition must be novel vs each parent
                pairs.append((i, j))
    def score(combine):
        hit = 0
        for i, j in pairs:
            si, sj = set(np.nonzero(anchors[i])[0]), set(np.nonzero(anchors[j])[0])
            union = si | sj
            out = combine(anchors[i], anchors[j])
            dec = set(np.nonzero(out > 0.5)[0])
            if dec == union and dec != si and dec != sj:
                hit += 1
        return hit / len(pairs)
    add = score(lambda a, b: a + b)
    geo = score(lambda a, b: 0.5*a + 0.5*b)      # geodesic midpoint (H_6108)
    return add, geo, len(pairs)

seeds = [6108, 6109, 6110]
adds, geos = [], []
for s in seeds:
    a, g, npair = run(s)
    adds.append(a); geos.append(g)
    print(f"seed={s}  pairs={npair}  additive_floor={a:.3f}  geodesic(H_6108)={g:.3f}")
ma, mg = float(np.mean(adds)), float(np.mean(geos))
margin = 0.15
print(f"\nMEAN  additive_floor={ma:.3f}  geodesic={mg:.3f}  (frozen margin={margin})")
green = mg >= ma + margin
print(f"lift(geo-add) = {mg-ma:+.3f}")
print(f"VERDICT: {'GREEN-DIRECTIONAL' if green else 'FALSIFIED / floor'}  (numpy => DIRECTIONAL, transfer-UNVERIFIED; cf H_6112 numpy overstates)")
