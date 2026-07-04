#!/usr/bin/env python3
"""
H_9129 L5 hippocampal associative-store lane — 303M ENGINE-NATIVE rung(2).

Escalates STEP-0 (toy iid-random orthogonal codes → reach=1.0 exact, DIRECTIONAL) to REAL
anima ByteGPT-303M h1129 representations via the byte-exact core/decode.py engine forward
(== `anima evaluate --py` engine ops; a_eval_py_canonical). Frozen bar pre-registered in
PREREG.md (p7). The lane operator (DG pattern-separation + CA3 pattern-completion) is a numpy
substrate laid on top of ENGINE representations — rung(2) "measure on real 303M reps".

Uncheatable BIND test = Dušek–Eichenbaum transitive inference on a REAL corpus concept
co-occurrence graph:
  reachable   = within-chain non-adjacent (2-hop+), held-out, never a stored premise edge
  unreachable = cross-chain, count-matched, no stored path, held-out
Both share the same surface form. Controls: FORM baseline (raw 303M-rep cosine), SHUFFLE
(permute wiring; SAME reps/edges → isolates relation), LANE-OFF (empty store → causal).
"""
import os, sys, json, time, re
import numpy as np

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d   # byte-exact anima engine (bytegpt_decode.hexa twin)

CKPT   = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
CORPUS = os.path.join(_REPO, "archive", "data", "corpus.txt")
OUTDIR = os.path.dirname(__file__)

# ---- locked hyperparameters (PREREG.md) ----
SEED      = 20260705
N_CHAINS  = 8
CHAIN_LEN = 6
DIM       = 2048
ACTIVE    = 40
STEPS     = 6
KWTA      = 40
N_ITEMS   = N_CHAINS * CHAIN_LEN
rng = np.random.default_rng(SEED)

STOP = set("""the a an and or but if then else of to in on at for with as by from into over under
this that these those it its is are was were be been being have has had do does did will would
can could should may might must not no nor so than too very just also more most much many some
any all each every both few other such only own same about above after again against because
before below between during through until while your you they them their there here what when
where which who whom whose why how our out off down up we he she his her him me my mine ours
i am pm mr ms dr etc vs via per got get getbe really think know like well yeah okay something
things thing want need make made even still back come came going go went one two three""".split())

# ── engine-native 303M representation ────────────────────────────────────────
def bg_hidden_seq_W(W, ids, T):
    """Byte-identical to core/decode.py::bg_forward_last_W EXCEPT it returns the full
    pre-lnf residual-stream hidden [T,d] instead of the last-position head logits.
    Same weights, same ops (_bg_layernorm_rows / _bg_mha / _bg_gelu / _bg_apply_bind).
    The mean-pool over positions is the 303M concept representation."""
    dd = W["d"]; nlay = W["nlay"]; nh = W["nh"]
    ids = np.asarray(ids, dtype=np.int64)
    x = W["tok"][ids] + W["pos"][0:T]
    for Lr in range(nlay):
        nrm = d._bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, dd)
        aout = d._bg_mha(nrm, W["inW"][Lr], W["inB"][Lr], W["oW"][Lr], W["oB"][Lr], T, dd, nh)
        x = x + aout
        nrm = d._bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, dd)
        h4 = d._bg_gelu(nrm @ W["m0W"][Lr].T + W["m0B"][Lr])
        x = x + (h4 @ W["m2W"][Lr].T + W["m2B"][Lr])
    if W.get("bind"):
        x = d._bg_apply_bind(x, W["bind"], T, dd, nh)
    return x  # [T,d] pre-lnf residual stream

def rep303(W, word):
    ids = list(word.encode("utf-8", "surrogateescape"))
    H = bg_hidden_seq_W(W, ids, len(ids))   # [T,d]
    return H.mean(axis=0)                     # [d] mean-pooled concept vector

# ── real corpus concept co-occurrence graph ──────────────────────────────────
def load_lines():
    lines = []
    with open(CORPUS, "r", encoding="utf-8", errors="surrogateescape") as f:
        for ln in f:
            ln = ln.strip()
            if ln.startswith(("A:", "B:")):
                ln = ln[2:].strip()
            # english content lines only (>=3 ascii-word tokens)
            toks = re.findall(r"[a-z]{4,}", ln.lower())
            toks = [t for t in toks if t not in STOP]
            if len(toks) >= 3:
                lines.append(toks)
    return lines

def build_graph(lines):
    from collections import Counter
    freq = Counter(t for ln in lines for t in set(ln))
    # candidate vocab = frequent content words
    vocab = [w for w, c in freq.most_common(400) if c >= 6]
    vset = set(vocab)
    # line-level co-occurrence counts (undirected)
    co = {}
    for ln in lines:
        u = [t for t in set(ln) if t in vset]
        for a in range(len(u)):
            for b in range(a + 1, len(u)):
                k = (min(u[a], u[b]), max(u[a], u[b]))
                co[k] = co.get(k, 0) + 1
    return vocab, freq, co

def greedy_chains(vocab, freq, co):
    """Build N_CHAINS disjoint chains of CHAIN_LEN via greedy strongest-co-occurrence walk.
    Adjacent link = real strong corpus co-occurrence (the stored premise). Disjoint nodes."""
    adj = {}
    for (a, b), c in co.items():
        adj.setdefault(a, []).append((c, b))
        adj.setdefault(b, []).append((c, a))
    for w in adj:
        adj[w].sort(reverse=True)
    used = set()
    # seeds = most frequent words that still anchor a strong edge
    seeds = [w for w in vocab if w in adj]
    chains = []
    for seed in seeds:
        if len(chains) >= N_CHAINS:
            break
        if seed in used:
            continue
        chain = [seed]; used.add(seed)
        while len(chain) < CHAIN_LEN:
            cur = chain[-1]
            nxt = None
            for c, w in adj.get(cur, []):
                if w not in used and c >= 3:   # real co-occurrence >=3
                    nxt = w; break
            if nxt is None:
                break
            chain.append(nxt); used.add(nxt)
        if len(chain) == CHAIN_LEN:
            chains.append(chain)
        else:
            for w in chain:      # release a failed short chain's nodes
                used.discard(w)
    return chains

# ── DG pattern separation of the 303M representation → sparse CA3 code ────────
def kwta_vec(v, k):
    if k >= v.size:
        return (v > 0).astype(np.float32)
    idx = np.argpartition(v, -k)[-k:]
    out = np.zeros_like(v)
    pos = idx[v[idx] > 0]
    out[pos] = 1.0
    return out

def dg_codes(reps):
    """Fixed seeded random projection (DG expansion) of each 303M rep → kWTA sparse binary
    code. Content derives from the 303M rep, so correlated reps → overlapping codes (crosstalk
    PRESERVED = honest test); the projection is fixed/untrained (no handed advantage)."""
    n, dmod = reps.shape
    P = rng.standard_normal((DIM, dmod)).astype(np.float32) / np.sqrt(dmod)
    R = reps / (np.linalg.norm(reps, axis=1, keepdims=True) + 1e-9)
    drive = R @ P.T                      # [n, DIM]
    C = np.zeros((n, DIM), dtype=np.float32)
    for i in range(n):
        C[i] = kwta_vec(drive[i], ACTIVE)
    return C

def build_store(codes, successor):
    W = np.zeros((DIM, DIM), dtype=np.float32)
    for cur, nxt in successor.items():
        W += np.outer(codes[nxt], codes[cur])
    return W

def relatedness(W, codes, i, j):
    x = codes[i].copy(); cj = codes[j]
    cjn = np.linalg.norm(cj) + 1e-9; best = 0.0
    for _ in range(STEPS):
        x = kwta_vec(W @ x, KWTA)
        ov = float(x @ cj) / ((np.linalg.norm(x) + 1e-9) * cjn)
        if ov > best: best = ov
    return best

def form_cos(reps, i, j):
    a, b = reps[i], reps[j]
    return float(a @ b) / ((np.linalg.norm(a) + 1e-9) * (np.linalg.norm(b) + 1e-9))

def summarize(name, arr):
    return f"{name}: mean={arr.mean():.4f} std={arr.std():.4f} med={np.median(arr):.4f} n={len(arr)}"

def main():
    t0 = time.time()
    print("[1/5] loading real 303M h1129 engine ...", flush=True)
    W = d.bg_load(CKPT)
    assert d.bg_is_bytegpt(CKPT), "not bytegpt"
    print(f"      engine d={W['d']} nlay={W['nlay']} nh={W['nh']} vocab={W['vocab']}", flush=True)

    print("[2/5] building real corpus concept co-occurrence graph ...", flush=True)
    lines = load_lines()
    vocab, freq, co = build_graph(lines)
    chains = greedy_chains(vocab, freq, co)
    assert len(chains) == N_CHAINS, f"only {len(chains)} chains built (need {N_CHAINS})"
    items = [w for ch in chains for w in ch]
    assert len(items) == N_ITEMS
    idx = {w: k for k, w in enumerate(items)}
    print(f"      corpus lines={len(lines)} vocab={len(vocab)} chains={len(chains)}", flush=True)
    for c, ch in enumerate(chains):
        print(f"        chain{c}: {' -> '.join(ch)}", flush=True)

    def chain_of(k):  return k // CHAIN_LEN
    def pos_in(k):    return k % CHAIN_LEN

    print("[3/5] extracting REAL 303M representations for %d concepts ..." % N_ITEMS, flush=True)
    reps = np.zeros((N_ITEMS, W["d"]), dtype=np.float64)
    for k, w in enumerate(items):
        reps[k] = rep303(W, w)
    print(f"      reps done ({time.time()-t0:.1f}s)", flush=True)

    codes = dg_codes(reps)
    avg_overlap = np.mean([float(codes[a] @ codes[b]) / ACTIVE
                           for a in range(N_ITEMS) for b in range(a+1, N_ITEMS)])
    print(f"      mean pairwise code overlap = {avg_overlap:.4f} (0=orthogonal like toy; >0 = real crosstalk)", flush=True)

    # premise edges = adjacent within chain
    successor = {}
    for c in range(N_CHAINS):
        base = c * CHAIN_LEN
        for p in range(CHAIN_LEN - 1):
            successor[base + p] = base + p + 1

    # held-out pairs
    reachable, unreachable = [], []
    for c in range(N_CHAINS):
        base = c * CHAIN_LEN
        for a in range(CHAIN_LEN):
            for b in range(a + 2, CHAIN_LEN):
                reachable.append((base + a, base + b))
    seen = set()
    while len(unreachable) < len(reachable):
        i = int(rng.integers(N_ITEMS)); j = int(rng.integers(N_ITEMS))
        if chain_of(i) == chain_of(j): continue
        k = (min(i, j), max(i, j))
        if k in seen: continue
        seen.add(k); unreachable.append((i, j))

    print("[4/5] scoring FORM / STORE / SHUFFLE / LANE-OFF ...", flush=True)
    fr = np.array([form_cos(reps, i, j) for i, j in reachable])
    fu = np.array([form_cos(reps, i, j) for i, j in unreachable])

    Ws = build_store(codes, successor)
    sr = np.array([relatedness(Ws, codes, i, j) for i, j in reachable])
    su = np.array([relatedness(Ws, codes, i, j) for i, j in unreachable])

    keys = list(successor.keys()); vals = list(successor.values())
    perm = rng.permutation(len(vals))
    while any(perm[k] == k for k in range(len(perm))):   # derangement (destroy all wiring)
        perm = rng.permutation(len(vals))
    succ_sh = {keys[k]: vals[perm[k]] for k in range(len(keys))}
    Wsh = build_store(codes, succ_sh)
    shr = np.array([relatedness(Wsh, codes, i, j) for i, j in reachable])
    shu = np.array([relatedness(Wsh, codes, i, j) for i, j in unreachable])

    Woff = np.zeros((DIM, DIM), dtype=np.float32)
    lor = np.array([relatedness(Woff, codes, i, j) for i, j in reachable])
    lou = np.array([relatedness(Woff, codes, i, j) for i, j in unreachable])

    gaps = {}
    for (i, j), v in zip(reachable, sr):
        gaps.setdefault(pos_in(j) - pos_in(i), []).append(v)

    store_gap = float(sr.mean() - su.mean())
    form_gap  = float(fr.mean() - fu.mean())
    shuf_gap  = float(shr.mean() - shu.mean())
    loff_gap  = float(lor.mean() - lou.mean())
    ratio     = float(sr.mean() / (su.mean() + 1e-9))
    max_signal = float(max(sr.mean(), su.mean()))

    # ── PRE-REGISTERED verdict logic (PREREG.md — no post-hoc tuning) ──
    shuffle_collapsed = shuf_gap < 0.5 * store_gap if store_gap > 0 else True
    lane_off_collapsed = abs(loff_gap) < 0.05 and lor.mean() < 0.05
    fooled_by_form = not shuffle_collapsed
    handed = bool(abs(sr.mean() - 1.0) < 1e-6)

    if max_signal < 0.02:
        verdict = "RED"; tier = "floor (retrieves nothing)"
    elif store_gap > 0.50 and shuffle_collapsed and lane_off_collapsed:
        verdict = "GREEN"; tier = "BIND survives on real 303M substrate"
    elif store_gap < 0.50 or ratio < 1.5:
        verdict = "WALL"; tier = "collapses on real substrate (toy=7.88x)"
    else:
        verdict = "WALL"; tier = "ambiguous / control failed"

    L = []
    L.append("# H_9129 L5 hippocampal associative-store — 303M ENGINE-NATIVE rung(2)")
    L.append(f"ckpt={CKPT}")
    L.append(f"engine: real ByteGPT-303M h1129 d={W['d']} nlay={W['nlay']} nh={W['nh']} vocab={W['vocab']} (core/decode.py byte-exact, == anima evaluate --py ops)")
    L.append(f"seed={SEED} N_CHAINS={N_CHAINS} CHAIN_LEN={CHAIN_LEN} DIM={DIM} ACTIVE={ACTIVE} STEPS={STEPS} KWTA={KWTA}")
    L.append(f"rep = mean-pooled pre-lnf final-layer 303M hidden of the word bytes")
    L.append("")
    L.append("## real corpus concept chains (adjacent link = real strong co-occurrence = stored premise)")
    for c, ch in enumerate(chains):
        L.append(f"  chain{c}: {' -> '.join(ch)}")
    L.append(f"  mean pairwise DG-code overlap = {avg_overlap:.4f}  (toy STEP-0 = 0 orthogonal; >0 = REAL 303M crosstalk)")
    L.append("")
    L.append("## FORM baseline (raw 303M-rep cosine) — representation-geometry confound")
    L.append("  " + summarize("form_reachable  ", fr))
    L.append("  " + summarize("form_unreachable", fu))
    L.append(f"  form_gap = {form_gap:+.4f}")
    L.append("")
    L.append("## STORE lane (CA3 completion relatedness on real 303M codes)")
    L.append("  " + summarize("store_reachable  ", sr))
    L.append("  " + summarize("store_unreachable", su))
    L.append(f"  store_gap = {store_gap:+.4f}   ratio reach/unreach = {ratio:.2f}x")
    L.append("")
    L.append("## per-gap reachable (transitive distance)")
    for g in sorted(gaps):
        a = np.array(gaps[g]); L.append(f"  gap={g}: mean={a.mean():.4f} n={len(a)}")
    L.append("")
    L.append("## SHUFFLE ablation (permute wiring; SAME reps/edges) — decisive BIND control")
    L.append("  " + summarize("shuf_reachable  ", shr))
    L.append("  " + summarize("shuf_unreachable", shu))
    L.append(f"  shuf_gap = {shuf_gap:+.4f}")
    L.append("")
    L.append("## LANE-OFF ablation (empty store W=0) — causal check")
    L.append("  " + summarize("loff_reachable  ", lor))
    L.append("  " + summarize("loff_unreachable", lou))
    L.append(f"  loff_gap = {loff_gap:+.4f}")
    L.append("")
    L.append("## VERDICT (against PREREG.md frozen bar)")
    L.append(f"  store_gap>0.50            = {store_gap>0.50}  (store_gap={store_gap:.4f})")
    L.append(f"  shuffle_collapsed         = {shuffle_collapsed}  (shuf_gap={shuf_gap:.4f} vs 0.5*store_gap={0.5*store_gap:.4f})")
    L.append(f"  lane_off_collapsed        = {lane_off_collapsed}  (loff_gap={loff_gap:.4f}, loff_reach_mean={lor.mean():.4f})")
    L.append(f"  fooled_by_form            = {fooled_by_form}")
    L.append(f"  handed_advantage(reach==1)= {handed}")
    L.append(f"  engine_native             = True (real 303M h1129 reps via core/decode.py)")
    L.append(f"  >>> VERDICT = {verdict}  ({tier})")

    out = "\n".join(L)
    print("\n" + out, flush=True)
    with open(os.path.join(OUTDIR, "result.txt"), "w") as f:
        f.write(out + "\n")
    res = dict(verdict=verdict, tier=tier, engine_native=True,
               store_gap=store_gap, form_gap=form_gap, shuf_gap=shuf_gap, loff_gap=loff_gap,
               ratio=ratio, store_reach=float(sr.mean()), store_unreach=float(su.mean()),
               shuffle_collapsed=bool(shuffle_collapsed), lane_off_collapsed=bool(lane_off_collapsed),
               fooled_by_form=bool(fooled_by_form), handed_advantage=bool(handed),
               mean_code_overlap=float(avg_overlap), max_signal=max_signal,
               chains=chains, n_reach=len(reachable), n_unreach=len(unreachable),
               seconds=round(time.time()-t0, 1))
    with open(os.path.join(OUTDIR, "result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n[5/5] done {time.time()-t0:.1f}s  verdict={verdict}", flush=True)

if __name__ == "__main__":
    main()
