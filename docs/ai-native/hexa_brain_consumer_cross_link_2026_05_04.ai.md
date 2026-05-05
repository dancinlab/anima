---
date: 2026-05-04
package: anima
relationship: consumer-of-hexa-brain
status: LANDED
owner: anima monorepo
cycle: hexa-brain v1.1.0 dual-subsystem cross-link (succeeds same-day v1.0.0)
ssot_artifact: ../../.roadmap.eeg + ../../anima-eeg/ + ../../anima-eeg-core/ (legacy mirrors)
upstream_pin: hexa-brain v1.1.0 @ hexa-brain commit d75f7c3d (anima source 1b306eec24)
---

# hexa-brain external dependency cross-link — anima side (2026-05-04)

## §1 Forward-pointer

This doc is a **forward-pointer** for anima readers. The EEG capture +
analysis primitives plus paradigm + metric + filter pipeline primitives that
historically lived inside this monorepo at `anima/anima-eeg/` and
`anima/anima-eeg-core/` were spun off into a standalone repo on 2026-05-04
in a **two-stage** evolution:

- **v1.0.0** (commit `1ffd00ee`) — flat-layout single-subsystem spinoff of
  `anima/anima-eeg/`.
- **v1.1.0** (commit `d75f7c3d`, same day) — dual-subsystem layout with
  `eeg/` + `core/`, after merging `anima/anima-eeg-core/` as the second
  subsystem.

Standing facts:

- **Hexa-brain canonical**: <https://github.com/need-singularity/hexa-brain>
- **Spinoff date**: 2026-05-04
- **Spinoff source commit (anima HEAD at split)**:
  `1b306eec24999ffd28505995655674b0f2beaa31`
- **Subtree prefixes**: `anima-eeg/` (eeg subsystem) + `anima-eeg-core/`
  (core subsystem). Full git history preserved for both, rooted at directory
  contents.
- **License**: switched anima own#14 → MIT for hexa-lang ecosystem alignment

If you are reading anima code that imports from `anima-eeg/<file>.hexa` or
`anima-eeg-core/<path>.hexa`, you are reading the **legacy mirrors**. The
canonical source of truth is now in hexa-brain. Make changes there; the
legacy mirrors are retained only during the stabilization grace period
(see §3).

## §2 Pinned upstream version

Anima cycles consuming hexa-brain MUST pin to **v1.1.0** (commit `d75f7c3d`)
until the cross-repo dependency contract stabilizes. v1.0.0 was a same-day
predecessor and consumers should NOT pin to it (single-subsystem flat layout
is incompatible with v1.1.0+ dual-subsystem expectations). Pinning ensures:

- Reproducible cycle artifacts (any anima cycle can re-run with the same
  hexa-brain version it was authored against).
- Compatibility-test boundary (anima CI can detect when an upgrade to
  hexa-brain v1.2+ requires migration work).
- Audit trail (`git blame` on a hexa-brain reference resolves to a known
  hexa-brain commit, not "whatever was at HEAD when this ran").

The hexa-brain v1.1.0 SSOT artifact:
- Tag (when published): `v1.1.0`
- Commit hash: `d75f7c3d`
- Anima-side cross-link to spinoff handoff:
  `~/core/hexa-brain/docs/ai-native/v1_0_0_spinoff_2026_05_04.ai.md` (origin
  record + v1.0→v1.1 same-day transition log)

## §3 Stability protocol

Anima retains BOTH `anima/anima-eeg/` AND `anima/anima-eeg-core/` as the
legacy mirrors until **all** of:

1. All anima cross-references migrated from `anima-eeg/<file>.hexa` AND
   `anima-eeg-core/<path>.hexa` to either the planned
   `anima/anima-eeg-bridge.hexa` shim or direct `hexa-brain` subprocess
   calls.
2. At least 2 anima cycles complete without hexa-brain interface change
   (signaling de-facto API stability).
3. `.roadmap.eeg` updated to reference hexa-brain as the SSOT instead of
   `anima/anima-eeg/` and `anima/anima-eeg-core/`.

Until those gates pass, the legacy mirrors exist as redundant copies. In
case of conflict between any of the mirrors and hexa-brain canonical,
**hexa-brain wins**.

## §4 Cross-links to hexa-brain ai-native docs

The matching ai-native package on the hexa-brain side:

| Doc | Path (hexa-brain repo) | Purpose |
|---|---|---|
| Index | `docs/ai-native/_INDEX.md` | Reading order + SSOT artifacts |
| Spinoff handoff | `docs/ai-native/v1_0_0_spinoff_2026_05_04.ai.md` | Origin + v1.0→v1.1 transition + subsystem map |
| eeg manifest | `docs/ai-native/eeg_subsystem_module_manifest_2026_05_04.ai.md` | 30 `eeg/*.hexa` + 33 `eeg/protocols/` inventory + 16 verbs |
| core manifest | `docs/ai-native/core_subsystem_module_manifest_2026_05_04.ai.md` | 68-file core inventory (5 paradigms + 20 metrics + 5 gates + 11 artifact + 9 integrations + 6 hw + 9 _core + 2 prng) + 14 verbs |
| CLI design | `docs/ai-native/cli_dispatch_design_2026_05_04.ai.md` | `bin/hexa-brain` v1.1.0 dual-subsystem dispatcher rationale |
| Reverse cross-link | `docs/ai-native/anima_consumer_cross_link_2026_05_04.ai.md` | Hexa-brain side of THIS pointer |

## §5 Honest C3 (raw#10)

1. **Anima `anima-eeg/` legacy mirror not yet deleted**: working tree at
   anima HEAD still contains the full `anima-eeg/` subtree. Edits there are
   silently divergent from hexa-brain canonical. Mitigation: this doc is the
   only in-tree pointer; if it is lost, future anima readers may not know the
   spinoff happened. Compensating: `.roadmap.eeg` will receive an additive
   amendment (separate cycle) noting the spinoff.
2. **`anima-eeg-bridge.hexa` adapter shim does not yet exist**: the planned
   single-file bridge that subprocess-calls `hexa-brain` and translates
   BrainState events into anima's Φ-substrate format is documented in
   hexa-brain's `anima_consumer_cross_link_2026_05_04.ai.md` §2 but is not
   yet implemented. Anima-side EEG consumption today is scattered across
   modules referencing `anima-eeg/<file>.hexa` and `anima-eeg-core/<path>.hexa`
   paths directly. Bridge implementation is a v1.x anima-side task and
   should subsume both legacy paths.
3. **No automated cross-repo compatibility test**: if hexa-brain ships a
   breaking interface change (e.g. `eeg/closed_loop.hexa` WebSocket schema
   bump or `core/tool/modules/_integrations/clm_eeg_p[1-3].hexa` API change)
   before anima migrates, the failure surfaces only at runtime. Pin to
   v1.1.0 (commit `d75f7c3d`) explicitly to hold this stable.
4. **Cross-references in old anima commit messages reference `anima-eeg/`
   and `anima-eeg-core/`**: `git log -- anima-eeg/`, `git log --
   anima-eeg-core/`, and `git log --grep "anima-eeg"` will continue to
   surface valid commit history; those references are **not** broken since
   the legacy mirrors still exist. After mirror deletion (gate §3), those
   references become orphan blob refs (recoverable but not directly browsable
   from working tree).
5. **No git submodule / subtree merge wiring**: hexa-brain is an
   **independent** repo, not a git submodule of anima. Anima does not pull
   hexa-brain commits automatically. To consume an updated hexa-brain
   version, anima must (a) install hexa-brain locally
   (`HEXA_BRAIN_ROOT=~/core/hexa-brain`), (b) update the version pin in this
   doc + `.roadmap.eeg`, and (c) run any cross-repo migration cycle implied
   by the upgrade. There is no auto-track mechanism in v1.0.0.

## §6 Action items for future anima cycles

- **Immediate (any cycle)**: when adding new anima code that needs EEG
  capture/analysis, prefer `hexa-brain` subprocess invocation over deeper
  imports from `anima-eeg/`. Document the version pin in your cycle's
  ai-native doc.
- **v1.x anima cycle**: write `anima/anima-eeg-bridge.hexa` and migrate the
  scattered `anima-eeg/<file>.hexa` references to use it.
- **v1.x anima cycle**: amend `.roadmap.eeg` additively to declare hexa-brain
  as the SSOT.
- **Once stability gates pass**: remove `anima/anima-eeg/` legacy mirror in
  a single dedicated cycle with a corresponding ai-native doc.

## §7 Composability

- **Upstream**: hexa-brain (this is the dependency this doc cross-links to).
- **Downstream**: any anima research track that consumes EEG primitives
  (BLM brain-LM, P9 SFT, CLM-EEG, Φ-substrate research, audio-corpora EEG
  conditioning). All of these currently reference `anima-eeg/<file>.hexa`
  paths and will migrate to bridge or subprocess invocation per §6.
