"""frontier_diff.py -- diff HW vs SW frontier raster JSONL by input_idx.

Reads two JSONL files (frontier_hw.py and frontier_sw.py output for the SAME
--axis/--act-bits/--wseed) and reports per-input y_sha256 match + |Δ| max per
neuron. Exit 0 iff every input byte-identical (max Hamming 0).

Usage: python frontier_diff.py hw.jsonl sw.jsonl
"""
import json, sys
def load(p):
    recs={}; meta=None
    for l in open(p):
        l=l.strip()
        if not l: continue
        d=json.loads(l)
        if "meta" in d: meta=d["meta"]; continue
        recs[d["input_idx"]]=d
    return meta,recs
hm,hw=load(sys.argv[1]); sm,sw=load(sys.argv[2])
print(f"axis={hm.get('axis')} act_bits={hm.get('act_bits')} wseed={hm.get('wseed')} "
      f"HWw={hm.get('weights_sha256')} SWw={sm.get('weights_sha256')} "
      f"weights_match={hm.get('weights_sha256')==sm.get('weights_sha256')}")
n_ident=0; max_h=0; ndiv=0
for idx in sorted(hw):
    h=hw[idx]; s=sw.get(idx)
    if s is None: print(f" idx{idx}: SW MISSING"); ndiv+=1; continue
    ident=h["y_sha256"]==s["y_sha256"]
    ham=sum(1 for a,b in zip(h["y"],s["y"]) if a!=b)
    dmax=max((abs(a-b) for a,b in zip(h["y"],s["y"])),default=0)
    max_h=max(max_h,ham)
    if ident: n_ident+=1
    else: ndiv+=1
    print(f" idx{idx}: {'IDENT' if ident else 'DIVERGE'} HW={h['y_sha256']} SW={s['y_sha256']} hamming={ham} |Δ|max={dmax}")
print(f"SUMMARY axis={hm.get('axis')}: ident={n_ident}/{len(hw)} divergent={ndiv} max_hamming={max_h}")
sys.exit(0 if ndiv==0 else 1)
