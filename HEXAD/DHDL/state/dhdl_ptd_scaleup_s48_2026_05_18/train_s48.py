#!/usr/bin/env python3
"""train_s48.py — RESEARCH.md §48 DH-DL + PTD-aux scale-up trainer.

§44 byte-equivalent trainer except corpus path (multi-§24-run scale-up
trace_corpus_s48.jsonl, 192,000 records, sha256 e34b45522b76e99e…).

Architecture (DESIGN_S38.md §2 carry, §44 byte-equal):
    shared trunk    : 14 -> 32   (ReLU)             — 480 params
    decision head   : 32 -> 16 -> 3   (softmax)     — 579 params
    PTD aux head    : 32 -> 16 -> 14  (linear MSE)  — 766 params
    total           : 1,825 params

Combined loss (§44 byte-equal):
    L = L_decision + λ_safety · L_safety + λ_ptd · L_ptd_nextstate

B-S48-3 LAMBDA-PTD-OFF-REDUCTION (CONNECTION-POINT, carries B-S44-2):
    λ_ptd = 0 ⇒ L = §44 DH-DL at same seed (PTD head zero-gradient).

from-scratch RANDOM seed-fixed 1337 (g_clm_from_scratch). $0 Mac CPU numpy.
80/20 STRATIFIED train/holdout split (§44 byte-equal rule).
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

import numpy as np

SEED = 1337
LABELS = ("CONTINUE_THINK", "EMIT_VOICE", "REMAIN_SILENT")
LABEL_IDX = {lab: i for i, lab in enumerate(LABELS)}
EMIT_IDX = LABEL_IDX["EMIT_VOICE"]

FEATURE_KEYS = (
    "f_relevance", "f_info_gap", "f_curiosity", "f_pain",
    "f_coherence", "f_originality", "f_balance", "f_dynamics",
    "psi_dir", "psi_entropy", "tension", "thinker_score",
    "seconds_since_last", "ratchet",
)
N_IN = len(FEATURE_KEYS)
H1, H2_DEC, N_OUT_DEC = 32, 16, 3
H2_PTD, N_OUT_PTD = 16, 14
LAMBDA_SAFETY = 0.5
LR = 0.10
EPOCHS = 120
BATCH = 256


def _load_corpus(path: Path):
    X, Y, S, T, P = [], [], [], [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        X.append([float(r[k]) for k in FEATURE_KEYS])
        Y.append(LABEL_IDX[r["decision_label"]])
        S.append(1.0 if r["safety_extended_ok"] else 0.0)
        T.append(int(r["trace_idx"]))
        P.append(int(r["step"]))
    return (np.asarray(X, dtype=np.float64),
            np.asarray(Y, dtype=np.int64),
            np.asarray(S, dtype=np.float64),
            np.asarray(T, dtype=np.int64),
            np.asarray(P, dtype=np.int64))


def _build_next_record_map(T, P):
    key_to_idx = {}
    for i in range(len(T)):
        key_to_idx[(int(T[i]), int(P[i]))] = i
    n = len(T)
    next_i = np.zeros(n, dtype=np.int64)
    mask = np.zeros(n, dtype=np.float64)
    for i in range(n):
        k_next = (int(T[i]), int(P[i]) + 1)
        if k_next in key_to_idx:
            next_i[i] = key_to_idx[k_next]
            mask[i] = 1.0
        else:
            next_i[i] = i
            mask[i] = 0.0
    return next_i, mask


def _stratified_split(Y, holdout_frac=0.2):
    train_idx, holdout_idx = [], []
    for lab in range(3):
        idx = np.where(Y == lab)[0]
        k = int(len(idx) * holdout_frac)
        holdout_idx.extend(idx[:k].tolist())
        train_idx.extend(idx[k:].tolist())
    return np.asarray(sorted(train_idx)), np.asarray(sorted(holdout_idx))


def _relu(z):
    return np.maximum(z, 0.0)


def _softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def train(corpus_path: Path, out_path: Path, lambda_ptd: float) -> dict:
    rng = np.random.RandomState(SEED)
    X, Y, S, T, P = _load_corpus(corpus_path)
    next_i, mask = _build_next_record_map(T, P)

    tr, ho = _stratified_split(Y, 0.2)
    in_train = np.zeros(len(Y), dtype=np.bool_)
    in_train[tr] = True
    valid_pair = mask.astype(np.bool_) & in_train[next_i]
    ptd_mask = valid_pair.astype(np.float64)

    Xtr, Ytr, Str = X[tr], Y[tr], S[tr]
    tr_arr = tr
    n = Xtr.shape[0]

    mean = Xtr.mean(axis=0)
    std = Xtr.std(axis=0)
    std[std == 0.0] = 1.0
    Xn = (Xtr - mean) / std
    X_next_n = (X[next_i[tr_arr]] - mean) / std
    pm_tr = ptd_mask[tr_arr]

    counts = np.array([(Ytr == c).sum() for c in range(3)], dtype=np.float64)
    total = counts.sum()
    cw = np.minimum(total / (3.0 * np.maximum(counts, 1.0)), 50.0)

    W1 = rng.randn(N_IN, H1) * math.sqrt(2.0 / N_IN)
    b1 = np.zeros(H1)
    Wd2 = rng.randn(H1, H2_DEC) * math.sqrt(2.0 / H1)
    bd2 = np.zeros(H2_DEC)
    Wd3 = rng.randn(H2_DEC, N_OUT_DEC) * math.sqrt(2.0 / H2_DEC)
    bd3 = np.zeros(N_OUT_DEC)
    Wp2 = rng.randn(H1, H2_PTD) * math.sqrt(2.0 / H1)
    bp2 = np.zeros(H2_PTD)
    Wp3 = rng.randn(H2_PTD, N_OUT_PTD) * math.sqrt(2.0 / H2_PTD)
    bp3 = np.zeros(N_OUT_PTD)

    train_loss_hist, dec_loss_hist, safe_loss_hist, ptd_loss_hist = [], [], [], []

    for epoch in range(EPOCHS):
        order = rng.permutation(n)
        epoch_loss = 0.0; epoch_dec = 0.0; epoch_safe = 0.0; epoch_ptd = 0.0
        nb = 0
        for bstart in range(0, n, BATCH):
            bidx = order[bstart:bstart + BATCH]
            xb = Xn[bidx]; yb = Ytr[bidx]; sb = Str[bidx]
            xnb = X_next_n[bidx]; pmb = pm_tr[bidx]
            B = xb.shape[0]

            # forward
            z1 = xb @ W1 + b1
            a1 = _relu(z1)
            zd2 = a1 @ Wd2 + bd2
            ad2 = _relu(zd2)
            zd3 = ad2 @ Wd3 + bd3
            p = _softmax(zd3)
            zp2 = a1 @ Wp2 + bp2
            ap2 = _relu(zp2)
            xhat = ap2 @ Wp3 + bp3

            # losses
            wb = cw[yb]
            py = p[np.arange(B), yb]
            l_dec = -(wb * np.log(np.clip(py, 1e-12, 1.0))).sum()
            p_emit = p[:, EMIT_IDX]
            l_safe = LAMBDA_SAFETY * ((1.0 - sb) * p_emit ** 2).sum()
            sq = (xhat - xnb) ** 2
            l_ptd_per = sq.mean(axis=1) * pmb
            l_ptd = lambda_ptd * l_ptd_per.sum()
            batch_loss = (l_dec + l_safe + l_ptd) / B
            epoch_loss += batch_loss
            epoch_dec += l_dec / B
            epoch_safe += l_safe / B
            epoch_ptd += l_ptd / B
            nb += 1

            # backward: decision head
            onehot = np.zeros((B, N_OUT_DEC))
            onehot[np.arange(B), yb] = 1.0
            dzd3 = wb[:, None] * (p - onehot)
            coeff = LAMBDA_SAFETY * 2.0 * p_emit * (1.0 - sb)
            ind = np.zeros(N_OUT_DEC); ind[EMIT_IDX] = 1.0
            dpemit_dz = p_emit[:, None] * (ind[None, :] - p)
            dzd3 = dzd3 + coeff[:, None] * dpemit_dz
            dzd3 /= B
            gWd3 = ad2.T @ dzd3
            gbd3 = dzd3.sum(axis=0)
            dad2 = dzd3 @ Wd3.T
            dzd2 = dad2 * (zd2 > 0.0)
            gWd2 = a1.T @ dzd2
            gbd2 = dzd2.sum(axis=0)
            da1_from_dec = dzd2 @ Wd2.T

            # backward: PTD aux head — gradient gated by lambda_ptd
            # (B-S48-3 connection-point: lambda_ptd=0 ⇒ PTD head contributes 0)
            dxhat = (lambda_ptd / N_OUT_PTD) * 2.0 * (xhat - xnb) * pmb[:, None] / B
            gWp3 = ap2.T @ dxhat
            gbp3 = dxhat.sum(axis=0)
            dap2 = dxhat @ Wp3.T
            dzp2 = dap2 * (zp2 > 0.0)
            gWp2 = a1.T @ dzp2
            gbp2 = dzp2.sum(axis=0)
            da1_from_ptd = dzp2 @ Wp2.T

            # shared trunk backprop sums both heads
            da1 = da1_from_dec + da1_from_ptd
            dz1 = da1 * (z1 > 0.0)
            gW1 = xb.T @ dz1
            gb1 = dz1.sum(axis=0)

            # SGD
            Wd3 -= LR * gWd3; bd3 -= LR * gbd3
            Wd2 -= LR * gWd2; bd2 -= LR * gbd2
            Wp3 -= LR * gWp3; bp3 -= LR * gbp3
            Wp2 -= LR * gWp2; bp2 -= LR * gbp2
            W1 -= LR * gW1; b1 -= LR * gb1

        train_loss_hist.append(epoch_loss / max(nb, 1))
        dec_loss_hist.append(epoch_dec / max(nb, 1))
        safe_loss_hist.append(epoch_safe / max(nb, 1))
        ptd_loss_hist.append(epoch_ptd / max(nb, 1))

    out = {
        "research_md_section": "§48",
        "trainer": "train_s48.py",
        "lambda_ptd": lambda_ptd,
        "lambda_safety": LAMBDA_SAFETY,
        "seed": SEED,
        "arch": {
            "shared_trunk": [N_IN, H1],
            "decision_head": [H1, H2_DEC, N_OUT_DEC],
            "ptd_aux_head": [H1, H2_PTD, N_OUT_PTD],
        },
        "lr": LR, "epochs": EPOCHS, "batch": BATCH,
        "n_train": int(n), "n_holdout": int(len(ho)),
        "n_ptd_valid_pairs_train": int(pm_tr.sum()),
        "train_class_counts": counts.astype(int).tolist(),
        "class_weights": cw.tolist(),
        "feature_keys": list(FEATURE_KEYS),
        "feature_mean": mean.tolist(),
        "feature_std": std.tolist(),
        "train_loss_first": float(train_loss_hist[0]),
        "train_loss_last": float(train_loss_hist[-1]),
        "decision_loss_first": float(dec_loss_hist[0]),
        "decision_loss_last": float(dec_loss_hist[-1]),
        "safety_loss_first": float(safe_loss_hist[0]),
        "safety_loss_last": float(safe_loss_hist[-1]),
        "ptd_loss_first": float(ptd_loss_hist[0]),
        "ptd_loss_last": float(ptd_loss_hist[-1]),
        "head": {
            "shared": {"W1": W1.tolist(), "b1": b1.tolist()},
            "decision": {
                "W2": Wd2.tolist(), "b2": bd2.tolist(),
                "W3": Wd3.tolist(), "b3": bd3.tolist(),
            },
            "ptd_aux": {
                "W2": Wp2.tolist(), "b2": bp2.tolist(),
                "W3": Wp3.tolist(), "b3": bp3.tolist(),
            },
        },
        "honest_note": (
            "§48 scale-up trainer on 4× §27 (192k records, 4 phase regimes). "
            "λ_ptd=0 ⇒ §44 DH-DL byte-equal (B-S48-3 connection-point). "
            "Still DISTILLATION not emergence (§38 §7 carry — decision label "
            "is the §24 hand-coded threshold, head learns that function)."
        ),
    }
    out_path.write_text(json.dumps(out, ensure_ascii=False))
    return out


def main() -> int:
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description="§48 DH-DL + PTD scale-up trainer")
    ap.add_argument("--corpus", type=Path, default=here / "trace_corpus_s48.jsonl")
    ap.add_argument("--lambda-ptd", type=float, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = train(args.corpus, args.out, args.lambda_ptd)
    print(json.dumps({
        "lambda_ptd": out["lambda_ptd"],
        "n_train": out["n_train"], "n_holdout": out["n_holdout"],
        "n_ptd_pairs": out["n_ptd_valid_pairs_train"],
        "train_loss_first": round(out["train_loss_first"], 5),
        "train_loss_last": round(out["train_loss_last"], 5),
        "decision_loss_last": round(out["decision_loss_last"], 5),
        "ptd_loss_last": round(out["ptd_loss_last"], 5),
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
