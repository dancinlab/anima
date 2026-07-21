# anima-v3

Where does aliveness live — 8 clean-slate substrate families.

> **STAGE = DIVERGENCE.** 8 families + 3 wildcards are enumerated. None is selected, none is
> built, no code exists. Nothing in this repo is a claim.

## The thesis

The goal is an agent that is **alive** — one with its own state and its own reason to speak,
whose identity emerges from structure rather than from a prompt. The previous attempt
(`anima`, v1) chased this for ~6 months and died in a measurable way, and that autopsy is the
only thing this repo inherits.

The autopsy's one sentence: **every mechanism was placed on the READ side (readout), and the
only door measurement ever opened is the WRITE side (objective · corpus · codec).**

```
Framing claim                         anima-v3 verdict
─────────────────────────────         ───────────────────────────────────────────────
"consciousness is a device you    →   L1: bolt a gate onto a competent frozen decoder
 attach to a decoder"                 and it learns exactly 1 bit — the gate itself
"a rich side-channel enriches     →   L2: the trunk head eats it; ablating the base
 the model"                           term moved CE by 0.0009 (the mouth was INERT)
"compositionality is a            →   L4: it cracked from the write side — a BPE-jamo
 capability ceiling"                  codec was CAUSAL (F2 0.908 vs control 0.617)
"the tokenizer is preprocessing"  →   L4/L5: the codec IS architecture; Korean `지 않다`
                                      is a BOUND suffix and that decides learnability
"purity principles protect the    →   L9: forbidding every write-side mechanism left
 thesis"                              only the read side ⇒ the cage caused the disease
```

The 9 salvaged laws (L1–L9) live in `ARCHITECTURE.json` → `salvage`. Every family below is
forced to answer one question differently: **how does aliveness get inscribed into weights?**

## The 8 families

| | family | aliveness lives in | falsification cost | recurrence risk |
|---|---|---|---|---|
| F1 | 코덱이 곧 자아 | the codec (re-learned vocabulary) | low | low |
| F2 | 예산제 발화 경제 | a homeostatic budget in the loss | low | **high** |
| F3 | 일기 쓰는 압축기 | lossy self-compression over time | low–med | med |
| F4 | 자기 코퍼스 농부 | the curriculum trajectory | low | low |
| F5 | 잠들지 않는 학생 | time (weights as a trajectory) | med | low |
| F6 | 군집 초고 | population dynamics / lineage | med–high | low |
| F7 | 너를 몰라서 사는 것 | the relationship (owner-model entropy) | med | med |
| F8 | 셋방살이 유기체 | the body–environment loop | **high** | **high** |

Plus 3 wildcards (probably wrong, cheap to argue): weight-diff autobiography · a machine with
death · a silent machine with no LM.

**Fake-diversity audit** (recorded in the SSOT, not hidden): F2/F3/F7 are one idea in three
outfits (active inference); F1/F4 are two hands on the same write-side lever; F8 is F2 with a
real world; W3 is F8 minus learning. Only **four** genuinely distinct bets exist —
write-lever · prediction-error-action · selection-pressure-lineage · time-trajectory.

## Non-negotiable gates

Two measurements are mandatory in every falsifier, because their absence is what killed v1:

- **L1 check** — does the mechanism's seam have effective rank > 1, or is it 1 bit again?
- **L2 check** — ablate the channel; does ΔCE actually move, or is it decoration?

One inherited principle, and only one: **p7 — perplexity/CE is never truth** (Goodhart). Per
L9 the other seven purity principles manufactured the disease and are discarded. Each family
names which principle it breaks.

## Sibling

`anima-v4` asks the narrower question: *what would make the A⇄G tension itself the thinking?*
(7 mechanisms). This repo does not presume two engines at all.

## Structure

```
anima-v3/
├─ src/              — source code (empty — divergence stage)
├─ state/            — all work artifacts, git-tracked
│  └─ diverge_aliveness_2026-07-16/   — the verbatim divergence + the prompt that produced it
├─ ARCHITECTURE.json — design SSOT (JSON `children` tree, update-in-place)
├─ architecture.html — human viewer for the JSON (run `python3 serve.py`)
├─ HYPOTHESES/       — pre-register → falsify → run → verdict (registry + cards)
├─ tool/             — shared deterministic harness the hypothesis cards run against
└─ CHANGELOG.md      — history (append-only)
```

## Provenance

The divergence was produced by Fable 5 from a brief carrying the v1 autopsy; both the brief and
the verbatim output are preserved under `state/diverge_aliveness_2026-07-16/` as the seed of
record. The live design SSOT is `ARCHITECTURE.json`. The v1 evidence trail (verdicts, hypothesis
cards, convergence records) stays in the `anima` repo — this repo holds pointers, not copies.

## Viewing

```
python3 serve.py        # serve on :8000, open architecture.html
```
