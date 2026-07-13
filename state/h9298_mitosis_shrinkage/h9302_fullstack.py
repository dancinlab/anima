#!/usr/bin/env python3
"""H_9301 — MITOSIS GROWTH-BREAK: is the division ceiling capacity, or a degenerate-split defect?: is the mitosis division genealogy itself the statistical
inheritance structure? (p8-native generalization of the H_9298 GREEN)

H_9298 proved: shrink a child distribution toward its parent and the partition cost vanishes
(2.61186 -> 2.45205). But MITOSIS ALREADY HAS a parent/child structure -- the division lineage.
Every experiment so far built the partition with it and then THREW IT AWAY (flat leaves only).

Here the lineage IS the backoff chain:
    P_node = l*MLE_node + (1-l)*P_parent(node),   l = n/(n+T)  (Witten-Bell, zero free hypers)
    internal node statistics = the TRAIN counts of its whole subtree
    root backs off to uniform.

ARMS (identical partition / identical cells / identical WB formula -- only the backoff path differs):
  A1    P(next | leaf)                     -- the jamo floor (flat leaf-MLE + Laplace)  [CALIB 2.51335]
  FLAT  leaf -> ROOT directly              -- intermediate ancestors SKIPPED (pure shrinkage amount)
  LIN   leaf -> parent -> ... -> root      -- THE LEVER (lineage used)
  SHUF  LIN with the genealogy REWIRED     -- same depth, same shrinkage amount, wrong ancestors
        (the decisive control: if LIN only beats FLAT it could just be "more shrinkage";
         it must ALSO beat SHUF for the win to be attributable to the LINEAGE.)

Frozen bars (FREEZE_H9299.txt): GREEN iff L1 (LIN-FLAT <= -0.02) AND L2 (LIN-SHUF <= -0.02, 3/3).
"LIN <= A1" is NOT evidence (H_9298 already broke A1 with shrinkage) -> diagnostic only.
Headline bars are read ONLY at the matched cell count (11, same as H_9298). The grow_max sweep is
a pre-registered DIAGNOSTIC (prediction P1: LIN non-increasing in cells; FLAT/A1 degrade) and
picking its best point for the verdict is forbidden.
"""
import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

try:
    import torch
except Exception as exc:
    print("FATAL: torch import failed:", exc); sys.exit(1)

LAPLACE = 1.0
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
HANGUL_LO, HANGUL_HI = 44032, 55203
JAMO_FLOOR = 2.51335
RAW_CEILING = 2.95342
KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
L1_BAR = -0.02
L2_BAR = -0.02


def log(*a):
    print(*a, flush=True)


# ---- symbol / depth / vocab (verbatim H_1316 port) -----------------------------------------
def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch):
                jset.add(ord(jc))
    js = sorted(jset)
    return {cp: 256 + i for i, cp in enumerate(js)}, js


def syll_jamo_nbytes(njamo):
    if njamo == 3:
        return [1, 1, 1]
    if njamo == 2:
        return [2, 1]
    if njamo == 1:
        return [3]
    out = [1] * njamo
    out[0] += (3 - njamo) if njamo < 3 else 0
    return out


def make_symbol_stream(text, jamo_to_id):
    syms, nby = [], []
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                syms.append(jamo_to_id[ord(jc)]); nby.append(nb[j])
        else:
            for b in ch.encode("utf-8"):
                syms.append(b); nby.append(1)
    return np.asarray(syms, dtype=np.int64), np.asarray(nby, dtype=np.int64)


def depth_stream(text):
    depth, d = [], 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            for j in range(len(nfd)):
                d = 0 if j == 0 else d + 1
                depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                d = d + 1 if 128 <= b <= 191 else 0
                depth.append(d)
    return np.asarray(depth, dtype=np.int64)


def seed_centers():
    return [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]


def assign_all(centers_t, X_t):
    return torch.argmin(torch.cdist(X_t, centers_t, p=2), dim=1)


def all_heads(Y_t, owner, K, ntr, vj, dev):
    H = torch.full((K, vj), LAPLACE, dtype=torch.float64, device=dev)
    flat = owner[:ntr] * vj + Y_t[:ntr]
    H.view(-1).index_add_(0, flat, torch.ones(flat.shape[0], dtype=torch.float64, device=dev))
    return H / H.sum(dim=1, keepdim=True)


def owned_ce(Y_t, owner, k, ntr, p_row):
    mask = owner[:ntr] == k
    if not mask.any():
        return -1.0
    return -torch.log(p_row[Y_t[:ntr][mask]] + 1e-12).mean().item()


def grow_on_lineage(X_tr, Y_tr, ntr, vj, dev, grow_max, split_thresh=SPLIT_THRESH_CE, min_owned=MIN_OWNED):
    """The H_1306/H_1307 gradient-free split rule VERBATIM, but it now also RECORDS the genealogy.

    Returns (leaf_centers, parent_of_leaf, internal_parent) where the tree is expressed over
    stable node ids: node 0..n-1, leaves are the live cells. Split rule itself is UNCHANGED --
    we only stop throwing the lineage away."""
    # node bookkeeping: centers per node, parent id per node, and which nodes are current leaves
    node_center = [list(c) for c in seed_centers()]
    node_parent = [-1, -1]                     # the two seeds are roots of the forest -> parent = virtual ROOT
    leaves = [0, 1]
    dead = set()                       # cells proven unsplittable (degenerate median) -- H_9301 repair
    while len(leaves) < grow_max:
        ct = torch.tensor([node_center[i] for i in leaves], dtype=torch.float64, device=dev)
        owner = assign_all(ct, X_tr)
        K = len(leaves)
        owntr = owner[:ntr]
        owned_n = torch.bincount(owntr, minlength=K).cpu().numpy()
        Hmat = all_heads(Y_tr, owner, K, ntr, vj, dev)
        local_ce = np.full(K, -1.0)
        for k in range(K):
            if owned_n[k] > 0:
                local_ce[k] = owned_ce(Y_tr, owner, k, ntr, Hmat[k])
        elig = [k for k in range(K) if owned_n[k] >= min_owned and local_ce[k] > split_thresh
                and leaves[k] not in dead]
        if not elig:
            break
        pick, bestce = elig[0], local_ce[elig[0]]
        for k in elig[1:]:
            if local_ce[k] > bestce:
                bestce, pick = local_ce[k], k
        if len(leaves) + 1 > grow_max:
            break
        pts = X_tr[:ntr][owntr == pick]
        if pts.shape[0] == 0:
            dead.add(leaves[pick]); continue
        ax = int(torch.argmax(pts.var(dim=0, unbiased=False)).item())
        col = pts[:, ax]
        m = col.shape[0]
        scol, _ = torch.sort(col)
        med = (scol[m // 2].item() if m % 2 == 1
               else ((scol[m // 2 - 1] + scol[m // 2]) / 2.0).item())
        lo, hi = col <= med, col > med
        if int(lo.sum().item()) == 0 or int(hi.sum().item()) == 0:
            # REPAIR (H_9301): a degenerate median split makes THIS cell unsplittable -- it must not
            # terminate the growth of every OTHER still-eligible cell. Blacklist and continue.
            dead.add(leaves[pick]); continue
        mother = leaves[pick]                                   # <-- the lineage fact we used to discard
        c_lo = pts[lo].mean(dim=0).cpu().numpy().tolist()
        c_hi = pts[hi].mean(dim=0).cpu().numpy().tolist()
        id_lo, id_hi = len(node_center), len(node_center) + 1
        node_center += [c_lo, c_hi]
        node_parent += [mother, mother]
        leaves = [leaves[i] for i in range(len(leaves)) if i != pick] + [id_lo, id_hi]
    return leaves, node_center, node_parent


def score_stream(syms, depth, vj):
    n = len(syms)
    idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    return np.stack([last, second, cdep], axis=1), syms[idx].astype(np.int64), idx


# ---- hierarchical Witten-Bell over an arbitrary ancestor chain ------------------------------
def _leaf_counts(owner_tr, Y_tr, K, vj, dev):
    cnt = torch.zeros((K, vj), dtype=torch.float64, device=dev)
    cnt.view(-1).index_add_(0, owner_tr * vj + Y_tr,
                            torch.ones(Y_tr.shape[0], dtype=torch.float64, device=dev))
    return cnt


def _chain_probs(leaf_cnt, chains, vj, dev):
    """chains[k] = [k, a1, a2, ..., root_ancestor] as LEAF-INDEX SETS: each ancestor is represented
    by the set of leaves in its subtree (that is exactly its TRAIN count support). Returns the
    (K, vj) probability matrix produced by recursive Witten-Bell down each chain."""
    K = leaf_cnt.shape[0]
    P = torch.zeros((K, vj), dtype=torch.float64, device=dev)
    uniform = torch.full((vj,), 1.0 / vj, dtype=torch.float64, device=dev)
    for k in range(K):
        chain = chains[k]
        # walk from the ROOT down to the leaf, shrinking each level toward the level above
        p = uniform
        for leafset in reversed(chain):
            c = leaf_cnt[leafset].sum(dim=0)          # counts of this ancestor's subtree
            n = c.sum()
            T = (c > 0).sum().to(torch.float64)
            lam = n / (n + T + 1e-12)
            mle = c / (n + 1e-12)
            p = lam * mle + (1.0 - lam) * p
        P[k] = p
    return P


def ce_from_P(P, owner_te, Y_te, NB_te):
    p = P[owner_te, Y_te]
    return (-torch.log(p + 1e-12)).sum().item() / float(NB_te.sum())


def build_chains(leaves, node_parent, mode, rng=None):
    """Chain of ancestor LEAF-SETS for each leaf.
       mode 'lin'  : true genealogy (mother, grandmother, ...)
       mode 'flat' : leaf -> ROOT only (all leaves), no intermediate ancestors
       mode 'shuf' : same tree SHAPE/depth, but each leaf's ancestor chain is replaced by another
                     leaf's chain (per-seed permutation) -> shrinkage amount preserved, ancestors wrong."""
    K = len(leaves)
    leaf_pos = {nid: i for i, nid in enumerate(leaves)}
    allleaves = list(range(K))

    def ancestors_of(nid):
        """subtree leaf-index sets of each strict ancestor of node nid, mother-first."""
        out = []
        p = node_parent[nid]
        while p != -1:
            # leaves under p
            sub = []
            for lid in leaves:
                q = lid
                while q != -1:
                    if q == p:
                        sub.append(leaf_pos[lid]); break
                    q = node_parent[q]
            out.append(sub)
            p = node_parent[p]
        return out

    true_chains = []
    for nid in leaves:
        c = [[leaf_pos[nid]]] + ancestors_of(nid) + [allleaves]
        true_chains.append(c)

    if mode == "lin":
        return true_chains
    if mode == "flat":
        return [[[i], allleaves] for i in range(K)]
    if mode == "shuf":
        perm = rng.permutation(K)
        out = []
        for i in range(K):
            donor = true_chains[perm[i]]
            # keep MY leaf at the head (the partition is unchanged), inherit the DONOR's ancestors
            out.append([[i]] + donor[1:])
        return out
    raise ValueError(mode)



def _cond_tables(owner_tr, C_tr, Y_tr, K, ncod, vj, dev):
    key = owner_tr * ncod + C_tr
    cnt = torch.zeros((K * ncod, vj), dtype=torch.float64, device=dev)
    cnt.view(-1).index_add_(0, key * vj + Y_tr,
                            torch.ones(Y_tr.shape[0], dtype=torch.float64, device=dev))
    return cnt, cnt.sum(dim=1), (cnt > 0).sum(dim=1).to(torch.float64)


def ce_coda_wb(owner_tr, C_tr, Y_tr, owner_te, C_te, Y_te, NB_te, K, ncod, vj, dev):
    """coda-conditioned Witten-Bell shrinkage on top of a REPAIRED (uncapped) cell pool."""
    H = all_heads(Y_tr, owner_tr, K, len(Y_tr), vj, dev)
    cnt, n_kc, T_kc = _cond_tables(owner_tr, C_tr, Y_tr, K, ncod, vj, dev)
    kt = owner_te * ncod + C_te
    n_row, T_row = n_kc[kt], T_kc[kt]
    lam = n_row / (n_row + T_row + 1e-12)
    p = lam * (cnt[kt, Y_te] / (n_row + 1e-12)) + (1.0 - lam) * H[owner_te, Y_te]
    return (-torch.log(p + 1e-12)).sum().item() / float(NB_te.sum())


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--cells-sweep", default="11,40,160,320")
    ap.add_argument("--seeds", default="4336,4337,4338")
    ap.add_argument("--out", default="/tmp/h9302_out")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    log(f"=== H_9302 — FULL-STACK (coda x uncapped growth x shrinkage) === device={dev}")

    raw = open(a.corpus, "rb").read()[:30000000]
    sha = hashlib.sha256(raw).hexdigest()
    if sha != KO_SHA:
        log("FATAL: corpus sha mismatch"); sys.exit(2)
    text = raw.decode("utf-8", errors="ignore")
    j2i, js = build_jamo_vocab(text)
    vj = 256 + len(js)

    # prev_coda stream (H_9298 definition, verbatim)
    NO_CODA, NONE_CODA = -1, -2
    syms, nby, pcod, cur = [], [], [], NONE_CODA
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                syms.append(j2i[ord(jc)]); nby.append(nb[j]); pcod.append(cur)
            cur = j2i[ord(nfd[2])] if len(nfd) == 3 else NO_CODA
        else:
            for b in ch.encode("utf-8"):
                syms.append(b); nby.append(1); pcod.append(cur)
    syms = np.asarray(syms, dtype=np.int64); nby = np.asarray(nby, dtype=np.int64)
    pcod = np.asarray(pcod, dtype=np.int64)
    depth = depth_stream(text)
    X, Y, idx = score_stream(syms, depth, vj)
    NB, C = nby[idx], pcod[idx]
    codas = sorted(set(C.tolist())); cmap = {c: i for i, c in enumerate(codas)}
    C = np.asarray([cmap[c] for c in C], dtype=np.int64); ncod = len(codas)

    X, Y, NB, C = X[::a.ko_stride], Y[::a.ko_stride], NB[::a.ko_stride], C[::a.ko_stride]
    n = X.shape[0]; ar = np.arange(n); e, o = (ar % 2 == 0), (ar % 2 == 1)
    Xall = torch.tensor(np.concatenate([X[e], X[o]]), dtype=torch.float64, device=dev)
    Yall = torch.tensor(np.concatenate([Y[e], Y[o]]), dtype=torch.long, device=dev)
    Ctr = C[e]; Cte = C[o]
    Ctr_t = torch.tensor(Ctr, dtype=torch.long, device=dev)
    Cte_t = torch.tensor(Cte, dtype=torch.long, device=dev)
    Yte_t = torch.tensor(Y[o], dtype=torch.long, device=dev)
    NBte_t = torch.tensor(NB[o], dtype=torch.float64, device=dev)
    ntr = int(e.sum())
    seeds = [int(s) for s in a.seeds.split(",")]
    log(f"[split] train={ntr} test={int(o.sum())} Vj={vj} coda={ncod}")

    sweep = {}
    for gmax in [int(g) for g in a.cells_sweep.split(",")]:
        leaves, ctr_, par_ = grow_on_lineage(Xall, Yall, ntr, vj, dev, gmax, 0.0, MIN_OWNED)
        K = len(leaves)
        ct = torch.tensor([ctr_[i] for i in leaves], dtype=torch.float64, device=dev)
        owner = assign_all(ct, Xall)
        otr, ote = owner[:ntr], owner[ntr:]
        Ytr_t = Yall[:ntr]
        a1 = ce_from_P(all_heads(Yall, owner, K, ntr, vj, dev), ote, Yte_t, NBte_t)
        full = ce_coda_wb(otr, Ctr_t, Ytr_t, ote, Cte_t, Yte_t, NBte_t, K, ncod, vj, dev)
        sh = []
        for sd in seeds:
            rng = np.random.default_rng(sd)
            cs_tr = torch.tensor(rng.permutation(Ctr), dtype=torch.long, device=dev)
            cs_te = torch.tensor(rng.permutation(Cte), dtype=torch.long, device=dev)
            sh.append(ce_coda_wb(otr, cs_tr, Ytr_t, ote, cs_te, Yte_t, NBte_t, K, ncod, vj, dev))
        shm = float(np.mean(sh))
        sweep[K] = dict(cells=K, A1=a1, FULL=full, SHUF=shm, per_seed=sh,
                        paired=[full - v for v in sh])
        log(f"[cells={K}] A1={a1:.5f}  FULL(coda+WB)={full:.5f}  coda-shuf={shm:.5f}  "
            f"paired d={full-shm:+.5f}")

    HEAD = 320
    M = sweep.get(HEAD) or sweep[max(sweep)]
    calib = abs(sweep[11]["A1"] - JAMO_FLOOR) <= 1e-4 if 11 in sweep else False
    f1 = M["FULL"] <= 2.43205
    f2 = (M["FULL"] - M["SHUF"] <= -0.02) and all(d < 0 for d in M["paired"])
    if not calib:
        v = "INVALID - 11-cell A1 CALIB FAIL"
    elif f1 and f2:
        v = "GREEN - F1 and F2: growth COMPOUNDS on top of coda+shrinkage."
    elif M["FULL"] >= 2.45205:
        v = "KILL/NO-COMPOUND - growth adds nothing on top of the 11-cell coda head (same information)."
    else:
        v = "DIRECTIONAL - improves on 2.45205 but short of the -0.02 compound bar."
    log("-" * 70)
    log(f"HEADLINE cells={M['cells']}  FULL={M['FULL']:.5f}  (H_9298 11-cell coda = 2.45205)")
    log(f"  F1 COMPOUND (<= 2.43205) : {f1}")
    log(f"  F2 EARNED   (<= -0.02)   : {f2}  (d={M['FULL']-M['SHUF']:+.5f}, per-seed {[round(d,5) for d in M['paired']]})")
    log(f"VERDICT: {v}")
    json.dump({"id": "H_9302", "sweep": {str(k): x for k, x in sweep.items()}, "headline_cells": M["cells"],
               "CALIB_pass": calib, "F1_compound": f1, "F2_earned": f2,
               "GREEN": bool(f1 and f2), "verdict": v, "wall_s": time.time() - t0},
              open(os.path.join(a.out, "h9302_summary.json"), "w"), indent=2, ensure_ascii=False)
    log("[done]")


if __name__ == "__main__":
    main()
