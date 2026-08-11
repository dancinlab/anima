#!/usr/bin/env python3
# serialize_bind.py — anima STANDALONE injected-bind re-serialize entry
# (base ByteGPT .bin + injected torch .pt → engine .bin with a "BGB\x01" trailer).
#
# WHY THIS FILE (H_9027 · a_clm_gen_pipeline sibling for the BYTE mouth): a trained
# BindAttn model = the FROZEN base ByteGPT + N appended GATED transformer blocks
# (applied after the L base blocks, before ln_f: x = x + gate*(block(x)-x)). This
# command bridges the injected torch .pt back onto the base .bin so the combined
# model is engine-loadable and scoreable via `anima-py evaluate <bin>` with ZERO
# changes to cli/evaluate.py (bg_is_bytegpt stays true; bg_load reads the trailer).
#
# REFERENCE-MATCH (NOT a reimplementation): the byte layout is core/serialize.py::
# serialize_bind (mirrors `serialize`'s per-layer write + the CLM "CLMB" bind-trailer
# precedent), and it is the SAME grammar core/decode.py bg_load parses. This file only
# reads argv, then calls that one backend — it invents no new layout.
#
# TORCH IS ALLOWED HERE (training family): reading the injected .pt (unpickle) is the
# only torch touch. This is the LEARNING-side re-export, NOT the torch-free measurement
# surface (cli/evaluate.py) the gate enforcer targets.
#
# USAGE (installed canonical `anima-py` command)
#   anima serialize-bind <base.bin> <injected.pt> <out.bin>
#     <base.bin>      plain engine ByteGPT .bin (5xu32 header, NO trailer)
#     <injected.pt>   torch {"bind": <Block state_dict | list | dict>,
#                            "gate": <scalar | list | dict>, "config": {...}}
#     <out.bin>       output engine .bin = base bytes verbatim + BGB trailer

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
# UNIFIED serializer = core/serialize.py (same resolution cli/serialize.py uses).
sys.path.insert(0, os.path.join(_REPO, "core"))


def serialize_bind_usage():
    print("anima serialize-bind — base ByteGPT .bin + injected torch .pt → .bin + BGB trailer.")
    print("")
    print("usage:")
    print("  anima serialize-bind <base.bin> <injected.pt> <out.bin>")
    print("")
    print("  splice N appended gated transformer blocks (BindAttn .pt) onto a base ByteGPT")
    print("  .bin so the combined model is engine-loadable + scoreable via")
    print("  `anima-py evaluate <out.bin>`. gate=0 => byte-identical to the base .bin.")


def serialize_bind_run(argv):
    if len(argv) < 3:
        serialize_bind_usage()
        return 2
    base_bin, injected_pt, out_bin = argv[0], argv[1], argv[2]
    if not os.path.exists(base_bin):
        print("ERROR: base .bin not found: " + base_bin)
        return 2
    if not os.path.exists(injected_pt):
        print("ERROR: injected .pt not found: " + injected_pt)
        return 2

    import serialize as S       # core/serialize.py — serialize_bind = bind-trailer SSOT
    import decode as D          # core/decode.py — CORE-loadable self-check (bg_load)

    print("=== anima serialize-bind — base .bin + injected .pt → .bin + BGB ===")
    print("base:     " + base_bin)
    print("injected: " + injected_pt)
    print("out:      " + out_bin)

    S.serialize_bind(base_bin, injected_pt, out_bin)
    nbytes = os.path.getsize(out_bin)
    print("WRITTEN " + str(nbytes) + " bytes -> " + out_bin)

    # ── CORE-loadable self-check (mirror of core/decode.py BYTE mouth) ─────────
    print("")
    print("=== CORE-loadable self-check (core/decode.py bg_load BYTE mouth) ===")
    is_bg = D.bg_is_bytegpt(out_bin)
    print("  bg_is_bytegpt = " + str(is_bg))
    if not is_bg:
        print("FAIL — output .bin is NOT recognized as a ByteGPT mouth.")
        return 1
    W = D.bg_load(out_bin)
    nb = len(W.get("bind", []))
    print("  bg_load ok    = " + str(W.get("ok")) + "   n_bind blocks = " + str(nb))
    if not W.get("ok") or nb < 1:
        print("FAIL — output .bin did not round-trip a BGB trailer.")
        return 1
    print("  ✅ CORE-loadable with " + str(nb) + " injected-bind block(s).")
    print("  NOTE: this is a STRUCTURE round-trip only — the engine-native ρ-AXON reach")
    print("        verdict (former G0-G6) is `anima-py evaluate <out.bin>` (a_engine_native_learning).")
    return 0


def main(argv):
    if len(argv) >= 1 and argv[0] in ("-h", "--help"):
        serialize_bind_usage()
        return 0
    return serialize_bind_run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
