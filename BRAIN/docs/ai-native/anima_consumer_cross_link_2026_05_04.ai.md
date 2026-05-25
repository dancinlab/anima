---
date: 2026-05-04
package: hexa-brain
subsystem: cross_link
status: LANDED
owner: hexa-brain repo (cross-cycle: anima monorepo)
cycle: v1.1.0
ssot_artifact: anima/.roadmap.eeg + anima/anima-eeg/ + anima/anima-eeg-core/ (legacy mirrors)
---

# Anima consumer cross-link — v1.1.0 (2026-05-04)

## §1 Why anima needs hexa-brain

Anima is a consciousness-research monorepo whose EEG-conditioned tracks (BLM
brain-LM, P9 SFT, CLM-EEG, Φ-substrate research) all consume scalp-EEG capture
+ analysis primitives plus paradigm/metric/filter primitives. Pre-spinoff,
those primitives lived in `anima/anima-eeg/` (capture pipeline) and
`anima/anima-eeg-core/` (paradigms + metrics + filter pipeline). After v1.1.0
spinoff (2026-05-04), they live in this hexa-brain repo as **two subsystems**:

- `eeg/` (capture pipeline, formerly `anima/anima-eeg/`)
- `core/` (paradigms + metrics, formerly `anima/anima-eeg-core/`)

Anima is therefore a **downstream consumer** of hexa-brain. The dependency is
at the artifact level (`eeg/recordings/sessions/*.npy` produced by hexa-brain's
`eeg/collect.hexa` / `eeg/eeg_recorder.hexa`), at the WebSocket-event level
(`eeg/closed_loop.hexa` emits BrainState events consumed by anima's
consciousness runtime), and at the metric-pipeline level (anima cycles call
`tool/module/_integrations/clm_eeg_p[1-3].hexa` for CLM-EEG conditioning).

## §2 Anima-side adapter pattern

The intended cross-repo coupling shape:

```
+--------------------+              +--------------------------+
|     anima monorepo |              |     hexa-brain repo      |
|                    |              |                          |
|  anima-eeg-bridge.hexa  -- thin -->   collect / closed_loop  |
|  (consciousness adapter)             (real-hardware capture) |
|                    |              |                          |
|  (consumes .npy)   |  <-- npy ----+   recordings/sessions/   |
+--------------------+              +--------------------------+
```

`anima-eeg-bridge.hexa` is the **planned** thin shim on the anima side that:
1. Resolves the hexa-brain install root (`HEXA_BRAIN_ROOT` env or
   `~/.hexa-brain` default).
2. Invokes `hexa-brain collect`, `hexa-brain analyze`, etc. via subprocess.
3. Translates BrainState WebSocket events into anima's internal Φ-substrate
   message format.

As of 2026-05-04 this bridge does **not** yet exist as a single file;
anima-side EEG consumption is currently scattered across modules that
historically referenced `anima-eeg/<file>.hexa` paths. Consolidating into one
bridge file is a v1.x task on the anima side, not hexa-brain side.

## §3 Stability protocol

Anima retains BOTH `anima/anima-eeg/` AND `anima/anima-eeg-core/` as
**legacy mirrors** during the stabilization grace period. Deletion of each
mirror is gated on:

1. All anima cross-references migrated from `anima-eeg/<file>.hexa` and
   `anima-eeg-core/<path>.hexa` to either `anima-eeg-bridge.hexa` (preferred)
   or direct `hexa-brain` subprocess calls.
2. At least 2 anima cycles complete without hexa-brain interface change
   (signaling de-facto API stability).
3. `.roadmap.eeg` updated to reference hexa-brain as the SSOT instead of the
   anima-side mirrors.

Until those gates pass, the two anima-side directories are **mirrors** and
hexa-brain is the **canonical**. Drift between any of the three (anima-eeg
mirror, anima-eeg-core mirror, hexa-brain canonical) during grace period is
possible; in case of conflict, hexa-brain wins.

## §4 Roadmap propagation

Two roadmap files are now in scope:

- **anima**: `.roadmap.eeg` — anima's EEG track roadmap. Receives an
  **additive amendment** noting hexa-brain as the upstream SSOT and pinning
  the v1.0.0 spinoff hash. No subtraction from existing entries.
- **hexa-brain**: `.roadmap.hexa_brain` — this repo's substrate-ladder
  roadmap (v1-v5: scalp EEG → intracranial → high-density → closed-loop BMI →
  chronic implant). Cond.1 (v1 scalp EEG) is COMPLETE; cond.2-5 are SPEC_PHASE.

Anima cycles that consume hexa-brain MUST pin the version (currently v1.0.0)
in their cycle docs to avoid races where hexa-brain commits ahead of an
in-flight anima cycle's expectations.


1. **Anima retains `anima-eeg/` as legacy mirror until end of grace period**:
   the deletion is not yet performed and not yet scheduled. Consumers may
   accidentally edit the anima-side legacy mirror instead of the hexa-brain
   canonical, causing silent divergence. Mitigation: both repos cross-link to
   each other's ai-native docs, so a curious reader can find the canonical;
   no automated lint enforces this yet.
2. **Cross-repo refs may drift if hexa-brain commits ahead**: if hexa-brain
   ships a v1.1 with breaking interface changes (e.g. `closed_loop.hexa`
   WebSocket event schema bump) before anima's adapter migrates, anima
   sessions will silently break or emit incorrect events. There is no
   compatibility test in either repo's CI yet. Pin to v1.0.0 explicitly until
   the bridge stabilizes.
3. **Anima cycles must lock hexa-brain version pin to avoid races**: each
   anima cycle that depends on hexa-brain primitives should record the
   resolved hexa-brain commit hash in its cycle ai-native doc (alongside any
   tagged version). Without this, future debug of an anima failure cannot
   distinguish "hexa-brain regressed" from "anima regressed" without git
   archaeology across two repos.
4. **Consciousness-coupling code must be re-platformed**: `closed_loop.hexa`
   currently lives in hexa-brain root (correctly, per spinoff plan) but
   contains some anima-specific hooks (Φ-substrate event formats, anima
   consciousness-runtime WebSocket protocol details). These hooks should move
   to the planned `anima-eeg-bridge.hexa` on the anima side; the hexa-brain
   `closed_loop.hexa` should emit substrate-agnostic events. This re-platform
   has not yet been done — the coupling lives where it has always been.
5. **v1.1.0 frozen at this hash**: the v1.1.0 release reflects the working-tree
   state at 2026-05-04 commit `d75f7c3d` with the dual-subsystem layout
   (eeg/ + core/), bin/hexa-brain dispatcher, .roadmap.hexa_brain v1.1.0
   updates, and this AI-native doc package. v1.0.0 (commit `1ffd00ee`) was
   the same-day predecessor (single-subsystem flat layout); both are
   reachable in git history and must not be force-pushed. Any breaking
   interface change ships as v1.2+.

## §6 Forward references

- Anima-side forward-pointer:
  `anima/docs/ai-native/hexa_brain_consumer_cross_link_2026_05_04.ai.md`
  (lands in this same cycle; landed additively without modifying other anima
  files).
- Hexa-brain CHANGELOG provenance section: `CHANGELOG.md` v1.0.0
  "Provenance" subsection (anima HEAD `1b306eec24999ffd28505995655674b0f2beaa31`).
- Hexa-brain README sister-repo section: `README.md` "Sister repositories"
  block.
- Spinoff handoff: `v1_0_0_spinoff_2026_05_04.ai.md` (this package).

## §7 Composability

- **Upstream from anima's perspective**: hexa-brain (this repo).
- **Downstream from hexa-brain's perspective**: anima (consumer); other
  hexa-lang ecosystem packages that may need EEG (none confirmed yet).
