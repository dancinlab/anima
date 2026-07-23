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
⟹ Fable's hub-density pre-mortem does NOT kill supply at this scale.
⚠️ HONESTY: this 3,171 used a permissive sentence splitter that let list-dump blocks
("List of…", year-birth/death rows) count as co-occurrence. Stage-1 tightened the extractor
to PROSE-ONLY (single-line, terminal punctuation, no date-list rows) because list adjacency
is not a relation — that dropped usable supply to **BRIDGED/UNBRIDGED = 396 each, SEEN 500**,
still above MDE. The prose numbers are the honest ones.

## Stage 1 RESULT — 🔴 NO COMPOSITION SIGNAL (prereg row 2 · measured 2026-07-23 · summer)
Engine-native single-size probe. Trained `--arm ctrl --objective ce_marginal --arch clm`
(production ConvMoE, plain CE) 6000 steps on the 3.84MB train slice (loss 5.68→2.04);
pedestal = same config, 1 step (untrained, 5.68). Scored with the engine's own byte-CE
(`decode.clm_ce_seq_W`) as a 2AFC: real held-out sentence vs the same sentence with C
swapped to a freq-matched never-co-occurring entity. **p9-clean: training corpus, the
(A,C) fact, AND the probe sentence are all natural — no hand-built template** (an earlier
templated build was off-standard and was discarded).

| stratum | trained acc | pedestal acc | collapse-Δ |
|---|---|---|---|
| SEEN (pos-control) | 0.756 | 0.576 | +0.180 |
| BRIDGED (composition) | 0.828 | 0.513 | +0.316 |
| UNBRIDGED (similarity floor) | 0.808 | 0.525 | +0.283 |

- **Instrument VALID**: SEEN trained 0.756 ≥ 0.70 pos-control bar; pedestal ≈ chance (0.51–0.58).
- **Training works**: every stratum lifts far above pedestal (collapse-Δ +0.18 to +0.32) —
  the byte-LM genuinely learned to prefer real natural text over entity-swapped text.
- **BUT no composition**: BRIDGED (0.828) vs UNBRIDGED (0.808) gap = **+0.020, SE 0.027,
  z 0.74** → not significant, far below the prereg ≥.05 bar. collapse-Δ gap = +0.033.
  The model prefers the real entity **whether or not a training bridge exists** ⟹ the signal
  is **co-occurrence / topical similarity, not bridge-mediated composition**. Prereg table
  row 2: the DV cannot see the faculty — **redesign the DV before any data-scale spend.**

### Why the swap-2AFC can't isolate composition (the DV defect to fix)
Real-vs-swap is won by LOCAL fluency: a freq-matched but topically-wrong C′ ("…Mercedes and
**Aachen** retired") is simply less probable in context than the real C, and a trained LM
detects that from general co-occurrence stats without ever binding A to C. UNBRIDGED scoring
as high as BRIDGED is the proof. A composition-isolating DV must make the distractor
**bridge-plausible but never-composed** (e.g. C′ that shares A's neighbours yet never meets A),
so only a model that actually traversed the 2-hop path can win. That is the V6_22 redesign.

## Scope
Stage-0 = $0 feasibility (DONE, GREEN). Stage-1 = pool GPU on summer (~$0 marginal, owned
host · DONE, 🔴 no-composition). Single ckpt · single seed · 4.6MB · production ConvMoE trunk.
The data-scale ladder is **NOT warranted yet** — the DV doesn't discriminate composition, so
scaling data would amplify a co-occurrence signal, not answer the question. Next = V6_22
(bridge-plausible distractor DV), not a bigger corpus. DIRECTIONAL; TERMINAL only via
engine-native `anima-py`.
