#!/usr/bin/env python3
"""H_9235 per-position recovery probe — tests RF-decay vs bilingual-dilution for the last-position A-forgetting.
For each position t of the pair context "The A and the B", a linear probe (trained on seen pairs) recovers A / B.
Result (real 303M e1_slw): A fully recoverable at its own region (pos 6-17 = 0.88) then DECAYS to 0.07 by the last
position while B rises to 1.00 — classic receptive-field / causal decay, LANGUAGE-INDEPENDENT (A's representation is
NOT thinned; it is present at its own position, just outside the last position's RF). ⟹ the last-position wall is
architectural (RF-bound, #42492882), NOT bilingual-capacity dilution; an English-only model would decay identically.
The fix = a read-side lane pooling the earlier positions (where A survives) into the generation point (fork A)."""
import json, numpy as np
Z = np.load("pair_hidden.npz"); concepts = json.load(open("concepts.json"))
names = sorted(concepts, key=lambda c: concepts[c]["idx"]); N = len(names)
keys = [k[:-5] for k in Z.files if k.endswith("__seq")]
def parse(k): p = k.split("_"); return p[0], int(p[-2]), int(p[-1])
train = [(k,) + parse(k)[1:] for k in keys if k.startswith("train_")]
held = [(k,) + parse(k)[1:] for k in keys if k.startswith("held_")]
T, d = Z[keys[0] + "__seq"].shape
def probe_pos(t, which):
    Xtr = np.array([Z[it[0] + "__seq"][t] for it in train]); Xte = np.array([Z[it[0] + "__seq"][t] for it in held])
    ytr = np.array([it[which] for it in train]); yte = np.array([it[which] for it in held])
    mu = Xtr.mean(0); sd = Xtr.std(0) + 1e-6; Xtr = (Xtr - mu) / sd; Xte = (Xte - mu) / sd
    W = np.zeros((N, d))
    for _ in range(1200):
        z = Xtr @ W.T; z -= z.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
        g = p; g[np.arange(len(ytr)), ytr] -= 1; W -= 0.4 * g.T @ Xtr / len(ytr)
    return float(((Xte @ W.T).argmax(1) == yte).mean())
if __name__ == "__main__":
    rows = {t: {"A": round(probe_pos(t, 1), 4), "B": round(probe_pos(t, 2), 4)} for t in range(T)}
    for t in range(T): print("pos %2d: A=%.2f B=%.2f" % (t, rows[t]["A"], rows[t]["B"]))
    json.dump(rows, open("perpos_RESULT.json", "w"), indent=1)
