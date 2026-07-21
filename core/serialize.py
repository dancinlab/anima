# ==========================================================================
# ⛔ ENGINE-INTERNAL — DO NOT RUN DIRECTLY. 학습/직렬화는 cli/ 단일진입만:
#   anima train | anima serialize  (canonical=hexa cli/{train,serialize}.hexa).
# `python3 core/serialize.py` 직접 실행 = 단일진입 우회(#2603) + DIRECTIONAL. cli/ import만 허용.
# ==========================================================================
"""core/serialize.py — UNIFIED PY SERIALIZE ENGINE: byte-faithful 1:1 merge of the
two per-mouth serializer backends into ONE module (parallel to core/decode.py, the
unified CONV+BYTE decoder).

  * CONV (CLM ConvMoE) mouth  = the verbatim body of archive/train/clm/model/
                                clm_serialize_v2.py — torch/numpy state_dict → .clm
                                v0.2/v0.3 (`serialize_v3` = the byte-grammar SSOT
                                that core/decode.hexa's CONV mouth parses).
  * BYTE (ByteGPT transformer) = the verbatim body of tool/bytegpt_serialize.py —
                                torch .pt → engine .bin (5×u32 header) BRIDGE.

Per CLAUDE.md a_clm_gen_pipeline + a_engine_native_learning: serialize is the
LEARNING-side bridge (it must UNPICKLE a torch .pt = irreducibly Python — train/
serialize MAY use torch; this is NOT the verdict scorer). This module is the numpy/
struct bridge for BOTH mouth artifacts; it exposes the UNION of both backends'
public names so a caller can do `import serialize as S` (→ CLM `serialize_v3`) OR
`import serialize as BGS` (→ ByteGPT `serialize`) with ZERO call-site churn (a pure
drop-in for clm_serialize_v2.py + bytegpt_serialize.py — mirrors how core/decode.py
unioned clm_decode + bytegpt_decode).

Organization:
  (a) SHARED — struct/numpy imports + the CLM magic byte constants.
  (b) CONV (CLM) — the full clm_serialize_v2.py public API, VERBATIM (serialize_v2,
      serialize_v3, serialize_v3_bind, and every helper). serialize_v3 is the byte
      SSOT (byte-identical to the golden reexport_d768_v2_fast.clm) — copied
      verbatim, NOT "improved".
  (c) BYTE (ByteGPT) — the full bytegpt_serialize.py public API. Its top-level
      `serialize(pt, bin)` is the .pt → .bin bridge; the ByteGPT-only helper _f32le.
  (d) NAME-DISPATCH — the two backends each defined a top-level `serialize` with a
      DIFFERENT signature (CLM `serialize(sd,L,E,out)` vs ByteGPT `serialize(pt,bin)`).
      They cannot both bind the bare name. The LIVE importer contract (grep-verified)
      is: cli/serialize.py + cli/train.py call `S.serialize_v3` (never bare CLM
      `serialize`), and cli/train.py calls `BGS.serialize` (the ByteGPT bridge). So:
        * top-level `serialize`     = ByteGPT `serialize(pt, bin)`  (satisfies BGS.serialize)
        * `serialize_clm(sd,L,E,out)` = the CLM unified entry (was clm's bare `serialize`;
                                        preserved under a distinct name, no live caller)
      Both keep serialize_v2/serialize_v3/serialize_v3_bind (CLM) unchanged.
  (e) `serialize_auto(...)` — a small target-extension dispatcher (.bin → ByteGPT,
      else → CLM serialize_v3), convenience only; the existing entry points are
      UNRENAMED.
"""
from __future__ import annotations

# ⛔ ENGINE-INTERNAL — DO NOT RUN DIRECTLY (단일진입 우회 #2603). cli/ import만 허용.
# 가드는 `from __future__` 뒤에 둔다 — 앞에 두면 SyntaxError(from __future__ must be at top).
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ core/serialize.py 직접 실행 금지 — cli/ 단일진입(anima train/serialize, canonical=hexa) 경유. #2603")

import struct
from typing import Dict, Any

try:
    import numpy as np
except Exception:  # pragma: no cover - numpy is effectively always present
    np = None


# ════════════════════════════════════════════════════════════════════════
# (a) SHARED — CLM magic byte constants (used by the CONV serializer).
# ════════════════════════════════════════════════════════════════════════
MAGIC = bytes([67, 76, 77, 1])      # "CLM\x01"
CLMX = bytes([67, 76, 77, 88])      # "CLMX"
CLMB = bytes([67, 76, 77, 66])      # "CLMB" — bind-readout (Hadamard) extension
INT4_SYM_MAX = 7

# Every appended-trailer magic, in chain order CLMB→SLW→CLML→CLMS→MBND→IFAN→TFLD. A lane-carrying
# model is "a normal .clm + trailer chain", so the main-blob parity gate (clm_roundtrip_is_identity)
# has to know which trailing bytes are a legitimate lane and which are corruption. Keep in lockstep
# with the append_*_trailer functions below and their <lane>_MAGIC constants in core/<lane>.py.
_TRAILER_MAGICS = (
    CLMB,                            # "CLMB" — bind-readout (Hadamard)
    bytes([83, 76, 87, 1]),          # "SLW\x01" — gated-write forward slots (core/slw.py)
    bytes([67, 76, 77, 76]),         # "CLML"   — core/clml.py
    bytes([67, 76, 77, 83]),         # "CLMS"   — store-bridge lane (core/clms.py)
    bytes([77, 66, 78, 68]),         # "MBND"   — mouth binder (core/mbnd.py)
    bytes([73, 70, 65, 78]),         # "IFAN"   — core/ifan.py
    bytes([84, 70, 76, 68]),         # "TFLD"   — tension field (core/tension_field.py)
)


# ════════════════════════════════════════════════════════════════════════
# H_9200 E1 — "SLW\x01" gated-write forward-slot trailer (CORE-owned codec in
# core/slw.py). Appended at the END of the trailer chain (after CLMX ext / CLMB),
# so an SLW model = a normal additive .clm + this trailer. Absent => byte-identical
# to today's additive .clm (the loaders passthrough on a short/absent read).
# ════════════════════════════════════════════════════════════════════════
def append_slw_trailer(out_path: str, slw_module) -> int:
    """Append the SLW trailer to an already-written .clm (after serialize_v3). Reads
    the trained torch SLWModule, packs it via core/slw.pack_slw, and appends the
    bytes. Returns the number of trailer bytes written. No-op path: callers only
    invoke this when model.slw is not None, so the additive .clm stays untouched."""
    from slw import slw_weights_from_torch, pack_slw   # core/slw.py (same core/ dir)
    trailer = pack_slw(slw_weights_from_torch(slw_module))
    with open(out_path, "ab") as f:
        f.write(trailer)
    return len(trailer)


# ════════════════════════════════════════════════════════════════════════
# fork-A "CLML" read-side context-pooling lane trailer (CORE-owned codec in
# core/clml.py). Appended at the END of the trailer chain (after CLMX / CLMB /
# SLW), so a lane model = a normal .clm + this trailer. Absent => byte-identical
# (loaders passthrough on short/absent read). Trains a frozen-trunk lane (H_9235).
# ════════════════════════════════════════════════════════════════════════
def append_clml_trailer(out_path: str, clml) -> int:
    """Append the CLML lane trailer to an already-written .clm. `clml` = a trained torch
    CLMLModule OR a ready numpy weight dict (W1,b1,W2,w_g,b_g,r,tau). Returns bytes written.
    Callers only invoke this when the model actually has a fork-A lane."""
    from clml import pack_clml, clml_weights_from_torch   # core/clml.py (same core/ dir)
    w = clml if isinstance(clml, dict) else clml_weights_from_torch(clml)
    trailer = pack_clml(w)
    with open(out_path, "ab") as f:
        f.write(trailer)
    return len(trailer)


# ════════════════════════════════════════════════════════════════════════
# H_9423 "CLMS" store-bridge lane trailer (CORE-owned codec in core/clms.py).
# Appended at the END of the trailer chain (after CLMX / CLMB / SLW / CLML), so a
# store-bridge model = a normal .clm + this trailer. MUST be appended after CLML to
# keep the chain order CLMB→SLW→CLML→CLMS. Absent => byte-identical (loaders
# passthrough on short/absent read). The co-trained store-lookup bridge (H_9423).
# ════════════════════════════════════════════════════════════════════════
def append_clms_trailer(out_path: str, clms) -> int:
    """Append the CLMS store-bridge lane trailer to an already-written .clm. `clms` = a trained torch
    CLMSModule OR a ready numpy weight dict (key_emb,W_q,val,W_h,b_h,W_out,lam,n_slot,d_k,d_s,r,key_seed).
    Returns bytes written. Callers only invoke this when the model actually has a store-bridge lane, and
    ONLY after append_clml_trailer (if any) so the chain end stays CLMS."""
    from clms import pack_clms, clms_weights_from_torch   # core/clms.py (same core/ dir)
    w = clms if isinstance(clms, dict) else clms_weights_from_torch(clms)
    trailer = pack_clms(w)
    with open(out_path, "ab") as f:
        f.write(trailer)
    return len(trailer)


# ════════════════════════════════════════════════════════════════════════
# H_9698 "MBND" mouth-binder lane trailer (CORE-owned codec in core/mbnd.py).
# Appended AFTER CLMS so the chain end is CLMB→SLW→CLML→CLMS→MBND, matching the
# read order in core/decode.py. Absent => byte-identical (read_mbnd passthroughs
# on a short/absent read, leaving the offset untouched).
# ════════════════════════════════════════════════════════════════════════
def append_mbnd_trailer(out_path: str, mb) -> int:
    """Append the MBND mouth-binder trailer to an already-written .clm. `mb` = a trained torch
    MouthBinder OR a ready numpy weight dict (Q,K,V,U,b_pos,W_o,lam,rank,d,linear). Returns bytes
    written. Call ONLY after append_clms_trailer (if any) so the chain end stays MBND."""
    from mbnd import pack_mbnd, mbnd_weights_from_torch   # core/mbnd.py (same core/ dir)
    w = mb if isinstance(mb, dict) else mbnd_weights_from_torch(mb)
    trailer = pack_mbnd(w)
    with open(out_path, "ab") as f:
        f.write(trailer)
    return len(trailer)


# ════════════════════════════════════════════════════════════════════════
# H_9803 "IFAN" branch-latent ideation-fan trailer (CORE-owned codec in core/ifan.py).
# Appended AFTER MBND so the chain end is CLMB→SLW→CLML→CLMS→MBND→IFAN, matching the
# read order in core/decode.py. Absent => byte-identical (read_ifan passthroughs on a
# short/absent/mismatched read, leaving the offset untouched).
# ════════════════════════════════════════════════════════════════════════
def append_ifan_trailer(out_path: str, fan) -> int:
    """Append the IFAN branch-latent trailer to an already-written .clm. `fan` = a trained torch
    BranchLatentFan OR a ready numpy weight dict (K,rank,d,V,route_L,W_in,W_h,W_out,lam). Returns
    bytes written. Call ONLY after append_mbnd_trailer (if any) so the chain end stays IFAN."""
    from ifan import pack_ifan, ifan_weights_from_torch    # core/ifan.py (same core/ dir)
    w = fan if isinstance(fan, dict) else ifan_weights_from_torch(fan)
    trailer = pack_ifan(w)
    with open(out_path, "ab") as f:
        f.write(trailer)
    return len(trailer)


def append_tfld_trailer(out_path: str, lane) -> int:
    """Append the H_9805 TFLD write-side tension-field trailer to an already-written .clm. `lane` =
    a trained torch TensionFieldLane OR a ready numpy weight dict (n_bucket,rank,d,arm_code,phi,
    W_up,lam). Returns bytes written. Call LAST (after append_ifan_trailer, if any) so the chain
    end stays TFLD."""
    from tension_field import pack_tfld, tfld_weights_from_torch   # core/tension_field.py
    w = lane if isinstance(lane, dict) else tfld_weights_from_torch(lane)
    trailer = pack_tfld(w)
    with open(out_path, "ab") as f:
        f.write(trailer)
    return len(trailer)


# readout-type flag (CLMB byte[4]). 0 = additive Conv1d(d->V) (default, NO CLMB
# section); 1 = bind/Hadamard  g=u*v ; 2 = bind_linear (param-matched add) g=u+v.
RO_ADDITIVE = 0
RO_BIND_HADAMARD = 1
RO_BIND_LINEAR = 2


# ════════════════════════════════════════════════════════════════════════
# (b) CONV (CLM) — verbatim port of clm_serialize_v2.py. serialize_v3 is the
#     .clm byte-grammar SSOT core/decode.hexa's CONV mouth parses (golden
#     reexport_d768_v2_fast.clm). DO NOT alter the byte layout.
# ════════════════════════════════════════════════════════════════════════

# state_dict key names of a CLMConvMoE configured E=2 / n_trunk_layers=1.
# (CLM/model/model.py: embed, embed_conv, trunk[0], moe.router, moe.experts[0/1],
#  norm_out, readout). The decoder block order is ecW,tcW,e0W,e1W,rW,roW.
_KEYMAP = {
    "ecW": "embed_conv.conv.weight",
    "tcW": "trunk.0.conv.conv.weight",
    "e0W": "moe.experts.0.conv.conv.weight",
    "e1W": "moe.experts.1.conv.conv.weight",
    "rW":  "moe.router.weight",
    "roW": "readout.weight",
    # ext (CLMX) sources
    "embed": "embed.weight",
    "ecB": "embed_conv.conv.bias",
    "tcB": "trunk.0.conv.conv.bias",
    "e0B": "moe.experts.0.conv.conv.bias",
    "e1B": "moe.experts.1.conv.conv.bias",
    "rB":  "moe.router.bias",
    "roB": "readout.bias",
    "tgG": "trunk.0.norm.weight",
    "tgB": "trunk.0.norm.bias",
    "noG": "norm_out.weight",
    "noB": "norm_out.bias",
}

_BLOCK_ORDER = ["ecW", "tcW", "e0W", "e1W", "rW", "roW"]
_EXT_ORDER = ["embed", "ecB", "tcB", "e0B", "e1B", "rB", "roB",
              "tgG", "tgB", "noG", "noB"]


# --------------------------------------------------------------------------- #
# v0.3 — GENERAL (n_trunk_layers L, n_experts E) block/ext ordering.
#
# The CLM\x01 format is ALREADY self-describing: nblk (byte[4]) + each block's
# (cout,rest) + n_ext + each ext count fully determine the layout. v0.2 only
# *hardcoded* the block-role assignment (L=1,E=2). v0.3 generalizes that
# assignment WITHOUT changing the byte grammar, so it is byte-exact backward
# compatible — a v0.3 file with L=1,E=2 is byte-identical to a v0.2 file.
#
# General block order   (nblk = L + E + 3):
#   ecW · tcW_0..tcW_{L-1} · e0W..e{E-1}W · rW(cout=E) · roW(cout=V)
# General ext order      (n_ext = 2L + E + 6):
#   embed · ecB · tcB_0..tcB_{L-1} · e0B..e{E-1}B · rB · roB ·
#   tgG_0..tgG_{L-1} · tgB_0..tgB_{L-1} · noG · noB
#
# At L=1,E=2 this reduces EXACTLY to _BLOCK_ORDER / _EXT_ORDER above (the trunk
# bias tcB_0, then expert biases e0B,e1B, then rB,roB, then trunk GN tgG_0,tgB_0,
# then noG,noB) — byte-identical to v0.2.
#
# (L,E) recovery at decode time: E = cout of block[nblk-2] (router), V = cout of
# block[nblk-1] (readout), L = nblk - E - 3.  No new bytes, no magic bump.
# --------------------------------------------------------------------------- #

# torch state_dict key templates for the general CLMConvMoE (model.py).
#   embed.weight · embed_conv.conv.{weight,bias}
#   trunk.{i}.conv.conv.{weight,bias} · trunk.{i}.norm.{weight,bias}
#   moe.experts.{j}.conv.conv.{weight,bias} · moe.router.{weight,bias}
#   norm_out.{weight,bias} · readout.{weight,bias}
def _general_block_keymap(L: int, E: int):
    """logical slot -> torch key, for the L*E general block order."""
    km = {"ecW": "embed_conv.conv.weight"}
    for i in range(L):
        km[f"tc{i}W"] = f"trunk.{i}.conv.conv.weight"
    for j in range(E):
        km[f"e{j}W"] = f"moe.experts.{j}.conv.conv.weight"
    km["rW"] = "moe.router.weight"
    km["roW"] = "readout.weight"
    return km


def _general_ext_keymap(L: int, E: int):
    km = {"embed": "embed.weight", "ecB": "embed_conv.conv.bias"}
    for i in range(L):
        km[f"tc{i}B"] = f"trunk.{i}.conv.conv.bias"
    for j in range(E):
        km[f"e{j}B"] = f"moe.experts.{j}.conv.conv.bias"
    km["rB"] = "moe.router.bias"
    km["roB"] = "readout.bias"
    for i in range(L):
        km[f"tg{i}G"] = f"trunk.{i}.norm.weight"
    for i in range(L):
        km[f"tg{i}B"] = f"trunk.{i}.norm.bias"
    km["noG"] = "norm_out.weight"
    km["noB"] = "norm_out.bias"
    return km


def _general_block_order(L: int, E: int):
    return (["ecW"] + [f"tc{i}W" for i in range(L)]
            + [f"e{j}W" for j in range(E)] + ["rW", "roW"])


def _general_ext_order(L: int, E: int):
    return (["embed", "ecB"]
            + [f"tc{i}B" for i in range(L)]
            + [f"e{j}B" for j in range(E)]
            + ["rB", "roB"]
            + [f"tg{i}G" for i in range(L)]
            + [f"tg{i}B" for i in range(L)]
            + ["noG", "noB"])


def _to_np(x) -> "np.ndarray":
    """Coerce a torch.Tensor / numpy array / nested list to a float32 numpy array."""
    if np is None:
        raise RuntimeError("numpy is required for serialize_v2")
    # torch tensor (duck-typed: has detach + cpu + numpy)
    if hasattr(x, "detach"):
        x = x.detach().cpu().float().numpy()
    return np.asarray(x, dtype=np.float32)


def _conv_w_to_2d(w: "np.ndarray", name: str) -> "np.ndarray":
    """Map a weight tensor to the (cout, rest=Cin*K) 2-D layout the decoder expects.

    nn.Conv1d weight is (out, in, K). Decoder col-major within a block walks
    j = ci*K + k (see clm_decode _clmd_conv1d xcol indexing: ci*K + k), and the
    weight is read flat as w[co*rest + j] with j over Cin*K. nn.Conv1d's (out,in,K)
    flattened C-order is exactly co, then (in, K) -> in*K + k = ci*K + k. So a
    plain reshape(cout, -1) is byte-correct.
    nn.Linear-style (router/readout are Conv1d k=1) -> (out, in, 1) -> (out, in).
    """
    w = np.asarray(w, dtype=np.float32)
    if w.ndim == 3:
        cout = w.shape[0]
        return w.reshape(cout, -1)
    if w.ndim == 2:
        return w
    raise ValueError(f"unexpected weight ndim {w.ndim} for {name}")


def _quant_block(w2d: "np.ndarray"):
    """int4-sym per-output-channel quant. Returns (codes int8 [cout,rest], scale f32 [cout])."""
    cout = w2d.shape[0]
    amax = np.abs(w2d).max(axis=1)
    scale = np.maximum(amax / INT4_SYM_MAX, 1e-12).astype(np.float32)  # >0, never div0
    codes = np.round(w2d / scale[:, None])
    codes = np.clip(codes, -INT4_SYM_MAX, INT4_SYM_MAX).astype(np.int64)
    return codes.reshape(-1), scale, cout, w2d.shape[1]


def _pack_nibbles(codes_flat: "np.ndarray") -> bytes:
    """Pack flat int4 codes [-7,7] to bytes, 2 codes/byte, matching the decoder:
       low nibble = even-index code (+8), high nibble = odd-index code (+8)."""
    n = codes_flat.shape[0]
    off = (codes_flat.astype(np.int64) + 8) & 0xF            # 0..15
    if n % 2 == 1:
        off = np.concatenate([off, np.zeros(1, dtype=np.int64)])
    lo = off[0::2]   # even indices -> low nibble
    hi = off[1::2]   # odd indices  -> high nibble
    packed = ((hi << 4) | lo).astype(np.uint8)
    return packed.tobytes()


def _pack_conv_block(w2d: "np.ndarray") -> bytes:
    codes_flat, scale, cout, rest = _quant_block(w2d)
    out = bytearray()
    out += struct.pack("<I", cout)
    out += struct.pack("<I", rest)
    out += _pack_nibbles(codes_flat)
    out += scale.astype("<f4").tobytes()
    return bytes(out)


def _pack_ext(arr: "np.ndarray") -> bytes:
    flat = np.asarray(arr, dtype=np.float32).reshape(-1)
    return struct.pack("<I", flat.shape[0]) + flat.astype("<f4").tobytes()


def _resolve_state_dict(state_dict_or_ckpt, cfg) -> Dict[str, "np.ndarray"]:
    """Return a {logical_or_torch_key: np.ndarray} mapping.

    Accepts:
      - a path (str) to a torch ckpt  -> torch.load (lazy import)
      - a torch state_dict (OrderedDict of tensors)
      - a plain dict keyed by torch keys (e.g. 'embed.weight') OR by logical
        slot names (e.g. 'embed','ecW',...) -> values numpy/list arrays.
    """
    sd = state_dict_or_ckpt
    if isinstance(sd, str):
        import torch  # lazy
        sd = torch.load(sd, map_location="cpu")
        if isinstance(sd, dict) and "model" in sd and hasattr(sd.get("model"), "items"):
            sd = sd["model"]
    return sd


def _get(sd: Dict[str, Any], logical: str, keymap=None) -> "np.ndarray":
    """Fetch a weight by logical slot name, accepting either logical keys or
    torch state_dict keys in the source dict. `keymap` overrides _KEYMAP (used by
    the general v0.3 path with per-(L,E) slot names)."""
    km = keymap if keymap is not None else _KEYMAP
    if logical in sd:
        return _to_np(sd[logical])
    tkey = km[logical]
    if tkey in sd:
        return _to_np(sd[tkey])
    raise KeyError(
        f"missing weight for slot '{logical}' (tried torch key '{tkey}'); "
        f"available keys: {list(sd.keys())[:12]}..."
    )


def _assert_e2_l1(cfg):
    """The CORE decoder hardcodes E=2 experts + 1 trunk layer. Enforce it."""
    if cfg is None:
        return
    n_e = getattr(cfg, "n_experts", None)
    n_l = getattr(cfg, "n_trunk_layers", None)
    if n_e is not None and n_e != 2:
        raise ValueError(
            f"core/decode.hexa CONV mouth is FIXED to E=2 experts; cfg.n_experts={n_e}. "
            f"Train with a CLMConfig(n_experts=2, n_trunk_layers=1) preset."
        )
    if n_l is not None and n_l != 1:
        raise ValueError(
            f"core/decode.hexa CONV mouth is FIXED to 1 trunk layer; "
            f"cfg.n_trunk_layers={n_l}. Train with n_trunk_layers=1."
        )


def serialize_v2(state_dict_or_ckpt, cfg, out_path: str) -> str:
    """Pack a CLMConvMoE (E=2 / 1-trunk) state_dict to a CLM\\x01 v0.2 .clm that
    core/decode.hexa's CONV mouth loads. Returns out_path.

    cfg may be a CLMConfig (asserted E=2/L1) or None (skip the assert — caller
    vouches the dict already matches the E=2/L1 slot layout, e.g. synthetic test).
    """
    if np is None:
        raise RuntimeError("numpy is required for serialize_v2")
    _assert_e2_l1(cfg)
    sd = _resolve_state_dict(state_dict_or_ckpt, cfg)

    blob = bytearray()
    blob += MAGIC
    blob += struct.pack("<B", 6)            # nblk = 6

    for slot in _BLOCK_ORDER:
        w = _get(sd, slot)
        w2d = _conv_w_to_2d(w, slot)
        blob += _pack_conv_block(w2d)

    blob += CLMX
    blob += struct.pack("<B", len(_EXT_ORDER))   # n_ext = 11
    for slot in _EXT_ORDER:
        blob += _pack_ext(_get(sd, slot))

    with open(out_path, "wb") as f:
        f.write(blob)
    return out_path


def serialize_v3(state_dict_or_ckpt, n_trunk_layers: int, n_experts: int,
                 out_path: str, n_factions: int = 0) -> str:
    """Pack a GENERAL CLMConvMoE(n_trunk_layers=L, n_experts=E, d, K) to a
    CLM\\x01 v0.3 .clm that core/decode.hexa's CONV mouth loads.

    v0.3 == v0.2 byte grammar, generalized block/ext counts (see the v0.3 note
    above). At L=1,E=2 the output is BYTE-IDENTICAL to serialize_v2 (verified by
    the round-trip gate). d, K, V are read from the weight shapes — no width
    hardcode. Returns out_path.

    n_factions>0 (H_9643): a faction model's grouped trunk conv must be dense-materialized and a
    CLMF trailer appended so `anima-py evaluate --faction-lesion` can read K. That logic lives in
    clm_serialize_v2 (the faction-aware SSOT); we DELEGATE rather than keep a second copy of the
    grouped-conv materialize — a near-miss between two copies of the slot-name test is exactly the
    silent corruption clm_serialize_v2._conv_groups_for was written to prevent. n_factions=0 keeps
    the standard additive path byte-identical.
    """
    if np is None:
        raise RuntimeError("numpy is required for serialize_v3")
    L, E = int(n_trunk_layers), int(n_experts)
    if L < 1 or E < 1:
        raise ValueError(f"need L>=1 and E>=1, got L={L} E={E}")
    sd = _resolve_state_dict(state_dict_or_ckpt, None)
    if int(n_factions or 0) > 0:
        import clm_serialize_v2 as _V2                # same core/ package, faction-aware SSOT
        blob = _V2._pack_main_blob(sd, L, E) + _V2.pack_faction_section(sd, int(n_factions))
        with open(out_path, "wb") as f:
            f.write(blob)
        return out_path
    blob = _pack_main_blob(sd, L, E)
    with open(out_path, "wb") as f:
        f.write(blob)
    return out_path


def _pack_main_blob(sd: Dict[str, Any], L: int, E: int) -> bytearray:
    """Pack the MAIN CLM\\x01 body (MAGIC + nblk + conv blocks + CLMX + ext arrays)
    for a general (L,E) CLMConvMoE, returning a bytearray (no CLMB section). Shared
    by serialize_v3 (additive) and serialize_v3_bind (which appends a CLMB section).
    The readout slot roW (cout=block[nblk-1].cout=V, rest) is taken from
    'readout.weight' / roB from 'readout.bias': for a bind model the caller has
    routed Wo -> readout.{weight,bias} so the block is (V, k) instead of (V, d)
    (the byte grammar is self-describing — rest is read from the header at decode)."""
    bkm = _general_block_keymap(L, E)
    ekm = _general_ext_keymap(L, E)
    border = _general_block_order(L, E)
    eorder = _general_ext_order(L, E)
    nblk = len(border)            # = L + E + 3
    n_ext = len(eorder)           # = 2L + E + 6

    blob = bytearray()
    blob += MAGIC
    blob += struct.pack("<B", nblk)
    for slot in border:
        w = _get(sd, slot, bkm)
        w2d = _conv_w_to_2d(w, slot)
        blob += _pack_conv_block(w2d)
    blob += CLMX
    blob += struct.pack("<B", n_ext)
    for slot in eorder:
        blob += _pack_ext(_get(sd, slot, ekm))
    return blob


def _bget(sd: Dict[str, Any], names) -> "np.ndarray":
    """Fetch the first present key among `names` from a (torch- or logical-keyed)
    state dict, coerced to a float32 numpy array. Accepts a 'base.'-stripped dict."""
    for nm in names:
        if nm in sd:
            return _to_np(sd[nm])
    raise KeyError(f"none of {names} present (have: {list(sd.keys())[:16]}...)")


def serialize_v3_bind(state_dict_or_ckpt, n_trunk_layers: int, n_experts: int,
                      readout_type: int, out_path: str) -> str:
    """Pack a BIND-readout CLMConvMoE (the EXP-3 ARM-BIND architecture:
    BindCLM = production trunk + Hadamard byte readout u=Wa(x), v=Wb(x),
    g=u*v (readout_type=1) or u+v (readout_type=2), logits=Wo(g)) to a CLM\\x01
    .clm that core/decode.hexa's CONV mouth loads.

    BYTE LAYOUT (backward-compatible, in-place extension — no magic bump):
      · MAIN body == serialize_v3, EXCEPT the readout slot roW carries **Wo**
        (cout=V, rest=k) and roB carries **Wo.bias** (V). All trunk/embed/MoE
        blocks+ext are IDENTICAL to the additive ctrl arm (only the readout
        differs — the EXP-3 design intent). The self-describing (d,E,V,L,K)
        recovery is UNCHANGED (E=block[nblk-2].cout, V=block[nblk-1].cout, the
        readout block's `rest` field = k).
      · a CLMB trailer is appended AFTER the CLMX ext arrays:
          "CLMB"            (67,76,77,66)
          readout_type:u8   (1=Hadamard u*v, 2=linear u+v)
          Wa conv block     (cout=k, rest=d, int4-sym + per-channel fp32 scale)
          Wb conv block     (cout=k, rest=d, int4-sym + per-channel fp32 scale)
          Wa_bias ext       (u32 k + k*f32)
          Wb_bias ext       (u32 k + k*f32)
        An additive .clm has NO CLMB section, so the decoder defaults
        readout_type=0 (a_engine_native_learning backward-compat: existing
        additive .clm decode byte-identically).

    Accepts a torch state_dict (BindCLM.state_dict(): base.<trunk...> + Wa/Wb/Wo
    .{weight,bias}) OR a logical dict (Wa,WaB,Wb,WbB,Wo,WoB + v3 slot names).
    Returns out_path."""
    if np is None:
        raise RuntimeError("numpy is required for serialize_v3_bind")
    L, E = int(n_trunk_layers), int(n_experts)
    rt = int(readout_type)
    if L < 1 or E < 1:
        raise ValueError(f"need L>=1 and E>=1, got L={L} E={E}")
    if rt not in (RO_BIND_HADAMARD, RO_BIND_LINEAR):
        raise ValueError(f"readout_type must be 1 (hadamard) or 2 (linear), got {rt}")
    sd = _resolve_state_dict(state_dict_or_ckpt, None)

    # normalize: strip BindCLM's 'base.' trunk prefix into bare CLMConvMoE keys.
    norm: Dict[str, Any] = {}
    for k, v in sd.items():
        nk = k[5:] if k.startswith("base.") else k
        norm[nk] = v

    # bind readout weights (Wa/Wb -> CLMB ; Wo -> routed into the roW/roB slots).
    Wa = _bget(norm, ["Wa.weight", "Wa"])
    WaB = _bget(norm, ["Wa.bias", "WaB"])
    Wb = _bget(norm, ["Wb.weight", "Wb"])
    WbB = _bget(norm, ["Wb.bias", "WbB"])
    Wo = _bget(norm, ["Wo.weight", "Wo"])
    WoB = _bget(norm, ["Wo.bias", "WoB"])
    norm["readout.weight"] = Wo        # (V, k, 1) -> roW block (cout=V, rest=k)
    norm["readout.bias"] = WoB         # (V,)      -> roB ext

    blob = _pack_main_blob(norm, L, E)
    blob += CLMB
    blob += struct.pack("<B", rt)
    blob += _pack_conv_block(_conv_w_to_2d(Wa, "Wa"))   # (k, d)
    blob += _pack_conv_block(_conv_w_to_2d(Wb, "Wb"))   # (k, d)
    blob += _pack_ext(WaB)                               # (k,)
    blob += _pack_ext(WbB)                               # (k,)

    with open(out_path, "wb") as f:
        f.write(blob)
    return out_path


def serialize_clm(state_dict_or_ckpt, n_trunk_layers: int, n_experts: int,
                  out_path: str) -> str:
    """Unified CLM entry: routes to serialize_v3 (general). For L=1,E=2 the v3 path
    is byte-identical to serialize_v2, so this is the single CLM serializer for ANY
    (L,E,d). cfg-free — caller states (L,E) explicitly.

    NAME NOTE (union dispatch): in the standalone clm_serialize_v2.py this was the
    bare `serialize`; on the unified module the bare `serialize` binds the ByteGPT
    .pt→.bin bridge (BGS.serialize contract), so the CLM unified entry lives here
    as `serialize_clm`. No live importer called the CLM bare `serialize` (grep-
    verified); all live callers use `serialize_v3` directly."""
    return serialize_v3(state_dict_or_ckpt, n_trunk_layers, n_experts, out_path)


# ════════════════════════════════════════════════════════════════════════
# (c) BYTE (ByteGPT) — verbatim port of tool/bytegpt_serialize.py. torch .pt →
#     engine .bin (5×u32 header) BRIDGE. Ground-truth layout = core/decode.hexa
#     BYTE mouth (bg_load / bytegpt_forward_last).
#
#   header 5x u32 little-endian: [vocab, d, n_layer, n_head, block]
#   tok[vocab*d]  pos[block*d]
#   per layer: ln1.w[d] ln1.b[d] in_proj.w[3d*d] in_proj.b[3d]
#              out_proj.w[d*d] out_proj.b[d] ln2.w[d] ln2.b[d]
#              mlp0.w[4d*d] mlp0.b[4d] mlp2.w[d*4d] mlp2.b[d]
#   ln_f.w[d] ln_f.b[d]  head[vocab*d]     (all little-endian float32.)
#
# WEIGHT ORIENTATION: torch nn.Linear.weight is [out,in] row-major; the engine's
# _bg_linear ALSO stores W as [Co,Ci] row-major and transposes at load, so torch's
# native [out,in] is written VERBATIM (NO transpose here). in_proj_weight [3d,d] is
# rows Q|K|V — exactly what _bg_mha expects (NO reordering).
# ════════════════════════════════════════════════════════════════════════

def _f32le(t) -> bytes:
    """Flatten a torch tensor ROW-MAJOR (C-contiguous) to little-endian float32 bytes."""
    import torch  # training family — torch OK here (.pt bridge)
    a = t.detach().cpu().to(torch.float32).contiguous().numpy()
    a = np.ascontiguousarray(a, dtype="<f4")  # little-endian float32, C order
    return a.tobytes()


def serialize(pt_path: str, bin_path: str) -> None:
    """ByteGPT .pt (cfg+state_dict) → engine .bin BRIDGE (BGS.serialize contract).

    torch is imported here (the .pt bridge is LEARNING-side, a_clm_gen_pipeline) — this
    is NOT the verdict scorer; the verdict is the engine `anima evaluate <bin>` (generator
    L3 → core/decode.hexa BYTE mouth)."""
    import torch  # training family — torch OK here (.pt bridge)
    ck = torch.load(pt_path, map_location="cpu", weights_only=False)
    sd = ck["model"]
    cfg = ck["config"]
    vocab, d, n_layer, n_head, block = (
        int(cfg["vocab"]), int(cfg["d"]), int(cfg["n_layer"]),
        int(cfg["n_head"]), int(cfg["block"]),
    )
    print(f"[cfg] vocab={vocab} d={d} n_layer={n_layer} n_head={n_head} block={block}", flush=True)
    print(f"[cfg] val_ce={ck.get('val_ce')} step={ck.get('step')} nparam={ck.get('nparam')}", flush=True)

    def W(key, shape):
        if key not in sd:
            raise KeyError(f"missing state_dict key: {key}")
        t = sd[key]
        if tuple(t.shape) != tuple(shape):
            raise ValueError(f"{key} shape {tuple(t.shape)} != expected {tuple(shape)}")
        return _f32le(t)

    out = bytearray()
    # header
    out += struct.pack("<5I", vocab, d, n_layer, n_head, block)
    # embeddings
    out += W("tok.weight", (vocab, d))
    out += W("pos.weight", (block, d))
    # per layer
    for i in range(n_layer):
        p = f"blocks.{i}."
        out += W(p + "ln1.weight", (d,))
        out += W(p + "ln1.bias", (d,))
        out += W(p + "attn.in_proj_weight", (3 * d, d))
        out += W(p + "attn.in_proj_bias", (3 * d,))
        out += W(p + "attn.out_proj.weight", (d, d))
        out += W(p + "attn.out_proj.bias", (d,))
        out += W(p + "ln2.weight", (d,))
        out += W(p + "ln2.bias", (d,))
        out += W(p + "mlp.0.weight", (4 * d, d))
        out += W(p + "mlp.0.bias", (4 * d,))
        out += W(p + "mlp.2.weight", (d, 4 * d))
        out += W(p + "mlp.2.bias", (d,))
    # final norm + tied head
    out += W("ln_f.weight", (d,))
    out += W("ln_f.bias", (d,))
    head_key = "head.weight" if "head.weight" in sd else "tok.weight"  # tied
    out += W(head_key, (vocab, d))

    # expected size check
    per_layer = (d + d) + (3 * d * d + 3 * d) + (d * d + d) + (d + d) + \
                (4 * d * d + 4 * d) + (d * 4 * d + d)
    expected = 20 + (vocab * d + block * d) * 4 + n_layer * per_layer * 4 + \
               (d + d + vocab * d) * 4
    if len(out) != expected:
        raise AssertionError(f"size mismatch: wrote {len(out)} expected {expected}")

    with open(bin_path, "wb") as f:
        f.write(out)
    print(f"[ok] wrote {bin_path}  bytes={len(out)} (expected {expected})", flush=True)


# alias — the ByteGPT bridge under a mouth-explicit name (parallels serialize_clm).
bytegpt_serialize = serialize


# ════════════════════════════════════════════════════════════════════════
# (c2) BYTE injected-bind (BGB) — base ByteGPT .bin (verbatim) + N appended
#      GATED transformer blocks -> engine .bin with a "BGB\x01" trailer. The
#      ByteGPT analogue of the CONV "CLMB" bind-readout extension: the base
#      bytes are copied UNCHANGED and the trailer is appended after `head`, so a
#      gate=0 file decodes byte-identically to its base (core/decode.py bg_load
#      reads the optional trailer; W["bind"]=[] when absent -> zero regression).
#
#   BGB trailer (after head): magic 66,71,66,1 ; u32 n_bind ;
#     per bind block: the SAME 12 param tensors as a base layer in the SAME
#       order/layout as `serialize` above (ln1.w[d] ln1.b[d] in_proj.w[3d,d]
#       in_proj.b[3d] out_proj.w[d,d] out_proj.b[d] ln2.w[d] ln2.b[d]
#       mlp0.w[4d,d] mlp0.b[4d] mlp2.w[d,4d] mlp2.b[d], all LE f32 VERBATIM —
#       torch native [out,in], NO transpose) ; then one LE f32 `gate`.
#
# Reading the injected torch .pt (unpickle) is the only torch touch (training
# family, a_clm_gen_pipeline / a_engine_native_learning: serializer may use torch).
# The injected .pt carries a standard transformer Block state_dict + a scalar gate
# per appended block (BindAttnByteGPT: self.bind=Block(...), self.gate).
# ════════════════════════════════════════════════════════════════════════

BGB = bytes([66, 71, 66, 1])        # "BGB\x01" — ByteGPT injected-bind trailer


def _bfind(bsd, suffix):
    """Resolve a Block state_dict tensor by key SUFFIX (robust to a 'bind.'/module
    prefix). Exact match first, else the unique / shortest suffix match."""
    if suffix in bsd:
        return bsd[suffix]
    cands = [k for k in bsd if k.endswith(suffix)]
    if not cands:
        raise KeyError("bind block missing key *" + suffix + " (keys=" + ",".join(sorted(bsd)) + ")")
    cands.sort(key=len)
    return bsd[cands[0]]


def _bind_block_bytes(bsd, d):
    """Map ONE torch Block state_dict -> BGB block bytes (12 tensors, bg_load order,
    VERBATIM f32le — same orientation as `serialize`'s per-layer write, no transpose)."""
    def w(name, shape):
        t = _bfind(bsd, name)
        if tuple(t.shape) != tuple(shape):
            raise ValueError(f"bind {name} shape {tuple(t.shape)} != expected {tuple(shape)}")
        return _f32le(t)
    out = bytearray()
    out += w("ln1.weight", (d,))
    out += w("ln1.bias", (d,))
    out += w("attn.in_proj_weight", (3 * d, d))
    out += w("attn.in_proj_bias", (3 * d,))
    out += w("attn.out_proj.weight", (d, d))
    out += w("attn.out_proj.bias", (d,))
    out += w("ln2.weight", (d,))
    out += w("ln2.bias", (d,))
    out += w("mlp.0.weight", (4 * d, d))
    out += w("mlp.0.bias", (4 * d,))
    out += w("mlp.2.weight", (d, 4 * d))
    out += w("mlp.2.bias", (d,))
    return bytes(out)


def _is_block_sd(x):
    """True if x is a single Block state_dict (has an in_proj_weight-suffixed key)."""
    return isinstance(x, dict) and any(str(k).endswith("in_proj_weight") for k in x)


def _scalar(g):
    """Coerce a gate (python number / 0-d or 1-elem torch tensor / list) -> float."""
    if hasattr(g, "detach"):
        g = g.detach().cpu().reshape(-1)
        return float(g[0])
    if isinstance(g, (list, tuple)):
        return float(g[0])
    return float(g)


def _normalize_bind_list(binds, gates):
    """Return an ordered list of (block_state_dict, gate_float). Accepts:
      * single Block state_dict + scalar gate                  -> [(sd, g)]
      * list of Block state_dicts + list|scalar of gates       -> zipped
      * dict{idx: Block state_dict} + dict|list|scalar gates   -> index-ordered."""
    if _is_block_sd(binds):
        return [(binds, _scalar(gates))]
    if isinstance(binds, (list, tuple)):
        n = len(binds)
        gl = gates if isinstance(gates, (list, tuple)) else [gates] * n
        return [(binds[i], _scalar(gl[i])) for i in range(n)]
    if isinstance(binds, dict):
        keys = sorted(binds, key=lambda k: (int(k) if str(k).isdigit() else 1 << 30, str(k)))
        out = []
        for i, k in enumerate(keys):
            if isinstance(gates, dict):
                g = gates[k]
            elif isinstance(gates, (list, tuple)):
                g = gates[i]
            else:
                g = gates
            out.append((binds[k], _scalar(g)))
        return out
    raise TypeError("unrecognized 'bind' payload type: " + str(type(binds)))


def serialize_bind(base_bin: str, injected_pt: str, out_bin: str) -> str:
    """base ByteGPT .bin (bytes VERBATIM) + injected torch .pt -> engine .bin + BGB
    trailer. injected_pt = {"bind": <Block state_dict | list | dict>, "gate":
    <scalar | list | dict>, "config": {...}}. Supports N>=1 appended blocks.

    torch is imported ONLY to unpickle the .pt (irreducible); the byte layout is
    reference-matched to `serialize` (per-layer write) + core/decode.py bg_load."""
    import torch  # training family — torch OK here (.pt bridge)
    base = open(base_bin, "rb").read()
    if len(base) < 20:
        raise ValueError("base .bin too small (no 5xu32 header): " + base_bin)
    vocab, d, n_layer, n_head, block = struct.unpack("<5I", base[:20])
    # sanity: reject a CLM base (CLM\x01 magic) — BGB rides ByteGPT only.
    if base[0] == 67 and base[1] == 76 and base[2] == 77 and base[3] == 1:
        raise ValueError("base is a CLM .clm, not a ByteGPT .bin: " + base_bin)

    ck = torch.load(injected_pt, map_location="cpu", weights_only=False)
    if not (isinstance(ck, dict) and "bind" in ck and "gate" in ck):
        raise KeyError("injected .pt must have keys {'bind','gate'}; got " + str(list(ck)[:8]))
    blocks = _normalize_bind_list(ck["bind"], ck["gate"])
    if len(blocks) < 1:
        raise ValueError("injected .pt carried 0 bind blocks")

    trailer = bytearray()
    trailer += BGB
    trailer += struct.pack("<I", len(blocks))
    for bsd, gate in blocks:
        bsd = {k: (v.detach().cpu() if hasattr(v, "detach") else v) for k, v in bsd.items()}
        trailer += _bind_block_bytes(bsd, d)
        trailer += struct.pack("<f", float(gate))

    with open(out_bin, "wb") as f:
        f.write(base)
        f.write(bytes(trailer))
    print(f"[ok] wrote {out_bin}  base={len(base)} + BGB(n_bind={len(blocks)},d={d})"
          f" trailer={len(trailer)} = {len(base) + len(trailer)} bytes"
          f"  gates={[round(g, 6) for _, g in blocks]}", flush=True)
    return out_bin


# ════════════════════════════════════════════════════════════════════════
# (d.inv) ByteGPT .bin → torch state_dict INVERSE — warm-start reader.
#   The exact byte-for-byte inverse of serialize() above (same 5×u32 header +
#   flat little-endian float32 tensor order). Used by `anima-py train --init
#   <base.bin>` to warm-start a fresh ByteGPT from a trained engine .bin. The
#   byte grammar SSOT stays in THIS file (mirror of serialize's write order).
# ════════════════════════════════════════════════════════════════════════

def deserialize_bytegpt(bin_path: str) -> "Tuple[Dict[str, Any], Dict[str, int]]":
    """Read a ByteGPT engine `.bin` (5×u32 header) back into a torch state_dict.

    Returns (state_dict, cfg) where state_dict has the EXACT keys ByteGPT.state_dict()
    emits (tok/pos/blocks.{i}.*/ln_f/head — head==tok since the head is tied) and cfg =
    {vocab,d,n_layer,n_head,block}. This is the byte-inverse of serialize(): it walks the
    same tensor order and reshapes each little-endian float32 slice to torch's native
    [out,in] orientation (serialize wrote torch's layout VERBATIM, so no transpose)."""
    import torch  # training/warm-start family — torch OK here (.bin bridge, a_clm_gen_pipeline)
    rb = open(bin_path, "rb").read() if not isinstance(bin_path, (bytes, bytearray)) else bin_path
    if len(rb) < 20:
        raise ValueError(f"deserialize_bytegpt: {bin_path} too short ({len(rb)}B) for a 5×u32 header")
    vocab, d, n_layer, n_head, block = struct.unpack_from("<5I", rb, 0)
    off = 20

    def rd(shape) -> "torch.Tensor":
        nonlocal off
        n = 1
        for s in shape:
            n *= s
        arr = np.frombuffer(rb, dtype="<f4", count=n, offset=off).astype(np.float32)
        off += 4 * n
        return torch.from_numpy(np.ascontiguousarray(arr).reshape(shape))

    sd: Dict[str, Any] = {}
    sd["tok.weight"] = rd((vocab, d))
    sd["pos.weight"] = rd((block, d))
    for i in range(n_layer):
        p = f"blocks.{i}."
        sd[p + "ln1.weight"] = rd((d,))
        sd[p + "ln1.bias"] = rd((d,))
        sd[p + "attn.in_proj_weight"] = rd((3 * d, d))
        sd[p + "attn.in_proj_bias"] = rd((3 * d,))
        sd[p + "attn.out_proj.weight"] = rd((d, d))
        sd[p + "attn.out_proj.bias"] = rd((d,))
        sd[p + "ln2.weight"] = rd((d,))
        sd[p + "ln2.bias"] = rd((d,))
        sd[p + "mlp.0.weight"] = rd((4 * d, d))
        sd[p + "mlp.0.bias"] = rd((4 * d,))
        sd[p + "mlp.2.weight"] = rd((d, 4 * d))
        sd[p + "mlp.2.bias"] = rd((d,))
    sd["ln_f.weight"] = rd((d,))
    sd["ln_f.bias"] = rd((d,))
    sd["head.weight"] = rd((vocab, d))   # tied — equals tok.weight in a serialized model
    if off != len(rb):
        raise AssertionError(
            f"deserialize_bytegpt: consumed {off}B but file is {len(rb)}B "
            f"(header cfg vocab={vocab} d={d} n_layer={n_layer} n_head={n_head} block={block} "
            f"— corrupt or wrong-arch .bin)")
    cfg = {"vocab": vocab, "d": d, "n_layer": n_layer, "n_head": n_head, "block": block}
    return sd, cfg


# ════════════════════════════════════════════════════════════════════════
# (e) FORMAT DISPATCH — pick the mouth serializer by target extension. Convenience
#     only; the existing entry points (serialize_v3 / serialize) are UNRENAMED.
# ════════════════════════════════════════════════════════════════════════

def serialize_auto(src, out_path: str, *, n_trunk_layers: int = None,
                   n_experts: int = None):
    """Dispatch by target extension: '.bin' → ByteGPT bridge (src=.pt path,
    serialize(pt,bin)); else → CLM serialize_v3 (src=state_dict/ckpt, needs
    n_trunk_layers/n_experts). The two mouth serializers have different input
    contracts (ByteGPT reads a .pt PATH; CLM takes a state_dict + (L,E)), so this
    only routes — it does not unify the signatures."""
    if str(out_path).endswith(".bin"):
        return serialize(src, out_path)
    if n_trunk_layers is None or n_experts is None:
        raise ValueError("CLM serialize_auto needs n_trunk_layers + n_experts")
    return serialize_v3(src, n_trunk_layers, n_experts, out_path)


# ---------------------------------------------------------------------------
# .clm -> state_dict  (the inverse of _pack_main_blob)
#
# Why this exists: `anima-py train --init` warm-starts from a `.pt`, and used to REFUSE a `.clm`
# ("dequant->state_dict remap is a follow-on"). That refusal is a trap in practice — a pod is torn
# down, only the `.clm` is pulled (a_fire_recover_complete), and the `.pt` is gone forever. Then
# every warm-start experiment on that checkpoint is dead, not for any scientific reason but for a
# missing inverse. H_9313 hit exactly this: the C34 `.pt` no longer exists anywhere.
#
# The map is exact in structure and lossy only where the format itself is lossy: conv blocks are
# int4-symmetric per-output-channel quantized, so dequantizing gives back `code * scale` — the
# EXACT weights the engine has been decoding all along, not an approximation of the original .pt.
# That is the right thing to warm-start from: it is the model we measured, byte for byte.
# ext arrays (biases, norms, embedding) are stored fp32 and come back exactly.
#
# Round-trip is idempotent by construction: dequantized values are exactly representable, so
# re-serializing them reproduces the same codes. `clm_roundtrip_is_identity` proves it on a real
# file rather than asserting it.
# ---------------------------------------------------------------------------

def _unpack_nibbles(buf: bytes, n: int) -> "np.ndarray":
    """Inverse of _pack_nibbles: bytes -> flat int4 codes in [-7, 7]."""
    raw = np.frombuffer(buf, dtype=np.uint8)
    lo = (raw & 0x0F).astype(np.int64) - 8          # even indices
    hi = ((raw >> 4) & 0x0F).astype(np.int64) - 8   # odd indices
    out = np.empty(raw.shape[0] * 2, dtype=np.int64)
    out[0::2] = lo
    out[1::2] = hi
    return out[:n]


def deserialize_v3(clm_path: str, n_trunk_layers: int, n_experts: int, K: int = 3):
    """Read a CLM\\x01 v0.3 `.clm` back into a torch-keyed state_dict of numpy arrays.

    Exact inverse of _pack_main_blob for (L, E): same block/ext ORDER, same KEYMAP. Conv blocks
    come back dequantized (code * per-row scale) — which is precisely what core/decode.py runs, so
    a model warm-started from this IS the measured model, not a reconstruction of a lost original.

    Returns {torch_key: np.ndarray}. Shapes are restored to nn.Conv1d's (out, in, K); a k=1 slot
    (router / readout) comes back as (out, in, 1).
    """
    if np is None:
        raise RuntimeError("numpy is required for deserialize_v3")
    L, E = int(n_trunk_layers), int(n_experts)
    blob = open(clm_path, "rb").read()
    if blob[:4] != MAGIC:
        raise ValueError(f"{clm_path}: not a CLM\\x01 file (magic={blob[:4]!r})")

    border, eorder = _general_block_order(L, E), _general_ext_order(L, E)
    bkm, ekm = _general_block_keymap(L, E), _general_ext_keymap(L, E)

    p = 4
    nblk = struct.unpack_from("<B", blob, p)[0]
    p += 1
    if nblk != len(border):
        raise ValueError(f"{clm_path}: nblk={nblk} but (L={L},E={E}) expects {len(border)} — "
                         "wrong L/E for this file")

    sd = {}
    for slot in border:
        cout, rest = struct.unpack_from("<II", blob, p)
        p += 8
        nbytes = (cout * rest + 1) // 2
        codes = _unpack_nibbles(blob[p:p + nbytes], cout * rest).reshape(cout, rest)
        p += nbytes
        scale = np.frombuffer(blob[p:p + 4 * cout], dtype="<f4").astype(np.float32)
        p += 4 * cout
        w2d = (codes.astype(np.float32) * scale[:, None])       # dequant — exact, not approximate
        # (cout, Cin*K) -> (cout, Cin, K). A k=1 slot has rest == Cin.
        kk = K if (rest % K == 0 and slot not in ("rW", "roW")) else 1
        sd[bkm[slot]] = w2d.reshape(cout, rest // kk, kk)

    if blob[p:p + 4] != CLMX:
        raise ValueError(f"{clm_path}: CLMX marker not found at offset {p}")
    p += 4
    n_ext = struct.unpack_from("<B", blob, p)[0]
    p += 1
    if n_ext != len(eorder):
        raise ValueError(f"{clm_path}: n_ext={n_ext} but (L={L},E={E}) expects {len(eorder)}")
    for slot in eorder:
        n = struct.unpack_from("<I", blob, p)[0]
        p += 4
        sd[ekm[slot]] = np.frombuffer(blob[p:p + 4 * n], dtype="<f4").astype(np.float32).copy()
        p += 4 * n

    # embed / norms / biases are 1-D on the wire; restore embed to (V, d).
    emb = sd[ekm["embed"]]
    d = sd[bkm["ecW"]].shape[1]          # embed_conv in-channels == d
    sd[ekm["embed"]] = emb.reshape(-1, d)
    return sd


def clm_roundtrip_is_identity(clm_path: str, n_trunk_layers: int, n_experts: int) -> bool:
    """Prove the inverse is exact: deserialize -> serialize must reproduce the file BYTE for BYTE.

    This is the parity gate a warm-start from `.clm` rests on. If it holds, then training that
    starts from deserialize_v3(f) starts from exactly the weights the engine decodes out of f —
    so a post-CPT delta cannot be a dequantization artifact.
    """
    sd = deserialize_v3(clm_path, n_trunk_layers, n_experts)
    repacked = bytes(_pack_main_blob(sd, int(n_trunk_layers), int(n_experts)))
    raw = open(clm_path, "rb").read()
    if repacked == raw:
        return True
    # A lane-carrying model IS "a normal .clm + trailer chain" (CLMB→SLW→CLML→CLMS→MBND→IFAN→TFLD,
    # see the trailer sections above), and _pack_main_blob packs only the MAIN blob. Comparing it to
    # the WHOLE file therefore rejected every store-bridge / mouth-binder checkpoint that ever
    # trained — not because the inverse was inexact, but because the gate measured the wrong span.
    # The property a warm-start actually rests on is about the main blob: deserialize_v3 ->
    # _pack_main_blob must reproduce it byte for byte. Assert exactly that, on the file's PREFIX.
    # The excess must be a real trailer (known magic) — arbitrary trailing bytes stay a refusal, so
    # a truncated/corrupt/foreign file cannot sneak through as "just a trailer".
    # NOTE for callers: deserialize_v3 reads the main blob ONLY, so the returned state_dict carries
    # NO lane weights. Warm-starting from a lane-carrying ckpt restores the trunk, not the lane.
    if not (len(raw) > len(repacked) and raw.startswith(repacked)):
        return False
    if raw[len(repacked):len(repacked) + 4] not in _TRAILER_MAGICS:
        return False
    # Magic alone is NOT enough: a truncated/corrupt lane, or arbitrary bytes glued after a valid
    # magic, would both sail through and the lane would go silently missing. Walk the chain with the
    # CORE-owned readers (no second parser to drift) and demand it consume EXACTLY to EOF.
    try:
        emb = sd.get("embed.weight")
        V, d = (int(emb.shape[0]), int(emb.shape[1])) if emb is not None else (0, 0)
        return _trailer_chain_end(raw, len(repacked), d, V) == len(raw)
    except Exception:
        return False        # an unparseable trailer is a refusal, never a pass


def _trailer_chain_end(raw: bytes, off: int, d: int, V: int) -> int:
    """Offset after walking the appended-trailer chain at `off`, in the ONE legal chain order
    SLW→CLML→CLMS→MBND→IFAN→TFLD. Each reader passthroughs (returns `off` unchanged) when its magic
    is absent, so a partial chain walks fine; a trailer out of order simply stops the walk and the
    caller's `== len(raw)` fails. Deliberately syntactic — it proves the bytes are a well-formed
    chain that ends where the file ends, and says NOTHING about whether the lane weights are sane
    (that belongs to whoever runs the lane, not to a warm-start parity gate)."""
    # Two live layouts: vendored `core/` straight on sys.path, and the installed `anima_py.core`
    # package. Import must resolve in BOTH — a bare `from slw import …` raises ModuleNotFoundError
    # inside the wheel, and the caller's except-clause would turn that into "checkpoint refused".
    def _rd(mod, name):
        try:
            m = __import__(mod, fromlist=[name])            # vendored core/ on sys.path
        except ModuleNotFoundError:
            m = __import__("anima_py.core." + mod, fromlist=[name])   # installed wheel
        return getattr(m, name)
    read_slw = _rd("slw", "read_slw")
    read_clml = _rd("clml", "read_clml")
    read_clms = _rd("clms", "read_clms")
    read_mbnd = _rd("mbnd", "read_mbnd")
    read_ifan = _rd("ifan", "read_ifan")
    read_tfld = _rd("tension_field", "read_tfld")
    _, off = read_slw(raw, off)
    for rd in (read_clml, read_clms, read_mbnd, read_ifan):
        _, off = rd(raw, off, d, V)
    _, off = read_tfld(raw, off, d)
    return off

# ── "CNRM" trunk-norm marker (H_9875) ────────────────────────────────────────────
# One byte at the very end of the trailer chain: 1 = the trunk was trained with per-position
# normalization (core/model.py::PerPositionGroupNorm), 0/absent = the legacy sequence-global
# GroupNorm. It is a MARKER, not weights — the decode path needs to know which reduction the
# weights were fitted under, and without it an engine-native score of a position-norm ckpt silently
# measures a different model. Never appended for global-norm ckpts, so every existing .clm and
# every default build stays byte-identical.
CNRM_MAGIC = b"CNRM"


def append_trunknorm_trailer(path: str, trunk_norm: str) -> str:
    """Append the CNRM marker to a .clm. No-op for the legacy 'global' mode (byte-identical)."""
    if trunk_norm != "position":
        return path
    with open(path, "ab") as f:
        f.write(CNRM_MAGIC + bytes([1]))
    return path
