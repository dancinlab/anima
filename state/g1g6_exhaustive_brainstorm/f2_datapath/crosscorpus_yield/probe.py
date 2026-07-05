#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F2 crosscorpus_yield — $0 pure-corpus-statistic breadth probe.
Gate metric reference-matched to the E1 $0 pre-gate mechanism (per task spec):
 - whitespace tokenize; PER-CORPUS vocab = top-400 tokens by frequency.
 - ordered adjacent concept pair (a,b): t_i,t_{i+1} both in vocab, a!=b.
 - follower = t_{i+2}; top-follower(a,b)=most-common follower after "a b".
 - unordered {a,b} QUALIFIED iff both orders occur >= MIN_OCC(3).
 - differ_frac = frac qualified where top-follower(a,b)!=top-follower(b,a).
 - NON-DEGENERATE-POWERED iff differ_frac>=2/3 AND n_qualified>=10.
"""
import json
from collections import Counter, defaultdict

MIN_OCC=3; TOP_VOCAB=400; POWER=10; FRAC_BAR=2.0/3.0
OUTDIR="/Users/mini/dancinlab/anima/state/g1g6_exhaustive_brainstorm/f2_datapath/crosscorpus_yield"
CORPORA={
 "consciousness_anchor":"/Users/mini/dancinlab/anima/archive/state_legacy/anima_phase1a1_color_cosmology_2026_05_12/consciousness_anchor.txt",
 "corpus":"/Users/mini/dancinlab/anima/archive/data/corpus.txt",
 "consciousness_self_ref":"/Users/mini/dancinlab/anima/archive/data/consciousness_self_ref.txt",
 "self_play_200":"/Users/mini/dancinlab/anima/archive/data/self_play_200.txt",
 "ko_wiki":"/Users/mini/dancinlab/anima/archive/data/.corpus_cache/.corpus_cache/ko_wiki.txt",
}
def tokenize(p):
    t=[]
    with open(p,"r",encoding="utf-8",errors="replace") as f:
        for line in f: t.extend(line.split())
    return t
def analyze(p):
    toks=tokenize(p); ntok=len(toks)
    freq=Counter(toks)
    vocab=set(w for w,_ in freq.most_common(TOP_VOCAB))
    pair_follow=defaultdict(Counter); pair_count=Counter()
    n=len(toks)
    for i in range(n-1):
        a,b=toks[i],toks[i+1]
        if a in vocab and b in vocab and a!=b:
            pair_count[(a,b)]+=1
            if i+2<n: pair_follow[(a,b)][toks[i+2]]+=1
    seen=set(); n_qualified=0; n_differ=0; examples=[]
    for (a,b) in list(pair_count.keys()):
        key=tuple(sorted((a,b)))
        if key in seen: continue
        c_ab=pair_count[(a,b)]; c_ba=pair_count[(b,a)]
        if c_ab>=MIN_OCC and c_ba>=MIN_OCC:
            seen.add(key); n_qualified+=1
            tf_ab=pair_follow[(a,b)].most_common(1); tf_ba=pair_follow[(b,a)].most_common(1)
            f_ab=tf_ab[0][0] if tf_ab else None; f_ba=tf_ba[0][0] if tf_ba else None
            differ=(f_ab!=f_ba)
            if differ: n_differ+=1
            if len(examples)<12:
                examples.append({"pair":key,"c_ab":c_ab,"c_ba":c_ba,"follow_ab":f_ab,"follow_ba":f_ba,"differ":differ})
    differ_frac=(n_differ/n_qualified) if n_qualified else 0.0
    per_mtok=(n_qualified/(ntok/1e6)) if ntok else 0.0
    if n_qualified>=POWER and differ_frac>=FRAC_BAR: verdict="NON-DEGENERATE-POWERED"
    elif n_qualified>=POWER: verdict="DEGENERATE-POWERED"
    else: verdict="INCONCLUSIVE-SPARSE"
    return {"path":p,"n_tokens":ntok,"vocab_size":len(vocab),"n_qualified":n_qualified,
            "n_differ":n_differ,"differ_frac":round(differ_frac,4),
            "qualified_per_Mtoken":round(per_mtok,3),"verdict":verdict,"examples":examples}
def main():
    out={"MIN_OCC":MIN_OCC,"TOP_VOCAB":TOP_VOCAB,"POWER":POWER,"FRAC_BAR":FRAC_BAR,"corpora":{}}
    for name,path in CORPORA.items():
        try: out["corpora"][name]=analyze(path)
        except Exception as e: out["corpora"][name]={"error":str(e)}
        r=out["corpora"][name]
        print(f"{name:24s} tok={r.get('n_tokens',0):>10,} n_qual={r.get('n_qualified',0):>4} "
              f"differ_frac={r.get('differ_frac',0):.3f} per_Mtok={r.get('qualified_per_Mtoken',0):>7.2f} {r.get('verdict','?')}")
    any_powered=any(r.get("n_qualified",0)>=POWER for r in out["corpora"].values())
    any_nondeg=any(r.get("verdict")=="NON-DEGENERATE-POWERED" for r in out["corpora"].values())
    max_qual=max((r.get("n_qualified",0) for r in out["corpora"].values()),default=0)
    out["breadth"]={"any_corpus_powered":any_powered,"any_corpus_non_degenerate_powered":any_nondeg,
        "max_n_qualified":max_qual,
        "conclusion":("UNIVERSAL-STARVATION" if not any_powered else ("CORPUS-SPECIFIC-DENSE" if any_nondeg else "POWERED-BUT-DEGENERATE"))}
    print("\nBREADTH:",json.dumps(out["breadth"]))
    import os; os.makedirs(OUTDIR,exist_ok=True)
    with open(OUTDIR+"/RESULT.json","w") as f: json.dump(out,f,ensure_ascii=False,indent=2)
    with open(OUTDIR+"/probe.py","w") as f:
        f.write(open(__file__).read())
if __name__=="__main__": main()
