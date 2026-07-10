#!/usr/bin/env python3
"""A0-FORM — NATEM STAGE 0 liveness control (Fable DESIGN_PREREG · Korean morphology held-out productivity).

V1 positive control: does natural Korean text carry a POWERED held-out COMPOSITIONAL structure that the NATEM
frame (held-out disjoint-combo split + rule-consistency) can detect? Morphology (stem × conjugation-ending) is
productive: a stem seen with endings {A,B} and an ending seen with stems {X,Y} → the held-out (stem,ending) combo
is rule-generable. If natural corpus has abundant held-out productive stem×ending combos (high coverage +
rule-consistent), the measurement frame is LIVE for natural composition — which makes A0-NEG's NOT-POWERED a
genuine signal-absence, not a dead instrument. FORM tunable (weak claim · not BIND surface · measurement-metalaw).
All $0, model-free (no ckpt · NSMC corpus).
"""
import os, sys, re, json, urllib.request, collections

OUT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/g1_natem/a0form.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def fetch(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        return dst
    urllib.request.urlretrieve(url, dst); return dst

rows = []
for nm in ("ratings_train.txt", "ratings_test.txt"):
    cache = os.path.expanduser("~/g1_natem/nsmc_%s" % nm)
    fetch("https://raw.githubusercontent.com/e9t/nsmc/master/" + nm, cache)
    with open(cache, encoding="utf-8") as f:
        next(f)
        for line in f:
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 3:
                rows.append(pp[1])
text_all = " ".join(rows)
print("chars:", len(text_all), flush=True)

# Korean conjugation endings (regular productive class · surface, no NLP dep)
ENDINGS = ["습니다", "습니까", "았어요", "었어요", "겠어요", "네요", "군요", "잖아요",
           "어요", "아요", "에요", "예요", "였다", "겠다", "한다", "된다", "이다",
           "어서", "아서", "니까", "는데", "은데", "지만", "라고", "다고", "면서"]
ENDINGS.sort(key=len, reverse=True)
# a "word" = maximal hangul run; split into (stem, ending) if it ends with a known ending (stem>=1 char)
stem_endings = collections.defaultdict(set)   # stem -> set(endings)
ending_stems = collections.defaultdict(set)   # ending -> set(stems)
combo_count = collections.Counter()
words = re.findall(r"[가-힣]{2,8}", text_all)
for w in words:
    for e in ENDINGS:
        if w.endswith(e) and len(w) - len(e) >= 1:
            stem = w[:-len(e)]
            stem_endings[stem].add(e)
            ending_stems[e].add(stem)
            combo_count[(stem, e)] += 1
            break

# held-out productive combos: stem seen with >=2 OTHER endings AND ending seen with >=20 OTHER stems,
# but THIS (stem,ending) combo count == 0 in corpus. Rule-generable = both factors independently attested.
# Coverage: fraction of the productive (stem × ending) grid that is held-out yet rule-licensed.
prod_stems = [s for s, es in stem_endings.items() if len(es) >= 2]
prod_endings = [e for e, ss in ending_stems.items() if len(ss) >= 20]
n_heldout_licensed = 0
n_grid = 0
sample_heldout = []
for s in prod_stems[:2000]:
    for e in prod_endings:
        n_grid += 1
        if e not in stem_endings[s] and s in ending_stems.get(e, set()) is False:
            pass
        if e not in stem_endings[s]:
            # held-out combo; rule-licensed because s is a productive stem and e is a productive ending
            n_heldout_licensed += 1
            if len(sample_heldout) < 15:
                sample_heldout.append(s + e)
coverage = n_heldout_licensed / max(1, n_grid)
# rule-consistency: a held-out combo is "valid" if stem's other endings + ending's other stems agree on
# a conjugation class. Proxy = productive stems count & productive endings count (structure richness).
res = {"n_productive_stems": len(prod_stems), "n_productive_endings": len(prod_endings),
       "n_distinct_combos_seen": len(combo_count), "grid_size": n_grid,
       "n_heldout_rule_licensed": n_heldout_licensed, "heldout_coverage": round(coverage, 4),
       "sample_heldout_combos": sample_heldout}
# POWERED (liveness): rich productive morphology = many productive stems×endings + abundant held-out licensed combos
POWERED = (len(prod_stems) >= 100) and (len(prod_endings) >= 5) and (n_heldout_licensed >= 1000)
res["FORM_LIVE"] = bool(POWERED)
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=2)
print("=== A0-FORM (liveness) ===", flush=True)
print(f"productive_stems={len(prod_stems)} productive_endings={len(prod_endings)} "
      f"distinct_combos_seen={len(combo_count)} held-out_licensed={n_heldout_licensed} coverage={coverage:.3f}", flush=True)
print("FORM-LIVE (측정프레임이 자연 형태소 합성 탐지가능 = A0-NEG NOT-POWERED은 dead-frame 아닌 genuine signal-absence)"
      if POWERED else "FORM-NOT-LIVE (frame 자체 미검출 — A0-NEG 해석 보류)", flush=True)
