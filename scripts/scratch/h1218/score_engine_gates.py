#!/usr/bin/env python3
"""H_1218 — score G1/G2/G6 over a set of greedy generations using the FROZEN
UNIVERSE/gauge_lib.py evaluators VERBATIM (no metric re-invention, p7).

Input  : a JSON {rows:[{role, seed, text}]} (either engine RESULT lines parsed
         into this shape, or the torch_greedy_baseline.py output).
Corpus : data/corpus.txt (the git-tracked dialogue corpus — the 1.5GB broad
         training corpus from H_1140/H_1158 is ephemeral and GONE, so G2
         corpus-absence here is an UPPER BOUND: fewer corpus files => fewer hits
         => MORE n-grams flagged novel. Flagged explicitly in the verdict.)

Reuses gauge_lib: known_word_ratio, _coverage (G1), _content_ngrams + _corpus_absent
(G2), _words + _jaccard (G6) — the SAME functions compute_inline_gauges uses.

GREEDY note: gauge_lib.compute_inline_gauges DECODES with top-k=40 temp=0.7 SAMPLING.
This scorer takes ALREADY-GENERATED greedy text and applies the SAME scoring functions.
So the *evaluators* are frozen-verbatim; the *decode* is greedy (deterministic,
engine-parity) NOT the sampled gauge decode. Reported honestly.
"""
import argparse, json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "tool"))
import gauge_lib as G

def score(rows, corpus_paths, kwr_floor=0.50, jaccard_distinct=0.25):
    by = {r["role"]: r for r in rows}
    out = {}

    # ── G1 composed-distinct (H_1129): _coverage over the composed-seed decode ──
    comp = by.get("G1_composed", {}).get("text", "")
    out["g1_composed_distinct"] = len(G._coverage(comp))
    out["g1_comp_text"] = comp

    # ── G2 corpus-absence (H_1140): comp_out + first 3 single-concept decodes ──
    g2_texts = [comp]
    for i in range(3):
        g2_texts.append(by.get(f"G2_single_{i}", {}).get("text", ""))
    all_grams = set()
    kwr_by_text = []
    for t in g2_texts:
        k = G.known_word_ratio(t)
        kwr_by_text.append(round(k, 3))
        if k >= kwr_floor:
            all_grams |= G._content_ngrams(t)
    if corpus_paths and all_grams:
        novel = [g for g in sorted(all_grams) if G._corpus_absent(g, corpus_paths)]
        out["g2_total_ngrams"] = len(all_grams)
        out["g2_novel_ngrams"] = len(novel)
        out["g2_novelty_rate"] = round(len(novel) / len(all_grams), 5)
        out["g2_sample_novel"] = novel[:15]
    else:
        out["g2_total_ngrams"] = len(all_grams)
        out["g2_novelty_rate"] = 0.0 if not all_grams else None
    out["g2_kwr_by_text"] = kwr_by_text

    # ── G6 ideation (H_1158): per ideation seed, keep if kwr>=floor + Jaccard-distinct ──
    idea_word_sets = []
    idea_rows = []
    for i in range(5):
        r = by.get(f"G6_ideation_{i}")
        if not r:
            continue
        o = r["text"]
        k = G.known_word_ratio(o)
        idea_rows.append({"i": i, "kwr": round(k, 3), "text": o[:80]})
        if k >= kwr_floor:
            ws = set(G._words(o))
            if ws:
                idea_word_sets.append(ws)
    kept = []
    for ws in idea_word_sets:
        if all(G._jaccard(ws, k) <= jaccard_distinct for k in kept):
            kept.append(ws)
    out["g6_count"] = len(kept)
    out["g6_ideas"] = idea_rows
    if len(kept) >= 2:
        dists = []
        for a in range(len(kept)):
            for b in range(a + 1, len(kept)):
                dists.append(1.0 - G._jaccard(kept[a], kept[b]))
        out["g6_jaccard"] = round(sum(dists) / len(dists), 5)
    else:
        out["g6_jaccard"] = None
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", required=True, help="JSON with rows[].{role,text}")
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.gens))
    rows = d["rows"] if "rows" in d else d
    res = score(rows, a.corpus)
    res["label"] = a.label
    res["corpus_paths"] = a.corpus
    json.dump(res, open(a.out, "w"), indent=2)
    print(f"[{a.label}] G1 composed_distinct = {res['g1_composed_distinct']}")
    print(f"[{a.label}] G2 novelty_rate = {res.get('g2_novelty_rate')} "
          f"({res.get('g2_novel_ngrams')}/{res.get('g2_total_ngrams')} novel)")
    print(f"[{a.label}] G6 count = {res['g6_count']}  jaccard = {res.get('g6_jaccard')}")
    print(f"[{a.label}] G2 kwr_by_text = {res['g2_kwr_by_text']}")
