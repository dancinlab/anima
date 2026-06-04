#!/usr/bin/env python3
"""v0.2-CLMX .clm serializer — torch CLMConvMoE state_dict -> ENGINE-loadable .clm.

WHY (the Lane P serializer-gap):
  v0.1 (clm_serialize.py) writes  [MAGIC CLM\x01][u32 hdr_len][JSON header][body][JSON manifest].
  The ENGINE decoder (CORE/clm_decode.hexa) CANNOT read that — clm_decodable() returns
  false because there is no CLMX trailer (embed/GN/bias the forward needs are absent).

  This writer produces the v0.2-CLMX layout the decoder DOES read, byte-compatible
  with the canonical host-side reexport (state/laneg_d768_recover/reexport_d8_v2.clm),
  so a torch-trained model becomes ENGINE-loadable.

HONEST SCOPE (a_train_flame_forge):
  This is the **Lane G-ref (torch-trained)** path. The emitted .clm BINARY contains
  NO torch / ATen / Python — it is a pure int4+fp32 byte stream the .hexa ENGINE decodes.
  But the TRAINER is torch, so this is NOT the forge production ENGINE (which stays
  util-blocked pending hexa-lang). The win: a torch+CUDA-trained model can now be
  ENGINE-loaded, unblocking a working 3B/7B ENGINE .clm NOW.

DECODER ARCH CONSTRAINT (CORE/clm_decode.hexa: `let E=2; let V=256`, 1-trunk walk):
  The decoder hardcodes E=2, V=256, and a SINGLE trunk layer (one tcW block). So the
  torch model MUST be built with n_experts=2, n_trunk_layers=1, vocab_size=256.
  This writer asserts that shape and refuses otherwise (no silent wrong-arch .clm).

BYTE CONTRACT (matched to clm_decode.hexa reader + reexport_d8_v2.clm, both verified):
  [MAGIC "CLM\x01"] [u8 nblk=6]
  6 conv blocks, each:
     [u32 cout] [u32 rest]                 rest = Cin*K
     [int4 nibbles, 2/byte, (cout*rest+1)//2 bytes]   code = (nibble & 0xF) - 8  (lo then hi)
     [fp32 scale[cout], little-endian]     w = code * scale[output_channel]
     block order: ecW, tcW, e0W, e1W, rW(K=1), roW(K=1)
  [CLMX trailer]
     ["CLMX"] [u8 n_ext=11]
     11 ext tensors, each: [u32 n] [fp32[n] little-endian]
     order: embed(V*d), ecB(d), tcB(d), e0B(d), e1B(d), rB(E), roB(V),
            tgG(d), tgB(d), noG(d), noB(d)

torch state_dict keys (CLM/model/model.py, n_trunk_layers=1):
  embed.weight (V,d)            -> embed (already (V,d) row-major)
  embed_conv.conv.weight (d,d,K)-> ecW   ; embed_conv.conv.bias (d)   -> ecB
  trunk.0.conv.conv.weight      -> tcW   ; trunk.0.conv.conv.bias     -> tcB
  trunk.0.norm.weight/bias (d)  -> tgG/tgB
  moe.experts.0.conv.conv.weight-> e0W   ; .bias -> e0B
  moe.experts.1.conv.conv.weight-> e1W   ; .bias -> e1B
  moe.router.weight (E,d,1)     -> rW    ; moe.router.bias (E) -> rB
  norm_out.weight/bias (d)      -> noG/noB
  readout.weight (V,d,1)        -> roW   ; readout.bias (V) -> roB

The conv-weight flatten matches the decoder im2col exactly: torch Conv1d weight is
(Cout, Cin, K) which flattens row-major to w[co*Cin*K + ci*K + k]; the decoder reads
w[co*rest + j] with rest=Cin*K and j=ci*K+k -> identical index. No permute needed.

Deterministic: int4-sym via torch.round, per-output-channel scale.
"""
from __future__ import annotations
import argparse, os, struct, sys
import torch

INT4_SYM_MAX = 7   # symmetric [-7,+7] (chip rejects -8); matches clm_serialize.py v0.1

MAGIC = b"CLM\x01"
CLMX = b"CLMX"


# --------------------------------------------------------------------------- #
# int4-sym quant (identical scheme to v0.1 clm_serialize.py)
# --------------------------------------------------------------------------- #
def sym_int4_scale(w: torch.Tensor) -> torch.Tensor:
    """Per-output-channel symmetric int4 scale: amax / 7, clamped away from 0."""
    out_c = w.shape[0]
    flat = w.detach().reshape(out_c, -1)
    amax = flat.abs().amax(dim=1).clamp_min(1e-8)
    return amax / INT4_SYM_MAX   # (out_c,)


def quant_block(w: torch.Tensor):
    """w: (Cout, Cin, K) or (Cout, Cin) conv weight.
    Returns (cout, rest, nibble_bytes, scale_fp32_bytes) per the decoder block contract.
    """
    cout = w.shape[0]
    flat = w.detach().reshape(cout, -1).to(torch.float32)
    rest = flat.shape[1]
    scale = sym_int4_scale(w)                       # (cout,)
    # code = round(w / scale_per_channel), clamped to [-7,7]
    q = torch.clamp(torch.round(flat / scale.reshape(cout, 1)),
                    -INT4_SYM_MAX, INT4_SYM_MAX).to(torch.int64)
    # pack 2 codes/byte, offset +8 -> nibble in [1..15]; element i even -> low nibble,
    # i odd -> high nibble (decoder: byte&0xF = codes[i], (byte/16)&0xF = codes[i+1]).
    codes = (q.reshape(-1) + 8).clamp(0, 15).to(torch.int64)
    n = codes.numel()
    if n % 2:
        codes = torch.cat([codes, torch.zeros(1, dtype=torch.int64)])
    lo = codes[0::2]                                 # even index -> low nibble
    hi = codes[1::2]                                 # odd index  -> high nibble
    packed = ((hi << 4) | lo).to(torch.uint8)
    nibble_bytes = bytes(packed.tolist())
    scale_bytes = scale.to(torch.float32).contiguous().numpy().tobytes()
    return cout, rest, nibble_bytes, scale_bytes


def write_block(buf: bytearray, w: torch.Tensor):
    cout, rest, nibbles, scale_b = quant_block(w)
    buf += struct.pack("<I", cout)
    buf += struct.pack("<I", rest)
    buf += nibbles
    buf += scale_b


def write_ext(buf: bytearray, t: torch.Tensor):
    flat = t.detach().reshape(-1).to(torch.float32).contiguous()
    buf += struct.pack("<I", flat.numel())
    buf += flat.numpy().tobytes()


# --------------------------------------------------------------------------- #
# serialize a CLMConvMoE state_dict -> v0.2-CLMX .clm
# --------------------------------------------------------------------------- #
def serialize_v2(sd: dict, out_path: str) -> dict:
    """sd: torch state_dict of a CLMConvMoE built with n_experts=2,
    n_trunk_layers=1, vocab_size=256. Writes the v0.2-CLMX .clm at out_path.
    """
    # ---- arch assertions (decoder hardcodes E=2, V=256, 1-trunk) ----------- #
    embed = sd["embed.weight"]                       # (V, d)
    V, d = embed.shape
    assert V == 256, f"decoder hardcodes V=256, got V={V}"
    rW = sd["moe.router.weight"]                     # (E, d, 1)
    E = rW.shape[0]
    assert E == 2, f"decoder hardcodes E=2, got E={E}"
    assert "trunk.0.conv.conv.weight" in sd, "missing trunk.0 (need 1-trunk)"
    assert "trunk.1.conv.conv.weight" not in sd, \
        "decoder walks a SINGLE trunk block; n_trunk_layers must be 1"
    assert "moe.experts.0.conv.conv.weight" in sd and \
           "moe.experts.1.conv.conv.weight" in sd, "need exactly experts 0,1"
    assert "moe.experts.2.conv.conv.weight" not in sd, "decoder is E=2; expert>1 present"

    ecW = sd["embed_conv.conv.weight"]               # (d,d,K)
    K = ecW.shape[2]

    buf = bytearray()
    buf += MAGIC
    buf += bytes([6])                                # nblk = 6

    # ---- 6 conv blocks (order matches _clmd_load_block call sequence) ------ #
    write_block(buf, sd["embed_conv.conv.weight"])           # ecW
    write_block(buf, sd["trunk.0.conv.conv.weight"])         # tcW
    write_block(buf, sd["moe.experts.0.conv.conv.weight"])   # e0W
    write_block(buf, sd["moe.experts.1.conv.conv.weight"])   # e1W
    write_block(buf, sd["moe.router.weight"])                # rW   (K=1)
    write_block(buf, sd["readout.weight"])                   # roW  (K=1)

    # ---- CLMX trailer ------------------------------------------------------ #
    buf += CLMX
    buf += bytes([11])                               # n_ext = 11
    write_ext(buf, sd["embed.weight"])               # embed  (V*d)
    write_ext(buf, sd["embed_conv.conv.bias"])       # ecB    (d)
    write_ext(buf, sd["trunk.0.conv.conv.bias"])     # tcB    (d)
    write_ext(buf, sd["moe.experts.0.conv.conv.bias"])  # e0B (d)
    write_ext(buf, sd["moe.experts.1.conv.conv.bias"])  # e1B (d)
    write_ext(buf, sd["moe.router.bias"])            # rB     (E)
    write_ext(buf, sd["readout.bias"])               # roB    (V)
    write_ext(buf, sd["trunk.0.norm.weight"])        # tgG    (d)
    write_ext(buf, sd["trunk.0.norm.bias"])          # tgB    (d)
    write_ext(buf, sd["norm_out.weight"])            # noG    (d)
    write_ext(buf, sd["norm_out.bias"])              # noB    (d)

    with open(out_path, "wb") as f:
        f.write(buf)

    return {"out": out_path, "bytes": len(buf), "d": d, "K": K,
            "E": E, "V": V, "n_blocks": 6}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _load_state_dict(ckpt_path: str) -> dict:
    obj = torch.load(ckpt_path, map_location="cpu")
    if isinstance(obj, dict) and "state_dict" in obj and "embed.weight" not in obj:
        obj = obj["state_dict"]
    return obj


def main():
    ap = argparse.ArgumentParser(description="v0.2-CLMX torch .clm serializer")
    ap.add_argument("--ckpt", required=True, help="torch CLMConvMoE state_dict (.pt)")
    ap.add_argument("--out", required=True, help="output .clm path")
    a = ap.parse_args()
    sd = _load_state_dict(a.ckpt)
    summary = serialize_v2(sd, a.out)
    import json
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
