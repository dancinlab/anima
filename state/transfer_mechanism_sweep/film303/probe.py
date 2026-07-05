#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G1 escape crux — mechanism-side vs target-side wall, on REAL 303M reps.

The transfer-mechanism sweep showed bilinear/multiplicative binding (FiLM/TPR/slot) EARNS
cross-distribution transfer on a SYNTHETIC bilinear target. F2 showed the real-corpus recombination
target is collocation-only (transfer 0). So: is the G1 wall MECHANISM-side (mechanisms can't bind) or
TARGET-side (the real 303M composition isn't a transferable bilinear form)?

This probe answers it on REAL 303M h1129 reps. Target = the 303M's OWN joint pair representation
h(a,b) (final-LN hidden of "a b"). Predictors = the two single reps h(a), h(b). Train a FiLM
(multiplicative, a proven transfer-earning mechanism) and an ADDITIVE baseline to predict h(a,b) from
[h(a),h(b)] on TRAIN concepts, TEST on DISJOINT held-out concepts (cross-distribution).
  - FiLM cross R² >> additive cross R²  => the 303M composes pairs as a TRANSFERABLE bilinear form
    => wall is MECHANISM-side (a bilinear readout escapes) => GPU-go on FiLM readout.
  - FiLM cross R² ~= additive              => the 303M pair-composition is additive/idiosyncratic (no
    transferable bilinear interaction) => wall is TARGET-side (matches §4 additive + F2 collocation);
    a better mechanism cannot help — escape needs authored transferable-form data.
py-canonical numpy (engine-native). Pool (summer 303M), never mini.
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decode as D
CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
VOCAB = os.path.join(HERE, "vocab.json")
N_CONCEPT = 140      # concepts to rep (single forwards)
N_TRAIN_PAIRS = 2200
N_TEST_PAIRS = 700
D_LOW = 64           # PCA-reduce reps to keep the trained heads well-posed

def rep(W, text):
    ids = list(text.encode("utf-8"))
    return np.asarray(D.bg_forward_last_hidden(W, ids, len(ids)), dtype=np.float64)

def pca_fit(X, k):
    mu = X.mean(0); Xc = X - mu
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    return mu, Vt[:k].T

def r2(pred, true):
    ss_res = np.sum((pred - true) ** 2); ss_tot = np.sum((true - true.mean(0)) ** 2)
    return 1.0 - ss_res / ss_tot

def train_head(feat, Y, lam=1.0):
    A = np.hstack([feat, np.ones((len(feat), 1))])
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ Y)

def apply_head(w, feat):
    return np.hstack([feat, np.ones((len(feat), 1))]) @ w

def main():
    vocab = json.load(open(VOCAB))
    if isinstance(vocab, dict): vocab = vocab.get("vocab", list(vocab.keys()))
    words = [w for w in vocab if w.isalpha()][:N_CONCEPT]
    print(f"[1/4] load 303M · {len(words)} single reps ...", flush=True)
    W = D.bg_load(CKPT)
    S = np.stack([rep(W, w) for w in words])                 # single reps [N, d]
    mu, P = pca_fit(S, D_LOW); Sl = (S - mu) @ P             # [N, D_LOW]

    rng = np.random.RandomState(20260705)
    n = len(words); tr_idx = np.arange(0, int(n * 0.7)); te_idx = np.arange(int(n * 0.7), n)  # DISJOINT concepts
    def samp(idx, k):
        out = []
        while len(out) < k:
            a, b = rng.choice(idx), rng.choice(idx)
            if a != b: out.append((a, b))
        return out
    trp, tep = samp(tr_idx, N_TRAIN_PAIRS), samp(te_idx, N_TEST_PAIRS)

    print(f"[2/4] joint reps: {len(trp)} train + {len(tep)} test pairs (303M forwards) ...", flush=True)
    def joint(pairs):
        return np.stack([(rep(W, words[a] + " " + words[b]) - mu) @ P for a, b in pairs])
    Ytr, Yte = joint(trp), joint(tep)                        # [P, D_LOW] target = 303M joint pair rep

    ha_tr = Sl[[a for a, b in trp]]; hb_tr = Sl[[b for a, b in trp]]
    ha_te = Sl[[a for a, b in tep]]; hb_te = Sl[[b for a, b in tep]]

    print("[3/4] ADDITIVE baseline: predict h(a,b) from [h(a),h(b)] ...", flush=True)
    add_tr = np.hstack([ha_tr, hb_tr]); add_te = np.hstack([ha_te, hb_te])
    wa = train_head(add_tr, Ytr); add_cross = r2(apply_head(wa, add_te), Yte)

    print("[4/4] FiLM: h(a) gates h(b) — gamma/beta(a) * h(b) ...", flush=True)
    # FiLM feature: element-wise product ha*hb (multiplicative bind) + ha + hb (so it can also be additive)
    film_tr = np.hstack([ha_tr * hb_tr, ha_tr, hb_tr]); film_te = np.hstack([ha_te * hb_te, ha_te, hb_te])
    wf = train_head(film_tr, Ytr); film_cross = r2(apply_head(wf, film_te), Yte)

    delta = film_cross - add_cross
    if delta >= 0.05:
        verdict = "MECHANISM-SIDE"; decision = ("FiLM(bilinear) beats additive on cross-distribution 303M "
            "pair-rep prediction -> the 303M composes pairs as a transferable bilinear form -> a bilinear "
            "readout escapes -> GPU-go on FiLM/slot readout.")
    else:
        verdict = "TARGET-SIDE"; decision = ("FiLM ~= additive on cross-distribution -> the 303M pair-"
            "composition carries NO transferable bilinear interaction beyond additive (matches §4 + F2 "
            "collocation) -> the G1 wall is TARGET/DATA-side, not mechanism-capacity; a better mechanism "
            "cannot help. Escape needs authored transferable-form data.")
    out = {"probe": "G1 escape crux — FiLM vs additive on real 303M joint pair-rep, cross-distribution",
           "n_concept": len(words), "d_low": D_LOW, "n_train_pairs": len(trp), "n_test_pairs": len(tep),
           "additive_cross_r2": round(float(add_cross), 4), "film_cross_r2": round(float(film_cross), 4),
           "delta_film_minus_additive": round(float(delta), 4), "verdict": verdict, "decision": decision}
    json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), ensure_ascii=False, indent=1)
    print(f"    additive_cross={add_cross:.4f} film_cross={film_cross:.4f} delta={delta:+.4f} -> {verdict}", flush=True)

if __name__ == "__main__":
    main()
