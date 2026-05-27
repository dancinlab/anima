<!-- ai:meta
schema: anima.doc.landed.v1
bg_lane: BG-NEXUS-KICK-3
stage: stage_2_prep
ts_utc: 2026-05-05T11:50:25Z
spec_ref: docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md
verdict_ref: state/anima_core_dialogue_stage_2_prep_2026_05_05/verdict.json
no_commit: true
no_exec: true
-->

# Anima Core Dialogue — Stage 2 Prep Landed (2026-05-05)

## §1 Scope

Stage 2 prep of the emerge dialogue roadmap (spec §8 stage 2). $0, mac-local, no exec, no commit.
Lands the dispatcher + REPL infrastructure so that Stage 1 mount (NEXUS-KICK-1) can be fired
immediately on landing without further glue work.

## §2 Deliverables

| Artifact | Path | Status |
|---|---|---|
| CLI hexa dispatcher | `tool/anima_cli/dialogue.hexa` | landed |
| Bash REPL wrapper   | `bin/anima-core-dialogue.bash` (chmod +x) | landed |
| Session log root    | `state/anima_core_dialogues/`            | created |
| Verdict             | `state/anima_core_dialogue_stage_2_prep_2026_05_05/verdict.json` | landed |
| Companion (this doc)| `docs/anima_core_dialogue_stage_2_prep_landed_2026_05_05.ai.md` | landed |

## §3 CLI integration

The existing `bin/anima` top-level dispatcher routes `anima <topic>` to
`tool/anima_cli/<topic>.hexa` automatically (no patch required to `bin/anima`).
Adding `tool/anima_cli/dialogue.hexa` therefore enables `anima dialogue ...`
without further glue.

Verbs:

```
anima dialogue                                      topic-level help
anima dialogue --selftest                           readiness probe
anima dialogue --substrate clm-v4 --probe "text"    one-shot (Stage 1 dep)
anima dialogue --substrate clm-v4 --interactive     REPL  (Stage 1 dep)
```

The standalone wrapper provides the same surface for direct shell invocation:

```
bin/anima-core-dialogue.bash --selftest
bin/anima-core-dialogue.bash --probe "text"
bin/anima-core-dialogue.bash --interactive
```

## §4 Session log infrastructure

Per-session JSONL at `state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>.jsonl`,
schema `anima.dialogue.v1`, line kinds:

- `session_start`        — once, at REPL/probe entry
- `user_turn`            — user input text
- `substrate_turn`       — phi-star + axis activation + dominant cells + hidden-state delta (mount emit verbatim)
- `session_end`          — once, on REPL exit
- `session_summary`      — aggregated mean phi-star, drift min/max, n_turns

The bash wrapper carries:
- session log creation + idempotent append
- JSON-string escape for user input
- awk-based session summary aggregation on exit
- INT/TERM trap finalization

## §5 Pre-Stage-1 verification

```
$ bin/anima-core-dialogue.bash --selftest
verdict: STAGE_2_READY (awaiting Stage 1 mount)
exit=0

$ bin/anima-core-dialogue.bash --probe "test"
anima-core-dialogue --probe: stage_1_pending
exit=3

$ anima dialogue --selftest
verdict: STAGE_2_READY (awaiting Stage 1 mount)
exit=0
```

The `stage_1_pending` guard fires as designed when
`anima-core/runtime/clm_v4_mount.hexa` is absent.

## §6 Fire recipe after Stage 1 lands

```
anima dialogue --selftest                       # expect verdict: READY
bin/anima-core-dialogue.bash --interactive      # REPL opens; substrate-coupled dialogue begins
```

## §7 Honest C3 (raw#10, ≥5)

See `verdict.json -> honest_c3` (8 caveats):
C1 stage_1_pending until mount lands  |  C2 metric is anima-internal heuristic  |
C3 session schema provisional pending mount emit format  |  C4 REPL stdin carried by bash, not hexa  |
C5 phi-star baseline 41.86 hard-coded  |  C6 dominant_cells heuristic deferred to mount  |
C7 chat-capability not promised  |  C8 session_summary awk parsing fragile to schema drift.

## §8 Compliance

- raw#9   hexa+bash carve-out: dispatcher is hexa, REPL glue is bash, no .py introduced
- raw#10  ≥5 honest C3: 8 caveats listed
- raw#11  snake_case throughout
- raw#15  no-hardcode: ANIMA env / git-root / `_resolve_root` patterns
