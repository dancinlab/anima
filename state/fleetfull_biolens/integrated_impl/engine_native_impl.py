#!/usr/bin/env python3
"""
H_9129 IMPLEMENT rung — integrated PFC×BG×hippo lane, engine-native PROMOTION.

Frontier: integrated 3-component G1 recombination lane =
  PFC role↔filler bind  ×  basal-ganglia Go/NoGo content-gate  ×  hippocampal
  pattern-completion  →  mouth cleanup READOUT.
rung-2 (state/g1g6_biolens_en/integrated/) landed this on REAL h1129 303M engine
residual reps (Arm B, real corpus co-occurrence topology): reach 0.236 vs
unreach 0.023, all 3 ablations CAUSAL, shuffle collapsed — but capped at
DIRECTIONAL for two reasons: (i) the rep-extraction forward COPIED decode.py's
loop body rather than provably being decode.py's canonical forward, and (ii) the
residual-stream "rogue dimension" preprocessing (centering) was applied post-hoc,
not wired+pre-registered into the pipeline as a declared transform.

THIS rung delivers the IMPLEMENT-phase promotion (mini-safe · $0 · no pod):
  1. CANONICAL-PATH PROOF — reps come from decode.py's exact engine ops AND we
     PROVE byte-parity to decode.py's canonical `bg_forward_last_W` (the same
     forward `anima evaluate --py` runs): my final-layer residual, pushed through
     ln_f + tied head, must equal bg_forward_last_W's logits to ULP. Recorded.
  2. PREPROCESSING WIRED + PRE-REGISTERED — the rogue-dimension transform is a
     named block chosen BEFORE any lane result:
        raw       : norm-only (collinear control — expected to collapse)
        center    : mean-removed + unit  == PRIMARY (minimal honest transform)
        rogue1    : center + strip top-1 residual PC (the dominant rogue dim)
        whiten    : PCA-whiten  == SENSITIVITY ONLY (honest by-construction caveat:
                    full whitening artificially orthogonalizes → re-introduces the
                    HRR+D-capacity by-construction advantage the bar warns against;
                    NOT the primary verdict form).
  3. REAL corpus relation graph, HELD-OUT 2-hop: reachable = color→size chain
     that is NEVER stored (only color→mat and mat→size edges are in M) — reachable
     ONLY by chaining two REAL corpus edges. unreachable = dangling material
     (onward mat→size edge withheld) — identical surface form, no completion path.
  4. 3-component ablation (bind/gate/completion OFF) + shuffle-derange, engine-native.

PRE-REGISTERED BAR (task step-3 · no tune-to-green · VERBATIM):
  primary form = `center`. PASS-leg iff, on the primary form:
    (a) reach − unreach gap > 0.15   AND not fooled_by_form (|gap|>0.15 same test)
    (b) shuffle collapse: shuffleΔ > 0.15 toward chance
    (c) all three lane-OFF ablations CAUSAL: dropΔ > 0.15 each (INERT floor if not)
  raw MUST collapse (fooled / INERT) to prove the transform is load-bearing, not
  a free pass. by-construction avoidance: reps are REAL 303M — reach must NOT come
  out ~1.0 exact; a real non-orthogonal signature (reach well below 1.0) is required.

TIER (a_engine_native_learning, honest): the REPS are engine-native and byte-parity
proven to decode.py's canonical forward (== anima evaluate --py forward). The lane
SCORING is a custom numpy HRR relational-memory metric, NOT an `anima evaluate --py`
G0-G6 decode-scoring gate, and the lane is NOT wired into core/ (that is rung-3,
BLOCKED-INFRA — needs pool CUDA for the daemon full-binary). So the strict terminal
tier is DIRECTIONAL (strong): engine-native representations, but numpy-mirror
scoring on an unwired lane. GREEN is gated on the rung-3 core/ wire.
"""
import os, sys, re, json, collections
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as D  # canonical engine ops (== the forward anima evaluate --py runs)

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
DIM = 1024
SEEDS = list(range(12))
CORPORA = [os.path.join(_REPO, "core/testdata/clm_mid_5lang_c4.txt"),
           os.path.join(_REPO, "core/testdata/flores5_dev_devtest.txt")]

# ════════════════════════════════════════════════════════════════════════════
# (1) CANONICAL-PATH residual extraction + byte-parity proof to decode.py
# ════════════════════════════════════════════════════════════════════════════
def residual_and_logits(W, s):
    """Run the h1129 forward using decode.py's EXACT engine ops and return BOTH
    the final-layer residual x:[T,d] (pre-ln_f) AND the last-position logits
    obtained by pushing x[-1] through decode.py's ln_f + tied head — so the caller
    can assert byte-parity against decode.py's canonical bg_forward_last_W."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]
    ids = np.asarray(D._seed_to_ids(s), dtype=np.int64)
    T = len(ids)
    x = W["tok"][ids] + W["pos"][0:T]
    for Lr in range(nlay):
        nrm = D._bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, d)
        aout = D._bg_mha(nrm, W["inW"][Lr], W["inB"][Lr], W["oW"][Lr], W["oB"][Lr], T, d, nh)
        x = x + aout
        nrm = D._bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, d)
        h4 = D._bg_gelu(nrm @ W["m0W"][Lr].T + W["m0B"][Lr])
        x = x + (h4 @ W["m2W"][Lr].T + W["m2B"][Lr])
    lastrow = D._bg_layernorm_rows(x[T - 1:T], W["lnfw"], W["lnfb"], 1, d)[0]
    logits = W["head"] @ lastrow
    return x, logits


def prove_canonical(W, probes):
    """Assert my extraction's last-pos logits == decode.py canonical
    bg_forward_last_W to ULP for several probe strings. Returns worst |Δ|."""
    worst = 0.0
    for s in probes:
        ids = D._seed_to_ids(s); T = len(ids)
        canon = D.bg_forward_last_W(W, ids, T)
        _, mine = residual_and_logits(W, s)
        worst = max(worst, float(np.max(np.abs(canon - mine))))
    return worst


# ════════════════════════════════════════════════════════════════════════════
# (2) WIRED, PRE-REGISTERED preprocessing block (rogue-dimension transforms)
# ════════════════════════════════════════════════════════════════════════════
def pp_raw(V):
    return V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)

def pp_center(V):
    Vc = V - V.mean(axis=0, keepdims=True)
    return Vc / (np.linalg.norm(Vc, axis=1, keepdims=True) + 1e-9)

def pp_rogue1(V):
    """center, then project OUT the top-1 principal component (the dominant
    residual-stream rogue dim), then re-unit. Minimal targeted rogue removal."""
    Vc = V - V.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Vc, full_matrices=False)
    top = Vt[0]
    Vp = Vc - (Vc @ top)[:, None] * top[None, :]
    return Vp / (np.linalg.norm(Vp, axis=1, keepdims=True) + 1e-9)

def pp_whiten(V):
    """PCA-whiten (sensitivity ONLY — honest by-construction caveat). Equalises
    all component variances → artificially orthogonalises real reps → inflates
    HRR reach toward the by-construction ceiling. NOT the primary verdict form."""
    Vc = V - V.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Vc, full_matrices=False)
    Vw = (U * (1.0 / (S + 1e-6))) @ Vt  # unit-variance components back in d-space
    return Vw / (np.linalg.norm(Vw, axis=1, keepdims=True) + 1e-9)

PREPROC = {"raw": pp_raw, "center": pp_center, "rogue1": pp_rogue1, "whiten": pp_whiten}
PRIMARY = "center"

# ════════════════════════════════════════════════════════════════════════════
# HRR ops (identical to rung-2 / STEP-0 — the lane mechanism is UNCHANGED)
# ════════════════════════════════════════════════════════════════════════════
def bind(a, b):   return np.fft.irfft(np.fft.rfft(a) * np.fft.rfft(b), n=DIM)
def inv(a):       return np.concatenate([a[:1], a[1:][::-1]])
def unbind(m, k): return bind(m, inv(k))
def _unit(x):     return x / (np.linalg.norm(x) + 1e-9)
def cleanup(v, cb):
    s = cb @ (v / (np.linalg.norm(v) + 1e-9)); return int(np.argmax(s))

# ════════════════════════════════════════════════════════════════════════════
# (3) REAL corpus relation graph (co-occurrence)
# ════════════════════════════════════════════════════════════════════════════
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
            for w in ws: wc[w] += 1
            for i in range(len(ws)):
                for j in range(i + 1, len(ws)):
                    a, b = sorted((ws[i], ws[j])); cooc[(a, b)] += 1
    return wc, cooc

def co(cooc, x, y):
    if x == y: return 0
    return cooc.get((x, y) if x < y else (y, x), 0)

def pick_pools(wc, n_per=24):
    cand = [w for w, c in wc.most_common(400) if c >= 8 and len(w) >= 4]
    words = cand[: 3 * n_per]
    return {"A": words[0::3][:n_per], "B": words[1::3][:n_per], "C": words[2::3][:n_per]}

def corpus_map(src_words, dst_words, cooc):
    a = np.zeros(len(src_words), dtype=int)
    for i, s in enumerate(src_words):
        best, bj = -1, i % len(dst_words)
        for j, dst in enumerate(dst_words):
            c = co(cooc, s, dst)
            if c > best: best, bj = c, j
        a[i] = bj
    return a

# ════════════════════════════════════════════════════════════════════════════
# (4) integrated lane + ablations (mechanism identical to rung-2)
# ════════════════════════════════════════════════════════════════════════════
def run_seed(seed, reps, amap, bmap, shuffle=False):
    rng = np.random.default_rng(seed)
    COLOR, MAT, SIZE = reps["A"], reps["B"], reps["C"]
    N = len(COLOR)
    R1, R2, D1, D2 = (lambda v: v / np.linalg.norm(v, axis=1, keepdims=True))(
        rng.standard_normal((4, DIM)))
    a = amap.copy(); ad = rng.permutation(N)
    b = bmap.copy(); bd = rng.permutation(N)
    connected_mat = set(rng.permutation(N)[:N // 2].tolist())
    reach = [i for i in range(N) if a[i] in connected_mat]
    unreach = [i for i in range(N) if a[i] not in connected_mat]
    gold = lambda i: b[a[i]]

    b_store = b
    if shuffle:
        der = rng.permutation(N)
        while np.any(der == np.arange(N)): der = rng.permutation(N)
        b_store = b[der]

    M = np.zeros(DIM)
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
        if not use_bind:    key1 = c
        elif not use_gate:  key1 = bind(c, _unit(R1 + D1 + R2 + D2))
        else:               key1 = bind(c, R1)
        raw = unbind(M, key1)
        mat_vec = MAT[cleanup(raw, MAT)] if use_completion else raw
        if not use_bind:    key2 = mat_vec
        elif not use_gate:  key2 = bind(mat_vec, _unit(R1 + D1 + R2 + D2))
        else:               key2 = bind(mat_vec, R2)
        return cleanup(unbind(M, key2), SIZE)

    def acc(cols, **kw):
        if not cols: return float("nan")
        return sum(1 for i in cols if pipe(i, **kw) == gold(i)) / len(cols)

    return {"full_reach": acc(reach), "full_unreach": acc(unreach),
            "bindoff_reach": acc(reach, use_bind=False),
            "gateoff_reach": acc(reach, use_gate=False),
            "compoff_reach": acc(reach, use_completion=False),
            "n_reach": len(reach), "n_unreach": len(unreach)}


def eval_form(reps, amap, bmap):
    rows = [run_seed(s, reps, amap, bmap, False) for s in SEEDS]
    srows = [run_seed(s, reps, amap, bmap, True) for s in SEEDS]
    K = ["full_reach", "full_unreach", "bindoff_reach", "gateoff_reach", "compoff_reach"]
    agg = {k: float(np.nanmean([r[k] for r in rows])) for k in K}
    sagg = {k: float(np.nanmean([r[k] for r in srows])) for k in K}
    N = len(reps["A"]); chance = 1.0 / N
    gap = agg["full_reach"] - agg["full_unreach"]
    ab = {p: {"reach": agg["%s_reach" % p],
              "drop": agg["full_reach"] - agg["%s_reach" % p],
              "verdict": "CAUSAL" if agg["full_reach"] - agg["%s_reach" % p] > 0.15 else "INERT"}
          for p in ("bindoff", "gateoff", "compoff")}
    shuf_drop = agg["full_reach"] - sagg["full_reach"]
    return {
        "chance": chance,
        "reach": agg["full_reach"], "unreach": agg["full_unreach"], "gap": gap,
        "fooled_by_form": bool(abs(gap) <= 0.15),
        "shuffle_reach": sagg["full_reach"], "shuffle_drop": shuf_drop,
        "shuffle_collapsed": bool(shuf_drop > 0.15),
        "ablation": ab,
        "n_reach": rows[0]["n_reach"], "n_unreach": rows[0]["n_unreach"],
    }


def rep_diag(V):
    vn = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
    G = vn @ vn.T
    off = G[~np.eye(len(G), dtype=bool)]
    norms = np.linalg.norm(V, axis=1)
    return {"offdiag_cos_abs_mean": float(np.abs(off).mean()),
            "offdiag_cos_max": float(off.max()),
            "norm_ratio": float(norms.max() / (norms.min() + 1e-12))}


def main():
    print("[impl] loading h1129 303M via decode.py canonical …", flush=True)
    W = D.bg_load(CKPT)
    print("[impl] d=%d nlay=%d nh=%d vocab=%d" % (W["d"], W["nlay"], W["nh"], W["vocab"]), flush=True)

    # (1) canonical-path byte-parity proof
    parity_worst = prove_canonical(W, ["forest", "salt", "deep", "engine", "market"])
    print("[impl] canonical byte-parity worst|Δlogit| vs decode.bg_forward_last_W = %.3e" % parity_worst, flush=True)

    # (3) real corpus relation graph
    wc, cooc = build_cooc()
    pools = pick_pools(wc)
    amap = corpus_map(pools["A"], pools["B"], cooc)
    bmap = corpus_map(pools["B"], pools["C"], cooc)
    a_real = float(np.mean([co(cooc, pools["A"][i], pools["B"][amap[i]]) > 0 for i in range(len(amap))]))
    b_real = float(np.mean([co(cooc, pools["B"][m], pools["C"][bmap[m]]) > 0 for m in range(len(bmap))]))
    print("[impl] corpus-backed edges a=%.0f%% b=%.0f%%" % (100 * a_real, 100 * b_real), flush=True)

    # raw 303M mean-pool reps (engine-native)
    print("[impl] extracting canonical residual reps for %d words …" % sum(len(pools[p]) for p in pools), flush=True)
    raw_reps = {}
    for pk in "ABC":
        rows = []
        for w in pools[pk]:
            x, _ = residual_and_logits(W, w)
            rows.append(x.mean(axis=0))
        raw_reps[pk] = np.array(rows)

    # (2) wired preprocessing block — run every declared form
    forms = {}; diags = {}
    for name, fn in PREPROC.items():
        reps = {pk: fn(raw_reps[pk]) for pk in "ABC"}
        forms[name] = eval_form(reps, amap, bmap)
        diags[name] = rep_diag(np.concatenate([reps[pk] for pk in "ABC"]))

    # ── verdict on the PRIMARY (pre-registered) form ──
    P = forms[PRIMARY]
    ab = P["ablation"]
    bar = {
        "gap_gt_0_15": bool(P["gap"] > 0.15),
        "not_fooled": bool(not P["fooled_by_form"]),
        "shuffle_collapsed": bool(P["shuffle_collapsed"]),
        "bind_causal": ab["bindoff"]["verdict"] == "CAUSAL",
        "gate_causal": ab["gateoff"]["verdict"] == "CAUSAL",
        "comp_causal": ab["compoff"]["verdict"] == "CAUSAL",
        "raw_collapses": bool(forms["raw"]["fooled_by_form"] or
                              forms["raw"]["ablation"]["bindoff"]["verdict"] == "INERT"),
        "not_by_construction": bool(P["reach"] < 0.90),  # real reps not clean → reach<<1
    }
    all_pass = all(bar.values())

    out = {
        "frontier": "integrated PFC×BG×hippo (G1 recombination)",
        "phase": "implement",
        "ckpt": "h1129.bin (303M ByteGPT, real)",
        "canonical_path": {
            "reps_via": "core/decode.py bg_load + _bg_mha/_bg_layernorm_rows/_bg_gelu",
            "byte_parity_worst_dlogit_vs_bg_forward_last_W": parity_worst,
            "byte_parity_proven": bool(parity_worst < 1e-6),
        },
        "corpus": {"a_edges_real_frac": a_real, "b_edges_real_frac": b_real,
                   "pools": pools},
        "primary_form": PRIMARY,
        "preproc_forms": forms,
        "rep_diag": diags,
        "prereg_bar": bar,
        "bar_all_pass": bool(all_pass),
        "seeds": len(SEEDS), "D": DIM,
    }
    with open(os.path.join(_HERE, "result.json"), "w") as f:
        json.dump(out, f, indent=2)

    # ── print ──
    print("\n=== H_9129 IMPLEMENT — integrated lane · engine-native (real 303M · decode.py canonical) ===")
    print("canonical byte-parity worst|Δlogit| = %.3e  (proven=%s)" % (parity_worst, parity_worst < 1e-6))
    print("N=%d chance=%.3f seeds=%d | corpus edges a=%.0f%% b=%.0f%%\n"
          % (len(pools["A"]), 1.0 / len(pools["A"]), len(SEEDS), 100 * a_real, 100 * b_real))
    hdr = "%-8s reach  unreach  gap     fooled  shuf   shufD  |bindD gateD compD | offcos"
    print(hdr % "form")
    print("-" * 92)
    for name in ("raw", "center", "rogue1", "whiten"):
        r = forms[name]; a = r["ablation"]
        star = " *" if name == PRIMARY else ""
        print("%-8s %.3f  %.3f   %+.3f  %-5s  %.3f  %.3f  |%.2f  %.2f  %.2f | %.3f%s"
              % (name, r["reach"], r["unreach"], r["gap"], str(r["fooled_by_form"]),
                 r["shuffle_reach"], r["shuffle_drop"], a["bindoff"]["drop"],
                 a["gateoff"]["drop"], a["compoff"]["drop"],
                 diags[name]["offdiag_cos_abs_mean"], star))
    print("\nPRIMARY=%s pre-registered bar:" % PRIMARY)
    for k, v in bar.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nbar_all_pass = %s" % all_pass)
    print("(whiten = SENSITIVITY only; higher reach there is the by-construction inflation the bar excludes)")


if __name__ == "__main__":
    main()
