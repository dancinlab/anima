#!/usr/bin/env python3
"""
H_9129 L5 hippocampal associative-store — rung(3) NOVEL-CHAIN vs STORED-RECALL discriminator.

★ MANDATORY gate for GREEN-cement (task frozen bar): isolate that the reach>>unreach lift is
G1 *novel 2-edge chaining* and NOT G2 *stored recall* (MLC / H_1835 trap guard). Runs over
REAL ByteGPT-303M h1129 representations via core/decode.py (== `anima evaluate --py` engine
ops, a_eval_py_canonical), center_zscore de-anisotropy read (rung-2 GREEN lens, pre-registered).

Arms (all form-matched, held-out relative to the stored premise edges):
  RECALL      (gap=1, DIRECTLY STORED premise edges)   -> G2 stored recall (positive control)
  NOVEL-CHAIN (gap>=2, NEVER stored, needs >=2 edges)  -> the G1 claim
  UNREACH     (cross-chain, no path)                    -> chance floor
  FORM        raw 303M-rep cosine                       -> representation-geometry confound

★ LESION broken-chain control (decisive, within-store):
  Knock out ONE mid-chain edge (m -> m+1) per chain. Same reps, same codes, same store minus
  one link. Reachable gap>=2 pairs split by whether their transitive path CROSSES the lesion:
    path_broken (a<=m<m+1<=b)  MUST collapse  (proves completion follows the actual stored path)
    path_intact (both on one side of the lesion) MUST survive
  If completion were stored-recall or a form artifact, lesion LOCATION would not matter.
  If path_broken collapses while path_intact survives => genuine sequential 2-edge+ chaining.

SHUFFLE (derangement of wiring, same reps/edges) and LANE-OFF (empty store) kept as standard
BIND/causal controls. No post-hoc tuning: bar frozen in PREREG_rung3.md.
"""
import os, sys, json, time, re
import numpy as np

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d   # byte-exact anima engine (== anima evaluate --py ops)

CKPT   = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
CORPUS = os.path.join(_REPO, "archive", "data", "corpus.txt")
OUTDIR = os.path.dirname(__file__)

# ---- locked hyperparameters (identical to rung-2 PREREG) ----
SEED      = 20260705
N_CHAINS  = 8
CHAIN_LEN = 6
DIM       = 2048
ACTIVE    = 40
STEPS     = 6
KWTA      = 40
N_ITEMS   = N_CHAINS * CHAIN_LEN
PREPROC   = "center_zscore"   # rung-2 GREEN lens (pre-registered de-anisotropy)
rng = np.random.default_rng(SEED)

STOP = set("""the a an and or but if then else of to in on at for with as by from into over under
this that these those it its is are was were be been being have has had do does did will would
can could should may might must not no nor so than too very just also more most much many some
any all each every both few other such only own same about above after again against because
before below between during through until while your you they them their there here what when
where which who whom whose why how our out off down up we he she his her him me my mine ours
i am pm mr ms dr etc vs via per got get getbe really think know like well yeah okay something
things thing want need make made even still back come came going go went one two three""".split())

# ── engine-native 303M representation (byte-exact to core/decode.py ops) ──────
def bg_hidden_seq_W(W, ids, T):
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
    return x

def rep303(W, word):
    ids = list(word.encode("utf-8", "surrogateescape"))
    H = bg_hidden_seq_W(W, ids, len(ids))
    return H.mean(axis=0)

# ── real corpus concept co-occurrence graph (identical to rung-2) ────────────
def load_lines():
    lines = []
    with open(CORPUS, "r", encoding="utf-8", errors="surrogateescape") as f:
        for ln in f:
            ln = ln.strip()
            if ln.startswith(("A:", "B:")):
                ln = ln[2:].strip()
            toks = re.findall(r"[a-z]{4,}", ln.lower())
            toks = [t for t in toks if t not in STOP]
            if len(toks) >= 3:
                lines.append(toks)
    return lines

def build_graph(lines):
    from collections import Counter
    freq = Counter(t for ln in lines for t in set(ln))
    vocab = [w for w, c in freq.most_common(400) if c >= 6]
    vset = set(vocab)
    co = {}
    for ln in lines:
        u = [t for t in set(ln) if t in vset]
        for a in range(len(u)):
            for b in range(a + 1, len(u)):
                k = (min(u[a], u[b]), max(u[a], u[b]))
                co[k] = co.get(k, 0) + 1
    return vocab, freq, co

def greedy_chains(vocab, freq, co):
    adj = {}
    for (a, b), c in co.items():
        adj.setdefault(a, []).append((c, b))
        adj.setdefault(b, []).append((c, a))
    for w in adj:
        adj[w].sort(reverse=True)
    used = set()
    seeds = [w for w in vocab if w in adj]
    chains = []
    for seed in seeds:
        if len(chains) >= N_CHAINS:
            break
        if seed in used:
            continue
        chain = [seed]; used.add(seed)
        while len(chain) < CHAIN_LEN:
            cur = chain[-1]; nxt = None
            for c, w in adj.get(cur, []):
                if w not in used and c >= 3:
                    nxt = w; break
            if nxt is None:
                break
            chain.append(nxt); used.add(nxt)
        if len(chain) == CHAIN_LEN:
            chains.append(chain)
        else:
            for w in chain:
                used.discard(w)
    return chains

# ── DG pattern separation + CA3 completion ───────────────────────────────────
def kwta_vec(v, k):
    if k >= v.size:
        return (v > 0).astype(np.float32)
    idx = np.argpartition(v, -k)[-k:]
    out = np.zeros_like(v)
    pos = idx[v[idx] > 0]
    out[pos] = 1.0
    return out

def preprocess(reps, mode):
    R = reps.copy()
    if mode == "raw":
        return R
    mu = R.mean(axis=0, keepdims=True)
    if mode == "center":
        return R - mu
    if mode == "center_zscore":
        Rc = R - mu; sd = Rc.std(axis=0, keepdims=True) + 1e-6; return Rc / sd
    raise ValueError(mode)

def dg_codes(reps, proj_rng):
    n, dm = reps.shape
    P = proj_rng.standard_normal((DIM, dm)).astype(np.float32) / np.sqrt(dm)
    R = reps / (np.linalg.norm(reps, axis=1, keepdims=True) + 1e-9)
    drive = R @ P.T
    return np.stack([kwta_vec(drive[i], ACTIVE) for i in range(n)])

def build_store(codes, edges):
    """edges = list of (cur, nxt) directed premise links."""
    W = np.zeros((DIM, DIM), dtype=np.float32)
    for cur, nxt in edges:
        W += np.outer(codes[nxt], codes[cur])
    return W

def relatedness(W, codes, i, j):
    x = codes[i].copy(); cj = codes[j]
    cjn = np.linalg.norm(cj) + 1e-9; best = 0.0
    for _ in range(STEPS):
        x = kwta_vec(W @ x, KWTA)
        ov = float(x @ cj) / ((np.linalg.norm(x) + 1e-9) * cjn)
        if ov > best:
            best = ov
    return best

def form_cos(reps, i, j):
    a, b = reps[i], reps[j]
    return float(a @ b) / ((np.linalg.norm(a) + 1e-9) * (np.linalg.norm(b) + 1e-9))

def summarize(name, arr):
    if len(arr) == 0:
        return f"{name}: (empty)"
    arr = np.asarray(arr)
    return f"{name}: mean={arr.mean():.4f} std={arr.std():.4f} med={np.median(arr):.4f} n={len(arr)}"

def mean_of(arr):
    return float(np.mean(arr)) if len(arr) else float("nan")


def main():
    t0 = time.time()
    print("[1/6] loading real 303M h1129 engine ...", flush=True)
    W = d.bg_load(CKPT)
    assert d.bg_is_bytegpt(CKPT), "not bytegpt"
    print(f"      engine d={W['d']} nlay={W['nlay']} nh={W['nh']} vocab={W['vocab']}", flush=True)

    print("[2/6] building real corpus concept co-occurrence graph ...", flush=True)
    lines = load_lines()
    vocab, freq, co = build_graph(lines)
    chains = greedy_chains(vocab, freq, co)
    assert len(chains) == N_CHAINS, f"only {len(chains)} chains built"
    items = [w for ch in chains for w in ch]
    assert len(items) == N_ITEMS

    def chain_of(k): return k // CHAIN_LEN
    def pos_in(k):   return k % CHAIN_LEN

    print("[3/6] extracting REAL 303M representations ...", flush=True)
    reps = np.zeros((N_ITEMS, W["d"]), dtype=np.float64)
    for k, w in enumerate(items):
        reps[k] = rep303(W, w)
    print(f"      reps done ({time.time()-t0:.1f}s)", flush=True)

    R = preprocess(reps, PREPROC)
    proj_rng = np.random.default_rng(SEED)
    codes = dg_codes(R, proj_rng)
    avg_overlap = float(np.mean([float(codes[a] @ codes[b]) / ACTIVE
                                 for a in range(N_ITEMS) for b in range(a+1, N_ITEMS)]))

    # premise edges = adjacent within-chain (gap=1) — the ONLY thing stored
    full_edges = []
    for c in range(N_CHAINS):
        base = c * CHAIN_LEN
        for p in range(CHAIN_LEN - 1):
            full_edges.append((base + p, base + p + 1))
    stored_set = set(full_edges)

    # ── pair sets ─────────────────────────────────────────────────────────────
    recall_pairs = []      # gap=1, directly stored (G2 recall positive control)
    novel_pairs  = []      # gap>=2, never stored (G1 novel chain)
    for c in range(N_CHAINS):
        base = c * CHAIN_LEN
        for a in range(CHAIN_LEN):
            recall_pairs += [(base + a, base + a + 1)] if a + 1 < CHAIN_LEN else []
            for b in range(a + 2, CHAIN_LEN):
                novel_pairs.append((base + a, base + b))
    # sanity: none of the novel pairs is a stored edge
    assert all((i, j) not in stored_set for i, j in novel_pairs), "novel pair leaked into store!"

    unreach = []
    seen = set()
    while len(unreach) < len(novel_pairs):
        i = int(rng.integers(N_ITEMS)); j = int(rng.integers(N_ITEMS))
        if chain_of(i) == chain_of(j):
            continue
        k = (min(i, j), max(i, j))
        if k in seen:
            continue
        seen.add(k); unreach.append((i, j))

    print("[4/6] scoring FORM / RECALL / NOVEL-CHAIN / UNREACH ...", flush=True)
    Wfull = build_store(codes, full_edges)
    fr = [form_cos(R, i, j) for i, j in novel_pairs]
    fu = [form_cos(R, i, j) for i, j in unreach]
    rc = [relatedness(Wfull, codes, i, j) for i, j in recall_pairs]   # G2 recall
    nc = [relatedness(Wfull, codes, i, j) for i, j in novel_pairs]    # G1 novel-chain
    ur = [relatedness(Wfull, codes, i, j) for i, j in unreach]

    # per-gap for novel-chain
    gaps = {}
    for (i, j), v in zip(novel_pairs, nc):
        gaps.setdefault(pos_in(j) - pos_in(i), []).append(v)

    # ── SHUFFLE (derangement of successor targets, same reps/edges) ───────────
    print("[5/6] SHUFFLE / LANE-OFF / LESION broken-chain controls ...", flush=True)
    curs = [e[0] for e in full_edges]; nxts = [e[1] for e in full_edges]
    perm = rng.permutation(len(nxts))
    while any(perm[k] == k for k in range(len(perm))):
        perm = rng.permutation(len(nxts))
    sh_edges = [(curs[k], nxts[perm[k]]) for k in range(len(curs))]
    Wsh = build_store(codes, sh_edges)
    shr = [relatedness(Wsh, codes, i, j) for i, j in novel_pairs]
    shu = [relatedness(Wsh, codes, i, j) for i, j in unreach]

    # ── LANE-OFF (empty store) ────────────────────────────────────────────────
    Woff = np.zeros((DIM, DIM), dtype=np.float32)
    lor = [relatedness(Woff, codes, i, j) for i, j in novel_pairs]

    # ── LESION broken-chain control ───────────────────────────────────────────
    # Knock out the middle edge (m -> m+1), m = 2, in EVERY chain. Same store minus one link/chain.
    M = 2   # lesion the (pos2 -> pos3) edge in each chain
    lesion_edges = [e for e in full_edges
                    if not (pos_in(e[0]) == M and pos_in(e[1]) == M + 1)]
    Wles = build_store(codes, lesion_edges)
    # split novel pairs by whether their path crosses the lesion (a<=M and b>=M+1, same chain)
    path_broken, path_intact = [], []
    for (i, j) in novel_pairs:
        a, b = pos_in(i), pos_in(j)
        if a <= M and b >= M + 1:
            path_broken.append((i, j))
        else:
            path_intact.append((i, j))
    lb = [relatedness(Wles, codes, i, j) for i, j in path_broken]
    li = [relatedness(Wles, codes, i, j) for i, j in path_intact]
    # baseline of the SAME pairs under the intact full store (isolates the lesion effect)
    lb0 = [relatedness(Wfull, codes, i, j) for i, j in path_broken]
    li0 = [relatedness(Wfull, codes, i, j) for i, j in path_intact]

    # ── metrics ───────────────────────────────────────────────────────────────
    m_recall = mean_of(rc); m_novel = mean_of(nc); m_unreach = mean_of(ur)
    m_form_r = mean_of(fr); m_form_u = mean_of(fu)
    m_shuf_r = mean_of(shr); m_shuf_u = mean_of(shu)
    m_loff = mean_of(lor)
    store_gap = m_novel - m_unreach
    form_gap  = m_form_r - m_form_u
    shuf_gap  = m_shuf_r - m_shuf_u
    ratio     = m_novel / (m_unreach + 1e-9)
    m_pb = mean_of(lb); m_pi = mean_of(li); m_pb0 = mean_of(lb0); m_pi0 = mean_of(li0)

    # ── PRE-REGISTERED discriminator logic (PREREG_rung3.md) ──────────────────
    shuffle_collapsed  = shuf_gap < 0.5 * store_gap if store_gap > 0 else True
    lane_off_collapsed = m_loff < 0.05
    # novel-chain lifts >> unreach (the reach>>unreach frozen bar, gap>0.5)
    novel_lift_ok = store_gap > 0.50
    # NOVEL-vs-RECALL: the discriminator's core. NOVEL-CHAIN must genuinely lift (not floor),
    # i.e. the store supplies the 2-edge chain. (recall is a positive control that store works.)
    recall_works = m_recall > 0.50
    # LESION isolation: path_broken collapses AND path_intact survives => genuine chaining,
    # NOT stored recall / form (lesion location matters only if completion walks the path).
    lesion_broken_collapses = (m_pb0 - m_pb) > 0.50 and m_pb < 0.50
    lesion_intact_survives  = m_pi > 0.50 and (m_pi0 - m_pi) < 0.20
    lesion_isolates = lesion_broken_collapses and lesion_intact_survives
    novel_not_recall = novel_lift_ok and lesion_isolates   # G1 chaining isolated from G2 recall

    if max(m_novel, m_unreach) < 0.02:
        verdict = "RED"; tier = "floor (retrieves nothing)"
    elif novel_lift_ok and shuffle_collapsed and lane_off_collapsed and novel_not_recall:
        verdict = "DISCRIMINATOR-PASS"; tier = "novel 2-edge chaining isolated from stored recall"
    elif novel_lift_ok and not lesion_isolates:
        verdict = "RECALL-OR-FORM"; tier = "lift present but lesion control fails (not genuine chaining)"
    else:
        verdict = "WALL"; tier = "novel-chain does not lift over unreachable"

    L = []
    L.append("# H_9129 L5 rung(3) — NOVEL-CHAIN vs STORED-RECALL discriminator (303M engine-native)")
    L.append(f"ckpt={CKPT}")
    L.append(f"engine: real ByteGPT-303M h1129 d={W['d']} nlay={W['nlay']} nh={W['nh']} (core/decode.py == anima evaluate --py ops)")
    L.append(f"seed={SEED} preproc={PREPROC} DIM={DIM} ACTIVE={ACTIVE} STEPS={STEPS} KWTA={KWTA}")
    L.append(f"stored premises = {len(full_edges)} adjacent (gap=1) edges ONLY; DG-code overlap={avg_overlap:.4f}")
    L.append("")
    L.append("## chains")
    for c, ch in enumerate(chains):
        L.append(f"  chain{c}: {' -> '.join(ch)}")
    L.append("")
    L.append("## FORM baseline (raw 303M-rep cosine, novel pairs)")
    L.append("  " + summarize("form_novel  ", fr))
    L.append("  " + summarize("form_unreach", fu))
    L.append(f"  form_gap = {form_gap:+.4f}")
    L.append("")
    L.append("## RECALL (gap=1 DIRECTLY STORED) — G2 stored-recall positive control")
    L.append("  " + summarize("recall(stored gap=1)", rc))
    L.append("")
    L.append("## NOVEL-CHAIN (gap>=2 NEVER stored) — G1 claim   vs   UNREACH (cross-chain)")
    L.append("  " + summarize("novel_chain ", nc))
    L.append("  " + summarize("unreach     ", ur))
    L.append(f"  store_gap (novel-unreach) = {store_gap:+.4f}   ratio = {ratio:.2f}x")
    L.append("  per-gap novel-chain (transitive distance):")
    for g in sorted(gaps):
        a = np.array(gaps[g]); L.append(f"    gap={g}: mean={a.mean():.4f} n={len(a)}")
    L.append("")
    L.append("## SHUFFLE (derangement of wiring; SAME reps/edges)")
    L.append("  " + summarize("shuf_novel  ", shr))
    L.append("  " + summarize("shuf_unreach", shu))
    L.append(f"  shuf_gap = {shuf_gap:+.4f}")
    L.append("")
    L.append("## LANE-OFF (empty store W=0)")
    L.append("  " + summarize("loff_novel  ", lor))
    L.append("")
    L.append(f"## LESION broken-chain control (knock out edge pos{M}->pos{M+1} in every chain)")
    L.append("  path_broken = novel pairs whose transitive path CROSSES the lesion (must collapse)")
    L.append("  path_intact = novel pairs entirely on one side of the lesion (must survive)")
    L.append("  " + summarize("path_broken @lesioned store", lb))
    L.append("  " + summarize("path_broken @intact store  ", lb0) + "  (baseline)")
    L.append("  " + summarize("path_intact @lesioned store", li))
    L.append("  " + summarize("path_intact @intact store  ", li0) + "  (baseline)")
    L.append(f"  lesion drop on broken paths = {m_pb0 - m_pb:+.4f}   on intact paths = {m_pi0 - m_pi:+.4f}")
    L.append("")
    L.append("## DISCRIMINATOR VERDICT (against PREREG_rung3.md frozen bar)")
    L.append(f"  novel_lift_ok (store_gap>0.50)         = {novel_lift_ok}  (store_gap={store_gap:.4f})")
    L.append(f"  recall_works (positive control >0.50)  = {recall_works}  (recall={m_recall:.4f})")
    L.append(f"  shuffle_collapsed                      = {shuffle_collapsed}  (shuf_gap={shuf_gap:.4f})")
    L.append(f"  lane_off_collapsed                     = {lane_off_collapsed}  (loff={m_loff:.4f})")
    L.append(f"  lesion_broken_collapses                = {lesion_broken_collapses}  (drop={m_pb0-m_pb:.4f}, resid={m_pb:.4f})")
    L.append(f"  lesion_intact_survives                 = {lesion_intact_survives}  (intact={m_pi:.4f}, drop={m_pi0-m_pi:.4f})")
    L.append(f"  >>> novel_NOT_recall (G1 isolated)     = {novel_not_recall}")
    L.append(f"  >>> engine_native = True (real 303M h1129 reps via core/decode.py)")
    L.append(f"  >>> DISCRIMINATOR = {verdict}  ({tier})")

    out = "\n".join(L)
    print("\n" + out, flush=True)
    with open(os.path.join(OUTDIR, "result_discriminator.txt"), "w") as f:
        f.write(out + "\n")
    res = dict(
        verdict=verdict, tier=tier, engine_native=True, preproc=PREPROC,
        recall=m_recall, novel_chain=m_novel, unreach=m_unreach, store_gap=store_gap,
        ratio=ratio, form_gap=form_gap, shuf_gap=shuf_gap, loff=m_loff,
        path_broken_lesioned=m_pb, path_broken_intact=m_pb0,
        path_intact_lesioned=m_pi, path_intact_intact=m_pi0,
        lesion_drop_broken=m_pb0 - m_pb, lesion_drop_intact=m_pi0 - m_pi,
        novel_lift_ok=bool(novel_lift_ok), recall_works=bool(recall_works),
        shuffle_collapsed=bool(shuffle_collapsed), lane_off_collapsed=bool(lane_off_collapsed),
        lesion_broken_collapses=bool(lesion_broken_collapses),
        lesion_intact_survives=bool(lesion_intact_survives),
        novel_not_recall=bool(novel_not_recall),
        mean_code_overlap=avg_overlap, n_recall=len(recall_pairs), n_novel=len(novel_pairs),
        n_unreach=len(unreach), n_path_broken=len(path_broken), n_path_intact=len(path_intact),
        chains=chains, seconds=round(time.time() - t0, 1))
    with open(os.path.join(OUTDIR, "result_discriminator.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n[6/6] done {time.time()-t0:.1f}s  verdict={verdict}", flush=True)


if __name__ == "__main__":
    main()
