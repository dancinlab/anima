#!/usr/bin/env python3
"""H_9313 — the dissociation on the REAL corpus: grow ONCE, then swap only the head.

H_9311's pre-registered control B3 ("the FLAT head must degrade under starvation") came back
UNREADABLE: the flat faculty is locked at 10 cells by the degenerate-split break, so it never
reaches the starved regime at all (flat change = +0.00000). That is an un-engaged axis, not a
refutation.

To see the dissociation on the real corpus, growth and head must be separated: grow the partition
ONCE with the repaired faculty, then rebuild the per-cell heads over that SAME partition twice --
once flat (Laplace count-MLE), once Witten-Bell -- using the engine's own _jh_counts /
_jh_counts_wb over the engine's own _jh_assign. Same centers, same owners, same test set. The
estimator is the only difference. (H_9309's E2 did this on a toy stream; this does it for real.)

Frozen bars: FREEZE.txt.
"""
import hashlib, json, math, os, sys, time, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import engine_cli as E                                    # the LIVE engine

KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
H9311_WB_320 = 2.46370          # CALIB anchor (H_9311, grow_max=320)
CALIB_TOL = 0.01
D1_MARGIN = 0.02
HANGUL_LO, HANGUL_HI = 44032, 55203
KO_STRIDE = 2500
LAPLACE = 1.0
MIN_OWNED = 8
SPLIT_THRESH_CE = 0.05
LADDER = [10, 40, 160, 320]


def log(*a):
    print(*a, flush=True)


def syll_nbytes(n):
    return [1, 1, 1] if n == 3 else ([2, 1] if n == 2 else [3])


def build(raw):
    text = raw.decode("utf-8", errors="ignore")
    jset = set()
    for ch in text:
        if HANGUL_LO <= ord(ch) <= HANGUL_HI:
            for j in unicodedata.normalize("NFD", ch):
                jset.add(ord(j))
    js = sorted(jset)
    j2i = {cp: 256 + i for i, cp in enumerate(js)}
    vj = 256 + len(js)
    syms, nby, depth, d = [], [], [], 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_nbytes(len(nfd))
            for k, jc in enumerate(nfd):
                syms.append(j2i[ord(jc)]); nby.append(nb[k])
                d = 0 if k == 0 else d + 1
                depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                syms.append(b); nby.append(1)
                d = d + 1 if 128 <= b <= 191 else 0
                depth.append(d)
    return syms, nby, depth, vj, len(js)


def score(centers, heads, vj, Xte, Yte, NBte):
    af = E._jh_field(centers, len(centers))
    own = E._jh_assign(af, Xte)
    nats = 0.0
    for i in range(len(Xte)):
        nats -= math.log(heads[own[i]][Yte[i]] + 1e-12)
    return nats / float(sum(NBte))


def main():
    t0 = time.time()
    corpus = sys.argv[1]
    raw = open(corpus, "rb").read()[:30000000]
    sha = hashlib.sha256(raw).hexdigest()
    log(f"[C1] sha={sha[:16]}...  match={sha == KO_SHA}")
    if sha != KO_SHA:
        log("FATAL: sha mismatch. STOP."); sys.exit(2)
    syms, nby, depth, vj, nj = build(raw)
    log(f"[C1] Vj={vj} (anchor 323)")
    if vj != 323:
        log("FATAL: Vj != 323. STOP."); sys.exit(2)

    X, Y, NB = [], [], []
    n = len(syms)
    i = 4
    while i < n - 1:
        X.append([syms[i-1]/float(vj), syms[i-2]/float(vj), depth[i-1]/3.0])
        Y.append(syms[i]); NB.append(nby[i])
        i += 1
    X, Y, NB = X[::KO_STRIDE], Y[::KO_STRIDE], NB[::KO_STRIDE]
    Xtr = [X[k] for k in range(len(X)) if k % 2 == 0]
    Ytr = [Y[k] for k in range(len(Y)) if k % 2 == 0]
    Xte = [X[k] for k in range(len(X)) if k % 2 == 1]
    Yte = [Y[k] for k in range(len(Y)) if k % 2 == 1]
    NBte = [NB[k] for k in range(len(NB)) if k % 2 == 1]
    log(f"[split] scored={len(X)} train={len(Xtr)} test={len(Xte)}")

    cfg = E.EngineConfig(True, True, True, True)
    seeds = [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]
    pooled = E._jh_pooled(Ytr, len(Xtr), vj, LAPLACE)
    res = {"id": "H_9313", "corpus_sha256": sha, "vj": vj, "stride": KO_STRIDE, "sweep": []}

    log("\n[SWEEP] grow ONCE per rung with the repaired faculty; rebuild the head twice over the")
    log("        SAME partition (engine's own _jh_counts / _jh_counts_wb). Estimator = only change.")
    for gm in LADDER:
        g = E.jamo_head_grow_shrink(E.jamo_head_new([r[:] for r in seeds], vj, 3),
                                    Xtr, Ytr, len(Xtr), gm, MIN_OWNED, SPLIT_THRESH_CE, LAPLACE, cfg)
        cells = E.jamo_head_cells(g)
        af = E._jh_field(g.centers, cells)
        own = E._jh_assign(af, Xtr)
        flat_heads = [E._jh_counts(Ytr, own, k, len(Xtr), vj, LAPLACE) for k in range(cells)]
        wb_heads = [E._jh_counts_wb(Ytr, own, k, len(Xtr), vj, pooled) for k in range(cells)]
        ce_f = score(g.centers, flat_heads, vj, Xte, Yte, NBte)
        ce_w = score(g.centers, wb_heads, vj, Xte, Yte, NBte)
        res["sweep"].append({"grow_max": gm, "cells": cells, "flat_ce": ce_f, "wb_ce": ce_w})
        log(f"  cells={cells:4d}  ~{len(Xtr)//max(cells,1):4d} pts/cell   "
            f"FLAT-head {ce_f:.5f}   WB-head {ce_w:.5f}   d={ce_w-ce_f:+.5f}")

    first, last = res["sweep"][0], res["sweep"][-1]
    calib = abs(last["wb_ce"] - H9311_WB_320) <= CALIB_TOL
    log(f"\n[C2 CALIB] WB-head @320 = {last['wb_ce']:.5f}  vs H_9311 anchor {H9311_WB_320}  "
        f"d={last['wb_ce']-H9311_WB_320:+.5f} -> {'PASS' if calib else 'FAIL'}")
    res["CALIB_pass"] = bool(calib)
    if not calib:
        res["verdict"] = "INVALID - CALIB fail vs H_9311 anchor; bars NOT read"
        log(f"\nVERDICT: {res['verdict']}")
        json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "h9313_result.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(0)

    flat_deg = last["flat_ce"] - first["flat_ce"]
    wb_deg = last["wb_ce"] - first["wb_ce"]
    d1 = flat_deg >= D1_MARGIN
    log(f"\nD1 STARVATION-ENGAGED (FLAT-head degrades >= +{D1_MARGIN}) : {d1}   "
        f"(flat {flat_deg:+.5f})")

    if not d1:
        v = ("UNREADABLE - the FLAT head did not degrade over the sweep => the starvation axis is not "
             "engaged in this window (stride 2500); the dissociation bar cannot be read here. This is "
             "an un-engaged axis, NOT a refutation. Needs more cells or a smaller stride (new prereg).")
        res.update({"D1_starvation_engaged": False, "flat_degradation": flat_deg,
                    "wb_degradation": wb_deg, "verdict": v, "wall_s": time.time() - t0})
        log(f"\nVERDICT: {v}")
        json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "h9313_result.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(0)

    d2 = wb_deg < flat_deg
    log(f"D2 DISSOCIATION       (WB degrades less than FLAT)     : {d2}   "
        f"(wb {wb_deg:+.5f} vs flat {flat_deg:+.5f})")
    if d2:
        v = ("DISSOCIATED - the H_9301 mirror finding transfers to the real corpus engine-native: over "
             "the SAME partition, the flat count-MLE head degrades under starvation while the "
             "shrinkage head does not (or degrades less)")
    else:
        v = ("NO-DISSOC - starvation IS engaged but shrinkage does not blunt it => the mirror's "
             "dissociation does not hold on the real corpus (honest negative, bar unmoved)")
    res.update({"D1_starvation_engaged": True, "D2_dissociation": bool(d2),
                "flat_degradation": flat_deg, "wb_degradation": wb_deg,
                "GREEN": bool(d2), "verdict": v, "wall_s": time.time() - t0})
    log(f"\nVERDICT: {v}")
    log(f"wall={time.time()-t0:.1f}s")
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "h9313_result.json"), "w"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
