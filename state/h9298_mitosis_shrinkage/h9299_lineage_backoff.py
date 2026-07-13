#!/usr/bin/env python3
"""H_9299 — LINEAGE-BACKOFF: is the mitosis division genealogy itself the statistical
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


def grow_on_lineage(X_tr, Y_tr, ntr, vj, dev, grow_max):
    """The H_1306/H_1307 gradient-free split rule VERBATIM, but it now also RECORDS the genealogy.

    Returns (leaf_centers, parent_of_leaf, internal_parent) where the tree is expressed over
    stable node ids: node 0..n-1, leaves are the live cells. Split rule itself is UNCHANGED --
    we only stop throwing the lineage away."""
    # node bookkeeping: centers per node, parent id per node, and which nodes are current leaves
    node_center = [list(c) for c in seed_centers()]
    node_parent = [-1, -1]                     # the two seeds are roots of the forest -> parent = virtual ROOT
    leaves = [0, 1]
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
        elig = [k for k in range(K) if owned_n[k] >= MIN_OWNED and local_ce[k] > SPLIT_THRESH_CE]
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
            break
        ax = int(torch.argmax(pts.var(dim=0, unbiased=False)).item())
        col = pts[:, ax]
        m = col.shape[0]
        scol, _ = torch.sort(col)
        med = (scol[m // 2].item() if m % 2 == 1
               else ((scol[m // 2 - 1] + scol[m // 2]) / 2.0).item())
        lo, hi = col <= med, col > med
        if int(lo.sum().item()) == 0 or int(hi.sum().item()) == 0:
            break
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--ko-window", type=int, default=30000000)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--grow-sweep", default="40,160")   # 40 -> yields the matched 11 cells
    ap.add_argument("--seeds", default="4336,4337,4338")
    ap.add_argument("--out", default="/tmp/h9299_out")
    ap.add_argument("--cpu", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()

    dev = torch.device("cpu" if (a.cpu or not torch.cuda.is_available()) else "cuda")
    log(f"=== H_9299 — LINEAGE-BACKOFF (mitosis genealogy = inheritance) === device={dev}")

    raw = open(a.corpus, "rb").read()[:a.ko_window]
    sha = hashlib.sha256(raw).hexdigest()
    if sha != KO_SHA:
        log(f"FATAL: corpus sha {sha[:16]} != anchor - REFUSING (provenance gate). STOP.")
        sys.exit(2)
    text = None
    for cut in range(0, 4):
        try:
            text = raw[:len(raw) - cut].decode("utf-8"); break
        except UnicodeDecodeError:
            continue
    log(f"[corpus] {len(raw)} B sha={sha[:16]}... PASS")

    jamo_to_id, js = build_jamo_vocab(text)
    vj = 256 + len(js)
    syms, nby = make_symbol_stream(text, jamo_to_id)
    depth = depth_stream(text)
    X, Y, idx = score_stream(syms, depth, vj)
    NB = nby[idx]
    X, Y, NB = X[::a.ko_stride], Y[::a.ko_stride], NB[::a.ko_stride]
    n = X.shape[0]
    ar = np.arange(n)
    e, o = (ar % 2 == 0), (ar % 2 == 1)
    Xtr, Ytr = X[e], Y[e]
    Xte, Yte, NBte = X[o], Y[o], NB[o]

    Xall = torch.tensor(np.concatenate([Xtr, Xte]), dtype=torch.float64, device=dev)
    Yall = torch.tensor(np.concatenate([Ytr, Yte]), dtype=torch.long, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.long, device=dev)
    NBte_t = torch.tensor(NBte, dtype=torch.float64, device=dev)
    ntr = Xtr.shape[0]
    seeds = [int(s) for s in a.seeds.split(",")]
    log(f"[split] scored={n} train={ntr} test={Xte.shape[0]}  Vj={vj}")

    sweep = {}
    for gmax in [int(g) for g in a.grow_sweep.split(",")]:
        leaves, node_center, node_parent = grow_on_lineage(Xall, Yall, ntr, vj, dev, gmax)
        K = len(leaves)
        ct = torch.tensor([node_center[i] for i in leaves], dtype=torch.float64, device=dev)
        owner = assign_all(ct, Xall)
        owner_tr, owner_te = owner[:ntr], owner[ntr:]
        Ytr_t = Yall[:ntr]
        leaf_cnt = _leaf_counts(owner_tr, Ytr_t, K, vj, dev)

        a1 = ce_from_P(all_heads(Yall, owner, K, ntr, vj, dev), owner_te, Yte_t, NBte_t)
        lin = ce_from_P(_chain_probs(leaf_cnt, build_chains(leaves, node_parent, "lin"), vj, dev),
                        owner_te, Yte_t, NBte_t)
        flat = ce_from_P(_chain_probs(leaf_cnt, build_chains(leaves, node_parent, "flat"), vj, dev),
                         owner_te, Yte_t, NBte_t)
        shuf = []
        for sd in seeds:
            rng = np.random.default_rng(sd)
            ch = build_chains(leaves, node_parent, "shuf", rng)
            shuf.append(ce_from_P(_chain_probs(leaf_cnt, ch, vj, dev), owner_te, Yte_t, NBte_t))
        shuf_mean = float(np.mean(shuf))
        depth_max = max(len(c) for c in build_chains(leaves, node_parent, "lin"))
        sweep[gmax] = dict(cells=K, tree_depth=depth_max, A1=a1, FLAT=flat, LIN=lin,
                           SHUF_mean=shuf_mean, SHUF_per_seed=shuf,
                           paired=[lin - v for v in shuf])
        log(f"[grow_max={gmax}] cells={K} depth={depth_max}  A1={a1:.5f}  FLAT={flat:.5f}  "
            f"LIN={lin:.5f}  SHUF={shuf_mean:.5f}  L1(LIN-FLAT)={lin-flat:+.5f}  "
            f"L2(LIN-SHUF)={lin-shuf_mean:+.5f}")

    # headline = the MATCHED cell count (the H_9298 partition: 11 cells)
    matched = None
    for g, r in sweep.items():
        if r["cells"] == 11:
            matched = g; break
    if matched is None:
        matched = sorted(sweep)[0]
    M = sweep[matched]
    calib_ok = abs(M["A1"] - JAMO_FLOOR) <= 1e-4
    l1 = (M["LIN"] - M["FLAT"]) <= L1_BAR
    l2 = ((M["LIN"] - M["SHUF_mean"]) <= L2_BAR) and all(d < 0 for d in M["paired"])

    if not calib_ok:
        verdict = "INVALID - A1 CALIB FAIL (measurement defect, not a result)"
    elif l1 and l2:
        verdict = "GREEN - L1 and L2: the mitosis LINEAGE is the statistical inheritance structure. p8 strengthened literally."
    elif (M["LIN"] - M["SHUF_mean"]) >= 0:
        verdict = "KILL - L2 >= 0: the genealogy is irrelevant; it is just total shrinkage => reduces to H_9298."
    else:
        verdict = "DIRECTIONAL - L1 xor L2 (margin short)"

    # pre-registered diagnostic P1 (NOT a bar): is LIN non-increasing in cell count?
    gs = sorted(sweep, key=lambda g: sweep[g]["cells"])
    p1_lin_monotone = all(sweep[gs[i + 1]]["LIN"] <= sweep[gs[i]]["LIN"] + 1e-9 for i in range(len(gs) - 1))
    p1_flat_degrades = any(sweep[gs[i + 1]]["A1"] > sweep[gs[i]]["A1"] for i in range(len(gs) - 1))

    log("-" * 79)
    log(f"HEADLINE (matched cells={M['cells']}, grow_max={matched})")
    log(f"  A1 jamo floor   {M['A1']:.5f}  [CALIB {'PASS' if calib_ok else 'FAIL'}]")
    log(f"  FLAT (->root)   {M['FLAT']:.5f}")
    log(f"  LIN  (lineage)  {M['LIN']:.5f}   d vs A1 = {M['LIN']-M['A1']:+.5f}  [diagnostic only]")
    log(f"  SHUF (rewired)  {M['SHUF_mean']:.5f}   per-seed {[round(v,5) for v in M['SHUF_per_seed']]}")
    log(f"  L1 LINEAGE-BEATS-FLAT (<= {L1_BAR}) : {l1}   (d={M['LIN']-M['FLAT']:+.5f})")
    log(f"  L2 EARNED vs SHUF     (<= {L2_BAR}) : {l2}   (d={M['LIN']-M['SHUF_mean']:+.5f}, "
        f"per-seed {[round(d,5) for d in M['paired']]})")
    log(f"  P1 diagnostic: LIN monotone non-increasing in cells = {p1_lin_monotone} ; "
        f"A1 degrades somewhere = {p1_flat_degrades}")
    log(f"VERDICT: {verdict}")
    wall = time.time() - t0
    log(f"wall={wall:.1f}s")

    json.dump({"id": "H_9299", "device": str(dev), "ko_window_sha256": sha,
               "matched_grow_max": matched, "headline": M, "sweep": {str(k): v for k, v in sweep.items()},
               "CALIB_pass": calib_ok, "L1_lineage_beats_flat": l1, "L2_earned_vs_shuffled_genealogy": l2,
               "P1_LIN_monotone_in_cells": p1_lin_monotone, "P1_A1_degrades": p1_flat_degrades,
               "GREEN": bool(l1 and l2), "verdict": verdict, "seeds": seeds, "wall_s": wall},
              open(os.path.join(a.out, "h9299_summary.json"), "w"), indent=2, ensure_ascii=False)
    log("[done]")


if __name__ == "__main__":
    main()
