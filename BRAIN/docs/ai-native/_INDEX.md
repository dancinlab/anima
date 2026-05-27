# hexa-brain AI-native doc package — INDEX

**Cycle**: v1.1.0 dual-subsystem layout (2026-05-04, same-day successor to v1.0.0 spinoff)
**Convention**: anima `docs/ai-native/*.ai.md` pattern — frontmatter, decision
are **handoff docs for AI agents** (future Claude sessions, CI bots, library
consumers).

## Reading order

1. **`v1_0_0_spinoff_2026_05_04.ai.md`** — start here. Origin story (anima
   monorepo subtree split), v1.0.0 → v1.1.0 same-day evolution, module
   boundaries, CLI dispatch pointer, anima-consumer cross-link pointer.
2. **`eeg_subsystem_module_manifest_2026_05_04.ai.md`** — eeg subsystem (30
   `eeg/*.hexa` + 33 `eeg/protocols/` + 1 `eeg/protocol/`). Public API
   (16 verbs), hardware deps, sibling pointers, future evolution path.
   Production-ready surface with 7 cycles of real OpenBCI hardware evidence.
3. **`core_subsystem_module_manifest_2026_05_04.ai.md`** — core subsystem
   (68 hexa files: 5 paradigms + 20 metrics + 5 gates + 11 artifact
   detectors + 9 integrations + 6 hardware abstractions + 9 core utilities
   + 2 PRNG primitives). Public API (14 verbs), v1.2+ evolution path.
4. **`cli_dispatch_design_2026_05_04.ai.md`** — `bin/hexa-brain` v1.1.0
   dual-subsystem dispatcher design. Verb taxonomy (16 eeg + 14 core), bash
   carve-out justification, future GUI/TUI evolution.
5. **`anima_consumer_cross_link_2026_05_04.ai.md`** — anima monorepo cross-repo
   dependency contract. Stability protocol, version-pin guidance (v1.1.0),
   planned `anima-eeg-bridge.hexa` shim.

## Cross-link to anima

Anima carries the matching forward-pointer at:

- `anima/docs/ai-native/hexa_brain_consumer_cross_link_2026_05_04.ai.md`

That document does the reverse: explains hexa-brain as anima's external
dependency and pins the v1.0.0 reference.

## SSOT artifacts

| Artifact | Path | Purpose |
|---|---|---|
| Roadmap | `.roadmap.hexa_brain` | mk2 JSONL with v1-v5 substrate ladder + cond.1b core |
| Changelog | `CHANGELOG.md` | Per-version release notes (v1.0.0 + v1.1.0 sections) |
| README user-facing | `README.md` | New-user install + quickstart (dual subsystem) |
| README ai-native (eeg legacy) | `eeg/README.ai.md` | Original anima-eeg ai-native entry (pre-spinoff scaffold; still valid for eeg-side reading) |
| CLI binary | `bin/hexa-brain` | Bash dispatcher (~240 lines, 16 eeg verbs + 14 core verbs) |
| Provenance | anima `1b306eec24999ffd28505995655674b0f2beaa31` | Spinoff source commit (both subtrees) |
| v1.0.0 commit | `1ffd00ee` | Initial v1.0.0 single-subsystem spinoff |
| v1.1.0 commit | `d75f7c3d` | Dual-subsystem layout + unified dispatcher |


1. **This index is non-binding**: changing the reading order or adding new
   docs requires editing this file; there is no auto-generation. If a doc
   lands without an index update, the index becomes stale silently.
2. **Doc count vs reality**: this index lists 5 manifest .ai.md files (not
   counting the index itself). The `eeg/doc/ai-native/` and
   `tool/module/*/README.ai.md` subtrees contain additional ai-native
   docs from earlier scaffold cycles
   (`eeg/doc/ai-native/anima_eeg_structure_refactor_plan_2026_05_03.ai.md`,
   `eeg/doc/ai-native/quality_monitoring_system_plan_2026_05_03.ai.md`,
   plus `tool/module/_*/README.ai.md` × 8). Those are
   **historical/per-module context** and not superseded; future readers
   should treat them as pre-v1.1.0 ancestor docs or per-module deep-dive
   references.
3. **No timestamp tracking**: docs include a `date` frontmatter field but
   there is no mtime-vs-frontmatter consistency check. Manual edits may
   leave the date stale; treat the date as the *original landing date* not
   the *last-modified date*.
4. **No cross-link enforcement**: each doc references sibling docs by
   filename; if a sibling is renamed the references go stale silently. A v1.x
   lint target could enforce this; not present in v1.0.0.
5. **Scope discipline**: this package documents the *spinoff handoff* and the
   *as-shipped v1.0.0* surface. Per-cycle research-decision docs (e.g.
   "BG-A real smoke verdict 2026-05-XX") are **not** in scope here — those
   continue to land in `docs/` (non-ai-native) as they did pre-spinoff.

## Next-cycle todos (visible to future agents)

- v1.2 — extend `bin/hexa-brain` dispatcher to expose more of the 68 core
  files (currently only 14 verbs route into the 5-paradigm + 9-`_core/`
  utility subset; 49 modules in `_metrics/` + `_gates/` + `_artifact/` +
  `_integrations/` + `_hw/` + `_prng/` are not exposed). Update
  `cli_dispatch_design_2026_05_04.ai.md` C3 #4.
- v1.2 — add bash/zsh/fish completion script for the 30 verbs.
- v1.2 — consolidate `eeg/core/quality_audit + quality_ledger` into the
  top-level `core/` namespace to remove the eeg/core vs core name collision
  (see eeg manifest C3 #6, core manifest §6).
- v1.x — write `anima/anima-eeg-bridge.hexa` thin shim; update
  `anima_consumer_cross_link_2026_05_04.ai.md` §2 to mark bridge as landed.
  `.venv-eeg/` BrainFlow Python under hexa-brain's own `.own N` taxonomy
  (currently inherited from anima without re-paperwork).
- v1.x — add GitHub Actions CI for the `--selftest` aggregate (currently
  no CI; selftest invariants live per-file).
