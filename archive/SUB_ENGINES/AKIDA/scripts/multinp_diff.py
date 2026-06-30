"""multinp_diff.py -- diff HW(multi-NP) vs SW(single numpy) by y_sha256.

multinp records carry y_sha256 + y_len (the full y is too large to emit). Byte-
identity ⟺ y_sha256 + y_len match for every probe input AND weights_sha256 match.
Exit 0 iff fully identical (placement-invariant). Usage: multinp_diff.py hw sw
"""
import json, sys
def load(p):
    recs = {}; meta = None
    for l in open(p):
        l = l.strip()
        if not l: continue
        d = json.loads(l)
        if "meta" in d: meta = d["meta"]; continue
        recs[d["input_idx"]] = d
    return meta, recs
hm, hw = load(sys.argv[1]); sm, sw = load(sys.argv[2])
wmatch = hm.get("weights_sha256") == sm.get("weights_sha256")
print(f"axis=multinp layers={hm.get('layers')} units={hm.get('units')} "
      f"act_bits={hm.get('act_bits')} on_hw={hm.get('on_hardware')} "
      f"np_total={hm.get('np_total')} multi_np={hm.get('multi_np')} "
      f"n_seq={hm.get('n_sequences')} weights_match={wmatch}")
n_ident = 0; ndiv = 0
for idx in sorted(hw):
    h = hw[idx]; s = sw.get(idx)
    if s is None: print(f" idx{idx}: SW MISSING"); ndiv += 1; continue
    ident = (h["y_sha256"] == s["y_sha256"]) and (h["y_len"] == s["y_len"])
    if ident: n_ident += 1
    else: ndiv += 1
    print(f" idx{idx}: {'IDENT' if ident else 'DIVERGE'} "
          f"HW={h['y_sha256']}({h['y_len']}) SW={s['y_sha256']}({s['y_len']})")
ok = (ndiv == 0) and wmatch
print(f"SUMMARY axis=multinp: ident={n_ident}/{len(hw)} divergent={ndiv} "
      f"weights_match={wmatch} np_total={hm.get('np_total')} -> "
      f"{'PLACEMENT-INVARIANT' if ok else 'DIVERGENCE'}")
sys.exit(0 if ok else 1)
