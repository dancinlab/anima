"""H_9302 — certify the instrument BEFORE reading another negative off it.

Every negative this lane has produced (H_9289 INFO-ABSENT, H_9297 EARNED, H_9300) was read off a
probe that never demonstrated it can call a TRUE thing true. Its only liveness gate was
V-FIT (train_fit >= 0.90), which at 20 train atoms in d=768 reads 1.000 for EVERY arm -- including
base_only and shuffle_grid -- because 20 points in 768 dimensions are always separable. A gate that
cannot fail is not a gate (convergence probe-capacity-py-1).

THE POSITIVE CONTROL. The 20 train atoms are grid atoms: the model was EXPLICITLY taught their
polarity. If the representation encodes polarity at all, it must encode THEIRS. So:

  · do NOT mean-pool. Each of an atom's 24 contexts is its own sample -> 20 x 24 = 480 samples in
    the train split, which is what makes leave-one-ATOM-out cross-validation powered at all.
  · leave-one-ATOM-out (never leave-one-context-out: contexts of the same atom share the stem, so a
    context-level split leaks the atom and would certify a probe that only reads orthography).
  · read TWO accuracies per fold: per-CONTEXT (n=480, chance sd 0.0228 -- this is where the power
    is) and per-ATOM by majority vote over the held-out atom's 24 contexts (n=20, chance sd 0.1118).
  · the same run on base_only and shuffle_grid is the NEGATIVE control: those arms never saw the
    polarity grid, so a probe that reads them equally well is reading something other than polarity.

DECISION (frozen before the numbers):
  LIVE   : main arms clear the per-context permutation null AND beat both control arms
           -> the instrument can read taught polarity; its held-out negatives mean something.
  DEAD   : main arms sit at chance, or the controls match them
           -> the instrument was never able to read polarity from ANYTHING, and every negative in
              this lane (H_9289/H_9297/H_9300) is INVALID, not a wall. The frontier's
              "wall = extraction channel" would then rest on nothing.

$0: reads the npz dumps already on disk (win=24 and win=192, 4 arms).
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
N_PERM = 200
SEED = 7


def load(arm: str, win: int):
    tag = "gt_n92" if win == 24 else f"w{win}"
    npz = np.load(os.path.join(HERE, "hid", f"{tag}_{arm}.npz"))
    meta = json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
    X, y, atom = [], [], []
    for ai, a in enumerate(meta):
        if a["split"] != "train":            # the POSITIVE control lives in the taught atoms
            continue
        for i in a["ids"]:
            k = i + "__last"
            if k in npz.files:
                X.append(npz[k]); y.append(a["pol"]); atom.append(ai)
    return np.array(X, np.float64), np.array(y), np.array(atom)


def loo_atom(X, y, atom, rng=None):
    """Leave-one-ATOM-out. Returns (per-context acc, per-atom majority-vote acc)."""
    yy = y if rng is None else _permute_by_atom(y, atom, rng)
    ctx_hit, atom_hit, n_ctx = 0, 0, 0
    for a in np.unique(atom):
        te = atom == a
        s = StandardScaler().fit(X[~te])
        m = LogisticRegression(max_iter=2000, C=0.1).fit(s.transform(X[~te]), yy[~te])
        p = m.predict(s.transform(X[te]))
        ctx_hit += int((p == yy[te]).sum()); n_ctx += int(te.sum())
        atom_hit += int((p.mean() > 0.5) == (yy[te][0] > 0.5))
    return ctx_hit / n_ctx, atom_hit / len(np.unique(atom))


def _permute_by_atom(y, atom, rng):
    """Permute the LABEL of each atom (not of each context) — a context-level shuffle would leave
    each atom's label almost intact under majority vote and fake a null that is far too easy."""
    ids = np.unique(atom)
    lab = {a: y[atom == a][0] for a in ids}
    perm = rng.permutation([lab[a] for a in ids])
    return np.array([perm[list(ids).index(a)] for a in atom])


def main() -> int:
    win = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    out = {"win": win, "arms": {}}
    print(f"H_9302 — INSTRUMENT LIVENESS · win={win} · positive control = the 20 GRID-TAUGHT atoms")
    print(f"  per-context n=480 (chance sd {math.sqrt(0.25/480):.4f}) · "
          f"per-atom n=20 (chance sd {math.sqrt(0.25/20):.4f})\n")
    for arm in ARMS:
        X, y, atom = load(arm, win)
        ctx, at = loo_atom(X, y, atom)
        rng = np.random.default_rng(SEED)
        null = np.array([loo_atom(X, y, atom, rng)[0] for _ in range(N_PERM)])
        p = float((null >= ctx).mean())
        out["arms"][arm] = {"per_context": ctx, "per_atom": at, "perm_p": p,
                            "perm_null_p95": float(np.quantile(null, 0.95)),
                            "n_context": int(len(y)), "n_atom": int(len(np.unique(atom)))}
        kind = "EXPERIMENT" if arm.startswith("main") else "control  "
        print(f"  {kind} {arm:>13} | per-context {ctx:.3f} (perm p={p:.3f}, null p95 "
              f"{np.quantile(null, 0.95):.3f})  ·  per-atom {at:.3f}")

    m = [out["arms"][a] for a in ("main_s7", "main_s11")]
    c = [out["arms"][a] for a in ("base_only", "shuffle_grid")]
    live = (all(x["perm_p"] < 0.05 for x in m)
            and min(x["per_context"] for x in m) > max(x["per_context"] for x in c))
    print()
    out["verdict"] = ("✅ INSTRUMENT LIVE — the probe reads polarity the model was TAUGHT, above its "
                      "own permutation null and above both untaught controls. Its held-out negatives "
                      "carry meaning."
                      if live else
                      "🧨 INSTRUMENT DEAD — the probe cannot read polarity even where the model was "
                      "explicitly taught it, or the untaught controls read just as well. Every "
                      "negative in this lane (H_9289 · H_9297 · H_9300) is INVALID, not a wall — "
                      "and 'wall = extraction channel' rests on nothing.")
    print("VERDICT:", out["verdict"])
    json.dump(out, open(os.path.join(HERE, f"probe_liveness_w{win}.json"), "w"),
              ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
