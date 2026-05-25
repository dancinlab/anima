#!/usr/bin/env python3
"""train_dhdl.py — RESEARCH.md §27 DH-DL 3-class decision-head trainer.

Standalone thin MLP (14 -> 32 -> 16 -> 3) trained on the §27 trace corpus.
$0 Mac CPU — numpy-vectorized MLP with EXPLICIT hand-coded analytic backprop
(NO torch, NO autograd, NO GPU). numpy vectorizes the matrix ops; the backprop
is still written out by hand so the gradient path is auditable. The head has
~700 params; a standalone thin MLP is adequate (DESIGN_DHDL.md §2 — the head
consumes only physics features, no live Engine A hidden tensor, no GPU needed).

Dual loss (DESIGN_DHDL.md §3):
  L = L_decision + lambda * L_safety
  L_decision = class-weighted categorical cross-entropy (B-DHDL-3 Shannon CE>=0)
  L_safety   = lambda * (1 - safety_extended_ok) * p[EMIT_VOICE]^2  (B-DHDL-3)

from-scratch RANDOM seed-fixed 1337 (g_clm_from_scratch).
80/20 STRATIFIED train/holdout split.

Output: dhdl_head.json (trained weights + train metadata).
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
H1, H2, N_OUT = 32, 16, 3
LAMBDA_SAFETY = 0.5
LR = 0.10
EPOCHS = 120
BATCH = 256


def _load_corpus(path: Path):
    X, Y, S = [], [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        X.append([float(r[k]) for k in FEATURE_KEYS])
        Y.append(LABEL_IDX[r["decision_label"]])
        S.append(1.0 if r["safety_extended_ok"] else 0.0)
    return (np.asarray(X, dtype=np.float64),
            np.asarray(Y, dtype=np.int64),
            np.asarray(S, dtype=np.float64))


def _stratified_split(Y, holdout_frac=0.2):
    """Stratified by label — each split keeps the same class proportions.
    Deterministic (first k of each class -> holdout)."""
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


def train(corpus_path: Path, out_path: Path) -> dict:
    rng = np.random.RandomState(SEED)        # g_clm_from_scratch seed-fixed
    X, Y, S = _load_corpus(corpus_path)

    tr, ho = _stratified_split(Y, 0.2)
    Xtr, Ytr, Str = X[tr], Y[tr], S[tr]

    # input standardization — mean/std from TRAIN only
    mean = Xtr.mean(axis=0)
    std = Xtr.std(axis=0)
    std[std == 0.0] = 1.0
    Xn = (Xtr - mean) / std

    # class weights (inverse-frequency, clamped) — counters 96% REMAIN_SILENT
    counts = np.array([(Ytr == c).sum() for c in range(3)], dtype=np.float64)
    total = counts.sum()
    cw = np.minimum(total / (3.0 * np.maximum(counts, 1.0)), 50.0)

    # He init (ReLU) from-scratch RANDOM seed-fixed 1337
    W1 = rng.randn(N_IN, H1) * math.sqrt(2.0 / N_IN)
    b1 = np.zeros(H1)
    W2 = rng.randn(H1, H2) * math.sqrt(2.0 / H1)
    b2 = np.zeros(H2)
    W3 = rng.randn(H2, N_OUT) * math.sqrt(2.0 / H2)
    b3 = np.zeros(N_OUT)

    n = Xn.shape[0]
    loss_hist = []

    for epoch in range(EPOCHS):
        order = rng.permutation(n)
        epoch_loss = 0.0
        nb = 0
        for bstart in range(0, n, BATCH):
            bidx = order[bstart:bstart + BATCH]
            xb = Xn[bidx]                       # (B, N_IN)
            yb = Ytr[bidx]                      # (B,)
            sb = Str[bidx]                      # (B,)
            B = xb.shape[0]

            # ── forward ──────────────────────────────────────────────
            z1 = xb @ W1 + b1
            a1 = _relu(z1)
            z2 = a1 @ W2 + b2
            a2 = _relu(z2)
            z3 = a2 @ W3 + b3
            p = _softmax(z3)                    # (B, 3)

            # ── dual loss ────────────────────────────────────────────
            wb = cw[yb]                                    # (B,)
            py = p[np.arange(B), yb]                       # (B,)
            l_dec = -(wb * np.log(np.clip(py, 1e-12, 1.0))).sum()
            p_emit = p[:, EMIT_IDX]
            l_safe = LAMBDA_SAFETY * ((1.0 - sb) * p_emit ** 2).sum()
            batch_loss = (l_dec + l_safe) / B
            epoch_loss += batch_loss
            nb += 1

            # ── backward (explicit hand-coded) ───────────────────────
            # decision CE: dL_dec/dz3 = w * (p - onehot)
            onehot = np.zeros((B, N_OUT))
            onehot[np.arange(B), yb] = 1.0
            dz3 = wb[:, None] * (p - onehot)               # (B,3)
            # safety term: L_safe = lam*(1-s)*p_emit^2
            #   dL_safe/dp_emit = lam*(1-s)*2*p_emit
            #   dp_k/dz3_j = p_k*(1[k=j]-p_j); only k=emit matters
            #   dL_safe/dz3_j = (dL_safe/dp_emit) * p_emit*(1[j=emit]-p_j)
            coeff = LAMBDA_SAFETY * 2.0 * p_emit * (1.0 - sb)   # (B,)
            ind = np.zeros(N_OUT); ind[EMIT_IDX] = 1.0
            dpemit_dz = p_emit[:, None] * (ind[None, :] - p)    # (B,3)
            dz3 = dz3 + coeff[:, None] * dpemit_dz
            dz3 /= B                                        # mean-grad

            gW3 = a2.T @ dz3
            gb3 = dz3.sum(axis=0)
            da2 = dz3 @ W3.T
            dz2 = da2 * (z2 > 0.0)
            gW2 = a1.T @ dz2
            gb2 = dz2.sum(axis=0)
            da1 = dz2 @ W2.T
            dz1 = da1 * (z1 > 0.0)
            gW1 = xb.T @ dz1
            gb1 = dz1.sum(axis=0)

            # ── SGD update ───────────────────────────────────────────
            W3 -= LR * gW3; b3 -= LR * gb3
            W2 -= LR * gW2; b2 -= LR * gb2
            W1 -= LR * gW1; b1 -= LR * gb1

        loss_hist.append(epoch_loss / max(nb, 1))

    out = {
        "research_md_section": "§27",
        "trainer": "train_dhdl.py",
        "seed": SEED,
        "arch": [N_IN, H1, H2, N_OUT],
        "lambda_safety": LAMBDA_SAFETY,
        "lr": LR, "epochs": EPOCHS, "batch": BATCH,
        "n_train": int(n), "n_holdout": int(len(ho)),
        "train_class_counts": counts.astype(int).tolist(),
        "class_weights": cw.tolist(),
        "feature_keys": list(FEATURE_KEYS),
        "feature_mean": mean.tolist(),
        "feature_std": std.tolist(),
        "train_loss_first": float(loss_hist[0]),
        "train_loss_last": float(loss_hist[-1]),
        "train_loss_hist": [float(x) for x in loss_hist],
        "head": {
            "arch": [N_IN, H1, H2, N_OUT],
            "W1": W1.tolist(), "b1": b1.tolist(),
            "W2": W2.tolist(), "b2": b2.tolist(),
            "W3": W3.tolist(), "b3": b3.tolist(),
        },
        "honest_note": (
            "Trained head approximates the §24 talker_should_emit decision "
            "function. High accuracy = capability (function approximation), "
            "NOT emergence. See eval_dhdl.py threshold-distillation gap probe."
        ),
    }
    out_path.write_text(json.dumps(out, ensure_ascii=False))
    return out


def main() -> int:
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description="§27 DH-DL decision-head trainer")
    ap.add_argument("--corpus", type=Path, default=here / "trace_corpus.jsonl")
    ap.add_argument("--out", type=Path, default=here / "dhdl_head.json")
    args = ap.parse_args()
    out = train(args.corpus, args.out)
    print(json.dumps({
        "n_train": out["n_train"], "n_holdout": out["n_holdout"],
        "train_loss_first": round(out["train_loss_first"], 5),
        "train_loss_last": round(out["train_loss_last"], 5),
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
