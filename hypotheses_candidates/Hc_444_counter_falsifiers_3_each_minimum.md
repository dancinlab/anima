---
id: Hc_444
slug: counter-falsifiers-3-each-minimum
title: Each n=6 domain spec must declare ≥3 counter-examples AND ≥3 falsifiers (honesty-check pattern)
domain: math
status: candidate-unverified
source_doc: docs/spec/anima-soc/anima-soc.md
source_lines: 329-333, 574-593
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: §7.10. COUNTER_EXAMPLES (elementary charge, Planck h, π, alpha, Avogadro) ≥3. FALSIFIERS (±15% measurement, uniqueness counter, MC bottom 50%, χ² p<0.001, OEIS recomputation breakdown) ≥3. Methodological discipline pattern.
---

## Hypothesis
Each n=6 domain specification, to be honest-science compliant, must declare at least 3 named counter-examples (independent constants not derivable from n=6) AND at least 3 named falsifiers (concrete observations that would discard the core claim). Counter-examples remove special-pleading; falsifiers operationalize disproof.

## Migration TODO
- [ ] Audit all n=6 domain specs for ≥3 counter ≥3 falsifier
- [ ] Reject specs failing the pattern
- [ ] Build automated honesty-check linter
- [ ] Falsifier of this hypothesis: a domain succeeds without 3+3 declarations
