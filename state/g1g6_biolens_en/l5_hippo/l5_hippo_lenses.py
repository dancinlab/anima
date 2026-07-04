#!/usr/bin/env python3
"""
H_9129 L5 hippo rung(2) — a_break_the_wall CONTROLLED LENSES over the 303M representation.

The single-lens run gave store_gap~=0 (WALL), but with a red flag: raw mean-pooled 303M
reps are near-collinear (form cosine 0.9999 for EVERY pair; DG-code overlap 0.985). That is
the well-known LLM anisotropy (a dominant shared "common" direction) — it can masquerade as a
substrate wall (cf. H_1590 torch-artifact lesson). Before cementing WALL we control the
representation extraction with >=2-3 lenses. For each lens we report:
  form_sep  = does the RAW 303M rep already separate reachable(within-chain) vs unreachable
              (cross-chain)?  (form_reach_cos - form_unreach_cos)   -> reps discriminative?
  store_gap = does the CA3 lane separate them?
  shuf_gap / loff_gap = BIND + causal controls.
Same real 303M h1129 engine (core/decode.py), same corpus graph, same seed — only the
rep-preprocessing (pool × centering/whitening) varies.
"""
import os, sys, json, time, re
import numpy as np
_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d
import l5_hippo_engine_native as base   # reuse graph + engine helpers

CKPT = base.CKPT; OUTDIR = os.path.dirname(__file__)
DIM, ACTIVE, STEPS, KWTA = base.DIM, base.ACTIVE, base.STEPS, base.KWTA
N_CHAINS, CHAIN_LEN, N_ITEMS, SEED = base.N_CHAINS, base.CHAIN_LEN, base.N_ITEMS, base.SEED

def kwta(v, k):
    if k >= v.size: return (v > 0).astype(np.float32)
    idx = np.argpartition(v, -k)[-k:]; out = np.zeros_like(v)
    pos = idx[v[idx] > 0]; out[pos] = 1.0; return out

def dg_codes(reps, rng):
    n, dm = reps.shape
    P = rng.standard_normal((DIM, dm)).astype(np.float32) / np.sqrt(dm)
    R = reps / (np.linalg.norm(reps, axis=1, keepdims=True) + 1e-9)
    drive = R @ P.T
    return np.stack([kwta(drive[i], ACTIVE) for i in range(n)])

def build_store(codes, succ):
    W = np.zeros((DIM, DIM), dtype=np.float32)
    for c, nx in succ.items(): W += np.outer(codes[nx], codes[c])
    return W

def relatedness(W, codes, i, j):
    x = codes[i].copy(); cj = codes[j]; cjn = np.linalg.norm(cj) + 1e-9; best = 0.0
    for _ in range(STEPS):
        x = kwta(W @ x, KWTA)
        ov = float(x @ cj) / ((np.linalg.norm(x) + 1e-9) * cjn)
        if ov > best: best = ov
    return best

def fcos(reps, i, j):
    a, b = reps[i], reps[j]
    return float(a @ b) / ((np.linalg.norm(a) + 1e-9) * (np.linalg.norm(b) + 1e-9))

def preprocess(reps, mode):
    R = reps.copy()
    if mode == "raw":            return R
    mu = R.mean(axis=0, keepdims=True)
    if mode == "center":         return R - mu
    if mode == "center_zscore":
        Rc = R - mu; sd = Rc.std(axis=0, keepdims=True) + 1e-6; return Rc / sd
    if mode == "center_drop_top":  # remove top-1 principal (common) direction after centering
        Rc = R - mu
        U, S, Vt = np.linalg.svd(Rc, full_matrices=False)
        return Rc - (Rc @ Vt[0][:, None]) @ Vt[0][None, :]
    raise ValueError(mode)

def main():
    t0 = time.time()
    print("[load] real 303M h1129 ...", flush=True)
    W = d.bg_load(CKPT)
    lines = base.load_lines(); vocab, freq, co = base.build_graph(lines)
    chains = base.greedy_chains(vocab, freq, co)
    items = [w for ch in chains for w in ch]
    print(f"[graph] chains={len(chains)} items={len(items)}", flush=True)

    # extract BOTH mean-pool and last-token 303M hidden in one pass
    print("[reps] extracting mean-pool + last-token 303M hidden ...", flush=True)
    mp = np.zeros((N_ITEMS, W["d"])); lt = np.zeros((N_ITEMS, W["d"]))
    for k, w in enumerate(items):
        ids = list(w.encode("utf-8", "surrogateescape"))
        H = base.bg_hidden_seq_W(W, ids, len(ids))
        mp[k] = H.mean(axis=0); lt[k] = H[-1]
    print(f"[reps] done {time.time()-t0:.1f}s", flush=True)

    def cof(k): return k // CHAIN_LEN
    successor = {}
    for c in range(N_CHAINS):
        b = c * CHAIN_LEN
        for p in range(CHAIN_LEN - 1): successor[b + p] = b + p + 1
    reachable, unreachable = [], []
    for c in range(N_CHAINS):
        b = c * CHAIN_LEN
        for a in range(CHAIN_LEN):
            for bb in range(a + 2, CHAIN_LEN): reachable.append((b + a, b + bb))
    rng0 = np.random.default_rng(SEED); seen = set()
    while len(unreachable) < len(reachable):
        i = int(rng0.integers(N_ITEMS)); j = int(rng0.integers(N_ITEMS))
        if cof(i) == cof(j): continue
        key = (min(i, j), max(i, j))
        if key in seen: continue
        seen.add(key); unreachable.append((i, j))

    pools = {"meanpool": mp, "lasttok": lt}
    modes = ["raw", "center", "center_zscore", "center_drop_top"]
    rows = []
    for pn, P in pools.items():
        for m in modes:
            R = preprocess(P, m)
            fr = np.array([fcos(R, i, j) for i, j in reachable])
            fu = np.array([fcos(R, i, j) for i, j in unreachable])
            rng = np.random.default_rng(SEED)   # same projection seed per lens
            codes = dg_codes(R, rng)
            ov = float(np.mean([float(codes[a] @ codes[b]) / ACTIVE
                                for a in range(N_ITEMS) for b in range(a+1, N_ITEMS)]))
            Ws = build_store(codes, successor)
            sr = np.array([relatedness(Ws, codes, i, j) for i, j in reachable])
            su = np.array([relatedness(Ws, codes, i, j) for i, j in unreachable])
            keys = list(successor.keys()); vals = list(successor.values())
            perm = rng.permutation(len(vals))
            while any(perm[k] == k for k in range(len(perm))): perm = rng.permutation(len(vals))
            ssh = {keys[k]: vals[perm[k]] for k in range(len(keys))}
            Wsh = build_store(codes, ssh)
            shr = np.array([relatedness(Wsh, codes, i, j) for i, j in reachable])
            shu = np.array([relatedness(Wsh, codes, i, j) for i, j in unreachable])
            Woff = np.zeros((DIM, DIM), dtype=np.float32)
            lor = np.array([relatedness(Woff, codes, i, j) for i, j in reachable])
            store_gap = float(sr.mean() - su.mean()); form_sep = float(fr.mean() - fu.mean())
            shuf_gap = float(shr.mean() - shu.mean()); ratio = float(sr.mean()/(su.mean()+1e-9))
            shuf_col = shuf_gap < 0.5*store_gap if store_gap > 0 else True
            loff_col = float(lor.mean()) < 0.05
            rows.append(dict(pool=pn, mode=m, code_overlap=ov, form_reach=float(fr.mean()),
                form_sep=form_sep, store_reach=float(sr.mean()), store_unreach=float(su.mean()),
                store_gap=store_gap, ratio=ratio, shuf_gap=shuf_gap, loff_reach=float(lor.mean()),
                shuffle_collapsed=bool(shuf_col), lane_off_collapsed=bool(loff_col)))

    # verdict over lenses: is there ANY lens where reps become discriminative AND lane lifts?
    best = max(rows, key=lambda r: r["store_gap"])
    any_form_sep = any(r["form_sep"] > 0.05 for r in rows)
    any_green = any(r["store_gap"] > 0.50 and r["shuffle_collapsed"] and r["lane_off_collapsed"] for r in rows)

    L = []
    L.append("# H_9129 L5 hippo rung(2) — controlled-lens sweep over 303M representation (a_break_the_wall)")
    L.append(f"engine: real ByteGPT-303M h1129 (core/decode.py byte-exact) · {time.time()-t0:.1f}s")
    L.append("")
    L.append("code_overlap: mean pairwise DG-code overlap (0=orthogonal ideal; ->1 = degenerate/collinear reps)")
    L.append("form_sep: raw-303M-rep cosine reach-unreach (>0 => reps ALREADY separate related concepts)")
    L.append("store_gap: CA3 lane reach-unreach   ratio: reach/unreach")
    L.append("")
    hdr = f"{'pool':9} {'mode':16} {'ovlap':>6} {'form_sep':>9} {'st_reach':>8} {'st_gap':>8} {'ratio':>6} {'shuf_gap':>8} {'loff':>6} {'shufCol':>7}"
    L.append(hdr); L.append("-"*len(hdr))
    for r in rows:
        L.append(f"{r['pool']:9} {r['mode']:16} {r['code_overlap']:6.3f} {r['form_sep']:+9.4f} "
                 f"{r['store_reach']:8.4f} {r['store_gap']:+8.4f} {r['ratio']:6.2f} "
                 f"{r['shuf_gap']:+8.4f} {r['loff_reach']:6.3f} {str(r['shuffle_collapsed']):>7}")
    L.append("")
    L.append("## READING")
    L.append(f"  any lens where 303M reps SEPARATE related concepts (form_sep>0.05) = {any_form_sep}")
    L.append(f"  any lens meeting GREEN bar (store_gap>0.5 & shuffle-collapse & lane-off) = {any_green}")
    L.append(f"  best lens = {best['pool']}/{best['mode']}  store_gap={best['store_gap']:+.4f} ratio={best['ratio']:.2f}")
    if any_green:
        vv = "GREEN"; why = "at least one de-anisotropy lens restores lane BIND on real 303M reps"
    elif any_form_sep:
        vv = "WALL"; why = "de-anisotropy makes reps discriminative (form_sep>0) yet CA3 lane still fails to chain them"
    else:
        vv = "WALL"; why = "303M single-word reps are anisotropic/non-discriminative across ALL lenses; lane cannot bind what the substrate does not separate"
    L.append(f"  >>> LENS VERDICT = {vv}  ({why})")
    out = "\n".join(L)
    print("\n"+out, flush=True)
    with open(os.path.join(OUTDIR, "result_lenses.txt"), "w") as f: f.write(out+"\n")
    with open(os.path.join(OUTDIR, "result_lenses.json"), "w") as f:
        json.dump(dict(rows=rows, any_form_sep=any_form_sep, any_green=any_green,
                       best=best, verdict=vv), f, indent=2)
    print(f"\n[done] {time.time()-t0:.1f}s verdict={vv}", flush=True)

if __name__ == "__main__":
    main()
