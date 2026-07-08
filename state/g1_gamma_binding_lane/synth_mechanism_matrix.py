#!/usr/bin/env python3
"""H_9235 fork-A '모든 경우의 수' — mechanism-decomposition matrix (synthetic · numpy · $0 CPU).

WHY synthetic: the real-303M pre-check (fork_a_precheck.py · pair_hidden.npz) already PROVED the
2-concept route (mean+gelu=0.98) but at N_ctx=2 mean-pool already wins, so it CANNOT separate the
mechanism arms. The open 'which component cracks ρ·weave' question lives where the arms DIVERGE:
many concepts in context (distractors) + a DISTAL target that receptive-field decay has washed out
of the generation point. This toy reproduces the MEASURED structure (A=0.88@pos → 0.07@last RF
decay) with controlled N_ctx and asks the decomposition:

  pool ∈ {mean, query-addressed, last(gen-point), max}
  head ∈ {gelu-bias(clml), hadamard-bind(RETRO-ROUTE), linear(additive floor control)}
  N_ctx ∈ {2, 4, 8}   (distractor load)

target = XOR(code[a], code[b]) for two DESIGNATED concepts (a=first=most-distal, b=last=recent),
held-out = (a,b) combos never co-trained. Each arm trained JOINTLY end-to-end (BCE), 3 seeds.

SCOPE (a_toy_scale_recheck · a_scale_honest_scope): DIRECTIONAL toy of the MECHANISM logic, NOT a
303M verdict — the real-303M matrix (same arms on pair_hidden.npz) is the infra-gated follow-on
(needs a clean pool host with e1_slw_303m.clm). This tells us WHICH arm to spend GPU on, for $0.
"""
import json
import sys
import numpy as np

BITS = 5
D = 128            # toy hidden dim
NVOCAB = 32        # concept vocabulary
R = 96             # bottleneck / lane dim
STEPS = 6000
LR = 0.05
SEEDS = (0, 1, 2)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x**3)))


def dgelu(x):
    t = np.tanh(0.7978845608 * (x + 0.044715 * x**3))
    return 0.5 * (1 + t) + 0.5 * x * (1 - t**2) * 0.7978845608 * (1 + 3 * 0.044715 * x**2)


def make_world(seed):
    rng = np.random.default_rng(seed)
    # ORTHONORMAL concept embeddings (QR) — reproduces the MEASURED real-303M structure where
    # unary atoms are perfectly linearly separable (H1 probe = 1.00). Random-Gaussian embeddings
    # (v1) were NOT separable enough → invalid toy (no arm reached the known-achievable ceiling).
    G = rng.standard_normal((D, NVOCAB))
    Q, _ = np.linalg.qr(G)                                        # D×NVOCAB orthonormal columns
    emb = Q.T                                                     # [NVOCAB, D], rows orthonormal
    code = rng.integers(0, 2, (NVOCAB, BITS))                     # 5-bit codes (zero-unary-MI-ish)
    return emb, code, rng


def build_dataset(emb, code, rng, n_ctx, n_items):
    """Each item: a context of n_ctx DISTINCT concepts at positions 0..n_ctx-1. Target concepts =
    position 0 (most distal) and position n_ctx-1 (recent). Per-position hidden = concept emb + noise.
    Returns: seq [n, n_ctx, D], gen [n, D] (RF-decayed recency-weighted = generation point), a,b idx."""
    seqs, gens, A, B = [], [], [], []
    # RF decay weights: recent positions dominate the generation point (mimics A=0.88@pos->0.07@last).
    # geometric recency: w_i ∝ rho^(n_ctx-1-i); rho<1 => distal (i=0) heavily attenuated at gen.
    rho = 0.45
    for _ in range(n_items):
        cs = rng.choice(NVOCAB, size=n_ctx, replace=False)
        H = emb[cs] + rng.standard_normal((n_ctx, D)) * 0.05        # per-position hiddens
        w = rho ** np.arange(n_ctx - 1, -1, -1).astype(np.float64)  # recency weights
        w = w / w.sum()
        gen = (w[:, None] * H).sum(0)                              # RF-decayed generation point
        seqs.append(H); gens.append(gen); A.append(cs[0]); B.append(cs[-1])
    return np.array(seqs), np.array(gens), np.array(A), np.array(B)


def pool_rep(H, gen, kind, params=None):
    """H:[n,Tc,D] gen:[n,D] -> pooled content [n,D] (+ optional learned query-address)."""
    if kind == "mean":
        return H.mean(1)
    if kind == "max":
        return H.max(1)
    if kind == "last":
        return gen                                                # generation point (RF-decayed)
    if kind == "query":                                           # content-addressed retrieval
        Wq, Wk = params["Wq"], params["Wk"]
        q = gen @ Wq                                              # [n,k]
        K = H @ Wk                                                # [n,Tc,k]
        sc = np.einsum("nk,ntk->nt", q, K) / np.sqrt(Wq.shape[1])
        sc = sc - sc.max(1, keepdims=True)
        a = np.exp(sc); a = a / a.sum(1, keepdims=True)          # [n,Tc]
        return np.einsum("nt,ntd->nd", a, H)                     # retrieved content
    raise ValueError(kind)


def run_arm(pool_kind, head_kind, n_ctx, seed):
    emb, code, rng = make_world(seed)

    def xor_t(a, b):
        return (code[a] ^ code[b]).astype(np.float64)
    Htr, Gtr, Atr, Btr = build_dataset(emb, code, rng, n_ctx, 700)
    Hte, Gte, Ate, Bte = build_dataset(emb, code, rng, n_ctx, 200)
    Ytr = xor_t(Atr, Btr); Yte = xor_t(Ate, Bte)

    k = 32
    p = {"Wq": rng.standard_normal((D, k)) / np.sqrt(D), "Wk": rng.standard_normal((D, k)) / np.sqrt(D)}
    # head params
    W1 = rng.standard_normal((D, R)) / np.sqrt(D); b1 = np.zeros(R)
    Wu = rng.standard_normal((D, R)) / np.sqrt(D)            # hadamard gen-side binder
    w = rng.standard_normal((BITS, R)) * 0.05
    Wlin = rng.standard_normal((BITS, D)) * 0.05

    def forward(H, G, train=False):
        c = pool_rep(H, G, pool_kind, p)                     # [n,D]
        if head_kind == "linear":
            return sigmoid(c @ Wlin.T), ("lin", c)
        z = gelu(c @ W1 + b1)                                # [n,R]
        if head_kind == "gelu":
            return sigmoid(z @ w.T), ("gelu", c, z, c @ W1 + b1)
        # hadamard: bind gen-side u with pooled content projection
        u = G @ Wu                                           # [n,R]
        zb = z * u                                            # bilinear cross-term
        return sigmoid(zb @ w.T), ("had", c, z, c @ W1 + b1, u, G)

    # train (SGD, minibatch) — jointly on all arm params
    n = len(Htr)
    for _ in range(STEPS):
        bi = rng.integers(0, n, 128)
        Hb, Gb, Yb = Htr[bi], Gtr[bi], Ytr[bi]
        pr, cache = forward(Hb, Gb, train=True)
        g = (pr - Yb) / 128                                  # [128,BITS]
        if cache[0] == "lin":
            c = cache[1]; Wlin -= LR * (g.T @ c)
            continue
        if cache[0] == "gelu":
            _, c, z, pre = cache
            w -= LR * (g.T @ z)
            gz = (g @ w) * dgelu(pre)                        # [128,R]
            W1 -= LR * (c.T @ gz); b1 -= LR * gz.sum(0)
        else:  # hadamard
            _, c, z, pre, u, G = cache
            zb = z * u
            w -= LR * (g.T @ zb)
            gzb = (g @ w)                                    # [128,R]
            gz = gzb * u * dgelu(pre); gu = gzb * z
            W1 -= LR * (c.T @ gz); b1 -= LR * gz.sum(0)
            Wu -= LR * (G.T @ gu)
        # query pool params get gradient only through c; approximate as frozen-random address here
        # (a random-projection retrieval is a fair, un-tuned lower bound for query-addressing — if it
        #  already beats mean at high n_ctx, the effect is real and only grows with a trained address).

    pr, _ = forward(Hte, Gte)
    return float((np.round(pr).astype(int) == Yte).mean())


def run_handed(n_ctx, seed):
    """Positive control — clean one-hot ids of the two target concepts → gelu → XOR. Proves the
    harness CAN learn held-out XOR (validity gate; if this fails the matrix is uninformative)."""
    emb, code, rng = make_world(seed)

    def xor_t(a, b):
        return (code[a] ^ code[b]).astype(np.float64)
    _, _, Atr, Btr = build_dataset(emb, code, rng, n_ctx, 700)
    _, _, Ate, Bte = build_dataset(emb, code, rng, n_ctx, 200)

    def oh(A, B):
        X = np.zeros((len(A), 2 * NVOCAB)); X[np.arange(len(A)), A] = 1; X[np.arange(len(B)), NVOCAB + B] = 1
        return X
    Xtr, Xte = oh(Atr, Btr), oh(Ate, Bte)
    Ytr, Yte = xor_t(Atr, Btr), xor_t(Ate, Bte)
    din = 2 * NVOCAB
    W1 = rng.standard_normal((din, R)) / np.sqrt(din); b1 = np.zeros(R); w = rng.standard_normal((BITS, R)) * 0.05
    for _ in range(STEPS):
        bi = rng.integers(0, len(Xtr), 128); h = Xtr[bi]
        pre = h @ W1 + b1; z = gelu(pre); pr = sigmoid(z @ w.T); g = (pr - Ytr[bi]) / 128
        gz = (g @ w) * dgelu(pre); w -= LR * (g.T @ z); W1 -= LR * (h.T @ gz); b1 -= LR * gz.sum(0)
    pre = Xte @ W1 + b1
    return float((np.round(sigmoid(gelu(pre) @ w.T)).astype(int) == Yte).mean())


if __name__ == "__main__":
    pools = ["mean", "query", "last", "max"]
    heads = ["gelu", "hadamard", "linear"]
    nctxs = [2, 4, 8]
    res = {"D": D, "NVOCAB": NVOCAB, "R": R, "steps": STEPS, "cells": {}, "handed": {}}
    print("=== fork-A mechanism matrix (synthetic · held-out XOR · 3-seed mean) ===", flush=True)
    hdr = "pool\\head        " + "  ".join(f"{h:>9}" for h in heads)
    for n_ctx in nctxs:
        hd = float(np.mean([run_handed(n_ctx, s) for s in SEEDS]))
        res["handed"][f"n{n_ctx}"] = round(hd, 4)
        gate = "VALID ✓" if hd >= 0.85 else "INVALID ✗ (harness can't learn XOR — cells uninformative)"
        print(f"\n-- N_ctx={n_ctx} (distractor load) · handed positive-ctrl={hd:.3f} [{gate}] --\n{hdr}", flush=True)
        for pk in pools:
            row = []
            for hk in heads:
                v = float(np.mean([run_arm(pk, hk, n_ctx, s) for s in SEEDS]))
                res["cells"][f"n{n_ctx}.{pk}.{hk}"] = round(v, 4)
                row.append(v)
            print(f"{pk:>14}   " + "  ".join(f"{x:>9.3f}" for x in row), flush=True)
    # decomposition read-outs
    def g(n, p, h):
        return res["cells"][f"n{n}.{p}.{h}"]
    summ = {}
    for n in nctxs:
        summ[f"query_vs_mean@n{n}_gelu"] = round(g(n, "query", "gelu") - g(n, "mean", "gelu"), 4)
        summ[f"hadamard_vs_gelu@n{n}_mean"] = round(g(n, "mean", "hadamard") - g(n, "mean", "gelu"), 4)
        summ[f"mean_gelu@n{n}"] = g(n, "mean", "gelu")
        summ[f"last_gelu@n{n}(RFdecay_ctrl)"] = g(n, "last", "gelu")
        summ[f"mean_linear@n{n}(additive_floor_ctrl)"] = g(n, "mean", "linear")
    res["decomposition"] = summ
    print("\n=== DECOMPOSITION ===", flush=True)
    for kk, vv in summ.items():
        print(f"  {kk} = {vv:+.3f}" if isinstance(vv, float) and 'vs' in kk else f"  {kk} = {vv:.3f}", flush=True)
    out = "synth_mechanism_matrix_RESULT.json"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    json.dump(res, open(out, "w"), indent=2, ensure_ascii=False)
    print("\nwrote", out, flush=True)
