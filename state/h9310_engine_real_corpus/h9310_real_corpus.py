#!/usr/bin/env python3
"""H_9310 — engine-native re-measurement of the shrinkage faculty on the REAL KO jamo stream.

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
H1321_ANCHOR = 2.82046
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
    seeds = [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]            # H_1307 SEED_CENTERS, dim-3

    res = {"id": "H_9310", "corpus_sha256": sha, "vj": vj, "stride": KO_STRIDE,
           "scored": len(X), "grow_max": grow_max}

    log("\n[FLAT]   live E.jamo_head_grow  (the H_1321-verified path)")
    f = E.jamo_head_grow(E.jamo_head_new([r[:] for r in seeds], vj, 3),
                         Xtr, Ytr, len(Xtr), grow_max, MIN_OWNED, SPLIT_THRESH_CE, LAPLACE, cfg)
    f_cells = E.jamo_head_cells(f)
    f_ce = ce_per_byte(f, Xte, Yte, NBte)
    log(f"  cells={f_cells}  CE={f_ce:.5f} nats/byte")

    log("[SHRINK] live E.jamo_head_grow_shrink  (H_9309: growth repair + WB head)")
    w = E.jamo_head_grow_shrink(E.jamo_head_new([r[:] for r in seeds], vj, 3),
                                Xtr, Ytr, len(Xtr), grow_max, MIN_OWNED, SPLIT_THRESH_CE, LAPLACE, cfg)
    w_cells = E.jamo_head_cells(w)
    w_ce = ce_per_byte(w, Xte, Yte, NBte)
    log(f"  cells={w_cells}  CE={w_ce:.5f} nats/byte")

    calib = abs(f_ce - H1321_ANCHOR) <= CALIB_TOL
    log(f"\n[C3 CALIB] FLAT {f_ce:.5f}  vs H_1321 anchor {H1321_ANCHOR}  "
        f"d={f_ce-H1321_ANCHOR:+.5f}  (tol {CALIB_TOL}) -> {'PASS' if calib else 'FAIL'}")
    res.update({"flat_cells": f_cells, "flat_ce": f_ce, "shrink_cells": w_cells, "shrink_ce": w_ce,
                "h1321_anchor": H1321_ANCHOR, "CALIB_pass": bool(calib)})

    if not calib:
        res["verdict"] = "INVALID - CALIB fail: the port does not reproduce H_1321's engine-native anchor; bars NOT read"
        log(f"\nVERDICT: {res['verdict']}")
        json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "h9310_result.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(0)

    r1 = w_cells > f_cells
    r2 = w_ce < f_ce - R2_MARGIN
    log(f"\nR1 GROWTH-UNCAPPED  (SHRINK cells > FLAT cells) : {r1}   ({w_cells} vs {f_cells})")
    log(f"R2 SHRINKAGE-HELPS  (CE_shrink < CE_flat - {R2_MARGIN}) : {r2}   "
        f"(d={w_ce-f_ce:+.5f})")

    if r1 and r2:
        v = ("ENGINE-NATIVE ON REAL CORPUS - both transfers reproduce on the real KO jamo stream "
             "through the live engine faculties (not a toy)")
    elif r2:
        v = ("PARTIAL - shrinkage helps on the real corpus, but the growth cap does not bind here "
             "(honest: the H_9309 toy cap result does not generalize to this stream)")
    elif r1:
        v = ("PARTIAL - the growth cap binds on the real corpus, but shrinkage does not clear the "
             "CE bar (honest negative on R2, bar unmoved)")
    else:
        v = ("KILL - neither transfer reproduces on the real corpus => the mirror gains were "
             "configuration-specific (honest negative, bars unmoved)")
    res.update({"R1_growth_uncapped": bool(r1), "R2_shrinkage_helps": bool(r2),
                "GREEN": bool(r1 and r2), "verdict": v, "wall_s": time.time() - t0})
    log(f"\nVERDICT: {v}")
    log(f"wall={time.time()-t0:.1f}s")
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "h9310_result.json"), "w"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
