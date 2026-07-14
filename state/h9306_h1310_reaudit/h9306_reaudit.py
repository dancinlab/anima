#!/usr/bin/env python3
"""H_9306 — re-audit of H_1310 ("from-scratch pure mitosis is capacity-bound / LOCAL-EXPERT CEILING").

H_1310's arm definition, verbatim: "Each cell holds an online add-1 next-byte table."
That is a FLAT per-cell count-MLE head -- exactly the estimator H_9301 showed degrades by
+0.0555 nats as cells grow (starvation variance), while a shrinkage head stays flat. And H_1310
grew it to 512 cells. So its headline DVs (FLOOR, CONTROL) ride causally on that defect.

This re-audit changes ONE thing: the per-cell head (flat add-1 -> Witten-Bell shrinkage toward
the pooled global table). Corpus, split, ladder, split-rule, controls and BARS are H_1310's,
byte-for-byte. Introducing a new, more favourable DV would be retroactive tune-to-green; we do
not. We re-read H_1310's OWN frozen bars.

  FLOOR   (H_1310 bar 3): B_scratch[512] < A_freq - 0.02        [A_freq = order-2 n-gram floor]
  CONTROL (H_1310 bar 4): B_shuffle[512] >= B_scratch[512] + 0.10

H_1310 measured: A_freq 2.50884 · B_scratch[512] 2.57788 (FLOOR FAIL, +0.069 above)
                 B_shuffle[512] 2.53592 (CONTROL FAIL -- shuffle BEAT targeting)

CALIB gates (blocking): the port must reproduce A_freq and the FLAT B_scratch[512] before the
WB arm is read at all (reference-match).
"""
import argparse, hashlib, json, os, random, sys, time
import numpy as np

CORPUS_SHA = "86864aa32dcf1c8680ab254e1b28357bf0326c8d45a86837ae4e3b9d09350f62"
A_FREQ_ANCHOR = 2.50884
FLAT_512_ANCHOR = 2.57788
FLOOR_MARGIN = 0.02
CONTROL_MARGIN = 0.10
SPLIT_THRESH = 0.55
MIN_OWNED = 2
MIN_OBS = 4
LADDER = [1, 8, 64, 512]
SEEDS = [13101, 13102, 13103]
V = 27                       # a-z + space


def log(*a):
    print(*a, flush=True)


def build_corpus(path="h1310_corpus.bin"):
    """H_1310's corpus, sha-pinned to 86864aa3... The recipe is
    /usr/share/dict/words -> isalpha 2..12 -> lowercase -> Random(13100).shuffle -> first 4000
    words -> space-join + newline -> 24000 bytes. NOTE: /usr/share/dict/words is a per-HOST
    system asset and differs between machines (summer's build hashed 48550825..., the mac's
    reproduces the anchor exactly), so the bytes are shipped as a pinned file rather than rebuilt
    on the compute host. The sha gate below is what actually guarantees provenance."""
    return open(path, "rb").read()


def encode(b):
    """27-symbol alphabet: a-z -> 0..25, everything else (space/newline) -> 26."""
    out = np.full(len(b), 26, dtype=np.int64)
    arr = np.frombuffer(b, dtype=np.uint8)
    m = (arr >= 97) & (arr <= 122)
    out[m] = arr[m] - 97
    return out


def pairs(sym):
    """order-2 context -> next symbol. X = the 2 previous symbols as a 2-D POINT.

    H_1310's split is a "2-means median bisection of its owned territory" -- territory implies a
    metric space, so the context must be a point, not a packed categorical id. (A first port
    bisected the packed id s[i-2]*V + s[i-1]; that geometry is meaningless, growth saturated at
    64 cells, and the CALIB gate refused to read the WB arm. Reference-match: align the first
    divergence, do not shake flags.) This 2-D form matches the lane's canonical grow_on."""
    X = np.stack([sym[:-2], sym[1:-1]], axis=1).astype(np.float64)
    ctx = (sym[:-2] * V + sym[1:-1]).astype(np.int64)     # kept for the exact n-gram floor
    return X, ctx, sym[2:].astype(np.int64)


def head_probs(cnt, mode):
    """cnt: (K, V) train counts owned by each cell. Returns (K, V) probability rows."""
    if mode == "flat":
        p = cnt + 1.0                                  # H_1310's "online add-1 table"
        return p / p.sum(axis=1, keepdims=True)
    # Witten-Bell shrinkage toward the pooled global table. Zero free hyperparameters.
    pooled = cnt.sum(axis=0) + 1.0
    pooled = pooled / pooled.sum()
    n = cnt.sum(axis=1, keepdims=True)                 # tokens in the cell
    T = (cnt > 0).sum(axis=1, keepdims=True).astype(np.float64)   # distinct next-types seen
    lam = n / (n + T + 1e-12)
    mle = cnt / (n + 1e-12)
    return lam * mle + (1.0 - lam) * pooled[None, :]


def ce(P, owner, y):
    p = np.clip(P[owner, y], 1e-12, 1.0)
    return float(-np.log(p).mean())


def assign(centers, X):
    d = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    return np.argmin(d, axis=1)


def grow(X_tr, y_tr, target_cells, rng, shuffle_pick):
    """H_1310's gradient-free mitosis, verbatim: one prototype at the centroid; a cell's running
    owned-error (1 - p(true)) over SPLIT_THRESH with >=MIN_OWNED owned and >=MIN_OBS obs is
    ELIGIBLE; the worst-error eligible cell splits (median bisection of its owned contexts).
    shuffle_pick=True is H_1310's CONTROL: split a RANDOM eligible cell instead of the worst."""
    centers = [X_tr.mean(axis=0).tolist()]          # one prototype at the all-context centroid
    dead = set()
    while len(centers) < target_cells:
        C = np.asarray(centers)
        owner = assign(C, X_tr)
        K = len(centers)
        cnt = np.zeros((K, V))
        np.add.at(cnt, (owner, y_tr), 1.0)
        P = head_probs(cnt, "flat")                 # eligibility uses H_1310's own rule
        err = 1.0 - P[owner, y_tr]
        elig = []
        for k in range(K):
            m = owner == k
            n = int(m.sum())
            if k not in dead and n >= MIN_OWNED and n >= MIN_OBS and err[m].mean() > SPLIT_THRESH:
                elig.append((float(err[m].mean()), k))
        if not elig:
            break
        pick = int(rng.choice([k for _, k in elig])) if shuffle_pick else max(elig)[1]
        pts = X_tr[owner == pick]
        ax = int(np.argmax(pts.var(axis=0)))
        col = pts[:, ax]
        med = float(np.median(col))
        lo, hi = col <= med, col > med
        if lo.sum() == 0 or hi.sum() == 0:
            dead.add(pick)                          # H_9301's repair: blacklist, do not kill growth
            continue
        centers[pick] = pts[lo].mean(axis=0).tolist()
        centers.append(pts[hi].mean(axis=0).tolist())
    C = np.asarray(centers)
    return C, assign(C, X_tr), len(centers)


def score(C, owner_tr, y_tr, X_te, y_te, K, mode):
    cnt = np.zeros((K, V))
    np.add.at(cnt, (owner_tr, y_tr), 1.0)
    P = head_probs(cnt, mode)
    return ce(P, assign(C, X_te), y_te)


def a_freq(ctx_tr, y_tr, ctx_te, y_te):
    """order-2 add-1 Markov = the exact n-gram counting FLOOR."""
    cnt = np.zeros((V * V, V))
    np.add.at(cnt, (ctx_tr, y_tr), 1.0)
    P = (cnt + 1.0)
    P = P / P.sum(axis=1, keepdims=True)
    return ce(P, ctx_te, y_te)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/h9306")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()

    raw = build_corpus()
    sha = hashlib.sha256(raw).hexdigest()
    log(f"[corpus] {len(raw)} B sha={sha[:16]}...  anchor-match={sha == CORPUS_SHA}")
    if sha != CORPUS_SHA:
        log("FATAL: corpus sha != H_1310 anchor - provenance gate. STOP."); sys.exit(2)

    sym = encode(raw)
    X, ctx, y = pairs(sym)
    n = len(ctx)
    ntr = int(n * 0.8)
    X_tr, X_te = X[:ntr], X[ntr:]
    ctx_tr, y_tr, ctx_te, y_te = ctx[:ntr], y[:ntr], ctx[ntr:], y[ntr:]
    log(f"[split] train={ntr} test={n-ntr}  (H_1310: 19198 / 4800)")

    af = a_freq(ctx_tr, y_tr, ctx_te, y_te)
    log(f"[CALIB-1] A_freq (n-gram floor) = {af:.5f}   anchor {A_FREQ_ANCHOR}  d={af-A_FREQ_ANCHOR:+.5f}")

    res = {"id": "H_9306", "corpus_sha256": sha, "A_freq": af, "A_freq_anchor": A_FREQ_ANCHOR,
           "ladder": {}, "seeds": SEEDS}
    for mode in ["flat", "wb"]:
        res["ladder"][mode] = {}
        for cells in LADDER:
            vals, shuf = [], []
            for sd in SEEDS:
                rng = np.random.default_rng(sd)
                C, o, K = grow(X_tr, y_tr, cells, rng, shuffle_pick=False)
                vals.append(score(C, o, y_tr, X_te, y_te, K, mode))
                rng2 = np.random.default_rng(sd + 500)
                C2, o2, K2 = grow(X_tr, y_tr, cells, rng2, shuffle_pick=True)
                shuf.append(score(C2, o2, y_tr, X_te, y_te, K2, mode))
            res["ladder"][mode][cells] = {"scratch": float(np.mean(vals)),
                                          "shuffle": float(np.mean(shuf))}
            log(f"  [{mode:4s}] cells={cells:4d}  B_scratch={np.mean(vals):.5f}  "
                f"B_shuffle={np.mean(shuf):.5f}")

    flat512 = res["ladder"]["flat"][512]["scratch"]
    wb512 = res["ladder"]["wb"][512]["scratch"]
    wb512s = res["ladder"]["wb"][512]["shuffle"]

    calib1 = abs(af - A_FREQ_ANCHOR) <= 0.005
    calib2 = abs(flat512 - FLAT_512_ANCHOR) <= 0.02
    log(f"\n[CALIB-2] FLAT B_scratch[512] = {flat512:.5f}  anchor {FLAT_512_ANCHOR}  "
        f"d={flat512-FLAT_512_ANCHOR:+.5f}")
    log(f"[CALIB] 1={'PASS' if calib1 else 'FAIL'}  2={'PASS' if calib2 else 'FAIL'}")

    if not (calib1 and calib2):
        log("\nINVALID - port does not reproduce H_1310; the WB arm is NOT read (reference-match).")
        res["verdict"] = "INVALID - CALIB fail; port does not reproduce H_1310"
        json.dump(res, open(os.path.join(a.out, "h9306_summary.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(0)

    floor_bar = af - FLOOR_MARGIN
    floor_pass = wb512 < floor_bar
    ctrl_delta = wb512s - wb512
    ctrl_pass = ctrl_delta >= CONTROL_MARGIN

    log("\n" + "=" * 70)
    log(f"H_1310's OWN frozen bars, re-read with the estimator swapped (bars UNMOVED):")
    log(f"  A_freq (n-gram floor)      = {af:.5f}   -> FLOOR bar = {floor_bar:.5f}")
    log(f"  FLAT B_scratch[512]        = {flat512:.5f}   (H_1310: {FLAT_512_ANCHOR} -> FLOOR FAIL)")
    log(f"  WB   B_scratch[512]        = {wb512:.5f}")
    log(f"  (3) FLOOR   WB < {floor_bar:.5f} : {floor_pass}")
    log(f"  (4) CONTROL WB shuffle - scratch = {ctrl_delta:+.5f}  (>= +{CONTROL_MARGIN}) : {ctrl_pass}")

    if floor_pass:
        v = ("REOPEN - H_1310's LOCAL-EXPERT CEILING was an ESTIMATOR defect: with strength-sharing, "
             "gradient-free from-scratch mitosis DOES beat the n-gram floor on H_1310's own frozen bar")
    else:
        v = ("UPHELD - H_1310's ceiling SURVIVES the estimator swap: shrinkage does not clear the "
             "n-gram floor either => the ceiling is real, the estimator is innocent (honest negative)")
    log(f"\nVERDICT: {v}")
    res.update({"floor_bar": floor_bar, "wb_512": wb512, "flat_512": flat512,
                "floor_pass": bool(floor_pass), "control_delta": ctrl_delta,
                "control_pass": bool(ctrl_pass), "CALIB_pass": bool(calib1 and calib2),
                "verdict": v, "wall_s": time.time() - t0})
    json.dump(res, open(os.path.join(a.out, "h9306_summary.json"), "w"), indent=2, ensure_ascii=False)
    log(f"wall={time.time()-t0:.1f}s\n[done]")


if __name__ == "__main__":
    main()
