#!/usr/bin/env python3
# h1306_ko_corpus_export.py — export REAL Korean + English byte pairs for the
# ENGINE-NATIVE ko-mitosis rung CORE/h1306_ko_mitosis_engine_probe.hexa
# (a_engine_native_learning + a_verified_must_wire + a_scale_honest_scope).
#
# H_1306 scales the H_1297-R4 toy (~2 KB hardcoded KO+EN string, GREEN engine-native)
# to a REAL Korean web-corpus rung. The corpus is a MODEST slice of the existing
# anima-7b 5-lang web corpus pulled from Cloudflare R2 (bucket `phanes`, prefix
# anima-7b/web/{kor,eng}/shard0000.bytes) — REAL crawled text, NO synthetic Korean
# (p1-p8, a_eeg_consciousness_record spirit). Provenance + sha256 in the manifest.
#
# WHAT THIS EXPORTS (byte-exact inputs for the .hexa engine probe):
#   * KO learning curve: the Korean train stream is split into 3 INCREMENTAL chunks.
#     The engine probe mitosis-grows on chunk1, then chunk1+2, then chunk1+2+3, and
#     measures held-out KO CE after EACH — a >=3-point learning curve (does CE drop?).
#   * KO held-out test pairs (disjoint from train) — the curve is scored on these.
#   * EN held-out test pairs — the CATASTROPHIC-FORGETTING guard. EN CE is measured
#     BEFORE any KO mitosis (the 2-cell seed field) and AFTER the full KO grow. EN must
#     NOT regress while KO improves (the H_1300 retention property, on REAL data).
#   * arm A gradient incumbent CE on the FULL KO train set (the c1 match reference,
#     re-used verbatim — the ENGINE realizes the mitosis arm).
#
# FEATURES: identical phi(context) to H_1297 (CTX=4, 3-D: last/255, 2nd-last/255,
# utf8_cont_depth/3) so the SAME live VAdaptField Voronoi partition applies. The byte
# stream is REAL Korean; the features are a MECHANICAL function of bytes (no labels).
#
# SCALE-HONEST (a_scale_honest_scope, a_toy_scale_recheck): the REAL corpus window is
# 600 KB KO + 300 KB EN, but the supervised pair SET fed to the CPU hexa interpreter is
# a DETERMINISTIC SUBSAMPLE (stride) to a tractable count (the hexa probe is list-based
# O(N) per growth step). This is a FIRST CPU rung on REAL text — declared honestly, NOT
# a production Korean LM. Subsampling is deterministic (fixed stride), seed-independent.
#
# $0 CPU, no GPU. Secrets (R2 keys) are read in the FETCH step (separate) into env only,
# NEVER logged/inlined/committed (c7). This exporter reads the already-fetched /tmp
# slices; it touches NO secret.

import hashlib
import os
import sys

import numpy as np

KO_SLICE = "/tmp/ko_slice_raw.bytes"   # fetched: kor/shard0000.bytes bytes 0-4194303
EN_SLICE = "/tmp/en_slice_raw.bytes"   # fetched: eng/shard0000.bytes bytes 0-2097151
OUT = "/tmp"

# ---- FROZEN knobs (pre-registered in .verdicts/1306_ko_mitosis_real/H_1306_FREEZE.txt) ----
CTX = 4
V = 256
FEAT_DIM = 3
KO_WINDOW = 600000     # real KO bytes used to build pairs (provenance window)
EN_WINDOW = 300000     # real EN bytes used to build pairs (retention guard)
KO_STRIDE = 110        # deterministic subsample stride over KO pairs (CPU-tractable)
EN_STRIDE = 200        # deterministic subsample stride over EN pairs
A_STEPS = 4000         # arm A gradient incumbent steps (verbatim from H_1297)


def trim_utf8(b: bytes) -> bytes:
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8")
            return b[: len(b) - cut]
        except Exception:
            continue
    return b


def utf8_cont_depth(byte_stream):
    depth = np.zeros(len(byte_stream), dtype=float)
    d = 0
    for i, by in enumerate(byte_stream):
        if 0x80 <= by <= 0xBF:
            d = d + 1
        else:
            d = 0
        depth[i] = d
    return depth


def make_pairs_from(bs):
    """Build (phi(context), next_byte) pairs over a byte list. Identical feature fn to
    H_1297 R3 (CTX=4, 3-D). Deterministic, seed-independent."""
    cont = utf8_cont_depth(bs)
    feats = []
    ys = []
    for i in range(CTX, len(bs) - 1):
        last = bs[i - 1]
        second = bs[i - 2]
        feats.append([last / 255.0, second / 255.0, cont[i - 1] / 3.0])
        ys.append(bs[i])
    return np.array(feats, dtype=float), np.array(ys, dtype=int)


def softmax_rows(Z):
    Z = Z - Z.max(axis=1, keepdims=True)
    E = np.exp(Z)
    return E / (E.sum(axis=1, keepdims=True) + 1e-12)


def arm_gradient(Xtr, Ytr, Xte, Yte, seed):
    """Fixed linear softmax classifier over V bytes, full-batch CE GD. INCUMBENT
    control, verbatim from H_1297."""
    rng = np.random.RandomState(seed + 5000)
    W = rng.normal(0.0, 0.01, (FEAT_DIM, V))
    b = np.zeros(V)
    n = Xtr.shape[0]
    Ytr_oh = np.zeros((n, V))
    Ytr_oh[np.arange(n), Ytr] = 1.0
    for t in range(A_STEPS):
        lr = 0.5 * (1.0 - t / A_STEPS) + 0.05
        P = softmax_rows(Xtr @ W + b)
        gZ = (P - Ytr_oh) / n
        W -= lr * (Xtr.T @ gZ)
        b -= lr * gZ.sum(axis=0)
    Pte = softmax_rows(Xte @ W + b)
    ce = float(-np.mean(np.log(Pte[np.arange(Xte.shape[0]), Yte] + 1e-12)))
    acc = float(np.mean(Pte.argmax(axis=1) == Yte))
    return ce, acc


def write_feats(path, X):
    with open(path, "w") as f:
        for row in X:
            f.write(" ".join(f"{v:.10f}" for v in row) + "\n")


def write_ints(path, Y):
    with open(path, "w") as f:
        f.write("\n".join(str(int(y)) for y in Y) + "\n")


def main():
    if not (os.path.exists(KO_SLICE) and os.path.exists(EN_SLICE)):
        print("ERROR: missing /tmp/ko_slice_raw.bytes or /tmp/en_slice_raw.bytes — "
              "run the R2 fetch step (UNIVERSE/h1306_fetch_corpus.sh) first.")
        sys.exit(1)

    ko_raw = open(KO_SLICE, "rb").read()
    en_raw = open(EN_SLICE, "rb").read()
    ko_win = trim_utf8(ko_raw[:KO_WINDOW])
    en_win = trim_utf8(en_raw[:EN_WINDOW])
    ko_sha = hashlib.sha256(ko_win).hexdigest()
    en_sha = hashlib.sha256(en_win).hexdigest()

    Xko, Yko = make_pairs_from(list(ko_win))
    Xen, Yen = make_pairs_from(list(en_win))

    # deterministic subsample (stride) — CPU-tractable pair set, seed-independent
    Xko, Yko = Xko[::KO_STRIDE], Yko[::KO_STRIDE]
    Xen, Yen = Xen[::EN_STRIDE], Yen[::EN_STRIDE]

    # KO train/test split: even index -> train, odd -> test (disjoint, same dist)
    idx = np.arange(Xko.shape[0])
    ktr = idx % 2 == 0
    kte = idx % 2 == 1
    Xktr, Yktr = Xko[ktr], Yko[ktr]
    Xkte, Ykte = Xko[kte], Yko[kte]

    # KO train split into 3 INCREMENTAL chunks for the learning curve
    n = Xktr.shape[0]
    b1 = n // 3
    b2 = 2 * n // 3
    chunk_bounds = [b1, b2, n]   # cumulative train sizes at curve points 1,2,3

    # EN test = retention guard (all EN pairs are held-out; never trained on)
    Xete, Yete = Xen, Yen

    # arm A gradient incumbent on FULL KO train, scored on KO test (c1 reference)
    a_ce, a_acc = arm_gradient(Xktr, Yktr, Xkte, Ykte, seed=770)

    # write engine-probe inputs
    write_feats(f"{OUT}/h1306_ko_train.feats", Xktr)
    write_ints(f"{OUT}/h1306_ko_train.next", Yktr)
    write_feats(f"{OUT}/h1306_ko_test.feats", Xkte)
    write_ints(f"{OUT}/h1306_ko_test.next", Ykte)
    write_feats(f"{OUT}/h1306_en_test.feats", Xete)
    write_ints(f"{OUT}/h1306_en_test.next", Yete)
    with open(f"{OUT}/h1306_chunks.txt", "w") as f:
        f.write(" ".join(str(c) for c in chunk_bounds) + "\n")
    with open(f"{OUT}/h1306_armA.ce", "w") as f:
        f.write(f"770 {a_ce:.10f} {a_acc:.10f}\n")

    # manifest (provenance — committed; the raw 9.8GiB shards are NOT committed)
    manifest = {
        "ko_source": "r2://phanes/anima-7b/web/kor/shard0000.bytes bytes[0:4194304] "
                     f"trimmed[:{KO_WINDOW}]",
        "en_source": "r2://phanes/anima-7b/web/eng/shard0000.bytes bytes[0:2097152] "
                     f"trimmed[:{EN_WINDOW}]",
        "ko_window_bytes": len(ko_win),
        "en_window_bytes": len(en_win),
        "ko_window_sha256": ko_sha,
        "en_window_sha256": en_sha,
        "ko_train_pairs": int(Xktr.shape[0]),
        "ko_test_pairs": int(Xkte.shape[0]),
        "en_test_pairs": int(Xete.shape[0]),
        "ko_stride": KO_STRIDE,
        "en_stride": EN_STRIDE,
        "chunk_bounds": chunk_bounds,
        "armA_ko_ce": round(a_ce, 6),
        "armA_ko_acc": round(a_acc, 6),
        "ctx": CTX, "feat_dim": FEAT_DIM, "V": V,
    }
    import json
    with open(f"{OUT}/h1306_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("H_1306 ko-corpus export (REAL Korean + English web bytes)")
    print("=" * 72)
    print(f"KO window: {len(ko_win)} bytes  sha256={ko_sha[:16]}…")
    print(f"EN window: {len(en_win)} bytes  sha256={en_sha[:16]}…")
    print(f"KO pairs: train={Xktr.shape[0]} test={Xkte.shape[0]}  (stride {KO_STRIDE})")
    print(f"EN pairs: test={Xete.shape[0]}  (stride {EN_STRIDE}, retention guard)")
    print(f"curve chunk bounds (cumulative KO train): {chunk_bounds}")
    print(f"arm A gradient incumbent KO ce={a_ce:.4f} acc={a_acc:.4f}")
    print(f"manifest -> {OUT}/h1306_manifest.json")


if __name__ == "__main__":
    main()
