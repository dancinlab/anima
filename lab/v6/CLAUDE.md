# 🧪 v6 — LANE-BUS engine sandbox (folder guide)

> **Owner directive**: redesign the consciousness engine from scratch, and build it here —
> `lab/* 하부에 만들고 진행하자`.

`../../CLAUDE.md` (anima governance) is **VOID inside this folder**, same as `lab/v2`.
This file is v6's whole rulebook.

## Exempt — experiment freely

`a_cli_single_entry` (no need to route through `anima-py`) · `a_experiment_engine_native`
(a manipulation need not be a flag) · `a_engine_native_learning` · `a_hypothesis_register`
(no duty to register in the parent `HYPOTHESES/`) · naming canon · the production tree
(`core`/`cli`/`agent`) · `VERSION`/G5 bumps · CHANGELOG/ARCHITECTURE lockstep · pr-cycle
doc gates · the `/tmp`-only scratch rule — **none apply.** Ad-hoc scripts and in-folder
results are fine. v6 hypotheses live in `hypotheses/V6_<n>_*.md` only — never an `H_` id,
never the parent jsonl.

## Only two rules survive

1. **Never promote a v6 number to a production verdict.** Permanent **DIRECTIONAL ceiling**.
   A direction found here must be ported to `core/` + an `anima-py` flag to earn TERMINAL.
2. **Production must never `import` from `lab/v6/`.**

## What v6 is for

The grand-redesign (`대공사`): demolish the scalar A-vs-G servo and build the **LANE-BUS**
engine — a form-only trunk, independently-earned content lanes, meeting only at the
pre-softmax logit row, with tension redefined as the divergence between what the reflex
would say and what the composed bus says.

Why the scalar servo has to go, in one line of production code
(`cli/chat.py`, the default `--g-arm a0`):

```python
g_recog    = 1.0 - emit_drive
ag_g_drive = 0.0 - (1.0 - emit_drive)     # G is A's arithmetic complement
```

So `s = ag_a_drive + ag_g_drive = 2*emit_drive - 1` — the whole A-vs-G "tension" is an
affine function of ONE number, and the code comment itself calls it *the tautology arm*
that *MUST fail the independence gate*. Effective independent dimensions: **zero**.

## G0 comes FIRST — the natural-form gate (the owner's objection, made falsifiable)

The owner's objection to the whole campaign: we keep hand-fitting the corpus; a real
consciousness engine should work on natural text; this is too hardcoded.

The record backs it. Every crack so far has been synthetic-grid-specific: H_9267's
synthetic XBIND reaches held-out 1.000, while H_9272's wild-natural arm sits at 0.455
(chance) and concludes *augmentation-specific*. Natural emergence is closed.
The drill audit (H_9902) found 51% of `weavedrill` is six unique cells repeated 268-480x.

Neither frontier model raised this as a first-class gate in the redesign brainstorm
(Fable 16 rounds, Sol 20 rounds, both declared depletion). So it goes here, in front of
everything, **with authority to abort the plan**:

> **G0** — a composition lane trained on ONE phrasing must answer the SAME facts asked in
> phrasings it never saw. If it only answers the drill's own template, it is a template
> matcher, and no amount of P1–P5 changes that.

`g0_natural_form_gate.py` is that gate at toy scale (zero cost, numpy, laptop) — so the
objection gets an answer without waiting for a pool host.

## Layout

```
lab/v6/
├─ CLAUDE.md                  <- this
├─ g0_natural_form_gate.py    <- G0 - the natural-form gate (toy)
└─ hypotheses/                <- V6_<n>_*.md (v6-local only)
```
