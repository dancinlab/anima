"""V6_22 -- build bridge-plausible, context-matched distractors ($0 numpy/regex).

Reconciled Fable+Sol design. From V6_21's prose (S, A, C) triples (orientation A-before-C,
C once in S), build a distractor C' that is:
  - never co-occurring with A in the full corpus
  - path-class matched: SEEN/BRIDGED need a shared non-hub training neighbour with A;
    UNBRIDGED needs none
  - surface matched: freq bucket, byte length +-2, degree bucket, entity-word count
  - CONTEXT matched: cosine of C''s training context-vector to the sentence context is in the
    same band as C's (equates topical fit -> only A->C binding can separate them)
  - globally UNIQUE (each C' used once; fewest-eligible items first) -> no reuse artifact

Emits v6_22_items.jsonl consumed by v6_22_analyze.py. Deterministic (no RNG).
p9-clean: the probe is the real held-out sentence; only the swapped endpoint changes.
"""
import re, sys, json, math, collections, itertools
from corpus_path import natural_corpus

HELDOUT_FRAC = 0.20
CAP = 700
WIN = 12               # +-token context window
HUB_PCTL = 0.95        # exclude bridges above this degree percentile

ENT = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b")
WORD = re.compile(r"[a-z]{3,}")
STOP = {"the","this","that","these","those","there","when","while","after","before","however",
        "although","because","during","some","many","most","their","they","and","but","new",
        "for","from","with","was","were","are","has","have","had","its","his","her","which",
        "who","also","been","into","than","then","them","other","such","more","only"}
_DATE_LIST = re.compile(r"^\s*\d{3,4}\s*[–-]")
_YEAR_ONLY = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")


def prose_sentences(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE_LIST.match(line):
            continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (30 < len(s) < 400) or _YEAR_ONLY.search(s):
                continue
            if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12:
                continue
            if not s.endswith((".", "!", "?")):
                continue
            yield s


def ent_set(s):
    return {x for x in ENT.findall(s) if x.split()[0] not in STOP and len(x) > 3}


def content_words(s):
    return [w for w in WORD.findall(s.lower()) if w not in STOP]


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "v6_22_items.jsonl"
    full = open(natural_corpus(), encoding="utf-8", errors="ignore").read()
    cut = int(len(full) * (1 - HELDOUT_FRAC))
    train_txt, eval_txt = full[:cut], full[cut:]

    # --- train graph + stats + context vectors ---
    freq = collections.Counter(); adj = collections.defaultdict(set)
    pairs_tr = set()
    ctx = collections.defaultdict(collections.Counter)   # entity -> content-word counts
    dfw = collections.Counter()                          # doc freq of words (for idf)
    for s in prose_sentences(train_txt):
        es = ent_set(s); cw = content_words(s)
        for w in set(cw): dfw[w] += 1
        for x in es:
            freq[x] += 1
            ctx[x].update(cw)
        for a, b in itertools.combinations(sorted(es), 2):
            pairs_tr.add((a, b)); adj[a].add(b); adj[b].add(a)
    train_ents = set(freq)
    # full-corpus co-occurrence (train+heldout) to forbid ever-composed C'
    pairs_all = set(pairs_tr)
    for s in prose_sentences(eval_txt):
        for a, b in itertools.combinations(sorted(ent_set(s)), 2):
            pairs_all.add((a, b))

    N = max(len(freq), 1)
    idf = {w: math.log(1 + N / (1 + dfw[w])) for w in dfw}
    def vec(counter):
        return {w: cnt * idf.get(w, 0.0) for w, cnt in counter.items()}
    def l2(v):
        return math.sqrt(sum(x * x for x in v.values())) or 1.0
    def cos(u, v):
        if len(u) > len(v): u, v = v, u
        return sum(x * v.get(w, 0.0) for w, x in u.items()) / (l2(u) * l2(v))

    degrees = sorted(len(adj[e]) for e in train_ents)
    hub_deg = degrees[int(len(degrees) * HUB_PCTL)] if degrees else 1<<30
    def fbk(f): return 0 if f<=1 else 1 if f<=2 else 2 if f<=5 else 3 if f<=12 else 4
    def dbk(d): return 0 if d<=1 else 1 if d<=3 else 2 if d<=7 else 3 if d<=15 else 4
    def ewc(e): return e.count(" ") + 1

    # index entities by surface signature for fast candidate lookup
    by_sig = collections.defaultdict(list)
    for e in sorted(train_ents):
        by_sig[(fbk(freq[e]), dbk(len(adj[e])), ewc(e))].append(e)

    def cn(a, x):  # shared NON-HUB training neighbours
        return {b for b in (adj.get(a, set()) & adj.get(x, set())) if len(adj[b]) < hub_deg}

    # --- mine held-out triples (orientation A before C, C occurs once) ---
    triples = {"SEEN": [], "BRIDGED": [], "UNBRIDGED": []}
    seen = set()
    for s in prose_sentences(eval_txt):
        es = sorted(ent_set(s))
        for a, c in itertools.combinations(es, 2):
            if (a, c) in seen or a not in train_ents or c not in train_ents:
                continue
            seen.add((a, c))
            # orientation: keep the (earlier, later) as (A, C) by position in s
            ia, ic = s.find(a), s.find(c)
            if ia < 0 or ic < 0: continue
            A, C = (a, c) if ia < ic else (c, a)
            if len(re.findall(r"\b"+re.escape(C)+r"\b", s)) != 1:
                continue
            if (A, C) in pairs_tr:
                st = "SEEN"
            else:
                shared = cn(A, C)
                if shared and any(b in s for b in shared):  # bridge literally in S = giveaway
                    continue
                st = "BRIDGED" if shared else "UNBRIDGED"
            triples[st].append((A, C, s))

    # --- build distractors with global unique assignment ---
    sctx_cache = {}
    def sentence_ctx(s):
        if s not in sctx_cache:
            sctx_cache[s] = vec(collections.Counter(content_words(s)))
        return sctx_cache[s]

    def eligibility(A, C, s, stratum):
        want_bridge = stratum in ("SEEN", "BRIDGED")
        csig = (fbk(freq[C]), dbk(len(adj[C])), ewc(C))
        cbytes = len(C.encode()); cap = C[:1].isupper()
        cvec = vec(ctx[C]); svec = sentence_ctx(s)
        target_cos = cos(cvec, svec)
        cands = []
        for e in by_sig.get(csig, ()):
            if e == A or e == C or e in s: continue
            key = (A, e) if A < e else (e, A)
            if key in pairs_all: continue                      # never co-occur w/ A
            if abs(len(e.encode()) - cbytes) > 2: continue
            if e[:1].isupper() != cap: continue
            has = bool(cn(A, e))
            if want_bridge and not has: continue
            if not want_bridge and has: continue
            fit = cos(vec(ctx[e]), svec)
            d = abs(fit - target_cos) + 0.3*abs(math.log2((freq[e]+1)/(freq[C]+1)))
            cands.append((d, e))
        cands.sort()
        return cands  # sorted by distance

    used = set()
    items = []
    for stratum in ("SEEN", "BRIDGED", "UNBRIDGED"):
        elig = []
        for (A, C, s) in triples[stratum]:
            elig.append((A, C, s, eligibility(A, C, s, stratum)))
        # fewest-eligible first (Sol) so scarce items get their pick
        elig.sort(key=lambda t: len(t[3]))
        picked = []
        for (A, C, s, cands) in elig:
            cp = next((e for _, e in cands if e not in used), None)
            if cp is None: continue
            used.add(cp)
            sp = re.sub(r"\b"+re.escape(C)+r"\b", cp, s, count=1)
            picked.append({"stratum": stratum, "a": A, "c": C, "c_distract": cp,
                           "attested": [s], "distract": [sp], "anchor": A})
            if len(picked) >= CAP: break
        items += picked

    with open(out_path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    n = collections.Counter(it["stratum"] for it in items)
    print(f"wrote {len(items)} items -> {out_path}  (bridge-plausible, context-matched, unique C')")
    for st in ("SEEN", "BRIDGED", "UNBRIDGED"):
        print(f"  {st:<10} {n[st]:>4}  (MDE floor 300)")
    if min(n["BRIDGED"], n["UNBRIDGED"]) < 300:
        print("  ⚠️ SUPPLY BLOCKED (<300) — do not fire the verdict table (pilot only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
