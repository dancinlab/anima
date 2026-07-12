#!/usr/bin/env python3
"""spangeom_probe.py — SPAN-GEOM verdict (H_9288 stage-1). Span-level stem-NEG-class frozen probe.

Reads spangeom_hidden.npz (<pid>__seq = [win, d] per prompt) + spangeom_prompts.json (cue per prompt).
Span-pools __seq over the cue's own byte-rows (located in the last --win bytes). Two decisive tests
whether the frozen base 303M forms a stem-invariant NEG class at the SPAN level:

  (i)  LOSO span classifier: train NEG(안/않)-span vs pre-verbal-adverb-span; TEST held-out NEG(못/아니)
       -span vs adverb-span. Byte-identity can't transfer under LOSO → a hit needs a shared NEG feature.
  (ii) RSA Δ = mean cos(within-NEG across stems) − mean cos(NEG↔adverb), vs a label-permutation null.

Controls (probe-defect-census compliant — NO max(controls), paired bootstrap, MDE precomputed):
  · shuffle-y (train on shuffled labels → must floor)
  · adv-misfire (P(pred=NEG | held-out adverb) — high = novelty detector, not NEG-specific)
  · rand-span baseline (NEG vs random content syllable — sanity that SOMETHING is learnable)

Verdict:
  CLASS-EXISTS  = both held-out LOSO bacc ≥ 0.75 & CI-lo > 0.55 & RSA Δ > perm-null(97.5%) & adv-misfire ≤ 0.6
  CLASS-ABSENT  = both held-out bacc within 0.10 of chance & shuffle clean
  INCONCLUSIVE  = otherwise
EXISTS ⟹ substrate represents the morpheme abstraction, only fails to CONSUME it (read/route side =
already earned-terminal) ⟹ morpheme-tokenizer premise refuted, lever closes. ABSENT ⟹ premise alive
⟹ license MORPH-ATOM pod run (stage-2).
"""
import json
import sys
import numpy as np

NPZ = sys.argv[1] if len(sys.argv) > 1 else "spangeom_hidden.npz"
PROMPTS = sys.argv[sys.argv.index("--prompts") + 1] if "--prompts" in sys.argv else "spangeom_prompts.json"
WIN = int(sys.argv[sys.argv.index("--win") + 1]) if "--win" in sys.argv else 48


def span_rows(prompt, cue):
    wb = prompt.encode("utf-8")[-WIN:]
    nb = cue.encode("utf-8")
    idx = wb.rfind(nb)
    if idx < 0:
        return None
    return list(range(idx, idx + len(nb)))


def load():
    z = np.load(NPZ)
    meta = {it["id"]: it for it in json.load(open(PROMPTS, encoding="utf-8"))["items"]}
    X, cls = [], []
    for pid, it in meta.items():
        k = pid + "__seq"
        if k not in z.files:
            continue
        rows = span_rows(it["prompt"], it["cue"])
        if rows is None:
            continue
        seq = z[k]
        rows = [r for r in rows if r < seq.shape[0]]
        if not rows:
            continue
        X.append(seq[rows].mean(0)); cls.append(it["cls"])
    return np.array(X, float), np.array(cls)


def fit(X, y, l2=1.0, iters=500, lr=0.1):
    Xb = np.hstack([X, np.ones((len(X), 1))]); w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Xb @ w))
        w -= lr * (Xb.T @ (p - y) / len(y) + l2 * np.r_[w[:-1], 0] / len(y))
    return w


def pred(w, X):
    return (1 / (1 + np.exp(-(np.hstack([X, np.ones((len(X), 1))]) @ w)))) >= 0.5


def bacc(y, yh):
    m = [(yh[y == c] == c).mean() for c in (0, 1) if (y == c).sum()]
    return float(np.mean(m)) if m else 0.0


def loso_fold(Xs, cls, held, neg_train, ctrl, rng):
    tr = np.isin(cls, neg_train) | (cls == ctrl)
    ytr = np.isin(cls[tr], neg_train).astype(int)
    w = fit(Xs[tr], ytr)
    te = (cls == held) | (cls == ctrl)
    yte = (cls[te] == held).astype(int)
    acc = bacc(yte, pred(w, Xs[te]))
    ys = ytr.copy(); rng.shuffle(ys); ws = fit(Xs[tr], ys)
    acc_sh = bacc(yte, pred(ws, Xs[te]))
    # adv/ctrl misfire: P(pred=NEG | held-out ctrl spans)
    misfire = float(pred(w, Xs[cls == ctrl]).mean())
    te_idx = np.where(te)[0]; boots = []
    for _ in range(1000):
        bi = rng.choice(te_idx, len(te_idx), replace=True)
        boots.append(bacc((cls[bi] == held).astype(int), pred(w, Xs[bi])))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"heldout_bacc": round(acc, 3), "ci95": [round(lo, 3), round(hi, 3)],
            "shuffle": round(acc_sh, 3), "misfire": round(misfire, 3),
            "n_held": int((cls == held).sum()), "n_ctrl": int((cls == ctrl).sum())}


def rsa(Xs, cls, rng):
    negs = ["an", "anh", "mot", "ani"]
    cent = {c: Xs[cls == c].mean(0) for c in negs + ["adv"] if (cls == c).sum()}
    def cos(a, b):
        return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
    within = np.mean([cos(cent[a], cent[b]) for i, a in enumerate(negs) for b in negs[i+1:]
                      if a in cent and b in cent])
    across = np.mean([cos(cent[a], cent["adv"]) for a in negs if a in cent and "adv" in cent])
    delta = within - across
    # permutation null: shuffle neg/adv labels among {neg∪adv} spans, recompute Δ
    mask = np.isin(cls, negs + ["adv"])
    lbl = cls[mask].copy(); Xm = Xs[mask]
    null = []
    for _ in range(1000):
        perm = lbl.copy(); rng.shuffle(perm)
        cn = {c: Xm[perm == c].mean(0) for c in negs + ["adv"] if (perm == c).sum()}
        w_ = np.mean([cos(cn[a], cn[b]) for i, a in enumerate(negs) for b in negs[i+1:] if a in cn and b in cn])
        a_ = np.mean([cos(cn[a], cn["adv"]) for a in negs if a in cn and "adv" in cn])
        null.append(w_ - a_)
    p975 = float(np.percentile(null, 97.5))
    return {"rsa_delta": round(delta, 4), "within_neg_cos": round(float(within), 4),
            "neg_adv_cos": round(float(across), 4), "perm_null_97.5": round(p975, 4),
            "exceeds_null": bool(delta > p975)}


def main():
    X, cls = load()
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Xs = (X - mu) / sd
    rng = np.random.RandomState(7)
    from collections import Counter
    counts = dict(Counter(cls.tolist()))
    out = {"n": len(cls), "d": X.shape[1], "usable_per_class": counts, "folds": {}, "rand_baseline": {}}
    for held in ("mot", "ani"):
        if (cls == held).sum() < 30 or (cls == "adv").sum() < 30:
            out["folds"][held] = {"skip": "n<30"}
            continue
        out["folds"][held] = loso_fold(Xs, cls, held, ["an", "anh"], "adv", rng)
        out["rand_baseline"][held] = loso_fold(Xs, cls, held, ["an", "anh"], "rand", rng)
    out["rsa"] = rsa(Xs, cls, rng)
    nmin = min([counts.get(c, 1) for c in ("mot", "ani", "adv")])
    se = np.sqrt(0.25 / max(1, nmin))
    out["MDE_bacc"] = "SE≈%.3f, detectable Δ≈%.2f (2·SE) at nmin=%d" % (se, 2 * se, nmin)
    folds = [f for f in out["folds"].values() if "skip" not in f]
    exists = (len(folds) >= 1 and all(f["heldout_bacc"] >= 0.75 and f["ci95"][0] > 0.55 and f["misfire"] <= 0.6 for f in folds)
              and out["rsa"]["exceeds_null"])
    absent = (len(folds) >= 1 and all(abs(f["heldout_bacc"] - 0.5) < 0.10 and f["shuffle"] < 0.60 for f in folds))
    out["SPANGEOM"] = ("CLASS-EXISTS (span NEG class present → consume-side only → morpheme-lever premise REFUTED, lever closes)"
                       if exists else
                       "CLASS-ABSENT (no span NEG class → premise ALIVE → license MORPH-ATOM pod stage-2)"
                       if absent else
                       "INCONCLUSIVE (middling → inspect folds; may need layer sweep or larger n)")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
