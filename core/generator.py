# ==========================================================================
# ⛔ ENGINE-INTERNAL / DEPRECATED py-MIRROR — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 cli/ 단일진입만: anima eval | train | serialize
#   (canonical = hexa core/*.hexa 단일 SSOT; py 미러는 2026-06-28 폐기, DIRECTIONAL).
# 이 파일을 `python3 core/generator.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ generator.py 직접 실행 금지 — cli/ 단일진입(anima eval/train/serialize, canonical=hexa) 경유. #2603")

"""core/generator.py — PY PRODUCTION ENGINE: byte-faithful 1:1 mirror of the
L3 MOUTH-DISPATCH surface of core/generator.hexa.

Per CLAUDE.md a_two_production_mirror / a_core_engine_map: hexa + py are TWO
co-equal production engines kept at byte-parity. generator.hexa is the SINGLE L3
typed mouth slot — it sniffs a ckpt header and dispatches to ONE of two mouth
ARCHITECTURES (conv .clm via clm_decode, ByteGPT .bin via bytegpt_decode). This
module is the py mirror of that dispatcher; it routes to the already-parity-proven
core/clm_decode.py and core/bytegpt_decode.py (themselves 1:1 ports of their
.hexa SSOTs). NO torch in the path — stdlib + numpy (via the decoders) only.

Scope: this mirrors generator.hexa's PUBLIC dispatch surface (a_core_engine_map):
  gen_mouth_kind      generator.hexa:628  header-sniff CLM\\x01 / 5xu32 / unknown
  gen_auto_backend    generator.hexa:641  -> gen_bytegpt_backend | gen_clm_backend
  gen_auto_chat       generator.hexa:684  -> gen_bytegpt_chat    | gen_clm_chat
  gen_auto_ideate     generator.hexa:750  -> gen_bytegpt_ideate  | gen_clm_ideate
plus the per-architecture single entries each dispatcher picks between:
  gen_null_backend    :74    gen_clm_backend  :101   gen_bytegpt_backend :175
  gen_clm_chat        :599   gen_bytegpt_chat :664
  gen_clm_ideate      :697   gen_clm_ideate_W :713   gen_bytegpt_ideate  :728
and the header helpers they reuse:
  _gen_is_bytegpt     :148   _gen_clm_probe_header :224   _gen_rd_u32 :792

NOTE the sniff is reproduced VERBATIM from generator.hexa (NOT the looser ranges
in bytegpt_decode.bg_is_bytegpt): generator.hexa::_gen_is_bytegpt requires
vocab==256, n_layer in 1..64, n_head divides d, block in 1..8192 — these tighter
bounds are the dispatcher's actual edge-case behavior and must be mirrored exactly.

The VERDICT path stays engine-native (hexa); this is the parity-proven py mirror.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import clm_decode as _clm        # core/clm_decode.py — ConvMoE .clm mouth
import bytegpt_decode as _bg     # core/bytegpt_decode.py — ByteGPT .bin mouth


# ════════════════════════════════════════════════════════════════════════
# header helpers — 1:1 from generator.hexa
# ════════════════════════════════════════════════════════════════════════

def _gen_rd_u32(rb, off):
    """generator.hexa:792 _gen_rd_u32 — little-endian u32 from a byte buffer."""
    return rb[off] + rb[off + 1] * 0x100 + rb[off + 2] * 0x10000 + rb[off + 3] * 0x1000000


def _gen_path_is_file(p):
    """generator.hexa:245 _gen_path_is_file — empty path -> false, else isfile."""
    if len(p) == 0:
        return False
    return os.path.isfile(p)


def _gen_is_bytegpt(p):
    """generator.hexa:148 _gen_is_bytegpt — true iff `p` is a ByteGPT flat binary,
    NOT a .clm. Reject the CLM\\x01 magic; then require a SANE 5xu32 header:
    vocab==256, n_layer in 1..64, n_head divides d, block in 1..8192. Edge-safe
    (missing/short file -> false). Bounds are tighter than bytegpt_decode.bg_is_bytegpt;
    these are the dispatcher's verbatim discriminator (mirror exactly)."""
    if len(p) == 0:
        return False
    if not _gen_path_is_file(p):
        return False
    try:
        rb = open(p, 'rb').read()
    except Exception:
        return False
    if len(rb) < 20:
        return False
    # reject the .clm magic outright (CLM\x01 = 67,76,77,1)
    if rb[0] == 67 and rb[1] == 76 and rb[2] == 77 and rb[3] == 1:
        return False
    vocab = _gen_rd_u32(rb, 0)
    d = _gen_rd_u32(rb, 4)
    nlay = _gen_rd_u32(rb, 8)
    nh = _gen_rd_u32(rb, 12)
    block = _gen_rd_u32(rb, 16)
    if vocab != 256:
        return False
    if nlay < 1 or nlay > 64:
        return False
    if nh < 1 or d < 1:
        return False
    if (d // nh) * nh != d:       # n_head must divide d
        return False
    if block < 1 or block > 8192:
        return False
    return True


def _gen_clm_probe_header(p):
    """generator.hexa:224 _gen_clm_probe_header — verify the CLM\\x01 header.
    Returns {exists, valid, nblocks}. Edge-safe: missing/empty/truncated -> valid=False."""
    if len(p) == 0:
        return {"exists": False, "valid": False, "nblocks": 0}
    if not _gen_path_is_file(p):
        return {"exists": False, "valid": False, "nblocks": 0}
    rb = open(p, 'rb').read()
    # need at least MAGIC(4) + nblocks(1) = 5 bytes
    if len(rb) < 5:
        return {"exists": True, "valid": False, "nblocks": 0}
    magic_ok = rb[0] == 67 and rb[1] == 76 and rb[2] == 77 and rb[3] == 1
    if not magic_ok:
        return {"exists": True, "valid": False, "nblocks": 0}
    nblocks = rb[4]
    return {"exists": True, "valid": True, "nblocks": nblocks}


# ════════════════════════════════════════════════════════════════════════
# §1 backend constructors (the pluggable "vtable" records)
# ════════════════════════════════════════════════════════════════════════

def gen_null_backend():
    """generator.hexa:74 gen_null_backend — always-ready deterministic placeholder."""
    return {"kind": "null", "loaded": True, "ckpt": ""}


def gen_clm_backend(ckpt_path):
    """generator.hexa:101 gen_clm_backend — parse the .clm header at the single L3
    entry; surface loaded (header admit) + decodable (v0.2 CLMX trailer present)."""
    probe = _gen_clm_probe_header(ckpt_path)
    exists = probe["exists"]
    valid = probe["valid"]
    nblk = probe["nblocks"]
    loaded = valid
    decodable = valid and _clm.clm_decodable(ckpt_path)
    if not exists:
        reason = "no ckpt at path"
    elif not valid:
        reason = "file present but not a valid .clm (bad CLM\\x01 magic)"
    else:
        reason = ("valid .clm admitted + LOADED (magic+structure OK, nblocks="
                  + str(nblk)
                  + "); decode forward LANDED + descends CORE-mounted at d=768 (loaded=valid)")
    return {"kind": "clm", "loaded": loaded, "decodable": decodable, "valid": valid,
            "ckpt": ckpt_path, "ckpt_exists": exists, "nblocks": nblk, "reason": reason}


def gen_bytegpt_backend(ckpt_path):
    """generator.hexa:175 gen_bytegpt_backend — parse the 5xu32 ByteGPT header at the
    single L3 entry. ByteGPT-format file => valid+loaded+decodable=True; else honest
    rejection (valid=False) so generate() falls through to null (no garbage)."""
    if not _gen_is_bytegpt(ckpt_path):
        exists = _gen_path_is_file(ckpt_path)
        reason = ("no ckpt at path" if not exists
                  else "file present but not a ByteGPT flat binary (bad 5xu32 header)")
        return {"kind": "bytegpt", "loaded": False, "decodable": False, "valid": False,
                "ckpt": ckpt_path, "ckpt_exists": exists, "nlayer": 0, "d": 0, "reason": reason}
    rb = open(ckpt_path, 'rb').read()
    vocab = _gen_rd_u32(rb, 0); d = _gen_rd_u32(rb, 4)
    nlay = _gen_rd_u32(rb, 8); nh = _gen_rd_u32(rb, 12)
    block = _gen_rd_u32(rb, 16)
    reason = ("valid ByteGPT flat binary admitted + LOADED (vocab=" + str(vocab)
              + " d=" + str(d) + " n_layer=" + str(nlay) + " n_head=" + str(nh)
              + " block=" + str(block) + "); decode forward = full-24-layer BYTE-EXACT-argmax "
              + "parity with torch ByteGPT (H_1157 R1, G1 inherited)")
    return {"kind": "bytegpt", "loaded": True, "decodable": True, "valid": True,
            "ckpt": ckpt_path, "ckpt_exists": True, "vocab": vocab, "d": d,
            "nlayer": nlay, "nhead": nh, "block": block, "reason": reason}


# ════════════════════════════════════════════════════════════════════════
# MOUTH-TYPE DISPATCHER — generator.hexa §"MOUTH-TYPE DISPATCHER" (609+)
# ════════════════════════════════════════════════════════════════════════

def gen_mouth_kind(ckpt_path):
    """generator.hexa:628 gen_mouth_kind — sniff a ckpt and report the mouth
    ARCHITECTURE: "bytegpt" | "clm" | "unknown". ByteGPT checked FIRST (its magic
    is the ABSENCE of CLM\\x01 + a sane 5xu32 header, strictly disjoint from a .clm)."""
    if _gen_is_bytegpt(ckpt_path):
        return "bytegpt"
    probe = _gen_clm_probe_header(ckpt_path)
    if probe["valid"]:
        return "clm"
    return "unknown"


def gen_auto_backend(ckpt_path):
    """generator.hexa:641 gen_auto_backend — THE mouth dispatcher. Sniff and return
    the right backend record; "clm"/"unknown" both go to gen_clm_backend (it self-
    reports valid=False for a non-.clm/absent file -> generate() falls through to null)."""
    kind = gen_mouth_kind(ckpt_path)
    if kind == "bytegpt":
        return gen_bytegpt_backend(ckpt_path)
    return gen_clm_backend(ckpt_path)


# ════════════════════════════════════════════════════════════════════════
# CHAT entries — greedy byte-continuation of a composed dialogue seed
# ════════════════════════════════════════════════════════════════════════

def gen_clm_chat(ckpt_path, seed, max_new):
    """generator.hexa:599 gen_clm_chat — thin caller of the ONE .clm decode mouth
    (clm_decode_argmax). ok=False with reason for a v0.1 (non-decodable) file."""
    if not _clm.clm_decodable(ckpt_path):
        return {"ok": False, "text": "",
                "reason": "ckpt not v0.2-decodable (no CLMX trailer; embed/GN absent)"}
    r = _clm.clm_decode_argmax(ckpt_path, seed, max_new)
    return {"ok": r["ok"], "text": r["text"],
            "reason": "decoded via clm_decode_argmax (CLMConvMoE int4 forward)"}


def gen_bytegpt_chat(ckpt_path, seed, max_new):
    """generator.hexa:664 gen_bytegpt_chat — thin caller of the ONE ByteGPT decode
    mouth (bytegpt_decode_argmax_ranged, OOM-safe ranged load). seed string -> byte
    ids (vocab256 byte LM), exactly as the hexa builds sids via ord(substring(...))."""
    if gen_mouth_kind(ckpt_path) != "bytegpt":
        return {"ok": False, "text": "",
                "reason": "ckpt not a ByteGPT flat binary (bad 5xu32 [256,d,L,H,block] header)"}
    sids = list(seed.encode('utf-8', 'surrogateescape'))
    r = _bg.bytegpt_decode_argmax_ranged(ckpt_path, sids, max_new)
    return {"ok": r["ok"], "text": r["text"],
            "reason": "decoded via bytegpt_decode_argmax_ranged (24-layer GPT-2-class byte forward)"}


def gen_auto_chat(ckpt_path, seed, max_new):
    """generator.hexa:684 gen_auto_chat — mouth-dispatched chat. Same {ok,text,reason}
    shape for both mouths so the chat loop is mouth-agnostic."""
    if gen_mouth_kind(ckpt_path) == "bytegpt":
        return gen_bytegpt_chat(ckpt_path, seed, max_new)
    return gen_clm_chat(ckpt_path, seed, max_new)


# ════════════════════════════════════════════════════════════════════════
# IDEATE entries — the seeded-sampling siblings (G6 best-of-K source)
# ════════════════════════════════════════════════════════════════════════

def gen_clm_ideate(ckpt_path, seed, max_new, top_k, temp, seed_rng):
    """generator.hexa:697 gen_clm_ideate — seeded top-k sampler on the .clm mouth
    (clm_decode_topk_sampled). HARD-BOUNDED by max_new."""
    if not _clm.clm_decodable(ckpt_path):
        return {"ok": False, "text": "",
                "reason": "ckpt not v0.2-decodable (no CLMX trailer; embed/GN absent)"}
    r = _clm.clm_decode_topk_sampled(ckpt_path, seed, max_new, top_k, temp, seed_rng)
    return {"ok": r["ok"], "text": r["text"],
            "reason": "ideated via clm_decode_topk_sampled (seeded top-k, best-of-K source)"}


def gen_clm_ideate_W(W, seed, max_new, top_k, temp, seed_rng):
    """generator.hexa:713 gen_clm_ideate_W — SAME mouth off a PRE-LOADED weight map
    (clm_load_weights) so a multi-decode driver loads the 303M ConvMoE ONCE."""
    r = _clm.clm_decode_topk_sampled_W(W, seed, max_new, top_k, temp, seed_rng)
    return {"ok": r["ok"], "text": r["text"],
            "reason": "ideated via clm_decode_topk_sampled_W (loaded-W, seeded top-k)"}


def gen_bytegpt_ideate(ckpt_path, seed, max_new, top_k, temp, seed_rng):
    """generator.hexa:728 gen_bytegpt_ideate — seeded top-k sampler on the ByteGPT
    mouth (bytegpt_decode_topk_sampled_ranged, OOM-safe). HARD-BOUNDED by max_new."""
    if gen_mouth_kind(ckpt_path) != "bytegpt":
        return {"ok": False, "text": "",
                "reason": "ckpt not a ByteGPT flat binary (bad 5xu32 [256,d,L,H,block] header)"}
    sids = list(seed.encode('utf-8', 'surrogateescape'))
    r = _bg.bytegpt_decode_topk_sampled_ranged(ckpt_path, sids, max_new, top_k, temp, seed_rng)
    return {"ok": r["ok"], "text": r["text"],
            "reason": "ideated via bytegpt_decode_topk_sampled_ranged (seeded top-k, OOM-safe)"}


def gen_auto_ideate(ckpt_path, seed, max_new, top_k, temp, seed_rng):
    """generator.hexa:750 gen_auto_ideate — mouth-dispatched ideate (the seeded-sampling
    sibling of gen_auto_chat). Same {ok,text,reason} contract for both mouths so the
    G0-G6 gate scorers run on EITHER mouth via this ONE typed entry (mouth-agnostic)."""
    if gen_mouth_kind(ckpt_path) == "bytegpt":
        return gen_bytegpt_ideate(ckpt_path, seed, max_new, top_k, temp, seed_rng)
    return gen_clm_ideate(ckpt_path, seed, max_new, top_k, temp, seed_rng)


# ════════════════════════════════════════════════════════════════════════
# CLI — for the byte-parity harness (mirror of a hexa main calling the same)
# ════════════════════════════════════════════════════════════════════════

def _main(argv):
    if len(argv) < 2:
        print("usage: generator.py <cmd> ...", file=sys.stderr)
        return 2
    cmd = argv[1]
    if cmd == "kind":
        print("KIND:" + gen_mouth_kind(argv[2]))
        return 0
    if cmd == "ideate":
        # ideate <ckpt> <seed> <gen> <top_k> <temp> <seed_rng>
        ck, seed, gen = argv[2], argv[3], int(argv[4])
        top_k = int(argv[5]); temp = float(argv[6]); rng = int(argv[7])
        r = gen_auto_ideate(ck, seed, gen, top_k, temp, rng)
        sys.stdout.buffer.write(b"KIND:" + gen_mouth_kind(ck).encode() + b"\n")
        sys.stdout.buffer.write(b"OK:" + (b"true" if r["ok"] else b"false") + b"\n")
        sys.stdout.buffer.write(b"TEXT:" + r["text"].encode('utf-8', 'surrogateescape') + b"\n")
        return 0
    if cmd == "chat":
        ck, seed, gen = argv[2], argv[3], int(argv[4])
        r = gen_auto_chat(ck, seed, gen)
        sys.stdout.buffer.write(b"KIND:" + gen_mouth_kind(ck).encode() + b"\n")
        sys.stdout.buffer.write(b"OK:" + (b"true" if r["ok"] else b"false") + b"\n")
        sys.stdout.buffer.write(b"TEXT:" + r["text"].encode('utf-8', 'surrogateescape') + b"\n")
        return 0
    print("unknown cmd", cmd, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
