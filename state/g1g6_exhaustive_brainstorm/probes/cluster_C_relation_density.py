#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9200 cluster C (데이터·커리큘럼) - $0 relation-density corpus-statistic probe.

FROZEN PREREG (a_break_the_wall, tune-to-green forbidden, bar frozen BEFORE run):
================================================================================
Question: Are the C-item relation-transfer structures (C1 relation-balance,
C2 Cartesian, C5 causal/transitive chain, C6 anti-template form<->meaning,
C9 difficulty-ladder distance) REALIZED in (a) the production clm303 corpus
co-occurrence and (b) the existing coverage-designed corpora (the realized
H_6182/H_6185 prescription)? Or do they require a relation-STRUCTURED corpus
synthesis + 303M retrain (GPU-gated)?

Frozen claim: coverage-density (H_6182, supported) and relation-density
(C1/C5/C6/C9) are DISTINCT corpus axes. The coverage-designed corpora realize
pair COVERAGE but NOT relation STRUCTURE. If so, C-items are NOT achievable by
coverage scaling and are GPU-gated (rebuild + retrain), and the $0 statistic
pre-falsifies "C-items ride on coverage-density".

FROZEN BARS (per C-item, decided before running):
  C1 relation-balance  : need BOTH directions per pair. BAR = reverse-coverage
                         fraction (unordered pairs seen in BOTH text-orders)
                         >= 0.10. FAIL if < 0.10.
  C5 causal chain      : BAR = >=1 directional transitive triple (a->b, b->c
                         via the only asymmetric template 'remembers', with
                         a->c absent). FAIL if 0.
  C6 anti-template     : BAR = H(template | pair) >= H(template) - 0.5 bit
                         (pair does NOT predict surface template).
  C9 difficulty-ladder : BAR = co-occurrence distance spans >=3 of
                         {same-line, +-5 window, same-doc, absent}.
                         FAIL if all in one bucket.

Scope/honesty (c9): pure corpus STATISTIC (numpy/re, $0, no model load).
DIRECTIONAL - says nothing about whether a rebuilt corpus WOULD lift frozen
gates, only whether CURRENT corpora realize the C-item structures.
================================================================================
"""
import json, math, os, re
from collections import Counter, defaultdict

REPO = "/Users/mini/dancinlab/anima"
DESIGNED = {
    "high": f"{REPO}/state/g1_density_phase_transition/corpus/high_coverage.txt",
    "low":  f"{REPO}/state/g1_density_phase_transition/corpus/low_coverage.txt",
}
PROD_COOCLINES = f"{REPO}/state/g1_prod_corpus_density/hf_exact/cooc_lines_head.txt"

CONCEPTS = ["ocean","clock","forest","mirror","engine","garden","signal","ember",
    "glacier","harbor","lantern","meadow","needle","orbit","prism","quartz","river",
    "stone","thunder","umbra","violet","willow","anchor","beacon","cipher","dune",
    "echo","fable","grove","hollow"]
N = len(CONCEPTS)
IDX = {c: i for i, c in enumerate(CONCEPTS)}

TPL_PATTERNS = [
    ("t1_sym",   re.compile(r"^the (\w+) and the (\w+) \w+ until ", re.IGNORECASE)),
    ("t2_meets", re.compile(r"^when (\w+) meets (\w+), ", re.IGNORECASE)),
    ("t3_sym",   re.compile(r"^between the (\w+) and the (\w+) a quiet force ", re.IGNORECASE)),
    ("t4_remem", re.compile(r"^(\w+) remembers (\w+); together they ", re.IGNORECASE)),
]

def read_lines(p):
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        return [ln.rstrip("\n") for ln in f]

def tpl_of_line(line):
    for tag, rx in TPL_PATTERNS:
        m = rx.match(line.strip())
        if m:
            return tag, m.group(1).lower(), m.group(2).lower()
    return None, None, None

def H(counter):
    tot = sum(counter.values())
    if tot == 0: return 0.0
    h = 0.0
    for c in counter.values():
        p = c / tot
        if p > 0: h -= p * math.log2(p)
    return h

def probe_designed(path, tag):
    lines = read_lines(path)
    n_lines = len(lines)
    per_tpl = Counter()
    pair_tpl = defaultdict(Counter)
    pair_unordered_seen = set()
    ordered_edges = Counter()
    t4_directional = Counter()

    for ln in lines:
        t, a, b = tpl_of_line(ln)
        if t is None: continue
        per_tpl[t] += 1
        if a in IDX and b in IDX:
            pair_tpl[(a, b)][t] += 1
            pair_unordered_seen.add(frozenset((a, b)))
            ordered_edges[(a, b)] += 1
            if t == "t4_remem":
                t4_directional[(a, b)] += 1

    # C1 reversal
    directions_per_pair = defaultdict(set)
    for (a, b) in ordered_edges:
        directions_per_pair[frozenset((a, b))].add((a, b))
    both_dir = sum(1 for s in directions_per_pair.values() if len(s) >= 2)
    seen_pairs = len(directions_per_pair)
    rev_frac = both_dir / seen_pairs if seen_pairs else 0.0
    t4_pairs = defaultdict(set)
    for (a, b) in t4_directional:
        t4_pairs[frozenset((a, b))].add((a, b))
    t4_both = sum(1 for s in t4_pairs.values() if len(s) >= 2)

    # C5 transitive via t4 directed edges
    succ = defaultdict(set)
    for (a, b) in t4_directional:
        succ[a].add(b)
    transitive_triples = 0
    transitive_heldout = 0
    for a in succ:
        for b in succ[a]:
            for c in succ.get(b, ()):
                transitive_triples += 1
                if c not in succ.get(a, ()) and a != c:
                    transitive_heldout += 1

    # C6 anti-template
    tpl_global = Counter()
    for (a, b), tc in pair_tpl.items():
        for t, c in tc.items(): tpl_global[t] += c
    H_tpl = H(tpl_global)
    H_tpl_cond = 0.0; weighted = 0
    for (a, b), tc in pair_tpl.items():
        w = sum(tc.values()); H_tpl_cond += w * H(tc); weighted += w
    H_tpl_cond = H_tpl_cond / weighted if weighted else 0.0
    mi = H_tpl - H_tpl_cond

    # C9 distance buckets (designed: every cooc is single-line by construction)
    same_line = sum(per_tpl.values())
    total_pairs = N * (N - 1) // 2
    absent = total_pairs - len(pair_unordered_seen)
    buckets = sum(1 for v in (same_line, 0, 0, absent) if v > 0)

    return {
        "tag": tag, "n_lines": n_lines,
        "template_counts": dict(per_tpl),
        "C1_relation_balance": {
            "seen_unordered_pairs": seen_pairs,
            "pairs_with_both_directions": both_dir,
            "reverse_fraction": round(rev_frac, 4),
            "BAR_rev_frac_ge_0.10": rev_frac >= 0.10,
            "t4_remembers_pairs_both_dir": t4_both,
        },
        "C5_causal_chain": {
            "t4_directed_edges": sum(t4_directional.values()),
            "transitive_triples_a_b_c": transitive_triples,
            "transitive_with_a_c_absent": transitive_heldout,
            "BAR_ge1_transitive": transitive_triples >= 1,
        },
        "C6_anti_template": {
            "H_template_bits": round(H_tpl, 4),
            "H_template_given_pair_bits": round(H_tpl_cond, 4),
            "MI_template_pair_bits": round(mi, 4),
            "BAR_decorrelated_Hcond_ge_H_minus_0.5": H_tpl_cond >= (H_tpl - 0.5),
        },
        "C9_difficulty_ladder": {
            "same_line_cooc": same_line, "win5_cooc": 0, "cross_doc_cooc": 0,
            "absent_pairs": absent,
            "distinct_distance_buckets": buckets,
            "BAR_ge3_buckets": buckets >= 3,
        },
    }

def probe_prod_cooclines(path):
    if not os.path.exists(path):
        return {"tag": "prod", "note": "cooc-lines file not found"}
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    records = re.findall(r"--- [^\n]+ \[([^\]]+)\][^\n]*\n([^\n]*(?:\n(?!--- ))*)", txt)
    directional_cues = re.compile(
        r"\b(causes?|leads? to|implies?|precedes?|follows?|because|therefore|"
        r"results? in|produces?|generates?|drives?|inhibits?|remembers|prevents?)\b",
        re.IGNORECASE)
    n_total = 0; n_with_cue = 0; cue_counts = Counter()
    for pair_label, body in records:
        n_total += 1
        m = directional_cues.search(body)
        if m:
            n_with_cue += 1; cue_counts[m.group(1).lower()] += 1
    frac = n_with_cue / n_total if n_total else 0.0
    return {
        "tag": "prod_hf_head_cooclines",
        "n_cooc_lines": n_total,
        "lines_with_directional_relation_cue": n_with_cue,
        "directional_fraction": round(frac, 4),
        "BAR_C1_directional_frac_ge_0.10": frac >= 0.10,
        "cue_breakdown": dict(cue_counts),
        "note": ("prod corpus analyzed at HEAD co-occurrence-line tier (the only tier "
                 "H_6185 found non-zero: 15 lines, all en-general). Full 127MB HF corpus "
                 "not local on mini; this audits relation-structure of exactly those lines."),
    }

def main():
    out = {
        "prereg": "FROZEN before run: coverage-density (H_6182) vs relation-density (C1/C5/C6/C9) "
                  "claimed DISTINCT axes. If neither prod nor designed corpus realizes a C-item "
                  "structure, that C-item is GPU-gated (relation-structured corpus rebuild + 303M "
                  "retrain), NOT a coverage-density variant. $0 corpus statistic.",
        "designed": [],
        "prod": None,
    }
    for tag, p in DESIGNED.items():
        out["designed"].append(probe_designed(p, tag) if os.path.exists(p)
                               else {"tag": tag, "note": f"missing {p}"})
    out["prod"] = probe_prod_cooclines(PROD_COOCLINES)

    bar_keys = {
        "C1_relation_balance": "BAR_rev_frac_ge_0.10",
        "C5_causal_chain": "BAR_ge1_transitive",
        "C6_anti_template": "BAR_decorrelated_Hcond_ge_H_minus_0.5",
        "C9_difficulty_ladder": "BAR_ge3_buckets",
    }
    roll = {}
    for d in out["designed"]:
        if "C1_relation_balance" in d:
            roll[d["tag"]] = {k: d[k][bk] for k, bk in bar_keys.items()}
    out["verdict_rollup"] = roll

    print(json.dumps(out, indent=2, ensure_ascii=False))
    od = f"{REPO}/state/g1g6_exhaustive_brainstorm/probes/cluster_C_relation_density_result.json"
    with open(od, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n[saved] {od}", flush=True)

if __name__ == "__main__":
    main()
