# 🧪 v2 — rule-exempt experiment zone (folder guide)

> **Owner directive**: *"v2 does not get the rules applied — it's an experiment."*
> *"v2's hypotheses are created inside v2 only."*

`../CLAUDE.md` (the anima governance) is **VOID inside this folder**. This file is v2's whole
rulebook. Prose in this tree may be Korean; this guide is English because the english-only
baseline for `CLAUDE.md` is always-on and cannot be shrunk by config.

## Exempt — experiment freely

`a_cli_single_entry` (no need to route through `anima-py`) · `a_experiment_engine_native`
(need not be a flag) · `a_engine_native_learning` · `a_hypothesis_register` (**no duty** to
register in the parent `HYPOTHESES/`) · naming canon (`.canonical-ok` exempts the subtree; a
`v2` suffix is fine) · the production tree (`core`/`cli`/`agent`) · `VERSION`/G5 bumps ·
CHANGELOG/ARCHITECTURE lockstep · pr-cycle doc gates · the `/tmp`-only scratch rule —
**none of them apply.** Scratch files, ad-hoc scripts and in-folder results are all fine.

## ⛔ Only two survive

1. **Never promote a v2 number to a production verdict.** v2 lives outside `core/`, so it is a
   permanent **DIRECTIONAL ceiling** (every bypass died undecidable — H_9303/H_9307). A
   direction found here must be **ported to `core/` + an `anima-py` flag** to earn TERMINAL.
2. **Production must never `import` from `lab/v2/`** (same reason as `a_no_archive_import`).

## 🧪 Hypotheses live in v2 only (owner directive)

- A v2 hypothesis is **one surface: `hypotheses/V2_<n>_<slug>.md`**. Do NOT add it to the
  parent `HYPOTHESES/HYPOTHESES.jsonl`, do NOT use an `H_` number (that would collide with the
  parent's G6 unique-id gate), do NOT create an ARCHITECTURE gate node.
- Numbering starts at `V2_1` and increments inside v2. Card shape is free; skeleton below.
- When a v2 direction is **ported to production**, THAT is when the parent conventions apply:
  a NEW `H_` card + jsonl (2 surfaces) + an ARCHITECTURE gate node. The v2 card is cited as
  that H's `source`, nothing more.

```markdown
# V2_<n> — <the question in one line>
**status:** ⏳ PRE-REGISTERED | 🟢 SUPPORTED | 🔴 DEAD | ⚪ NO-VERDICT   (all DIRECTIONAL-capped)
**bars:** bars.json (frozen · committed before any data was seen)
## Question / Intervention / Arms+controls / Gates / Result / Falsify
```

## 🔬 The rules are waived; not fooling yourself is not

Frozen bars (`bars.json`), controls and the gradcheck stay — not because the repo mandates
them, but because **they ARE the experiment** (drop them and v2 discriminates nothing). This
is v2's own design, not an imposed gate.

- Commit `bars.json` **before looking at data**. Editing a number after reading a result is
  tune-to-green.
- `evaluate.py` does not merely hide P1 before the gates pass — it does not **compute** it.
  If the primary number is already on screen, every later "gate" call is shopping.
- If you add a guard, first check the guard **can fail** (`gradcheck.py --selftest`).
- A negative is a result. The grey zone is `NO-VERDICT`, never a re-tuned bar.

## Files

```
lab/v2/
├─ CLAUDE.md      — this guide (v2 rule SSOT)
├─ README.md      — hypothesis · how to run · why it mirrors the wall
├─ .canonical-ok  — naming-canon subtree exemption marker
├─ bars.json      — 🔒 frozen gate constants (committed pre-run · never edited after)
├─ hypotheses/    — 🧪 v2's own cards (V2_<n>_*.md · never in the parent jsonl)
├─ gen.py         — synthetic task stream + eval-key 0-shot hard-assert
├─ model.py       — trunk (byte-LM) + store + bridge · numpy fwd/bwd
├─ loss.py        — the single forward/loss/backward path (train·eval·gradcheck share it)
├─ gradcheck.py   — C0-d finite differences (+ `--selftest` = can the guard fail?)
├─ train.py       — `--arm {COTRAIN,BOLT,NOSTORE,SLOWROT} --seed N`
├─ evaluate.py    — SEQUENTIAL gate evaluator (C0→C1→C2→P1)
└─ run_all.sh     — 2 seeds × 4 arms + gates
```

Checkpoints go to `/tmp/v2/` (volatile; reproduce from the seed).
