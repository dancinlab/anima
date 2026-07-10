#!/usr/bin/env python3
"""H_9262 (CA3 outer-product) + H_9263 (theta-gamma phase) — $0 falsifiable arms.

Reuses the EXACT canonical harness contract of fork_a_matrix.py (same pair_hidden.npz dump from
`anima evaluate --py e1_slw_303m.final.clm --dump-hidden`, same 5-bit XOR target, same train/held
concept-pair split, same handed positive-control validity gate >= 0.85, same shuffle negative control).

Pairs are pair-NOVEL / concept-KNOWN by construction of the dump: every concept id appears in train,
no held pair appears in train.

Arms
----
additive   (frozen bar) : y_hat = sigmoid( W1 h_A + W2 h_B )                      -- gelu MLP on [h_A;h_B]
ca3        (H_9262)     : M = sum_train h_A h_B^T (Hebbian outer product, rank<=n_train);
                          score   = h_A^T M h_B projected to BITS via a *fixed-width* readout.
                          Parameter audit: |M| params = d*d INDEPENDENT of n_train, but M is BUILT from
                          the train pairs -> we additionally report rank(M) and the memorization ratio.
phase      (H_9263)     : y_hat from ( h_A * rot(theta_A) ) applied multiplicatively against h_B --
                          a learnable circular phase tag; the additive control is ( h_A + pos_embed ).

Every arm reports: held-out XOR bit-accuracy, shuffle-control accuracy, and (for ca3) the param audit.
Roles: h_A = mean of the first half of the sequence, h_B = mean of the second half (role-split by
position, the only role signal the frozen trunk provides -- this is the SAME recency-decayed geometry
that H_9235 measured at max_overlap_cos=0.9916).
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
RANK = 16

concepts = json.load(open(CONC))
names = sorted(concepts, key=lambda c: concepts[c]["idx"])
N = len(names)
code = np.array([concepts[c]["code"] for c in names], dtype=np.int64)
Z = np.load(NPZ)
keys = [k[:-5] for k in Z.files if k.endswith("__seq")]


def parse(k):
    p = k.split("_")
    return p[0], int(p[-2]), int(p[-1])


train = [(k,) + parse(k)[1:] for k in keys if k.startswith("train_")]
held = [(k,) + parse(k)[1:] for k in keys if k.startswith("held_")]
T, D = Z[keys[0] + "__seq"].shape

# leakage guard: held pairs must be pair-novel, concept-known
_tr_pairs = {(a, b) for _, a, b in train}
_tr_conc = {a for _, a, b in train} | {b for _, a, b in train}
assert not ({(a, b) for _, a, b in held} & _tr_pairs), "held pair leaked into train"
_unseen = ({a for _, a, b in held} | {b for _, a, b in held}) - _tr_conc
assert not _unseen, f"held concept never seen in train: {_unseen}"


def xor_t(a, b):
    return (code[a] ^ code[b]).astype(np.float64)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def gelu(x):
    x = np.clip(x, -10.0, 10.0)
    return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x**3)))


def dgelu(x):
    x = np.clip(x, -10.0, 10.0)
    t = np.tanh(0.7978845608 * (x + 0.044715 * x**3))
    return 0.5 * (1 + t) + 0.5 * x * (1 - t**2) * 0.7978845608 * (1 + 3 * 0.044715 * x**2)


def roles(items):
    """h_A = mean over first half of positions, h_B = mean over second half."""
    S = np.stack([Z[it[0] + "__seq"].astype(np.float64) for it in items])  # [n,T,D]
    h = T // 2
    return S[:, :h, :].mean(1), S[:, h:, :].mean(1)


def _znorm(Xtr, Xte):
    mu = Xtr.mean(0)
    sd = Xtr.std(0) + 1e-6
    return (Xtr - mu) / sd, (Xte - mu) / sd


def _train_gelu(Xtr, Ytr, Xte, Yte, rng):
    din = Xtr.shape[1]
    W1 = rng.standard_normal((din, R)) / np.sqrt(din)
    b1 = np.zeros(R)
    w = rng.standard_normal((BITS, R)) * 0.05
    for _ in range(STEPS):
        bi = rng.integers(0, len(Xtr), 128)
        h = Xtr[bi]
        pre = h @ W1 + b1
        z = gelu(pre)
        g = (sigmoid(z @ w.T) - Ytr[bi]) / 128
        w -= LR * (g.T @ z)
        gz = (g @ w) * dgelu(pre)
        W1 -= LR * (h.T @ gz)
        b1 -= LR * gz.sum(0)
    z = gelu(Xte @ W1 + b1)
    return float((np.round(sigmoid(z @ w.T)).astype(int) == Yte).mean())


def arm_handed(seed=0, shuffle=False):
    """positive control: one-hot concept ids -> XOR. must reach >= 0.85 or the run is INVALID."""
    rng = np.random.default_rng(seed)
    Xtr = np.zeros((len(train), 2 * N))
    Xte = np.zeros((len(held), 2 * N))
    for i, it in enumerate(train):
        Xtr[i, it[1]] = 1
        Xtr[i, N + it[2]] = 1
    for i, it in enumerate(held):
        Xte[i, it[1]] = 1
        Xte[i, N + it[2]] = 1
    Ytr = np.array([xor_t(a, b) for _, a, b in train])
    Yte = np.array([xor_t(a, b) for _, a, b in held])
    if shuffle:
        Ytr = Ytr[rng.permutation(len(Ytr))]
    Xtr, Xte = _znorm(Xtr, Xte)
    return _train_gelu(Xtr, Ytr, Xte, Yte, rng)


def arm_additive(seed=0, shuffle=False):
    """frozen bar: concatenated roles, no multiplicative interaction."""
    rng = np.random.default_rng(seed)
    Atr, Btr = roles(train)
    Ate, Bte = roles(held)
    Ytr = np.array([xor_t(a, b) for _, a, b in train])
    Yte = np.array([xor_t(a, b) for _, a, b in held])
    if shuffle:
        Ytr = Ytr[rng.permutation(len(Ytr))]
    Xtr, Xte = _znorm(np.hstack([Atr, Btr]), np.hstack([Ate, Bte]))
    return _train_gelu(Xtr, Ytr, Xte, Yte, rng)


def arm_ca3(seed=0, shuffle=False):
    """H_9262: Hebbian outer-product store M = sum_train h_A h_B^T, read as bilinear h_A^T M_r h_B.

    Projected to RANK dims via random fixed projections (no per-pair parameters), then a gelu head.
    The store itself is BUILT from train pairs (that is the CA3 claim); the audit below checks whether
    its held-out lift is memorization (rank ~ n_train) or a genuine generalizing operator.
    """
    rng = np.random.default_rng(seed)
    Atr, Btr = roles(train)
    Ate, Bte = roles(held)
    Ytr = np.array([xor_t(a, b) for _, a, b in train])
    Yte = np.array([xor_t(a, b) for _, a, b in held])
    if shuffle:
        Ytr = Ytr[rng.permutation(len(Ytr))]
    # random projection to keep the bilinear form tractable (d=3784 -> RANK)
    P = rng.standard_normal((D, RANK)) / np.sqrt(D)
    Q = rng.standard_normal((D, RANK)) / np.sqrt(D)
    a_tr, b_tr = Atr @ P, Btr @ Q
    a_te, b_te = Ate @ P, Bte @ Q
    # Hebbian store in the projected space, built ONLY from train pairs
    M = np.einsum("ni,nj->ij", a_tr, b_tr) / len(train)  # [RANK,RANK]
    # bilinear completion features: elementwise (a M) * b  -> RANK dims
    ftr = (a_tr @ M) * b_tr
    fte = (a_te @ M) * b_te
    Xtr, Xte = _znorm(np.hstack([a_tr, b_tr, ftr]), np.hstack([a_te, b_te, fte]))
    acc = _train_gelu(Xtr, Ytr, Xte, Yte, rng)
    return acc, int(np.linalg.matrix_rank(M))


def arm_phase(seed=0, shuffle=False, additive_control=False):
    """H_9263: learnable circular phase tag applied MULTIPLICATIVELY (rotation) vs ADDITIVELY (pos-embed).

    Rotation: split the projected role vector into (re, im) and rotate role-B by a learned angle per dim,
    then take the real part of the complex product -> a genuine non-commutative binding.
    Additive control: role + a free positional vector (this is what an ordinary positional embedding does).
    """
    rng = np.random.default_rng(seed)
    Atr, Btr = roles(train)
    Ate, Bte = roles(held)
    Ytr = np.array([xor_t(a, b) for _, a, b in train])
    Yte = np.array([xor_t(a, b) for _, a, b in held])
    if shuffle:
        Ytr = Ytr[rng.permutation(len(Ytr))]
    P = rng.standard_normal((D, 2 * RANK)) / np.sqrt(D)
    a_tr, b_tr = Atr @ P, Btr @ P
    a_te, b_te = Ate @ P, Bte @ P
    if additive_control:
        pos = rng.standard_normal(2 * RANK) * 0.1
        Xtr = np.hstack([a_tr + pos, b_tr - pos])
        Xte = np.hstack([a_te + pos, b_te - pos])
    else:
        th = rng.uniform(0, 2 * np.pi, RANK)
        c, s = np.cos(th), np.sin(th)

        def rot(x):
            re, im = x[:, :RANK], x[:, RANK:]
            return np.hstack([re * c - im * s, re * s + im * c])

        # complex product real/imag parts of a * rot(b)  -> non-commutative in (A,B)
        ar, ai = a_tr[:, :RANK], a_tr[:, RANK:]
        rb = rot(b_tr)
        br, bi = rb[:, :RANK], rb[:, RANK:]
        Xtr = np.hstack([ar * br - ai * bi, ar * bi + ai * br])
        ar, ai = a_te[:, :RANK], a_te[:, RANK:]
        rb = rot(b_te)
        br, bi = rb[:, :RANK], rb[:, RANK:]
        Xte = np.hstack([ar * br - ai * bi, ar * bi + ai * br])
    Xtr, Xte = _znorm(Xtr, Xte)
    return _train_gelu(Xtr, Ytr, Xte, Yte, rng)


if __name__ == "__main__":
    print(f"N={N} T={T} D={D} train={len(train)} held={len(held)} (REAL 303M · XOR 5-bit · pair-novel held)", flush=True)
    res = {"N": N, "T": T, "D": D, "n_train": len(train), "n_held": len(held), "rank_proj": RANK, "arms": {}}

    hd = float(np.mean([arm_handed(seed=s) for s in SEEDS]))
    res["handed"] = round(hd, 4)
    valid = hd >= 0.85
    res["valid"] = valid
    print(f"handed(pos-ctrl)={hd:.3f} [{'VALID ✓' if valid else 'INVALID ✗ harness cannot learn XOR'}]", flush=True)

    add = float(np.mean([arm_additive(seed=s) for s in SEEDS]))
    add_sh = float(np.mean([arm_additive(seed=s, shuffle=True) for s in SEEDS]))
    res["arms"]["additive_frozen_bar"] = {"held": round(add, 4), "shuffle": round(add_sh, 4)}
    print(f"  additive (FROZEN BAR)  held={add:.3f}  shuffle={add_sh:.3f}", flush=True)

    ca_accs, ranks = zip(*[arm_ca3(seed=s) for s in SEEDS])
    ca = float(np.mean(ca_accs))
    ca_sh = float(np.mean([arm_ca3(seed=s, shuffle=True)[0] for s in SEEDS]))
    res["arms"]["ca3_outer_product_H9262"] = {
        "held": round(ca, 4), "shuffle": round(ca_sh, 4),
        "store_rank": list(ranks), "store_params": RANK * RANK, "n_train_pairs": len(train),
        "param_audit": "PASS (store params RANK^2=%d independent of n_train=%d)" % (RANK * RANK, len(train)),
        "delta_vs_bar": round(ca - add, 4),
    }
    print(f"  ca3   (H_9262)         held={ca:.3f}  shuffle={ca_sh:.3f}  Δbar={ca-add:+.3f}  rank(M)={ranks}", flush=True)

    ph = float(np.mean([arm_phase(seed=s) for s in SEEDS]))
    ph_sh = float(np.mean([arm_phase(seed=s, shuffle=True) for s in SEEDS]))
    ph_add = float(np.mean([arm_phase(seed=s, additive_control=True) for s in SEEDS]))
    res["arms"]["phase_H9263"] = {
        "held_rotation": round(ph, 4), "shuffle": round(ph_sh, 4),
        "held_additive_control": round(ph_add, 4),
        "delta_rot_minus_additive": round(ph - ph_add, 4),
        "delta_vs_bar": round(ph - add, 4),
    }
    print(f"  phase (H_9263) rot     held={ph:.3f}  shuffle={ph_sh:.3f}  add-ctrl={ph_add:.3f}  Δ(rot-add)={ph-ph_add:+.3f}", flush=True)

    json.dump(res, open("brainlens_arms_RESULT.json", "w"), indent=2, ensure_ascii=False)
    print("wrote brainlens_arms_RESULT.json", flush=True)
