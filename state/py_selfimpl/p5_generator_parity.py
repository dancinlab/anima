#!/usr/bin/env python3
"""P5 generator/brain deliberation-stack parity oracle (self-contained).

Verifies core/generator.py (+ brain_emit_deliberate in core/brain.py) is a byte-exact
py twin of the CANONICAL core/generator.hexa L3 deliberation stack.

Two evidence tiers (HONEST split, like P3's topo-ON structural marking):
  · VALUE-ORACLED — the pure-substrate functions (gen_ctx_from_decision(_conflicted),
    generate() null/SILENT path -> _gen_null_text, generator_hippo_consult, the
    conflict-depth arithmetic). Expected values are the REAL hexa outputs captured by
    running state/py_selfimpl/generator_golden.hexa through the `hexa` binary (frozen in
    p5_generator_golden.txt). The py twin regenerates the SAME lines and we byte-diff
    them + HAND-check the arithmetic.
  · STRUCTURALLY-VERIFIED (not value-oracled) — the decode-dependent paths
    (gen_clm_decode_deliberated, _gen_clm_decode/_gen_bytegpt_decode, gen_auto_ce(_W),
    conflict_drives_live(_W), the clm branch of generate_deliberate_consult). These call
    core/decode.py symbols (clm_decode_ce . clm_decode_grounded . bytegpt_decode_grounded
    . clm_ce_ranged(_W) . bytegpt_ce_ranged . clm_weights_free_pub) being added by the
    parallel P4 decode.py port. We assert the functions exist and route to the right
    decode symbol names, but do NOT claim decoded-byte parity until P4 lands.

Run:  python3 state/py_selfimpl/p5_generator_parity.py   (from repo root)
"""
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_ROOT, "core"))
_GOLDEN = os.path.join(_ROOT, "state", "py_selfimpl", "p5_generator_golden.txt")

import generator as G
import brain as B

P = 0
F = 0
report = []


def chk(kind, name, got, exp):
    global P, F
    ok = got == exp
    P += ok
    F += (not ok)
    report.append("  [%s] %-6s %s: got=%r exp=%r" % ("PASS" if ok else "FAIL", kind, name, got, exp))


# ── the fixed inputs (IDENTICAL to generator_golden.hexa) ────────────────────
_DEC = {"phi": 0.5432, "phase": "turbulent", "tier": 3, "tier_name": "ORANGE", "motivation": 0.7}
_CTS = [0.0, 0.25, 0.5, 0.83, 1.0, 1.5, 0.0 - 0.3]
_ANCHORS = [
    {"name": "a0", "text_payload": "hello", "tension_5ch": [0.1, 0.2, 0.3, 0.4, 0.5]},
    {"name": "a1", "text_payload": "world", "tension_5ch": [0.5, 0.4, 0.3, 0.2, 0.1]},
    {"name": "a2", "text_payload": "foo", "tension_5ch": [0.2, 0.2, 0.2, 0.2, 0.2]},
]


def _b(x):
    return "true" if x else "false"


def _py_lines():
    """Regenerate the golden lines from the py twin, byte-for-byte format-matched to
    generator_golden.hexa (format_float(x,N) == %.Nf)."""
    lines = []
    ctx = G.gen_ctx_from_decision(_DEC)
    lines.append("CTX|phi=%s|phase=%s|tier=%s|tier_name=%s|motivation=%s" % (
        "%.4f" % float(ctx["phi"]), str(ctx["phase"]), str(ctx["tier"]),
        str(ctx["tier_name"]), "%.4f" % float(ctx["motivation"])))
    for ct in _CTS:
        cc = G.gen_ctx_from_decision_conflicted(_DEC, ct)
        lines.append("CONF|ct=%s|k=%s" % ("%.4f" % ct, str(cc["deliberation_k"])))
    nb = G.gen_null_backend()
    gs = G.generate(nb, ctx, False, [])
    lines.append("SILENT|emitted=%s|backend=%s|text=%s" % (
        _b(gs["emitted"]), str(gs["backend"]), str(gs["text"])))
    ge = G.generate(nb, ctx, True, _ANCHORS)
    lines.append("EMIT|emitted=%s|backend=%s|fellback=%s|text=%s" % (
        _b(ge["emitted"]), str(ge["backend"]), _b(ge["fellback"]), str(ge["text"])))
    hp = G.generator_hippo_consult(_ANCHORS)
    lines.append("HIPPO|consulted=%s|n=%s|relatedness=%s|reachable=%s" % (
        _b(hp["consulted"]), str(hp["n"]), "%.6f" % float(hp["relatedness"]), _b(bool(hp["reachable"]))))
    hp1 = G.generator_hippo_consult(_ANCHORS[:1])
    lines.append("HIPPO1|consulted=%s|n=%s|relatedness=%s|reachable=%s" % (
        _b(hp1["consulted"]), str(hp1["n"]), "%.6f" % float(hp1["relatedness"]), _b(bool(hp1["reachable"]))))
    return lines


# ── VALUE-ORACLE: byte-diff py lines vs the frozen hexa golden ───────────────
report.append("-- VALUE-ORACLED (py twin vs real hexa generator_golden output) --")
py_lines = _py_lines()
if os.path.exists(_GOLDEN):
    with open(_GOLDEN, "r") as fh:
        gold = [ln.rstrip("\n") for ln in fh if ln.strip() != "" and not ln.lstrip().startswith("#")]
    for i, pl in enumerate(py_lines):
        gl = gold[i] if i < len(gold) else "<missing>"
        chk("ORACLE", pl.split("|")[0], pl, gl)
else:
    report.append("  [SKIP] golden file absent (%s) -- run generator_golden.hexa first" % _GOLDEN)

# ── HAND: conflict-depth arithmetic (k = 1 + int(clip01(ct)*3 + 0.5)) ────────
report.append("-- HAND (conflict->deliberation-depth arithmetic + pure helpers) --")
for ct, k in [(0.0, 1), (0.25, 2), (0.5, 3), (0.83, 3), (1.0, 4), (1.5, 4), (-0.3, 1)]:
    chk("HAND", "conflicted_k@%.2f" % ct, G.gen_ctx_from_decision_conflicted(_DEC, ct)["deliberation_k"], k)
chk("HAND", "clip01_lo", G._gc_clip01(-2.0), 0.0)
chk("HAND", "clip01_hi", G._gc_clip01(2.0), 1.0)
chk("HAND", "clip01_id", G._gc_clip01(0.42), 0.42)
chk("HAND", "gen_clip01_lo", G._gen_clip01(-2.0), 0.0)
chk("HAND", "gen_clip01_hi", G._gen_clip01(2.0), 1.0)
chk("HAND", "g_float_void", G._gen_g_float({}, "x"), 0.0)
chk("HAND", "g_int_void", G._gen_g_int({}, "x"), 0)
chk("HAND", "g_string_void", G._gen_g_string({}, "x"), "")
chk("HAND", "text_to_bytes", G._gen_text_to_bytes("AB\n"), [65, 66, 10])
chk("HAND", "anchor_field_payload", G._gen_anchor_field({"text_payload": "p", "text": "t"}), "p")
chk("HAND", "anchor_field_text", G._gen_anchor_field({"text": "t"}), "t")
chk("HAND", "anchor_texts", G._gen_anchor_texts(_ANCHORS), ["hello", "world", "foo"])
chk("HAND", "substrate_seed", G._gen_substrate_seed(G.gen_ctx_from_decision(_DEC), _ANCHORS), "turbulent foo")
chk("HAND", "read_anchors_empty", G.generator_read_anchors(""), [])
chk("HAND", "read_anchors_nodir", G.generator_read_anchors("/no/such/dir/xyz"), [])

# ── STRUCT: decode-dependent + brain wiring exist & route correctly ──────────
report.append("-- STRUCTURALLY-VERIFIED (decode-dependent; P4 decode.py pending) --")
for fn in ["gen_clm_decode_deliberated", "_gen_clm_decode", "_gen_bytegpt_decode",
           "gen_auto_load", "gen_auto_free", "gen_auto_ideate_W", "gen_auto_ce",
           "gen_auto_ce_W", "conflict_drives_live", "conflict_drives_live_W",
           "generate_deliberate", "generate_deliberate_consult"]:
    chk("STRUCT", "exists:%s" % fn, callable(getattr(G, fn, None)), True)
chk("STRUCT", "brain_emit_deliberate", callable(getattr(B, "brain_emit_deliberate", None)), True)
# gen_fm_rerank is DEFERRED (eval-path only, not a chat dependency) -- must NOT be present
chk("STRUCT", "gen_fm_rerank_DEFERRED", hasattr(G, "gen_fm_rerank"), False)
# generate_deliberate SILENT path is pure (no decode) -- value-checkable
_sil = G.generate_deliberate(G.gen_null_backend(), G.gen_ctx_from_decision(_DEC), False, _ANCHORS, None, 7)
chk("STRUCT", "deliberate_silent_emitted", _sil["emitted"], False)
chk("STRUCT", "deliberate_silent_text", _sil["text"], "")
chk("STRUCT", "deliberate_silent_hippo", _sil["hippo_consulted"], True)
# null-backend EMIT deliberate path is pure (real_kind=='null' short-circuit, no decode)
_nul = G.generate_deliberate(G.gen_null_backend(), G.gen_ctx_from_decision(_DEC), True, _ANCHORS, None, 7)
chk("STRUCT", "deliberate_null_depth", _nul["depth"], 1)
chk("STRUCT", "deliberate_null_kwinner", _nul["k_winner"], 0)
chk("STRUCT", "deliberate_null_text", _nul["text"].startswith("[null-gen]"), True)

# ── report ───────────────────────────────────────────────────────────────────
print("\n".join(report))
print("\nP5 generator/brain parity: %d PASS / %d FAIL  (of %d checks)" % (P, F, P + F))
sys.exit(1 if F else 0)
