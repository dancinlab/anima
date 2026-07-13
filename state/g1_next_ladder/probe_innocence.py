"""Tier-0 #1 · PROBE INNOCENCE BATTERY — is GATE-0 a valid gate at all?

A gate whose POSITIVE CONTROL fails is not a gate. GATE-0 asks whether held-out atom polarity is
linearly readable from the model's representation (bar 0.65). Before reading its FAIL as a fact
about the model, the instrument must be shown to detect the signal WHERE IT MUST EXIST:
the P_grid TRAIN atoms — the ones the model was explicitly trained on and behaviorally masters
(SEEN D-acc 0.9625 for main_s7).

precedent: morphatom-gate-py-1 — a 4-fold instrument defect once forged "the codec failed to learn"
out of a model whose training-stream nll was 0.993 (perfect). Suspect the probe first.

Battery (all $0, existing reps_*.npz):
  1. TRAIN-atom leave-one-out probe (positive control)  + label-shuffle control
  2. capacity sweep — l2 in {5, 50, 500}, PCA k in {4, 8, 16}, and a nearest-centroid prototype
     (the lowest-capacity classifier there is). If polarity were present in this readout point in
     ANY form, at least one setting must clear it.
  3. HELD-OUT probe (the GATE-0 headline) for reference.

Verdict:
  positive control PASSES (>=0.85)  -> instrument OK; a held-out FAIL is a fact about generalization
  positive control FAILS everywhere -> GATE-0 is reading a point where polarity is not represented
                                       even for atoms the model demonstrably masters. GATE-0 cannot
                                       license any conclusion until a readout point that passes the
                                       positive control is found. INVALID-INSTRUMENT (suspend, do not
                                       flip the verdict — suspending is the honest move).
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = os.path.expanduser("~/anima-weights/c34")
SEED = 7
BAR_POS_CTRL = 0.85          # the positive control must clear this for GATE-0 to mean anything
SHUFFLE_REPS = 10


def logreg_l2(Xtr, ytr, Xte, l2=5.0, iters=800, lr=0.1):
    """frozen protocol (gt_step0_gprobe.py), with the sigmoid guarded against overflow."""
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


def loo(X, y, l2=5.0):
    hits = []
    for i in range(len(y)):
        m = np.ones(len(y), bool)
        m[i] = False
        p = logreg_l2(X[m], y[m], X[i:i + 1], l2=l2)
        hits.append(int((p[0] >= 0.5) == bool(y[i])))
    return float(np.mean(hits))


def loo_shuffle(X, y, l2=5.0, reps=SHUFFLE_REPS):
    rng = np.random.RandomState(SEED)
    return float(np.mean([loo(X, rng.permutation(y), l2) for _ in range(reps)]))


def prototype_loo(X, y):
    """nearest-centroid — the lowest-capacity readout. If polarity is anywhere in this point, a
    class-mean split should at least beat chance."""
    hits = []
    for i in range(len(y)):
        m = np.ones(len(y), bool)
        m[i] = False
        c0, c1 = X[m][y[m] == 0].mean(0), X[m][y[m] == 1].mean(0)
        pred = 1 if np.linalg.norm(X[i] - c1) < np.linalg.norm(X[i] - c0) else 0
        hits.append(int(pred == y[i]))
    return float(np.mean(hits))


def run(tag="main_s7"):
    p = os.path.join(KEEP, f"reps_{tag}.npz")
    if not os.path.exists(p):
        raise SystemExit(f"[PENDING] reps_{tag}.npz 미회수")
    z = np.load(p, allow_pickle=True)
    X, y, split = z["X"].astype("float64"), z["y"], z["split"]
    tr, te = split == "train", split == "heldout"
    Xtr, ytr = X[tr], y[tr]

    print("=" * 72)
    print(f"프로브 무죄 배터리 — {tag} (reps 재사용 · $0)")
    print(f"  원자: train={tr.sum()} heldout={te.sum()} · d={X.shape[1]}")
    print("=" * 72)

    rows = []
    for l2 in (5.0, 50.0, 500.0):
        rows.append((f"raw d={X.shape[1]} l2={l2:g}", loo(Xtr, ytr, l2), loo_shuffle(Xtr, ytr, l2, 5)))

    Xc = Xtr - Xtr.mean(0)
    Vt = np.linalg.svd(Xc, full_matrices=False)[2]
    for k in (4, 8, 16):
        Xp = Xc @ Vt[:k].T
        rows.append((f"PCA k={k} l2=5", loo(Xp, ytr, 5.0), loo_shuffle(Xp, ytr, 5.0, 5)))

    rows.append(("prototype(최근접평균)", prototype_loo(Xtr, ytr), 0.5))

    print(f"  {'설정':26s} {'LOO':>6s} {'셔플':>6s}")
    for name, a, s in rows:
        print(f"  {name:26s} {a:6.3f} {s:6.3f}")

    best = max(r[1] for r in rows)
    p_te = logreg_l2(X[tr], y[tr], X[te])
    ho = float(np.mean((p_te >= 0.5).astype(int) == y[te]))
    print(f"\n  HELD-OUT probe (GATE-0 헤드라인) = {ho:.4f}  (bar 0.65)")
    print(f"  양성대조 최고치 = {best:.4f}  (bar {BAR_POS_CTRL})")

    print("\n" + "=" * 72)
    if best >= BAR_POS_CTRL:
        v = ("🟢 INSTRUMENT-OK — 프로브가 '아는' 원자의 극성을 읽는다. "
             "held-out FAIL 은 일반화에 대한 사실로 읽어도 된다.")
    else:
        v = ("⛔ INVALID-INSTRUMENT — 어떤 용량 설정으로도 양성대조가 서지 않는다. "
             "모델이 행동으로 통달한(SEEN 0.96) 원자조차 이 읽기 지점에서 극성이 선형·프로토타입 어느 쪽으로도 "
             "표현되지 않는다. ⟹ GATE-0 은 극성이 표현되지 않는 지점을 읽고 있다 = 이 게이트로는 "
             "어떤 결론도 licensing 할 수 없다. verdict 를 뒤집는 게 아니라 **판정을 유보**하는 것이 정직한 수. "
             "NEXT = 읽기 지점 탐색(답-토큰 위치 · 층 스윕 · 비선형) 후 양성대조를 통과하는 지점에서만 재판정.")
    print("VERDICT:", v)
    print("=" * 72)
    return v


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "main_s7")
