# G1 OPERATOR-LEVER on structured-hard tasks — RESULT (2026-07-02, H_6166 follow-on)

**TIER: 🧱 NO OPERATOR LEVER.** aiden CPU $0, torch=DIRECTIONAL. The valid lever test (after H_6166 proved
random-target cheap-gates were unlearnable artifacts): on a STRUCTURED-but-HARD target y=T2[u[fa],v[fb]]
(factored NON-additive rule; K=shared-latent cardinality = difficulty knob), where the plain ADDITIVE trunk
only PARTIALLY generalizes held-out (real headroom), does a multiplicative composition OPERATOR
(hadamard / bilinear) lift held-out recombination >=+0.15 over additive?

## Result — NO (max +0.026 in any headroom regime)
| K (NF=12) | headroom (1-add) | add held | best-mult (bilinear) | Δ mult-add |
|---|---|---|---|---|
| 8  | 0.165 | 0.835 | 0.862 | +0.026 |
| 10 | 0.211 | 0.789 | 0.806 | +0.016 |
| 12 | 0.279 | 0.722 | 0.730 | +0.008 |

(K=6 saturated add≈1.0, no headroom.) hadamard was WORSE than additive at every K. n(Δ>=+0.15) = 0.
(Note: the run's final verdict-print line hit a trivial dict/float reporting bug AFTER all per-K data was
computed and logged — data complete, re-run unnecessary; verdict read directly from logged per-K output.)

## Reading — recombination is TASK-STRUCTURE-bound, not OPERATOR-bound
- When the composition has learnable structure, the plain ADDITIVE trunk ALREADY recombines held-out at
  72-98% (rising as K shrinks = more sharing). The multiplicative operator adds essentially nothing (<+0.03).
- So the whole "which composition operator" campaign (Hadamard / TPR / HRR / bilinear / tensor-product / γ —
  H_1602/H_1816/H_1823/H_1840/H_6164) was chasing the wrong variable: the operator was never the lever.
- Combined with H_6166 (random-target = unlearnable artifact): the complete G1 picture is (1) random/
  structureless target -> nobody recombines (chance ceiling, artifact); (2) structured target -> plain
  additive trunk recombines (72-98%), NO operator lever needed or available.

## Answer to "G1 레버 발견"
There is NO composition-operator lever for held-out recombination. Recombination capability is bound by
whether the TASK has learnable factored structure (real composition does) + adequate training — and a plain
trunk already has it. The prior operator-search wall was doubly mis-framed: random targets (unlearnable) +
operator focus (irrelevant). Follow-on: does the REAL anima trunk recombine held-out REAL structured concept
pairs (H_1218/clm303 structure-aware re-test)? That is the remaining genuine question.

## Provenance
toy_structured_lever.py (K∈{6,8,10,12}, arms add/hadamard/bilinear, 3 seed), run.log. aiden CPU, $0.
