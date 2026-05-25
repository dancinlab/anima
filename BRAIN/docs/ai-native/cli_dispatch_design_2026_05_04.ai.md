---
date: 2026-05-04
package: hexa-brain
subsystem: cli
status: LANDED
owner: hexa-brain repo
cycle: v1.1.0
ssot_artifact: bin/hexa-brain
---

# CLI dispatch design — v1.1.0 (2026-05-04)

## §1 Purpose

`bin/hexa-brain` is the **single binary entry-point** that fronts the hexa-brain
package. It provides verb-routed dispatch organized as `hexa-brain <subsystem>
<verb> [args...]` where `<subsystem>` is `eeg` or `core` and `<verb>` is one
of 16 eeg verbs or 14 core verbs (or a fall-through). This eliminates the need
for users to memorize 100+ filenames or remember the canonical
`hexa run <path>` invocation pattern; one binary becomes the discovery
surface for both subsystems.

The v1.0.0 dispatcher routed only eeg verbs at the top level (8 verbs flat).
The v1.1.0 dispatcher introduces the **two-level subsystem-then-verb routing**
to accommodate the new `core/` subsystem without verb-name collisions.

## §2 Dispatch rationale

Three options were considered for the v1.1.0 redesign:

1. **Pure-hexa entry shim** (`eeg.hexa --subcmd <verb>`). Rejected: hexa-lang
   v1 does not yet have a stable subcmd dispatch surface; argv parsing
   ergonomics are weaker than POSIX shell.
   reliable cross-platform shim for `exec`-style verb routing without a
   dependency on the hexa-lang argument parser maturing.
3. **Per-verb symlinks** (e.g. `bin/hexa-brain-eeg-calibrate -> hexa-brain`).
   Considered for tab-completion friendliness but adds 30+ symlinks for
   marginal UX gain; deferred to v1.x if user demand emerges.

The chosen approach: a single ~240-line bash script (`bin/hexa-brain`) that:
1. Resolves repo root via `HEXA_BRAIN_ROOT` env, `realpath` of script parent,
   or `~/.hexa-brain` fallback. **Validates that `eeg/` AND `core/` exist**
   before proceeding.
2. Pattern-matches the first arg as `<subsystem>`, shifts, then pattern-matches
   the second arg as `<verb>` within that subsystem.
3. Locates the `hexa` runtime via `command -v hexa` (lazy — only when actually
   dispatching to a hexa file).
4. `exec`s the matched `.hexa` file with remaining args passed through.
5. Falls through to subsystem routers (`eeg/eeg.hexa` for unknown eeg verb,
   error for unknown core verb — see §7 C3 #2).


The full script is `bin/hexa-brain` (~7.7 KB, 240 lines). Top-level routing:

```bash
case "$SUBSYS" in
  eeg)
    VERB="${1:-}"; shift || true
    resolve_hexa_bin
    case "$VERB" in
      board-health|health) exec "$HEXA_BIN" run "$ROOT/eeg/board_health_check.hexa" "$@" ;;
      calibrate)           exec "$HEXA_BIN" run "$ROOT/eeg/calibrate.hexa" "$@" ;;
      collect)             exec "$HEXA_BIN" run "$ROOT/eeg/collect.hexa" "$@" ;;
      analyze)             exec "$HEXA_BIN" run "$ROOT/eeg/analyze.hexa" "$@" ;;
      experiment)          exec "$HEXA_BIN" run "$ROOT/eeg/experiment.hexa" "$@" ;;
      closed-loop|nback|meditation) exec "$HEXA_BIN" run "$ROOT/eeg/closed_loop.hexa" "$@" ;;
      validate|brain-likeness)      exec "$HEXA_BIN" run "$ROOT/eeg/validate_consciousness.hexa" "$@" ;;
      realtime)            exec "$HEXA_BIN" run "$ROOT/eeg/realtime.hexa" "$@" ;;
      recorder)            exec "$HEXA_BIN" run "$ROOT/eeg/eeg_recorder.hexa" "$@" ;;
      electrode-adjust)    exec "$HEXA_BIN" run "$ROOT/eeg/electrode_adjustment_helper.hexa" "$@" ;;
      impedance)           exec "$HEXA_BIN" run "$ROOT/eeg/impedance_check.hexa" "$@" ;;
      lsl-capture)         exec "$HEXA_BIN" run "$ROOT/eeg/lsl_capture.hexa" "$@" ;;
      dual-stream)         exec "$HEXA_BIN" run "$ROOT/eeg/dual_stream.hexa" "$@" ;;
      neurofeedback)       exec "$HEXA_BIN" run "$ROOT/eeg/neurofeedback.hexa" "$@" ;;
      full-helmet-view)    exec "$HEXA_BIN" run "$ROOT/eeg/full_helmet_view.hexa" "$@" ;;
      router|"")           exec "$HEXA_BIN" run "$ROOT/eeg/eeg.hexa" "$@" ;;
      --help|-h|help)      # emits eeg verb list
      *)
        # Fall through: try eeg/<verb>.hexa (with -→_), else delegate to eeg.hexa router
        if [[ -f "$ROOT/eeg/${VERB//-/_}.hexa" ]]; then
          exec "$HEXA_BIN" run "$ROOT/eeg/${VERB//-/_}.hexa" "$@"
        else
          exec "$HEXA_BIN" run "$ROOT/eeg/eeg.hexa" "$VERB" "$@"
        fi ;;
    esac
    ;;
  core)
    VERB="${1:-}"; shift || true
    resolve_hexa_bin
    case "$VERB" in
      core|"")                    exec "$HEXA_BIN" run "$ROOT/tool/core/eeg_core.hexa" "$@" ;;
      paradigm-daily-life)        exec "$HEXA_BIN" run "$ROOT/tool/module/_paradigms/daily_life.hexa" "$@" ;;
      paradigm-resting|paradigm-resting-baseline)
                                  exec "$HEXA_BIN" run "$ROOT/tool/module/_paradigms/resting_baseline.hexa" "$@" ;;
      paradigm-p300-visual|paradigm-visual-p300)
                                  exec "$HEXA_BIN" run "$ROOT/tool/module/_paradigms/visual_p300.hexa" "$@" ;;
      paradigm-p300-auditory|paradigm-auditory-p300)
                                  exec "$HEXA_BIN" run "$ROOT/tool/module/_paradigms/auditory_p300.hexa" "$@" ;;
      paradigm-integration-test)  exec "$HEXA_BIN" run "$ROOT/tool/module/_paradigms/_integration_test.hexa" "$@" ;;
      export|eeg-export)          exec "$HEXA_BIN" run "$ROOT/tool/module/_core/eeg_export.hexa" "$@" ;;
      jsonl-audit)                exec "$HEXA_BIN" run "$ROOT/tool/module/_core/jsonl_audit.hexa" "$@" ;;
      adapter)                    exec "$HEXA_BIN" run "$ROOT/tool/module/_core/_adapter.hexa" "$@" ;;
      filter-pipeline)            exec "$HEXA_BIN" run "$ROOT/tool/module/_core/filter_pipeline.hexa" "$@" ;;
      pipeline-suggester)         exec "$HEXA_BIN" run "$ROOT/tool/module/_core/pipeline_suggester.hexa" "$@" ;;
      falsifier-runner)           exec "$HEXA_BIN" run "$ROOT/tool/module/_core/falsifier_runner.hexa" "$@" ;;
      chflags-lock)               exec "$HEXA_BIN" run "$ROOT/tool/module/_core/chflags_lock.hexa" "$@" ;;
      npy-loader)                 exec "$HEXA_BIN" run "$ROOT/tool/module/_core/npy_loader.hexa" "$@" ;;
      --help|-h|help)             # emits core verb list
      *) echo "Unknown core verb: $VERB" >&2; exit 1 ;;
    esac
    ;;
  -h|--help|help|"") print_help ;;
  *) echo "Unknown subsystem: $SUBSYS (valid: eeg, core, help)" >&2; exit 1 ;;
esac
```

`set -uo pipefail` is on (note: NOT `-e` — error handling is explicit per
branch); exec-style invocation propagates exit codes of the underlying `.hexa`
runs without bash interpolation.

## §4 Verb taxonomy

### §4.1 EEG verbs (16 verbs, all routed)

| Verb | Aliases | Backing file (under `eeg/`) |
|---|---|---|
| `board-health` | `health` | `board_health_check.hexa` |
| `calibrate` | — | `calibrate.hexa` |
| `collect` | — | `collect.hexa` |
| `analyze` | — | `analyze.hexa` |
| `experiment` | — | `experiment.hexa` |
| `closed-loop` | `nback`, `meditation` | `closed_loop.hexa` |
| `validate` | `brain-likeness` | `validate_consciousness.hexa` |
| `realtime` | — | `realtime.hexa` |
| `recorder` | — | `eeg_recorder.hexa` |
| `electrode-adjust` | — | `electrode_adjustment_helper.hexa` |
| `impedance` | — | `impedance_check.hexa` |
| `lsl-capture` | — | `lsl_capture.hexa` |
| `dual-stream` | — | `dual_stream.hexa` |
| `neurofeedback` | — | `neurofeedback.hexa` |
| `full-helmet-view` | — | `full_helmet_view.hexa` |
| `router` | (default for empty) | `eeg.hexa` |

Plus a **fall-through** for unknown verbs: tries `eeg/<verb>.hexa` (with `-` →
`_`), else delegates to `eeg/eeg.hexa <verb>`. This keeps newly-added eeg
files reachable without dispatcher updates.

### §4.2 CORE verbs (14 verbs, all routed)

| Verb | Aliases | Backing file (under `tool/core/`) |
|---|---|---|
| `core` | (default for empty) | `eeg_core.hexa` |
| `paradigm-resting` | `paradigm-resting-baseline` | `modules/_paradigms/resting_baseline.hexa` |
| `paradigm-daily-life` | — | `modules/_paradigms/daily_life.hexa` |
| `paradigm-p300-visual` | `paradigm-visual-p300` | `modules/_paradigms/visual_p300.hexa` |
| `paradigm-p300-auditory` | `paradigm-auditory-p300` | `modules/_paradigms/auditory_p300.hexa` |
| `paradigm-integration-test` | — | `modules/_paradigms/_integration_test.hexa` |
| `export` | `eeg-export` | `modules/_core/eeg_export.hexa` |
| `jsonl-audit` | — | `modules/_core/jsonl_audit.hexa` |
| `adapter` | — | `modules/_core/_adapter.hexa` |
| `filter-pipeline` | — | `modules/_core/filter_pipeline.hexa` |
| `pipeline-suggester` | — | `modules/_core/pipeline_suggester.hexa` |
| `falsifier-runner` | — | `modules/_core/falsifier_runner.hexa` |
| `chflags-lock` | — | `modules/_core/chflags_lock.hexa` |
| `npy-loader` | — | `modules/_core/npy_loader.hexa` |

Unknown core verbs **error out** (exit 1) — there is no fall-through for
core, by design (see §7 C3 #2).

### §4.3 Meta verbs

- `--version` / `-V` — parses first `## [X.Y.Z]` line from `CHANGELOG.md`.
- `--help` / `-h` / `help` — emits both-subsystem usage block.
- Per-subsystem help: `hexa-brain eeg --help`, `hexa-brain core --help`.

## §5 Help output design

The top-level `--help` output is a 60+ line block listing both subsystems'
verbs plus EXAMPLES + DOCS + LICENSE + Repo path. The complete block:

```
hexa-brain — neural substrate hexa pipeline (scalp EEG to intracortical-class)

USAGE:
  hexa-brain <subsystem> <verb> [args...]

SUBSYSTEMS:
  eeg    — scalp EEG capture pipeline (OpenBCI Cyton+Daisy 16ch)
  core   — paradigms + metrics + filter pipeline (anima-eeg-core)

EEG VERBS (hexa-brain eeg <verb>):  [16 verbs listed]
CORE VERBS (hexa-brain core <verb>): [14 verbs listed]

GLOBAL FLAGS:
  --version, -V    Print version from CHANGELOG.md
  --help, -h       This text

EXAMPLES:
  hexa-brain eeg board-health             # hardware preflight
  hexa-brain eeg calibrate                # impedance check
  hexa-brain eeg collect --secs 60        # 60s capture
  hexa-brain core paradigm-resting        # resting baseline paradigm
  hexa-brain core paradigm-p300-visual    # P300 visual paradigm
  hexa-brain eeg analyze --topomap        # offline analysis

DOCS:
  README.md, CHANGELOG.md, .roadmap.hexa_brain
  eeg/doc/, eeg/README.ai.md
  docs/core/, design/core/

LICENSE: MIT
Repo:    $ROOT
```

The dynamically-printed `Repo` line aids debugging when multi-clone setups
exist on the same machine.

## §6 Future GUI/TUI evolution (defer)

Out of scope for v1.1.0. Candidate paths if user demand emerges:

- **Rich-TUI launcher** — front the verbs in a Rich panel UI for users who
  prefer a menu over CLI.
- **Hexa-native GUI** — once hexa-lang grows a UI primitive set,
  re-implement the dispatcher in pure-hexa (would also resolve C3 #1).
- **WebSocket UI** — extend `eeg/closed_loop.hexa`'s WebSocket server
  pattern to expose all verbs as JSON-RPC, allowing a web dashboard.
- **bash/zsh completion script** — `_hexa-brain` completion file for tab-cycling
  through the 30 verbs. Half-day implementation, deferred to v1.2.

None of these are on the v1.1.x roadmap. Bash dispatcher remains canonical.


   formally violated by `bin/hexa-brain` being a bash script. The carve-out
   is justified by (a) hexa-lang v1 lacks robust argv/subcmd parsing, (b)
   POSIX-shell semantics are needed for `exec` exit-code propagation, and
   (c) the dispatcher is non-load-bearing for measurement correctness — only
   ergonomics. A pure-hexa rewrite is a v2+ candidate when hexa-lang argument
   parsing matures.
2. **EEG fall-through but no core fall-through**: the eeg subsystem has a
   fall-through (try `eeg/<verb>.hexa` → delegate to `eeg/eeg.hexa`) but the
   core subsystem errors on unknown verbs. Rationale: eeg has a flat
   `eeg/*.hexa` layout where new verbs map naturally to filenames; core has
   nested `modules/_<dir>/*.hexa` so there's no canonical filename mapping.
   Adding a smarter core fall-through (search all `_*/` subdirs) is a v1.2 task.
3. **Verb names hard-coded require update if hexa file added/renamed**: the
   case statements in `bin/hexa-brain` have 16 + 14 = 30 explicit verb
   branches. If a new `.hexa` is added or renamed, the dispatcher must be
   manually updated. There is no auto-discovery from the repo `.hexa` listing.
   This is a known maintenance liability; v1.x may add a generated verb table.
4. **Only 14 of 68 core files exposed**: the core subsystem has 68 hexa files
   but the dispatcher exposes only 14 verbs (5 paradigms + top-level entry +
   8 of 9 `_core/` utilities). The 49 modules under
   `_metrics/`, `_gates/`, `_artifact/`, `_integrations/`, `_hw/`, `_prng/`
   are reachable only via `hexa run tool/module/<dir>/<file>.hexa`
   directly. Closing this gap is a v1.2+ task.
5. **No completion script v1.1.0**: no bash/zsh/fish completion is shipped.
   Users must type verb names exactly. Adding `_hexa-brain` completion is a
   half-day task deferred to v1.2.
6. **Exit code propagation passthrough**: `exec` is used for the verb branches
   (so the .hexa file's exit code becomes the dispatcher's), but the
   `--version` and `--help` branches return their own exit codes. Unknown
   subsystem returns 1; unknown core verb returns 1; unknown eeg verb falls
   through (so its exit code is whatever `eeg/eeg.hexa` returns). This is
   correct but underdocumented; users may not realize that exit codes from
   underlying .hexa files surface verbatim.

## §8 Composability

- **Upstream**: bash 4+, `hexa` runtime on PATH, the 30 backing `.hexa` files
  it routes to plus the additional ~50 reachable via `hexa run` directly.
- **Downstream**: end-user shell sessions; CI scripts that want named-verb
  invocation; future hexa-lang ecosystem packages that may discover
  hexa-brain via PATH.
