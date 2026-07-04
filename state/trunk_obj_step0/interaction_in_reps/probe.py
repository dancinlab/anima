#!/usr/bin/env python3
"""H_9131 §4 — interaction-in-reps falsifier (Fable wall-break, THE $0 GPU go/no-go).

The retracted STEP-0 (../noncommutative_derisk/derisk.py) probed the non-commutative
residual r(a,b)=(P[a,b]-P[b,a])/tot with a bilinear on FROZEN STRUCTURAL embeddings
(anchor-relative co-occ profiles) — bind R^2 < additive on held-out ⇒ FALSIFIED-on-those-
features. But that did NOT test the actual trunk: does the 303M FORWARD representation
carry the interaction?  This probe answers exactly that, engine-native.

Question (decides the ② GPU trunk-retrain go/no-go):
  Does the 303M joint forward rep h(a,b) linearly encode the additive-blind residual
  r(a,b) BEYOND what a linear probe on the separate single-concept reps [z(a),z(b)] can,
  on HELD-OUT pairs (combo unseen; both concepts seen singly)?

  PASS  → interaction is IN the reps, unsurfaced ⇒ an objective aux loss (F1/②) can teach
          the trunk to emit it ⇒ GPU trunk-retrain JUSTIFIED.
  FAIL  → joint ≈ additive on held-out ⇒ reps don't carry it ⇒ objective aux can't conjure
          it ⇒ KILL the ② GPU spend; fall to F2 (data-density, ember+dune already positive).

Reuses: vocab.json + P.npy + label from ../noncommutative_derisk (1:1, no re-derivation);
303M reps via core/decode.py::bg_forward_last_hidden (== anima evaluate --py forward path,
TERMINAL-eligible; the primitive added for exactly this). $0 mini, single forwards only.
Frozen bar pre-registered here BEFORE running (a_break_the_wall, no tune-to-green)."""
import os
import sys
import json
import time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
_DERISK = os.path.join(_REPO, "state", "trunk_obj_step0", "noncommutative_derisk")
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d   # bg_load / bg_forward_last_hidden (== anima evaluate --py ops)

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
# ---- frozen structural constants (inherited from derisk.py PREREG, verbatim) ----
K_ANCHOR = 32
MINC_TGT = 40
HELDOUT_FRAC = 0.20
DELTA = 0.10          # same held-out R^2 margin bar as STEP-0
SEEDS = [7, 4302, 4303]
MAX_PAIRS = 2600      # cap joint forwards for mini-safety ($0 gate; subsample is seeded+logged)
T_CAP = 32            # byte-context cap for a pair "a b"


def build_pairs():
    """EXACT copy of derisk.build_frozen's anchor/concept/pair/label logic, but returns
    WORD STRINGS (for 303M forward) instead of frozen structural embeddings Z."""
    vocab = json.load(open(f"{_DERISK}/vocab.json"))["vocab"]
    P = np.load(f"{_DERISK}/P.npy")
    N = P.shape[0]
    tot = P + P.T
    deg = tot.sum(1)
    anchors = set(int(a) for a in np.argsort(-deg)[:K_ANCHOR])
    concepts = [i for i in range(N) if i not in anchors]
    pairs = []
    for ci in range(len(concepts)):
        a = concepts[ci]
        for cj in range(ci + 1, len(concepts)):
            b = concepts[cj]
            m = tot[a, b]
            if m < MINC_TGT:
                continue
            y = (P[a, b] - P[b, a]) / m       # non-commutative residual, model-free
            pairs.append((a, b, float(y)))
    return vocab, np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs]), \
           np.array([p[2] for p in pairs]), concepts


def ids_of(word, W):
    return list(word.encode("utf-8", "surrogateescape"))


def fit_eval(Xtr, ytr, Xte, yte):
    """closed-form lstsq R^2 with intercept — same estimator as derisk (no ridge/tune)."""
    def aug(X):
        return np.hstack([X, np.ones((X.shape[0], 1))])
    coef, *_ = np.linalg.lstsq(aug(Xtr), ytr, rcond=None)
    def r2(X, y):
        pred = aug(X) @ coef
        ssr = float(((y - pred) ** 2).sum()); sst = float(((y - y.mean()) ** 2).sum())
        return 1.0 - ssr / sst if sst > 0 else float("nan")
    return r2(Xtr, ytr), r2(Xte, yte)


def run_seed(seed, A, B, Y, Zsingle, Hjoint):
    """Zsingle[i]=303M single rep of concept i; Hjoint[k]=303M joint rep of pair k."""
    rng = np.random.default_rng(seed)
    n = len(Y); idx = np.arange(n); rng.shuffle(idx)
    n_hold = int(round(HELDOUT_FRAC * n))
    hold_cand, train_idx = idx[:n_hold], idx[n_hold:]
    train_concepts = set(A[train_idx].tolist()) | set(B[train_idx].tolist())
    train_pairset = set(zip(A[train_idx].tolist(), B[train_idx].tolist()))
    hold_idx = np.array([i for i in hold_cand
                         if (int(A[i]), int(B[i])) not in train_pairset
                         and int(A[i]) in train_concepts and int(B[i]) in train_concepts])
    assert len(train_pairset & set(zip(A[hold_idx].tolist(), B[hold_idx].tolist()))) == 0

    # ADDITIVE arm: linear probe on the SEPARATE single-concept reps [z(a) , z(b)]
    add_tr = np.hstack([Zsingle[A[train_idx]], Zsingle[B[train_idx]]])
    add_te = np.hstack([Zsingle[A[hold_idx]], Zsingle[B[hold_idx]]])
    r2_add_tr, r2_add = fit_eval(add_tr, Y[train_idx], add_te, Y[hold_idx])

    # JOINT arm: linear probe on the 303M JOINT forward rep h(a,b)
    j_tr, j_te = Hjoint[train_idx], Hjoint[hold_idx]
    r2_j_tr, r2_joint = fit_eval(j_tr, Y[train_idx], j_te, Y[hold_idx])

    # SHUFFLE control: joint rep paired to a scrambled label's partner (destroy interaction)
    perm = rng.permutation(len(hold_idx))
    r2_sf_tr, r2_sf = fit_eval(Hjoint[train_idx], Y[train_idx], Hjoint[hold_idx], Y[hold_idx][perm])

    gap = r2_joint - r2_add
    return {"seed": seed, "n_pairs": int(n), "n_train": int(len(train_idx)),
            "n_heldout": int(len(hold_idx)),
            "r2_joint": r2_joint, "r2_additive": r2_add, "r2_shuffle_label": r2_sf,
            "r2_joint_train": r2_j_tr, "r2_additive_train": r2_add_tr,
            "gap_joint_minus_additive": gap,
            "pass_gap": bool(gap >= DELTA),
            "pass_shuffle_collapse": bool(r2_sf < DELTA),
            "leak_joint_exact1": bool(abs(r2_joint - 1.0) < 1e-9)}


def main():
    t0 = time.time()
    print("[1/4] build pairs from frozen census (derisk 1:1) ...", flush=True)
    vocab, A, B, Y, concepts = build_pairs()
    print(f"      {len(vocab)} vocab · {len(Y)} pairs · {len(concepts)} concepts", flush=True)
    # seeded subsample for mini-safety (log what's dropped — no silent cap)
    if len(Y) > MAX_PAIRS:
        rng = np.random.default_rng(20260705)
        keep = rng.choice(len(Y), MAX_PAIRS, replace=False)
        A, B, Y = A[keep], B[keep], Y[keep]
        print(f"      subsampled {MAX_PAIRS}/{len(keep)} pairs (seed 20260705) for $0 gate", flush=True)
    used = sorted(set(A.tolist()) | set(B.tolist()))

    print(f"[2/4] 303M single reps for {len(used)} concepts (h1129) ...", flush=True)
    W = d.bg_load(CKPT)
    assert d.bg_is_bytegpt(CKPT)
    dd = W["d"]
    Zsingle = np.zeros((P_N := (max(used) + 1), dd), dtype=np.float64)
    for c in used:
        ids = ids_of(vocab[c], W)
        Zsingle[c] = d.bg_forward_last_hidden(W, ids, len(ids))
    print(f"      single reps done ({time.time()-t0:.1f}s)", flush=True)

    print(f"[3/4] 303M JOINT reps for {len(Y)} pairs (context 'a b') ...", flush=True)
    Hjoint = np.zeros((len(Y), dd), dtype=np.float64)
    for k in range(len(Y)):
        wa, wb = vocab[int(A[k])], vocab[int(B[k])]
        ids = ids_of(wa + " " + wb, W)[:T_CAP]
        Hjoint[k] = d.bg_forward_last_hidden(W, ids, len(ids))
        if k % 400 == 0:
            print(f"      joint {k}/{len(Y)} ({time.time()-t0:.1f}s)", flush=True)
    print(f"      joint reps done ({time.time()-t0:.1f}s)", flush=True)

    print("[4/4] fit additive vs joint, 3 seeds ...", flush=True)
    results = [run_seed(s, A, B, Y, Zsingle, Hjoint) for s in SEEDS]
    n_pass = sum(r["pass_gap"] and r["pass_shuffle_collapse"] for r in results)
    any_leak = any(r["leak_joint_exact1"] for r in results)
    if any_leak:
        verdict = "INVALID-LEAK"
    elif n_pass >= 2:
        verdict = "PASS-interaction-in-reps → ② GPU JUSTIFIED"
    elif n_pass == 0:
        verdict = "FAIL-joint≈additive → KILL ② GPU, fall to F2 (data-density)"
    else:
        verdict = "DIRECTIONAL (1/3 seeds)"

    summary = {
        "probe": "H_9131 §4 interaction-in-reps (303M forward joint vs additive, held-out)",
        "engine": f"real ByteGPT-303M h1129 d={W['d']} nlay={W['nlay']} (core/decode.py bg_forward_last_hidden == anima evaluate --py)",
        "ckpt": CKPT, "delta_bar": DELTA, "seeds": SEEDS, "n_pass_2of3": n_pass,
        "max_pairs": MAX_PAIRS, "verdict": verdict, "results": results,
        "bar": "PASS iff ≥2/3 seeds: (r2_joint − r2_additive) ≥ 0.10 held-out AND shuffle-label collapses (<0.10); no joint=1.0 leak.",
        "honesty": "py 2-production numpy = engine-native TERMINAL-eligible (a_eval_py_canonical). Frozen residual label = corpus co-occ, model-free.",
    }
    print("\n" + json.dumps(summary, ensure_ascii=False, indent=2))
    with open(f"{_HERE}/RESULT.json", "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n[done] {time.time()-t0:.1f}s → RESULT.json  verdict={verdict}")


if __name__ == "__main__":
    main()
