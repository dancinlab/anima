#!/usr/bin/env python3
"""H_9235 fork-A '모든 경우의 수' — REAL-303M mechanism matrix (numpy · torch-free · pair_hidden.npz).

The definitive (engine-native, a_eval_py_canonical) counterpart of synth_mechanism_matrix.py: runs the
SAME pool×head decomposition on the REAL 303M per-position hiddens the precheck used. fork_a_precheck.py
established mean+gelu=0.98 / last+gelu=0.47 / mean+linear=0.43 / handed=1.0 / shuffle=0.50. This adds the
un-measured arms so we know WHICH read-side mechanism is load-bearing before spending GPU on training:

  pool ∈ {mean, query-addressed, last, max}   head ∈ {gelu-bias(clml), hadamard-bind(RETRO-ROUTE), linear}

INPUT: pair_hidden.npz (train_/held_ *__seq per-position [T,d]) + concepts.json — the SAME artifacts the
$0 precheck consumed (dump: `anima evaluate --py <e1_slw_303m.clm> --dump-hidden pair_prompts.json --out
pair_hidden.npz --win 24` on a clean pool host). INFRA-GATED only on that dump (summer overloaded / aiden
lacks the ckpt / rent=go); the code is ready. VALIDITY: handed arm (one-hot ids→gelu) must reach ≥0.85 or
the run is INVALID (convergence rung-b-analyze-py-1 gate). $0 numpy once hiddens are cached.
"""
import json
import sys
import numpy as np

NPZ = sys.argv[1] if len(sys.argv) > 1 else "pair_hidden.npz"
CONC = sys.argv[2] if len(sys.argv) > 2 else "concepts.json"
BITS = 5
R = 128
STEPS = 4000
LR = 0.05
SEEDS = (0, 1, 2)

concepts = json.load(open(CONC))
names = sorted(concepts, key=lambda c: concepts[c]["idx"])
N = len(names)
code = np.array([concepts[c]["code"] for c in names], dtype=np.float64)
Z = np.load(NPZ)
keys = [k[:-5] for k in Z.files if k.endswith("__seq")]


def parse(k):
    p = k.split("_")
    return p[0], int(p[-2]), int(p[-1])


train = [(k,) + parse(k)[1:] for k in keys if k.startswith("train_")]
held = [(k,) + parse(k)[1:] for k in keys if k.startswith("held_")]
T, D = Z[keys[0] + "__seq"].shape


def xor_t(a, b):
    return (code[a].astype(int) ^ code[b].astype(int)).astype(np.float64)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x**3)))


def dgelu(x):
    t = np.tanh(0.7978845608 * (x + 0.044715 * x**3))
    return 0.5 * (1 + t) + 0.5 * x * (1 - t**2) * 0.7978845608 * (1 + 3 * 0.044715 * x**2)


def seqs(items):
    return np.stack([Z[it[0] + "__seq"].astype(np.float64) for it in items])   # [n,T,D]


def pool_rep(S, kind, p):
    gen = S[:, T - 1, :]
    if kind == "mean":
        return S.mean(1)
    if kind == "max":
        return S.max(1)
    if kind == "last":
        return gen
    if kind == "query":
        q = gen @ p["Wq"]; K = S @ p["Wk"]
        sc = np.einsum("nk,ntk->nt", q, K) / np.sqrt(p["Wq"].shape[1])
        sc = sc - sc.max(1, keepdims=True)
        a = np.exp(sc); a = a / a.sum(1, keepdims=True)
        return np.einsum("nt,ntd->nd", a, S)
    raise ValueError(kind)


def run_arm(pool_kind, head_kind, handed=False, shuffle=False, seed=0):
    rng = np.random.default_rng(seed)
    Str, Ste = seqs(train), seqs(held)
    Ytr = np.array([xor_t(it[1], it[2]) for it in train]); Yte = np.array([xor_t(it[1], it[2]) for it in held])
    if shuffle:
        Ytr = Ytr[rng.permutation(len(Ytr))]
    k = 64
    p = {"Wq": rng.standard_normal((D, k)) / np.sqrt(D), "Wk": rng.standard_normal((D, k)) / np.sqrt(D)}

    def feat(S, items):
        if handed:
            X = np.zeros((len(items), 2 * N))
            for i, it in enumerate(items):
                X[i, it[1]] = 1; X[i, N + it[2]] = 1
            return X
        return pool_rep(S, pool_kind, p)
    Xtr = feat(Str, train); Gtr = Str[:, T - 1, :]
    Xte = feat(Ste, held); Gte = Ste[:, T - 1, :]
    mu = Xtr.mean(0); sd = Xtr.std(0) + 1e-6
    Xtr = (Xtr - mu) / sd; Xte = (Xte - mu) / sd
    gmu = Gtr.mean(0); gsd = Gtr.std(0) + 1e-6
    Gtr = (Gtr - gmu) / gsd; Gte = (Gte - gmu) / gsd
    din = Xtr.shape[1]

    if head_kind == "linear":
        W = rng.standard_normal((BITS, din)) * 0.05
        for _ in range(STEPS):
            bi = rng.integers(0, len(Xtr), 128); h = Xtr[bi]
            g = (sigmoid(h @ W.T) - Ytr[bi]) / 128; W -= LR * (g.T @ h)
        return float((np.round(sigmoid(Xte @ W.T)).astype(int) == Yte).mean())

    W1 = rng.standard_normal((din, R)) / np.sqrt(din); b1 = np.zeros(R)
    Wu = rng.standard_normal((D, R)) / np.sqrt(D)
    w = rng.standard_normal((BITS, R)) * 0.05
    for _ in range(STEPS):
        bi = rng.integers(0, len(Xtr), 128); h = Xtr[bi]; G = Gtr[bi]
        pre = h @ W1 + b1; z = gelu(pre)
        if head_kind == "hadamard" and not handed:
            u = G @ Wu; zb = z * u; pr = sigmoid(zb @ w.T)
            g = (pr - Ytr[bi]) / 128; w -= LR * (g.T @ zb); gzb = g @ w
            gz = gzb * u * dgelu(pre); W1 -= LR * (h.T @ gz); b1 -= LR * gz.sum(0)
            Wu -= LR * (G.T @ (gzb * z))
        else:
            pr = sigmoid(z @ w.T); g = (pr - Ytr[bi]) / 128
            w -= LR * (g.T @ z); gz = (g @ w) * dgelu(pre)
            W1 -= LR * (h.T @ gz); b1 -= LR * gz.sum(0)
    pre = Xte @ W1 + b1; z = gelu(pre)
    if head_kind == "hadamard" and not handed:
        z = z * (Gte @ Wu)
    return float((np.round(sigmoid(z @ w.T)).astype(int) == Yte).mean())


if __name__ == "__main__":
    print("N=%d T=%d D=%d train=%d held=%d (REAL 303M · XOR 5-bit)" % (N, T, D, len(train), len(held)), flush=True)
    res = {"N": N, "T": T, "D": D, "cells": {}}
    hd = round(float(np.mean([run_arm("mean", "gelu", handed=True, seed=s) for s in SEEDS])), 4)
    sh = round(float(np.mean([run_arm("mean", "gelu", shuffle=True, seed=s) for s in SEEDS])), 4)
    res["handed"] = hd; res["shuffle"] = sh
    valid = "VALID ✓" if hd >= 0.85 else "INVALID ✗ (harness can't learn XOR)"
    print(f"handed(pos-ctrl)={hd:.3f} [{valid}]  shuffle={sh:.3f}", flush=True)
    for pk in ("mean", "query", "last", "max"):
        for hk in ("gelu", "hadamard", "linear"):
            v = round(float(np.mean([run_arm(pk, hk, seed=s) for s in SEEDS])), 4)
            res["cells"][f"{pk}.{hk}"] = v
            print(f"  {pk:>6}+{hk:<9} heldout_XOR={v:.3f}", flush=True)
    json.dump(res, open("fork_a_matrix_RESULT.json", "w"), indent=2, ensure_ascii=False)
    print("wrote fork_a_matrix_RESULT.json", flush=True)
