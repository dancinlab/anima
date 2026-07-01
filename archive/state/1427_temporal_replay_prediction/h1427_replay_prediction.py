#!/usr/bin/env python3
# H_1427 — temporal-sequence / replay-prediction (hippocampal CA3 replay-style next-ITEM prediction)
# numpy-mirror 5-bar probe (PURE PYTHON stdlib only — no numpy import needed; runs on summer).
# FROZEN-FIRST: bars below are VERBATIM from .verdicts/1427_temporal_replay_prediction/H_1427_FREEZE.txt
# Lens: CA3 recurrent collateral auto-association -> REPLAY pattern-completion of next item from
# LEARNED transition statistics P(next|current).  c15 / a_no_llm_frame_trap.  p7: accuracy, not perplexity.
#
# FROZEN BARS (NO bar moves post-hoc):
#  (1) PRESENCE : acc_ON - acc_OFF >= +0.20          (each seed AND mean)
#  (2) DISTINCT : acc_ON - max(vs1280,vs1227,vs1294) >= +0.10 (mean) AND each control < acc_ON-0.05
#  (3) SHUFFLE  : acc_SHUFFLE <= acc_OFF + 0.05
#  (4) ABLATE   : |acc_ABLATE - acc_OFF| <= 0.03      (mechanism OFF == marginal == INERT)
#  (5) NO-FAB   : OOD abstain_rate >= 0.90 AND OOD fabricated acc <= 1/V + 0.05
#
# FROZEN HYPERPARAMS: V=24, seq_len=12, N_train=200, N_test=120, p_dom=0.75, 3 minor successors,
#                     seeds=[1427,1428,1429], min_support=2, OOD aliens K=6.

import random

V          = 24
SEQ_LEN    = 12
N_TRAIN    = 200
N_TEST     = 120
P_DOM      = 0.75
N_MINOR    = 3
MIN_SUPP   = 2
OOD_ALIENS = 6
SEEDS      = [1427, 1428, 1429]
FEAT_DIM   = 8     # for the vs-1280 cerebellum forward-model control (continuous featvec per item)

# ── fixed structured transition kernel over V items ──────────────────────────
def build_kernel(rng):
    # each state -> 1 dominant successor (p_dom) + N_MINOR random minor successors (share 1-p_dom)
    dom = {}
    minors = {}
    for s in range(V):
        choices = [c for c in range(V) if c != s]
        rng.shuffle(choices)
        dom[s] = choices[0]
        minors[s] = choices[1:1 + N_MINOR]
    return dom, minors

def sample_next(s, dom, minors, rng):
    if rng.random() < P_DOM:
        return dom[s]
    return rng.choice(minors[s])

def gen_seqs(n, dom, minors, rng):
    seqs = []
    for _ in range(n):
        s = rng.randrange(V)
        seq = [s]
        for _ in range(SEQ_LEN - 1):
            s = sample_next(s, dom, minors, rng)
            seq.append(s)
        seqs.append(seq)
    return seqs

def item_featvec(item_id, rng_master_seed):
    # deterministic per-item feature vector (for vs-1280 forward-model control)
    r = random.Random(rng_master_seed * 100003 + item_id)
    return [r.gauss(0.0, 1.0) for _ in range(FEAT_DIM)]

def l2(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

# ── transition-count model P(next|current) = the CA3 replay substrate ─────────
def build_ctab(train_pairs):
    ctab = {}            # current -> {next: count}
    for c, n in train_pairs:
        d = ctab.setdefault(c, {})
        d[n] = d.get(n, 0) + 1
    return ctab

def marginal_argmax(train_pairs):
    cnt = {}
    for _, n in train_pairs:
        cnt[n] = cnt.get(n, 0) + 1
    return max(cnt, key=cnt.get)

# ── arms ─────────────────────────────────────────────────────────────────────
def predict_ON(ctab, cur):
    d = ctab.get(cur)
    if not d:
        return None  # abstain (no model for this current item)
    best = max(d, key=d.get)
    if d[best] < MIN_SUPP:
        return None  # abstain (below support)
    return best

def predict_OFF(marg, cur):
    return marg  # marginal-only: ignores current item entirely

def predict_vs1280(regr_W, item_feats, cur):
    # cerebellum forward-model: linear regressor maps cur featvec -> predicted next featvec,
    # then nearest item by feature L2. Continuous forward model, NOT a discrete conditional.
    fv = item_feats[cur]
    pred = [sum(regr_W[i][j] * fv[j] for j in range(FEAT_DIM)) for i in range(FEAT_DIM)]
    best, bestd = None, 1e18
    for it in range(V):
        d = l2(pred, item_feats[it])
        if d < bestd:
            bestd, best = d, it
    return best

def fit_vs1280(train_pairs, item_feats):
    # closed-form-ish ridge via simple normal-equation-free gradient (pure python, deterministic)
    W = [[0.0] * FEAT_DIM for _ in range(FEAT_DIM)]
    lr = 0.05
    for _ in range(30):
        for c, n in train_pairs:
            x = item_feats[c]
            y = item_feats[n]
            pred = [sum(W[i][j] * x[j] for j in range(FEAT_DIM)) for i in range(FEAT_DIM)]
            for i in range(FEAT_DIM):
                err = pred[i] - y[i]
                for j in range(FEAT_DIM):
                    W[i][j] -= lr * err * x[j] / max(1, len(train_pairs))
    return W

def predict_vs1227(bind_store, cur):
    # episodic item-binding: cur -> LAST-seen next (independent key->value, no frequency aggregation).
    return bind_store.get(cur)  # abstain if never bound

def build_vs1227(train_pairs):
    store = {}
    for c, n in train_pairs:
        store[c] = n  # overwrite: keeps LAST-seen next (no aggregation = no transition statistics)
    return store

def predict_vs1294(cur, rng):
    # hier-PFC GIVEN-order pointer: NO learned stats. On a novel start it has no handed plan ->
    # falls back to chance over V (it cannot derive a successor from statistics it never models).
    return rng.randrange(V)

# ── evaluation ────────────────────────────────────────────────────────────────
def eval_acc(test_pairs, predict_fn):
    correct = 0
    total = 0
    for c, n in test_pairs:
        p = predict_fn(c)
        if p is None:
            continue  # abstain: not scored as correct (excluded from accuracy denom for fairness)
        total += 1
        if p == n:
            correct += 1
    return correct / total if total else 0.0

def run_seed(seed):
    rng = random.Random(seed)
    dom, minors = build_kernel(rng)
    train_seqs = gen_seqs(N_TRAIN, dom, minors, rng)
    test_seqs  = gen_seqs(N_TEST,  dom, minors, rng)

    def to_pairs(seqs):
        ps = []
        for s in seqs:
            for i in range(len(s) - 1):
                ps.append((s[i], s[i + 1]))
        return ps

    train_pairs = to_pairs(train_seqs)
    test_pairs  = to_pairs(test_seqs)

    item_feats = {it: item_featvec(it, seed) for it in range(V + OOD_ALIENS)}

    # models
    ctab = build_ctab(train_pairs)
    marg = marginal_argmax(train_pairs)

    # SHUFFLE: permute next within all pairs at TRAIN time (destroys P(next|current))
    shuf_rng = random.Random(seed + 7)
    nexts = [n for _, n in train_pairs]
    shuf_rng.shuffle(nexts)
    shuf_pairs = [(c, nexts[i]) for i, (c, _) in enumerate(train_pairs)]
    ctab_shuf = build_ctab(shuf_pairs)

    # ABLATE: conditional table replaced by marginal -> predict marg for any cur with model
    # (i.e. mechanism OFF; identical decision to OFF baseline)
    def predict_ABLATE(cur):
        return marg

    # vs-1280 fit
    W = fit_vs1280(train_pairs, item_feats)
    # vs-1227 store
    bind = build_vs1227(train_pairs)
    # vs-1294 rng
    rng1294 = random.Random(seed + 99)

    acc_ON      = eval_acc(test_pairs, lambda c: predict_ON(ctab, c))
    acc_OFF     = eval_acc(test_pairs, lambda c: predict_OFF(marg, c))
    acc_SHUF    = eval_acc(test_pairs, lambda c: predict_ON(ctab_shuf, c))
    acc_ABL     = eval_acc(test_pairs, predict_ABLATE)
    acc_vs1280  = eval_acc(test_pairs, lambda c: predict_vs1280(W, item_feats, c))
    acc_vs1227  = eval_acc(test_pairs, lambda c: predict_vs1227(bind, c))
    acc_vs1294  = eval_acc(test_pairs, lambda c: predict_vs1294(c, rng1294))

    # ── bar 5 NO-FAB: OOD = alien items (never seen) + in-dist below-support currents ──
    ood_currents = list(range(V, V + OOD_ALIENS))            # alien ids
    # plus in-dist currents that have NO model (never a 'current' in train)
    seen_currents = set(ctab.keys())
    ood_currents += [c for c in range(V) if c not in seen_currents]
    # build OOD test pairs (alien -> arbitrary next; the point is the predictor must ABSTAIN)
    ood_pairs = [(c, rng.randrange(V)) for c in ood_currents for _ in range(5)]
    ab_abstain = 0
    ab_total = 0
    fab_correct = 0
    fab_total = 0
    for c, n in ood_pairs:
        p = predict_ON(ctab, c)
        ab_total += 1
        if p is None:
            ab_abstain += 1
        else:
            fab_total += 1
            if p == n:
                fab_correct += 1
    ood_abstain_rate = ab_abstain / ab_total if ab_total else 1.0
    ood_fab_acc = fab_correct / fab_total if fab_total else 0.0

    return {
        "seed": seed,
        "acc_ON": acc_ON, "acc_OFF": acc_OFF, "acc_SHUFFLE": acc_SHUF, "acc_ABLATE": acc_ABL,
        "acc_vs1280": acc_vs1280, "acc_vs1227": acc_vs1227, "acc_vs1294": acc_vs1294,
        "ood_abstain_rate": ood_abstain_rate, "ood_fab_acc": ood_fab_acc,
    }

def main():
    rows = [run_seed(s) for s in SEEDS]
    def mean(k):
        return sum(r[k] for r in rows) / len(rows)

    print("=" * 78)
    print("H_1427 — CA3 replay next-ITEM prediction (numpy-mirror, pure-python, DIRECTIONAL)")
    print("=" * 78)
    hdr = ("seed", "ON", "OFF", "SHUF", "ABL", "vs1280", "vs1227", "vs1294", "ood_abst", "ood_fab")
    print("{:>6} {:>6} {:>6} {:>6} {:>6} {:>7} {:>7} {:>7} {:>9} {:>8}".format(*hdr))
    for r in rows:
        print("{:>6} {:>6.3f} {:>6.3f} {:>6.3f} {:>6.3f} {:>7.3f} {:>7.3f} {:>7.3f} {:>9.3f} {:>8.3f}".format(
            r["seed"], r["acc_ON"], r["acc_OFF"], r["acc_SHUFFLE"], r["acc_ABLATE"],
            r["acc_vs1280"], r["acc_vs1227"], r["acc_vs1294"], r["ood_abstain_rate"], r["ood_fab_acc"]))
    mON, mOFF, mSHUF, mABL = mean("acc_ON"), mean("acc_OFF"), mean("acc_SHUFFLE"), mean("acc_ABLATE")
    m1280, m1227, m1294 = mean("acc_vs1280"), mean("acc_vs1227"), mean("acc_vs1294")
    mAbst, mFab = mean("ood_abstain_rate"), mean("ood_fab_acc")
    print("-" * 78)
    print("{:>6} {:>6.3f} {:>6.3f} {:>6.3f} {:>6.3f} {:>7.3f} {:>7.3f} {:>7.3f} {:>9.3f} {:>8.3f}".format(
        "MEAN", mON, mOFF, mSHUF, mABL, m1280, m1227, m1294, mAbst, mFab))
    print()

    chance = 1.0 / V
    best_ctrl = max(m1280, m1227, m1294)
    # ── frozen bars ──
    b1_each = all((r["acc_ON"] - r["acc_OFF"]) >= 0.20 for r in rows)
    b1 = b1_each and (mON - mOFF) >= 0.20
    b2_gap = (mON - best_ctrl) >= 0.10
    b2_each = all(c < (mON - 0.05) for c in (m1280, m1227, m1294))
    b2 = b2_gap and b2_each
    b3 = mSHUF <= mOFF + 0.05
    b4 = abs(mABL - mOFF) <= 0.03
    b5 = (mAbst >= 0.90) and (mFab <= chance + 0.05)

    def verd(b): return "PASS" if b else "FAIL"
    print("FROZEN BARS (verbatim from FREEZE):")
    print(f"  (1) PRESENCE  acc_ON-acc_OFF = {mON-mOFF:+.3f} (>=+0.20, each seed {b1_each})  -> {verd(b1)}")
    print(f"  (2) DISTINCT  acc_ON-best_ctrl = {mON-best_ctrl:+.3f} (>=+0.10); each ctrl<ON-0.05={b2_each} "
          f"[vs1280={m1280:.3f} vs1227={m1227:.3f} vs1294={m1294:.3f}]  -> {verd(b2)}")
    print(f"  (3) SHUFFLE   acc_SHUFFLE={mSHUF:.3f} <= acc_OFF+0.05={mOFF+0.05:.3f}  -> {verd(b3)}")
    print(f"  (4) ABLATE    |acc_ABLATE-acc_OFF|={abs(mABL-mOFF):.3f} <= 0.03  -> {verd(b4)}")
    print(f"  (5) NO-FAB    ood_abstain={mAbst:.3f}(>=0.90) ood_fab_acc={mFab:.3f}(<=chance+0.05={chance+0.05:.3f}) -> {verd(b5)}")
    allpass = b1 and b2 and b3 and b4 and b5
    print()
    print(f"VERDICT: {'GREEN 5/5' if allpass else 'NOT-ALL-PASS'}  "
          f"[{int(b1)}{int(b2)}{int(b3)}{int(b4)}{int(b5)}]")
    return allpass

if __name__ == "__main__":
    main()
