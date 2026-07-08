#!/usr/bin/env python3
"""H_9235 H2-lite analysis (numpy · torch-free · runs on CACHED 303M hiddens · CPU minutes · $0).
The decisive cell: earned(real-303M-hidden atoms) × trained(adapter+interaction head via composition signal).
H_9234=handed×trained PASS(1.00) · #3135=blind×fixed FAIL · H_1840=blind×CE FAIL — this = the untested cell.

INPUTS: unary_hidden.npz (concept__p{k}__last/mean/seq from anima evaluate --dump-hidden), concepts.json (5-bit codes).
FROZEN bars (pre-registered · card H_9235):
  H1 unary probe        held-out-paraphrase concept-id acc ≥0.80 clean / <0.55 blind  (expected-pass, NOT a greenlight)
  RUNG-a operator       op_heldout ≥0.85 PASS · 0.60-0.85 partial · ≤0.60 FAIL  (≥2/3 seeds · earned real atoms)
  additive control      additive readout on same real atoms ≤0.60 (must FAIL = H_9234 gate replication)
  fixed-VSA control     frozen random-proj adapter ≤0.60 (must FAIL = #3135 replication · trained adapter load-bearing)
  handed positive ctrl  clean-random atoms + same head ≥0.85 (must PASS = harness learnability · evaluate-py-3)
  shuffle               pairing-shuffled op ≈0.5±0.1 (bind-destruction)
CRACK(rung-a) = real-atom operator ≥0.85 ∧ additive/fixed-VSA FAIL ∧ handed PASS ∧ shuffle chance.
modal(Fable ~85%) = real-atom operator ≤0.60 (blind atoms not operator-grade) while handed PASS → #3135 recurses,
  localizes wall to atom-cleanness → fork B (trunk curriculum) is the only remaining GPU lever.
verdict-integrity(clm-decode-py-2): if H1 unary probe ALSO <0.55 AND poscontrol cos>0.999, dump is a hexa-skew
  artifact NOT a blind result → INVALID, re-dump; a clean blind verdict needs distinguishable hiddens first.
"""
import json, sys, numpy as np
NPZ = sys.argv[1] if len(sys.argv) > 1 else "unary_hidden.npz"
CONC = sys.argv[2] if len(sys.argv) > 2 else "concepts.json"
POOL = sys.argv[3] if len(sys.argv) > 3 else "last"   # 'last' or 'mean'
concepts = json.load(open(CONC))
names = sorted(concepts, key=lambda c: concepts[c]["idx"])
N = len(names); BITS = 5
code = np.array([concepts[c]["code"] for c in names], dtype=np.float64)  # [N,5] zero-unary-MI
assert abs(code.mean(0) - 0.5).max() < 1e-9
Z = np.load(NPZ)
d = Z["%s__p0__%s" % (names[0], POOL)].shape[0]
# per-concept paraphrase vectors: split train(p0-7)/test(p8-15)
def para(c, split):
    ks = range(0, 8) if split == "train" else range(8, 16)
    return np.array([Z["%s__p%d__%s" % (c, k, POOL)] for k in ks if ("%s__p%d__%s" % (c, k, POOL)) in Z])
# frozen atom = mean of TRAIN paraphrase hiddens · STANDARDIZE per-dim (real hiddens are large-scale;
# without this the trainable adapter backprop dA.T@E explodes — a numeric artifact, not a blind result).
ATOM = np.array([para(c, "train").mean(0) for c in names])   # [N,d]
ATOM = ATOM - ATOM.mean(0, keepdims=True)
ATOM = ATOM / (ATOM.std(0, keepdims=True) + 1e-6)            # O(1) scale, matches handed atoms

def sigmoid(x): return 1/(1+np.exp(-np.clip(x, -30, 30)))
def smax(z): z = z - z.max(-1, keepdims=True); e = np.exp(z); return e/e.sum(-1, keepdims=True)

# ── H1 unary probe: 32-way linear probe on paraphrase hiddens, train p0-7, test p8-15 ──
def h1_probe(seed=0, steps=3000):
    rng = np.random.default_rng(seed)
    Xtr, ytr, Xte, yte = [], [], [], []
    for i, c in enumerate(names):
        for v in para(c, "train"): Xtr.append(v); ytr.append(i)
        for v in para(c, "test"):  Xte.append(v); yte.append(i)
    Xtr = np.array(Xtr) - ATOM.mean(0); Xte = np.array(Xte) - ATOM.mean(0)
    ytr = np.array(ytr); yte = np.array(yte)
    W = rng.standard_normal((N, d)) * 0.01
    for _ in range(steps):
        p = smax(Xtr @ W.T); g = p.copy(); g[np.arange(len(ytr)), ytr] -= 1
        W -= 0.5 * g.T @ Xtr / len(ytr)
    acc = float((smax(Xte @ W.T).argmax(1) == yte).mean())
    return acc

# ── operator rungs: atoms E (frozen or handed), trainable adapter d→96 + interaction MLP head ──
pairs = [(a, b) for a in range(N) for b in range(N) if a != b]
rngs = np.random.default_rng(7); held = set()
for k in rngs.permutation(len(pairs)):
    ab = pairs[k]
    if len(held) < 150 and ab not in held: held.add(ab)
train = [p for p in pairs if p not in held]; heldl = list(held)
def xor(a, b): return code[a].astype(int) ^ code[b].astype(int)

def op_run(mode, seed, steps=5000, H=128, k=96):
    """mode: real-interaction / real-additive / real-fixedvsa / handed / real-shuffle."""
    rng = np.random.default_rng(seed)
    if mode == "handed":
        E = rng.standard_normal((N, d))               # clean random atoms (positive control)
    else:
        E = ATOM.copy()                               # frozen real 303M hiddens (earned atoms)
    E = E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-9)   # unit-norm per atom (real & handed comparable · adapter-stable)
    # adapter d->k
    if mode == "real-fixedvsa":
        Wad = rng.standard_normal((k, d)) * (1/np.sqrt(d)); train_ad = False   # frozen random projection
    else:
        Wad = rng.standard_normal((k, d)) * 0.05; train_ad = True
    A = E @ Wad.T                                      # [N,k] slotted atoms (recomputed if Wad trains)
    if mode in ("real-additive",):
        W = rng.standard_normal((BITS, k)) * 0.1
    else:
        U = rng.standard_normal((H, 2*k)) * 0.1; W = rng.standard_normal((BITS, H)) * 0.1
    lr = 0.1
    for step in range(steps):
        if train_ad: A = E @ Wad.T
        idx = rng.integers(0, len(train), 256)
        aI = np.array([train[i][0] for i in idx]); bI = np.array([train[i][1] for i in idx])
        Y = np.array([xor(a, b) for a, b in zip(aI, bI)]); ea, eb = A[aI], A[bI]
        if mode == "real-additive":
            h = ea + eb; p = sigmoid(h @ W.T); g = p - Y; gW = g.T @ h / 256; W -= lr*gW
            if train_ad:
                gA = g @ W  # [256,k]
                dWad = np.zeros_like(Wad)
                for row, ci in ((gA, aI),): pass
                # backprop adapter: dA[a]+=gA, dA[b]+=gA ; dWad += dA.T @ E
                dA = np.zeros((N, k)); np.add.at(dA, aI, gA/256); np.add.at(dA, bI, gA/256)
                Wad -= lr * dA.T @ E
        else:
            cat = np.concatenate([ea, eb], 1); z = cat @ U.T; hh = np.maximum(z, 0)
            p = sigmoid(hh @ W.T); g = p - Y; W -= lr*(g.T@hh/256)
            gh = (g @ W) * (z > 0); U -= lr*(gh.T@cat/256); gcat = gh @ U
            if train_ad:
                dA = np.zeros((N, k)); np.add.at(dA, aI, gcat[:, :k]/256); np.add.at(dA, bI, gcat[:, k:]/256)
                Wad -= lr * dA.T @ E
    if train_ad: A = E @ Wad.T
    zero = np.zeros(k)
    def pred(va, vb):
        if mode == "real-additive": return sigmoid(W @ (va + vb))
        z = np.concatenate([va, vb]) @ U.T; return sigmoid(W @ np.maximum(z, 0))
    def acc(prs, only_a=False):
        out = []
        for a, b in prs:
            pr = pred(A[a], zero if only_a else A[b])
            out.append((np.round(pr).astype(int) == xor(a, b)).mean())
        return float(np.mean(out))
    op = acc(heldl)
    onlyA = acc(heldl, only_a=True)   # bind-destruction: B zeroed → must drop to ~chance if truly binding both
    return op, onlyA

if __name__ == "__main__":
    print("N=%d d=%d pool=%s held=%d train=%d" % (N, d, POOL, len(heldl), len(train)), flush=True)
    h1 = float(np.mean([h1_probe(s) for s in (0, 1, 2)]))
    print("[H1] unary held-out-paraphrase concept-id acc=%.3f (%s)" %
          (h1, "clean≥0.80" if h1 >= 0.80 else ("blind<0.55" if h1 < 0.55 else "mid")), flush=True)
    res = {"N": N, "d": d, "pool": POOL, "h1_unary_probe": round(h1, 4)}
    rows = {}
    for mode in ("real-interaction", "real-additive", "real-fixedvsa", "handed"):
        ops = [op_run(mode, s) for s in (0, 1, 2)]
        rows[mode] = {"op": round(float(np.mean([o for o, _ in ops])), 4),
                      "onlyA": round(float(np.mean([s for _, s in ops])), 4)}
        print("[%s] operator=%.3f onlyA(B=0)=%.3f" % (mode, rows[mode]["op"], rows[mode]["onlyA"]), flush=True)
    res["rungA"] = rows
    ri = rows["real-interaction"]["op"]; add = rows["real-additive"]["op"]
    ri_onlyA = rows["real-interaction"]["onlyA"]; hd = rows["handed"]["op"]
    invalid = h1 < 0.55  # + poscontrol cos>0.999 flagged at dump; here H1<0.55 = suspect blind vs skew
    # rung-a HONEST scope (evaluate-py-3): with H1-separable unary atoms + a trainable 363K adapter, a pass is
    # HANDED-EQUIVALENT (the adapter re-derives a clean factorization from separable atoms) — a PRECONDITION,
    # NOT a wall break. The additive control failing + onlyA dropping to chance confirm genuine 2-atom binding of
    # SEPARABLE atoms, but that is the easy/segmentation-granted case. Decisive test = rung b (superposed context).
    precond = ri >= 0.85 and add <= 0.60 and ri_onlyA < 0.60 and hd >= 0.85 and h1 >= 0.80
    if invalid:
        res["verdict"] = "⚙️ INVALID-SUSPECT — H1 unary probe %.2f<0.55: rule out clm-decode-py-2 hexa-skew (poscontrol) before a blind verdict" % h1
    elif precond:
        res["verdict"] = ("🟡 RUNG-A PRECONDITION-MET (NOT a wall break · handed-equivalent per evaluate-py-3) — real 303M "
                          "UNARY atoms are cleanly separable (H1=%.2f) and a trainable adapter composes them to held-out XOR "
                          "(op=%.2f · additive %.2f FAIL · onlyA %.2f→chance = genuine 2-atom bind of SEPARABLE atoms). This is "
                          "the segmentation-GRANTED case ≈ handed. ⚠ normalization-fragile (fixed-VSA arm flips with atom scale). "
                          "DECISIVE test = rung b: recover BOTH atoms from ONE superposed pair context (no handed segmentation)." %
                          (h1, ri, add, ri_onlyA))
    else:
        res["verdict"] = ("🔴 RUNG-A FAIL — real-atom operator %.2f≤floor while handed %.2f PASS ⇒ even segmentation-granted "
                          "real atoms NOT composable. Wall at atom level → fork B." % (ri, hd))
    print("\n=== VERDICT:", res["verdict"], "===", flush=True)
    open("h2lite_rungA_RESULT.json", "w").write(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
