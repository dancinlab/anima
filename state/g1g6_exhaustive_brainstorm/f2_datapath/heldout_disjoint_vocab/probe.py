#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F2 heldout_disjoint_vocab — the one $0 tiebreaker that forks the data-axis decision
(F2_SYNTHESIS.md "The one $0 tiebreaker that forks the decision").

Question (surface analog of the G1 held-out recombination test, still $0 numpy):
  consciousness_anchor content-word order signal is REAL & POWERED (n=49, differ_frac 0.959)
  but is it COMPOSITIONAL/GENERALIZABLE or just MEMORIZED IN-DISTRIBUTION COLLOCATION?
  Split the corpus into TRAIN / HELDOUT text halves and the content vocab into two
  frequency-parity halves. Learn seen adjacent pairs on TRAIN. On HELDOUT, test whether
  NOVEL cross-half pairs (a in HALF_A, b in HALF_B, sorted-key NEVER seen adjacent in TRAIN)
  carry the same order-distinguishing follower asymmetry.
    - novel pairs carry order signal (real >> shuffle-null) -> order GENERALIZES -> F2 real
      lever -> E1 GPU-go on the anchor content-word recipe (pool, frozen-first).
    - only seen collocations carry it (novel collapses / underpowered) -> memorized collocation
      -> F2 collocation-only confirmed -> data axis stays terminal (H_9121/H_9127) -> pivot.

Metric reference-matched to content_word_tiebreaker/probe.py (the E1 gate mechanism):
  whitespace tokens; content vocab = drop top-50 freq-stoplist + wordlike + top-400 remainder;
  ordered adjacent in-vocab pair (a,b) a!=b, follower = t_{i+2};
  unordered {a,b} QUALIFIED iff both orders >= MIN_OCC in HELDOUT;
  differ = top-follower(a,b) != top-follower(b,a); differ_frac = frac qualified that differ.
Controls (why this is not the differ-is-high-by-chance artifact):
  SHUFFLE-NULL: reassign every heldout follower by sampling (seeded) from the global heldout
  follower multiset, keeping per-pair occurrence counts; recompute differ_frac on the SAME
  novel-cross-half pairs. A real generalizing order signal => real_frac - shuffle_frac >= MARGIN.
  (differ_frac alone is high even for random small samples, so the null is mandatory.)
Frozen bars (no tune-to-green, p7): MIN_OCC=3, POWER=10, FRAC_BAR=2/3, MARGIN=0.20.
DIRECTIONAL numpy probe (a_toy_scale_recheck): forks GPU-go, does NOT cement a tier.
"""
import json, re, os, random
from collections import Counter, defaultdict

MIN_OCC = 3
TOP_VOCAB = 400
DROP_TOP = 50
POWER = 10
FRAC_BAR = 2.0 / 3.0
MARGIN = 0.20
SEED = 7
N_SHUFFLE = 20

REPO = "/Users/mini/dancinlab/anima"
ANCHOR = REPO + "/archive/state_legacy/anima_phase1a1_color_cosmology_2026_05_12/consciousness_anchor.txt"
OUTDIR = REPO + "/state/g1g6_exhaustive_brainstorm/f2_datapath/heldout_disjoint_vocab"

LETTER = re.compile(r"[A-Za-z가-힣一-鿿]")


def wordlike(tok):
    if len(tok) < 2:
        return False
    if tok.endswith(":"):
        return False
    letters = LETTER.findall(tok)
    if len(letters) < 2:
        return False
    nonletter = sum(1 for c in tok if not LETTER.match(c))
    if nonletter > len(letters):
        return False
    if tok.startswith("\\"):
        return False
    return True


def tokenize(p):
    t = []
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            t.extend(line.split())
    return t


def seen_pairs(toks, vocab):
    """Sorted-key set of adjacent in-vocab pairs actually seen in TRAIN text."""
    s = set()
    for i in range(len(toks) - 1):
        a, b = toks[i], toks[i + 1]
        if a in vocab and b in vocab and a != b:
            s.add(tuple(sorted((a, b))))
    return s


def collect(toks, vocab):
    """pair_count and pair_follow over adjacent in-vocab pairs of one text span."""
    pair_follow = defaultdict(Counter)
    pair_count = Counter()
    followers = []
    n = len(toks)
    for i in range(n - 1):
        a, b = toks[i], toks[i + 1]
        if a in vocab and b in vocab and a != b:
            pair_count[(a, b)] += 1
            if i + 2 < n:
                f = toks[i + 2]
                pair_follow[(a, b)][f] += 1
                followers.append(f)
    return pair_count, pair_follow, followers


def qualified_keys(pair_count, key_filter):
    """Unordered {a,b} qualified (both orders >= MIN_OCC) passing key_filter(key,(a,b))."""
    out = []
    seen = set()
    for (a, b) in list(pair_count.keys()):
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        if pair_count[(a, b)] >= MIN_OCC and pair_count[(b, a)] >= MIN_OCC:
            if key_filter(key, a, b):
                seen.add(key)
                out.append((key, a, b))
    return out


def differ_frac(keys, pair_follow):
    n_diff = 0
    ex = []
    for (key, a, b) in keys:
        tf_ab = pair_follow[(a, b)].most_common(1)
        tf_ba = pair_follow[(b, a)].most_common(1)
        f_ab = tf_ab[0][0] if tf_ab else None
        f_ba = tf_ba[0][0] if tf_ba else None
        d = (f_ab != f_ba)
        if d:
            n_diff += 1
        if len(ex) < 15:
            ex.append({"pair": list(key), "f_ab": f_ab, "f_ba": f_ba, "differ": d})
    frac = (n_diff / len(keys)) if keys else 0.0
    return frac, n_diff, ex


def shuffle_null(keys, pair_count, global_followers, rng):
    """Reassign every follower slot from the global follower multiset; differ_frac over keys."""
    fracs = []
    pool = list(global_followers)
    for _ in range(N_SHUFFLE):
        rng.shuffle(pool)
        idx = 0
        pf = defaultdict(Counter)
        # rebuild followers per ordered pair, sampling from the shuffled pool in order
        for (key, a, b) in keys:
            for (x, y) in ((a, b), (b, a)):
                c = pair_count[(x, y)]
                for _k in range(c):
                    if idx < len(pool):
                        pf[(x, y)][pool[idx]] += 1
                        idx += 1
        f, _, _ = differ_frac(keys, pf)
        fracs.append(f)
    return sum(fracs) / len(fracs) if fracs else 0.0


def main():
    rng = random.Random(SEED)
    toks = tokenize(ANCHOR)
    n = len(toks)
    freq = Counter(toks)
    ranked = [w for w, _ in freq.most_common()]
    stop = set(ranked[:DROP_TOP])
    content_ranked = [w for w in ranked if w not in stop and wordlike(w)]
    vocab = set(content_ranked[:TOP_VOCAB])
    # frequency-parity vocab halves (disjoint): rank-even -> A, rank-odd -> B
    half_a = set(w for i, w in enumerate(content_ranked[:TOP_VOCAB]) if i % 2 == 0)
    half_b = set(w for i, w in enumerate(content_ranked[:TOP_VOCAB]) if i % 2 == 1)

    mid = n // 2
    train, heldout = toks[:mid], toks[mid:]
    train_seen = seen_pairs(train, vocab)
    hp_count, hp_follow, hp_followers = collect(heldout, vocab)

    def cross_half(key, a, b):
        return (a in half_a and b in half_b) or (a in half_b and b in half_a)

    def cross_half_novel(key, a, b):
        return cross_half(key, a, b) and key not in train_seen

    def cross_half_seen(key, a, b):
        return cross_half(key, a, b) and key in train_seen

    novel_keys = qualified_keys(hp_count, cross_half_novel)
    seen_keys = qualified_keys(hp_count, cross_half_seen)

    nf, nd, nex = differ_frac(novel_keys, hp_follow)
    sf, sd, sex = differ_frac(seen_keys, hp_follow)
    null_novel = shuffle_null(novel_keys, hp_count, hp_followers, rng) if novel_keys else 0.0

    n_novel = len(novel_keys)
    generalizes = (n_novel >= POWER and nf >= FRAC_BAR and (nf - null_novel) >= MARGIN)
    if n_novel < POWER:
        verdict = "INCONCLUSIVE-SPARSE"
    elif generalizes:
        verdict = "ORDER-GENERALIZES"
    else:
        verdict = "COLLOCATION-ONLY"

    decision = {
        "ORDER-GENERALIZES": "F2 real lever -> E1 GPU-go (anchor content-word recipe, pool, frozen-first)",
        "COLLOCATION-ONLY": "memorized collocation -> data axis TERMINAL (H_9121/H_9127) -> pivot H_6163 falsifier-lane",
        "INCONCLUSIVE-SPARSE": "novel cross-half pairs underpowered (n<10) -> cannot clear -> data axis stays terminal, no GPU-go",
    }[verdict]

    out = {
        "probe": "heldout_disjoint_vocab",
        "corpus": ANCHOR,
        "params": {"MIN_OCC": MIN_OCC, "TOP_VOCAB": TOP_VOCAB, "DROP_TOP": DROP_TOP,
                   "POWER": POWER, "FRAC_BAR": round(FRAC_BAR, 4), "MARGIN": MARGIN,
                   "SEED": SEED, "N_SHUFFLE": N_SHUFFLE},
        "n_tokens": n, "train_tokens": len(train), "heldout_tokens": len(heldout),
        "vocab_size": len(vocab), "half_a": len(half_a), "half_b": len(half_b),
        "train_seen_pairs": len(train_seen),
        "novel_cross_half": {"n_qualified": n_novel, "differ_frac": round(nf, 4),
                             "shuffle_null_frac": round(null_novel, 4),
                             "real_minus_null": round(nf - null_novel, 4), "examples": nex},
        "seen_cross_half_reference": {"n_qualified": len(seen_keys), "differ_frac": round(sf, 4),
                                      "examples": sex},
        "verdict": verdict, "decision": decision,
        "scope_caveat": "single synthetic legacy corpus (consciousness_anchor); DIRECTIONAL numpy probe forks GPU-go, does not cement a tier (a_toy_scale_recheck)",
    }
    print(f"heldout_disjoint_vocab | tok={n:,} train_seen_pairs={len(train_seen)} vocab={len(vocab)} (A={len(half_a)} B={len(half_b)})")
    print(f"  NOVEL cross-half : n={n_novel:>3} differ_frac={nf:.3f} shuffle_null={null_novel:.3f} real-null={nf-null_novel:+.3f}")
    print(f"  SEEN  cross-half : n={len(seen_keys):>3} differ_frac={sf:.3f}  (reference: seen collocations should carry signal)")
    print(f"  VERDICT: {verdict} -> {decision}")
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTDIR + "/RESULT.json", "w") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
