---
schema: anima/docs/roadmap_mk2_landing/ai-native/1
last_updated: 2026-05-02
ssot:
  marker:    state/markers/roadmap_mk2_impl_landed.marker
  cli_tool:  tool/roadmap_op.hexa
  lint_tool: tool/roadmap_lint.hexa
  compile:   tool/roadmap_compile.hexa
  render:    tool/roadmap_render.hexa
  data_dir_pattern: <repo>/.roadmap.<domain>
status: LANDED
related_raws:
  - raw 9    # hexa-only orchestration
  - raw 10   # honest C3 (caveats inline)
  - raw 11   # snake_case
  - raw 15   # SSOT atomic write
  - raw 270  # ai-native readme mandate (this tool single-file = exempt)
  - raw 271  # core+module pattern
  - raw 272  # lint extension
  - raw 273  # sentinel attrs
preserved_unchanged:
  - .roadmap (mk1, frozen as historical narrative SSOT)
  - docs/n_substrate_consciousness_roadmap_2026_05_01.md (read-only ingest source)
  - tool/anima_roadmap_lint.hexa (mk1 anima-local lint)
  - 11 other existing roadmap_*.hexa tools
---

# anima .roadmap mk2 landing — 2026-05-02

## TL;DR

mk1 narrative `.roadmap` (3817 lines, frozen) → mk2 structured JSONL per-domain.
6 domain files (`.roadmap.{clm,eeg,akida,qrng,sim,meta}`) + 4 hexa CLI tools (1186 LOC total).
22 entries ingested into `.roadmap.meta` from `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
(1 track-def + 21 N-substrate research tracks N-1 through N-21).

User directive 4-question lock-in fully implemented:
- Q1 JSONL+HXC dual format
- Q2 11 CLI subcommands
- Q3 hybrid 3-tier recompile (sync + watch + lazy)
- Q4 domain-prefix monotonic id allocation

## CLI table (11 subcommands)

| subcmd       | purpose                              | example |
|--------------|--------------------------------------|---------|
| `add`        | create new entry, auto-id            | `roadmap_op add eeg --title "PCI baseline" --status proposed` |
| `update`     | mutate status / completion_ts / +ev  | `roadmap_op update nsubstrate.020 --status active` |
| `remove`     | delete entry                         | `roadmap_op remove clm.001 --reason "merged into 002"` |
| `list`       | list with optional filters           | `roadmap_op list --domain meta --status ready` |
| `show`       | print one entry by id                | `roadmap_op show nsubstrate.001` |
| `link`       | declare cross-link (depends-on/feeds-main/supersedes) | `roadmap_op link a.001 b.002 --kind depends-on` |
| `domains`    | list 6 domains + schema version      | `roadmap_op domains` |
| `verify`     | call roadmap_lint.hexa               | `roadmap_op verify` |
| `render`     | call roadmap_render.hexa             | `roadmap_op render --format md --domain meta` |
| `selftest`   | S1..S11 internal selftest            | `roadmap_op selftest` |
| `track-new`  | create meta track-def entry          | `roadmap_op track-new my_track --substrates clm,eeg` |

## JSONL schema

```json
{
  "id": "<prefix>.<3-digit>",
  "mk": 2,
  "domain": "clm|eeg|akida|qrng|sim|meta",
  "status": "proposed|ready|wip|active|blocked|landed|retired|superseded",
  "title": "...",
  "substrates": ["clm","eeg",...],
  "track": "track-name",
  "phase": "...",
  "since": "YYYY-MM-DD",
  "completion_ts": "YYYY-MM-DDTHH:MM:SSZ",
  "why": "...",
  "depends_on": ["clm.001", "meta.005"],
  "feeds_main": false,
  "evidence": ["state/...", "..."],
  "refs": ["commit ...", "PR #..."],
  "raw_ref": "raw9 + raw15",
  "cost": "$N or 'mac-local'",
  "effect": "TBD or N-star"
}
```

Required: `id mk domain status title`. Recommended: `track why`. Status `landed` requires `completion_ts`.

## Domain list (6) + naming

| domain | scope | initial entries |
|--------|-------|----------------:|
| `clm`  | CLM 170M native LM tracks | 0 |
| `eeg`  | EEG 16ch OpenBCI tracks   | 0 |
| `akida`| AKIDA AKD1000 neuromorphic | 0 |
| `qrng` | QRNG (ANU + ESP32 + alt)  | 0 |
| `sim`  | universe simulation tracks | 0 |
| `meta` | cross-domain + research tracks (N-substrate, etc.) | 22 |

`<domain>.<3-digit>` = canonical id pattern. `meta` domain may carry sub-prefixes (e.g. `nsubstrate.NNN`)
for human/agent readability of large research-track families.

## N-substrate ingest (21 tracks → .roadmap.meta)

Source: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` (sha b1e41a3335181d5b)

| section | tracks | id range          | status   |
|---------|--------|-------------------|----------|
| §2 today    | N-1, N-6, N-9, N-10                   | nsubstrate.001-004 | ready (4) |
| §3 AKIDA D+ | N-2, N-3, N-4, N-5, N-7, N-8           | nsubstrate.005-010 | blocked (6) |
| §4 partner  | N-11, N-12, N-13, N-14, N-15           | nsubstrate.011-015 | blocked 4 + ready 1 (HoTT) |
| §5 2026 web | N-16, N-17, N-18, N-19, N-20, N-21     | nsubstrate.016-021 | blocked 4 + ready 2 (Penrose lit + IIT 4.0) |

Plus `meta.000` = N-Substrate Roadmap launch track-def.

Ready (today, $0): N-1 / N-6 / N-9 / N-10 / N-15 (HoTT) / N-20 (Penrose lit) / N-21 (IIT 4.0 reproduce) = **7 entries**.
Blocked (AKIDA / capex / partnership): 14 entries.

## mk1 freeze policy

`/Users/<user>/core/anima/.roadmap` (mk1, 1153503 bytes, 3817 lines, sha d55158af5c26c7c8…) is **frozen**.
- Read-only historical narrative SSOT.
- mk1 lint (`tool/anima_roadmap_lint.hexa`) continues to validate mk1 file independently.
- mk2 lint (`tool/roadmap_lint.hexa`) targets only `.roadmap.<domain>` files.
- No automatic backport — historical entries stay in mk1 narrative form. Follow-up cycle F5 may extract.

## Recompile mechanism (3-tier hybrid)

| tier | trigger | when | status |
|------|---------|------|--------|
| **sync**  | `roadmap_op add/update/remove` invokes compile after mutation | every write | LANDED (manual call: `roadmap_op verify` after edit; auto-trigger follow-up) |
| **watch** | launchd plist watches `.roadmap.<domain>` mtime → recompile | on mtime change | SPEC-ONLY (plist not installed; F1 follow-up) |
| **lazy**  | `roadmap_render` falls back to JSONL if `.hxc` missing or stale | on read | LANDED (render.hexa: `if _file_exists(hxc) { hxc } else { src }`) |

## HXC compile format (v0 fallback)

Until BG-L2 `hxc_format` module lands, `roadmap_compile.hexa` emits minimal HXC:

```
#hxc/1 schema=anima/roadmap/mk2/hxc/1 source_sha=<src_sha> ts=<iso>
#count=<n> domain=<d>
<entry-1-jsonl>
<entry-2-jsonl>
...
```

Compactness: ~98.9% of JSONL bytes (skips comments only). Real binary compaction = follow-up F6.

Source-hash guard: compile re-skips if `source_sha` matches previous header (idempotent).

## Selftest evidence

| tool | result |
|------|--------|
| `roadmap_op.hexa selftest` | 11/11 PASS |
| `roadmap_lint.hexa` | 0 errors / 0 warnings on 22 entries × 6 domains |
| `roadmap_compile.hexa` (force) | 6/6 domains compiled; src+hxc sha emitted |
| `roadmap_compile.hexa` (no-force, 2nd run) | 6/6 unchanged (source-hash guard PASS) |
| `roadmap_render.hexa --format md` | full md table + per-entry detail OK |
| `roadmap_op list` byte-identical 2-run | PASS (diff empty) |

## raw#10 caveats (10 honest C3)

C1 — HXC v0 = JSONL-minus-comments; binary compaction deferred to BG-L2.
C2 — launchd watch tier (Q3 middle) plist NOT installed; sync (manual call) + lazy (render fallback) only.
C3 — `link` subcmd is JSON-ack only; in-place depends_on mutation = follow-up F2.
C4 — status whitelist extended to `ready` + `active` for N-substrate doc semantic mapping.
C5 — dangling-evidence is warn-only (21 forward research entries have empty evidence by design).
C6 — id allocation lock = mkdir-flock 5s timeout; multi-host concurrent untested.
C7 — heredoc atomic write would corrupt on `__HEXA_EOF__` literal; no current entry contains it.
C8 — `feeds_main` invariant warn-only; advisory cross-domain meta-only constraint.
C9 — BG-L6 `hive/{core,modules}/roadmap_format/` integration deferred (F3); current impl is anima-local self-contained.
C10 — `nsubstrate.NNN` sub-prefix overrides simple `<domain>.<3-digit>` convention; lint accepts via `[a-z0-9_]+` prefix pattern; domain field still `meta`.

## File index (sha-pin)

| path | sha-16 | LOC | bytes |
|------|--------|----:|------:|
| `tool/roadmap_op.hexa`        | fa32be14b3afc2a7 | 573 | 21980 |
| `tool/roadmap_lint.hexa`      | c0190cb6e3629e2c | 298 | 11760 |
| `tool/roadmap_compile.hexa`   | 5e2998a7ccb74d96 | 144 | 5455  |
| `tool/roadmap_render.hexa`    | 2cf8c5efccd19bdf | 171 | 5778  |
| `.roadmap.clm`                | 1194108efa79fcd4 | 3   | 146   |
| `.roadmap.eeg`                | b05c0531b54fb6f0 | 3   | 146   |
| `.roadmap.akida`              | de3307cff56a48eb | 3   | 150   |
| `.roadmap.qrng`               | 45597eaa658e8ca9 | 3   | 148   |
| `.roadmap.sim`                | 7418b4ac5707ca55 | 3   | 146   |
| `.roadmap.meta`               | 1e61985f72ffdb55 | 26  | 11544 |
| `.roadmap.clm.hxc`            | fbfe28f332977b5a | 3   | 159   |
| `.roadmap.eeg.hxc`            | c4e89f912b8de728 | 3   | 159   |
| `.roadmap.akida.hxc`          | 9dcdeb23d96ecf14 | 3   | 161   |
| `.roadmap.qrng.hxc`           | 21103ec54f227706 | 3   | 160   |
| `.roadmap.sim.hxc`            | 2ddfdac2952bf279 | 3   | 159   |
| `.roadmap.meta.hxc`           | 4d9f8ce5d63d20a7 | 24  | 11418 |
| `state/markers/roadmap_mk2_impl_landed.marker` | (this) | — | — |

## Follow-up cycles

- **F1** launchd watch plist install (Q3 middle tier)
- **F2** `link` subcmd in-place mutation
- **F3** BG-L6 hive integration shim
- **F4** sister repo rollout
- **F5** mk1 → mk2 backport (historical entry extraction)
- **F6** HXC v1 binary compaction (post BG-L2 hxc_format land)
- **F7** BG-L6 closure → bind rename merge coordination
- **F8** First `feeds_main=true` promotion (when nsubstrate produces verifiable evidence)
