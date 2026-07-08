#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Premise-swap verifier toy (owner "가 구현" · Fable GO-TOY): does a corpus-OUTSIDE deterministic
verifier escape the G1 DPI ceiling that all 5 in-corpus axes hit?

DPI ceiling (proven this session): learning signal = f(corpus); I(model;truth) <= I(corpus;truth);
static corpus carries 0 bit of bind-vs-retrieval info (F2 novel n=0) -> no in-corpus signal
(incl. A<->B debate) beats 0. THE non-dominated escape (Fable, info-theoretic): a DETERMINISTIC
verifier is a SEPARATE truth-channel — each accept/reject bit is a function of ground truth, not the
corpus -> injects I(.;truth) the corpus lacks. p6-safe (fact, not learned reward; AlphaZero game-rule
class), p7-safe (exact checker = property's definition, Goodhart gap 0; eval-only cells NEVER queried),
p8-literal (learn-during-interaction).

Verifier here = the Z_K group-law exact check (b == (a+g[r]) mod K) treated as a BUDGETED query
channel (corpus-outside execution fact). Differs from the ab_debate ORACLE arm (which floored at 0.06)
in the 3 ways Fable identified: (i) k-sample SEARCH per cell (oracle = argmax 1-candidate), (ii) negative
feedback (rejected b excluded, resample), (iii) query BUDGET. 0.06 was the "filter-only ceiling", not
"verifier useless" — ARM7 tests whether SEARCH breaks it.

3-partition FIREWALL (anti-leakage): train (initial CE) · queryable (verifier may be queried) ·
EVAL-ONLY (verifier can NEVER query — the frozen bar is measured HERE = genuine generalization of the
group law from verifier-labeled cells, not memorization of verifier answers).

ARMS: (1) CE-only [floor]  (7) A-proposal + budgeted verifier + resample
      (8a) random-proposal + verifier, same budget [does A-guidance add over active labeling?]
      (8b) corpus-extension null: add |solved| TRUE cells directly [verifier~=this => 'buying corpus']

FROZEN BARS (pre-registered · immutable · p7): GO iff
  reach(ARM7, EVAL-ONLY) - reach(CE, EVAL-ONLY) >= +0.15 on >=2/3 seeds  AND
  reach(ARM7) > reach(ARM8a random) + 0.10.
Any fail = KILL (interaction/verifier does not escape at toy scale). DIRECTIONAL (a_toy_scale_recheck).
"""
import json, os, math
import numpy as np

K = 24
D = 64
H = 128
GENERATORS = [1, 2, 3, 5, 7, 11]
NR = len(GENERATORS)
EPOCHS = 150
LR = 0.5
WD = 0.02
LABEL_SMOOTH = 0.15
ROUNDS = 12
K_SAMPLE = 4              # candidates A proposes per queryable cell
QUERY_BUDGET = 160        # verifier queries per round (budgeted truth-channel)
TEMP = 2.0               # proposal temperature (exploration)
SEEDS = [7, 4302, 4303]
OUTDIR = "/Users/mini/dancinlab/anima/state/ab_debate_recombination"

ALL_CELLS = [(a, r) for a in range(K) for r in range(NR)]
def true_b(a, r): return (a + GENERATORS[r]) % K


class MLP:
    def __init__(self, rng):
        self.Efirst = rng.standard_normal((K, D)) * 0.1
        self.Erel = rng.standard_normal((NR, D)) * 0.1
        self.W1 = rng.standard_normal((2 * D, H)) * (1.0 / math.sqrt(2 * D))
        self.b1 = np.zeros(H)
        self.W2 = rng.standard_normal((H, K)) * (1.0 / math.sqrt(H))
        self.b2 = np.zeros(K)

    def _x(self, first, rel):
        return np.concatenate([self.Efirst[first], self.Erel[rel]], axis=1)

    def prob(self, first, rel):
        x = self._x(np.asarray(first), np.asarray(rel))
        lg = np.tanh(x @ self.W1 + self.b1) @ self.W2 + self.b2
        lg -= lg.max(axis=1, keepdims=True)
        e = np.exp(lg)
        return e / e.sum(axis=1, keepdims=True)

    def fit(self, first, rel, tgt, epochs=EPOCHS):
        first = np.asarray(first); rel = np.asarray(rel); tgt = np.asarray(tgt)
        n = len(first)
        if n == 0:
            return
        for _ in range(epochs):
            x = self._x(first, rel)
            h = np.tanh(x @ self.W1 + self.b1)
            lg = h @ self.W2 + self.b2
            lg -= lg.max(axis=1, keepdims=True)
            e = np.exp(lg); p = e / e.sum(axis=1, keepdims=True)
            dlg = p - (LABEL_SMOOTH / K)
            dlg[np.arange(n), tgt] -= (1.0 - LABEL_SMOOTH)
            dlg /= n
            gW2 = h.T @ dlg + WD * self.W2; gb2 = dlg.sum(0)
            dh = (dlg @ self.W2.T) * (1 - h * h)
            gW1 = x.T @ dh + WD * self.W1; gb1 = dh.sum(0)
            gx = dh @ self.W1.T
            self.W2 -= LR * gW2; self.b2 -= LR * gb2
            self.W1 -= LR * gW1; self.b1 -= LR * gb1
            gEf = gx[:, :D]; gEr = gx[:, D:]
            for i in range(n):
                self.Efirst[first[i]] -= LR * gEf[i]
                self.Erel[rel[i]] -= LR * gEr[i]


def reach(model, cells):
    if not cells:
        return 0.0
    p = model.prob([a for a, r in cells], [r for a, r in cells])
    pred = p.argmax(1)
    return sum(1 for i, (a, r) in enumerate(cells) if pred[i] == true_b(a, r)) / len(cells)


def fit_on(cells_bmap, rng):
    """cells_bmap: dict (a,r)->b (b = true or verifier-confirmed pseudo-label)."""
    m = MLP(rng)
    ks = list(cells_bmap.keys())
    m.fit([a for a, r in ks], [r for a, r in ks], [cells_bmap[k] for k in ks])
    return m


def run_verifier(train, queryable, eval_only, rng, mode):
    """mode: 'ce' | 'verifier' | 'random' | 'corpusnull'. reach measured on eval_only (never queried)."""
    solved = {(a, r): true_b(a, r) for (a, r) in train}       # (a,r)->b
    A = fit_on(solved, rng)
    if mode == "ce":
        return reach(A, eval_only), 0
    n_added = 0
    excluded = {}                                             # (a,r) -> set of rejected b (negative feedback)
    for _ in range(ROUNDS):
        budget = QUERY_BUDGET
        pool = [c for c in queryable if c not in solved]
        rng.shuffle(pool)
        if mode == "corpusnull":
            # buy |per-round-quota| TRUE cells directly, no verifier search (upper-null)
            quota = min(QUERY_BUDGET // K_SAMPLE, len(pool))
            for (a, r) in pool[:quota]:
                solved[(a, r)] = true_b(a, r); n_added += 1
            A = fit_on(solved, rng); continue
        pa = A.prob([a for a, r in pool], [r for a, r in pool]) if pool else None
        for j, (a, r) in enumerate(pool):
            if budget <= 0:
                break
            bad = excluded.get((a, r), set())
            for _k in range(K_SAMPLE):
                if budget <= 0:
                    break
                if mode == "random":
                    b_hat = int(rng.integers(K))
                else:                                         # 'verifier' = A temperature-proposal
                    pj = pa[j] ** (1.0 / TEMP); pj = pj / pj.sum()
                    b_hat = int(rng.choice(K, p=pj))
                if b_hat in bad:
                    continue
                budget -= 1                                   # one verifier query
                if b_hat == true_b(a, r):                     # deterministic verifier (execution fact)
                    solved[(a, r)] = b_hat; n_added += 1; break
                else:
                    bad.add(b_hat)                            # negative feedback -> resample
            excluded[(a, r)] = bad
        A = fit_on(solved, rng)
    return reach(A, eval_only), n_added


def one_seed(seed):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(ALL_CELLS))
    n = len(ALL_CELLS); n_tr = int(round(0.30 * n)); n_ev = int(round(0.30 * n))
    train = [ALL_CELLS[i] for i in perm[:n_tr]]
    eval_only = [ALL_CELLS[i] for i in perm[n_tr:n_tr + n_ev]]      # NEVER queried by verifier
    queryable = [ALL_CELLS[i] for i in perm[n_tr + n_ev:]]
    r_ce, _ = run_verifier(train, queryable, eval_only, np.random.default_rng(seed + 1), "ce")
    r7, add7 = run_verifier(train, queryable, eval_only, np.random.default_rng(seed + 2), "verifier")
    r8a, _ = run_verifier(train, queryable, eval_only, np.random.default_rng(seed + 3), "random")
    r8b, _ = run_verifier(train, queryable, eval_only, np.random.default_rng(seed + 4), "corpusnull")
    return {"seed": seed, "n_train": n_tr, "n_eval_only": n_ev, "n_queryable": len(queryable),
            "reach_eval_only": {"1_ce": round(r_ce, 4), "7_verifier": round(r7, 4),
                                "8a_random": round(r8a, 4), "8b_corpusnull": round(r8b, 4)},
            "arm7_cells_added": add7}


def main():
    res = [one_seed(s) for s in SEEDS]
    def g(k): return [r["reach_eval_only"][k] for r in res]
    d = [res[i]["reach_eval_only"]["7_verifier"] - res[i]["reach_eval_only"]["1_ce"] for i in range(len(SEEDS))]
    bar_lift = sum(1 for x in d if x >= 0.15) >= 2
    bar_vs_random = (float(np.mean(g("7_verifier"))) - float(np.mean(g("8a_random")))) >= 0.10
    bars = {"verifier-CE>=+0.15@2of3(eval-only)": bar_lift, "verifier>random+0.10": bar_vs_random}
    verdict = "GO-DIRECTIONAL" if all(bars.values()) else "KILL"
    out = {"probe": "premise_verifier", "params": {"K": K, "generators": GENERATORS, "K_SAMPLE": K_SAMPLE,
           "QUERY_BUDGET": QUERY_BUDGET, "ROUNDS": ROUNDS, "TEMP": TEMP, "seeds": SEEDS,
           "firewall": "eval_only cells NEVER queried by verifier (no label leakage)"},
           "seeds": res, "frozen_bars": bars, "verdict": verdict,
           "decision": ("corpus-outside deterministic verifier ESCAPES the DPI ceiling (search breaks the "
                        "0.06 filter-only oracle bound) -> engine-native path: execution-verifier lane"
                        if verdict == "GO-DIRECTIONAL" else
                        "verifier does not beat controls at toy scale -> escape not demonstrated here"),
           "scope": "toy Z_K closure + exact group-law verifier; real domains need a real deterministic "
                    "checker (code exec / equation / SAT); a_toy_scale_recheck. oracle 0.06 = filter-only bound."}
    for r in res:
        rr = r["reach_eval_only"]
        print(f"seed {r['seed']}: CE={rr['1_ce']:.2f} VERIFIER={rr['7_verifier']:.2f} "
              f"random={rr['8a_random']:.2f} corpusnull={rr['8b_corpusnull']:.2f} | arm7_added={r['arm7_cells_added']}")
    print("FROZEN BARS:", json.dumps(bars))
    print("VERDICT:", verdict, "->", out["decision"])
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTDIR + "/VERIFIER_RESULT.json", "w") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
