# ⚠️ SUPERSEDED by anima eval single-entry (cli/anima.hexa -- eval) per PR #2603/#2605/#2607.
# torch-free fallback scorer (②), NOT a 박제 path. Kept for audit only. clm303 verdict = H_1579.
#!/usr/bin/env python3
# score_clm303_g6.py — TORCH-FREE engine-native G6 frozen 5-bar scorer for clm303 (.clm).
#
# a_engine_native_learning compliance:
#   DECODE is engine-native — fragments come from core/clm_decode.hexa via
#   state/1564_savant_g6_decode/engine_decode_batch_clm_cli.hexa (clm_decode_batch_to_file).
#   SCORE is pure text analysis of those engine bytes — no tensor-framework / array-lib / decode
#   mirror is used here. The frozen detector (COMPARATOR/MEASURABLE/STANCE + _is_falsifiable) and
#   the 5-bar logic are copied VERBATIM from state/1464_pairing_contrastive_bind/g6_common.py
#   (h1305 FROZEN), so this scorer is byte-equivalent to the parent harness MINUS the parent's
#   module-level tensor-framework dependency (which the parent only needs for its own decode
#   path, which we bypass entirely — decode already happened on the live engine).
#
# HARD-GATE self-check (a_engine_native_learning): this file pulls in no tensor framework, no
#   array library, and no decode mirror. The only g-helper module used is its text-only helpers
#   (_words/_KNOWN/_STOPWORDS/known_word_ratio/_jaccard), which have no module-level tensor import.
#
# usage: score_clm303_g6.py <text_helpers.py> <trained_frag.txt> [base_frag.txt]
import os, sys, importlib.util, random

# ── load the text-helper module (text-only helpers, no module-level tensor import) ──
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

GAUGE = sys.argv[1]
g = _load("gauge", GAUGE)

# ── FROZEN detector sets (VERBATIM from h1305 / g6_common, FREEZE.txt I) ──
COMPARATOR = {"if", "when", "whenever", "than", "more", "less", "greater", "fewer",
              "higher", "lower", "increases", "decreases", "correlates", "predicts",
              "causes", "depends", "unless", "whereas", "versus", "compared",
              "proportional", "faster", "slower", "stronger", "weaker"}
MEASURABLE = {"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"}
STANCE = {"that", "s", "a", "profound", "question", "i", "think", "interesting",
          "good", "nice", "great", "wonderful", "beautiful", "amazing"}

# frozen knobs (g6_common)
KWR_FLOOR = 0.50          # known-word-ratio coherence floor (G0)
JACCARD_DISTINCT = 0.50   # B2 pairwise-jaccard distinctness
SEEDS = [7, 4302, 4303]   # frozen eval cells (match jobs.tsv)
IDEATION = ["in"] * 5     # 5 ideation prompts per cell
HELDOUT = ["ho"] * 5      # 5 held-out prompts per cell


def _is_falsifiable(text):
    """FROZEN structural test (VERBATIM): comparator + measurable + negatable content claim."""
    wl = g._words(text)
    if not wl:
        return False
    wset = set(wl)
    a = bool(wset & COMPARATOR)
    b = bool(wset & MEASURABLE)
    content = [w for w in wl if len(w) >= 3 and w in g._KNOWN and w not in g._STOPWORDS]
    c_i = len(content) >= 2
    c_ii = not text.rstrip().endswith("?")
    first3 = set(wl[:3])
    c_iii = not (first3 and first3 <= STANCE)
    c = c_i and c_ii and c_iii
    return a and b and c


def _fals_count(ideas):
    return sum(1 for i in ideas if i["fals"])


def _distinct_count(ideas):
    kept = []
    for i in ideas:
        if not i["coh"]:
            continue
        ws = set(g._words(i["text"]))
        if not ws:
            continue
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    return len(kept)


def _cross_shuffle_fals(ideas, rng):
    """DECISIVE B3 (VERBATIM): re-weld each idea's comparator clause with a measurable
    token from a DIFFERENT idea, re-score with FROZEN detector; earned binding => FALS drops."""
    n = len(ideas)
    if n < 2:
        return _fals_count(ideas)
    src = [(k + 1) % n for k in range(n)]
    fals = 0
    for k, idea in enumerate(ideas):
        donor = ideas[src[k]]
        if not idea["meas"]:
            if idea["fals"]:
                fals += 1
            continue
        txt = idea["text"]
        words = txt.split()
        own_meas = set(idea["meas"])
        kept_words = [w for w in words if w.strip(".,;:!?").lower() not in own_meas]
        donor_meas = donor["meas"][0] if donor["meas"] else ""
        spliced = (" ".join(kept_words) + (" " + donor_meas if donor_meas else "")).strip()
        if _is_falsifiable(spliced):
            fals += 1
    return fals


def parse_frags(path):
    """tag<TAB>text per fragment (commit-early/resumable contract); tag = 'cell|kind|idx'."""
    frags = {}
    cur = None
    with open(path, errors="replace") as f:
        for ln in f:
            if "\t" in ln:
                key, txt = ln.split("\t", 1)
                parts = key.split("|")
                if len(parts) == 3:
                    cell, kind, idx = parts[0], parts[1], parts[2]
                    k = (int(cell), kind, int(idx))
                    if k not in frags:
                        frags[k] = txt.rstrip("\n"); cur = k
                        continue
            if cur is not None:
                frags[cur] += " " + ln.rstrip("\n")
    return frags


def ideas(frags, kind, sr):
    out = []
    for i in range(5):
        t = frags.get((sr, kind, i), "")
        wset = set(g._words(t))
        out.append({"text": t, "comp": sorted(wset & COMPARATOR), "meas": sorted(wset & MEASURABLE),
                    "fals": _is_falsifiable(t), "coh": g.known_word_ratio(t) >= KWR_FLOOR})
    return out


def evaluate(frags, label):
    rng = random.Random(1234)
    rec = {"in_fals": [], "in_dist": [], "shuf_fals": [], "ho_fals": [], "in_coh": []}
    for sr in SEEDS:
        ii = ideas(frags, "in", sr)
        ho = ideas(frags, "ho", sr)
        rec["in_fals"].append(_fals_count(ii))
        rec["in_dist"].append(_distinct_count(ii))
        rec["shuf_fals"].append(_cross_shuffle_fals(ii, rng))
        rec["ho_fals"].append(_fals_count(ho))
        rec["in_coh"].append(sum(1 for i in ii if i["coh"]) / len(ii))
    m = lambda xs: round(sum(xs) / len(xs), 4)
    return {"label": label, "FALS_in": m(rec["in_fals"]), "DIST_in": m(rec["in_dist"]),
            "FALS_shuf": m(rec["shuf_fals"]), "FALS_ho": m(rec["ho_fals"]),
            "COH_in": m(rec["in_coh"])}


def main():
    trained = sys.argv[2]
    base_path = sys.argv[3] if len(sys.argv) > 3 else None
    te = evaluate(parse_frags(trained), "TRAINED clm303")
    be = evaluate(parse_frags(base_path), "BASE") if base_path else None

    print("\n========== clm303 G6 FROZEN 5-BAR (engine-native decode · mean/3 cells) ==========")
    if be:
        print(f"  BASE      FALS_in={be['FALS_in']}  DIST_in={be['DIST_in']}  "
              f"FALS_shuf={be['FALS_shuf']}  FALS_ho={be['FALS_ho']}  COH_in={be['COH_in']}")
    print(f"  TRAINED   FALS_in={te['FALS_in']}  DIST_in={te['DIST_in']}  "
          f"FALS_shuf={te['FALS_shuf']}  FALS_ho={te['FALS_ho']}  COH_in={te['COH_in']}")

    b1 = te["FALS_in"] >= 1
    b2 = te["DIST_in"] >= 5
    b3 = te["FALS_shuf"] < te["FALS_in"]
    b4 = te["FALS_ho"] >= 1
    g0 = te["COH_in"] >= KWR_FLOOR
    b5 = (te["FALS_in"] >= be["FALS_in"] + 1) if be else None
    print(f"\n  G0 COHERENCE  (KWR>=0.50)          : {'PASS' if g0 else 'FAIL'}  ({te['COH_in']})")
    print(f"  B1 FALS-FLOOR (FALS_in>=1)         : {'PASS' if b1 else 'FAIL'}")
    print(f"  B2 COUNT      (DIST_in>=5)         : {'PASS' if b2 else 'FAIL'}  [G1/G2 recombination]")
    print(f"  B3 SHUFFLE    (FALS_shuf<FALS_in)  : {'PASS' if b3 else 'FAIL'}  [earned binding, not form]")
    print(f"  B4 HELD-OUT   (FALS_ho>=1)         : {'PASS' if b4 else 'FAIL'}")
    if b5 is None:
        print(f"  B5 vs-BASE    (need base .clm)     : N/A  (no base ckpt — follow-on)")
    else:
        print(f"  B5 vs-BASE    (trained>=base+1)    : {'PASS' if b5 else 'FAIL'}")

    core = b1 and b2 and b3 and b4 and g0
    verdict = "GREEN" if (core and (b5 is None or b5)) else "WALL/negative"
    print(f"\n  VERDICT(core G0+B1-B4): {'GREEN' if core else 'NOT-GREEN'}"
          f"  | full(+B5): {verdict}")
    print("\n  (decode=ENGINE-NATIVE core/clm_decode.hexa CLMConvMoE · score=g6_common frozen 5-bar VERBATIM, torch-free)")
    print("SCORE_CLM303_DONE")


if __name__ == "__main__":
    main()
