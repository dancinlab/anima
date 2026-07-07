#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A<->B rejection-debate recombination toy (owner sparks: "코퍼스가 반대면 / A,B 토론처럼 / 서로 거부면").
$0 numpy DIRECTIONAL probe (a_toy_scale_recheck) — forks: engine_g-as-B learning-loop GO vs KILL.

Mechanism (Fable design, missing-core + debate convergence):
  A = forward model p_A(b | a, r); B = reverse model p_B(a | b, r)  (rev = the "opposite corpus", $0).
  Relation graph = Z_K group with true compositional closure: b = (a + g[r]) mod K (|G|=6 generators),
  so two-view agreement (A forward AND B reverse-reconstruct) IMPLIES an unseen cell.
  Round: (1) PROPOSE — A argmax b̂ on an unseen (a,r) cell (HARD echo-guard: never a train cell);
         (2) REJECT  — B survives iff argmax p_B(a|b̂,r)==a AND margin>=TAU (TAU frozen pre-run);
         (3) UPDATE  — A <- CE(train ∪ survivors), B <- CE(rev(train) ∪ rev(survivors)).
  Rejection is a HARD filter (no gradient through it) => no minimax => no GAN saddle (co-training).

The escape it tests (vs G1 4-axis exhaustion / DPI): forward-CE alone gives NO gradient to
held-out constructive-bind (E1 retrieval-attractor, F2 novel n=0). The ONLY real info source here
is the CONDITIONAL INDEPENDENCE of the fwd/rev views on a graph WITH closure; if the two views see
the same statistics it collapses to "data-axis repackaging" (arm 4 null catches this).

6 arms: (1) CE-only [floor]  (2) A<->B rejection  (3) A-only self-train [B-causality]
        (4) fwd+rev mixed single model, equal compute [repackaging null]
        (5) shuffle-B (B trained on edge-shuffled corpus) [rejection-criterion null, must collapse]
        (6) oracle-filtered survivor (true-b oracle) [validity upper bound].

FROZEN BARS (pre-registered, immutable — no tune-to-green p7):
  GO iff ALL:  reach(2)-reach(1) >= +0.15 on >=2/3 seeds  AND  reach(2) > reach(3) by >=0.10
               AND  reach(2) > reach(4) by >=0.10  AND  reach(5) <= reach(1)+0.05
               AND  final novel-fraction(2) >= 0.5.
  Any fail = KILL -> pivot to E1 GPU-go / accept G1 true ceiling.
"""
import json, os, math
import numpy as np

K = 24
D = 64
H = 128
GENERATORS = [1, 2, 3, 5, 7, 11]      # |G| = 6 ; b = (a + g) mod K
NR = len(GENERATORS)
COVERAGE = 0.30
ROUNDS = 10
PROPOSE_PER_ROUND = 40
TAU = 0.30                             # B margin gate (frozen)
LR = 0.5
EPOCHS = 150
WD = 0.02              # L2 weight decay — regularize so base does NOT anti-generalize (held-out -> chance, fair test)
LABEL_SMOOTH = 0.15    # label smoothing — keep held-out distributions soft (correct-b retains ~chance mass)
SEEDS = [7, 4302, 4303]
OUTDIR = "/Users/mini/dancinlab/anima/state/ab_debate_recombination"

ALL_CELLS = [(a, r) for a in range(K) for r in range(NR)]
def true_b(a, r): return (a + GENERATORS[r]) % K
def true_a(b, r): return (b - GENERATORS[r]) % K


# ---- minimal 1-hidden-layer softmax-CE MLP over (first_id in [0,K), rel_id in [0,NR)) -> K logits ----
class MLP:
    def __init__(self, rng):
        self.Efirst = rng.standard_normal((K, D)) * 0.1
        self.Erel = rng.standard_normal((NR, D)) * 0.1
        self.W1 = rng.standard_normal((2 * D, H)) * (1.0 / math.sqrt(2 * D))
        self.b1 = np.zeros(H)
        self.W2 = rng.standard_normal((H, K)) * (1.0 / math.sqrt(H))
        self.b2 = np.zeros(K)

    def _x(self, first, rel):
        return np.concatenate([self.Efirst[first], self.Erel[rel]], axis=1)  # [N,2D]

    def logits(self, first, rel):
        x = self._x(first, rel)
        h = np.tanh(x @ self.W1 + self.b1)
        return x, h, h @ self.W2 + self.b2

    def prob(self, first, rel):
        _, _, lg = self.logits(np.asarray(first), np.asarray(rel))
        lg -= lg.max(axis=1, keepdims=True)
        e = np.exp(lg)
        return e / e.sum(axis=1, keepdims=True)

    def fit(self, first, rel, tgt, epochs=EPOCHS, lr=LR):
        first = np.asarray(first); rel = np.asarray(rel); tgt = np.asarray(tgt)
        n = len(first)
        if n == 0:
            return
        for _ in range(epochs):
            x, h, lg = self.logits(first, rel)
            lg -= lg.max(axis=1, keepdims=True)
            e = np.exp(lg); p = e / e.sum(axis=1, keepdims=True)
            # label-smoothed CE gradient: target = (1-eps)*onehot + eps/K
            dlg = p - (LABEL_SMOOTH / K)
            dlg[np.arange(n), tgt] -= (1.0 - LABEL_SMOOTH)
            dlg /= n
            gW2 = h.T @ dlg + WD * self.W2; gb2 = dlg.sum(0)
            dh = (dlg @ self.W2.T) * (1 - h * h)
            gW1 = x.T @ dh + WD * self.W1; gb1 = dh.sum(0)
            gx = dh @ self.W1.T                                   # [n,2D]
            gEf = gx[:, :D]; gEr = gx[:, D:]
            self.W2 -= lr * gW2; self.b2 -= lr * gb2
            self.W1 -= lr * gW1; self.b1 -= lr * gb1
            for i in range(n):
                self.Efirst[first[i]] -= lr * gEf[i]
                self.Erel[rel[i]] -= lr * gEr[i]


def reach(model, cells):
    """ordered held-out reach: frac of cells whose argmax-b == true_b (model = forward A)."""
    if not cells:
        return 0.0
    firsts = [a for (a, r) in cells]; rels = [r for (a, r) in cells]
    p = model.prob(firsts, rels)
    pred = p.argmax(1)
    ok = sum(1 for i, (a, r) in enumerate(cells) if pred[i] == true_b(a, r))
    return ok / len(cells)


def train_forward(cells, rng):
    m = MLP(rng)
    m.fit([a for a, r in cells], [r for a, r in cells], [true_b(a, r) for a, r in cells])
    return m


def train_reverse(cells, rng, shuffle=False):
    """B predicts a from (b, rel). shuffle=edge-shuffled corpus -> rejection criterion meaningless."""
    m = MLP(rng)
    firsts = [true_b(a, r) for a, r in cells]; rels = [r for a, r in cells]
    tgts = [a for a, r in cells]
    if shuffle and tgts:
        perm = rng.permutation(len(tgts)); tgts = [tgts[i] for i in perm]
    m.fit(firsts, rels, tgts)
    return m


def run_debate(train, heldout, rng, mode):
    """mode: 'ab' | 'aonly' | 'shuffleB' | 'oracle'. Returns (reach, novel_fraction, valid_precision)."""
    train_set = set(train)
    A = train_forward(list(train_set), rng)
    B = train_reverse(list(train_set), rng, shuffle=(mode == "shuffleB")) if mode in ("ab", "shuffleB") else None
    survivors = []           # (a,r,b_hat)
    n_prop = 0; n_valid = 0
    for _ in range(ROUNDS):
        unseen = [c for c in ALL_CELLS if c not in train_set]
        if not unseen:
            break
        idx = rng.choice(len(unseen), size=min(PROPOSE_PER_ROUND, len(unseen)), replace=False)
        batch = [unseen[i] for i in idx]
        pa = A.prob([a for a, r in batch], [r for a, r in batch])
        new = []
        for j, (a, r) in enumerate(batch):
            pj = pa[j] / pa[j].sum()
            b_hat = int(rng.choice(K, p=pj))          # A PROPOSES BY SAMPLING (Fable design: 샘플링)
            accept = False
            if mode == "aonly":
                accept = True                          # no B (causal control)
            elif mode == "oracle":
                accept = (b_hat == true_b(a, r))       # validity oracle (upper bound)
            else:                                      # ab / shuffleB
                pb = B.prob([b_hat], [r])[0]
                top = int(pb.argmax()); srt = np.sort(pb)[::-1]
                margin = srt[0] - srt[1]
                accept = (top == a and margin >= TAU)
            if accept:
                n_prop += 1
                if b_hat == true_b(a, r):
                    n_valid += 1
                new.append((a, r, b_hat))
        for (a, r, b_hat) in new:
            train_set.add((a, r)); survivors.append((a, r, b_hat))
        # UPDATE both on train ∪ survivors (survivors use b_hat as pseudo-label)
        fa = [a for a, r in train] + [a for a, r, b in survivors]
        ra = [r for a, r in train] + [r for a, r, b in survivors]
        ta = [true_b(a, r) for a, r in train] + [b for a, r, b in survivors]
        A = MLP(rng); A.fit(fa, ra, ta)
        if mode in ("ab", "shuffleB"):
            fb = [true_b(a, r) for a, r in train] + [b for a, r, b in survivors]
            rb = [r for a, r in train] + [r for a, r, b in survivors]
            tb = [a for a, r in train] + [a for a, r, b in survivors]
            if mode == "shuffleB" and tb:
                perm = rng.permutation(len(tb)); tb = [tb[i] for i in perm]
            B = MLP(rng); B.fit(fb, rb, tb)
    novel_frac = (len(survivors) / max(1, n_prop)) if mode != "aonly" else (len(survivors) / max(1, ROUNDS * PROPOSE_PER_ROUND))
    valid_prec = (n_valid / max(1, n_prop))
    return reach(A, heldout), (len(survivors) / max(1, ROUNDS * PROPOSE_PER_ROUND)), valid_prec


def train_bidir_null(train, heldout, rng):
    """arm 4: single model on fwd+rev mixed corpus, equal compute (repackaging null)."""
    m = MLP(rng)
    fa = [a for a, r in train] + [true_b(a, r) for a, r in train]
    ra = [r for a, r in train] + [r for a, r in train]
    ta = [true_b(a, r) for a, r in train] + [a for a, r in train]
    m.fit(fa, ra, ta, epochs=EPOCHS * 2)   # equal-ish compute to A<->B two-model
    return reach(m, heldout)


def one_seed(seed):
    rng = np.random.default_rng(seed)
    n_train = int(round(COVERAGE * len(ALL_CELLS)))
    perm = rng.permutation(len(ALL_CELLS))
    train = [ALL_CELLS[i] for i in perm[:n_train]]
    heldout = [ALL_CELLS[i] for i in perm[n_train:]]
    r1 = reach(train_forward(train, np.random.default_rng(seed + 1)), heldout)      # CE-only
    r2, nf2, vp2 = run_debate(train, heldout, np.random.default_rng(seed + 2), "ab")
    r3, _, _ = run_debate(train, heldout, np.random.default_rng(seed + 3), "aonly")
    r4 = train_bidir_null(train, heldout, np.random.default_rng(seed + 4))
    r5, _, _ = run_debate(train, heldout, np.random.default_rng(seed + 5), "shuffleB")
    r6, _, _ = run_debate(train, heldout, np.random.default_rng(seed + 6), "oracle")
    return {"seed": seed, "n_train": n_train, "n_heldout": len(heldout),
            "reach": {"1_ce_only": round(r1, 4), "2_ab_debate": round(r2, 4),
                      "3_a_only": round(r3, 4), "4_bidir_null": round(r4, 4),
                      "5_shuffleB": round(r5, 4), "6_oracle": round(r6, 4)},
            "arm2_novel_fraction": round(nf2, 4), "arm2_valid_precision": round(vp2, 4)}


def main():
    results = [one_seed(s) for s in SEEDS]
    def g(k):  # per-arm reach across seeds
        return [r["reach"][k] for r in results]
    d21 = [results[i]["reach"]["2_ab_debate"] - results[i]["reach"]["1_ce_only"] for i in range(len(SEEDS))]
    bar_lift = sum(1 for x in d21 if x >= 0.15) >= 2                      # >=2/3 seeds
    m2 = float(np.mean(g("2_ab_debate")))
    bar_vs3 = (m2 - float(np.mean(g("3_a_only")))) >= 0.10
    bar_vs4 = (m2 - float(np.mean(g("4_bidir_null")))) >= 0.10
    bar_shuffle = float(np.mean(g("5_shuffleB"))) <= float(np.mean(g("1_ce_only"))) + 0.05
    bar_novel = float(np.mean([r["arm2_novel_fraction"] for r in results])) >= 0.5
    bars = {"lift>=0.15@2of3seeds": bar_lift, "ab>a_only+0.10": bar_vs3,
            "ab>bidir_null+0.10": bar_vs4, "shuffleB<=ce+0.05": bar_shuffle,
            "novel_fraction>=0.5": bar_novel}
    verdict = "DIRECTIONAL-GO" if all(bars.values()) else "KILL"
    out = {"probe": "ab_debate_recombination", "params": {"K": K, "generators": GENERATORS,
           "coverage": COVERAGE, "rounds": ROUNDS, "TAU": TAU, "seeds": SEEDS},
           "seeds": results, "frozen_bars": bars, "verdict": verdict,
           "decision": ("engine_g-as-B learning-loop worth engine-native 303M (E1 GPU-go path)"
                        if verdict == "DIRECTIONAL-GO" else
                        "A<->B rejection does not beat controls -> KILL -> G1 true ceiling stands (DPI)"),
           "scope": "toy with TRUE Z_K closure; real corpus closure is poor (F2 collocation-only, C5) -> 303M transfer ~80-85% kill even if toy GO (a_toy_scale_recheck)"}
    for r in results:
        rr = r["reach"]
        print(f"seed {r['seed']}: CE={rr['1_ce_only']:.2f} AB={rr['2_ab_debate']:.2f} Aonly={rr['3_a_only']:.2f} "
              f"bidir={rr['4_bidir_null']:.2f} shufB={rr['5_shuffleB']:.2f} oracle={rr['6_oracle']:.2f} "
              f"| novel={r['arm2_novel_fraction']:.2f} valid={r['arm2_valid_precision']:.2f}")
    print("FROZEN BARS:", json.dumps(bars))
    print("VERDICT:", verdict, "->", out["decision"])
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTDIR + "/RESULT.json", "w") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
