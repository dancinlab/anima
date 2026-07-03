#!/usr/bin/env python3
"""Apply the A11 TPR (CLMT v0.3) forward-slot to core/decode.py (numpy scorer).

Two edits (idempotent):
  (1) clm_load_weights: after the optional CLMB block, parse an optional
      "CLMT" trailer -> bind_type=3, roles[R,d], S1 (=roWt-twin) + S1 bias.
  (2) _fwd_logits: add a bind_type==3 branch computing the TPR role-filler
      readout  out = sum_r S_r . (yn (Hadamard) roles[r]).
core/decode.hexa gets the byte-identical mirror (_clmd_load + _clmd_fwd_logits).
"""
import sys, io

path = sys.argv[1]
src = open(path).read()
if "CLMT" in src:
    print("already patched"); sys.exit(0)

# ---- edit (1): CLMT parse in clm_load_weights, before `return W` -------------
anchor_ret = "        # roWt is already Wo.T = (k, V); roB is already WoB (V,) — loaded above.\n\n    return W"
clmt_parse = '''        # roWt is already Wo.T = (k, V); roB is already WoB (V,) — loaded above.

    # ── optional CLMT TPR role-filler section (A11 CE-deleted TPR forward-slot) ──
    # "CLMT" = 67,76,77,84.  bind_type=3.  out = sum_r S_r . (yn ⊙ roles[r]).
    #   CLMT magic 67,76,77,84 | R:u8 | roles ext (R*d f32) | S1 conv block (V,d
    #   int4-sym) | S1 bias ext (V,).  The MAIN roW/roB slot carries S_0/S_0.bias.
    #   Absent => bind_type stays 0/1/2 (old golden .clm decode byte-identically).
    if (off + 5 <= len(rb)
            and rb[off] == 67 and rb[off + 1] == 76
            and rb[off + 2] == 77 and rb[off + 3] == 84):
        off += 4                                   # skip "CLMT"
        R = rb[off]; off += 1
        roles_flat, off = _load_ext(rb, off)       # (R*d,)
        S1W, off = _load_block(rb, off)            # (V, d) int4-sym
        S1B, off = _load_ext(rb, off)              # (V,)
        W["bind_type"] = 3
        W["R"] = int(R)
        W["roles"] = roles_flat.reshape(R, d)      # [R, d]
        W["S1Wt"] = S1W.T.copy()                   # (d, V)
        W["S1B"] = S1B
        # roWt=(d,V) holds S_0.T, roB=(V,) holds S_0.bias — loaded above (standard slot).

    return W'''
if anchor_ret not in src:
    # tolerate an ascii em-dash variant
    anchor_ret2 = anchor_ret.replace("—", "-")
    if anchor_ret2 in src:
        anchor_ret = anchor_ret2
        clmt_parse = clmt_parse.replace("—", "-").replace("⊙", "(x)")
    else:
        print("FATAL: load anchor not found"); sys.exit(2)
src = src.replace(anchor_ret, clmt_parse, 1)

# ---- edit (2): bind_type==3 branch in _fwd_logits ---------------------------
anchor_ro = '''    # readout: additive Conv1d (standard) OR Hadamard/linear bind (CLMB)
    if W.get("bind_type", 0) != 0:'''
new_ro = '''    # readout: standard | CLMB Hadamard/linear bind | CLMT TPR role-filler bind
    _bt = W.get("bind_type", 0)
    if _bt == 3:
        # CLMT TPR readout: out = sum_r S_r . (yn (Hadamard) roles[r]); S_0=roWt slot.
        roles = W["roles"]                        # [R, d]
        c0 = yn * roles[0]                        # [T, d]
        c1 = yn * roles[1]                        # [T, d]
        out_logits = (c0 @ W["roWt"] + W["roB"]) + (c1 @ W["S1Wt"] + W["S1B"])  # [T, V]
    elif _bt != 0:'''
if anchor_ro not in src:
    anchor_ro2 = anchor_ro.replace("—", "-")
    if anchor_ro2 in src:
        anchor_ro = anchor_ro2
    else:
        print("FATAL: readout anchor not found"); sys.exit(3)
src = src.replace(anchor_ro, new_ro, 1)

open(path, "w").write(src)
print("PATCHED", path)
