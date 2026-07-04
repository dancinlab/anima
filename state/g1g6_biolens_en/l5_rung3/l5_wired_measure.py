#!/usr/bin/env python3
"""
H_9129 L5 rung-3 — WIRED measurement: the discriminator numbers reproduced by calling
the LIVE core/hippo_lane.py ops directly (dg_decorrelate / dg_codes / hippo_build_store /
hippo_relatedness), over REAL ByteGPT-303M h1129 reps via core/decode.py (== anima
evaluate --py ops, a_eval_py_canonical). Proves the reach>>unreach + lesion signal is
produced by the WIRED core/ lane op (byte-parity twin of core/kosmos_io.hexa), not a
throwaway harness. No new metric; identical algorithm to l5_discriminator.py.
"""
import os, sys, re
import numpy as np

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d
import hippo_lane as H            # ← the LIVE core/ lane op

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
CORPUS = os.path.join(_REPO, "archive", "data", "corpus.txt")
SEED, N_CHAINS, CHAIN_LEN = 20260705, 8, 6
DIM, ACTIVE, STEPS, KWTA = 2048, 40, 6, 40
N_ITEMS = N_CHAINS * CHAIN_LEN
STOP = set("""the a an and or but if then else of to in on at for with as by from into over under
this that these those it its is are was were be been being have has had do does did will would
can could should may might must not no nor so than too very just also more most much many some
any all each every both few other such only own same about above after again against because
before below between during through until while your you they them their there here what when
where which who whom whose why how our out off down up we he she his her him me my mine ours
i am pm mr ms dr etc vs via per got get getbe really think know like well yeah okay something
things thing want need make made even still back come came going go went one two three""".split())

def bg_hidden_seq_W(W, ids, T):
    dd, nlay, nh = W["d"], W["nlay"], W["nh"]
    ids = np.asarray(ids, dtype=np.int64)
    x = W["tok"][ids] + W["pos"][0:T]
    for Lr in range(nlay):
        nrm = d._bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, dd)
        x = x + d._bg_mha(nrm, W["inW"][Lr], W["inB"][Lr], W["oW"][Lr], W["oB"][Lr], T, dd, nh)
        nrm = d._bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, dd)
        h4 = d._bg_gelu(nrm @ W["m0W"][Lr].T + W["m0B"][Lr])
        x = x + (h4 @ W["m2W"][Lr].T + W["m2B"][Lr])
    if W.get("bind"):
        x = d._bg_apply_bind(x, W["bind"], T, dd, nh)
    return x

def rep303(W, w):
    ids = list(w.encode("utf-8", "surrogateescape"))
    return bg_hidden_seq_W(W, ids, len(ids)).mean(axis=0)

def load_lines():
    out = []
    with open(CORPUS, encoding="utf-8", errors="surrogateescape") as f:
        for ln in f:
            ln = ln.strip()
            if ln.startswith(("A:", "B:")): ln = ln[2:].strip()
            toks = [t for t in re.findall(r"[a-z]{4,}", ln.lower()) if t not in STOP]
            if len(toks) >= 3: out.append(toks)
    return out

def build_graph(lines):
    from collections import Counter
    freq = Counter(t for ln in lines for t in set(ln))
    vocab = [w for w, c in freq.most_common(400) if c >= 6]; vset = set(vocab)
    co = {}
    for ln in lines:
        u = [t for t in set(ln) if t in vset]
        for a in range(len(u)):
            for b in range(a+1, len(u)):
                k = (min(u[a], u[b]), max(u[a], u[b])); co[k] = co.get(k, 0)+1
    return vocab, co

def greedy_chains(vocab, co):
    adj = {}
    for (a, b), c in co.items():
        adj.setdefault(a, []).append((c, b)); adj.setdefault(b, []).append((c, a))
    for w in adj: adj[w].sort(reverse=True)
    used, chains = set(), []
    for seed in [w for w in vocab if w in adj]:
        if len(chains) >= N_CHAINS: break
        if seed in used: continue
        chain = [seed]; used.add(seed)
        while len(chain) < CHAIN_LEN:
            nxt = None
            for c, w in adj.get(chain[-1], []):
                if w not in used and c >= 3: nxt = w; break
            if nxt is None: break
            chain.append(nxt); used.add(nxt)
        if len(chain) == CHAIN_LEN: chains.append(chain)
        else:
            for w in chain: used.discard(w)
    return chains

def m(a): return float(np.mean(a)) if len(a) else float("nan")

def main():
    W = d.bg_load(CKPT)
    v, co = build_graph(load_lines()); chains = greedy_chains(v, co)
    items = [w for ch in chains for w in ch]
    reps = np.stack([rep303(W, w) for w in items])

    # ── LIVE core/hippo_lane.py ops ──
    Rw = H.dg_decorrelate(reps, "center_zscore")
    codes = H.dg_codes(Rw, DIM, ACTIVE, SEED)
    edges = [(c*CHAIN_LEN+p, c*CHAIN_LEN+p+1) for c in range(N_CHAINS) for p in range(CHAIN_LEN-1)]
    Ws = H.hippo_build_store(codes, edges, DIM)

    def rel(store, i, j): return H.hippo_relatedness(store, codes, i, j, STEPS, KWTA)
    def cof(k): return k // CHAIN_LEN
    def pin(k): return k % CHAIN_LEN

    recall = [(c*CHAIN_LEN+a, c*CHAIN_LEN+a+1) for c in range(N_CHAINS) for a in range(CHAIN_LEN-1)]
    novel  = [(c*CHAIN_LEN+a, c*CHAIN_LEN+b) for c in range(N_CHAINS)
              for a in range(CHAIN_LEN) for b in range(a+2, CHAIN_LEN)]
    rng = np.random.default_rng(SEED); seen = set(); unreach = []
    while len(unreach) < len(novel):
        i = int(rng.integers(N_ITEMS)); j = int(rng.integers(N_ITEMS))
        if cof(i) == cof(j): continue
        k = (min(i, j), max(i, j))
        if k in seen: continue
        seen.add(k); unreach.append((i, j))

    rc = [rel(Ws, i, j) for i, j in recall]
    nc = [rel(Ws, i, j) for i, j in novel]
    ur = [rel(Ws, i, j) for i, j in unreach]
    off = np.zeros((DIM, DIM), dtype=np.float32)
    lo = [rel(off, i, j) for i, j in novel]
    # lesion pos2->pos3
    Mles = 2
    les_edges = [(c, n) for (c, n) in edges if not (pin(c) == Mles and pin(n) == Mles+1)]
    Wl = H.hippo_build_store(codes, les_edges, DIM)
    pb = [(i, j) for i, j in novel if pin(i) <= Mles and pin(j) >= Mles+1]
    pi = [(i, j) for i, j in novel if not (pin(i) <= Mles and pin(j) >= Mles+1)]
    lb = [rel(Wl, i, j) for i, j in pb]; lb0 = [rel(Ws, i, j) for i, j in pb]
    li = [rel(Wl, i, j) for i, j in pi]; li0 = [rel(Ws, i, j) for i, j in pi]

    print("WIRED via core/hippo_lane.py (LIVE op) over real 303M h1129 reps:")
    print(f"  recall(gap1 stored) = {m(rc):.4f}   novel_chain = {m(nc):.4f}   unreach = {m(ur):.4f}")
    print(f"  store_gap (novel-unreach) = {m(nc)-m(ur):+.4f}   ratio = {m(nc)/(m(ur)+1e-9):.2f}x")
    print(f"  lane_off(novel) = {m(lo):.4f}")
    print(f"  lesion broken paths: {m(lb0):.4f} -> {m(lb):.4f} (drop {m(lb0)-m(lb):+.4f})")
    print(f"  lesion intact paths: {m(li0):.4f} -> {m(li):.4f} (drop {m(li0)-m(li):+.4f})")
    ok = (m(nc)-m(ur) > 0.50) and (m(lo) < 0.05) and ((m(lb0)-m(lb)) > 0.50) and (m(li) > 0.50)
    print(f"  >>> LIVE-OP reproduces discriminator PASS = {ok}")

if __name__ == "__main__":
    main()
