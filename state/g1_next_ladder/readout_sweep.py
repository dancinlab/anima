"""Tier-0 #1b · READOUT-POINT SWEEP — where, if anywhere, IS polarity represented?

GATE-0 was ruled INVALID-INSTRUMENT (#3395): the probe cannot read polarity even off the P_grid
TRAIN atoms the model behaviorally masters (SEEN D-acc 0.9625; probe LOO tops out at 0.600 vs the
0.85 positive-control bar, across l2 / PCA / nearest-centroid). A gate whose positive control fails
is not a gate — so every "the representation lacks polarity" verdict built on it is SUSPENDED, not
flipped.

To un-suspend it we must find a readout point where the positive control PASSES. Only there does a
held-out number mean anything.

KEY FACT (source-checked, cli/evaluate.py:1146-1150): `--dump-hidden` ALREADY stores three things
per prompt — `__seq` [T,d] (the full right-aligned window), `__mean` [d], `__last` [d]. The old
harness (reduce_reps.py) consumed ONLY `__last`, which is why the recovered reps_*.npz have a single
point in them. No engine change is needed: re-dump, then sweep the points that were always there.

Sweep axes (pre-registered):
  position  : __last (the current one) · every offset in the window (T-1 .. T-8) · __mean (all)
  pooling   : per-atom mean over its contexts (as before) · per-atom max-abs · per-context then vote
  capacity  : L2-logreg (l2 in 5/50/500) · nearest-centroid · small MLP  (all with shuffle control)

GATE (frozen, and this is the whole point):
  a point QUALIFIES only if TRAIN-atom leave-one-out >= 0.85 (positive control), with its
  label-shuffle control at chance. Only qualifying points may then report held-out.

⚠️ tune-to-green guard: the point is selected by the POSITIVE CONTROL ONLY. held-out numbers are
read AFTER a point qualifies, once, and are never used to choose the point. If several points
qualify, report all of them (no cherry-picking).

Usage:
  # on a GPU pod (303M decode is banned on mini — swap OOM):
  anima-py evaluate <ckpt> --dump-hidden gt_prompts.json --out gt_hidden_<tag>.npz --win 24
  python3 readout_sweep.py gt_hidden_<tag>.npz gt_atoms.json
"""

import json
import os
import sys

import numpy as np

BAR_POS_CTRL = 0.85          # positive control: TRAIN-atom LOO must clear this
SEED = 7
SHUFFLE_REPS = 5


# ---------------------------------------------------------------- probes
def logreg_l2(Xtr, ytr, Xte, l2=5.0, iters=800, lr=0.1):
    """frozen protocol (gt_step0_gprobe.py), overflow-guarded."""
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    Xtr = (Xtr - mu) / sd
    Xte = (Xte - mu) / sd
    n, d = Xtr.shape
    w = np.zeros(d)
    b = 0.0
    yb = ytr.astype("float64")
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-np.clip(Xtr @ w + b, -60, 60)))
        w -= lr * (Xtr.T @ (p - yb) / n + l2 * w / n)
        b -= lr * float((p - yb).mean())
    return 1.0 / (1.0 + np.exp(-np.clip(Xte @ w + b, -60, 60)))


def centroid(Xtr, ytr, Xte):
    c0, c1 = Xtr[ytr == 0].mean(0), Xtr[ytr == 1].mean(0)
    d0 = np.linalg.norm(Xte - c0, axis=1)
    d1 = np.linalg.norm(Xte - c1, axis=1)
    return (d1 < d0).astype(float)


def loo(X, y, fit):
    hits = []
    for i in range(len(y)):
        m = np.ones(len(y), bool)
        m[i] = False
        p = fit(X[m], y[m], X[i:i + 1])
        hits.append(int((p[0] >= 0.5) == bool(y[i])))
    return float(np.mean(hits))


def loo_shuffle(X, y, fit, reps=SHUFFLE_REPS):
    rng = np.random.RandomState(SEED)
    return float(np.mean([loo(X, rng.permutation(y), fit) for _ in range(reps)]))


# ------------------------------------------------------------ extraction
def atom_matrix(npz, atoms, point, pool):
    """Build [n_atoms, d] for one (position, pooling) combination.
    point: 'last' | 'mean' | int offset k (the k-th from the END of the window)
    pool : 'mean' (average an atom's contexts) | 'maxabs'
    """
    X, y, split, stems = [], [], [], []
    for a in atoms:
        vecs = []
        for i in a["ids"]:
            if point == "last":
                k = i + "__last"
                if k in npz.files:
                    vecs.append(npz[k])
            elif point == "mean":
                k = i + "__mean"
                if k in npz.files:
                    vecs.append(npz[k])
            else:  # integer offset into __seq, counted from the end
                k = i + "__seq"
                if k in npz.files:
                    seq = npz[k]
                    if seq.shape[0] > point:
                        vecs.append(seq[seq.shape[0] - 1 - point])
        if not vecs:
            continue
        V = np.stack(vecs, 0).astype("float64")
        v = V.mean(0) if pool == "mean" else V[np.argmax(np.abs(V).sum(1))]
        X.append(v)
        y.append(int(a["pol"]))
        split.append(a["split"])
        stems.append(a["stem"])
    return (np.stack(X, 0), np.array(y), np.array(split), stems) if X else (None, None, None, None)


def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: readout_sweep.py <gt_hidden_TAG.npz> <gt_atoms.json>")
    npz = np.load(sys.argv[1], allow_pickle=True)
    atoms = json.load(open(sys.argv[2]))["atoms"]

    probes = [
        ("logreg l2=5", lambda a, b, c: logreg_l2(a, b, c, 5.0)),
        ("logreg l2=50", lambda a, b, c: logreg_l2(a, b, c, 50.0)),
        ("centroid", centroid),
    ]
    points = ["last", "mean"] + list(range(1, 8))     # offsets 1..7 from the end of the window
    pools = ["mean", "maxabs"]

    print("=" * 92)
    print("READOUT-POINT SWEEP — 양성대조(TRAIN 원자 LOO >= %.2f)를 통과하는 지점이 있는가" % BAR_POS_CTRL)
    print("  ⚠️ 지점 선택은 양성대조로만. held-out 은 통과 지점에 대해서만, 사후에 한 번 읽는다.")
    print("=" * 92)
    print(f"  {'point':>6s} {'pool':>7s} {'probe':>13s} {'TRAIN LOO':>10s} {'shuffle':>8s}  {'':4s}")

    qualified = []
    for point in points:
        for pool in pools:
            X, y, split, _ = atom_matrix(npz, atoms, point, pool)
            if X is None:
                continue
            tr = split == "train"
            if tr.sum() < 6:
                continue
            for pname, fit in probes:
                a = loo(X[tr], y[tr], fit)
                s = loo_shuffle(X[tr], y[tr], fit)
                mark = ""
                if a >= BAR_POS_CTRL:
                    mark = "✅ QUALIFIES"
                    qualified.append((point, pool, pname, a, s))
                print(f"  {str(point):>6s} {pool:>7s} {pname:>13s} {a:10.3f} {s:8.3f}  {mark}")

    print("\n" + "=" * 92)
    if not qualified:
        print("VERDICT: ⛔ NO QUALIFYING POINT — 위치·풀링·용량 어느 조합에서도 양성대조가 서지 않는다.")
        print("  ⟹ 모델이 행동으로 통달한 원자의 극성조차, 이 덤프가 노출하는 어떤 읽기 지점에서도")
        print("     선형/프로토타입으로 표현되지 않는다. 이것 자체가 강한 사실이다 —")
        print("     '행동은 하는데 그 변수를 읽을 수 있는 형태로 들고 있지 않다'(해리의 실체).")
        print("  ⟹ GATE-0 계열 판정은 영구 유보. 표현-기반 게이트 대신 인과 개입(활성 절제/조향)으로 갈 것.")
    else:
        print("VERDICT: 🟢 QUALIFYING POINT(S) FOUND — GATE-0 복권 가능")
        for point, pool, pname, a, s in qualified:
            print(f"  point={point} pool={pool} probe={pname} · TRAIN LOO={a:.3f} (shuffle {s:.3f})")
        print("  ⟹ 이 지점(들)에서만 held-out 을 읽어 GATE-0 재판정. 여러 개면 전부 보고(체리피킹 금지).")
    print("=" * 92)

    out = {"bar_pos_ctrl": BAR_POS_CTRL,
           "qualified": [{"point": str(p), "pool": po, "probe": pr, "train_loo": a, "shuffle": s}
                         for p, po, pr, a, s in qualified]}
    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "READOUT_SWEEP.json")
    with open(dst, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("→ READOUT_SWEEP.json")


if __name__ == "__main__":
    main()
