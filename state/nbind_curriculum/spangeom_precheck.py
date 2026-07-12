#!/usr/bin/env python3
"""spangeom_precheck.py — $0 UNDERPOWERED directional pre-check for Fable SPAN-GEOM.

Reuses the earn-seal dump (loso_hidden.npz has __seq = [24-byte-window, d] per prompt) to ask the
morpheme-lever premise ONE LEVEL BELOW the earn-seal: does the frozen base 303M form a stem-level NEG
equivalence class at the SPAN level (pooled over the negation stem's OWN bytes), not sentence mean-pool?

LOSO span classifier: train NEG(안/않)-span vs adverb(매우/정말…)-span, TEST held-out NEG(못/아니)-span
vs adverb-span. Byte-identity features can't transfer under LOSO (held-out stem's bytes never trained),
so a hit REQUIRES a shared NEG-like span feature = the class exists. shuffle + adv-position controls.

⚠️ UNDERPOWERED: only prompts whose stem falls in the 24-byte window are usable (~25-30/stem, the dump
window was built for mean-pool not span). SE≈0.09 → MDE(bacc) ≈ 0.18. A STARK result (≥0.75 or ≈0.50)
is directional; a middling one is inconclusive → fire the proper n≥300 pod SPAN-GEOM. NOT cement-grade.
"""
import json
import sys
import numpy as np

NPZ = "/Users/mini/anima-weights/nbind_cement/loso_hidden.npz"
PROMPTS = sys.argv[sys.argv.index("--prompts") + 1] if "--prompts" in sys.argv else \
    "/private/tmp/claude-501/-Users-mini-dancinlab-anima/f5b1994e-2cff-42cb-9e82-494c5e7d490b/scratchpad/loso_prompts.json"
WIN = 24

STEM_BYTES = {"an": "안", "anh": "않", "mot": "못", "ani": "아니"}
ADVERBS = ["매우", "정말", "아주", "너무", "진짜", "완전"]


def locate(win_bytes, needle_bytes):
    """Return list of byte-row indices in the 24-byte window covering needle (last occurrence)."""
    n = len(needle_bytes)
    idx = win_bytes.rfind(needle_bytes)
    if idx < 0:
        return None
    return list(range(idx, idx + n))


def build():
    z = np.load(NPZ)
    items = {it["id"]: it["prompt"] for it in json.load(open(PROMPTS, encoding="utf-8"))["items"]}
    X, y, g = [], [], []          # span-pooled vec, label(neg=1/adv=0), group(stem or 'adv')
    stats = {"neg": {}, "adv": 0, "adv_missed": 0}
    for pid, prompt in items.items():
        base = pid.rsplit("_", 1)[0]
        seqk = pid + "__seq"
        if seqk not in z.files:
            continue
        seq = z[seqk]                      # (24, d)
        wb = prompt.encode("utf-8")[-WIN:]
        if base in STEM_BYTES:
            nb = STEM_BYTES[base].encode("utf-8")
            rows = locate(wb, nb)
            stats["neg"].setdefault(base, [0, 0])
            if rows is None:
                stats["neg"][base][1] += 1     # missed (stem not in window)
                continue
            stats["neg"][base][0] += 1
            X.append(seq[rows].mean(0)); y.append(1); g.append(base)
        elif base == "adv":
            rows = None
            for adv in ADVERBS:
                rows = locate(wb, adv.encode("utf-8"))
                if rows is not None:
                    break
            if rows is None:
                stats["adv_missed"] += 1
                continue
            stats["adv"] += 1
            X.append(seq[rows].mean(0)); y.append(0); g.append("adv")
    return np.array(X, float), np.array(y, int), np.array(g), stats


def fit(X, y, l2=1.0, iters=400, lr=0.1):
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


def main():
    X, y, g, stats = build()
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Xs = (X - mu) / sd
    adv = g == "adv"
    rng = np.random.RandomState(7)
    out = {"n_total": len(y), "d": X.shape[1], "usable_per_class": {
        k: v[0] for k, v in stats["neg"].items()}, "n_adv": stats["adv"],
        "missed": {k: v[1] for k, v in stats["neg"].items()}, "folds": {}}
    for held in ("mot", "ani"):
        te_neg = g == held
        tr = ((g == "an") | (g == "anh") | adv)          # train on 안/않 neg + adverbs
        if te_neg.sum() < 8 or adv.sum() < 8:
            out["folds"][held] = {"skip": "n<8", "n_neg": int(te_neg.sum())}
            continue
        w = fit(Xs[tr], y[tr])
        te = te_neg | adv
        acc = bacc(y[te], pred(w, Xs[te]))
        ys = y[tr].copy(); rng.shuffle(ys); ws = fit(Xs[tr], ys)
        acc_sh = bacc(y[te], pred(ws, Xs[te]))
        # paired bootstrap CI on held-out bacc (1000 resamples)
        te_idx = np.where(te)[0]; boots = []
        for _ in range(1000):
            bi = rng.choice(te_idx, len(te_idx), replace=True)
            boots.append(bacc(y[bi], pred(w, Xs[bi])))
        lo, hi = np.percentile(boots, [2.5, 97.5])
        out["folds"][held] = {"heldout_bacc": round(acc, 3), "ci95": [round(lo, 3), round(hi, 3)],
                              "shuffle": round(acc_sh, 3), "n_neg": int(te_neg.sum()), "n_adv": int(adv.sum())}
    se = np.sqrt(0.25 / max(1, min(stats["neg"].get("mot", [1])[0], stats["neg"].get("ani", [1])[0])))
    out["MDE_bacc_note"] = "approx SE=%.3f, detectable Δ≈%.2f (2·SE)" % (se, 2 * se)
    strong_exist = all(f.get("heldout_bacc", 0) >= 0.75 and f.get("ci95", [0])[0] > 0.55
                       for f in out["folds"].values() if "skip" not in f) and len([f for f in out["folds"].values() if "skip" not in f]) >= 1
    chance = all(abs(f.get("heldout_bacc", 0.5) - 0.5) < 0.10 for f in out["folds"].values() if "skip" not in f)
    out["PRECHECK"] = ("DIRECTIONAL-EXISTS (class may exist at span → lever likely closes; confirm n300)"
                       if strong_exist else
                       "DIRECTIONAL-ABSENT (no span class → lever premise alive; fire pod SPAN-GEOM)"
                       if chance else
                       "INCONCLUSIVE (underpowered/middling → fire pod SPAN-GEOM n≥300)")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
