import re, json, collections
lines = [l.split("\t")[1] for l in open("/Users/mini/g1_natem/nsmc_ratings_train.txt", encoding="utf-8").read().splitlines()[1:] if len(l.split("\t"))>2]
N=len(lines)
c=collections.Counter()
# negator span occurrences (surface-level, the spans the encoder would match)
pats = {
  "free_안":   r"(?:^|\s)안\s",
  "free_못":   r"(?:^|\s)못\s",
  "bound_않":  r"지\s*않",
  "bound_못하": r"지\s*못하",
  "bound_아니": r"지\s*아니",
  "아니_free": r"(?:^|\s)아니\s",  # archaic? check count
}
for L in lines:
    for k,p in pats.items():
        c[k]+=len(re.findall(p,L))
# placebo candidate morphemes: frequency-matched non-negator, label-uncorrelated.
# NSMC label is col0 (0=neg,1=pos). Recompute with labels for correlation.
rows = [l.split("\t") for l in open("/Users/mini/g1_natem/nsmc_ratings_train.txt", encoding="utf-8").read().splitlines()[1:] if len(l.split("\t"))>2]
neg_span_total = c["free_안"]+c["free_못"]+c["bound_않"]+c["bound_못하"]+c["bound_아니"]
# candidate placebo morphemes (frequent, content-neutral, not negators): 진짜, 정말, 그냥, 너무, 완전, 영화
cand = ["진짜","정말","그냥","너무","완전","최고","그리고","때문","라고","보고","생각","사람","연기","스토리","배우","감동"]
cc=collections.Counter(); pol=collections.defaultdict(lambda:[0,0])
for r in rows:
    if len(r)<3: continue
    try: lab=int(r[2])
    except ValueError: continue
    if lab not in (0,1): continue
    t=r[1]
    for w in cand:
        n=t.count(w)
        if n:
            cc[w]+=n; pol[w][lab]+=1
out={"corpus_lines":N,"negator_spans":dict(c),"neg_span_total":neg_span_total,
     "placebo_candidates":{}}
for w in cand:
    total=cc[w]; p0,p1=pol[w][0],pol[w][1]
    lc = abs(p1-p0)/max(1,(p1+p0))   # label skew, want ~0
    ratio = total/max(1,neg_span_total)
    out["placebo_candidates"][w]={"count":total,"freq_ratio_vs_negspan":round(ratio,3),
        "label_skew":round(lc,3),"in_2x_band":0.5<=ratio<=2.0}
json.dump(out, open("/private/tmp/claude-501/-Users-mini-dancinlab-anima-v4/33bbfc0c-35c4-43b3-85b4-abb17a5e233d/scratchpad/openparams.json","w"), ensure_ascii=False, indent=2)
print("done")
