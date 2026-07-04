#!/usr/bin/env python3
"""
H_9129 rung-2 — ARM B: integrated lane on REAL 303M reps AND a REAL corpus
relation graph (co-occurrence), not a synthetic permutation topology.

Arm A grounded the SYMBOLS in the engine (real 303M reps) but the relation
topology (color->material->size) was a random permutation. Arm B additionally
grounds the RELATIONS in the real training-distribution corpus
(core/testdata/clm_mid_5lang_c4.txt + flores5_dev_devtest.txt): the a[] / b[]
mappings are the cross-pool TOP-COLLOCATE (argmax line-level co-occurrence),
i.e. the actual relational structure of the corpus. Everything else is identical
to integrated_engine.py (same HRR bind/gate/completion, same shuffle + 3-part
ablations, same frozen bar).

held-out novelty: a reachable query asks color->size, a pair that is NEVER stored
(only color->mat and mat->size edges are in M) and whose two words need not
co-occur directly — it is reachable ONLY by chaining two real corpus edges =
genuine 2-hop relational recombination on real relations + real engine symbols.
unreachable = the intermediate material is 'dangling' (its onward mat->size edge
is withheld from M) — identical surface form, no completion path.

Tier: DIRECTIONAL (real reps + real relations, but lane not wired to core/ and
not the `anima evaluate --py` decode path — rung-3). a_engine_native_learning.
"""
import os, sys, re, json, collections
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as DEC
from extract_reps import residual_reps, CKPT

D = 1024
SEEDS = list(range(12))
CORPORA = [os.path.join(_REPO, "core/testdata/clm_mid_5lang_c4.txt"),
           os.path.join(_REPO, "core/testdata/flores5_dev_devtest.txt")]

_STOP = set(("the a an of to and in is it that this for on with as are was be by at from or not "
    "but his her they we you i he she them me my your our their its do does did has have had will "
    "would can could should may might must shall when where what which who whom how why all any some "
    "no one two then than into out up down over under more most less about so very just only own same "
    "such each few other been here there now if also these those being both while because during "
    "before after above below again further once new were through even first many").split())


def build_cooc():
    wc = collections.Counter(); cooc = collections.Counter()
    for p in CORPORA:
        for ln in open(p, encoding="utf-8", errors="ignore"):
            asc = sum(1 for c in ln if ord(c) < 128)
            if not ln or asc / max(1, len(ln)) <= 0.9:
                continue
            ws = [w for w in re.findall(r"[a-z]{3,}", ln.lower()) if w not in _STOP]
            ws = list(dict.fromkeys(ws))
            for w in ws:
                wc[w] += 1
            for i in range(len(ws)):
                for j in range(i + 1, len(ws)):
                    a, b = sorted((ws[i], ws[j])); cooc[(a, b)] += 1
    return wc, cooc


def co(cooc, x, y):
    if x == y:
        return 0
    return cooc.get((x, y) if x < y else (y, x), 0)


def pick_pools(wc, cooc, n_per=24):
    # frequent, concrete-ish content words; split top-3N by frequency into 3 pools.
    cand = [w for w, c in wc.most_common(400) if c >= 8 and len(w) >= 4]
    words = cand[: 3 * n_per]
    return {"A": words[0::3][:n_per], "B": words[1::3][:n_per], "C": words[2::3][:n_per]}


def extract(W, pools):
    out = {}
    for pk, words in pools.items():
        rows = [residual_reps(W, w).mean(axis=0) for w in words]
        out[pk] = np.array(rows)
    return out


def _cn(V):
    Vc = V - V.mean(0, keepdims=True)
    return Vc / (np.linalg.norm(Vc, axis=1, keepdims=True) + 1e-9)


# ── HRR ops (identical) ──
def bind(a, b):  return np.fft.irfft(np.fft.rfft(a) * np.fft.rfft(b), n=D)
def inv(a):      return np.concatenate([a[:1], a[1:][::-1]])
def unbind(m, k):return bind(m, inv(k))
def _unit(x):    return x / (np.linalg.norm(x) + 1e-9)
def cleanup(v, cb):
    s = cb @ (v / (np.linalg.norm(v) + 1e-9)); i = int(np.argmax(s)); return i


def corpus_map(src_words, dst_words, cooc):
    """a[i] = index in dst of the TOP co-occurring word with src_words[i]
    (real corpus relation). Ties/zero -> deterministic hash fallback."""
    a = np.zeros(len(src_words), dtype=int)
    for i, s in enumerate(src_words):
        best, bj = -1, i % len(dst_words)
        for j, d in enumerate(dst_words):
            c = co(cooc, s, d)
            if c > best:
                best, bj = c, j
        a[i] = bj
    return a


def run_seed(seed, reps, amap, bmap, shuffle=False):
    rng = np.random.default_rng(seed)
    COLOR, MAT, SIZE = reps["A"], reps["B"], reps["C"]
    N = len(COLOR)
    R1, R2, D1, D2 = (lambda v: v / np.linalg.norm(v, axis=1, keepdims=True))(
        rng.standard_normal((4, D)))
    a = amap.copy()
    ad = rng.permutation(N)               # decoy color->mat (random)
    b = bmap.copy()
    bd = rng.permutation(N)               # decoy mat->size (random)
    connected_mat = set(rng.permutation(N)[:N // 2].tolist())

    reach = [i for i in range(N) if a[i] in connected_mat]
    unreach = [i for i in range(N) if a[i] not in connected_mat]
    gold = lambda i: b[a[i]]

    b_store = b
    if shuffle:
        der = rng.permutation(N)
        while np.any(der == np.arange(N)):
            der = rng.permutation(N)
        b_store = b[der]

    M = np.zeros(D)
    for i in range(N):
        M += bind(bind(COLOR[i], R1), MAT[a[i]])
        M += bind(bind(COLOR[i], D1), MAT[ad[i]])
    for m in range(N):
        if m in connected_mat:
            M += bind(bind(MAT[m], R2), SIZE[b_store[m]])
        M += bind(bind(MAT[m], D2), SIZE[bd[m]])
    M = _unit(M)

    def pipe(i, use_bind=True, use_gate=True, use_completion=True):
        c = COLOR[i]
        if not use_bind:      key1 = c
        elif not use_gate:    key1 = bind(c, _unit(R1 + D1 + R2 + D2))
        else:                 key1 = bind(c, R1)
        raw = unbind(M, key1)
        mat_vec = MAT[cleanup(raw, MAT)] if use_completion else raw
        if not use_bind:      key2 = mat_vec
        elif not use_gate:    key2 = bind(mat_vec, _unit(R1 + D1 + R2 + D2))
        else:                 key2 = bind(mat_vec, R2)
        return cleanup(unbind(M, key2), SIZE)

    def acc(cols, **kw):
        if not cols: return float("nan")
        return sum(1 for i in cols if pipe(i, **kw) == gold(i)) / len(cols)

    return {"full_reach": acc(reach), "full_unreach": acc(unreach),
            "bindoff_reach": acc(reach, use_bind=False),
            "gateoff_reach": acc(reach, use_gate=False),
            "compoff_reach": acc(reach, use_completion=False),
            "n_reach": len(reach), "n_unreach": len(unreach)}


def main():
    print("[armB] building real corpus co-occurrence graph …", flush=True)
    wc, cooc = build_cooc()
    pools = pick_pools(wc, cooc)
    print("[armB] pools A/B/C (real corpus-frequent words):")
    for pk in "ABC":
        print("   %s: %s" % (pk, " ".join(pools[pk])))
    print("[armB] loading h1129 + extracting 303M reps for %d corpus words …"
          % sum(len(pools[p]) for p in pools), flush=True)
    W = DEC.bg_load(CKPT)
    raw_reps = extract(W, pools)
    reps = {p: _cn(raw_reps[p]) for p in pools}                     # centered+unit (primary)
    amap = corpus_map(pools["A"], pools["B"], cooc)                 # REAL relation
    bmap = corpus_map(pools["B"], pools["C"], cooc)                 # REAL relation
    # how "real" is the graph? fraction of mappings backed by nonzero co-occurrence
    a_real = np.mean([co(cooc, pools["A"][i], pools["B"][amap[i]]) > 0 for i in range(len(amap))])
    b_real = np.mean([co(cooc, pools["B"][m], pools["C"][bmap[m]]) > 0 for m in range(len(bmap))])

    rows  = [run_seed(s, reps, amap, bmap, shuffle=False) for s in SEEDS]
    srows = [run_seed(s, reps, amap, bmap, shuffle=True)  for s in SEEDS]
    K = ["full_reach", "full_unreach", "bindoff_reach", "gateoff_reach", "compoff_reach"]
    agg  = {k: float(np.nanmean([r[k] for r in rows]))  for k in K}
    sagg = {k: float(np.nanmean([r[k] for r in srows])) for k in K}
    N = len(pools["A"]); chance = 1.0 / N
    gap = agg["full_reach"] - agg["full_unreach"]
    ab = {p: {"drop": agg["full_reach"] - agg["%s_reach" % p],
              "verdict": "CAUSAL" if agg["full_reach"] - agg["%s_reach" % p] > 0.15 else "INERT"}
          for p in ("bindoff", "gateoff", "compoff")}
    shuf_drop = agg["full_reach"] - sagg["full_reach"]
    out = {"arm": "B_real_corpus_topology", "D": D, "N": N, "seeds": len(SEEDS),
           "chance": chance, "a_edges_real_frac": float(a_real),
           "b_edges_real_frac": float(b_real),
           "full_reach": agg["full_reach"], "full_unreach": agg["full_unreach"],
           "gap_reach_minus_unreach": gap, "fooled_by_form": bool(abs(gap) < 0.10),
           "ablation": ab, "shuffle_reach": sagg["full_reach"],
           "shuffle_drop": shuf_drop, "shuffle_collapsed": bool(shuf_drop > 0.15),
           "pools": pools}
    with open(os.path.join(_HERE, "result_armB.json"), "w") as f:
        json.dump(out, f, indent=2)

    print("\n=== ARM B (real corpus co-occurrence topology · real 303M reps) ===")
    print("N=%d chance=%.3f | corpus-backed edges: a=%.0f%% b=%.0f%%"
          % (N, chance, 100 * a_real, 100 * b_real))
    print("reach=%.3f  unreach=%.3f  gap=%+.3f  fooled=%s"
          % (agg["full_reach"], agg["full_unreach"], gap, abs(gap) < 0.10))
    print("shuffle_reach=%.3f  shuffleΔ=%.3f  collapsed=%s"
          % (sagg["full_reach"], shuf_drop, shuf_drop > 0.15))
    for p in ("bindoff", "gateoff", "compoff"):
        print("  %-8s Δ=%.3f -> %s" % (p, ab[p]["drop"], ab[p]["verdict"]))


if __name__ == "__main__":
    main()
