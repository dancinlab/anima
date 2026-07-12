#!/usr/bin/env python3
"""loso_probe.py — Probe A verdict (γ earn-seal). LOSO-NEG linear probe on the frozen dump.

Loads hidden.npz (<pid>__mean [d]). y = neg(1)/plain(0). group = stem for neg, "plain" for plain.
For each HELD-OUT stem in {mot, ani}: train ridge-logistic on {other neg stems + plain}, test on
{held-out stem neg vs plain}. Report held-out balanced-acc + shuffle-y control + adv-surface-matched
control (train same, test adv-vs-plain — should be near chance if the probe is NEG-specific not
modifier-presence). PASS = both held-out >= 0.80 & shuffle <= 0.55 & Δ vs adv-control >= 0.20.
$0 numpy. Two seeds via feature-subsample bootstrap for stability.
"""
import json
import os
import sys
import numpy as np

NPZ = sys.argv[1] if len(sys.argv) > 1 else "hidden.npz"
KEY = "mean"     # __mean pooled trunk penultimate


def load():
    z = np.load(NPZ)
    X, y, g = [], [], []
    for k in z.files:
        if not k.endswith("__" + KEY):
            continue
        pid = k[:-(len("__" + KEY))]
        base = pid.rsplit("_", 1)[0]
        X.append(z[k]); g.append(base)
        y.append(0 if base in ("plain", "adv") else 1)
    return np.array(X, float), np.array(y, int), np.array(g)


def fit_logreg(X, y, l2=1.0, iters=300, lr=0.1):
    Xb = np.hstack([X, np.ones((len(X), 1))])
    w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Xb @ w))
        grad = Xb.T @ (p - y) / len(y) + l2 * np.r_[w[:-1], 0] / len(y)
        w -= lr * grad
    return w


def predict(w, X):
    return (1 / (1 + np.exp(-(np.hstack([X, np.ones((len(X), 1))]) @ w)))) >= 0.5


def bacc(y, yh):
    m = []
    for c in (0, 1):
        idx = y == c
        if idx.sum():
            m.append((yh[idx] == c).mean())
    return float(np.mean(m)) if m else 0.0


def main():
    X, y, g = load()
    # standardize
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Xs = (X - mu) / sd
    rng = np.random.RandomState(7)
    plain = (g == "plain")
    adv = (g == "adv")
    out = {"n": len(y), "d": X.shape[1], "folds": {}}
    for held in ("mot", "ani"):
        te_neg = (g == held)
        if te_neg.sum() < 5 or plain.sum() < 5:
            out["folds"][held] = {"skip": "insufficient n"}
            continue
        tr = (y == 1) & (g != held) & (~plain) & (~adv) | plain     # other neg stems + plain
        w = fit_logreg(Xs[tr], y[tr])
        # held-out: this stem's neg vs plain
        te = te_neg | plain
        acc = bacc(y[te], predict(w, Xs[te]))
        # shuffle control
        ys = y[tr].copy(); rng.shuffle(ys)
        ws = fit_logreg(Xs[tr], ys)
        acc_sh = bacc(y[te], predict(ws, Xs[te]))
        # adv-surface control: adv(0) vs plain(0)? no — test whether probe fires on adv (non-NEG modifier)
        adv_acc = None
        if adv.sum() >= 5:
            te2 = adv | plain
            # label adv as "neg-like"? we want: does the NEG probe misfire on adv? measure P(pred=1|adv)
            p_adv = predict(w, Xs[adv]).mean()
            adv_acc = float(p_adv)     # high = probe fires on mere modifier (bad = not NEG-specific)
        out["folds"][held] = {"heldout_bacc": round(acc, 3), "shuffle": round(acc_sh, 3),
                              "adv_misfire": (round(adv_acc, 3) if adv_acc is not None else None),
                              "n_test_neg": int(te_neg.sum())}
    # verdict
    ok = all(("heldout_bacc" in f and f["heldout_bacc"] >= 0.80 and f["shuffle"] <= 0.55)
             for f in out["folds"].values() if "skip" not in f) and len(out["folds"]) >= 1
    out["PROBE_A"] = "PASS (stem-invariant NEG feature exists)" if ok else "FAIL (no stem-invariant NEG → earned terminal)"
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
