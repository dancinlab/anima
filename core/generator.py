# ==========================================================================
# ⛔ ENGINE-INTERNAL — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 `anima-py` 단일진입만 사용한다.
# 이 파일을 `python3 core/generator.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ generator.py 직접 실행 금지 — canonical `anima-py` 경유. #2603")

"""core/generator.py — canonical Python L3 mouth dispatcher.

The dispatcher sniffs checkpoint headers and selects one of two mouth
architectures: Conv ``.clm`` or ByteGPT ``.bin``. It routes both through
``core/decode.py`` and uses only the standard library plus NumPy.

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
in decode.bg_is_bytegpt): generator.hexa::_gen_is_bytegpt requires
vocab==256, n_layer in 1..64, n_head divides d, block in 1..8192 — these tighter
bounds are the dispatcher's actual edge-case behavior and must be mirrored exactly.

The installed ``anima-py`` command is the sole verdict entry.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import decode as _clm        # core/decode.py (unified) — ConvMoE .clm mouth API
import decode as _bg         # same module; both aliases resolve the union public API (ByteGPT .bin mouth)


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
    (missing/short file -> false). Bounds are tighter than decode.bg_is_bytegpt;
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

_CHAT_TURN_STOP_MARKERS = (
    "\nuser:", "\nUser:", "\n사용자:", "\n<|user|>", "\n<usr>",
)


def gen_chat_turn_text(text, stop_markers=None):
    """Return only the assistant turn from a raw byte-mouth continuation.

    A dialogue-trained byte model naturally continues with the next user role because
    vocab 256 has no dedicated EOS token.  Chat must stop at that role boundary; emitting
    the synthetic next user turn is a runtime framing bug, not additional model content.
    The raw continuation remains available to evaluators through ``raw_text``.
    """
    if not isinstance(text, str):
        raise TypeError("chat continuation must be str")
    markers = _CHAT_TURN_STOP_MARKERS if stop_markers is None else tuple(stop_markers)
    stop = len(text)
    matched = ""
    for marker in markers:
        if not isinstance(marker, str) or not marker:
            raise ValueError("chat stop markers must be non-empty strings")
        pos = text.find(marker)
        if 0 <= pos < stop:
            stop = pos
            matched = marker
    return {"text": text[:stop].strip(), "stop_marker": matched,
            "stopped": bool(matched), "raw_text": text}


def _chat_turn_result(result):
    if not result.get("ok"):
        return result
    turn = gen_chat_turn_text(str(result.get("text", "")))
    out = dict(result)
    out.update(turn)
    return out

def gen_clm_chat(ckpt_path, seed, max_new):
    """generator.hexa:599 gen_clm_chat — thin caller of the ONE .clm decode mouth
    (clm_decode_argmax). ok=False with reason for a v0.1 (non-decodable) file."""
    if not _clm.clm_decodable(ckpt_path):
        return {"ok": False, "text": "",
                "reason": "ckpt not v0.2-decodable (no CLMX trailer; embed/GN absent)"}
    r = _clm.clm_decode_argmax(ckpt_path, seed, max_new)
    return _chat_turn_result({
        "ok": r["ok"], "text": r["text"],
        "reason": "decoded via clm_decode_argmax (CLMConvMoE int4 forward)",
    })


def gen_bytegpt_chat(ckpt_path, seed, max_new):
    """generator.hexa:664 gen_bytegpt_chat — thin caller of the ONE ByteGPT decode
    mouth (bytegpt_decode_argmax_ranged, OOM-safe ranged load). seed string -> byte
    ids (vocab256 byte LM), exactly as the hexa builds sids via ord(substring(...))."""
    if gen_mouth_kind(ckpt_path) != "bytegpt":
        return {"ok": False, "text": "",
                "reason": "ckpt not a ByteGPT flat binary (bad 5xu32 [256,d,L,H,block] header)"}
    sids = list(seed.encode('utf-8', 'surrogateescape'))
    r = _bg.bytegpt_decode_argmax_ranged(ckpt_path, sids, max_new)
    return _chat_turn_result({
        "ok": r["ok"], "text": r["text"],
        "reason": "decoded via bytegpt_decode_argmax_ranged (24-layer GPT-2-class byte forward)",
    })


def gen_auto_chat(ckpt_path, seed, max_new):
    """generator.hexa:684 gen_auto_chat — mouth-dispatched chat. Same {ok,text,reason}
    shape for both mouths so the chat loop is mouth-agnostic."""
    if gen_mouth_kind(ckpt_path) == "bytegpt":
        return gen_bytegpt_chat(ckpt_path, seed, max_new)
    return gen_clm_chat(ckpt_path, seed, max_new)


# ════════════════════════════════════════════════════════════════════════
# IDEATE entries — the seeded-sampling siblings (ρ·fan best-of-K source · ideation · former G6)
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


def gen_penult_pooled_W(W, seed):
    """generator.hexa gen_penult_pooled_W — H_9257 lane-23b self-grounding read (py 2-production
    twin). The mounted 303M's REAL penultimate pooled rep for `seed`, off a PRE-LOADED weight map.
    Thin READ-ONLY wrapper over decode.clm_penult_pooled_W — NOT a 2nd decode path / NOT a mouth
    (emits no bytes); the runtime self-continuity lane taps the trunk penult to ground self_drift_exp
    in real experienced content. self⊥mouth: the returned vector never feeds emit."""
    return _clm.clm_penult_pooled_W(W, seed)


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
    ρ-AXON reach scorers (former G0-G6) run on EITHER mouth via this ONE typed entry (mouth-agnostic)."""
    if gen_mouth_kind(ckpt_path) == "bytegpt":
        return gen_bytegpt_ideate(ckpt_path, seed, max_new, top_k, temp, seed_rng)
    return gen_clm_ideate(ckpt_path, seed, max_new, top_k, temp, seed_rng)


# ════════════════════════════════════════════════════════════════════════
# §2 substrate_ctx helpers + §DELIBERATE stack — 1:1 from generator.hexa
# (P5 py-selfimpl: the L3 deliberation stack the daemon emit path drives via
#  brain_emit_deliberate → generate_deliberate → generate_deliberate_consult.)
# ════════════════════════════════════════════════════════════════════════

def _gen_g_float(m, k):
    """generator.hexa:414 _gen_g_float — Map field → float, void/absent → 0.0."""
    v = m.get(k)
    if v is None:
        return 0.0
    if str(v) == "void":
        return 0.0
    return float(v)


def _gen_g_int(m, k):
    """generator.hexa:419 _gen_g_int — Map field → int, void/absent → 0."""
    v = m.get(k)
    if v is None:
        return 0
    if str(v) == "void":
        return 0
    return int(v)


def _gen_g_string(m, k):
    """generator.hexa:424 _gen_g_string — Map field → string, void/absent → ""."""
    v = m.get(k)
    if v is None:
        return ""
    if str(v) == "void":
        return ""
    return str(v)


def _gen_fmt4(x):
    """generator.hexa:2765 _gen_fmt4 — format_float(x, 4); hexa format_float(x,4)
    ≡ py f"{x:.4f}" (kosmos_io.py K1 carve-out; parity-verified in the oracle)."""
    return "%.4f" % x


def gen_ctx_from_decision(decision):
    """generator.hexa:264 gen_ctx_from_decision — adapt a brain_decide() record into
    the substrate_ctx the generator consumes (decouples generate() from brain's shape)."""
    return {
        "phi": _gen_g_float(decision, "phi"),
        "phase": _gen_g_string(decision, "phase"),
        "tier": _gen_g_int(decision, "tier"),
        "tier_name": _gen_g_string(decision, "tier_name"),
        "motivation": _gen_g_float(decision, "motivation"),
    }


def _gc_clip01(x):
    """generator.hexa:281 _gc_clip01 — [0,1] clip."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def gen_ctx_from_decision_conflicted(decision, conflict_t):
    """generator.hexa:282 gen_ctx_from_decision_conflicted — carry a per-tick
    deliberation depth k = 1 + round(clip01(conflict_t)·KMAX) into the decode ctx
    (KMAX=3). low conflict → k=1 (argmax, bytes unchanged); high → k>1 (best-of-K)."""
    ctx = gen_ctx_from_decision(decision)
    kmax = 3
    k = 1 + int(_gc_clip01(conflict_t) * float(kmax) + 0.5)
    if k < 1:
        k = 1
    if k > 1 + kmax:
        k = 1 + kmax
    ctx["deliberation_k"] = k
    return ctx


def _gen_text_to_bytes(s):
    """generator.hexa:293 _gen_text_to_bytes — text → byte-int list (surrogateescape
    mirrors the hexa byte_at loop, same convention as gen_bytegpt_chat's sids)."""
    return list(s.encode('utf-8', 'surrogateescape'))


def gen_clm_decode_deliberated(ckpt, seed, gen, k, base_seed):
    """generator.hexa:306 gen_clm_decode_deliberated — H_9102 efferent seam. k=1 ⇒
    argmax (byte-identical). k>1 ⇒ decode k sampled candidates at det rng offsets and
    return the CONFLICT-MINIMIZING (lowest clm_decode_ce) one. Selection metric = the
    engine-measured CE (P4-decode: _clm.clm_decode_ce)."""
    r1 = _clm.clm_decode_argmax(ckpt, seed, gen)
    t1 = str(r1["text"]) if r1["ok"] else ""
    ce1m = _clm.clm_decode_ce(ckpt, _gen_text_to_bytes(seed + t1))
    ce1 = float(ce1m["ce"])
    if k <= 1:
        return {"text": t1, "k": 1, "ce_sel": ce1, "ce_k1": ce1}
    offsets = [0, 101, 202, 303]
    best_text = ""
    best_ce = 1000000.0
    got = False
    kk = 4 if k > 4 else k
    oi = 0
    while oi < kk:
        rs = _clm.clm_decode_topk_sampled(ckpt, seed, gen, 8, 0.7, base_seed + offsets[oi])
        if rs["ok"]:
            ts = str(rs["text"])
            cem = _clm.clm_decode_ce(ckpt, _gen_text_to_bytes(seed + ts))
            ce = float(cem["ce"])
            if (not got) or ce < best_ce:
                best_ce = ce
                best_text = ts
                got = True
        oi = oi + 1
    if not got:
        return {"text": t1, "k": 1, "ce_sel": ce1, "ce_k1": ce1}
    return {"text": best_text, "k": kk, "ce_sel": best_ce, "ce_k1": ce1}


# NOTE (true-gap triage): generator.hexa:357 gen_fm_rerank (forward-model best-of-K
# referential-game rerank, Option C / H_9118) is DEFERRED from the py twin. It is
# EVAL-PATH-ONLY heavy forge glue — its ONLY caller is state/9119_fm_b50_measure/
# fm_b50.hexa (a research harness), never the chat/emit path (brain_emit_deliberate →
# generate_deliberate never calls it). It needs the forge load-once scratch surface
# (clm_load_W · clm_scratch_new_pub · clm_ce_seq_W · clm_scratch_free_pub ·
# clm_weights_free_pub) that numpy does not need for chat. Same rationale as the
# deferred smoke faculties: not a chat dependency ⇒ py legitimately defers it.


# ── §3 anchor READ wiring (kosmos_io) ────────────────────────────────────────

def generator_read_anchors(dir_path):
    """generator.hexa:439 generator_read_anchors — read .kosmos anchors from a dir so
    brain_decide can pass real substrate memory into generate(). Thin wrapper over
    kosmos_io.load_anchors. FAITHFUL-BEHAVIOR PORT: the hexa uses exec("test -d ...")
    to gate on dir existence; the py twin uses a pure os.path.isdir (no shell —
    a_no_archive_import / py-channel self-containment). [] for a missing dir."""
    from kosmos_io import load_anchors
    if len(dir_path) == 0:
        return []
    if not os.path.isdir(dir_path):
        return []
    return load_anchors(dir_path)


# ── §4 the generator interface — generate() ──────────────────────────────────

def generate(backend, substrate_ctx, emit_decision, anchors, mouth=None):
    """generator.hexa:469 generate — the single L3 entry. BACKEND-AGNOSTIC dispatch.
    SILENT (emit_decision False) ⇒ emitted=False ∧ text="" (p5: never fabricate). EMIT
    ⇒ try the backend, fall THROUGH to null if not loaded/decodable (no garbage).

    `mouth` (H_9325 DO-MOUTH · default None ⇒ byte-identical to the greedy production
    path) = {"temp": float, "top_k": int, "seed_rng": int}. It REVEALS the substrate's
    own byte-posterior instead of OVERWRITING the emit decision: the gate
    (brain_decide_anchored → should_emit) never sees it, so every emit still stands on
    real tension (p5). It only replaces the argmax ROUNDING of the mouth with the
    substrate's own distribution at T=1.0 — the one non-arbitrary temperature.
    The SILENT branch below is untouched: no `mouth` value can ever fabricate speech."""
    if not emit_decision:
        return {"emitted": False, "backend": str(backend["kind"]), "text": "", "fellback": False}
    kind = str(backend["kind"])
    loaded = bool(backend["loaded"])
    if kind == "null":
        return {"emitted": True, "backend": "null",
                "text": _gen_null_text(substrate_ctx, anchors), "fellback": False}
    if kind == "clm":
        decodable = bool(backend["decodable"])
        if loaded and decodable:
            text = _gen_clm_decode(backend, substrate_ctx, anchors, mouth)
            return {"emitted": True, "backend": "clm", "text": text, "fellback": False}
        return {"emitted": True, "backend": "null",
                "text": _gen_null_text(substrate_ctx, anchors), "fellback": True}
    if kind == "bytegpt":
        decodable = bool(backend["decodable"])
        if loaded and decodable:
            return {"emitted": True, "backend": "bytegpt",
                    "text": _gen_bytegpt_decode(backend, substrate_ctx, anchors), "fellback": False}
        return {"emitted": True, "backend": "null",
                "text": _gen_null_text(substrate_ctx, anchors), "fellback": True}
    return {"emitted": True, "backend": "null",
            "text": _gen_null_text(substrate_ctx, anchors), "fellback": True}


def _gen_null_text(ctx, anchors):
    """generator.hexa:559 _gen_null_text — deterministic placeholder from substrate
    numerics + anchor memory ONLY (NO chatbot reply / persona / instruction). p7:
    reproducible byte-for-byte for the same input."""
    phase = _gen_g_string(ctx, "phase")
    tier = _gen_g_string(ctx, "tier_name")
    phi = _gen_g_float(ctx, "phi")
    motiv = _gen_g_float(ctx, "motivation")
    n_anchor = len(anchors)
    s = "[null-gen]"
    s = s + " phase=" + phase
    s = s + " tier=" + tier
    s = s + " phi=" + _gen_fmt4(phi)
    s = s + " motiv=" + _gen_fmt4(motiv)
    s = s + " anchors=" + str(n_anchor)
    if n_anchor > 0:
        last = anchors[n_anchor - 1]
        s = s + " last_anchor=" + str(last["name"])
    return s


def _gen_clm_decode(backend, ctx, anchors, mouth=None):
    """generator.hexa:615 _gen_clm_decode — REAL substrate-anchored .clm content. The
    model emits its OWN bytes: substrate-derived seed (phase word + most-recent anchor
    text, NO user prompt/persona — a_substrate_native_speak). anchors present ⇒
    engine-side grounded retrieve-then-copy (_clm.clm_decode_grounded, P4-decode).
    deliberation_k>1 ⇒ best-of-K. else argmax. Honest fallthrough to _gen_null_text."""
    ckpt = str(backend["ckpt"])
    phase = _gen_g_string(ctx, "phase")
    seed = phase + " "
    n = len(anchors)
    if n > 0:
        a = anchors[n - 1]
        seed = seed + _gen_anchor_text(a)
    if n > 0:
        # H_9328 · THIS is the daemon's real mouth (anchors are always present in a live
        # session). Measured: grounded=0 / lm=80 — the anchor-copy never fires at l_min=8,
        # so every byte falls through to the SAME argmax rounding. `mouth` is threaded in so
        # the REVEAL lands where the engine actually generates; the anchor-copy step itself
        # is never sampled (that path is the p5 anti-fabrication guarantee).
        texts = _gen_anchor_texts(anchors)
        rg = _clm.clm_decode_grounded(ckpt, seed, 80, texts, 8, mouth)
        if rg["ok"]:
            return str(rg["text"])
        return _gen_null_text(ctx, anchors)
    dk = _gen_g_int(ctx, "deliberation_k")
    if dk > 1:
        dd = gen_clm_decode_deliberated(ckpt, seed, 80, dk, 20260703)
        return str(dd["text"])
    if mouth is not None and float(mouth["temp"]) > 0.0:
        # H_9325 DO-MOUTH — REVEAL the substrate's own posterior instead of rounding it
        # to argmax. Reached ONLY on an emit the gate already approved on real tension.
        r = _clm.clm_decode_topk_sampled(ckpt, seed, 80, int(mouth["top_k"]),
                                         float(mouth["temp"]), int(mouth["seed_rng"]))
    else:
        r = _clm.clm_decode_argmax(ckpt, seed, 80)
    if not r["ok"]:
        return _gen_null_text(ctx, anchors)
    return str(r["text"])


def _gen_bytegpt_decode(backend, ctx, anchors):
    """generator.hexa:666 _gen_bytegpt_decode — ByteGPT analog of _gen_clm_decode.
    Same substrate seed + anti-fabrication grounded-copy contract (_bg.bytegpt_decode_
    grounded, P4-decode). No anchors ⇒ plain ByteGPT greedy continuation."""
    ckpt = str(backend["ckpt"])
    phase = _gen_g_string(ctx, "phase")
    seed = phase + " "
    n = len(anchors)
    if n > 0:
        a = anchors[n - 1]
        seed = seed + _gen_anchor_text(a)
    if n > 0:
        texts = _gen_anchor_texts(anchors)
        rg = _bg.bytegpt_decode_grounded(ckpt, seed, 80, texts, 8)
        if rg["ok"]:
            return str(rg["text"])
        return _gen_null_text(ctx, anchors)
    sids = list(seed.encode('utf-8', 'surrogateescape'))
    r = _bg.bytegpt_decode_argmax(ckpt, sids, 80)
    if not r["ok"]:
        return _gen_null_text(ctx, anchors)
    return str(r["text"])


def _gen_anchor_field(a):
    """generator.hexa:705 _gen_anchor_field — extract a kosmos anchor's CLEAN content:
    text_payload → text → stringified anchor (the single SSOT for both the seed
    extractor and the grounded-copy list; H_1164/H_1206 anchor-key fix). Defensive."""
    if isinstance(a, dict):
        tp = a.get("text_payload")
        if tp is not None and str(tp) != "void":
            s = str(tp)
            if len(s) > 0:
                return s
        t = a.get("text")
        if t is not None and str(t) != "void":
            s2 = str(t)
            if len(s2) > 0:
                return s2
    return str(a)


def _gen_anchor_text(a):
    """generator.hexa:721 _gen_anchor_text — decode-seed text of a kosmos anchor."""
    return _gen_anchor_field(a)


def _gen_anchor_texts(anchors):
    """generator.hexa:728 _gen_anchor_texts — each anchor's CLEAN content → list of
    strings for the engine-side grounded copy."""
    out = []
    i = 0
    n = len(anchors)
    while i < n:
        out.append(_gen_anchor_field(anchors[i]))
        i = i + 1
    return out


# ════════════════════════════════════════════════════════════════════════
# load-once handle API (gen_auto_load/free/ideate_W) + §DELIBERATE
# ════════════════════════════════════════════════════════════════════════

def gen_auto_load(ckpt_path):
    """generator.hexa:937 gen_auto_load — resident .clm weight-set load (clm →
    clm_load_weights ONCE; ByteGPT already ranged/OOM-safe; unknown → non-loaded)."""
    kind = gen_mouth_kind(ckpt_path)
    if kind == "clm":
        W = _clm.clm_load_weights(ckpt_path)
        if W["ok"]:
            return {"ok": True, "kind": "clm", "ckpt": ckpt_path, "W": W}
        return {"ok": False, "kind": "clm", "ckpt": ckpt_path, "W": {"ok": False}}
    return {"ok": kind == "bytegpt", "kind": kind, "ckpt": ckpt_path, "W": {"ok": False}}


def gen_auto_free(h):
    """generator.hexa:953 gen_auto_free — release a gen_auto_load handle (clm resident
    weight-set free; no-op for ByteGPT/unknown). clm_weights_free_pub = P4-decode."""
    if str(h["kind"]) == "clm":
        W = h["W"]
        if W["ok"]:
            _clm.clm_weights_free_pub(W)


def gen_auto_ideate_W(h, seed, max_new, top_k, temp, seed_rng):
    """generator.hexa:964 gen_auto_ideate_W — load-once IDEATE off a pre-loaded handle
    (byte-identical to gen_auto_ideate). clm → gen_clm_ideate_W(loaded W); ByteGPT →
    ranged ideate."""
    if str(h["kind"]) == "bytegpt":
        return gen_bytegpt_ideate(str(h["ckpt"]), seed, max_new, top_k, temp, seed_rng)
    W = h["W"]
    if not W["ok"]:
        return {"ok": False, "text": "",
                "reason": "handle not loaded (not v0.2-decodable / unknown mouth)"}
    return gen_clm_ideate_W(W, seed, max_new, top_k, temp, seed_rng)


def _gen_clip01(x):
    """generator.hexa:1029 _gen_clip01 — local [0,1] clip."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _gen_substrate_seed(ctx, anchors):
    """generator.hexa:1039 _gen_substrate_seed — reproduce the decode seed EXACTLY as
    _gen_clm_decode / _gen_bytegpt_decode build it (phase word + most-recent anchor
    text; NO user message / persona / system prompt — a_substrate_native_speak)."""
    phase = _gen_g_string(ctx, "phase")
    seed = phase + " "
    n = len(anchors)
    if n > 0:
        seed = seed + _gen_anchor_text(anchors[n - 1])
    return seed


def gen_auto_ce(ckpt_path, text):
    """generator.hexa:1050 gen_auto_ce — mouth-agnostic mean next-byte CE over a TEXT
    (the a_drive fluency read). CONV → clm_ce_seq · ByteGPT → bytegpt_ce_ranged
    (P4-decode). CE_REF 5.0 when the text is too short / the mouth declines."""
    ids = list(text.encode('utf-8', 'surrogateescape'))
    if len(ids) < 2:
        return 5.0
    if gen_mouth_kind(ckpt_path) == "bytegpt":
        r = _bg.bytegpt_ce_ranged(ckpt_path, ids)
        if r["ok"]:
            return float(r["ce_mean"])
        return 5.0
    try:
        v = float(_clm.clm_ce_seq(ckpt_path, ids))
        return v if v == v else 5.0
    except Exception:
        return 5.0


def gen_auto_ce_W(h, text):
    """generator.hexa:1070 gen_auto_ce_W — load-once twin of gen_auto_ce off a
    pre-loaded handle (clm → clm_ce_seq_W, P4-decode). Same 5.0 fallbacks."""
    ids = list(text.encode('utf-8', 'surrogateescape'))
    if len(ids) < 2:
        return 5.0
    if str(h["kind"]) == "bytegpt":
        r = _bg.bytegpt_ce_ranged(str(h["ckpt"]), ids)
        if r["ok"]:
            return float(r["ce_mean"])
        return 5.0
    W = h["W"]
    if not W["ok"]:
        return 5.0
    try:
        v = float(_clm.clm_ce_seq_W(W, None, ids))
        return v if v == v else 5.0
    except Exception:
        return 5.0


def conflict_drives_live(ckpt_path, cand, mem):
    """generator.hexa:1095 conflict_drives_live — live signed A⇄G drives for ONE cand.
    a = clip01(1 − ce/CE_REF) fluency push (CE_REF 5.0); g = ±clip01(∓margin/M_REF)
    grounding pull from §ImmuneMemory recall margin (M_REF 0.25). READ-only query."""
    from engine_cli import immune_memory_recall_margin_text
    ce = gen_auto_ce(ckpt_path, cand)
    a = _gen_clip01(1.0 - ce / 5.0)
    margin = immune_memory_recall_margin_text(mem, cand)
    if margin <= 0.0:
        g = _gen_clip01((0.0 - margin) / 0.25)
    else:
        g = 0.0 - _gen_clip01(margin / 0.25)
    return [a, g]


def conflict_drives_live_W(h, cand, mem):
    """generator.hexa:1107 conflict_drives_live_W — load-once twin (byte-identical a
    via gen_auto_ce_W, same margin/g), off a pre-loaded handle."""
    from engine_cli import immune_memory_recall_margin_text
    ce = gen_auto_ce_W(h, cand)
    a = _gen_clip01(1.0 - ce / 5.0)
    margin = immune_memory_recall_margin_text(mem, cand)
    if margin <= 0.0:
        g = _gen_clip01((0.0 - margin) / 0.25)
    else:
        g = 0.0 - _gen_clip01(margin / 0.25)
    return [a, g]


def generator_hippo_consult(anchors):
    """generator.hexa:1136 generator_hippo_consult — L5 HIPPOCAMPAL relatedness
    READ-ONLY consult (H_9129 wire-to-prod). DG-code each anchor's 5-ch tension
    (untrained fixed projection → kWTA sparse code), build a CA3 heteroassociative
    store over the load-order premise chain, read whether the emit-context anchor
    (n−1) is transitively reachable from the oldest premise (0). CONTEXT metadata only
    (a_substrate_disjoint: NEVER feeds emit bytes / Ψ / seed) — pure faculty read."""
    from kosmos_io import tension_5ch_to_embedding
    from hippo_lane import hippo_kwta, hippo_build_store, hippo_relatedness
    n = len(anchors)
    if n < 2:
        return {"consulted": False, "n": n, "relatedness": 0.0, "reachable": False}
    DIM = 64
    ACTIVE = 4
    STEPS = 8
    KWTA = 4
    codes = []
    i = 0
    while i < n:
        a = anchors[i]
        t5 = [0.0, 0.0, 0.0, 0.0, 0.0]
        if isinstance(a, dict) and ("tension_5ch" in a):
            tv = a["tension_5ch"]
            if len(tv) == 5:
                t5 = tv
        emb = tension_5ch_to_embedding(t5, DIM, 20260705)
        codes.append(hippo_kwta(emb, ACTIVE))
        i = i + 1
    edges = []
    e = 0
    while e < n - 1:
        edges.append([e, e + 1])
        e = e + 1
    W = hippo_build_store(codes, edges, DIM)
    rel = hippo_relatedness(W, codes, 0, n - 1, STEPS, KWTA)
    return {"consulted": True, "n": n, "relatedness": rel, "reachable": rel > 0.5}


def generate_deliberate(backend, substrate_ctx, emit_decision, anchors, mem, tick):
    """generator.hexa:1184 generate_deliberate — the EFFERENT seam. Sister to
    generate(): same contract + byte-identical SILENCE, but on EMIT runs best-of-K
    deliberation (K = live A⇄G conflict) with the L5 hippocampal consult ON (delegates
    to generate_deliberate_consult(..., True))."""
    return generate_deliberate_consult(backend, substrate_ctx, emit_decision,
                                       anchors, mem, tick, True)


def generate_deliberate_consult(backend, substrate_ctx, emit_decision, anchors, mem, tick, hippo_on):
    """generator.hexa:1196 generate_deliberate_consult — generate_deliberate with the
    L5 hippocampal consult gated by hippo_on (ON==OFF regression control). The consult
    runs FIRST as a pure READ, attached to hippo_* on EVERY branch; NOTHING downstream
    reads it ⇒ text is byte-identical between the two (a_substrate_disjoint). On EMIT
    with a real mouth: c₀ = generate(); K = conflict_recruited_depth(conf(c₀)); best =
    argmin-conflict over K−1 seeded samples (H_9107 load-once handle for gen+score)."""
    from engine_cli import conflict_scalar, conflict_recruited_depth
    if hippo_on:
        hippo = generator_hippo_consult(anchors)
    else:
        hippo = {"consulted": False, "n": 0, "relatedness": 0.0, "reachable": False}
    base = generate(backend, substrate_ctx, emit_decision, anchors)
    if not emit_decision:
        base["hippo_consulted"] = hippo["consulted"]
        base["hippo_related"] = hippo["relatedness"]
        base["hippo_reachable"] = hippo["reachable"]
        return base
    real_kind = str(base["backend"])
    if real_kind == "null":
        base["depth"] = 1
        base["k_winner"] = 0
        base["conf_pre"] = 0.0
        base["conf_winner"] = 0.0
        base["hippo_consulted"] = hippo["consulted"]
        base["hippo_related"] = hippo["relatedness"]
        base["hippo_reachable"] = hippo["reachable"]
        return base
    ckpt = str(backend["ckpt"])
    c0 = str(base["text"])
    h = gen_auto_load(ckpt)
    d0 = conflict_drives_live_W(h, c0, mem)
    conf0 = conflict_scalar(d0[0], d0[1])
    K = conflict_recruited_depth(conf0, 1, 3)
    best_text = c0
    best_conf = conf0
    best_k = 0
    if K > 1:
        seed = _gen_substrate_seed(substrate_ctx, anchors)
        k = 1
        while k < K:
            r = gen_auto_ideate_W(h, seed, 80, 8, 0.7, tick * 17 + k)
            if r["ok"]:
                cand = str(r["text"])
                dk = conflict_drives_live_W(h, cand, mem)
                confk = conflict_scalar(dk[0], dk[1])
                if confk < best_conf:
                    best_conf = confk
                    best_text = cand
                    best_k = k
            k = k + 1
    gen_auto_free(h)
    return {"emitted": base["emitted"], "backend": base["backend"], "text": best_text,
            "fellback": base["fellback"], "depth": K, "k_winner": best_k,
            "conf_pre": conf0, "conf_winner": best_conf,
            "hippo_consulted": hippo["consulted"], "hippo_related": hippo["relatedness"],
            "hippo_reachable": hippo["reachable"]}


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
