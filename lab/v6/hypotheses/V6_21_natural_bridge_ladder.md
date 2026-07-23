<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_21 — natural-bridge ladder: does a composition DV track the measured pair-repetition curve?

**origin:** lab-full divergence (Fable 5 primary · Sol answer was an incomplete exec-trace,
no usable final synthesis captured → Fable adopted, no dissent to record). Frontier fork
after H_9931 (δ=8 UNDECIDABLE, drill-only) + p9 hardening (synthetic = instrument check,
natural corpus = standard). DIRECTIONAL design — cements only via `core/` + `anima-py`.

## The fork (Fable's ranking, adopted)
- **Track B FIRST (this card)** — put a MODEL in the loop on the NATURAL axis. Every
  natural number so far (V6_13/14, relation ladder) is a corpus property with no model;
  every model number is synthetic. The empty cell is their intersection. V6_14 already
  showed the relevant scale is ~16–130MB (1–2 orders), not 10¹² tokens — so this is a
  pool-sized bet, not an unaffordable abstraction.
- **Track C SECOND** — port the rotation/operator crack to `core/`+`anima-py`. Value
  dropped under p9 (earns TERMINAL on a drill instrument), but the readout becomes canonical
  and any natural campaign needs it. Do it when a pool trip is scheduled anyway.
- **Track A PARKED (not run)** — H_9931's δ=8 extrapolation question is drill-only either
  way; fold into C's port decision if/when C fires. Reason written here, not dropped.

## Question
Train the same model on natural EN prose at sizes spanning V6_14's repetition regimes; test
whether it prefers entity pairs **attested in held-out natural text** over never-attested
distractors — and whether that preference **requires a 2-hop bridge in the training slice**.
Ground truth is the corpus itself (the pair really meets in text the model never saw) —
on-standard, no hand-built drill.

## Strata (per training slice)
- **SEEN** — A,C co-occur in the training slice (positive control).
- **BRIDGED** — A,C never meet in training, but some B meets both (composition stratum).
- **UNBRIDGED** — A,C never meet in training and share no bridge B (similarity floor).

## DV
2AFC accuracy: (A,C) attested-in-heldout vs (A,C′) frequency-matched never-co-occurring
distractor. `anima-py evaluate --gen-ctx-2afc`. Read as collapse-Δ vs controls; chance
derived per realized split, not assumed 0.5. ≥2 phrasing templates per item (bakes G0
natural-form gate into the DV).

## Controls (≥2, named)
1. **Pedestal** — untrained/shuffled-weights on identical eval → realized chance floor.
2. **Positive control** — SEEN must clear preregistered ≥0.70 at every size, else INVALID.
3. **Exposure-matched repeated-small arm** — H_9931 lesson weaponized: at 16MB, an arm
   trained on the 4.8MB slice repeated to 16MB total bytes (same token exposure, no new
   pairs). Composition tracking TRUE size but not repeated-small ⟹ lever = fresh pair
   repetition, not tokens seen.
4. **UNBRIDGED stratum** — the discriminator: signal without a bridge = embedding
   similarity, not binding.

## Prereg decision table
| Result | Reading |
|---|---|
| BRIDGED Δ > UNBRIDGED Δ (gap ≥ .05, CI excl 0) AND BRIDGED rises with size; repeated-small flat | natural composition supply USABLE, lever = pair repetition → escalate one 303M point + port DV as `anima-py` flag (C fires) |
| both strata above chance, no BRIDGED>UNBRIDGED gap | signal = co-occurrence similarity, not composition — DV can't see faculty; redesign before scale spend |
| all unseen strata at chance at all sizes, pos-control green, repeated-small flat | V6_14's repetition extrapolation NOT sufficient at this model scale — directional negative on "data quantity alone", NOT closed (amplifier caveat) |
| pos-control at chance anywhere | INVALID — fix training/instrument first |

## Pre-mortem (Fable) — the load-bearing risk
BRIDGED/UNBRIDGED confounded by **hub density**: bridged pairs sit in denser neighborhoods
(bridges are hubs) → BRIDGED beats UNBRIDGED by topical proximity, faking composition. Prereg
mitigation: match strata on A/C mention counts AND neighbor degree; only a gap surviving
degree-matching is green. **If degree-matching kills item supply below the MDE, that is
itself a result** — natural text at this scale can't pose the composition question cleanly →
redirect before any GPU.

## Stage 0 — $0 FEASIBILITY GATE (this is what runs first · `v6_21_natural_bridge_supply.py`)
Before any GPU: on the available 4.6MB natural corpus, mine the three strata from a disjoint
held-out slice against a training slice, apply degree-matching, and report item supply per
stratum vs MDE (n≥300/stratum). GREEN gate = BRIDGED and UNBRIDGED both survive
degree-matching at n≥300 → construct the eval + dispatch the training ladder. RED gate =
supply below MDE → the natural corpus at this scale can't pose the question; report and
redirect (do NOT spend GPU).

## Stage 0 RESULT — 🟢 GREEN (measured 2026-07-23 · `v6_21_natural_bridge_supply.py`)
On the 4.81MB natural corpus (train 3.84MB / held-out 0.96MB, disjoint; 29,322 entities,
150,188 training pairs):

| stratum | raw held-out pairs | distractor-feasible |
|---|---|---|
| SEEN (pos-control) | 11,727 | 11,727 |
| BRIDGED (composition) | 7,694 | 7,694 |
| UNBRIDGED (similarity floor) | 6,841 | 6,841 |

**Degree+freq-matched fieldable n = 3,171/stratum** (BRIDGED vs UNBRIDGED, per density
signature bin) — **10× the MDE floor (300)**. SEEN positive-control supply = 11,727.
⟹ Fable's hub-density pre-mortem does NOT kill supply at this scale: even after removing the
confound, the natural axis poses the composition question with ample n. **Eval is
constructible; training ladder warranted.**

## Stage 1 (NEXT) — engine-native single-size probe before the full ladder
Cheapest decisive test (fluency-pregate discipline): build the 2AFC eval from the matched
strata, train one small model on the 3.84MB training slice (pool ~$10), run
`anima-py evaluate` → is BRIDGED Δ > UNBRIDGED Δ above the pedestal, with SEEN ≥ 0.70
positive-control? If it fails at one size, the size ladder is moot (cheap kill). If it
passes, fetch a larger EN dump (Simple English Wikipedia ~250MB) and run Fable's
4.8/16/48/130MB ladder + the repeated-small exposure-matched arm.

## Scope
Stage-0 = $0 laptop numpy/regex on 4.6MB corpus (DONE, GREEN). Stage-1 = pool GPU (~$10,
autonomous per a_fire_autonomous). Full ladder needs a larger EN dump, fetched only if
Stage-1 passes. DIRECTIONAL; faculty claim earns TERMINAL only via engine-native `anima-py`.
