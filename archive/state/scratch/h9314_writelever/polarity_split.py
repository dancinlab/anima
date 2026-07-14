"""H_9314 — split WRITE by polarity. This is the check that tells a real result from an artefact.

WRITE rose 0.448 -> 0.793 across the budget grid, and the naive reading is "the polarity is
landing". It is not that simple, and the split says why:

    cell            positive atoms (14)   negative atoms (15)   WRITE
    600  @ 5e-5           0.143                 0.733           0.448
    2000 @ 5e-5           0.119                 0.800           0.471
    6000 @ 5e-5           0.167                 0.956           0.575
    600  @ 2e-4           0.190                 0.956           0.586
    2000 @ 2e-4           0.571                 1.000           0.793

The low-budget cells are not learning. They are COLLAPSING onto the majority label: the negative
atoms climb to 0.96 while the positive atoms sit at 0.17 — worse than chance, because the model is
answering "부정" to nearly everything and the labels happen to be 14:15. A WRITE of 0.575 built that
way is an artefact of the label ratio, not evidence that any atom's polarity was written.
(convergence corpus-py-1: with balanced labels, a collapsed response distribution means the
gradient has no direction and the score is an accident.)

What makes 2000@2e-4 different is not that WRITE is higher. It is that the POSITIVE side finally
moves — 0.190 -> 0.571 — while the negative side saturates. The collapse breaks. That is the first
cell in this sweep where the model is distinguishing atoms rather than guessing a constant.

So the sweep's headline number (WRITE) and its meaning diverge, and only this decomposition
separates them. Any budget claim must be made on the positive-atom column, not on WRITE.
"""

import collections
import json
import os

K = os.path.expanduser("~/anima-weights/c34")
H = os.path.expanduser("~/anima-weights/h9314")

CELLS = [(600, "5e-5"), (2000, "5e-5"), (6000, "5e-5"), (600, "2e-4"), (2000, "2e-4"),
         (6000, "2e-4"), (2000, "5e-4"), (6000, "5e-4")]


def held_atoms():
    a = json.load(open(os.path.join(K, "gt_atoms.json")))["atoms"]
    return [x for x in a if x["split"] == "heldout"]


def per_atom(path, keys):
    """man_trainlines.json is built atom-major, 3 flip0 forms each — so rows map by index."""
    if not os.path.exists(path):
        return None
    rows = json.load(open(path))["splits"]["heldout"]["rows"]
    if len(rows) != len(keys):
        return None
    d = collections.defaultdict(list)
    for (stem, pol), r in zip(keys, rows):
        d[(stem, pol)].append(1 if r["margin"] > 0 else 0)
    return {k: sum(v) / len(v) for k, v in d.items()}


def main():
    A = held_atoms()
    keys = [(a["stem"], a["pol"]) for a in A for _ in range(3)]
    npos = sum(1 for a in A if a["pol"] == 1)
    nneg = len(A) - npos

    print("=" * 78)
    print("H_9314 — WRITE 를 극성별로 쪼갠다 (라벨 긍정 %d : 부정 %d)" % (npos, nneg))
    print("  다수 라벨 붕괴라면 **부정만 오르고 긍정은 바닥**에 남는다 — 그건 학습이 아니다")
    print("=" * 78)
    print()
    print("  cell               긍정원자(%d)   부정원자(%d)   WRITE   판정" % (npos, nneg))
    for st, lr in CELLS:
        d = per_atom(os.path.join(H, "wl_s%d_lr%s_held.json" % (st, lr)), keys)
        if not d:
            continue
        pos = [v for (s, p), v in d.items() if p == 1]
        neg = [v for (s, p), v in d.items() if p == 0]
        p, n, w = sum(pos) / len(pos), sum(neg) / len(neg), sum(d.values()) / len(d)
        # A cell is only "learning" if the minority side moves too. Everything else is the ratio.
        tag = ("붕괴(다수라벨)" if p < 0.30 else
               "학습 시작" if p < 0.70 else "학습")
        print("  %-5d @ %-6s      %.3f          %.3f        %.3f   %s" % (st, lr, p, n, w, tag))
    print()
    print("  ⟹ 예산 주장은 **WRITE 가 아니라 긍정원자 열**에서 해야 한다.")


if __name__ == "__main__":
    main()
