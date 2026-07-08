#!/usr/bin/env python3
"""C2 Stage-B (Fable design · FROZEN bars) — does a substrate USE the world channel's held-out
combination-MI, or does it enter as additive-unary (Fable's modal failure)?

Toy token-LM over COCO object-token sequences. Text channel = objects MENTIONED in captions.
World channel = objects CO-PRESENT per annotations. Held-out test pairs = the 68 A2 pairs
(img_cooc high, cap_cooc==0). Conditions, same trunk:
  (i)  captions only                         -> held-out pair NEVER linked in text
  (ii) captions + world events (test pairs)  -> world supplies the held-out link
  (a)  captions + SHUFFLED world events       -> pairing randomized (bind-destruction control)
  (b)  captions + world events (OTHER pairs)  -> test pair absent from world channel
Probe (frozen before train): for each held-out (A,B), rank B by P(B|A) among all concepts → AUC.
FROZEN Bar B (n=3 seeds): Δ(ii−i) ≥ +0.10 AND Δ(a−i) ≤ +0.02 AND Δ(b−i) ≤ +0.02.
PASS-B = world channel usable (C2 fuel-lever real). FAIL-B = additive superposition (Fable modal →
wall = property of any finite experience channel).
"""
import os, json, math, random, urllib.request, zipfile
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
DEV = 'cuda' if torch.cuda.is_available() else 'cpu'
HERE = os.path.dirname(os.path.abspath(__file__))
ANN = os.path.join(HERE, "coco_ann"); INST = os.path.join(ANN, "annotations", "instances_val2017.json")
CAPS = os.path.join(ANN, "annotations", "captions_val2017.json")

def ensure():
    if os.path.exists(INST): return
    os.makedirs(ANN, exist_ok=True); z = os.path.join(ANN, "a.zip")
    urllib.request.urlretrieve("http://images.cocodataset.org/annotations/annotations_trainval2017.zip", z)
    zipfile.ZipFile(z).extractall(ANN); os.remove(z)

def build():
    inst = json.load(open(INST)); caps = json.load(open(CAPS))
    cats = {c["id"]: c["name"] for c in inst["categories"]}
    names = sorted(cats.values()); idx = {n: i for i, n in enumerate(names)}; V = len(names)
    img_objs = {}
    for a in inst["annotations"]: img_objs.setdefault(a["image_id"], set()).add(cats[a["category_id"]])
    img_txt = {}   # objects actually mentioned in this image's captions
    caps_by = {}
    for a in caps["annotations"]: caps_by.setdefault(a["image_id"], []).append(a["caption"].lower())
    for im, cs in caps_by.items():
        blob = " ".join(cs); img_txt[im] = set(n for n in names if n in blob)
    return names, idx, V, img_objs, img_txt

def held_out_pairs(idx, img_objs, img_txt, names):
    from itertools import combinations
    ic = {}; cc = {}
    for im in img_objs:
        objs = img_objs[im]; txt = img_txt.get(im, set())
        for A, B in combinations(sorted(objs), 2):
            ic[(A, B)] = ic.get((A, B), 0) + 1
            if A in txt and B in txt: cc[(A, B)] = cc.get((A, B), 0) + 1
    return [p for p in ic if ic[p] >= 20 and cc.get(p, 0) == 0]

class LM(nn.Module):
    def __init__(s, V, d=64, seed=0):
        super().__init__(); torch.manual_seed(seed)
        s.emb = nn.Embedding(V + 1, d); s.ln = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, 4, batch_first=True); s.head = nn.Linear(d, V)
    def forward(s, x):  # x: (B,T) token ids (BOS=V)
        T = x.shape[1]; h = s.emb(x)
        m = torch.triu(torch.full((T, T), float('-inf'), device=x.device), 1)
        a, _ = s.attn(s.ln(h), s.ln(h), s.ln(h), attn_mask=m, need_weights=False)
        return s.head(h + a)

def make_docs(names, idx, V, img_objs, img_txt, test_pairs, mode, seed):
    rng = random.Random(100 + seed); docs = []
    tset = set(test_pairs)
    other = None
    for im in img_txt:  # (i) caption docs = mentioned-object sequence
        toks = [idx[n] for n in sorted(img_txt[im])]
        if len(toks) >= 2: docs.append(toks)
    # world events: per image, co-present pairs
    from itertools import combinations
    ev = []
    for im in img_objs:
        for A, B in combinations(sorted(img_objs[im]), 2):
            ev.append((A, B))
    if mode == 'i':
        pass
    elif mode == 'ii':
        for A, B in ev:
            if (A, B) in tset: docs.append([idx[A], idx[B]])
    elif mode == 'a':  # shuffled: keep A, random partner (bind-destroy)
        alln = names
        for A, B in ev:
            if (A, B) in tset: docs.append([idx[A], idx[rng.choice(alln)]])
    elif mode == 'b':  # other pairs only (test pair absent)
        for A, B in ev:
            if (A, B) not in tset: docs.append([idx[A], idx[B]])
    return docs

def train_eval(docs, test_pairs, names, idx, V, seed):
    torch.manual_seed(seed); m = LM(V, seed=seed).to(DEV)
    opt = torch.optim.Adam(m.parameters(), 3e-3)
    BOS = V
    # pad docs to batches
    data = [[BOS] + d for d in docs]
    rng = random.Random(seed)
    for step in range(3000):
        batch = [rng.choice(data) for _ in range(128)]
        T = max(len(b) for b in batch)
        x = torch.full((128, T), BOS, dtype=torch.long)
        for i, b in enumerate(batch): x[i, :len(b)] = torch.tensor(b)
        x = x.to(DEV)
        logits = m(x[:, :-1]); loss = F.cross_entropy(logits.reshape(-1, V), x[:, 1:].reshape(-1).clamp(max=V-1))
        opt.zero_grad(); loss.backward(); opt.step()
    # probe: P(B|A) rank among all concepts
    m.eval(); aucs = []
    with torch.no_grad():
        for A, B in test_pairs:
            xa = torch.tensor([[BOS, idx[A]]], device=DEV)
            p = F.softmax(m(xa)[0, -1], -1)  # P(next | A)
            true = p[idx[B]].item()
            neg = [p[j].item() for j in range(V) if j != idx[A] and j != idx[B]]
            auc = sum(1 for x in neg if x < true) / len(neg)
            aucs.append(auc)
    return float(np.mean(aucs))

if __name__ == "__main__":
    ensure()
    names, idx, V, img_objs, img_txt = build()
    test_pairs = held_out_pairs(idx, img_objs, img_txt, names)
    print(f"device={DEV} V={V} held-out test pairs={len(test_pairs)}", flush=True)
    res = {"n_test_pairs": len(test_pairs), "seeds": {}}
    for seed in (0, 1, 2):
        row = {}
        for mode in ('i', 'ii', 'a', 'b'):
            docs = make_docs(names, idx, V, img_objs, img_txt, test_pairs, mode, seed)
            row[mode] = round(train_eval(docs, test_pairs, names, idx, V, seed), 4)
        row["d_ii"] = round(row['ii'] - row['i'], 4); row["d_a"] = round(row['a'] - row['i'], 4); row["d_b"] = round(row['b'] - row['i'], 4)
        res["seeds"][seed] = row
        print(f"seed{seed}: i={row['i']:.3f} ii={row['ii']:.3f} a(shuf)={row['a']:.3f} b(other)={row['b']:.3f} | Δii={row['d_ii']:+.3f} Δa={row['d_a']:+.3f} Δb={row['d_b']:+.3f}", flush=True)
    S = res["seeds"]
    passB = (all(S[s]['d_ii'] >= 0.10 for s in S) and all(S[s]['d_a'] <= 0.02 for s in S) and all(S[s]['d_b'] <= 0.02 for s in S))
    res["verdict"] = ("🟢 PASS-B (world channel usable → C2 fuel-lever real → rig justified · scope G1-concrete)"
                      if passB else "🔴 FAIL-B (world MI enters additive/unusable → wall = property of any finite experience channel · γ sole survivor)")
    print("\n=== VERDICT:", res["verdict"], "===")
    open(os.path.join(HERE, "stage_b_RESULT.json"), "w").write(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res["seeds"], indent=2))
