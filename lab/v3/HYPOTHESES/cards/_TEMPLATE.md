---
id: H_XXX
slug: short-kebab-slug
title: one-line falsifiable claim (what, and the expected direction/magnitude)
domain: (pick one of this campaign's domains)
status: pre-register-frozen | supported | partial | falsified
exploration_method: how the candidate was framed (closed-form / sim / survey)
verification_method: deterministic harness + N pre-registered falsifiers
pre_register_frozen: true
frozen_at: YYYY-MM-DD
deterministic: true
llm: none
---

# H_XXX — <short title>

## Hypothesis

State the claim operationally: what quantity, computed how, predicted to do what.
A hypothesis that cannot be numerically falsified does not belong here.

## Why

Tie to the architecture levels in `ARCHITECTURE.json`, the imported spec under
`state/`, and to sister hypotheses.

## Predictions

- **P1**: ... (a specific number or inequality)
- **P2**: ...

## Variables

- list each input with its pre-registered value and source (mark `?` if unverified)
- list each measured output quantity

## Run Protocol

- **harness**: `tool/anima_v3.py` (functions used)
- **run script**: `state/<hX>_<slug>_<date>/run_<id>.py`
- **deterministic**: stdlib only, no randomness, $0 local
- **run cmd**: `python3 state/<hX>_<slug>_<date>/run_<id>.py`
- **artifacts**: `state/<hX>_<slug>_<date>/result.json`

## Criteria

- **C1 ...**: ...
- **verdict_rule**: SUPPORTED = all falsifiers PASS; FALSIFIED = any trigger.

## Falsifiers (pre-registered, measurable — aim for >=5)

- **F-..-1**: <condition that, if true, refutes a component> (measured how)
- ... (include at least one negative control and one bounds check)

## Honest Limits (aim for >=3)

- **L1**: where the numbers are representative not measured
- **L2**: what the model ignores
- **L3**: what would move the result

## Cross-Links

- **architecture**: `ARCHITECTURE.json` (level node)
- **spec**: `state/<imported-origin-spec>.md`
- **sister H**: ...
- **harness**: `tool/anima_v3.py`

## Verdict

_None yet — pre-register-frozen, still-to-run._

<!-- After running, paste the VERBATIM stdout in a fenced block + link result.json. -->
