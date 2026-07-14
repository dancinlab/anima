"""C1b — how wide is the operator's surface coverage? Two surfaces is not a census.

C1 measured two unseen negation surfaces and got opposite answers: `별로 {s}지 않다` runs the rule
perfectly (Δ=−1.000, p=.000, both seeds) while `{s}지는 않다` sits dead centre of the null (p=.500).
That is enough to refute memorisation, but it is far too thin to CHOOSE a surface for C3 — pick from
a sample of two and the choice is a coin flip dressed up as a criterion.

So: widen the census. Every candidate is byte-audited against the pretraining corpus (0 occurrences
in arrow lines) — the audit that already killed Fable's own first candidate, `안 {s}다`, at 58 hits.

The point is NOT to find a surface where the answer comes out nicely. It is to find the surfaces
where the OPERATOR RUNS AT ALL — because on a surface where the operator does not run, asking
"does the CPT-written fact reach the operator" is asking about something that is not there, and the
≈0 you would get back is a surface artifact, not evidence about binding. That distinction is the
whole difference between a chosen instrument and tune-to-green.
"""
import json, sys

# Every one of these is byte-audited below; only 0-occurrence surfaces survive into the manifest.
CAND = [
    ("negL",  "{s}지 않다",        "TRAINED"),      # anchors
    ("negE",  "전혀 {s}지 않다",    "TRAINED"),
    ("negS",  "안 {s}고",          "TRAINED-weak"),
    ("novB",  "별로 {s}지 않다",    "novel"),        # C1: perfect
    ("novT",  "{s}지는 않다",      "novel"),        # C1: null
    ("novG",  "그다지 {s}지 않다",  "novel"),        # degree adverb, like 별로
    ("novJ",  "결코 {s}지 않다",    "novel"),        # emphatic, like 전혀
    ("novH",  "하나도 {s}지 않다",  "novel"),        # emphatic quantifier
    ("novA",  "그리 {s}지 않다",    "novel"),        # degree adverb
    ("novN",  "{s}지 않았다",       "novel"),        # past tense — inflection, not adverb
]
TMPL = "이 영화 {surf} => "

corpus = open(sys.argv[1], encoding="utf-8").read()
arrow = [l for l in corpus.split("\n") if "=>" in l]
nat = [l for l in corpus.split("\n") if "=>" not in l]
atoms = json.load(open(sys.argv[2]))["atoms"]
seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]

print("=== 바이트 감사 — arrow 등장 0회인 표면만 새 표면으로 인정")
keep, maxb = [], 0
for tag, pat, kind in CAND:
    na = sum(1 for s, _ in seen for l in arrow if pat.format(s=s) in l)
    nn = sum(1 for s, _ in seen for l in nat if pat.format(s=s) in l)
    ok = kind.startswith("TRAINED") or na == 0
    print("  %-16s %-12s arrow=%4d 자연문=%3d  %s" % (pat, kind, na, nn,
          "✅" if ok else "🔴 오염 — 탈락"))
    if ok:
        keep.append((tag, pat))

rows = []
for tag, pat in keep:
    for stem, pol in seen:
        surf = pat.format(s=stem)
        seed = TMPL.format(surf=surf)
        maxb = max(maxb, len(seed.encode()))
        rows.append({"a": stem, "b": tag, "p": stem, "surf": surf, "pol": pol, "flip": 1,
                     "seed": seed, "gold": "부정." if pol == 1 else "긍정.",
                     "counterfactual": "긍정." if pol == 1 else "부정.",
                     "gold_word": "부정" if pol == 1 else "긍정"})
json.dump({"format": "nbind-eval-v1", "task": "H_9328 C1b — surface-coverage census",
           "gen": 8, "win": 64, "seen": [], "heldout": rows},
          open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
print("\nC1b manifest: %d rows (%d stems x %d surfaces)  max_bytes=%d  %s"
      % (len(rows), len(seen), len(keep), maxb, "✅ win=64 커버" if maxb <= 64 else "🔴 초과"))
