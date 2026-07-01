# H_6122 — Mouth 제거 -> retrieval-composition  (numpy DIRECTIONAL screen)
# MECHANISM: generation = search .kosmos anchor pool for tension-matched anchors and ASSEMBLE;
#            trunk emits only a combination index (which anchors + order), NOT the content.
#
# CONTRAST vs walled family:
#   - additive-readout baseline = the WALLED operator class (H_1816/1823/1834): a single
#     parametric readout blends two independent concept vectors additively -> interference,
#     dominant concept wins -> composed output collapses toward 1 distinct feature.
#   - H_6122 operator = trunk picks TWO anchor indices (one per tension component) from a
#     non-parametric pool, then assembles the retrieved *text* -> both features survive.
#
# Concepts are INDEPENDENT (color-axis  _|_  shape-axis). Pool stores SINGLE-concept anchors
# only; "red circle" was NEVER stored together (novel composition = G1 recombination target).
#
# FROZEN BAR (declared BEFORE run):
#   metric = composed_distinct = # of the 2 target features (1 color + 1 shape) present in output,
#            averaged over all novel (color,shape) query pairs, mean over 5 seeds.
#   GREEN-DIRECTIONAL iff  retrieval_composed >= 1.5  AND  retrieval - additive >= 0.5 (margin).
#   Else FALSIFIED/floor.
# Also report a DEEP-BIND probe: a fused interaction token that was never stored -> retrieval
#   CANNOT synthesize it (juxtaposition != deep bind). Honest scope, not part of the pass bar.
import numpy as np

D = 64
COLORS = ["red","blue","green"]      # concept axis A
SHAPES = ["circle","square","tri"]   # concept axis B  (independent of A)

def seeded(seed):
    rng = np.random.default_rng(seed)
    # independent random unit codes for each atomic feature
    code = {}
    for w in COLORS+SHAPES:
        v = rng.standard_normal(D); v /= np.linalg.norm(v); code[w]=v
    # ---- anchor pool: ONE anchor per single feature (non-parametric store). text = the word.
    pool = [(w, code[w], w) for w in COLORS+SHAPES]   # (feature, tension-vec, text)
    return rng, code, pool

def additive_readout(code, pool, c, s):
    # WALLED class: blend the two request vectors, decode through a single shared readout that
    # emits the K nearest pool features to the blended vector. Additive blend of two independent
    # unit vectors -> a vector whose nearest neighbors are dominated by whichever is closer; the
    # single readout emits ONE assembled string.
    q = (code[c] + code[s]); q /= np.linalg.norm(q)
    sims = np.array([q @ v for (_,v,_) in pool])
    top = int(np.argmax(sims))                      # single-slot parametric readout
    out = pool[top][2]
    feats = set(out.split())
    return len(feats & {c,s})

def retrieval_composition(code, pool, c, s):
    # H_6122: trunk emits a COMBINATION INDEX = (argmax match to color-tension, argmax match to
    # shape-tension) -> retrieve BOTH anchors -> ASSEMBLE (concatenate retrieved text).
    def pick(req):
        sims = np.array([req @ v for (_,v,_) in pool])
        return pool[int(np.argmax(sims))][2]
    a = pick(code[c]); b = pick(code[s])
    out = a + " " + b                               # assembly of retrieved anchor text
    feats = set(out.split())
    return len(feats & {c,s})

def deep_bind_reachable(pool, c, s):
    # a fused interaction token "c|s" that requires genuine binding was NEVER stored -> retrieval
    # of separate anchors can never synthesize it. Returns 1 iff such a fused token exists in pool.
    texts = {t for (_,_,t) in pool}
    return 1 if f"{c}|{s}" in texts else 0

def run():
    add_scores, ret_scores, deep_scores = [], [], []
    for seed in [7,11,23,42,101]:
        rng, code, pool = seeded(seed)
        a_s=[]; r_s=[]; d_s=[]
        for c in COLORS:
            for s in SHAPES:                        # every (color,shape) = novel, never co-stored
                a_s.append(additive_readout(code,pool,c,s))
                r_s.append(retrieval_composition(code,pool,c,s))
                d_s.append(deep_bind_reachable(pool,c,s))
        add_scores.append(np.mean(a_s)); ret_scores.append(np.mean(r_s)); deep_scores.append(np.mean(d_s))
    add=float(np.mean(add_scores)); ret=float(np.mean(ret_scores)); deep=float(np.mean(deep_scores))
    print(f"[H_6122 retrieval-composition numpy DIRECTIONAL screen]  D={D}, 9 novel pairs x 5 seeds")
    print(f"  additive-readout (WALLED class) composed_distinct = {add:.3f}  (floor)")
    print(f"  retrieval-composition            composed_distinct = {ret:.3f}")
    print(f"  margin (ret - additive)                             = {ret-add:.3f}")
    print(f"  deep-bind fused-token reachable (honest scope)      = {deep:.3f}  (0 = cannot synthesize novel interaction)")
    bar_ret, bar_margin = 1.5, 0.5
    green = (ret >= bar_ret) and (ret-add >= bar_margin)
    print(f"  FROZEN BAR: ret>={bar_ret} AND margin>={bar_margin}")
    print(f"  VERDICT: {'GREEN-DIRECTIONAL (numpy, transfer-UNVERIFIED)' if green else 'FALSIFIED/floor'}")

if __name__=='__main__':
    run()
