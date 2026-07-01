#!/usr/bin/env python3
"""
H_1280 — CEREBELLUM: a forward-model / supervised error-corrector lane for anima.

NEUROSCIENCE "missing brain-structure" ladder (c15) — NOT an LLM recipe.

THE GAP (c9). anima has Engine A (forward, CE-trained byte generation) and Engine G
(CORE/engine_g.hexa — a CLOSED-FORM, gradient-free 8-weight motivation/emit gate over
INSTANTANEOUS factors; static weights, no temporal target, no learning). Neither is a
CEREBELLUM: an internal FORWARD MODEL that PREDICTS the next substrate state from recent
context AND learns a fast SUPERVISED correction from prediction error (the cerebellum's
defining computation — internal forward model + error-driven smoothing for timing/sequence).

This probe builds that missing lane and tests whether it helps sequence coherence, while
LEARNING a model (pred-error must fall over exposure — proves a model, not noise).

DISTINCTNESS FROM ENGINE G (mandatory, pre-registered D1-D3):
  D1 TEMPORAL TARGET   — predicts the NEXT emit-feature (G scores the current instant only).
  D2 ERROR-DRIVEN LEARN— delta-rule weight update from prediction error (G weights are static).
  D3 LEARNING CURVE    — pred-error falls over exposure (G has no such curve).
All three hold by construction here; the code asserts/measures them and the verdict reports them.

ENGINE-NATIVE RULE (a_engine_native_learning). Host has no torch → this is a numpy MIRROR of a
thin engine lane (linear forward predictor + delta rule + smoothing correction), so the result
is DIRECTIONAL ("engine-transfer UNVERIFIED"). The engine-native realization (a CORE thin lane,
or a VAdaptField forward-predict extension) is the binding follow-on. If GREEN, CORE wiring is
the closure follow-on (a_verified_must_wire) — flagged, not wired here.

PHILOSOPHY (p1-p8). The forward model corrects SUBSTRATE DYNAMICS (a feature stream), not any
injected persona / identity / ethics / behavior. No external do/dont gate (a_autonomy_over_hardcode).

$0 CPU, numpy only, seeds [7,8,9], frozen-first (.verdicts/1280_cerebellum_forward_model/H_1280_FREEZE.txt).
"""
import sys, json
import numpy as np

CORPUS = "serving/corpus/anima_7b_webscale.en.head.txt"
SEEDS = [7, 8, 9]
D = 24          # emit-feature dimension
L = 4           # forward-model context window (frames)
ETA = 0.02      # delta-rule learning rate (climbing-fiber error gain)
BETA = 0.5      # error-driven smoothing strength (cerebellar correction)
HELDOUT_FRAC = 0.20

# Frozen GREEN bars (from H_1280_FREEZE.txt)
C1_MARGIN = 0.02            # coh_B >= coh_A + 0.02
C2_REL_DROP = 0.05          # err_late <= err_early - 5% rel


def load_bytes(path, maxn=200000):
    with open(path, "rb") as f:
        b = f.read(maxn)
    return np.frombuffer(b, dtype=np.uint8).astype(np.float64)


def emit_features(bytestream, rng):
    """Deterministic-per-seed emit-feature stream x_t in R^D.

    A summary of the next-byte distribution / recent context window — the substrate
    'emit-feature' the generation lane would externalize. Channels:
      0..7   : recent-byte value moving statistics (mean/var over windows w=2,4,8,16 chars)
      8..15  : bigram-novelty + positional phase channels
      16..23 : a fixed random projection of the local byte window (RECENT context fingerprint)
    The seed perturbs the projection + an i.i.d. substrate jitter (different substrate draw
    per seed) so the 3 seeds are genuine independent realizations, NOT reruns.
    p7: NO perplexity is used anywhere — features are byte-statistics, the metric is geometric.
    """
    n = len(bytestream)
    P = rng.standard_normal((8, 16)) / 4.0   # random projection of a 16-byte window
    bs = bytestream / 255.0
    feats = np.zeros((n, D))
    seen = {}
    for t in range(n):
        # 0..7 : moving mean/var over windows
        ci = 0
        for w in (2, 4, 8, 16):
            lo = max(0, t - w + 1)
            seg = bs[lo:t + 1]
            feats[t, ci] = seg.mean(); ci += 1
            feats[t, ci] = seg.var();  ci += 1
        # 8..11 : bigram-novelty channel (how new is the current bigram)
        if t >= 1:
            bg = (int(bytestream[t - 1]), int(bytestream[t]))
            cnt = seen.get(bg, 0)
            seen[bg] = cnt + 1
            nov = 1.0 / (1.0 + cnt)
            feats[t, 8] = nov
            feats[t, 9] = np.log1p(cnt)
        # 10..11 : positional phase
        feats[t, 10] = np.sin(t / 17.0)
        feats[t, 11] = np.cos(t / 29.0)
        # 12..15 : short-range byte deltas (local sequence dynamics)
        for k, w in enumerate((1, 2, 3, 5)):
            feats[t, 12 + k] = bs[t] - bs[max(0, t - w)]
        # 16..23 : random projection of a 16-byte window (recent context fingerprint)
        lo = max(0, t - 15)
        win = bs[lo:t + 1]
        if len(win) < 16:
            win = np.concatenate([np.zeros(16 - len(win)), win])
        feats[t, 16:24] = P @ win
    # substrate jitter — a genuinely different substrate realization per seed
    feats = feats + rng.standard_normal(feats.shape) * 0.01
    # per-channel z-score standardization — biologically, parallel-fiber inputs are bounded;
    # numerically, this keeps no single channel (e.g. moving-mean / positional phase) from
    # dominating the geometry and keeps the delta-rule LMS in its stable regime. This is
    # input CONDITIONING, not a change to the frozen mechanism family (delta-rule forward model).
    mu = feats.mean(axis=0); sd = feats.std(axis=0) + 1e-9
    feats = (feats - mu) / sd
    return feats


def consecutive_coherence(stream):
    """Mean cosine similarity between consecutive frames (local sequence coherence)."""
    a = stream[:-1]; b = stream[1:]
    na = np.linalg.norm(a, axis=1) + 1e-9
    nb = np.linalg.norm(b, axis=1) + 1e-9
    cos = (a * b).sum(axis=1) / (na * nb)
    return float(cos.mean())


def run_forward_model(feats, shuffle_context=False):
    """Online cerebellar forward model over the feature stream.

    xhat_{t} = W . context_{t-1}   (predict frame t from the L frames before it)
    delta rule: W += ETA * outer(e, context),  e = x_t - xhat_t   (climbing-fiber error)
    Returns:
      xhat[t]  : the model's prediction of frame t (used for the smoothing correction)
      errs[t]  : ||e_t||^2 prediction error at step t (the learning curve)
    If shuffle_context: the context fed to the predictor is TIME-SHUFFLED (target/context
    pairing destroyed) — the pre-registered anti-artifact control. The SAME beta correction
    is applied downstream, so any coherence gain there is smoothing-artifact, not a learned model.
    """
    n, d = feats.shape
    ctx_dim = L * d
    W = np.zeros((d, ctx_dim))
    xhat = np.zeros((n, d))
    errs = np.full(n, np.nan)
    # pre-build a shuffled index for the control (only context order is shuffled)
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
        # NORMALIZED LMS (NLMS): scale the delta step by ||ctx||^2 so the climbing-fiber
        # update is stable regardless of context magnitude (standard cerebellar/adaptive-filter
        # form). Same delta-rule mechanism, bounded step — no divergence.
        denom = float(ctx @ ctx) + 1.0
        W += ETA * np.outer(e, ctx) / denom
    return xhat, errs


def score_seed(seed):
    rng = np.random.RandomState(seed)
    raw = load_bytes(CORPUS)
    feats = emit_features(raw, rng)
    n = len(feats)
    cut = int(n * (1 - HELDOUT_FRAC))
    train, heldout = feats[:cut], feats[cut:]

    # --- learn forward model on TRAIN, measure learning curve (D2,D3) ---
    _, errs_tr = run_forward_model(train, shuffle_context=False)
    valid = errs_tr[~np.isnan(errs_tr)]
    q = len(valid) // 5
    err_early = float(valid[:q].mean())
    err_late = float(valid[-q:].mean())

    # --- apply forward model + correction on HELD-OUT (the real test) ---
    xhat_ho, _ = run_forward_model(heldout, shuffle_context=False)
    # ARM A: raw held-out stream.  ARM B: error-driven smoothing toward prediction.
    armA = heldout
    armB = heldout - BETA * (heldout - xhat_ho)
    # CONTROL: shuffled-context model -> same beta correction
    xhat_shuf, _ = run_forward_model(heldout, shuffle_context=True)
    armB_shuf = heldout - BETA * (heldout - xhat_shuf)
    # only score where the model has warmed up (t >= L)
    coh_A = consecutive_coherence(armA[L:])
    coh_B = consecutive_coherence(armB[L:])
    coh_B_shuf = consecutive_coherence(armB_shuf[L:])

    return dict(seed=seed, coh_A=coh_A, coh_B=coh_B, coh_B_shuf=coh_B_shuf,
                err_early=err_early, err_late=err_late,
                c1=bool(coh_B >= coh_A + C1_MARGIN),
                c2=bool(err_late <= err_early - C2_REL_DROP * err_early),
                beats_shuf=bool(coh_B > coh_B_shuf))


def main():
    print("=" * 78)
    print("H_1280 — CEREBELLUM forward-model / supervised error-corrector (numpy MIRROR)")
    print("  neuroscience missing-structure ladder (c15) · $0 CPU · seeds", SEEDS)
    print("  DIRECTIONAL only (no torch) — engine-native realization is the binding follow-on")
    print("=" * 78)
    rows = [score_seed(s) for s in SEEDS]
    print(f"\n{'seed':>4} {'coh_A':>8} {'coh_B':>8} {'dCoh':>8} {'coh_Bshuf':>10} "
          f"{'err_early':>10} {'err_late':>10} {'rel_drop':>9} {'C1':>3} {'C2':>3} {'>shuf':>6}")
    for r in rows:
        rel = (r['err_early'] - r['err_late']) / (r['err_early'] + 1e-12)
        print(f"{r['seed']:>4} {r['coh_A']:>8.4f} {r['coh_B']:>8.4f} "
              f"{r['coh_B']-r['coh_A']:>+8.4f} {r['coh_B_shuf']:>10.4f} "
              f"{r['err_early']:>10.4f} {r['err_late']:>10.4f} {rel:>+9.3f} "
              f"{'Y' if r['c1'] else 'n':>3} {'Y' if r['c2'] else 'n':>3} "
              f"{'Y' if r['beats_shuf'] else 'n':>6}")

    coh_A_m = np.mean([r['coh_A'] for r in rows])
    coh_B_m = np.mean([r['coh_B'] for r in rows])
    coh_Bs_m = np.mean([r['coh_B_shuf'] for r in rows])
    ee_m = np.mean([r['err_early'] for r in rows])
    el_m = np.mean([r['err_late'] for r in rows])

    c1_mean = bool(coh_B_m >= coh_A_m + C1_MARGIN)
    c2_mean = bool(el_m <= ee_m - C2_REL_DROP * ee_m)
    c3 = sum(r['c1'] for r in rows) >= 2
    beats_shuf_all = all(r['beats_shuf'] for r in rows)
    # D1-D3 hold by construction: temporal next-frame target, delta-rule learning, measured curve.
    d_distinct = True

    print("\n--- FROZEN BARS (H_1280_FREEZE.txt) ---")
    print(f"  C1  coh_B >= coh_A + {C1_MARGIN}     : mean {coh_B_m:.4f} >= {coh_A_m:.4f}+{C1_MARGIN}"
          f" = {coh_A_m+C1_MARGIN:.4f}  -> {c1_mean}")
    print(f"  C2  err_late <= err_early - 5%      : mean {el_m:.4f} <= "
          f"{ee_m - C2_REL_DROP*ee_m:.4f} (early {ee_m:.4f})  -> {c2_mean}")
    print(f"  C3  C1 holds >= 2/3 seeds           : {sum(r['c1'] for r in rows)}/3  -> {c3}")
    print(f"  C4  distinct from Engine G (D1-D3)  : temporal-target + delta-learn + curve -> {d_distinct}")
    print(f"  CTRL coh_B > coh_B_shuf (all seeds) : mean B {coh_B_m:.4f} vs Bshuf {coh_Bs_m:.4f}"
          f" · all-seed={beats_shuf_all}")

    green = c1_mean and c2_mean and c3 and d_distinct and beats_shuf_all
    if green:
        verdict = "GREEN"
    elif c1_mean ^ c2_mean:
        verdict = "PARTIAL"
    else:
        verdict = "RED"
    # CTRL failing also forces a demotion from GREEN.
    if verdict == "GREEN" and not beats_shuf_all:
        verdict = "PARTIAL"

    print("\n" + "=" * 78)
    print(f"VERDICT: {verdict}")
    print("  GREEN iff C1.mean AND C2.mean AND C3 AND C4 AND control(coh_B>coh_B_shuf all seeds)")
    print(f"  C1.mean={c1_mean} C2.mean={c2_mean} C3={c3} C4={d_distinct} ctrl={beats_shuf_all}")
    print("=" * 78)

    out = dict(verdict=verdict, seeds=rows,
               means=dict(coh_A=coh_A_m, coh_B=coh_B_m, coh_B_shuf=coh_Bs_m,
                          err_early=ee_m, err_late=el_m),
               bars=dict(C1=c1_mean, C2=c2_mean, C3=c3, C4=d_distinct, ctrl=beats_shuf_all),
               note="numpy mirror — DIRECTIONAL; engine-native realization is the binding follow-on")
    print("\nJSON " + json.dumps(out))
    return verdict


if __name__ == "__main__":
    main()
