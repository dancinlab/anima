#!/usr/bin/env python3
"""H_9235 fork-A — Gate 1 (base CE) + Gate 2 (trainability probe) on the NO-COPY dump (numpy · $0 · decisive).
Gate 1: base (lane-OFF) CE at the non-copyable word-initial composed positions. Must be ≫0 (≳1 nat) — if ≈0
        the trunk already routes these in weights, format can't help (go straight to Gate 2 verdict).
Gate 2 (THE decisive cheap terminal, Fable): fit a same-capacity MLP probe pool_yn → target(word-initial byte /
        word-id) on TRAIN. If it CAN'T fit train, no CE loss can → (B) SIGNAL-WALL: fork-A route exists (XOR pre-check
        0.98) but the frozen pool gives no learnable real-task signal = H_1840 one level up (learning-signal wall, NOT
        representation). If it fits train AND generalizes to held examples → lane trainable → proceed to Gate 3/4.
INPUT: nocopy_hidden.npz (n*__mean [d] pooled yn, n*__logits [V] base), nocopy_prompts.json (target byte + word)."""
import sys
import json
import numpy as np

NPZ = sys.argv[1] if len(sys.argv) > 1 else "nocopy_hidden.npz"
PROMPTS = sys.argv[2] if len(sys.argv) > 2 else "nocopy_prompts.json"
spec = json.load(open(PROMPTS)); items = spec["items"]
Z = np.load(NPZ)
ids = [it["id"] for it in items if (it["id"] + "__mean") in Z.files and (it["id"] + "__logits") in Z.files]
by = {it["id"]: it for it in items}
d = Z[ids[0] + "__mean"].shape[0]; V = Z[ids[0] + "__logits"].shape[0]
POOL = np.array([Z[i + "__mean"] for i in ids], dtype=np.float64)          # [N,d] pooled yn
BL = np.array([Z[i + "__logits"] for i in ids], dtype=np.float64)          # [N,V] base logits
TGT = np.array([by[i]["target"] for i in ids], dtype=np.int64)             # next-byte target
WORDS = [by[i]["word"].lower() for i in ids]
wvocab = sorted(set(WORDS)); widx = {w: k for k, w in enumerate(wvocab)}
WID = np.array([widx[w] for w in WORDS], dtype=np.int64)                    # word class
N = len(ids)
print("N=%d d=%d V=%d word-classes=%d" % (N, d, V, len(wvocab)), flush=True)

def ce(logits, y):
    m = logits.max(1, keepdims=True); lse = m[:, 0] + np.log(np.exp(logits - m).sum(1))
    return float((lse - logits[np.arange(len(y)), y]).mean())

# ── Gate 1: base CE at these routing positions ──
g1 = ce(BL, TGT); base_acc = float((BL.argmax(1) == TGT).mean())
print("[Gate1] base(lane-OFF) CE=%.3f nat · next-byte acc=%.3f  %s" %
      (g1, base_acc, "≫0 → residual EXISTS (routing signal present)" if g1 >= 1.0 else "≈0 → trunk already routes (weights-memorized · signal may be dead)"), flush=True)

# ── Gate 2: MLP probe pool_yn → word-id (train fit + held generalize) ──
rng = np.random.default_rng(7); perm = rng.permutation(N); ntr = int(N * 0.8)
tr, te = perm[:ntr], perm[ntr:]
mu = POOL[tr].mean(0); sd = POOL[tr].std(0) + 1e-6
X = (POOL - mu) / sd
def gelu(x): return 0.5*x*(1+np.tanh(0.7978845608*(x+0.044715*x**3)))
def dgelu(x):
    t = np.tanh(0.7978845608*(x+0.044715*x**3)); return 0.5*(1+t)+0.5*x*(1-t*t)*0.7978845608*(1+3*0.044715*x*x)
def probe(y, ncls, H=128, steps=6000, lr=0.1):
    W1 = rng.standard_normal((d, H))*(1/np.sqrt(d)); b1 = np.zeros(H); W2 = rng.standard_normal((H, ncls))*0.05
    for _ in range(steps):
        bi = tr[rng.integers(0, len(tr), 256)]; h = X[bi]
        z = h@W1+b1; a = gelu(z); lg = a@W2; lg -= lg.max(1, keepdims=True)
        p = np.exp(lg); p /= p.sum(1, keepdims=True); g = p.copy(); g[np.arange(len(bi)), y[bi]] -= 1; g /= len(bi)
        gW2 = a.T@g; ga = g@W2.T; gz = ga*dgelu(z); gW1 = h.T@gz; gb1 = gz.sum(0)
        W2 -= lr*gW2; W1 -= lr*gW1; b1 -= lr*gb1
    def acc(idx):
        lg = gelu(X[idx]@W1+b1)@W2; return float((lg.argmax(1) == y[idx]).mean())
    return acc(tr), acc(te)
tr_acc, te_acc = probe(WID, len(wvocab))
chance = 1.0/len(wvocab)
print("[Gate2] probe pool_yn→word-id: TRAIN acc=%.3f · held acc=%.3f (chance=%.3f)" % (tr_acc, te_acc, chance), flush=True)

res = {"N": N, "d": d, "word_classes": len(wvocab), "gate1_base_ce": round(g1, 4), "gate1_base_acc": round(base_acc, 4),
       "gate2_train_acc": round(tr_acc, 4), "gate2_held_acc": round(te_acc, 4), "chance": round(chance, 4)}
if tr_acc < 0.30:
    res["verdict"] = ("🧱 (B) SIGNAL-WALL — the probe CANNOT fit even TRAIN (%.2f, chance %.2f): the frozen pool gives no "
                      "learnable name→word routing signal. fork-A route exists (XOR 0.98) but is UNTRAINABLE from the real "
                      "task = H_1840 one level up (learning-signal wall, NOT representation). Honest terminal." % (tr_acc, chance))
elif te_acc >= 0.5 and te_acc >= 2*chance:
    res["verdict"] = ("🟢 TRAINABLE — probe fits train (%.2f) AND generalizes to held examples (%.2f ≫ chance %.2f) ⇒ the "
                      "pool carries a routable signal → proceed to Gate 3 (lane train on word-initial CE) + Gate 4 (system-G1)." % (tr_acc, te_acc, chance))
else:
    res["verdict"] = ("🟡 MEMORIZES not ROUTES — train fits (%.2f) but held ≈chance (%.2f vs %.2f): probe memorizes contexts, "
                      "no pair-agnostic route = underspecification/additive-floor risk. lane likely learns unigram tilt; "
                      "Gate 4 ablation-specificity would catch it. DIRECTIONAL-negative." % (tr_acc, te_acc, chance))
print("\n=== VERDICT:", res["verdict"], "===", flush=True)
open("clml_gate12_RESULT.json", "w").write(json.dumps(res, indent=2, ensure_ascii=False))
print(json.dumps(res, indent=2, ensure_ascii=False))
