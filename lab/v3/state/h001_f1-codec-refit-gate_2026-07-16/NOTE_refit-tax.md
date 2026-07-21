# Refit tax vs the rig budget — order-of-magnitude check (2026-07-16)

Prompted by `salvage.l10-codec-swap-costs-the-embedding`, recovered from the v1 H_9288 lane
during H_001's G-5 protocol reconstruction. Not a verdict — a sizing check that says whether
`rig-budget` as specified is even self-consistent.

## Inputs

| quantity | value | source |
|---|---|---|
| recovery steps after a codec swap | ~20-25k (used 22.5k) | v1 MEASURED (H_9288 re-fire: CPT budget raised to 20-25k, gate-terminated) |
| tokens/step | 8 x 1024 | **`?` representative** — not measured; a typical small-LM batch x seq |
| bytes/token | ~3.5 | `?` representative (same figure the L2 threshold derivation uses) |
| rig budget | ~300 MB/arm, MATCHED | `rig-budget` |

## Result

One refit costs ~645 MB of recovery = **215% of the arm's entire 300 MB budget**, before the
adaptive arm learns anything. k refits scale linearly (k=4 -> 860%). The frozen arm pays 0%.

## What this does and does not establish

- **Does**: the rig as specified (matched ~300 MB/arm, periodic refit) is very likely
  self-inconsistent — the adaptive arm cannot pay the measured recovery tax AND learn the task
  inside the same budget. Any delta measured this way confounds "refit is useless" with "refit
  was never given the budget to pay for itself" (`rig-swap-cost-budget-confound`).
- **Does NOT**: settle the tax's true size for F1. Three transfers are unjustified:
  1. **Change magnitude** — v1's swap was utf-8 -> a wholly new 2-byte alphabet. F1's refit is an
     INCREMENTAL BPE re-merge on drifted data: most merges survive, some boundaries shift. The
     wrong-prior effect should be far smaller, possibly negligible. This is the biggest unknown
     and it cuts in F1's favour.
  2. **Scale** — v1 measured at 303M; the rig is 10M. Recovery cost does not transfer linearly,
     and the embedding mass fraction is much higher at 10M (which cuts against F1).
  3. **tokens/step is `?`** — the headline percentage moves linearly with it.

## What would settle it

A $0-to-cheap pilot measuring the recovery cost of an INCREMENTAL BPE refit (not an alphabet
swap) at 10M scale: refit on drifted data, re-map surviving tokens' embeddings by identity,
fresh-init only the changed ones, and measure steps-to-recover on frozen probes. If incremental
refit recovers in ~hundreds of steps rather than ~20k, `l10` does not bind F1 and the rig is
viable; if it recovers in ~10k+, the F1 twin cannot be made attributable at this budget and the
family needs a different rig (or dies).

Feeds the successor card. Raised to Fable as the R2 anchor question.
