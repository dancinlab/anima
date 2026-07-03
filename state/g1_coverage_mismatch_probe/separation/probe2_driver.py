#!/usr/bin/env python3
"""Addendum: HELD-OUT NON-GATE recombination — decisive ②(surface/window-lock) vs ③(real floor).
짧은 개념 쌍만(both가 T=24 window 안). 함께 학습 안 됨(held_out) but 개념 각각은 학습됨.
BOTH attr HIT => held-out 재조합 성립 => gate 실패=window/surface 아티팩트=② ; MISS => ③ 가능.
또 dilation/window 확인용으로 seen 짧은-쌍 대조군 포함.
"""
import sys, os, json, time
SCRATCH=os.path.dirname(os.path.abspath(__file__))
REPO="/Users/mini/dancinlab/anima"
CKPT="/Users/mini/anima-weights/g1_l8_cov/clm303_deep_L8_cov.clm"
DESIGN=os.path.join(REPO,"state/g1_coverage_prod_block/design.json")
OUT=os.path.join(REPO,"state/g1_coverage_mismatch_probe/separation/probe2_heldout_nongate.json")
sys.path.insert(0,os.path.join(SCRATCH,"core"))
import numpy as np, decode as clm
d=json.load(open(DESIGN)); C=d["concepts_en"]; A=d["attrs_en"]
covered=set(tuple(p) for p in d["covered_pairs"]); held=set(tuple(p) for p in d["held_out"])
T=24; GEN=26
W=clm.clm_load_weights(CKPT); V=W["V"]
print(f"[load] ok",flush=True)
def greedy(pfx,gen=GEN):
    sb=pfx.encode("utf-8","surrogateescape");sl=len(sb);tok=np.empty(T,dtype=np.float64)
    for p in range(T):
        si=sl-T+p;tok[p]=float(sb[si]) if si>=0 else 32.0
    out=bytearray()
    for _ in range(gen):
        lg=clm._fwd_logits(W,tok,T);row=lg[T-1];bi=0;bv=row[0]
        for k in range(1,V):
            if row[k]>bv:bv=row[k];bi=k
        out.append(bi);tok[:T-1]=tok[1:];tok[T-1]=float(bi)
    return out.decode("utf-8","surrogateescape")
# held-out non-gate pairs w/ short concepts (both fit in ~24B window)
ho=[(30,31),(30,33),(33,35),(11,29),(25,31),(8,22),(9,21),(17,24),(14,30),(15,19),(12,23),(22,25),(27,33),(16,37)]
res={"heldout_nongate":[], "seen_short_ctrl":[]}
def winlen(a,b): return len(f"the {C[a]} and the {C[b]} yield ".encode())
print("\n=== HELD-OUT non-gate pairs (never co-trained; concepts each trained) ===",flush=True)
for (a,b) in ho:
    assert (a,b) in held, f"{(a,b)} not held-out"
    pfx=f"the {C[a]} and the {C[b]} yield ";txt=greedy(pfx)
    ha,hb=A[a] in txt,A[b] in txt
    res["heldout_nongate"].append({"pair":[a,b],"A":C[a],"B":C[b],"ra":A[a],"rb":A[b],"winB":winlen(a,b),"out":txt,"ra_hit":ha,"rb_hit":hb})
    print(f"  [ra={'Y' if ha else '.'} rb={'Y' if hb else '.'}] win={winlen(a,b)}B {C[a]}+{C[b]} want {A[a]}+{A[b]} => {txt!r}",flush=True)
# seen SHORT control (covered pairs, short concepts, both in-window) to show mapping fires when window OK
seen_short=[(30,34) if (30,34) in covered else None]
# pick covered short pairs
cand=[(a,b) for (a,b) in covered if winlen(a,b)<=28 and a>=5 and b>=5]
cand=sorted(cand,key=lambda p:winlen(*p))[:10]
print("\n=== SEEN short control (covered, both in-window) ===",flush=True)
for (a,b) in cand:
    pfx=f"the {C[a]} and the {C[b]} yield ";txt=greedy(pfx)
    ha,hb=A[a] in txt,A[b] in txt
    res["seen_short_ctrl"].append({"pair":[a,b],"win":winlen(a,b),"ra":A[a],"rb":A[b],"out":txt,"ra_hit":ha,"rb_hit":hb})
    print(f"  [ra={'Y' if ha else '.'} rb={'Y' if hb else '.'}] win={winlen(a,b)}B {C[a]}+{C[b]} want {A[a]}+{A[b]} => {txt!r}",flush=True)
sh=res["heldout_nongate"]; sc=res["seen_short_ctrl"]
summ={"heldout_nongate_both":[sum(x["ra_hit"] and x["rb_hit"] for x in sh),len(sh)],
      "heldout_nongate_any":[sum(x["ra_hit"] or x["rb_hit"] for x in sh),len(sh)],
      "seen_short_both":[sum(x["ra_hit"] and x["rb_hit"] for x in sc),len(sc)],
      "seen_short_any":[sum(x["ra_hit"] or x["rb_hit"] for x in sc),len(sc)]}
print("\n=== SUMMARY ===",flush=True)
for k,v in summ.items():print(f"  {k}: {v[0]}/{v[1]}",flush=True)
json.dump({"results":res,"summary":summ},open(OUT,"w"),ensure_ascii=False,indent=1)
print(f"[done] -> {OUT}",flush=True)
