#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F2 datapath cell = relation_typed.  $0 corpus statistic (numpy/re/collections).
NO model load.  Reference-matches the E1 order-distinguishing gate.

E1 gate (verbatim from task spec; reference impl e1_pregate/gate.py stale/absent):
  For ordered ADJACENT concept pairs (a,b), compare the top-follower token of
  (a,b) vs the top-follower of the reversed (b,a).  A pair is QUALIFIED iff BOTH
  orders occur >= MIN_OCC (3) times, a != b.  differ_frac = fraction of qualified
  pairs where top-follower(a,b) != top-follower(b,a).
  NON-DEGENERATE iff differ_frac >= 2/3 AND n_qualified >= 10 (powered).
  Underpowered (n<10) => INCONCLUSIVE-SPARSE.

THIS CELL:  On corpus.txt, contrast
  RAW   : bare adjacency   a b            (E1 baseline, concepts consecutive)
  TYPED : relation-typed    a <conn> b     (conn = short function/relation token,
          1 or 2 tokens, from a fixed connector set)
Question: does the ORDER signal live in TYPED relations rather than bare
adjacency?  Report n_qualified for TYPED vs RAW.

Vocab: rebuilt from THE SAME corpus by frequency (top-400), NOT hand-picked
(per hard rule).  Connectors are a fixed function/relation set (methodological,
not concept hand-pick).
"""
import json, re
from collections import Counter, defaultdict

REPO = "/Users/mini/dancinlab/anima"
CORPUS = f"{REPO}/archive/data/corpus.txt"
OUT = f"{REPO}/state/g1g6_exhaustive_brainstorm/f2_datapath/relation_typed/RESULT.json"

MIN_OCC = 3
POWERED = 10
DIFFER_BAR = 2.0/3.0
TOPN_VOCAB = 400

CONN1 = {
    "is","are","was","were","be","been","being","of","in","to","has","have","had",
    "on","at","for","with","as","by","a","an","the","and","or","that","from","into",
    "about","over","under","between","through","like","makes","make","gives","give",
    "means","causes","cause","becomes","become","needs","need","uses","use","feels",
    "feel","seems","seem","holds","hold","carries","carry","drives","drive","not",
}
CONN2 = {
    ("is","a"),("is","the"),("is","not"),("is","an"),("is","just"),("is","more"),
    ("leads","to"),("part","of"),("kind","of"),("more","than"),("out","of"),
    ("based","on"),("bound","to"),("has","a"),("has","the"),("can","be"),
    ("has","to"),("able","to"),("form","of"),("sort","of"),("results","in"),
}


def tokenize(text):
    return re.findall(r"[0-9a-zA-Z가-힣]+", text.lower())


def build_vocab(toks, n):
    c = Counter(toks)
    return set(w for w, _ in c.most_common(n)), c


def gate(ordered_pairs_followers):
    top = {}
    occ = {}
    for pr, fc in ordered_pairs_followers.items():
        occ[pr] = sum(fc.values())
        top[pr] = fc.most_common(1)[0][0] if fc else None
    qualified = []
    for (a, b) in ordered_pairs_followers:
        if a == b:
            continue
        rev = (b, a)
        if rev in occ and occ[(a, b)] >= MIN_OCC and occ[rev] >= MIN_OCC:
            if (b, a) < (a, b):
                continue
            qualified.append((a, b))
    n_q = len(qualified)
    differ = 0
    examples = []
    for (a, b) in qualified:
        t_ab, t_ba = top[(a, b)], top[(b, a)]
        d = (t_ab != t_ba)
        if d:
            differ += 1
        if len(examples) < 15:
            examples.append({
                "a": a, "b": b,
                "occ_ab": occ[(a, b)], "occ_ba": occ[(b, a)],
                "top_ab": t_ab, "top_ba": t_ba, "differs": d,
            })
    frac = (differ / n_q) if n_q else 0.0
    return n_q, round(frac, 4), differ, examples


def collect(toks, vocab):
    raw = defaultdict(Counter)
    typed = defaultdict(Counter)
    typed_by_conn = defaultdict(lambda: defaultdict(Counter))
    n = len(toks)
    for i in range(n - 1):
        a = toks[i]
        if a not in vocab:
            continue
        b = toks[i + 1]
        if b in vocab and i + 2 < n:
            raw[(a, b)][toks[i + 2]] += 1
        c1 = toks[i + 1]
        if c1 in CONN1 and i + 3 < n:
            b2 = toks[i + 2]
            if b2 in vocab and b2 != a:
                typed[(a, b2)][toks[i + 3]] += 1
                typed_by_conn[c1][(a, b2)][toks[i + 3]] += 1
        if i + 4 < n:
            c2pair = (toks[i + 1], toks[i + 2])
            if c2pair in CONN2:
                b3 = toks[i + 3]
                if b3 in vocab and b3 != a:
                    typed[(a, b3)][toks[i + 4]] += 1
                    key = " ".join(c2pair)
                    typed_by_conn[key][(a, b3)][toks[i + 4]] += 1
    return raw, typed, typed_by_conn


def main():
    text = open(CORPUS, "r", encoding="utf-8", errors="replace").read()
    toks = tokenize(text)
    vocab, freq = build_vocab(toks, TOPN_VOCAB)

    raw, typed, typed_by_conn = collect(toks, vocab)

    nq_raw, df_raw, dd_raw, ex_raw = gate(raw)
    nq_typed, df_typed, dd_typed, ex_typed = gate(typed)

    per_conn = {}
    for conn, d in sorted(typed_by_conn.items()):
        nq, df, dd, _ = gate(d)
        per_conn[conn] = {"n_qualified": nq, "differ_frac": df,
                          "total_ordered_pairs": len(d)}
    per_conn_top = dict(sorted(per_conn.items(),
                               key=lambda kv: kv[1]["n_qualified"],
                               reverse=True)[:12])

    def verdict(nq, df):
        if nq < POWERED:
            return "INCONCLUSIVE-SPARSE"
        return "NON-DEGENERATE-POWERED" if df >= DIFFER_BAR else "DEGENERATE-POWERED"

    out = {
        "cell": "relation_typed",
        "corpus": CORPUS,
        "n_tokens": len(toks),
        "vocab_size": len(vocab),
        "vocab_build": "top-400 by frequency from corpus.txt (no hand-pick)",
        "MIN_OCC": MIN_OCC, "POWERED_THRESHOLD": POWERED, "DIFFER_BAR": DIFFER_BAR,
        "RAW_adjacency": {
            "n_ordered_pairs": len(raw),
            "n_qualified": nq_raw,
            "differ_frac": df_raw,
            "n_differ": dd_raw,
            "verdict": verdict(nq_raw, df_raw),
            "examples": ex_raw,
        },
        "TYPED_relation": {
            "n_ordered_pairs": len(typed),
            "n_qualified": nq_typed,
            "differ_frac": df_typed,
            "n_differ": dd_typed,
            "verdict": verdict(nq_typed, df_typed),
            "examples": ex_typed,
        },
        "per_connector_top12": per_conn_top,
        "comparison": {
            "typed_minus_raw_n_qualified": nq_typed - nq_raw,
            "order_signal_in_typed_not_raw":
                (nq_typed >= POWERED and df_typed >= DIFFER_BAR) and
                not (nq_raw >= POWERED and df_raw >= DIFFER_BAR),
        },
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("RAW_adjacency", "TYPED_relation")},
                     indent=2, ensure_ascii=False))
    print("\nRAW  :", {k: out["RAW_adjacency"][k] for k in
          ("n_ordered_pairs", "n_qualified", "differ_frac", "verdict")})
    print("TYPED:", {k: out["TYPED_relation"][k] for k in
          ("n_ordered_pairs", "n_qualified", "differ_frac", "verdict")})
    print("\n[saved]", OUT)


if __name__ == "__main__":
    main()
