#!/usr/bin/env python3
# measure.py — L2-2 coord grounding measurement (H_9097). DIRECTIONAL (--py numpy mirror
# of the LIVE core/decode.hexa bytegpt_hidden_pool_ranged + content_axis_from_pooled and
# core/engine_cli.hexa self_drift_exp/self_chain_fit). Engine-native (.hexa) re-measure =
# ING follow-on (4-rung ladder). grep: `import numpy` present (via core/decode) => label
# DIRECTIONAL, not terminal. NO torch, NO gauge_lib.
#
# GROUNDS content_axis (a synthetic int in every prior H_9038 check) in the 303M's REAL
# lived experience = its pooled penultimate representation of the text it processed.
#
# Two arms, IDENTICAL fold (content_axis_from_pooled dim=8), only the SOURCE vector differs:
#   MAIN : pooled penultimate of the 303M (bytegpt_hidden_pool_ranged)   — real experience
#   FNV  : immune_embed_key(text) FNV-1a hash (deterministic but MEANING-ARBITRARY) — the
#          pre-registered NO-GROUNDING baseline (predicted to collapse the within>between gap)
#
# Phase HEAVY (pool, 303M): compute pooled -> axis for all texts, cache axes.json.
# Phase LIGHT (anywhere)  : G1'/G2'/G3' falsifiers from axes.json.
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))

import decode as bg
import engine_cli as ec

DIM = 8            # identity axis count (self_new dim)
STEP = 0.25        # self_drift_exp step (design-frozen)
SEED_AXIS = 0      # seed identity self_new(DIM, SEED_AXIS)
N_CHAIN = 32       # texts that build each chain
N_HELD = 8         # held-out texts per stream for G3'
STREAMS = ["ko_general", "en_general", "ko_sns"]
AXES_JSON = os.path.join(HERE, "axes.json")


def _load_stream(short):
    p = os.path.join(HERE, "streams", f"{short}.txt")
    with open(p, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]
    return lines[: N_CHAIN + N_HELD]


# ── FROZEN fold shared by both arms (mirror of content_axis_from_pooled) ──
def fold_axis(vec, dim):
    return bg.content_axis_from_pooled(vec, dim)


def main_axis_W(W, text):
    # 303M forward via HOISTED weights (bg_hidden_pool_W) — bytegpt_hidden_pool_ranged
    # reloads per call, so for the 120-text sweep we load ONCE and reuse (H_1400 W-hoist).
    ids = list(text.encode("utf-8", "surrogateescape"))
    T = len(ids)
    pooled = bg.bg_hidden_pool_W(W, ids, T)
    return fold_axis([float(v) for v in pooled], DIM)


def fnv_axis(text):
    v = ec.immune_embed_key(text)          # 64-dim FNV, meaning-arbitrary
    return fold_axis(v, DIM)


def compute_axes(ckpt):
    """HEAVY: 303M forward per text (MAIN) + cheap FNV. Cache to axes.json.
    Loads the ckpt ONCE (W-hoist) — bytegpt_hidden_pool_ranged is the single-shot
    engine-parity entry; here we reuse its bg_load_ranged + bg_hidden_pool_W internals."""
    print(f"[load] {ckpt} ...", flush=True)
    W = bg.bg_load_ranged(ckpt)
    print(f"[load ok] d={W['d']} nlay={W['nlay']} nh={W['nh']} vocab={W['vocab']}", flush=True)
    out = {"ckpt": ckpt, "dim": DIM, "streams": {}}
    for s in STREAMS:
        texts = _load_stream(s)
        rec = {"main": [], "fnv": [], "pooled": [], "n": len(texts)}
        for i, t in enumerate(texts):
            ids = list(t.encode("utf-8", "surrogateescape"))
            pooled = [float(v) for v in bg.bg_hidden_pool_W(W, ids, len(ids))]
            ma = fold_axis(pooled, DIM)
            fa = fnv_axis(t)
            rec["main"].append(ma)
            rec["fnv"].append(fa)
            rec["pooled"].append(pooled)     # raw penultimate (wall-taxonomy diagnostic)
            print(f"  {s}[{i:02d}] main_axis={ma} fnv_axis={fa}  ({len(ids)}B)", flush=True)
        out["streams"][s] = rec
    with open(AXES_JSON, "w") as w:
        json.dump(out, w, indent=1)
    print(f"[axes cached] {AXES_JSON}")
    return out


# ── self-chain builders (mirror LIVE engine_cli self_drift_exp / self_chain) ──
def build_chain(axes):
    s = ec.self_new(DIM, SEED_AXIS)
    c = ec.self_chain_new(s)
    for ax in axes:
        s = ec.self_drift_exp(s, int(ax), STEP)
        c = ec.self_chain_append(c, s)
    return s, c   # latest identity, full chain


def latest_of(axes):
    s, _ = build_chain(axes)
    return s


# ── deterministic shuffle (LCG, frozen) — permute axis list, structure intact ──
def lcg_perm(n, seed):
    idx = list(range(n))
    x = (seed * 1103515245 + 12345) & 0x7FFFFFFF
    for i in range(n - 1, 0, -1):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        j = x % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    return idx


def g1_gap(axes_by_stream):
    """G1' separation: within-stream two-half cos MINUS between-stream half cos."""
    halfA = {}
    halfB = {}
    for s in STREAMS:
        ax = axes_by_stream[s][:N_CHAIN]
        halfA[s] = latest_of(ax[:N_CHAIN // 2])
        halfB[s] = latest_of(ax[N_CHAIN // 2:])
    within = []
    for s in STREAMS:
        within.append(ec.self_cos(halfA[s], halfB[s]))
    between = []
    for i in range(len(STREAMS)):
        for j in range(len(STREAMS)):
            if i == j:
                continue
            # cross-stream half pairs (both A-A and A-B directions)
            between.append(ec.self_cos(halfA[STREAMS[i]], halfA[STREAMS[j]]))
            between.append(ec.self_cos(halfA[STREAMS[i]], halfB[STREAMS[j]]))
    mw = sum(within) / len(within)
    mb = sum(between) / len(between)
    return mw, mb, mw - mb, within, between


def g3_retrieval(axes_by_stream):
    """G3' retrieval: each held-out text's candidate increment ranked by self_chain_fit
    against the 3 stream chains; hit iff its OWN stream ranks top-1."""
    chains = {}
    latests = {}
    for s in STREAMS:
        lat, ch = build_chain(axes_by_stream[s][:N_CHAIN])
        chains[s] = ch
        latests[s] = lat
    hits = 0
    total = 0
    detail = []
    for o in STREAMS:
        held = axes_by_stream[o][N_CHAIN:N_CHAIN + N_HELD]
        for a_h in held:
            fits = {}
            for s in STREAMS:
                cand = ec.self_drift_exp(latests[s], int(a_h), STEP)
                fits[s] = ec.self_chain_fit(cand, chains[s])
            pred = max(STREAMS, key=lambda s: fits[s])
            hit = (pred == o)
            hits += 1 if hit else 0
            total += 1
            detail.append((o, int(a_h), pred, hit, {s: round(fits[s], 3) for s in STREAMS}))
    return hits, total, detail


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _l2n(v):
    m = _dot(v, v) ** 0.5
    return [x / m for x in v] if m > 0 else v


def pooled_diagnostic(axes):
    """WALL TAXONOMY (a_break_the_wall): the frozen argmax-L2 fold collapses. Does the RAW
    pooled penultimate ITSELF carry per-stream experience structure (=> fold is the artifact,
    follow-on) or not (=> ceiling)? Mean-center pooled across all 120, build per-stream
    centroids from the 32 chain texts, nearest-centroid-classify the 24 held-out. Chance=8/24.
    This is DIAGNOSTIC ONLY — it does NOT move the frozen G1'/G2'/G3' bar."""
    st = axes["streams"]
    if "pooled" not in st[STREAMS[0]]:
        print("\n[pooled diagnostic] no raw pooled vectors cached — skip")
        return
    allp = []
    for s in STREAMS:
        allp += st[s]["pooled"]
    D = len(allp[0])
    gmean = [sum(p[i] for p in allp) / len(allp) for i in range(D)]

    def center(p):
        return [p[i] - gmean[i] for i in range(D)]

    cent = {}
    for s in STREAMS:
        chain = [center(p) for p in st[s]["pooled"][:N_CHAIN]]
        c = [sum(p[i] for p in chain) / len(chain) for i in range(D)]
        cent[s] = _l2n(c)
    # within/between on centered-pooled centroids
    csim = []
    for i in range(len(STREAMS)):
        for j in range(i + 1, len(STREAMS)):
            csim.append((STREAMS[i], STREAMS[j], _dot(cent[STREAMS[i]], cent[STREAMS[j]])))
    hits = 0
    total = 0
    for o in STREAMS:
        for p in st[o]["pooled"][N_CHAIN:N_CHAIN + N_HELD]:
            pc = _l2n(center(p))
            pred = max(STREAMS, key=lambda s: _dot(pc, cent[s]))
            hits += 1 if pred == o else 0
            total += 1
    print("\n===== POOLED DIAGNOSTIC (raw penultimate, centered — fold BYPASSED) =====")
    for a, b, sim in csim:
        print(f"  centroid_cos({a},{b}) = {sim:+.4f}   (lower = streams more separated)")
    print(f"  nearest-centroid held-out classification = {hits}/{total}  (chance {total//len(STREAMS)}/{total})")
    if hits >= 16:
        print("  => penultimate CARRIES per-stream experience signal; the argmax-L2 FOLD discards it (metric-artifact wall (a)).")
    else:
        print("  => penultimate does NOT separate streams at mean-pool (ceiling wall (d)).")


def analyze(axes):
    st = axes["streams"]
    for arm in ("main", "fnv"):
        abs_ = {s: st[s][arm] for s in STREAMS}
        print(f"\n===== ARM = {arm.upper()} =====")
        # axis histograms (root diagnostic: do streams get distinct axis distributions?)
        for s in STREAMS:
            h = [0] * DIM
            for a in abs_[s][:N_CHAIN]:
                h[a] += 1
            print(f"  {s:11s} axis-hist(chain) = {h}")
        # G1'
        mw, mb, gap, within, between = g1_gap(abs_)
        print(f"  G1' within_cos={mw:.4f}  between_cos={mb:.4f}  GAP={gap:+.4f}  (bar +0.10)")
        print(f"      within = {[round(x,3) for x in within]}")
        # G2' shuffle
        flat = []
        order = []
        for s in STREAMS:
            for k in range(N_CHAIN):
                flat.append(abs_[s][k]); order.append((s, k))
        perm = lcg_perm(len(flat), 20260702)
        shuf_by_stream = {s: list(abs_[s]) for s in STREAMS}
        for pos, (s, k) in enumerate(order):
            shuf_by_stream[s][k] = flat[perm[pos]]
        mw2, mb2, gap2, _, _ = g1_gap(shuf_by_stream)
        print(f"  G2' shuffled GAP={gap2:+.4f}  (collapse bar |gap|<0.03)")
        # G3'
        hits, total, detail = g3_retrieval(abs_)
        print(f"  G3' retrieval top-1 = {hits}/{total}  (chance {total//len(STREAMS)}/{total}, bar >=16/24)")
        # verdicts
        v1 = "PASS" if gap >= 0.10 else "FAIL"
        v2 = "PASS(collapse)" if abs(gap2) < 0.03 else "FAIL(no-collapse)"
        v3 = "PASS" if hits >= 16 else "FAIL"
        print(f"  VERDICT[{arm}]: G1'={v1}  G2'={v2}  G3'={v3}")
    pooled_diagnostic(axes)


def main(argv):
    ckpt = None
    do_heavy = True
    for a in argv:
        if a == "--analyze-only":
            do_heavy = False
        elif a.startswith("--ckpt="):
            ckpt = a.split("=", 1)[1]
        elif not a.startswith("--"):
            ckpt = a
    if do_heavy:
        if not ckpt:
            print("usage: measure.py <ckpt.bin> | measure.py --analyze-only", file=sys.stderr)
            return 2
        axes = compute_axes(ckpt)
    else:
        with open(AXES_JSON) as f:
            axes = json.load(f)
    analyze(axes)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
