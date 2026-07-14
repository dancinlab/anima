#!/usr/bin/env python3
"""H_9311 — where does growth STOP once the budget is released? (engine-native, real corpus)

H_9309 wired jamo_head_grow_shrink into core/engine_cli and passed its two bars -- but its smoke
ran on a TOY SYNTHETIC stream (labelled honestly). This closes that gap: the same LIVE engine
faculties, fed the REAL 30MB KO window (sha c47b6808..., byte-identical to H_1307 RUN A / H_1316 /
H_9298), on H_1321's engine-native configuration (Vj=323, ko_stride=2500, nats/UTF-8-byte).

    FLAT   = E.jamo_head_grow          (the existing, H_1321-verified path -- untouched)
    SHRINK = E.jamo_head_grow_shrink   (H_9309: growth repair + Witten-Bell head)

CALIB (blocking): the FLAT arm must reproduce H_1321's engine-native anchor 2.82046 (|d| <= 0.05)
before either bar is read. Frozen bars: FREEZE.txt.
"""
import hashlib, json, os, sys, time, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import engine_cli as E                                    # the LIVE engine

KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
H9310_FLAT_40 = 2.82046   # H_9310 anchors at grow_max=40 -- the CALIB gate
H9310_SHRINK_40 = 2.71886
B1_MARGIN = 0.02
FLAT_TOL = 0.01
CALIB_TOL = 0.05
R2_MARGIN = 0.02
HANGUL_LO, HANGUL_HI = 44032, 55203
KO_STRIDE = 2500
LAPLACE = 1.0
MIN_OWNED = 8
SPLIT_THRESH_CE = 0.05


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


def ce_per_byte(jh, Xte, Yte, NBte):
    """Same head, same partition -- scored on H_1321's nats/UTF-8-byte axis (the engine's own
    jamo_head_ce returns nats/symbol; the anchor is per byte, so we score per byte)."""
    import math
    af = E._jh_field(jh.centers, len(jh.centers))
    own = E._jh_assign(af, Xte)
    nats = 0.0
    for i in range(len(Xte)):
        nats -= math.log(jh.heads[own[i]][Yte[i]] + 1e-12)
    return nats / float(sum(NBte))


def main():
    t0 = time.time()
    corpus = sys.argv[1]
    grow_max = int(sys.argv[2]) if len(sys.argv) > 2 else 40

    raw = open(corpus, "rb").read()[:30000000]
    sha = hashlib.sha256(raw).hexdigest()
    log(f"[C1] corpus sha={sha[:16]}...  match={sha == KO_SHA}")
    if sha != KO_SHA:
        log("FATAL: sha != H_1307 RUN A anchor. STOP."); sys.exit(2)

    syms, nby, depth, vj, njamo = build(raw)
    log(f"[C2] Vj={vj} (anchor 323)  distinct jamo={njamo}")
    if vj != 323:
        log("FATAL: Vj != 323. STOP."); sys.exit(2)

    X, Y, NB = [], [], []
    n = len(syms)
    i = 4
    while i < n - 1:
        X.append([syms[i - 1] / float(vj), syms[i - 2] / float(vj), depth[i - 1] / 3.0])
        Y.append(syms[i]); NB.append(nby[i])
        i += 1
    X, Y, NB = X[::KO_STRIDE], Y[::KO_STRIDE], NB[::KO_STRIDE]
    Xtr = [X[k] for k in range(len(X)) if k % 2 == 0]
    Ytr = [Y[k] for k in range(len(Y)) if k % 2 == 0]
    Xte = [X[k] for k in range(len(X)) if k % 2 == 1]
    Yte = [Y[k] for k in range(len(Y)) if k % 2 == 1]
    NBte = [NB[k] for k in range(len(NB)) if k % 2 == 1]
    log(f"[split] scored={len(X)}  train={len(Xtr)}  test={len(Xte)}  (H_1321 window, stride {KO_STRIDE})")

    cfg = E.EngineConfig(True, True, True, True)          # mitosis ON (p8 growth gate)
    seeds = [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]

    res = {"id": "H_9311", "corpus_sha256": sha, "vj": vj, "stride": KO_STRIDE,
           "scored": len(X), "sweep": []}
    log("\n[SWEEP] budget released. Both arms are LIVE engine faculties; all points reported.")
    for gm in [10, 20, 40, 80, 160, 320]:
        f = E.jamo_head_grow(E.jamo_head_new([r[:] for r in seeds], vj, 3),
                             Xtr, Ytr, len(Xtr), gm, MIN_OWNED, SPLIT_THRESH_CE, LAPLACE, cfg)
        w = E.jamo_head_grow_shrink(E.jamo_head_new([r[:] for r in seeds], vj, 3),
                                    Xtr, Ytr, len(Xtr), gm, MIN_OWNED, SPLIT_THRESH_CE, LAPLACE, cfg)
        fc, wc = E.jamo_head_cells(f), E.jamo_head_cells(w)
        fce, wce = ce_per_byte(f, Xte, Yte, NBte), ce_per_byte(w, Xte, Yte, NBte)
        res["sweep"].append({"grow_max": gm, "flat_cells": fc, "flat_ce": fce,
                             "shrink_cells": wc, "shrink_ce": wce})
        log(f"  grow_max={gm:4d}   FLAT {fc:3d} cells {fce:.5f}   "
            f"SHRINK {wc:3d} cells {wce:.5f}   d={wce-fce:+.5f}")

    at40 = [r for r in res["sweep"] if r["grow_max"] == 40][0]
    calib = (abs(at40["flat_ce"] - H9310_FLAT_40) <= FLAT_TOL and
             abs(at40["shrink_ce"] - H9310_SHRINK_40) <= FLAT_TOL)
    log(f"\n[CALIB @ grow_max=40] FLAT {at40['flat_ce']:.5f} (anchor {H9310_FLAT_40}) · "
        f"SHRINK {at40['shrink_ce']:.5f} (anchor {H9310_SHRINK_40}) -> {'PASS' if calib else 'FAIL'}")
    res["CALIB_pass"] = bool(calib)
    if not calib:
        res["verdict"] = "INVALID - CALIB fail vs H_9310 anchors; bars NOT read"
        log(f"\nVERDICT: {res['verdict']}")
        json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "h9311_result.json"), "w"),
                  indent=2, ensure_ascii=False)
        sys.exit(0)

    last = res["sweep"][-1]
    b1 = last["shrink_ce"] <= at40["shrink_ce"] - B1_MARGIN
    # B2: first plateau (|dCE| < 0.01 between adjacent points)
    plateau = None
    for i in range(1, len(res["sweep"])):
        if abs(res["sweep"][i]["shrink_ce"] - res["sweep"][i-1]["shrink_ce"]) < 0.01:
            plateau = res["sweep"][i]["shrink_cells"]; break
    flat_deg = res["sweep"][-1]["flat_ce"] - res["sweep"][0]["flat_ce"]
    shrink_deg = last["shrink_ce"] - at40["shrink_ce"]

    log(f"\nB1 GROWTH-PAYS  (SHRINK@max <= SHRINK@40 - {B1_MARGIN}) : {b1}   (d={shrink_deg:+.5f})")
    log(f"B2 SATURATION   first plateau at cells = {plateau}")
    log(f"B3 FLAT-CONTROL flat change over sweep = {flat_deg:+.5f}  (>0 = starvation engaged)")

    if b1:
        v = ("GROWTH-PAYS - releasing the budget keeps improving => growth is PRODUCTIVE on the real "
             "corpus; H_9301's G3 ('harmless but not productive') FLIPS here")
    elif shrink_deg > 0.02:
        v = ("DEGRADES - shrinkage does NOT stop the pool from getting worse as it grows => something "
             "the estimator cannot fix (new finding)")
    else:
        v = ("SATURATES - growth is HARMLESS but NOT PRODUCTIVE (H_9301 G3 confirmed engine-native on "
             "the real corpus): past a point, splitting more cells buys nothing")
    res.update({"B1_growth_pays": bool(b1), "B2_plateau_cells": plateau,
                "B3_flat_degradation": flat_deg, "shrink_delta_vs_40": shrink_deg,
                "verdict": v, "wall_s": time.time() - t0})
    log(f"\nVERDICT: {v}")
    log(f"wall={time.time()-t0:.1f}s")
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "h9311_result.json"), "w"),
              indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
