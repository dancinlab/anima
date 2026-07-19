"""v2/probe_decode.py — V2_7 DECODE-PROBE (scratch · rule-exempt zone).

Question: BOLT's seed-split (s7 held-out 0.611 / s11 0.491≈chance) — is it because the
frozen NOSTORE trunk encodes the queried entity at the query position for seed7 but NOT
for seed11?

Method (engine-native to the toy — reuses model.trunk_fwd, gen.Stream, train.encode_batch;
does NOT re-implement any forward pass):
  1. Load the frozen NOSTORE trunk ckpt for a seed.
  2. Over HELD-OUT eval entities, run the frozen trunk forward and take the hidden at qpos
     (the last prompt byte — exactly where bridge_fwd forms its query h_q @ W_q).
  3. Train a linear probe (multinomial logistic regression, plain numpy GD) to predict the
     queried entity's IDENTITY (1-of-128 over the held-out entity set) from that hidden.
     If a linear map cannot recover the entity identity from h_q, then no linear W_q can
     form a query that discriminates the store slot -> the bolt-on bridge is starved.
  4. Report held-out probe accuracy per seed. COTRAIN trunk = positive reference.

Chance = 1/128 = 0.0078.
"""

import json
import os
import pickle

import numpy as np

import gen
import model as M
from train import encode_batch

HERE = os.path.dirname(os.path.abspath(__file__))
FKDIR = "/tmp/v2-store_only-mlpfk"   # gate=store_only readout=mlp fixed_key tag=fk


def hidden_at_qpos(params, cfg, exs, chunk=256):
    """Run the frozen trunk forward and return (N,d) hidden at the query position."""
    outs = []
    for i in range(0, len(exs), chunk):
        sub = exs[i:i + chunk]
        ids, tg, mask, sids, vidx, qp, ap = encode_batch(sub, cfg)
        _, hidden, _ = M.trunk_fwd(params, cfg, ids)      # engine-native forward
        outs.append(hidden[np.arange(len(sub)), qp])       # (b,d) at query byte
    return np.concatenate(outs, axis=0)


def labels_for(exs, ent2lab):
    """Queried entity identity = store_names[slot]."""
    return np.array([ent2lab[e["store_names"][e["slot"]]] for e in exs], dtype=np.int64)


def softmax(z):
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def train_logreg(Xtr, ytr, C, iters=800, lr=0.5, l2=1e-4, seed=0):
    """Multinomial logistic regression, plain numpy full-batch GD + Adam. Standardises X on
    the TRAIN split only. Returns a predict(X) closure."""
    mu = Xtr.mean(0, keepdims=True)
    sd = Xtr.std(0, keepdims=True) + 1e-8
    Xs = (Xtr - mu) / sd
    N, d = Xs.shape
    Xb = np.concatenate([Xs, np.ones((N, 1))], axis=1)      # bias column
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((d + 1, C)) * 0.01
    Y = np.zeros((N, C)); Y[np.arange(N), ytr] = 1.0
    m = np.zeros_like(W); v = np.zeros_like(W); b1, b2, eps = 0.9, 0.999, 1e-8
    for t in range(1, iters + 1):
        P = softmax(Xb @ W)
        g = Xb.T @ (P - Y) / N + l2 * W
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * (g * g)
        mh = m / (1 - b1 ** t); vh = v / (1 - b2 ** t)
        W -= lr * mh / (np.sqrt(vh) + eps)

    def predict(X):
        Xs2 = (X - mu) / sd
        Xb2 = np.concatenate([Xs2, np.ones((len(X), 1))], axis=1)
        return (Xb2 @ W).argmax(1)                          # argmax == argmax(softmax)
    return predict


def slot_retrieval_probe(params, cfg, tr, te, chunk=256, iters=1200, lr=0.05, seed=0):
    """Bridge-FAITHFUL probe: fit ONLY a linear query W (d,d) — exactly bridge_fwd's
    q = hidden_q @ W_q — such that softmax over (q . frozen_key_slot)/sqrt(d) picks the
    queried slot out of 8. This is the retrieval half a bolt-on bridge must form on the
    frozen trunk, in isolation from the readout/operator. Chance = 1/8 = 0.125."""
    d = cfg["d"]

    def feats(exs):
        H, K, Y = [], [], []
        for i in range(0, len(exs), chunk):
            sub = exs[i:i + chunk]
            ids, tg, mask, sids, vidx, qp, ap = encode_batch(sub, cfg)
            _, hidden, _ = M.trunk_fwd(params, cfg, ids)
            keys, _ = M.store_keys(params, cfg, sids)          # frozen content-addresses
            H.append(hidden[np.arange(len(sub)), qp]); K.append(keys)
            Y.append(np.array([e["slot"] for e in sub]))
        return np.concatenate(H), np.concatenate(K), np.concatenate(Y)

    Htr, Ktr, ytr = feats(tr)
    Hte, Kte, yte = feats(te)
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((d, d)) * 0.02
    m = np.zeros_like(W); v = np.zeros_like(W); b1, b2, eps = 0.9, 0.999, 1e-8
    N = len(Htr); scale = 1.0 / np.sqrt(d)
    Yoh = np.zeros((N, Ktr.shape[1])); Yoh[np.arange(N), ytr] = 1.0
    for t in range(1, iters + 1):
        q = Htr @ W                                             # (N,d)
        logits = np.einsum("nd,nsd->ns", q, Ktr) * scale        # (N,S) == bridge att
        P = softmax(logits)
        dlog = (P - Yoh) / N * scale
        dq = np.einsum("ns,nsd->nd", dlog, Ktr)                 # (N,d)
        g = Htr.T @ dq
        m = b1 * m + (1 - b1) * g; v = b2 * v + (1 - b2) * (g * g)
        W -= lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps)
    qte = Hte @ W
    pred = (np.einsum("nd,nsd->ns", qte, Kte) * scale).argmax(1)
    return float((pred == yte).mean())


def probe_arm(arm, seed, eval_ent, n_slots, n_train=20000, n_test=8000):
    ck = pickle.load(open(os.path.join(FKDIR, f"{arm}_seed{seed}.pkl"), "rb"))
    params, cfg = ck["params"], ck["cfg"]
    if "key_emb_frozen" not in params:
        # NOSTORE has no store; the slot-retrieval probe needs the SAME frozen content-
        # addresses BOLT had to retrieve against -> inject BOLT's key_emb_frozen (frozen,
        # never trained, so identical to what a bolt-on bridge on this trunk would query).
        bolt = pickle.load(open(os.path.join(FKDIR, f"BOLT_seed{seed}.pkl"), "rb"))["params"]
        params = dict(params); params["key_emb_frozen"] = bolt["key_emb_frozen"]
    ent2lab = {nm: i for i, nm in enumerate(eval_ent)}
    C = len(eval_ent)

    # distinct held-out draws for probe-train / probe-test (both 0-shot entities)
    tr = gen.Stream(seed + 2000, eval_ent, n_slots).batch(n_train)
    te = gen.Stream(seed + 3000, eval_ent, n_slots).batch(n_test)

    Xtr = hidden_at_qpos(params, cfg, tr)
    Xte = hidden_at_qpos(params, cfg, te)
    ytr = labels_for(tr, ent2lab)
    yte = labels_for(te, ent2lab)

    pred = train_logreg(Xtr, ytr, C, seed=seed)(Xte)
    ident = float((pred == yte).mean())
    slot = slot_retrieval_probe(params, cfg, tr, te, seed=seed)
    return ident, slot, C


def main():
    bars = json.load(open(os.path.join(HERE, "bars.json")))
    t = bars["task"]
    _, eval_ent = gen.split_pool(t["entity_pool"], t["entity_train"], t["entity_eval"])
    n_slots = t["store_slots"]
    seeds = bars["seeds"]

    print("=" * 74)
    print("V2_7 DECODE-PROBE — entity identity from the frozen trunk's query-pos hidden")
    print(f"  held-out entity classes = {len(eval_ent)}  (chance = {1/len(eval_ent):.4f})")
    print(f"  probe = multinomial logreg on hidden[qpos]  (fk config: {FKDIR})")
    print("=" * 74)
    print("  identity = 1-of-128 linear decode of queried entity from hidden[qpos]")
    print("  slot-retr= bridge-faithful linear query vs 8 frozen keys (chance 0.125)")
    print("-" * 74)
    res = {}
    for arm in ("NOSTORE", "COTRAIN"):
        for s in seeds:
            ident, slot, C = probe_arm(arm, s, eval_ent, n_slots)
            res[(arm, s)] = (ident, slot)
            print(f"  {arm:8s} seed{s:<2d}: identity {ident:.4f} ({ident*C:.0f}x)   "
                  f"slot-retr {slot:.4f} ({slot/0.125:.1f}x chance)")
    print("-" * 74)
    ns = {s: res[("NOSTORE", s)] for s in seeds}
    print(f"  NOSTORE frozen-trunk:  identity s{seeds[0]}={ns[seeds[0]][0]:.4f} "
          f"s{seeds[1]}={ns[seeds[1]][0]:.4f} (ratio {ns[seeds[0]][0]/max(ns[seeds[1]][0],1e-9):.2f}x) | "
          f"slot-retr s{seeds[0]}={ns[seeds[0]][1]:.4f} s{seeds[1]}={ns[seeds[1]][1]:.4f} "
          f"(ratio {ns[seeds[0]][1]/max(ns[seeds[1]][1],1e-9):.2f}x)")
    print("  BOLT held-out was s7 0.611 / s11 0.491 (flip-coh 0.85 / 0.00) — same direction?")
    return res


if __name__ == "__main__":
    main()
