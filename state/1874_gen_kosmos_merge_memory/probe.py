# H_1874 — kosmos Merge = compositional memory (#40 = #5 anchor-walk + #13 Chomsky Merge)
# DIRECTIONAL numpy probe ($0, terminal-forbidden by a_engine_native_learning).
#
# QUESTION (the ONLY thing this answers): does recursive Merge that PERSISTS each
# labeled parent into a discrete .kosmos anchor store make two INDEPENDENT/DISTANT
# concepts COMPOSABLE at DEPTH (composed_distinct > additive floor) where the walled
# ACTIVATION-superposition operators (TPR H_1466, circconv H_1823, HRR) collapse?
#
# DISTINCTION from walled prior art: H_1466/1816/1823/1834/1819 all put composition
# into a FIXED-DIM ACTIVATION vector -> additive/superposition floor (depth-0,
# substrate-framebreak-g1-combination-operator). H_1874 puts it into a GROWING
# DISCRETE PERSISTENT store (a_substrate_disjoint "분리=보존"): structure is OUT of
# the activation superposition. Same-leaf-multiset trees differ only by GROUPING/ORDER
# (hierarchy) -> a true compositional-memory operator must distinguish them.
#
# ARMS (3): ADDITIVE (sum of leaves; grouping-invariant floor) | HRR (Plate circular-
# convolution recursive bind, the STRONG fixed-dim activation baseline; crosstalk grows
# with depth) | MERGE-PERSIST (H_1874: each Merge -> fresh labeled anchor id in a dict
# = .kosmos; parent references children by id; recovery = persistent structure walk).
#
# FROZEN BAR (set BEFORE run):
#   At depth D=3 (8 leaves), over M=24 distinct same-multiset trees:
#   composed_distinct = # trees UNIQUELY & CORRECTLY recovered.
#   DIRECTIONAL-REACHABLE  iff  MERGE composed_distinct >= HRR + M/2  AND  >= ADDITIVE + M/2.
#   (Expected additive floor ~1: all perms of full leaf set -> identical sum vector.)
#   Honest: if MERGE does NOT clear both by M/2, report FALSIFIED/floor.
import numpy as np

DIM = 64
LEAVES = 8            # independent/distant concept alphabet
M = 24               # distinct same-multiset trees per depth
SEEDS = [7, 42, 4302]
MARGIN = M/2

def rng_unit(rng, n, d):
    v = rng.standard_normal((n, d)); v /= np.linalg.norm(v, axis=1, keepdims=True); return v

def cconv(a, b):  # circular convolution (HRR bind)
    return np.fft.irfft(np.fft.rfft(a) * np.fft.rfft(b), n=DIM)

def ccorr(a, b):  # circular correlation (HRR unbind): ccorr(r, cconv(r,x)) ~= x
    return np.fft.irfft(np.conj(np.fft.rfft(a)) * np.fft.rfft(b), n=DIM)

def balanced_tree_perms(rng):
    # depth-3 balanced binary tree over all 8 leaves; a "composition" = a leaf ORDERING.
    # same multiset {0..7} -> additive sum identical for every ordering.
    base = list(range(LEAVES))
    perms, seen = [], set()
    while len(perms) < M:
        p = tuple(rng.permutation(base))
        if p not in seen:
            seen.add(p); perms.append(list(p))
    return perms

def encode_additive(order, leaf):
    return leaf[order].sum(axis=0)

def encode_hrr(order, leaf, RL, RR):
    # recursive balanced fold: pair -> node = RL#l + RR#r, then fold up
    lvl = [leaf[i] for i in order]
    while len(lvl) > 1:
        nxt = []
        for k in range(0, len(lvl), 2):
            nxt.append(cconv(RL, lvl[k]) + cconv(RR, lvl[k+1]))
        lvl = nxt
    return lvl[0]

def decode_hrr(vec, leaf, RL, RR, depth=3):
    # walk all 2^depth paths (L/R sequences), unbind, cleanup vs leaf codebook
    out = []
    for path in range(2**depth):
        v = vec
        for b in range(depth):
            role = RR if (path >> (depth-1-b)) & 1 else RL
            v = ccorr(role, v)
        sims = leaf @ v / (np.linalg.norm(leaf, axis=1)*np.linalg.norm(v)+1e-9)
        out.append(int(np.argmax(sims)))
    return out

# MERGE-PERSIST: build discrete anchor dict; recovery walks stored structure (exact)
def encode_merge(order, leaf):
    store = {}; nid = [LEAVES]
    def leaf_id(i): return i
    ids = [leaf_id(i) for i in order]
    while len(ids) > 1:
        nxt = []
        for k in range(0, len(ids), 2):
            a, b = ids[k], ids[k+1]
            new = nid[0]; nid[0]+=1
            store[new] = (a, b)          # persistent labeled parent anchor
            nxt.append(new)
        ids = nxt
    return ids[0], store
def decode_merge(root, store):
    def walk(x):
        if x < LEAVES: return [x]
        a,b = store[x]; return walk(a)+walk(b)
    return walk(root)

def run_seed(s):
    rng = np.random.default_rng(s)
    leaf = rng_unit(rng, LEAVES, DIM)
    RL, RR = rng_unit(rng, 1, DIM)[0], rng_unit(rng, 1, DIM)[0]
    trees = balanced_tree_perms(rng)
    res = {}
    for name in ("ADDITIVE","HRR","MERGE"):
        recs = []
        for order in trees:
            if name=="ADDITIVE":
                # additive has NO structure to decode; best it can do = the sum vector itself.
                # recovered "structure" = a canonical sort of the multiset (order lost).
                recs.append(tuple(sorted(order)))
            elif name=="HRR":
                v = encode_hrr(order, leaf, RL, RR)
                recs.append(tuple(decode_hrr(v, leaf, RL, RR, 3)))
            else:
                root, store = encode_merge(order, leaf)
                recs.append(tuple(decode_merge(root, store)))
        # composed_distinct = # trees recovered CORRECTLY (==true order) AND uniquely
        from collections import Counter
        cnt = Counter(recs)
        correct_unique = sum(1 for order, r in zip(trees, recs)
                             if r == tuple(order) and cnt[r]==1)
        exact = sum(1 for order, r in zip(trees, recs) if r==tuple(order))
        res[name] = (correct_unique, exact)
    return res

def main():
    agg = {"ADDITIVE":[], "HRR":[], "MERGE":[]}
    for s in SEEDS:
        r = run_seed(s)
        print(f"seed {s}: " + " | ".join(f"{k} distinct={v[0]:2d} exact={v[1]:2d}" for k,v in r.items()))
        for k in agg: agg[k].append(r[k][0])
    m = {k: float(np.mean(v)) for k,v in agg.items()}
    print(f"\nMEAN composed_distinct (of M={M}): "
          f"ADDITIVE={m['ADDITIVE']:.2f}  HRR={m['HRR']:.2f}  MERGE={m['MERGE']:.2f}")
    print(f"FROZEN BAR: MERGE >= HRR+{MARGIN:.0f} AND MERGE >= ADDITIVE+{MARGIN:.0f}")
    ok = (m['MERGE'] >= m['HRR']+MARGIN) and (m['MERGE'] >= m['ADDITIVE']+MARGIN)
    print("VERDICT:", "DIRECTIONAL-REACHABLE (persistent Merge composable at depth-3 where "
          "additive+HRR activation collapse)" if ok else "FLOOR / FALSIFIED")
    print("SCOPE: DIRECTIONAL numpy; MERGE is STORAGE-side compositional memory, does NOT "
          "test mouth-decode G1 recomb-objective (H_1602). by-construction caveat noted.")

if __name__ == "__main__":
    main()
