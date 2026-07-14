#!/usr/bin/env python3
"""H_9313 — PEDESTAL + C1 controls bolted onto H_9311's GROWTH-PAYS.

The instrument is H_9311's, copied verbatim (same corpus window / sha / Vj / stride / even-odd
split / ce_per_byte axis / LIVE engine faculties). ONLY the arm set changes.

  E     = repair + WB head, grown on the real (Xtr,Ytr)            [H_9311's experimental arm]
  C1    = E's centers EXACTLY, head refilled flat leaf-MLE          [mediating-covariate control]
  P0X   = grown on a ROW-SHUFFLED X' (split choice independent of Y), head refilled on real (X,Y)
  P0Y   = targets shuffled in BOTH train and test (X _|_ Y) -> truth = 0, any gain = estimator
  P1    = a 4th SPIKE-IN axis (Y/Vj) that determines Y             [positive control / liveness]

Usage:  h9313_arms.py prep <corpus>
        h9313_arms.py run <arm> <seed_idx> <grow_max>
"""
import hashlib, json, math, os, pickle, random, sys, time, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
for _c in (os.path.join(HERE, "..", "..", "core"), os.path.join(HERE, "core")):
    if os.path.isfile(os.path.join(_c, "engine_cli.py")):
        sys.path.insert(0, _c); break
import engine_cli as E                                   # the LIVE engine

KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
HANGUL_LO, HANGUL_HI = 44032, 55203
KO_STRIDE = 2500
LAPLACE = 1.0
MIN_OWNED = 8
SPLIT_THRESH_CE = 0.05
XSHUF_SEED = 7                                           # P0X row-shuffle (frozen, PREREG)
YSHUF_TR, YSHUF_TE = 20260714, 20260715                  # P0Y engine shuffle seeds (frozen)
DATA = os.path.join(HERE, "results", "data.pkl")


def log(*a):
    print(*a, flush=True)


def syll_nbytes(n):
    return [1, 1, 1] if n == 3 else ([2, 1] if n == 2 else [3])


def build(raw):
    """H_9311 build(), verbatim."""
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


def prep(corpus):
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
    d = {
        "vj": vj, "sha": sha,
        "Xtr": [X[k] for k in range(len(X)) if k % 2 == 0],
        "Ytr": [Y[k] for k in range(len(Y)) if k % 2 == 0],
        "Xte": [X[k] for k in range(len(X)) if k % 2 == 1],
        "Yte": [Y[k] for k in range(len(Y)) if k % 2 == 1],
        "NBte": [NB[k] for k in range(len(NB)) if k % 2 == 1],
        "scored": len(X),
    }
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    pickle.dump(d, open(DATA, "wb"))
    log(f"[split] scored={len(X)}  train={len(d['Xtr'])}  test={len(d['Xte'])}  (stride {KO_STRIDE})")


# ---------------------------------------------------------------- instrument (H_9311 verbatim)
def point_nats(jh, Xte, Yte):
    """Per-test-point -log p, on the same head/partition H_9311 scored. ce_per_byte() below is
    H_9311's function byte-for-byte; this just keeps the summands so a PAIRED test is possible."""
    af = E._jh_field(jh.centers, len(jh.centers))
    own = E._jh_assign(af, Xte)
    return [-math.log(jh.heads[own[i]][Yte[i]] + 1e-12) for i in range(len(Xte))]


def ce_per_byte_from(nats, NBte):
    return sum(nats) / float(sum(NBte))


def seed_pair(idx, dim):
    if idx == 0:
        base = [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]           # H_9311's frozen pair (CALIB)
        if dim == 4:
            return [base[0] + [0.3], base[1] + [0.7]]
        return [r[:] for r in base]
    r = random.Random(100 + idx)
    return [[r.uniform(0.0, 1.0) for _ in range(dim)] for _ in range(2)]


def refill(centers, Xtr, Ytr, vj, dim, mode):
    """Rebuild a head on a GIVEN partition. mode 'flat' = _jh_counts (leaf-MLE) · 'wb' = _jh_counts_wb."""
    af = E._jh_field(centers, len(centers))
    own = E._jh_assign(af, Xtr)
    ntr = len(Xtr)
    heads = []
    if mode == "wb":
        pooled = E._jh_pooled(Ytr, ntr, vj, LAPLACE)
        for k in range(len(centers)):
            heads.append(E._jh_counts_wb(Ytr, own, k, ntr, vj, pooled))
    else:
        for k in range(len(centers)):
            heads.append(E._jh_counts(Ytr, own, k, ntr, vj, LAPLACE))
    return E.JamoHead(centers, heads, vj, dim)


def run(arm, sidx, gm):
    t0 = time.time()
    d = pickle.load(open(DATA, "rb"))
    vj = d["vj"]
    Xtr, Ytr, Xte, Yte, NBte = d["Xtr"], d["Ytr"], d["Xte"], d["Yte"], d["NBte"]
    ntr = len(Xtr)
    cfg = E.EngineConfig(True, True, True, True)            # mitosis ON (p8 growth gate)
    out = {"arm": arm, "seed": sidx, "grow_max": gm, "vj": vj, "n_test": len(Xte),
           "sum_nb": sum(NBte)}

    if arm == "P1":                                          # SPIKE-IN positive control (dim 4)
        dim = 4
        Xtr_u = [Xtr[i] + [Ytr[i] / float(vj)] for i in range(ntr)]
        Xte_u = [Xte[i] + [Yte[i] / float(vj)] for i in range(len(Xte))]
        Ytr_u, Yte_u = Ytr, Yte
    elif arm == "P0Y":                                       # TRUE-ZERO pedestal: X _|_ Y everywhere
        dim = 3
        Xtr_u, Xte_u = Xtr, Xte
        Ytr_u = E.jamo_head_shuffle_targets(Ytr, vj, YSHUF_TR)
        Yte_u = E.jamo_head_shuffle_targets(Yte, vj, YSHUF_TE)
    else:                                                    # E / C1 / P0X
        dim = 3
        Xtr_u, Xte_u, Ytr_u, Yte_u = Xtr, Xte, Ytr, Yte

    if arm == "P0X":
        rnd = random.Random(XSHUF_SEED)
        perm = list(range(ntr)); rnd.shuffle(perm)
        Xgrow = [Xtr[p][:] for p in perm]                    # (X,Y) pairing destroyed for GROWTH only
    else:
        Xgrow = Xtr_u

    jh0 = E.jamo_head_new([r[:] for r in seed_pair(sidx, dim)], vj, dim)
    w = E.jamo_head_grow_shrink(jh0, Xgrow, Ytr_u, ntr, gm, MIN_OWNED, SPLIT_THRESH_CE, LAPLACE, cfg)
    out["cells"] = E.jamo_head_cells(w)

    if arm == "P0X":
        w = refill(w.centers, Xtr, Ytr, vj, dim, "wb")       # head from the REAL (X,Y)
    nats = point_nats(w, Xte_u, Yte_u)
    out["ce"] = ce_per_byte_from(nats, NBte)
    out["nats"] = nats

    if arm == "E":                                           # C1 rides free on E's EXACT centers
        c1 = refill(w.centers, Xtr, Ytr, vj, dim, "flat")
        n1 = point_nats(c1, Xte, Yte)
        out["c1_ce"] = ce_per_byte_from(n1, NBte)
        out["c1_cells"] = E.jamo_head_cells(c1)
        out["c1_nats"] = n1

    out["wall_s"] = time.time() - t0
    p = os.path.join(HERE, "results", f"{arm}_s{sidx}_g{gm}.json")
    json.dump(out, open(p, "w"))
    log(f"[{arm} s{sidx} g{gm}] cells={out['cells']} ce={out['ce']:.5f}"
        + (f" c1_ce={out['c1_ce']:.5f}" if "c1_ce" in out else "")
        + f"  wall={out['wall_s']:.0f}s")


if __name__ == "__main__":
    if sys.argv[1] == "prep":
        prep(sys.argv[2])
    else:
        run(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
