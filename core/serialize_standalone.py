# ==========================================================================
# ⛔ ENGINE-INTERNAL TOOL — agent 가 직접 타이핑 금지. 학습/직렬화는 cli/ 단일진입만:
#   anima-py train | anima-py serialize.
# cli/serialize.py 가 torch .pt→.clm v0.3 bridge 를 내부 호출하므로 __main__
# hard-exit 가드는 두지 않는다. 직접 실행 차단은 단일진입 정책이 담당한다.
# ==========================================================================
#!/usr/bin/env python3
# serialize.py — anima STANDALONE re-serialize entry (.pt → .clm v0.3 + held-out gate).
#
# WHY THIS FILE (recovery/re-export · a_clm_gen_pipeline): `anima train` ALREADY
# auto-serializes its trained weights to .clm v0.3 and runs the held-out mirror-DESCENT
# gate at the end of a run (cli/train.py post-serialize block). This
# standalone command exists for the SEPARATE case: re-exporting an ALREADY-TRAINED torch
# .pt checkpoint (recovery, re-export, re-verification) without re-training.
#
# REFERENCE-MATCH (NOT a reimplementation): the byte layout comes from the GROUND-TRUTH
# unified serializer core/serialize.py::serialize_v3 (the same byte grammar the
# canonical decoder parses), and the held-out gate is the kept
# torch-interop sibling verify_clm_v2.py descent (math.log mirror, dt_ln-immune). This file
# only loads the .pt, derives L/E from the state-dict keys, and calls those two backends —
# it invents no new layout and no new gate.
#
# TORCH IS ALLOWED HERE (training family): unlike cli/evaluate.py (torch-free
# measurement) this is the LEARNING-side re-export and must read a torch .pt. The gate
# enforcer's torch grep targets the measurement surfaces (evaluate / anima dispatch), not
# the trainer/serializer family (a_engine_native_learning: train/ may use torch).
#
# USAGE (installed canonical command)
#   anima-py serialize <ckpt.pt> <out.clm> [--heldout <path>] [--train <path>] [--nwin N]
#     <ckpt.pt>    torch state_dict (or {"state_dict": ...}/{"model": ...}) checkpoint
#     <out.clm>    output .clm v0.3 path (engine-loadable, CLM magic)
#     --heldout    held-out byte corpus for the post-serialize mirror-DESCENT gate
#                  (a_clm_gen_pipeline: structure round-trip is NOT enough)
#     --train      optional train corpus (gap-vs-heldout overfit advisory)
#     --nwin N     descent window length (default 64)

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# verify_clm_v2.py (held-out DESCENT gate) is a KEPT torch-interop SIBLING in this same
# train/clm/model/ dir. The serializer itself is now the UNIFIED core/serialize.py (CLM
# serialize_v3 + ByteGPT bridge, parallel to core/decode.py) — add core/ so `import
# serialize` resolves. core/ = <repo>/core; from …/archive/train/clm/model/ walk up 4 to
# the repo root (…/archive/train/clm/model → …/archive/train/clm → …/archive/train →
# …/archive → repo). If that core/ is absent (staged pod), fall back to _HERE.
sys.path.insert(0, _HERE)
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(_HERE))))
_CORE = os.path.join(_REPO, "core")
if os.path.isdir(_CORE) and _CORE not in sys.path:
    sys.path.insert(0, _CORE)


def serialize_usage():
    """Print the canonical usage banner (installed `anima serialize` command form)."""
    print("anima serialize — re-export a torch .pt to .clm v0.3 + held-out DESCENT gate.")
    print("")
    print("usage:")
    print("  anima serialize <ckpt.pt> <out.clm> [--heldout <path>] [--train <path>] [--nwin N]")
    print("")
    print("  re-serialize an ALREADY-TRAINED torch checkpoint to an engine-loadable .clm")
    print("  (ground-truth bridge serialize_v3) and verify it models held-out text")
    print("  (verify_clm_v2 mirror-DESCENT gate). `anima train` does this automatically;")
    print("  this command is for recovery / re-export of an existing .pt.")


def _strval(argv, flag, dflt):
    i = 0
    while i < len(argv):
        if argv[i] == flag and i + 1 < len(argv):
            return argv[i + 1]
        i += 1
    return dflt


def _intval(argv, flag, dflt):
    v = _strval(argv, flag, None)
    return int(v) if v is not None else dflt


def _derive_LE(sd):
    """Derive (L trunk layers, E experts) from the state-dict keys (reference-match
    of serialize_v2._general_block_keymap naming: trunk.{i}.* and moe.experts.{j}.*)."""
    L = 0
    E = 0
    for k in sd.keys():
        if k.startswith("trunk.") and k.endswith(".conv.conv.weight"):
            try:
                L = max(L, int(k.split(".")[1]) + 1)
            except (ValueError, IndexError):
                pass
        if k.startswith("moe.experts.") and k.endswith(".conv.conv.weight"):
            try:
                E = max(E, int(k.split(".")[2]) + 1)
            except (ValueError, IndexError):
                pass
    return L, E


def serialize_run(argv):
    if len(argv) < 2:
        serialize_usage()
        return 2

    pt = argv[0]
    out = argv[1]
    heldout = _strval(argv[2:], "--heldout", None)
    train_corpus = _strval(argv[2:], "--train", None)
    nwin = _intval(argv[2:], "--nwin", 64)

    if not os.path.exists(pt):
        print("ERROR: torch checkpoint not found: " + pt)
        return 2

    import torch                                          # training family — torch OK here
    import serialize as S                                 # core/serialize.py — serialize_v3 = bridge SSOT
    import verify_clm_v2 as VC                            # clm_decodable / descent (this dir)

    print("=== anima serialize — .pt → .clm v0.3 (ground-truth bridge) ===")
    print("pt:      " + pt)
    print("out:     " + out)

    raw = torch.load(pt, map_location="cpu")
    # normalize to a flat state_dict (mirror serialize_v2._resolve_state_dict inputs).
    if isinstance(raw, dict) and "state_dict" in raw and isinstance(raw["state_dict"], dict):
        sd = raw["state_dict"]
    elif isinstance(raw, dict) and "model" in raw and isinstance(raw["model"], dict):
        sd = raw["model"]
    else:
        sd = raw
    sd = {k: (v.detach().cpu() if hasattr(v, "detach") else v) for k, v in sd.items()}

    L, E = _derive_LE(sd)
    if L < 1 or E < 1:
        print("ERROR: could not derive L/E from state-dict keys "
              "(expected trunk.{i}.conv.conv.weight / moe.experts.{j}.conv.conv.weight). "
              "Is this an anima CLMConvMoE checkpoint?")
        return 2
    print("derived: L(trunk)=" + str(L) + "  E(experts)=" + str(E))

    S.serialize_v3(sd, n_trunk_layers=L, n_experts=E, out_path=out)
    nbytes = os.path.getsize(out)
    print("WRITTEN " + str(nbytes) + " bytes -> " + out)

    # ── CORE-loadable self-check (mirror of core/clm_decode.hexa) ────────────
    rb = open(out, "rb").read()
    decodable = VC.clm_decodable(rb)
    print("")
    print("=== CORE-loadable self-check (mirror of core/clm_decode.hexa) ===")
    print("  clm_decodable = " + str(decodable))
    if not decodable:
        print("FAIL — serialized .clm is NOT CORE-loadable (see above).")
        return 1

    # ── held-out mirror-DESCENT gate (a_clm_gen_pipeline) ────────────────────
    if heldout:
        if not os.path.exists(heldout):
            print("ERROR: --heldout corpus not found: " + heldout)
            return 2
        print("")
        print("post-serialize held-out DESCENT gate (verify_clm_v2 mirror, dt_ln-immune):")
        rc = VC.run_descent_gate_cli(out, heldout, train_corpus, nwin)
        if rc != 0:
            print("  ⛔ DESCENT GATE FAIL — serialized .clm broken/overfit; do NOT mark "
                  "done / HF-upload (a_clm_gen_pipeline).")
            return 1
        print("  ✅ DESCENT GATE PASS — serialized .clm models held-out text.")
    else:
        print("")
        print("NOTE: no --heldout corpus given — structure round-trip only. The .clm is "
              "CORE-loadable but its held-out predictive descent is UNVERIFIED "
              "(a_clm_gen_pipeline: decodable != generalizing). Pass --heldout to gate it.")
    return 0


def main(argv):
    if len(argv) >= 1 and argv[0] in ("-h", "--help"):
        serialize_usage()
        return 0
    return serialize_run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
