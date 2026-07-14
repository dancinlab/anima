#!/usr/bin/env python3
"""H_9298 — WB-coda SHRINKAGE: does removing the fragmentation cost recover the EARNED
cross-syllable information that H_1336 proved present (+0.076 nats) but could not bank?

Law under test:  gain = new_information - partition_cost,  and partition_cost is paid UP FRONT.
The count-MLE hard-partition estimator class has no partial purchase (no shared statistical
strength): every new conditioning bit forces a multiplicative sample-splitting cost.

Estimators (all ride the SAME gradient-free Voronoi partition; the mitosis rule is untouched):
  A1  P(next | cell)                                    <- the jamo floor, CALIB anchor 2.51335
  B1  P(next | cell, prev_coda), HARD-BACKOFF           <- H_1336 replication, CALIB anchor 2.61186
  B2  P(next | cell, prev_coda) = l*MLE(cell,coda) + (1-l)*MLE(cell)   <- THE LEVER
      l = Witten-Bell = n / (n + T)   (n = count(cell,coda), T = distinct next types there)
      ZERO free hyperparameters -> tune-to-green is structurally impossible.
  B2s B2 with prev_coda POSITION-SHUFFLED (per seed)    <- the earned control (pairing broken,
      coda marginal + fragmentation structure preserved). NOT a label bijection (provably vacuous).

Frozen bars live in FREEZE.txt. GREEN iff S1 (B2 <= 2.49335) AND S2 (B2 - B2s <= -0.02, 3/3 seeds).
"B2 <= A1" is NOT evidence (WB collapses to A1 at l->0) -> reported as diagnostic only.

Port provenance: pipeline recovered 1:1 from the H_1316 bytecode that produced the 2.51335 anchor
(UNIVERSE/__pycache__/h1316_ko_jamo_mitosis.cpython-314.pyc) -- geometry, mitosis knobs, symbol
stream, depth stream and CE axis are byte-faithful. The two CALIB gates verify the port.
"""
import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

try:
    import torch
except Exception as exc:
    print("FATAL: torch import failed:", exc); sys.exit(1)

# ---- frozen knobs (verbatim from H_1316/H_1336) -------------------------------------------
LAPLACE = 1.0
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
HANGUL_LO, HANGUL_HI = 44032, 55203
JAMO_FLOOR = 2.51335          # A1 anchor (H_1316)
B1_ANCHOR = 2.61186           # B1 anchor (H_1336)
RAW_CEILING = 2.95342
KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
S1_BAR = 2.49335              # jamo floor - 0.02
S2_BAR = -0.02

NO_CODA = -1                  # open syllable (L,V only)
NONE_CODA = -2                # nothing completed yet


def log(*a):
    print(*a, flush=True)


# ---- symbol / depth / vocab (1:1 port) ----------------------------------------------------
def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch):
                jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    return {cp: 256 + i for i, cp in enumerate(jamo_sorted)}, jamo_sorted


def syll_jamo_nbytes(njamo):
    """Distribute the syllable's 3 UTF-8 bytes across its jamo so they SUM to 3."""
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
    """(syms, nbytes, prev_coda) -- prev_coda = coda symbol-id of the most recently COMPLETED
    Hangul syllable (NONE_CODA before the first, NO_CODA for an open syllable). It is the
    cross-syllable phonotactic context the within-syllable head structurally cannot see."""
    syms, nby, pcod = [], [], []
    cur = NONE_CODA
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                sid = jamo_to_id[ord(jc)]
                syms.append(sid); nby.append(nb[j]); pcod.append(cur)
            # syllable now COMPLETE -> it becomes the context for what follows
            cur = jamo_to_id[ord(nfd[2])] if len(nfd) == 3 else NO_CODA
        else:
            for b in ch.encode("utf-8"):
                syms.append(b); nby.append(1); pcod.append(cur)
    return (np.asarray(syms, dtype=np.int64),
            np.asarray(nby, dtype=np.int64),
            np.asarray(pcod, dtype=np.int64))


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


# ---- gradient-free mitosis substrate (1:1 port) --------------------------------------------
def seed_centers():
    """H_1307 SEED_CENTERS pattern, 3-D."""
    return [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]


def assign_all(centers_t, X_t):
    return torch.argmin(torch.cdist(X_t, centers_t, p=2), dim=1)


def all_heads(Y_t, owner, K, ntr, vj, dev):
    Hmat = torch.full((K, vj), LAPLACE, dtype=torch.float64, device=dev)
    own, y = owner[:ntr], Y_t[:ntr]
    flat = own * vj + y
    ones = torch.ones(flat.shape[0], dtype=torch.float64, device=dev)
    Hmat.view(-1).index_add_(0, flat, ones)
    return Hmat / Hmat.sum(dim=1, keepdim=True)


def owned_ce(Y_t, owner, k, ntr, p_row):
    mask = owner[:ntr] == k
    if not mask.any():
        return -1.0
    yk = Y_t[:ntr][mask]
    return -torch.log(p_row[yk] + 1e-12).mean().item()


def grow_on(centers, X_tr, Y_tr, ntr, vj, dev, grow_max):
    """Faithful port of the H_1306/H_1307 hexa _grow_on (gradient-free, cells only SPLIT -- p8)."""
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = torch.tensor(centers, dtype=torch.float64, device=dev)
        owner = assign_all(ct, X_tr)
        K = len(centers)
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
        if len(centers) + 1 > grow_max:
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
        c_lo = pts[lo].mean(dim=0).cpu().numpy().tolist()
        c_hi = pts[hi].mean(dim=0).cpu().numpy().tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers


def score_stream(syms, depth, vj):
    n = len(syms)
    idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    X = np.stack([last, second, cdep], axis=1)
    Y = syms[idx].astype(np.int64)
    return X, Y, idx


# ---- the three heads -----------------------------------------------------------------------
def ce_A1(owner_tr, Y_tr, owner_te, Y_te, NB_te, K, vj, dev):
    """P(next | cell) -- the jamo floor."""
    H = all_heads(Y_tr, owner_tr, K, len(Y_tr), vj, dev)
    p = H[owner_te, Y_te]
    nats = (-torch.log(p + 1e-12)).sum().item()
    return nats / float(NB_te.sum())


def _cond_tables(owner_tr, C_tr, Y_tr, K, ncod, vj, dev):
    """Counts n[cell, coda, next] as a flat (K*ncod, vj) matrix + its row sums / type counts."""
    key = owner_tr * ncod + C_tr
    cnt = torch.zeros((K * ncod, vj), dtype=torch.float64, device=dev)
    cnt.view(-1).index_add_(0, key * vj + Y_tr,
                            torch.ones(Y_tr.shape[0], dtype=torch.float64, device=dev))
    n_kc = cnt.sum(dim=1)                              # tokens in (cell, coda)
    T_kc = (cnt > 0).sum(dim=1).to(torch.float64)      # distinct next-types in (cell, coda)
    return cnt, n_kc, T_kc


def ce_B1(owner_tr, C_tr, Y_tr, owner_te, C_te, Y_te, NB_te, K, ncod, vj, dev):
    """H_1336: HARD-BACKOFF. Unseen (cell,coda) at test -> the cell-marginal (= A1)."""
    H = all_heads(Y_tr, owner_tr, K, len(Y_tr), vj, dev)
    cnt, n_kc, _ = _cond_tables(owner_tr, C_tr, Y_tr, K, ncod, vj, dev)
    cond = (cnt + LAPLACE) / (cnt + LAPLACE).sum(dim=1, keepdim=True)
    key_te = owner_te * ncod + C_te
    p_cond = cond[key_te, Y_te]
    p_back = H[owner_te, Y_te]
    seen = (n_kc[key_te] > 0)
    p = torch.where(seen, p_cond, p_back)
    nats = (-torch.log(p + 1e-12)).sum().item()
    return nats / float(NB_te.sum())


def ce_B2(owner_tr, C_tr, Y_tr, owner_te, C_te, Y_te, NB_te, K, ncod, vj, dev):
    """THE LEVER: Witten-Bell shrinkage -- no fragmentation, strength shared with the parent cell.
       P = l*MLE(cell,coda) + (1-l)*P(next|cell),   l = n/(n+T).  Zero free hyperparameters."""
    H = all_heads(Y_tr, owner_tr, K, len(Y_tr), vj, dev)          # the parent (cell) distribution
    cnt, n_kc, T_kc = _cond_tables(owner_tr, C_tr, Y_tr, K, ncod, vj, dev)
    key_te = owner_te * ncod + C_te
    n_row = n_kc[key_te]
    T_row = T_kc[key_te]
    lam = n_row / (n_row + T_row + 1e-12)             # WB; n=0 -> lam=0 -> exactly the parent
    mle = cnt[key_te, Y_te] / (n_row + 1e-12)         # raw MLE of the child
    parent = H[owner_te, Y_te]
    p = lam * mle + (1.0 - lam) * parent
    nats = (-torch.log(p + 1e-12)).sum().item()
    return nats / float(NB_te.sum())


def cond_mi(owner_tr, C_tr, Y_tr, K, ncod, vj, dev):
    """P0 gate: I(next ; prev_coda | cell) on TRAIN only. >0.01 nats => the cells do NOT already
       encode prev_coda => the lever is not a no-op (H_1329 depletion condition)."""
    cnt, _, _ = _cond_tables(owner_tr, C_tr, Y_tr, K, ncod, vj, dev)
    N = float(Y_tr.shape[0])
    c3 = cnt.view(K, ncod, vj)
    cell_cnt = c3.sum(dim=1)                                        # (K, vj)
    n_cell = cell_cnt.sum(dim=1, keepdim=True)
    p_y_g_cell = cell_cnt / (n_cell + 1e-12)
    n3 = c3.sum(dim=2, keepdim=True)
    p_y_g_kc = c3 / (n3 + 1e-12)
    lg = torch.log(p_y_g_kc + 1e-12) - torch.log(p_y_g_cell.unsqueeze(1) + 1e-12)
    return float((c3 * lg).sum().item() / N)                        # nats/symbol


# -------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--ko-window", type=int, default=30000000)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--grow-max", type=int, default=40)
    ap.add_argument("--seeds", default="4336,4337,4338")
    ap.add_argument("--out", default="/tmp/h9298_out")
    ap.add_argument("--cpu", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()

    dev = torch.device("cpu" if (a.cpu or not torch.cuda.is_available()) else "cuda")
    log(f"=== H_9298 — WB-coda SHRINKAGE vs the jamo floor {JAMO_FLOOR} === device={dev}")

    raw = open(a.corpus, "rb").read()[:a.ko_window]
    sha = hashlib.sha256(raw).hexdigest()
    log(f"[corpus] {len(raw)} B sha={sha[:16]}...")
    if sha != KO_SHA:
        log("FATAL: corpus sha != H_1307 RUN A anchor - REFUSING to run (provenance gate). STOP.")
        sys.exit(2)
    text = None
    for cut in range(0, 4):
        try:
            text = raw[:len(raw) - cut].decode("utf-8"); break
        except UnicodeDecodeError:
            continue

    jamo_to_id, jamo_sorted = build_jamo_vocab(text)
    vj = 256 + len(jamo_sorted)
    log(f"[jamo] distinct={len(jamo_sorted)}  Vj={vj}")

    syms, nby, pcod = make_symbol_stream(text, jamo_to_id)
    depth = depth_stream(text)
    X, Y, idx = score_stream(syms, depth, vj)
    NB = nby[idx]
    C = pcod[idx]

    codas = sorted(set(C.tolist()))
    cmap = {c: i for i, c in enumerate(codas)}
    C = np.asarray([cmap[c] for c in C], dtype=np.int64)
    ncod = len(codas)
    log(f"[coda] distinct prev_coda tokens = {ncod}  (H_1336 = 29)")

    X, Y, NB, C = X[::a.ko_stride], Y[::a.ko_stride], NB[::a.ko_stride], C[::a.ko_stride]
    n = X.shape[0]
    ar = np.arange(n)
    e, o = (ar % 2 == 0), (ar % 2 == 1)
    Xtr, Ytr, Ctr = X[e], Y[e], C[e]
    Xte, Yte, NBte, Cte = X[o], Y[o], NB[o], C[o]
    log(f"[split] scored={n}  train={Xtr.shape[0]}  test={Xte.shape[0]}")

    Xall = torch.tensor(np.concatenate([Xtr, Xte]), dtype=torch.float64, device=dev)
    Yall = torch.tensor(np.concatenate([Ytr, Yte]), dtype=torch.long, device=dev)
    ntr = Xtr.shape[0]

    centers = grow_on(seed_centers(), Xall, Yall, ntr, vj, dev, a.grow_max)
    ct = torch.tensor(centers, dtype=torch.float64, device=dev)
    K = len(centers)
    owner = assign_all(ct, Xall)
    owner_tr, owner_te = owner[:ntr], owner[ntr:]
    log(f"[mitosis] cells={K}  (H_1336 = 11)")

    Ytr_t = torch.tensor(Ytr, dtype=torch.long, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.long, device=dev)
    Ctr_t = torch.tensor(Ctr, dtype=torch.long, device=dev)
    Cte_t = torch.tensor(Cte, dtype=torch.long, device=dev)
    NBte_t = torch.tensor(NBte, dtype=torch.float64, device=dev)

    mi = cond_mi(owner_tr, Ctr_t, Ytr_t, K, ncod, vj, dev)
    log(f"[P0] I(next ; prev_coda | cell) = {mi:.5f} nats/sym  (gate > 0.01)")

    a1 = ce_A1(owner_tr, Ytr_t, owner_te, Yte_t, NBte_t, K, vj, dev)
    b1 = ce_B1(owner_tr, Ctr_t, Ytr_t, owner_te, Cte_t, Yte_t, NBte_t, K, ncod, vj, dev)
    log(f"[CALIB] A1 jamo floor   = {a1:.5f}   (anchor {JAMO_FLOOR}  d={a1-JAMO_FLOOR:+.5f})")
    log(f"[CALIB] B1 hard-backoff = {b1:.5f}   (anchor {B1_ANCHOR}  d={b1-B1_ANCHOR:+.5f})")

    b2 = ce_B2(owner_tr, Ctr_t, Ytr_t, owner_te, Cte_t, Yte_t, NBte_t, K, ncod, vj, dev)
    log(f"[B2] WB-shrinkage       = {b2:.5f}   (S1 bar <= {S1_BAR})")

    seeds = [int(s) for s in a.seeds.split(",")]
    b2s_per_seed = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        Ctr_s = torch.tensor(rng.permutation(Ctr), dtype=torch.long, device=dev)
        Cte_s = torch.tensor(rng.permutation(Cte), dtype=torch.long, device=dev)
        v = ce_B2(owner_tr, Ctr_s, Ytr_t, owner_te, Cte_s, Yte_t, NBte_t, K, ncod, vj, dev)
        b2s_per_seed.append(v)
        log(f"[B2s seed {sd}] coda position-shuffle = {v:.5f}   paired d(B2-B2s) = {b2-v:+.5f}")

    b2s = float(np.mean(b2s_per_seed))
    sd_ctrl = float(np.std(b2s_per_seed, ddof=1)) if len(b2s_per_seed) > 1 else 0.0
    paired = [b2 - v for v in b2s_per_seed]

    calib_ok = abs(a1 - JAMO_FLOOR) <= 1e-4
    p0_ok = mi > 0.01
    s1 = (b2 <= S1_BAR) and (b2 < RAW_CEILING)
    s2 = (b2 - b2s <= S2_BAR) and all(d < 0 for d in paired)

    if not calib_ok:
        verdict = "INVALID - CALIB FAIL (A1 does not reproduce the anchor; measurement defect, not a result)"
    elif not p0_ok:
        verdict = "NO-OP - P0 FAIL: the cells already encode prev_coda; the lever is a no-op (law untouched)"
    elif s1 and s2:
        verdict = "GREEN - S1 and S2: the jamo floor BREAKS once the fragmentation cost is removed. Law CONFIRMED."
    elif (b2 - b2s) >= 0:
        verdict = "KILL - S2 delta >= 0: the coda information does NOT survive shrinkage => the law is WRONG (re-audit X2)."
    else:
        verdict = "DIRECTIONAL - S1 xor S2 (margin short; mechanism alive)"

    log("-" * 79)
    log(f"raw ceiling         {RAW_CEILING}")
    log(f"A1 jamo floor       {a1:.5f}   [CALIB {'PASS' if calib_ok else 'FAIL'}]")
    log(f"B1 hard-backoff     {b1:.5f}   (H_1336 = {B1_ANCHOR})")
    log(f"B2 WB-shrinkage     {b2:.5f}   d vs floor = {b2-a1:+.5f}   [diagnostic only, NOT a bar]")
    log(f"B2s pos-shuffle     {b2s:.5f}   sd={sd_ctrl:.5f}")
    log(f"S1 BELOW-FLOOR (B2 <= {S1_BAR})          : {s1}")
    log(f"S2 EARNED      (B2-B2s <= {S2_BAR}, 3/3) : {s2}   (d={b2-b2s:+.5f}, per-seed {[round(d,5) for d in paired]})")
    log(f"VERDICT: {verdict}")
    wall = time.time() - t0
    log(f"wall={wall:.1f}s")

    json.dump({
        "id": "H_9298", "device": str(dev),
        "ko_window_bytes": len(raw), "ko_window_sha256": sha,
        "corpus_identical_to_H1307_runA": sha == KO_SHA,
        "ko_stride": a.ko_stride, "grow_max": a.grow_max, "cells": K,
        "jamo_vocab_Vj": vj, "distinct_jamo": len(jamo_sorted), "distinct_prev_coda_tokens": ncod,
        "P0_cond_mi_nats": mi, "P0_pass": p0_ok,
        "raw_ceiling": RAW_CEILING,
        "A1_jamo_floor_inrun": a1, "A1_anchor": JAMO_FLOOR, "CALIB_pass": calib_ok,
        "B1_hard_backoff_inrun": b1, "B1_anchor": B1_ANCHOR,
        "B2_wb_shrinkage": b2,
        "B2s_pos_shuffle_mean": b2s, "B2s_per_seed": b2s_per_seed, "B2s_sd": sd_ctrl,
        "paired_delta_per_seed": paired,
        "delta_B2_vs_floor_DIAGNOSTIC_ONLY": b2 - a1,
        "delta_B2_vs_shuffle": b2 - b2s,
        "S1_below_floor": s1, "S2_earned": s2,
        "GREEN": bool(s1 and s2), "verdict": verdict,
        "seeds": seeds, "wall_s": wall,
    }, open(os.path.join(a.out, "h9298_summary.json"), "w"), indent=2, ensure_ascii=False)
    log("[done]")


if __name__ == "__main__":
    main()
