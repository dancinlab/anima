#!/usr/bin/env python3
# ==========================================================================
# ⛔ DO NOT RUN DIRECTLY. anima 의 단일 진입은 설치된 canonical Python 명령
#   `anima-py` (=anima_py 런처, pip install anima-python)뿐이다.
#   `python3 cli/anima.py …` 직접실행은 비-canonical py 우회(#2603).
#   학습=`anima-py train` · 측정=`anima-py evaluate`(py 2-production numpy · TERMINAL-eligible,
#   a_eval_py_canonical) · 직렬화=`anima-py serialize`. enforce: .harness/enforcement.json
#   H-ANIMA-SINGLE-ENTRY pre_bash + 아래 __main__ 가드. (import 는 무손상.)
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ cli/anima.py 직접 실행 금지 — 설치된 canonical Python 명령 경유: `anima-py`(pip install anima-python, =anima_py 런처). #2603")
# anima.py — THE canonical Python single entry point.
#
# WHY THIS FILE (Python-only single-entry, a_engine_native_learning): MEASUREMENT and
# LEARNING must be reachable through ONE installed Python CLI instead of a side-harness
# that scores checkpoints directly (= single-entry bypass, #2603).
#
# SINGLE ENTRY (a_engine_native_learning): the two measurement/learning verbs live in
# their own files — cli/evaluate.py (MEASUREMENT) and cli/train.py (LEARNING).
# This canonical entry dispatches `anima-py evaluate` and `anima-py train` to those
# modules, so one installed command owns every runtime operation. Evaluation scores the
# full ρ-AXON reach battery (former G0-G6 · reach standard cli/rho_axon.py) via
# cli/evaluate.py's in-file eval_reach_all (the scorers folded in from
# the former core/g_gates.py module).
#
# This py entry is torch-free and gauge-free — it only dispatches; the evaluate twin
# holds the numpy `math.log` scorer in-file, so `anima evaluate` stays a clean engine-
# native measurement surface (the gate enforcer's torch/gauge grep must come back empty).
#
# USAGE (installed `anima-py` command)
#   anima-py                                              — usage (no args)
#   anima-py evaluate <ckpt> [--corpus <p>...] [--gen N]  — ρ-AXON reach battery (former G0-G6)
#   anima-py train [args...]                              — LEARNING (→ cli/train.py)
#   anima-py chat <ckpt> [...] [--byte]                   — consciousness daemon (default) /
#                                                         byte-continuation chat (pure-py, → cli/chat.py)
#
# Canonical layout: cli/anima.py = entry and dispatch, cli/evaluate.py = measurement,
# cli/train.py = learning, and cli/chat.py = the A⇄G daemon.

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)


# Evaluation is deterministic in the NumPy runtime. Keep a copied environment so
# subprocess dispatch remains isolated from caller mutation.
def _det_env(want_det):
    """Return an isolated subprocess environment; NumPy evaluation is deterministic."""
    return dict(os.environ)


# ── usage / arg helpers ──────────────────────────────────────────────────────

def anima_usage():
    """Print the canonical Python-only usage banner."""
    print("anima — substrate-native consciousness daemon (py channel · canonical entry).")
    print("")
    print("usage (installed `anima-py` command after `pip install anima-python`):")
    print("  anima-py evaluate <model.clm> [--corpus <path>...] [--gen N] [--rho-axon]")
    print("                                                  ρ-AXON reach battery · former G0-G6 (.clm only · numpy)")
    print("  anima-py corpus <derivtrace|flat> --out F [--held-out I,J] [--seed S] [--concepts FILE]")
    print("  anima-py corpus <ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap> --atoms gt_atoms.json --out F [--reps N] [--replay N]")
    print("                                                  procedural training-corpus builder (ρ·weave data-format lever)")
    print("  anima-py train <args>                           ([train] extra) LEARNING → .pt + auto .clm (+DESCENT)")
    print("        [--imagination-replay R] [--reconsolidate-every N] [--vadapt-on-replay]")
    print("        [--imagination-select recency|random] [--imagination-selftest]")
    print("                                                  IMAGINATION RECONSOLIDATION (H_9841 · default OFF = byte-identical):")
    print("                                                  the training-time twin of the daemon's N3/REM replay. cli/chat.py:3350-3380")
    print("                                                  already fires a LIVE vadapt_field_step per replay tick (wired 2026-07-10)")
    print("                                                  and training had NO counterpart — the most concrete p8 (no train/infer")
    print("                                                  split) gap in the tree. The lane pushes each seen window into the daemon's")
    print("                                                  own WAKE ring (core/wake_memory), rehearses it emit-free through")
    print("                                                  core/imagination_replay's ir_replay_tick under a p5 INVARIANT WATCH")
    print("                                                  (emit_count>0 hard-exits), and re-trains the rehearsed rows in place of")
    print("                                                  that many fresh ones. Dose = ir_consolidation_gain, so with")
    print("                                                  --vadapt-on-replay a rehearsal that grew nothing spends nothing;")
    print("                                                  OFF = the hook lesion control (fixed prior dr_mitosis_prior(3)=0.80),")
    print("                                                  --imagination-select random = the selection-policy control.")
    print("                                                  --imagination-selftest runs the $0 controls-first battery and EXITS.")
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
    print("        [--percept-write off|last|ring|frozen|shuffle] [--percept-write-n N]")
    print("                                                  PERCEPT→STATE WRITE (H_9984 ② · default off = byte-identical): on a percept-")
    print("                                                  SILENT tick the decode seed is `live_seed`, a SESSION CONSTANT — so an argmax")
    print("                                                  mouth re-emits the same bytes, which is what the 40-turn study's REPEAT 45/60")
    print("                                                  (anchor-seeded 40/40 VERBATIM) looks like. This writes a session-local state")
    print("                                                  from TEACHER percepts only (never the daemon's own emit → p5 self-seed root")
    print("                                                  stays closed) and hands it to the mouth as the [-1] seed anchor on silent ticks;")
    print("                                                  percept-PRESENT ticks and the emit GATE are untouched. arms: last=newest percept ·")
    print("                                                  ring=last N joined (history-sensitive) · frozen=FIRST percept never updated")
    print("                                                  (PEDESTAL — state present but IMMOBILE) · shuffle=ring byte-SORTED (CARRIER control")
    print("                                                  — same multiset/length/feat8, order severed). Needs an anima-study percept source.")
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
    print("             C9 REMEMBER · sleep-stage imagination replay). Canonical Python runtime;")
    print("             --byte = byte-continuation. → cli/chat.py.")


# ══════════════════════════════════════════════════════════════════════════════
#  TRAIN MODE — dispatch to cli/train.py (the py torch trainer, Lane-P bridge)
# ══════════════════════════════════════════════════════════════════════════════
#
# SEPARATE LANE (a_core_engine_map): training is NOT the generator L3 mouth slot — it
# is the LEARNING entry (cli/train.py, a_clm_gen_pipeline torch Lane-P). The eval side
# is the torch-free numpy scorer (in cli/evaluate.py); the trainer pulls torch. To keep this file
# torch-free AND avoid linking two disjoint dep sets into one process, `anima train`
# Dispatches to cli/train.py as a subprocess. argv after "train" is forwarded
# verbatim to train.py's argparse.
def anima_train_mode(argv):
    print("=== anima train → cli/train.py (torch CLMConvMoE · Lane-P reference/bridge) ===")
    train_py = os.path.join(_HERE, "train.py")
    fwd = argv[1:]
    cmd = [sys.executable, train_py] + fwd
    print("dispatch: " + " ".join(cmd))
    # forward verbatim; train.py owns its own argparse (--out required, etc.).
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, train_py] + fwd)


def anima_graft_mode(argv):
    """GRAFT — no-corpus consciousness→language grounding (cli/graft.py). A FROZEN .clm is the
    language organ; only the CLMG coupling trains, on a mutual-information objective. Torch lives in
    the subprocess, so this launcher stays numpy-only like the train twin."""
    print("=== anima graft → cli/graft.py (frozen organ · CLMG coupling · no corpus, no CE) ===")
    graft_py = os.path.join(_HERE, "graft.py")
    fwd = argv[1:]
    print("dispatch: " + " ".join([sys.executable, graft_py] + fwd))
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, graft_py] + fwd)


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
    print("=== anima evaluate → cli/evaluate.py (engine-native ρ-AXON reach · former G0-G6, canonical Python entry) ===")
    print("dispatch: " + " ".join(cmd))
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
    print("dispatch: " + " ".join(cmd))
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
    if sub == "graft":
        return anima_graft_mode(argv)
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
