# H_9200 E1 — CE-deleted forward-slot (content-dependent order → CE target)

## Rationale (from the A7 CONTENT signal)
A7 deepen (#3010) showed the 303M trunk's whitened reversal antisymmetry is
**content-dependent** (std 0.17, corr 0.72 with content distance) — order-change
modulates by concept content. This is the first content-bearing latent signal inside
the G1/G6 wall. §4 showed the joint content interaction is NOT decodable from the
frozen rep; E1 tests whether FORCING the trunk to predict an order-swapped token
(content-dependent order target) during training makes the CE minimizer learn a
compositional representation.

## Mechanism (substrate-first, NOT an LLM trick)
- Substrate analogy: cerebellar forward-model error over an ordered trajectory — the
  model must predict the NEXT byte GIVEN a context whose ORDER is the signal. By
  deleting the standard next-byte target at a "composition slot" and replacing it with
  an order-swapped reconstruction target, the gradient can only be reduced if the trunk
  builds a representation where the two concepts' content AND their order jointly
  determine the prediction. Additive/exchangeable parameters cannot reduce this loss
  (DPI escape at the objective level — the target is non-commutative by construction).
- This is distinct from F1/② (residual aux head) and from H_1602 (additive aux): E1
  puts the non-commutative target INTO the main CE next-token slot at marked positions,
  not a side head.

## Construction (training arm in cli/train.py torch REFERENCE → .clm v0.2)
1. **Slot marking.** In a byte sequence, mark "composition slots" — positions where two
   concept tokens a,b were seen adjacent. At those slots, with prob p_swap, replace the
   standard next-byte CE target with the byte that WOULD follow the order-swapped pair
   (b,a) in the corpus (a model-free corpus pass supplies the swap targets).
2. **Loss.** L = CE_nextbyte(standard) over non-slot positions + CE_nextbyte(swapped-order
   target) over slot positions. λ_swap warmup; frozen λ_swap after warmup (pre-registered).
3. **Controls (separate ckpts, frozen):**
   - λ_swap=0 (additive floor baseline).
   - shuffle-target arm (slot target is a random corpus byte, not the order-swapped one).
   - total-order arm (swap target from an additive-sufficient pair where r≈0).
4. **Wire.** torch REFERENCE trainer → clm_reexport.hexa → .clm v0.2 → `anima evaluate --py`
   G0-G6 ladder (== core/decode.py, TERMINAL-eligible). H_9200 frozen kill-contract
   applies (G0 4/5, ≥2/3 seeds, bind-destruction delta, paraphrase invariance, intervention
   sensitivity, held-out leak 0, component-OFF ablation, G6 set-distinct simultaneous).

## Frozen bar (pre-registered BEFORE any GPU run)
- **GREEN-WIRED (G1-eligible)** ⟺ E1 arm lifts frozen G1 (best_distinct≥2 ∧ >max_single)
  on ≥2/3 seeds, AND λ_swap=0/shuffle/total-order control arms do NOT lift G1, AND G0
  stays 4/5, AND no held-out combination leak.
- **WALL (objective still inert)** ⟺ E1 arm does not beat λ_swap=0 on frozen G1 → the
  non-commutative CE target does not move the trunk → G1 wall is terminal for this
  substrate class.
- **DIRECTIONAL** ⟺ partial lift with one control ambiguous.

## $0 pre-GPU gate (must clear before owner GPU-go)
A frozen-rep cheaper-than-retrain check that E1's target is even non-trivially
satisfiable: on the existing 303M ckpt, does the order-swapped target byte differ from
the standard target byte at ≥2/3 marked slots? (If the corpus rarely distinguishes
order at the slot, E1's target is degenerate and the GPU spend is wasted.) This is a
single corpus pass + existing ckpt decode — $0 mini.

## Cost / dependency
- GPU: trunk retrain on owned pool (summer/aiden RTX5070), no rent. ~1 H100-day order
  per H_9131 STEP-1 precedent, but owned-pool so wall-time not dollars.
- Depends on: corpus order-slot marking script ($0) + cli/train.py arm (code) + the $0
  pre-GPU gate above clearing.

## Honest scope
A PASS would be the first objective-side G1 lift on the 303M ByteGPT trunk. A WALL
would terminalize the G1/G6 capability ceiling (every target-side route exhausted,
matching the §4 / STEP-0.5 / sweep convergence). Either is a decisive result worth the
owned-pool GPU.
