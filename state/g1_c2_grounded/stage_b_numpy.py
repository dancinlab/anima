#!/usr/bin/env python3
"""C2 Stage-B (numpy · mini-runnable · torch-free) — scope: ASSOCIATION / fuel-lever.
Tests whether the world channel's held-out co-occurrence becomes LEARNABLE where text-only can't,
i.e. does C2 work as a FUEL lever (feeds coverage-density) — NOT the deep-recombination operator (γ, separate).
Model = 1-layer softmax over concept embeddings: P(next | last) = softmax(W emb[last]). Trained on token docs.
Conditions (i captions / ii +world test-pair events / a shuffled / b other-pair) × 3 seeds.
Probe: held-out (A,B) → rank B by P(B|A), AUC vs negatives.
FROZEN Bar B: Δ(ii−i)≥+0.10 ∧ Δ(a)≤+0.02 ∧ Δ(b)≤+0.02.
"""
import os, json, random, urllib.request, zipfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ANN = os.path.join(HERE, "coco_ann"); INST = os.path.join(ANN, "annotations", "instances_val2017.json")
CAPS = os.path.join(ANN, "annotations", "captions_val2017.json")

def ensure():
    if os.path.exists(INST): return
    os.makedirs(ANN, exist_ok=True); z = os.path.join(ANN, "a.zip")
    print("downloading COCO...", flush=True)
    urllib.request.urlretrieve("http://images.cocodataset.org/annotations/annotations_trainval2017.zip", z)
    zipfile.ZipFile(z).extractall(ANN); os.remove(z)

def build():
    inst = json.load(open(INST)); caps = json.load(open(CAPS))
    cats = {c["id"]: c["name"] for c in inst["categories"]}
    names = sorted(cats.values()); idx = {n: i for i, n in enumerate(names)}; V = len(names)
    img_objs = {}
    for a in inst["annotations"]: img_objs.setdefault(a["image_id"], set()).add(cats[a["category_id"]])
    caps_by = {}
    for a in caps["annotations"]: caps_by.setdefault(a["image_id"], []).append(a["caption"].lower())
    img_txt = {im: set(n for n in names if n in " ".join(cs)) for im, cs in caps_by.items()}
    return names, idx, V, img_objs, img_txt

def held_out(idx, img_objs, img_txt, names):
    from itertools import combinations
    ic, cc = {}, {}
    for im in img_objs:
        objs, txt = img_objs[im], img_txt.get(im, set())
        for A, B in combinations(sorted(objs), 2):
            ic[(A, B)] = ic.get((A, B), 0) + 1
            if A in txt and B in txt: cc[(A, B)] = cc.get((A, B), 0) + 1
    return [p for p in ic if ic[p] >= 20 and cc.get(p, 0) == 0]

def make_pairs(names, idx, img_objs, img_txt, test, mode, seed):
    """training as (last_token, next_token) pairs from docs."""
    from itertools import combinations
    rng = random.Random(100 + seed); tset = set(test); P = []
    for im in img_txt:  # caption doc = sequence of mentioned objects → all ordered adjacent-ish (use all ordered pairs within doc)
        toks = sorted(img_txt[im])
        for i in range(len(toks)):
            for j in range(len(toks)):
                if i != j: P.append((idx[toks[i]], idx[toks[j]]))
    ev = []
    for im in img_objs:
        for A, B in combinations(sorted(img_objs[im]), 2): ev += [(A, B), (B, A)]
    if mode == 'ii':
        for A, B in ev:
            if (A, B) in tset or (B, A) in tset: P.append((idx[A], idx[B]))
    elif mode == 'a':
        for A, B in ev:
            if (A, B) in tset or (B, A) in tset: P.append((idx[A], rng.randrange(len(names))))
    elif mode == 'b':
        for A, B in ev:
            if not ((A, B) in tset or (B, A) in tset): P.append((idx[A], idx[B]))
    return np.array(P, dtype=np.int64) if P else np.zeros((0, 2), np.int64)

def train_eval(P, test, idx, V, seed, d=48, steps=4000, bs=512, lr=0.2):
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((V, d)) * 0.1; W = rng.standard_normal((V, d)) * 0.1
    n = len(P)
    for _ in range(steps):
        b = P[rng.integers(0, n, bs)]
        a, y = b[:, 0], b[:, 1]
        h = E[a]                          # (bs,d)
        logits = h @ W.T                  # (bs,V)
        logits -= logits.max(1, keepdims=True)
        p = np.exp(logits); p /= p.sum(1, keepdims=True)
        g = p; g[np.arange(bs), y] -= 1   # dL/dlogits
        gW = g.T @ h / bs
        gE = g @ W / bs
        W -= lr * gW
        np.add.at(E, a, -lr * gE)
    # probe AUC
    aucs = []
    for A, B in test:
        h = E[idx[A]]; sc = W @ h
        sc = sc - sc.max(); pr = np.exp(sc); pr /= pr.sum()
        t = pr[idx[B]]; neg = [pr[j] for j in range(V) if j != idx[A] and j != idx[B]]
        aucs.append(sum(1 for x in neg if x < t) / len(neg))
    return float(np.mean(aucs))

if __name__ == "__main__":
    ensure()
    names, idx, V, img_objs, img_txt = build()
    test = held_out(idx, img_objs, img_txt, names)
    print(f"V={V} held-out test pairs={len(test)}", flush=True)
    res = {"n_test_pairs": len(test), "scope": "ASSOCIATION/fuel-lever (NOT deep-recombination operator=γ separate)", "seeds": {}}
    for seed in (0, 1, 2):
        row = {}
        for mode in ('i', 'ii', 'a', 'b'):
            P = make_pairs(names, idx, img_objs, img_txt, test, mode, seed)
            row[mode] = round(train_eval(P, test, idx, V, seed), 4)
        row["d_ii"] = round(row['ii']-row['i'], 4); row["d_a"] = round(row['a']-row['i'], 4); row["d_b"] = round(row['b']-row['i'], 4)
        res["seeds"][seed] = row
        print(f"seed{seed}: i={row['i']:.3f} ii={row['ii']:.3f} a={row['a']:.3f} b={row['b']:.3f} | Δii={row['d_ii']:+.3f} Δa={row['d_a']:+.3f} Δb={row['d_b']:+.3f}", flush=True)
    S = res["seeds"]
    passB = (all(S[s]['d_ii'] >= 0.10 for s in S) and all(S[s]['d_a'] <= 0.02 for s in S) and all(S[s]['d_b'] <= 0.02 for s in S))
    res["verdict"] = ("🟢 PASS-B (world channel usable as FUEL → C2 feeds coverage-density · deep-recomb operator=γ separate · scope G1-concrete)"
                      if passB else "🔴 FAIL-B (world MI not usable even as association → wall = property of any finite experience channel)")
    print("\n=== VERDICT:", res["verdict"], "===")
    open(os.path.join(HERE, "stage_b_RESULT.json"), "w").write(json.dumps(res, indent=2, ensure_ascii=False))
