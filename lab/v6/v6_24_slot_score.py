"""V6_24 -- localized C-slot readout ($0, numpy). Fixes V6_23's readout wall.

V6_23 verdict: whole-sentence byte-CE averaged the composition signal over ~200 bytes ->
margins ~0.01 nats, below the noise floor, so even memorised pairs were unreadable. The
signal lives ONLY at the swapped entity. This readout scores the mean next-byte NLL of the
C-slot bytes ALONE, conditioned on the (identical, shared) prefix ending in A. That isolates
"given this context, is the real endpoint C or the distractor C' more predictable" -- the
composition question, undiluted.

Engine-native: uses decode._fwd_logits (the exact production trunk forward). Correct iff the
model finds the real C-slot cheaper (lower NLL) than the swapped C'-slot in the same context.

Usage: v6_24_slot_score.py <model.clm> <items.jsonl> [--label NAME] [--limit N]
"""
import sys, os, json, collections, importlib.util
import numpy as np


def _add_decode():
    spec = importlib.util.find_spec("anima_py")
    if spec and spec.submodule_search_locations:
        base = list(spec.submodule_search_locations)[0]
        for c in (os.path.join(base, "core"), base):
            if os.path.isdir(c): sys.path.insert(0, c)
    for c in ("/opt/homebrew/lib/python3.14/site-packages/anima_py/core",):
        if os.path.isdir(c): sys.path.insert(0, c)


def main():
    model, items_path = sys.argv[1], sys.argv[2]
    label = sys.argv[sys.argv.index("--label")+1] if "--label" in sys.argv else "model"
    limit = int(sys.argv[sys.argv.index("--limit")+1]) if "--limit" in sys.argv else 10**9
    _add_decode()
    import decode as clm
    W = clm.clm_load_weights(model)

    def slot_nll(sentence, entity):
        raw = sentence.encode("utf-8")
        eb = entity.encode("utf-8")
        idx = raw.find(eb)
        b = list(raw)
        if idx < 1 or len(b) < 2:      # need a prefix byte before the slot
            return None
        T = len(b) - 1
        tok = np.array([float(x) for x in b[:T]], dtype=np.float64)
        logits = clm._fwd_logits(W, tok, T)          # [T, V]; logits[p] predicts b[p+1]
        lo, hi = idx, min(idx + len(eb), len(b))      # slot bytes b[lo..hi)
        nlls = []
        for q in range(lo, hi):
            lg = logits[q-1]                          # predicts b[q]
            m = float(lg.max())
            logZ = m + np.log(np.exp(lg - m).sum())
            nlls.append(float(logZ - lg[b[q]]))
        return sum(nlls)/len(nlls) if nlls else None

    per = collections.defaultdict(lambda: [0, 0])
    margins = collections.defaultdict(list)
    n = 0
    with open(items_path, encoding="utf-8") as f:
        for line in f:
            if n >= limit: break
            d = json.loads(line)
            a = slot_nll(d["attested"][0], d["c"])
            x = slot_nll(d["distract"][0], d["c_distract"])
            if a is None or x is None: continue
            correct = a < x
            per[d["stratum"]][0] += int(correct); per[d["stratum"]][1] += 1
            margins[d["stratum"]].append(x - a)      # >0 = real cheaper = favored
            n += 1

    print(f"# V6_24 localized C-slot readout -- label={label}  model={os.path.basename(model)}")
    print(f"{'stratum':<12}{'n':>6}{'acc':>8}{'mean_margin(nats)':>18}")
    for st in ("SEEN", "BRIDGED", "UNBRIDGED"):
        c, t = per[st]
        acc = c/t if t else float("nan")
        mm = sum(margins[st])/len(margins[st]) if margins[st] else float("nan")
        print(f"{st:<12}{t:>6}{acc:>8.4f}{mm:>18.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
