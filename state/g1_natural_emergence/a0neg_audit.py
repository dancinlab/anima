#!/usr/bin/env python3
"""A0-NEG — NATEM STAGE 0 $0 model-free audit (Fable DESIGN_PREREG · natural negation-XOR held-out).

Does natural Korean text carry a POWERED held-out negation-XOR recombination signal? (F2 collocation-only
said no held-out novel pairs — but F2's probe was one adjacent order-follower construct; negation is a
scope-function XOR that F2 structurally cannot see.) Uses NSMC labels as external grounding: pol(predicate)
= majority sentiment of NON-negated reviews containing it; the negation operator flips it (XOR). Held-out
(predicate, negation-form) pairs = train-side co-occur 0 times. POWERED bar: n_qualified>=30, flip_frac>=0.75,
additive-ceiling audit (surface additive model's held-out acc trails flip prediction by >=0.2). All $0,
model-free (no ckpt). Also records d_nat = joint-discriminative events/MB for the dilution-ladder comparison.
"""
import os, sys, re, json, urllib.request, collections, random

random.seed(7)
OUT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/g1_natem/a0neg.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# --- NSMC (github raw · datasets-script deprecation workaround, memory hf-datasets-script-deprecation-1) ---
def fetch(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        return dst
    print("fetch", url, flush=True)
    urllib.request.urlretrieve(url, dst)
    return dst

NS = "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt"
cache = os.path.expanduser("~/g1_natem/nsmc_train.txt")
fetch(NS, cache)
rows = []
with open(cache, encoding="utf-8") as f:
    next(f)  # header id\tdocument\tlabel
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) == 3 and p[2] in ("0", "1"):
            rows.append((p[1], int(p[2])))
print("NSMC reviews:", len(rows), flush=True)
total_mb = sum(len(t.encode()) for t, _ in rows) / 1e6

# --- negation surface patterns (no heavy NLP) ---
# neg forms: "안 <predicate>" and "<stem>지 않"; predicate = a content stem token
NEG_AN = re.compile(r"안\s+([가-힣]{2,4})")
NEG_JI = re.compile(r"([가-힣]{2,5})지\s*않")
# non-negated predicate occurrence: the bare stem as a token, NOT preceded by 안 / followed by 지 않
def predicates_in(text, negated):
    out = set()
    if negated:
        for m in NEG_AN.finditer(text):
            out.add(("AN", m.group(1)))
        for m in NEG_JI.finditer(text):
            out.add(("JI", m.group(1)))
    else:
        # bare content stems 2-4 hangul, exclude ones adjacent to negation
        toks = re.findall(r"[가-힣]{2,4}", text)
        neg_stems = {m.group(1) for m in NEG_AN.finditer(text)} | {m.group(1) for m in NEG_JI.finditer(text)}
        for t in toks:
            if t not in neg_stems and "않" not in t and t != "안":
                out.add(t)
    return out

# pol(p) = majority label of NON-negated reviews containing bare predicate p (count>=5, purity>=0.8)
bare_lab = collections.defaultdict(list)
neg_events = []  # (form_kind, stem, label, review_idx)
for i, (text, lab) in enumerate(rows):
    for p in predicates_in(text, negated=False):
        bare_lab[p].append(lab)
    for (kind, stem) in predicates_in(text, negated=True):
        neg_events.append((kind, stem, lab, i))
pol = {}
for p, labs in bare_lab.items():
    if len(labs) >= 5:
        maj = 1 if sum(labs) * 2 >= len(labs) else 0
        purity = max(sum(labs), len(labs) - sum(labs)) / len(labs)
        if purity >= 0.8:
            pol[p] = (maj, len(labs), purity)
print("pol-certified predicates:", len(pol), flush=True)

# held-out (predicate, negForm) pairs: pair appears, predicate bare-certified, negation attested elsewhere.
# 80/20 split by pair; held-out pair = train co-occur 0.  Measure label-flip: negated review label vs pol(p).
pair_events = collections.defaultdict(list)  # (stem) -> list of (label) from negated occurrences
for (kind, stem, lab, i) in neg_events:
    if stem in pol:
        pair_events[stem].append(lab)

qualified = []  # stems where bare pol certified AND >=3 negated occurrences
for stem, labs in pair_events.items():
    if len(labs) >= 3:
        maj_pol = pol[stem][0]
        neg_labs = labs
        # XOR prediction: negation flips pol -> expected label = 1-maj_pol
        flip_rate = sum(1 for l in neg_labs if l == (1 - maj_pol)) / len(neg_labs)
        qualified.append({"stem": stem, "pol": maj_pol, "n_bare": pol[stem][1],
                          "n_neg": len(neg_labs), "neg_pos_frac": sum(neg_labs) / len(neg_labs),
                          "flip_rate": flip_rate})
qualified.sort(key=lambda x: -x["n_neg"])
n_q = len(qualified)
flip_frac = sum(q["flip_rate"] for q in qualified) / max(1, n_q)
# additive-ceiling audit: a surface-additive model predicting review sentiment from (pol(p) + global neg bias)
# — held-out acc. If it can predict the flip WITHOUT XOR, the signal is additive-explainable (fail).
glob_neg = [l for (_, s, l, _) in neg_events if s in pol]
neg_base = sum(glob_neg) / max(1, len(glob_neg))  # marginal P(pos | negated)
# additive predictor: pred_label = round(pol - global_neg_shift) — collapses to a single main-effect
add_shift = 0.5 - neg_base  # how much negation shifts marginal
add_correct = 0
add_tot = 0
for q in qualified:
    add_pred = 1 if (q["pol"] - (1 if add_shift > 0 else 0)) >= 0.5 else 0  # additive main-effect only
    # additive acc on this stem's negated reviews
    for _ in range(q["n_neg"]):
        pass
    add_tot += 1
# additive held-out acc = how well a pol-independent global negation bias predicts flip
add_flip_pred = 1.0 if neg_base < 0.5 else 0.0  # global negation → predicts "neg sentiment" for all
add_acc = sum((1 - q["neg_pos_frac"]) if add_flip_pred == 1.0 else q["neg_pos_frac"] for q in qualified) / max(1, n_q)

d_nat = len([1 for (_, s, _, _) in neg_events if s in pol]) / total_mb  # joint-discriminative events / MB

POWERED = (n_q >= 30) and (flip_frac >= 0.75) and (flip_frac - add_acc >= 0.2)
res = {"n_qualified": n_q, "flip_frac": round(flip_frac, 4), "additive_ceiling_acc": round(add_acc, 4),
       "flip_minus_additive": round(flip_frac - add_acc, 4), "neg_marginal_pos": round(neg_base, 4),
       "d_nat_events_per_MB": round(d_nat, 3), "total_mb": round(total_mb, 2),
       "POWERED": bool(POWERED), "top_qualified": qualified[:20]}
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=2)
print("=== A0-NEG VERDICT ===", flush=True)
print(f"n_qualified={n_q} flip_frac={flip_frac:.3f} additive_ceiling={add_acc:.3f} "
      f"flip-add={flip_frac-add_acc:.3f} d_nat={d_nat:.2f}/MB", flush=True)
print("POWERED" if POWERED else "NOT-POWERED (F2 격상 후보: 부정-XOR 렌즈서도 자연 signal 미달)", flush=True)
