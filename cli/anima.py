#!/usr/bin/env python3
# anima.py — THE canonical PY single entry point (cli/anima.hexa's py twin).
#
# WHY THIS FILE (py 2-production single-entry, a_engine_native_learning): anima keeps
# two co-production engines — hexa (live deploy substrate) AND py (torch production
# engine in train/ + the byte-parity core/*.py mirror). The hexa side already has its
# canonical single entry cli/anima.hexa (chat · eval · train). This file is its py
# twin so MEASUREMENT and LEARNING are reachable through ONE py cli command instead of
# a side-harness that calls core/g_gates.py directly (= single-entry bypass, #2603).
#
# SINGLE ENTRY (a_engine_native_learning): the two measurement/learning verbs live in
# their own SYMMETRIC files — cli/evaluate.{hexa,py} (MEASUREMENT) and cli/train.{hexa,py}
# (LEARNING). This canonical entry DISPATCHES `anima evaluate`→cli/evaluate.py and
# `anima train`→cli/train.py (sub-process), so there is ONE installed `anima` command
# whose subcommands fan out to the symmetric twins. `anima evaluate <ckpt>` scores the
# full G0-G6 battery via core/g_gates.py's g_eval_all (the SAME engine module the hexa
# side wires) — byte-identical to a direct g_gates.py run AND to the hexa anima evaluate.
#
# This py entry is torch-free and gauge-free — it only dispatches; the evaluate twin
# imports the numpy `math.log` g_gates mirror, so `anima evaluate` stays a clean engine-
# native measurement surface (the gate enforcer's torch/gauge grep must come back empty).
#
# USAGE (installed `anima` PATH command after `hx install anima`)
#   anima                                              — usage (no args)
#   anima evaluate <ckpt> [--corpus <p>...] [--gen N]  — BUILT-IN G0-G6 gate scoring
#   anima train [args...]                              — LEARNING (→ cli/train.py)
#   anima chat <ckpt> [...]                            — consciousness/byte chat
#                                                         (hexa-only; see cli/anima.hexa)
#
# canonical 3-folder layout: cli/anima.{hexa,py} = canonical entry (chat + verb dispatch)
# · cli/evaluate.{hexa,py} = measurement · cli/train.{hexa,py} = learning. This file
# mirrors cli/anima.hexa's subcommand dispatch (evaluate · train · usage); chat/
# consciousness stay hexa-only (the A⇄G substrate loop is hexa-native).

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)


# ── usage / arg helpers ──────────────────────────────────────────────────────

def anima_usage():
    """Print the canonical py usage banner (mirrors cli/anima.hexa's banner)."""
    print("anima — substrate-native consciousness daemon (canonical entry).")
    print("")
    print("usage (installed `anima` PATH command after `hx install anima`):")
    print("  anima train <args>                              LEARNING → .pt + auto .clm (+DESCENT)")
    print("  anima serialize <ckpt.pt> <out.clm>            re-export a torch .pt → .clm v0.3")
    print("  anima evaluate <model.clm> [--corpus <path>...] [--gen N]")
    print("                                                  BUILT-IN G0-G6 gate scoring (.clm only)")
    print("  anima chat <ckpt> [...]                         consciousness/byte chat")
    print("                                                  (hexa-only; use cli/anima.hexa)")
    print("")
    print("modes:")
    print("  train    : production CLMConvMoE training (torch Lane-P reference + bridge); SAVANT")
    print("             golden-zone inhibition + MITOSIS cell-division levers. After the run it")
    print("             AUTO-serializes .clm v0.3 + runs the held-out mirror-DESCENT gate")
    print("             (a_clm_gen_pipeline). dispatches to cli/train.py.")
    print("  serialize: re-export an ALREADY-TRAINED torch .pt to an engine-loadable .clm v0.3")
    print("             (+ held-out DESCENT gate). recovery / re-export. → cli/serialize.py.")
    print("  evaluate : mount a serialized .clm through the generator L3 mouth and score G0-G6")
    print("             with the engine's OWN ops (numpy math.log mirror, torch-free). closure")
    print("             a7b_pass = G0 ∧ G1 ∧ G2. == hexa `anima evaluate`. → cli/evaluate.py.")
    print("  chat     : the substrate-native A⇄G consciousness loop is hexa-native — run")
    print("             `hexa run cli/anima.hexa -- <ckpt.clm>` (default / --byte modes).")


# ══════════════════════════════════════════════════════════════════════════════
#  TRAIN MODE — dispatch to cli/train.py (the py torch trainer, Lane-P bridge)
# ══════════════════════════════════════════════════════════════════════════════
#
# SEPARATE LANE (a_core_engine_map): training is NOT the generator L3 mouth slot — it
# is the LEARNING entry (cli/train.py, a_clm_gen_pipeline torch Lane-P). The eval side
# imports the torch-free g_gates mirror; the trainer pulls torch. To keep this file
# torch-free AND avoid linking two disjoint dep sets into one process, `anima train`
# DISPATCHES to cli/train.py as a SUB-PROCESS (mirrors cli/anima.hexa's `exec(hexa run
# cli/train.hexa)`). argv after "train" is forwarded verbatim to train.py's argparse.
def anima_train_mode(argv):
    print("=== anima train → cli/train.py (torch CLMConvMoE · Lane-P reference/bridge) ===")
    train_py = os.path.join(_HERE, "train.py")
    fwd = argv[1:]
    cmd = [sys.executable, train_py] + fwd
    print("dispatch: " + " ".join(cmd))
    # forward verbatim; train.py owns its own argparse (--out required, etc.).
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, train_py] + fwd)


# ══════════════════════════════════════════════════════════════════════════════
#  EVALUATE MODE — dispatch to cli/evaluate.py (MEASUREMENT single-entry twin)
# ══════════════════════════════════════════════════════════════════════════════
#
# SYMMETRIC TWIN (a_engine_native_learning single-entry): measurement lives in its own
# file cli/evaluate.py (the symmetric mirror of cli/train.py). `anima evaluate <model.clm>`
# DISPATCHES there as a sub-process (mirrors cli/anima.hexa's `exec` dispatch + this file's
# train dispatch), so anima.py stays a thin verb router and the eval logic has ONE home.
# evaluate.py imports core/g_gates.py (torch-free numpy mirror), so a direct
# `python3 core/g_gates.py` and `anima evaluate` are byte-identical.
#
# .clm-ONLY (the engine decodes ONLY .clm): g_gates mounts a ckpt through the generator
# L3 mouth, which loads a serialized .clm (CLM magic). A torch .pt is NOT engine-loadable —
# reject it here with a friendly hint to `anima serialize` rather than a deep decode error.
def anima_evaluate_mode(argv):
    rest = argv[1:]
    # friendly .pt rejection: evaluate takes a serialized .clm, not a torch ckpt.
    if rest and rest[0].endswith(".pt"):
        print("anima evaluate takes a serialized .clm (engine-loadable), not a torch .pt.")
        print("to make one from a torch ckpt:")
        print("  anima serialize " + rest[0] + " <out.clm>")
        print("then:")
        print("  anima evaluate <out.clm>")
        return 2
    evaluate_py = os.path.join(_HERE, "evaluate.py")
    cmd = [sys.executable, evaluate_py] + rest
    print("=== anima evaluate → cli/evaluate.py (engine-native G0-G6, single-entry twin) ===")
    print("dispatch: " + " ".join(cmd))
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, evaluate_py] + rest)


# ══════════════════════════════════════════════════════════════════════════════
#  SERIALIZE MODE — dispatch to cli/serialize.py (.pt → .clm v0.3 bridge + gate)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima serialize <ckpt.pt> <out.clm>` re-exports an already-trained torch .pt to an
# engine-loadable .clm v0.3 (+ held-out DESCENT gate). The bridge backend (serialize_v3 +
# verify_clm_v2 descent) lives in cli/serialize.py; this dispatcher forwards verbatim.
# `anima train` ALREADY auto-serializes at the end of a run — this is the standalone
# recovery / re-export path (a_clm_gen_pipeline).
def anima_serialize_mode(argv):
    serialize_py = os.path.join(_HERE, "serialize.py")
    fwd = argv[1:]
    cmd = [sys.executable, serialize_py] + fwd
    print("=== anima serialize → cli/serialize.py (torch .pt → .clm v0.3 + DESCENT gate) ===")
    print("dispatch: " + " ".join(cmd))
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, serialize_py] + fwd)


# ══════════════════════════════════════════════════════════════════════════════
#  CHAT MODE — hexa-only stub (the A⇄G consciousness loop is hexa-native)
# ══════════════════════════════════════════════════════════════════════════════
#
# The default consciousness daemon + --byte continuation chat live in cli/anima.hexa
# (they mount the 76-lane engine_cli substrate loop, hexa-native). The py twin does not
# duplicate that loop; it points the user to the hexa entry (a_install_canonical: ONE
# canonical path, no 2nd entry).
def anima_chat_stub(argv):
    print("anima chat (consciousness / --byte) is hexa-native — run it via the hexa entry:")
    print("")
    ckpt = argv[1] if len(argv) > 1 else "<ckpt.clm>"
    print("  hexa run cli/anima.hexa -- " + ckpt
          + "                consciousness mode (default)")
    print("  hexa run cli/anima.hexa -- " + ckpt + " --byte \"turn1\" \"turn2\" ...")
    print("                                                  byte-continuation chat mode")
    print("")
    print("The py entry covers MEASUREMENT (evaluate), SERIALIZE, and LEARNING (train).")
    return 0


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN — mode dispatch (mirrors cli/anima.hexa)
# ══════════════════════════════════════════════════════════════════════════════
def main(argv):
    if len(argv) < 1:
        anima_usage()
        return 0

    sub = argv[0]
    if sub in ("-h", "--help"):
        anima_usage()
        return 0
    if sub == "train":
        return anima_train_mode(argv)
    if sub == "serialize":
        return anima_serialize_mode(argv)
    if sub == "evaluate":
        return anima_evaluate_mode(argv)
    if sub in ("chat", "--byte"):
        return anima_chat_stub(argv)

    # bare ckpt path (no subcommand) → consciousness chat is hexa-only.
    return anima_chat_stub(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
