# G1/G6 typed workspace v1

## Decision

G1 composition and G6 falsification move out of the CLM mouth into an explicit state machine.
The existing model remains the eventual extractor and surface realizer; it is not allowed to invent
an implicit composition or bypass verification during this rung.

```text
extract/retrieve -> facts -> compose -> propose -> falsify -> select -> mouth
                            G1                    G6
```

`core/cognitive_workspace.py` is the state machine. `core/workspace_adapters.py` persists typed facts
through the canonical `.kosmos` writer/reader and exposes only the selected result as grounded decode
context. It never guesses facts from prose anchors.

## Invariants

1. Composition is a two-operand join. A single fact cannot produce a recombination.
2. Every derived fact carries both operand provenances plus the rule name.
3. Every claim declares at least one falsifier before evaluation.
4. A claim is selectable only when its proposition is grounded and no falsifier is present.
5. The mouth can serialize only the selected claim. It cannot inspect workspace candidates.
6. Existing G1/G6 bars and detectors remain frozen; this module does not redefine success.

## Boundary and next rung

This rung proves orchestration and fail-closed behavior, not capability. It does not parse natural
language, learn rules, retrieve `.kosmos` facts, call a CLM, or claim a G1/G6 lift.

The next rung should add adapters, in this order:

1. H_9124 derivation traces -> `CompositionRule` inputs.
2. grounded contradiction output -> falsifier facts (adapter exists; live-memory smoke pending).
3. selected fact -> existing grounded decoder invocation (context adapter exists; CLI wiring pending).

Each adapter needs an OFF control and a pairing-shuffle control. No GPU fire is justified before
those adapters preserve the invariants above in an engine-native smoke.

## Production reach seam

`anima-py evaluate <ckpt> --workspace-reach` wraps only compound `ideate` calls. Atomic calls are
delegated byte-for-byte to the mounted model, so G1's `max_single` remains an earned model baseline.
The wrapper has no concept table: it splits arbitrary clauses, extracts compact lexical operands,
performs sequential binary composition, and realizes an explicit measurable hypothesis.

`--workspace-reach-only` invokes the unchanged frozen G1/G6 scoring functions without paying for
unrelated axes. Its verdict is **system reach**, never a claim that the bare CLM weights changed.
