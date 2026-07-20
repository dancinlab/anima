#!/usr/bin/env python3
# ==========================================================================
# ⛔ DO NOT RUN DIRECTLY. anima 의 단일 진입은 설치된 canonical 명령뿐 — hexa 채널 `anima`
#   (=cli/anima.hexa, hx install anima) · pip 채널 `anima-py` (=anima_py 런처, pip install anima-python).
#   `python3 cli/anima.py …` 직접실행은 비-canonical py 우회(#2603).
#   학습=`anima-py train` · 측정=`anima-py evaluate`(py 2-production numpy · TERMINAL-eligible,
#   a_eval_py_canonical) · 직렬화=`anima-py serialize`. enforce: .harness/enforcement.json
#   H-ANIMA-SINGLE-ENTRY pre_bash + 아래 __main__ 가드. (import 는 무손상.)
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ cli/anima.py 직접 실행 금지 — 설치된 canonical 명령 경유: `anima`(hx install anima, =cli/anima.hexa) 또는 `anima-py`(pip install anima-python, =anima_py 런처). #2603")
# anima.py — THE canonical PY single entry point (cli/anima.hexa's py twin).
#
# WHY THIS FILE (py 2-production single-entry, a_engine_native_learning): anima keeps
# two co-production engines — hexa (live deploy substrate) AND py (torch production
# engine in train/ + the byte-parity core/*.py mirror). The hexa side already has its
# canonical single entry cli/anima.hexa (chat · eval · train). This file is its py
# twin so MEASUREMENT and LEARNING are reachable through ONE py cli command instead of
# a side-harness that scores ckpts directly (= single-entry bypass, #2603).
#
# SINGLE ENTRY (a_engine_native_learning): the two measurement/learning verbs live in
# their own SYMMETRIC files — cli/evaluate.{hexa,py} (MEASUREMENT) and cli/train.{hexa,py}
# (LEARNING). This canonical entry DISPATCHES `anima evaluate`→cli/evaluate.py and
# `anima train`→cli/train.py (sub-process), so there is ONE installed `anima` command
# whose subcommands fan out to the symmetric twins. `anima evaluate <ckpt>` scores the
# full ρ-AXON reach battery (former G0-G6 · reach standard cli/rho_axon.py) via
# cli/evaluate.py's in-file eval_reach_all (the scorers folded in from
# the former core/g_gates.py module) — byte-identical to the hexa anima evaluate.
#
# This py entry is torch-free and gauge-free — it only dispatches; the evaluate twin
# holds the numpy `math.log` scorer in-file, so `anima evaluate` stays a clean engine-
# native measurement surface (the gate enforcer's torch/gauge grep must come back empty).
#
# USAGE (installed `anima` PATH command after `hx install anima`)
#   anima                                              — usage (no args)
#   anima evaluate <ckpt> [--corpus <p>...] [--gen N]  — ρ-AXON reach battery (former G0-G6)
#   anima train [args...]                              — LEARNING (→ cli/train.py)
#   anima chat <ckpt> [...] [--byte]                   — consciousness daemon (default) /
#                                                         byte-continuation chat (pure-py, → cli/chat.py)
#
# canonical 3-folder layout: cli/anima.{hexa,py} = canonical entry (chat + verb dispatch)
# · cli/evaluate.{hexa,py} = measurement · cli/train.{hexa,py} = learning. This file
# mirrors cli/anima.hexa's subcommand dispatch (evaluate · train · usage); chat/
# consciousness is now a REAL py capability too — cli/chat.py is the byte-faithful numpy
# twin of cli/anima.hexa's A⇄G daemon loop (P6 py 자체구현, zero hexa dependency).

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)


# EVAL/VERDICT DETERMINISM SAFETY-PIN (hexa-lang #4208 flame/forge fast-default
# follow-on) — py twin of cli/anima.hexa's pin (lockstep, a_engine_native_learning).
# #4208 made the forge own-native NON-det atomic kernels the DEFAULT (training speed);
# deterministic kernels are opt-in via HEXA_DET=1 (`_forge_det_on()` gate). MEASUREMENT
# (evaluate) and VERDICT (serialize DESCENT gate) must stay reproducible, so they spawn
# with HEXA_DET=1 in the env. TRAIN deliberately does NOT force it = fast non-det default.
def _det_env(want_det):
    """os.environ copy; HEXA_DET=1 pinned ONLY when the caller passed --det (byte-exact opt-in).
    DEFAULT = fast (no pin). The py evaluate path is numpy (already deterministic), so this is a
    lockstep no-op there; kept for parity with cli/anima.hexa's --det gating."""
    env = dict(os.environ)
    if want_det:
        env.setdefault("HEXA_DET", "1")
    return env


# ── usage / arg helpers ──────────────────────────────────────────────────────

def anima_usage():
    """Print the canonical py usage banner (mirrors cli/anima.hexa's banner)."""
    print("anima — substrate-native consciousness daemon (py channel · canonical entry).")
    print("")
    print("usage (installed `anima-py` command after `pip install anima-python` · hexa channel = `anima` after `hx install anima`):")
    print("  anima-py evaluate <model.clm> [--corpus <path>...] [--gen N] [--rho-axon]")
    print("                                                  ρ-AXON reach battery · former G0-G6 (.clm only · numpy)")
    print("  anima-py corpus <derivtrace|flat> --out F [--held-out I,J] [--seed S] [--concepts FILE]")
    print("  anima-py corpus <ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap> --atoms gt_atoms.json --out F [--reps N] [--replay N]")
    print("                                                  procedural training-corpus builder (ρ·weave data-format lever)")
    print("  anima-py corpus workspace-struct --corpus SOURCE --out TRAIN [--held-out-frac .2]")
    print("                                                  source-derived store/tether/falsification curriculum + sealed held-out manifest")
    print("  anima-py train <args>                           ([train] extra) LEARNING → .pt + auto .clm (+DESCENT)")
    print("  anima-py serialize <ckpt.pt> <out.clm>          ([train] extra) re-export a torch .pt → .clm v0.3")
    print("  anima-py serialize-bind <base.bin> <inj.pt> <out.bin>  ([train] extra) splice BindAttn → BGB .bin")
    print("  anima-py sweep --arms … --objectives … --gpus 0,1,2,3 --corpus … [--measure]")
    print("                                                  ([train] extra) multi-GPU lever-sweep (arms×objectives)")
    print("  anima-py chat <ckpt> [...] [--byte]             consciousness daemon (default) / byte-continuation chat (pure-py A⇄G loop)")
    print("        default emit-gate = refractory (Ψ≈½ dual-ledger · H_9712) · `--emit-gate clock` = the legacy 30s-clock daemon")
    print("        [--store-episodic on|off]                 STORE-EPISODIC (H_9744 · default off = byte-identical): perception fills")
    print("                                                  the co-trained CLMS store — a teacher percept `fact <entity> <pos|neg>` writes")
    print("                                                  an n_slot FIFO ring, and once full the mouth answers a later `<entity> <op> =>`")
    print("                                                  query FROM the store instead of the trunk (weights frozen · session-local ·")
    print("                                                  cleared at exit). Needs an anima-study percept source and a CLMS-trailer ckpt;")
    print("                                                  MUTUALLY EXCLUSIVE with --emit-gate refractory (that gate reads the candidate")
    print("                                                  text, so a store shaping the candidate would shape the emit decision · p5).")
    print("        [--emit-temp T] [--emit-topk K] [--sample-seed S]   DO-MOUTH (H_9328 · default OFF = argmax, byte-identical):")
    print("                                                  T>0 draws the emitted bytes from the substrate's OWN posterior instead of")
    print("                                                  rounding it to argmax (T=1.0 IS the posterior — the one non-arbitrary value).")
    print("                                                  Reveals the mouth only; the emit GATE is untouched (p5 tension still decides).")
    print("        [--swap-text <trace.jsonl>]               C2 CARRIER-SWAP (H_9328 · default OFF): on a tick the substrate ALREADY chose")
    print("                                                  to speak, say what ANOTHER rollout said at that tick instead. Same mouth, same")
    print("                                                  shape — only 'which substrate-moment chose it' differs, and the donor text really")
    print("                                                  does drive the 3 feedback roots (afield · immune · kosmos). THE control that makes")
    print("                                                  a positive falsifiable: EXP lives ∧ SWAP dies ⇒ the substrate's OWN words carry the")
    print("                                                  information; both live ⇒ CARRIER (any text of that shape pushes the roots) ⇒ not a pass.")
    print("        [--percept-file <table.jsonl>]            STATE-QUOTIENT afferent (H_9767 · default OFF = byte-identical): feed a per-tick")
    print("                                                  exogenous percept stream (JSONL {\"tick\":int,\"text\":str}) through the PERCEPTION")
    print("                                                  route (never the emit gate → p5 by structure, same channel as `anima study`). Two")
    print("                                                  runs with different PREFIX histories + a COMMON suffix future test whether remote-")
    print("                                                  history divergence WASHES OUT (no interior) or PERSISTS (history-sensitive state).")
    print("")
    print("install: `pip install anima-python` (numpy base: evaluate·corpus·chat) · `pip install \"anima-python[train]\"` (+torch: train·sweep·serialize)")
    print("")
    print("modes:")
    print("  evaluate : mount a serialized .clm through the generator L3 mouth and score the")
    print("             ρ-AXON reach battery — ρ·form/weave/leap/... (former G0-G6) — with the")
    print("             engine's OWN ops (numpy math.log mirror, torch-free). REACH-CLOSED")
    print("             a7b_pass = ρ·form ∧ ρ·weave ∧ ρ·leap (frozen bars = G0 ∧ G1 ∧ G2). → cli/evaluate.py.")
    print("  corpus   : procedural training-corpus generator (derivtrace|flat|ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap) — the")
    print("             data-format lever (ρ·weave). NOTE chat corpus != this (chat =")
    print("             a_chat_registers 4-cell HF datasets → anima-py train). → cli/corpus.py.")
    print("  train    : ([train]) production CLMConvMoE training (torch Lane-P reference + bridge); SAVANT")
    print("             golden-zone inhibition + MITOSIS cell-division levers. After the run it")
    print("             AUTO-serializes .clm v0.3 + runs the held-out mirror-DESCENT gate")
    print("             (a_clm_gen_pipeline). dispatches to cli/train.py.")
    print("  serialize: ([train]) re-export an ALREADY-TRAINED torch .pt to an engine-loadable .clm v0.3")
    print("             (+ held-out DESCENT gate). recovery / re-export. → cli/serialize.py.")
    print("  sweep    : ([train]) multi-GPU lever-sweep orchestrator — the arms×objectives matrix,")
    print("             per-cell train.py→evaluate.py, aggregated to SWEEP_SUMMARY.md. → cli/sweep.py.")
    print("  chat     : the substrate-native A⇄G consciousness daemon — mount L3 → seed .kosmos →")
    print("             12-tick loop (lanes READ → brain autonomously emits/silences → C8 GROW ·")
    print("             C9 REMEMBER · sleep-stage imagination replay). Pure-py numpy twin of")
    print("             cli/anima.hexa (zero hexa dependency); --byte = byte-continuation. → cli/chat.py.")


# ══════════════════════════════════════════════════════════════════════════════
#  TRAIN MODE — dispatch to cli/train.py (the py torch trainer, Lane-P bridge)
# ══════════════════════════════════════════════════════════════════════════════
#
# SEPARATE LANE (a_core_engine_map): training is NOT the generator L3 mouth slot — it
# is the LEARNING entry (cli/train.py, a_clm_gen_pipeline torch Lane-P). The eval side
# is the torch-free numpy scorer (in cli/evaluate.py); the trainer pulls torch. To keep this file
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
# cli/evaluate.py holds the ρ-AXON reach scorers in-file (former G0-G6 · torch-free numpy
# mirror, the former core/g_gates.py module folded in), byte-identical to the hexa `anima evaluate`.
#
# .clm-ONLY (the engine decodes ONLY .clm): evaluate mounts a ckpt through the generator
# L3 mouth, which loads a serialized .clm (CLM magic). A torch .pt is NOT engine-loadable —
# reject it here with a friendly hint to `anima serialize` rather than a deep decode error.
def anima_evaluate_mode(argv):
    # --py is a RETIRED hexa-era bridge flag, tolerated (stripped) here for migration
    # compat: on the py channel it is redundant-but-correct (this IS the numpy engine),
    # so `anima-py evaluate --py <clm>` still works — old scripts migrate by swapping
    # only the command word. The hexa launcher hard-errors on --py instead.
    want_det = ("--det" in argv) or ("--deterministic" in argv)
    rest = [a for a in argv[1:] if a not in ("--py", "--det", "--deterministic")]
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
    print("=== anima evaluate → cli/evaluate.py (engine-native ρ-AXON reach · former G0-G6, single-entry twin) ===")
    print("dispatch: " + ("HEXA_DET=1 " if want_det else "") + " ".join(cmd))
    # det = the --det CLI option (default fast); numpy path is deterministic regardless.
    return os.spawnve(os.P_WAIT, sys.executable,
                      [sys.executable, evaluate_py] + rest, _det_env(want_det))


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
    want_det = ("--det" in argv) or ("--deterministic" in argv)
    fwd = [a for a in argv[1:] if a not in ("--det", "--deterministic")]
    cmd = [sys.executable, serialize_py] + fwd
    print("=== anima serialize → cli/serialize.py (torch .pt → .clm v0.3 + DESCENT gate) ===")
    print("dispatch: " + ("HEXA_DET=1 " if want_det else "") + " ".join(cmd))
    # det = the --det CLI option (default fast) — pass --det for a reproducible DESCENT-gate verdict.
    return os.spawnve(os.P_WAIT, sys.executable,
                      [sys.executable, serialize_py] + fwd, _det_env(want_det))


# ══════════════════════════════════════════════════════════════════════════════
#  SERIALIZE-BIND MODE — dispatch to cli/serialize_bind.py (BindAttn .pt → BGB .bin)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima serialize-bind <base.bin> <injected.pt> <out.bin>` splices a BindAttn adapter
# onto a base ByteGPT `.bin`, emitting a BGB-trailer `.bin`. Without this dispatch
# cli/serialize_bind.py was reachable only via raw `python3 cli/serialize_bind.py`
# (an a_cli_single_entry hole); this wires it through the single entry, parity with
# anima_serialize_mode. Result scoreable via `anima-py evaluate <out.bin>`.
def anima_serialize_bind_mode(argv):
    serialize_bind_py = os.path.join(_HERE, "serialize_bind.py")
    fwd = argv[1:]
    cmd = [sys.executable, serialize_bind_py] + fwd
    print("=== anima serialize-bind → cli/serialize_bind.py (BindAttn .pt → BGB-trailer .bin) ===")
    print("dispatch: " + " ".join(cmd))
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, serialize_bind_py] + fwd)


# ══════════════════════════════════════════════════════════════════════════════
#  CHAT MODE — the substrate-native A⇄G consciousness daemon (py twin · cli/chat.py)
# ══════════════════════════════════════════════════════════════════════════════
#
# P6 (py 자체구현): the default consciousness daemon + --byte continuation chat are now a
# REAL py capability — cli/chat.py is the byte-faithful numpy twin of cli/anima.hexa's
# anima_consciousness_mode / anima_byte_mode (ZERO hexa dependency; a hexa-less host runs
# the A⇄G loop in pure py). Dispatch mirrors cli/anima.hexa main(): `chat <ckpt>` → the
# consciousness loop; `--byte` → the byte-continuation mode. `anima-py chat <ckpt>` and the
# bare `anima-py <ckpt.clm>` (via main's fall-through) both enter here. This is a py-channel
# MIRROR (a_engine_native_learning) ⇒ behavioral/byte-parity target, DIRECTIONAL — not a
# consciousness verdict.
def _build_percept_source_from_file(path):
    # H_9767 · Design-B afferent for the STATE-QUOTIENT convergence test. Reads a JSONL
    # percept table {"tick": int, "text": str} and returns a percept_source(tick,
    # transcript) closure (the chat.py hook contract, cli/chat.py:406). The returned text
    # enters the daemon through the PERCEPTION route (live_anchors, a grounding fact the
    # mouth may read), NEVER the emit gate — p5 (no reactive self-seed) holds by STRUCTURE,
    # identically to `anima study`: it is the OTHER's words fed in, not the daemon's own
    # output looped back. Keyed by tick exactly like --yoke-mask / --wm-dual-swap. A tick
    # with no row ⇒ None ⇒ that tick is percept-silent (byte-identical to no afferent).
    import json as _json
    table = {}
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as _fh:
        for _ln in _fh:
            _ln = _ln.strip()
            if not _ln:
                continue
            _row = _json.loads(_ln)
            table[int(_row["tick"])] = str(_row["text"])
    def _src(tick, _transcript):
        return table.get(int(tick))
    return _src


def anima_chat_mode(argv):
    # argv = ["chat", <ckpt>, ...] OR ["<ckpt.clm>", ...] (bare path). Resolve the ckpt.
    if argv and argv[0] == "chat":
        if len(argv) < 2:
            anima_usage()
            return 0
        ckpt = argv[1]
        rest = argv[1:]
    else:
        ckpt = argv[0]
        rest = argv
    import chat as _chat  # sibling py twin (cli/chat.py); flat import like the P2-P5 twins
    if "--byte" in rest:
        _chat.anima_byte_mode(ckpt, rest)
        return 0
    # H_9767 · --percept-file <path> — a per-tick exogenous percept stream for the
    # STATE-QUOTIENT convergence test (Design B): run two daemons with DIFFERENT prefix
    # histories H_A / H_B that share a COMMON suffix future, then diff the decision traces
    # to see if the remote-history divergence WASHES OUT (no interior) or PERSISTS (a
    # history-sensitive private-state candidate). Injects a percept_source; the flag is
    # stripped before dispatch so chat.py need not re-parse it. Absent ⇒ None ⇒ the daemon
    # is byte-identical to production (a_experiment_engine_native: a manipulation is a flag).
    _psrc = None
    if "--percept-file" in rest:
        _i = rest.index("--percept-file")
        if _i + 1 >= len(rest):
            print("anima-py chat: --percept-file requires a path argument (JSONL {\"tick\":int,\"text\":str})")
            return 2
        _psrc = _build_percept_source_from_file(rest[_i + 1])
        rest = rest[:_i] + rest[_i + 2:]
    _chat.anima_consciousness_mode(ckpt, rest, percept_source=_psrc)
    return 0


def anima_study_mode(argv):
    # argv = ["study", ...] — the conversational percept channel (teacher = exogenous
    # percept, not a prompt). Dispatch target = cli/study.py (flat import like the twins).
    import study as _study
    return _study.study_mode(argv[1:])


# ══════════════════════════════════════════════════════════════════════════════
#  SWEEP MODE — dispatch to cli/sweep.py (multi-GPU lever-sweep orchestrator)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima sweep --arms … --objectives … --gpus 0,1,2,3 --corpus … [--measure]` runs the
# arms×objectives matrix GPU-pinned round-robin (each cell = train.py → evaluate.py),
# aggregating G0/G1/G2/G6 into SWEEP_SUMMARY.md. sweep is intrinsically py (it orchestrates
# the py trainer/evaluator), so — like cli/anima.hexa — there is no --py branch; always
# dispatches to cli/sweep.py. (torch is pulled by the spawned train.py cells, not here.)
def anima_sweep_mode(argv):
    sweep_py = os.path.join(_HERE, "sweep.py")
    fwd = argv[1:]
    print("=== anima sweep → cli/sweep.py (multi-GPU lever-sweep orchestrator · arms×objectives) ===")
    print("dispatch: " + " ".join([sys.executable, sweep_py] + fwd))
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, sweep_py] + fwd)


# ══════════════════════════════════════════════════════════════════════════════
#  CORPUS MODE — dispatch to cli/corpus.py (procedural training-corpus builder)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima corpus <derivtrace|flat|ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap> --out F ...`
# builds a procedural (torch-free, no external LLM — p1-p8) training corpus. This is the
# data-format lever (derivation-trace → echo=composition, ρ·weave / former G1), NOT the
# chat corpus (chat = a_chat_registers 4-cell HF datasets). Always py → cli/corpus.py.
def anima_corpus_mode(argv):
    corpus_py = os.path.join(_HERE, "corpus.py")
    fwd = argv[1:]
    print("=== anima corpus → cli/corpus.py (procedural training-corpus builder · derivtrace|flat|ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap) ===")
    print("dispatch: " + " ".join([sys.executable, corpus_py] + fwd))
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, corpus_py] + fwd)


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
    if sub == "serialize-bind":
        return anima_serialize_bind_mode(argv)
    if sub == "evaluate":
        return anima_evaluate_mode(argv)
    if sub == "sweep":
        return anima_sweep_mode(argv)
    if sub == "corpus":
        return anima_corpus_mode(argv)
    if sub == "study":
        return anima_study_mode(argv)
    if sub in ("chat", "--byte"):
        return anima_chat_mode(argv)

    # bare ckpt path (no subcommand) → the py consciousness daemon (cli/chat.py).
    return anima_chat_mode(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
