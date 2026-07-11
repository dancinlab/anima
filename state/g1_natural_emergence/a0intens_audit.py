#!/usr/bin/env python3
"""A0-INTENS — NATEM STAGE 0 extension ($0 · degree-modifier composition · non-XOR lens).

Beyond the XOR class (A0-NEG negation, A0-ADV adversative), does a DIFFERENT natural compositional axis —
degree modification (intensifier × adjective) — carry a POWERED held-out non-additive recombination signal?
Two intensifier polarities: amplifiers (너무/정말/진짜/매우 · preserve polarity, expected ADDITIVE) vs
downtoners/NPIs (별로/전혀/그다지 · flip toward negative, XOR-like). Audit held-out (intensifier, adjective-stem)
combos: does the review label follow a compositional rule beyond the additive marginal? Model-free · NSMC ·
tests whether the Hahn-Goyal 'in-context compositional operations' survive as HELD-OUT signal for a non-XOR axis.
"""
import os, sys, re, json, urllib.request, collections
OUT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/g1_natem/a0intens.json")
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

AMP = ["너무", "정말", "진짜", "매우", "완전", "아주"]      # amplifiers (preserve)
DOWN = ["별로", "전혀", "그다지", "딱히", "그닥"]            # downtoners/NPI (flip→neg)
INTENS = AMP + DOWN
# (intensifier, following adjective-stem) pairs
pair_ev = collections.defaultdict(list)   # (intens, stem) -> labels
bare = collections.defaultdict(list)      # stem bare polarity
for i, (text, lab) in enumerate(rows):
    used = set()
    for it in INTENS:
        for m in re.finditer(re.escape(it) + r"\s*([가-힣]{2,4})", text):
            pair_ev[(it, m.group(1))].append(lab); used.add(m.group(1))
    for t in re.findall(r"[가-힣]{2,4}", text):
        if t not in used and t not in INTENS:
            bare[t].append(lab)
pol = {}
for s, labs in bare.items():
    if len(labs) >= 5:
        maj = 1 if sum(labs) * 2 >= len(labs) else 0
        if max(sum(labs), len(labs) - sum(labs)) / len(labs) >= 0.8:
            pol[s] = maj
# held-out combo qualified: pol(stem) certified · pair >=3 occurrences
qual = []
for (it, stem), labs in pair_ev.items():
    if stem in pol and len(labs) >= 3:
        mp = pol[stem]
        is_down = it in DOWN
        # compositional rule: amplifier keeps pol(stem); downtoner flips to negative(0)
        expected = 0 if is_down else mp
        acc = sum(1 for l in labs if l == expected) / len(labs)
        qual.append({"it": it, "stem": stem, "down": is_down, "pol": mp, "n": len(labs),
                     "pos_frac": sum(labs) / len(labs), "rule_acc": acc})
qual.sort(key=lambda x: -x["n"])
n_q = len(qual)
rule_acc = sum(q["rule_acc"] for q in qual) / max(1, n_q)
# additive ceiling: marginal-only predictor (pol(stem) ignoring intensifier)
add_acc = sum((q["pos_frac"] if q["pol"] == 1 else 1 - q["pos_frac"]) for q in qual) / max(1, n_q)
# downtoner-only sub-analysis (the XOR-like sub-signal)
downq = [q for q in qual if q["down"]]
down_flip = sum(q["rule_acc"] for q in downq) / max(1, len(downq))
d_nat = sum(len(v) for v in pair_ev.values()) / total_mb
POWERED = (n_q >= 30) and (rule_acc >= 0.75) and (rule_acc - add_acc >= 0.2)
res = {"n_qualified": n_q, "rule_acc": round(rule_acc, 4), "additive_ceiling": round(add_acc, 4),
       "rule_minus_additive": round(rule_acc - add_acc, 4), "n_downtoner": len(downq),
       "downtoner_flip_acc": round(down_flip, 4), "d_nat_events_per_MB": round(d_nat, 3),
       "POWERED": bool(POWERED), "top": qual[:15]}
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=2)
print("=== A0-INTENS (degree-modifier 조합·non-XOR 축) ===", flush=True)
print(f"n_q={n_q} rule_acc={rule_acc:.3f} additive_ceiling={add_acc:.3f} rule-add={rule_acc-add_acc:.3f} "
      f"downtoner_flip={down_flip:.3f}(n={len(downq)}) d_nat={d_nat:.1f}/MB", flush=True)
print("POWERED" if POWERED else "NOT-POWERED (degree 조합도 held-out non-additive signal 미달 = 자연 held-out compositional signal 부재가 XOR 넘어 broad)", flush=True)
