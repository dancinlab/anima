# anima-v3

## Project

anima-v3 asks **where aliveness lives** — a clean-slate campaign for an agent that is ALIVE
(own state, own reason to speak, identity from structure rather than from a prompt). The
predecessor `anima` (v1) is discarded entirely; its only inheritance is a set of measured,
sealed verdicts that say where the ground is soft. Deep structure → `ARCHITECTURE.json`.

## Tree

```
anima-v3/
├─ src/              — source code
├─ state/            — all work artifacts (experiments · bench · verification), git-tracked
├─ ARCHITECTURE.json — final architecture SSOT (JSON `children` tree, update-in-place)
├─ architecture.html — human viewer for the JSON (run `python3 serve.py`)
├─ HYPOTHESES/       — pre-register → falsify → run → verdict (registry + cards)
├─ tool/             — shared deterministic harness the hypothesis cards run against
└─ CHANGELOG.md      — history (append-only)
```

## Scope

- do: treat the **system** as the unit of design — the whole chain, not one rig.
- dont: mistake the first rig/result for the campaign's boundary (it is the first instance).

## Implementation home (demiurge d3)

- do: consume reusable implementation from the sibling `hexa-lang` stdlib.
- do: upstream reusable logic TO that stdlib (commons upstream-fix); keep this repo design + verdicts.
- dont: own stdlib here · treat this repo as a code home.
- dont: duplicate implementation across topical/domain folders — they hold **docs / manifests only**.

## Compute engine (demiurge d_qforge_default · skip for non-compute labs)

- do: default heavy compute (DFT / DFPT / el-ph / physics sim) to the from-scratch `QFORGE` stack.
- do: migrate QE→QFORGE piece-by-piece, absorbing a piece only after it passes the gate (**≤1 % vs QE**).
- do: build every compute input deck via `hexa deck` (d_deck_always).
- do: if QFORGE blocks, run QE in parallel AND push the QFORGE fix at once (d_qforge_fix).
- dont: treat QE/bespoke as the default (it is reference/fallback only) · shelve a QFORGE fix · hand-build a deck.

## Artifacts + lockstep

- do: put every work artifact under `state/` only (commons preserve-state).
- do: update `ARCHITECTURE.json` in lockstep with any code/design change · log it in `CHANGELOG.md`.
- dont: scatter report/notes dirs · change design without touching the SSOT tree.

## Research before real measurement (`실측전 research`)

- do: run a literature research pass FIRST, before renting compute or an expensive measurement.
- do: spend on real compute only after research justifies it — a cheap proxy may suffice.
- dont: rent compute on an unresearched question (the answer may already be in the literature).

## SSOT discipline

- do: treat repo-root `ARCHITECTURE.json` as the live design SSOT — not this file, not the README.
- do: distill findings into the tree · keep one fact per node, pushing deeper detail to child nodes.
- dont: track current design in this file/README · pile many facts into one cell.

## Seeds of record

- do: treat imported origin docs under `state/` as seeds of record — distill FROM them into the tree.
- dont: edit a seed to track current design (a record is of its time; let it go stale).

## tool/ boundary

- do: keep `tool/` to deterministic verification primitives — closed-form checks + falsifier ledger.
- dont: put reusable domain implementation in `tool/` (that belongs in the `hexa-lang` stdlib).
