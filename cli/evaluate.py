#!/usr/bin/env python3
# evaluate.py — anima MEASUREMENT single entry (cli/evaluate.hexa's py twin).
#
# WHY THIS FILE (single-entry measurement · a_engine_native_learning): anima's two
# installed verbs are SYMMETRIC across two files — cli/train.{hexa,py} = LEARNING,
# cli/evaluate.{hexa,py} = MEASUREMENT. `anima evaluate <ckpt>` scores the full G0-G6
# battery by importing core/g_gates.py's g_eval_all — the SAME engine module the hexa
# side wires (gen_auto_ideate → gen_clm_ideate → clm_decode mirror), so the py evaluate
# is byte-identical to a direct g_gates.py run AND to the hexa `anima evaluate`. No new
# metric is invented here; this file is a thin dispatcher onto the existing engine op.
# g_gates is NOT a user-facing command — evaluate is the single-entry CLI that calls it.
#
# This py evaluate is torch-free and gauge-free — g_gates.py is the numpy `math.log`
# mirror, so `anima evaluate` stays a clean engine-native measurement surface (the gate
# enforcer's torch/gauge grep over this file must come back empty).
#
# USAGE (installed `anima` PATH command — NOT `hexa run`):
#   python3 cli/evaluate.py                              — usage (no args)
#   python3 cli/evaluate.py <ckpt> [--corpus <p>...] [--gen N]
#                                                       — BUILT-IN G0-G6 gate scoring
#
# 2-PRODUCTION (a_engine_native_learning): byte-parity twin = cli/evaluate.hexa. Both
# dispatch onto the SAME g_eval_all engine op.

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
# core/ is the engine package; import g_gates as the single G0-G6 entry (its byte-
# parity .py mirror, a_engine_native_learning). Add core/ to the path so its sibling
# imports (clm_decode, generator, g6_ideation, ...) resolve.
sys.path.insert(0, os.path.join(_REPO, "core"))


# ── usage / arg helpers ──────────────────────────────────────────────────────

def evaluate_usage():
    """Print the canonical py usage banner (installed `anima evaluate` command form)."""
    print("anima evaluate — BUILT-IN G0-G6 gate scoring (engine-native, single-entry).")
    print("")
    print("usage:")
    print("  anima evaluate <ckpt> [--corpus <path>...] [--gen N]")
    print("")
    print("  mount ANY ckpt through the generator L3 mouth (file-format dispatched) and")
    print("  score G0-G6 with the engine's OWN ops (numpy math.log mirror, torch-free).")
    print("  closure a7b_pass = G0 ∧ G1 ∧ G2.")


def evaluate_corpus(argv):
    """Collect every token after "--corpus" up to the next flag (mirrors hexa)."""
    paths = []
    i = 0
    while i < len(argv):
        if argv[i] == "--corpus":
            j = i + 1
            while j < len(argv):
                a = argv[j]
                if a.startswith("--"):
                    break
                paths.append(a)
                j += 1
            i = j
        else:
            i += 1
    return paths


def evaluate_intval(argv, flag, dflt):
    """Value after `flag` parsed as int, or `dflt` if absent."""
    i = 0
    while i < len(argv):
        if argv[i] == flag and i + 1 < len(argv):
            return int(argv[i + 1])
        i += 1
    return dflt


def _pf(passed):
    return "🟢 PASS" if passed else "🔴 FAIL"


def _yn(ok):
    return "✅" if ok else "⏳"


# ══════════════════════════════════════════════════════════════════════════════
#  EVALUATE — BUILT-IN G0-G6 gate scoring (core/g_gates.py, single entry)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima evaluate <ckpt> [--corpus <path>...] [--gen N]` — import g_gates.g_eval_all and
# score the full G0-G6 battery through the generator L3 mouth (engine-native, torch-
# free). Output mirrors the hexa `anima evaluate` table + the g_gates _fmt block, so a
# direct `python3 core/g_gates.py <ckpt> ...` and this single entry are byte-identical.

def evaluate_run(argv):
    """argv = ["<ckpt>", "--corpus ...", "--gen N"]."""
    if len(argv) < 1:
        evaluate_usage()
        return 2
    # import the engine module lazily so usage/help never need core/ deps.
    import g_gates

    ckpt = argv[0]
    corpus = evaluate_corpus(argv[1:])
    gen = evaluate_intval(argv[1:], "--gen", 40)

    # cheap header-sniff for the mouth label (mirrors hexa gen_mouth_kind) — do NOT
    # construct _Mouth here (it eagerly loads weights and raises on a non-decodable
    # ckpt before g_eval_all runs).
    if g_gates.bg.bg_is_bytegpt(ckpt):
        mouth_kind = "bytegpt"
    elif g_gates.clm.clm_decodable(ckpt):
        mouth_kind = "clm"
    else:
        mouth_kind = "unknown"

    print("=== anima evaluate — BUILT-IN G0-G6 gate scoring (engine-native, single-entry) ===")
    print("ckpt:   " + ckpt + "  (mouth: " + mouth_kind + ")")
    cnote = "(none — G2 novelty needs a corpus)"
    if corpus:
        cnote = str(len(corpus)) + " file(s)"
    print("corpus: " + cnote)
    print("gen:    " + str(gen) + " tokens/decode  (frozen bars · ARCHITECTURE.json frozen SSOT)")
    print("")

    r = g_gates.g_eval_all(ckpt, corpus, gen)
    g0 = r["g0"]; g1 = r["g1"]; g2 = r["g2"]
    g3 = r["g3"]; g5 = r["g5"]; g6 = r["g6"]

    print("gate                              verdict   detail")
    print("  ──────────────────────────────────────────────────────────────────")
    print("  G0 COHERENCE     " + _pf(bool(g0["pass"]))
          + "  kwr>=0.50 on " + str(g0["n_coherent"]) + "/5 (need >=4)")
    print("  G1 RECOMBINATION " + _pf(bool(g1["pass"]))
          + "  best_distinct=" + str(g1["best_distinct"]) + " > max_single=" + str(g1["max_single"])
          + " (need >=2 & >max_single)")
    g2detail = ("novel=" + str(g2["n_novel"]) + " (need>=3) · control=" + str(g2["control_novel"])
                + " (need 0) · coherent=" + str(g2["coherent"]))
    print("  G2 NOVELTY       " + _pf(bool(g2["pass"])) + "  " + g2detail)
    print("  G3 PHILOSOPHY    " + _yn(bool(g3["ok"])) + " (read)"
          + "  continuity=" + ("%.6f" % g3["continuity"]) + " · impostor="
          + ("%.6f" % g3["impostor_cos"]) + " (architecture, not a decode score)")
    print("  G4 PROVENANCE    — N/A    "
          + "HF/recovery = process gate (a_hf_* / a_fire_recover_complete), out of eval scope")
    g5detail = "L1 fab=" + ("%.4f" % g5["l1_rate"]) + " (<=0.30) · L2=" + str(g5["l2_note"])
    print("  G5 NON-FAB       " + _pf(bool(g5["l1_pass"])) + "  " + g5detail)
    print("  G6 IDEATION ★    " + _pf(bool(g6["pass"]))
          + "  distinct=" + str(g6["dist"]) + " (need>=5) · falsifiable=" + str(g6["fals"])
          + " (need>=1) · frame-leaks=" + str(g6["frame_leaks"]))
    print("  ──────────────────────────────────────────────────────────────────")
    closed = bool(r["closure"])
    print("")
    print("CLOSURE (a7b_pass = G0 ∧ G1 ∧ G2): " + _pf(closed))
    if closed:
        print("  → PUBLIC-eligible (G0∧G1∧G2 all PASS).")
    else:
        print("  → NOT closure (PRIVATE/WIP) — closure needs G0∧G1∧G2 all PASS.")
    return 0


def main(argv):
    if len(argv) >= 1 and argv[0] in ("-h", "--help"):
        evaluate_usage()
        return 0
    return evaluate_run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
