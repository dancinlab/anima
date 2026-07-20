# G1/G6 typed workspace v1

## Decision

G1 composition and G6 falsification move out of the CLM mouth into an explicit state machine.
The existing model remains the eventual extractor and surface realizer; it is not allowed to invent
an implicit composition or bypass verification during this rung.

```text
extract/retrieve -> facts -> compose -> propose -> falsify -> select -> mouth
                            G1                    G6
```

`core/cognitive_workspace.py` is the first vertical slice. It is deliberately deterministic and
dependency-free so its causal contract can be tested before any 303M training or decode wiring.

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

1. `.kosmos`/hippocampus anchors -> `Fact` with source provenance.
2. H_9124 derivation traces -> `CompositionRule` inputs.
3. grounded contradiction output -> falsifier facts.
4. selected fact -> existing grounded decode context.

Each adapter needs an OFF control and a pairing-shuffle control. No GPU fire is justified before
those adapters preserve the invariants above in an engine-native smoke.
