<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_29 — LANE-BUS Step-3: does an EMIT-TIED residual-consumption gate beat its ablations?

**origin:** V6_28 showed discharge is not emergent → it must be ARCHITECTED into the emit gate.
lab-full (Fable primary — 4-arm ablation with A3 free-forget as the decisive p5 control; Sol
concurred, added the WRONG-ADDRESS control and preferred a balanced-accuracy DV + subtractive
addressed-consumption — adopted Fable's NLL DV + multiplicative reset, kept Sol's WRONG-ADDR arm).
DIRECTIONAL.

## Emit ground truth (Fable option b · non-circular · p9 natural)
`emit_t = 1[ argmax(composed_t) == y_{t+1}  AND  argmax(reflex_t) != y_{t+1} ]` — emit exactly
where real tension existed (reflex alone wrong) AND the content lane resolved it (composed right).
Both failure modes of speech (parroting when reflex suffices, guessing when composed is wrong) map
to silence — p5 operationalized. `y_{t+1}` is the actual next byte, external to the gate's inputs,
so the target is NOT a deterministic function of the features (options a/c would be circular).

## Build (reuses trained57 · no new base training)
- **Phase A** ($0 laptop · `v6_29_cache.py`, DONE): frozen feature cache — τ∈R¹⁶ (frozen Gaussian
  256→16 projection of composed−reflex logits), x∈R⁶ (KL both ways, entropies, argmax-agree,
  composed top1−top2 margin), emit labels, sentence ids. **420 sentences, 41,792 positions,
  emit rate 0.419** (pre-reg envelope [0.05,0.60] ✓ — good power).
- **Phase B** (torch, summer · `v6_29_train.py`): tiny recurrent gate heads, 3 seeds, BCE loss.
  Arms: FULL (emit-tied `r=(1−g₋₁)λr₋₁+Uτ`) · A1 (no-consume) · A2 (yoked-random reset) · A3
  (free-forget `f=σ(a'x+b'r)` — same gating expressivity WITHOUT the emit tie) · WRONG-ADDR
  (Sol: consume a norm-matched deranged packet) · B0 (memoryless pedestal). Primary DV = held-out
  per-position NLL. Positive control = synthetic integrate-and-fire (FULL≫A1 or VOID).

## Frozen decision table
| condition | verdict |
|---|---|
| positive control fails | VOID |
| B0−FULL ≤ 0 | memory buys nothing → gate is memoryless, discharge moot |
| A1−FULL z≥3 AND ≥10% of B0→FULL headroom, AND FULL ≥ A3 | 🟢 architected discharge VALIDATED (emit-tie costs nothing vs free-forget) → build real gate |
| consumption helps but A3 > FULL (z≥3) | residual consumed but NOT at emits → p5 emit⇄discharge tie WRONG |
| FULL ≈ A1 (TOST) | discharge doesn't help → drop residual consumption from p5 |

## Pre-mortem (both models)
"Consumption helps" could be the generic fact that gated RNNs beat leaky integrators (pure
expressivity, zero p5 content). A2 (input-independent reset) does not cover it — only **A3
(free-forget)** does: same gating power without the emit tie, so FULL≥A3 is the real p5 verdict,
not A1−FULL. Sol's WRONG-ADDR guards the complementary failure (consumption is refractory/timing,
not content-addressed). `emit_t` is a designer-chosen p5 operationalization + 8-byte reflex proxy
⇒ DIRECTIONAL regardless of outcome; TERMINAL only after the core/+anima-py port, in-vivo.

## RESULT — ⏳ Phase B training on summer (pending)
To be filled from the trainer output.

## Scope
Phase A $0 laptop (DONE). Phase B ~$0 marginal (summer CPU, tiny heads). Single ckpt · reflex =
8B-window proxy. DIRECTIONAL; TERMINAL only via anima-py port.
