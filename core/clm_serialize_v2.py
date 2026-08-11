# ==========================================================================
# ⛔ ENGINE-INTERNAL — DO NOT RUN DIRECTLY. 학습/직렬화는 cli/ 단일진입만:
#   anima-py train | anima-py serialize.
# `python3 train/clm/model/clm_serialize_v2.py` 직접 실행 = 단일진입 우회(#2603) + DIRECTIONAL. cli/ import만 허용.
# ==========================================================================
#!/usr/bin/env python3
"""Lane P REMEDY — torch -> .clm serializer matching core/clm_decode.hexa EXACTLY.

The prior CLM/model/clm_serialize.py emits a 2-track JSON-header format that
shares only the "CLM\\x01" magic with the ENGINE decoder and is NOT loadable
(see .verdicts/lane-p-clm/F-CLM-SERIALIZE-GAP.txt). This v2 serializer packs the
EXACT CLM\\x01 v0.2 byte layout that core/clm_decode.hexa::clm_decodable parses.

CLM\\x01 v0.2 byte layout (ground truth = core/clm_decode.hexa + the golden
reference state/laneg_d768_recover/reexport_d768_v2_fast.clm):

  [0:4]  MAGIC "CLM\\x01"  = bytes 67,76,77,1
  [4]    nblk : u8          = 6  (production CLMConvMoE, E=2 / 1 trunk layer)
  then nblk conv blocks, each:
    u32 cout (LE)
    u32 rest (LE)            rest = Cin*K
    int4 nibbles             ((cout*rest+1)//2 bytes, 2 codes/byte, sym int4)
    fp32 per-channel scale   (cout float32 LE)
  block order (decoder-fixed):
    block0 ecW : cout=d,  rest=d*K   (K = rest0/d)
    block1 tcW : cout=d,  rest=d*K
    block2 e0W : cout=d,  rest=d*K
    block3 e1W : cout=d,  rest=d*K
    block4 rW  : cout=E,  rest=d     (router, K=1) -> E=2
    block5 roW : cout=V,  rest=d     (readout, K=1) -> V=256
  CLMX v0.2 trailer (REQUIRED — clm_decodable()=false without it):
    "CLMX" = 67,76,77,88
    n_ext : u8 = 11
    then 11 ext arrays, EACH = u32 count (LE) + count float32 (LE), in ORDER:
      embed (V*d), ecB (d), tcB (d), e0B (d), e1B (d), rB (E), roB (V),
      tgG (d), tgB (d), noG (d), noB (d)
    (tg* = trunk GroupNorm affine, no* = output GroupNorm affine)

int4-sym quant (decoder dequant w[co,j] = code * scale[co]):
  per OUTPUT channel co:  scale[co] = max_j(|w[co,j]|) / 7   (clamped >0)
                          code[co,j] = round(w[co,j]/scale[co]) clamped to [-7,7]

NIBBLE PACKING — must match the decoder byte-for-byte. The decoder reads, for a
flat code index i (i even):
    code[i]   = (byte & 0xF) - 8        # low nibble
    code[i+1] = ((byte >> 4) & 0xF) - 8 # high nibble
So: low nibble  holds the EVEN index code (+8 offset),
    high nibble holds the ODD  index code (+8 offset).
  byte = ((code[i+1]+8) << 4) | (code[i]+8)
The trailing code of an odd-length run pads its high nibble with 0.

torch is imported lazily: pass a ckpt path / state_dict (torch present) OR a
plain dict of numpy/list weight arrays (torch absent) so the serializer is
testable without torch.
"""
from __future__ import annotations

# ⛔ ENGINE-INTERNAL — DO NOT RUN DIRECTLY (단일진입 우회 #2603). cli/ import만 허용.
# 가드는 `from __future__` 뒤에 둔다 — 앞에 두면 SyntaxError(from __future__ must be at top).
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ clm_serialize_v2.py 직접 실행 금지 — canonical `anima-py` 경유. #2603")

import re
import struct
from typing import Dict, Any

try:
    import numpy as np
except Exception:  # pragma: no cover - numpy is effectively always present
    np = None

MAGIC = bytes([67, 76, 77, 1])      # "CLM\x01"
CLMX = bytes([67, 76, 77, 88])      # "CLMX"
CLMB = bytes([67, 76, 77, 66])      # "CLMB" — bind-readout (Hadamard) extension
CLMF = bytes([67, 76, 77, 70])      # "CLMF" — H_9643 faction lane (K + cross-faction bridge)
INT4_SYM_MAX = 7

# readout-type flag (CLMB byte[4]). 0 = additive Conv1d(d->V) (default, NO CLMB
# section); 1 = bind/Hadamard  g=u*v ; 2 = bind_linear (param-matched add) g=u+v.
RO_ADDITIVE = 0
RO_BIND_HADAMARD = 1
RO_BIND_LINEAR = 2

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


# H_9643: the trunk/embed convs are grouped iff the model was built with --n-factions K.
# Set by the packer from the state dict's own faction section; read by _conv_w_to_2d. A module
# global (not a shape guess) because ONLY the model knows which convs it grouped.
_FACTION_GROUPS = {"n": 0}
# Which conv slots core/model.py builds with groups=K when the faction lane is ON:
# the embed conv ("ecW") and every trunk layer ("tc0W", "tc1W", … — see _general_block_order).
# The expert convs ("e0W"…), router ("rW") and readout ("roW") are NEVER grouped: MoE+readout
# are the CONSENSUS stage and stay full-mixing on purpose.
_GROUPED_SLOT_RE = re.compile(r"^(ecW|tc\d+W)$")


def _conv_groups_for(name: str) -> int:
    """groups for a conv slot: K for the faction-grouped slots, 1 for everything else.

    Matched by an EXACT slot pattern, never a prefix. An earlier cut used a startswith("tcW")
    test against the real slot names tc0W/tc1W and matched NOTHING — the trunk went out grouped
    (48,64) while the decoder expected dense (192,64) and the matmul blew up. A near-miss on a
    name is silent; the regex is anchored so a miss is a miss.
    """
    n = int(_FACTION_GROUPS.get("n", 0) or 0)
    if n <= 1:
        return 1
    base = name.split(".")[0] if "." in name else name
    return n if _GROUPED_SLOT_RE.match(base) else 1


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
        cout, cin_per_g, ks = w.shape
        # H_9643 grouped (faction) conv: nn.Conv1d(d, d, ks, groups=K) stores weight as
        # (d, d/K, ks) — only each output channel's OWN faction's inputs. The decoder's byte
        # grammar is dense: it reads rest = Cin*K with Cin = d and walks j = ci*ks + k over ALL
        # d input channels. Writing the (d, d/K, ks) reshape would silently mean "rest = d/K*ks"
        # and the decoder would read the wrong columns. So materialize the block-diagonal into a
        # dense (d, d, ks) with structural zeros off the faction block — same math, decoder-shaped
        # bytes (the TLoRA/bind sections set the precedent: the .clm stays one grammar).
        #
        # `groups` is passed in by the CALLER, never inferred. An earlier cut guessed "grouped iff
        # cout % cin_per_g == 0 and cin_per_g != cout" and that guess ate the READOUT: readout is
        # an honest dense Conv1d(64 -> 256, k=1) whose weight is (256, 64, 1), which satisfies the
        # guess and got expanded to (256, 256, 1) — the decoder then read a (256,256) roWt and the
        # matmul blew up. A shape cannot tell you the author's intent; the model must say.
        groups = int(_conv_groups_for(name) or 1)
        if groups > 1:
            if cout % groups or cin_per_g * groups != cout:
                raise ValueError(
                    f"{name}: groups={groups} inconsistent with weight {w.shape} "
                    f"(expected (cout, cout/groups, ks))")
            dense = np.zeros((cout, cout, ks), dtype=np.float32)
            per_out = cout // groups
            for g in range(groups):
                o0, o1 = g * per_out, (g + 1) * per_out
                i0, i1 = g * cin_per_g, (g + 1) * cin_per_g
                dense[o0:o1, i0:i1, :] = w[o0:o1, :, :]
            w = dense
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
            f"core/clm_decode.hexa is FIXED to E=2 experts; cfg.n_experts={n_e}. "
            f"Train with a CLMConfig(n_experts=2, n_trunk_layers=1) preset."
        )
    if n_l is not None and n_l != 1:
        raise ValueError(
            f"core/clm_decode.hexa is FIXED to 1 trunk layer; "
            f"cfg.n_trunk_layers={n_l}. Train with n_trunk_layers=1."
        )


def serialize_v2(state_dict_or_ckpt, cfg, out_path: str) -> str:
    """Pack a CLMConvMoE (E=2 / 1-trunk) state_dict to a CLM\\x01 v0.2 .clm that
    core/clm_decode.hexa loads. Returns out_path.

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
                 out_path: str) -> str:
    """Pack a GENERAL CLMConvMoE(n_trunk_layers=L, n_experts=E, d, K) to a
    CLM\\x01 v0.3 .clm that core/clm_decode.hexa loads.

    v0.3 == v0.2 byte grammar, generalized block/ext counts (see the v0.3 note
    above). At L=1,E=2 the output is BYTE-IDENTICAL to serialize_v2 (verified by
    the round-trip gate). d, K, V are read from the weight shapes — no width
    hardcode. Returns out_path.
    """
    if np is None:
        raise RuntimeError("numpy is required for serialize_v3")
    L, E = int(n_trunk_layers), int(n_experts)
    if L < 1 or E < 1:
        raise ValueError(f"need L>=1 and E>=1, got L={L} E={E}")
    sd = _resolve_state_dict(state_dict_or_ckpt, None)
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

    # H_9643: tell _conv_w_to_2d which convs are grouped. Derived from the state dict itself
    # (the bridge exists iff the faction lane is on) — never guessed from a shape.
    K_fac = 0
    for k in sd:
        if k.endswith("faction_bridge.gate"):
            g = np.asarray(sd[k]).reshape(-1)
            wb = None
            for k2 in sd:
                if k2.endswith("faction_bridge.proj.weight"):
                    wb = np.asarray(sd[k2])
            if wb is not None:
                d_model = int(g.shape[0])
                for k3 in sd:
                    if k3.endswith("trunk.0.conv.conv.weight"):
                        w3 = np.asarray(sd[k3])
                        K_fac = int(d_model // w3.shape[1]) if w3.ndim == 3 and w3.shape[1] else 0
            break
    _FACTION_GROUPS["n"] = K_fac

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


def pack_faction_section(sd: Dict[str, Any], n_factions: int) -> bytearray:
    """H_9643 CLMF — the faction lane's trailer. Absent => K=0 (OFF) and the decoder's
    golden path is untouched, exactly like a .clm with no CLMB.

    LAYOUT (appended AFTER the CLMX ext arrays, same self-describing style):
      "CLMF"        (67,76,77,70)
      n_factions    u32 LE
      lam           float32 LE     — the bridge scale. `evaluate` overrides this to run the
                                     debate ON/OFF ablation WITHOUT touching a weight.
      gate          u32 count + count float32 LE   — per-channel pre-sigmoid gate (d)
      W_b           u32 count + count float32 LE   — 1x1 bridge conv (d*d, row-major cout,cin)
      b_b           u32 count + count float32 LE   — bridge bias (d)

    W_b is written UNMASKED; the mask is structural (M_cross zeroes the within-faction block)
    and is re-derived from n_factions at load. Writing the masked matrix would make the zeros
    indistinguishable from learned zeros — the reader must know WHY they are zero.
    """
    blob = bytearray()
    if not n_factions or n_factions <= 0:
        return blob
    blob += CLMF
    blob += struct.pack("<I", int(n_factions))
    lam = _bget(sd, ["faction_bridge.lam", "base.faction_bridge.lam"])
    blob += struct.pack("<f", float(np.asarray(lam).reshape(-1)[0]))
    for names in (["faction_bridge.gate", "base.faction_bridge.gate"],
                  ["faction_bridge.proj.weight", "base.faction_bridge.proj.weight"],
                  ["faction_bridge.proj.bias", "base.faction_bridge.proj.bias"]):
        blob += _pack_ext(_bget(sd, names))
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
    .clm that core/clm_decode.hexa loads.

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


def serialize(state_dict_or_ckpt, n_trunk_layers: int, n_experts: int,
              out_path: str) -> str:
    """Unified entry: routes to serialize_v3 (general). For L=1,E=2 the v3 path
    is byte-identical to serialize_v2, so this is the single serializer for ANY
    (L,E,d). cfg-free — caller states (L,E) explicitly."""
    return serialize_v3(state_dict_or_ckpt, n_trunk_layers, n_experts, out_path)


if __name__ == "__main__":  # pragma: no cover
    import argparse, json, os, sys
    ap = argparse.ArgumentParser(description="torch CLMConvMoE -> CLM\\x01 v0.2 .clm")
    ap.add_argument("--ckpt", required=True, help="torch state_dict ckpt path")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-experts", type=int, default=2)
    ap.add_argument("--n-trunk-layers", type=int, default=1)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--kernel-size", type=int, default=3)
    a = ap.parse_args()
    _HERE = os.path.dirname(os.path.abspath(__file__))
    if _HERE not in sys.path:
        sys.path.insert(0, _HERE)
    from model import CLMConfig  # noqa
    cfg = CLMConfig(n_experts=a.n_experts, n_trunk_layers=a.n_trunk_layers,
                    d_model=a.d_model, kernel_size=a.kernel_size)
    p = serialize_v2(a.ckpt, cfg, a.out)
    print(json.dumps({"out": p, "bytes": os.path.getsize(p)}))
