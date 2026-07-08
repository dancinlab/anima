#!/usr/bin/env python3
"""H_9235 fork-A $0 pre-check (Fable design · numpy · torch-free · cached pair hiddens · CPU minutes).
Decisive question: can a read-side POOLER (mean-pool over positions → gelu bottleneck → readout) route BOTH concepts
from the superposed context into a rep that supports HELD-OUT non-additive (XOR) composition, where the last-position
(generation point) rep FAILS? = does fork A (context-pooling lane) have a route before we wire/train it into .clm.

Mirrors the lane exactly: c = mean_t yn_t ; z = gelu(c@W1+b1) [r=128] ; y = sigmoid(z@w) → 5-bit XOR(code_i,code_j).
Trained JOINTLY end-to-end on SEEN pairs only (BCE) — NOT the two-stage recover→bind probe (avoids rung-b-analyze-py-1
artifact). Test = held-out pairs (combinations never co-trained).
CONTROLS (one per session trap · convergence rung-b-analyze-py-1):
  main    mean-pool + gelu       held-out XOR ≥0.85 = route exists (fork A alive)
  lane-OFF last-position + gelu   ≤0.60 must FAIL (last A=0.07 predicts; proves ROUTING is the lever, not the head)
  additive mean-pool + LINEAR head ≤0.60 must FAIL (gelu-pass ∧ linear-fail = the bottleneck nonlinearity composes)
  handed  clean one-hot ids + gelu ≥0.85 must PASS (harness learnability · positive control)
  shuffle mean-pool + shuffled labels ≈0.5 (bind-destruction)
CRACK = main ≥0.85 ∧ lane-OFF ≤0.60 ∧ additive ≤0.60 ∧ handed ≥0.85 ∧ shuffle chance → fork A route proven ($0)
  → wire CLML lane into .clm + train frozen-trunk + engine-native system-G1 (the terminal G1 verdict).
honest kill (Fable §6): held-out CLASSIFICATION pass ≠ composed GENERATION; only system-G1 sees that. pre-check green
  = "route exists", not "G1 falls".
"""
import json, sys, numpy as np
NPZ = sys.argv[1] if len(sys.argv) > 1 else "pair_hidden.npz"
CONC = sys.argv[2] if len(sys.argv) > 2 else "concepts.json"
concepts = json.load(open(CONC))
names = sorted(concepts, key=lambda c: concepts[c]["idx"]); N = len(names); BITS = 5
code = np.array([concepts[c]["code"] for c in names], dtype=np.float64)
Z = np.load(NPZ)
keys = [k[:-5] for k in Z.files if k.endswith("__seq")]
def parse(k): p = k.split("_"); return p[0], int(p[-2]), int(p[-1])
train = [(k,) + parse(k)[1:] for k in keys if k.startswith("train_")]
held = [(k,) + parse(k)[1:] for k in keys if k.startswith("held_")]
T, d = Z[keys[0] + "__seq"].shape
def xor(a, b): return code[a].astype(int) ^ code[b].astype(int)
def sigmoid(x): return 1/(1+np.exp(-np.clip(x, -30, 30)))
def gelu(x): return 0.5 * x * (1 + np.tanh(0.7978845608 * (x + 0.044715 * x**3)))
def dgelu(x):
    t = np.tanh(0.7978845608 * (x + 0.044715 * x**3))
    return 0.5*(1+t) + 0.5*x*(1-t**2)*0.7978845608*(1+3*0.044715*x**2)

def feat(item, kind, handed_atoms=None):
    if kind == "handed":                              # clean one-hot concept ids (positive control · no XOR in features)
        a, b = item[1], item[2]; v = np.zeros(2*N); v[a] = 1; v[N+b] = 1; return v
    S = Z[item[0] + "__seq"].astype(np.float64)
    c = S[T-1] if kind == "last" else S.mean(0)       # generation point vs full-context pool
    return c

def build(items, kind):
    X = np.array([feat(it, kind) for it in items])
    mu = X.mean(0); sd = X.std(0) + 1e-6
    return (X - mu) / sd, mu, sd

def run(kind, seed, steps=4000, r=128, lr=0.05, linear=False, shuffle=False):
    rng = np.random.default_rng(seed)
    Xtr, mu, sd = build(train, kind); Xte = (np.array([feat(it, kind) for it in held]) - mu) / sd
    Ytr = np.array([xor(it[1], it[2]) for it in train], dtype=np.float64)
    Yte = np.array([xor(it[1], it[2]) for it in held], dtype=np.float64)
    if shuffle: Ytr = Ytr[rng.permutation(len(Ytr))]
    din = Xtr.shape[1]
    if linear:
        W = rng.standard_normal((BITS, din)) * 0.05
        for _ in range(steps):
            bi = rng.integers(0, len(Xtr), 128); h = Xtr[bi]; p = sigmoid(h @ W.T); g = p - Ytr[bi]
            W -= lr * g.T @ h / 128
        return float((np.round(sigmoid(Xte @ W.T)).astype(int) == Yte).mean())
    W1 = rng.standard_normal((din, r)) * (1/np.sqrt(din)); b1 = np.zeros(r)
    w = rng.standard_normal((BITS, r)) * 0.05
    for _ in range(steps):
        bi = rng.integers(0, len(Xtr), 128); h = Xtr[bi]
        pre = h @ W1 + b1; z = gelu(pre); p = sigmoid(z @ w.T); g = p - Ytr[bi]
        gw = g.T @ z / 128; gz = (g @ w) * dgelu(pre)
        gW1 = h.T @ gz / 128; gb1 = gz.mean(0)
        w -= lr*gw; W1 -= lr*gW1; b1 -= lr*gb1
    pre = Xte @ W1 + b1; return float((np.round(sigmoid(gelu(pre) @ w.T)).astype(int) == Yte).mean())

if __name__ == "__main__":
    print("N=%d T=%d d=%d train=%d held=%d (XOR 5-bit · joint end-to-end)" % (N, T, d, len(train), len(held)), flush=True)
    res = {"N": N, "T": T, "d": d}
    arms = {
        "main(mean+gelu)":   dict(kind="mean"),
        "laneOFF(last+gelu)": dict(kind="last"),
        "additive(mean+lin)": dict(kind="mean", linear=True),
        "handed(onehot+gelu)": dict(kind="handed"),
        "shuffle(mean+gelu)": dict(kind="mean", shuffle=True),
    }
    for name, kw in arms.items():
        v = round(float(np.mean([run(seed=s, **kw) for s in (0, 1, 2)])), 4)
        res[name] = v; print("[%s] heldout_XOR=%.3f" % (name, v), flush=True)
    m = res["main(mean+gelu)"]; lo = res["laneOFF(last+gelu)"]; ad = res["additive(mean+lin)"]
    hd = res["handed(onehot+gelu)"]; sh = res["shuffle(mean+gelu)"]
    if hd < 0.85:
        res["verdict"] = "⚙️ INVALID — handed positive control %.2f<0.85: harness can't learn XOR, pre-check uninformative" % hd
    elif m >= 0.85 and lo <= 0.60 and ad <= 0.60 and sh < 0.60:
        res["verdict"] = ("🟢 FORK-A ROUTE PROVEN ($0) — mean-pool+gelu routes both concepts to held-out XOR (%.2f) where "
                          "last-position FAILS (%.2f) and a linear head FAILS (%.2f) ⇒ the context-pooling lane has a real "
                          "route + the bottleneck nonlinearity composes. → wire CLML lane + frozen-trunk train + engine-native "
                          "system-G1 (terminal G1 verdict). NB: route≠generation; system-G1 is the real bar." % (m, lo, ad))
    elif m >= 0.85 and lo > 0.60:
        res["verdict"] = "🟡 ROUTE-BUT-NO-ROUTING-GAIN — main %.2f but lane-OFF %.2f also passes: last-position suffices, pooling not the lever (re-examine)." % (m, lo)
    else:
        res["verdict"] = ("🔴 FORK-A NO ROUTE — mean-pool+gelu held-out XOR=%.2f<0.85 while handed=%.2f: the additive-operator "
                          "wall re-enters at LEARNING (superposed pool → pair-specific lookup, no generalizing bind). fork A dead "
                          "at $0; the read-side route over the frozen trunk does not compose held-out pairs." % (m, hd))
    print("\n=== VERDICT:", res["verdict"], "===", flush=True)
    open("fork_a_precheck_RESULT.json", "w").write(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
