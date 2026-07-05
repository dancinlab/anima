#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H_6163 pre-gate rung — CROSS-DATASET generalization + lane-OFF ablation.

The pre-gate showed the frozen 303M rep carries a falsifiability signal beyond surface (v2 minimal-pair
rep 0.71 > surface 0.55). This rung tests whether that direction GENERALIZES and is CAUSAL:
  - TRAIN a linear falsifier direction on the v1 naive statements, TEST on the v2 minimal-pair set
    (a DIFFERENT distribution, surface-controlled). If the naive-learned direction transfers to
    minimal pairs and beats a surface baseline trained/tested the same way, the direction captures a
    generalizable falsifiability representation, not dataset-specific surface cues.
  - lane-OFF ABLATION: zero the rep (or shuffle rep dims) -> must collapse to chance (rep is causal).
Decision (pre-registered):
  FIRM-GO   <=> cross-test rep_acc >= 0.65 AND (rep - surface) >= 0.08 AND ablation collapses (<=0.60).
  NO-TRANSFER <=> cross-test rep_acc <= 0.60 (direction is dataset-specific -> weaker premise).
Statement lists reused verbatim from the committed v1/v2 probes (reference-match, no re-authoring).
Pool (summer 303M h1129); ~120 forwards.
"""
import os, sys, json, ast
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decode as D
CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")

def load_lists():
    base = os.path.dirname(HERE)
    v1 = ast_lists(os.path.join(base, "pregate", "probe.py"), ("FALSIFIABLE", "UNFALSIFIABLE"))
    v2pairs = ast_lists(os.path.join(base, "minpair", "probe.py"), ("PAIRS",))["PAIRS"]
    return v1["FALSIFIABLE"], v1["UNFALSIFIABLE"], v2pairs

def ast_lists(path, names):
    out = {}
    for node in ast.parse(open(path).read()).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") in names:
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out

def rep(W, text):
    ids = list(text.encode("utf-8"))
    return np.asarray(D.bg_forward_last_hidden(W, ids, len(ids)), dtype=np.float64)

def fit_dir(Xtr, ytr, lam=1.0):
    t = np.where(ytr == 1, 1.0, -1.0)
    A = np.hstack([Xtr, np.ones((len(Xtr), 1))])
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ t)

def acc(w, X, y):
    pred = (np.hstack([X, np.ones((len(X), 1))]) @ w) > 0
    return float(np.mean(pred == (y == 1)))

def surface_feats(train_texts, texts):
    grams = set()
    for t in train_texts:
        s = t.lower()
        for i in range(len(s) - 2): grams.add(s[i:i+3])
    grams = sorted(grams); gi = {g: i for i, g in enumerate(grams)}
    def feat(ts):
        X = np.zeros((len(ts), len(grams)))
        for r, t in enumerate(ts):
            s = t.lower()
            for i in range(len(s) - 2):
                if s[i:i+3] in gi: X[r, gi[s[i:i+3]]] += 1
        return X
    return feat(train_texts), feat(texts)

def main():
    F, U, PAIRS = load_lists()
    naive = F + U; y_naive = np.array([1]*len(F) + [0]*len(U))
    mp = [f for f, u in PAIRS] + [u for f, u in PAIRS]; y_mp = np.array([1]*len(PAIRS) + [0]*len(PAIRS))
    print(f"[1/3] load 303M · naive {len(naive)} + minpair {len(mp)} reps ...", flush=True)
    W = D.bg_load(CKPT)
    Rn = np.stack([rep(W, t) for t in naive]); Rm = np.stack([rep(W, t) for t in mp])
    # whiten each set by naive-population stats (train-domain whitening; apply same to test)
    mu, sd = Rn.mean(0), Rn.std(0) + 1e-8
    Rnw = (Rn - mu) / sd; Rmw = (Rm - mu) / sd
    print("[2/3] cross-dataset: train naive -> test minpair (rep) ...", flush=True)
    w = fit_dir(Rnw, y_naive)
    rep_cross = acc(w, Rmw, y_mp)
    # lane-OFF ablation: zero the rep -> only bias remains -> must collapse to chance (rep is causal)
    abl = acc(w, np.zeros_like(Rmw), y_mp)
    print("[3/3] surface baseline cross-dataset ...", flush=True)
    Xtr, Xte = surface_feats(naive, mp)
    ws = fit_dir(Xtr, y_naive); surf_cross = acc(ws, Xte, y_mp)
    delta = rep_cross - surf_cross
    firm = rep_cross >= 0.65 and delta >= 0.08 and abl <= 0.60
    verdict = "FIRM-GO" if firm else ("NO-TRANSFER" if rep_cross <= 0.60 else "PARTIAL")
    out = {"probe": "H_6163 cross-dataset generalization + ablation", "n_naive": len(naive), "n_mp": len(mp),
           "rep_cross_naive2mp": round(rep_cross, 4), "surface_cross_naive2mp": round(surf_cross, 4),
           "rep_minus_surface": round(delta, 4), "ablation_zero": round(abl, 4), "verdict": verdict,
           "bar": "FIRM-GO iff rep_cross>=0.65 AND rep-surface>=0.08 AND ablation<=0.60"}
    json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), ensure_ascii=False, indent=1)
    print(f"    rep_cross={rep_cross:.3f} surface_cross={surf_cross:.3f} delta={delta:+.3f} ablation={abl:.3f} -> {verdict}", flush=True)

if __name__ == "__main__":
    main()
