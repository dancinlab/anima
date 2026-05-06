# anima cli mk2 — Phase 2 dialogue REPL landed (2026-05-06)

Companion verdict: state/anima_cli_mk2_2026_05_06/phase_2_dialogue_repl_verdict.json

## Scope

tool/anima_cli/dialogue.hexa Phase 2:
1. native --interactive REPL (readline loop) replaces stub
2. mount.hexa --probe stdout parser (phi_star / drift / axes / dom / delta)
3. JSONL session log emit (anima.dialogue.v1) — start/user/substrate/end/summary
4. --probe one-shot path also auto-logs to daily session JSONL
5. --selftest extends to 5-turn synthetic conversation
6. raw#9/raw#10/raw#15 + own 17 정합 유지

## What changed

### tool/anima_cli/dialogue.hexa  (294 → 612 LoC, +318)

Added modules:

- mount probe + parser (`_probe_and_parse`, `_extract_phi_star`,
  `_extract_phi_drift`, `_extract_axes`, `_extract_dominant_cells`,
  `_extract_hidden_delta`)
- session log emitters (`_ensure_session_log`, `_log_user_turn`,
  `_log_substrate_turn`, `_log_session_end`, `_emit_session_summary`)
- sub_interactive(argv) — native readline REPL
- sub_probe(argv) — auto-log to daily session JSONL
- sub_selftest() — 5-turn synthetic conversation

### Bug fix during validation

drift_pp leading `+` was emitted as JSON-illegal `"phi_star_drift_pp":+0.0017`
and not matched by awk regex `[-0-9.]+` in summary aggregation. Fixed by
stripping leading `+` in `_extract_phi_drift` before JSONL emit.

## Validation (5-turn + 4 integration tests)

| Test | Verdict | Note |
| --- | --- | --- |
| --selftest 5-turn synthetic | PASS | phi 41.8344 ~ 41.9371 |
| --probe one-shot + auto-log | PASS | 09-27-58.jsonl, 5 lines |
| --interactive 3-turn + /exit | PASS | 09-30-38.jsonl, n_turns=3 |
| --interactive 2-turn + drift sign fix | PASS | drift_max_pp=0.0017 |
| bin/anima dialogue --interactive | PASS | bash dispatcher wire OK |
| blank-line exit | PASS | 09-40-37.jsonl session_end OK |

### 5-turn trajectory (--selftest)

```
phi_star    : 41.8344, 41.9094, 41.8960, 41.8695, 41.9371
dom_first   :     3,       5,       2,       4,       4
top_axis    : agency, temporal, temporal, identity, identity
```

phi-star drift range = [-0.0256, +0.0771] pp from baseline 41.86, well
within paradigm v11 G3 stability window. dom_first / top_axis varying per
prompt = substrate is responding to input (= paradigm D direction signal).

## Session log schema (anima.dialogue.v1)

state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>.jsonl

Lines per session:
- session_start: ts_utc, session_log, phi_star_baseline, substrate, mode
- user_turn: ts_utc, user_input
- substrate_turn: ts_utc, phi_star, phi_star_drift_pp, axis_activation
  (5-key map), dominant_cells (3-int array), hidden_state_delta_l2
- session_end: ts_utc
- session_summary: ts_utc, n_turns, phi_star_mean, phi_star_drift_min_pp,
  phi_star_drift_max_pp

Schema is identical to bin/anima-core-dialogue.bash output, so downstream
tool/anima_cli/dialogue_session_analyzer.hexa is compatible without change.

## anima cli mk2 T1 wire

bin/anima (legacy bash dispatcher) routes `dialogue` topic to
tool/anima_cli/dialogue.hexa. Verified:

```
$ printf '안녕\n/q\n' | ./bin/anima dialogue --interactive
── anima dialogue --interactive ──
session_log : .../2026-05-06/09-37-52.jsonl
> [turn 1] phi=41.8271 drift=-0.0329 top_axis=agency dom=[0,2,6]
> 
[anima dialogue] session summary  n_turns=1  phi_star_mean=41.8271
```

bin/anima.hexa (mk2 schema-driven dispatcher) is print-stub-only — its
exec syscall integration is Phase 1 second sub-cycle (separate landed doc).
User-facing surface is unblocked because bin/anima legacy bash dispatcher
already routes correctly.

## Honest C3 (≥5)

- C1 substrate-as-metric heuristic, no external validation
- C2 phi_star baseline 41.86 hard-coded as drift reference (paradigm v11 G3)
- C3 hidden_state_delta_l2 always 0.0 — mount.hexa --probe is fresh-process
  per turn, prior_hidden persistence not wired (Phase 3 TODO)
- C4 REPL parser is line-based regex on mount stdout; mount emit format
  changes break it
- C5 chat-capability NOT promised (own 17 ALM forced learning closed)
- C6 Ctrl+C SIGINT handling unverified — readline behavior under signal is
  hexa-runtime-dependent
- C7 mount cold-load ~25-30s/turn (transformers AutoModelForCausalLM) — not
  interactive-fast yet (Phase 4 mount-daemon candidate)

## raw 준수

- raw#9 hexa-only — no .py in this layer (mount.hexa transient_py shim is own 4 LOCKED)
- raw#10 honest C3 = 7 caveats (≥5 satisfied)
- raw#15 additive — old --interactive stub replaced; --probe / --selftest
  preserved + extended; mount.hexa / bash wrapper / other anima_cli modules
  untouched
- own 17 — ALM forced learning DEPRECATED, backend = clm_v4_mount only
  (DEFAULT_MODEL = need-singularity/clm-v4-mk2-v1)

## Known limits

1. mount cold-load latency ~25-30s/turn — Phase 4 mount-daemon candidate
2. hidden_state_delta_l2 = 0.0 — Phase 3 prior_hidden npz path persistence
3. Ctrl+C SIGINT untested via stdin pipe driver
4. anima.hexa mk2 dispatcher print-stub (Phase 1 second sub-cycle pending)

## Next sub-cycle candidates (완성도 lens ranked)

1. Phase 3 — mount-daemon + prior_hidden persist (highest sales gain)
2. Phase 4 — T2 ops actual exec wire (replace anima.hexa print stub)
3. Phase 5 — T3 stub 9 commands (anima connect/disconnect/...)
4. Phase 6 — spec yaml direct read (when hexa stdlib yaml lands)

Recommended: Phase 3 first. Interactive REPL sales ceiling is the 25s
cold-load — without daemon, users abandon. Phase 4/5 are backend stub
completeness, low sales impact.

## Outputs

- code: tool/anima_cli/dialogue.hexa (612 LoC, +318)
- verdict: state/anima_cli_mk2_2026_05_06/phase_2_dialogue_repl_verdict.json
- this doc: docs/anima_cli_mk2_phase_2_dialogue_repl_landed_2026_05_06.ai.md
- 6 validation session logs: state/anima_core_dialogues/2026-05-06/09-{27,30,35,37,40}-*.jsonl

commit X (held until explicit user request).
