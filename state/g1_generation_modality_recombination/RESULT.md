# GENERATION-modality held-out recombination (G1-NEXT-2 reframed by H_6169) — RESULT (2026-07-02)

**TIER: 🟠 DIRECTIONAL-POSITIVE — the GENERATION modality supports held-out compositional recombination.**
torch toy = DIRECTIONAL. aiden $0. Reframed #2: H_6169 showed anima G1 = generation-diversity, so the real
recombination question is "does GENERATION (not classification) support held-out recombination?"

## Setup
Small AR transformer (d128, 3L), synthetic compositional language seq=[A,B,SEP,o1,o2,o3], o=structured
factored rule (o=fn(bucket(A),bucket(B))) vs RANDOM per-(A,B). Train next-token CE on SEEN (A,B) combos,
hold out 25%, measure held-out GENERATION exact-match of the output triple. 6 seeds.

## Result — held-out generation tracks seen ~1:1 for structured, 0 for random
| seed | struct seen | struct held | held/seen | random held |
|---|---|---|---|---|
| 4302 | 0.625 | 0.516 | 0.83 | 0.000 |
| 4303 | 1.000 | 0.969 | 0.97 | 0.000 |
| 4304 | 0.812 | 0.781 | 0.96 | 0.000 |
| 4305 | 0.708 | 0.734 | 1.04 | 0.000 |
| 7, 11 | 0.000 | — (opt non-convergence, excluded) | — | 0.000 |

Across the 4 seeds that trained (seen>0.5): **held/seen ≈ 0.95 (no generalization gap)** — a model that
learns the seen combos GENERATES held-out combos essentially as well. RANDOM target: held=0.000 all seeds
(unlearnable, correct). Robust metric = held/seen ratio (~1.0 struct vs 0 random), NOT abs-convergence.

## Honest caveats (verify-done)
- Small-transformer optimization is FLAKY: 2/6 seeds (7,11) failed to fit even SEEN (seen=0.0) — an
  optimization non-convergence, not a recombination failure; excluded from the ratio. Only 1/6 hit seen=1.0.
- torch toy = DIRECTIONAL (not engine-native). But the qualitative law (struct held≈seen, random held=0) is
  consistent across every seed that trained, and matches H_6167 (classification) + H_6168 (real features distinct).

## Reading — closes reframed #2
The GENERATION modality is NOT the barrier to held-out recombination: when the composition has learnable
structure, a plain AR model generates held-out combos with ~no generalization gap. Therefore anima's
real-text G1=0 (a generation-diversity floor per H_6169) reflects a TRAINING/OBJECTIVE/data issue (the 303M
wasn't trained to elicit compositional generation on structured targets), NOT a generation-modality or
substrate incapability (H_6168: concepts distinctly encoded).

## Provenance
toy_gen_recomb.py (6 seeds, 8000 steps), run.log, result.json. aiden CPU, torch, $0.
