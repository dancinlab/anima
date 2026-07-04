#!/usr/bin/env python3
# F5 fixture assembler. Inputs:
#   emits.tsv          : concept<TAB>tidx<TAB>emit   (48 rows, 16 concepts x 3 templates)
#   oracle_ranks.tsv   : concept<TAB>tidx<TAB>rank_true<TAB>rank_decoy
#       rank_true  = rank (1..16) of the TRUE concept when I (opus, out-of-alveolus oracle)
#                    rank all 16 concepts by fit to the emit (concept token stripped).
#       rank_decoy = rank of the FIXED-permutation decoy concept d=(cidx+7)%16 for that emit
#                    (the shuffle control: emit judged against a wrong referent).
# Output: fixture.tsv  cidx tidx rr_diff rr_self rr_shuf f0..f7   (concept-major, 48 rows)
import sys, math

CONCEPTS = ["canyon","tundra","cathedral","cello","scorpion","windmill",
            "parasol","anthill","microscope","landslide","sundial","fern",
            "pier","blizzard","lodestone","mast"]
VOWELS=set("aeiou")

def feats(e):
    b=e.encode('utf-8','ignore'); n=max(len(b),1)
    L=len(b)
    mean=sum(b)/n/255.0
    distinct=len(set(b))/n
    sp=sum(1 for x in b if x==32)/n
    alpha=[x for x in b if (65<=x<=90 or 97<=x<=122)]
    ar=len(alpha)/n
    vr=(sum(1 for x in alpha if chr(x).lower() in VOWELS)/max(len(alpha),1))
    up=sum(1 for x in b if 65<=x<=90)/n
    from collections import Counter
    cnt=Counter(b); ent=-sum((c/n)*math.log2(c/n) for c in cnt.values())/8.0
    return [round(min(L/64.0,1.0),4),round(mean,4),round(distinct,4),round(sp,4),
            round(ar,4),round(vr,4),round(up,4),round(min(ent,1.0),4)]

def lcs_len(a,b):
    a=a.lower(); b=b.lower()
    if not a or not b: return 0
    dp=[0]*(len(b)+1); best=0
    for i in range(len(a)):
        ndp=[0]*(len(b)+1)
        for j in range(len(b)):
            if a[i]==b[j]:
                ndp[j+1]=dp[j]+1; best=max(best,ndp[j+1])
        dp=ndp
    return best

def selfpair_rr(emit, true_idx):
    # in-alveolus surface matcher: rank concepts by longest-common-substring to the emit.
    scores=[(lcs_len(emit,CONCEPTS[k]),k) for k in range(16)]
    scores.sort(key=lambda x:(-x[0],x[1]))
    order=[k for _,k in scores]
    rank=order.index(true_idx)+1
    return round(1.0/rank,4)

def main():
    emits={}
    for ln in open('emits.tsv'):
        ln=ln.rstrip('\n')
        if not ln: continue
        p=ln.split('\t')
        if len(p)<3: p=p+['']*(3-len(p))
        c,t,e=p[0],int(p[1]),'\t'.join(p[2:])
        emits[(c,t)]=e
    ranks={}
    for ln in open('oracle_ranks.tsv'):
        ln=ln.strip()
        if not ln or ln.startswith('#'): continue
        c,t,rt,rd=ln.split('\t')
        ranks[(c,int(t))]=(int(rt),int(rd))
    out=[]
    for ci,c in enumerate(CONCEPTS):
        for t in range(3):
            e=emits.get((c,t),'')
            rt,rd=ranks.get((c,t),(16,16))
            rr_diff=round(1.0/rt,4); rr_shuf=round(1.0/rd,4)
            rr_self=selfpair_rr(e,ci)
            f=feats(e)
            out.append([ci,t,rr_diff,rr_self,rr_shuf]+f)
    with open('fixture.tsv','w') as w:
        for r in out:
            w.write('\t'.join(map(str,r))+'\n')
    print("wrote fixture.tsv rows=",len(out))
    import statistics as st
    print("D_diff=",round(st.mean(r[2] for r in out),4),
          "D_self=",round(st.mean(r[3] for r in out),4),
          "D_shuf=",round(st.mean(r[4] for r in out),4))

if __name__=='__main__': main()
