# Typed workspace held-out semantic certification

## Verdict

**CERTIFIED — 11/11 held-out panels, 121/121 checks.** This panel scores exact triples and contains no
keyword-coverage criterion.

Run through the production evaluation entry point:

```bash
python3 cli/evaluate.py --workspace-semantic
```

Panels: energy, biology, navigation, Korean growth, software compilation, everyday causality,
negative causality, conditionals, and 3-, 4-, and 5-step relation chains. Every panel passed:

- exact live derivation;
- storage-order invariance;
- direction reversal collapse;
- relation-pair shuffle collapse;
- missing-middle collapse;
- irrelevant-fact invariance;
- falsification OFF selects primary;
- matching contradiction selects alternative and marks primary `FALSIFIED`;
- shuffled contradiction is inert;
- both candidates contradicted causes abstention.

This closes the narrow objection that the frozen G1 result could be only concept-keyword accumulation.
The certification asks whether the typed relation join produces the exact expected new fact and whether
causal corruptions change that fact in the preregistered direction.

## Scope

Cases are deterministic architecture fixtures, not learned natural-language extraction. They certify
the workspace operator and verifier across unseen symbols/domains. The 303M natural-language realizer
is independently checked and fails closed to the structured rendering when it drops required meaning.
