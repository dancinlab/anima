"""H_9927 -- the last untouched variable: the real retrain has NO ORACLE.

Every measurement in this chain, from H_9915 to H_9926, handed the address over for free:
a = one_hot(target_slot), so v reduced to a polarity-selected constant and the only question
was whether the readout could use the operator. A real lane retrain has no such gift. It must
form the query, address the store by content, AND read the result -- and the query comes from
h, which is exactly what the offset perturbs.

So this closes the gap. The address is computed the way core/clms.py:163 computes it:

    K = [_entity_key(key_emb, e) for e in the 8 slot entities]     frozen key table
    q = h @ W_q                                                    W_q TRAINED
    a = softmax(q @ K.T / sqrt(d_k))                               lane_type 3: a -= 1/n_slot
    v = a @ (val[pols] - mean)
    z = gelu(concat([v, h @ W_g]) @ W_h + b_h);  s = z @ W_out

The queried entity is recovered from the dump's own prompt spec ("is ruros => " -> ruros) and
placed in one of the eight slots; the other seven are fresh nonce. Everything trainable is a
clms. parameter, which is what --freeze-trunk leaves trainable (cli/train.py:2351).

Compared against H_9926's oracle numbers on the same two splits:

    oracle, W_g trainable      held-mean 0.9208 (dense) / 0.8994 (sparse)
    no oracle                  this file

If the no-oracle arm holds up, the toy has finally been run under the real retrain's
conditions and the effect size stands. If it collapses, then the whole chain's 0.90 was bought
by a gift the retrain does not get, and the fire calculus goes back to unfavourable.
"""
import numpy as np, os, sys, json, re
import anima_py
sys.path.insert(0, os.path.join(os.path.dirname(anima_py.__file__), "core"))
import decode as clm
from clms import _entity_key

W = clm.clm_load_weights(os.path.join(os.path.expanduser("~"), "anima-weights",
                                      "store303_s2000.clm"))
c = W["clms"]
Wg0 = np.asarray(c["W_g"], dtype=np.float64)
Wq0 = np.asarray(c["W_q"], dtype=np.float64)
key_emb = np.asarray(c["key_emb"], dtype=np.float64)
val = np.asarray(c["val"], dtype=np.float64)
n_slot, d_k, r = int(c["n_slot"]), int(c["d_k"]), int(c["r"])
SCALE = 1.0 / np.sqrt(float(d_k))
LR, LR_BIG, STEPS, MOM = 3e-3, 3e-3 / 34.0, 3000, 0.9
D = list(range(9))

ZS = [np.load(f, allow_pickle=True) for f in ("rot_a.npz", "rot_b.npz", "rot_c.npz")]
SPEC = {}
for f in ("rot_a.json", "rot_b.json", "rot_c.json"):
    for it in json.load(open(f))["items"]:
        SPEC[it["id"]] = it["prompt"]


def load(d, op):
    hs, ents = [], []
    for z in ZS:
        for k in sorted(z.files):
            if k.startswith("d%d|%s|" % (d, op)) and k.endswith("__last"):
                pid = k[:-len("__last")]
                p = SPEC.get(pid)
                if p is None:
                    continue
                toks = p.split()
                hs.append(np.asarray(z[k], dtype=np.float64).reshape(-1))
                ents.append(toks[1])                       # "is <entity> => "
    return np.stack(hs), ents


HH = {d: {o: load(d, o) for o in ("is", "not")} for d in D}
base = 0.5 * (val[0] + val[1])
CONS, VOW = "bdgkmnprstvz", "aeiou"


def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x ** 3)))


def dgelu(x):
    t = np.tanh(0.7978845608 * (x + 0.044715 * x ** 3))
    return 0.5 * (1.0 + t) + 0.5 * x * (1.0 - t ** 2) * 0.7978845608 * (1.0 + 3 * 0.044715 * x ** 2)


def nonce(rr, L=5):
    s = ""
    while len(s) < L:
        s += rr.choice(list(CONS)) + rr.choice(list(VOW))
    return s[:L]


def build(ds, seed):
    rr = np.random.default_rng(seed)
    hs, Ks, Vs, ys = [], [], [], []
    for d in ds:
        for op, opv in (("is", 0), ("not", 1)):
            hh, ents = HH[d][op]
            for i in range(len(hh)):
                tslot = int(rr.integers(0, n_slot))
                names = [nonce(rr) for _ in range(n_slot)]
                names[tslot] = ents[i]                     # the queried entity really is in the store
                pols = np.array([0] * (n_slot // 2) + [1] * (n_slot - n_slot // 2))
                rr.shuffle(pols)
                K = np.stack([_entity_key(key_emb, e) for e in names]).astype(np.float64)
                hs.append(hh[i]); Ks.append(K)
                Vs.append(val[pols] - base)
                ys.append(1.0 if ((pols[tslot] == 0) != (opv == 1)) else -1.0)
    return np.stack(hs), np.stack(Ks), np.stack(Vs), np.array(ys)


def fwd(Xh, Ks, Vs, Wq, Wg, Wh, bh, Wo):
    q = Xh @ Wq                                            # (n, d_k)
    att = np.einsum("nk,nsk->ns", q, Ks) * SCALE
    att = att - att.max(axis=1, keepdims=True)
    e = np.exp(att); a = e / e.sum(axis=1, keepdims=True)
    ac = a - 1.0 / n_slot                                  # lane_type 3 centring
    v = np.einsum("ns,nsd->nd", ac, Vs)
    cat = np.concatenate([v, Xh @ Wg], axis=1)
    pre = cat @ Wh + bh
    z = gelu(pre); s = z @ Wo
    return s, z, pre, cat, a, v, q


def train(ds, seed=7, shuffle=False):
    Xh, Ks, Vs, y = build(ds, seed)
    rng = np.random.default_rng(seed)
    if shuffle:
        y = y[rng.permutation(len(y))]
    Wq = Wq0.copy(); Wg = Wg0.copy()
    Wh = rng.normal(0, 0.126, (val.shape[1] + Wg.shape[1], r)); bh = np.zeros(r)
    Wo = rng.normal(0, 0.054, (r, 2))
    mq = np.zeros_like(Wq); mg = np.zeros_like(Wg)
    mh = np.zeros_like(Wh); mo = np.zeros_like(Wo); mb = np.zeros_like(bh)
    for _ in range(STEPS):
        s, z, pre, cat, a, v, q = fwd(Xh, Ks, Vs, Wq, Wg, Wh, bh, Wo)
        m = s[:, 0] - s[:, 1]
        p = 1.0 / (1.0 + np.exp(-np.clip(m * y, -60, 60)))
        gm = (-(1 - p) * y)[:, None] * np.array([1.0, -1.0])
        gz = gm @ Wo.T * dgelu(pre)
        mh = MOM * mh + cat.T @ gz / len(y)
        mo = MOM * mo + z.T @ gm / len(y)
        mb = MOM * mb + gz.mean(0)
        gcat = gz @ Wh.T
        gv = gcat[:, :val.shape[1]]
        mg = MOM * mg + Xh.T @ gcat[:, val.shape[1]:] / len(y)
        # through v = (a - 1/n) @ Vs  ->  a  ->  softmax  ->  att  ->  q
        ga = np.einsum("nd,nsd->ns", gv, Vs)
        gatt = a * (ga - (ga * a).sum(axis=1, keepdims=True))
        gq = np.einsum("ns,nsk->nk", gatt, Ks) * SCALE
        mq = MOM * mq + Xh.T @ gq / len(y)
        Wq -= LR_BIG * mq; Wg -= LR_BIG * mg
        Wh -= LR * mh; Wo -= LR * mo; bh -= LR * mb
    return Wq, Wg, Wh, bh, Wo


def sc(P, dd, seed=99):
    Wq, Wg, Wh, bh, Wo = P
    Xh, Ks, Vs, y = build(dd, seed)
    s, _, _, _, _, _, _ = fwd(Xh, Ks, Vs, Wq, Wg, Wh, bh, Wo)
    return float((np.sign(s[:, 0] - s[:, 1]) == y).mean())


print("  NO ORACLE -- the lane must address the store itself (W_q trained, keys frozen)")
print("  %-22s %8s %10s %9s   %s" % ("train offsets", "seen", "held-mean", "held-min",
                                     "H_9926 oracle held-mean"))
print("  " + "-" * 78)
for S, prev in (([0, 1, 2, 3, 5, 7], 0.9208), ([0, 2, 5, 8], 0.8994)):
    HO = [d for d in D if d not in S]
    P = train(S)
    held = [sc(P, [d]) for d in HO]
    print("  %-22s %8.4f %10.4f %9.4f   %.4f" % (str(S), sc(P, S), float(np.mean(held)),
                                                 min(held), prev))
S = [0, 1, 2, 3, 5, 7]
HO = [d for d in D if d not in S]
null = [float(np.mean([sc(train(S, seed=s, shuffle=True), [d]) for d in HO])) for s in (7, 11)]
print("  shuffled-label floor: mean %.4f  max %.4f" % (float(np.mean(null)), float(np.max(null))))
