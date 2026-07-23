"""V6_25 Step-1 -- density-controlled training arms ($0 construction).

For each arm k in {1,8,64}: build a training corpus where every SEEN target pair's
train-bearing sentence appears exactly k times, total bytes held ~constant (trim pair-free
sentences to compensate for the duplicated bytes). The eval (v6_23_items SEEN probes, held
out) is unchanged. Tests: does direct binding (SEEN acc) rise when a pair's natural
co-occurrence is upsampled?

FIRST CUT (honest fluency-pregate): this does NOT yet marginal-match single-entity counts, so
a POSITIVE result would be pair-density OR entity-familiarity (both rise with k) -- to be
disambiguated by a marginal-matched v2. A NEGATIVE result (SEEN flat even with both helping)
already kills the density hypothesis decisively. Caveat recorded in the card.

Emits train_arm_k{1,8,64}.txt. Deterministic.
"""
import sys, os, re, json, itertools, collections

ENT = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b")
STOP = {"The","This","That","These","Those","There","When","While","After","Before","However",
        "Although","Because","During","Some","Many","Most","Their","They","It","In","On","At",
        "For","From","With","And","But","New","List"}
_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")
KS = [1, 8, 64]

def prose_lines(txt):
    """Yield (sentence, is_prose) preserving ALL lines so the base corpus stays intact."""
    for line in txt.split("\n"):
        yield line

def is_prose(s):
    s = s.strip()
    if not s or _DATE.match(s) or _YEAR.search(s): return False
    if not (30 < len(s) < 400): return False
    if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12: return False
    return s.endswith((".","!","?"))

def ent_set(s):
    return {x for x in ENT.findall(s) if x.split()[0] not in STOP and len(x) > 3}

def main():
    items = [json.loads(l) for l in open("v6_23_items.jsonl", encoding="utf-8")]
    seen_pairs = {tuple(sorted((d["a"], d["c"]))) for d in items if d["stratum"] == "SEEN"}
    print(f"{len(seen_pairs)} SEEN target pairs")

    base = open(os.path.expanduser("train_slice_57.txt"), encoding="utf-8", errors="ignore").read()
    lines = base.split("\n")
    # find ONE bearing train sentence per target pair (first occurrence), and index pair-free prose lines
    bearing = {}                    # pair -> line index
    pairfree_idx = []               # indices of prose lines carrying no target pair (trim pool)
    for i, ln in enumerate(lines):
        if not is_prose(ln): continue
        es = ent_set(ln)
        hit = None
        if len(es) >= 2:
            for a, c in itertools.combinations(sorted(es), 2):
                if (a, c) in seen_pairs and (a, c) not in bearing:
                    bearing[(a, c)] = i; hit = (a, c)
        if hit is None:
            pairfree_idx.append(i)
    print(f"bearing sentences found for {len(bearing)}/{len(seen_pairs)} pairs; {len(pairfree_idx)} pair-free prose lines")

    base_bytes = len(base.encode())
    for k in KS:
        extra = []                  # (k-1) extra copies of each bearing sentence
        add_bytes = 0
        for (a, c), i in bearing.items():
            s = lines[i]
            for _ in range(k - 1):
                extra.append(s); add_bytes += len(s.encode()) + 1
        # trim pair-free prose lines (from the end of the pool) to compensate add_bytes
        drop = set(); trimmed = 0; j = len(pairfree_idx) - 1
        while trimmed < add_bytes and j >= 0:
            idx = pairfree_idx[j]; trimmed += len(lines[idx].encode()) + 1; drop.add(idx); j -= 1
        kept = [ln for i2, ln in enumerate(lines) if i2 not in drop]
        out_lines = kept + extra
        out = "\n".join(out_lines)
        path = f"train_arm_k{k}.txt"
        open(path, "w", encoding="utf-8").write(out)
        print(f"k={k:<3} -> {path}  {len(out.encode())/1e6:.1f}MB "
              f"(base {base_bytes/1e6:.1f} + dup {add_bytes/1e6:.1f} - trim {trimmed/1e6:.1f})  "
              f"extra_sents={len(extra)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
