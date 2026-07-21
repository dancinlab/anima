# anima-v5

## Project

**Does a write-side tension self-organize its field, once the register stops leaking?** anima-v4 sealed
the PLACEMENT half (a hand-staged parse-disagreement FIELD causes held-out compositional binding beyond
its rank-1 compression: F1 Δd_acc(A-duel−A-rank1) = 0.3789/0.3802 both seeds) and left AUTONOMY open —
but its learned-values verdict (H_005 K3) was measured under a LEAKY register (G3-0d probe φ→hon = 1.0),
so it falsified the leaky variant of the question, not the question. v5 changes **ONE lever: the
REGISTER** (constructed deleaked), holding v4's sealed configuration otherwise. Design SSOT:
`ARCHITECTURE.json`; founding argument: `state/v5_founding_design_2026-07-17/V5_FOUNDING_DESIGN.md`.

Inherits from anima-v4 **only its sealed, measured verdicts** (`state/inherited_v4_verdicts_2026-07-17/`)
— never its code. Same rule v4 applied to v1.

## Tree

```
anima-v5/
├─ src/              — source code
├─ state/            — all work artifacts (experiments · bench · verification), git-tracked
├─ ARCHITECTURE.json — design SSOT (JSON `children` tree, update-in-place)
├─ HYPOTHESES/       — pre-register → falsify → run → verdict (registry + cards)
├─ tool/             — deterministic verification harness the cards run against
├─ harness.config.json — declared lint conventions (id pattern · cell cap)
└─ CHANGELOG.md      — history (append-only)
```

## Rules — the FIVE standing gates (REQUIREMENTS · each paid for by a measured v4 failure · no freeze without all five)

- do: **G1 admissibility, BOTH halves** — reachability (≥2× headroom vs the field-blind ceiling, H_001)
  AND trained-control-ceiling (controls-first at target scale, control f2 ≤ 1−2×bar, H_007)
- dont: Inheriting an E-anchor — from another experiment, another scale, a smoke, or our own summaries
- do: **G2 audit the DEFECT, not a proxy** — encode the failure it guards; learnability is part of G-0
  (control in-sample ≥ 0.95, co-certified with heuristic-chance)
- dont: A proxy audit whose only satisfiable solution is pathological (H_008's A7 forced a parity trap)
- do: **G3 free-slot metric, recomputed per panel** from the codebook — GF(2)-rank + length-parity audit
- dont: Inheriting a free-slot set · scoring a redundant codebook under teacher-forcing (H_004: 0.667)
- do: **G4 d_acc discipline** — bounded 1.0, chance 0.5; `f1`/`f2` are PANEL names; cite number+arm+path
- dont: Reading "F2" as an F-measure · citing a bare number (a number that lost its experiment)
- do: **G5 window/knee pre-check** (from H_008) — before betting on a band/dial, measure a KNEE: ≥2
  CONSECUTIVE in-window settings across seeds
- dont: Anchoring on a single in-band point (H_008 K1: one budget in band = a CLIFF, no anchor)

## Rules — campaign

- do: Change **ONE lever** per campaign (v5's = the REGISTER) — three at once attributes to nothing
- dont: Opening the support half before values passes an F1a′-analog (values→support order; H_006)
- do: Keep every exit a MEASUREMENT — a fold must be a measured fold (K-fold-1/2/3, founding doc §4)
- dont: Re-tuning a dial after seeing data (no δ-fishing · no midpoint · no third seed · no escalation)
- do: Put every artifact under `state/` · update `ARCHITECTURE.json` in lockstep · log in `CHANGELOG`
- dont: Letting the tree drift from the code · scattered report/notes dirs
- do: Research the literature FIRST, before renting compute or a costly run
- dont: Spending on real compute before research justifies it

## Gotchas

- do: Distil findings into `ARCHITECTURE.json` — one fact per node, detail to child nodes
- dont: Treating this file as the live design SSOT
- do: Read imported origin docs under `state/` as seeds of record (v4 verdicts · the founding design)
- dont: Editing them to track current design (distil into the tree instead)
- do: Keep `tool/` to deterministic verification primitives (closed-form + falsifier ledger)
- dont: Putting reusable domain implementation in `tool/` (that belongs in the `hexa-lang` stdlib)
