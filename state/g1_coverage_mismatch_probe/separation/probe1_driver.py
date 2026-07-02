#!/usr/bin/env python3
"""L8-cov separation probe — mac local run (aiden numpy broken, summer swap-thrash).
엔진-native core/decode.py(main) numpy byte-parity greedy. 재학습 없음, 기존 ckpt forward only.
"""
import sys, os, json, time
SCRATCH = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/mini/dancinlab/anima"
CKPT = "/Users/mini/anima-weights/g1_l8_cov/clm303_deep_L8_cov.clm"
DESIGN = os.path.join(REPO, "state/g1_coverage_prod_block/design.json")
OUT = os.path.join(REPO, "state/g1_coverage_mismatch_probe/separation/probe_out.json")
sys.path.insert(0, os.path.join(SCRATCH, "core"))
import numpy as np
import decode as clm

d = json.load(open(DESIGN))
C = d["concepts_en"]; A = d["attrs_en"]
covered = set(tuple(p) for p in d["covered_pairs"])
gate_pairs = [tuple(p) for p in d["held_out_gate_internal"]]
GEN = 30; T = 24
assert clm.clm_decodable(CKPT)
t0 = time.time()
W = clm.clm_load_weights(CKPT)
V = W["V"]
print(f"[load] V={V} d={W['d']} L={W['L']} E={W['E']} K={W['K']} in {time.time()-t0:.1f}s", flush=True)

def greedy(prefix, gen=GEN):
    sb = prefix.encode("utf-8","surrogateescape"); sl=len(sb)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si=sl-T+p; tok[p]=float(sb[si]) if si>=0 else 32.0
    out=bytearray()
    for _ in range(gen):
        lg=clm._fwd_logits(W,tok,T); row=lg[T-1]
        bi=0;bv=row[0]
        for k in range(1,V):
            if row[k]>bv: bv=row[k];bi=k
        out.append(bi); tok[:T-1]=tok[1:]; tok[T-1]=float(bi)
    return out.decode("utf-8","surrogateescape")

res={"single":[],"seen_pair":[],"heldout_gate_pair":[]}
single_idx=list(range(5))+[5,6,7,21,8,9]
print("\n===== (1) SEEN single-concept -> attr : '{C} brings ' =====",flush=True)
for i in single_idx:
    pfx=f"{C[i]} brings "; txt=greedy(pfx,24); h=A[i] in txt
    res["single"].append({"i":i,"concept":C[i],"attr":A[i],"prefix":pfx,"out":txt,"attr_hit":h})
    print(f"  [{'HIT ' if h else 'miss'}] {C[i]:>14}->{A[i]:<8} => {txt!r}",flush=True)

seen_pairs=[(5,21),(5,6),(1,7),(0,8),(4,5),(3,7),(7,15),(9,10),(6,9),(11,14),(0,9),(2,9)]
seen_pairs=[p for p in seen_pairs if p in covered]
print("\n===== (2) SEEN pairs (covered) : 'the {A} and the {B} yield ' =====",flush=True)
for (a,b) in seen_pairs:
    pfx=f"the {C[a]} and the {C[b]} yield "; txt=greedy(pfx,GEN)
    ha,hb=A[a] in txt,A[b] in txt
    res["seen_pair"].append({"pair":[a,b],"A":C[a],"B":C[b],"ra":A[a],"rb":A[b],"prefix":pfx,"out":txt,"ra_hit":ha,"rb_hit":hb})
    print(f"  [ra={'Y' if ha else '.'} rb={'Y' if hb else '.'}] {C[a]}+{C[b]} want {A[a]}+{A[b]} => {txt!r}",flush=True)

print("\n===== (3) HELD-OUT gate-internal pairs : 'the {A} and the {B} yield ' =====",flush=True)
for (a,b) in gate_pairs:
    pfx=f"the {C[a]} and the {C[b]} yield "; txt=greedy(pfx,GEN)
    ha,hb=A[a] in txt,A[b] in txt
    res["heldout_gate_pair"].append({"pair":[a,b],"A":C[a],"B":C[b],"ra":A[a],"rb":A[b],"prefix":pfx,"out":txt,"ra_hit":ha,"rb_hit":hb})
    print(f"  [ra={'Y' if ha else '.'} rb={'Y' if hb else '.'}] {C[a]}+{C[b]} want {A[a]}+{A[b]} => {txt!r}",flush=True)

# also: held-out gate SINGLE-concept prefix (RF-clean, both gate concepts fit alone)
print("\n===== (3b) HELD-OUT gate pair via SINGLE-concept prefix (RF-clean) '{A} brings ' =====",flush=True)
res["heldout_gate_single"]=[]
for (a,b) in gate_pairs:
    for x in (a,b):
        pfx=f"{C[x]} brings "; txt=greedy(pfx,20); h=A[x] in txt
        res["heldout_gate_single"].append({"i":x,"concept":C[x],"attr":A[x],"out":txt,"attr_hit":h})
# dedup single gate concepts already in (1); this loop redundant for gates already tested — keep unique
seen_ids=set()
uniq=[]
for r in res["heldout_gate_single"]:
    if r["i"] not in seen_ids: seen_ids.add(r["i"]); uniq.append(r)
res["heldout_gate_single"]=uniq
for r in uniq:
    print(f"  [{'HIT ' if r['attr_hit'] else 'miss'}] {r['concept']}->{r['attr']} => {r['out']!r}",flush=True)

summary={
 "single_attr_hit":[sum(x["attr_hit"] for x in res["single"]),len(res["single"])],
 "seen_pair_any":[sum(x["ra_hit"] or x["rb_hit"] for x in res["seen_pair"]),len(res["seen_pair"])],
 "seen_pair_both":[sum(x["ra_hit"] and x["rb_hit"] for x in res["seen_pair"]),len(res["seen_pair"])],
 "heldout_gate_any":[sum(x["ra_hit"] or x["rb_hit"] for x in res["heldout_gate_pair"]),len(res["heldout_gate_pair"])],
 "heldout_gate_both":[sum(x["ra_hit"] and x["rb_hit"] for x in res["heldout_gate_pair"]),len(res["heldout_gate_pair"])],
}
print("\n===== SUMMARY =====",flush=True)
for k,v in summary.items(): print(f"  {k}: {v[0]}/{v[1]}",flush=True)
json.dump({"ckpt":CKPT,"gen":GEN,"T":T,"results":res,"summary":summary},open(OUT,"w"),ensure_ascii=False,indent=1)
print(f"\n[done] {time.time()-t0:.1f}s -> {OUT}",flush=True)
