#!/usr/bin/env python3
"""F2 datapath cell = self_vocab_corpustxt
Re-run the E1 order-distinguishing gate on archive/data/corpus.txt with vocab
REBUILT from corpus.txt itself (top-400 freq, re.findall [a-z]+). Prior E1 run used
MISMATCHED consciousness_anchor vocab -> n_qualified=0. Isolates vocab-mismatch from
true order-structure scarcity. $0 pure corpus stats; never loads 303M.
Gate: tokens=re.findall([a-z]+); vocab=top-400 by freq; for a=tok[i],b=tok[i+1] both
in vocab and a!=b, follower c=tok[i+2] -> trigram[(a,b)][c]+=1. pair_occ=sum. pair {a,b}
QUALIFIED iff both orders occur>=MIN_OCC(3). differ_frac=frac where top-follower(a,b)!=
top-follower(b,a). NON-DEGENERATE iff differ_frac>=2/3 AND n_qualified>=10; n<10 => INCONCLUSIVE-SPARSE.
Vocab rebuilt by pure frequency (no hand-pick) => not tune-to-green."""
import re, json, collections, os
CORPUS="/Users/mini/dancinlab/anima/archive/data/corpus.txt"
OUTDIR="/Users/mini/dancinlab/anima/state/g1g6_exhaustive_brainstorm/f2_datapath/self_vocab_corpustxt"
TOPK=400; MIN_OCC=3; POWER=10; DIFFER_THR=2.0/3.0
text=open(CORPUS,encoding="utf-8",errors="replace").read()
tokens=re.findall(r"[a-z]+",text.lower()); n_tokens=len(tokens)
freq=collections.Counter(tokens)
vocab_list=[w for w,_ in freq.most_common(TOPK)]; vocab=set(vocab_list)
trigram=collections.defaultdict(collections.Counter)
for i in range(n_tokens-2):
    a,b=tokens[i],tokens[i+1]
    if a in vocab and b in vocab and a!=b:
        trigram[(a,b)][tokens[i+2]]+=1
def pair_occ(p): return sum(trigram.get(p,{}).values())
def top_follower(p):
    ctr=trigram.get(p)
    if not ctr: return None
    return max(sorted(ctr.items()),key=lambda kv:kv[1])[0]
seen=set(); qualified=[]
for (a,b) in list(trigram.keys()):
    key=tuple(sorted((a,b)))
    if key in seen: continue
    seen.add(key); x,y=key
    oxy=pair_occ((x,y)); oyx=pair_occ((y,x))
    if oxy>=MIN_OCC and oyx>=MIN_OCC:
        txy=top_follower((x,y)); tyx=top_follower((y,x))
        qualified.append((x,y,oxy,oyx,txy,tyx,txy!=tyx))
n_qualified=len(qualified); n_differ=sum(1 for q in qualified if q[6])
differ_frac=(n_differ/n_qualified) if n_qualified else 0.0
verdict=("INCONCLUSIVE-SPARSE" if n_qualified<POWER else
         "NON-DEGENERATE-POWERED" if differ_frac>=DIFFER_THR else "DEGENERATE-POWERED")
sample=[{"a":q[0],"b":q[1],"occ_ab":q[2],"occ_ba":q[3],"tf_ab":q[4],"tf_ba":q[5],"differ":q[6]}
        for q in sorted(qualified,key=lambda q:-(q[2]+q[3]))[:25]]
result={"cell":"self_vocab_corpustxt","corpus":CORPUS,
    "vocab_source":"corpus.txt self, top-400 by frequency (re.findall [a-z]+)",
    "n_tokens":n_tokens,"n_unique_tokens":len(freq),"topk_vocab":TOPK,
    "vocab_min_freq":freq[vocab_list[-1]] if vocab_list else 0,"MIN_OCC":MIN_OCC,
    "n_ordered_bigram_types_in_vocab":len(trigram),"n_qualified":n_qualified,
    "n_differ":n_differ,"differ_frac":round(differ_frac,4),"power_threshold":POWER,
    "powered":n_qualified>=POWER,"verdict":verdict,"sample_qualified_top25":sample}
os.makedirs(OUTDIR,exist_ok=True)
json.dump(result,open(os.path.join(OUTDIR,"RESULT.json"),"w"),ensure_ascii=False,indent=2)
print(json.dumps({k:v for k,v in result.items() if k!="sample_qualified_top25"},ensure_ascii=False,indent=2))
print("--- top qualified sample ---")
for s in sample[:15]: print(s)
