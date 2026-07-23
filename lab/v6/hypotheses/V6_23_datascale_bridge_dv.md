<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_23 — the clean composition DV at data scale: 57MB natural corpus fields it

**origin:** V6_22 proved the bridge-plausible + context-matched DV is sound but INVALID×2 at
4.6MB (BRIDGED n=129 < 300; SEEN instrument 0.531 < 0.70). Both models predicted supply was
the bottleneck. V6_23 = the SAME DV on a larger natural corpus. DIRECTIONAL — cements only via
`core/`+`anima-py`.

## Corpus (on-standard, natural)
`~/anima-weights/en_general.txt` — **57MB natural EN prose** (AP news articles, not lists),
already local (no external fetch needed). Train = first 80% (47.8MB), held-out = last 20%.
EN-first per CLAUDE.md. Same V6_22 DV construction, re-run at 12× scale.

## Supply — 🟢 GREEN (measured 2026-07-23 · `v6_22_build_dv.py`, ANIMA_NATURAL_CORPUS override)
After the full calipers (bridge-plausible + whole-sentence context match + never-co-occur +
surface match + globally unique C′), all three strata hit the CAP:

| stratum | n | vs 4.6MB (V6_22) |
|---|---|---|
| SEEN | 700 | 700 |
| BRIDGED | **700** | 129 → **recovered** |
| UNBRIDGED | 700 | 700 |

The 4.6MB supply-block is gone: the clean composition DV is fieldable at ≥300/stratum at 57MB.
(Builder needed a 2-hop-reach precompute to scale — see #4469; the naive per-candidate
common-neighbour recompute went superlinear.)

## Training (summer, GPU)
`anima-py train --arm ctrl --objective ce_marginal --arch clm --steps 15000` on the 47.8MB
train slice (loss 5.66→1.96, wall 114s, CUDA). Pedestal = 1 step (untrained). More steps than
V6_21's 6000 to give the instrument margin the V6_22 hard distractor needs. Scored with the
engine's own byte-CE (`decode.clm_ce_seq_W`) as the natural-cloze 2AFC.

## RESULT — 🔴 INVALID-INSTRUMENT + INCONCLUSIVE (measured 2026-07-23, n=700/stratum)
Data scale recovered SUPPLY (700/stratum) but **not** the instrument. trained57 / pedestal57 /
collapse-Δ:

| stratum | trained | pedestal | collapse-Δ |
|---|---|---|---|
| SEEN (pos-control) | 0.563 | 0.469 | +0.094 |
| BRIDGED | 0.517 | 0.467 | +0.050 |
| UNBRIDGED | 0.570 | 0.559 | +0.011 |

- **V1 INVALID-INSTRUMENT** — SEEN trained **0.563 < 0.70**. 57MB + 15000 steps did NOT restore
  margin (training did lift SEEN +0.094 over pedestal, but it plateaus at 0.56). ⟹ V6_22's
  instrument failure was **structural to the DV, not a supply/undertraining artifact**: a
  genuinely context-matched distractor leaves the byte-CE readout almost no signal even for
  MEMORISED pairs.
- **Primary INCONCLUSIVE** — D = Δ_BRIDGED − Δ_UNBRIDGED = **+0.039, z≈1.0, 95% CI [−0.035,
  +0.112]** spans 0. At n=700 (well above MDE) there is no significant composition signal, and
  **V6_22's +0.108 hint (n=129) did NOT replicate** — it shrank to +0.039. Raw trained BRIDGED
  0.517 is actually *below* UNBRIDGED 0.570; the small positive DiD rides entirely on a pedestal
  quirk (pedestal UNBRIDGED 0.559 elevated). No honest composition signal survives.

### What this closes: the bottleneck moved from SUPPLY to READOUT SENSITIVITY
Mean CE margins are ~0.008–0.01 nats — at the byte-CE noise floor. The context-matched
swap-2AFC over a byte-LM is **too insensitive to read even memorised pairs**, so it cannot read
composition either. This is not "composition absent" — it is "this readout is instrument-dead
for this contrast." Data scale was necessary (fixed supply) but not sufficient (readout wall).
Consistent with the campaign's standing p9 prior (natural emergence closed), now sharpened: on
a clean on-standard DV, natural composition sits **below the byte-CE 2AFC detection floor**.

### Next (if the lane is reopened) — a more sensitive readout, not a bigger corpus
The corpus axis is now exhausted for THIS readout. A composition signal, if it exists, needs a
readout with margin: a trained linear probe on the trunk's penultimate hidden state at the
C-slot (V6_22 pre-mortem's diagnostic, promoted to primary), or a generation/rank test, not a
whole-sentence byte-CE difference. That is V6_24 — a readout change, engine-native.

## Scope
$0 construction + reused-corpus training (~$0 marginal on owned summer). Single ckpt · single
seed. DIRECTIONAL; the first potentially-on-standard composition reading if it clears the gates
— but TERMINAL only via engine-native `anima-py` port. Anchor-ablation audit (V6_22 pre-mortem)
still required before any PRESENT verdict is trusted.
