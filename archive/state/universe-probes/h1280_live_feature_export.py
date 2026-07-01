#!/usr/bin/env python3
"""
H_1280 R2 — feature-stream + numpy-reference export for the LIVE-engine cerebellar
forward-model probe (CORE/h1280_live_cerebellum_probe.hexa).

This is the EXPORT half of the engine-native realization (a_engine_native_learning).
It reproduces the H_1280 R1 numpy MIRROR (UNIVERSE/h1280_cerebellum_forward_model.py)
VERBATIM — same CORPUS, same emit_features, same seeds, same constants — and writes,
per seed:

  /tmp/h1280_feat_seed<S>.txt   the post-z-score DIM=24 feature stream (one frame per
                                line, D space-separated floats). This is the EXACT
                                stream the R1 mirror scores; the live .hexa engine
                                consumes it and reproduces the result with NO numpy.

  /tmp/h1280_ref_seed<S>.txt    the R1 numpy reference for the F2 byte-exact parity
                                check: coh_A coh_B coh_B_shuf err_early err_late
                                (one line, 5 space-separated floats, full precision).

The live engine probe re-derives coh_A / coh_B / coh_B_shuf / err_early / err_late on
the LIVE VForwardField (vforward_new / _predict / _err / _update / _correct, added to
CORE/engine_cli.hexa this round) and asserts they match these references — so the GREEN
is the ACTUAL engine, not the mirror (the binding verdict per a_engine_native_learning).

p7: NO perplexity anywhere — features are byte-statistics, the metric is geometric
cosine coherence + L2 prediction error. $0 CPU, numpy only.
"""
import sys
import numpy as np

CORPUS = "serving/corpus/anima_7b_webscale.en.head.txt"
SEEDS = [7, 8, 9]
D = 24
L = 4
ETA = 0.02
BETA = 0.5
HELDOUT_FRAC = 0.20

# Live-engine tractability (a_engine_native_learning · c2). The R1 mirror scored the
# full 200KB stream (200k frames). The LIVE hexa engine runs the SAME mechanism but
# interpreted, so a 200k-frame run over a 24×96 weight matrix is wall-prohibitive. We
# score a contiguous SUBSET and compute the numpy reference on EXACTLY that subset, so
# the F2 numpy↔hexa parity is byte-exact and the GREEN is on the real engine, not the
# mirror. The cerebellar coherence-lift is a LOCAL-frame property (consecutive cosine),
# so it holds on the subset; the learning curve still has ample exposure. Honest scope:
# the subset is a representative window of the same corpus (a_scale_honest_scope —
# the live realization is the binding leg; full-stream 200k stays the R1 mirror record).
TRAIN_N = 6000      # learning-curve exposure (>> the 5% drop needs only a few k frames)
HELDOUT_N = 3000    # held-out scored window (armA/armB coherence)


def load_bytes(path, maxn=200000):
    with open(path, "rb") as f:
        b = f.read(maxn)
    return np.frombuffer(b, dtype=np.uint8).astype(np.float64)


def emit_features(bytestream, rng):
    """VERBATIM copy of the R1 mirror emit_features (UNIVERSE/h1280_cerebellum_forward_model.py)."""
    n = len(bytestream)
    P = rng.standard_normal((8, 16)) / 4.0
    bs = bytestream / 255.0
    feats = np.zeros((n, D))
    seen = {}
    for t in range(n):
        ci = 0
        for w in (2, 4, 8, 16):
            lo = max(0, t - w + 1)
            seg = bs[lo:t + 1]
            feats[t, ci] = seg.mean(); ci += 1
            feats[t, ci] = seg.var();  ci += 1
        if t >= 1:
            bg = (int(bytestream[t - 1]), int(bytestream[t]))
            cnt = seen.get(bg, 0)
            seen[bg] = cnt + 1
            nov = 1.0 / (1.0 + cnt)
            feats[t, 8] = nov
            feats[t, 9] = np.log1p(cnt)
        feats[t, 10] = np.sin(t / 17.0)
        feats[t, 11] = np.cos(t / 29.0)
        for k, w in enumerate((1, 2, 3, 5)):
            feats[t, 12 + k] = bs[t] - bs[max(0, t - w)]
        lo = max(0, t - 15)
        win = bs[lo:t + 1]
        if len(win) < 16:
            win = np.concatenate([np.zeros(16 - len(win)), win])
        feats[t, 16:24] = P @ win
    feats = feats + rng.standard_normal(feats.shape) * 0.01
    mu = feats.mean(axis=0); sd = feats.std(axis=0) + 1e-9
    feats = (feats - mu) / sd
    return feats


def consecutive_coherence(stream):
    a = stream[:-1]; b = stream[1:]
    na = np.linalg.norm(a, axis=1) + 1e-9
    nb = np.linalg.norm(b, axis=1) + 1e-9
    cos = (a * b).sum(axis=1) / (na * nb)
    return float(cos.mean())


def run_forward_model(feats, shuffle_context=False):
    """VERBATIM copy of the R1 mirror run_forward_model (NLMS delta-rule forward model)."""
    n, d = feats.shape
    ctx_dim = L * d
    W = np.zeros((d, ctx_dim))
    xhat = np.zeros((n, d))
    errs = np.full(n, np.nan)
    if shuffle_context:
        perm = np.random.RandomState(0).permutation(n)
    for t in range(L, n):
        if shuffle_context:
            idx = [perm[(t - L + k) % n] for k in range(L)]
            ctx = np.concatenate([feats[i] for i in idx])
        else:
            ctx = feats[t - L:t].reshape(-1)
        pred = W @ ctx
        xhat[t] = pred
        e = feats[t] - pred
        errs[t] = float(e @ e)
        denom = float(ctx @ ctx) + 1.0
        W += ETA * np.outer(e, ctx) / denom
    return xhat, errs


def main():
    raw = load_bytes(CORPUS)
    for seed in SEEDS:
        rng = np.random.RandomState(seed)
        feats = emit_features(raw, rng)
        n = len(feats)
        cut = int(n * (1 - HELDOUT_FRAC))
        # take the SUBSET windows (contiguous) — train from the head of the train span,
        # heldout from the head of the held-out span. Same frames the live engine reads.
        train = feats[:cut][:TRAIN_N]
        heldout = feats[cut:][:HELDOUT_N]

        # learning curve on TRAIN (D2/D3)
        _, errs_tr = run_forward_model(train, shuffle_context=False)
        valid = errs_tr[~np.isnan(errs_tr)]
        q = len(valid) // 5
        err_early = float(valid[:q].mean())
        err_late = float(valid[-q:].mean())

        # held-out arms (the real test)
        xhat_ho, _ = run_forward_model(heldout, shuffle_context=False)
        armA = heldout
        armB = heldout - BETA * (heldout - xhat_ho)
        xhat_shuf, _ = run_forward_model(heldout, shuffle_context=True)
        armB_shuf = heldout - BETA * (heldout - xhat_shuf)
        coh_A = consecutive_coherence(armA[L:])
        coh_B = consecutive_coherence(armB[L:])
        coh_B_shuf = consecutive_coherence(armB_shuf[L:])

        # export the HELD-OUT feature stream (the leg the live engine scores) so the
        # engine re-derives coh_A/coh_B identically. We export held-out (not the whole
        # stream) because that is exactly armA/armB's input; the live engine runs its
        # OWN forward model over it. err_early/err_late come from TRAIN, so we also
        # export the TRAIN stream for the live learning-curve leg.
        fpath = "/tmp/h1280_feat_seed%d.txt" % seed
        with open(fpath, "w") as f:
            # header: two ints — train_rows heldout_rows — then train rows, then heldout rows.
            f.write("%d %d\n" % (len(train), len(heldout)))
            for row in train:
                f.write(" ".join("%.10g" % v for v in row) + "\n")
            for row in heldout:
                f.write(" ".join("%.10g" % v for v in row) + "\n")

        rpath = "/tmp/h1280_ref_seed%d.txt" % seed
        with open(rpath, "w") as f:
            f.write("%.12g %.12g %.12g %.12g %.12g\n"
                    % (coh_A, coh_B, coh_B_shuf, err_early, err_late))

        # export the shuffle permutation (RandomState(0).permutation over HELDOUT_N) so
        # the live engine's shuffled-context CONTROL reads the SAME index walk — the
        # control is byte-identical to numpy, not a re-draw. One index per line.
        perm = np.random.RandomState(0).permutation(len(heldout))
        ppath = "/tmp/h1280_perm_seed%d.txt" % seed
        with open(ppath, "w") as f:
            f.write("\n".join(str(int(v)) for v in perm) + "\n")

        print("seed=%d  train=%d heldout=%d  coh_A=%.6f coh_B=%.6f (+%.6f) "
              "coh_Bshuf=%.6f  err_early=%.4f err_late=%.4f  -> %s , %s"
              % (seed, len(train), len(heldout), coh_A, coh_B, coh_B - coh_A,
                 coh_B_shuf, err_early, err_late, fpath, rpath))


if __name__ == "__main__":
    main()
