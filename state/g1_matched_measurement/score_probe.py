#!/usr/bin/env python3
"""H_6189 offline scorer — reads raw --probe continuations, applies the FROZEN bars (PREREG.md).
Usage: python3 score_probe.py <L8cov.json> [--null L4clean.json L8nocov.json]
Deterministic; re-runnable from raw bytes. No ckpt touched."""
import json, os, sys, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
d = json.load(open(os.path.join(ROOT, "state/g1_coverage_prod_block/design.json")))
ATTRS = set(d["attrs_en"])

def extract(cont):
    """first two attr-vocab tokens appearing in the continuation (substring-free vocab)."""
    toks = []
    for w in cont.replace(".", " ").replace(",", " ").replace(";", " ").split():
        w = w.strip()
        if w in ATTRS:
            toks.append(w)
        if len(toks) == 2:
            break
    return toks

def score_items(items, fit_only=True):
    strict = loose = n = 0
    per = {}
    for it in items:
        if fit_only and not it.get("window_fit"):
            continue
        exp = it["expect"]
        got = extract(it["continuation"])
        n += 1
        loose_ok = len(exp) <= len([g for g in got if g in exp]) if len(exp) == 1 else (
            len(set(exp) & set(got)) == 2)
        strict_ok = (len(exp) == 1 and got[:1] == exp) or (
            len(exp) == 2 and got[:2] == exp)
        strict += strict_ok; loose += loose_ok
        t = it["template"]; per.setdefault(t, [0, 0]); per[t][0] += strict_ok; per[t][1] += 1
    return dict(n=n, strict=round(strict / n, 4) if n else 0.0,
                loose=round(loose / n, 4) if n else 0.0,
                per_template={t: round(v[0] / v[1], 3) for t, v in per.items()})

def perm_null(items, trials=1000, seed=6185):
    """derangement null: shuffle expect->concept assignment, rescore strict."""
    rng = random.Random(seed)
    fit = [it for it in items if it.get("window_fit") and len(it["expect"]) == 2]
    if not fit: return 0.0
    got = [extract(it["continuation"]) for it in fit]
    hits = []
    allexp = [it["expect"] for it in fit]
    for _ in range(trials):
        perm = allexp[:]; rng.shuffle(perm)
        h = sum(1 for g, e in zip(got, perm) if g[:2] == e) / len(fit)
        hits.append(h)
    hits.sort()
    return dict(mean=round(sum(hits) / len(hits), 4), p95=round(hits[int(0.95 * len(hits))], 4))

def load(path):
    j = json.load(open(path)); return j["items"]

if __name__ == "__main__":
    cov = load(sys.argv[1])
    nulls = []
    if "--null" in sys.argv:
        for p in sys.argv[sys.argv.index("--null") + 1:]:
            if p.startswith("--"): break
            nulls.append((os.path.basename(p), load(p)))
    held = [it for it in cov if it["arm"] == "heldout"]
    seen = [it for it in cov if it["arm"] == "seen"]
    unary = [it for it in cov if it["arm"] == "unary"]
    R = dict(
        heldout_fit=score_items(held), seen_fit=score_items(seen), unary=score_items(unary, fit_only=False),
        perm_null=perm_null(held),
        nulls={name: score_items([it for it in its if it["arm"] == "heldout"]) for name, its in nulls},
    )
    # frozen bars
    val_b = R["unary"]["strict"] >= 0.80
    val_c = R["seen_fit"]["strict"] >= 0.60
    h = R["heldout_fit"]["strict"]; s = R["seen_fit"]["strict"]
    p95 = R["perm_null"]["p95"] if isinstance(R["perm_null"], dict) else 1.0
    nulls_chance = all(v["strict"] <= p95 for v in R["nulls"].values()) if R["nulls"] else None
    if not (val_b and val_c):
        verdict = "⚙️ VOID (validity gate fail: unary<0.80 or seen<0.60)"
    elif h >= 0.50 and h >= 0.7 * s and h > p95 and (nulls_chance is not False):
        verdict = "🟢 GREEN-of-artifact (canonical G1=0 = measurement artifact; held-out ADDITIVE recombination real @303M · scope: not earned bind)"
    elif h <= p95:
        verdict = "🔴 KILL (held-out ≤ perm-null → genuine ceiling even matched+windowed)"
    else:
        verdict = "🟠 INCONCLUSIVE"
    R["verdict"] = verdict
    print(json.dumps(R, indent=2, ensure_ascii=False))
