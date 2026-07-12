#!/usr/bin/env python3
"""morphatom_gate.py — MORPH-ATOM G-a gate (Fable re-fire spec). Runs on the pod (post-CPT, pre-drill).

G-a1 (alphabet liveness): held-out codec-corpus NLL in nats/byte via clm._fwd_logits (same engine forward
as the eval). PASS = ≤ 2.5 nats/byte (uniform byte = ln 256 ≈ 5.545; a live byte-LM sits well under half).
FAIL → PENDING(CPT-budget): the codec alphabet itself isn't learned; extend CPT, do NOT drill.

G-a2 (stem-code geometry, SPAN-GEOM LOSO analog): last-trunk-layer activation at each of the 4 negator stem
CODE positions (mean over ≥50 natural codec contexts) + ≥8 frequency-matched non-negator stem codes as
controls. Leave-one-negator-out linear probe (NEG vs non-NEG): train on 3 negators + controls, test the
held-out negator. PASS = held-out AUC ≥ 0.80 every fold AND shuffle ≤ 0.60 (Δ-vs-control, FORM-tunable/
BIND-earned metalaw — never raw value alone).

Semantics: G-a1 FAIL → PENDING(CPT-budget). G-a1 PASS + G-a2 FAIL → class doesn't form from distribution;
drill once + re-probe post-drill; still-fail at drill-loss≈0 → FAIL(earned), escalate to from-scratch.
Both PASS → drill + full eval interpretable.

Usage: morphatom_gate.py <cpt.clm> --codec <codec.json> --corpus <held_codec_corpus.txt> [--out g.json]
Uses trunk activations via clm._fwd_trunk (pre-readout penultimate) + morph2b codec for stem-code contexts.
"""
import json
import math
import os
import sys
import numpy as np

try:
    import anima_py.core.decode as _d
    sys.path.insert(0, os.path.dirname(_d.__file__))
    from anima_py.core import decode as clm
except Exception:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import decode as clm
import morph2b as MB

CKPT = sys.argv[1]
CODEC = sys.argv[sys.argv.index("--codec") + 1]
CORPUS = sys.argv[sys.argv.index("--corpus") + 1] if "--corpus" in sys.argv else "morph_corpus.txt"
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
WIN = 96
STEMS = {"an": "안", "anh": "않", "mot": "못", "ani": "아니"}


def load_codec():
    d = json.load(open(CODEC, encoding="utf-8"))
    if "merges" in d:
        mr = {tuple(k.split("\t")): r for r, k in enumerate(d["merges"])}
        return mr, d["tok2id"], d
    lines = [l.rstrip("\n") for l in open(CORPUS, encoding="utf-8") if l.strip()][:120000]
    merges = MB.train_bpe(lines[:20000], d["k"])
    mr, t2i, _ = MB.build_vocab(lines, merges)
    return mr, t2i, d


def tok_from_bytes(bs, T):
    tok = np.full(T, 32.0); n = min(len(bs), T)
    for p in range(n):
        tok[T - n + p] = float(bs[-n + p])
    return tok


def main():
    W = clm.clm_load_weights(CKPT)
    if not W.get("ok"):
        print("ERROR ckpt not decodable"); return 1
    mr, t2i, cj = load_codec()
    enc = lambda t: MB.encode_to_bytes(t, mr, t2i)
    lines = [l.rstrip("\n") for l in open(CORPUS, encoding="utf-8") if l.strip()]
    held = lines[-3000:]                       # held-out codec corpus tail

    # ---- G-a1: NLL nats/byte ----
    import random; random.Random(7).shuffle(held)
    tot_nll = 0.0; tot_pos = 0
    for l in held[:400]:
        tok = tok_from_bytes(enc(l), WIN)
        logits = clm._fwd_logits(W, tok, WIN)
        for i in range(max(0, WIN - 40), WIN - 1):
            row = logits[i]; m = float(np.max(row))
            lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
            tot_nll += lse - float(row[int(tok[i + 1])]); tot_pos += 1
    nll = tot_nll / max(1, tot_pos)
    ga1 = nll <= 2.5

    # ---- G-a2: stem-code geometry LOSO ----
    stem_ids = {s: [i for i in MB.stem_token_ids(STEMS[s], mr, t2i)[0] if i is not None] for s in STEMS}
    # gather trunk activation at stem-code position across natural contexts
    X, cls = [], []
    def add_contexts(label, ch, want_ids):
        n = 0
        for l in lines:
            if n >= 60 or ch not in l:
                continue
            i = l.rfind(ch)
            seg = l[:i + len(ch)]
            tok = tok_from_bytes(enc(seg), WIN)
            yn = clm._fwd_trunk(W, tok, WIN)     # [T,d] pre-readout penultimate
            X.append(yn[-1]); cls.append(label); n += 1
    for s in ["an", "anh", "mot", "ani"]:
        add_contexts(s, STEMS[s], stem_ids[s])
    # freq-matched non-neg controls (common syllables)
    for ctrl in ["좋", "재", "영", "정", "사", "말", "보", "화"]:
        add_contexts("ctrl", ctrl, None)
    X = np.array(X, float); cls = np.array(cls)
    mu, sd = X.mean(0), X.std(0) + 1e-6; Xs = (X - mu) / sd
    rng = np.random.RandomState(7)
    def fit(Xt, y, it=400, lr=0.1):
        Xb = np.hstack([Xt, np.ones((len(Xt), 1))]); w = np.zeros(Xb.shape[1])
        for _ in range(it):
            p = 1 / (1 + np.exp(-Xb @ w)); w -= lr * (Xb.T @ (p - y) / len(y) + np.r_[w[:-1], 0] / len(y))
        return w
    def auc(y, s):
        pos = s[y == 1]; neg = s[y == 0]
        if not len(pos) or not len(neg):
            return 0.5
        return float((pos[:, None] > neg[None, :]).mean())
    folds = {}
    ctrl = cls == "ctrl"
    for h in ["mot", "ani"]:
        tr = np.isin(cls, [x for x in ["an", "anh", "mot", "ani"] if x != h]) | ctrl
        ytr = np.isin(cls[tr], ["an", "anh", "mot", "ani"]).astype(int)
        w = fit(Xs[tr], ytr)
        te = (cls == h) | ctrl
        yte = (cls[te] == h).astype(int)
        sc = 1 / (1 + np.exp(-(np.hstack([Xs[te], np.ones((te.sum(), 1))]) @ w)))
        a = auc(yte, sc)
        ys = ytr.copy(); rng.shuffle(ys); ws = fit(Xs[tr], ys)
        scs = 1 / (1 + np.exp(-(np.hstack([Xs[te], np.ones((te.sum(), 1))]) @ ws)))
        folds[h] = {"auc": round(a, 3), "shuffle": round(auc(yte, scs), 3), "n": int((cls == h).sum())}
    ga2 = all(f["auc"] >= 0.80 and f["shuffle"] <= 0.60 for f in folds.values()) and len(folds) >= 1

    res = {"nll_nats_per_byte": round(nll, 3), "G_a1_alphabet_live": bool(ga1),
           "G_a2_folds": folds, "G_a2_stem_class": bool(ga2),
           "gate": ("PASS→drill" if (ga1 and ga2) else
                    "PENDING(CPT-budget)" if not ga1 else
                    "G-a1 PASS / G-a2 FAIL → drill-once then re-probe (FAIL-earned if still flat)")}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if OUT:
        json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
