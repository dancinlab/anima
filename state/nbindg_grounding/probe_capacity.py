"""H_9296 — is H_9289's INFO-ABSENT a fact about the REPRESENTATION, or about the PROBE?

The frontier's whole next move rests on this. H_9291 proved the information IS there: an ideal
reader, given byte-identical left-context to what the 303M saw, recovers all 29 held-out atoms'
polarity (29/29, shuffle control 0.517). H_9289 then found the 303M's frozen representation does
NOT yield it (probe acc 0.5517 ≈ chance, bar 0.65) and concluded INFO-ABSENT — which is what
relocated the wall to the "extraction channel" and made O/C-channel design the next frontier move.

But H_9289's G-PROBE made two choices that are not the representation's fault if they are wrong:
  1. it is LINEAR (L2-logreg), and
  2. it MEAN-POOLS an atom's 24 contexts into one vector before asking.
"The 303M did not encode polarity" and "it is not readable linearly, after averaging 24 contexts"
are different claims. The oracle, note, read each context SEPARATELY.

So: hold everything from H_9289 fixed — same frozen 4-arm checkpoints, same gt_prompts (K_CTX=24,
WIN=24), same atom split, same bar 0.65, same shuffle control — and move ONLY the probe's capacity,
up a four-rung ladder. Pre-registered in PREREG_H9296.md and committed before the hiddens were
dumped.

    P-LIN      mean-pooled · L2-logreg   → must reproduce H_9289 (V-REPRO), else nothing is read
    P-NL       mean-pooled · MLP         → is polarity encoded NONLINEARLY?
    P-CTX      per-context · logreg → per-atom majority vote → did the mean-pooling erase it?
    P-CTX-NL   per-context · MLP → vote  → the ceiling of the ladder

A probe that clears the bar only by memorising is worthless, so every rung carries a label-shuffle
control (V-SHUF) and a train-fit floor (V-FIT); base_only must stay below bar everywhere (V-BASE).
"""

from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = 0.65                      # frozen in H_9289 — not moved
L2 = 1e-3
SEED = 7
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
REPRO_TARGET, REPRO_TOL = 0.5517, 0.03      # V-REPRO: P-LIN must land on H_9289's number


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def logreg(Xtr, ytr, Xte, l2=L2, iters=800, lr=0.1):
    """L2 logistic regression — byte-faithful to H_9289's `_logreg_l2`."""
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    w, b = np.zeros(Xtr.shape[1]), 0.0
    for _ in range(iters):
        p = _sigmoid(Xtr @ w + b)
        g = Xtr.T @ (p - ytr) / len(ytr) + l2 * w
        w -= lr * g
        b -= lr * float((p - ytr).mean())
    return _sigmoid(Xte @ w + b), _sigmoid(Xtr @ w + b)


def mlp(Xtr, ytr, Xte, hidden=32, l2=L2, iters=1500, lr=0.05, seed=SEED):
    """One hidden layer, tanh. The nonlinear rung of the ladder."""
    rng = np.random.default_rng(seed)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    d = Xtr.shape[1]
    W1 = rng.normal(0, 1 / np.sqrt(d), (d, hidden))
    b1 = np.zeros(hidden)
    w2 = rng.normal(0, 1 / np.sqrt(hidden), hidden)
    b2 = 0.0
    n = len(ytr)
    for _ in range(iters):
        h = np.tanh(Xtr @ W1 + b1)
        p = _sigmoid(h @ w2 + b2)
        dz = (p - ytr) / n
        gw2 = h.T @ dz + l2 * w2
        gb2 = float(dz.sum())
        dh = np.outer(dz, w2) * (1 - h ** 2)
        gW1 = Xtr.T @ dh + l2 * W1
        gb1 = dh.sum(0)
        W1 -= lr * gW1; b1 -= lr * gb1; w2 -= lr * gw2; b2 -= lr * gb2
    te = _sigmoid(np.tanh(Xte @ W1 + b1) @ w2 + b2)
    tr = _sigmoid(np.tanh(Xtr @ W1 + b1) @ w2 + b2)
    return te, tr


def load(arm: str):
    """Per-atom context vectors — NOT pooled. Pooling is one of the things on trial."""
    npz = np.load(os.path.join(HERE, "hid", f"gt_hidden_{arm}.npz"))
    meta = json.load(open(os.path.join(HERE, "gt_atoms.json")))["atoms"]
    ctx, y, split, stems = [], [], [], []
    for a in meta:
        vs = [npz[i + "__last"] for i in a["ids"] if (i + "__last") in npz.files]
        if not vs:
            continue
        ctx.append(np.stack(vs, 0).astype(np.float64))
        y.append(a["pol"]); split.append(a["split"]); stems.append(a["stem"])
    return ctx, np.array(y), np.array(split), stems


def run_arm(arm: str, shuffle_labels: bool = False) -> dict:
    ctx, y, split, _ = load(arm)
    if shuffle_labels:
        y = np.random.default_rng(SEED).permutation(y)
    tr = split == "train"
    te = ~tr
    pooled = np.stack([c.mean(0) for c in ctx], 0)

    res = {}
    for name, fit in (("P-LIN", logreg), ("P-NL", mlp)):
        pte, ptr = fit(pooled[tr], y[tr].astype(float), pooled[te])
        res[name] = {"heldout": float(((pte > 0.5) == y[te]).mean()),
                     "train_fit": float(((ptr > 0.5) == y[tr]).mean())}

    # per-context rungs: fit on every context of every train atom, then MAJORITY-VOTE per test atom
    Xtr = np.concatenate([ctx[i] for i in np.where(tr)[0]], 0)
    ytr = np.concatenate([np.full(len(ctx[i]), y[i]) for i in np.where(tr)[0]]).astype(float)
    for name, fit in (("P-CTX", logreg), ("P-CTX-NL", mlp)):
        hits, fits = [], []
        for i in np.where(te)[0]:
            p, _ = fit(Xtr, ytr, ctx[i])
            hits.append(float(np.mean(p > 0.5) > 0.5) == y[i])
        for i in np.where(tr)[0]:
            p, _ = fit(Xtr, ytr, ctx[i])
            fits.append(float(np.mean(p > 0.5) > 0.5) == y[i])
        res[name] = {"heldout": float(np.mean(hits)), "train_fit": float(np.mean(fits))}
    return res


def main() -> int:
    out = {"bar": BAR, "arms": {}, "shuffle": {}}
    print(f"H_9296 — probe-capacity ladder · bar {BAR} (frozen in H_9289) · $0 · frozen ckpts\n")
    for arm in ARMS:
        out["arms"][arm] = run_arm(arm)
        out["shuffle"][arm] = run_arm(arm, shuffle_labels=True)

    print(f"{'arm':>13} | {'P-LIN':>16} {'P-NL':>16} {'P-CTX':>16} {'P-CTX-NL':>16}")
    print(f"{'':>13} | {'held (train)':>16} " * 1 + "…")
    print("-" * 90)
    for arm in ARMS:
        r = out["arms"][arm]
        cells = " ".join(f"{r[p]['heldout']:.3f} ({r[p]['train_fit']:.2f})".rjust(16)
                         for p in ("P-LIN", "P-NL", "P-CTX", "P-CTX-NL"))
        print(f"{arm:>13} | {cells}")
    print()
    print("label-SHUFFLE control (must sit at chance — anything high is memorisation):")
    for arm in ARMS:
        r = out["shuffle"][arm]
        cells = " ".join(f"{r[p]['heldout']:.3f}".rjust(16)
                         for p in ("P-LIN", "P-NL", "P-CTX", "P-CTX-NL"))
        print(f"{arm:>13} | {cells}")
    print()

    m7 = out["arms"]["main_s7"]
    v = {
        "V_REPRO": abs(m7["P-LIN"]["heldout"] - REPRO_TARGET) <= REPRO_TOL,
        "V_FIT": all(out["arms"][a][p]["train_fit"] >= 0.90
                     for a in ("main_s7", "main_s11") for p in m7),
        "V_SHUF": all(abs(out["shuffle"][a][p]["heldout"] - 0.5) <= 0.08
                      for a in ARMS for p in m7),
        "V_BASE": all(out["arms"]["base_only"][p]["heldout"] < BAR for p in m7),
    }
    for k, ok in v.items():
        print(f"{k:>8}: {'PASS' if ok else 'FAIL'}")
    out["v_gates"] = {k: bool(x) for k, x in v.items()}
    print()

    if not all(v.values()):
        verdict = "⏳ INVALID — a standing V-gate failed; no tier is reported."
    else:
        best_p = max(("P-LIN", "P-NL", "P-CTX", "P-CTX-NL"),
                     key=lambda p: max(m7[p]["heldout"], out["arms"]["main_s11"][p]["heldout"]))
        best = max(m7[best_p]["heldout"], out["arms"]["main_s11"][best_p]["heldout"])
        if best >= BAR:
            verdict = (f"🔓 PROBE-ARTIFACT — {best_p} reaches {best:.3f} ≥ bar {BAR}. "
                       "The signal WAS in the representation; H_9289's INFO-ABSENT is retracted "
                       "and the frontier's O/C-channel diagnosis needs re-examination.")
        elif best > 0.58:
            verdict = (f"🟡 PARTIAL — best probe {best_p} = {best:.3f}: above chance but below the "
                       f"frozen bar {BAR}. Partial signal is present; report the effect size, do "
                       "not move the bar.")
        else:
            verdict = (f"🧱 INFO-ABSENT CONFIRMED (strengthened) — the whole capacity ladder stays "
                       f"at chance (best {best_p} = {best:.3f}). H_9289 survives a probe that is "
                       "nonlinear AND per-context. The representation really lacks it ⇒ the "
                       "O/C-channel move is the right next step.")
    print(f"VERDICT: {verdict}")
    out["verdict"] = verdict
    json.dump(out, open(os.path.join(HERE, "probe_capacity.json"), "w"),
              ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
