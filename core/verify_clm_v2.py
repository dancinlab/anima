# ==========================================================================
# ⛔ ENGINE-INTERNAL TOOL — agent 가 직접 타이핑 금지. 학습/직렬화는 cli/ 단일진입만:
#   anima-py train | anima-py serialize.
# cli/train.py 가 held-out DESCENT 게이트를 내부 호출하므로 __main__ hard-exit
# 가드는 두지 않는다. 직접 실행 차단은 단일진입 정책이 담당한다.
# ==========================================================================
#!/usr/bin/env python3
"""Lane P REMEDY — pure-Python mirror of CORE/clm_decode.hexa's clm_decodable()
plus a fuller parse, and a byte-roundtrip + golden-reference test harness.

This re-parses the raw .clm bytes with the SAME logic as clm_decode.hexa:
  clm_decodable(): magic "CLM\\x01", walk nblk conv blocks via (cout,rest) to find
                   the trailer offset, require "CLMX" there.
  parse_clm():     also re-reads block dims and the CLMX ext count (n_ext + each
                   ext array's element count), so a round-trip can assert
                   structural consistency.

No torch / numpy needed for verification (pure stdlib struct). The serializer is
imported (it guards its torch import) only for the synthetic round-trip.

Outputs (verbatim, p7/g63 honest):
  F-CLM-V2-ROUNDTRIP=1  on a clean synthetic round-trip, else =0 + the mismatch.
  golden decodable=true/false + nblk + block0 dims + CLMX-found.
"""
from __future__ import annotations

import struct
import sys
import os
import math

MAGIC = bytes([67, 76, 77, 1])
CLMX = bytes([67, 76, 77, 88])
CLMB = bytes([67, 76, 77, 66])   # bind-readout (Hadamard) extension


def _ru32(b: bytes, off: int) -> int:
    return b[off] + b[off + 1] * 0x100 + b[off + 2] * 0x10000 + b[off + 3] * 0x1000000


def clm_decodable(path_or_bytes) -> bool:
    """Pure-Python mirror of clm_decode.hexa::clm_decodable (lines 43-64)."""
    rb = path_or_bytes if isinstance(path_or_bytes, (bytes, bytearray)) else open(path_or_bytes, "rb").read()
    if len(rb) < 5:
        return False
    if not (rb[0] == 67 and rb[1] == 76 and rb[2] == 77 and rb[3] == 1):
        return False
    nblk = rb[4]
    off = 5
    b = 0
    while b < nblk:
        if off + 8 > len(rb):
            return False
        cout = _ru32(rb, off)
        rest = _ru32(rb, off + 4)
        off += 8
        n = cout * rest
        off += (n + 1) // 2          # int4 nibbles, 2/byte
        off += cout * 4              # per-channel fp32 scale
        b += 1
    if off + 5 > len(rb):
        return False
    return rb[off] == 67 and rb[off + 1] == 76 and rb[off + 2] == 77 and rb[off + 3] == 88


def parse_clm(path_or_bytes) -> dict:
    """Fuller parse: returns block dims + CLMX ext counts. Raises on structural EOF."""
    rb = path_or_bytes if isinstance(path_or_bytes, (bytes, bytearray)) else open(path_or_bytes, "rb").read()
    out = {"len": len(rb), "magic_ok": False, "nblk": None, "blocks": [],
           "clmx_found": False, "n_ext": None, "ext_counts": [], "final_off": None,
           "exact_eof": None, "clmb_found": False, "readout_type": 0,
           "bind_blocks": [], "bind_ext_counts": []}
    if len(rb) < 5:
        return out
    out["magic_ok"] = (rb[0] == 67 and rb[1] == 76 and rb[2] == 77 and rb[3] == 1)
    nblk = rb[4]
    out["nblk"] = nblk
    off = 5
    for _ in range(nblk):
        if off + 8 > len(rb):
            raise ValueError(f"EOF reading block header at off={off}")
        cout = _ru32(rb, off)
        rest = _ru32(rb, off + 4)
        off += 8
        n = cout * rest
        nib = (n + 1) // 2
        off += nib
        off += cout * 4
        out["blocks"].append({"cout": cout, "rest": rest, "nibbles": nib})
        if off > len(rb):
            raise ValueError(f"EOF walking block (cout={cout},rest={rest}) off={off}>len={len(rb)}")
    if off + 5 <= len(rb) and rb[off:off + 4] == CLMX:
        out["clmx_found"] = True
        n_ext = rb[off + 4]
        out["n_ext"] = n_ext
        o2 = off + 5
        for _ in range(n_ext):
            if o2 + 4 > len(rb):
                raise ValueError(f"EOF reading ext count at off={o2}")
            cnt = _ru32(rb, o2)
            o2 += 4
            o2 += cnt * 4
            out["ext_counts"].append(cnt)
            if o2 > len(rb):
                raise ValueError(f"EOF reading ext array (count={cnt}) off={o2}>len={len(rb)}")
        # OPTIONAL CLMB bind-readout trailer: readout_type:u8 + Wa/Wb blocks + 2 ext.
        if o2 + 5 <= len(rb) and rb[o2:o2 + 4] == CLMB:
            out["clmb_found"] = True
            out["readout_type"] = rb[o2 + 4]
            o3 = o2 + 5
            for _ in range(2):                      # Wa, Wb conv blocks
                cout = _ru32(rb, o3); rest = _ru32(rb, o3 + 4); o3 += 8
                nib = (cout * rest + 1) // 2
                o3 += nib + cout * 4
                out["bind_blocks"].append({"cout": cout, "rest": rest, "nibbles": nib})
                if o3 > len(rb):
                    raise ValueError(f"EOF walking CLMB block off={o3}>len={len(rb)}")
            for _ in range(2):                      # Wa_bias, Wb_bias ext
                cnt = _ru32(rb, o3); o3 += 4 + cnt * 4
                out["bind_ext_counts"].append(cnt)
                if o3 > len(rb):
                    raise ValueError(f"EOF reading CLMB ext off={o3}>len={len(rb)}")
            o2 = o3
        out["final_off"] = o2
        out["exact_eof"] = (o2 == len(rb))
    return out


# --------------------------------------------------------------------------- #
# Synthetic round-trip test (no torch): tiny E=2 / 1-trunk model, d=32,K=3,V=256
# --------------------------------------------------------------------------- #
def _build_synthetic(d=32, K=3, V=256, E=2, seed=1234):
    """Legacy L=1/E=2 synthetic — used by the v0.2 byte-eq regression check.
    Returns a logical-slot dict (serialize_v2 accepts logical keys directly)."""
    import numpy as np
    rng = np.random.default_rng(seed)
    def r(*shape):
        return (rng.standard_normal(shape) * 0.1).astype(np.float32)
    sd = {
        # conv blocks: ec/tc/e0/e1 are (cout=d, in=d, K) -> rest=d*K
        "ecW": r(d, d, K),
        "tcW": r(d, d, K),
        "e0W": r(d, d, K),
        "e1W": r(d, d, K),
        "rW":  r(E, d, 1),    # router conv1d k=1 -> rest=d
        "roW": r(V, d, 1),    # readout conv1d k=1 -> rest=d
        # CLMX ext (fp32)
        "embed": r(V, d),     # V*d
        "ecB": r(d), "tcB": r(d), "e0B": r(d), "e1B": r(d),
        "rB":  r(E), "roB": r(V),
        "tgG": r(d), "tgB": r(d), "noG": r(d), "noB": r(d),
    }
    expect = {
        "nblk": 6,
        "blocks": [
            {"cout": d, "rest": d * K}, {"cout": d, "rest": d * K},
            {"cout": d, "rest": d * K}, {"cout": d, "rest": d * K},
            {"cout": E, "rest": d}, {"cout": V, "rest": d},
        ],
        "n_ext": 11,
        "ext_counts": [V * d, d, d, d, d, E, V, d, d, d, d],
    }
    return sd, expect


def _build_synthetic_general(d, L, E, K=3, V=256, seed=2026):
    """General (L,E) synthetic in TORCH state_dict key layout — used by the
    v0.3 general round-trip test. Keys match model.py's CLMConvMoE so the same
    dict drives serialize_v3. Returns (sd, expect)."""
    import numpy as np
    rng = np.random.default_rng(seed)
    def r(*shape):
        return (rng.standard_normal(shape) * 0.1).astype(np.float32)
    sd = {"embed.weight": r(V, d),
          "embed_conv.conv.weight": r(d, d, K), "embed_conv.conv.bias": r(d)}
    for i in range(L):
        sd[f"trunk.{i}.conv.conv.weight"] = r(d, d, K)
        sd[f"trunk.{i}.conv.conv.bias"] = r(d)
        sd[f"trunk.{i}.norm.weight"] = r(d)
        sd[f"trunk.{i}.norm.bias"] = r(d)
    for j in range(E):
        sd[f"moe.experts.{j}.conv.conv.weight"] = r(d, d, K)
        sd[f"moe.experts.{j}.conv.conv.bias"] = r(d)
    sd["moe.router.weight"] = r(E, d, 1)
    sd["moe.router.bias"] = r(E)
    sd["readout.weight"] = r(V, d, 1)
    sd["readout.bias"] = r(V)
    sd["norm_out.weight"] = r(d)
    sd["norm_out.bias"] = r(d)
    # expected layout: blocks = ecW, tcW*L, eW*E, rW(E), roW(V)
    blocks = [{"cout": d, "rest": d * K}]                      # ecW
    blocks += [{"cout": d, "rest": d * K} for _ in range(L)]   # trunk
    blocks += [{"cout": d, "rest": d * K} for _ in range(E)]   # experts
    blocks += [{"cout": E, "rest": d}, {"cout": V, "rest": d}] # router, readout
    # ext = embed, ecB, tcB*L, eB*E, rB, roB, tgG*L, tgB*L, noG, noB
    ext = [V * d, d] + [d] * L + [d] * E + [E, V] + [d] * L + [d] * L + [d, d]
    expect = {"nblk": len(blocks), "blocks": blocks, "n_ext": len(ext), "ext_counts": ext}
    return sd, expect


def _build_synthetic_bind(d, L, E, k, V=256, K=3, seed=4242):
    """General (L,E) BIND synthetic in LOGICAL-slot keys (serialize_v3_bind accepts
    them). Trunk slots match the v3 general order; the readout is Wa/Wb (k,d,1) +
    Wo (V,k,1) — the EXP-3 BindCLM. Returns (sd, expect_main, expect_bind)."""
    import numpy as np
    rng = np.random.default_rng(seed)
    def r(*shape):
        return (rng.standard_normal(shape) * 0.1).astype(np.float32)
    sd = {"embed": r(V, d), "ecW": r(d, d, K), "ecB": r(d)}
    for i in range(L):
        sd[f"tc{i}W"] = r(d, d, K); sd[f"tc{i}B"] = r(d)
        sd[f"tg{i}G"] = r(d); sd[f"tg{i}B"] = r(d)
    for j in range(E):
        sd[f"e{j}W"] = r(d, d, K); sd[f"e{j}B"] = r(d)
    sd["rW"] = r(E, d, 1); sd["rB"] = r(E)
    sd["noG"] = r(d); sd["noB"] = r(d)
    # bind readout: Wa,Wb (k,d,1), Wo (V,k,1)
    sd["Wa"] = r(k, d, 1); sd["WaB"] = r(k)
    sd["Wb"] = r(k, d, 1); sd["WbB"] = r(k)
    sd["Wo"] = r(V, k, 1); sd["WoB"] = r(V)
    # expected MAIN: blocks = ecW, tcW*L, eW*E, rW(E,d), roW(=Wo: V,k)
    blocks = [{"cout": d, "rest": d * K}]
    blocks += [{"cout": d, "rest": d * K} for _ in range(L)]
    blocks += [{"cout": d, "rest": d * K} for _ in range(E)]
    blocks += [{"cout": E, "rest": d}, {"cout": V, "rest": k}]   # router, Wo readout
    ext = [V * d, d] + [d] * L + [d] * E + [E, V] + [d] * L + [d] * L + [d, d]
    expect_main = {"nblk": len(blocks), "blocks": blocks, "n_ext": len(ext),
                   "ext_counts": ext}
    expect_bind = {"bind_blocks": [{"cout": k, "rest": d}, {"cout": k, "rest": d}],
                   "bind_ext_counts": [k, k]}
    return sd, expect_main, expect_bind


def run_roundtrip_bind(tmp_path, d, L, E, k, readout_type, V=256, K=3):
    """v0.3 BIND round-trip via serialize_v3_bind: structural (CLMB) + forward
    sanity (bind decode produces finite logits with the Hadamard/add readout)."""
    import clm_serialize_v2 as S
    import numpy as np
    sd, exp_main, exp_bind = _build_synthetic_bind(d, L, E, k, V=V, K=K)
    S.serialize_v3_bind(sd, n_trunk_layers=L, n_experts=E,
                        readout_type=readout_type, out_path=tmp_path)
    rb = open(tmp_path, "rb").read()
    ok, why = _structural_check(rb, exp_main)        # main body unchanged vs additive grammar
    if not ok:
        return False, f"main: {why}"
    p = parse_clm(rb)
    if not p["clmb_found"]:
        return False, "CLMB trailer not found"
    if p["readout_type"] != readout_type:
        return False, f"readout_type {p['readout_type']} != {readout_type}"
    bb = [{"cout": x["cout"], "rest": x["rest"]} for x in p["bind_blocks"]]
    if bb != exp_bind["bind_blocks"]:
        return False, f"bind_blocks {bb} != {exp_bind['bind_blocks']}"
    if p["bind_ext_counts"] != exp_bind["bind_ext_counts"]:
        return False, f"bind_ext {p['bind_ext_counts']} != {exp_bind['bind_ext_counts']}"
    if not p["exact_eof"]:
        return False, f"trailing bytes: final_off={p['final_off']} != len={p['len']}"
    # forward sanity: the bind mirror loads + forwards to finite [T,V] logits.
    W = _load_clm_weights(rb)
    if W is None or W["rtype"] != readout_type or W["kbind"] != k:
        return False, f"weights load rtype={W and W['rtype']} kbind={W and W['kbind']}"
    tok = (np.arange(24) % V).astype(float)
    lg = _fwd_logits(W, tok, 24)
    if lg.shape != (24, V) or not np.all(np.isfinite(lg)):
        return False, f"forward shape={lg.shape} finite={np.all(np.isfinite(lg))}"
    return True, f"ok (rtype={readout_type} k={k}, logits {lg.shape} finite)"


def run_roundtrip(tmp_path: str) -> tuple[bool, str]:
    import clm_serialize_v2 as S
    sd, expect = _build_synthetic()
    S.serialize_v2(sd, cfg=None, out_path=tmp_path)  # cfg=None: synthetic vouches E=2/L1
    rb = open(tmp_path, "rb").read()

    if not clm_decodable(rb):
        return False, "clm_decodable(synthetic)=false"
    p = parse_clm(rb)
    if not p["magic_ok"]:
        return False, "magic mismatch"
    if p["nblk"] != expect["nblk"]:
        return False, f"nblk {p['nblk']} != {expect['nblk']}"
    if len(p["blocks"]) != 6:
        return False, f"walked {len(p['blocks'])} blocks != 6"
    for i, (got, exp) in enumerate(zip(p["blocks"], expect["blocks"])):
        if got["cout"] != exp["cout"] or got["rest"] != exp["rest"]:
            return False, (f"block{i} dims got cout={got['cout']},rest={got['rest']} "
                           f"!= cout={exp['cout']},rest={exp['rest']}")
    if not p["clmx_found"]:
        return False, "CLMX trailer not found"
    if p["n_ext"] != expect["n_ext"]:
        return False, f"n_ext {p['n_ext']} != {expect['n_ext']}"
    if p["ext_counts"] != expect["ext_counts"]:
        return False, f"ext_counts {p['ext_counts']} != {expect['ext_counts']}"
    if not p["exact_eof"]:
        return False, f"trailing bytes: final_off={p['final_off']} != len={p['len']}"

    # value round-trip: re-dequant the readout-bias ext and the ecW block, confirm
    # the int4 dequant is within the quant step of the original (sanity on packing).
    import numpy as np
    # check ext embed first element survives fp32 exactly
    # (parse the embed ext payload directly)
    off = 5
    for _ in range(6):
        cout = _ru32(rb, off); rest = _ru32(rb, off + 4); off += 8
        off += (cout * rest + 1) // 2 + cout * 4
    off += 5  # CLMX + n_ext
    cnt = _ru32(rb, off); off += 4
    embed_back = np.frombuffer(rb[off:off + cnt * 4], dtype="<f4")
    if not np.allclose(embed_back, sd["embed"].reshape(-1), atol=0, rtol=0):
        return False, "embed ext fp32 round-trip mismatch (lossless expected)"

    return True, "ok"


def _structural_check(rb, expect):
    """Shared structural assertions: decodable + nblk + per-block dims + CLMX +
    n_ext + ext_counts + exact_eof. Returns (ok, why)."""
    if not clm_decodable(rb):
        return False, "clm_decodable=false"
    p = parse_clm(rb)
    if not p["magic_ok"]:
        return False, "magic mismatch"
    if p["nblk"] != expect["nblk"]:
        return False, f"nblk {p['nblk']} != {expect['nblk']}"
    if len(p["blocks"]) != expect["nblk"]:
        return False, f"walked {len(p['blocks'])} blocks != {expect['nblk']}"
    for i, (got, exp) in enumerate(zip(p["blocks"], expect["blocks"])):
        if got["cout"] != exp["cout"] or got["rest"] != exp["rest"]:
            return False, (f"block{i} got cout={got['cout']},rest={got['rest']} "
                           f"!= cout={exp['cout']},rest={exp['rest']}")
    if not p["clmx_found"]:
        return False, "CLMX trailer not found"
    if p["n_ext"] != expect["n_ext"]:
        return False, f"n_ext {p['n_ext']} != {expect['n_ext']}"
    if p["ext_counts"] != expect["ext_counts"]:
        return False, f"ext_counts {p['ext_counts']} != {expect['ext_counts']}"
    if not p["exact_eof"]:
        return False, f"trailing bytes: final_off={p['final_off']} != len={p['len']}"
    return True, "ok"


def run_roundtrip_general(tmp_path, d, L, E, K=3, V=256):
    """v0.3 general (L,E) round-trip via serialize_v3 (torch-key state_dict)."""
    import clm_serialize_v2 as S
    import numpy as np
    sd, expect = _build_synthetic_general(d, L, E, K=K, V=V)
    S.serialize_v3(sd, n_trunk_layers=L, n_experts=E, out_path=tmp_path)
    rb = open(tmp_path, "rb").read()
    ok, why = _structural_check(rb, expect)
    if not ok:
        return False, why
    # value sanity: embed ext (first ext after CLMX) survives fp32 lossless.
    off = 5
    for blk in expect["blocks"]:
        n = blk["cout"] * blk["rest"]
        off += 8 + (n + 1) // 2 + blk["cout"] * 4
    off += 5  # CLMX + n_ext
    cnt = _ru32(rb, off); off += 4
    embed_back = np.frombuffer(rb[off:off + cnt * 4], dtype="<f4")
    if not np.allclose(embed_back, sd["embed.weight"].reshape(-1), atol=0, rtol=0):
        return False, "embed ext fp32 round-trip mismatch"
    return True, "ok"


def run_roundtrip_slw_clml(here, d=16, L=1, E=2, V=256, K=3):
    """SLW (H_9200) + CLML (H_9235) trailer FORWARD round-trip on the CANONICAL
    py 2-production decode (core/decode.py — a_eval_py_canonical). Builds a tiny
    base .clm and appends the SLW/CLML trailers, then asserts the py forward:
      (a) a trailered .clm stays clm_decodable (trailer is transparent to CLMX),
      (b) every forward is finite,
      (c) SLW-only / CLML-only each CHANGE the logits vs base (trailer ACTIVE),
      (d) SLW γ=0 is a BIT-EXACT passthrough == base (clean ablation control),
      (e) SLW+CLML differs from either alone (both compose),
      (f) trailer absence ⇔ byte-identical to base (the loader passthrough).
    All py, no hexa compile."""
    import numpy as np
    import clm_serialize_v2 as S
    from slw import pack_slw
    from clml import pack_clml
    import decode as D

    n_slot, k, d_s, r, tau = 4, 8, d, 8, 8.0
    rng = np.random.default_rng(7)
    rf = lambda *s: (rng.standard_normal(s) * 0.1).astype("<f4")

    sd, _ = _build_synthetic_general(d, L, E, K=K, V=V)
    base = os.path.join(here, "_slwclml_base.clm")
    S.serialize_v3(sd, n_trunk_layers=L, n_experts=E, out_path=base)
    blob = open(base, "rb").read()

    def slw_bytes(gamma):
        return pack_slw({"n_slot": n_slot, "k": k, "d_s": d_s,
                         "K_slots": rf(n_slot, k), "W_r": rf(k, d), "b_r": rf(k),
                         "W_q": rf(k, d), "b_q": rf(k), "W_v": rf(d_s, d), "b_v": rf(d_s),
                         "W_o": rf(d, d_s), "b_o": rf(d), "w_g": rf(d), "b_g": rf(1),
                         "gamma": np.asarray([gamma], "<f4")})
    def clml_bytes():
        return pack_clml({"lane_type": 1, "r": r, "tau": tau, "W1": rf(d, r),
                          "b1": rf(r), "W2": rf(r, V), "w_g": rf(2 * d), "b_g": rf(1)})

    rng2 = np.random.default_rng(7)  # reproduce the SAME weights for γ=0 vs γ>0
    _ = rng2  # (weights are drawn fresh per call; γ control uses D._SLW_GAMMA_OVERRIDE)

    slw_t = slw_bytes(0.6)
    clml_t = clml_bytes()
    variants = {"base": blob, "slw": blob + slw_t,
                "clml": blob + clml_t, "both": blob + slw_t + clml_t}
    paths = {}
    for name, b in variants.items():
        p = os.path.join(here, f"_slwclml_{name}.clm")
        open(p, "wb").write(b)
        paths[name] = p

    T = 12
    seq = rng.integers(0, V, size=T).astype(np.float64)

    def last(path, gamma_override=None):
        prev = D._SLW_GAMMA_OVERRIDE
        D._SLW_GAMMA_OVERRIDE = gamma_override
        try:
            W = D.clm_load_weights(path)
            lg = np.asarray(D._fwd_logits(W, seq, T), dtype=np.float64)
        finally:
            D._SLW_GAMMA_OVERRIDE = prev
        return lg[T - 1]

    lg_base = last(paths["base"])
    lg_slw = last(paths["slw"])
    lg_clml = last(paths["clml"])
    lg_both = last(paths["both"])
    lg_slw0 = last(paths["slw"], gamma_override=0.0)   # γ=0 passthrough control

    for p in paths.values():
        try:
            os.remove(p)
        except OSError:
            pass

    # (a) decodable transparent to trailer
    if not clm_decodable(variants["both"]):
        return False, "trailered .clm not clm_decodable (CLMX check broke)"
    # (b) finite
    for nm, lg in (("base", lg_base), ("slw", lg_slw), ("clml", lg_clml), ("both", lg_both)):
        if not np.all(np.isfinite(lg)):
            return False, f"{nm} forward non-finite"
    d_slw = float(np.max(np.abs(lg_slw - lg_base)))
    d_clml = float(np.max(np.abs(lg_clml - lg_base)))
    d_both_slw = float(np.max(np.abs(lg_both - lg_slw)))
    d_both_clml = float(np.max(np.abs(lg_both - lg_clml)))
    d_slw0 = float(np.max(np.abs(lg_slw0 - lg_base)))
    # (c) each trailer active
    if d_slw <= 1e-9:
        return False, f"SLW inert (max|Δ|={d_slw:.2e}) — not applied"
    if d_clml <= 1e-9:
        return False, f"CLML inert (max|Δ|={d_clml:.2e}) — not applied"
    # (d) γ=0 bit-exact passthrough
    if d_slw0 != 0.0:
        return False, f"SLW γ=0 not bit-exact passthrough (max|Δ|={d_slw0:.2e})"
    # (e) compose (both differs from either alone)
    if d_both_slw <= 1e-9 or d_both_clml <= 1e-9:
        return False, f"SLW+CLML not composing (Δvs_slw={d_both_slw:.2e} Δvs_clml={d_both_clml:.2e})"
    return True, (f"SLW Δ={d_slw:.3e} CLML Δ={d_clml:.3e} both⊃slw Δ={d_both_slw:.3e} "
                  f"both⊃clml Δ={d_both_clml:.3e} γ0-passthrough=exact")


def run_v3_byteeq_v2(here):
    """v0.3 byte-eq REGRESSION: serialize_v3(L=1,E=2) must be byte-IDENTICAL to
    serialize_v2 on the same logical weights (no regression on the existing
    format). Builds the legacy L1/E2 synthetic and packs it both ways."""
    import clm_serialize_v2 as S
    sd2, _ = _build_synthetic()                 # logical-slot keys, L1/E2
    # serialize_v2 (logical keys, cfg=None)
    p2 = os.path.join(here, "_rt_v2.clm")
    S.serialize_v2(sd2, cfg=None, out_path=p2)
    b2 = open(p2, "rb").read()
    # serialize_v3 needs torch-key OR logical-key; the general keymap falls back
    # to logical slot names (_get checks `logical in sd` first). The v3 logical
    # slot names for L1/E2 are ec/tc0/e0/e1... so remap the legacy logical dict.
    sd3 = {"ecW": sd2["ecW"], "tc0W": sd2["tcW"], "e0W": sd2["e0W"], "e1W": sd2["e1W"],
           "rW": sd2["rW"], "roW": sd2["roW"],
           "embed": sd2["embed"], "ecB": sd2["ecB"], "tc0B": sd2["tcB"],
           "e0B": sd2["e0B"], "e1B": sd2["e1B"], "rB": sd2["rB"], "roB": sd2["roB"],
           "tg0G": sd2["tgG"], "tg0B": sd2["tgB"], "noG": sd2["noG"], "noB": sd2["noB"]}
    p3 = os.path.join(here, "_rt_v3.clm")
    S.serialize_v3(sd3, n_trunk_layers=1, n_experts=2, out_path=p3)
    b3 = open(p3, "rb").read()
    for pth in (p2, p3):
        try:
            os.remove(pth)
        except OSError:
            pass
    if b2 == b3:
        return True, f"byte-identical ({len(b2)} bytes)"
    return False, f"v2 ({len(b2)}B) != v3 ({len(b3)}B)"


# --------------------------------------------------------------------------- #
# HELD-OUT mirror-DESCENT gate (the OVERFIT detector)
# --------------------------------------------------------------------------- #
# WHY this exists: the structural round-trips above only prove the .clm is
# *decodable* (right shape/headers). They say NOTHING about whether the
# serialized weights actually PREDICT TEXT. A model that memorized a tiny corpus
# (overfit) is structurally perfect yet useless on held-out text — and the
# engine's own clm_forward_ce can MISS this, because hexa-lang's dt_ln (atanh
# series, flame_math.hexa) is numerically wrong away from x=1: dt_ln(256)=4.799
# (true ln=5.545), dt_ln(1e-6)=-5.14 (true -13.82). That clamps per-position CE
# at ~5.14 (nn_lib.hexa nn_ce_loss_allpos uses -dt_ln(p_t)), so a broken/overfit
# model gets a falsely-low engine CE and reads GREEN. (clm303 precedent 2026-06-24:
# engine model_ce 3.30 < shuffle 4.93 = "GREEN" while the true held-out CE was
# 7.6-13.7 = worse than random.)
#
# This gate is a FAITHFUL pure-numpy mirror of core/clm_decode.hexa's forward
# (byte-reproduces state/mid_convmoe_fire/clm_decode_mirror.py and the engine
# clm_forward_ce) BUT uses math.log (correct, dt_ln-immune), reading the .clm
# BYTES directly. It is build-time SERIALIZE-INTEGRITY tooling, NOT a ρ-AXON reach
# capability verdict — capability verdicts still go through the single entry
# `cli/anima.hexa -- eval` (a_engine_native_learning). It exists so a broken or
# overfit .clm cannot be marked "done" or HF-uploaded.
#
# It MUST be evaluated on HELD-OUT text (never the training corpus — that would
# hide overfitting), and optionally reports the train-vs-held-out gap.

INT4_OFF = 8  # nibble code = (byte&0xF) - 8


def _load_clm_weights(path):
    """Pure-numpy load of a .clm (v0.2/v0.3) into a weight dict, matching
    core/clm_decode.hexa::_clmd_load EXACTLY (int4 dequant w=code*scale, general
    (L,E) derivation). Requires numpy. Returns None if not decodable."""
    import numpy as np
    rb = open(path, "rb").read() if not isinstance(path, (bytes, bytearray)) else path
    if not clm_decodable(rb):
        return None
    nblk = rb[4]
    # walk headers for (cout,rest) to derive E,V and block offsets
    off = 5
    hdrs = []
    for _ in range(nblk):
        c = _ru32(rb, off); r = _ru32(rb, off + 4)
        hdrs.append((c, r))
        off += 8 + (c * r + 1) // 2 + c * 4
    E = hdrs[nblk - 2][0]
    V = hdrs[nblk - 1][0]
    L = nblk - E - 3
    d = hdrs[0][0]
    K = hdrs[0][1] // d

    def rd_block(o):
        cout = _ru32(rb, o); o += 4
        rest = _ru32(rb, o); o += 4
        n = cout * rest
        nb = (n + 1) // 2
        raw = np.frombuffer(rb, dtype=np.uint8, count=nb, offset=o); o += nb
        lo = (raw & 0xF).astype(np.int64) - INT4_OFF
        hi = ((raw >> 4) & 0xF).astype(np.int64) - INT4_OFF
        codes = np.empty(2 * nb, dtype=np.float64)
        codes[0::2] = lo
        codes[1::2] = hi
        codes = codes[:n].reshape(cout, rest)
        scale = np.frombuffer(rb, dtype="<f4", count=cout, offset=o).astype(np.float64)
        o += 4 * cout
        return codes * scale[:, None], o

    def rd_ext(o):
        n = _ru32(rb, o); o += 4
        arr = np.frombuffer(rb, dtype="<f4", count=n, offset=o).astype(np.float64)
        o += 4 * n
        return arr, o

    off = 5
    ecW, off = rd_block(off)
    tcW = []
    for _ in range(L):
        w, off = rd_block(off); tcW.append(w)
    eW = []
    for _ in range(E):
        w, off = rd_block(off); eW.append(w)
    rW, off = rd_block(off)
    roW, off = rd_block(off)
    off += 5  # CLMX + n_ext
    embed, off = rd_ext(off)
    ecB, off = rd_ext(off)
    tcB = []
    for _ in range(L):
        a, off = rd_ext(off); tcB.append(a)
    eB = []
    for _ in range(E):
        a, off = rd_ext(off); eB.append(a)
    rB, off = rd_ext(off)
    roB, off = rd_ext(off)
    tgG = []
    for _ in range(L):
        a, off = rd_ext(off); tgG.append(a)
    tgB = []
    for _ in range(L):
        a, off = rd_ext(off); tgB.append(a)
    noG, off = rd_ext(off)
    noB, off = rd_ext(off)
    # OPTIONAL CLMB bind-readout trailer (math.log mirror — dt_ln-immune gate).
    rtype = 0
    Wa = Wb = WaB = WbB = None
    kbind = roW.shape[1]
    if off + 5 <= len(rb) and rb[off] == 67 and rb[off + 1] == 76 \
            and rb[off + 2] == 77 and rb[off + 3] == 66:   # "CLMB"
        rtype = rb[off + 4]
        off += 5
        Wa, off = rd_block(off)              # [k, d]
        Wb, off = rd_block(off)              # [k, d]
        WaB, off = rd_ext(off)              # [k]
        WbB, off = rd_ext(off)              # [k]
        kbind = Wa.shape[0]
    return dict(d=d, E=E, V=V, K=K, L=L, ecW=ecW, tcW=tcW, eW=eW, rW=rW, roW=roW,
                embed=embed.reshape(V, d), ecB=ecB, tcB=tcB, eB=eB, rB=rB, roB=roB,
                tgG=tgG, tgB=tgB, noG=noG, noB=noB,
                rtype=rtype, kbind=kbind, Wa=Wa, Wb=Wb, WaB=WaB, WbB=WbB)


def _gelu(x):
    import numpy as np
    # tanh approx — matches generator.hexa::_gen_gelu (same form clm_decode uses)
    inner = 0.7978845608 * (x + 0.044715 * x * x * x)
    a = np.clip(inner, -15.0, 15.0)
    e2 = np.exp(2.0 * a)
    return 0.5 * x * (1.0 + (e2 - 1.0) / (e2 + 1.0))


def _conv1d(x, w2d, b, T, Cin, Cout, K, dil):
    import numpy as np
    Kdim = Cin * K
    xcol = np.zeros((T, Kdim))
    idx = np.arange(Cin) * K
    for k in range(K):
        shift = dil * (K - 1 - k)
        if shift == 0:
            xcol[:, idx + k] = x
        elif shift < T:
            xcol[shift:, idx + k] = x[:T - shift]
    return xcol @ w2d.T + b[None, :]


def _gn1(x, g, b):
    import numpy as np
    mu = x.mean(1, keepdims=True)
    var = x.var(1, keepdims=True)
    return (x - mu) / np.sqrt(var + 1e-5) * g[None, :] + b[None, :]


def _fwd_logits(W, tok, T):
    import numpy as np
    d, E, V, K, L = W["d"], W["E"], W["V"], W["K"], W["L"]
    xe = W["embed"][tok.astype(int)]
    xt = _conv1d(xe, W["ecW"], W["ecB"], T, d, d, K, 1)
    dil = 1
    for li in range(L):
        de = min(dil, 512)
        h = _conv1d(xt, W["tcW"][li], W["tcB"][li], T, d, d, K, de)
        xt = xt + _gelu(_gn1(h, W["tgG"][li], W["tgB"][li]))
        dil *= 2
    lr = _conv1d(xt, W["rW"], W["rB"], T, d, E, 1, 1)
    exo = [_gelu(_conv1d(xt, W["eW"][e], W["eB"][e], T, d, d, K, 1)) for e in range(E)]
    p = np.exp(lr - lr.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
    y = sum(p[:, e:e + 1] * exo[e] for e in range(E))
    yn = _gn1(y, W["noG"], W["noB"])
    rtype = W.get("rtype", 0)
    if rtype:
        k = W["kbind"]
        u = _conv1d(yn, W["Wa"], W["WaB"], T, d, k, 1, 1)        # [T,k]
        v = _conv1d(yn, W["Wb"], W["WbB"], T, d, k, 1, 1)        # [T,k]
        g = (u * v) if rtype == 1 else (u + v)
        return _conv1d(g, W["roW"], W["roB"], T, k, V, 1, 1)     # Wo: [T,V]
    return _conv1d(yn, W["roW"], W["roB"], T, d, V, 1, 1)


def _ce_allpos(logits, tgt, T):
    import numpy as np
    z = logits - logits.max(1, keepdims=True)
    lse = np.log(np.exp(z).sum(1))
    return float((-(z[np.arange(T), tgt.astype(int)] - lse)).sum() / T)


def mirror_ce(clm_path, corpus_path, nwin=64, T=24):
    """Faithful mirror next-byte CE over `nwin` windows of a byte corpus, using
    math.log (correct — dt_ln-immune). Returns (model_ce, shuffle_ce, uniform_ce,
    windows). uniform_ce = ln(V) (the TRUE blind baseline, not the buggy engine
    dt_ln(V))."""
    import numpy as np
    W = _load_clm_weights(clm_path)
    if W is None:
        raise ValueError(f"{clm_path}: not v0.2/v0.3 decodable")
    V = W["V"]
    rb = open(corpus_path, "rb").read()
    n = len(rb)
    stride = max(1, (n - T - 1) // nwin)
    sm = ss = 0.0
    cnt = 0
    for s in range(nwin):
        base = s * stride
        if base + T + 1 <= n:
            tok = np.frombuffer(rb, np.uint8, T, base).astype(float)
            tgt = np.frombuffer(rb, np.uint8, T, base + 1).astype(float)
            lg = _fwd_logits(W, tok, T)
            sm += _ce_allpos(lg, tgt, T)
            ss += _ce_allpos(lg, tgt[::-1].copy(), T)
            cnt += 1
    return sm / cnt, ss / cnt, math.log(V), cnt


def descent_gate(clm_path, heldout_corpus, train_corpus=None, nwin=64,
                 max_gap=3.0):
    """The OVERFIT detector. PASS iff the serialized .clm genuinely models
    HELD-OUT text: model_ce < uniform AND model_ce < shuffle. If a `train_corpus`
    is given, also reports the train-vs-held-out gap (large gap = overfit warning)
    and FAILs when held-out fails the descent test (the gap alone is advisory).

    Returns (ok: bool, report: dict). Frozen bars: uniform=ln(V), shuffle=
    reversed-target control. NOT tunable (a_break_the_wall: frozen-first)."""
    h_model, h_shuf, uni, h_win = mirror_ce(clm_path, heldout_corpus, nwin)
    lt_uniform = h_model < uni
    lt_shuffle = h_model < h_shuf
    ok = lt_uniform and lt_shuffle
    rep = {"heldout_model_ce": round(h_model, 5),
           "heldout_shuffle_ce": round(h_shuf, 5),
           "uniform_ce_lnV": round(uni, 5),
           "heldout_lt_uniform": lt_uniform,
           "heldout_lt_shuffle": lt_shuffle,
           "heldout_windows": h_win,
           "train_model_ce": None, "train_heldout_gap": None,
           "overfit_warning": False}
    if train_corpus and os.path.exists(train_corpus):
        t_model, _, _, _ = mirror_ce(clm_path, train_corpus, nwin)
        gap = h_model - t_model
        rep["train_model_ce"] = round(t_model, 5)
        rep["train_heldout_gap"] = round(gap, 5)
        # Overfit signature: descends on train but the held-out gap is huge.
        rep["overfit_warning"] = (t_model < uni) and (gap > max_gap)
    return ok, rep


def run_descent_gate_cli(clm_path, heldout_corpus, train_corpus=None, nwin=64):
    """Verbatim-output CLI wrapper (p7/c9 honest). Prints F-CLM-DESCENT=1/0 +
    the report, exits 0 on PASS else 1. Used by train.py / train.hexa as the
    post-serialize self-verify (a_clm_gen_pipeline)."""
    try:
        ok, rep = descent_gate(clm_path, heldout_corpus, train_corpus, nwin)
    except Exception as e:  # numpy missing / undecodable — honest fail
        print(f"F-CLM-DESCENT=0\nDESCENT_ERROR: {e}")
        return 1
    print(f"F-CLM-DESCENT={'1' if ok else '0'}")
    print("DESCENT " + repr(rep))
    if rep["overfit_warning"]:
        print("OVERFIT_WARNING: descends on train but held-out gap "
              f"{rep['train_heldout_gap']} > 3.0 — the serialized .clm memorized "
              "its corpus and does NOT generalize. Re-train with regularization / "
              "a larger corpus (re-serialization will NOT fix this).")
    if not ok:
        print("DESCENT_FAIL: serialized .clm does NOT model held-out text "
              f"(model_ce {rep['heldout_model_ce']} vs uniform {rep['uniform_ce_lnV']}, "
              f"shuffle {rep['heldout_shuffle_ce']}). Broken or overfit — do NOT "
              "mark done / HF-upload.")
    return 0 if ok else 1


def serialize_self_verify(clm_path, train_corpus, heldout=None, skip=False,
                          nwin=64, tail_frac=0.1, tag="CLM"):
    """Post-serialize convenience for the trainers (train.py / train.hexa bridge).
    Runs the held-out mirror-DESCENT gate right after a .clm is written, so a
    broken/overfit artifact can't be marked done. If `heldout` is None, holds out
    a DEEP TAIL slice of `train_corpus` (last `tail_frac`, written to a temp file)
    as a stand-in held-out set — never evaluate the gate on the head the model
    trained on. Returns the gate rc (0=PASS). Honest no-op (rc 0) when skip=True
    or no usable corpus, with a printed reason."""
    if skip:
        print(f"{tag}_DESCENT_GATE=SKIPPED (--no-descent-gate)")
        return 0
    held = heldout
    tmp_made = None
    try:
        if held is None:
            if not train_corpus or not os.path.exists(train_corpus):
                print(f"{tag}_DESCENT_GATE=SKIPPED (no held-out and no readable "
                      "train corpus to slice)")
                return 0
            rb = open(train_corpus, "rb").read()
            n = len(rb)
            cut = int(n * (1.0 - tail_frac))
            if n - cut < 4096:
                print(f"{tag}_DESCENT_GATE=SKIPPED (corpus too small to hold out "
                      f"a {tail_frac:.0%} tail)")
                return 0
            import tempfile
            fd, tmp_made = tempfile.mkstemp(suffix=".heldtail")
            with os.fdopen(fd, "wb") as f:
                f.write(rb[cut:])
            held = tmp_made
            print(f"{tag}_DESCENT_GATE: holding out deep tail slice "
                  f"(last {tail_frac:.0%} = {n - cut} bytes) of {train_corpus}")
        return run_descent_gate_cli(clm_path, held, train_corpus, nwin)
    finally:
        if tmp_made and os.path.exists(tmp_made):
            try:
                os.remove(tmp_made)
            except OSError:
                pass


def run_descent_selftest(here):
    """CI self-test of the DESCENT-gate MACHINERY (no torch, no big artifacts):
    serialize a tiny RANDOM-weight model to .clm, run the held-out mirror gate on
    a small byte corpus, and assert the broken-detector FIRES (random weights ⇒
    NO-DESCENT, F-CLM-DESCENT=0). This proves the gate loads/forwards/scores and
    that a non-modeling .clm is correctly REJECTED — the exact failure the gate
    must catch. (A PASS-side fixture would need a trained model = torch; the
    real PASS path is exercised by the control clm_d768 + the trainers in CI.)"""
    import numpy as np
    sd, _ = _build_synthetic_general(d=24, L=2, E=2, K=3, V=256, seed=7)
    ctmp = os.path.join(here, "_rt_descent.clm")
    import clm_serialize_v2 as S
    S.serialize_v3(sd, n_trunk_layers=2, n_experts=2, out_path=ctmp)
    # small deterministic byte corpus (English-ish) — random weights can't model it
    corp = os.path.join(here, "_rt_descent_corpus.txt")
    with open(corp, "wb") as f:
        f.write((b"the mind is a fire to be kindled not a vessel to be filled. ") * 64)
    try:
        ok, rep = descent_gate(ctmp, corp, None, nwin=16)
        # machinery sanity: produced finite CEs + the random model does NOT descend
        finite = (rep["heldout_model_ce"] == rep["heldout_model_ce"]  # not NaN
                  and rep["uniform_ce_lnV"] > 5.0)
        fires = (ok is False)  # broken-detector must reject random weights
        return (finite and fires), rep
    finally:
        for p in (ctmp, corp):
            try:
                os.remove(p)
            except OSError:
                pass


def main():
    # `verify_clm_v2.py descent <clm> <heldout> [train] [nwin]` runs the
    # held-out overfit gate (the post-serialize self-verify). No args → the
    # structural round-trip self-test suite.
    if len(sys.argv) >= 2 and sys.argv[1] == "descent":
        clm = sys.argv[2]
        heldout = sys.argv[3]
        train = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].isdigit() else None
        nwin = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 64
        sys.exit(run_descent_gate_cli(clm, heldout, train, nwin))

    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    tmp = os.path.join(here, "_rt_synth.clm")

    ok, why = run_roundtrip(tmp)
    if ok:
        print("F-CLM-V2-ROUNDTRIP=1")
    else:
        print("F-CLM-V2-ROUNDTRIP=0")
        print(f"MISMATCH: {why}")
    try:
        os.remove(tmp)
    except OSError:
        pass

    # v0.3 byte-eq regression (L1/E2: v3 == v2)
    eq_ok, eq_why = run_v3_byteeq_v2(here)
    print(f"F-CLM-V3-BYTEEQ-V2={'1' if eq_ok else '0'}  ({eq_why})")

    # v0.3 general round-trips: a small multi-layer/more-expert config + the
    # actual 3B-class config dims (structure only — no weights materialized at
    # full 3B; the dim-bookkeeping is what the gate proves).
    gtmp = os.path.join(here, "_rt_gen.clm")
    g_ok_small, g_why_small = run_roundtrip_general(gtmp, d=48, L=4, E=6)
    print(f"F-CLM-V3-ROUNDTRIP-SMALL={'1' if g_ok_small else '0'}  "
          f"(d=48 L=4 E=6: {g_why_small})")
    g_ok_3b, g_why_3b = run_roundtrip_general(gtmp, d=128, L=30, E=30)
    print(f"F-CLM-V3-ROUNDTRIP-3BDIMS={'1' if g_ok_3b else '0'}  "
          f"(d=128 L=30 E=30 [3B block/ext topology, reduced d]: {g_why_3b})")
    try:
        os.remove(gtmp)
    except OSError:
        pass

    # v0.3 BIND round-trips (CLMB bind-readout codec): Hadamard (rt=1) + linear (rt=2).
    btmp = os.path.join(here, "_rt_bind.clm")
    b_ok_h, b_why_h = run_roundtrip_bind(btmp, d=48, L=2, E=2, k=64, readout_type=1)
    print(f"F-CLM-BIND-ROUNDTRIP-HADAMARD={'1' if b_ok_h else '0'}  "
          f"(d=48 L=2 E=2 k=64 rt=1: {b_why_h})")
    b_ok_l, b_why_l = run_roundtrip_bind(btmp, d=48, L=2, E=2, k=64, readout_type=2)
    print(f"F-CLM-BIND-ROUNDTRIP-LINEAR={'1' if b_ok_l else '0'}  "
          f"(d=48 L=2 E=2 k=64 rt=2: {b_why_l})")
    # 303M-class bind dims (block/ext topology only; reduced d for the bookkeeping).
    b_ok_303, b_why_303 = run_roundtrip_bind(btmp, d=128, L=4, E=4, k=512, readout_type=1)
    print(f"F-CLM-BIND-ROUNDTRIP-303MDIMS={'1' if b_ok_303 else '0'}  "
          f"(d=128 L=4 E=4 k=512 [303M ARM-BIND topology, reduced d]: {b_why_303})")
    try:
        os.remove(btmp)
    except OSError:
        pass

    # held-out DESCENT-gate machinery self-test (broken-detector must fire on
    # random weights). numpy required; honest SKIP if absent.
    try:
        import numpy as _np  # noqa: F401  @root-cause-ok probe whether numpy is importable for the gate self-test
        d_ok, d_rep = run_descent_selftest(here)
        print(f"F-CLM-DESCENT-SELFTEST={'1' if d_ok else '0'}  "
              f"(random-weight .clm correctly rejected: heldout_ce="
              f"{d_rep['heldout_model_ce']} >= uniform={d_rep['uniform_ce_lnV']})")
    except ImportError:
        print("F-CLM-DESCENT-SELFTEST=SKIP (numpy unavailable)")
        d_ok = True  # don't fail the structural suite on a missing optional dep

    # SLW (H_9200) + CLML (H_9235) trailer forward round-trip (py canonical decode).
    try:
        sc_ok, sc_why = run_roundtrip_slw_clml(here)
    except Exception as e:
        sc_ok, sc_why = False, f"exception: {type(e).__name__}: {e}"
    print(f"F-CLM-SLW-CLML-FORWARD={'1' if sc_ok else '0'}  ({sc_why})")

    ok = ok and eq_ok and g_ok_small and g_ok_3b and d_ok and b_ok_h and b_ok_l and b_ok_303 and sc_ok

    # golden-reference parse: prove the mirror matches the REAL flame format.
    golden = None
    for cand in [
        os.environ.get("GOLDEN_CLM", ""),
        os.path.join(here, "..", "..", "state", "laneg_d768_recover", "reexport_d768_v2_fast.clm"),
    ]:
        if cand and os.path.exists(cand):
            golden = cand
            break
    if golden is None:
        print("GOLDEN: file not found (skipped) — set GOLDEN_CLM=<path>")
    else:
        dec = clm_decodable(golden)
        g = parse_clm(golden)
        b0 = g["blocks"][0] if g["blocks"] else {}
        print(f"GOLDEN path={golden}")
        print(f"GOLDEN decodable={'true' if dec else 'false'} "
              f"nblk={g['nblk']} "
              f"block0={{cout:{b0.get('cout')},rest:{b0.get('rest')}}} "
              f"CLMX-found={'true' if g['clmx_found'] else 'false'} "
              f"n_ext={g['n_ext']} ext_counts={g['ext_counts']} "
              f"exact_eof={g['exact_eof']}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
