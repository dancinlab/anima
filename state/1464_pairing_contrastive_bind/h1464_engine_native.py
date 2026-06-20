#!/usr/bin/env python3
"""h1441_engine_native.py — H_1441 FROZEN 5-bar ENGINE-NATIVE adapter.

decode = live CORE/bytegpt_decode (engine_decode_batch_cli.hexa, each trained .bin), score =
g6_common FROZEN 5-bar (B1-B5 incl. cross-shuffle B3) VERBATIM. Replaces g6_common._decode_ideas'
torch _decode with ENGINE fragments → the verdict is ENGINE-NATIVE (a_engine_native_learning),
unlike the H_1435/36/37 torch-probe DIRECTIONAL. detector + cross-shuffle + bars all imported.

PHASE1 (--jobs-only): emit jobs.tsv = IDEATION_SEEDS(in) + HELDOUT_SEEDS(ho) × 3 seed_rng.
  decode 3× (contrastive.bin / shuffle.bin / base=chat_full.bin) → out_{contra,shuf,base}_*.
PHASE2 (--score <contra_glob> <shuf_glob> <base_glob>): parse each → evaluate → print_bars.
"""
import os, sys, importlib.util, re, glob, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
g = C.g
IDEATION = list(g.IDEATION_SEEDS)
HELDOUT = C.HELDOUT_SEEDS
HERE = os.path.dirname(os.path.abspath(__file__))

def gen_jobs(path):
    lines = []
    for sr in C.SEEDS:
        for i, s in enumerate(IDEATION):
            lines.append(f"{sr}\t{sr}|in|{i}\t{s}")
        for i, s in enumerate(HELDOUT):
            lines.append(f"{sr}\t{sr}|ho|{i}\t{s}")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines)

def parse_frags(out_glob):
    TAG = re.compile(r'^(\d+)\|(in|ho)\|(\d+)\t(.*)$')
    frags = {}
    for fn in sorted(glob.glob(out_glob)):
        cur = None
        with open(fn, errors="replace") as f:
            for ln in f:
                m = TAG.match(ln)
                if m:
                    sr, kind, i, txt = m.groups()
                    key = (int(sr), kind, int(i))
                    if key not in frags:
                        frags[key] = txt; cur = key
                    else:
                        cur = None
                elif cur is not None:
                    frags[cur] += " " + ln.rstrip("\n")
    return frags

def ideas(frags, seeds, kind, sr):
    """g6_common._decode_ideas 의 engine 버전 (decode→fragment, 채점은 동일)."""
    out = []
    for i, s in enumerate(seeds):
        t = frags.get((sr, kind, i), "")
        wset = set(g._words(t))
        out.append({"text": t, "comp": sorted(wset & C.COMPARATOR), "meas": sorted(wset & C.MEASURABLE),
                    "fals": C._is_falsifiable(t), "coh": g.known_word_ratio(t) >= C.KWR_FLOOR})
    return out

def evaluate_engine(frags, label):
    """g6_common.evaluate 로직 VERBATIM (decode 만 engine fragments)."""
    rng = random.Random(1234)
    rec = {"in_fals": [], "in_dist": [], "shuf_fals": [], "ho_fals": []}
    for sr in C.SEEDS:
        ii = ideas(frags, IDEATION, "in", sr)
        ho = ideas(frags, HELDOUT, "ho", sr)
        rec["in_fals"].append(C._fals_count(ii))
        rec["in_dist"].append(C._distinct_count(ii))
        rec["shuf_fals"].append(C._cross_shuffle_fals(ii, rng))
        rec["ho_fals"].append(C._fals_count(ho))
    mean = lambda xs: round(sum(xs) / len(xs), 4)
    return {"label": label, "FALS_in": mean(rec["in_fals"]), "DIST_in": mean(rec["in_dist"]),
            "FALS_shuf": mean(rec["shuf_fals"]), "FALS_ho": mean(rec["ho_fals"])}

def main():
    if "--jobs-only" in sys.argv:
        n = gen_jobs(os.path.join(HERE, "jobs.tsv"))
        print(f"JOBS_ONLY_DONE {n} (IDEATION={len(IDEATION)} HELDOUT={len(HELDOUT)} × {len(C.SEEDS)} seeds)")
        return
    if "--score" in sys.argv:
        idx = sys.argv.index("--score")
        contra, shuf, base = sys.argv[idx+1], sys.argv[idx+2], sys.argv[idx+3]
        te = evaluate_engine(parse_frags(contra), "TRAINED")
        se = evaluate_engine(parse_frags(shuf), "SHUF-CORP")
        be = evaluate_engine(parse_frags(base), "BASE")
        C.print_bars("H_1441 contrastive ENGINE-NATIVE", be, te, se)
        print("\n(decode=ENGINE-NATIVE .bin CORE/bytegpt_decode · score=g6_common frozen 5-bar VERBATIM)")
        print("(1435/36/37 torch DIRECTIONAL: form installed but B3 cross-shuffle did NOT collapse)")
        print("SCORE_NATIVE_DONE")
        return
    print("usage: --jobs-only | --score <contra_glob> <shuf_glob> <base_glob>")

if __name__ == "__main__":
    main()
