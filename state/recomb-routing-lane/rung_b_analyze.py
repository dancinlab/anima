#!/usr/bin/env python3
"""H_9235 rung b — the DECISIVE segmentation test (numpy · torch-free · CACHED pair hiddens · fast · $0).
rung a granted segmentation (1 clean atom/slot = handed-equivalent). rung b asks the wall's real question:
do the 303M per-position hiddens keep TWO concepts SEPARABLE in ONE superposed context ("The A and the B"),
so a read-side lane could recover both and bind them? If yes → wall NOT in representation (fork A wiring). If no
→ wall = context-segmentation (fork B trunk curriculum). This is measured ROBUSTLY as SLOT-RECOVERY: can a linear
probe (trained on SEEN pairs) recover BOTH atom identities from the pair context — the operator then follows from
H_9234 (separable atoms → interaction binds). No fragile trained attention pooler; direct decodability.

INPUT: pair_hidden.npz (train_A_B__seq/held_A_B__seq = per-position [T,d]), concepts.json.
Poolings probed: mean · max · concat(mean,max) · best-single-position. For each, a 32-way linear probe for the
FIRST concept (A) and SECOND (B), trained on seen pairs, tested held-out.
FROZEN bars (card H_9235):
  slot-recovery A & B   held-out per-concept acc ≥0.70 BOTH → context keeps both separable (segmentation OK)
  operator (confirm)    on the two recovered concept-logit vectors → interaction head → held-out XOR ≥0.85
  additive control      additive readout on recovered reps ≤0.60 (must FAIL)
CRACK = recover A ≥0.70 ∧ recover B ≥0.70 ∧ operator ≥0.85 ∧ additive FAIL → wall NOT in repr → fork A.
modal(Fable ~85%) = recover A or B <0.70 (concepts entangled/superposed in the context) ⇒ wall = context-SEGMENTATION
  → fork B trunk curriculum the only remaining GPU lever; no read-side lane over the frozen trunk suffices.
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

def pooled(item, kind):
    k = item[0]
    if kind == "last": return Z[k + "__last"].astype(np.float64)     # generation point (causal after both concepts)
    if kind == "mean": return Z[k + "__mean"].astype(np.float64)
    S = Z[k + "__seq"].astype(np.float64)
    if kind == "max": return S.max(0)
    if kind == "lastmean": return np.concatenate([Z[k + "__last"].astype(np.float64), Z[k + "__mean"].astype(np.float64)])
    return S  # raw

def probe(Xtr, ytr, Xte, yte, steps=2500, lr=0.4):
    mu = Xtr.mean(0); sd = Xtr.std(0) + 1e-6
    Xtr = (Xtr - mu) / sd; Xte = (Xte - mu) / sd
    W = np.zeros((N, Xtr.shape[1]))
    for _ in range(steps):
        z = Xtr @ W.T; z -= z.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
        g = p; g[np.arange(len(ytr)), ytr] -= 1; W -= lr * g.T @ Xtr / len(ytr)
    return float(((Xte @ W.T).argmax(1) == yte).mean()), W, mu, sd

def sigmoid(x): return 1/(1+np.exp(-np.clip(x, -30, 30)))

if __name__ == "__main__":
    print("N=%d T=%d d=%d train=%d held=%d" % (N, T, d, len(train), len(held)), flush=True)
    res = {"N": N, "T": T, "d": d, "n_train": len(train), "n_held": len(held), "recovery": {}}
    best_rec = {"A": 0.0, "B": 0.0}
    for kind in ("last", "mean", "lastmean"):
        Xtr = np.array([pooled(it, kind) for it in train]); Xte = np.array([pooled(it, kind) for it in held])
        aA, _, _, _ = probe(Xtr, np.array([it[1] for it in train]), Xte, np.array([it[1] for it in held]))
        aB, _, _, _ = probe(Xtr, np.array([it[2] for it in train]), Xte, np.array([it[2] for it in held]))
        res["recovery"][kind] = {"A": round(aA, 4), "B": round(aB, 4)}
        best_rec["A"] = max(best_rec["A"], aA); best_rec["B"] = max(best_rec["B"], aB)
        print("[recover:%s] A=%.3f B=%.3f" % (kind, aA, aB), flush=True)
    # operator: build 2 concept-logit reps from the best pooling's probes, feed interaction head
    kind = "lastmean"
    Xtr = np.array([pooled(it, kind) for it in train]); Xte = np.array([pooled(it, kind) for it in held])
    _, WA, muA, sdA = probe(Xtr, np.array([it[1] for it in train]), Xte, np.array([it[1] for it in held]))
    _, WB, muB, sdB = probe(Xtr, np.array([it[2] for it in train]), Xte, np.array([it[2] for it in held]))
    def rep(it):
        x = pooled(it, kind); sA = ((x - muA) / sdA) @ WA.T; sB = ((x - muB) / sdB) @ WB.T
        return np.concatenate([sA, sB])   # [2N] concept-logit slots (recovered from real context)
    def rep_handed(it):
        oa = np.zeros(N); oa[it[1]] = 1; ob = np.zeros(N); ob[it[2]] = 1
        return np.concatenate([oa, ob])   # ground-truth one-hot slots (positive control · must PASS)
    def op_train(mode, seed):
        rng = np.random.default_rng(seed); k = 2 * N; H = 128
        rf = rep_handed if mode == "handed" else rep
        Rtr = np.array([rf(it) for it in train]); Rte = np.array([rf(it) for it in held])
        Ytr = np.array([xor(it[1], it[2]) for it in train]); Yte = np.array([xor(it[1], it[2]) for it in held])
        if mode == "additive":
            W = rng.standard_normal((BITS, k)) * 0.05
            for _ in range(3000):
                bi = rng.integers(0, len(Rtr), 128); h = Rtr[bi]; p = sigmoid(h @ W.T); g = p - Ytr[bi]
                W -= 0.1 * g.T @ h / 128
            return float((np.round(sigmoid(Rte @ W.T)).astype(int) == Yte).mean())
        U = rng.standard_normal((H, k)) * 0.1; W = rng.standard_normal((BITS, H)) * 0.1
        for _ in range(4000):
            bi = rng.integers(0, len(Rtr), 128); h = Rtr[bi]
            z = h @ U.T; hh = np.maximum(z, 0); p = sigmoid(hh @ W.T); g = p - Ytr[bi]
            W -= 0.1 * (g.T @ hh / 128); gh = (g @ W) * (z > 0); U -= 0.1 * (gh.T @ h / 128)
        z = Rte @ U.T; return float((np.round(sigmoid(np.maximum(z, 0) @ W.T)).astype(int) == Yte).mean())
    op = round(float(np.mean([op_train("inter", s) for s in (0, 1, 2)])), 4)
    op_add = round(float(np.mean([op_train("additive", s) for s in (0, 1, 2)])), 4)
    op_handed = round(float(np.mean([op_train("handed", s) for s in (0, 1, 2)])), 4)
    res["operator"] = op; res["operator_additive"] = op_add; res["operator_handed_ctrl"] = op_handed
    print("[operator] interaction=%.3f additive=%.3f handed-ctrl=%.3f" % (op, op_add, op_handed), flush=True)
    rA, rB = best_rec["A"], best_rec["B"]
    res["best_recovery"] = {"A": round(rA, 4), "B": round(rB, 4)}
    crack = rA >= 0.70 and rB >= 0.70 and op >= 0.85 and op_add <= 0.60
    if crack:
        res["verdict"] = ("🟢 RUNG-B CRACK — the 303M superposed context KEEPS both concepts separable (recover A=%.2f B=%.2f) "
                          "and a lane binds them to held-out XOR (op=%.2f · additive %.2f FAIL) ⇒ wall NOT in representation "
                          "→ fork A read-side lane wiring (system-G1)." % (rA, rB, op, op_add))
    elif rA >= 0.70 and rB >= 0.70:
        res["verdict"] = ("🟡 RUNG-B PARTIAL — both concepts RECOVERABLE (A=%.2f B=%.2f) but operator=%.2f<0.85: segmentation OK, "
                          "binding the recovered slots is the residual → adapter/lane tuning, not a trunk wall." % (rA, rB, op))
    else:
        res["verdict"] = ("🔴 RUNG-B FAIL — the 303M context does NOT keep both concepts separable (recover A=%.2f B=%.2f <0.70) ⇒ "
                          "concepts are entangled/superposed in one context (#3135 recurses at segmentation). Wall = context-SEGMENTATION "
                          "→ fork B trunk curriculum the only remaining GPU lever; no read-side lane over the frozen trunk suffices." % (rA, rB))
    print("\n=== VERDICT:", res["verdict"], "===", flush=True)
    open("h2lite_rungB_RESULT.json", "w").write(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
