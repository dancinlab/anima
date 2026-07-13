"""A7 — does the model have a SENTIMENT AXIS at all? (the floor beneath the whole M1/M2 fork)

The O/C design forks on M1 (the CE never wrote atom→polarity) vs M2 (it wrote it, but only
generatively). H_9299 tried to settle that with a likelihood contrast and the probe failed its own
powered positive control. Before repairing that probe again, there is a cheaper and more basic
question underneath both branches:

    can the frozen 303M separate a POSITIVE review context from a NEGATIVE one, in its own
    representation, at all?

If it cannot, there is no sentiment axis for an atom to be written onto, M1 is true by default, and
every downstream design (inversion curriculum, abstention objective) is moot. If it can — and
strongly — then the axis exists, the atom→polarity link is specifically what is missing, and the
fork stays alive and worth measuring properly.

Note this is NOT the same question H_9297 answered. H_9297 asked whether a HELD-OUT ATOM's polarity
is decodable from the hidden state at the atom's own position. This asks whether a WHOLE REVIEW's
sentiment is decodable — a far easier task the corpus supervises on every line. A model that fails
even this has no sentiment representation whatsoever; a model that passes it has one, and the
atom-level absence becomes a statement about the atom→axis WRITE, not about the axis.

Data: real reviews, labelled by the corpus itself (naver rating ≤2 / ≥4, steam 0/1, NSMC 0/1).
Probe: the same L2-logreg on the same `--dump-hidden __last` representation H_9297 used, so a pass
here and a failure there cannot be blamed on different instruments.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = "/tmp/animaenv/bin/anima-py"
CKPT_DIR = os.path.expanduser("~/anima-weights/natem_n2")
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
WIN = int(__import__("sys").argv[1]) if len(__import__("sys").argv)>1 else 24
N_TRAIN, N_TEST = 400, 200      # reviews per split (balanced)
SEED = 7
L2 = 1e-3


def _sig(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def logreg(Xtr, ytr, Xte, iters=800, lr=0.1):
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    w, b = np.zeros(Xtr.shape[1]), 0.0
    for _ in range(iters):
        p = _sig(Xtr @ w + b)
        w -= lr * (Xtr.T @ (p - ytr) / len(ytr) + L2 * w)
        b -= lr * float((p - ytr).mean())
    return _sig(Xte @ w + b), _sig(Xtr @ w + b)


def main() -> int:
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "nbind_curriculum")))
    sys.path.insert(0, HERE)
    import gen_nbindg_n2 as GN2

    rng = np.random.default_rng(SEED)
    rows = GN2.load_corpora()
    pos = [t for t, l in rows if l == 1 and len(t.encode()) >= 40]
    neg = [t for t, l in rows if l == 0 and len(t.encode()) >= 40]
    rng.shuffle(pos); rng.shuffle(neg)
    k = (N_TRAIN + N_TEST) // 2
    texts = pos[:k] + neg[:k]
    labels = np.array([1] * k + [0] * k)
    idx = rng.permutation(len(texts))
    texts = [texts[i] for i in idx]
    labels = labels[idx]

    spec = os.path.join(HERE, "a7_prompts.json")
    json.dump({"items": [{"id": f"r{i}", "prompt": t[:120]} for i, t in enumerate(texts)]},
              open(spec, "w"), ensure_ascii=False)

    n_te = N_TEST
    sd = math.sqrt(0.25 / n_te)
    print(f"A7 — sentiment-axis floor · WIN = {WIN} BYTES (≈{WIN//3} 한글자) · {len(texts)} real reviews "
          f"({N_TRAIN} train / {N_TEST} test) · chance sd = {sd:.4f}")
    print("     can the frozen representation separate a POSITIVE review from a NEGATIVE one?\n")

    out = {"n_test": n_te, "chance_sd": sd, "arms": {}}
    for arm in ARMS:
        npz_path = os.path.join(HERE, f"a7_hidden_w{WIN}_{arm}.npz")
        if not os.path.exists(npz_path):
            subprocess.run([ANIMA, "evaluate", os.path.join(CKPT_DIR, f"natem_n2_{arm}.clm"),
                            "--dump-hidden", spec, "--out", npz_path, "--win", str(WIN)],
                           check=True, capture_output=True)
        npz = np.load(npz_path)
        X = np.stack([npz[f"r{i}__last"] for i in range(len(texts))]).astype(np.float64)
        Xtr, ytr = X[:N_TRAIN], labels[:N_TRAIN].astype(float)
        Xte, yte = X[N_TRAIN:], labels[N_TRAIN:]
        pte, ptr = logreg(Xtr, ytr, Xte)
        acc = float(((pte > 0.5) == yte).mean())
        fit = float(((ptr > 0.5) == ytr).mean())
        p1 = float(stats.binom.sf(int(((pte > 0.5) == yte).sum()) - 1, n_te, 0.5))
        out["arms"][arm] = {"test_acc": acc, "train_fit": fit, "sigma": (acc - 0.5) / sd,
                            "exact_p": p1}
        print(f"  {arm:>13} | review-sentiment acc {acc:.3f} ({(acc-0.5)/sd:+.1f}σ) "
              f"· train {fit:.2f} · p = {p1:.2e}")

    best = max(out["arms"][a]["test_acc"] for a in ARMS)
    print()
    if best >= 0.70:
        v = (f"✅ SENTIMENT AXIS EXISTS (best {best:.3f}) — the frozen 303M represents review "
             "sentiment perfectly well. So the axis is there, and what is missing is specifically "
             "the WRITE from a held-out ATOM onto it. M1 ('nothing was written') therefore means "
             "'the atom was not written onto an axis that demonstrably exists' — the fork stays "
             "live and the O/C design's premise holds.")
    elif best >= 0.58:
        v = (f"🟡 WEAK AXIS (best {best:.3f}) — sentiment is only partly represented. An atom→axis "
             "write would have little to write onto; report the effect size, do not conclude.")
    else:
        v = (f"🧱 NO SENTIMENT AXIS (best {best:.3f}) — the model cannot even tell a positive review "
             "from a negative one in its own representation. Then there is nothing for an atom's "
             "polarity to be written ONTO: M1 is true by construction, and the inversion curriculum "
             "and the abstention objective are BOTH moot. The recipe must first build the axis.")
    print(f"VERDICT: {v}")
    out["verdict"] = v
    json.dump(out, open(os.path.join(HERE, f"audit_a7_w{WIN}.json"), "w"), ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
