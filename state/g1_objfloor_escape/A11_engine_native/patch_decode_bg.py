#!/usr/bin/env python3
"""Apply the A11 ByteGPT-TPR (BGT trailer) forward-slot to core/decode.py.
  (1) bg_load: parse optional "BGT\\x01" trailer -> tpr_roles[R,d], tpr_S1[V,d].
  (2) bg_forward_last_W: TPR readout branch out = head.(h*roles0) + S1.(h*roles1).
  (3) bytegpt_decode_topk_sampled_W: force full-forward for TPR (KV path bypasses head).
"""
import sys
path = sys.argv[1]
src = open(path).read()
if "tpr_roles" in src:
    print("already bg-patched"); sys.exit(0)

# (1) bg_load BGT parse — insert before the bg_load return dict
anchor1 = '''            blk, off = _bg_read_bind_block(rb, off, d)
            bind.append(blk)

    return {"ok": True, "vocab": vocab,'''
new1 = '''            blk, off = _bg_read_bind_block(rb, off, d)
            bind.append(blk)

    # ── optional BGT TPR readout trailer (A11 CE-deleted TPR forward-slot) ──
    # "BGT\\x01"=66,71,84,1 after head (+ any BGB). R:u32 | roles[R*d] | S1[V*d] f32.
    # head slot carries S_0. Absent => tpr_roles=None (byte-identical plain decode).
    tpr_roles = None; tpr_S1 = None
    if (off + 8 <= len(rb) and rb[off] == 66 and rb[off + 1] == 71
            and rb[off + 2] == 84 and rb[off + 3] == 1):
        off += 4
        Rt = _bg_rd_u32(rb, off); off += 4
        tpr_roles = _rd_f32(rb, off, Rt * d).reshape(Rt, d); off += Rt * d * 4
        tpr_S1 = _rd_f32(rb, off, vocab * d).reshape(vocab, d); off += vocab * d * 4

    return {"ok": True, "vocab": vocab, "tpr_roles": tpr_roles, "tpr_S1": tpr_S1,'''
assert anchor1 in src, "bg_load anchor not found"
src = src.replace(anchor1, new1, 1)

# (2) bg_forward_last_W TPR readout branch
anchor2 = '''    lastrow = _bg_layernorm_rows(x[T - 1:T], W["lnfw"], W["lnfb"], 1, d)[0]   # [d]
    logits = W["head"] @ lastrow                            # [vocab]
    return logits'''
new2 = '''    lastrow = _bg_layernorm_rows(x[T - 1:T], W["lnfw"], W["lnfb"], 1, d)[0]   # [d]
    if W.get("tpr_roles") is not None:
        rl = W["tpr_roles"]                                 # [R, d]
        logits = W["head"] @ (lastrow * rl[0]) + W["tpr_S1"] @ (lastrow * rl[1])  # TPR slot
    else:
        logits = W["head"] @ lastrow                        # [vocab]
    return logits'''
assert anchor2 in src, "bg_forward_last_W anchor not found"
src = src.replace(anchor2, new2, 1)

# (3) force full-forward for TPR (KV path bypasses the head)
anchor3 = '''    vocab = W["vocab"]
    toks = _seed_to_ids(seed_ids)
    outl = []
    rng = _mix32(seed_rng)
    st = {'cache': None, 'start': None}'''
new3 = '''    if W.get("tpr_roles") is not None:
        return bytegpt_decode_topk_sampled_W_full(W, seed_ids, gen, top_k, temp, seed_rng)
    vocab = W["vocab"]
    toks = _seed_to_ids(seed_ids)
    outl = []
    rng = _mix32(seed_rng)
    st = {'cache': None, 'start': None}'''
assert anchor3 in src, "decode dispatch anchor not found"
src = src.replace(anchor3, new3, 1)

open(path, "w").write(src)
print("BG_PATCHED", path)
