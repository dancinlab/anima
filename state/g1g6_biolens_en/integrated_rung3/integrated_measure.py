#!/usr/bin/env python3
"""
H_9129 INTEGRATED rung-3 — WIRED engine-native measurement of the 3-component lane:
  L1 PFC variable-binding (core/wm_bind_lane.py)  ×
  L2 basal-ganglia content-gate (core/content_gate_lane.py)  ×
  L5 hippocampal completion (core/hippo_lane.py, reused, already GREEN #2996)
over REAL ByteGPT-303M h1129 representations via core/decode.py (== `anima evaluate --py`
2-production ops, a_eval_py_canonical). Calls the LIVE core/ lane ops directly (not a
throwaway harness). Frozen bar = PREREG.md; no post-hoc tuning.
"""
import os, sys, re, json, time
import numpy as np

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d
import wm_bind_lane as L1        # LIVE core/ lane op
import content_gate_lane as L2   # LIVE core/ lane op
import hippo_lane as L5          # LIVE core/ lane op (already GREEN)

CKPT   = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
CORPUS = os.path.join(_REPO, "archive", "data", "corpus.txt")
OUTDIR = os.path.dirname(__file__)

# ── frozen hyperparameters (PREREG.md) ──
SEED, N_CHAINS, CHAIN_LEN = 20260705, 8, 6
DIM, ACTIVE, STEPS, KWTA  = 2048, 40, 6, 40
NOGO, E_SCALE, PREPROC    = 0.30, 6.0, "center_zscore"
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
def cof(k): return k // CHAIN_LEN
def pin(k): return k % CHAIN_LEN


def build_keys(reps, role_bind):
    """L1 PFC: key = DG(center_zscore( role[pos] ⊛ unit(rep) )) if role_bind else
    DG(center_zscore(rep)). Position role vectors are fixed seeded HRR roles."""
    dim_rep = reps.shape[1]
    if role_bind:
        rng = np.random.default_rng(SEED + 4242)
        roles = rng.standard_normal((CHAIN_LEN, dim_rep))
        bound = np.zeros_like(reps)
        for k in range(reps.shape[0]):
            bound[k] = L1.hrr_bind(L1.unit(roles[pin(k)]), L1.unit(reps[k]))
        base = bound
    else:
        base = reps
    Rw = L5.dg_decorrelate(base, PREPROC)          # center_zscore (or raw)
    return L5.dg_codes(Rw, DIM, ACTIVE, SEED)

def build_keys_raw(reps, role_bind):
    """RAW control: PREPROC=raw (no centering)."""
    dim_rep = reps.shape[1]
    if role_bind:
        rng = np.random.default_rng(SEED + 4242)
        roles = rng.standard_normal((CHAIN_LEN, dim_rep))
        base = np.zeros_like(reps)
        for k in range(reps.shape[0]):
            base[k] = L1.hrr_bind(L1.unit(roles[pin(k)]), L1.unit(reps[k]))
    else:
        base = reps
    Rw = L5.dg_decorrelate(base, "raw")
    return L5.dg_codes(Rw, DIM, ACTIVE, SEED)


def rel(store, codes, i, j, steps):
    return L5.hippo_relatedness(store, codes, i, j, steps, KWTA)


def measure(codes, edges, reach, unreach, steps):
    W = L5.hippo_build_store(codes, edges, DIM)
    r = [rel(W, codes, i, j, steps) for i, j in reach]
    u = [rel(W, codes, i, j, steps) for i, j in unreach]
    return m(r), m(u), m(r) - m(u)


def main():
    t0 = time.time()
    print("[1/5] loading real 303M h1129 engine ...", flush=True)
    W = d.bg_load(CKPT); assert d.bg_is_bytegpt(CKPT)
    print(f"      d={W['d']} nlay={W['nlay']} nh={W['nh']}", flush=True)

    print("[2/5] corpus graph + chains ...", flush=True)
    v, co = build_graph(load_lines()); chains = greedy_chains(v, co)
    assert len(chains) == N_CHAINS, f"only {len(chains)} chains"
    items = [w for ch in chains for w in ch]

    print("[3/5] extracting REAL 303M reps ...", flush=True)
    reps = np.stack([rep303(W, w) for w in items])
    print(f"      reps done ({time.time()-t0:.1f}s)", flush=True)

    # genuine premise edges (adjacent) + distractor cross-chain edges (equal count)
    genuine = [(c*CHAIN_LEN+p, c*CHAIN_LEN+p+1) for c in range(N_CHAINS) for p in range(CHAIN_LEN-1)]
    rng = np.random.default_rng(SEED)
    distractors, seen = [], set(genuine)
    while len(distractors) < len(genuine):
        i = int(rng.integers(N_ITEMS)); j = int(rng.integers(N_ITEMS))
        if cof(i) == cof(j): continue
        k = (i, j)
        if k in seen: continue
        seen.add(k); distractors.append(k)

    def strength(i, j):
        a, b = items[i], items[j]
        return float(co.get((min(a, b), max(a, b)), 0))

    # ── L2 content-gate over candidate pool ──
    cand = [(i, j, strength(i, j)) for (i, j) in genuine] + \
           [(i, j, strength(i, j)) for (i, j) in distractors]
    admitted_on  = L2.cgate_admit(cand, NOGO, E_SCALE)     # gate ON
    admitted_off = [(i, j) for (i, j, s) in cand]          # gate OFF (admit all)
    gs = L2.gate_stats(cand, NOGO, E_SCALE)

    # ── held-out pair sets ──
    reach = [(c*CHAIN_LEN+a, c*CHAIN_LEN+b) for c in range(N_CHAINS)
             for a in range(CHAIN_LEN) for b in range(a+2, CHAIN_LEN)]
    unreach, seen2 = [], set()
    while len(unreach) < len(reach):
        i = int(rng.integers(N_ITEMS)); j = int(rng.integers(N_ITEMS))
        if cof(i) == cof(j): continue
        k = (min(i, j), max(i, j))
        if k in seen2: continue
        seen2.add(k); unreach.append((i, j))
    assert all((i, j) not in set(genuine) for i, j in reach), "reach leaked a stored edge"

    print("[4/5] FULL + ablation measurements (LIVE core/ ops) ...", flush=True)
    # FULL = L1 on, L2 on, L5 multi-step
    keys_full = build_keys(reps, role_bind=True)
    fr, fu, fg = measure(keys_full, admitted_on, reach, unreach, STEPS)

    # L1-OFF (no role bind)
    keys_noL1 = build_keys(reps, role_bind=False)
    a1r, a1u, a1g = measure(keys_noL1, admitted_on, reach, unreach, STEPS)

    # L2-OFF (admit all incl distractors)  — keys same as FULL
    a2r, a2u, a2g = measure(keys_full, admitted_off, reach, unreach, STEPS)

    # L5-OFF (single hop)
    a5r, a5u, a5g = measure(keys_full, admitted_on, reach, unreach, 1)

    # RAW (no centering)
    keys_raw = build_keys_raw(reps, role_bind=True)
    rr, ru, rg = measure(keys_raw, admitted_on, reach, unreach, STEPS)

    # LANE-OFF (empty store)
    off = np.zeros((DIM, DIM), dtype=np.float32)
    lor = [rel(off, keys_full, i, j, STEPS) for i, j in reach]

    def drop(ablg): return (fg - ablg) / (fg + 1e-9)
    d1, d2, d5 = drop(a1g), drop(a2g), drop(rg if False else a5g)
    draw = drop(rg)

    causal_L1 = d1 >= 0.5
    causal_L2 = d2 >= 0.5
    causal_L5 = d5 >= 0.5
    centering = draw >= 0.5
    gap_ok = fg > 0.15
    all_causal = causal_L1 and causal_L2 and causal_L5

    if gap_ok and all_causal and centering:
        verdict = "GREEN-WIRED (faculty scope)"
    elif gap_ok:
        verdict = "DIRECTIONAL (component INERT or centering not load-bearing)"
    else:
        verdict = "WALL (no held-out lift)"

    L = []
    L.append("# H_9129 INTEGRATED rung-3 — engine-native WIRED measurement (303M h1129)")
    L.append(f"ckpt={CKPT}")
    L.append(f"engine: real ByteGPT-303M d={W['d']} nlay={W['nlay']} nh={W['nh']} (core/decode.py == anima evaluate --py ops)")
    L.append(f"seed={SEED} DIM={DIM} ACTIVE={ACTIVE} STEPS={STEPS} KWTA={KWTA} NOGO={NOGO} E_SCALE={E_SCALE} preproc={PREPROC}")
    L.append(f"chains={N_CHAINS} len={CHAIN_LEN}; genuine_edges={len(genuine)} distractors={len(distractors)}")
    L.append("")
    L.append("## chains")
    for c, ch in enumerate(chains): L.append(f"  chain{c}: {' -> '.join(ch)}")
    L.append("")
    L.append("## L2 content-gate (Go/NoGo over genuine premises + distractors)")
    L.append(f"  admitted_ON={len(admitted_on)}  admitted_OFF(all)={len(admitted_off)}")
    L.append(f"  gate_stats: tp(genuine admitted)={gs['tp']} fp(distractor admitted)={gs['fp']} "
             f"tn(distractor rejected)={gs['tn']} fn(genuine rejected)={gs['fn']}")
    L.append("")
    L.append("## reach (same-chain gap>=2, held-out)  vs  unreach (cross-chain)")
    L.append(f"  FULL (L1+L2+L5):  reach={fr:.4f}  unreach={fu:.4f}  gap={fg:+.4f}")
    L.append(f"  lane_off(empty W): reach={m(lor):.4f}")
    L.append("")
    L.append("## ABLATIONS (drop = fraction of FULL gap lost; CAUSAL iff drop>=0.50)")
    L.append(f"  L1-OFF (no role-bind):    reach={a1r:.4f} unreach={a1u:.4f} gap={a1g:+.4f}  drop={d1:+.3f}  causal={causal_L1}")
    L.append(f"  L2-OFF (admit distractrs):reach={a2r:.4f} unreach={a2u:.4f} gap={a2g:+.4f}  drop={d2:+.3f}  causal={causal_L2}")
    L.append(f"  L5-OFF (single hop):      reach={a5r:.4f} unreach={a5u:.4f} gap={a5g:+.4f}  drop={d5:+.3f}  causal={causal_L5}")
    L.append(f"  RAW  (no centering):      reach={rr:.4f} unreach={ru:.4f} gap={rg:+.4f}  drop={draw:+.3f}  centering_load_bearing={centering}")
    L.append("")
    L.append("## VERDICT (vs PREREG.md frozen bar)")
    L.append(f"  gap>0.15                = {gap_ok}  (gap={fg:.4f})")
    L.append(f"  all 3 ablations CAUSAL  = {all_causal}  (L1={causal_L1} L2={causal_L2} L5={causal_L5})")
    L.append(f"  centering load-bearing  = {centering}")
    L.append(f"  engine_native           = True (real 303M h1129 reps via core/decode.py)")
    L.append(f"  LIVE-OP                 = True (calls core/wm_bind_lane + content_gate_lane + hippo_lane)")
    L.append(f"  >>> INTEGRATED rung-3 = {verdict}")
    out = "\n".join(L)
    print("\n" + out, flush=True)
    with open(os.path.join(OUTDIR, "result_integrated.txt"), "w") as f: f.write(out + "\n")
    res = dict(verdict=verdict, engine_native=True, gap=fg, reach=fr, unreach=fu,
               lane_off=m(lor),
               abl_L1=dict(gap=a1g, drop=d1, causal=bool(causal_L1)),
               abl_L2=dict(gap=a2g, drop=d2, causal=bool(causal_L2)),
               abl_L5=dict(gap=a5g, drop=d5, causal=bool(causal_L5)),
               raw=dict(gap=rg, drop=draw, centering_load_bearing=bool(centering)),
               gate_stats=gs, gap_ok=bool(gap_ok), all_causal=bool(all_causal),
               chains=chains, seconds=round(time.time()-t0, 1))
    with open(os.path.join(OUTDIR, "result_integrated.json"), "w") as f: json.dump(res, f, indent=2)
    print(f"\n[5/5] done {time.time()-t0:.1f}s verdict={verdict}", flush=True)


if __name__ == "__main__":
    main()
