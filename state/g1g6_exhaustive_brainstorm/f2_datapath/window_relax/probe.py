#!/usr/bin/env python3
"""F2 datapath cell = window_relax.

RELAX the E1 order-distinguishing gate slot from strict adjacent-bigram to
within-window-k ordered co-occurrence (k in {1(=ref),3,5}) on the REAL Korean
corpus consciousness_anchor.txt. Does widening the slot POWER the gate
(n_qualified >= 10) while keeping it order-distinguishing (differ_frac >= 2/3)?

Reference metric = e1_pregate/gate.py (read & reference-matched):
  - qualified pair (a,b): BOTH (a,b) and (b,a) co-occur >= MIN_OCC(=3) times,
    a != b (self-pairs excluded), each side counted once (seen-set dedupe).
  - differ = top-follower(a,b) != top-follower(b,a).
  - differ_frac = differ / n_qualified.  NON-DEGENERATE <=> frac >= 2/3.
  Powered <=> n_qualified >= 10 (else INCONCLUSIVE-SPARSE).

WINDOW RELAX (the single changed variable vs ref):
  ref (k=1): pair = adjacent bigram (toks[i], toks[i+1]); follower = toks[i+2].
  k>1      : for each i, for each offset d in 1..k, if toks[i],toks[i+d] both in
             vocab -> ordered co-occurrent pair (a=toks[i], b=toks[i+d]).
             Follower = "next vocab token after the window" = first token in vocab
             at position > i+d (bounded forward scan).

Two arms (honesty — no tune-to-green):
  ARM A (ref-vocab control): original 400-word vocab.json + `[a-z]+` tokenizer
         (exactly E1's tokenization) — isolates the pure window effect on the
         same starved ASCII slot E1 used.
  ARM B (corpus-native): vocab REBUILT from THIS corpus as top-400 tokens by
         frequency (Korean-inclusive tokenizer) — NOT hand-picked, NOT authored;
         the honest test of whether widening the slot exposes DENSE
         order-distinguishing structure that actually exists in the corpus.
"""
import json, os, re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/mini/dancinlab/anima"
VOCAB_REF = os.path.join(REPO, "state", "trunk_obj_step0", "noncommutative_derisk", "vocab.json")
CORPUS = os.path.join(REPO, "archive", "state_legacy",
                      "anima_phase1a1_color_cosmology_2026_05_12", "consciousness_anchor.txt")
MIN_OCC = 3
BAR = 2.0 / 3.0
FWD_SCAN_CAP = 30   # bound the "next vocab token" forward scan (density -> usually 1)

raw = open(CORPUS, encoding="utf-8", errors="ignore").read()


def run_gate(toks, vset, k):
    """Window-k ordered co-occurrence gate. Returns (n_qualified, differ, frac, examples)."""
    n = len(toks)
    follower = defaultdict(Counter)
    for i in range(n - 1):
        a = toks[i]
        if a not in vset:
            continue
        jmax = min(i + k, n - 1)
        for j in range(i + 1, jmax + 1):
            b = toks[j]
            if b not in vset or a == b:
                continue
            # follower = next vocab token strictly after b's position j
            f = None
            end = min(j + 1 + FWD_SCAN_CAP, n)
            for p in range(j + 1, end):
                if toks[p] in vset:
                    f = toks[p]
                    break
            if f is not None:
                follower[(a, b)][f] += 1

    qualified, differ, seen = [], 0, set()
    for (a, b), fab in follower.items():
        if (a, b) in seen or (b, a) in seen:
            continue
        fba = follower.get((b, a))
        if fba is None:
            continue
        nab, nba = sum(fab.values()), sum(fba.values())
        if nab < MIN_OCC or nba < MIN_OCC:
            continue
        seen.add((a, b)); seen.add((b, a))
        top_ab = fab.most_common(1)[0][0]
        top_ba = fba.most_common(1)[0][0]
        d = top_ab != top_ba
        differ += int(d)
        qualified.append({"pair": f"{a}|{b}", "n_ab": nab, "n_ba": nba,
                          "top_ab": top_ab, "top_ba": top_ba, "differ": d})
    nq = len(qualified)
    frac = differ / nq if nq else 0.0
    return nq, differ, frac, qualified[:12]


def verdict_of(nq, frac):
    if nq < 10:
        return "INCONCLUSIVE-SPARSE"
    return "NON-DEGENERATE-POWERED" if frac >= BAR else "DEGENERATE-POWERED"


# ---- ARM A: reference vocab + `[a-z]+` tokenizer (E1 tokenization) ----
vref = json.load(open(VOCAB_REF))
vref = vref["vocab"] if isinstance(vref, dict) else vref
vset_ref = set(vref)
toks_ascii = re.findall(r"[a-z]+", raw.lower())

# ---- ARM B: corpus-native top-400 vocab + Korean-inclusive tokenizer ----
# tokenizer: Hangul syllable runs OR ascii-letter runs (strips punctuation/particles-tail punct)
toks_kr = re.findall(r"[가-힣]+|[a-z]+", raw.lower())
freq = Counter(toks_kr)
vset_kr = set(w for w, _ in freq.most_common(400))

arms = {}
for arm, (toks, vset) in {"A_ref_vocab_ascii": (toks_ascii, vset_ref),
                          "B_corpus_native_top400": (toks_kr, vset_kr)}.items():
    per_k = {}
    for k in (1, 3, 5):
        nq, differ, frac, ex = run_gate(toks, vset, k)
        per_k[f"k{k}"] = {"n_qualified": nq, "n_differ": differ,
                          "differ_frac": round(frac, 4),
                          "verdict": verdict_of(nq, frac), "examples": ex}
    arms[arm] = {"n_tokens": len(toks), "vocab_size": len(vset), "per_k": per_k}

out = {"cell": "window_relax", "corpus": os.path.basename(CORPUS),
       "min_occ": MIN_OCC, "bar": BAR, "fwd_scan_cap": FWD_SCAN_CAP,
       "reference_gate": "e1_pregate/gate.py",
       "arms": arms}
json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), ensure_ascii=False, indent=1)

for arm, d in arms.items():
    print(f"=== ARM {arm}  ntok={d['n_tokens']} |V|={d['vocab_size']} ===")
    for k, r in d["per_k"].items():
        print(f"  {k}: n_qualified={r['n_qualified']:4d} differ={r['n_differ']:4d} "
              f"frac={r['differ_frac']:.3f} -> {r['verdict']}")
