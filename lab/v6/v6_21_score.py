"""V6_21 Stage-1c -- score the 2AFC eval with the engine's OWN byte-CE ($0, numpy).

For each item, the model's byte-NLL (mean next-byte cross-entropy) of the ATTESTED
phrasing is compared to the DISTRACTOR phrasing (averaged over templates). The model
"prefers" whichever it finds more likely (lower NLL). Correct = it prefers attested.

Engine-native: uses `decode.clm_ce_seq_W` -- the exact CE the trunk computes -- so no
re-implemented forward pass (a_experiment_engine_native is void in lab/v6, but reusing the
real scorer keeps the number honest). Runs on the numpy host path; no torch, no GPU.

Usage: v6_21_score.py <model.clm> <eval_items.jsonl> [--label NAME]
Report accuracy per stratum. Read against a pedestal (untrained .clm) run separately;
BRIDGED-vs-UNBRIDGED gap is the composition discriminator, SEEN is the positive control.
"""
import sys, os, json, glob, collections

def _add_decode_to_path():
    # locate the installed anima_py package via importlib -- no filesystem glob (a recursive
    # ~/ glob here once stalled scoring for 30 min scanning anima-weights)
    try:
        import importlib.util
        spec = importlib.util.find_spec("anima_py")
        if spec and spec.submodule_search_locations:
            base = list(spec.submodule_search_locations)[0]
            for cand in (os.path.join(base, "core"), base):
                if os.path.isdir(cand):
                    sys.path.insert(0, cand)
    except Exception:
        pass
    for base in ("/opt/homebrew/lib/python3.14/site-packages/anima_py",):
        for cand in (base + "/core", base):
            if os.path.isdir(cand):
                sys.path.insert(0, cand)


def main():
    model = sys.argv[1]
    items_path = sys.argv[2]
    label = "model"
    if "--label" in sys.argv:
        label = sys.argv[sys.argv.index("--label") + 1]
    _add_decode_to_path()
    import decode as clm

    W = clm.clm_load_weights(model)

    def nll(text):
        return clm.clm_ce_seq_W(W, None, list(text.encode("utf-8")))

    per = collections.defaultdict(lambda: [0, 0])  # stratum -> [correct, total]
    margins = collections.defaultdict(list)
    with open(items_path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            a_nll = sum(nll(t) for t in d["attested"]) / len(d["attested"])
            x_nll = sum(nll(t) for t in d["distract"]) / len(d["distract"])
            correct = a_nll < x_nll           # prefers attested = lower NLL
            per[d["stratum"]][0] += int(correct)
            per[d["stratum"]][1] += 1
            margins[d["stratum"]].append(x_nll - a_nll)  # >0 = attested favored

    print(f"# V6_21 2AFC accuracy -- label={label}  model={os.path.basename(model)}")
    print(f"{'stratum':<12} {'n':>5} {'acc':>7} {'mean_margin':>12}")
    print("-" * 40)
    out = {"label": label, "model": os.path.basename(model), "strata": {}}
    for st in ("SEEN", "BRIDGED", "UNBRIDGED"):
        c, n = per[st]
        acc = c / n if n else float("nan")
        mm = sum(margins[st]) / len(margins[st]) if margins[st] else float("nan")
        print(f"{st:<12} {n:>5} {acc:>7.4f} {mm:>12.5f}")
        out["strata"][st] = {"n": n, "acc": acc, "mean_margin": mm}
    print("JSON " + json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
