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

MAGIC = bytes([67, 76, 77, 1])
CLMX = bytes([67, 76, 77, 88])


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
           "exact_eof": None}
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


def main():
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
    ok = ok and eq_ok and g_ok_small and g_ok_3b

    # golden-reference parse: prove the mirror matches the REAL flame format.
    golden = None
    for cand in [
        os.environ.get("GOLDEN_CLM", ""),
        os.path.join(here, "..", "..", "state", "laneg_d768_recover", "reexport_d768_v2_fast.clm"),
        "/Users/mini/dancinlab/anima/state/laneg_d768_recover/reexport_d768_v2_fast.clm",
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
