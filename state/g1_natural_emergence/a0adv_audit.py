#!/usr/bin/env python3
"""A0-ADV — NATEM STAGE 0 extension ($0 model-free · adversative-XOR held-out · XOR-class 완전 감사).

A0-NEG covered negation (부정); this covers adversative (역접 "지만/그러나") — the XOR-class sibling (γ census:
XOR = negation/adversative = the only theoretical non-additive class in natural text). Adversative flips the
expected sentiment: "<posword> 지만 ..." → review label often negative (the "but" clause dominates). Audit whether
held-out (posword, adversative) combos carry a POWERED flip beyond the additive marginal. Same bar as A0-NEG.
NSMC labels · $0 · no ckpt.
"""
import os, sys, re, json, urllib.request, collections

OUT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/g1_natem/a0adv.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
def fetch(u, d):
    if os.path.exists(d) and os.path.getsize(d) > 1000: return d
    urllib.request.urlretrieve(u, d); return d
rows = []
for nm in ("ratings_train.txt", "ratings_test.txt"):
    c = os.path.expanduser("~/g1_natem/nsmc_%s" % nm)
    fetch("https://raw.githubusercontent.com/e9t/nsmc/master/" + nm, c)
    with open(c, encoding="utf-8") as f:
        next(f)
        for line in f:
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 3 and pp[2] in ("0", "1"):
                rows.append((pp[1], int(pp[2])))
total_mb = sum(len(t.encode()) for t, _ in rows) / 1e6

ADV = re.compile(r"([가-힣]{2,4})(?:지만|는데|은데|지마는|다만|그러나|하지만)")
# pol(stem) from non-adversative bare occurrences
bare = collections.defaultdict(list)
adv_events = []
for i, (text, lab) in enumerate(rows):
    has_adv = bool(re.search(r"지만|그러나|하지만|는데|은데", text))
    for t in re.findall(r"[가-힣]{2,4}", text):
        if not has_adv:
            bare[t].append(lab)
    for m in ADV.finditer(text):
        adv_events.append((m.group(1), lab))
pol = {}
for p, labs in bare.items():
    if len(labs) >= 5:
        maj = 1 if sum(labs) * 2 >= len(labs) else 0
        pur = max(sum(labs), len(labs) - sum(labs)) / len(labs)
        if pur >= 0.8:
            pol[p] = maj
adv_by = collections.defaultdict(list)
for (stem, lab) in adv_events:
    if stem in pol:
        adv_by[stem].append(lab)
qual = []
for stem, labs in adv_by.items():
    if len(labs) >= 3:
        mp = pol[stem]
        flip = sum(1 for l in labs if l == (1 - mp)) / len(labs)
        qual.append({"stem": stem, "pol": mp, "n_adv": len(labs), "adv_pos_frac": sum(labs) / len(labs), "flip": flip})
qual.sort(key=lambda x: -x["n_adv"])
n_q = len(qual)
flip_frac = sum(q["flip"] for q in qual) / max(1, n_q)
adv_all = [l for (s, l) in adv_events if s in pol]
adv_base = sum(adv_all) / max(1, len(adv_all))
add_pred = 1.0 if adv_base < 0.5 else 0.0
add_acc = sum((1 - q["adv_pos_frac"]) if add_pred == 1.0 else q["adv_pos_frac"] for q in qual) / max(1, n_q)
d_nat = len(adv_all) / total_mb
POWERED = (n_q >= 30) and (flip_frac >= 0.75) and (flip_frac - add_acc >= 0.2)
res = {"n_qualified": n_q, "flip_frac": round(flip_frac, 4), "additive_ceiling_acc": round(add_acc, 4),
       "flip_minus_additive": round(flip_frac - add_acc, 4), "adv_marginal_pos": round(adv_base, 4),
       "d_nat_events_per_MB": round(d_nat, 3), "POWERED": bool(POWERED), "top": qual[:15]}
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=2)
print("=== A0-ADV (역접 XOR) ===", flush=True)
print(f"n_q={n_q} flip={flip_frac:.3f} add_ceiling={add_acc:.3f} flip-add={flip_frac-add_acc:.3f} d_nat={d_nat:.2f}/MB", flush=True)
print("POWERED" if POWERED else "NOT-POWERED (역접도 자연 held-out XOR signal 미달 → XOR-class 완전 NOT-POWERED)", flush=True)
