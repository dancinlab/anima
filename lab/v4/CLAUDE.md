# anima-v4

## Project

A⇄G where the tension IS the thinking — write-side substrate. A successor campaign that inherits
nothing from anima(v1) but its sealed, measured verdicts; the two-engine premise is kept, the
emit-controller it degenerated into is rejected. Stage and live design: `ARCHITECTURE.json`.

## Tree

```
anima-v4/
├─ src/              — source code
├─ state/            — all work artifacts (experiments · bench · verification), git-tracked
├─ ARCHITECTURE.json — design SSOT (JSON `children` tree, update-in-place)
├─ architecture.html — human viewer for the JSON (run `python3 serve.py`)
├─ HYPOTHESES/       — pre-register → falsify → run → verdict (registry + cards)
├─ tool/             — deterministic verification harness the cards run against
├─ harness.config.json — this repo's declared lint conventions (id pattern · cell cap)
└─ CHANGELOG.md      — history (append-only)
```

## Rules

- do: Treat the **system** as the scope — the whole chain is the unit of design
- dont: Taking the first rig/result as the boundary (it is the first instance)
- do: Upstream reusable implementation to the `hexa-lang` stdlib (demiurge d3 · upstream-fix)
- dont: Owning stdlib here · duplicating implementation across topical folders (docs only)
- do: Default heavy compute to `QFORGE`-native, migrating QE piece-by-piece past its gate
- dont: Shelving a QFORGE blocker — run QE in parallel AND push the fix (d_qforge_fix)
- do: Build every compute input deck via `hexa deck` (d_deck_always)
- dont: Hand-writing an input deck
- do: Put every artifact under `state/` (commons preserve-state)
- dont: Scattered report/notes dirs
- do: Update `ARCHITECTURE.json` in lockstep with any code/design change; log in `CHANGELOG.md`
- dont: Letting the tree drift from the code
- do: Research the literature FIRST, before renting compute or a costly run (`실측전 research`)
- dont: Spending on real compute before research justifies it
- do: Check a falsifier is ADMISSIBLE before building it (`verification.admissibility-gate`)
- dont: Pre-registering a threshold unchecked against the metric ceiling and the control (H_001)
- do: Keep the ablation to ONE variable — vary the mechanism, hold the alphabet fixed
- dont: A falsifier the scaffolding alone clears (it certifies the scaffolding, not the mechanism)
- do: Cite a number with the ARM that produced it and that arm's source path
- dont: Citing a bare number ("control 0.617") — it is a number that lost its experiment

## Gotchas

- do: Distil findings into `ARCHITECTURE.json` — one fact per node, detail to child nodes
- dont: Treating this file or the README as the live design SSOT
- do: Read imported origin docs under `state/` as seeds of record
- dont: Editing them to track current design (distil into the tree instead)
- do: Keep `tool/` to deterministic verification primitives (closed-form + falsifier ledger)
- dont: Putting reusable domain implementation in `tool/` (that belongs in `hexa-lang` stdlib)
- do: Report the metric as `d_acc` — bounded at 1.0, chance floor 0.5, and `f1`/`f2` are PANEL names
- dont: Reading "F2" as an F-measure (`salvage.L4.metric-is-d-acc` — it broke every falsifier once)
