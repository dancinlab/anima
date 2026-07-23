"""V6_25 Step-0 -- observational density pilot ($0). Fable-adopted; tests the cause the
V6_24 closure BLAMED but never manipulated: is direct binding (SEEN) weak because natural
co-occurrence is singleton-dominated? Read SEEN accuracy vs each pair's REALISED co-occurrence
count k in the training slice. Nothing is curated -- k is measured, so this is p9-clean.

If naturally-frequent (high-k) SEEN pairs trend toward the 0.70 instrument bar while singletons
sit at chance, the dose story is confirmed and the V6_25 causal arms (k in {1,8,64}) are
warranted. If SEEN is flat in k, the closure is deeper than density (architectural) -- and the
expensive arms are spared.

Reuses trained57.clm/pedestal57.clm + v6_23_items.jsonl + train_slice_57.txt. Engine-native
C-slot readout (decode._fwd_logits), frozen from V6_24.
"""
import sys, os, re, json, collections, itertools, importlib.util
import numpy as np

ENT = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b")
STOP = {"The","This","That","These","Those","There","When","While","After","Before","However",
        "Although","Because","During","Some","Many","Most","Their","They","It","In","On","At",
        "For","From","With","And","But","New","List"}
_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]")
_YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")

def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (30 < len(s) < 400) or _YEAR.search(s): continue
            if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12: continue
            if not s.endswith((".","!","?")): continue
            yield s

def ent_set(s):
    return {x for x in ENT.findall(s) if x.split()[0] not in STOP and len(x) > 3}

def _decode():
    spec = importlib.util.find_spec("anima_py")
    if spec and spec.submodule_search_locations:
        b = list(spec.submodule_search_locations)[0]
        for c in (os.path.join(b,"core"), b):
            if os.path.isdir(c): sys.path.insert(0,c)
    for c in ("/opt/homebrew/lib/python3.14/site-packages/anima_py/core",):
        if os.path.isdir(c): sys.path.insert(0,c)

def main():
    items = [json.loads(l) for l in open("v6_23_items.jsonl", encoding="utf-8")]
    # target pairs (sorted tuple) -> we need co-occurrence k in the TRAIN slice
    targets = {tuple(sorted((d["a"], d["c"]))): 0 for d in items}
    train = open(os.path.expanduser("train_slice_57.txt"), encoding="utf-8", errors="ignore").read() \
        if os.path.exists("train_slice_57.txt") else \
        open(os.path.expanduser("~/anima-weights/en_general.txt"), encoding="utf-8", errors="ignore").read()[:0]
    print("counting co-occurrence k per target pair in the train slice ...", flush=True)
    for s in prose(train):
        es = ent_set(s)
        if len(es) < 2: continue
        for a, c in itertools.combinations(sorted(es), 2):
            key = (a, c)
            if key in targets:
                targets[key] += 1

    _decode(); import decode as clm
    def load(m): return clm.clm_load_weights(m)
    Wt, Wp = load("trained57.clm"), load("pedestal57.clm")
    def slot_nll(W, sentence, entity):
        raw = sentence.encode("utf-8"); eb = entity.encode("utf-8"); idx = raw.find(eb)
        b = list(raw)
        if idx < 1 or len(b) < 2: return None
        T = len(b) - 1
        logits = clm._fwd_logits(W, np.array([float(x) for x in b[:T]], dtype=np.float64), T)
        lo, hi = idx, min(idx+len(eb), len(b)); nl = []
        for q in range(lo, hi):
            lg = logits[q-1]; m = float(lg.max()); nl.append(float(m+np.log(np.exp(lg-m).sum())-lg[b[q]]))
        return sum(nl)/len(nl) if nl else None
    def correct(W, d):
        a = slot_nll(W, d["attested"][0], d["c"]); x = slot_nll(W, d["distract"][0], d["c_distract"])
        return None if (a is None or x is None) else (a < x)

    # bin by k (only SEEN has k>=1 by construction; BRIDGED/UNBRIDGED k=0 by design)
    bins = [(1,1),(2,3),(4,7),(8,10**9)]
    def blabel(k):
        for lo,hi in bins:
            if lo<=k<=hi: return f"k={lo}" if lo==hi else f"k={lo}-{hi if hi<10**9 else '∞'}"
        return "k=0"
    agg = collections.defaultdict(lambda: collections.defaultdict(lambda:[0,0,0]))  # stratum->bin->[t_correct,p_correct,n]
    kdist = collections.Counter()
    for d in items:
        k = targets[tuple(sorted((d["a"], d["c"])))]
        bl = blabel(k); kdist[(d["stratum"],bl)] += 1
        ct = correct(Wt, d); cp = correct(Wp, d)
        if ct is None or cp is None: continue
        cell = agg[d["stratum"]][bl]; cell[0]+=int(ct); cell[1]+=int(cp); cell[2]+=1

    print(f"\n{'stratum':<11}{'k-bin':<10}{'n':>5}{'SEEN_acc(tr)':>13}{'ped':>8}{'Δ':>8}")
    print("-"*60)
    for st in ("SEEN","BRIDGED","UNBRIDGED"):
        for lo,hi in bins:
            bl = f"k={lo}" if lo==hi else f"k={lo}-{hi if hi<10**9 else '∞'}"
            c = agg[st].get(bl)
            if not c or c[2]==0: continue
            t,p,n = c[0]/c[2], c[1]/c[2], c[2]
            print(f"{st:<11}{bl:<10}{n:>5}{t:>13.4f}{p:>8.4f}{t-p:>+8.4f}")
    # headline: does the TRAINING EFFECT (collapse-Δ = trained-pedestal) rise with k?
    # (raw accuracy is confounded -- pedestal drifts with k -- so read collapse-Δ, not raw acc)
    seen = agg["SEEN"]
    lowk = seen.get("k=1"); hik = seen.get("k=8-∞")
    if lowk and hik and lowk[2] and hik[2]:
        lo_d = (lowk[0]-lowk[1])/lowk[2]; hi_d = (hik[0]-hik[1])/hik[2]
        lo_acc, hi_acc = lowk[0]/lowk[2], hik[0]/hik[2]
        print(f"\ncollapse-Δ: SEEN(k=1)={lo_d:+.3f}  SEEN(k>=8)={hi_d:+.3f}  dose-Δ={hi_d-lo_d:+.3f}")
        print(f"abs acc:    SEEN(k=1)={lo_acc:.3f}   SEEN(k>=8)={hi_acc:.3f} (bar 0.70)")
        dose = hi_d - lo_d
        if dose > 0.04 and hik[2] >= 100:
            print("→ density-dose CONFIRMED and powered — arms optional (observational may suffice)")
        elif dose > 0.04:
            print(f"→ density-dose PRESENT in collapse-Δ but high-k underpowered (n={hik[2]}) — causal arms WARRANTED")
        else:
            print("→ collapse-Δ FLAT in k — closure is deeper than density; spare the arms, go LANE-BUS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
