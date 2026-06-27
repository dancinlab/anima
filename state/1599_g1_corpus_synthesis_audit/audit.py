#!/usr/bin/env python3
"""L3 — corpus 2-concept synthesis-content audit (CHEAP, no model, GPU 0, torch-free).

Question (a_break_the_wall, data-distribution lens): does the training corpus
(4 cells ko/en general/sns) actually CONTAIN 2-concept synthesis examples — i.e. lines
where two of the G1 seed concepts' keyword-sets BOTH appear in the same window? If the
co-occurrence frequency is below a frozen threshold, no objective/depth can teach a model
to compose what it never saw (data-starvation ceiling).

Frozen metric (mirror of g1_multiseed.py CONCEPTS — VERBATIM, not changed):
  CONCEPTS keyword-sets are the same 5 concept families. A "synthesis example" = a corpus
  line (or sentence) in which >=2 DISTINCT concept families each have at least one keyword
  present. This mirrors the G1 scorer's `coverage()` (>=2 distinct families) applied to the
  CORPUS rather than to model output.

Frozen prediction (pre-registered BEFORE running):
  If synthesis_rate (lines with >=2 distinct concept families / total non-empty lines)
  < 0.5% in EVERY cell  -> DATA-STARVATION SUPPORTED (corpus does not teach 2-concept synth).
  If any cell >= 0.5%    -> data-starvation REFUTED for that cell (synth examples present;
                            the wall is not pure data absence).
The 0.5% bar is frozen-first and reported verbatim; the raw rates are reported regardless.
"""
from __future__ import annotations
import sys, os, re, json, time

HERE = os.path.dirname(os.path.abspath(__file__))

# ── frozen concept keyword-sets (VERBATIM from g1_multiseed.py CONCEPTS) ──────────────
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]
# also include the concept-sentence words themselves (same KNOWN expansion the scorer does)
FAMILIES = []
for _c, _kw in CONCEPTS:
    fam = set(_kw)
    fam |= {w for w in re.findall(r"[0-9a-z가-힣]+", _c.lower())}
    FAMILIES.append(fam)

def words(s): return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())

def families_hit(text):
    """Return set of concept-family indices with >=1 keyword present in text."""
    wl = set(words(text))
    return {i for i, fam in enumerate(FAMILIES) if wl & fam}

CELLS = {
    "gen_ko": "sns_ko.txt",  # placeholder, fixed below
}

def audit_file(path, granularity="line"):
    n = 0
    fam_count = {0:0,1:0,2:0,3:0,4:0,5:0}  # by #distinct families hit
    pair_counts = {}  # frozenset(pair) -> count of windows with both
    single_fam_lines = 0
    with open(path, errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if granularity == "sentence":
                units = re.split(r"[.!?\n]|다\.|요\.", line)
            else:
                units = [line]
            for u in units:
                u = u.strip()
                if not u:
                    continue
                n += 1
                hit = families_hit(u)
                k = min(len(hit), 5)
                fam_count[k] = fam_count.get(k,0)+1
                if len(hit) == 1:
                    single_fam_lines += 1
                if len(hit) >= 2:
                    lh = sorted(hit)
                    for a in range(len(lh)):
                        for b in range(a+1, len(lh)):
                            key = (lh[a], lh[b])
                            pair_counts[key] = pair_counts.get(key,0)+1
    synth = sum(v for k,v in fam_count.items() if k >= 2)
    rate = synth / n if n else 0.0
    return {
        "n_units": n,
        "fam_count_by_distinct": fam_count,
        "synth_units(>=2 distinct families)": synth,
        "synth_rate": round(rate, 6),
        "synth_rate_pct": round(rate*100, 4),
        "single_family_units": single_fam_lines,
        "top_pairs": sorted(((k,v) for k,v in pair_counts.items()), key=lambda x:-x[1])[:8],
    }

def main():
    corpus_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "..", "clm303_clean_corpus")
    corpus_dir = os.path.abspath(corpus_dir)
    cells = {
        "gen_en": os.path.join(corpus_dir, "gen_en.txt"),
        "gen_ko": os.path.join(corpus_dir, "gen_ko.txt"),
        "sns_en": os.path.join(corpus_dir, "sns_en.txt"),
        "sns_ko": os.path.join(corpus_dir, "sns_ko.txt"),
    }
    BAR = 0.005  # 0.5% frozen
    print("="*80)
    print("L3 CORPUS 2-CONCEPT SYNTHESIS AUDIT  (H_1599)")
    print(f"date {time.strftime('%Y-%m-%d %H:%M:%S')}  host {os.uname().nodename}")
    print(f"corpus_dir {corpus_dir}")
    print(f"FROZEN bar: synth_rate < {BAR*100}% in ALL cells => DATA-STARVATION SUPPORTED")
    print("concept families:")
    for i, fam in enumerate(FAMILIES):
        print(f"  fam{i}: {sorted(fam)}")
    print("="*80)
    results = {}
    for gran in ("line", "sentence"):
        print(f"\n##### granularity = {gran} #####")
        results[gran] = {}
        for cell, p in cells.items():
            if not os.path.isfile(p):
                print(f"  {cell}: MISSING {p}"); continue
            r = audit_file(p, gran)
            results[gran][cell] = r
            below = r["synth_rate"] < BAR
            print(f"  {cell:8s} n={r['n_units']:7d} synth>=2fam={r['synth_units(>=2 distinct families)']:6d} "
                  f"rate={r['synth_rate_pct']:.4f}% {'<BAR(starved)' if below else '>=BAR(present)'}")
            print(f"            distinct-family histogram {r['fam_count_by_distinct']}")
            print(f"            top concept-pairs {r['top_pairs']}")
    # verdict on LINE granularity (primary)
    line_rates = {c: results['line'][c]['synth_rate'] for c in results['line']}
    all_below = all(v < BAR for v in line_rates.values())
    verdict = "DATA-STARVATION SUPPORTED" if all_below else "DATA-STARVATION REFUTED (synth examples present)"
    print("\n"+"="*80)
    print(f"VERDICT (line granularity, frozen bar {BAR*100}%): {verdict}")
    print(f"  per-cell line synth_rate: { {c: round(v*100,4) for c,v in line_rates.items()} } %")
    print("="*80)
    out = {"bar_pct": BAR*100, "verdict": verdict, "results": results,
           "line_synth_rate_pct": {c: round(v*100,4) for c,v in line_rates.items()}}
    with open(os.path.join(HERE, "result.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"wrote {os.path.join(HERE,'result.json')}")

if __name__ == "__main__":
    main()
